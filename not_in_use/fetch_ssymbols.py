import requests
from bs4 import BeautifulSoup
import concurrent.futures


# Function to get a list of stock symbols from a source (example: scraping NASDAQ)
def get_stock_symbols():
    # Example source for scraping stock symbols; replace with a reliable source if needed
    url = "https://raw.githubusercontent.com/dhhagan/stocks/master/scripts/stock_info.csv"
    response = requests.get(url)
    print(response.status_code)
    symbols = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'market tab1'})
        for row in table.find_all('tr')[1:]:
            symbol = row.find('td').get_text()
            symbols.append(symbol)
    else:
        print(f"Failed to retrieve stock symbols. Status code: {response.status_code}")
    return symbols


# Function to get article titles and stock changes from a single page
def get_articles_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all('h3', class_='clamp  svelte-j87knz')
        stock_changes = soup.find_all('span', class_='e3b14781 ee3e99dd')

        articles = []
        for headline, stock_change in zip(headlines, stock_changes):
            articles.append({
                'headline': headline.get_text(),
                'stock_change': stock_change.get_text()
            })
        return articles
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []


# Function to scrape multiple pages concurrently for a specific stock symbol
def scrape_multiple_pages_concurrently(stock_symbol, num_pages):
    base_url = f"https://finance.yahoo.com/quote/{stock_symbol}/news"
    urls = [f"{base_url}?offset={page_num * 10}" for page_num in range(num_pages)]
    all_articles = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(get_articles_from_page, urls))

    for articles in results:
        all_articles.extend(articles)
        if not articles:
            break  # Stop if no more articles are found

    return all_articles


# Get the list of stock symbols (e.g., from NASDAQ)
stock_symbols = get_stock_symbols()

# Number of pages to scrape for each stock symbol
num_pages = 3

# Scrape articles for each stock symbol
all_scraped_articles = []

for stock_symbol in stock_symbols:
    print(f"Scraping news for {stock_symbol}...")
    articles = scrape_multiple_pages_concurrently(stock_symbol, num_pages)
    all_scraped_articles.append({
        'stock_symbol': stock_symbol,
        'articles': articles
    })
    print(f"Total articles scraped for {stock_symbol}: {len(articles)}")
    for article in articles:
        print(f"Headline: {article['headline']}, Stock Change: {article['stock_change']}")

# Optionally, save the articles to a file
# with open("yahoo_finance_stock_news.json", "w", encoding="utf-8") as file:
#     json.dump(all_scraped_articles, file, ensure_ascii=False, indent=4)
