import pandas as pd
import time
import concurrent.futures
from finvizfinance.quote import finvizfinance
import fv_screener_processor
from stock_ch import extract_change
from sentiment import body_sentiment, stock_statistical_values
from visual import visualize_correlation


def input_date(prompt):
    while True:
        try:
            return input(f"{prompt} (format: YYYY-MM-DD): ")
        except ValueError:
            print("Invalid format. Please enter the date in YYYY-MM-DD format.")


class NewsProcessor:
    def __init__(self, start_date, end_date):
        self.sentiment_of_change = {}
        self.client = finvizfinance
        self.start_date = start_date
        self.end_date = end_date

    def get_news_data(self, ticker):
        try:
            stock = self.client(ticker)
            news_df = stock.ticker_news()
            news_df['Quote'] = ticker
            time.sleep(2)
            return news_df
        except Exception as e:
            print(f"An error occurred while fetching news for {ticker}: {e}")
            return pd.DataFrame()

    def fetch_news(self, quotes):
        news_data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(self.get_news_data, q): q for q in quotes}
            for future in concurrent.futures.as_completed(futures):
                try:
                    news_data.extend(future.result().to_dict('records'))
                except Exception as e:
                    print(f"Error fetching news for {futures[future]}: {e}")
        return news_data

    def fetch_trend_sentiments(self, quotes):
        for quote in quotes:
            try:
                change = extract_change(quote)
                self.sentiment_of_change[quote] = stock_statistical_values(change, quote)
            except Exception as e:
                print(f"Error fetching trend sentiment for {quote}: {e}")

    def process_news_data(self, news_data):
        if not news_data:
            return pd.DataFrame()

        news_df = pd.DataFrame(news_data)
        news_df['Date'] = news_df['Date'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        news_df = news_df[(news_df['Date'] >= self.start_date) & (news_df['Date'] <= self.end_date)]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(body_sentiment, link): link for link in news_df['Link']}
            for future in concurrent.futures.as_completed(futures):
                link = futures[future]
                try:
                    news_df.loc[news_df['Link'] == link, 'Body Sentiment'] = future.result()
                except Exception as e:
                    print(f"Error processing sentiment for Link {link}: {e}")
                    news_df.loc[news_df['Link'] == link, 'Body Sentiment'] = None

        news_df['Trend Sentiment'] = news_df['Quote'].apply(lambda q: self.sentiment_of_change.get(q, None))
        news_df['Trend Sentiment'] = news_df['Trend Sentiment'].fillna(0.00)
        news_df['Date'] = pd.to_datetime(news_df['Date'])

        return news_df[['Date', 'Quote', 'Link', 'Body Sentiment', 'Trend Sentiment']]

    def run(self, quotes, interval=600):
        while True:
            news_data = self.fetch_news(quotes)
            self.fetch_trend_sentiments(quotes)
            if news_data:
                processed_df = self.process_news_data(news_data)
                # print(processed_df)
                processed_df.to_csv('news_data_with_sentiments.csv', index=False)
                visualize_correlation('news_data_with_sentiments.csv')
                print("News data with sentiments saved to news_data_with_sentiments.csv")
            time.sleep(interval)


if __name__ == "__main__":
    start_date = "2024-07-19"
    end_date = "2024-07-22"
    quotes = fv_screener_processor.tickers
    processor = NewsProcessor(start_date, end_date)
    processor.run(quotes)
