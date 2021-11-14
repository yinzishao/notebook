- [cluster-deployment](https://clickhouse.tech/docs/en/getting-started/tutorial/#cluster-deployment)
- [阿里云数据库clickhouse](https://help.aliyun.com/product/144466.html?spm=a2c4g.11186623.6.540.2ac02ac4sIj978)
- [集群监控的指标参考](https://help.aliyun.com/document_detail/172413.html?spm=a2c4g.11186623.6.585.14ff150cAX4a3o)

# 基本概念

## 系列
ClickHouse集群包含两个系列，分别是高可用系列和单副本系列。高可用系列每个节点包含两个副本，即是双副本集群；单副本系列每个节点只有1个副本。

高可用集群的某个副本服务不可用的时候，同一节点（分片）的另一个副本还可以继续服务，因此集群是高可用集群；单副本集群的某一个副本服务不可用的时候，会导致整个集群不可用，**需要等待该副本完全恢复服务状态**，集群才能继续提供稳定服务。

因此，高可用集群的资源以及对应的购买成本都是单副本集群的2倍。

> 注意副本的概念。其和ES不一样。

## 分片（Shard）
在超大规模海量数据处理场景下，单台服务器的存储、计算资源会成为瓶颈。为了进一步提高效率，云数据库ClickHouse将海量数据分散存储到多台服务器上，每台服务器只存储和处理海量数据的一部分，在这种架构下，每台服务器被称为一个分片（Shard）。

## 副本（Replica）
为了在异常情况下保证数据的安全性和服务的高可用性，ClickHouse提供了副本机制，将单台服务器的数据冗余存储在2台或多台服务器上。

## 本地表（Local Table）
本地表的数据，只会存储在当前写入的节点上，不会被分散到多台机器上。

## 分布式表（Distributed Table）
分布式表是本地表的集合，它将多个本地表抽象为一张统一的表，对外提供写入、查询功能。当写入分布式表时，数据会被自动分发到集合中的各个本地表中；当查询分布式表时，集合中的各个本地表都会被分别查询，并且把最终结果汇总后返回。

> 本地表与分布式表的区别在于：本地表的写入和查询，受限于单台服务器的存储、计算资源，不具备横向拓展能力；而分布式表的写入和查询，则可以利用多台服务器的存储、计算资源，具有较好的横向拓展能力。

## 单机表（Non-Replicated Table）
单机表的数据，只会存储在当前机器上，不会被复制到其他机器，即只有一个副本。

## 复制表（Replicated Table）
复制表的数据，会被自动复制到多台机器上，形成多个副本。

> 单机表与复制表的区别在于：
>   - 单机表在异常情况下无法保证服务高可用。
>   - 复制表在至少有一个正常副本的情况下，仍旧能够对外提供服务。

# ClickHouse二级索引
ClickHouse官方开源版目前没有二级索引的功能设计，以下二级索引相关功能是云数据库ClickHouse的增强功能，并且只适配于v20.3以及更高的内核版本。这里的二级索引和官方开源版的索引并不是一个原理，解决的也不是同一类问题，二级索引最常见的使用场景是对根据非排序键的等值条件进行点查加速。


---
# zookeeper

## settings
在使用复制表时，ClickHouse使用ZooKeeper来存储副本的元数据。如果不使用复制表，则可以忽略此部分参数

```yaml
<node index="1">
    <host>example_host</host>
    <port>2181</port>
</node>
```

当尝试连接到ZooKeeper集群时，`index`属性指定节点的顺序。

- session_timeout: 客户端会话的最大超时（毫秒）。

- root: 用作ClickHouse服务器使用的znode根的znode。可选。

- identity: 用户和密码，ZooKeeper可以要求它访问请求的znode。可选。


### use_minimalistic_part_header_in_zookeeper

如果使用use_minimalistic_part_header_in_zookeeper = 1, 复制的表使用单个znode紧凑地存储数据块的headers。如果表包含许多列，则此存储方法将大大减少Zookeeper中存储的数据量。

> 您不能将ClickHouse服务器降级到不支持此设置的版本。

> 在群集中的服务器上升级ClickHouse时要小心。不要一次升级所有服务器。在测试环境中测试ClickHouse的新版本更安全，或者只在集群的几个服务器上测试

> 已经使用此设置存储的数据部件头无法恢复为其以前的（非紧凑型）表示形式。

## 配置方式
ClickHouse使用一组zookeeper标签定义相关配置，默认情况下，在全局配置config.xml中定义即可。但是各个副本所使用的Zookeeper配置通常是相同的，为了便于在多个节点之间复制配置文件，更常见的做法是将这一部分配置抽离出来，独立使用一个文件保存。

首先，在服务器的/etc/clickhouse-server/config.d目录下创建一个名为metrika.xml的配置文件：

接着，在全局配置config.xml中使用<include_from>标签导入刚才定义的配置：
`<include_from>/etc/clickhouse-server/config.d/metrika.xml</include_from>`
并引用ZooKeeper配置的定义：
`<zookeeper incl="zookeeper-servers" optional="false" />`

其中，incl与metrika.xml配置文件内的节点名称要彼此对应。至此，整个配置过程就完成了。

ClickHouse在它的系统表中，颇为贴心地提供了一张名为zookeeper的代理表。通过这张表，可以使用SQL查询的方式读取远端ZooKeeper内的数据。有一点需要注意，在用于查询的SQL语句中，必须指定path条件，例如查询根路径： `SELECT * FROM system.zookeeper where path = '/'`

## tips
您不应该使用手动编写的脚本在不同的ZooKeeper集群之间传输数据，因为结果对于连续节点是不正确的。切勿出于同样的原因使用“zkcopy”实用程序： https://github.com/ksprojects/zkcopy/issues/15

如果要将现有的ZooKeeper集群一分为二，正确的方法是增加其副本的数量，然后将其重新配置为两个独立的集群。

不要在与ClickHouse相同的服务器上运行ZooKeeper。因为ZooKeeper对延迟非常敏感，ClickHouse可能会利用所有可用的系统资源。

使用默认设置，ZooKeeper是定时炸弹：

使用默认配置（请参阅autopurge）时，ZooKeeper服务器不会从旧的快照和日志中删除文件，这是操作员的责任。

必须炸掉这枚炸弹。

附带zookeeper的一些配置。

```
见链接
```

- [zookeeper](https://clickhouse.tech/docs/en/operations/tips/#zookeeper)
- [server-settings_zookeeper](https://clickhouse.tech/docs/en/operations/server-configuration-parameters/settings/#server-settings_zookeeper)




---
# replication

使用副本的好处甚多。首先，由于增加了数据的冗余存储，所以降低了数据丢失的风险；其次，由于副本采用了**多主架构**，所以**每个副本实例都可以作为数据读、写的入口，这无疑分摊了节点的负载**

```sql
CREATE TABLE table_name
(
    EventDate DateTime,
    CounterID UInt32,
    UserID UInt32
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/table_name', '{replica}')
PARTITION BY toYYYYMM(EventDate)
ORDER BY (CounterID, EventDate, intHash32(UserID))
SAMPLE BY intHash32(UserID)

```

ReplicatedMergeTree的定义方式如下：

```ENGINE =ReplicatedMergeTree('zk_path','replica_name')```

zk_path用于指定在ZooKeeper中创建的数据表的路径，路径名称是自定义的，并没有固定规则，用户可以设置成自己希望的任何路径。

> 对于zk_path而言，同一张数据表的同一个分片的不同副本，应该定义相同的路径；而对于replica_name而言，同一张数据表的同一个分片的不同副本，应该定义不同的名称。

这些参数可以包含宏替换的占位符，即大括号的部分。它们会被替换为配置文件里 ‘macros’ 那部分配置的值。示例：
```yaml
<macros>
    <layer>05</layer>
    <shard>02</shard>
    <replica>example05-02-1.yandex.ru</replica>
</macros>
```

`SELECT * FROM system.macros`

- [replication](https://clickhouse.tech/docs/en/engines/table-engines/mergetree-family/replication/)


副本协同的核心流程主要有INSERT、MERGE、MUTATION和ALTER四种，分别对应了**数据写入、分区合并、数据修改和元数据修改**。INSERT和ALTER查询是分布式执行的。借助ZooKeeper的事件通知机制，多个副本之间会自动进行有效协同，但是它们**不会使用ZooKeeper存储任何分区数据**。而**其他查询并不支持分布式执行**，包括SELECT、CREATE、DROP、RENAME和ATTACH。例如，为了创建多个副本，我们需要分别登录每个ClickHouse节点，在它们本地执行各自的CREATE语句（后面将会介绍如何利用集群配置简化这一操作）。

可以看到，在INSERT的写入过程中，ZooKeeper不会进行任何实质性的数据传输。本着谁执行谁负责的原则，在这个案例中由CH5首先在本地写入了分区数据。之后，也由**这个副本负责发送Log日志，通知其他副本下载数据**。如果设置了insert_quorum并且insert_quorum&gt;=2，则还会由该副本**监控完成写入的副本数量**。其他副本在接收到Log日志之后，会选择一个**最合适的远端副本，点对点地下载分区数据**。

无论MERGE操作从哪个副本发起，其合并计划都会交**由主副本来制定**。

主副本还会锁住执行线程，对日志的接收情况进行监听

其监听行为由replication_alter_partitions_sync参数控制，默认值为1。当此参数为0时，不做任何等待；为1时，只等待主副本自身完成；为2时，会等待所有副本拉取完成。

在MERGE的合并过程中，ZooKeeper也不会进行任何实质性的数据传输，所有的合并操作，最终都是由**各个副本在本地完成的**。而无论合并动作在哪个副本被触发，都会首先被**转交至主副本**，再由主副本负责**合并计划的制定、消息日志的推送以及对日志接收情况的监控**。

> 在使用副本时，不需要依赖任何集群配置, ReplicatedMergeTree结合ZooKeeper就能完成全部工作。

---
# 分片

通过引入数据副本，虽然能够有效降低数据的丢失风险（多份存储），并提升查询的性能（分摊查询、读写分离），但是仍然有一个问题没有解决，那就是数据表的容量问题。到目前为止，每个副本自身，仍然保存了数据表的全量数据。所以在业务量十分庞大的场景中，依靠副本并不能解决单表的性能瓶颈。想要从根本上解决这类问题，需要借助另外一种手段，即进一步将**数据水平切分**，也就是我们将要介绍的数据分片。

对于一个完整的方案来说，还需要考虑数据在写入时，如何被**均匀地写至各个shard**，以及数据在查询时，如何**路由到每个shard**，并组合成结果集。所以，ClickHouse的数据分片需要结合Distributed表引擎一同使用

Distributed表引擎自身**不存储任何数据**，它能够作为分布式表的一层**透明代理**，在集群内部自动开展数据的写入、分发、查询、路由等工作。


集群配置支持自定义分片和副本的数量，这种形式需要使用shard标签代替先前的node，除此之外的配置完全相同。在这种自定义配置的方式下，分片和副本的数量完全交由配置者掌控。其中，shard表示逻辑上的数据分片，而物理上的分片则用replica表示。如果在1个shard标签下定义N(N>=1)组replica，则该shard的语义表示1个分片和N-1个副本。

从上面的配置信息中能够得出结论，集群中replica数量的上限是由ClickHouse节点的数量决定的，例如为了部署集群sharding_ha，需要4个ClickHouse服务节点作为支撑

不知道大家是否还记得，在前面介绍数据副本时为了创建多张副本表，我们需要分别登录到每个ClickHouse节点，在它们本地执行各自的CREATE语句。这是因为在默认的情况下，CREATE、DROP、RENAME和ALTER等DDL语句并不支持分布式执行。而在加入集群配置后，就可以使用新的语法实现分布式DDL执行了

在默认情况下，分布式DDL在ZooKeeper内使用的根路径为：`/clickhouse/task_queue/ddl`。该路径由config.xml内的distributed_ddl配置指定

在此根路径之下，还有一些其他的监听节点，其中包括/query-[seq]，其是DDL操作日志，每执行一次分布式DDL查询，在该节点下就会新增一条操作日志，以记录相应的操作指令。当各个节点监听到有新日志加入的时候，便会响应执行。DDL操作日志使用ZooKeeper的持久顺序型节点，每条指令的名称以query-为前缀，后面的序号递增

## 执行流程
- （1）推送DDL日志：首先在CH5节点执行CREATE TABLE ON CLUSTER，本着谁执行谁负责的原则，在这个案例中将会由CH5节点负责创建DDLLogEntry日志并将日志推送到ZooKeeper，同时也会由这个节点负责监控任务的执行进度。
- （2）拉取日志并执行：CH5和CH6两个节点分别监听/ddl/query-0000000064日志的推送，于是它们分别拉取日志到本地。首先，它们会判断各自的host是否被包含在DDLLog-Entry的hosts列表中。如果包含在内，则进入执行流程，执行完毕后将状态写入finished节点；如果不包含，则忽略这次日志的推送。
- （3）确认执行进度：在步骤1执行DDL语句之后，客户端会阻塞等待180秒，以期望所有host执行完毕。如果等待时间大于180秒，则会转入后台线程继续等待（等待时间由distributed_ddl_task_timeout参数指定，默认为180秒）

对于分布式表与本地表之间表结构的一致性检查，**Distributed表引擎采用了读时检查的机制，这意味着如果它们的表结构不兼容，只有在查询时才会抛出错误**，而在创建表时并不会进行检查。不同ClickHouse节点上的本地表之间，使用不同的表引擎也是可行的，但是通常不建议这么做，保持它们的结构一致，有利于后期的维护并避免造成不可预计的错误。

> 查时检查

Distributed表引擎的定义形式如下所示：
`ENGINE = Distributed(cluster, database, table [,sharding_key])`
其中，各个参数的含义分别如下：
- cluster：集群名称，与集群配置中的自定义名称相对应。在对分布式表执行写入和查询的过程中，它会使用集群的配置信息来找到相应的host节点。
- database和table：分别对应数据库和表的名称，分布式表使用这组配置映射到本地表。
- sharding_key：分片键，选填参数。在数据写入的过程中，分布式表会依据分片键的规则，将数据分布到各个host节点的本地表。


在上面的语句中使用了ON CLUSTER分布式DDL，这意味着在集群的每个分片节点上，都会创建一张Distributed表，如此一来便可以从其中任意一端发起对所有分片的读、写请求

## 分片权重
在集群的配置中，有一项weight（分片权重）的设置

```
 <shard><!-- 分片 -->
        <weight>10</weight><!-- 分片权重 -->
            ……
 </shard>
```

## slot（槽）
slot可以理解成许多小的水槽，如果把数据比作是水的话，那么数据之水会顺着这些水槽流进每个数据分片。slot的数量等于所有分片的权重之和，假设集群sharding_simple有两个Shard分片，第一个分片的weight为10，第二个分片的weight为20，那么slot的数量则等于30。slot按照权重元素的取值区间，与对应的分片形成映射关系。在这个示例中，如果slot值落在[0,10)区间，则对应第一个分片；如果slot值落在[10,20]区间，则对应第二个分片。

## 选择函数
选择函数用于判断一行待写入的数据应该被写入哪个分片，整个判断过程大致分成两个步骤：
（1）它会找出slot的取值，其计算公式如下：
`slot = shard_value % sum_weight`
（2）基于slot值找到对应的数据分片。

## 写入
在向集群内的分片写入数据时，通常有两种思路：

- 一种是借助外部计算系统，事先将数据均匀分片，再借由计算系统直接将数据写入ClickHouse集群的各个本地表

    上述这种方案通常拥有更好的写入性能，因为分片数据是被并行点对点写入的。但是这种方案的实现主要依赖于外部系统，而不在于ClickHouse自身

- 第二种思路是通过Distributed表引擎代理写入分片数据的，接下来开始介绍数据写入的核心流程。

    在这种实现方式下，即使本地表不使用ReplicatedMergeTree表引擎，也能实现数据副本的功能。Distributed会同时负责分片和副本的数据写入工作，而副本数据的写入流程与分片逻辑相同

## 将数据写入分片的核心流程
1.在第一个分片节点写入本地分片数据

执行之后分布式表主要会做两件事情：

- 第一，根据分片规则划分数据，在这个示例中，30会归至分片1，而10、200和55则会归至分片2；
- 第二，将属于当前分片的数据直接写入本地表test_shard_2_local

2.第一个分片建立远端连接，准备发送远端分片数据

3.第一个分片向远端分片发送数据。其中，每份目录将会由独立的线程负责发送，数据在传输之前会被压缩。

4.第二个分片接收数据并写入本地

5.由第一个分片确认完成写

Distributed表**负责所有分片的写入工作**。本着谁执行谁负责的原则，在这个示例中，由CH5节点的分布式表负责切分数据，并向所有其他分片节点发送数据。

在由Distributed表负责向远端分片发送数据时，有**异步写和同步写**两种模式：

- 如果是异步写，则在Distributed表写完本地分片之后，INSERT查询就会返回成功写入的信息；
- 如果是同步写，则在执行INSERT查询之后，会等待所有分片完成写入。

使用何种模式由insert_distributed_sync参数控制，默认为false，即异步写。如果将其设置为true，则可以一进步通过insert_distributed_timeout参数控制同步等待的超时时间。

## 副本复制数据的核心流程

### 通过Distributed复制数据

建表之后，向Distributed表写入数据，它会负责将数据写入集群内的每个replica。

细心的朋友应该能够发现，在这种实现方案下，Distributed节点需要同时负责分片和副本的数据写入工作，它很有可能会成为写入的单点瓶颈，所以就有了接下来将要说明的第二种方案。

### 通过ReplicatedMergeTree复制数据
如果在集群的shard配置中增加internal_replication参数并将其设置为true（默认为false），那么Distributed表在该shard中只会选择一个合适的replica并对其写入数据。此时，如果使用ReplicatedMergeTree作为本地表的引擎，则在该shard内，多个replica副本之间的数据复制会交由ReplicatedMergeTree自己处理，不再由Distributed负责，从而为其减负。

在shard中选择replica的算法大致如下：首选，在ClickHouse的服务节点中，拥有一个全局计数器errors_count，当服务出现任何异常时，该计数累积加1；接着，当一个shard内拥有多个replica时，选择errors_count错误最少的那个。

---
# 分布式查询的核心流程

与数据写入有所不同，在面向集群查询数据的时候，只能通过Distributed表引擎实现。当Distributed表接收到SELECT查询的时候，它会依次查询每个分片的数据，再合并汇总返回。

在查询数据的时候，如果集群中的一个shard，拥有多个replica，那么Distributed表引擎需要面临**副本选择**的问题。它会使用负载均衡算法从众多replica中选择一个，而具体使用何种负载均衡算法，则由load_balancing参数控制

`load_balancing = random/nearest_hostname/in_order/first_or_random`

有如下四种负载均衡算法：

- random是默认的负载均衡算法，正如前文所述，在ClickHouse的服务节点中，拥有一个全局计数器errors_count，当服务发生任何异常时，该计数累积加1。而random算法会选择errors_count错误数量最少的replica，如果多个replica的errors_count计数相同，则在它们之中随机选择一个。

- nearest_hostname可以看作random算法的变种，首先它会选择errors_count错误数量最少的replica，如果多个replica的errors_count计数相同，则选择集群配置中host名称与当前host最相似的一个。而相似的规则是以当前host名称为基准按字节逐位比较，找出不同字节数最少的一个

- in_order同样可以看作random算法的变种，首先它会选择errors_count错误数量最少的replica，如果多个replica的errors_count计数相同，则按照集群配置中replica的定义顺序逐个选择。

- first_or_random可以看作in_order算法的变种，首先它会选择errors_count错误数量最少的replica，如果多个replica的errors_count计数相同，它首先会选择集群配置中第一个定义的replica，如果该replica不可用，则进一步随机选择一个其他的replica。

分布式查询与分布式写入类似，同样本着谁执行谁负责的原则，它会由接收SELECT查询的Distributed表，并负责串联起整个过程。首先它会将针对分布式表的SQL语句，按照分片数量将查询**拆分成若干个针对本地表的子查询，然后向各个分片发起查询，最后再汇总各个分片的返回结果**。

如果在分布式查询中使用子查询，可能会面临两难的局面: IN查询的子句应该使用本地表还是分布式表？（使用JOIN面临的情形与IN类似）。

因此可以得出结论，在**IN查询子句使用分布式表**的时候，查询请求会被放大N的平方倍，其中N等于集群内分片节点的数量，假如集群内有10个分片节点，则在一次查询的过程中，会最终导致100次的查询请求，这显然是不可接受的。

可以看到，在使用GLOBAL修饰符之后，ClickHouse使用**内存表临时保存了IN子句查询到的数据**，并将其**发送到远端分片节点**，以此到达了**数据共享的目的**，从而避免了查询放大的问题。由于数据会在网络间分发，所以需要特别注意临时表的大小，IN或者JOIN子句返回的数据不宜过大。如果表内存在重复数据，也可以事先在子句SQL中增加DISTINCT以实现去重。


---

# 问题

Q: 重复执行同一个插入语句，发现在ReplicatedMergeTree表，没有生效？是因为insert block hash 一致。则不同步？

A: 2021.04.07 06:34:35.392136 [ 102 ] {800bf2f5-9794-4671-a034-f6f907f3789e} <Information> company_db.events (Replicated OutputStream): Block with ID 20210102_4590586592883310685_4443160467449148857 already exists; ignoring it.

---
# ClickHouse复制表、分布式表机制与使用方法
- [百分点大数据技术团队：ClickHouse国家级项目最佳实践](https://www.jiqizhixin.com/articles/2020-05-06-5)

internal_replication =true 这个参数和数据的写入，自动复制相关。从生产环境角度考虑，我们都是复制表，通过本地表写入，这里配置true就好。不推荐也不需要考虑其他情况。

将internal_replication设置为true，这种配置下，写入不需要通过分布式表，而是将数据直接写入到每个shard内任意的一个本地表中

我们只借助于分布式表提供分布式查询能力，与数据写入无关，类似创建DB的View命令，所以这里只需要在提供查询入口的机器上创建，并不一定在所有机器上创建。

实际生产运维中，我们并不推荐集群指令的方式，建议通过运维的方式，从管理规范上，准备日常维护的批量脚本，，配置文件的分发和命令的执行，从操作机上，使用脚本批量远程登陆执行。

禁止分布式写入，采用本地表写入。

禁止使用的原因是需要设计及减少Part的生成频率。这对整个集群的稳定性和整体性能有着决定的作用。这个在之前我司的分享中曾经介绍过。我们控制批次的上线和批次的时间窗口。保障写入操作对每个节点的稳定压力。

这里也分享下我们在做评估写入稳定性测试的结果，作为大家可借鉴的评估思路。其本质是平衡好合并速度和Part数量的关系，一定是需要相对均衡的。

（1） 写本地表

数据写入时，可以由客户端控制数据分布，直接写入集群中ClickHouse实例的本地表。也可以通过LB组件（如LVS，Nginx）进行控制。

（2） 写分布式表

数据写入时，先写入集群中的分布式表下的节点临时目录，再由分布式表将Insert语句分发到集群各个节点上执行，分布式表不存储实际数据。

ClickHouse在分布式写入时，会根据节点数量在接收请求的节点的下创建集群节点的临时目录，数据（Insert语句）会优先提交的本地目录下，之后同步数据到对应的节点。此过程好处是提交后，数据不会丢失。我们模拟同步过程中节点异常，重启后数据也会自动恢复。如果你的数据量及集群压力并不大，分布式也可以认为是一种简单的实现方式。

（3） 写入副本同步

在集群配置中，shard标签里面配置的replica互为副本。将internal_replication设置成true，此时写入同一个shard内的任意一个节点的本地表，zookeeper会自动异步的将数据同步到互为副本的另一个节点。

ClickHouse的JDBC客户端是通过HTTP的方式与ClickHouse进行交互的。我们可以判断场景的可以基于HTTP协议做负载均衡，路由的中间件是可以满足需求的。这样我们的选择其实就有很多了。基于传统运维常见中间件的如：LVS,Nginx，HAProxy都有相关的能力。这里我们选用了Nginx。

同时我们发现社区目前也提供了CHProxy作为负载均衡和HTTP代理。从我们角度更愿意选择一个简单，熟悉的。

我们基于它实现2个目的：（1）、负载均衡能力（2）、采集请求响应日志。

大家可能奇怪第2个目的，ClickHouse本身有自己的查询响应日志，为啥还要单独采集。原因很简单，我们把ClickHouse本身的日志定位为做具体问题，排查与分析的日志，日志分散在了集群内部，并且分布式的查询转换为本地SQL后作为集群的系统行监测，我们认为并不合适。我们通过Nginx日志分析线上业务的请求情况，并进行可视化展现包括业务使用情况，慢查询，并发能力等等，如果确实有需要追溯的场景时候，才会使用到ClickHouse的自身日志。

需要注意的是，我们只针对提供查询入口的实例配置分布式表，然后通过Nginx进行代理。由Nginx将请求路由到代理的ClickHouse实例，这样既将请求分摊开，又避免了单点故障，同时实现了负载均衡和高可用。并且我们在生产环境中也根据不同的业务配置路由入口，实现访问的业务和负载隔离。

Nginx转发后的节点（根据负载配置多个），使用Distribute表引擎作为集群的统一访问入口，当客户端查询分布式表时，ClickHouse会将查询分发到集群中各个节点上执行，并将各个节点的返回结果在分布式表所在节点上进行汇聚，将汇聚结果作为最终结果返回给客户端。

---
# ClickHouse复制表、分布式表机制与使用方法

- [ClickHouse复制表、分布式表机制与使用方法](https://www.jianshu.com/p/ab811cceb856)

##　Replicated Table & ReplicatedMergeTree Engines

ClickHouse的副本机制之所以叫“复制表”，是因为它工作在表级别，而不是集群级别（如HDFS）。也就是说，用户在创建表时可以通过指定引擎选择该表是否高可用，每张表的分片与副本都是互相独立的。

ReplicatedMergeTree引擎族在ZK中存储大量数据，包括且不限于表结构信息、元数据、操作日志、副本状态、数据块校验值、数据part merge过程中的选主信息等等。可见，ZK在复制表机制下扮演了元数据存储、日志框架、分布式协调服务三重角色，任务很重，所以需要额外保证ZK集群的可用性以及资源（尤其是硬盘资源）。


## Distributed Table & Distributed Engine

ClickHouse分布式表的本质并不是一张表，而是一些本地物理表（分片）的分布式视图，本身并不存储数据。

支持分布式表的引擎是Distributed，建表DDL语句示例如下，_all只是分布式表名比较通用的后缀而已。

在分布式表上执行查询的流程简图如下所示。发出查询后，各个实例之间会交换自己持有的分片的表数据，最终汇总到同一个实例上返回给用户。

而在写入时，我们有两种选择：一是写分布式表，二是写underlying的本地表。孰优孰劣呢？

直接写分布式表的优点自然是可以让ClickHouse控制数据到分片的路由，缺点就多一些：

- 数据是先写到一个分布式表的实例中并缓存起来，再逐渐分发到各个分片上去，实际是双写了数据（写入放大），浪费资源；
- 数据写入默认是异步的，短时间内可能造成不一致；
- 目标表中会产生较多的小parts，使merge（即compaction）过程压力增大。

相对而言，直接写本地表是同步操作，更快，parts的大小也比较合适，但是就要求应用层额外实现sharding和路由逻辑，如轮询或者随机等。

应用层路由并不是什么难事，所以如果条件允许，在生产环境中总是推荐写本地表、读分布式表。

## ZooKeeper
千万要调教好ZooKeeper集群，一旦ZK不可用，复制表和分布式表就不可用了。ZK的数据量基本上与CK的数据量成正相关，所以一定要配置自动清理：

```
autopurge.purgeInterval = 1
autopurge.snapRetainCount = 5
```

另外，ZK的log文件和snapshot文件建议分不同的盘存储，尽量减少follower从leader同步的磁盘压力，且余量必须要留足，毕竟硬盘的成本不算高。

- [ClickHouse Better Practices](https://www.jianshu.com/p/363d734bdc03)


```sql
SELECT
    brand_id,
    countDistinct(ad_id) AS cnt
FROM ad_aggs_outer_dis_all
GROUP BY brand_id
ORDER BY cnt DESC
LIMIT 10
-- 10 rows in set. Elapsed: 2.098 sec. Processed 23.03 million rows, 276.40 MB (10.98 million rows/s., 131.76 MB/s.)


SELECT
    brand_id,
    countDistinct(ad_id) AS cnt
FROM ad_aggs_outer
GROUP BY brand_id
ORDER BY cnt DESC
LIMIT 10

-- 10 rows in set. Elapsed: 1.451 sec. Processed 23.03 million rows, 276.40 MB (15.88 million rows/s., 190.53 MB/s.)

```


