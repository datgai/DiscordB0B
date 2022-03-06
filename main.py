import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

import time
import datetime
import random
import os

# Variables
Clukk = time.asctime(time.localtime())
thetime = datetime.datetime.strptime(Clukk, "%c")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('0 '), case_insensitive=True, intents=intents)
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'default_search': 'ytsearch'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
songq = []


@bot.event
async def on_ready():
    print(' logged in as {0.user}'.format(discord.Client))
    await bot.change_presence(activity=discord.Game('w̶̡͌i̷͉̚t̷̘̎h̶̙̀ ̸̙͊ḧ̶̯́i̴̳̾ṡ̷͚ ̷̾͜f̷͈͛r̸̬̾i̴̢̎e̷̠͒ñ̶̥d̵͜͝s̸̮̆'))


@bot.event
async def on_message(message):
    if message.author == discord.Client.user:
        return
    else:
        if bot.user.mentioned_in(message):
            print(message.content[22:])
            greets = []
            if any(word in message.content.lower() for word in greets):
                print("message received")
                greetings = ["Greetings ", "Beep. Boop. ", "Hello There ",
                             "01101000 01100101 01101100 01101100 01101111"]
                user_id = message.author.id
                await message.channel.send(random.choice(greetings) + "<@%s>" % user_id)
        await bot.process_commands(message)


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.channel.send('pong.')


@bot.command(pass_context=True)
async def say(ctx):
    await ctx.channel.send(ctx.message.content[26:])


@bot.command(pass_context=True)
async def clear(ctx, number: int):
    await ctx.channel.send("Deleting " + str(number) + " Messages...")
    try:
        await ctx.channel.purge(limit=number + 1)
        print(str(number) + " messages deleted")
    except Exception as e:
        print(e)


@bot.command(pass_context=True)
async def telltime(ctx):
    await ctx.channel.send("It is now " + thetime.strftime("%I:%M %p"))


@bot.command(pass_context=True)
async def telldate(ctx):
    await ctx.channel.send(
        "Today is " + thetime.strftime("%A") + ',' + thetime.strftime("%d") + ' of ' + thetime.strftime("%B %Y"))


@bot.command(pass_context=True)
async def connect(ctx):
    try:
        await ctx.message.author.voice.channel.connect()
        print("connecting to " + str(ctx.message.author.voice.channel))
        await ctx.channel.send("Joining voice channel " + str(ctx.message.author.voice.channel))
    except Exception as e:
        print(e)


@bot.command()
async def mq(ctx, url):
    songq.append([ctx.author.voice.channel, url])
    await ctx.send("<%s> added into queue." % url)


@bot.command()
async def playm(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    def sing():
        global playing_song
        for channel, song in songq:
            if channel == ctx.voice_client.channel:
                current_song = song
                print(current_song)
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(current_song, download=False)
                    try:
                        url = info['url']
                    except Exception as e:
                        url = info['entries'][0]['url']
                        playing_song = 'https://www.youtube.com/watch?v=' + info['entries'][0]['id']
                        print(playing_song)
                if not voice.is_playing():
                    songq.remove([ctx.author.voice.channel, current_song])
                voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda e: sing())
                voice.is_playing()

                print("<%s> playing..." % current_song)

    sing()
    await ctx.send("%s playing..." % playing_song)


@bot.command()
async def m(ctx, url):
    await connect(ctx)
    await mq(ctx, url)
    try:
        await playm(ctx)
    except Exception as e:
        print(e)


@bot.command()
async def skipm(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await playm(ctx)


@bot.command()
async def clearmqueue(ctx):
    for songdata in songq:
        if songdata[0] == ctx.author.voice.channel:
            songq.remove(songdata)


@bot.command()
async def disconnect(ctx):
    if ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
        await ctx.send("Leaving Voice...")
        await clearmqueue(ctx)


@bot.command()
async def mqueue(ctx):
    await ctx.send(songq)


@bot.command(pass_context=True)
async def tolong(ctx):
    await ctx.channel.send(" ")


bot.run(os.getenv('DISCORD-TOKEN'))