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
bot = commands.Bot(command_prefix=commands.when_mentioned_or('BOB '),case_insensitive=True,intents=intents)


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
    print(ctx.message.content)


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
    await ctx.channel.send("Joining Voice...")
    vchannel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(vchannel)
    else:
        voice = await vchannel.connect()

@bot.command()
async def music(ctx, url):
    await connect(ctx)
    print("Playing music "+ url)
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')

    # check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return

@bot.command()
async def disconnect(ctx):
    await ctx.send("Leaving Voice...")
    for vc in bot.voice_clients:
        await vc.disconnect()

# addgoogle
# get a random image from Imgur.
# cat
# wiki
# urbandict
# timer

bot.run("NDgxMDkzNzgwNzc1MjM5Njkw.W3rDfw.lkxSn97X6BXqBNoqq9AhrmMFK3E")
print ("hello world")
sys.stdout.flush()
