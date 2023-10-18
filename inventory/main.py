from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection

from product import product_info, ProductResult

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

Products = product_info(redis_connect)


@app.get('/products')
async def all():
    return [await format(pk) for pk in Products.all_pks()]


async def format(pk: str):
    product = Products.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity_available
    }


@app.post('/products')
async def create_product(prods: ProductResult):
    product_data = Products(**prods.model_dump())
    product_data.save()

    return product_data


@app.get('/products/{pk}')
async def get_one(pk: str):
    product_data = Products.get(pk)
    return product_data
 