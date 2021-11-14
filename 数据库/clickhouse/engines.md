
# CollapsingMergeTree

- [CollapsingMergeTree官方文档](https://clickhouse.tech/docs/en/engines/table-engines/mergetree-family/collapsingmergetree/)

> 类比拉链表

当ClickHouse合并数据部分时，具有相同排序键（ORDER BY）的每组连续行将减少到不超过两行，一行的符号为1（“state”行），另一行的符号为-1（“cancel”行）。

- 如果“state”和“cancel”行的数目匹配，并且最后一行是“state”行，则显示第一行“cancel”和最后一行“state”。
- 如果“state”行多于“cancel”行。则save最后一个“state”行。
- 如果“cancel”行多于“state”行，则save第一个“cancel”行。
- 在其他情况下，没有一行。

> 指的是插入后，执行optimize table final操作后select的行为。其跟select final是有区别的！

另外，如果“状态”行比“取消”行多出至少2行，或者“取消”行比“状态”行多出至少2行，则**合并将继续**，但ClickHouse将此情况视为逻辑错误并将其记录在服务器日志中。如果同一数据被多次插入，则可能发生此错误。

## 多线程的问题
该sign是必需的，因为合并算法**不能保证具有相同排序键的所有行都在相同的结果数据部分中**，甚至在相同的物理服务器上。ClickHouse进程选择具有**多个线程的查询**，它不能预测结果中的行顺序。如果需要从CollasingMergeTree表中获取完全“折叠”的数据，则**需要进行聚合**。

如果需要在不进行聚合的情况下提取数据（例如，检查是否存在最新值与特定条件匹配的行），可以对FROM子句使用一个final修饰符。这种方法的效率要低得多。

我们使用两个INSERT查询来创建两个不同的数据部分。如果我们用一个查询插入数据，**ClickHouse将创建一个数据部分，并且永远不会执行任何合并**。

> ？： 是说select是在不同的数据部分合并发生才会发生折叠。如果一条语句插入多个相同的主键id会怎么样呢？

SELECT查询是在两个线程中执行的，我们得到了一个随机的行顺序。未发生折叠，因为尚未合并数据部分。ClickHouse在一个我们**无法预测的未知时刻合并数据部分**。

如果我们不需要聚合并且想要强制折叠，我们可以使用FROM子句的FINAL修饰符。这种选择数据的方法效率很低。不要把它用在大表上。




```sql
CREATE TABLE UAct
(
    `UserID` UInt64,
    `PageViews` UInt8,
    `Duration` UInt8,
    `Sign` Int8
)
ENGINE = CollapsingMergeTree(Sign)
partition by (Duration)
ORDER BY UserID

```

```sql
truncate table UAct
INSERT INTO UAct select number, number+1, number, 1 from system.numbers limit 10
INSERT INTO UAct select number, number, number, -1 from system.numbers limit 10
select * from UAct final
optimize table UAct final
select * from UAct
-- 返回空值： 即使非主键列不一样，也是能正常消除
```


```sql
truncate table UAct
INSERT INTO UAct select number, 0, number, 1 from system.numbers limit 10
INSERT INTO UAct select number, 1, number, -1 from system.numbers limit 10
INSERT INTO UAct select number, 2, number, -1 from system.numbers limit 10
select * from UAct final
-- 返回2
optimize table UAct final
select * from UAct
-- 仅仅保留2。因为如果“state”行多于“cancel”行。则save最后一个“state”行。
```

```sql
truncate table UAct
-- 空数据，先删除-1的无用数据
INSERT INTO UAct select number, 0, number, -1 from system.numbers limit 10
INSERT INTO UAct select number, 1, number, 1 from system.numbers limit 10

select * from UAct final order by UserID
-- 返回最后的10行
optimize table UAct final
select * from UAct
-- 但是无法消除无用的数据！如果“state”和“cancel”行的数目匹配，并且最后一行是“state”行，则显示第一行“cancel”和最后一行“state”。
-- 这时候如果是sum(指标*sign)，则是错误数据了
```


```sql
truncate table UAct
-- 同一条语句执行sign一样的。默认保留了最后一条数据。
INSERT INTO UAct values (1, 0, 1, 1), (1, 2, 2, 1);
select * from UAct
-- 同一条语句执行sign不一样的。没有保存任何数据。
INSERT INTO UAct values (1, 0, 1, 1), (1, 2, 2, -1);
-- 同一条语句执行sign不一样的。两行都保存了。
INSERT INTO UAct values (1, 0, 1, -1), (1, 2, 2, 1);
-- 结论： 同一个语句的，按照上面的合并规则先进行合并后存储。
```


所以对于binlog同步折叠树需要注意：select * from table是肯定无法拿到正确的数据的，需要加上final进行获取。因为binlog也是实时同步的，会拿到多行数据。
> 要注意final效率很低，不要在大表且生产环境使用

而如果想通过sum(PageViews * Sign) AS PageViews进行相关数据统计的话。需要建立clickhouse表的时候，需要建立一个**纯净的全量+binlog增量的表**。这个比较难实现。无法拿到全量同步那一刻的增量游标，而只能重复消费binlog游标了。而重复消费的话，会出现问题。具体做法参考： [mysql-snapshots](https://debezium.io/documentation/reference/connectors/mysql.html#mysql-snapshots), 通过锁表进行。

场景如下：binlog的删除操作会应用到clickhouse表中，而clichouse正确是应该没有数据的。虽然对final查询无影响，但是无论optimize但无法消除这些delete的行。对于sum()是一个脏数，影响结果。可能需要程序原始建表、独立控制才能做到纯净的全量同步+增量表。

重复的场景有：ch已删除，binlog再次删除。ch已插入，binlog再次插入。。。

而且在一个更特殊的异常结果中，就更坑了。如果cancel行重复插入多次（>2），即使后面state行正常插入。造成cancel行仍多于state行, state行就消失了！

例子：

```sql
truncate table UAct
-- 空数据，先删除-1的无用数据
INSERT INTO UAct select number, number, number, -1 from system.numbers limit 10
INSERT INTO UAct select number, number, number+10, -1 from system.numbers limit 10

INSERT INTO UAct select number, number+1, number, 1 from system.numbers limit 10
-- 无数据返回！
select * from UAct final
-- 保留第一次出现的cancel行
optimize table UAct final
select * from UAct
```

> 思考： 如何做一个更实时、且完整的mysql到ch的表呢？调研其他cdc工具是怎么做的？！

# MaterializeMySQL

- [materialize-mysql](https://clickhouse.tech/docs/en/engines/database-engines/materialize-mysql/):

使用MySQL中存在的所有表以及这些表中的所有数据创建ClickHouse数据库。 ClickHouse服务器用作MySQL副本。**它读取binlog并执行DDL和DML查询**。 此功能是**实验性的**。

数据复制

MaterialeMysQL不支持直接插入、删除和更新查询。但是，它们在数据复制方面受到支持：

- MySQL INSERT查询被转换为带sign为1的INSERT。

- MySQL DELETE查询转换为INSERT，sign为-1。

- MySQL UPDATE查询被转换成INSERT和INSERT，INSERT的sign为-1，INSERT的sign为1


- [MySQL到ClickHouse的高速公路-MaterializeMySQL引擎](https://bbs.huaweicloud.com/forum/thread-102438-1-1.html): 比较详细的介绍MaterializeMySQL引擎

可以看到：

1. 在DDL转化时默认增加了2个隐藏字段：_sign(-1删除, 1写入) 和 _version(数据版本)
2. 默认将表引擎设置为 ReplacingMergeTree，以 _version 作为 column version
3. 原DDL主键字段 runoob_id 作为ClickHouse排序键和分区键

可以看到，删除id为2的行只是额外插入了_sign == -1的一行记录，并没有真正删掉。

## 日志回放

MySQL 主从间数据同步时Slave节点将 BinLog Event 转换成相应的SQL语句，Slave 模拟 Master 写入。类似地，传统第三方插件沿用了MySQL主从模式的BinLog消费方案，即将 Event 解析后转换成 ClickHouse 兼容的 SQL 语句，然后在 ClickHouse 上执行（回放），但整个执行链路较长，通常性能损耗较大。不同的是，MaterializeMySQL 引擎提供的内部数据解析以及回写方案隐去了三方插件的复杂链路。回放时将 BinLog Event 转换成底层 Block 结构，然后直接写入底层存储引擎，接近于物理复制。此方案可以类比于将 BinLog Event 直接回放到 InnoDB 的 Page 中。

## 同步策略

### 位点同步

v20.9.1版本前是基于位点同步的，ClickHouse每消费完一批 BinLog Event，就会记录 Event 的位点信息到 .metadata 文件:

这样当 ClickHouse 再次启动时，它会把 {‘mysql-bin.000003’, 355005999} 二元组通过协议告知 MySQL Server，MySQL 从这个位点开始发送数据：

如果MySQL Server是一个集群，通过VIP对外服务，MaterializeMySQL创建 database 时 host 指向的是VIP，当**集群主从发生切换后**，{Binlog File, Binlog Position} 二元组不一定是准确的，因为**BinLog可以做reset操作**。

为了解决这个问题，v20.9.1版本后上线了 GTID 同步模式，废弃了不安全的位点同步模式。

### GTID同步

GTID模式**为每个 event 分配一个全局唯一ID和序号，直接告知 MySQL 这个 GTID 即可**，于是.metadata变为:

其中 0857c24e-4755-11eb-888c-00155dfbdec7 是生成 Event的主机UUID，1-783是已经同步的event区间

于是流程变为:

1. ClickHouse 发送 GTID:0857c24e-4755-11eb-888c-00155dfbdec7:1-783 给 MySQL
2. MySQL 根据 GTID 找到本地位点，读取下一个 Event 发送给 ClickHouse
3. ClickHouse 接收 BinLog Event 并完成同步操作
4. ClickHouse 更新 .metadata GTID信息

---

- [ClickHouse实时同步MySQL数据](https://my.oschina.net/u/4788009/blog/4711488): 两个方案：mysql -> canal -> clickhouse流入。通过mysql -> canal -> kafka -> clickhouse流入。
- [clickhouse_sinker](https://github.com/housepower/clickhouse_sinker): kafka -> clickhouse


----

# 物化视图

物化视图存储由相应的 SELECT 查询转换的数据。

一个物化视图的实现是这样的：当向SELECT指定的表插入数据时，插入的部分数据被这个SELECT查询转换，结果插入到视图中。也就是说物化视图创建好之后，如果源表被写入新数据，那么物化视图也会同步更新。

要注意的是： ClickHouse中的物化视图的实现更像是插入触发器。如果视图查询中存在某种聚合，则它仅应用于新插入的一批数据。对源表现有数据的任何更改（如更新、删除、删除分区等）都不会更改物化视图。

SELECT查询可以包含DISTINCT、GROUP BY、ORDER BY、LIMIT…请注意，对插入的**每个数据块分别执行相应的转换**。例如，如果设置了GROUP BY，则数据在插入期间聚合，但仅在插入数据的单个数据包中聚合。数据将不会进一步汇总。例外情况是使用独立执行数据聚合的引擎时，例如SummingMergeTree。

在物化视图上执行ALTER查询有局限性，因此可能不方便。如果物化视图使用[db.]name的构造，则可以DETACH视图，为目标表运行ALTER，然后附加先前detached（DETACH）的视图。

请注意，物化视图受optimize_on_insert设置的影响。数据在插入视图之前被合并。

视图看起来与普通表相同。例如，它们列在SHOW TABLES查询的结果中。

要删除视图，请使用DROP VIEW。尽管DROP TABLE也适用于视图。

- [MATERIALIZED VIEW](https://clickhouse.tech/docs/en/sql-reference/statements/create/view/)
- [joins-in-clickhouse-materialized-views](https://altinity.com/blog/2020-07-14-joins-in-clickhouse-materialized-views):  通过物化视图和join操作，进行实时汇总进汇总表的操作。但是要注意join的一些小陷阱。ClickHouse只触发联接中最左边的表。其他表可以为转换提供数据，但是视图不会对这些表上的插入做出反应。
