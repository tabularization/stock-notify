import requests
import config

alphavantage_endpoint = "https://www.alphavantage.co/query"
alphavantage_api = config.alphavantage_api

def get_stock_data():
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": config.STOCK,
        "apikey": alphavantage_api
    }
    response = requests.get(alphavantage_endpoint, params=params)
    response.raise_for_status()
    return response.json()