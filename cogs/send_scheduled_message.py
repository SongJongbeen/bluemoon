import asyncio
from discord.ext import commands, tasks
from utils.time_utils import is_every_hour, is_specific_hours

GUILD_ID = 1376827452164411503    # TEST SERVER
CHANNEL_ID = 1376827527330402396
BARRIER_ID = 1376872065969160192
FIELD_BOSS_ID = 1376877063549485156
MESSAGE_SCHEDULE = [
    {
        "name": "결계",
        "role_id": BARRIER_ID,
        "check_func": lambda: is_every_hour(minute=0),
        "message": "소환의 결계 2분전입니다."
    },
    {
        "name": "필보",
        "role_id": FIELD_BOSS_ID,
        "check_func": lambda: is_specific_hours([12, 18, 20, 22], 0),
        "message": "필드보스 시간입니다."
    }
]

class ScheduledMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduled_messages.start()

    @tasks.loop(seconds=30)
    async def scheduled_messages(self):
        guild = self.bot.get_guild(GUILD_ID)
        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        for schedule in MESSAGE_SCHEDULE:
            if schedule["check_func"]():
                role = guild.get_role(schedule["role_id"])
                await channel.send(f"{role.mention} {schedule["message"]}")
                await asyncio.sleep(60)  # 중복 전송 방지

async def setup(bot):
    await bot.add_cog(ScheduledMessageCog(bot))
