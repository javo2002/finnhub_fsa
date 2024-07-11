import requests
import pandas as pd
import time
import finnhub
import concurrent.futures
from stock_ch import calculate_trend, calculate_volatility
from sentiment import body_sentiment, stock_statistical_values
from datetime import datetime, timezone
from visual import visualize_correlation
import pytz

class NewsProcessor:
    def __init__(self, api_key, start_date, end_date):
        """Initialize key parameters."""
        self.api_key = api_key
        self.start_date = start_date
        self.end_date = end_date
        self.finnhub_client = finnhub.Client(api_key=api_key)
        self.sentiment_of_change = {}

    def fetch_company_news(self, quote):
        """Fetch company news data through API call with specified parameters."""
        try:
            news_data = self.finnhub_client.company_news(quote, _from=self.start_date, to=self.end_date)
            print(f"Fetched {len(news_data)} articles for {quote}")
            for article in news_data:
                article['quote'] = quote
            return news_data
        except Exception as e:
            print(f"Error fetching news for {quote}: {e}")
            return []

    def fetch_news(self, quotes):
        """Retrieve news data from multiple quotes using concurrent execution."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.fetch_company_news, quote) for quote in quotes]
            all_news_data = []
            for future in concurrent.futures.as_completed(futures):
                all_news_data.extend(future.result())
        return all_news_data

    def stock_trend_sentiments(self, quotes):
        """Update sentiments based on stock price changes."""
        for quote in quotes:
            percent_change = calculate_trend(quote)
            sentiment = stock_statistical_values(percent_change)
            self.sentiment_of_change[quote] = sentiment

    def calculate_stock_volatility(self, quote):
        """Calculate volatility for a given stock quote within the date range."""
        try:
            volatility = calculate_volatility(quote)
            return volatility
        except Exception as e:
            print(f"Error calculating volatility for {quote}: {e}")
            return None

    def process_news_and_sentiments(self, news_data):
        """Process news data and update sentiments."""
        if not news_data:
            return pd.DataFrame()

        # Find the most recent article
        most_recent_article = min(news_data, key=lambda x: x['datetime'])
        formatted_article = self.format_news_article(most_recent_article)

        if not formatted_article:
            return pd.DataFrame()

        df = pd.DataFrame([formatted_article])
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(self.extract_sentiment_from_url, row['URL']): row['URL'] for _, row in df.iterrows()}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    body_sentiment_result = future.result()
                    if body_sentiment_result:
                        quote = df.loc[df['URL'] == url, 'Quote'].values[0]
                        trend_sentiment = self.sentiment_of_change[quote]
                        volatility = self.calculate_stock_volatility(quote)
                        df.loc[df['URL'] == url, 'Body Sentiment'] = body_sentiment_result
                        df.loc[df['URL'] == url, 'Trend Sentiment'] = trend_sentiment
                        df.loc[df['URL'] == url, 'Volatility'] = volatility
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")

        # Format DataFrame to show only the required columns
        df = df[['Date', 'Quote', 'URL', 'Body Sentiment', 'Trend Sentiment', 'Volatility']]
        return df

    def run(self, quotes, interval=120):
        """Main method to run the news processing loop."""
        while True:
            news_data = self.fetch_news(quotes)
            self.stock_trend_sentiments(quotes)

            if news_data:
                df = self.process_news_and_sentiments(news_data)
                print(df)
                df.to_csv('news_data_with_sentiments.csv', mode='w', index=False)
                visualize = visualize_correlation('news_data_with_sentiments.csv')
                print(f'Stock price changes over the last hour: {self.sentiment_of_change}')
                print("News data with sentiments saved to news_data_with_sentiments.csv")

            time.sleep(interval)

    def extract_sentiment_from_url(self, url):
        """Process a single URL to extract sentiment."""
        try:
            return body_sentiment(url)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return None

    def format_news_article(self, article):
        """Format a single news article for DataFrame storage."""
        try:
            title = article['headline']
            date_utc = datetime.fromtimestamp(article['datetime'], tz=timezone.utc)  # Convert timestamp to UTC datetime
            date_est = date_utc.astimezone(pytz.timezone('US/Eastern'))  # Convert UTC to EST
            url = article['url']
            quote = article['quote']
            return {
                "Title": title,
                "Date": date_est.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
                "Quote": quote,
                "URL": url
            }
        except Exception as e:
            print(f"Error processing article: {e}")
            return None


if __name__ == "__main__":
    api_key = 'cpmethpr01quf620vds0cpmethpr01quf620vdsg'
    quotes = ['LCFY']
    start_date = "2024-06-01"
    end_date = "2024-07-11"
    processor = NewsProcessor(api_key, start_date, end_date)
    processor.run(quotes)
