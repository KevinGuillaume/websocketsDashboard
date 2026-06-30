import asyncio
import json
import websockets
import redis.asyncio as redis
from resources.redis_client import pool

SYMBOLS = ["btcusdt", "ethusdt", "bnbusdt"]

async def price_ingester():
    r = redis.Redis(connection_pool=pool, decode_responses=True)
    streams = "/".join([f"{s}@miniTicker" for s in SYMBOLS])
    url = f"wss://stream.binance.us:9443/stream?streams={streams}"

    while True:
        try:
            async with websockets.connect(url) as ws:
                print("Binance connected")
                async for message in ws:
                    data   = json.loads(message)
                    inner  = data["data"]
                    symbol = inner["s"]           # "BTCUSDT"
                    price  = float(inner["c"])    # latest price

                    # Store latest price
                    await r.set(f"prices:{symbol}", price)
                    # Notify listener
                    await r.publish(f"prices:{symbol}", price)

        except Exception as e:
            print(f"Binance disconnected: {e}, reconnecting in 5s...")
            await asyncio.sleep(5)