from datetime import datetime, timedelta
import yfinance as yf


today = datetime.today().date()
yesterday = today - timedelta(days=1)
stock_data = yf.download("meta", start=yesterday, end=today,  progress=False)


open_price = stock_data.iloc[-1]['Open']

close_price = stock_data.iloc[-1]['Close']

change_percent = ((close_price - open_price) / open_price) * 100

print(change_percent)

# Load and display the content of the file
file_path = '/mnt/data/sentiment_tester.py'