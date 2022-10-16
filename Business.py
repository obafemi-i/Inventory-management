from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'], 
    allow_headers=['*']

)

# This should be a different database but i didnt want to pay for a redis subscription. Another platform like mongodb would work here
redis = get_redis_connection(
    host='redis-18015.c59.eu-west-1-2.ec2.cloud.redislabs.com',
    port=18015,
    password='8xV1WSZnLc1OOFIUQtF3O3W93nOPGW47',
    decode_responses=True
)


class Order(HashModel):
    product_id:str
    price:float
    fee:float
    total:float
    quantity:int
    status:str # pending, complete, refund
  

    class Meta:
        database=redis


@app.get('/orders/{pk}')
def ger(pk:str):
    return Order.get(pk)


@app.post('/orders')
async def create (request:Request, background_tasks:BackgroundTasks):
    body = await request.json()

    r = requests.get(f'http://127.0.0.1:8001/ {body["id"]}')
    product = r.json()

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total = 1.2 * product['price'],
        quantity = body['quantity'],
        status = 'pending'
    )

    order.save()

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order:Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
    