import discord
from discord.ext import commands
from utils.perplexity import ask_perplexity

class QA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='qa')
    async def qa(self, ctx, *, question):
        await ctx.send("잠시만 기다려주세요...")
        answer = ask_perplexity(question)
        await ctx.send(answer)

async def setup(bot):
    await bot.add_cog(QA(bot))
