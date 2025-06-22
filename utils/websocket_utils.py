import json
import websockets
import datetime
import os

async def monitor_market(asset_ids, output_fp, title=None):
    output_fp = f"{output_fp}.json"
    url = 'wss://ws-subscriptions-clob.polymarket.com/ws/market'
    last_time_pong = datetime.datetime.now()

    if title:
        print(f"Monitoring: {title}")

    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({"assets_ids":asset_ids,"type":"market"}))

        option = "a" if os.path.exists(output_fp) else "w"

        with open(output_fp, option) as f:
            while True:
                m = await websocket.recv()
                if m != "PONG":
                    last_time_pong = datetime.datetime.now()
                d = json.loads(m)
                print(d)
                json.dump(d, f)
                if last_time_pong + datetime.timedelta(seconds=10) < datetime.datetime.now():
                    await websocket.send("PING")
