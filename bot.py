import discord
from discord.ext import commands
import config
import alphavantage

# Initialize the Discord bot
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Cooking 🧑‍🍳"))
    await bot.tree.sync()

@bot.tree.command(name="stock-alert")
async def stock_alert(ctx, ticker: str, article_limit: int):
    await ctx.response.send_message(f"Processing your request...", ephemeral=True)
    await alphavantage.check_price_movement(bot, ticker, article_limit)

bot.run(config.TOKEN)
