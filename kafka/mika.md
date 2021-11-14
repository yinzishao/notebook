# ConsumerConf
pkg/mika/conf.go:60

通过继承sarama.Config，来沿用原生的配置，并添加了自定义的配置，例如定时定量触发下游的配置。

ConsumerConf.New()
pkg/mika/consumer.go:21

返回的是一个Consumer类，该类暴露了两个方法，
Consume(Writer)： 消费者消费消息方法，接受一个参数是writer的类，目的是为了统一writer类。

writer类，继承io.Writer和Fluser, 统一提供write和flush方法。好处是能让接受到的控制器，控制相关的同步逻辑。自身writer也可以按需实现自己的write，是否需要缓冲区

Close： 消费者类


# groupConsumer(Consumer)

也就是ConsumerConf.New()返回的类

包括：消费者的配置信息，原生客户端得到的消费组客户端，日志，外部提供消费writer，取消消费方法，存储消息的chan，wg信号，游标管理。

并在Consume控制相关的逻辑，屏蔽了原生消费客户端的消费逻辑，通过Setup，来进行开始协程的监听消息队列的(doHandle)。Cleanup进行退出。ConsumeClaim获取到消息发送到消息对比。

doHandle 完成定时定量的逻辑，调用writer的write和flush
