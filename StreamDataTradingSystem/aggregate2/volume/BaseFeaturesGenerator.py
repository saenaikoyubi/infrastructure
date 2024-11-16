import pandas as pd
import numpy as np

from cols import Params
prms = Params()

cols1 = prms.cols1
cols2 = prms.cols2
cols3 = prms.cols3
cols4 = prms.cols4
cols5 = prms.cols5

class BaseFeaturesGenerator:
    def __init__(self):
        self.cols1 = cols1
        self.cols2 = cols2
        self.cols3 = cols3
        self.cols4 = cols4
        self.cols5 = cols5
        
    def generateBaseDf(self, df_org:pd.DataFrame):
        cols = ['UNIXTIME','side','size','price','priceChange']
        df = df_org[cols].copy()
        del df_org
        df['UNIXTIME'] = df['UNIXTIME'].astype(int)
        df['side'] = np.where(df['side'] == 'Buy', 1, np.where(df['side'] == 'Sell', -1, 0))
        df['priceChange'] = np.where(df['priceChange'] == 'PlusTick', 1, np.where(df['priceChange'] == 'MinusTick', -1, 0))
        df['price'] = df['price'].astype(float)
        df['size'] = df['size'].astype(float)
        df['price*size'] = df['price'] * df['size']
        df['side*size'] = df['side'] * df['size']
        df = df.sort_values('UNIXTIME')
        df = df.astype(float)
        return df
    
    def generateBaseFeatures(self, df:pd.DataFrame):
            cols = ['UNIXTIME'] + self.cols1 + self.cols2 + self.cols3 + self.cols4 + self.cols5
            series = pd.Series(index=cols)
            df = df.sort_index()
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
            rePrice = df['price'] - df['price'].iloc[0]
            rePrice = rePrice / rePrice.std()
            reCuSize = df['side*size'].cumsum()
            reCuSize = reCuSize - reCuSize.iloc[0]
            reCuSize = reCuSize / reCuSize.std()
            series['reHighPrice'] = rePrice.max()
            series['reLowPrice'] = rePrice.min()
            series['reClosePrice'] = rePrice.iloc[-1]
            series['reMeanPrice'] = rePrice.mean()
            series['re25%Price'] = rePrice.iloc[n_25]
            series['re50%Price'] = rePrice.iloc[n_50]
            series['re75%Price'] = rePrice.iloc[n_75]
            series['reCenterPrice'] = (series['reHighPrice']+series['reLowPrice']) / 2
            series['reHighCuSize'] = reCuSize.max()
            series['reLowCuSize'] = reCuSize.min()
            series['reCloseCuSize'] = reCuSize.iloc[-1]
            series['reMeanCuSize'] = reCuSize.mean()
            series['re25%CuSize'] = reCuSize.iloc[n_25]
            series['re50%CuSize'] = reCuSize.iloc[n_50]
            series['re75%CuSize'] = reCuSize.iloc[n_75]
            series['reCenterCuSize'] = (series['reHighCuSize']+series['reLowCuSize']) / 2
            
            series = series.fillna(0)
            del df
            return series