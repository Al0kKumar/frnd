import redis.asyncio as redis
import json
import os
from typing import Any

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

r = redis.from_url(REDIS_URL, decode_responses=True)

async def set_cache(key: str, value: Any, expire_seconds: int = 300):
    """
    Set a value in Redis with optional expiration (default 5 mins)
    """
    if value is None:
        await r.delete(key)
        return
    await r.set(key, json.dumps(value), ex=expire_seconds)

async def get_cache(key: str):
    """
    Retrieve a value from Redis. Returns Python object or None if not found.
    """
    value = await r.get(key)
    if value:
        return json.loads(value)
    return None

async def delete_cache(key: str):
    """
    Delete a cache key from Redis
    """
    await r.delete(key)
