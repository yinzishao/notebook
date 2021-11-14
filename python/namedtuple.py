import sys
from collections import namedtuple
from random import randint
from memory_profiler import profile

import tracemalloc

tracemalloc.start()

N = 10000


# @profile
def my_func():
    result = []

    for i in range(N):
        one = {}
        for j in range(0, 20):
            one[f"qs_incr_amount_field_{j}"] = randint(1, 100)
        result.append(one)
    return result


# @profile
def nt():
    fields = []
    for j in range(0, 20):
        fields.append(f"qs_incr_amount_field_{j}")
    Shape = namedtuple('Shape', fields)

    result = []
    for i in range(N):
        v = []
        for j in range(0, 20):
            v.append(randint(1, 100))
        result.append(Shape(*v))
    return result


# @profile
def main():
    """
    N = 10000
    42     53.7 MiB     36.1 MiB           1       result1 = my_func()
    43     53.7 MiB      0.0 MiB           1       print("dict: ", sys.getsizeof(result1))
    44     56.5 MiB      2.8 MiB           1       result = nt()
    45     56.5 MiB      0.0 MiB           1       print("nametuple: ", sys.getsizeof(result))

    :return:
    """
    result1 = my_func()
    print("dict: ", sys.getsizeof(result1))
    result = nt()
    print("nametuple: ", sys.getsizeof(result))
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics("lineno"):
        print(stat)


if __name__ == '__main__':
    main()
