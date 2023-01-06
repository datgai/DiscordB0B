from discord.ext import commands


class basic(commands.Cog):
    def __init__(self,bot):
        self.client = bot


async def setup(bot):
    await bot.add_cog(basic(bot))