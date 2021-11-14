
## gevent

Gevent是一个基于Greenlet实现的网络库(greenlet+前期libevent，后期libev)，通过greenlet实现协程。基本思想是一个greenlet就认为是一个协程，当一个greenlet遇到IO操作的时候，比如访问网络，就会**自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行**。由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO操作。


```python

import gevent

def test(n):
    for i in range(n):
        print(gevent.getcurrent(), i)
        # gevent.sleep(1)

if __name__ == '__main__':
    g1 = gevent.spawn(test, 3)
    g2 = gevent.spawn(test, 3)
    g3 = gevent.spawn(test, 3)

    g1.join()
    g2.join()
    g3.join()

```

可以看到3个greenlet是依次运行而不是交替运行。要让greenlet交替运行，**可以通过gevent.sleep()交出控制权**

当然在实际的代码里，我们不会用gevent.sleep()去切换协程，而是**在执行到IO操作时gevent会自动完成**，所以gevent需要将Python**自带的一些标准库的运行方式由阻塞式调用变为协作式运行**。这一过程在启动时通过monkey patch完成

> monkey patch的作用

```python
from gevent import monkey; monkey.patch_all()
```

- [Python协程详解](https://juejin.im/post/5d888151f265da03dd3db0f5)


---
# Gevent源码

- [一起读 Gevent 源码](https://segmentfault.com/a/1190000000613814)

我们知道 Gevent 是基于 Greenlet 实现的，greenlet 有的时候也被叫做**微线程或者协程**。其实 Greenlet 本身非常简单，其自身实现的功能也非常直接。区别于常规的编程思路——顺序执行、调用进栈、返回出栈—— **Greenlet 提供了一种在不同的调用栈之间自由跳跃的功能**。

> Greenlet 提供了一种在不同的调用栈之间自由跳跃的功能。事件循环进行greenlet的上下文切换

```python
from greenlet import greenlet

def test1():
    print 12
    gr2.switch()
    print 34

def test2():
    print 56
    gr1.switch()
    print 78

gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()
```

这里，每一个 greenlet 就是一个**调用栈**——您可以把他**想象成一个线程**，只不过真正的线程可以**并行执行**，而**同一时刻只能有一个** greenlet 在执行（同一线程里）。正如例子中最后三句话，我们创建了 gr1 和 gr2 两个不同的调用栈空间，入口函数分别是 test1 和 test2；这最后一句 gr1.switch() 得多解释一点。

因为除了 gr1 和 gr2，我们还有一个栈空间，也就是所有 Python 程序都得有的默认的栈空间——我们暂且称之为 main，而这一句 gr1.switch() 恰恰实现了从 main 到 gr1 的跳跃，也就是从**当前的栈跳到指定的栈**。这时，就犹如常规调用 test1() 一样，gr1.switch() 的调用暂时不会返回结果，程序会跳转到 test1 继续执行；只不过区别于普通函数调用时 test1() 会向当前栈压栈，而 gr1.switch() 则会将当前栈存档，替换成 gr1 的栈。

对于这种栈的切换，我们有时也称之为**执行权的转移**，或者说 main 交出了执行权，同时 gr1 获得了执行权。Greenlet 在底层是用汇编实现的这样的切换：把当前的栈（main）相关的寄存器啊什么的保存到内存里，然后把原本保存在内存里的 gr1 的相关信息恢复到寄存器里。这种操作速度非常快，**比操作系统对多进程调度的上下文切换还要快**。

这个时候 test1 执行到头了，gr1 的栈里面空了。Greenlet 设计了 parent greenlet 的概念，就是说，当一个 greenlet 的入口函数执行完之后，会自动切换回其 parent。默认情况下，greenlet 的 parent 就是创建该 greenlet 时所在的那个栈，前面的例子中，gr1 和 gr2 都是在 main 里被创建的，所以他们俩的 parent 都是 main。所以当 gr1 结束的时候，会回到 main 的最后一句，接着 main 结束了，所以整个程序也就结束了——78 从来没有被执行到过。另外，greenlet 的 parent 也可以手工设置。

## sleep

```python
def sleep(seconds=0):
    hub = get_hub()
    loop = hub.loop
    hub.wait(loop.timer(seconds))
```

这里我把一些当前用不着的代码做了一些清理，只留下了三句关键的代码，其中就有 Gevent 的两个关键的部件——**hub 和 loop**。loop 是 Gevent 的核心部件，也就是**主循环核心**，默认是用 Cython 写的 libev 的包装（所以性能杠杠滴），稍后会在详细提到它。hub 则是一个 greenlet，里面跑着 loop。

hub 是一个单例

```python
class Hub(greenlet):
    loop_class = config('gevent.core.loop', 'GEVENT_LOOP')

    def __init__(self):
        greenlet.__init__(self)
        loop_class = _import(self.loop_class)
        self.loop = loop_class()
```

同样这是一段精简了的代码，反映了一个 hub 的关键属性——loop。loop 实例随着 hub 实例的创建而创建，默认的 loop 就是 gevent/core.ppyx 里的 class loop，也可以通过环境变量 GEVENT_LOOP 来自定义。

值得注意的是，截止到 hub = get_hub() 和 loop = hub.loop，我们都只是创建了 hub 和 loop，并没有真正开始跑我们的主循环。稍安勿躁，第三句就要开始了。

loop 有一堆接口，对应着底层 libev 的各个功能，详见此处。我们这里用到的是 timer(seconds)，该函数返回的是一个 watcher 对象，对应着底层 libev 的 watcher 概念。我们大概能猜到，这个 watcher 对象会在几秒钟之后做一些什么事情，但是具体怎么做，让我们一起看看 hub.wait() 的实现吧。
```python
def wait(self, watcher):
    waiter = Waiter()
    watcher.start(waiter.switch)
    waiter.get()
```

代码也不长，不过能看到 watcher 的接口 watcher.start(method)，也就是说，当给定的几秒钟过了之后，会调用这里给的函数，也就是 waiter.switch。

> 回头看一下这个过程，其实也很简单的：当我们需要等待一个事件发生时——比如需要等待 1 秒钟的计时器事件，我们就**把当前的执行栈跟这个事件做一个绑定**（watcher.start(waiter.switch)），然后把执行权交给 hub；hub 则会**在事件发生后，根据注册的记录尽快回到原来的断点继续执行**。


hub 一旦拿到执行权，就可以做很多事情了，比如切换到别的 greenlet 去执行一些其他的任务，直到这些 greenlet 又主动把执行权交回给 hub。宏观的来看，就是这样的：一个 hub，好多个其他的任务 greenlet（其中没准就包括 main），**hub 负责总调度，去依次调用各个任务 greenlet**；任务 greenlet 则在**执行至下一次断点时，主动切换回 hub**。这样一来，许多个任务 greenlet 就可以看似并行地同步运行了，这种任务调度方式叫做**协作式的任务调度**（cooperative scheduling）。

> 个人理解： 也就是通过单例get_hub获取到hub 和 loop。loop 是 Gevent 的核心部件，也就是主循环核心。hub 则是一个 greenlet，里面跑着 loop。然后hub是总的，负责切换到其他的greenlet去执行任务，直到这些 greenlet 又主动把执行权交回给 hub。通过loop进行注册。wait进行交换控制权。而greenlet是自己实现的类似微线程和协程。

TODO: 太晦涩了，后续收集多些文章一起细读

---

- [TODO:去 async/await 之路(对比gevent)](https://zhuanlan.zhihu.com/p/45996168): TODO希望能更深入各自的源码原理进行对比！
- [Gevent高并发网络库精解:一些数据通信的数据结构](https://www.jianshu.com/p/ccf3bd34340f)
- [TODO: Python 开源异步并发框架的未来](https://segmentfault.com/a/1190000000471602)
