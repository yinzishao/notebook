# 多表查询
- 当两表关联查询只需要从左表出结果时，建议用IN而不是JOIN，即写成SELECT ... FROM left_table WHERE join_key IN (SELECT ... FROM right_table)的风格。

- 不管是LEFT、RIGHT还是INNER JOIN操作，小表都必须放在右侧。因为CK默认在大多数情况下都用hash join算法，左表固定为probe table，右表固定为build table且被广播。

- CK的查询优化器比较弱，JOIN操作的谓词不会下推，因此一定要先做完过滤、聚合等操作，再在结果集上做JOIN。这点与我们写其他平台SQL语句的习惯很不同，初期尤其需要注意。

- 两张分布式表上的IN和JOIN之前必须加上GLOBAL关键字。如果不加GLOBAL关键字的话，每个节点都会单独发起一次对右表的查询，而右表又是分布式表，就导致右表一共会被查询N2次（N是该分布式表的shard数量），这就是所谓的查询放大，会带来不小的overhead。加上GLOBAL关键字之后，右表只会在接收查询请求的那个节点查询一次，并将其分发到其他节点上。

- [ClickHouse Better Practices](https://www.jianshu.com/p/363d734bdc03)

# version

ClickHouse LTS 版本的发布规则是:

- 每半年发布一次 LTS 大版本;
- 在上一个 LTS 半年后，选择当时至少被一个大客户使用过的 stable 版本作为新的 LTS 版本。

LTS 版本的小版本升级只会包含 Bug fix 和 Backports，所以稳定性会大大提升。


针对不同的用户群体，ClickHouse 现在提供了不同的发布版本供选择。

- 如果你是稳定性优先的用户，可以选择 LTS 版本；
- 如果你是新特性优先的用户，使用普通的 stable 版本即可。

- [ClickHouse 的 LTS 版本是什么?](https://cloud.tencent.com/developer/article/1690233)
- [clickhouse-lts](https://repo.yandex.ru/clickhouse/deb/lts/main/)


---

# update后实时

更新后通过final进行获取实时数据。

Q: 更新过程中，进行并发查询会怎么样？final会相互阻塞查询吗？final会阻塞写吗？

- [handling-real-time-updates-in-clickhouse](https://altinity.com/blog/2020/4/14/handling-real-time-updates-in-clickhouse)

---
# PREWHERE 子句

- [prewhere-clause](https://clickhouse.tech/docs/en/sql-reference/statements/select/prewhere/)
使用PREWHERE时，首先只读取执行PREWHERE所需的列。然后读取运行查询所需的其他列，但仅读那些 PREWHERE 表示为真实的block。

如果查询中的少数列使用过滤条件，但提供强大的数据过滤，则使用 PREWHERE 是有意义的。这减少了要读取的数据量。

例如，为**提取大量列**但**只对少数列进行过滤**的查询编写PREWHERE非常有用

> 指的是**提取**大量的列的过滤页。对同样是过滤条件的列是没有帮助的？

---
与WHERE子句的意思相同。主要不同在于表数据的读取；PREWHERE 仅支持*MergeTree系列引擎

使用PREWHERE，只读取PREWHERE表达式中需要的列，根据PREWHERE执行的结果读取其他需要的列。

如在过滤条件中有少量不适合索引过滤的列，但它们又可提供很强的过滤能力，使用PREWHERE很有意义，帮助减少数据的读取。

例如，在一个需要提取大量列的查询中为少部分列编写PREWHERE是很有作用的。

1. 在一个查询中可以同时指定PREWHERE和WHERE，在这种情况下，PREWHERE优先于WHERE执行。

2. PREWHERE不适合用于已经存在于索引中的列：列已经存在于索引中，只有满足索引的数据块才会被读取。

3. 如将'optimize_move_to_prewhere'设置为1，并且在查询中不包含PREWHERE，则系统将自动的把适合PREWHERE表达式的部分从WHERE中抽离到PREWHERE中。

> 也就是能通过prewhere先根据条件的找出符合条件的列块，然后再去找其他列的块并根据prewhere条件进行过滤。prewhere f1 = 0 where f2 = 1

- [clickHouse之SQL语法之select（—）](https://blog.csdn.net/ma15732625261/article/details/86600106)
- [ClickHouse源码阅读](https://blog.csdn.net/B_e_a_u_tiful1205/article/details/104226269)

---
# 插入

插入的姿势，不应该频繁插入。会导致太多的分区。

你不应该每秒发送太多的insert语句。理想情况下-每秒/几秒钟插入一次。

因此，您可以每秒插入100K行，但只能使用一个大容量insert语句。当您每秒向*MergeTree表发送数百或数千条insert语句时，总会遇到一些错误，并且无法通过调整某些设置来更改它。

如果不能在外部将大量插入合并到一个大容量insert语句中，那么应该在*MergeTree table之前创建缓冲区表（Buffer table）。

ClickHouse在后台将这些较小的部分合并为较大的部分。它根据一定的规则选择要合并的部分。合并两个（或多个）部件后，将创建一个更大的部件，并将旧部件排队等待删除。您列出的设置允许微调合并部件的规则。合并过程的目标是为每个分区保留一个大的部分（或者每个分区保留几个不值得合并的大部分，因为它们太大）

预期的速度是：每1-2秒插入一次，每个插入包含10K-500K行数据。

后台合并的速度通常取决于存储速度、使用的压缩设置和mergetree选项，即合并算法-普通合并/聚合/求和/折叠等以及使用的排序键。

### 合并频率

无法控制。没有间隔。

不应依赖合并过程。它有自己复杂的算法来平衡parts数量。Merge并没有做最终合并的目标——合成一个parts，因为这样做效率不高，而且会浪费磁盘I/O和CPU。

您可以使用“optimize table xxx final”命令调用未计划的强制合并。 (好像加上final才起作用)

> 分区合并的过程。写入后的10～15分钟后台触发合并任务。合并后，并没有立刻删除，而会留存一段时间（8分钟），查询时自动过滤掉。但去重树好像没有达到相应的量级隔了很久的时间也没有进行合并。

- [分区目录的合并过程](./ClickHouse原理解析与应用.md#6.2.3分区目录的合并过程)

### final

可以通过final获取最新的行，它的工作方式类似于按主键分组以获得行的最新变体，但是工作速度明显慢于常规选择。

参考链接：

- [DB::Exception: Too many parts (600). Merges are processing significantly slower than inserts](https://github.com/ClickHouse/ClickHouse/issues/3174)
- [写入的详细说明](https://github.com/ClickHouse/ClickHouse/issues/3174#issuecomment-423435071)
- [Clickhouse - How often clickhouse triggers a merge operation and how to control it?](https://stackoverflow.com/a/62521478)
- [Best practice for single value update](https://github.com/ClickHouse/ClickHouse/issues/1661)


---
# ClickHouse 数据压缩与解压

那么为什么LZ4解压缩成为一个瓶颈呢？LZ4看起来是一种非常轻的算法:数据解压缩速率通常是每个处理器内核1到3 GB/s，具体取决于数据。这比典型的磁盘子系统快得多。此外，我们使用所有可用的中央处理器内核，解压缩在所有物理内核之间线性扩展。

首先，如果数据压缩率很高，则磁盘上数据占用空间就很小，在读取数据时磁盘IO会比较低，但是如果待解压的数据量很大则会影响到CPU使用率。在LZ4的情况下，解压缩数据所需的工作量几乎与解压缩数据本身的量成正比；其次，如果数据被缓存，你可能根本不需要从磁盘读取数据。可以依赖页面缓存或使用自己的缓存。缓存在面向列的数据库中更有效，因为只有经常使用的列保留在缓存中。这就是为什么LZ4经常成为CPU负载的瓶颈。

- [ClickHouse 在趣头条的实践](https://mp.weixin.qq.com/s/lP9quNJuhpXHxP-n8W0maw)
- [ClickHouse 数据压缩与解压](https://knifefly.cn/2019/08/25/ClickHouse%E5%8E%8B%E7%BC%A9%E4%B8%8E%E8%A7%A3%E5%8E%8B/)
- [How to speed up LZ4 decompression in ClickHouse](https://habr.com/en/company/yandex/blog/457612/)
- [压缩算法.md](../压缩算法.md)


---
# 如何进行分区的覆盖的

## 背景
更新场景，但是更新的效率不高，所以每天会进行全量复制的更改

## 问题

如果直接drop掉分区，后写入。会在当前写入进度中导致数据查询的异常

## 解决办法

通过影子表的方式进行分区覆盖

1. 创建一个结构一样的影子表
2. 往影子表进行数据的写入
3. 写入完成后，通过replace partition操作进行数据的替换
4. 删除旧分区的数据。如果需要保存旧的状态表，进行数据归档和淘汰策略。


---
# 分片与复制

需要提醒一下，每个clickhouse-server实例只能放一个分片的一个备份，也就是3分片2备份需要6台机器（6个不同的clickhouse-server）。

之前为了节省资源，打算循环使用，把shard1的两个副本放到hadoop1、hadoop2两个机器上，shard2的两个副本放到hadoop2、hadoop3上，shard3的两个副本放到hadoop3、hadoop1上，结果是不行的。

原因是shard+replica对应一个数据表，Distributed查询规则是每个shard里找一个replica，把结果合并。

## 禁止分布式写入，采用本地表写入。

社区很多伙伴在分享时，也都提到了禁止使用分布式表写入。我们也一样。

禁止使用的原因是需要 设计及减少Part的生成频率。这对整个集群的稳定性和整体性能有着决定的作用。这个在之前我司的分享中曾经介绍过。我们控制批次的上线和批次的时间窗口。保障写入操作对每个节点的稳定压力。

- [insert data via the distributed table or local table](https://github.com/ClickHouse/ClickHouse/issues/1854#issuecomment-363197252)

原因：
- 它更有效，因为它避免了临时数据的过度复制。
- 它更灵活，因为您可以使用任何复杂的切分模式，而不仅仅是简单的按除法模进行的切分。
注意事项：
- 插入到本地表需要客户机应用程序上更多的逻辑，并且可能更难使用。但它在概念上更简单。
- 如果您的查询依赖于一些关于数据分布的假设，比如使用IN或JOIN（连接同一位置的数据）而不是GLOBAL IN、GLOBAL JOIN的查询，那么您必须自己维护正确性。

### 写分布式表

数据写入时，先写入集群中的分布式表下的节点临时目录，再由分布式表将 Insert 语句分发到集群各个节点上执行，分布式表不存储实际数据。

ClickHouse 在分布式写入时，会根据节点数量在接收请求的节点的下创建集群节点的临时目录，数据（Insert 语句）会优先提交的本地目录下，之后同步数据到对应的节点。此过程好处是提交后，数据不会丢失。我们模拟同步过程中节点异常，重启后数据也会自动恢复。如果你的数据量及集群压力并不大，分布式也可以认为是一种简单的实现方式。


- [Clickhouse集群应用、分片、复制](https://www.jianshu.com/p/20639fdfdc99)
- [百分点大数据技术团队：ClickHouse国家级项目最佳实践](http://blog.itpub.net/69965230/viewspace-2690052/)
- [ClickHouse万亿数据双中心的设计与实践](https://cloud.tencent.com/developer/article/1530809)


---
# Maximum QPS for key value lookups

- [Maximum QPS for key-value lookups](https://altinity.com/blog/clickhouse-in-the-storm-part-2)

正如您所看到的，“fs12M”比“int20M”更倾向于使用一个更低的索引粒度，因为键更大，涉及到更多的列（包括一个相当大的字符串）。

- 对于fs12M，最好的QPS性能使索引粒度达到64和128
- 对于int20M–128和256。

如我们所料，查找“fs12”比查找“int20M”慢。使用PREWHERE而不是WHERE会带来显著的改进。

通过使用未压缩的缓存，可以提高小查询的性能。ClickHouse通常不缓存数据，但对于快速简短的查询，可以保留未压缩数据块的内部缓存。它可以通过配置文件级别的“use_uncompressed_cache”设置来打开。默认缓存大小为8GB，但可以增加。

启用use_uncompressed_cache可提供高达50%的改进。也就是说，对于“int20M”单次命中的情况，它的影响较小，因为在所有测试的案例中它已经非常快了。

但是如果QPS还不够呢？ClickHouse能做得更好吗？当然可以，但我们必须切换到另一种数据结构，以确保数据总是在内存中。ClickHouse有几个选项：我们将尝试外部字典和Join引擎。

词典通常用于与外部数据集成。请参阅我们关于这个主题的博客文章。然而，字典也可以用来为已经存储在ClickHouse中的数据建立内存缓存。

不幸的是，用FixedString键创建字典目前是不可能的，所以我们只测试'int20M'情况。

如果你不需要经常更新词典，那么字典就可以很好地工作。是否需要定期更新源字典中的源字典；是否需要定期更新源字典。有时可能不方便。另一个不便之处是XML配置。应该很快用dictionary ddl来解决这个问题，但目前我们必须坚持使用XML。

ClickHouse在内部使用联接表引擎来处理SQL联接。但是可以显式地创建这样一个表

之后，您可以像插入任何其他表一样插入该表中。理想情况下，您可以用一个INSERT填充整个表，但也可以分部分完成（但最好还是使用足够大的部分，不要太多的部分）。联接表保存在**内存中（就像字典一样，但更紧凑一点），并且还刷新在磁盘上。并且服务器重启后会自动恢复**。

不可能直接查询联接表；始终需要将其用作联接的正确部分。有两个选项可以从联接表中提取数据。第一个类似于使用joinGet函数的字典语法（它是由一个贡献者添加的，从18.6开始就可以使用）。或者你可以做一个真正的联合系统1表格）

当每次查找都需要执行大量joinGet调用时，“fs12M”可以清楚地看到joinGet和real join之间的区别。当你只需要打一次电话-没有区别。

**与字典相比，Join table的性能稍差。但是它更容易维护，因为它已经在数据库模式中了。与字典相比，连接使用更少的内存，并且可以轻松地添加新数据等等。不幸的是，更新是不可能的。**

## 总结

- ClickHouse不是一个键值数据库（惊喜！🙂 )
- 如果您需要在clickhouse中模拟键值查找场景，那么Join引擎和字典将提供最佳性能
- 如果每秒有大量查询，则禁用日志（或降低日志级别）可以提高性能
- 启用未压缩缓存有助于提高选择性能（对于“小”选择，返回很少的行）。最好只对特定的选择和特定的用户配置文件启用它
- 在高并发情况下使用max_thread=1
- 尽量保持同时连接的数量足够小，以获得最大的QPS性能。具体数字当然取决于硬件。使用我们的低端机器进行测试，16-32范围内的连接显示出最佳的QPS性能
- index_granularity=256看起来是UInt64键的键值类型方案的最佳选项，对于FixedString（16）键，还应考虑index_granularity=128。
- 使用PREWHERE而不是WHERE进行点查找。

ClickHouse不是一个键值存储，但是我们的结果证实了ClickHouse在不同并发级别的高负载下表现稳定，它能够在MergeTree表（当数据在文件系统缓存中时）上每秒大约4K次的查找，或者使用字典或连接引擎进行高达10K的查找。当然，在更好的硬件上你会有更好的数字。

这些结果与键值数据库（如Redis，在同一硬件上提供大约125K个QPS）相差甚远，但在某些情况下，即使这样的QPS速率也可以令人满意。例如，在通过复杂的OLAP计算实时创建的数据中进行基于id的查找/按id从物化视图中提取一些聚合等。当然，ClickHouse可以水平和垂直缩放。

---
# Maximum QPS estimation

- 在每个场景中，QPS在该计算机上的最大值为8到64个并发连接。
- 在启用keepalive和禁用日志的情况下，最大吞吐量约为97K QPS。
- 在启用日志的情况下，它大约慢了30%，并提供了大约71K个QPS。
- 这两个no keepalive变体都要慢得多（大约18.5kqps），甚至日志开销在这里也看不到。这是意料之中的，因为使用keepalive ClickHouse当然可以处理更多的ping，这要归功于跳过为每个请求建立连接的额外成本。

本机协议显示出比http更糟糕的性能，这可能令人惊讶，但实际上它是意料之中的：本机TCP/IP更复杂，并且有许多额外的协议特性。它不适合高QPS，而是用于来回传输大数据块。

此外，当native client中的并发性增加时，QPS会有相当大的降低，并发级别更高（>3000）。此时，系统将变得无响应并且不返回任何结果。最有可能的原因是clickhouse基准工具为每个连接使用一个单独的线程，而线程和上下文切换的数量对于系统来说太多了。

预期延迟会随着并发性的增加而降低。从目前来看，它看起来非常好：如果并发用户少于256个，则可以预期延迟低于50毫秒。

有趣的是，没有keepalive的http请求表现得非常稳定，即使有2K个并发用户，延迟也低于50ms。如果没有keepalive，延迟会更容易预测，并且stdev随着并发性的增加而保持较小，但是QPS的速率会有所降低。它可能与web服务器的实现细节有关：例如，当每个连接使用一个线程时，线程上下文切换会降低服务器的速度，并在达到某个并发级别后增加延迟。

> keepalive需要线程切换导致的性能损耗

默认情况下，ClickHouse使用多个线程处理更大的查询，以便高效地使用所有CPU核心。然而，如果您有大量并发连接，多线程处理将在上下文切换、重新连接线程和工作同步方面产生额外的成本。

为了测量并发连接和多线程的交互作用，让我们看看在一个综合选择中的不同之处，这个选择可以在默认多线程设置和max_threads=1的情况下找到最多100K个随机数。

结论很简单：为了在高并发情况下实现更高的QPS，使用max_threads=1设置。

- [Maximum QPS estimation](https://altinity.com/blog/clickhouse-in-the-storm-part-1)
