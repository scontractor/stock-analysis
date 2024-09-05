from dash import dcc, html

def create_layout():
    return html.Div([
        html.Div([
            html.H1("Stock Data Dashboard", className="dashboard-title"),
            html.Div([
                dcc.Input(id="stock-input", type="text", placeholder="Enter stock symbols (comma-separated)", className="stock-input"),
                html.Button("Fetch Data", id="fetch-button", className="fetch-button"),
            ], className="input-container"),
            html.Div([
                html.P("Select time range"),
                dcc.RadioItems(
                    id='time-range',
                    options=[
                        {'label': '1D', 'value': '1d'},
                        {'label': '5D', 'value': '5d'},
                        {'label': '1W', 'value': '7d'},
                        {'label': '1M', 'value': '1mo'},
                        {'label': 'YTD', 'value': 'ytd'},
                        {'label': 'Max', 'value': 'max'}
                    ],
                    value='1d',
                    inline=True
                )
            ], className="time-range-selector"),
        ], className="header"),
        html.Div(id="stock-data-container", className="data-container"),
        dcc.Graph(id="stock-chart", className="stock-chart"),
        dcc.Graph(id="stock-history-chart", className="stock-history-chart")
    ], className="dashboard")
