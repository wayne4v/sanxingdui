from collections import namedtuple

# Task 所需要携带的属性
# Node = namedtuple("Node", ["url", "re", "callback"])
User = namedtuple('User', ['name', 'sex', 'age'])
user = User(name='kongxx', sex='male', age=21)
user = User._make(['kongxx', 'male', 21])

print(user)
# print(Node)