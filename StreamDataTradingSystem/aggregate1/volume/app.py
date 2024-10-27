import asyncio
import websockets
import json
import psycopg2

# サーバのホストとポートを設定（サーバ3はポート12347、サーバ4は12348）
HOST = 'localhost'
PORT = 12345  # サーバ3なら12347、サーバ4なら12348に設定

# データベース接続設定
conn = psycopg2.connect("dbname=mydatabase user=user password=password host=db")
cursor = conn.cursor()

def insert_trade(trade):
    insert_query = 'INSERT INTO stream (UNIXTIME, side, size, price, priceChange, tradeID, blockTrade) VALUES ({}, \'{}\', {}, {}, \'{}\', \'{}\', \'{}\')'.format(
        trade['UNIXTIME'],
        trade['side'],
        trade['size'],
        trade['price'],
        trade['priceChange'],
        trade['tradeID'],
        trade['blockTrade']
    )
    cursor.execute(insert_query)
    conn.commit()

async def handle_data(websocket):
    async for message in websocket:
        # 受信したメッセージをJSONデコードしてリスト形式に変換
        trades_histories = json.loads(message)
        
        # 取引履歴のリストをループし、各取引データを表示
        for trade in trades_histories:
            insert_trade(trade)
            

async def start():
    # 指定ホストとポートでWebSocketサーバを起動
    async with websockets.serve(handle_data, HOST, PORT):
        print(f"Server started on ws://{HOST}:{PORT}")
        await asyncio.Future()  # 永遠に実行し続ける

# サーバ起動
asyncio.run(start())
