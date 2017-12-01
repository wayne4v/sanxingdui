def c():
    # yield 1
    for i in range(4):
        yield i ** 2

def d():
    x = 1
    while True:
        y = yield x
        print(y)
# print(type(c()))
#
# print(type(1))

# generator = c()
# for g in generator:
#     print(g)

geni = d()
geni.__next__()
geni.send(30)