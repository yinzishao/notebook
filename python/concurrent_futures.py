"""
https://docs.python.org/zh-cn/3/library/concurrent.futures.html

"""
from queue import Queue

import concurrent.futures
import urllib.request

# Object that signals shutdown
_sentinel = object()

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']


# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    return url


def _worker(queue):
    while True:
        msg = queue.get()
        if msg is _sentinel:
            break
        print(f'get msg: {msg}')


def run():
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        queue = Queue(maxsize=1)
        for _ in range(5):
            executor.submit(_worker, queue)

        for i in range(199):
            queue.put(i)
        # !!如果不传结束信号进去程序无法结束!!
        for _ in range(5):
            queue.put(_sentinel)


run()
