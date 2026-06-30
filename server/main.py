from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, Depends
from routers import positions
from resources.redis_client import get_redis_client,pool
from resources.database_client import engine
from binance_injestor import price_ingester
from binance_listener import price_listener
from resources.connection_manager import manager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server starting...")
    r = get_redis_client()
    await r.ping()
    print("Redis connected")
    print("MySQL ready")
    asyncio.create_task(price_ingester())
    print("Ingester task started") 
    asyncio.create_task(price_listener())
    print("Listener task started") 

    yield
    await pool.disconnect()
    await engine.dispose()
    print("Server shutting down...")

app = FastAPI(
    title="Web socket app server",
    version="1.0.0",
    lifespan=lifespan
)

# WebSocket endpoint — React connects here
@app.websocket("/ws/prices")
async def websocket_prices(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()    # keeps connection alive
    except Exception:
        manager.disconnect(ws)

app.include_router(positions.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

