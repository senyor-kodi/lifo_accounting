from utils_accounting import add_to_holdings, remove_from_holdings, fee_calc, flatten
from map_trades import map_trades
from classes import trade_class, holding_class, open_trades, closed_trades
import pandas as pd
import numpy as np
import time
import datetime


stables = ['USDT', 'USD','UST', 'USDC']

""" General  """

holdings_lifo = [] # holdings_lifo_list

new_trades_df = pd.read_excel(r'', engine='openpyxl') #read dataframe of new trades from downloaded history
old_open_trades = pd.read_excel(r'', engine='openpyxl') #read dataframe of current open trades

old_open_trades = old_open_trades[old_open_trades.Side == 'BUY']
old_open_trades = pd.DataFrame()

df_trades = map_trades(old_open_trades, new_trades_df, holdings_lifo)
    
df_open_trades = open_trades()
df_closed_trades = closed_trades()

transaction_num = 1

for i in range(len(df_trades)):
    if ('BUY' == df_trades.iloc[i]).any():
        buy_trade = trade_class(df_trades.iloc[i,0], df_trades.iloc[i,1], df_trades.iloc[i,2], df_trades.iloc[i,3], df_trades.iloc[i,4], df_trades.iloc[i,5], 
                                df_trades.iloc[i,6], df_trades.iloc[i,7])
        add_to_holdings(buy_trade, holdings_lifo)
    elif ('SELL' == df_trades.iloc[i]).any():
        sell_trade = trade_class(df_trades.iloc[i,0], df_trades.iloc[i,1], df_trades.iloc[i,2], df_trades.iloc[i,3], df_trades.iloc[i,4], df_trades.iloc[i,5],
                                 df_trades.iloc[i,6], df_trades.iloc[i,7])
        remove_from_holdings(sell_trade, holdings_lifo, df_closed_trades)
    else:
        print('Transaction #{} is not a valid trade'.format(str(transaction_num)))
        
    transaction_num += 1

df_closed_trades.to_file()
print(4)