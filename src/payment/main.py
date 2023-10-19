from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from starlette.requests import Request
import time
from redis_om import get_redis_connection, NotFoundError
from dotenv import dotenv_values
import requests

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

Orders = order_info(redis_connect)


@app.get('/orders/{pk}')
async def get_single_order(pk: str):
    orders = Orders.get(pk)
    return orders



@app.post('/orders')
async def create_order(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()           # id and quantity
    id = body['id']

    req = requests.get(f'http://localhost:8000/products/{id}')

    product = req.json()

    order = Orders(
        product_id=id,
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )

    order.save()

    background_tasks.add_task(completed, order)

    # await completed(order)

    return order

def completed(order: Orders):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis_connect.xadd('order_completed', order.model_dump(), '*')
