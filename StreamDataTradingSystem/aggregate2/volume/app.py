import asyncio
import websockets
import json
import pandas as pd

# サーバのホストとポートを設定（サーバ3はポート12347、サーバ4は12348）
HOST = 'localhost'
PORT = 12345  # サーバ3なら12347、サーバ4なら12348に設定

base_price = -1
thres = 0.2 / 100
group = []

async def handle_data(websocket):
    async for message in websocket:
        # 受信したメッセージをJSONデコードしてリスト形式に変換
        group = json.loads(message)
        
        df = pd.DataFrame(group)
        print(df)
        
                 


async def start_server():
    # 指定ホストとポートでWebSocketサーバを起動
    async with websockets.serve(handle_data, HOST, PORT):
        print(f"Server started on ws://{HOST}:{PORT}")
        await asyncio.Future()  # 永遠に実行し続ける

# サーバ起動
asyncio.run(start_server())
