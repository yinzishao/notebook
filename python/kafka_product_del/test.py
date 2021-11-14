#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kafka
import logging

from utils.kafka_v import Producer

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s] : %(message)s' #其中name为getlogger指定的名字

logging.basicConfig(level=logging.DEBUG, format=standard_format)
from utils.kafka_v import get_producer


def c():
    # 不用单例，会执行__del__
    producer = Producer(conf)
    print(producer)
    for i in range(3):
        producer.send('partopic', str(i).encode())


def b():
    # 用了单例，最后才是执行__del__，但是atexit原生已经强制退出了，导致没有发送数据
    producer = get_producer('t', conf)
    print(producer)
    for i in range(3):
        producer.send('partopic', str(i).encode())
    # producer.close()


def a():
    # 正常发送，没有主动调用close是不会发送的，是强制退出
    producer = kafka.KafkaProducer(**conf)
    for i in range(3):
        producer.send('partopic', str(i).encode())
    logging.info('手动触发close----------')
    producer.close()


if __name__ == "__main__":
    conf = dict(
        bootstrap_servers=['127.0.0.1:9092']
    )
    # a()
    # b()
    # c()

    # 这样子也不能执行__del__,main函数的引用释放会比atexit慢
    producer = Producer(conf)
    print(producer)
    for i in range(3):
        producer.send('partopic', str(i).encode())

