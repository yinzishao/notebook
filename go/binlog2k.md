异步执行run
主线程监听退出信号，进行handler的close（通过chan发送给binlog消费者后，进行各个kafka生产者的close()），然后执行保存binlog offset，最后关闭canal。

消费者OnRow,通过select去监听，每次来到这里*非阻塞*的得到chan的信号，没有信号，则执行default，执行下去。
消费者每次消费完，通过kafka生产者发送到队列，然后更新指标的数目，并且通过StoreUint32原子性增加binlog offset的位置。

问题：
所以如果没有发信号给消费者OnRow，直接close掉生产者会怎么样？会报错，因为是协程，消费者拿到了数据，但是主进程执行了kafka的关闭，导致协程执行出错？
那消费者OnRow后续在close过程中，在writer的close的阶段，canal.close之前，会再次被触发？select 还会收到退出信号吗？应该不行，那么还是会处理数据？

那又引出另一个问题，为什么需要对binlog进行Pos的StoreUint32，原因就是binlog消费和保存是分开协程处理的？还是onRow是多个协程么？但是我只看到一个
那如果是为了保存的原子性，那拿的时候需要原子性拿？不然以上的分析，还是会触发消费者事件，继续消费的。因为savePos在close writer之前，所以消费者不能完整执行，所以没有原子性拿也不会有原子性问题，但会报错。

main线程go func了run的携程，但是并没有正常销毁？

