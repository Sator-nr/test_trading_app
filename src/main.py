from __future__ import annotations

from typing import Annotated, Union
from fastapi import FastAPI, Depends
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from operations.router import router as router_operation
from src.auth.models import User
from tasks.router import router as router_tasks
from redis import asyncio as aioredis

app = FastAPI(
    title='Trading App'
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
app.include_router(router_tasks)


async def common_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding='utf8', decode_responce=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')

