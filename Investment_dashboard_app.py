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

# import all ticker symbols to be used in app
investment_ticker_symbols = pd.read_excel(io = 'inputs/Investment_ticker_symbols.xlsx',
                                          sheet_name = None)

stock_df = investment_ticker_symbols['Stock_list'].set_index('Stock')
index_df = investment_ticker_symbols['Index_list'].set_index('Index')
stock_dict_by_group = {}
stock_group_list = list(stock_df.Group.unique())
for stock_group in stock_group_list:
    stock_dict_by_group[stock_group] = stock_df.loc[stock_df['Group'] == stock_group,['Ticker']]
    

def generate_dropdown_menu_item(dropdown_item):
    '''
    Function to create dropdown menu items inside the function to create the dropdowns
    (Necessary, because otherwise run into error: TypeError: Object of type generator is not JSON serializable)
    '''
    return dbc.DropdownMenuItem(dropdown_item)
def generate_dropdown_menu(dropdown_df,group_name):
    '''
    Function to generate dropdown menus
    '''
    return dbc.DropdownMenu(label = f'Select a {group_name} stock...',
                            id = f'stock_ticker_dropdown_{group_name}',
                            children = [generate_dropdown_menu_item(dropdown_item) for dropdown_item in dropdown_df.index.to_list()])

app = Dash(__name__)
server = app.server

app.layout = html.Div(children = [html.Div(html.H2('Stock/Index/Commodity/Treasury Investing Dashboard',
                                                   style = {'text-align':'center'})),
                                  html.Div(dbc.Tabs(children = [dbc.Tab(children = [dbc.Col(children = [generate_dropdown_menu(stock_dict_by_group[group_name], group_name) for group_name in stock_group_list])],
                                                                        # need to group stocks and make dropdowns for each in a column or row (too many entries for a single dbc dropdown)
                                                                        label = "Stocks & ETF's",
                                                                        style = {'margin-left':'3px'}),
                                                                dbc.Tab(children = [dbc.Col(children = dbc.DropdownMenu(label = 'Select an Index...',
                                                                                                                        id = 'index_ticker_dropdown',
                                                                                                                        children = [generate_dropdown_menu_item(dropdown_item) for dropdown_item in index_df.index.to_list()]))],
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