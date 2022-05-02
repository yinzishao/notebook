


1.6 string

> 有说到底层结构、内存拷贝和[]byte的注意事项，但没有继续深入展开。


2.4 mutex

> 结构、自旋、starvation模式（饥饿）、 Woken状态（只管解锁、不用释放信号量）


2.5

> 为什么写锁定不会被饿死(readerWait、读切分两段、写操作将readerCount变成负值)
