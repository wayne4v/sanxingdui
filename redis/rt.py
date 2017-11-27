# import time
# import redis
# pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
# r = redis.StrictRedis(connection_pool=pool)
# #'''
# while True:
#     print(r.llen('tp'))
#     task = r.brpop('tp', 0)
#     print("get task: {}".format(task[1].decode('utf-8')))
#     # time.sleep(2)

# flag = True
# c = []
# while flag:
#     for i in range(100):
#         print(i)
#         c.append(i)
#         if len(c) <=10:
#             flag = True
#         else:
#             flag = False

# print(r.smembers('tp'))
import redis
pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
r = redis.StrictRedis(connection_pool=pool)
p = r.pubsub()
p.subscribe('tp')
for item in p.listen():
    print(item)
    if item['type'] == 'message':
        data =item['data']
        r.set('s',32)
        print(data)
        if item['data']=='over':
            break
p.unsubscribe('tp')
print('取消订阅')


