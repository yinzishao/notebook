# kafka源码

标签（空格分隔）： kafka

---
## 可重入
可重入（reentrant）函数可以由多于一个任务并发使用，而不必担心数据错误。相反， 不可重入（non-reentrant）函数不能由超过一个任务所共享，除非能确保函数的互斥 （或者使用信号量，或者在代码的关键部分禁用中断）。可重入函数可以在任意时刻被中断， 稍后再继续运行，不会丢失数据。可重入函数要么使用本地变量，要么在使用全局变量时 保护自己的数据。

- https://www.ibm.com/developerworks/cn/linux/l-reent.html

## event
线程之间的通讯事件
An event manages a flag that can be set to true with the set() method and reset to false with the clear() method. The wait() method blocks until the flag is true. The flag is initially false.

set() 置为true，clear重置为false，wait，等待多少秒直到为true

- https://docs.python.org/3/library/threading.html#event-objects

## threading.Timer
多少秒后触发某个事情，而不是**循环定时**触发的。思路是通过另起一个线程，
然后通过设定一个Event，然后通过event.wait(sec)来进行等待时间。也可以通过自己调用cancel，自己更新event提前结束。
https://juejin.im/post/5c8918f5f265da2dd6393633

## kafka.util.ReentrantTimer

工作原理：自己写了一个定时触发器。主要是通过active.wait(self.t)进行触发。因为event一直都是False，通过阻塞来进行等待，等待时间后，触发fn。

```python
    def _timer(self, active):
        while not (active.wait(self.t) or active.is_set()):
            self.fn(*self.args, **self.kwargs)
```
如何停止：stop函数立刻将信号设为true，~~立刻触发fn执行~~触发wati，得到true使之跳出循环，没有触发fn执行。然后通过`self.thread.join(self.t + 1)`等待该线程执行完毕？执行执行没完成，也不等待了，起码已经执行一次了，将fn设为None，避免再次执行。

疑问：stop函数会设一个`self.timer = None`不是该类的属性，作用是啥？TODO: 应该是供外部查看是否结束。

## threading.Thread.join
同步等待该线程完成，如果没设时间，则阻塞到线程销毁，如果指定timeout时间，则会等待一定时间后结束，可以通过is_alive()判断

As join() always returns None, you must call is_alive() after join() to decide whether a timeout happened – if the thread is still alive, the join() call timed out.

- https://docs.python.org/3/library/threading.html#threading.Thread.join
