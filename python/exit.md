## signal

如何捕获信号
```python
import sys
import signal
def sigterm_handler(catch_signal, frame):
    _ = catch_signal, frame
    print("脚本被timeout杀掉, 脚本参数是: ")
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)
```

---
## exit

os._exit()会直接将python程序终止，之后的所有代码都不会继续执行。

sys.exit()会引发一个异常：SystemExit，如果这个异常没有被捕获，那么python解释器将会退出。如果有捕获此异常的代码，那么这些代码还是会执行。捕获这个异常可以做一些额外的清理工作。0为正常退出，其他数值（1-127）为不正常，可抛异常事件供捕获。

一般来说os._exit() 用于在线程中退出, sys.exit() 用于在主线程中退出。

意思就是参数为数字的时候，和 shell 退出码意义是一样的，sys.exit(2)和sys.exit(1)只是为了区分结束原因


```
0 ：成功结束
1 ：通用错误　　
2 ：误用Shell命令
```

---
## timeout
timeout 命令的退出码：

正常情况timeout exit with status 124，并且send the TERM signal upon timeout。
如果程序捕获信号后，修改exit的status。可以通过--preserve-status 来进行更改。

`timeout --preserve-status 10 python manage.py sync_es --type=slogan`


- https://www.cnblogs.com/everest33Tong/p/6670461.html
