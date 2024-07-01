import aiohttp
import asyncio
from bs4 import BeautifulSoup


# Function to get article titles, time tags, and ticker symbols from a single page
async def get_articles_from_page(url, session):
    async with session.get(url) as response:
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            articles = []

            # Find all article items in the stream
            stream_items = soup.find_all('li', class_='stream-item svelte-7rcxn')
            for item in stream_items:
                headline = item.find('h3', class_='clamp svelte-w27v8j')
                time_tag = item.find('div', class_='publishing font-condensed svelte-1k3af9g')
                ticker_symbol = item.find('span', class_='symbol svelte-1ts22zv')

                if headline and time_tag and ticker_symbol:
                    title = headline.get_text()
                    time = time_tag.get_text()
                    symbol = ticker_symbol.get_text()

                    # Extract the time part correctly
                    time_stamp = time.split(" • ")
                    if len(time_stamp) > 1:
                        time_stamp = time_stamp[1]
                    else:
                        time_stamp = time_stamp[0]

                    formatted_article = (title, time_stamp, symbol)
                    articles.append(formatted_article)

            return articles
        else:
            print(f"Failed to retrieve the page. Status code: {response.status}")
            return []


# Function to scrape multiple pages concurrently using asyncio
async def scrape_multiple_pages_concurrently(base_url, num_pages, batch_size=10):
    urls = [f"{base_url}?offset={page_num * 10}" for page_num in range(1, num_pages + 1)]

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        all_articles = []
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            tasks = [get_articles_from_page(url, session) for url in batch]
            results = await asyncio.gather(*tasks)
            all_articles.extend([article for articles in results for article in articles])

    return all_articles


# Base URL of the Yahoo Finance News
base_url = "https://finance.yahoo.com/news"

# Scrape headlines, time tags, and ticker symbols from the first 40 pages concurrently (adjust as needed)
all_articles = asyncio.run(scrape_multiple_pages_concurrently(base_url, 100, batch_size=25))

# Print the total number of articles and the first article with time tag and ticker symbol
print(f"Total articles scraped: {len(all_articles)}")
if all_articles:
    print(f"First article: {all_articles[0]}")
