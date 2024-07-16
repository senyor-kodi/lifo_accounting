import pandas as pd
from classes import trade_class, open_trades, closed_trades, holding_class


def add_to_holdings(t, holdings_lifo):
    """
    Add trade to list of holdings

    Args:
        t ([trade class]): trade to be added to holdings
        holdings_lifo ([list]): list of current holdings
    """
    date = t.get_date()
    symbol = t.get_symbol()
    side = t.get_side()
    price = t.get_price()
    filled = t.get_filled()
    fee = t.get_fee()
    total = t.get_total()
    h = holding_class(date, symbol, side, price, filled, fee, total) # Re-initialize to append new object, rather than reference to original
    holdings_lifo.append(h)
    
   
def remove_from_holdings(t, holdings_lifo, df_closed_trades):
    """
    Remove trade from list of holdings. Searches for a matching trade by symbol, calculates statistics of closed trades and removes finished trades from holdings. 
    Returns updated dataframe of closed trades and list of holdings. 

    Args:
        t ([trade class]): trade to be removed from holdings
        holdings_lifo ([list]): list of current holdings
        df_closed_trades ([dataframe]): dataframe of closed trades

    Returns:
        df_closed_trades[dataframe]: updated dataframe of closed trades
    """
    
    d_list = []
    
    date = t.get_date()
    symbol = t.get_symbol()
    side = t.get_side()
    price = t.get_price()
    filled = t.get_filled()
    fee = t.get_fee()
    total = t.get_total()
    
    x = 0
    len_holdings_lifo = len(holdings_lifo)
    
    while len_holdings_lifo > x:

        holding_symbol = holdings_lifo[-x].get_symbol()
        
        while t.symbol == holding_symbol:
            holding_date = holdings_lifo[-x].get_date()
            holding_quant = holdings_lifo[-x].get_quant()
            holding_price = holdings_lifo[-x].get_price()
            holding_fee = holdings_lifo[-x].get_fee()
            if holding_quant == filled: #  Quantity is equal to that of the first remaining holding
                holding_pnl = (price - holding_price)*filled-(fee+holding_fee)
                data = {'entry_date':holding_date, 
                        'symbol': symbol,
                        'filled':holding_quant,
                        'close_date':date,
                        'entry_price':holding_price,
                        'close_price':price,
                        'fee': fee+holding_fee,
                        'profit':holding_pnl,
                        }
                holdings_lifo.pop(-x)
                len_holdings_lifo = len(holdings_lifo)
                df_closed_trades.append_dataframe(pd.DataFrame(data, index=[0]))
                if len_holdings_lifo <= x:
                    break
                else:
                    holding_symbol = holdings_lifo[-x].get_symbol()
                
            elif filled < holding_quant: # Quantity is smaller than in first correspondent holding ...
                holding_pnl = (price - holding_price)*filled-(fee+holding_fee)
                data = {'entry_date':holding_date, 
                        'symbol': symbol,
                        'filled':filled,
                        'close_date':date,
                        'entry_price':holding_price,
                        'close_price':price,
                        'fee': fee+holding_fee,
                        'profit':holding_pnl}
                holdings_lifo[-x].set_quantity(holding_quant-filled)
                df_closed_trades.append_dataframe(pd.DataFrame(data, index=[0]))
                len_holdings_lifo = len(holdings_lifo)
                break
                                           
            elif filled > holding_quant:  # Quantity sold exceeds value of the first remaining holding
                holding_pnl = (price - holding_price)*filled-(fee+holding_fee)
                data =  {'entry_date':holding_date, 
                        'symbol': symbol,
                        'filled':holding_quant,
                        'close_date':date,
                        'entry_price':holding_price,
                        'close_price':price,
                        'fee': fee+holding_fee,
                        'profit':holding_pnl}
                d_list.append(data)
                filled -= holding_quant
                holdings_lifo.pop(-x)
                len_holdings_lifo -= 1
                df_closed_trades.append_dataframe(pd.DataFrame(data, index=[0]))
                if len_holdings_lifo <= x:
                    break
                else:
                    holding_symbol = holdings_lifo[-x].get_symbol()
        x += 1                
    return df_closed_trades


stables = ['USDT', 'USD','UST', 'USDC']

def fee_calc(row):
    """
    Compute fees for a dataframe of trades taken 
    
    Args:
      row (row of dataframe, must have fee, fee_asset and price columns)
    
    Returns: 
        fee
    """
    if row.fee_asset in stables:
        return row.fee
    else:
        return row.fee*row.price

def flatten(t):
    """Flatten a list of lists into one single list 

    Args:
      t (list of lists)

    Returns:
      list
    """
    return [item for sublist in t for item in sublist]

