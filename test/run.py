# class t:
#     def __init__(self, root, *, path):
#         self.root = "root"
#         self.star = "*"
#         self.path = "path"
#     def __repr__(self):
#         print("{}, {}".format(self.root, self.star))

# print(t("a", "c", path="b"))

def foo(pos, *, forcenamed="1"):
    print(pos, forcenamed)

foo(10)

print(__name__)

# import logging
# logging.warning('Watch out!')  # will print a message to the console
# logging.info('I told you so')  # will not print anything

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
#
# import timeit
#
# t1 = timeit.time()
# t2 = timeit.time() - t1
# print(t2)

# import collections from n

from collections import namedtuple

# class Employee():
#     # name:
#     def __int__(self, name, id):
#         self.name = name
#         self.id = id
#     pass
#     def __repr__(self):
#         print("{}, {}".format(self.name, self.id))
#
# Employee = namedtuple('Employee', ['name', 'id'])
# # print(Employee('1','2'))
# print(Employee.id)

User = namedtuple("User", "name, gender, height")

user = User(name="y", gender='F', height=18)
print(user.name)
print(user.gender)

# https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=sa_menu_top_books_l1?ie=UTF8&node=658390051

# https://www.amazon.cn/s/ref=lp_658390051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051&bbn=658391051&ie=UTF8&qid=1511412704&rnid=658391051
# https://www.amazon.cn/s/ref=lp_658390051_nr_n_1?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658393051&bbn=658391051&ie=UTF8&qid=1511412704&rnid=658391051