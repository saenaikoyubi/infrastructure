import pandas as pd
import numpy as np

def generateBaseDf(df_org):
    cols = ['UNIXTIME','side','size','price','priceChange']
    df = df_org[cols].copy()
    df['UNIXTIME'] = df['UNIXTIME'].astype(int)
    df['side'] = np.where(df['side'] == 'Buy', 1, np.where(df['side'] == 'Sell', -1, 0))
    df['priceChange'] = np.where(df['priceChange'] == 'PlusTick', 1, np.where(df['priceChange'] == 'MinusTick', -1, 0))
    df['price'] = df['price'].astype(float)
    df['size'] = df['size'].astype(float)
    df['price*size'] = df['price'] * df['size']
    df = df.sort_values('UNIXTIME')
    return df
    
def generateBaseFeatures(df):
        cols1 = ['open', 'high', 'low', 'close', 'mean', 'VWMean', 'median', '25%', '50%', '75%','center']
        cols2 = ['buySideMean', 'sellSideMean', 'buySideVWMean', 'sellSideVWMean', 'buySideMedian', 'sellSideMedian', 'buySideCenter', 'sellSideCenter',\
            'buySide25%', 'buySide50%', 'buySide75%', 'sellSide25%', 'sellSide50%', 'sellSide75%']
        cols3 = ['sideMean', 'sideMedian', 'priceChangeMean']
        cols4 = ['opentime', 'closetime', 'time25%', 'time50%', 'time75%']
        cols = ['UNIXTIME'] + cols1 + cols2 + cols3 + cols4
        series = pd.Series(index=cols)
        n = df.shape[0]
        n_25 = int(n*0.25)
        n_50 = int(n*0.50)
        n_75 = int(n*0.75)
        vol_mean = df['size'].sum()
        series['UNIXTIME'] = df['UNIXTIME'].iloc[-1]
        series['open'] = df['price'].iloc[0]
        series['high'] = df['price'].max()
        series['low'] = df['price'].min()
        series['close'] = df['price'].iloc[-1]
        series['mean'] = df['price'].mean()
        series['VWMean'] = df['price*size'].sum() / vol_mean
        series['median'] = df['price'].median()
        series['25%'] = df['price'].iloc[n_25]
        series['50%'] = df['price'].iloc[n_50]
        series['75%'] = df['price'].iloc[n_75]
        series['center'] = (series['high'] + series['low']) / 2
        
        n_buy = df[df['side'] == 1].shape[0]
        n_sell = df[df['side'] == -1].shape[0]
        n_buy_25 = int(n_buy*0.25)
        n_buy_50 = int(n_buy*0.50)
        n_buy_75 = int(n_buy*0.75)
        n_sell_25 = int(n_sell*0.25)
        n_sell_50 = int(n_sell*0.50)
        n_sell_75 = int(n_sell*0.75)
        series['buySideMean'] = df[df['side'] == 1]['price'].mean()
        series['sellSideMean'] = df[df['side'] == -1]['price'].mean()
        series['buySideCenter'] = (df[df['side'] == 1]['price'].max() + df[df['side'] == 1]['price'].min()) / 2
        series['sellSideCenter'] = (df[df['side'] == -1]['price'].max() + df[df['side'] == -1]['price'].min()) / 2
        series['buySideMedian'] = df[df['side'] == 1]['price'].median()
        series['sellSideMedian'] = df[df['side'] == -1]['price'].median()
        series['buySideVWMean'] = df[df['side'] == 1]['price*size'].sum() / df[df['side'] == 1]['size'].sum() if n_buy != 0 else 0
        series['sellSideVWMean'] = df[df['side'] == -1]['price*size'].sum() / df[df['side'] == -1]['size'].sum() if n_sell != 0 else 0
        series['buySide25%'] = df[df['side'] == 1]['price'].iloc[n_buy_25] if n_buy != 0 else 0
        series['buySide50%'] = df[df['side'] == 1]['price'].iloc[n_buy_50] if n_buy != 0 else 0
        series['buySide75%'] = df[df['side'] == 1]['price'].iloc[n_buy_75] if n_buy != 0 else 0
        series['sellSide25%'] = df[df['side'] == -1]['price'].iloc[n_sell_25] if n_sell != 0 else 0
        series['sellSide50%'] = df[df['side'] == -1]['price'].iloc[n_sell_50] if n_sell != 0 else 0
        series['sellSide75%'] = df[df['side'] == -1]['price'].iloc[n_sell_75] if n_sell != 0 else 0
        series['sideMean'] = df['side'].mean()
        series['sideMedian'] = df['side'].median()
        series['priceChangeMean'] = df['priceChange'].mean()
        series['opentime'] = df['UNIXTIME'].iloc[0]
        series['closetime'] = df['UNIXTIME'].iloc[-1]
        series['time25%'] = df['UNIXTIME'].iloc[n_25]
        series['time50%'] = df['UNIXTIME'].iloc[n_50]
        series['time75%'] = df['UNIXTIME'].iloc[n_75]
        series = series.fillna(0)
        return series