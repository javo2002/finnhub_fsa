import redis
import re
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import time
from yah_scrape import scrape_multiple_pages_concurrently
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import concurrent.futures
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL of the Yahoo Finance News
base_url = "https://finance.yahoo.com/news"

# Redis configuration
redis_host = 'localhost'
redis_port = 6379
channel_name = 'news_sentiment'

# Initialize Redis client
try:
    r = redis.Redis(host=redis_host, port=redis_port)
    r.ping()  # Check connection
    logging.info("Connected to Redis!")
except redis.ConnectionError as e:
    logging.error(f"Redis connection error: {e}")
    exit(1)

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()


# Function to clean text
def clean_text(text):
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return text


# Function to analyze sentiment
def sentiment_analyzer(sentiment_text):
    cleaned_text = clean_text(sentiment_text)
    score = sid.polarity_scores(cleaned_text)
    return 'Positive' if score['compound'] > 0 else 'Negative'


# Function to publish messages to Redis
def publish_to_redis(channel, message):
    try:
        r.publish(channel, message)
        logging.info("Published message to Redis")
    except Exception as e:
        logging.error(f"Error publishing to Redis: {e}")


# Function to process a single article
def process_article(article):
    try:
        head, time, symbol = article
        sentiment_score = sentiment_analyzer(head)
        return {
            "Headline": head,
            "Time": time,
            "Sentiment Score": sentiment_score,
            "Symbol": symbol,
        }
    except Exception as e:
        logging.error(f"Error processing article: {e}")
        return None


# Function to fetch news and process sentiment
def fetch_and_process_news(channel):
    try:
        all_articles = asyncio.run(scrape_multiple_pages_concurrently(base_url, 10, batch_size=20))
        logging.info(f"Fetched {len(all_articles)} articles")

        # Process articles to get initial data
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            initial_results = list(executor.map(process_article, all_articles))

        # Filter out None results from processing
        initial_results = [result for result in initial_results if result is not None]

        logging.info(f"Processed {len(initial_results)} articles")

        # Create DataFrame from initial results
        df = pd.DataFrame(initial_results)

        # Publish DataFrame to Redis
        message = df.to_json(orient='records')
        publish_to_redis(channel, message)

        # Save DataFrame to a CSV file
        df.to_csv('news_sentiment_analysis.csv', index=False)

        # Print the DataFrame
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)
        logging.info(df)
    except Exception as e:
        logging.error(f"Error in fetch_and_process_news: {e}")


# Main loop to simulate real-time updates
def main():
    while True:
        fetch_and_process_news(channel_name)
        time.sleep(3600)  # Wait for 1 hour before fetching news again


if __name__ == "__main__":
    main()
