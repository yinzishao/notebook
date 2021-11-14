def check(func, args, exc):
    res = func(*args)
    print(res)
    assert res == exc
