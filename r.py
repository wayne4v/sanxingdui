import redis

from hashlib import md5
r = redis.StrictRedis(host='127.0.0.1',port=6379,db=0, password="foobared")
print(r)


str_input = "helo"
m5 = md5()
m5.update(str_input.encode('utf-8'))
str_input = m5.hexdigest()
print(str_input)


print(r.getbit('name','2'))
