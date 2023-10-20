import time

from main import redis_connect
from product import product_info


Products = product_info(redis_connect)

key = 'order_completed'          # consumer name
group = 'inventory-group'        # consumer group

try:
    redis_connect.xgroup_create(key, group)
except:
    print('Group already exists.')

while True:
    try:
        results = redis_connect.xreadgroup(group, key, {key: '>'}, None)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                product = Products.get(obj['product_id'])
                
                print(product)
                product.quantity_available = int(product.quantity_available) - int(obj['quantity'])
                product.save()

        
    except Exception as e:
        print(str(e))
        
    time.sleep(1)
