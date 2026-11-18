
import discord

MEDALS = ("🥇", "🥈", "🥉")


def _name(player: dict) -> str:
    user_id = player.get("discord_id")

    if user_id:
        return f"<@{user_id}>"

    return player.get("username") or "Unknown"


def _pp(player: dict) -> float:
    return float(player.get("total_pp", 0) or 0)


def _wpm(player: dict) -> float:
    return float(player.get("avg_wpm", 0) or 0)


def create_top_embed(players: list) -> discord.Embed:
    now = discord.utils.utcnow()

    embed = discord.Embed(
        title="Daily Competition | All-Time Rankings",
        description=f"Top daily performers  ·  <t:{int(now.timestamp())}:D>",
        color=discord.Color.from_rgb(240, 185, 11),
    )

    if not players:
        embed.description += "\n\nNo players have recorded scores yet."
        embed.set_footer(text="VIT Typing Club")
        return embed

    podium = "\n".join(
        f"{MEDALS[i]}  **{_name(p)}**  ·  "
        f"{_pp(p):,.2f} PP  ·  {_wpm(p):.2f} WPM"
        for i, p in enumerate(players[:3])
    )

    embed.add_field(
        name="\u200b",
        value=podium,
        inline=False,
    )

    if len(players) > 3:
        rest = "\n".join(
            f"`{rank}`  {_name(p)}  ·  "
            f"{_pp(p):,.2f} PP  ·  {_wpm(p):.2f} WPM"
            for rank, p in enumerate(players[3:10], start=4)
        )

        embed.add_field(
            name="\u200b",
            value=rest,
            inline=False,
        )

    embed.set_footer(
        text=f"VIT Typing Club  ·  {len(players)} players"
    )

    return embed
