import logging
from time import time

import requests

logging.basicConfig(level=logging.DEBUG, format="%(message)s")


def test_post():
    # TIME_WAIT 1 = > 1005 过了60秒后 TIME_WAIT 5
    for i in range(1000):
        a = requests.post("http://0.0.0.0:8091/account/session")
        print(a.request.headers)


def test_get():
    """
tcp        0      0 127.0.0.1:35068         127.0.0.1:8080          TIME_WAIT
tcp        0      0 127.0.0.1:8091          127.0.0.1:58120         TIME_WAIT
tcp        0      0 127.0.0.1:35876         127.0.0.1:8080          TIME_WAIT
tcp        0      0 127.0.0.1:8091          127.0.0.1:58496         TIME_WAIT

每个目的都从TIME_WAIT 1 = > 1005 过了60秒后 TIME_WAIT 5

两边的顺序不一样
    """
    for i in range(1000):
        # TIME_WAIT 1 = > 1005 过了60秒后 TIME_WAIT 5
        # python runserver
        a = requests.get("http://0.0.0.0:8091/account/session")
        # go beego
        a = requests.get("http://0.0.0.0:8080/account/session")


def test_session_get():
    """
    python runserver 即使用到session也有有问题
    beego 没有timewait相关问题

    对比上面的netstat，分析一下服务器主动time_wait的问题？
    :return:
    """
    # TIME_WAIT 1 = > 1005 过了60秒后 TIME_WAIT 5
    session = requests.Session()

    for i in range(1000):
        # TIME_WAIT 1 = > 1005 过了60秒后 TIME_WAIT 5
        # python runserver Resetting dropped connection: 0.0.0.0
        # https://stackoverflow.com/questions/28867840/why-do-i-constantly-see-resetting-dropped-connection-when-uploading-data-to-my/37678627
        # 1. Server doesn't support Keep-Alive.
        # 2. There's no data transfer in established connections for a while, so server drops connections.
        # https://stackoverflow.com/questions/25239650/python-requests-speed-up-using-keep-alive
        a = session.get("http://0.0.0.0:8091/account/session")
        # runserver用的是，可能没有实现keep-live的支持 socketserver.TCPServer
        # beego 没有timewait相关问题
        # a = session.get("http://0.0.0.0:8080")
        # a = session.get("http://baidu.com")


def test_session_get_with():
    """
    python runserver 即使用到session也有有问题
    beego 没有timewait相关问题

    对比上面的netstat，分析一下服务器主动time_wait的问题？
    :return:
    """
    for i in range(1000):
        # Session没有用，每次都建立连接需要全局单例
        with requests.Session() as s:
            a = s.get("http://0.0.0.0:8080")


# test_post()
# test_get()
# test_session_get()
test_session_get_with()

"""

session.get python runserver
出现： Resetting dropped connection: 0.0.0.0

tcp        0      0 127.0.0.1:8091          127.0.0.1:44066         TIME_WAIT

这个的意思是服务端主动关闭链接，应该是不支持keep-live。然后客户端再次请求，需要重新建立一个新端口和连接。


而在for get beego中
tcp        0      0 127.0.0.1:35876         127.0.0.1:8080          TIME_WAIT

是client主动关闭连接，而用session，则没有time_wait

结论： python runserver无法很好测试相关长连接，可能自身不支持或者线程池相关问题。待研究。
"""
