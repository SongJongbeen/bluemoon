from discord.ext import commands
import discord
import json
from utils.tts_utils import text_to_speech_file, remove_file, set_voice, get_voice

with open('data/ids.json', 'r', encoding='utf-8') as f:
    ids = json.load(f)
VOICE_CHANNEL_ID = int(ids['bluemoon_server']['voice_channel_id'])
TEXT_CHANNEL_ID = int(ids['bluemoon_server']['tts_channel_id'])

class TTSReaderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # DM, 다른 채널 무시
        if message.guild is None:
            return
        if message.channel.id != TEXT_CHANNEL_ID:
            return

        # 음성채널에 봇 연결 확인
        voice_channel = message.guild.get_channel(VOICE_CHANNEL_ID)
        if voice_channel is None:
            return
        voice_client = message.guild.voice_client
        if not voice_client or not voice_client.is_connected():
            try:
                voice_client = await voice_channel.connect()
            except discord.ClientException:
                return

        # TTS 변환 및 재생
        tts_text = message.content
        tts_path = text_to_speech_file(tts_text, model="tts-1")
        audio_source = discord.FFmpegPCMAudio(tts_path)
        
        def after_playing(error):
            if error:
                print(f"재생 중 오류 발생: {error}")
            remove_file(tts_path)
        
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=after_playing)
        else:
            remove_file(tts_path)

    @commands.command(name="목소리")
    async def set_voice_cmd(self, ctx, voice: str):
        if set_voice(voice):
            await ctx.send(f"목소리가 {voice}로 변경되었습니다.")
        else:
            await ctx.send(f"지원하는 목소리가 아닙니다. 가능한 목소리: alloy, echo, fable, onyx, nova, shimmer")

    @commands.command(name="현재목소리")
    async def get_voice_cmd(self, ctx):
        await ctx.send(f"현재 목소리: {get_voice()}")

async def setup(bot):
    await bot.add_cog(TTSReaderCog(bot))
