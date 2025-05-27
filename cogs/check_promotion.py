from discord.ext import commands
from utils.promotion import promote_item

class CheckPromotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='오늘의운세')
    async def check_promotion(self, ctx):
        promotion = promote_item()
        await ctx.send(f"오늘의 운세: {promotion}")

async def setup(bot):
    await bot.add_cog(CheckPromotion(bot))
