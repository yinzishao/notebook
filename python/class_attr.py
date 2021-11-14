class Abc():
    _f = []

    def run(self):
        self._f.append(1)

    def clear(self):
        self._f = []


a = Abc()
a.run()
print(a._f)
# [1]
b = Abc()
print(b._f)
# [1]

b.run()
print(a._f)
# [1, 1]
print(b._f)
# [1, 1]

# !!!: 实例方法置空，也无法置空类属性值
b.clear()
c = Abc()
# !!!: [1, 1]
print(c._f)

print('----------')


class Abc():
    _f = None

    def __init__(self):
        self._f = []

    def run(self):
        self._f.append(1)

    def clear(self):
        self._f = []


a = Abc()
a.run()
print(a._f)
# [1]
b = Abc()
print(b._f)
# []

# 实例的__init__属性，不会赋值给类属性
print('Abc._f:', Abc._f)
# Abc._f: None

b.run()
print(a._f)
# [1]
print(b._f)
# [1]

# 实例的__init__属性，不会赋值给类属性
print('Abc._f:', Abc._f)
# Abc._f: None

b.clear()
c = Abc()
print(c._f)
# []
