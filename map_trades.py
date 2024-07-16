import pandas as pd
from classes import trade_class, open_trades, closed_trades, holding_class
from utils_accounting import add_to_holdings, remove_from_holdings
from datetime import  timedelta

def map_trades(oldtrades_df, newtrades_df, holdings_lifo):
    """
    Returns a dataframe of all current open trades. Trades that are close to one another in time get added together.

    Args:
        oldtrades_df ([dataframe]): dataframe of old trades/previous holdings
        newtrades_df ([dataframe]): dataframe of new trades 
        holdings_lifo ([type]): list of current holdings

    Returns:
        df_trades [dataframe]: [description]
    """
        
    i = 0
            
    if oldtrades_df.shape[0] > 0:
        while i < oldtrades_df.shape[0]:
            if oldtrades_df.iloc[0,7]:
                open = trade_class(oldtrades_df.iloc[i,1], oldtrades_df.iloc[i,2], oldtrades_df.iloc[i,4], oldtrades_df.iloc[i,8], oldtrades_df.iloc[i,7],
                                        oldtrades_df.iloc[i,10], oldtrades_df.iloc[i,11], oldtrades_df.iloc[i,8]*oldtrades_df.iloc[i,7]+oldtrades_df.iloc[i,10])
                add_to_holdings(open, holdings_lifo)
                i += 1
            else:
                i += 1
            
    df_tmp = newtrades_df.copy()
    
    # Create shifted columns for time, ticker and type
    df_tmp['time(i-1)'] = newtrades_df['date'].shift(+1)-timedelta(minutes=5)
    df_tmp['ticker(i-1)'] = newtrades_df['symbol'].shift(+1)
    df_tmp['type(i-1)'] = newtrades_df['side'].shift(+1)

    # Compare if datetime(i) is less than datetime(i+1)+5minutes 
    df_tmp['time_bool'] = newtrades_df['date'] >= df_tmp['time(i-1)']
    # Compare if name of row i and i+1 is the same 
    df_tmp['ticker_bool'] = newtrades_df['symbol'] == df_tmp['ticker(i-1)']
    # Compare if type (buy/sell) of row i and i+1 is the same 
    df_tmp['side_bool'] = newtrades_df['side'] == df_tmp['type(i-1)']

    # Create mask column if 3 conditions above are met
    df_tmp['mask'] = df_tmp['time_bool'] & df_tmp['ticker_bool'] & df_tmp['side_bool']
    # Create inverse mask column
    df_tmp['inversed_mask'] = ~df_tmp['mask']
    # Create inverse mask cumsum column
    df_tmp['inversed_mask_cumsum'] = (~df_tmp['mask']).cumsum()

    # group same trades using inversed_mask_cumsum column
    g = df_tmp.groupby(df_tmp['inversed_mask_cumsum'])
        
    # Create dataframe of trades using groups created above
    
    cols_open = ['entry_date','symbol','side','price','filled','fee', 'fee_asset', 'total']

    df_trades = pd.DataFrame(index=[0], columns=cols_open)
        
    for k, v in g:
        d = g.get_group(k)
        d_price = d.price.mean()
        d_size = d.filled.sum()
        d_fee = d.fee.sum()
        d_fee_asset = d.fee_asset.iloc[0]
        d_total = d.total.sum()
        
        data = {'entry_date':d.iloc[0,0], 
            'symbol': d.iloc[0,1],
            'side':d.iloc[0,2],
            'price':d_price,
            'filled':d_size,
            'fee':d_fee, 
            'fee_asset':d_fee_asset, 
            'total':d_total 
            }
        df_loop = pd.DataFrame(data, index=[0])
        df_trades = df_trades.append(df_loop)

    df_trades = df_trades.dropna()
    df_trades = df_trades.iloc[::-1]
    
    return df_trades
        
    
    
