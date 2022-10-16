from Stock import redis, Itemss
import time

key = 'order_completed'
group = 'stock_group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists')


while True:
    try:
        results = redis.xreadgroup(group, key, {key:'>'}, None)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                item = Itemss.get(obj['item_id'])
                item.quantity = item.quantity * int(obj['quantity'])
                item.save()
    except Exception as e:
        print(str(e))
        time.sleep(1) 