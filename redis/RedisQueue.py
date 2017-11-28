import redis

r = redis.Redis(host="localhost", port=6379, db=0, password="foobared")
print(r)
for i in range(1, 100):
    r.lpush('tp', i)