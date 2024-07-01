import requests
import pandas as pd
import time
import finnhub
import concurrent.futures
from fetch_body import get_body
from sentiment import sentiment_analyzer


def fetch_sentiment(article_body):
    return sentiment_analyzer(article_body)


# Function to process a single article and add the quote
def process_article(article, quote):
    try:
        source = article['source']
        title = article['headline']
        date = article['datetime']
        return {
            "Title": title,
            "Date": date,
            "Quote": quote,
            "Source": source
        }
    except Exception as e:
        print(f"Error processing article: {e}")
        return None


# Function to fetch news from FINHub API for a single quote
def fetch_news_for_quote(api_key, quote, start_date, end_date):
    try:
        finnhub_client = finnhub.Client(api_key=api_key)
        news_data = finnhub_client.company_news(quote, _from=start_date, to=end_date)
        print(f"Fetched {len(news_data)} articles for {quote}")
        for article in news_data:
            article['quote'] = quote  # Add the quote to each article
        return news_data
    except Exception as e:
        print(f"Error fetching news for {quote}: {e}")
        return []


# Function to fetch news from FINHub API for different quotes using concurrent futures
def fetch_news_from_finhub(api_key, quotes, start_date="2024-06-01", end_date="2024-06-02"):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_news_for_quote, api_key, quote, start_date, end_date) for quote in quotes]
        all_news_data = []
        for future in concurrent.futures.as_completed(futures):
            all_news_data.extend(future.result())
    return all_news_data


# Function to fetch body paragraphs and analyze sentiments using concurrent futures
# def fetch_body_and_sentiment(articles):
#     results = []
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = [executor.submit(fetch_body_and_sentiment_single, article) for article in articles]
#
#         for future in concurrent.futures.as_completed(futures):
#             result = future.result()
#             if result:
#                 results.append(result)
#     return results


def fetch_body_and_sentiment_single(article):
    try:
        title_str = str(article['Title'])
        source_str = str(article['Source'])
        x = title_str + ' ' + source_str
        body = get_body(x)
        sentiment_score = fetch_sentiment(body)
        return {
            "Title": article['Title'],
            "Date": article['Date'],
            "Quote": article['Quote'],
            "Source": article['Source'],
            "Sentiment": sentiment_score
        }
    except Exception as e:
        print(f"Error fetching body and sentiment: {e}")
        return None


# Main function to run the news fetching process
def main():
    api_key = 'cpmethpr01quf620vds0cpmethpr01quf620vdsg'  # Replace with your actual API key
    quotes = ['AAPL', 'TSLA', 'NVDA']  # List of company quotes
    news_data = fetch_news_from_finhub(api_key, quotes)

    if news_data:
        processed_articles = [process_article(article, article['quote']) for article in news_data if article]
        df = pd.DataFrame(processed_articles)
        pd.set_option('display.max_colwidth', None)  # Expand df to the total view of columns
        pd.set_option('display.max_columns', None)
        df['Date'] = pd.to_datetime(df['Date'], unit='s')

        # results = fetch_body_and_sentiment(processed_articles)

        # df_results = pd.DataFrame(results)
        print(df)
        df.to_csv('news_data_with_sentiments.csv', index=False)
        print("News data with sentiments saved to news_data_with_sentiments.csv")


if __name__ == "__main__":
    main()
