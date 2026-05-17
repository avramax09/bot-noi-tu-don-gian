import discord
from discord.ext import commands
import asyncio

from config import TOKEN, PREFIX

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Đăng nhập: {bot.user}")

async def main():

    async with bot:
        await bot.load_extension("cogs.commands")
        await bot.start(TOKEN)

asyncio.run(main())