from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from redis_om import get_redis_connection, NotFoundError

from order import order_info, OrderModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

redis_connect = get_redis_connection(
    host='redis-15425.c72.eu-west-1-2.ec2.cloud.redislabs.com',
    port=15425,
    password='aMfi11n9Y62jzanGo90wRJulBDpa1f2r',
    decode_responses=True
)

orders = order_info(redis_connect)

@app.post('/orders')
async def create_order(request: Request):
    body = await request.json()