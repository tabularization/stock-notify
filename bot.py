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

news_sent = True

async def check_price_movement():
    global news_sent 
    global price_movement_symbol
    
    stock_data = get_stock_data()
    stock_price_yesterday = float(stock_data['Time Series (Daily)'][yesterday_formatted]['1. open'])
    stock_price_day_before_yesterday = float(stock_data['Time Series (Daily)'][day_before_yesterday_formatted]['4. close'])
    
    if stock_price_yesterday > stock_price_day_before_yesterday * 1.05:
        price_movement_symbol = "📈"
    if stock_price_yesterday < stock_price_day_before_yesterday * 0.95:
        price_movement_symbol = "📉"

    if news_sent and (stock_price_yesterday > stock_price_day_before_yesterday * 1.05 or stock_price_yesterday < stock_price_day_before_yesterday * .95):
        await send_news(stock_price_yesterday, stock_price_day_before_yesterday)
        news_sent = False
        await asyncio.sleep(86400)  # Delay of 24 hours
        news_sent = True

async def send_news(stock_price_yesterday, stock_price_day_before_yesterday):
    news_data = get_news_articles()
    news_title = [article['title'] for article in news_data]
    news_description = [article['description'] for article in news_data]
    news_url = [article['url'] for article in news_data]

    # Send news articles as messages
    guild = discord.utils.get(bot.guilds, id=config.GUILD_ID)
    channel = discord.utils.get(guild.text_channels, id=config.CHANNEL_ID)
    for i in range(len(news_data)):
        embed = discord.Embed(
            title=news_title[i],
            description=news_description[i],
            url = news_url[i],
            color=discord.Color.green()
        )
        embed.add_field(name="Stock", value=f"${config.STOCK}", inline=False)
        embed.add_field(name=f"{price_movement_symbol} Percentage Change", value=f"{round(((stock_price_yesterday - stock_price_day_before_yesterday) / stock_price_day_before_yesterday) * 100, 2)}%", inline=False)
        
        await channel.send(embed=embed)

@tasks.loop(hours=24)
async def price_movement_check():
    await check_price_movement()

@bot.event
async def on_ready():
    if market_open:
        print(f'Logged in as {bot.user.name}')
        print('------')
        await bot.change_presence(activity=discord.Game(name="Market is opened 🔓"))
        price_movement_check.start()
    else:
        print(f'Logged in as {bot.user.name}')
        print('------')
        await bot.change_presence(activity=discord.Game(name="Market is closed 🔒"))
        embed = discord.Embed(
            title="Market is closed on weekends.",
            color=discord.Color.green()
        )
        guild = bot.get_guild(config.GUILD_ID)
        channel = bot.get_channel(config.CHANNEL_ID)
        await channel.send(embed=embed)
        await bot.close()

bot.run(config.TOKEN)