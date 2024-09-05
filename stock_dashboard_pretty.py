import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from yahooquery import Ticker
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__)


# Define the app layout
def create_layout():
    return html.Div([
        html.Div([
            html.H1("Stock Data Dashboard", className="dashboard-title"),
            html.Div([
                dcc.Input(id="stock-input", type="text", placeholder="Enter stock symbols (comma-separated)",
                          className="stock-input"),
                html.Button("Fetch Data", id="fetch-button", className="fetch-button"),
            ], className="input-container"),
            html.Div([
                html.P("Select time range"),
                dcc.RadioItems(
                    id='time-range',
                    options=[
                        {'label': '1D', 'value': '1D'},
                        {'label': '5D', 'value': '5D'},
                        {'label': '1W', 'value': '1W'},
                        {'label': '1M', 'value': '1M'},
                        {'label': 'YTD', 'value': 'YTD'},
                        {'label': 'Max', 'value': 'MAX'}
                    ],
                    value='1D',
                    inline=True
                )
            ], className="time-range-selector"),
        ], className="header"),
        html.Div(id="stock-data-container", className="data-container"),
        dcc.Graph(id="stock-chart", className="stock-chart"),
        dcc.Graph(id="stock-history-chart", className="stock-history-chart")
    ], className="dashboard")


app.layout = create_layout()


# Fetch stock data
def fetch_stock_data(symbols, time_range):
    data = []
    history_data = {}

    for symbol in symbols:
        stock = Ticker(symbol)
        info = stock.summary_detail.get(symbol, {})
        financial_data = stock.financial_data.get(symbol, {})

        # Fetch historical data based on time range
        history = stock.history(period=time_range.lower())
        history_data[symbol] = history

        try:
            data.append({
                "Symbol": symbol,
                "Price": info.get("regularMarketPrice", "N/A"),
                "Market Cap": f"${info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else "N/A",
                "P/E Ratio": round(info.get("trailingPE", "N/A"), 2) if info.get("trailingPE") else "N/A",
                "Annual Revenue": f"${financial_data.get('totalRevenue', 'N/A'):,}" if financial_data.get(
                    'totalRevenue') else "N/A",
                "EPS": round(financial_data.get("epsTrailingTwelveMonths", "N/A"), 2) if financial_data.get(
                    "epsTrailingTwelveMonths") else "N/A",
                "Dividend Yield": f"{info.get('dividendYield', 'N/A'):.2%}" if info.get("dividendYield") else "N/A"
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    return pd.DataFrame(data), history_data


# Create stock data table
def create_stock_data_table(df):
    return html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ])
    ], className="stock-table")


# Create stock price comparison chart
def create_stock_price_chart(df):
    fig = go.Figure(data=[
        go.Bar(name='Stock Price', x=df['Symbol'], y=df['Price'])
    ])
    fig.update_layout(title='Stock Prices Comparison', xaxis_title='Symbols', yaxis_title='Price')
    return fig


# Create stock history chart
def create_stock_history_chart(history_data):
    fig = go.Figure()
    for symbol, history in history_data.items():
        if not history.empty:
            fig.add_trace(go.Scatter(x=history.index, y=history['close'], mode='lines', name=symbol))
    fig.update_layout(title='Stock Price History', xaxis_title='Date', yaxis_title='Price')
    return fig


@app.callback(
    [Output("stock-data-container", "children"),
     Output("stock-chart", "figure"),
     Output("stock-history-chart", "figure")],
    Input("fetch-button", "n_clicks"),
    [State("stock-input", "value"), State("time-range", "value")]
)
def update_dashboard(n_clicks, stock_symbols, time_range):
    if not stock_symbols:
        return "Please enter stock symbols", go.Figure(), go.Figure()

    symbols = [symbol.strip() for symbol in stock_symbols.split(",")]
    stock_data, history_data = fetch_stock_data(symbols, time_range)

    table = create_stock_data_table(stock_data)
    price_chart = create_stock_price_chart(stock_data)
    history_chart = create_stock_history_chart(history_data)

    return table, price_chart, history_chart


# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Stock Data Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f2f5;
            }
            .dashboard {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .dashboard-title {
                color: #2c3e50;
                text-align: center;
            }
            .input-container {
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }
            .stock-input {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #bdc3c7;
                border-radius: 5px 0 0 5px;
                width: 300px;
            }
            .fetch-button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 0 5px 5px 0;
                cursor: pointer;
            }
            .fetch-button:hover {
                background-color: #2980b9;
            }
            .data-container {
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                overflow-x: auto;
            }
            .stock-table {
                width: 100%;
                border-collapse: collapse;
            }
            .stock-table th, .stock-table td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #e0e0e0;
            }
            .stock-table th {
                background-color: #f8f9fa;
                font-weight: bold;
                color: #2c3e50;
            }
            .stock-table tr:hover {
                background-color: #f5f6fa;
            }
            .stock-chart, .stock-history-chart {
                margin-top: 20px;
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            .time-range-selector {
                text-align: center;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == "__main__":
    app.run_server(debug=True)