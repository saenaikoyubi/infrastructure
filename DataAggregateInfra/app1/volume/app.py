import time
import requests
import psycopg2
import pandas as pd

BYBIT_API_URL = "https://api.bybit.com/v2/public/orderBook/L2?symbol=BTCUSD"

# Database connection settings
DB_HOST = "db"
DB_NAME = "mydatabase"
DB_USER = "user"
DB_PASSWORD = "password"

# symbol
symbol = 'BTCUSDT'

def fetch_orderbook(symbol):
    url = "https://api.bybit.com/v5/market/orderbook"
    params = {
        "category": 'linear',
        "symbol": symbol,
        "limit": 100
    }
    response = requests.get(url, params=params)
    data = response.json()
    bid = pd.DataFrame(columns=['price', 'size'], data=data['result']['b'], dtype='float64').sort_values('price')[::-1].reset_index(drop=True)
    ask = pd.DataFrame(columns=['price', 'size'], data=data['result']['a'], dtype='float64').sort_values('price').reset_index(drop=True)
    return ask, bid

def _insert_step(data, tb_name, unixtime):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(
    f"INSERT INTO {tb_name} VALUES (%s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s "
    ")",
        (unixtime, *data)
    )
    conn.commit()
    cur.close()
    conn.close()
    return True

def save_orderbook():
    ask, bid = fetch_orderbook(symbol=symbol)
    unixtime = int(time.time())
    askprice = [float(d) for d in ask['price'].values]
    asksize = [float(d) for d in ask['size'].values]
    bidprice = [float(d) for d in bid['price'].values]
    bidsize = [float(d) for d in bid['size'].values]
    _insert_step(data=askprice, tb_name='askprice', unixtime=unixtime)
    _insert_step(data=asksize, tb_name='asksize', unixtime=unixtime)
    _insert_step(data=bidprice, tb_name='bidprice', unixtime=unixtime)
    _insert_step(data=bidsize, tb_name='bidsize', unixtime=unixtime)
    return True

if __name__ == '__main__':
    try:
        while True:
            save_orderbook()
            time.sleep(1)
            
    except Exception as e:
        print(f"Exception occurred: {e}")
