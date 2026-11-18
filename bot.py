import logging

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands

from config import DISCORD_TOKEN, TIMEZONE
from embeds.daily_leaderboard import create_daily_leaderboard_embed
from embeds.daily_quote import create_daily_quote_embed
from embeds.daily_graph import create_daily_graph_embed
from embeds.help import create_help_embed
from embeds.top import create_top_embed
from embeds.typegg_sync import create_typegg_sync_embed
from scheduler.jobs import post_daily_quote, post_final_leaderboard
from services.typegg_stats import get_user_daily_scores
from services.typingclub_api import get_daily_data
from services.typegg_sync import sync_typegg_scores
from services.typegg_stats import get_top_players
from db_connect import Database

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
log = logging.getLogger("typingclub")

intents = discord.Intents.default()
intents.message_content = True


class TypingClubBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents)
        self.scheduler = AsyncIOScheduler(timezone=TIMEZONE)
        self.db = Database()

    async def setup_hook(self):
        """Runs once before the bot connects, so jobs are never registered twice."""
        await self.db.connect()
        self._register_jobs()
        self.scheduler.start()

        for job in self.scheduler.get_jobs():
            log.info("Scheduled %s -> next run %s", job.id, job.next_run_time)

    def _register_jobs(self):
        jobs = (
            # (function, job id, hour, minute, misfire grace in seconds)
            (post_final_leaderboard, "daily_final_leaderboard", 5, 32, 120),
            (post_daily_quote, "daily_quote", 5, 40, 300),
        )

        for func, job_id, hour, minute, grace in jobs:
            self.scheduler.add_job(
                func,
                trigger=CronTrigger(hour=hour, minute=minute, timezone=TIMEZONE),
                args=[self],
                id=job_id,
                replace_existing=True,
                max_instances=1,
                coalesce=True,
                misfire_grace_time=grace,
            )

    async def on_ready(self):
        log.info("Logged in as %s", self.user)

    async def close(self):
        self.scheduler.shutdown(wait=False)
        await self.db.close()
        await super().close()

bot = TypingClubBot()


async def _send_daily_embed(ctx: commands.Context, build_embed):
    """Fetch today's data and post the embed produced by `build_embed(data)`."""
    data = await get_daily_data()

    if data is None:
        await ctx.send("Could not fetch today's competition data.")
        return

    await ctx.send(embed=build_embed(data))


@bot.command(name="h")
async def help_command(ctx: commands.Context):
    """Show available TypingClub commands."""

    await ctx.send(embed=create_help_embed())

@bot.command(name="daily")
async def daily(ctx: commands.Context):
    """Show today's quote."""
    await _send_daily_embed(ctx, lambda data: create_daily_quote_embed(data["quote"]))
 
 
@bot.command(name="leaderboard", aliases=["lb"])
async def leaderboard(ctx: commands.Context):
    """Show today's leaderboard."""
    await _send_daily_embed(ctx, create_daily_leaderboard_embed)


@bot.command(name="daily_graph", aliases=["dg"])
async def daily_graph(
    ctx: commands.Context,
    arg1: str = None,
    arg2: str = None
):
    """Show daily performance graph for user."""

    days = None
    target = ctx.author

    args = [arg for arg in (arg1, arg2) if arg is not None]

    for arg in args:
        if arg.lower() == "all":
            days = None
            continue

        try:
            parsed_days = int(arg)

            if parsed_days <= 0:
                await ctx.send("Please provide a positive number of days.")
                return

            days = parsed_days
            continue

        except ValueError:
            pass

        try:
            target = await commands.MemberConverter().convert(ctx, arg)

        except commands.MemberNotFound:
            await ctx.send(f"Couldn't find a Discord member matching `{arg}`.")
            return

    scores = await get_user_daily_scores(
        ctx.bot.db,
        str(target.id),
        days=days
    )

    if not scores:
        period = f"in the last {days} days" if days else "all time"

        await ctx.send(
            f"{target.display_name} has no recorded typing scores {period}."
        )
        return

    embed, file = create_daily_graph_embed(target, scores)

    embed.set_footer(
        text=f"VIT Typing Club • {'All Time' if days is None else f'Last {days} Days'}"
    )

    await ctx.send(embed=embed, file=file)

@bot.command(name="top")
async def top(ctx: commands.Context, limit: int = 10):
    """Show the top Daily players."""

    if limit < 1 or limit > 25:
        await ctx.send("Please choose a limit between 1 and 25.")
        return

    players = await get_top_players(ctx.bot.db, limit)

    if not players:
        await ctx.send("No typing scores have been recorded yet!")
        return

    embed = create_top_embed(players)

    await ctx.send(embed=embed)

@bot.command(name="sync")
async def sync(ctx: commands.Context):
    """Manually sync daily TypeGG scores."""
    result = await sync_typegg_scores(str(ctx.author.id))
    embed = create_typegg_sync_embed(result)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN is not set.")

    bot.run(DISCORD_TOKEN)