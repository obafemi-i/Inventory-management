from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'], 
    allow_headers=['*']

)
redis = get_redis_connection(
    host='redis-18015.c59.eu-west-1-2.ec2.cloud.redislabs.com',
    port=18015,
    password='8xV1WSZnLc1OOFIUQtF3O3W93nOPGW47',
    decode_responses=True
)


class Itemss(HashModel):
    name:str
    price:float
    quantity:int

    class Meta:
        database=redis



@app.get('/products') 
def all():
    return [format(pk) for pk in Itemss.all_pks()]


def format(pk:str):
    product = Itemss.get(pk)
    return {
        'id': product.pk,
        'name':product.name,
        'price':product.price,
        'quantity':product.quantity
    }


@app.post('/products')
def create(product:Itemss):
    return product.save()

@app.get('/products/{pk}')
def get_item(pk:str):
    return Itemss.get(pk)

@app.delete('/products/{pk}')
def delete(pk:str):
    return Itemss.delete(pk)
