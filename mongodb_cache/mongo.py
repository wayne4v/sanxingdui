from pymongo import MongoClient
import hashlib
import requests
import random

client = MongoClient()
db = client["Library"]
collection = db["book_html"]

for _ in range(20000):
    ri = random.randint(1, 1000)
    url = "http://www."+str(ri)+".com"
    text = "content"#rep.text

    md5 = hashlib.md5(url.encode('utf-8')).hexdigest()

    result = collection.find_one({"id": md5})
    if result:
        print(md5)
        print("{} is exists!!!".format(url))
        # print(result)
    else:
        book = {}
        book['title']='Mongodb Guide123'
        book['id'] = md5
        book['content'] = "test mongodb123"
        collection.insert_one(book)
        print("insert success!!")
        # print("nonono")
