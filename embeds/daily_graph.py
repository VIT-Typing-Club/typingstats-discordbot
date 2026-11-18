import io
import discord
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime


def create_daily_graph_embed(user, scores):

    if not scores:
        return None, None

    dates = [score["created_at"] for score in scores]
    wpms = [score["wpm"] for score in scores]

    total_pp = sum(score["pp"] or 0 for score in scores)

    avg_wpm = sum(wpms) / len(wpms)
    best_wpm = max(wpms)

    accuracies = [
        score["accuracy"]
        for score in scores
        if score["accuracy"] is not None
    ]

    avg_accuracy = (
        sum(accuracies) / len(accuracies)
        if accuracies else 0
    )

    plt.style.use("dark_background")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        dates,
        wpms,
        marker="o",
        linewidth=2,
        markersize=5,
        label="WPM"
    )

    ax.set_title("Daily WPM Progression", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Words Per Minute")

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%d %b")
    )

    ax.grid(alpha=0.2)
    ax.legend()

    fig.autofmt_xdate()
    fig.tight_layout()

    # Save graph to memory
    image_buffer = io.BytesIO()

    fig.savefig(
        image_buffer,
        format="png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)
    image_buffer.seek(0)

    embed = discord.Embed(
        title="Daily Performance Stats",
        description=f"User: **{user.display_name}**",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="Total PP",
        value=f"**{total_pp:,.2f}**",
        inline=True
    )

    embed.add_field(
        name="Average WPM",
        value=f"**{avg_wpm:.2f}**",
        inline=True
    )

    embed.add_field(
        name="Personal Best",
        value=f"**{best_wpm:.2f} WPM**",
        inline=True
    )

    embed.add_field(
        name="Average Accuracy",
        value=f"**{(avg_accuracy*100):.2f}%**",
        inline=True
    )

    embed.add_field(
        name="Total Scores",
        value=f"**{len(scores)}**",
        inline=True
    )

    embed.set_image(url="attachment://daily_graph.png")

    embed.set_footer(
        text="VIT Typing Club • Last 30 days"
    )

    file = discord.File(
        image_buffer,
        filename="daily_graph.png"
    )

    return embed, file
