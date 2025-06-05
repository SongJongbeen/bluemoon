import discord
import os
import json
from dotenv import load_dotenv
from discord.ext import commands
import discord.opus

load_dotenv()

with open('data/ids.json', 'r') as f:
    ids = json.load(f)

ROLE_CHANNEL_ID = int(ids['bluemoon_server']['bot_desc_id'])

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

    # 역할 버튼 메시지 관리
    channel = bot.get_channel(ROLE_CHANNEL_ID)
    if channel:
        # 채널의 메시지 기록을 가져옵니다
        async for message in channel.history(limit=100):
            print(message)
            if message.author == bot.user:
                print('Bot message found:', message.id)
                print('Components:', message.components)
                print('Has components:', hasattr(message, 'components'))
                if hasattr(message, 'components') and message.components:
                    # 기존 메시지 삭제
                    print('found: ', message)
                    await message.delete()
        
        # 새로운 역할 버튼 메시지 전송
        role_manager = bot.get_cog('RoleManager')
        if role_manager:
            await role_manager.send_role_message(channel)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(os.getenv('DISCORD_TOKEN'))
