import asyncio
import websockets
import json
import pandas as pd
import psycopg2
from helper import generateBaseDf, generateBaseFeatures

# サーバのホストとポートを設定（サーバ3はポート12347、サーバ4は12348）
HOST = "0.0.0.0"
PORT = 8765

# データベース接続設定
conn = psycopg2.connect("dbname=mydatabase user=user password=password host=db")
cursor = conn.cursor()


def insert_trade(trade):
    insert_query = 'INSERT INTO baseFeatures (UNIXTIME, open, high, low, close, mean, VWMean, median, "25%", "50%", "75%",\
                    center, buySideMean, sellSideMean, buySideVWMean, sellSideVWMean, buySideMedian, sellSideMedian, buySideCenter, sellSideCenter, "buySide25%", \
                        "buySide50%", "buySide75%", "sellSide25%", "sellSide50%", "sellSide75%", sideMean, sideMedian, priceChangeMean, opentime, closetime, \
                            "time25%", "time50%", "time75%") VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, \
                                                                {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, \
                                                                    {}, {}, {}, {}, {}, {}, {}, {}, {}, {},\
                                                                        {}, {}, {}, {})'.format(
        trade['UNIXTIME'],
        trade['open'],
        trade['high'],
        trade['low'],
        trade['close'],
        trade['mean'],
        trade['VWMean'],
        trade['median'],
        trade['25%'],
        trade['50%'],
        trade['75%'],
        trade['center'],
        trade['buySideMean'],
        trade['sellSideMean'],
        trade['buySideVWMean'],
        trade['sellSideVWMean'],
        trade['buySideMedian'],
        trade['sellSideMedian'],
        trade['buySideCenter'],
        trade['sellSideCenter'],
        trade['buySide25%'],
        trade['buySide50%'],
        trade['buySide75%'],
        trade['sellSide25%'],
        trade['sellSide50%'],
        trade['sellSide75%'],
        trade['sideMean'],
        trade['sideMedian'],
        trade['priceChangeMean'],
        trade['opentime'],
        trade['closetime'],
        trade['time25%'],
        trade['time50%'],
        trade['time75%']
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
            print("Received full data:")
            df = pd.DataFrame(full_data)
            base_df = generateBaseDf(df_org=df)
            base_feature_df = generateBaseFeatures(df=base_df)
            insert_trade(base_feature_df)

            # 使用済みデータを削除
            del received_data[data_id]

async def main():
    # WebSocketサーバーを起動してクライアントの接続を待機
    async with websockets.serve(handle_client, HOST, PORT):
        print(f"WebSocket server started on ws://{HOST}:{PORT}")
        await asyncio.Future()  # サーバーを無期限に実行

# 実行
asyncio.run(main())
