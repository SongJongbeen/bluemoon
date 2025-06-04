from discord.ext import commands
import discord
import json
from utils.music_utils import get_youtube_audio_info, MusicQueue

with open('data/ids.json', 'r', encoding='utf-8') as f:
    ids = json.load(f)

VOICE_CHANNEL_ID = int(ids['bluemoon_server']['voice_channel_id'])

class PlayMusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = MusicQueue()
        self.is_playing = False
        self.is_paused = False
        self.current = None
        self.volume = 0.5  # 50%
        self.repeat = 'off'

    async def ensure_voice(self, ctx):
        voice_channel = ctx.guild.get_channel(VOICE_CHANNEL_ID)
        if voice_channel is None:
            await ctx.send("지정된 음성채널이 없습니다.")
            return None
        voice_client = ctx.guild.voice_client
        if not voice_client or not voice_client.is_connected():
            try:
                voice_client = await voice_channel.connect()
            except discord.ClientException:
                await ctx.send("봇이 이미 다른 음성채널에 연결되어 있습니다.")
                return None
        return voice_client

    async def play_next(self, ctx):
        if self.queue.is_empty():
            self.is_playing = False
            self.current = None
            return
        item = self.queue.pop()
        self.current = item
        voice_client = ctx.guild.voice_client
        audio_source = discord.FFmpegPCMAudio(item['url'])
        audio_source = discord.PCMVolumeTransformer(audio_source, volume=self.volume)
        def after_playing(error):
            fut = self.bot.loop.create_task(self.after_song(ctx))
        voice_client.play(audio_source, after=after_playing)
        self.is_playing = True
        await ctx.send(f"지금 재생 중: {item['title']}")

    async def after_song(self, ctx):
        # 반복 모드 처리
        if self.repeat == 'one' and self.current:
            self.queue.queue.insert(0, self.current)
        elif self.repeat == 'all' and self.current:
            self.queue.queue.append(self.current)
        await self.play_next(ctx)

    @commands.command(name="재생")
    async def play(self, ctx, *, query: str):
        info = await get_youtube_audio_info(query)
        self.queue.add(info)
        await ctx.send(f"'{info['title']}'을(를) 큐에 추가했습니다.")
        if not self.is_playing:
            voice_client = await self.ensure_voice(ctx)
            if voice_client:
                await self.play_next(ctx)

    @commands.command(name="스킵")
    async def skip(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("다음 곡으로 넘어갑니다.")
        else:
            await ctx.send("재생 중인 곡이 없습니다.")

    @commands.command(name="비우기")
    async def stop(self, ctx):
        self.queue.clear()
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        self.is_playing = False
        self.current = None
        await ctx.send("음악 재생을 중지하고 큐를 비웠습니다.")

    @commands.command(name="일시정지")
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            self.is_paused = True
            await ctx.send("음악이 일시정지되었습니다.")
        else:
            await ctx.send("일시정지할 음악이 없습니다.")

    @commands.command(name="재개")
    async def resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and self.is_paused:
            voice_client.resume()
            self.is_paused = False
            await ctx.send("음악을 다시 재생합니다.")
        else:
            await ctx.send("다시 재생할 음악이 없습니다.")

    @commands.command(name="큐")
    async def queue_cmd(self, ctx):
        if self.queue.is_empty():
            await ctx.send("큐에 곡이 없습니다.")
        else:
            msg = "**[음악 큐]**\n"
            for idx, item in enumerate(self.queue.queue, 1):
                msg += f"{idx}. {item['title']}\n"
            await ctx.send(msg)

    @commands.command(name="셔플")
    async def shuffle(self, ctx):
        self.queue.shuffle()
        await ctx.send("큐가 셔플되었습니다.")

    @commands.command(name="반복")
    async def repeat_cmd(self, ctx, mode: str):
        if mode not in ['한곡', '전체', '해제']:
            await ctx.send("사용법: !반복 [한곡|전체|해제]")
            return
        if mode == '한곡':
            self.repeat = 'one'
            await ctx.send("현재 곡 반복 모드입니다.")
        elif mode == '전체':
            self.repeat = 'all'
            await ctx.send("큐 전체 반복 모드입니다.")
        else:
            self.repeat = 'off'
            await ctx.send("반복 모드가 해제되었습니다.")

    @commands.command(name="볼륨")
    async def volume(self, ctx, vol: int):
        if not (0 <= vol <= 100):
            await ctx.send("0~100 사이의 값을 입력하세요.")
            return
        self.volume = vol / 100.0
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.source:
            voice_client.source.volume = self.volume
        await ctx.send(f"볼륨을 {vol}%로 설정했습니다.")

    @commands.command(name="현재곡")
    async def now_playing(self, ctx):
        if self.current:
            await ctx.send(f"현재 재생 중: {self.current['title']}")
        else:
            await ctx.send("현재 재생 중인 곡이 없습니다.")

async def setup(bot):
    await bot.add_cog(PlayMusicCog(bot))
