from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, NotFoundError
from dotenv import dotenv_values

from product import product_info, ProductModel

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
async def create_product(prods: ProductModel):
    product_data = Products(**prods.model_dump())
    product_data.save()

    return product_data


@app.get('/products/{pk}')
async def get_one(pk: str):
    try:
        product_data = Products.get(pk)
        return product_data
    except NotFoundError:
        return {'Message': 'No product'}

@app.delete('/products/{pk}')
async def get_one(pk: str):
    return Products.delete(pk)
 