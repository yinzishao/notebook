from django.utils.synch import RWLock
import threading

lock = RWLock()


def r():
    """读进的时候只会被写给等待"""
    with lock.reader():
        import time
        for i in range(0, 3):
            print(i)
            time.sleep(i * 4)


def w():
    with lock.writer():
        import time
        for i in range(0, 3):
            print(i)
            time.sleep(i * 4)


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        r()
        print("退出线程：" + self.name)


class myWThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        w()
        print("退出线程：" + self.name)


# 创建新线程
# 创建写锁，线程二等待
thread1 = myWThread(1, "Thread-1", 1)
# 创建读锁，线程二不需要等待
# thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
import time

time.sleep(3)
thread2.start()
thread1.join()
thread2.join()
print("退出主线程")
