import yfinance as yf
import numpy as np


def calculate_volatility_yahoo(ticker, period='1y', window=252):
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
    print(np.std(log_returns.iloc[-window:]))
    print(np.sqrt(window))

    # Compute rolling volatility
    rolling_volatility = np.std(log_returns.iloc[-window:]) * np.sqrt(window)
    print(rolling_volatility)

    return rolling_volatility


calculate_volatility_yahoo('SISI', window=252)

