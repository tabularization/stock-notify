import discord
import config
import asyncio
from discord.ext import commands, tasks
from date import *
from alphavantage import get_stock_data
from newsapi import get_news_articles

# Initialize the Discord bot
intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

news_sent = False

async def check_price_movement():
    global news_sent
    
    stock_data = get_stock_data()
    stock_price_yesterday = float(stock_data['Time Series (Daily)'][yesterday]['5. adjusted close'])
    stock_price_day_before_yesterday = float(stock_data['Time Series (Daily)'][day_before_yesterday]['5. adjusted close'])

    if not news_sent and (stock_price_yesterday > stock_price_day_before_yesterday * 1.05 or stock_price_yesterday < stock_price_day_before_yesterday * .95):
        await send_news(stock_price_yesterday, stock_price_day_before_yesterday)
        news_sent = True
        await asyncio.sleep(900)  # Delay of 15 minutes
        news_sent = False

async def send_news(stock_price_yesterday, stock_price_day_before_yesterday):
    news_data = get_news_articles()
    news_title = [article['title'] for article in news_data]
    news_description = [article['description'] for article in news_data]
    news_url = [article['url'] for article in news_data]

    # Send news articles as messages
    guild = discord.utils.get(bot.guilds, id=config.GUILD_ID)
    channel = discord.utils.get(guild.text_channels, id=config.CHANNEL_ID)
    for i in range(len(news_data)):
        message = f"Percentage Change: {round(((stock_price_yesterday - stock_price_day_before_yesterday) / stock_price_day_before_yesterday) * 100, 2)}%\n"
        message += f"Title: {news_title[i]}\n"
        message += f"Description: {news_description[i]}\n"
        message += f"URL: {news_url[i]}"
        await channel.send(message)

@tasks.loop(minutes=15)
async def price_movement_check():
    await check_price_movement()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')
    await bot.change_presence(activity=discord.Game(name="Tracking the market📈"))
    price_movement_check.start()

bot.run(config.TOKEN)