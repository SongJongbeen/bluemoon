from discord.ext import commands
import discord
import json
from utils.tts_utils import text_to_speech_file, remove_file

with open('data/ids.json', 'r') as f:
    ids = json.load(f)

VOICE_CHANNEL_ID = ids['bluemoon_server']['voice_channel_id']
TEXT_CHANNEL_ID = ids['bluemoon_server']['tts_channel_id']

class TTSReaderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # 봇 메시지, DM, 다른 채널 무시
        if message.author.bot or message.guild is None:
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
                # 이미 다른 채널에 연결 중일 수 있음
                return

        # TTS 변환 및 재생
        # tts_text = f"{message.author.display_name} : {message.content}"
        tts_text = f"{message.content}"
        tts_path = text_to_speech_file(tts_text, model="tts-1", voice="alloy")
        audio_source = discord.FFmpegPCMAudio(tts_path)

        # 재생 중이면 무시(간단 구현, 큐잉 필요시 별도 구현)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=lambda e: remove_file(tts_path))
        else:
            # 이미 재생 중이면 파일만 삭제
            remove_file(tts_path)

async def setup(bot):
    await bot.add_cog(TTSReaderCog(bot))
