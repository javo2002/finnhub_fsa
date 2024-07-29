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
    return score['compound']


def body_sentiment(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraphs = soup.find_all('p')
    combined_text = " ".join([p.get_text() for p in paragraphs])
    return sentiment_analyzer(combined_text)


def adjust_sentiment_for_number(sentiment_score, percentage):
    # Custom adjustment logic
    trend_factor = 0.01  # Base adjustment factor for trend
    if percentage > 0:
        sentiment_score['compound'] = 0.1
        sentiment_score['compound'] += min(trend_factor * percentage, 1.0)  # Adjust positively
    else:
        sentiment_score['compound'] = -0.1
        sentiment_score['compound'] += max(trend_factor * percentage, -1.0)  # Adjust negatively
    # sentiment_score['compound'] += min(volatility * volatility_factor, 0.5)

    # Ensure compound score stays within -1 to 1
    sentiment_score['compound'] = max(min(sentiment_score['compound'], 1.0), -1.0)
    # print(f'Sentiment score of : {sentiment_score}')
    return sentiment_score['compound']


def stock_statistical_values(percentage, quote):
    # print('Higher volatility indicates stock is more likely to swing; recommended for short-term investments')
    # print('Lower volatility indicates stock is less likely to swing; recommended for long-term investments')
    if percentage > 0:
        sentence = f"There was a rise in the {quote}'s stock price, which increased by {percentage}% for today's current trading period"
    elif percentage < 0:
        sentence = f"There was a drop in the {quote}'s stock price, which fell by {percentage}% for today's currenttrading period"
    else:
        return None
    print(sentence)

    # Analyze the sentiment
    sentiment_scores = sia.polarity_scores(sentence)
    # Adjust sentiment score based on the stock change value
    adjusted_sentiment_scores = adjust_sentiment_for_number(sentiment_scores, percentage)

    return adjusted_sentiment_scores
