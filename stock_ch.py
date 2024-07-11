import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

def calculate_trend(ticker_symbol):
    print(ticker_symbol)
    today = datetime.today().date()
    today_str = str(today)
    yesterday = datetime.today().date() - timedelta(days=1)
    yesterday_str = str(yesterday)

    # Download minute-level data for today
    stock_today = yf.download(ticker_symbol, start=today_str, end=None, interval='1m', progress=False)
    # print(stock_today)
    # Download minute-level data for yesterday
    stock_yesterday = yf.download(ticker_symbol, start=yesterday_str, end=None, interval='1m', progress=False)
    # print(stock_yesterday)
    if not stock_today.empty and not stock_yesterday.empty:
        stock_today = stock_today.iloc[-1]
        current_price = stock_today['Close']

        stock_yesterday = stock_yesterday[stock_yesterday.index.date == yesterday].tail().iloc[-1]
        closing_price = stock_yesterday['Close']

        # print("Closing price from yesterday:")
        # print(closing_price)
        # print("Current Price:")
        # print(current_price)

        percent_change = (current_price - closing_price) / closing_price * 100
        # print(f"Percent Change:{percent_change}")
        return round(percent_change, 2)

    else:
        print("No data retrieved for given dates.")

# calculate_trend("VRPX")

def calculate_volatility(ticker, period='1y', window=252):
    """
    Calculate the historical volatility of a stock using Yahoo Finance data.

    Parameters:
    ticker (str): Ticker symbol of the stock.
    period (str): Period for which to fetch historical data (e.g., '1y' for 1 year).
    window (int): Number of trading days to calculate the rolling volatility (default is 252 for 1 year).

    Returns:
    float: Historical volatility value.
    """
    stock_data = yf.Ticker(ticker)
    hist_data = stock_data.history(period=period)

    # Calculate log returns
    close_prices = hist_data['Close']
    log_returns = np.log(close_prices / close_prices.shift(1))

    # Compute rolling volatility
    rolling_volatility = np.std(log_returns.iloc[-window:]) * np.sqrt(window)


    return rolling_volatility