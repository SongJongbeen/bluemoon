import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord.opus

load_dotenv()

# Opus 라이브러리 로드
try:
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus.so.0')
        print('Opus 라이브러리가 로드되었습니다.')
except Exception as e:
    print(f'Opus 라이브러리 로드 실패: {e}')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.load_extension('cogs.qa')  # Cog 로딩
    await bot.load_extension('cogs.search_member')
    await bot.load_extension('cogs.check_promotion')
    await bot.load_extension('cogs.manage_role')
    await bot.load_extension('cogs.ladder_game')
    await bot.load_extension('cogs.send_scheduled_message')
    await bot.load_extension('cogs.voice_control')
    await bot.load_extension('cogs.read_tts')
    # await bot.load_extension('cogs.play_music') # 음악 재생 기능 비활성화 (유튜브 정책책)
    await bot.load_extension('cogs.get_deian')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(os.getenv('DISCORD_TOKEN'))
