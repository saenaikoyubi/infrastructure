import asyncio
import websockets
import json
import psycopg2

# サーバのホストとポートを設定
HOST = "0.0.0.0"
PORT =  8765

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

# 受信したデータを保持する辞書
received_data = {}

async def handle_client(websocket, path):
    global received_data
    async for message in websocket:
        packet = json.loads(message)
        data_id = packet["data_id"]
        packet_number = packet["packet_number"]
        total_packets = packet["total_packets"]
        chunk = packet["chunk"]

        # 初めてのdata_idの場合、エントリを初期化
        if data_id not in received_data:
            received_data[data_id] = {
                "chunks": [None] * total_packets,
                "received_count": 0
            }
        
        # チャンクを保存
        received_data[data_id]["chunks"][packet_number - 1] = chunk
        received_data[data_id]["received_count"] += 1

        # 全パケットが揃った場合に結合
        if received_data[data_id]["received_count"] == total_packets:
            full_data = [item for sublist in received_data[data_id]["chunks"] for item in sublist]
            for trade in full_data:
                insert_trade(trade=trade)
            
            # 使用済みデータを削除
            del received_data[data_id]

async def main():
    # WebSocketサーバーを起動してクライアントの接続を待機
    async with websockets.serve(handle_client, HOST, PORT):
        print(f"WebSocket server started on ws://{HOST}:{PORT}")
        await asyncio.Future()  # サーバーを無期限に実行

# 実行
asyncio.run(main())
