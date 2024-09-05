# charts.py

import plotly.graph_objs as go
from dash import html
import pandas as pd

def create_stock_data_table(df):
    return html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ])
    ])

def create_stock_price_chart(df):
    fig = go.Figure()
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol]
        fig.add_trace(go.Bar(x=[symbol], y=[symbol_data['price'].iloc[0]], name=symbol))
    fig.update_layout(title='Stock Prices', xaxis_title='Symbols', yaxis_title='Price')
    return fig

def create_stock_history_chart(history_data):
    fig = go.Figure()
    for symbol, data in history_data.items():
        if not data.empty:
            fig.add_trace(go.Scatter(x=data.index, y=data['close'], mode='lines', name=symbol))
    fig.update_layout(title='Stock Price History', xaxis_title='Date', yaxis_title='Price')
    return fig
