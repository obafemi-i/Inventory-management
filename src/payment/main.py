from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from redis_om import get_redis_connection, NotFoundError
from dotenv import dotenv_values

from order import order_info, OrderModel


config = dotenv_values()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

redis_connect = get_redis_connection(
    host=config.get('HOST'),
    port=config.get('PORT'),
    password=config.get('PASSWORD'),
    decode_responses=True
)

orders = order_info(redis_connect)

@app.post('/orders')
async def create_order(request: Request):
    body = await request.json()
