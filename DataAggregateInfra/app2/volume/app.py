
from pybit.unified_trading import WebSocket
import psycopg2
from time import sleep

# データベース接続設定
conn = psycopg2.connect("dbname=mydatabase user=user password=password host=db")
cursor = conn.cursor()

# # データベースに取引履歴を挿入する関数
def insert_trade_history(trade_history):
    insert_query = 'INSERT INTO stream (UNIXTIME, side, size, price, priceChange, tradeID, blockTrade) VALUES ({}, \'{}\', {}, {}, \'{}\', \'{}\', \'{}\')'.format(
        trade_history['UNIXTIME'],
        trade_history['side'],
        trade_history['size'],
        trade_history['price'],
        trade_history['priceChange'],
        trade_history['tradeID'],
        trade_history['blockTrade']
    )
    cursor.execute(insert_query)
    conn.commit()

def handle_message(message):
    if 'topic' in message and message['topic'] == 'publicTrade.BTCUSDT':
        trades = message['data']
        for trade in trades:
            trade_history = {
                'UNIXTIME': trade['T'],
                'side': trade['S'],
                'size': trade['v'],
                'price': trade['p'],
                'priceChange': trade['L'],
                'tradeID': trade['i'],
                'blockTrade': trade['BT']
            }
            insert_trade_history(trade_history)

if __name__ == "__main__":
    try:
        ws = WebSocket(
            testnet=False,
            channel_type="linear",
        )

        ws.trade_stream(
            symbol="BTCUSDT",
            callback=handle_message
        )
        while True:
            sleep(1)
    except Exception as e:
        print(f"Exception occurred: {e}")

