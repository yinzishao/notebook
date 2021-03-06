- [表格存储 Tablestore](https://help.aliyun.com/product/27278.html?spm=a2c4g.11186623.6.540.250021afKG2Dmh)
- [从SQL到NoSQL—如何使用表格存储](https://developer.aliyun.com/article/64411?spm=a2c4g.11186623.2.48.71174c0cvqmpm9)
- [通道服务](https://help.aliyun.com/document_detail/102489.html?spm=a2c4g.11186623.6.657.14a1411dR1mwBm)
- [Tablestore 中接入 Data Lake Analytics](https://help.aliyun.com/document_detail/87488.html?spm=a2c4g.11186623.6.748.783374c0uvfBiz)
- [TableStore实战：DLA+SQL实时分析TableStore](https://developer.aliyun.com/article/682842)
- [表格存储TableStore2.0重磅发布，提供更强大数据管理能力](https://developer.aliyun.com/article/692900?spm=a2c6h.14164896.0.0.760953d9OtybIh): 多种数据模型、多元化索引、数据通道
- [blink+tablestore实现无限扩展性，高实时汇总计算及排行榜](https://developer.aliyun.com/article/712582): 流批一体
- [ots](https://blog.csdn.net/weixin_34209406/article/details/90625991)

# 从SQL到NoSQL

 数据库 | 关系型数据库 |	NoSQL
-------- | --- | ----
数据模型    |  关系模型对数据进行了规范化，严格的定义了表、列、索引、表之间的关系及其他数据库元素，使一张数据表的所有数据具有相同的结构。 | 非关系(NoSQL)数据库一般不会对表的结构进行严格的定义，一般使用分区键及键值来检索值、列集或者半结构化数据。
ACID        |   传统关系型数据库支持由 ACID （原子性、一致性、隔离性和持久性）定义的一组属性。其原子性体现在一个事务"全部成功或者全部失败"，即完全执行成功或完全不执行某项事务。一致性表示数据库事务不能破坏关系数据的完整性以及业务逻辑上的一致性。隔离性要求并发事务应分别执行，互不干扰。持久性即一旦事务提交后，它所做的修改将会永久的保存在数据库上，即使出现宕机也不会丢失。 | 为了获得**更为灵活的可水平扩展**的数据模型， NoSQL 数据库通常会**放弃传统关系数据库的部分 ACID 属性**。凭借这些特性，NoSQL数据库可用来克服一系列包括**性能瓶颈、可扩展性、运营复杂性以及不断增加的管理和支持成本**的问题，这也让 NoSQL 数据库成了传统关系型数据库在面临海量数据及高并发挑战时的最佳选择。
性能      |       性能一般取决于磁盘子系统、数据集大小以及查询优化、索引和表结构。 | 写性能通常受限于磁盘子系统，读性能则受限于结果集的大小
扩展      |       进行纵向扩展最简单的方式是使用更快的CPU、磁盘等硬件设备。要获得跨分布式系统的关系表，就需要增加使用成本及技术复杂度。 | 能够利用低成本硬件的分布式集群进行横向扩展，从而在不增加延迟的前提下提高吞吐量和数据规模。
API         |    对存储和检索数据的请求由符合结构化查询语言 (SQL) 的查询来传达。这些查询由关系数据库系统来解析和执行。 | 应用开发人员可以使用NoSQL数据库开放的 API 轻松存储和检索数据。通过分区键及键值，应用可以查找键值对、列集或者半结构化数据。


表格存储（TableStore）是 NoSQL 数据库的一种，提供海量 NoSQL 数据存储错误，支持 schemafree 的数据模型，提供**单行级别的事务**，服务端自动对数据进行**分区和负载均衡**，让单表数据从 GB 到 TB 再到 PB，访问并发从0至百万都无需繁琐的扩容流程，写性能在 TB 及 PB 级数据规模都能保持在**单个毫秒**，读性能只依赖结果数据集，而不受数据量的影响。

所以相比 OLTP（联机事务处理）场景，表格存储更适用于 Web 规模级应用程序，包括社交网络、游戏、媒体共享和 IoT（物联网）、日志监控等场景。

---
# 通道服务

通道服务（Tunnel Service）是基于表格存储数据接口上的全增量一体化服务。通道服务提供了增量、全量、增量加全量三种类型的分布式数据实时消费通道。通过为数据表建立数据通道，您可以简单地实现对表中历史存量和新增数据的消费处理。

表格存储适合元数据管理、时序数据监控、消息系统等服务应用，这些应用通常利用增量数据流或者先全量后增量的数据流来触发一些附加的操作逻辑，这些附加操作包括。
- 数据同步：将数据同步到缓存、搜索引擎或者数据仓库中。
- 事件驱动：触发函数计算、通知消费端消费或者调用一些API。
- 流式数据处理：对接流式或者流批一体计算引擎。
- 数据搬迁：数据备份到OSS、迁移到容量型的表格存储实例等。

---
# Data Lake Analytics

Tablestore 中接入 Data Lake Analytics（简称 DLA）服务的方式，为您提供一种快速的 OLAP（On-Line Analytical Processing） 解决方案。DLA 是阿里云一款通用的 **SQL 查询引擎**，使用通用的 SQL 语言（兼容 MySQL 5.7 绝大部分查询语法）可在 Tablestore 中进行灵活的数据分析。

如架构图所示，OLAP查询架构涉及阿里云DLA、Tablestore 和 OSS 三款产品。

- DLA：负责分布式 SQL 查询计算。在实际运行过程中将 SQL 查询请求进行任务**拆解**，产生若干**可并行化的子任务**，提升数据计算和查询能力。
- Tablestore：数据存储层，用于接收 DLA 的各类子查询任务。如果您在 Tablestore 中已经有**存量数据**，可以直接在 DLA 上建立**映射视图**，从而体验 SQL 计算的便捷服务。
- OSS：分布式对象存储系统，主要用于**保存查询结果**。
