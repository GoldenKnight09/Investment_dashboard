# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:43:15 2024

@author: chris
"""

import pandas as pd
from dash import html, dcc, Input, Output, Dash, State
import dash_bootstrap_components as dbc
import Supplemental_functions_investment_dashboard as sup_func
import yfinance as yf
import plotly.graph_objects as go

# import all ticker symbols to be used in app
investment_ticker_symbols = pd.read_excel(io = 'inputs/Investment_ticker_symbols.xlsx',
                                          sheet_name = None)

# look-up df for stocks:
stock_df = investment_ticker_symbols['Stock_list'].set_index('Ticker')
# look-up df for indices:
index_df = investment_ticker_symbols['Index_list'].set_index('Ticker')
index_dropdown_dict = dict((value, label) for label,value in zip(investment_ticker_symbols['Index_list']['Index'],
                                                                 investment_ticker_symbols['Index_list']['Ticker']))
# for some reason, dcc.Dropdown displays the dict value rather than the dict key, so invert dict
stock_dropdown_dict_by_group = {}
stock_group_list = list(investment_ticker_symbols['Stock_list'].Group.unique())
for stock_group in stock_group_list:
    stock_group_df = investment_ticker_symbols['Stock_list'].loc[investment_ticker_symbols['Stock_list']['Group'] == stock_group,:]
    stock_dict_by_group = dict((value, label) for label,value in zip(stock_group_df['Stock'],
                                                                     stock_group_df['Ticker']))
    stock_dropdown_dict_by_group[stock_group] = stock_dict_by_group

index_ticker_list = index_df.index.to_list()

# load stock category descriptions modal from txt file (with markdown)
with open('inputs/stock_categories_modal.txt','r') as scm:
    stock_cat = scm.read()
    
app = Dash(__name__)
server = app.server

app.layout = html.Div(children = [html.Div(html.H2('Stock/Index/Commodity/Treasury Investing Dashboard',
                                                   style = {'text-align':'center'})),
                                  html.Div(dbc.Tabs(children = [dbc.Tab(children = [dbc.Button('Click here for an explanation of the stock categories',
                                                                                               id = 'open_stock_cat_def_modal'),
                                                                                    dbc.Modal(children = [dbc.ModalHeader(dbc.ModalTitle('Stock Category Definitions'),
                                                                                                                          close_button = False),
                                                                                                          dbc.ModalBody(dbc.Container(children = [dcc.Markdown(stock_cat)])),
                                                                                                          dbc.ModalFooter(dbc.Button('Close',
                                                                                                                                     id = 'close_stock_cat_def_modal',
                                                                                                                                     className = 'ml-auto'))],
                                                                                              id = 'stock_cat_def_modal',
                                                                                              size = 'lg',
                                                                                              scrollable = True),
                                                                                    dbc.Col(children = [dcc.Dropdown(options = stock_group_list,
                                                                                                                     searchable = True,
                                                                                                                     placeholder = 'Select a stock group...',
                                                                                                                     id = 'stock_group_dropdown_menu'),
                                                                                                        dcc.Dropdown()],
                                                                                            width = 2),
                                                                                    dbc.Col(children = [dbc.Label(id = 'stock_ticker_test')])],
                                                                        label = "Stocks & ETF's",
                                                                        style = {'margin-left':'3px'}),
                                                                dbc.Tab(children = [dbc.Col(children = dcc.Dropdown(options = index_dropdown_dict,
                                                                                                                    searchable = True,
                                                                                                                    placeholder = 'Select an index...',
                                                                                                                    id = 'index_dropdown_menu'),
                                                                                            width = 2),
                                                                                    # might need to wrap the Col's in a dbc.Row
                                                                                    dbc.Col(children = [dbc.Label(id = 'index_ticker_test')],
                                                                                            width = 4)],
                                                                        label = 'Indices',
                                                                        style = {'margin-left':'3px'}),
                                                                dbc.Tab(children = [],
                                                                        label = 'Commodities',
                                                                        style = {'margin-left':'3px'}),
                                                                dbc.Tab(children = [],
                                                                        label = 'US Treasuries',
                                                                        style = {'margin-left':'3px'})],
                                                    style = {'margin-left':'3px'}))])

@app.callback(Output(component_id='stock_cat_def_modal', component_property='is_open'),
              Input(component_id='open_stock_cat_def_modal',component_property='n_clicks'),
              Input(component_id='close_stock_cat_def_modal',component_property='n_clicks'),
              State(component_id='stock_cat_def_modal',component_property='is_open'))

def toggle_stock_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(Output(component_id='stock_ticker_test',component_property='children'),
              Input(component_id='stock_group_dropdown_menu',component_property='value'))

def stock_ticker_test_display(stock_group_value):
    return stock_group_value

@app.callback(Output(component_id='index_ticker_test',component_property='children'),
              Input(component_id='index_dropdown_menu',component_property='value'))

def index_ticker_test_display(index_value):
    return index_value

if __name__ == '__main__':
    app.run(debug = False)