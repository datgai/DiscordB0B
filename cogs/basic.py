from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot


async def setup(bot):
    await bot.add_cog(Basic(bot))
