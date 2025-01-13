# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:43:15 2024

@author: chris
"""

import pandas as pd
from dash import html, dcc, Input, Output, Dash, State
import dash_bootstrap_components as dbc
import Supplemental_functions_investment_dashboard as sup_func
from datetime import date
# import yfinance as yf
# import plotly.graph_objects as go

# import all ticker symbols to be used in app
investment_ticker_symbols = pd.read_excel(io = 'inputs/Investment_ticker_symbols_and_treasury_terms.xlsx',
                                          sheet_name = None)

# look-up df for stocks:
stock_df = investment_ticker_symbols['Stock_list'].set_index('Ticker')
stock_dropdown_dict_by_group = {}
stock_group_list = list(investment_ticker_symbols['Stock_list'].Group.unique())
for stock_group in stock_group_list:
    stock_group_df = investment_ticker_symbols['Stock_list'].loc[investment_ticker_symbols['Stock_list']['Group'] == stock_group,:]
    stock_dict_list_by_group = list({'label':stock_group_df.loc[row,'Stock'],
                                     'value':stock_group_df.loc[row,'Ticker']} for row in stock_group_df.index)
    stock_dropdown_dict_by_group[stock_group] = stock_dict_list_by_group
# look-up df for indices:
index_df = investment_ticker_symbols['Index_list'].set_index('Ticker')
index_dropdown_dict = list({'label':investment_ticker_symbols['Index_list'].loc[row,'Index'],
                            'value':investment_ticker_symbols['Index_list'].loc[row,'Ticker']} for row in investment_ticker_symbols['Index_list'].index)

# dropdown menu dict for treasruries
treasury_dropdown_dict = list({'label':investment_ticker_symbols['Treasury_list'].loc[row,'Name'],
                               'value':investment_ticker_symbols['Treasury_list'].loc[row,'Term'] + ';' + investment_ticker_symbols['Treasury_list'].loc[row,'Type']} for row in investment_ticker_symbols['Treasury_list'].index)

# look-up df for treasuries
# treasury_df = investment_ticker_symbols['Security_list'].set_index('Term')

# load stock category descriptions modal from txt file (with markdown)
with open('inputs/stock_categories_modal.txt','r') as scm:
    stock_cat = scm.read()
    
# list for radio list of date options (both stock & indices)
radio_date_items = [{'label':'7 days','value':'7d'},
                    {'label':'14 days','value':'14d'},
                    {'label':'1 month','value':'1m'},
                    {'label':'3 months','value':'3m'},
                    {'label':'6 months','value':'6m'},
                    {'label':'YTD','value':'ytd'},
                    {'label':'1 year','value':'1y'},
                    {'label':'Max','value':'max'},
                    {'label':'Custom Range','value':'custom'}]
    
app = Dash(__name__)
server = app.server

app.layout = html.Div(children = [html.Div(html.H2('Stock/Index/Commodity/Treasury Investing Dashboard',
                                                   style = {'text-align':'center'})),
                                  html.Div(dbc.Container(dbc.Tabs(children = [dbc.Tab(dbc.Row(children = [dbc.Col(children = [dbc.Container(dbc.Card(children = [dbc.Button('Click here for an explanation of the stock categories',
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
                                                                                                                                                                 # consider dbc.Stack() with html.Div() for each "row" component to add spacing
                                                                                                                                                                 dcc.Dropdown(options = stock_group_list,
                                                                                                                                                                              searchable = True,
                                                                                                                                                                              placeholder = 'Select a stock group...',
                                                                                                                                                                              value = 'Retailers',
                                                                                                                                                                              id = 'stock_group_dropdown_menu'),
                                                                                                                                                                 dcc.Dropdown(placeholder = 'Select a stock...',
                                                                                                                                                                              id = 'stock_dropdown_menu'),
                                                                                                                                                                 dbc.Label('Select a date range to display',
                                                                                                                                                                           id = 'stock_radio_date_label'),
                                                                                                                                                                 dbc.RadioItems(options = radio_date_items,
                                                                                                                                                                                value = '14d',
                                                                                                                                                                                id = 'stock_radio_date'),
                                                                                                                                                                 dcc.DatePickerRange(start_date = sup_func.start_date('14d'),
                                                                                                                                                                                     end_date = date.today(),
                                                                                                                                                                                     max_date_allowed = date.today(),
                                                                                                                                                                                     id = 'stock_date_picker_range')],
                                                                                                                                                     body = True),
                                                                                                                                            fluid = True)],
                                                                                                                  width = 3),
                                                                                                          dbc.Col(children = [dbc.Container(children = [dcc.Graph(id = 'stock_plot')],
                                                                                                                                            fluid = True)],
                                                                                                                  width = 6)]),
                                                                                      label = "Stocks & ETF's"),
                                                                              dbc.Tab(dbc.Row(children = [dbc.Col(dbc.Container(dbc.Card(children = [dcc.Dropdown(options = index_dropdown_dict,
                                                                                                                                                                  searchable = True,
                                                                                                                                                                  placeholder = 'Select an index...',
                                                                                                                                                                  value = '^GSPC',
                                                                                                                                                                  id = 'index_dropdown_menu'),
                                                                                                                                                     dbc.Label('Select a date range to display',
                                                                                                                                                               id = 'index_radio_date_label'),
                                                                                                                                                     dbc.RadioItems(options = radio_date_items,
                                                                                                                                                                    value = '14d',
                                                                                                                                                                    id = 'index_radio_date'),
                                                                                                                                                     dcc.DatePickerRange(start_date = sup_func.start_date('14d'),
                                                                                                                                                                         end_date = date.today(),
                                                                                                                                                                         max_date_allowed = date.today(),
                                                                                                                                                                         id = 'index_date_picker_range')],
                                                                                                                                         body = True),
                                                                                                                                fluid = True),
                                                                                                                  width = 3),
                                                                                                          dbc.Col(dbc.Container(children = [dcc.Graph(id = 'index_plot')],
                                                                                                                                fluid = True),
                                                                                                                  width = 6)]),
                                                                                      label = 'Indices'),
                                                                              dbc.Tab(children = [],
                                                                                      label = 'Commodities'),
                                                                              dbc.Tab(dbc.Row(children = [dbc.Col(dbc.Container(dbc.Card(children = [dcc.Dropdown(options = treasury_dropdown_dict,
                                                                                                                                                                  searchable = True,
                                                                                                                                                                  placeholder = 'Select a security term...',
                                                                                                                                                                  value = '4-Week;Bill',
                                                                                                                                                                  id = 'treasury_dropdown_menu'),
                                                                                                                                                     dbc.Label('Select a date range to display',
                                                                                                                                                               id = 'treasure_radio_date_label'),
                                                                                                                                                     dbc.RadioItems(options = radio_date_items,
                                                                                                                                                                    value = '1m',
                                                                                                                                                                    id = 'treasury_radio_date'),
                                                                                                                                                     dcc.DatePickerRange(start_date = sup_func.start_date('1m'),
                                                                                                                                                                         end_date = date.today(),
                                                                                                                                                                         max_date_allowed = date.today(),
                                                                                                                                                                         id = 'treasury_date_picker_range')],
                                                                                                                                         body = True),
                                                                                                                                fluid = True),
                                                                                                                  width = 3),
                                                                                                          dbc.Col(dbc.Container(children = [dcc.Graph(id = 'treasury_plot')],
                                                                                                                                fluid = True),
                                                                                                                  width = 6)]),
                                                                                      label = 'US Treasuries')]),
                                                         fluid = True))])

@app.callback(Output(component_id='stock_cat_def_modal', component_property='is_open'),
              Input(component_id='open_stock_cat_def_modal',component_property='n_clicks'),
              Input(component_id='close_stock_cat_def_modal',component_property='n_clicks'),
              State(component_id='stock_cat_def_modal',component_property='is_open'))

def toggle_stock_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(Output(component_id='stock_dropdown_menu',component_property='options'),
              Input(component_id='stock_group_dropdown_menu',component_property='value'))

def stock_dropdown_menu(stock_group_value):
    return stock_dropdown_dict_by_group[stock_group_value]

@app.callback(Output(component_id='stock_dropdown_menu',component_property='value'),
              Input(component_id='stock_dropdown_menu',component_property='options'))

def stock_dropdown_menu_value(stock_dropdown_menu_options):
    return stock_dropdown_menu_options[0]['value']

@app.callback(Output(component_id='stock_date_picker_range',component_property='style'),
              Input(component_id='stock_radio_date',component_property='value'))

def render_stock_date_picker_range(stock_radio_date):
    if stock_radio_date != 'custom':
        return {'display':'none'}

@app.callback(Output(component_id='stock_plot',component_property='figure'),
              Input(component_id='stock_dropdown_menu',component_property='value'),
              Input(component_id='stock_radio_date',component_property='value'),
              Input(component_id='stock_date_picker_range',component_property='start_date'),
              Input(component_id='stock_date_picker_range',component_property='end_date'))

# TODO: try to find way to adjust default range for date_range_picker to correspond to last radio_button selction
# might be doable with State() / callback_context (ctx)

def render_stock_plot(stock_dropdown_ticker,stock_radio_date,stock_start_date,stock_end_date):
    fig_stock = sup_func.generate_eq_plotly_plot(stock_dropdown_ticker, stock_radio_date, 'Stock', stock_df,stock_start_date,stock_end_date)
    return fig_stock

@app.callback(Output(component_id='index_date_picker_range',component_property='style'),
              Input(component_id='index_radio_date',component_property='value'))

def render_index_date_picker_range(index_radio_date):
    if index_radio_date != 'custom':
        return {'display':'none'}

@app.callback(Output(component_id='index_plot',component_property='figure'),
              Input(component_id='index_dropdown_menu',component_property='value'),
              Input(component_id='index_radio_date',component_property='value'),
              Input(component_id='index_date_picker_range',component_property='start_date'),
              Input(component_id='index_date_picker_range',component_property='end_date'))

def render_index_plot(index_dropdown_ticker,index_radio_date,index_start_date,index_end_date):
    fig_index = sup_func.generate_eq_plotly_plot(index_dropdown_ticker, index_radio_date, 'Index', index_df,index_start_date,index_end_date)
    return fig_index

@app.callback(Output(component_id='treasury_date_picker_range',component_property='style'),
              Input(component_id='treasury_radio_date',component_property='value'))

def render_treasury_date_picker_range(treasury_radio_date):
    if treasury_radio_date != 'custom':
        return {'display':'none'}
    
@app.callback(Output(component_id='treasury_plot',component_property='figure'),
              Input(component_id='treasury_dropdown_menu',component_property='value'),
              Input(component_id='treasury_radio_date',component_property='value'),
              Input(component_id='treasury_date_picker_range',component_property='start_date'),
              Input(component_id='treasury_date_picker_range',component_property='end_date'))

def render_treasure_plot(security_dropdown_item,treasure_radio_date,treasury_start_date,treasury_end_date):
    security_type = security_dropdown_item.split(';')[1]
    security_term = security_dropdown_item.split(';')[0]
    fig_treasury = sup_func.generate_treasury_plotly_plot(security_type, security_term, treasure_radio_date, treasury_start_date, treasury_end_date)
    return fig_treasury

if __name__ == '__main__':
    app.run(debug = False)