# data_fetcher.py

from yahooquery import Ticker
import pandas as pd


def fetch_stock_data(symbols, time_range):
    stock_data = []
    history_data = {}

    for symbol in symbols:
        ticker = Ticker(symbol)
        info = ticker.summary_detail[symbol]
        history = ticker.history(period=time_range)

        stock_data.append({
            'symbol': symbol,
            'price': info.get('regularMarketPrice', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
        })

        history_data[symbol] = history

    return pd.DataFrame(stock_data), history_data
