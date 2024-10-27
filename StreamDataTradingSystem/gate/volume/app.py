import asyncio
import json
import websockets
from pybit.unified_trading import WebSocket

# BybitのWebSocket接続を設定
ws = WebSocket(testnet=False)  # テスト環境。実際の取引環境の場合はtestnet=False

# group分けする条件を設定
base_price = -1 
thres = 0.2 / 100 # base_priceからthres%以上価格が乖離するまで1グループとみなす
group = [] # グループを入れる箱
group_for_send = []

async def bybit_stream_handler():
    async for message in ws.stream('public', 'publicTrade.BTCUSDT'):
        data = json.loads(message)
        
        # メッセージが`publicTrade.BTCUSDT`トピックかどうかを確認
        if 'topic' in data and data['topic'] == 'publicTrade.BTCUSDT':
            trades = data['data']
            
            # 各取引データをリスト内辞書形式で整形
            trades_histories = [
                {
                    'UNIXTIME': trade['T'],
                    'side': trade['S'],
                    'size': trade['v'],
                    'price': trade['p'],
                    'priceChange': trade['L'],
                    'tradeID': trade['i'],
                    'blockTrade': trade['BT']
                } for trade in trades
            ]
            flg = True
            for i, trade in enumerate(trades_histories):
                if base_price < 0:
                    base_price = float(trade['price'])
                if abs(float(trade['price']) - base_price) / base_price > thres:
                        group += trades_histories[:i]
                        await send_to_aggregate2(group)
                        base_price = float(trade['price'])
                        group = [trades_histories][i:]
                        flg = False
                if flg:
                    group += trades_histories

            # 整形されたリストデータをサーバ3とサーバ4に送信
            await send_to_aggregate1(trades_histories)



async def send_to_aggregate1(data):
    async with websockets.connect('ws://192.168.1.3:12345') as websocket:
        await websocket.send(json.dumps(data))

async def send_to_aggregate2(data):
    async with websockets.connect('ws://192.168.1.4:12345') as websocket:
        await websocket.send(json.dumps(data))

async def start_bybit_stream():
    await bybit_stream_handler()  # Bybitのストリームからデータを受信

# asyncio.run(start_bybit_stream())で実行
asyncio.run(start_bybit_stream())
