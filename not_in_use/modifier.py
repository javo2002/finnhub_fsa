# import yfinance as yf
# import pandas as pd
# from datetime import datetime, timedelta
# import time
#
# today = datetime.today().date()
# today_str = str(today)
# yesterday = datetime.today().date() - timedelta(days=1)
# yesterday_str = str(yesterday)
#
#
# # Define the ticker symbol and today's start date
# ticker_symbol = 'SNGX'
#
#
# # Download minute-level data for today
# stock_today = yf.download(ticker_symbol, start=today_str, end=None, interval='1m', progress=False)
#
#
# # Download minute-level data for yesterday
# stock_yesterday = yf.download(ticker_symbol, start=yesterday_str, end=None, interval='1m', progress=False)
#
# if not stock_today.empty and not stock_yesterday.empty:
#     stock_today = stock_today.iloc[-1]
#     current_price = stock_today['Close']
#
#     stock_yesterday = stock_yesterday[stock_yesterday.index.date == yesterday].tail().iloc[-1]
#     closing_price = stock_yesterday['Close']
#
#     print("Closing price from yesterday:")
#     print(closing_price)
#     print("Current Price:")
#     print(current_price)
#
#     percent_change = (current_price - closing_price) / closing_price * 100
#     print(f"Percent Change:{percent_change}")
#
# else:
#     print("No data retrieved for given dates.")