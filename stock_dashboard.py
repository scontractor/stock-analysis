import yfinance as yf
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Data Dashboard"),
    dcc.Input(id="stock-input", type="text", placeholder="Enter stock symbols (comma-separated)"),
    html.Button("Fetch Data", id="fetch-button"),
    html.Div(id="stock-data-table")
])


@app.callback(
    Output("stock-data-table", "children"),
    Input("fetch-button", "n_clicks"),
    Input("stock-input", "value")
)
def update_stock_data(n_clicks, stock_symbols):
    if not stock_symbols:
        return "Please enter stock symbols"

    symbols = [symbol.strip() for symbol in stock_symbols.split(",")]
    data = []

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        info = stock.info

        try:
            data.append({
                "Symbol": symbol,
                "Price": info.get("currentPrice", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "P/E Ratio": info.get("trailingPE", "N/A"),
                "Annual Revenue": info.get("totalRevenue", "N/A"),
                "EPS": info.get("trailingEps", "N/A"),
                "Dividend Yield": info.get("dividendYield", "N/A")
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    df = pd.DataFrame(data)

    return html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ])
    ])


if __name__ == "__main__":
    app.run_server(debug=True)