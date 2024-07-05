import psycopg2
import numpy as np
import pandas as pd
import datetime

# Database connection settings
DB_HOST = "db"
DB_NAME = "mydatabase"
DB_USER = "user"
DB_PASSWORD = "password"

def get_data(tb_name, n):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    n += 20
    cur.execute(f"SELECT * FROM {tb_name} ORDER BY UNIXTIME DESC LIMIT {n};")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    rows = np.array(rows)
    times = rows[:, 0]
    data = rows[:, 1:]
    df = pd.DataFrame(columns=[f'{i}' for i in range(100)], index=times, data=data)[::-1]
    return df

def get_df(n=100):
    askprice_df = get_data('askprice', n=n)
    asksize_df = get_data('asksize', n=n)
    bidprice_df = get_data('bidprice', n=n)
    bidsize_df = get_data('bidsize', n=n)
    last_unixtime = np.min([askprice_df.index[-1], asksize_df.index[-1], bidprice_df.index[-1], bidsize_df.index[-1]])
    askprice_df = askprice_df.loc[:last_unixtime]
    asksize_df = asksize_df.loc[:last_unixtime]
    bidprice_df = bidprice_df.loc[:last_unixtime]
    bidsize_df = bidsize_df.loc[:last_unixtime].apply(lambda x: -x)
    
    askprice_df.index = [datetime.datetime.fromtimestamp(unixtime) for unixtime in askprice_df.index]
    asksize_df.index = [datetime.datetime.fromtimestamp(unixtime) for unixtime in asksize_df.index]
    bidprice_df.index = [datetime.datetime.fromtimestamp(unixtime) for unixtime in bidprice_df.index]
    bidsize_df.index = [datetime.datetime.fromtimestamp(unixtime) for unixtime in bidsize_df.index]
    return askprice_df, asksize_df, bidprice_df, bidsize_df

def fillna_with_mean(df):
    df_copy = df.copy()
    
    for col in df_copy.columns:
        mask = df_copy[col].isna()
        
        for i in df_copy[mask].index:
            prev_idx = df_copy.index.get_loc(i) - 1
            next_idx = df_copy.index.get_loc(i) + 1
            
            prev_val = df_copy[col].iloc[prev_idx] if prev_idx >= 0 else np.nan
            next_val = df_copy[col].iloc[next_idx] if next_idx < len(df_copy) else np.nan
            
            if not pd.isna(prev_val) and not pd.isna(next_val):
                df_copy[col].at[i] = (prev_val + next_val) / 2
            elif not pd.isna(prev_val):
                df_copy[col].at[i] = prev_val
            elif not pd.isna(next_val):
                df_copy[col].at[i] = next_val
                
    return df_copy

def get_df_1min(n=5000):
    askprice_df, asksize_df, bidprice_df, bidsize_df = get_df(n=n)
    askprice_df = fillna_with_mean(df=askprice_df.resample('1min').mean())
    asksize_df = fillna_with_mean(df=asksize_df.resample('1min').mean())
    bidprice_df = fillna_with_mean(df=bidprice_df.resample('1min').mean())
    bidsize_df = fillna_with_mean(df=bidsize_df.resample('1min').mean())
    return askprice_df, asksize_df, bidprice_df, bidsize_df
    
