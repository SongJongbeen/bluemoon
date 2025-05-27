import discord
from discord.ext import commands
from utils.members import search_member

class MemberSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='멤버')
    async def search(self, ctx, *, character_name):
        main_char, alts = search_member(character_name)

        if main_char is None:
            await ctx.send("해당하는 캐릭터를 찾을 수 없습니다.")
            return

        if character_name == main_char:
            # 메인 캐릭터로 검색한 경우
            alts_str = ', '.join(alts)
            await ctx.send(f"{main_char}님의 캐릭터: {alts_str}")
        else:
            # 부캐릭터로 검색한 경우
            await ctx.send(f"{character_name}님의 본캐릭터: {main_char}")

async def setup(bot):
    await bot.add_cog(MemberSearch(bot))
