import requests
import config
import discord

alphavantage_endpoint = "https://www.alphavantage.co/query"
alphavantage_api = config.alphavantage_api

def get_stock_data(ticker):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": alphavantage_api
    }
    response = requests.get(alphavantage_endpoint, params=params)
    return response.json()['Global Quote']

def get_news(ticker, article_limit):
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "sort": "RELEVANCE",
        "apikey": alphavantage_api,
    }
    response = requests.get(alphavantage_endpoint, params=params)
    return response.json()['feed'][0:article_limit]

async def get_sentiment(price_change):
    global sign
    if price_change < 0:
        sign = "Decrease of"
        return discord.Color.red()
    sign = "Increase of"
    return discord.Color.green()

async def check_price_movement(bot, ticker, article_limit):
    stock_data = get_stock_data(ticker)
    symbol = (stock_data['01. symbol'])
    open_price = float(stock_data['02. open'])
    high_price = float(stock_data['03. high'])
    low_price = float(stock_data['04. low'])
    price_today = float(stock_data['05. price'])
    volume = int(stock_data['06. volume'])
    price_change = float(stock_data['09. change'])
    percent_change = stock_data['10. change percent']
    await send_news(bot, symbol, article_limit, open_price, high_price, low_price, price_today, volume, price_change, percent_change)

async def send_news(bot, symbol, article_limit, open_price, high_price, low_price, price_today, volume, price_change, percent_change):
    news_data = get_news(symbol, article_limit)
    news_title = [article['title'] for article in news_data]
    news_sentiment = [article['overall_sentiment_label'] for article in news_data]
    news_url = [article['url'] for article in news_data]

    guild = discord.utils.get(bot.guilds, id=config.GUILD_ID)
    channel = discord.utils.get(guild.text_channels, id=config.CHANNEL_ID)
    for i in range(len(news_data)):
        embed = discord.Embed(
            title=news_title[i],
            url=news_url[i],
            color=await get_sentiment(price_change)
        )
        embed.add_field(name="Stock", value=symbol, inline=False)
        embed.add_field(name="Open Price", value=f"${open_price}", inline=True)
        embed.add_field(name="High Price", value=f"${high_price}", inline=True)
        embed.add_field(name="Low Price", value=f"${low_price}", inline=True)
        embed.add_field(name="Close Price", value=f"${price_today}", inline=True)
        embed.add_field(name="Volume", value=f"{volume} shares traded", inline=True)
        embed.add_field(name=f"{sign}", value=f"${price_change}", inline=True)
        embed.add_field(name="Percent Change", value=percent_change, inline=True)
        embed.add_field(name="Market Sentiment", value=f"{news_sentiment[i]}", inline=True)
        await channel.send(embed=embed)
