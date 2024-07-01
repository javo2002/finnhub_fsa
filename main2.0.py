import requests
import pandas as pd
import time
import finnhub
import concurrent.futures
from stock_ch import change_output
from sentiment import body_sentiment, prcnt_input
from datetime import datetime, timezone
import pytz
from transformers import pipeline
import torch

class NewsProcessor:
    def __init__(self, api_key, start_date, end_date):
        """Initialize key parameters."""
        self.api_key = api_key
        self.start_date = start_date
        self.end_date = end_date
        self.finnhub_client = finnhub.Client(api_key=api_key)
        self.sentiment_of_change = {}

        # Check if GPU is available and set the device accordingly
        device = 0 if torch.cuda.is_available() else -1
        self.sentiment_analyzer = pipeline('sentiment-analysis', model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", device=device)

    def fetch_news_for_quote(self, quote):
        """Fetch data through API call with specified parameters."""
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
        """Retrieve data from multiple quotes using concurrent execution."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.fetch_news_for_quote, quote) for quote in quotes]
            all_news_data = []
            for future in concurrent.futures.as_completed(futures):
                all_news_data.extend(future.result())
        return all_news_data

    def update_sentiment_of_change(self, quotes):
        """Update the sentiment based on stock price changes."""
        for quote in quotes:
            prcnt_change = change_output(quote)
            sentiment = prcnt_input(prcnt_change)
            self.sentiment_of_change[quote] = sentiment

    def process_news_data(self, news_data):
        """Process the news data and update sentiments."""
        if not news_data:
            return pd.DataFrame()

        # Find the most recent article
        most_recent_article = min(news_data, key=lambda x: x['datetime'])
        formatted_article = format_article(most_recent_article)

        if not formatted_article:
            return pd.DataFrame()

        df = pd.DataFrame([formatted_article])
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(process_url, row['URL']): row['URL'] for _, row in df.iterrows()}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    if data:
                        quote = df.loc[df['URL'] == url, 'Quote'].values[0]
                        adjusted_sentiment = adjust_sentiment(data, self.sentiment_of_change[quote])
                        df.loc[df['URL'] == url, 'Sentiment'] = adjusted_sentiment
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")

        # Format DataFrame to show only the required columns
        df = df[['Date', 'Quote', 'URL', 'Sentiment']]
        return df

    def run(self, quotes, interval=120):
        """Main method to run the news processing loop."""
        while True:
            news_data = self.fetch_news(quotes)
            self.update_sentiment_of_change(quotes)

            if news_data:
                df = self.process_news_data(news_data)
                print(df)
                df.to_csv('news_data_with_sentiments.csv', index=False)
                print(f'Stock price changes over the last hour: {self.sentiment_of_change}')
                print("News data with sentiments saved to news_data_with_sentiments.csv")

            time.sleep(interval)


def process_url(url):
    """Process a single URL to extract sentiment."""
    try:
        article_text = body_sentiment(url)  # Assuming body_sentiment fetches and returns the article text
        sentiment_result = processor.sentiment_analyzer(article_text[:512])  # Process only the first 512 characters
        sentiment = sentiment_result[0]['label']
        return sentiment
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None


def format_article(article):
    """Format a single news article for DataFrame storage."""
    try:
        title = article['headline']
        date_utc = datetime.fromtimestamp(article['datetime'], tz=timezone.utc)  # Convert timestamp to UTC datetime
        date_est = date_utc.astimezone(pytz.timezone('US/Eastern'))  # Convert UTC to EST
        print(date_utc)
        print(date_est)
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


def adjust_sentiment(sentiment, change):
    """Adjust sentiment based on stock price change."""
    if sentiment == 'Negative' and change < -0.3:
        return 'Negative'
    elif sentiment == 'Positive' and change < -0.3:
        return 'Negative'
    elif sentiment == 'Negative' and change > 0.3:
        return 'Positive'
    elif sentiment == 'Positive' and change > 0.3:
        return 'Positive'
    return sentiment


if __name__ == "__main__":
    api_key = 'cpmethpr01quf620vds0cpmethpr01quf620vdsg'
    quotes = ['NNE']  # Assuming 'AREB' is the ticker for American Rebel
    start_date = "2024-06-28"
    end_date = "2024-06-28"
    processor = NewsProcessor(api_key, start_date, end_date)
    processor.run(quotes)
