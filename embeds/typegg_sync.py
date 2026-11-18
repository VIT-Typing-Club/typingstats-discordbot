import discord

def create_typegg_sync_embed(result: dict) -> discord.Embed:
    success = result["success"]
    status = result.get("status")
    message = result["message"]

    embed = discord.Embed(
        title="Daily Score Sync",
        description=message,
        color=(
            discord.Color.green()
            if success
            else discord.Color.red()
        )
    )

    if status is not None:
        embed.set_footer(
            text=f"VIT Typing Club  ·  HTTP {status}"
        )
    else:
        embed.set_footer(text="VIT Typing Club")

    return embed
