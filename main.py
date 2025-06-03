import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

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
    await bot.load_extension('cogs.play_music')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(os.getenv('DISCORD_TOKEN'))
