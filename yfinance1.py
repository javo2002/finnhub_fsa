import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_top_daily_tickers():
    url = "https://finance.yahoo.com/gainers"  # URL for Yahoo Finance's top gainers page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    table = soup.find('table', {'class': 'W(100%)'})  # Locate the table with top gainers
    print(table)
    rows = table.find_all('tr')[1:]  # Skip the header row

    ticker_data = []
    for row in rows:
        cols = row.find_all('td')
        ticker = cols[0].text.strip()
        close_price = float(cols[2].text.strip().replace(',', ''))
        percent_change = float(cols[4].text.strip().replace('%', ''))
        ticker_data.append((ticker, close_price, percent_change))

    # Convert the list to a DataFrame
    df = pd.DataFrame(ticker_data, columns=['Ticker', 'Close Price', 'Percentage Change'])
    return df

if __name__ == "__main__":
    top_tickers = get_top_daily_tickers()
    print(top_tickers)
