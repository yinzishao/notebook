#!/usr/bin/env python
# -*- coding: utf-8 -*-


def fib(n):
    if n == 1 or n == 2:
        return 1
    return fib(n - 2) + fib(n - 1)


print(fib(5))


def fib(n):
    a, b = 0, 1
    while n > 0:
        yield b
        a, b = b, a + b
        n -= 1


print(list(fib(10)))
