# kafka介绍

在大数据中，使用了大量的数据。 关于数据，我们有两个主要挑战。第一个挑战是如何收集大量的数据，第二个挑战是分析收集的数据。 为了克服这些挑战，您必须需要一个消息系统。

物理上把Topic分成一个或多个Partition，每个Partition**在物理上对应一个文件夹**，该文件夹下存储这个Partition的所有**消息和索引文件**。

这里要注意，因为**Kafka读取特定消息的时间复杂度为O(1)，即与文件大小无关**，所以这里删除过期文件与提高Kafka性能无关。选择怎样的删除策略只与磁盘以及具体的需求有关。另外，Kafka会为每一个Consumer Group保留一些metadata信息——当前消费的消息的position，也即offset。这个offset由Consumer控制。正常情况下Consumer会在消费完一条消息后递增该offset。当然，Consumer也可将offset设成一个较小的值，重新消费一些消息。因为offet由Consumer控制，所以**Kafka broker是无状态的**，它不需要标记哪些消息被哪些消费过，也不需要通过broker去**保证同一个Consumer Group只有一个Consumer能消费某一条消息**，因此也就**不需要锁机制**，这也为Kafka的**高吞吐率**提供了有力保障。


每一个分区都是一个顺序的、不可变的消息队列， 并且可以持续的添加。分区中的消息都被分配了一个序列号，称之为偏移量(offset),在每个分区中此偏移量都是唯一的。

Kafka集群保持所有的消息，直到它们过期， 无论消息是否被消费了。

实际上消费者所持有的仅有的元数据就是这个偏移量，也就是消费者在这个log中的位置。 这个偏移量由消费者控制：正常情况当消费者消费消息的时候，偏移量也线性的的增加。但是实际偏移量由消费者控制，消费者可以将偏移量**重置**为更老的一个偏移量，重新读取消息。

可以看到这种设计对消费者来说操作自如， 一个消费者的操作不会影响其它消费者对此log的处理。


Kafka采用了一种分而治之的策略：分区。 因为Topic分区中消息只能由消费者组中的唯一一个消费者处理，所以消息肯定是按照先后顺序进行处理的。但是它也仅仅是保证Topic的一个分区顺序处理，不能保证跨分区的消息先后处理顺序。

同一Topic的一条消息只能被同一个Consumer Group内的一个Consumer消费，但多个Consumer Group可同时消费这一消息。


### Push/pull

作为一个消息系统，Kafka遵循了传统的方式，选择由Producer向broker push消息并由Consumer从broker pull消息。一些logging-centric system，比如Facebook的Scribe和Cloudera的Flume，采用push模式。事实上，push模式和pull模式各有优劣。

push模式很难适应**消费速率不同的消费者**，因为消息发送速率是由broker决定的。push模式的目标是**尽可能以最快速度传递消息**，但是这样很容易造成Consumer来不及处理消息，典型的表现就是**拒绝服务以及网络拥塞**。而pull模式则可以根据Consumer的消费能力以**适当的速率消费消息**。

> TODO: 对比rabbitmq的区别。生成环境会有什么问题。

### 对于Kafka而言，**pull模式更合适**。
- pull模式可**简化broker的设计**
- Consumer可**自主控制消费消息的速率**
- 同时Consumer可以自己**控制消费方式**——即可批量消费也可逐条消费
- 同时还能选择不同的提交方式从而实现**不同的传输语义**。 　　


---
# 消费者分区分配策略

同一时刻，**一条消息只能被组中的一个消费者实例消费**

消费者组订阅这个主题，意味着主题下的所有分区都会被组中的消费者消费到，如果按照从属关系来说的话就是，主题下的每个分区只从属于组中的一个消费者，不可能出现**组中的两个消费者负责同一个分区**。

问题： 如果分区数小于组中的消费者实例数

那么按照默认的策略（PS：之所以强调默认策略是因为你也可以自定义策略），有一些消费者是多余的，一直接不到消息而处于空闲状态。


- http://www.jasongj.com/2015/03/10/KafkaColumn1/
- [Kafka分区与消费者的关系](https://www.cnblogs.com/cjsblog/p/9664536.html)


## Kafka创建Topic时如何将分区放置到不同的Broker中？

1）副本因子**不能大于** Broker 的个数；

2）第一个分区（编号为0）的第一个副本放置位置是**随机**从 brokerList 选择的；

3）其他分区的第一个副本放置位置相对于第0个分区**依次往后移**。也就是如果我们有5个 Broker，5个分区，假设第一个分区放在第四个 Broker 上，那么第二个分区将会放在第五个 Broker 上；第三个分区将会放在第一个 Broker 上；第四个分区将会放在第二个 Broker 上，依次类推；

4）剩余的副本相对于第一个副本放置位置其实是由 **nextReplicaShift** 决定的，而这个数也是**随机产生**的；


---
# Kafka为什么快
> - [Kafka核心基础知识](https://juejin.cn/post/6898925796971249678#heading-17)

## 顺序读写
kafka的消息是不断追加到文件中的，这个特性使kafka可以充分利用磁盘的顺序读写性能

顺序读写不需要硬盘磁头的寻道时间，只需很少的扇区旋转时间，所以速度远快于随机读写

## 零拷贝

服务器先将文件从复制到内核空间，再复制到用户空间，最后再复制到内核空间并通过网卡发送出去，而零拷贝则是直接从内核到内核再到网卡，省去了用户空间的复制

Zero copy对应的是Linux中sendfile函数，这个函数会接受一个offsize来确定从哪里开始读取。现实中，不可能将整个文件全部发给消费者，他通过消费者传递过来的偏移量来使用零拷贝读取指定内容的数据返回给消费者

## 分区

kafka中的topic中的内容可以被分为多分partition存在,每个partition又分为多个段segment,所以每次操作都是针对一小部分做操作，很轻便，并且增加并行操作的能力

## 批量发送

kafka允许进行批量发送消息，producter发送消息的时候，可以将消息缓存在本地,等到了固定条件发送到kafka

1. 等消息条数到固定条数
2. 一段时间发送一次

## 数据压缩
Kafka还支持对消息集合进行压缩，Producer可以通过GZIP或Snappy格式对消息集合进行压缩。

压缩的好处就是减少传输的数据量，减轻对网络传输的压力。

Producer压缩之后，在Consumer需进行解压，虽然增加了CPU的工作，但在对大数据处理上，瓶颈在网络上而不是CPU，所以这个成本很值得


---
# Kafka消费与位移
> - [Kafka消费与位移](https://blog.csdn.net/Alex_Sheng_Sea/article/details/87781119)

offsets.retention.minutes：服务端_consumer_offsets保存的消费者offset的时间

- LogStartOffset:表示partition的**起始位置**,初始值为0,由于消息的增加以及日志清除策略影响，这个值会阶段性增大。尤其注意这个不能缩写未LSO,LSO代表的是LastStableOffset,**和事务有关**。
- ConsumerOffset:消费位移，表示partition的某个消费者消费到的位移位置。
- HighWatermark: 简称HW,代表消费端**能看到**的partition的最高日志位移,HW大于等于ConsumerOffset的值。
- LogEndOffset: 简称LEO,代表partition的最高日志位移，第消费者不可见,HW到LEO这之间的数据**未被follwer完全同步**。

---
# 如何保证消息的可靠性与一致性
> - [kafka-如何保证消息的可靠性与一致性](https://juejin.cn/post/6844903765565243406): ISR机制介绍。一些概念的介绍

## 在kafka中ISR是什么？

在zk中会保存AR（Assigned Replicas）列表，其中包含了分区所有的副本，其中 AR = ISR+OSR

- **ISR（in sync replica）**：是kafka动态维护的一组同步副本，在ISR中有成员存活时，只有这个组的成员才可以成为leader，内部保存的为**每次提交信息时必须同步的副本**（acks = all时），每当leader挂掉时，**在ISR集合中选举出一个follower作为leader提供服务**，当ISR中的副本被认为坏掉的时候，会被踢出ISR，当重新跟上leader的消息数据时，重新进入ISR。
- **OSR（out sync replica）**: 保存的副本不必保证必须同步完成才进行确认，**OSR内的副本是否同步了leader的数据，不影响数据的提交**，OSR内的follower尽力的去同步leader，可能数据版本会落后。

参考链接: [Kafka中的ISR、AR又代表什么？ISR伸缩又是什么？](#Kafka中的ISR、AR又代表什么？ISR伸缩又是什么？)

## kafka如何控制需要同步多少副本才可以返回确定到生产者消息才可用？

- 当写入到kakfa时，生产者可以选择是否等待0（只需写入leader）,1（只需同步一个副本） 或 -1（全部副本）的消息确认（这里的副本指的是ISR中的副本）。
> 这是啥参数？ack错误解释？只需要同步一个副本？ 0： 不需要等待。 1： 只需要写入leader。-1：全部副本。

- 需要**注意的是“所有副本确认”并不能保证全部分配副本已收到消息**。默认情况下，当acks=all时，只要当前所有在同步中的副本（**ISR中的副本**）收到消息，就会进行确认。所以Kafka的交付承诺可以这样理解：对没有提交成功的消息不做任何交付保证，而对于ISR中至少有一个存活的完全同步的副本的情况下的“成功提交”的消息保证不会丢失。


## kafka分区partition挂掉之后如何恢复？
在kafka中有一个partition recovery机制用于恢复挂掉的partition。

每个Partition会**在磁盘记录一个RecoveryPoint**（恢复点）, 记录已经**flush到磁盘的最大offset**。当broker fail 重启时,会进行loadLogs。 首先会读取该Partition的RecoveryPoint,找到包含RecoveryPoint点上的segment及以后的segment, 这些segment就是可能没有完全flush到磁盘segments。然后调用segment的recover,重新读取各个segment的msg,并重建索引。

优点：

1. 以segment为单位管理Partition数据,方便数据生命周期的管理,删除过期数据简单
2. 在程序崩溃重启时,加快recovery速度,只需恢复未完全flush到磁盘的segment即可

## 什么原因导致副本与leader不同步的呢？

- 慢副本：在一定周期时间内follower不能追赶上leader。最常见的原因之一是I / O瓶颈导致follower追加复制消息速度慢于从leader拉取速度。
- 卡住副本：在一定周期时间内follower停止从leader拉取请求。follower replica卡住了是由于GC暂停或follower失效或死亡。
- 新启动副本：当用户给主题增加副本因子时，新的follower不在同步副本列表中，直到他们完全赶上了leader日志。

一个partition的follower落后于leader足够多时，被认为不在同步副本列表或处于滞后状态。

正如上述所说，现在kafka判定落后有两种，副本滞后判断**依据是副本落后于leader最大消息数量(replica.lag.max.messages)或replicas响应partition leader的最长等待时间(replica.lag.time.max.ms)。前者是用来检测缓慢的副本,而后者是用来检测失效或死亡的副本**

> 落后的判断条件

## 如果ISR内的副本挂掉怎么办？

两种选择：
- 服务直接不可用一段时间等待ISR中副本恢复（祈祷恢复的副本有数据吧）
- 直接选用第一个副本（这个副本不一定在ISR中）作为leader

这两种方法也是在可用性和一致性之间的权衡。

服务不可用方式这种适用在不允许消息丢失的情况下使用，适用于一致性大于可用性，可以有两种做法

- **设置ISR最小同步副本数量**，如果ISR的当前数量大于设置的最小同步值，那么该分区才会接受写入，**避免了ISR同步副本过少**。如果小于最小值那么该分区将不接收写入。这个**最小值设置只有在acks = all的时候才会生效**。
> min.insync.replicas参数的含义。最小值设置只有在acks = all的时候才会生效

- 禁用unclean-leader选举，当isr中的所有副本全部不可用时，不可以使用OSR 中的副本作为leader，直接使服务不可用，直到等到ISR 中副本恢复再进行选举leader。

直接选择第一个副本作为leader的方式，适用于可用性大于一致性的场景，这也是kafka在isr中所有副本都死亡了的情况采用的默认处理方式，我们可以通过配置参数`unclean.leader.election.enable`来禁止这种行为，采用第一种方法。

## 那么ISR是如何实现同步的呢？
broker的offset大致分为三种：base offset、high watemark（HW）、log end offset（LEO）

- base offset：起始位移，replica中第一天消息的offset
- HW：replica高水印值，副本中最新一条已提交消息的位移。leader 的HW值也就是实际已提交消息的范围，每个replica都有HW值，但仅仅leader中的HW才能作为标示信息。什么意思呢，就是说当按照参数标准成功完成消息备份（成功同步给follower replica后）才会更新HW的值，代表消息理论上已经不会丢失，可以认为“已提交”。
- LEO：日志末端位移，也就是replica中下一条待写入消息的offset，注意哈，是下一条并且是待写入的，并不是最后一条。

过程:

1. broker 收到producer的请求
2. leader 收到消息，并成功写入，LEO 值+1
3. broker 将消息推给follower replica，follower 成功写入 LEO +1
4. 所有LEO 写入后，leader HW +1
5. 消息可被消费，并成功响应

## 解决上一个问题后，接下来就是kafka如何选用leader呢？
选举leader常用的方法是多数选举法，比如Redis等，但是kafka没有选用多数选举法，kafka采用的是**quorum（法定人数）**。

quorum是一种在分布式系统中常用的算法，主要用来**通过数据冗余来保证数据一致性的投票算法**。在kafka中该算法的实现就是ISR，**在ISR中就是可以被选举为leader的法定人数**。

在leader宕机后，只能从ISR列表中选取新的leader，无论ISR中哪个副本被选为新的leader，它**都知道HW之前的数据**，可以保证在切换了leader后，消费者可以继续看到HW之前已经提交的数据。

HW的截断机制：选出了新的leader，而新的leader**并不能保证已经完全同步了之前leader的所有数据，只能保证HW之前的数据是同步过的，此时所有的follower都要将数据截断到HW的位置，再和新的leader同步数据，来保证数据一致**。

当宕机的leader恢复，发现新的leader中的数据和自己持有的数据不一致，**此时宕机的leader会将自己的数据截断到宕机之前的hw位置**，然后同步新leader的数据。宕机的leader活过来也像follower一样同步数据，来保证数据的一致性。

## 总结

> 总结一下：
> - 通过in sync replica 来维护一个必须完全同步的副本。通过min.insync.replicas进行配置，默认是1。
> - 生产者通过写入ack进行副本数据的写入。但要注意是当前所有在同步中的副本（ISR中的副本）。
> - ISR内的副本挂掉，要注意可用性还是一致性。通过禁止`unclean.leader.election.enable`保证一致性。也可以通过min.insync.replicas进行配置避免同步副本过少。
> - HW（高水位值）、LEO（日志末端位移）概念，进行日志同步
> - leader选举，采用quorum法定人数。通过数据冗余来保证数据一致性的投票算法, ISR列表选取新的leader。通过HW的截断机制进行数据的一致性同步。


---
# Kafka中的ISR、AR又代表什么？ISR伸缩又是什么？

> - [kafka中的ISR、AR又代表什么？ISR伸缩又是什么？](https://blog.csdn.net/weixin_43975220/article/details/93190906)

Leader副本负责维护和跟踪ISR集合中所有的follower副本的滞后状态，**当follower副本落后太多或者失效时，leader副本会吧它从ISR集合中剔除**。如果OSR集合中follower副本“追上”了Leader副本，之后再**ISR集合中的副本才有资格被选举为leader**，而在OSR集合中的副本则没有机会（这个原则可以通过修改对应的参数配置来改变）

 Kafka在启动的时候会开启两个与ISR相关的定时任务，名称分别为“isr-expiration"和”isr-change-propagation".。

isr-expiration任务会**周期性的检测每个分区是否需要缩减其ISR集合**。这个周期和“replica.lag.time.max.ms”参数有关。大小是这个参数一半。默认值为5000ms，当检测到ISR中有是失效的副本的时候，就会缩减ISR集合。

如果某个分区的ISR集合发生变更， 则会将变更后的数据记录到ZooKerper对应/brokers/topics//partition//state节点中。

有缩减就会有补充，那么kafka何时扩充ISR的？

随着follower副本不断进行消息同步，follower副本LEO也会逐渐后移，并且最终赶上leader副本，此时follower副本就有资格进入ISR集合，追赶上leader副本的判定准侧是此副本的LEO是否小于leader副本HW，这里并不是和leader副本LEO相比。ISR扩充之后同样会更新ZooKeeper中的/broker/topics//partition//state节点和isrChangeSet，之后的步骤就和ISR收缩的时的相同。

当ISR集合发生增减时，或者ISR集合中任一副本LEO发生变化时，都会影响整个分区的HW。

> 细节没有进行细究。主要还是这两个参数: replica.lag.max.messages、replica.lag.time.max.ms。落后的时间与消息数量。恢复通过HW

---
# Kafka生产者ack机制剖析
> - [Kafka生产者ack机制剖析](https://juejin.cn/post/6857514628516315149): 一个比较简明扼要的总结分析生产者。


Kafka有两个很重要的配置参数，acks与min.insync.replicas .其中acks是producer的配置参数，min.insync.replicas是Broker端的配置参数，这两个参数对于**生产者不丢失数据起到了很大的作用**.

## 分区副本

Kafka的topic是可以分区的，并且可以为分区配置多个副本，改配置可以通过replication.factor参数实现. Kafka中的分区副本包括两种类型：领导者副本（Leader Replica）和追随者副本（Follower Replica)，每个分区在创建时都要选举一个副本作为领导者副本，其余的副本自动变为追随者副本.

在 Kafka 中，**追随者副本是不对外提供服务的**，也就是说，任何一个追随者副本都不能响应消费者和生产者的读写请求. 所有的请求**都必须由领导者副本来处理**. 换句话说，所有的读写请求都必须发往领导者副本所在的 Broker，由该 Broker 负责处理. 追随者副本不处理客户端请求，它唯一的任务就是**从领导者副本异步拉取消息**，并写入到自己的提交日志中，从而实现与领导者副本的同步.

## 同步副本(In-sync replicas)

In-sync replica(ISR)称之为同步副本，ISR中的副本都是与Leader进行同步的副本，所以不在该列表的follower会被认为与Leader是不同步的. 那么，ISR中存在是什么副本呢？首先可以明确的是：Leader副本总是存在于ISR中. 而follower副本是否在ISR中，取决于该follower副本是否与Leader副本保持了“同步”.

Kafka的broker端有一个参数**replica.lag.time.max.ms**, 该参数表示follower副本滞后与Leader副本的**最长时间间隔，默认是10秒**.  这就意味着，只要follower副本落后于leader副本的时间间隔不超过10秒，就可以认为该follower副本与leader副本是同步的，所以哪怕当前follower副本落后于Leader副本几条消息，只要在10秒之内赶上Leader副本，就不会被踢出出局.

> 还有一个最大延迟消息数

Kafka默认的副本因子是3，即每个分区只有1个leader副本和2个follower副本

## acks确认机制

对于消息是否丢失起着重要作用，该参数的配置具体如下：

*   acks=0，表示生产者在成功写入消息之前不会等待任何来自服务器的响应. 换句话说，一旦出现了问题导致服务器没有收到消息，那么生产者就无从得知，消息也就丢失了. 改配置由于不需要等到服务器的响应，所以可以以网络支持的最大速度发送消息，从而达到很高的吞吐量。

*   acks=1，表示只要集群的leader分区副本接收到了消息，就会向生产者发送一个成功响应的ack，此时生产者接收到ack之后就可以认为该消息是写入成功的. 一旦消息无法写入leader分区副本(比如网络原因、leader节点崩溃),生产者会收到一个错误响应，当生产者接收到该错误响应之后，为了避免数据丢失，会重新发送数据.这种方式的吞吐量取决于使用的是异步发送还是同步发送.

    > 尖叫提示：如果生产者收到了错误响应，即便是重新发消息，还是会有可能出现丢数据的现象. 比如，如果一个没有收到消息的节点成为了新的Leader，消息就会丢失.

*   acks =all/-1,表示只有所有参与复制的节点(ISR列表的副本)全部收到消息时，生产者才会接收到来自服务器的响应. 这种模式是最高级别的，也是最安全的，可以确保不止一个Broker接收到了消息. 该模式的延迟会很高.

## 最小同步副本

上面提到，当acks=all时，需要所有的副本都同步了才会发送成功响应到生产者. 其实这里面存在一个问题：如果Leader副本是唯一的同步副本时会发生什么呢？此时相当于acks=1.所以是不安全的.

Kafka的Broker端提供了一个参数\*\*`min.insync.replicas`\*\*,该参数控制的是消息至少被写入到多少个副本才算是"真正写入",该值默认值为1，生产环境设定为一个大于1的值可以提升消息的持久性. 因为如果同步副本的数量低于该配置值，则生产者会收到错误响应，从而确保消息不丢失.

Kafka的Broker端提供了一个参数**min.insync.replicas**,该参数控制的是消息至少被写入到多少个副本才算是"真正写入",该值默认值为1，生产环境设定为一个大于1的值可以提升消息的持久性. 因为如果同步副本的数量低于该配置值，则生产者会收到错误响应，从而确保消息不丢失.

当min.insync.replicas=2，如果此时ISR列表只有[1],2和3被踢出ISR列表，那么当acks=all时，则不能成功写入数；当acks=0或者acks=1可以成功写入数据.

这种情况是很容易引起误解的，如果acks=all且min.insync.replicas=2，此时ISR列表为[1,2,3],那么**还是会等到所有的同步副本都同步了消息**，才会向生产者发送成功响应的ack.因为min.insync.replicas=2只是一个**最低限制，即同步副本少于该配置值，则会抛异常**，而acks=all，是需要保证所有的ISR列表的副本都同步了才可以发送成功响应


---
# 如何保证Kafka不丢失消息

> - [如何保证Kafka不丢失消息](https://juejin.cn/post/6844904094021189639): 从生产者与消费者角度说明

## 生产者丢失消息的情况

试想一种情况：假如 leader 副本所在的 broker 突然挂掉，那么就要从 follower 副本重新选出一个 leader ，但是 leader 的数据还有一些没有被 follower 副本的同步的话，就会造成消息丢失。

### 设置 acks = all
解决办法就是我们设置  acks = all。acks 是 Kafka 生产者(Producer)  很重要的一个参数。

acks 的默认值即为1，代表我们的消息被leader副本接收之后就算被成功发送。当我们配置 acks = all **代表则所有副本都要接收到该消息之后该消息才算真正成功被发送**。

### 设置 replication.factor >= 3

为了保证 leader 副本能有 follower 副本能同步消息，我们一般会为 topic 设置 replication.factor >= 3。**这样就可以保证每个 分区(partition) 至少有 3 个副本。虽然造成了数据冗余，但是带来了数据的安全性。**

### 设置 min.insync.replicas > 1

一般情况下我们还需要设置 min.insync.replicas> 1 ，**这样配置代表消息至少要被写入到 2 个副本才算是被成功发送**。min.insync.replicas 的默认值为 1 ，在实际生产中应尽量避免默认值 1。

但是，为了保证整个 Kafka 服务的高可用性，你需要确保 replication.factor > min.insync.replicas 。为什么呢？设想一下加入两者相等的话，**只要是有一个副本挂掉，整个分区就无法正常工作了**。这明显违反高可用性！**一般推荐设置成 replication.factor = min.insync.replicas + 1**。

### 设置 unclean.leader.election.enable = false

Kafka 0.11.0.0版本开始 unclean.leader.election.enable 参数的默认值由原来的true 改为false

我们最开始也说了我们发送的消息会被发送到 leader 副本，然后 follower 副本才能从 leader 副本中拉取消息进行同步。多个 follower 副本之间的消息同步情况不一样，当我们配置了 unclean.leader.election.enable = false  的话，**当 leader 副本发生故障时就不会从  follower 副本中和 leader 同步程度达不到要求的副本中选择出  leader ，这样降低了消息丢失的可能性**。

> min.insync.replicas = ${N/2 + 1} 这样理解是有误的？并不是这样多数选举，而是quorum（法定人数）


## 消费者丢失消息的情况

我们知道消息在被追加到 Partition(分区)的时候都会分配一个特定的偏移量（offset）。偏移量（offset)表示 Consumer 当前消费到的 Partition(分区)的所在的位置。Kafka 通过偏移量（offset）可以保证消息在分区内的顺序性。

当消费者拉取到了分区的某个消息之后，消费者会自动提交了 offset。自动提交的话会有一个问题，试想一下，当消费者刚拿到这个消息准备进行真正消费的时候，突然挂掉了，消息实际上并没有被消费，但是 offset 却被自动提交了。

**解决办法也比较粗暴，我们手动关闭闭自动提交 offset，每次在真正消费完消息之后之后再自己手动提交 offset** 。 但是，细心的朋友一定会发现，这样**会带来消息被重新消费的问题**。比如你刚刚消费完消息之后，还没提交 offset，结果自己挂掉了，那么这个消息理论上就会被消费两次。


---
# max.poll.interval.ms

对于消息处理时间变化不可预测的用例，这两个选项都不够。处理这些情况的推荐方法是将消息处理移动到另一个线程，这允许使用者在处理器仍在工作时继续调用poll。必须注意确保承诺的偏移量不会超过实际位置。通常，禁用记录的自动提交，只有在线程完成处理记录后（取决于所需的传递语义），才能手动提交处理过的偏移量。还请注意，您需要暂停分区，以便在线程处理完以前返回的记录之前，不会从轮询接收到新记录。

- [Detecting Consumer Failures](https://kafka.apache.org/22/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html): 源码的注释更好介绍相应的场景和注意事项，比书籍的半吊子注释要强。多看看官方文档的蛛丝马迹。
