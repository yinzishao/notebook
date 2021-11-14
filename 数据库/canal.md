# Canal

> - [官方简介](https://github.com/alibaba/canal/wiki/%E7%AE%80%E4%BB%8B)

## 工作原理

### mysql主备复制实现

![](https://camo.githubusercontent.com/c26e367a6ffcce8ae6ecb39476a01bef14af6572124a6df050c4dc0c7f1074f3/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333038362f34363863316131342d653761642d333239302d396433642d3434616335303161373232372e6a7067)

从上层来看，复制分成三步：

1.  master将改变记录到二进制日志(binary log)中（这些记录叫做二进制日志事件，binary log events，可以通过show binlog events进行查看）；
2.  slave将master的binary log events拷贝到它的中继日志(relay log)；
3.  slave重做中继日志中的事件，将改变反映它自己的数据。

### canal的工作原理：

![](https://camo.githubusercontent.com/4d345ce5fbd095baa14291311ca7117e55a54cd5b80385b88287962a99eecad2/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333130372f63383762363762612d333934632d333038362d393537372d3964623035626530346339352e6a7067)

原理相对比较简单：

1.  canal模拟mysql slave的交互协议，伪装自己为mysql slave，向mysql master发送dump协议
2.  mysql master收到dump请求，开始推送binary log给slave(也就是canal)
3.  canal解析binary log对象(原始为byte流)

# 架构

![](https://camo.githubusercontent.com/752d022a1904b5bcabfaa7d71ce8f09507f3781190a18ee983f4ba3107035afb/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333132362f34393535303038352d306364322d333266612d383661362d6636373664623562353937622e6a7067)

说明：

*   server代表一个canal运行实例，对应于一个jvm
*   instance对应于一个数据队列 （1个server对应1..n个instance)

instance模块：

*   eventParser (数据源接入，模拟slave协议和master进行交互，协议解析)
*   eventSink (Parser和Store链接器，进行数据过滤，加工，分发的工作)
*   eventStore (数据存储)
*   metaManager (增量订阅&消费信息管理器)

## 知识科普

MySQL 的 Binary Log 介绍

*   [http://dev.mysql.com/doc/refman/5.5/en/binary-log.html](http://dev.mysql.com/doc/refman/5.5/en/binary-log.html)
*   [http://www.taobaodba.com/html/474\_mysqls-binary-log\_details.html](http://www.taobaodba.com/html/474_mysqls-binary-log_details.html)

简单点说：

*   mysql的binlog是多文件存储，定位一个LogEvent需要通过binlog filename + binlog position，进行定位
*   mysql的binlog数据格式，按照生成的方式，主要分为：statement-based、row-based、mixed。

```
    mysql> show variables like 'binlog\_format';
    +---------------+-------+
    | Variable\_name | Value |
    +---------------+-------+
    | binlog\_format | ROW   |
    +---------------+-------+
    1 row in set (0.00 sec)
```
目前canal支持所有模式的增量订阅(但配合同步时，因为statement只有sql，没有数据，无法获取原始的变更日志，所以一般建议为ROW模式)

## EventParser设计

大致过程：

![](https://camo.githubusercontent.com/131c6cd0be965c778353825f36af6b30fe62f5a391c7498a92b75881e91bd06a/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333134332f37393531633136392d663764662d336362332d616562622d6439323466353733313163622e6a7067)

整个parser过程大致可分为几步：

1.  Connection获取上一次解析成功的位置 (如果第一次启动，则获取初始指定的位置或者是当前数据库的binlog位点)
2.  Connection建立链接，发送BINLOG\_DUMP指令
    ```
        // 0. write command number
        // 1. write 4 bytes bin-log position to start at
        // 2. write 2 bytes bin-log flags
        // 3. write 4 bytes server id of the slave
        // 4. write bin-log file name
    ```
3.  Mysql开始推送Binaly Log
4.  接收到的Binaly Log的通过Binlog parser进行协议解析，补充一些特定信息
    // 补充字段名字，字段类型，主键信息，unsigned类型处理
5.  传递给EventSink模块进行数据存储，是一个阻塞操作，直到存储成功
6.  存储成功后，定时记录Binaly Log位置

mysql的Binlay Log网络协议：

![](https://camo.githubusercontent.com/62d8a2d85d401d1928d44e3cf7701174d06eed77b97d74a03d7888e975949c87/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333137332f36333861383361652d336235632d336638332d393732322d3263313931326537636163362e706e67)

说明：

*   图中的协议4byte header，主要是描述整个binlog网络包的length
*   binlog event structure，详细信息请参考：

    ~~forge.mysql.com/wiki/MySQL\_Internals\_Binary\_Log~~

## EventSink设计

![](https://camo.githubusercontent.com/d128d561b03453c5dd5d07d82bd4677408ba4486e77bbb39602a3aaf084598c1/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333231342f30613266643637312d643665392d336564372d623131302d3661336237333861336362302e6a7067)

说明：

*   数据过滤：支持通配符的过滤模式，表名，字段内容等
*   数据路由/分发：解决1:n (1个parser对应多个store的模式)
*   数据归并：解决n:1 (多个parser对应1个store)
*   数据加工：在进入store之前进行额外的处理，比如join

### 数据1:n业务

为了合理的利用数据库资源， 一般常见的业务都是按照schema进行隔离，然后在mysql上层或者dao这一层面上，进行一个数据源路由，屏蔽数据库物理位置对开发的影响，阿里系主要是通过cobar/tddl来解决数据源路由问题。

所以，一般一个数据库实例上，会部署多个schema，每个schema会有由1个或者多个业务方关注

### 数据n:1业务

同样，当一个业务的数据规模达到一定的量级后，必然会涉及到水平拆分和垂直拆分的问题，针对这些拆分的数据需要处理时，就需要链接多个store进行处理，消费的位点就会变成多份，而且数据消费的进度无法得到尽可能有序的保证。

所以，在一定业务场景下，需要将拆分后的增量数据进行归并处理，比如按照时间戳/全局id进行排序归并.

## EventStore设计

*   1\. 目前仅实现了Memory内存模式，后续计划增加本地file存储，mixed混合模式
*   2\. 借鉴了Disruptor的RingBuffer的实现思路

RingBuffer设计：

![](https://camo.githubusercontent.com/50af4886a30b4da7a20ac736b1df9ac948671cbd4ff60412b3d0a21c6e121161/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333233372f30363365383438302d313563382d336536362d626264332d3963343464656630396338662e6a7067)

定义了3个cursor

*   Put : Sink模块进行数据存储的最后一次写入位置
*   Get : 数据订阅获取的最后一次提取位置
*   Ack : 数据消费成功的最后一次消费位置

借鉴Disruptor的RingBuffer的实现，将RingBuffer拉直来看：
![](https://camo.githubusercontent.com/a3bc06a91e4d677042abd109e1159dfd559bd546772dc5696a90d02b6f08e7d5/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333233392f34663538393132642d376338652d333764652d623762382d3130646432316161366332322e6a7067)

实现说明：

*   Put/Get/Ack cursor用于递增，采用long型存储
*   buffer的get操作，通过取余或者与操作。(与操作： cusor & (size - 1) , size需要为2的指数，效率比较高)

## Instance设计

![](https://camo.githubusercontent.com/85a1c5bf4a842319f921bc12b725520392e324b059ea5d70d8dd132b9de50c17/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333234372f35646531633961662d373739382d336434322d626334332d3563353464383263346462662e6a7067)

instance代表了一个实际运行的数据队列，包括了EventPaser,EventSink,EventStore等组件。

抽象了CanalInstanceGenerator，主要是考虑配置的管理方式：

*   manager方式： 和你自己的内部web console/manager系统进行对接。(目前主要是公司内部使用)
*   spring方式：基于spring xml + properties进行定义，构建spring配置.

## Server设计

![](https://camo.githubusercontent.com/3cc638d475109ec126eae754b2a1ea4c4f08a5b99992a31a217699abc7076940/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333235372f66346466333862612d353965322d333938652d623565622d3162626662656363303637362e6a7067)

server代表了一个canal的运行实例，为了方便组件化使用，特意抽象了Embeded(嵌入式) / Netty(网络访问)的两种实现

*   Embeded : 对latency和可用性都有比较高的要求，自己又能hold住分布式的相关技术(比如failover)
*   Netty : 基于netty封装了一层网络协议，由canal server保证其可用性，采用的pull模型，当然latency会稍微打点折扣，不过这个也视情况而定。(阿里系的notify和metaq，典型的push/pull模型，目前也逐步的在向pull模型靠拢，push在数据量大的时候会有一些问题)

## 增量订阅/消费设计

![](https://camo.githubusercontent.com/cc52e7887225728a2f2b3abd73f0a39c81ecc5b1833d483930757790cb19a39f/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333239372f39643765643133652d366138362d333836642d393266342d3835323233386334373562662e6a7067)

具体的协议格式，可参见：[CanalProtocol.proto](https://github.com/alibaba/canal/blob/master/protocol/src/main/java/com/alibaba/otter/canal/protocol/CanalProtocol.proto)

get/ack/rollback协议介绍：

*   Message getWithoutAck(int batchSize)，允许指定batchSize，一次可以获取多条，每次返回的对象为Message，包含的内容为：
    a. batch id 唯一标识
    b. entries 具体的数据对象，对应的数据对象格式：[EntryProtocol.proto](https://github.com/alibaba/canal/blob/master/protocol/src/main/java/com/alibaba/otter/canal/protocol/EntryProtocol.proto)
*   void rollback(long batchId)，顾命思议，回滚上次的get请求，重新获取数据。基于get获取的batchId进行提交，避免误操作
*   void ack(long batchId)，顾命思议，确认已经消费成功，通知server删除数据。基于get获取的batchId进行提交，避免误操作

canal的get/ack/rollback协议和常规的jms协议有所不同，允许get/ack异步处理，比如可以连续调用get多次，后续异步按顺序提交ack/rollback，项目中称之为流式api.

流式api设计的好处：

*   get/ack异步化，减少因ack带来的网络延迟和操作成本 (99%的状态都是处于正常状态，异常的rollback属于个别情况，没必要为个别的case牺牲整个性能)
*   get获取数据后，业务消费存在瓶颈或者需要多进程/多线程消费时，可以不停的轮询get数据，不停的往后发送任务，提高并行化. (作者在实际业务中的一个case：业务数据消费需要跨中美网络，所以一次操作基本在200ms以上，为了减少延迟，所以需要实施并行化)

流式api设计：

![](https://camo.githubusercontent.com/a29476a3ed9176d2d67c038890e20926bb6e9d049519019d9723d514b8f6fb84/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333330302f37663739383665352d643863362d336131372d383739362d3731313636653662633264632e6a7067)

*   每次get操作都会在meta中产生一个mark，mark标记会递增，保证运行过程中mark的唯一性
*   每次的get操作，都会在上一次的mark操作记录的cursor继续往后取，如果mark不存在，则在last ack cursor继续往后取
*   进行ack时，需要按照mark的顺序进行数序ack，不能跳跃ack. ack会删除当前的mark标记，并将对应的mark位置更新为last ack cusor
*   一旦出现异常情况，客户端可发起rollback情况，重新置位：删除所有的mark, 清理get请求位置，下次请求会从last ack cursor继续往后取

## HA机制设计

canal的ha分为两部分，canal server和canal client分别有对应的ha实现

*   canal server: 为了减少对mysql dump的请求，不同server上的instance要求同一时间只能有一个处于running，其他的处于standby状态.
*   canal client: 为了保证有序性，一份instance同一时间只能由一个canal client进行get/ack/rollback操作，否则客户端接收无法保证有序。

整个HA机制的控制主要是依赖了zookeeper的几个特性，watcher和EPHEMERAL节点(和session生命周期绑定)，可以看下我之前zookeeper的相关文章。

Canal Server:

![](https://camo.githubusercontent.com/3e0e1f099ef2bf622cc4fbd7dd8d4132122f8e89ca79cbbe5b44fa364ebbe7bb/687474703a2f2f646c2e69746579652e636f6d2f75706c6f61642f6174746163686d656e742f303038302f333330332f64333230326332362d653935342d333563302d613331392d3537363034313032633537642e6a7067)
大致步骤：

1.  canal server要启动某个canal instance时都先向zookeeper进行一次尝试启动判断 (实现：创建EPHEMERAL节点，谁创建成功就允许谁启动)
2.  创建zookeeper节点成功后，对应的canal server就启动对应的canal instance，没有创建成功的canal instance就会处于standby状态
3.  一旦zookeeper发现canal server A创建的节点消失后，立即通知其他的canal server再次进行步骤1的操作，重新选出一个canal server启动instance.
4.  canal client每次进行connect时，会首先向zookeeper询问当前是谁启动了canal instance，然后和其建立链接，一旦链接不可用，会重新尝试connect.

Canal Client的方式和canal server方式类似，也是利用zookeeper的抢占EPHEMERAL节点的方式进行控制.


---
# 使用Canal实现全量+增量数据同步方案

*   若场景允许，请通过下游目标端对数据的幂等处理来达到数据的最终一致性
*   若业务场景需要全量和增量同步衔接上exactly once，可参考`debezium`的实现方案: 数据库锁+事务快照一致性读来解决这个问题。
*   Canal 本质是一个binlog 数据解析工具，在下游做了一些生态的适配

> Canal 本质是一个实时发布订阅的工具，大部分场景下游为了捕获更实时的变更消息。下游大部分程序支持幂等。

- [使用Canal实现全量+增量数据同步方案](https://github.com/alibaba/canal/issues/3288)

---

# 参考链接
- [canal的优化过程和讨论](https://github.com/alibaba/canal/issues/726): 分阶段进行优化。解析、并行、序列化、数据拷贝等方面。基于ringbuffer的并发模型，整个过程会分为4个阶段，多个阶段之间互相隔离和依赖，把最耗瓶颈的解析这块采用多线程的模型进行加速，预计整个优化完成，整个解析可以跑满整个千兆网卡。跟新版本的redis改成多线程的思路一致。
- [官方简介](https://github.com/alibaba/canal/wiki/%E7%AE%80%E4%BB%8B)

TODO:
- [谈谈对Canal（增量数据订阅与消费）的理解](https://blog.csdn.net/u013256816/article/details/52475190): TODO
- [canal设计上的一些小分析](https://kaimingwan.com/post/framworks/canal/canalshe-ji-shang-de-yi-xie-xiao-fen-xi)
- [深入解析中间件之-Canal](https://zqhxuyuan.github.io/2017/10/10/Midd-canal/)
- [CANAL源码解析](http://www.tianshouzhi.com/api/tutorials/canal/380)
