import yfinance as yf
import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def get_oslo_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Oslo_Stock_Exchange'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'html.parser')

    table = soup.find('table', {'class': 'wikitable sortable'})
    rows = table.find_all('tr')

    symbols = []

    for row in rows[1:]:  # skip the header row
        cells = row.find_all('td')
        symbol = cells[1].text.strip()
        symbols.append(symbol.replace("OSE: ", "") + '.OL')

    return symbols

async def get_stock_info(symbol, stocks):
    try:
        stock = yf.Ticker(symbol)
        stocks.append(stock.info)
    except Exception as e:
        print(f"Error with {symbol}: {e}")

async def main(stocks):
    symbols = await get_oslo_tickers()
    print(symbols)

    tasks = [get_stock_info(symbol, stocks) for symbol in symbols]
    await asyncio.gather(*tasks)
    return stocks

if __name__ == "__main__":
    stocks = []
    asyncio.run(main(stocks))
