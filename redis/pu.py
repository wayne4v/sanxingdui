import redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=0, password="foobared")
r = redis.StrictRedis(connection_pool=pool)
import ast

# task = r.brpop('tp', 0)
# d = ast.literal_eval(task[1].decode('utf-8'))
# print(d["a"])
t = 0
a = set()
while True:
    task = r.brpop('tp', 0)
    t += 1
    a.add(task[1].decode('utf-8'))
    if t % 10 == 0:
        print(a)
        a = set()
    # task = r.brpop('tp', 0)
    # print(task[1].decode('utf-8'))
'''
while True:
    print(r.llen('tp'))
    task = r.brpop('tp', 0)
    print("get task: {}".format(task[1].decode('utf-8')))
    # time.sleep(2)
'''