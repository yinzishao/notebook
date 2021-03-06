# RabbitMQ VS Kafka
> - [RabbitMQ 和 Kafka选哪个？](https://zhuanlan.zhihu.com/p/161224418)

**2、消息交换器**

RabbitMQ使用消息交换器来实现发布/订阅模式。发布者可以把消息发布到消息交换器上而不用知道这些消息都有哪些订阅者。

每一个订阅了交换器的消费者都会创建一个队列；然后消息交换器会把生产的消息放入队列以供消费者消费。消息交换器也可以基于各种路由规则为一些订阅者过滤消息。

**1、消息顺序**

换话句话说，只要我们是单个消费者，那么接收到的消息就是有序的。然而，一旦有多个消费者从同一个队列中读取消息，那么消息的处理顺序就没法保证了。

由于消费者读取消息之后可能会把消息放回（或者重传）到队列中（例如，处理失败的情况），这样就会导致消息的顺序无法保证。

一旦一个消息被重新放回队列，另一个消费者可以继续处理它，即使这个消费者已经处理到了放回消息之后的消息。因此，消费者组处理消息是无序的

**2、消息路由**

RabbitMQ可以基于定义的订阅者路由规则路由消息给一个消息交换器上的订阅者。一个主题交换器可以通过一个叫做routing\_key的特定头来路由消息。

或者，一个头部（headers）交换器可以基于任意的消息头来路由消息。这两种交换器都能够有效地让消费者设置他们感兴趣的消息类型，因此可以给解决方案架构师提供很好的灵活性。

另一方面，Kafka在处理消息之前是不允许消费者过滤一个主题中的消息。一个订阅的消费者在没有异常情况下会接受一个分区中的所有消息。

作为一个开发者，你可能使用Kafka流式作业（job），它会从主题中读取消息，然后过滤，最后再把过滤的消息推送到另一个消费者可以订阅的主题。但是，这需要更多的工作量和维护，并且还涉及到更多的移动操作。

**3、消息时序（timing）**

在测定发送到一个队列的消息时间方面，RabbitMQ提供了多种能力：

**1）消息存活时间（TTL）**

发送到RabbitMQ的每条消息都可以关联一个TTL属性。发布者可以直接设置TTL或者根据队列的策略来设置。

系统可以根据设置的TTL来限制消息的有效期。如果消费者在预期时间内没有处理该消息，那么这条消息会自动的从队列上被移除（并且会被移到死信交换器上，同时在这之后的消息都会这样处理）。

TTL对于那些有时效性的命令特别有用，因为一段时间内没有处理的话，这些命令就没有什么意义了。

**2）延迟/预定的消息**

RabbitMQ可以通过插件的方式来**支持延迟或者预定**的消息。当这个插件在消息交换器上启用的时候，生产者可以发送消息到RabbitMQ上，然后这个生产者可以延迟RabbitMQ路由这个消息到消费者队列的时间。

这个功能允许开发者调度将来（future）的命令，也就是在那之前不应该被处理的命令。例如，当生产者遇到限流规则时，我们可能会把这些特定的命令延迟到之后的一个时间执行。

Kafka没有提供这些功能。它在消息到达的时候就把它们写入分区中，这样消费者就可以立即获取到消息去处理。

Kafka也**没用为消息提供TTL的机制**，不过我们可以在**应用层实现**。

不过，我们必须要记住的一点是Kafka分区是一种追加模式的事务日志。所以，它是**不能处理消息时间**（或者分区中的位置）。

**4、消息留存（retention）**

当消费者成功消费消息之后，RabbitMQ就会把对应的消息**从存储中删除**。这种行为没法修改。它几乎是所有消息代理设计的必备部分。

相反，Kafka会给每个主题配置超时时间，只要没有达到超时时间的消息都会保留下来。在消息留存方面，Kafka仅仅把它当做消息日志来看待，并不关心消费者的消费状态。

消费者可以**不限次数的消费每条消息**，并且他们可以操作分区偏移来“及时”往返的处理这些消息。Kafka会周期的检查分区中消息的留存时间，一旦消息超过设定保留的时长，就会被删除。

Kafka的性能不依赖于存储大小。所以，理论上，它存储消息几乎不会影响性能（只要你的节点有足够多的空间保存这些分区）。

**5、容错处理**

RabbitMQ会给我们提供诸如交付重试和死信交换器（DLX）来处理消息处理故障。

DLX的主要思路是根据合适的配置信息**自动地把路由失败的消息发送到DLX**，并且在交换器上根据规则来进一步的处理，比如**异常重试，重试计数以及发送到“人为干预”的队列**。

查看下面篇文章，它在RabbitMQ处理重试上提供了额外的可能模式视角。

链接：[https://engineering.nanit.com/rabbitmq-retries-the-full-story-ca4cc6c5b493](https://link.zhihu.com/?target=https%3A//engineering.nanit.com/rabbitmq-retries-the-full-story-ca4cc6c5b493)

在RabbitMQ中我们需要记住最重要的事情是当一个消费者正在处理或者重试某个消息时（即使是在把它返回队列之前），其他消费者都可以并发的处理这个消息之后的其他消息。

当某个消费者在重试处理某条消息时，作为一个整体的消息处理逻辑不会被阻塞。所以，一个消费者可以同步地去重试处理一条消息，不管花费多长时间都不会影响整个系统的运行。

消费者1持续的在重试处理消息1，同时其他消费者可以继续处理其他消息

和RabbitMQ相反，Kafka没有提供这种开箱即用的机制。在Kafka中，需要我们自己**在应用层提供和实现消息重试机制**。

另外，我们需要注意的是当一个消费者正在同步地处理一个特定的消息时，那么同在这个分区上的其他消息是没法被处理的。

由于消费者不能改变消息的顺序，所以我们不能够拒绝和重试一个特定的消息以及提交一个在这个消息之后的消息。你只要记住，分区仅仅是一个追加模式的日志。

一个应用层解决方案可以把失败的消息提交到一个“重试主题”，并且从那个主题中处理重试；但是这样的话我们就会**丢失消息的顺序**。

我们可以在[http://Uber.com](https://link.zhihu.com/?target=http%3A//Uber.com)上找到Uber工程师实现的一个例子。如果消息处理的时延不是关注点，那么对错误有足够监控的Kafka方案可能就足够了。

如果消费者阻塞在重试一个消息上，那么底部分区的消息就不会被处理

**6、伸缩**

有多个基准测试，用于检查RabbitMQ和Kafka的性能。

尽管通用的基准测试对一些特定的情况会有限制，但是Kafka通常被认为比RabbitMQ有更优越的性能。

Kafka使用顺序磁盘I / O来提高性能。

从Kafka使用分区的架构上看，它在横向扩展上会优于RabbitMQ，当然RabbitMQ在纵向扩展上会有更多的优势。

Kafka的大规模部署通常每秒可以处理数十万条消息，甚至每秒百万级别的消息。

**7、消费者复杂度**

RabbitMQ使用的是智能代理和傻瓜式消费者模式。消费者注册到消费者队列，然后RabbitMQ把传进来的消息**推送给消费者**。RabbitMQ也有拉取（pull）API；不过，一般很少被使用。

RabbitMQ管理消息的分发以及队列上消息的移除（也可能转移到DLX）。消费者不需要考虑这块。

根据RabbitMQ结构的设计，当负载增加的时候，一个队列上的消费者组可以有效的从仅仅一个消费者扩展到多个消费者，并且不需要对系统做任何的改变。

## 总结

优先选择RabbitMQ的条件：

*   高级灵活的路由规则；
*   消息时序控制（控制消息**过期**或者消息**延迟**）；
*   高级的容错处理能力，在消费者更有可能处理消息不成功的情景中（瞬时或者持久）；
*   更简单的消费者实现。

优先选择Kafka的条件：

*   严格的消息顺序；
*   延长消息留存时间，包括过去消息重放的可能；
*   传统解决方案无法满足的高伸缩能力。

---
# 消息队列设计
> - [从0到1设计一个MQ消息队列](https://zhuanlan.zhihu.com/p/60288173) 、 [当设计消息队列时我们关心什么](https://developer.aliyun.com/article/73381)

## **消息队列整体设计思路**

主要是设计一个整体的消息被消费的数据流。

这里会涉及到：消息生产Producer、Broker(消息服务端)、消息消费者Consumer。

1.Producer(消息生产者)：发送消息到Broker。

2.Broker(服务端)：Broker这个概念主要来自于Apache的ActiveMQ，特指消息队列的服务端。

主要功能就是：把消息从发送端传送到接收端，这里会涉及到消息的存储、消息通讯机制等。

3.Consumer(消息消费者)：从消息队列接收消息，consumer回复消费确认。

## **Broker(消息队列服务端)设计重点**

1）消息的转储：在更合适的时间点投递，或者通过一系列手段辅助消息最终能送达消费机。

2）规范一种范式和通用的模式，以满足解耦、最终一致性、错峰等需求。

3）其实简单理解就是一个消息转发器，把一次RPC做成两次RPC，发送者把消息投递到broker，broker再将消息转发一手到接收端。

总结起来就是两次RPC加一次转储，如果要做消费确认，则是三次RPC。

**为了实现上述消息队列的基础功能：**

1）消息的传输

2）存储

3）消费

**就需要涉及到如下三个方面的设计：**

1）通信协议

2）存储选择

3）消费关系维护

## **通讯协议**

消息Message:既是信息的载体，消息发送者需要知道如何构造消息，消息接收者需要知道如何解析消息，它们需要按照一种统一的格式描述消息，这种统一的格式称之为消息协议。

传统的通信协议标准有XMPP和AMQP协议等，现在更多的消息队列从性能的角度出发使用自己设计实现的通信协议。

## **JMS和AMQP比较**

JMS: 只允许基于JAVA实现的消息平台的之间进行通信

AMQP: AMQP允许多种技术同时进行协议通信

3.Kafka的通信协议

Kafka的Producer、Broker和Consumer之间采用的是一套自行设计的基于TCP层的协议。Kafka的这套协议完全是为了Kafka自身的业务需求而定制的。

## **存储选型**

对于分布式系统，存储的选择有以下几种

1.内存

2.本地文件系统

3.分布式文件系统

4.nosql

5.DB

从速度上内存显然是最快的，对于允许消息丢失，消息堆积能力要求不高的场景(例如日志)，内存会是比较好的选择。

DB则是**最简单的实现可靠存储的方案**，很适合用在可靠性要求很高，最终一致性的场景(例如交易消息)，对于不需要100%保证数据完整性的场景，要求性能和消息堆积的场景，hbase也是一个很好的选择。

理论上，从速度来看，文件系统>分布式KV（持久化）>分布式文件系统>数据库，而可靠性却截然相反。

还是要从支持的业务场景出发作出最合理的选择，如果你们的消息队列是用来支持支付/交易等对可靠性要求非常高，但对**性能和量的要求没有这么高**，而且没有时间精力专门做文件存储系统的研究，DB是最好的选择。

对于不需要100%保证**数据完整性**的场景，要求**性能和消息堆积**的场景，hbase也是一个很好的选择，典型的比如 kafka的消息落地可以使用hadoop。

## **消费关系处理**

现在我们的消息队列初步具备了转储消息的能力。

下面一个重要的事情就是解析发送接收关系，进行正确的消息投递了。

市面上的消息队列定义了一堆让人晕头转向的名词，如JMS 规范中的Topic/Queue，Kafka里面的Topic/Partition/ConsumerGroup，RabbitMQ里面的Exchange等等。

抛开现象看本质，无外乎是单播与广播的区别。

所谓单播，就是点到点；而广播，是一点对多点。

为了实现广播功能，我们必须要维护消费关系，通常消息队列本身不维护消费订阅关系，可以**利用zookeeper等成熟的系统维护消费关系**，在消费关系发生变化时**下发通知**。

## 消息队列高级特性实现

*   消息的顺序
*   投递可靠性保证
*   消息持久化
*   支持不同消息模型
*   多实例集群功能
*   事务特性等

除了上述的消息队列基本功能以外，消息队列在某些特殊的场景还需要支持事务，消息重试等功能。

### 1.消息有序支持

消息队列中消息的有序性直接依赖与存储的选择，并且和存储的分布式部署以及消费端的并发情况密切相关。

消息的有序可以使用存储的顺序性来支持，比如Kafka，在一个partition上是一段连续的存储，可以保证这一段连续的消息有序。

![](http://images2015.cnblogs.com/blog/524341/201704/524341-20170406105652472-6145378.png)

使用Redis可以实现一个简单的消息队列，保证生产端和消费端都是单线程的生产和消费，因为底层数据机构有序，就可以实现消息的有序。

### 2.投递可靠性支持

消息投递的可靠性涉及到分布式数据一致性的话题，比如如何保证不丢数据，消息的幂等此类的问题。

RabbitMQ的设计是，当从队列当中取出一个消息的时候，RabbitMQ需要应用显式地回馈说已经获取到了该消息。如果一段时间内不回馈，RabbitMQ会将该消息重新分配给另外一个绑定在该队列上的消费者。另一种情况是消费者断开连接，但是获取到的消息没有回馈，则RabbitMQ同样重新分配。

投递的可靠性需要消费端和生产端一些约定的规则进行约束，保证投递的可靠性，肯定会影响性能，需要一些额外的工作来记录消息的状态等。

### 3.消息确认机制

消息确认机制可以给消息一致性提供支持，包括发送端的确认和消费端的确认，AMQP 协议本身使用的是事务机制进行消息确认，但是事务机制性能较差，并且容易发生阻塞。

Kafka应用的是ACK机制，RabbitMQ也设计了单独的消息确认机制。

### 4.消息发送和投递方式

消息队列支持不同的投递语义，以Kafka为例，提供三种不同的语义：

*   At most once 消息可能会丢，但绝不会重复传输
*   At least one 消息绝不会丢，但可能会重复传输
*   Exactly once 每条消息肯定会被传输一次且仅传输一次

类似的有阿里巴巴的MQ中间件，发送普通消息有三种实现方式：可靠同步发送、可靠异步发送、单向(Oneway)发送。

---
# 参考链接

- [消息中间件选型分析：从Kafka与RabbitMQ的对比看全局](https://juejin.cn/post/6844903590486605832)
- [消息队列设计精要](https://tech.meituan.com/2016/07/01/mq-design.html)
- [从0到1设计一个MQ消息队列](https://zhuanlan.zhihu.com/p/60288173)
- [当设计消息队列时我们关心什么](https://developer.aliyun.com/article/73381)
