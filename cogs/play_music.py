from discord.ext import commands
import discord
from utils.music_utils import get_youtube_audio_source

VOICE_CHANNEL_ID = 1376827452164411507

class MusicPlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, ctx, url: str):
        # 1. 음성채널 연결
        voice_channel = ctx.guild.get_channel(VOICE_CHANNEL_ID)
        if voice_channel is None:
            await ctx.send("지정된 음성채널이 존재하지 않습니다.")
            return

        voice_client = ctx.guild.voice_client
        if not voice_client or not voice_client.is_connected():
            try:
                voice_client = await voice_channel.connect()
            except discord.ClientException:
                await ctx.send("봇이 이미 다른 음성채널에 연결되어 있습니다.")
                return

        # 2. 유튜브 오디오 스트림 URL 추출
        await ctx.send("유튜브 오디오를 불러오는 중입니다...")
        try:
            audio_url, title = get_youtube_audio_source(url)
        except Exception as e:
            await ctx.send(f"유튜브 오디오를 불러오지 못했습니다: {e}")
            return

        # 3. 오디오 재생
        ffmpeg_options = {
            'options': '-vn'
        }
        audio_source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)

        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(audio_source)
        await ctx.send(f"지금 재생 중: {title}")

async def setup(bot):
    await bot.add_cog(MusicPlayerCog(bot))
