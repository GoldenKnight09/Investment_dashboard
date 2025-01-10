# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 22:51:51 2024

@author: chris
"""

import pandas as pd
from datetime import date, timedelta, datetime
from re import compile
# import dash_bootstrap_components as dbc
import yfinance as yf
import requests
import plotly.graph_objects as go

# def generate_dropdown_menu_item(dropdown_item):
#     '''
#     Function to create dropdown menu items inside the function to create the dropdowns
#     (Used to avoid: TypeError: Object of type generator is not JSON serializable)
    
#     Inputs:
#         dropdown_item: string to be converted into a dash bootstrap component DropdownMenuItem
#     Outputs:
#         dash bootstrap commponet DropdownMenuItem
#     '''
#     return dbc.DropdownMenuItem(children=dropdown_item,
#                                 id = f'dropdown_item_{dropdown_item}')
# def generate_dropdown_menu(dropdown_df,tab_prefix,group_name):
#     '''
#     Function to generate dropdown menus
    
#     Inputs:
#         dropdown_df: a dataframe with the dropdown menu items as the index
#         tab_prefix: string used as part of the component id
#         group_name: string tag included in the text displayed in the dropdown menu prompt as well as the element id
#     Outputs:
#         dash boostrap component DropdownMenu with DropdownMenuItem entries generated by the generate_dropdown_menu_item function
#     '''
#     return dbc.DropdownMenu(label = f'Select a {group_name} stock...',
#                             id = f'{tab_prefix}_dropdown_{group_name}',
#                             children = [generate_dropdown_menu_item(dropdown_item) for dropdown_item in dropdown_df.index.to_list()])

def non_day_timedelta(increment_type,increment_amount):
    '''
    Function used to convert string inputs into a date output
    
    Inputs:
        increment_type: string indicating the type of increment to be used to determine the date
        increment_amount: number indicating the amount of the increment to be used
    Returns: a datetime object (starting date argument for history() method)
    '''
    today_year = date.today().year
    today_month = date.today().month
    today_day = date.today().day
    if increment_type == 'y':
        new_year = today_year - increment_amount
    else:
        new_year = today_year
    if increment_type == 'm':
        new_month = today_month - increment_amount
        # add logic in case the start date is in the previous year
        if new_month <= 0:
            new_month = new_month + 12
            new_year = today_year - 1
    else:
        new_month = today_month
    if increment_type == 'ytd':
        if (today_month == 1) and (today_day == 1):
            new_day = today_day
        else:
            new_month, new_day = 1,1
    else:
        new_day = today_day
    # need to return monthes & days padded with leading zeroes
    return str(new_year) + '-' + str(new_month).zfill(2) + '-' + str(new_day).zfill(2)

def start_date(radio_date_input):
    '''
    Match-case function to parse date radioitem output from UI
    
    Inputs:
        radio_date_input: output from radioitem selectors from UI
    Returns: a matched datetime object (starting date for slicing equity data)
    '''
    match radio_date_input:
        case '7d':
            return (date.today() - timedelta(days = 7)).strftime('%Y-%m-%d')
        case '14d':
            return (date.today() - timedelta(days = 14)).strftime('%Y-%m-%d')
        case '1m':
            return non_day_timedelta('m', 1)
        case '3m':
            return non_day_timedelta('m', 3)
        case '6m':
            return non_day_timedelta('m', 6)
        case '1y':
            return non_day_timedelta('y', 1)
        case 'ytd':
            return non_day_timedelta('ytd', 0)
        # case max is the full ticker dataframe, no need to filter, use guard if statement to block this function
        # case custom is not valid for this function, use guard if statement to block this function
        case _: # catch
            return (date.today - timedelta(days = 3)).strftime('%Y-%m-%d')
        
def equity_plot_y_label(ticker_symbol,equity_type):
    '''
    Function to set the price chart y-axis (currency) label
    
    Inputs:
        ticker_symbol: string of ticker symbol that is being visualized
        equity_type: string corresponding to the type of equity (Stock, Index, Commodity), since options differ for each type
    Returns: string with appropriate units for the plot
    '''
    match equity_type:
        case 'Index':
            match ticker_symbol:
                case '^GDAXI':
                    return 'Price (€)'
                case '^FTSE':
                    return 'Price (£)'
                case '^N225' | '000001.SS' | '000300.SS':
                    return 'Price (¥)'
                case '^HSI':
                    return 'Price (HK$)'
                case _:
                    return 'Price ($)'
        case 'Stock':
            if '.' in ticker_symbol:
                ticker_split = compile(r'.*\.(\D{1,2})')
                match ticker_split.split(ticker_symbol)[1]:
                    case 'DE' | 'PA':
                        return 'Price (€)'
                    case 'L':
                        return 'Price (£)'
                    case 'SW':
                        return 'Price (CHF)'
                    case 'T' | 'SS':
                        return 'Price (¥)'
                    case 'HK':
                        return 'Price (HK$)'
            else:
                return 'Price ($)'

def generate_eq_plotly_plot(ticker_symbol,eq_date_select,equity_type,look_up_table,eq_custom_start_date,eq_custom_end_date):
    '''
    Function for generating a plot for equities
    
    Inputs:
        ticker_symbol: string corresponding to the ticker symbol of the equity
        date_select: string corresponding to the output from the radioitem selction
        equity_type: string correponding to the type of equity (Stock, Index, Commodity)
        look_up_table: dataframe using ticker symbols as index with full equity name as data
        custom_start_date: datetime object from daterange picker for starting slice date when custum date range is selected
        custom_end_date: datetime object from daterange picker for ending slice date when custum date range is selected
    Returns:
        Plotly graph object: candlestick plot
    '''
    if eq_date_select != 'custom':
        if eq_date_select == 'max':
            eq_start_date = '1901-01-01'
        else:
            eq_start_date = start_date(eq_date_select)
        # yfinance history() slice does not include final end date (typical Python)
        eq_end_date = (date.today() + timedelta(days = 1)).strftime('%Y-%m-%d')
    else:
        eq_start_date = eq_custom_start_date
        eq_end_date = (datetime.strptime(eq_custom_end_date, '%Y-%m-%d') + timedelta(days = 1)).strftime('%Y-%m-%d')
    eq_data = yf.Ticker(ticker_symbol).history(start = eq_start_date, end = eq_end_date, auto_adjust=False)
    # Ticker is not providing accurate price information
    # history returns dividend-adjusted price; use auto_adjust = False to avoid
    # history periods: ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    # can use yf.download() for more open-ended requests, or just take max period and then filter (fewer requests)
    # index is datetime stamp, only need dates for simple manipulations
    eq_data_by_date = eq_data.copy()
    eq_data_by_date['date'] = pd.to_datetime(eq_data.index.date)
    eq_data_by_date = eq_data_by_date.set_index('date')
    # London stock exchange stocks reported in pence, convert to pounds
    if '.L' in ticker_symbol:
        col_convert_list = ['Open',
                            'High',
                            'Low',
                            'Close']
        eq_data_by_date.loc[:,col_convert_list] = eq_data_by_date[col_convert_list] / 100
    percent_change = ((eq_data_by_date.iloc[-1,eq_data_by_date.columns.get_loc('Close')] - \
                      eq_data_by_date.iloc[0,eq_data_by_date.columns.get_loc('Close')]) / \
                      eq_data_by_date.iloc[0,eq_data_by_date.columns.get_loc('Close')]) * 100
    title_percent = '{:.2f}'.format(percent_change)
    fig = go.Figure(data = [go.Candlestick(x = eq_data_by_date.index,
                                           open = eq_data_by_date['Open'],
                                           high = eq_data_by_date['High'],
                                           low = eq_data_by_date['Low'],
                                           close = eq_data_by_date['Close'],
                                           increasing_line_color = 'darkseagreen',
                                           decreasing_line_color = 'red')])
    fig.update_layout(title = f'<b>{look_up_table.loc[ticker_symbol,equity_type]} ({title_percent}%)</b>',
                      title_font_size = 20,
                      title_x = 0.5,
                      xaxis_title = '<b>Date</b>',
                      yaxis_title = f'<b>{equity_plot_y_label(ticker_symbol, equity_type)}</b>',
                      xaxis_rangeslider_visible=False,
                      # showlegend = False,
                      plot_bgcolor = 'white')
    fig.update_xaxes(title_font_size = 15,
                     tickfont_size = 12,
                     showline = True, # plot area border line
                     linecolor = 'black', # plot area border line color
                     # mirror = True,
                     gridcolor = 'lightgray')
    fig.update_yaxes(title_font_size = 15,
                     tickfont_size = 12,
                     showline = True, # plot area border line
                     linecolor = 'black', # plot area border line color
                     # mirror = True,
                     gridcolor = 'lightgray')
    if max(eq_data_by_date['High'] > 10000):
        fig.update_yaxes(tickformat = '000')
    return fig

def generate_treasury_plotly_plot(security_term,t_date_select,t_custom_start_date,t_custom_end_date):
    '''
    Placeholder function for get request for treasury data via API
    '''
    if t_date_select != 'custom':
        if t_date_select == 'max':
            t_start_date = '1901-01-01'
        else:
            t_start_date = start_date(t_date_select)
        t_end_date = date.today().strftime('%Y-%m-%d')
    else:
        t_start_date = t_custom_start_date
        t_end_date = t_custom_end_date
    fields = ['security_term',
              'issue_date',
              # 'auction_date',
              # 'price_per100',
              'avg_med_discnt_rate']
    treasury_base_url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
    sec_auctions_endpoint = 'v1/accounting/od/auctions_query'
    fields_list_concat = ','.join(fields)
    fields_str = f'fields={fields_list_concat}'
    filter_list = ['security_term:eq:' + security_term,
                   'issue_date:gte:' + t_start_date,
                   'issue_date:lte:' + t_end_date]
    filter_list_concat = ','.join(filter_list)
    filter_str = f'filter={filter_list_concat}'
    sec_auction_list = []
    req_status = 200
    page_num = 1
    # request all potential pages of responses into list before concatenating into single dataframe
    while req_status == 200:
        pagination_str = f'page[number]={page_num}&page[size]=1000'
        response = requests.get(treasury_base_url + sec_auctions_endpoint + '?' + fields_str + '&' + filter_str + '&' + pagination_str)
        req_status = response.status_code
        # print(f'page_num {page_num} status_code is {req_status}')
        if req_status == 200:
            sec_auction_list.append(pd.DataFrame.from_dict(response.json()['data']))
        page_num += 1
    sec_auction_df = pd.concat(sec_auction_list).reset_index(drop = True)
    sec_plot_df = sec_auction_df.copy()
    # need to drop null
    sec_plot_df = sec_plot_df.loc[sec_plot_df.avg_med_discnt_rate != 'null',:]
    sec_plot_df['issue_date'] = pd.to_datetime(sec_auction_df['issue_date'])
    # data is object format
    sec_plot_df['avg_med_discnt_rate'] = sec_plot_df['avg_med_discnt_rate'].astype('float')
    sec_plot_df = sec_plot_df.sort_values(by = 'issue_date')
    fig = go.Figure(data = [go.Scatter(x = sec_plot_df['issue_date'],
                                       y = sec_plot_df['avg_med_discnt_rate'],
                                       mode = 'markers')])
    fig.update_layout(title = f'<b>{security_term} effective interest rates</b>',
                      title_font_size = 20,
                      title_x = 0.5,
                      xaxis_title = '<b>Date</b>',
                      yaxis_title = '<b>Effective interest rate</b>',
                      xaxis_rangeslider_visible=False,
                      # showlegend = False,
                      plot_bgcolor = 'white')
    fig.update_xaxes(title_font_size = 15,
                     tickfont_size = 12,
                     showline = True, # plot area border line
                     linecolor = 'black', # plot area border line color
                     # mirror = True,
                     gridcolor = 'lightgray')
    fig.update_yaxes(title_font_size = 15,
                     tickfont_size = 12,
                     showline = True, # plot area border line
                     linecolor = 'black', # plot area border line color
                     # mirror = True,
                     gridcolor = 'lightgray')
    return fig

def sup_func_main():
    pass

if __name__ == '__main__':
    sup_func_main()