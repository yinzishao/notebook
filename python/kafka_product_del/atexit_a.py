
class B:

    def __del__(self):
        # del 比atexit要慢！
        print('del-----bbb')

    def goodbye(self, name, adjective):
        print('Goodbye, %s, it was %s to meet you.' % (name, adjective))

def t():
    b = B()
    b.goodbye('b', 'gg')