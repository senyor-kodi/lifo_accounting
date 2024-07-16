import datetime
import numpy as np
import pandas as pd

class trade_class:
    def __init__(self, date:datetime, symbol:str, side:str, price:np.float64, filled:np.float64, fee:np.float64, fee_asset:str, total:np.float64):
        self.date = date
        self.symbol = symbol
        self.side = side
        self.price = price
        self.filled = filled
        self.fee = fee
        self.fee_asset = fee_asset
        self.total = total
        
    def get_date(self):
        return self.date
    def get_symbol(self):
        return self.symbol
    def get_side(self):
        return self.side
    def get_price(self):
        return self.price
    def get_filled(self):
        return self.filled
    def get_fee(self):
        return self.fee
    def get_fee_asset(self):
        return self.fee_asset
    def get_total(self):
        return self.total
    
class holding_class:        
    def __init__(self, date:datetime, symbol:str, side:str, price:np.float64, quantity:np.float64, fee:np.float64, total:np.float64):
        self.date = date
        self.symbol = symbol
        self.side = side
        self.price = price
        self.quantity = quantity 
        self.fee = fee
        self.total = total

    def get_date(self):
        return self.date
    def get_symbol(self):
        return self.symbol
    def get_price(self):
        return self.price
    def get_quant(self):
        return self.quantity
    def get_fee(self):
        return self.fee
    def get_total(self):
        return self.total

    def set_quantity(self,newQuant):
        self.quantity = newQuant
    def substract_x(self,toSubtract): # ONLY USE WHEN AMOUNT SUBTRACTING IS LESS THAN self.quantity
        self.quantity -= toSubtract
        
        
cols_open = ['entry_date','symbol','side','price','filled','fee', 'fee_asset', 'total']
cols_closed = ['entry_date', 'close_date', 'symbol','side','entry_price', 'close_price', 'filled','fee', 'profit']
        
class open_trades:
    def __init__(self):
        self.main_dataframe = pd.DataFrame(data=None, columns=cols_open)
        
    def append_dataframe(self, df_tmp):
        self.main_dataframe = self.main_dataframe.append(df_tmp)
    
    def to_file(self):
         self.main_dataframe.to_excel(r'C:\Users\danie\OneDrive\Desktop\daniel\coding\trading_local\open_trades.csv', index=False)
                 
class closed_trades:
    def __init__(self):
        self.main_dataframe = pd.DataFrame(data=None, columns=cols_closed)
        
    def append_dataframe(self, df_tmp):
        self.main_dataframe = self.main_dataframe.append(df_tmp)
    
    def to_file(self):
         self.main_dataframe.to_excel(r'C:\Users\danie\OneDrive\Desktop\daniel\coding\trading_local\closed_trades2.xlsx', index=False)