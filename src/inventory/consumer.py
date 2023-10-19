from main import redis_connect
from product import product_info

import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis_connect.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        redis_connect.xreadgroup(group, key, {key: '>'}, None)
    except Exception as e:
        print(str(e))
        
    time.sleep(5)
