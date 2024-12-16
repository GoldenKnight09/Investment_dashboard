# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:43:15 2024

@author: chris
"""

import pandas as pd
from dash import html, dcc, Input, Output, Dash, State
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.graph_objects as go

investment_ticker_symbols = pd.read_excel(io = 'inputs/Investment_ticker_symbols.xlsx',
                                          sheet_name = None)

app = Dash(__name__)
server = app.server

app.layout = html.Div(children = [html.Div(html.H2('Stock/Index/Commodity/Treasury Investing Dashboard',
                                                   style = {'text-align':'center'})),
                                  html.Div(dbc.Tabs(children = [dbc.Tab(children = [],
                                                                        label = "Stocks & ETF's",
                                                                        style = {'margin-left':'3px'}),
                                                                dbc.Tab(children = [],
                                                                        label = 'Indices',
                                                                        style = {'margin-left':'3px'}),
                                                                dbc.Tab(children = [],
                                                                        label = 'Commodities',
                                                                        style = {'margin-left':'3px'}),
                                                                dbc.Tab(children = [],
                                                                        label = 'US Treasuries',
                                                                        style = {'margin-left':'3px'})],
                                                    style = {'margin-left':'3px'}))])

if __name__ == '__main__':
    app.run(debug = False)