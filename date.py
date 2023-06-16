from datetime import datetime, timedelta 

today = datetime.now()
today_weekday = today.weekday()
days_to_subtract = 1


yesterday_formatted = (today - timedelta(days=days_to_subtract)).strftime("%Y-%m-%d")
yesterday_weekday = (today - timedelta(days=days_to_subtract)).weekday()

day_before_yesterday_formatted = (today - timedelta(days=days_to_subtract + 1)).strftime("%Y-%m-%d")
day_before_yesterday_weekday = (today - timedelta(days=days_to_subtract + 1)).weekday()

if 0 <= today_weekday <= 4:
    market_open = True
    if today_weekday == 0:
        yesterday_formatted = (today - timedelta(days=days_to_subtract + 2)).strftime("%Y-%m-%d")
        yesterday_weekday = (today - timedelta(days=days_to_subtract + 2)).weekday()
        day_before_yesterday_formatted = (today - timedelta(days=days_to_subtract + 3)).strftime("%Y-%m-%d")
        day_before_yesterday_weekday = (today - timedelta(days=days_to_subtract + 3)).weekday()
    if today_weekday == 1:
        day_before_yesterday_formatted = (today - timedelta(days=days_to_subtract + 3)).strftime("%Y-%m-%d")
        day_before_yesterday_weekday = (today - timedelta(days=days_to_subtract + 3)).weekday()
else:
    market_open = False
