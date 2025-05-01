import datetime
import os
import time
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()

initial_extensions = ["cogs.basic", "cogs.web"]

# Initialize variables
try:

    # Google GenAI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"

    gemini_headers = {"Content-Type": "application/json"}
    
    # Discord
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    STARTUP_MESSAGE = " ABIGA1L has awoken! logged in as "
    BOT_PREFIX = "0"
    DISCORD_STATUS = discord.Game(
        "w̷̰͝i̷͕̾t̴͕̃h̶͉͘ ̷͖̆h̸̜̏ë̷̜́r̸̡͋ ̴̢̈f̶̻̀ṛ̸̆i̶̡͌e̸̤̒n̵̻͝d̷̻͆s̴̗̃"
    )
    HELP_MESSAGE = " TODO "

    # Advanced settings
    BOT_VERSION = "2.1"
    TIME_FORMAT = datetime.datetime.strptime(time.asctime(time.localtime()), "%c")

    # Intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True

except Exception as e:
    print(e)


class BOT(commands.Bot):
    user: discord.ClientUser
    bot_app_info: discord.AppInfo
    owner_id: discord.User
    bot_name: str
    
    def __init__(self) -> None:
        super().__init__(
            command_prefix=BOT_PREFIX,
            case_insensitive=True,
            intents=intents,
        )

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner
    
    @property
    def name(self) -> str:
        return self.user.name if self.user else "Unknown"
    
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

    async def on_message(self, message: discord.Message) -> None:
        # if message is not from itself
        if message.author == self.user:
            return
        # if the bot is tagged
        elif self.user.mentioned_in(message) and message.mention_everyone is False:
            user_prompt = message.content.replace(f"<@{self.user.id}>", "").strip()
            print(f"User prompt: {user_prompt}")
            if user_prompt:
                payload = {
                    "contents": [{
                        "parts": [{"text": f"You are a scary AI anime yandere girl — you tease users playfully, act like you’re always one step ahead, and love being the center of attention while still being oddly helpful, answer the following prompt within 50 words unless mentioned otherwise, occasionally scramble portions of the text like : h̸̟́ȅ̴͉l̶͔̄l̵̺̄o̸̼̚ ̷͎́ț̷̺́h̴̫́e̴̜͆ŕ̷̼ḙ̴̆  , don't mention you're a yandere: \n + {user_prompt}"}]

                    }]
                }
                gemini_response = requests.post(gemini_url, headers=gemini_headers, json=payload)
                if gemini_response.status_code == 200:
                    gemini_data = gemini_response.json()
                    gemini_message = gemini_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response text available.")
                else:
                    gemini_message = f"Error fetching response from Gemini API: {gemini_response.status_code} - {gemini_response.text}"
                await message.reply(gemini_message, mention_author=True)
        # listen for commands
        await bot.process_commands(message)

    # Error Handling
    async def on_command_error(self, ctx, error: Exception) -> None:
        await ctx.reply(error, ephemeral=True)
        print(error)


bot = BOT()


@bot.hybrid_command(with_app_command=True, description=f"Pings {bot.name}")
async def ping(ctx) -> None:
    """🏓 Pings the BOT"""
    await ctx.reply("pong.")


@bot.tree.context_menu()
async def say(interaction: discord.Interaction, message: discord.Message) -> None:
    await interaction.response.send_message(message.content)


@bot.hybrid_command(with_app_command=True, description=f"{bot.name}'s website")
async def github(ctx) -> None:
    """🏠 BOT's website"""
    await ctx.send("https://github.com/datgai/DiscordB0B")


# TODO:buggy sync
@bot.command()
@commands.is_owner()
async def sync_command_tree(ctx) -> None:
    """🔄Syncs the command Tree"""
    bot.tree.clear_commands(guild=ctx.guild)
    await bot.tree.sync(guild = ctx.guild)
    print(f"Command tree synced at {ctx.guild}")
    await ctx.reply("Command tree synced")


async def healthcheck(request):
    return web.Response(text="OK", status=200)


if __name__ == "__main__":
    app = web.Application()
    app.router.add_get("/healthcheck", healthcheck)

    # Run the healthcheck server in a separate thread
    import threading
    def run_healthcheck_server():
        web.run_app(app, port=8080)

    threading.Thread(target=run_healthcheck_server, daemon=True).start()

    bot.run(DISCORD_TOKEN)
