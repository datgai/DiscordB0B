import os
import typing

import discord
import wavelink
from discord.ext import commands

# this cog uses wavelink library for music as opposed to youtube-dl

# Variables
LAVALINK_PASS = os.getenv("LAVALINK_PASS")
LAVALINK_PORT = os.getenv("LAVALINK_PORT")
LAVALINK_ADDRESS = os.getenv("LAVALINK_ADDRESS")


class Music(commands.Cog):
    """Blast some tunes"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self) -> None:
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(
            bot=self.bot,
            host=LAVALINK_ADDRESS,
            port=LAVALINK_PORT,
            password=LAVALINK_PASS,
        )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node) -> None:
        """Event fired when a node has finished connecting."""
        print(f"Node: <{node.identifier}> is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, player: wavelink.Player, track: wavelink.Track, reason
    ) -> None:
        ctx = player.ctx
        vc = ctx.voice_client

        if vc.loop:
            return await vc.play(track)
        next_song = vc.queue.get()
        await vc.play(next_song)
        mbed = discord.Embed(
            title=f"▶️ | Now playing {next_song}...",
            colour=discord.Colour.from_rgb(0, 255, 0),
        )
        await ctx.send(embed=mbed)

    @commands.hybrid_command(
        aliases=["vc"],
        with_app_command=True,
        description="B0B will connect to a voice channel..",
    )
    async def connect(self, ctx, *, channel: typing.Optional[discord.VoiceChannel]):
        """Connects to a voice channel"""
        if channel is None:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                return await ctx.send(
                    "No voice channel to connect to. Please either provide one or join one."
                )

        self.node = wavelink.NodePool.get_node()
        self.player = self.node.get_player(ctx.guild)

        # move channel if already connected to one
        if self.player is not None:
            if self.player.is_connected():
                await self.player.move_to(ctx.author.voice.channel)

        await channel.connect(cls=wavelink.Player)
        mbed = discord.Embed(
            title=f"🔗 | Connected to {channel.name}",
            colour=discord.Colour.from_rgb(0, 0, 255),
        )
        await ctx.send(embed=mbed)

    @commands.hybrid_command(
        aliases=["sm"],
        with_app_command=True,
        description="B0B will search for songs with the given search query.",
    )
    async def searchm(self, ctx, search: str):
        """Search for songs with the given search query."""
        tracks = await wavelink.YouTubeTrack.search(
            query=search,
        )
        for track in range(1, 6, 1):
            await ctx.send(f"{track}. {tracks[track].uri}")

    @commands.hybrid_command(
        aliases=["m"],
        with_app_command=True,
        description="B0B will play a song with the given search query.",
    )
    async def playm(self, ctx, *, track: wavelink.YouTubeTrack):
        """Play a song with the given search query."""

        if not ctx.voice_client:
            await self.connect(ctx, channel=ctx.author.voice.channel)
        vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            await vc.play(track)
            mbed = discord.Embed(
                title=f"▶️ | Now playing {track}...",
                colour=discord.Colour.from_rgb(0, 255, 0),
            )
        else:
            await vc.queue.put_wait(track)
            mbed = discord.Embed(
                title=f" 🎵 | Added {track} to queue...",
                colour=discord.Colour.from_rgb(0, 0, 255),
            )
        await ctx.send(embed=mbed)

        vc.ctx = ctx
        setattr(vc, "loop", False)

    @commands.hybrid_command(
        aliases=["skip"], with_app_command=True, description="B0B will skip a song"
    )
    async def skipm(self, ctx):
        """Skip the song"""
        vc = ctx.voice_client

        if vc.is_connected():
            if vc.is_playing():
                await vc.stop()
                mbed = discord.Embed(
                    title=f" ⏭️ | Skipped current music",
                    colour=discord.Colour.from_rgb(0, 0, 255),
                )
            else:
                mbed = discord.Embed(
                    title=f"Not playing any music right now. Beep.",
                    colour=discord.Colour.from_rgb(255, 0, 0),
                )
        else:
            mbed = discord.Embed(
                title=f"Not connected to any voice channels right now. Beep.",
                colour=discord.Colour.from_rgb(255, 0, 0),
            )
        await ctx.send(embed=mbed)

    @commands.hybrid_command(
        aliases=["pause"], with_app_command=True, description="B0B will pause the song"
    )
    async def pausem(self, ctx):
        """Pauses playback"""
        if self.player is None:
            return await ctx.send("B0B is not connected to any voice channels. Beep.")

        if not self.player.is_paused():
            if self.player.is_playing():
                await self.player.pause()
                mbed = discord.Embed(
                    title="⏸️ |Playback paused",
                    colour=discord.Colour.from_rgb(0, 0, 255),
                )
            else:
                mbed = discord.Embed(
                    title=f"Not playing any music right now. Beep.",
                    colour=discord.Colour.from_rgb(255, 0, 0),
                )
        return await ctx.send(embed=mbed)

    @commands.hybrid_command(
        aliases=["resume"],
        with_app_command=True,
        description="B0B will resume the song",
    )
    async def resumem(self, ctx):
        """Resumes playback"""
        if self.player is None:
            return await ctx.send("B0B is not connected to any voice channels. Beep.")

        if not self.player.is_paused():
            await self.player.resume()
            mbed = discord.Embed(
                title=" ▶️ | Playback resumed",
                colour=discord.Colour.from_rgb(0, 0, 255),
            )
        else:
            mbed = discord.Embed(
                title=f"Playback not paused. Beep.",
                colour=discord.Colour.from_rgb(255, 0, 0),
            )
        return await ctx.send(embed=mbed)

    @commands.hybrid_command(
        aliases=["q"], with_app_command=True, description="Ask B0B for music queue"
    )
    async def queuem(self, ctx) -> None:
        """Get music queue"""
        vc: wavelink.Player = ctx.voice_client
        for index, tracks in enumerate(vc.queue):
            await ctx.send(f"{index}. {tracks} \n")

    @commands.hybrid_command(
        aliases=["dc"],
        with_app_command=True,
        description="B0B will disconnect from voice channels",
    )
    async def disconnect(self, ctx) -> None:
        """Disconnect from voice channels"""
        vc: wavelink.Player = ctx.voice_client

        try:
            await vc.disconnect()
        except Exception as e:
            print(e)
        mbed = discord.Embed(
            title=f"🔌 |Disconnected from voice channel",
            colour=discord.Colour.from_rgb(0, 0, 255),
        )
        await ctx.send(embed=mbed)


async def setup(bot):
    await bot.add_cog(Music(bot))
