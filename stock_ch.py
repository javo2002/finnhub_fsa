import yfinance as yf
import time

# Function to get the current stock price and calculate change
def get_stock_change(ticker_symbol):
    try:
        # Download the stock data with 1-hour intervals for the last day
        stock = yf.download(ticker_symbol, period='1mo', interval='1d', progress=False)

        # Get the current price and the previous price
        current_price = stock['Close'].iloc[-1]
        previous_price = stock['Close'].iloc[-2]

        # Calculate the stock change
        stock_change = current_price - previous_price
        stock_change_percentage = (stock_change / previous_price) * 100

        return current_price, stock_change, stock_change_percentage
    except Exception as e:
        return None, None, str(e)


# Infinite loop to get stock updates every 5 minutes
def change_output(ticker_symbol):
    while True:
        current_price, stock_change, stock_change_percentage = get_stock_change(ticker_symbol)
        if current_price is not None:
            return round(stock_change_percentage,2)
        else:
            print(f"Error fetching stock data: {stock_change_percentage}")


print(change_output("AAPL"))