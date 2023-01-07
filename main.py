import datetime
import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

initial_extensions = ["cogs.basic", "cogs.music", "cogs.web"]

# Initialize variables
try:
    # Discord
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    STARTUP_MESSAGE = " B0B has awoken! logged in as "
    BOT_PREFIX = "0"
    DISCORD_STATUS = discord.Game(
        "w̶̡͌i̷͉̚t̷̘̎h̶̙̀ ̸̙͊ḧ̶̯́i̴̳̾ṡ̷͚ ̷̾͜f̷͈͛r̸̬̾i̴̢̎e̷̠͒ñ̶̥d̵͜͝s̸̮̆"
    )
    HELP_MESSAGE = " TODO "

    # Advanced settings
    BOT_VERSION = "2.0"
    TIME_FORMAT = datetime.datetime.strptime(time.asctime(time.localtime()), "%c")

    # Intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True

except Exception as e:
    print(e)


class B0B(commands.Bot):
    user: discord.ClientUser
    bot_app_info: discord.AppInfo

    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(BOT_PREFIX),
            case_insensitive=True,
            intents=intents,
        )

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    async def on_ready(self) -> None:
        print(STARTUP_MESSAGE + str(self.user))
        print(f"Version: {BOT_VERSION}")
        await self.change_presence(activity=DISCORD_STATUS)
        await self.initialize_cogs()

    async def setup_hook(self) -> None:
        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id

    async def initialize_cogs(self) -> None:
        for ext in initial_extensions:
            try:
                await self.load_extension(ext)
                print(f"Successfully loaded extension {ext}")
            except Exception as error:
                print(f"Failed to load extension {ext} due to {error}")

    async def on_message(self, message) -> None:
        # if message is not from itself
        if message.author == self.user:
            return
        # listen for commands
        await bot.process_commands(message)

    # Error Handling
    async def on_command_error(self, ctx, error: Exception) -> None:
        await ctx.reply(error, ephemeral=True)
        print(error)


bot = B0B()


@bot.hybrid_command(with_app_command=True, description="Pings B0B")
async def ping(ctx) -> None:
    """🏓 Pings B0B"""
    await ctx.reply("pong.")


@bot.tree.context_menu()
async def say(interaction: discord.Interaction, message: discord.Message) -> None:
    await interaction.response.send_message(message.content)


@bot.hybrid_command(with_app_command=True, description="B0B's website")
async def github(ctx) -> None:
    """🏠 B0B's website"""
    await ctx.send("https://github.com/datgai/DiscordB0B")


# TODO:buggy sync
@bot.command()
@commands.is_owner()
async def sync_command_tree(ctx) -> None:
    """🔄Syncs the command Tree"""
    await bot.tree.sync(guild = ctx.guild)
    print(f"Command tree synced at {ctx.guild}")
    await ctx.reply("Command tree synced")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
