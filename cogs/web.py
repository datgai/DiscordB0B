import json
import urllib

import bs4 as bs
import discord
from discord.ext import commands

# Variabals
header = {"User-Agent": "Mozilla"}


class Web(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    def connectParse(self, link: str) -> str:
        req = urllib.request.Request(url=link, headers=header)
        print("Connecting")
        resp = urllib.request.urlopen(req)
        print("Opening")
        parsed = bs.BeautifulSoup(resp, "html.parser")
        print("Parsing")
        return parsed

    @commands.hybrid_command(
        with_app_command=True,
        description="📚 Does a Wikipedia search",
    )
    async def wiki(self, ctx, search) -> None:
        search.replace(" ", "_")
        await ctx.send(f"https://en.wikipedia.org/wiki/{search}")

    @commands.hybrid_command(
        with_app_command=True,
        description="📷 Reddit",
    )
    async def reddit(
        self, ctx, subreddit: str, sort: str = "hot", number: int = 1
    ) -> None:
        try:
            soup = self.connectParse(f"https://www.reddit.com/r/{subreddit}/{sort}/")
        except Exception as e:
            print(e)
            await ctx.send(f"Unable to find Subreddit {subreddit}. Beep.")
        images = soup.find_all("img", {"id": "post-image"})
        print(images)

        if number >= len(images):
            for image in range(number):
                await ctx.send(images[image].get("src"))
        else:
            await ctx.send("Unable  to send that many requests. Beep.")

    @commands.hybrid_command(
        with_app_command=True,
        description="🎓 Hmm Quotes...",
    )
    async def quotes(self, ctx, mode: str = "random") -> None:

        soup = self.connectParse(f"https://zenquotes.io/api/{mode}")
        quotes = soup.findAll(text=True)
        quote = json.loads(str(quotes)[2:-2].encode("unicode_escape"))
        mbed = discord.Embed(
            title=f"Quotes : {mode}",
            description=f"{quote[0]['q']} \n - {quote[0]['a']}",
        )
        await ctx.send(embed=mbed)

    @commands.hybrid_command(
        aliases=["meow"],
        with_app_command=True,
        description="🐈 Meowww",
    )
    async def cat(self, ctx) -> None:
        soup = self.connectParse("https://api.thecatapi.com/v1/images/search")
        print("Parsing")
        cat = soup.findAll(text=True)
        catjson = json.loads(str(cat)[3:-3])
        catlink = catjson["url"]
        await ctx.send(catlink)

    @commands.hybrid_command(
        aliases=["bark", "woof"],
        with_app_command=True,
        description="🐕 Woofffff",
    )
    async def dog(self, ctx) -> None:
        soup = self.connectParse("https://api.thedogapi.com/v1/images/search")
        dog = soup.findAll(text=True)
        dogjson = json.loads(str(dog)[3:-3])
        doglink = dogjson["url"]
        await ctx.send(doglink)

    @commands.hybrid_command(
        aliases=["waifu"],
        with_app_command=True,
        description= "❤️ キャットガールズは最高です",
    )
    async def neko(self, ctx, mode: str = "neko") -> None:
        soup = self.connectParse(f"https://nekos.life/api/v2/img/{mode}")
        neko = soup.findAll(text=True)
        nekojson = json.loads(str(neko)[2:-4])
        try:
            nekolink = nekojson["url"]
            await ctx.send(nekolink)
        except KeyError:
            await ctx.send("Tag doesn't exist. Beep.")

    @commands.hybrid_command(
        with_app_command=True,
        description="💪 Tells you a fact about someone",
    )
    async def facts(self, ctx, person: str = "B0B") -> None:
        soup = self.connectParse("https://api.chucknorris.io/jokes/random")
        dude = soup.findAll(text=True)
        print(str(dude)[2:-2])
        dudejson = json.loads(str(dude)[2:-2].encode("unicode_escape"))
        fact = dudejson["value"].replace("Chuck Norris", person)
        print(fact)
        await ctx.send(fact)


async def setup(bot):
    await bot.add_cog(Web(bot))
