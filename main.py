import os
from flask import Flask, render_template
import requests

app = Flask(__name__)

# Replace with your actual API key
API_KEY = "INpfO7orXTeDYJeFYjWI5XIPP9eotDPG"

# List of Berkshire Hathaway's top holdings (you may want to expand this list)
BUFFETT_HOLDINGS = [
    "AAPL", "BAC", "AXP", "KO", "CVX", "OXY", "KHC", "MCO", "CB", "DVA"
]

def get_stock_data(symbol):
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]
    return None

@app.route('/')
def dashboard():
    portfolio = []
    for symbol in BUFFETT_HOLDINGS:
        stock_data = get_stock_data(symbol)
        if stock_data:
            portfolio.append(stock_data)
    return render_template('dashboard.html', portfolio=portfolio)

if __name__ == '__main__':
    app.run(debug=True)