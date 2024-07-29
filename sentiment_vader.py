import re
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

    adjusted_sentiment = sentiment_score # Sentiment score (+ or -) refers to the sentence variable.

    #Adjust the starting sentiment and ensure positive and negative percentages have the same absolute starter sentiment value

    if percentage > 0:
        adjusted_sentiment = 0.1
        adjusted_sentiment += min(trend_factor * percentage, 1.0)
    else:
        adjusted_sentiment = -0.1
        adjusted_sentiment += max(trend_factor * percentage, -1.0)  # Adjust negatively

    # Ensure compound score stays within -1 to 1
    adjusted_sentiment = max(min(adjusted_sentiment, 1.0), -1.0)

    return round(adjusted_sentiment, 4)


def stock_statistical_values(percentage, quote):
    if percentage > 0:
        sentence = f"There was a rise in the {quote}'s stock price, which increased by {percentage}% for today's current trading period"
    elif percentage < 0:
        sentence = f"There was a drop in the {quote}'s stock price, which fell by {percentage}% for today's current trading period"
    else:
        return None
    print(sentence)

    # Analyze the sentiment
    sentiment_scores = sia.polarity_scores(sentence)

    # Adjust sentiment score based on the stock change value
    adjusted_sentiment_score = adjust_sentiment_for_number(sentiment_scores['compound'], percentage)

    return adjusted_sentiment_score

# Example usage:
# print(stock_statistical_values(0.99, 'AAPL'))