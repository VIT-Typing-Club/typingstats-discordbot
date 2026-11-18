import discord

def create_help_embed():
    embed = discord.Embed(
        title="VIT Typing Club | Command Help",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="1. -daily",
        value="View today's daily typing quote and its details.",
        inline=False
    )

    embed.add_field(
        name="2. -leaderboard / -lb",
        value="View today's typing competition leaderboard.",
        inline=False
    )

    embed.add_field(
        name="3. -daily_graph / -dg",
        value=(
            "View daily typing performance statistics and WPM progression.\n"
            "**Usage:**\n"
            "`-dg` — All-time personal stats\n"
            "`-dg 30` — Last 30 days\n"
            "`-dg @user` — Another user's stats\n"
            "`-dg 30 @user` — Another user's last 30 days"
        ),
        inline=False
    )

    embed.set_footer(
        text="VIT Typing Club • Happy Typing!"
    )

    return embed