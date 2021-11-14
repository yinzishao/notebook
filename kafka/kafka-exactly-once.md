# Kafka 交付语义

> - [Kafka-交付语义--机制详解](https://zhuanlan.zhihu.com/p/74212257): 浅尝辄止

## 至少一次（at least once）&使用场景（Kafka 默认实现方式）
至少一次是指，消息肯定会被处理，但是存在被处理多次的可能。这个在实现精准一次处理之前的场景，并且在Kafka 0.11.0.0 版本之前经常使用的就是这种模式，但是同一条消息被消费多次（这里的消费指的是成功拉取到消息并且返回，而不是说业务上对这个消息已经成功使用），**因为网络抖动等原因可能会导致没有收到对应的响应而重复发送导致消息的多次消费或上传**。Kafka 最起码的保证就是至少一次，因为ISR机制，Kafka消息一旦提交成功（产生副本之后），这条消息近乎可以认为是不可能丢失的，所以至少一次被消费。

## 精准一次（exactly once）&使用场景（Kafka 支持机制）
精确一次指的是消息被处理且只会被处理一次。在0.11.0.0 之后支持事务和幂等性之后，使用较广的就变成精确一次了。

## 幂等性producer（Idempotent producer）

首先幂等性的概念：若一个操作执行n次（n>1）与执行一次的结果是相同的，那么这个操作就是幂等操作。在producer 端，当出现发送消息无响应或者响应超时之后，不管消息成功没，都会有一个重试策略，这就导致了消息的重复提交问题。

那如何实现幂等性呢，Kafka提供了一个enable.idempotent参数，设置为true时，就开启幂等了。

幂等的实现方式是给所提交的消息**都赋予一个序列号用于消息去重**（TCP 的方式），**但是和TCP 实现不同的是，这个序列号不会舍弃，始终随消息持久化保存，可以简单的理解为消息的一部分**。

这么做的目的是 防止leader副本挂掉之后，没法儿进行去重操作。并且**强制要求用户显指定一个producer id**（严格单调递增的），这样一来，一个（producer id，分区号）都有一个对应的序列号值，这就为去重操作提供了便利，当发送消息的序列化小于或者等于broker端保存的序列号时，broker就会拒绝这条消息。

当实现上述的Idempotent producer 就保证了消息可以重试n次直到提交成功，并且提交多次也仅会成功保存一次，进而从producer端保证了，消息只会被成功提交一次。

---
# Kafka的Exactly once语义与事务机制
> - [Kafka的Exactly-once语义与事务机制](https://www.cnblogs.com/luxiaoxun/p/13048474.html)

## 消息系统语义概述
在一个分布式发布订阅消息系统中，组成系统的计算机总会由于各自的故障而不能工作。在Kafka中，一个单独的broker，可能会在生产者发送消息到一个topic的时候宕机，或者出现网络故障，从而导致生产者发送消息失败。根据生产者如何处理这样的失败，产生了不同的语义：

- **至少一次语义**（At least once semantics）

    如果生产者收到了Kafka broker的确认（acknowledgement，ack），并且生产者的acks配置项设置为all（或-1），这就意味着消息已经被精确一次写入Kafka topic了。然而，如果生产者**接收ack超时或者收到了错误，它就会认为消息没有写入Kafka topic而尝试重新发送消息**。
    如果broker恰好在消息已经成功写入Kafka topic后，发送ack前，出了故障，生产者的重试机制就会导致这条消息被写入Kafka两次，从而导致同样的消息会被消费者消费不止一次。每个人都喜欢一个兴高采烈的给予者，但是这种方式会导致重复的工作和错误的结果。

- **至多一次语义**（At most once semantics）：如果生产者在ack超时或者返回错误的时候不重试发送消息，那么消息有可能最终并没有写入Kafka topic中，因此也就不会被消费者消费到。但是为了避免重复处理的可能性，我们接受有些消息可能被遗漏处理。

- **精确一次语义**（Exactly once semantics）： 即使生产者重试发送消息，也只会让消息被发送给消费者一次。

    精确一次语义是最令人满意的保证，但也是最难理解的。因为它**需要消息系统本身和生产消息的应用程序还有消费消息的应用程序一起合作**。比如，在成功消费一条消息后，你又把消费的offset重置到之前的某个offset位置，那么你将收到从那个offset到最新的offset之间的所有消息。这解释了为什么消息系统和客户端程序必须合作来保证精确一次语义。

## 幂等：partition内部的exactly-once顺序语义

幂等操作，是指可以执行多次，而不会产生与仅执行一次不同结果的操作，Producer的send操作现在是幂等的。在**任何导致producer重试**的情况下，相同的消息，如果被producer发送多次，也只会被写入Kafka一次。要打开此功能，并让所有partition获得exactly-once delivery、无数据丢失和in-order语义，需要修改broker的配置：enable.idempotence = true。

这个功能如何工作？它的工作方式类似于TCP：发送到Kafka的每批消息将包含一个序列号，该序列号用于重复数据的删除。与TCP不同，TCP只能在transient in-memory中提供保证。序列号将被持久化存储topic中，因此即使leader replica失败，接管的任何其他broker也将能感知到消息是否重复。

这种机制的开销相当低：它只是在每批消息中添加了几个额外字段:

- PID，在Producer初始化时分配，作为每个Producer会话的唯一标识；
- 序列号（sequence number），Producer发送的每条消息（更准确地说是每一个消息批次，即ProducerBatch）都会带有此序列号，从0开始单调递增。Broker根据它来判断写入的消息是否可接受。

> 任何导致producer**重试**的情况，如果是断电重启的情况下又会怎么样呢（消费一次消息，发送一次到下游。但是可能会在提交下游时成功或者失败时崩溃）？
> 问题的本质应该是如何保证准确一次消费并且能准确生产到下游，或者是说能让消费和生产实现端到端的一致性，在同一个kakfa链条也就是事务的作用。

## 事务：跨partition的原子性写操作

第二点，Kafka现在支持使用新事务API原子性的对跨partition进行写操作，该API允许producer**发送批量消息到多个partition**。该功能同样支持在同一个事务中提交消费者offsets，因此真正意义上实现了end-to-end的exactly-once delivery语义。

值得注意的是，某个Kafka topic partition内部的消息可能是事务完整提交后的消息，也可能是事务执行过程中的部分消息。

而从consumer的角度来看，有两种策略去读取事务写入的消息，通过"isolation.level"来进行配置：

- read_committed：可以同时读取事务执行过程中的部分写入数据和已经完整提交的事务写入数据；
- read_uncommitted：完全不等待事务提交，按照offsets order去读取消息，也就是兼容0.11.x版本前Kafka的语义；

我们必须通过配置consumer端的配置isolation.level，来正确使用事务API，通过使用 new Producer API并且对一些unique ID设置transaction.id（该配置属于producer端），该unique ID用于提供事务状态的连续性。


## Exactly-once 流处理

基于**幂等和原子性**，通过Streams API实现exactly-once流处理成为可能。如果要在流应用中实现相关语义，只需要配置 processing.guarantee=exactly_once，这会影响所有的流处理环境中的语义，包括将处理作业和由加工作业创建的所有物理状态同时写回到Kafka的操作。

这就是为什么Kafka Streams API提供的exactly-once保证是迄今为止任何流处理系统中的最强实现的原因。 它为以Kafka作为数据源的流处理应用程序提供端对端的exactly-once保证，Streams应用程序将任何Kafka的物化状态在最终环节写回到Kafka。 仅依靠外部数据系统实现物化状态的流处理系统仅支持对exactly-once的较弱保证。 即使他们使用Kafka作为流处理来源，在需要从故障中恢复的情况下，也只能rollback他们的Kafka消费者offset以重新消费并处理消息，而不能回滚关联状态，当更新不是幂等的时候会导致结果不正确。


## 小结

kafka 0.11.0.0版本引入了idempotent producer机制，在这个机制中同一消息可能被producer发送多次，但是在broker端只会写入一次，他为每一条消息编号去重，而且对kafka开销影响不大。

如何设置开启呢？ 需要设置producer端的新参数 enable.idempotent 为true。

而多分区的情况，我们需要保证原子性的写入多个分区，即写入到多个分区的消息要么全部成功，要么全部回滚。

这时候就需要使用事务，在producer端设置 transcational.id为一个指定字符串。

这样幂等producer只能保证单分区上无重复消息；事务可以保证多分区写入消息的完整性。

> 二阶段提交：本质是通过序列号/消息号，在重启的时候让双方保持一致。例如拿到消费消息后，获取到一个全局序号，然后重新判断一下下游的预提交阶段是在那个序号，进行提交/回滚。binlog/redo的提交。

这样producer端实现了exactly once，那么consumer端呢？

consumer端由于可能无法消费事务中所有消息，并且消息可能被删除，所以事务并不能解决consumer端exactly once的问题，我们可能还是需要自己处理这方面的逻辑。比如自己管理offset的提交，不要自动提交，也是可以实现exactly once的。
> ?： 错误。不要自动提交：exactly once不能解决?网上抄来抄去的辣鸡信息。

还有一个选择就是使用kafka自己的流处理引擎，也就是Kafka Streams，

设置processing.guarantee=exactly_once，就可以轻松实现exactly once了。

> rabbitmq无法保证准确一次性

> 这里的准确一次性是理解为kafka事务上的准确一次？是保证消费kafka，并生产到多个下游的partition这些是精确一次的，通过pid/任期和序列号解决。

> 而如果用到外部系统的，还是不能保证准确一次的？例如，如何保证生产到kafka是准确一次的？binlog的canal无法保证！如果是用户点击触发，当发送到生产者后保存，但客户端宕机，恢复重发。也是无法去重的？因为无法保证重启后的程序的序列号是一样的？当上下游都是kafka，是一个大整体事务的时候，才能识别重启前后的状态？tcp或者提交mysql后崩溃都是类似场景。可以理解为分布式事务问题？简单些全局应用层事务id，保证应用层的幂等性。或者就是先查一次是否成功写入（最后一次提交的记录，再判断是否需要写入？web相关页面隐藏着查一次最新的信息？），来应用层保证幂等和一致性（不一定？）。

---
# Exactly Once语义与事务机制原理
> - [Exactly Once语义与事务机制原理](http://www.jasongj.com/kafka/transaction/): 事务实现横向对比，PostgreSQL、zookeeper

但是在很多要求严格的场景下，如使用Kafka处理交易数据，`Exactly Once`语义是必须的。我们可以通过让下游系统具有幂等性来配合Kafka的`At Least Once`语义来间接实现`Exactly Once`。但是：

*   该方案要求下游系统支持幂等操作，限制了Kafka的适用场景
*   实现门槛相对较高，需要用户对Kafka的工作机制非常了解
*   对于Kafka Stream而言，Kafka本身即是自己的下游系统，但Kafka在0.11.0.0版本之前不具有幂等发送能力

因此，Kafka本身对`Exactly Once`语义的支持就非常必要。

## 操作原子性

操作的原子性是指，多个操作要么全部成功要么全部失败，不存在部分成功部分失败的可能。

实现原子性操作的意义在于：

*   操作结果更可控，有助于提升数据一致性
*   便于故障恢复。因为操作是原子的，从故障中恢复时只需要重试该操作（如果原操作失败）或者直接跳过该操作（如果原操作成功），而不需要记录中间状态，更不需要针对中间状态作特殊处理

# 实现事务机制的几个阶段

## 幂等性发送

上文提到，实现`Exactly Once`的一种方法是让下游系统具有幂等处理特性，而在Kafka Stream中，Kafka Producer本身就是“下游”系统，因此如果能让Producer具有幂等处理特性，那就可以让Kafka Stream在一定程度上支持`Exactly once`语义。

为了实现Producer的幂等语义，Kafka引入了 `Producer ID` （即 `PID` ）和 `Sequence Number` 。**每个新的Producer在初始化的时候会被分配一个唯一的PID，该PID对用户完全透明而不会暴露给用户**。

对于每个PID，该Producer发送数据的每个`<Topic, Partition>`都对应一个从0开始单调递增的`Sequence Number`。

类似地，Broker端也会为每个`<PID, Topic, Partition>`维护一个序号，并且每次Commit一条消息时将其对应序号递增。对于接收的每条消息，如果其序号比Broker维护的序号（即最后一次Commit的消息的序号）大一，则Broker会接受它，否则将其丢弃：

*   如果消息序号比Broker维护的序号大一以上，说明**中间有数据尚未写入**，也即乱序，此时Broker拒绝该消息，Producer抛出`InvalidSequenceNumber`
*   如果消息序号小于等于Broker维护的序号，说明**该消息已被保存**，即为重复消息，Broker直接丢弃该消息，Producer抛出`DuplicateSequenceNumber`

上述设计解决了0.11.0.0之前版本中的两个问题：

*   Broker保存消息后，发送**ACK前宕机**，Producer认为消息未发送成功并重试，造成数据重复
*   前一条消息发送失败，后一条消息发送成功，前一条消息重试后成功，造成数据乱序

> 这里只是保证broker的宕机和生产者的重试。但是无法保证生产者宕机的重试？数据的产生？

## 事务性保证

上述幂等设计只能保证单个Producer对于同一个`<Topic, Partition>`的`Exactly Once`语义。

另外，它并不能保证写操作的原子性——即多个写操作，要么全部被Commit要么全部不被Commit。

更不能保证多个读写操作的的原子性。尤其对于Kafka Stream应用而言，典型的操作即是从某个Topic消费数据，经过一系列转换后写回另一个Topic，保证从源Topic的读取与向目标Topic的写入的原子性有助于从故障中恢复。

**事务保证可使得应用程序将生产数据和消费数据当作一个原子单元来处理，要么全部成功，要么全部失败，即使该生产或消费跨多个`<Topic, Partition>`。**

另外，有状态的应用也可以保证重启后从断点处继续处理，也即事务恢复。

为了实现这种效果，**应用程序必须提供一个稳定的（重启后不变）唯一的ID**，也即 `Transaction ID` 。 `Transactin ID` 与 `PID` 可能一一对应。区别在于 `Transaction ID` **由用户提供**，而 `PID` 是**内部的实现对用户透明**。

另外，为了保证新的Producer启动后，旧的具有相同`Transaction ID`的Producer即失效，每次Producer通过`Transaction ID`拿到PID的同时，还会**获取一个单调递增的epoch**。由于旧的Producer的epoch比新Producer的epoch小，Kafka可以很容易识别出该Producer是老的Producer并拒绝其请求。

> 生产者标识 Transaction ID 和世代epoch保证事务恢复。

有了`Transaction ID`后，Kafka可保证：

*   跨Session的数据幂等发送。当具有相同`Transaction ID`的新的Producer实例被创建且工作时，旧的且拥有相同`Transaction ID`的Producer将不再工作。
*   跨Session的事务恢复。如果某个应用实例宕机，新的实例可以保证任何未完成的旧的事务要么Commit要么Abort，使得新实例从一个正常状态开始工作。

需要注意的是，上述的事务保证是从Producer的角度去考虑的。从Consumer的角度来看，该保证会相对弱一些。尤其是不能保证所有被某事务Commit过的所有消息都被一起消费，因为：

*   对于压缩的Topic而言，同一事务的某些消息可能被其它版本覆盖
*   事务包含的消息可能分布在多个Segment中（即使在同一个Partition内），当老的Segment被删除时，该事务的部分数据可能会丢失
*   Consumer在一个事务内可能通过seek方法访问任意Offset的消息，从而可能丢失部分消息
*   Consumer可能并不需要消费某一事务内的所有Partition，因此它将永远不会读取组成该事务的所有消息

## 事务中Offset的提交

许多基于Kafka的应用，尤其是Kafka Stream应用中同时包含Consumer和Producer，前者负责从Kafka中获取消息，后者负责将处理完的数据写回Kafka的其它Topic中。

为了实现该场景下的事务的原子性，Kafka需要保证对Consumer Offset的Commit与Producer对发送消息的Commit包含在同一个事务中。否则，如果在二者Commit中间发生异常，根据二者Commit的顺序可能会造成数据丢失和数据重复：

*   如果先Commit Producer发送数据的事务再Commit Consumer的Offset，即`At Least Once`语义，可能造成数据重复。
*   如果先Commit Consumer的Offset，再Commit Producer数据发送事务，即`At Most Once`语义，可能造成数据丢失。

> 上述第二步是实现将一组读操作与写操作作为一个事务处理的关键。因为Producer写入的数据Topic以及记录Comsumer Offset的Topic会被写入相同的Transactin Marker，所以这一组读操作与写操作要么全部COMMIT要么全部ABORT。

## 总结

*   `PID`与`Sequence Number`的引入实现了写操作的幂等性
*   写操作的幂等性结合`At Least Once`语义实现了单一Session内的`Exactly Once`语义
*   `Transaction Marker`与`PID`提供了识别消息是否应该被读取的能力，从而实现了事务的隔离性
*   Offset的更新标记了消息是否被读取，从而将对读操作的事务处理转换成了对写（Offset）操作的事务处理
*   Kafka事务的本质是，将一组写操作（如果有）对应的消息与一组读操作（如果有）对应的Offset的更新进行同样的标记（即`Transaction Marker`）来实现事务中涉及的所有读写操作同时对外可见或同时对外不可见
*   Kafka只提供对Kafka本身的读写操作的事务性，不提供包含外部系统的事务性

# 与其它系统事务机制对比

> 有待商榷

## PostgreSQL MVCC

Kafka的事务机制与《[MVCC PostgreSQL实现事务和多版本并发控制的精华](http://www.jasongj.com/sql/mvcc/)》一文中介绍的PostgreSQL通过MVCC实现事务的机制非常类似，对于事务的回滚，并不需要删除已写入的数据，都是将写入数据的事务标记为Rollback/Abort从而在读数据时过滤该数据。

## 两阶段提交

Kafka的事务机制与《[分布式事务（一）两阶段提交及JTA](http://www.jasongj.com/big_data/two_phase_commit/#%E4%B8%A4%E9%98%B6%E6%AE%B5%E6%8F%90%E4%BA%A4%E5%8E%9F%E7%90%86)》一文中所介绍的两阶段提交机制看似相似，都分PREPARE阶段和最终COMMIT阶段，但又有很大不同。

*   Kafka事务机制中，PREPARE时即要指明是`PREPARE_COMMIT`还是`PREPARE_ABORT`，并且只须在`Transaction Log`中标记即可，无须其它组件参与。而两阶段提交的PREPARE需要发送给所有的分布式事务参与方，并且事务参与方需要尽可能准备好，并根据准备情况返回`Prepared`或`Non-Prepared`状态给事务管理器。
*   Kafka事务中，一但发起`PREPARE_COMMIT`或`PREPARE_ABORT`，则确定该事务最终的结果应该是被`COMMIT`或`ABORT`。而分布式事务中，PREPARE后由各事务参与方返回状态，只有所有参与方均返回`Prepared`状态才会真正执行COMMIT，否则执行ROLLBACK
*   Kafka事务机制中，某几个Partition在COMMIT或ABORT过程中变为不可用，只影响该Partition不影响其它Partition。两阶段提交中，若唯一收到COMMIT命令参与者Crash，其它事务参与方无法判断事务状态从而使得整个事务阻塞
*   Kafka事务机制引入事务超时机制，有效避免了挂起的事务影响其它事务的问题
*   Kafka事务机制中存在多个`Transaction Coordinator`实例，而分布式事务中只有一个事务管理器

## Zookeeper

Zookeeper的原子广播协议与两阶段提交以及Kafka事务机制有相似之处，但又有各自的特点

*   Kafka事务可COMMIT也可ABORT。而Zookeeper原子广播协议只有COMMIT没有ABORT。当然，Zookeeper不COMMIT某消息也即等效于ABORT该消息的更新。
*   Kafka存在多个`Transaction Coordinator`实例，扩展性较好。而Zookeeper写操作只能在Leader节点进行，所以其写性能远低于读性能。
*   Kafka事务是COMMIT还是ABORT完全取决于Producer即客户端。而Zookeeper原子广播协议中某条消息是否被COMMIT取决于是否有一大半FOLLOWER ACK该消息。


```
KafkaProducer producer = createKafkaProducer(
  “bootstrap.servers”, “localhost:9092”,
  “transactional.id”, “my-transactional-id”);

producer.initTransactions();

KafkaConsumer consumer = createKafkaConsumer(
  “bootstrap.servers”, “localhost:9092”,
  “group.id”, “my-group-id”,
  "isolation.level", "read_committed");

consumer.subscribe(singleton(“inputTopic”));

while (true) {
  ConsumerRecords records = consumer.poll(Long.MAX_VALUE);
  producer.beginTransaction();
  for (ConsumerRecord record : records)
    producer.send(producerRecord(“outputTopic”, record));
  producer.sendOffsetsToTransaction(currentOffsets(consumer), group);
  producer.commitTransaction();
}
```

---
## Kafka 事务机制的流程
> - [Kafka 是如何实现事务的？](https://www.gushiciku.cn/pl/p3ka)

分布式系统的数据一致性是难的。要想理解一个系统提供何种程度的数据一致性保证，以及这样的保证对应用程序提出了什么样的要求，再及在哪些情况下一致性保证会出现什么方面的回退，细究其一致性机制的实现是必须的。

上面我们提到，事务机制的核心特征是能跨越多个分区原子地提交消息集合，甚至这些分区从属于不同的主题。同时，被提交的消息集合中的消息每条仅被提交一次，并保持它们在生产者应用中被生产的顺序写入到 Kafka 集群的消息日志中。此外，事务能够容忍生产者运行时出现异常甚至宕机重启。

实现事务机制最关键的概念就是事务的**唯一标识符**（ TransactionalID ），Kafka 使用 TransactionalID 来关联进行中的事务。TransactionalID 由用户提供，这是因为 Kafka 作为系统本身无法独立的识别出宕机前后的两个不同的进程其实是要同一个逻辑上的事务。

对于同一个生产者应用前后进行的多个事务，TransactionalID 并不需要每次都生成一个新的。这是因为 Kafka 还实现了 ProducerID 以及 **epoch 机制**。这个机制在事务机制中的用途主要是**用于标识不同的会话**，同一个会话 ProducerID 的值相同，但有可能有多个任期。ProducerID 仅在会话切换时改变，而任期会在每次新的事物初始化时被更新。这样，同一个 TransactionalID 就能作为跨会话的多个独立事务的标识。

## 参考链接
- [Kafka的Exactly-once语义与事务机制](https://www.cnblogs.com/luxiaoxun/p/13048474.html)
- [Kafka 0.11.0.0 是如何实现 Exactly-once 语义的](https://www.jianshu.com/p/5d889a67dcd3): Exactly-once处理是一种端到端的保证，在洒上去之前应用程序必须保证自身设计不违反该原则。 如果您使用的是**消费者API，则必须保证你提交的应用程序状态变更和你的偏移量是一致的**。对于流处理应用，情况会更好一些。 因为流处理是一个封闭的系统，其中输入、输出和状态修改都在相同的操作中建模，它实际上已经类似于exactly-once中的事务，具备原子性了。 配置更改就直接可以为您提供端到端的保证。
- [Exactly Once语义与事务机制原理](http://www.jasongj.com/kafka/transaction/): 事务实现横向对比，PostgreSQL、zookeeper
- [blog-transactions-apache-kafka](https://www.confluent.io/blog/transactions-apache-kafka/) 、 [Improved Robustness and Usability of Exactly-Once Semantics in Apache Kafka](https://www.confluent.io/blog/simplified-robust-exactly-one-semantics-in-kafka-2-5/) 、 [Exactly-Once Processing in Kafka explained](https://ssudan16.medium.com/exactly-once-processing-in-kafka-explained-66ecc41a8548)
