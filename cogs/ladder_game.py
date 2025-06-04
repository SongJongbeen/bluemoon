from discord.ext import commands
import random

class LadderGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='사다리')
    async def ladder(self, ctx, *, args):
        # 참가자와 결과를 콤마(,)로 구분
        try:
            participants, results = [item.strip() for item in args.split('/')]
            participants = [p.strip() for p in participants.split(',')]
            results = [r.strip() for r in results.split(',')]

            if len(participants) != len(results):
                await ctx.send("참가자 수와 결과 수가 일치하지 않습니다!")
                return

            # 결과 섞기
            shuffled_results = results.copy()
            random.shuffle(shuffled_results)

            # 결과 메시지 생성
            message = "🪜 사다리타기 결과 🪜\n\n"
            for participant, result in zip(participants, shuffled_results):
                message += f"{participant} ➡️ || {result} ||\n"

            await ctx.send(message)

        except ValueError:
            await ctx.send("올바른 형식으로 입력해주세요!\n사용법: !사다리 참가자1, 참가자2 | 결과1, 결과2")

async def setup(bot):
    await bot.add_cog(LadderGame(bot))
