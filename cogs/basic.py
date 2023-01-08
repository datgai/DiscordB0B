import discord
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(pass_context=True)
    async def poll(self, ctx, question, *options: str):
        "🗳️ | Creates  a poll"
        if len(options) <= 1:
            mbed = discord.Embed(
                title="Invalid format.",
                description=" It is : poll 'question' 'option1' 'option2'",
                colour=discord.Colour.red(),
            )
            await ctx.send(embed=mbed)

        elif len(options) > 10:
            mbed = discord.Embed(
                title="Too many options",
                description="Only up to 10 options.Beep",
                colour=discord.Colour.red(),
            )
            await ctx.send(embed=mbed)

        reactions = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]

        description = []

        # creates the poll embed
        for index, option in enumerate(options):
            description += f"\n {reactions[index]}    :    {option}\n"
        poll = discord.Embed(
            title=question,
            description="".join(description),
            colour=discord.Colour.green(),
        )
        react_message = await ctx.send(embed=poll)
        # add reaction to embed
        for reaction in reactions[: len(options)]:
            await react_message.add_reaction(reaction)


async def setup(bot):
    await bot.add_cog(Basic(bot))
