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

    # TODO: handle spaces
    @commands.hybrid_command(
        with_app_command=True,
        description="B0B google something for you ...",
    )
    async def google(self, ctx, search: str) -> None:
        """🤓 Does a search"""
        req = urllib.request.Request(
            url=f"https://www.google.com/search?q={search}&num=5", headers=header
        )
        print("Connecting")
        resp = urllib.request.urlopen(req)
        print("Opening")
        soup = bs.BeautifulSoup(resp, "html.parser")
        print("Parsing")
        links = soup.find_all("a")

        for link in links:
            link_href = link.get("href")
            if "url?q=" in link_href and not "webcache" in link_href:
                title = link.find_all("h3")
                if len(title) > 0:
                    await ctx.send(title[0].getText())
                    await ctx.send(link.get("href").split("?q=")[1].split("&sa=U")[0])

    @commands.hybrid_command(
        with_app_command=True,
        description="B0B wiki something for you ...",
    )
    async def wiki(self, ctx, search) -> None:
        """📚 Does a Wikipedia search"""
        search.replace(" ", "_")
        await ctx.send(f"https://en.wikipedia.org/wiki/{search}")

    @commands.hybrid_command(
        with_app_command=True,
        description="B0B send you pictures from reddit...",
    )
    async def reddit(
        self, ctx, subreddit: str, sort: str = "hot", number: int = 1
    ) -> None:
        "📷 Reddit"
        try:
            req = urllib.request.Request(
                url=f"https://www.reddit.com/r/{subreddit}/{sort}/", headers=header
            )
        except Exception as e:
            print(e)
            await ctx.send(f"Unable to find Subreddit {subreddit}. Beep.")
        print("Connecting")
        resp = urllib.request.urlopen(req)
        print("Opening")
        soup = bs.BeautifulSoup(resp, "html.parser")
        print("Parsing")
        images = soup.find_all("img", {"alt": "Post image"})
        print(images)

        if number >= len(images):
            for image in range(number):
                await ctx.send(images[image].get("src"))
        else:
            await ctx.send("Unable  to send that many requests. Beep.")

    @commands.hybrid_command(
        with_app_command=True,
        description="B0B will grant wisdom",
    )
    async def quotes(self, ctx, mode: str = "random") -> None:
        "🎓 Hmm Quotes..."
        req = urllib.request.Request(
            url=f"https://zenquotes.io/api/{mode}", headers=header
        )
        print("Connecting")
        resp = urllib.request.urlopen(req)
        print("Opening")
        soup = bs.BeautifulSoup(resp, "html.parser")
        print("Parsing")
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
        description="B0B send cat pics",
    )
    async def cat(self, ctx) -> None:
        "🐈 Meowww"

        req = urllib.request.Request(
            url=f"https://api.thecatapi.com/v1/images/search", headers=header
        )
        print("Connecting")
        resp = urllib.request.urlopen(req)
        print("Opening")
        soup = bs.BeautifulSoup(resp, "html.parser")
        print("Parsing")
        cat = soup.findAll(text=True)
        catjson = json.loads(str(cat)[3:-3])
        catlink = catjson["url"]
        await ctx.send(catlink)

    @commands.hybrid_command(
        aliases=["bark", "woof"],
        with_app_command=True,
        description="B0B send dog pics",
    )
    async def dog(self, ctx) -> None:
        "🐕 Woofffff"

        req = urllib.request.Request(
            url=f"https://api.thedogapi.com/v1/images/search", headers=header
        )
        print("Connecting")
        resp = urllib.request.urlopen(req)
        print("Opening")
        soup = bs.BeautifulSoup(resp, "html.parser")
        print("Parsing")
        dog = soup.findAll(text=True)
        dogjson = json.loads(str(dog)[3:-3])
        doglink = dogjson["url"]
        await ctx.send(doglink)

    @commands.hybrid_command(
        aliases=["waifu"],
        with_app_command=True,
        description="B0B send amazing pics",
    )
    async def neko(self, ctx, mode: str = "neko") -> None:
        "❤️ キャットガールズは最高です"

        req = urllib.request.Request(
            url=f"https://nekos.life/api/v2/img/{mode}", headers=header
        )
        print("Connecting")
        resp = urllib.request.urlopen(req)
        print("Opening")
        soup = bs.BeautifulSoup(resp, "html.parser")
        print("Parsing")
        neko = soup.findAll(text=True)
        nekojson = json.loads(str(neko)[2:-4])
        try:
            nekolink = nekojson["url"]
            await ctx.send(nekolink)
        except KeyError:
            await ctx.send("Tag doesn't exist. Beep.")

    @commands.hybrid_command(
        with_app_command=True,
        description="B0B will tell your facts",
    )
    async def facts(self, ctx, person: str = "B0B") -> None:
        "💪 Tells you a fact about someone"
        req = urllib.request.Request(
            url=f"https://api.chucknorris.io/jokes/random", headers=header
        )
        print("Connecting")
        resp = urllib.request.urlopen(req)
        print("Opening")
        soup = bs.BeautifulSoup(resp, "html.parser")
        print("Parsing")
        dude = soup.findAll(text=True)
        print(str(dude)[2:-2])
        dudejson = json.loads(str(dude)[2:-2].encode("unicode_escape"))
        fact = dudejson["value"].replace("Chuck Norris", person)
        print(fact)
        await ctx.send(fact)


async def setup(bot):
    await bot.add_cog(Web(bot))
