# kafka生产者的del问题

标签（空格分隔）： kafka

---
场景：单例模式的kafka自定义类，触发类中__del__，调用product.close()的时候，发现无法正常close()掉。

原因：
close(timeout=None) 默认调用的时候会阻塞掉，等待发送未完的请求。当timeout=0的时候则会强制退出，导致无法发出去，丟数据。

但是__del__调用也是close()，为什么不行呢？因为代码自己写的类__del__之前。kafka原生类已经调用了close(0)，导致强制退出了。那为什么kafka会比__del__快呢？

分析：
close(0)发现是在`kafka.producer.kafka.KafkaProducer._cleanup_factory`里面是第一被调用。发现_cleanup_factory是在`__init__`的时候通过`atexit.register(self._cleanup)`注册了, 退出的时候执行比__del__更早执行了！

这里有几个原因是：
1. 最重要的是单例模式里面保留的引用，导致无法释放__del__!正常是先执行__del__的。不管是方法单例，还是类的new单例，因为是类的属性，import就是引用了？
2. 还有就是，猜测main函数的引用释放会比atexit慢，其他正常引用（调用）后释放的__del__会比atexit快的。

思考：如何单例后进行销毁？

分析：单例目的就是为了避免重复的实例，所以不应该自行销毁。到程序结束的时候，引用没了，销毁就可以了？

思考：那如何优雅退出？

方案：参考原生，我也通过atexit.register(self.close)在kafka，init后注册自己的close，按照先进后出的原则，自身的close会先执行。不过要注意引用不能释放的问题，可以通过弱引用进行优化，不过既然都是单例，就不用了。

弱引用的原因是为了防止ref的计算增加。避免永不被回收。
> This only affects the KafkaProducer and is caused by the extra system reference caused by atexit.register(self.close). We should use a weakref proxy to allow gc to function normally on producer objects.

> 思考：也就是atexit.register(self._cleanup)也会异常引用+1，导致正常的gc无法进行内存的收回，甚至泄漏。这时候则需要通过weakref.proxy(self)进行弱引用。

参考链接：

- [atexit.register](https://docs.python.org/zh-cn/3/library/atexit.html)
- [weakref.proxy(self)](https://docs.python.org/zh-cn/3/library/weakref.html)
- [kafka-python更改弱引用的更改的提交](https://github.com/dpkp/kafka-python/pull/728/files)


