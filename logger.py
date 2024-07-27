import logging
import csv
import datetime

# Custom logging filter to add custom attributes to log records
class CustomFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'ticker'):
            record.ticker = ''
        if not hasattr(record, 'body_sentiment'):
            record.body_sentiment = ''
        if not hasattr(record, 'trend_sentiment'):
            record.trend_sentiment = ''
        return True

# Custom formatter to add separators and centered timestamp
class CustomFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        centered_timestamp = f"{timestamp:^80}"
        separator = '=' * 80
        log_entry = super().format(record)
        return f"\n\n{separator}\n{centered_timestamp}\n{separator}\n{log_entry}\n{separator}\n\n"

# Configure the logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create file handler
fh = logging.FileHandler('sentiment_analysis.log')
fh.setLevel(logging.INFO)

# Create and set custom formatter
formatter = CustomFormatter('%(ticker)s - Body Sentiment: %(body_sentiment)s - Trend Sentiment: %(trend_sentiment)s')
fh.setFormatter(formatter)

# Add filter and handler to logger
logger.addFilter(CustomFilter())
logger.addHandler(fh)

def log_sentiments(csv_file):
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            logger.info('Processing sentiment data',
                        extra={'ticker': row['Quote'], 'body_sentiment': row['Body Sentiment'], 'trend_sentiment': row['Trend Sentiment']})

if __name__ == "__main__":
    log_sentiments('news_data_with_sentiments.csv')
