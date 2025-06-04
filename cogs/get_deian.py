import asyncio
import re
import json
from datetime import datetime
from discord.ext import commands, tasks
from utils.selenium_utils import get_server_soup
from utils.time_utils import is_every_half_hour

with open('data/ids.json', 'r', encoding='utf-8') as f:
    ids = json.load(f)

GUILD_ID = int(ids['bluemoon_server']['server_id'])
CHANNEL_ID = int(ids['bluemoon_server']['bot_channel_id'])
ABYSS_HOLE_ID = int(ids['bluemoon_server']['abyss_hole_id'])

class GetAbyssHoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_abyss_hole.start()

    @tasks.loop(seconds=60)
    async def get_abyss_hole(self):
        if not is_every_half_hour(minutes=[20, 50]):    # 현재 검은구멍 리젠 시간
            return

        URL = "https://mobigg.kr/"
        SERVER = "데이안"
        guild = self.bot.get_guild(GUILD_ID)
        channel = self.bot.get_channel(CHANNEL_ID)
        role = guild.get_role(ABYSS_HOLE_ID)
        soup = get_server_soup(URL, SERVER)
        section = soup.find('section', class_='card report-list')

        # with open("data/abyss_hole.html", "w", encoding="utf-8") as f:
        #     f.write(soup.prettify())

        if section:
            display_none_div = section.find('div', style=lambda x: x and 'display: none' in x)
            report_cards = section.find_all('div', class_='report-card auto-generated')
            if display_none_div and not report_cards:
                now = datetime.now()
                print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} 얼음협곡 심층 검은 구멍 출현 없음")
                return
            elif report_cards:
                for card in report_cards:
                    card_text = card.get_text(strip=True)
                    match = re.search(r'(.+)남은 시간:(.+)(좋아요)', card_text)
                    if match:
                        location = match.group(1)
                        remaining_time = match.group(2)
                        if "여신" in location:
                            print("여신의 뜰")
                            continue
                        if remaining_time == "만료":
                            print("만료된 구멍")
                            continue
                        await channel.send(f"{role.mention} 얼음협곡 심층 검은 구멍 출현")
                        await channel.send(f"남은 시간: {remaining_time}")
                        break
                print("loop end")

        await asyncio.sleep(60)

async def setup(bot):
    await bot.add_cog(GetAbyssHoleCog(bot))
