import redis

r = redis.Redis(host="localhost", port=6379, db=0)
print(r)
for i in range(1, 10):
    r.lpush('tp', {"a":1})