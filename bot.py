import discord
from discord.ext import commands
import config
from alphavantage import *

# Initialize the Discord bot
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
async def check_price_movement():
    stock_data = get_stock_data()
    open_price = float(stock_data['02. open'])  
    high_price = float(stock_data['03. high'])
    low_price = float(stock_data['04. low'])
    price_today= float(stock_data['05. price'])
    volume = int(stock_data['06. volume'])
    price_change = float(stock_data['09. change'])  
    percent_change = stock_data['10. change percent']
    await send_news(open_price, high_price, low_price, price_today, volume, price_change, percent_change)

async def get_sentiment(price_change):
    global sign
    if price_change < 0:
        sign = "Decrease of"
        return discord.Color.red()
    sign = "Increase of"
    return discord.Color.green()
 
async def send_news(open_price, high_price, low_price, price_today, volume, price_change, percent_change): # VOLUME AND PRICE_TODAY WAS CHANGED
    # Retrieve news data
    news_data = get_news()
    news_title = [article['title'] for article in news_data]
    news_sentiment = [article['overall_sentiment_label'] for article in news_data]
    news_url = [article['url'] for article in news_data]

    # Send news articles as messages
    guild = discord.utils.get(bot.guilds, id=config.GUILD_ID)
    channel = discord.utils.get(guild.text_channels, id=config.CHANNEL_ID)
    for i in range(len(news_data)):
        embed = discord.Embed(
            title=news_title[i],
            url = news_url[i],
            color = await get_sentiment(price_change)
        )
        embed.add_field(name="Stock", value=f"${get_stock_symbol().upper()}", inline=False)
        embed.add_field(name="Open Price", value=f"${open_price}", inline=True)
        embed.add_field(name="High Price", value=f"${high_price}", inline=True)
        embed.add_field(name="Low Price", value=f"${low_price}", inline=True)
        embed.add_field(name="Close Price", value=f"${price_today}", inline=True)
        embed.add_field(name="Volume", value=f"{volume} shares traded", inline=True)
        embed.add_field(name=f"{sign}", value=f"${price_change}", inline=True)
        embed.add_field(name="Percent Change", value=percent_change, inline=True)
        embed.add_field(name="Market Sentiment", value=f"{news_sentiment[i]}", inline=True)
        await channel.send(embed=embed)

@bot.event
async def on_ready():
        print(f'Logged in as {bot.user.name}')
        await bot.change_presence(activity=discord.Game(name="Cooking 🧑‍🍳"))
        await bot.tree.sync()

@bot.tree.command(name="stock-alert")
async def stock_alert(ctx, ticker: str, article_limit: int):
    await ctx.response.send_message(f"Processing your request...", ephemeral=True)  
    with open('config.py', 'r') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        if 'STOCK' in lines[i]:
            lines[i] = 'STOCK = "{}"\n'.format(ticker)
        if 'LIMIT' in lines[i]:
            lines[i] = 'LIMIT = {}\n'.format((article_limit))
            break
    with open('config.py', 'w') as file:
        file.writelines(lines)
    await check_price_movement()

bot.run(config.TOKEN)