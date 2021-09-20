import discord
from discord.ext import commands

from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

import time
import datetime
import random
import sys

#Variables
Clukk = time.asctime(time.localtime())
thetime = datetime.datetime.strptime(Clukk, "%c")
intents = discord.Intents.all()
current_song =''
bot = commands.Bot(command_prefix=commands.when_mentioned_or('0 '),case_insensitive=True,intents=intents)
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True','default_search' : 'ytsearch'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
songq=[]

@bot.event
async def on_ready():
    print("B0B has awakened")
    await bot.change_presence(activity =discord.Game('w̶̡͌i̷͉̚t̷̘̎h̶̙̀ ̸̙͊ḧ̶̯́i̴̳̾ṡ̷͚ ̷̾͜f̷͈͛r̸̬̾i̴̢̎e̷̠͒ñ̶̥d̵͜͝s̸̮̆'))

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        print(message.content[22:])
        greets = ["hai","hey","hello","ni hao","yo","hi"]
        if any(word in message.content.lower() for word in greets):
            print("message rceived")
            greetings = ["Greetings ","Beep. Boop. ","Hello There ","01101000 01100101 01101100 01101100 01101111 "]
            userID = message.author.id
            await message.channel.send(random.choice(greetings)+"<@%s>"%(userID))
    await bot.process_commands(message)


@bot.command(pass_context = True)
async def ping(ctx):
    await ctx.channel.send ('pong.')

@bot.command(pass_context = True)
async def say(ctx):
    await ctx.channel.send (ctx.message.content)

@bot.command(pass_context = True)
async def clear(ctx, number: int):
    await ctx.channel.send("Deleting "+ str(number)+" Messages...")
    try:
        await ctx.channel.purge(limit=number+1)
        print(str(number) +" messages deleted")
    except Exception as e :
        print(e)

@bot.command(pass_context = True)
async def telltime(ctx):
    await ctx.channel.send("It is now " + thetime.strftime("%I:%M %p"))

@bot.command(pass_context = True)
async def telldate(ctx):
    await ctx.channel.send("Today is " + thetime.strftime("%A")+','+thetime.strftime("%d")+' of ' + thetime.strftime("%B %Y"))

@bot.command(pass_context = True)
async def tolong(ctx):
    await ctx.channel.send("Help yourself")

@bot.command(pass_context = True)
async def connect(ctx):
    try:
        await ctx.message.author.voice.channel.connect()
        await ctx.channel.send("Joining Voice...")
    except:
        pass


@bot.command()
async def mq(ctx,url):
    songq.append([ctx.author.voice.channel,url])
    await ctx.send("<%s> added into queue."%(url))

@bot.command()
async def play(ctx,url):
    voice = get(bot.voice_clients, guild=ctx.guild)
    for channel,song in songq:
        if channel == ctx.voice_client.channel:
            current_song = song
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(current_song, download=False)
                try:
                    URL = info['url']
                except Exception as e:
                    URL = info['entries'][0]['url']
                    current_song = 'https://www.youtube.com/watch?v='+ info['entries'][0]['id']
                    print(current_song)
            if not voice.is_playing():
                songq.remove([ctx.author.voice.channel, url])
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e:play(ctx))
            voice.is_playing()

            await ctx.send("%s playing..."%(current_song))
            print("<%s> playing..."%(current_song))


@bot.command()
async def m(ctx, url):
    voice = get(bot.voice_clients, guild=ctx.guild)
    await connect(ctx)
    await mq(ctx,url)
    try:
        await play(ctx,url)
    except:
        pass

@bot.command()
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await play(ctx)

@bot.command()
async def clearqueue(ctx):
    for songdata in songq:
         if songdata[0] == ctx.author.voice.channel:
                songq.remove(songdata)


@bot.command()
async def disconnect(ctx):
    if ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
        await ctx.send("Leaving Voice...")
        await clearqueue(ctx)

@bot.command()
async def checkqueue(ctx):
    await ctx.send(songq)

# addgoogle
# get a random image from Imgur.
# cat
# wiki
# urbandict
# timer

bot.run("NDgxMDkzNzgwNzc1MjM5Njkw.W3rDfw.lkxSn97X6BXqBNoqq9AhrmMFK3E")
print ("hello world")
sys.stdout.flush()
