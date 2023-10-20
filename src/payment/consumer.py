import time

from main import redis_connect
from order import order_info


Orders = order_info(redis_connect)

key = 'refund_order'          # consumer name
group = 'payment-group'        # consumer group

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

                print(result)
                
                order = Orders.get(obj['pk'])
                order.status = 'refunded'
                order.save()

        
    except Exception as e:
        print(str(e))
        
    time.sleep(1)
