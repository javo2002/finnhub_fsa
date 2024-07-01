import re
import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
def clean_text(text):
    # Remove special characters
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return text

# Function to analyze sentiment
def sentiment_analyzer(text):
    cleaned_text = clean_text(text)
    score = sia.polarity_scores(cleaned_text)
    return 'Positive' if score['compound'] > 0 else 'Negative'

def num_sentiment_analyzer(num):
    score = sia.polarity_scores(num)
    return score

def body_sentiment(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraphs = soup.find_all('p')
    combined_text = " ".join([p.get_text() for p in paragraphs])
    return sentiment_analyzer(combined_text)

# print(body_sentiment('https://finnhub.io/api/news?id=704bafa163722911e753ed7aeffba53084c83b7e16412886796f5310d5ca4d2e'))
num = "There was a drop in the company's stock price, which fell by 3.5% over the past hour"

# print(num_sentiment_analyzer(num))


def adjust_sentiment_for_number(sentiment_score, number):
    # Custom adjustment logic
    if number > 0:
        sentiment_score['compound'] += min(0.1 * number, 1.0)  # Adjust positively
    else:
        sentiment_score['compound'] += max(0.1 * number, -1.0)  # Adjust negatively

    # Ensure compound score stays within -1 to 1
    sentiment_score['compound'] = max(min(sentiment_score['compound'], 1.0), -1.0)
    return sentiment_score['compound']

# Example sentences with numerical context

def prcnt_input(num):
    if num > 0:
        sentence = f"There was a rise in the company's stock price, which increased by {num}% over the past hour"
    elif num < 0:
        sentence = f"There was a drop in the company's stock price, which fell by {num}% over the past hour"
    else:
        return None

    # Analyze the sentiment
    sentiment_scores = sia.polarity_scores(sentence)

    # Adjust sentiment score based on the numerical value
    adjusted_sentiment_scores = adjust_sentiment_for_number(sentiment_scores, num)

    return adjusted_sentiment_scores

# sentiment starting point for stock change developed headline:
# for positive headline: 0.2732,
# for negative headline: -0.2732

# .1x*(+-0.2732) = Updates sentiment
