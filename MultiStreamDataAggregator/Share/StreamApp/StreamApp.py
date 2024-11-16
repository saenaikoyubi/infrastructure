import asyncio
import json
import websockets
import psycopg2

# from .Share.ShareParam.ShareParam import ShareParam
from app.Share.ShareParam.ShareParam import ShareParam
shprm = ShareParam()
DBNAME = shprm.DBNAME
USER = shprm.USER
PASSWORD = shprm.PASSWORD
HOST = shprm.HOST
RECONNECT_DELAY = shprm.RECONNECT_DELAY

from app.Personal.Param.Param import Param
prm = Param()
symbol = prm.symbol

class StreamApp:
    def __init__(self):
    # データベース接続設定
        self.RECONNECT_DELAY = RECONNECT_DELAY
        self.symbol = symbol
        self.reset_DB_connection()

    def reset_DB_connection(self):
        self.conn = psycopg2.connect(f'dbname={DBNAME} user={USER} password={PASSWORD} host={HOST}')
        self.cursor = self.conn.cursor()

    def insert_trade(self, trade):
        try:
            insert_query = f'INSERT INTO "stream{self.symbol}" ("UNIXTIME", "side", "size", "price", "priceChange", "tradeID", "blockTrade") VALUES (%s, %s, %s, %s, %s, %s, %s)'
            self.cursor.execute(insert_query, (
                trade['UNIXTIME'],
                trade['side'],
                trade['size'],
                trade['price'],
                trade['priceChange'],
                trade['tradeID'],
                trade['blockTrade']
            ))
            self.conn.commit()
        except Exception as e:
            print(f"Failed to insert trade: {e}")
            self.conn.rollback()
            return False
        return True
      
    async def start_bybit_stream(self):
        while True:
            try:
                async with websockets.connect('wss://stream.bybit.com/v5/public/linear') as bybit_ws:
                    bybit_payload = {"op": "subscribe", "args": [f'publicTrade.{self.symbol}']}
                    await bybit_ws.send(json.dumps(bybit_payload))

                    while True:
                        response = await bybit_ws.recv()
                        message = json.loads(response)
                        if 'topic' in message and message['topic'] == f'publicTrade.{self.symbol}':
                            trades = message['data']
                            for trade in trades:
                                trades_history = {
                                        'UNIXTIME': trade['T'],
                                        'side': trade['S'],
                                        'size': trade['v'],
                                        'price': trade['p'],
                                        'priceChange': trade['L'],
                                        'tradeID': trade['i'],
                                        'blockTrade': trade['BT']
                                    } 
                                self.insert_trade(trade=trades_history)
                            
            except websockets.ConnectionClosedError as e:
                print("WebSocket connection closed, reconnecting in", self.RECONNECT_DELAY, "seconds:", e)
                await asyncio.sleep(self.RECONNECT_DELAY)  # 待機後に再接続を試行
            except Exception as e:
                print("An error occurred:", e)
                await asyncio.sleep(self.RECONNECT_DELAY)  # 待機後に再接続を試行

    async def main(self):
        print('start bybit steam')
        await self.start_bybit_stream()
        return True

    def run(self):
        asyncio.run(self.main())
        return True
        

