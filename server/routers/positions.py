from fastapi import APIRouter, Depends
import redis.asyncio as redis
from resources.redis_client import get_redis_client
from resources.database_client import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/positions", tags=["positions"])

@router.get("/")
async def get_prices():
    return {"prices": []}


@router.get("/{symbol}")
async def get_price(symbol: str, r: redis.Redis = Depends(get_redis_client), db: AsyncSession = Depends(get_db)):
    price = await r.get(f"prices:{symbol.upper()}")
    if not price:
        return {"error": "symbol not found"}
    return {"symbol": symbol.upper(), "price": float(price)}


