from datetime import datetime, timedelta

today = datetime.now()
days_to_subtract = 1
yesterday = (today - timedelta(days=days_to_subtract)).strftime("%Y-%m-%d")
day_before_yesterday =( today - timedelta(days=days_to_subtract + 1)).strftime("%Y-%m-%d")
today = today.strftime("%Y-%m-%d")
