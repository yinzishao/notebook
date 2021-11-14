import os
from atexit import register

from notebook.python.kafka_product_del.atexit_a import t


def main():
    print('main')
    # t 方法里面的B实例会比atexit先执行del
    t()


class A:

    def __del__(self):
        # 但是这里的del 比atexit要慢！
        # 猜测是因为这里是main函数调用的。
        print('del-----')

    def goodbye(self, name, adjective):
        print('Goodbye, %s, it was %s to meet you.' % (name, adjective))


# register(goodbye, 'Donny', 'nice')
# or:
# register(goodbye, adjective='nice', name='Donny')
if __name__ == '__main__':
    a = A()
    register(a.goodbye, adjective='nice', name='Donny')
    main()
    exit(1)  # 程序退出了
    print("---")  # 无法执行到这里
