import json
from discord.ext import commands
from utils.voice_utils import (
    join_voice_channel, leave_voice_channel,
    is_user_joined_channel, make_join_message
)
from utils.privacy_utils import is_privacy_allowed

with open('data/ids.json', 'r', encoding='utf-8') as f:
    ids = json.load(f)

VOICE_CHANNEL_ID = int(ids['bluemoon_server']['voice_channel_id'])
TEXT_CHANNEL_ID = int(ids['bluemoon_server']['tts_channel_id'])

class VoiceControlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # !입장 명령어: 봇이 음성채널에 입장
    @commands.command(name="입장")
    async def join(self, ctx):
        guild = ctx.guild
        result = await join_voice_channel(self.bot, guild, VOICE_CHANNEL_ID)
        if result:
            await ctx.send("음성채널에 입장했습니다.")
        else:
            await ctx.send("음성채널에 입장할 수 없습니다.")

    # !퇴장 명령어: 봇이 음성채널에서 퇴장
    @commands.command(name="퇴장")
    async def leave(self, ctx):
        guild = ctx.guild
        result = await leave_voice_channel(guild)
        if result:
            await ctx.send("음성채널에서 퇴장했습니다.")
        else:
            await ctx.send("봇이 음성채널에 연결되어 있지 않습니다.")

    # 누군가 입장하면 닉네임 알림
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # 봇은 무시
        if member.bot:
            return

        # 개인정보 허용 여부 확인
        if not is_privacy_allowed(member.display_name):
            return

        # 입장 알림
        if is_user_joined_channel(before, after, VOICE_CHANNEL_ID):
            text_channel = self.bot.get_channel(TEXT_CHANNEL_ID)
            if text_channel:
                await text_channel.send(make_join_message(member))

        # 아무도 없으면 자동 퇴장
        voice_client = member.guild.voice_client
        if voice_client and voice_client.channel and voice_client.channel.id == VOICE_CHANNEL_ID:
            # 해당 채널에 봇만 남았는지 확인
            if len([m for m in voice_client.channel.members if not m.bot]) == 0:
                await voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(VoiceControlCog(bot))
