import requests
import config
from date import *

news_endpoint = "https://newsapi.org/v2/everything"
news_api = config.newsapi_api

def get_news_articles():
    params = {
        "q": config.COMPANY_NAME,
        "from": day_before_yesterday,
        "to": yesterday,
        "sortBy": "popularity",
        "apiKey": news_api
    }
    response = requests.get(news_endpoint, params=params)
    response.raise_for_status()
    return response.json()['articles'][0:3]
