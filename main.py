import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands
from discord.ui import Select, View

app = Flask("")


@app.route("/")
def home():
    return "Bot Online!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)


class RulesSelect(Select):

    def __init__(self):
        options = [
            discord.SelectOption(
                label="Server Rules",
                value="server_rules",
                description="Click to view the server rules",
                emoji="📜",
            ),
            discord.SelectOption(
                label="Close",
                value="close_rules",
                description="Close the selection",
                emoji="❌",
            ),
        ]
        super().__init__(
            placeholder="Select an option for...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "server_rules":
            rules_embed = discord.Embed(
                title="📜 SERVER RULES",
                description=(
                    "Welcome to our server! To ensure a safe, friendly, and"
                    " enjoyable environment for everyone, please read and"
                    " follow our community guidelines below."
                ),
                color=discord.Color.from_rgb(88, 101, 242),
            )

            rules_embed.add_field(
                name="1️⃣ Mutual Respect",
                value=(
                    "Harassment, hate speech, toxicity, excessive profanity, or"
                    " insults towards any member will not be tolerated."
                ),
                inline=False,
            )
            rules_embed.add_field(
                name="2️⃣ No Spam or Self-Promotion",
                value=(
                    "Advertising other servers, posting referral links, or"
                    " sending unsolicited DMs to members is strictly"
                    " prohibited."
                ),
                inline=False,
            )
            rules_embed.add_field(
                name="3️⃣ Use Appropriate Channels",
                value=(
                    "Please keep discussions relevant to the channel topic"
                    " (e.g., use `#bot-commands` for bot interactions)."
                ),
                inline=False,
            )
            rules_embed.add_field(
                name="4️⃣ Privacy & Safety",
                value=(
                    "Do not share personal information (yours or others'),"
                    " including real names, addresses, phone numbers, or private"
                    " media."
                ),
                inline=False,
            )
            rules_embed.add_field(
                name="5️⃣ Staff Authority",
                value=(
                    "Moderators reserve the right to warn, mute, kick, or ban"
                    " anyone violating the rules. If you have questions, please"
                    " open a support ticket."
                ),
                inline=False,
            )

            rules_embed.set_footer(
                text=(
                    "Violating the rules may result in moderation action. •"
                    " Last updated: 2026"
                )
            )

            await interaction.response.send_message(
                embed=rules_embed, ephemeral=True
            )

        elif self.values[0] == "close_rules":
            await interaction.response.send_message(
                "Selection closed.", ephemeral=True
            )


class RulesView(View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RulesSelect())


@bot.event
async def on_ready():
    print(f"Done {bot.user.name} ({bot.user.id})")


@bot.command(name="rules")
async def rules_command(ctx):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    main_embed = discord.Embed(
        title="📜 SERVER RULES",
        description="Select an option for server rules below!",
        color=discord.Color.from_rgb(88, 101, 242),
    )
    main_embed.set_footer(text="Select an option from the menu below.")

    await ctx.send(embed=main_embed, view=RulesView())


bot.run(
    "MTU1NzYxMDgxOTg2MzMyMjYyNA.G8cYvm.hhcZ6v6htX503QrB 0p1HRRWnnbgTzUzV5ESYc4"
)
