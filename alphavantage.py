import requests
import config

alphavantage_endpoint = "https://www.alphavantage.co/query"
alphavantage_api = config.alphavantage_api

def get_stock_symbol():
    with open('config.py', 'r') as file:
        lines = file.readlines()
    for line in lines:
        if 'STOCK' in line:
            return line.split('=')[1].strip().strip('"')   
             
def get_article_limt():
    with open('config.py', 'r') as file:
        lines = file.readlines()
    for line in lines:
        if 'LIMIT' in line:
            return int(line.split('=')[1])        
        
def get_stock_data():
    stock_symbol = get_stock_symbol()
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": stock_symbol,
        "apikey": alphavantage_api
    }
    response = requests.get(alphavantage_endpoint, params=params)
    return response.json()['Global Quote']

def get_news():
    stock_symbol= get_stock_symbol()
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": stock_symbol,
        "sort": "RELEVANCE",
        "apikey": alphavantage_api,
    }
    response = requests.get(alphavantage_endpoint, params=params)
    return response.json()['feed'][0:get_article_limt()]


