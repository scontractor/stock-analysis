from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from data_fetcher import fetch_stock_data
from charts import create_stock_data_table, create_stock_price_chart, create_stock_history_chart
import plotly.graph_objs as go
import webbrowser
from threading import Timer
import os

# Initialize the Dash app with a dark theme
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stock Data Dashboard", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Input(id="stock-input", type="text", placeholder="Enter stock symbols (comma-separated)",
                      className="mb-2"),
            dbc.Button("Fetch Data", id="fetch-button", color="primary", className="mb-4"),
            dbc.Card([
                dbc.CardHeader("Select Time Range"),
                dbc.CardBody(
                    dcc.RadioItems(
                        id='time-range',
                        options=[
                            {'label': '1D', 'value': '1d'},
                            {'label': '5D', 'value': '5d'},
                            {'label': '1M', 'value': '1mo'},
                            {'label': 'YTD', 'value': 'ytd'},
                            {'label': 'MAX', 'value': 'max'}
                        ],
                        value='1d',
                        inline=True
                    )
                )
            ], className="mb-4")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="stock-data-container"), width=12, className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="stock-chart"), width=12, className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="stock-history-chart"), width=12)
    ])
], fluid=True, className="p-5")


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
    print(f"Fetching data for symbols: {symbols}, time range: {time_range}")

    try:
        stock_data, history_data = fetch_stock_data(symbols, time_range)
        print(f"Stock data shape: {stock_data.shape}")
        print(f"History data keys: {list(history_data.keys())}")
    except Exception as e:
        error_message = f"Error fetching data: {str(e)}"
        print(error_message)
        return error_message, go.Figure(), go.Figure()

    if stock_data.empty:
        print("No data available for the selected stocks.")
        return "No data available for the selected stocks.", go.Figure(), go.Figure()

    table = create_stock_data_table(stock_data)
    price_chart = create_stock_price_chart(stock_data)
    history_chart = create_stock_history_chart(history_data)

    print("Charts created successfully")

    # Update chart layouts for dark theme
    for chart in [price_chart, history_chart]:
        chart.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

    return table, price_chart, history_chart


def open_browser():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    if not os.path.exists(chrome_path):
        print(f"Chrome executable not found at {chrome_path}")
        print("Trying to open with default browser...")
        webbrowser.open_new('http://127.0.0.1:8050/')
    else:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

        try:
            webbrowser.get('chrome').open_new('http://127.0.0.1:8050/')
        except webbrowser.Error:
            print("Failed to open Chrome. Trying default browser...")
            webbrowser.open_new('http://127.0.0.1:8050/')


if __name__ == "__main__":
    # Use the Timer to delay the browser opening until the server is ready
    Timer(1, open_browser).start()
    app.run_server(debug=True)
