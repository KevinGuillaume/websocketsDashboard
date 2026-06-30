import asyncio
import json
import redis.asyncio as redis
from resources.connection_manager import manager

async def price_listener():
    while True:
        try:
            # Dedicated connection for pub/sub, not from the shared pool
            r = redis.Redis(
                host="localhost",
                port=6379,
                decode_responses=True,
                socket_timeout=None,           # ← no timeout, keep alive forever
                socket_keepalive=True,
            )
            async with r.pubsub() as ps:
                await ps.psubscribe("prices:*")
                print("Redis listener subscribed")
                async for msg in ps.listen():
                    if msg["type"] != "pmessage":
                        continue
                    symbol = msg["channel"].split(":")[1]
                    price  = float(msg["data"])
                    print(f"Broadcasting {symbol}: {price} to {len(manager.active)} clients")
                    await manager.broadcast(json.dumps({
                        "symbol": symbol,
                        "price":  price
                    }))
        except Exception as e:
            print(f"Listener crashed: {e}, reconnecting in 3s...")
            await asyncio.sleep(3)