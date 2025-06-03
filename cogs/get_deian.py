import asyncio
import re
from discord.ext import commands, tasks
from utils.selenium_utils import get_server_soup
from utils.time_utils import is_every_half_hour

GUILD_ID = 1376827452164411503    # TEST SERVER
CHANNEL_ID = 1376827527330402396
ABYSS_HOLE_ID = 1376877152418398299

class GetAbyssHoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_abyss_hole.start()

    @tasks.loop(seconds=60)
    async def get_abyss_hole(self):
        if not is_every_half_hour():
            return

        URL = "https://mobigg.kr/"
        SERVER = "데이안"
        guild = self.bot.get_guild(GUILD_ID)
        channel = self.bot.get_channel(CHANNEL_ID)
        role = guild.get_role(ABYSS_HOLE_ID)
        soup = get_server_soup(URL, SERVER)
        section = soup.find('section', class_='card report-list')

        if section:
            display_none_div = section.find('div', style=lambda x: x and 'display: none' in x)
            if display_none_div:
                return
            else:
                await channel.send(f"{role.mention} 얼음협곡 심층 검은 구멍 출현")
                for card in section.find_all('div', class_='report-card auto-generated'):
                    card_text = card.get_text(strip=True)
                    match = re.search(r'(.+)남은 시간:(.+)(좋아요)', card_text)
                    if match:
                        remaining_time = match.group(2)
                        await channel.send(f"남은 시간: {remaining_time}")

        await asyncio.sleep(60)

async def setup(bot):
    await bot.add_cog(GetAbyssHoleCog(bot))
