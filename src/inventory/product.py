from redis_om import HashModel
from pydantic import BaseModel


def product_info(redis):
    class Product(HashModel):
        name: str
        price: float
        quantity_available = int

        class Meta:
            database = redis

    return Product


class ProductModel(BaseModel):
    name: str
    price: float
    quantity_available: int