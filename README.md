# Finnhub Financial Sentiment Analysis

This project is designed to fetch company news data, process it for sentiment analysis, calculate stock trends and volatility, and visualize the correlation between these factors. The code is written in Python and leverages several libraries including `pandas`, `finnhub`, `concurrent.futures`, and `pytz`.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Configuration](#configuration)
4. [Understanding the Code](#understanding-the-code)
5. [License](#license)

## Installation

To get started with this project, you need to have Python installed on your machine. Follow these steps to set up the project:

1. **Clone the Repository:**

```bash
git clone https://github.com/javo2002/finnhub_fsa.git
cd finnhub_fsa
```

2. **Install Required Packages:**

```bash
pip install requests pandas finnhub-python concurrent.futures pytz
```

## Usage

To run the news processing and sentiment analysis, follow these steps:

1. **Set API Key and Date Range:**

   Open the `main.py` file and update the `api_key`, `start_date`, and `end_date` variables:

```python
api_key = 'YOUR_FINNHUB_API_KEY'
quotes = ['AAPL']  # Change to desired ticker symbols
start_date = "yyyy-mm-dd"  # Start date in Year-Month-Day format
end_date = "yyyy-mm-dd"    # End date in Year-Month-Day format
```

2. **Run the Script:**

   Execute the script using Python:

```bash
python main.py
```

## Configuration

Here are the key parameters you need to configure:

- `api_key`: Your Finnhub API key.
- `quotes`: A list of stock ticker symbols you want to analyze.
- `start_date`: The start date for fetching news articles (format: yyyy-mm-dd).
- `end_date`: The end date for fetching news articles (format: yyyy-mm-dd).

## Understanding the Code

### Key Components

1. **Imports and Class Initialization:**

   The necessary libraries are imported and the `NewsProcessor` class is initialized with key parameters.

```python
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
```

2. **Fetching Company News:**

   The `fetch_company_news` method retrieves news articles for a given stock ticker symbol within the specified date range.

```python
def fetch_company_news(self, quote):
    ...
```

3. **Concurrent News Fetching:**

   The `fetch_news` method retrieves news data for multiple stock ticker symbols concurrently.

```python
def fetch_news(self, quotes):
    ...
```

4. **Stock Trend and Sentiment Calculation:**

   The `stock_trend_sentiments` method updates the sentiment based on stock price changes.

```python
def stock_trend_sentiments(self, quotes):
    ...
```

5. **Calculating Stock Volatility:**

   The `calculate_stock_volatility` method calculates the volatility for a given stock ticker symbol.

```python
def calculate_stock_volatility(self, quote):
    ...
```

6. **Processing News and Sentiments:**

   The `process_news_and_sentiments` method processes the fetched news data and updates the sentiments.

```python
def process_news_and_sentiments(self, news_data):
    ...
```

7. **Main Execution Loop:**

   The `run` method contains the main loop that periodically fetches and processes news data.

```python
def run(self, quotes, interval=120):
    ...
```

8. **Helper Methods:**

   - `extract_sentiment_from_url`: Extracts sentiment from a given URL.
   - `format_news_article`: Formats a news article for DataFrame storage.

```python
def extract_sentiment_from_url(self, url):
    ...

def format_news_article(self, article):
    ...
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

---
