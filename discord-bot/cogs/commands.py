import discord
from discord.ext import commands
import time

from utils.game import game
from utils.text import normalize, get_first_word, get_last_word
from utils.database import add_score, get_top

class GameCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):

        if game.active:
            await ctx.send("Game đã chạy rồi.")
            return

        game.active = True
        game.last_word = "học sinh"
        game.used_words = ["học sinh"]
        game.last_player = None

        await ctx.send(
            f"🎮 Game bắt đầu!\n"
            f"Từ đầu tiên: **{game.last_word}**"
        )

    @commands.command()
    async def stop(self, ctx):

        game.active = False

        await ctx.send("🛑 Đã dừng game.")

    @commands.command()
    async def rank(self, ctx):

        top = get_top()

        if not top:
            await ctx.send("Chưa có dữ liệu.")
            return

        msg = "🏆 Leaderboard\n\n"

        for i, (uid, score) in enumerate(top[:10], start=1):
            user = await self.bot.fetch_user(int(uid))
            msg += f"{i}. {user.name} - {score} điểm\n"

        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not game.active:
            return

        text = normalize(message.content)

        if len(text.split()) < 2:
            return

        if game.last_player == message.author.id:
            await message.channel.send(
                "❌ Không được chơi 2 lượt liên tiếp."
            )
            return

        if text in game.used_words:
            await message.channel.send(
                "❌ Từ này đã được dùng."
            )
            return

        first_word = get_first_word(text)
        last_word = get_last_word(game.last_word)

        if first_word != last_word:
            await message.channel.send(
                f"❌ Sai nối từ.\n"
                f"Phải bắt đầu bằng: **{last_word}**"
            )
            return

        game.last_word = text
        game.used_words.append(text)
        game.last_player = message.author.id
        game.last_time = time.time()

        add_score(message.author.id, 1)

        await message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(GameCommands(bot))
