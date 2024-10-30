import asyncio
import json
import websockets

# group分けする条件を設定
base_price = -1 
thres = 0.2 / 100  # base_priceからthres%以上価格が乖離するまで1グループとみなす
group = []  # グループを入れる箱
RECONNECT_DELAY = 5  # 再接続までの待機時間（秒）
CHUNK_SIZE = 1000  # 分割サイズ（必要に応じて調整）

async def send_to_aggregate1(data):
    data_id = id(data)  # データごとに一意のIDを生成
    total_packets = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE  # 総パケット数
    async with websockets.connect('ws://192.168.2.3:8765') as websocket:
        for i in range(total_packets):
            chunk = data[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
            packet = {
                "data_id": data_id,
                "packet_number": i + 1,
                "total_packets": total_packets,
                "chunk": chunk
            }
            await websocket.send(json.dumps(packet))
        
async def send_to_aggregate2(data):
    data_id = id(data)  # データごとに一意のIDを生成
    total_packets = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE  # 総パケット数
    async with websockets.connect('ws://192.168.2.4:8765') as websocket:
        for i in range(total_packets):
            chunk = data[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
            packet = {
                "data_id": data_id,
                "packet_number": i + 1,
                "total_packets": total_packets,
                "chunk": chunk
            }
            await websocket.send(json.dumps(packet))
      
async def start_bybit_stream():
    global base_price, thres, group

    while True:
        try:
            async with websockets.connect('wss://stream.bybit.com/v5/public/linear') as bybit_ws:
                bybit_payload = {"op": "subscribe", "args": ["publicTrade.BTCUSDT"]}
                await bybit_ws.send(json.dumps(bybit_payload))

                while True:
                    response = await bybit_ws.recv()
                    message = json.loads(response)
                    if 'topic' in message and message['topic'] == 'publicTrade.BTCUSDT':
                        trades = message['data']
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
                            price = float(trade['price'])
                            if base_price < 0:
                                base_price = price
                            alpha = abs(price - base_price) / base_price
                            if  alpha > thres:
                                group += trades_histories[:i]
                                await send_to_aggregate2(group)
                                base_price = price
                                group = trades_histories[i:]
                                flg = False
                        if flg:
                            group += trades_histories
                        # print(f'{alpha*100:.4f}/{thres*100:.3f}', base_price, price)
                        await send_to_aggregate1(trades_histories)
                        
        except websockets.ConnectionClosedError as e:
            print("WebSocket connection closed, reconnecting in", RECONNECT_DELAY, "seconds:", e)
            await asyncio.sleep(RECONNECT_DELAY)  # 待機後に再接続を試行
        except Exception as e:
            print("An error occurred:", e)
            await asyncio.sleep(RECONNECT_DELAY)  # 待機後に再接続を試行

async def main():
    print('start bybit steam')
    await start_bybit_stream()

asyncio.run(main())
