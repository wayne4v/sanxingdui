import redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
while True:
    print(r.llen('tp'))
    task = r.brpop('tp', 0)
    print("get task: {}".format(task[1].decode('utf-8')))
    # time.sleep(2)