# go
- [go](./go)

## GMP
- [goroutine](./go/goroutine.md)

- [Golang 并发模型之 GMP 浅   尝](https://mp.weixin.qq.com/s/p_7qZH5Ix3vVJEvbPHyMng)
- [30+张图讲解: Golang调度器GMP原理与调度全分析](https://mp.weixin.qq.com/s?__biz=MzAxMTA4Njc0OQ==&mid=2651438895&idx=3&sn=d7328484410c825c6e35b51a324f0c65&chksm=80bb61ddb7cce8cba59349bcae7c067db08e66428650962450cd3a081b9e96fae8db45758087&scene=21#wechat_redirect): 这篇文章讲得很清晰，值得多读。很多点都说到了，M的回收与P的空闲与绑定。 [](#bookmark)
- [单核 CPU，开两个 Goroutine，其中一个死循环，会怎么样？](https://mp.weixin.qq.com/s/h27GXmfGYVLHRG3Mu_8axw): 1.14基于信号的抢占式调度实现原理
- [Golang的GPM 模型在网络编程中存在的问题](https://blog.haohtml.com/archives/30307): 抖动时创建的 goroutine 会进入全局 allgs 数组，该数组不会进行收缩，且每次 gc、sysmon、死锁检查期间都会进行全局扫描。 goroutine-per-connection 模式改IO多路复用。

## 并发
- [并发](./go/并发与锁.md)

- [源码面前无秘密 | Golang标准库 sync.WaitGroup](https://juejin.im/post/6866971615717457934): sync.WaitGroup的源码并不多但会考虑很多并发情况,总体难度适中,很适合go初学者作为go源码阅读的起点.
- [Go 语言标准库中 atomic.Value 的前世今生](https://blog.betacat.io/post/golang-atomic-value-exploration/)
- [Go 标准库源码学习（一）详解短小精悍的 Once](https://mp.weixin.qq.com/s/Lsm-BMdKCKNQjRndNCLwLw): 对once深入理解，提了3点疑问

- [理解真实世界中 Go 的并发 BUG](https://mp.weixin.qq.com/s/EnLxJEoPrASWytmM8jJtmg): 很多真实世界可能会发生的并发BUG，值得参考！

## map
- [go语言中的map实战](https://studygolang.com/articles/560): 并发修改哈希表
- [go sync.Map源码分析](https://juejin.im/post/6844903598317371399): 对比sync.map与concurrent-map
- [深入理解sync.Map](https://my.oschina.net/u/4587630/blog/4408032): 对比java和go的并发hash的标准库的区别
- [Go 1.9 sync.Map揭秘](https://colobu.com/2017/07/11/dive-into-sync-Map/)
- [通过实例深入理解sync.Map的工作原理](https://tonybai.com/2020/11/10/understand-sync-map-inside-through-examples/): 通过实例法，我们大致得到了sync.Map的工作原理和行为特征。read dirty之间的数据行为
- [go基础之map-写在前面（一)](https://mp.weixin.qq.com/s/Aw8AjDmuvf7n7ACWl7mwaw) : 源码，编译原理。相关链接中的文章也较详细。 [抽丝剥茧—Go哈希Map的鬼魅神功](https://mp.weixin.qq.com/s?__biz=MzAxMTA4Njc0OQ==&mid=2651440382&idx=3&sn=2aa006a968994df6027f8e6c5392722a&chksm=80bb1a0cb7cc931a3ce45fb280d0f2e04c9e9032e1b952c42a231688b28740b11fcfff44166f&scene=21#wechat_redirect)
- [1.8 万字详解 Go 是如何设计 Map 的](https://mp.weixin.qq.com/s/OJSxIXH87mjCkQn76eNQsQ): 太详细了，详细到底层分析

## GC
- [浅析 Golang 垃圾回收机制](https://mp.weixin.qq.com/s/LTz8UjCvaxZvAPRqeFCxjQ): 挺清晰的介绍垃圾回收的入门概念
- [GO GC 垃圾回收机制](https://segmentfault.com/a/1190000018161588): 比较概括。
- [图文结合，白话Go的垃圾回收原理](https://juejin.im/post/6882206650875248654): 比较清晰分析各种方法的优缺点，这样做的理由。而且在算法过程方面的讲述比较白话，但是在写屏障的介绍可能有点不好，不过也能让我们知道大概。 [](#bookmark)
- [图解: 宏观角度看 Go 语言如何实现垃圾回收中的 Stop the World](https://mp.weixin.qq.com/s/rt4lxGwaYo8IkTdmo186Cg): 说明stw的简要步骤，并且说明跟系统调用的关系，引出避免长时间的调用。

## chan
- [通道](./go/通道.md)

- [图解Golang channel源码](https://juejin.im/post/6875325172249788429): 主要是围绕着一个环形队列和两个链表展开
- [如何实现一个协程池？](https://github.com/iswbm/GolangCodingTime/blob/master/source/c04/c04_10.rst): 使用通道的实现的方法很值得推敲。
- [如何优雅地关闭Go channel](https://www.jianshu.com/p/d24dfbb33781): 有具体的准则和例子
- [剖析 Golang Context：从使用场景到源码分析](https://xie.infoq.cn/article/3e18dd6d335d1a6ab552a88e8): 比较深入浅出的介绍

## error
- [Go语言中的错误处理（Error Handling in Go）](http://ethancai.github.io/2017/12/29/Error-Handling-in-Go/): 理解goland的错误处理机制。
- [关于 Golang 错误处理的一些思考](https://mp.weixin.qq.com/s?__biz=MzAxMTA4Njc0OQ==&mid=2651441294&idx=3&sn=bb20e907f3886961777c2368e8d05cdd&chksm=80bb167cb7cc9f6a1bca359641a9eaa2316fc57f016ca6cab3cd4f13f101874594c7291b06ee&scene=21#wechat_redirect): 创建错误的形式，处理方法error、xerror，一些提案
- [一套优雅的 Go 错误问题解决方案](https://mp.weixin.qq.com/s/RFF2gSikqXiWXIaOxQZsxQ): 对常见错误处理的简单明了的总结

## 指针

- [深度剖析 Go 的 nil - 掘金](https://juejin.cn/post/6950053304650956807): 对nil值的深入理解！

## 其他
- [[]T 还是 []*T, 这是一个问题](https://colobu.com/2017/01/05/-T-or-T-it-s-a-question/): 只是说明了副本创建的各种情况
- [深度解密Go语言之关于 interface 的10个问题](https://www.cnblogs.com/qcrao-2018/p/10766091.html): 值接收者和指针接收者的区别
- [接口](https://draveness.me/golang/docs/part2-foundation/ch04-basic/golang-interface): 从底层汇编解释接口。eface、iface
- [说说 Go 语言中的空接口](https://github.com/iswbm/GolangCodingTime/blob/master/source/c02/c02_05.rst) 、[2.6 图解: 静态类型与动态类型](https://github.com/iswbm/GolangCodingTime/blob/master/source/c02/c02_06.rst)
- [应用编译，计算机中一定要掌握的知识细节](https://mp.weixin.qq.com/s/YKZ3MJuGVgWJG69WATRPPQ): 预处理、编译、汇编以及链接。go实例分析前三个部分

- [golang中多goroutine操作map时直接赋值不用加锁？](https://github.com/Terry-Mao/gopush-cluster/issues/44): cow和指针赋值不能确保是原子行为 [谈谈go语言编程的并发安全](http://yanyiwu.com/work/2015/02/07/golang-concurrency-safety.html) [copy-on-write技术](https://chunlife.top/2019/09/03/copy-on-write%E6%8A%80%E6%9C%AF/)
- [benchmark 基准测试 | Go 语言高性能编程 | 极客兔兔](https://geektutu.com/post/hpg-benchmark.html)


## 网络
- [Go netpoller 原生网络模型之源码全面揭秘](https://strikefreedom.top/go-netpoll-io-multiplexing-reactor): 从源码和例子分析。引出reactor对比分析、gnet等。简单介绍了select、epoll的代码结束，而且详细对比了分析各自的优缺点，并且很好的从源码分析了几个问题，但是没有再深入介绍？。TODO
- [如何优化 Go HTTP client 的性能](https://www.loginradius.com/blog/async/tune-the-go-http-client-for-high-performance/): Client的Timeout参数与DefaultMaxIdleConnsPerHost
- [在 golang 中是如何对 epoll 进行封装的？](https://mp.weixin.qq.com/s/hjWhh_zHfxmH1yZFfvu_zA): 详细的底层代码介绍

## etcd
- [跟 etcd 学习数据库中事务隔离的实现](https://blog.betacat.io/post/2019/08/learn-transaction-isolation-levels-from-etcd/)
- [MVCC 在 etcd 中的实现](https://blog.betacat.io/post/mvcc-implementation-in-etcd/)

## awesome

- [Go编程时光](http://golang.iswbm.com/en/latest/): 这个项目的基本用法讲述得还可以。可以当成写代码的手册类。网页中标亮点为重点。
- [go-zero](https://www.yuque.com/tal-tech/go-zero/yaoehb):  理解架构和源码。
- [Go 语言设计与实现](https://draveness.me/golang/): draveness大神的书


---
# python
- [gevent.md](./python/gevent.md)
- [uwsgi.md](./python/uwsgi.md)

## 网络
- [深入理解uwsgi和gunicorn网络模型[上]](http://xiaorui.cc/archives/4264): 这篇文章比较深入，提了问题也很到位，有助思考
- [去 async/await 之路](https://zhuanlan.zhihu.com/p/45996168): 说明python的异步的一些方式和对比。
- [Gevent高并发网络库精解:一些数据通信的数据结构](https://www.jianshu.com/p/ccf3bd34340f)
- [TODO: Python 开源异步并发框架的未来](https://segmentfault.com/a/1190000000471602)

- [How To Use Linux epoll with Python](https://harveyqing.gitbooks.io/python-read-and-write/content/python_advance/how_to_use_linux_epoll.html): 一个比较简单的代码使用实例，比较简短。

## 数据结构
- [sort](./algorithm/排序/sorted.md): python的排序是怎么实现的
- [Python字典dict实现原理](https://zhuanlan.zhihu.com/p/74003719): TODO python的字典是怎么实现的，如何解决hash冲突。


---
# java

## 锁
- [搞懂 Java 并发中的 AQS 是怎么运行的](https://mp.weixin.qq.com/s/tMI6qV_ItuTqlKZiUnAlmg): 晦涩难懂
- [i++ 是线程安全的吗？](https://mp.weixin.qq.com/s/H0E_y6tC4d8-AxqJS3u--A): volatile解决了线程间共享变量的可见性问题、 volatile并不能解决线程同步问题

---
# 数据库
- [Flink Exactly-Once 投递实现浅析](https://developer.aliyun.com/article/714835)
- [canal的优化过程和讨论](https://github.com/alibaba/canal/issues/726): 分阶段进行优化。解析、并行、序列化、数据拷贝等方面。基于ringbuffer的并发模型，整个过程会分为4个阶段，多个阶段之间互相隔离和依赖，把最耗瓶颈的解析这块采用多线程的模型进行加速，预计整个优化完成，整个解析可以跑满整个千兆网卡。跟新版本的redis改成多线程的思路一致。

---
# clickhouse

## 低基数
- [ClickHouse中的低基数字段优化](https://mp.weixin.qq.com/s/XKQk4hsdj8VN8TnYdrOnuw): 指如何优化低基数的字符串字段。通过LowCardinality把字段通过类似position的压缩技术，改成字典。字符越长效果越佳。
- [LowCardinality Data Type](https://clickhouse.tech/docs/en/sql-reference/data-types/lowcardinality/): 官网文档
- [A MAGICAL MYSTERY TOUR OF THE LOWCARDINALITY DATA TYPE](https://altinity.com/blog/2019/3/27/low-cardinality): 不知道对数值类型有多少优化空间。
- [LowCardinality 数据类型的神秘之旅](https://blog.csdn.net/jiangshouzhuang/article/details/103268340): 具体的倒排索引图和具体的代码与例子。
- [allow_suspicious_low_cardinality_types](https://clickhouse.tech/docs/en/operations/settings/settings/#allow_suspicious_low_cardinality_types): 允许或限制将LowCardinality用于固定大小为8个字节或更少的数据类型：数字数据类型和FixedString（8_bytes_or_less）。要注意较小的固定值可能适得其反。

- [LowCardinality](./数据库/clickhouse/LowCardinality.md)： 总结与测试

## 官方文章
- [博客](https://altinity.com/blog/)

- [five-ways-to-handle-as-of-queries-in-clickhouse](https://altinity.com/blog/2020/4/8/five-ways-to-handle-as-of-queries-in-clickhouse): 通过比较5种方式去，来说明怎么拿时间序列的最靠近的一行（窗口、Top K 的场景）。比较贴近生产的例子。
- [joins-in-clickhouse-materialized-views](https://altinity.com/blog/2020-07-14-joins-in-clickhouse-materialized-views):  通过物化视图和join操作，进行实时汇总进汇总表的操作。但是要注意join的一些小陷阱。ClickHouse只触发联接中最左边的表。其他表可以为转换提供数据，但是视图不会对这些表上的插入做出反应。
- [clickhouse-dictionaries-reloaded](https://altinity.com/blog/2020/5/19/clickhouse-dictionaries-reloaded): 字典的一个改版优化。之前字典声明和使用的不便。新版本可以直接通过ddl进行管理，而且能更好优化join查询。它只需要5次调用，而不需要扫描1000万行表（？：字面理解是左边直接调用了5次join。还是说字典直接在内存，所以能优化数据装载过程而已）。
- [大规模并行日志处理对比](https://altinity.com/blog/2017/9/13/massive-parallel-log-processing-with-clickhouse): 通过限制cpu核数测试其性能差距。查询的姿势影响着并发性。
- [集群的查询分析对比](https://altinity.com/blog/2017/6/16/clickhouse-in-a-general-analytical-workload-based-on-star-schema-benchmark): 集群和子查询都线性提升3倍，两表join提升不到2倍，三表join只略微提升。通过子查询避免多表join，能优化6倍
- [lz4和zstd对比](https://altinity.com/blog/2017/11/21/compression-in-clickhouse): zstd压缩率更高。冷运行时间几乎没有差异（因为IO时间占优势的减压时间），但热运行中LZ4的速度要快得多（因为IO操作少得多，并且解码性能成为主要因素）。如果涉及到大范围扫描，则zstd。如果io足够快，则lz4。如果超快ssd，可以指定无压缩。
- [sql-for-clickhouse-dba](https://altinity.com/blog/2020/5/12/sql-for-clickhouse-dba): 系统表的一些指标、查询相关信息的查询语句
- [NEW ENCODINGS TO IMPROVE CLICKHOUSE EFFICIENCY](https://altinity.com/blog/2019/7/new-encodings-to-improve-clickhouse): [编码压缩对比](./数据库/clickhouse/编码压缩对比.md)
- [clickhouse-aggregatefunctions-and-aggregatestate](https://altinity.com/blog/2017/7/10/clickhouse-aggregatefunctions-and-aggregatestate): AggregatingMergeTree，clickhouse聚合状态的特性，让多维度的去重需求更快。
- [压测例子](https://github.com/Altinity/clickhouse-sts/)
- [**优化手段**](https://altinity.com/presentations/2019/10/9/clickhouse-query-performance-tips-and-tricks): max_threads、分区裁剪、prewhere、提前减少join的数据量; 主键的块选择性granularity、排序建让随机行减少增加压缩率、二级索引、编码压缩、物化视图;更精简的数据类型、zstd压缩算法、字典优化join、近似算法采样优化查询、分布式集群优化大数据。

## 集群
- [ClickHouse原理解析与应用.md](./数据库/clickhouse/cluster.md)
- [ClickHouse复制表、分布式表机制与使用方法](https://www.jianshu.com/p/ab811cceb856): 比较入门的简明介绍. [ClickHouse Better Practices](https://www.jianshu.com/p/363d734bdc03): 一些实践建议
- [百分点大数据技术团队：ClickHouse国家级项目最佳实践](https://www.jiqizhixin.com/articles/2020-05-06-5): 一些集群使用的实践
- TODO: [Clickhouse最佳实战之业界实战汇总及分析](https://zhuanlan.zhihu.com/p/161248414)

## 位图
- [ClickHouse留存分析工具十亿数据秒级查询方案](https://mp.weixin.qq.com/s/Bh5aEvpBgSEDkTozpfMFkw): 通过位图的，优化留存用户的分析。有具体代码与总结、参考文献。
- [ClickHouse遇见RoaringBitmap](https://blog.csdn.net/nazeniwaresakini/article/details/108166089): 引出AggregateFunction、源码分析。
- [bitmap-functions](https://clickhouse.tech/docs/en/sql-reference/functions/bitmap-functions/): 官方文档
- [bitmap](./数据库/clickhouse/bitmap.md): 总结测试与例子。
- [高效压缩位图RoaringBitmap的原理与应用](https://www.jianshu.com/p/818ac4e90daf): 前言介绍的挺好的，对比布隆过滤器和HyperLogLog。和用单纯的位图的空间占用引出RBM、相关论文。但是后面的算法详解有点简陋
- [RoaringBitmap数据结构及原理](https://blog.csdn.net/yizishou/article/details/78342499): 有比较具体空间和过程的分析

## 其他
- [配置文件说明](https://www.cnblogs.com/zhoujinyi/p/12627780.html): 配置的相关文档与实践配置
- [苏宁基于 ClickHouse 的大数据全链路监控实践](https://cloud.tencent.com/developer/article/1696928)
- [MySQL到ClickHouse的高速公路-MaterializeMySQL引擎](https://bbs.huaweicloud.com/forum/thread-102438-1-1.html): 比较详细的介绍MaterializeMySQL引擎
- [How to solve Clickhouse OOM](https://chowdera.com/2020/12/20201202205329308t.html): 内存使用的一些说明
- [Projections](https://github.com/ClickHouse/ClickHouse/pull/20202) 、 [2021年ClickHouse最王炸功能来袭，性能轻松提升40倍](https://mp.weixin.qq.com/s/CXSOPyZWORGBf9_GRQRFfQ): 投射功能！

---
# mysql

- [一次SQL查询优化原理分析](https://www.jianshu.com/p/0768ebc4e28d): 回表、分页优化。引出INNODB_BUFFER_PAGE的使用
- [优化 SQLite 在 Go 中的性能](https://turriate.com/articles/making-sqlite-faster-in-go): 连接池和prepare
- [从网友对 MySQL 手册的一个疑问聊起](https://mp.weixin.qq.com/s/EwLTpzIbtRE3Mlt0OtRyVg): 如何用3个字节表示年月日
- [为什么MySQL不建议delete删除数据](https://juejin.cn/post/6913695663028961293): 详细解析删除操作。有具体的工具分析底层数据的分布，而且通过对比物理读次数、逻辑读次数分析结果。碎片：删除数据会在页面上留下一些”空洞”。
- [优化 | 实例解析MySQL性能瓶颈排查定位](https://mp.weixin.qq.com/s?__biz=MjM5NzAzMTY4NQ==&mid=506446073&idx=6&sn=74335facf3bcf7ede3af7ce03765b343&scene=19): 实例优化。
- [MySQL客户端连接登入hang住原因分析](https://my.oschina.net/yejr/blog/4815112): pstack和SIGSTOP、mysql处理信号的方式
- [数据库查询性能优化指南](https://my.oschina.net/u/4273516/blog/4934611): 比较全面命令的系统性能优化指南。vmstat, uptime、top、mpstat或者sar, perf top、iostat、pidstat和iotop
- [MySQL又双叒崩了——记beego的stmt优化](https://mp.weixin.qq.com/s/jehtP2WniN8Zkn-tyJZ88g): 并发锁处理的姿势。double-check和计数回收。
- [为什么 MySQL 使用 B+ 树](https://draveness.me/whys-the-design-mysql-b-plus-tree/): draveness
- [8.0移除查询缓存](https://mysqlserverteam.com/mysql-8-0-retiring-support-for-the-query-cache/)

- [InnoDB 隔离模式的 MySQL 性能影响](https://www.percona.com/blog/2015/01/14/mysql-performance-implications-of-innodb-isolation-modes/): 长事务增加MVCC的历史版本维护成本，如果有并发更新，性能更慢 、 [Innodb 事务历史往往隐藏着危险的“债务”](https://www.percona.com/blog/2014/10/17/innodb-transaction-history-often-hides-dangerous-debt/): 长事务导致清理线程停止，undo log过大无法放到buffer里，导致移到磁盘，IO下降。 、 [InnoDB的多版本控制处理可能是致命弱点](https://www.percona.com/blog/2014/12/17/innodbs-multi-versioning-handling-can-be-achilles-heel/)

- [MySQL · 源码分析 · InnoDB Repeatable Read隔离级别之大不同](http://mysql.taobao.org/monthly/2017/06/07/): 有兴趣和能力要看下源码
- [mysql-snapshots](https://debezium.io/documentation/reference/connectors/mysql.html#mysql-snapshots): debezium如何做精确一次的mysql快照。锁表
- [innodb_log_buffer_size 到底有什么作用？](https://mp.weixin.qq.com/s/y8zQ6106ZwRSvj2RMDrs2w): 通过实验观察redo log 的写缓存。开启 innodb metrics 和 performance_schema，观察 3M 左右的 redo log，发生了 7 次 IO，6 次 write 和 1 次 sync，每次 write 大概需要 0.8ms。

- [MySQL · 引擎特性 · 基于GTID复制实现的工作原理](http://mysql.taobao.org/monthly/2020/05/09/) , [MySQL5.7杀手级新特性：GTID原理与实战](https://keithlan.github.io/2016/06/23/gtid/)
- [MySQL 并行复制演进及 MySQL 8.0 中基于 WriteSet 的优化](https://zhuanlan.zhihu.com/p/37129637): 详细介绍复制的相关历程

- [行格式和溢出](https://www.yuque.com/u2278269/gq5x74/pzkge7): 行格式分布和溢出分析
- [为什么阿里巴巴不建议MySQL使用Text类型？](https://juejin.cn/post/6898479206087262222) 、 [记一次关于 Mysql 中 text 类型和索引问题引起的慢查询的定位及优化](https://juejin.cn/post/6844903879318962183)




---
# Redis
- [Redis事务、Lua事务和管道的实践探究](https://github.com/littlejoyo/Blog/issues/39): 一个比较完整详细的对比
- [redis-eventloop](https://draveness.me/redis-eventloop/)
- [HyperLogLog 算法的原理讲解以及 Redis 是如何应用它的](https://juejin.cn/post/6844903785744056333): 一个深入浅出的讲述
- [颠覆认知——Redis会遇到的15个「坑」，你踩过几个？](https://mp.weixin.qq.com/s/F0RJhouiqdwweLk6fGsh0A): 贴合实际。TODO

---
# ES
- [官方博客](https://www.elastic.co/cn/blog/)

- [ES查询性能优化-优先选择keyword类型](https://summerisgreen.com/blog/2019-12-01-2019-12-01-es%E6%9F%A5%E8%AF%A2%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96-%E4%BC%98%E5%85%88%E9%80%89%E6%8B%A9keyword%E7%B1%BB%E5%9E%8B.html): 优先使用keyword而不是number!
- [number?keyword?傻傻分不清楚](https://elasticsearch.cn/article/446): wood大叔
- [Elasticsearch 5.x 源码分析（12）对类似枚举数据的搜索异常慢的一种猜测](https://www.jianshu.com/p/9830413f62eb): 结合源码问题分析一例，可惜没结论

- [Elasticsearch性能监控（一）](https://mp.weixin.qq.com/s/QBjSSYVjHJMLJ6-7yj1bzA): todo
- [elasticsearch-unassigned-shards](https://www.datadoghq.com/blog/elasticsearch-unassigned-shards): elasticsearch对unassigned-shards的问题排查与恢复

- [Elasticsearch 高并发写入优化的开源协同经历](https://www.infoq.cn/article/hadbrlw6fao0fmshxkpz): 优化写入调优

- [ElasticSearch 集群压力测试指南](https://mp.weixin.qq.com/s/kzEazBDlphFxfxJmVBQhYA): 相关入门介绍和指标说明
- [Elasticsearch分布式一致性原理剖析(三)-Data篇](https://zhuanlan.zhihu.com/p/35299145): 深入分析一致性的一些问题和原理

- [可视化 Lucene 的段合并](https://blog.mikemccandless.com/2011/02/visualizing-lucenes-segment-merges.html): TODO

---
# 容器
- [Kubernetes 如何使用 Nginx-Ingress 实现蓝绿和金丝雀发布](https://mp.weixin.qq.com/s/SAE4IvjVPVV1dfS4ZXwzbQ): Ingress-Nginx在0.21版本引入了Canary功能。一个具体的例子介绍使用。而且后面介绍了A/B测试和蓝绿部署以及金丝雀区别，
- [如何为服务网格选择入口网关？](https://zhaohuabing.com/post/2019-03-29-how-to-choose-ingress-for-service-mesh/): 介绍了内部服务间的通信(Cluster IP、Istio Sidecar Proxy)的优缺点。如何从外部网络访问， 如何为服务网格选择入口网关？。介绍包括Pod、Service、NodePort、LoadBalancer、Ingress、Gateway、VirtualService等，最后采用API Gateway + Sidecar Proxy作为服务网格的流量入口。还不能很好理解。
- [Docker 核心技术与实现原理](https://draveness.me/docker/), [Docker 原理知识](https://juejin.cn/post/6844904143660777485)
- [Kubernetes面试题](https://blog.csdn.net/estarhao/article/details/114703958): 问题比较多，但比较入门，不够深入，开阔视野
- [什么是 Istio？为什么 Kubernetes 需要 Istio？](https://jimmysong.io/blog/what-is-istio-and-why-does-kubernetes-need-it/)

---
## 优雅退出
- [优雅退出](./SOD/优雅退出.md)
- [优雅退出例子](./SOD/优雅退出例子.md)

### 参考链接
- [Service Mesh 实践（五）: 优雅启动和优雅关闭](https://www.dozer.cc/2020/02/graceful-start-and-shutdown.html)
- [pod-lifecycle](https://kubernetes.io/zh/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination-forced)
- [kubernetes-best-practices-terminating-with-grace](https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-terminating-with-grace)
- [bestpractice-pod-prestop](http://docs.api.xiaomi.com/en/app-engine-k8s/bestpractice-pod-prestop.html)
- [linux: nohup 命令实现守护进程（屏蔽 SIGHUP 信号）](https://my.oschina.net/sallency/blog/827737)
- [停止或暂停程序的信号: intr、quit、stop](https://my.oschina.net/u/2914561/blog/808585)
- [一次 Docker 容器内大量僵尸进程排查分析](https://juejin.cn/post/6844904029248552973)
- [Dumb-Init进程信号处理](https://my.oschina.net/xiaominmin/blog/3223293)
- [docker-containerd-shim](https://juejin.im/entry/6844903454549229576)
- [when-a-parent-process-is-killed-by-kill-9-will-subprocess-also-be-killed](https://stackoverflow.com/questions/1491674/when-a-parent-process-is-killed-by-kill-9-will-subprocess-also-be-killed)
- [僵尸进程例子](https://github.com/Yelp/dumb-init/issues/128)

- [揭密容器环境下 Golang 回收子进程的运行机制](https://mp.weixin.qq.com/s/3HsqtHwWReX1S3ggP2_owg): reaper例子子进程提前回收，父进程wait失败。解决办法：同步锁

- [gRPC的平滑关闭和在Kubernetes上的服务摘流方案总结](https://mp.weixin.qq.com/s/lCTyZgSK3b-rJtV9l6PNYA):
    - 术语：摘流只需要运维人员从负载均衡上把机器节点的IP拿掉，待应用重启或者更新完毕后再将机器节点的IP挂回负载均衡上即可。
    - 原因：并行发生，这就导致了有可能Pod已经进入关闭序列了，但是Service那里还没有做完摘流。
    - 方案：利用 Pod 关闭生命周期里的preStop 钩子，让其执行 sleep 命令休眠5~10秒，通过延迟关闭Pod来让Service先完成摘流，preStop的执行并不影响Pod内应用继续处理现存请求。让并行执行的摘流和平滑关闭动作在时间线上尽量错开了，也就不会出现Service摘流可能会有延迟的问题了

---
# 中间件
- [认识长轮询：配置中心是如何实现推送的？](https://mp.weixin.qq.com/s/YjvL0sUTGHxR3GJFqrP8qg): tcp长连接发现问题时间要比较久。保活计时器来保证的。keepalive只能检测连接是否存活，不能检测连接是否可用，而且参数是机器操作系统层面，不够灵活。
- [抖音春晚活动背后的 Service Mesh 流量治理技术](https://juejin.cn/post/6969012264342913038): Service Mesh的基本概念
- [Service Mesh 和 API Gateway 关系深度探讨](https://mp.weixin.qq.com/s/zhJ3koaApEOVfdyyXuAGUQ): 详细分析两者之间的联系

---
# 分布式
- [分布式](./SOD/分布式)

## redis
- [redis分布式锁](./redis/分布式锁.md)
- [再有人问你分布式锁，这篇文章扔给他](https://juejin.cn/post/6844903688088059912): mysql、redis、zk

- [分布式锁的实现之 redis 篇](https://xiaomi-info.github.io/2019/12/17/redis-distributed-lock/): redis锁相关会存在的问题与图分析
- [分布式锁用 Redis 还是 Zookeeper？](https://juejin.im/post/6894853961761685517): 分析具体场景，两种解决办法的简单使用与对比。
- [基于Redis实现分布式锁之前，这些坑你一定得知道](https://juejin.cn/post/6844904086236561416): redlock比较详细的坑点，与解决办法思路。
- [Redis事务、Lua事务和管道的实践探究](https://github.com/littlejoyo/Blog/issues/39): 较详细的对比

## 分布式锁
- [分布式柔性事务的TCC方案](https://mp.weixin.qq.com/s/tnmQaHpo49XUtYBvsrx1Ig): TCC的总结

## 一致性哈希
- [图解什么是一致性哈希算法](https://mp.weixin.qq.com/s/9XwiEPjCD6vxrpr-rp3a6A): 比较详细的原理介绍与redis对比
- [python简单实现一致性哈希](./python/constant_hash.py)

## 其他
- [如何保障消息100%投递成功、消息幂等性？](https://mp.weixin.qq.com/s/I5GF-3UUbrVfgoIMJmLUbw): 从业务场景出发，从消息队列到幂等性的一些思考。
- [幂等性浅谈](https://www.jianshu.com/p/475589f5cd7b): 简述幂等的常用三种思路。

- [分布式系统的时间方案小结](https://www.91im.net/im/1267.html): 所以，如果我们没法实现TrueTime，同时又觉得HLC太复杂，但又想获取全局时间，TSO没准是一个很好的选择，因为它足够简单高效。

---
# web

## csrf
- [Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [跨域资源共享 CORS 详解-阮一峰](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)
- [不要再问我跨域的问题了](https://juejin.cn/post/6844903639304110093)
- [浏览器系列之 Cookie 和 SameSite 属性 ](https://github.com/mqyqingfeng/Blog/issues/157): 阿里对SameSite的影响分析和研究。
- [前端安全系列（二）：如何防止CSRF攻击？-美团技术团队](https://tech.meituan.com/2018/10/11/fe-security-csrf.html)
- [什么是跨域请求以及实现跨域的方案](https://www.jianshu.com/p/f880878c1398)
- [简单请求](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS)
- [django的csrf它是如何工作的](https://yiyibooks.cn/xx/Django_1.11.6/ref/csrf.html)
- [如何通过JWT防御CSRF](https://segmentfault.com/a/1190000003716037)



---
# 操作系统

- [记一次面试：进程之间究竟有哪些通信方式？](https://mp.weixin.qq.com/s/CGqy0j5WvarN6mTmYB8vSA)
- [read文件一个字节实际会发生多大的磁盘IO？](https://mp.weixin.qq.com/s/LcuWAg10hxZjCoyR1cMJSQ): 深入内核组件，读取文件的过程
- [MIT6.S081](https://github.com/huihongxiao/MIT6.S081): 课程是基于一个类似于Unix但是简单的多的教学操作系统XV6来讲解，虽然不是原汁原味的Linux，但是对于理解Linux的工作方式和结构是足够了

## CPU
- [Linux性能优化：CPU篇](https://zhuanlan.zhihu.com/p/180402964): 本文主要帮助理解 CPU 相关的性能指标，常见的 CPU 性能问题以及解决方案梳理。
- [软中断会吃掉你多少CPU？](https://zhuanlan.zhihu.com/p/80513852)
- [10分钟教会你看懂top](https://juejin.cn/post/6844903919588491278): top详解
- [Linux Load Averages：什么是平均负载？](https://zhuanlan.zhihu.com/p/75975041): 好文。从源码变更提交分析，使用 bcc／eBPF 测量了不间断状态下的堆栈的 trace 和时间.

## 内存
- [函数运行时在内存中是什么样子？](https://mp.weixin.qq.com/s?__biz=MzU2NTYyOTQ4OQ==&mid=2247484963&idx=1&sn=542d3bec57c6a9dfc17c83005fd2c030&chksm=fcb9817dcbce086b10cb44cad7c9777b0088fb8d9d6baf71ae36a9b03e1f8ef5bec62b79d6f7&scene=21#wechat_redirect): 跳转地址、存放参数、局部变量、寄存器初始值。不要创建过大的局部变量、函数栈帧，也就是调用层次不能太多
- [自己动手实现一个malloc内存分配器](https://mp.weixin.qq.com/s/FpXLBOVm5P-sNTr2S7PyhQ): 比较直白的内存分配器介绍：我们的简单内存分配器采用了First Fit分配算法；找到一个满足要求的内存块后会进行切分，剩下的作为新的内存块；同时当释放内存时会立即合并相邻的空闲内存块，同时为加快合并速度，我们引入了Donald Knuth的设计方法，为每个内存块增加footer信息。
- [Go内存分配那些事](https://lessisbetter.site/2019/07/06/go-memory-allocation/): 虚拟内存、栈和堆、堆内存管理。比较偏向go内存的主题，要先补习下操作系统相关的知识。
- [为什么 Redis 快照使用子进程](https://draveness.me/whys-the-design-redis-bgsave-fork/): 写时拷贝
- [深入剖析虚拟内存工作原理](https://mp.weixin.qq.com/s/c81Fvws0J2tHjcdTgxvv6g): 计算机存储器、虚拟内存、页表、缺页中断、加速翻译&优化页表、TLB 加速、多级页表、倒排页表

## 磁盘
- [磁盘IO的调度模型](https://zhuanlan.zhihu.com/p/22604682)
- [存储进阶—怎么才能保证 IO 数据的安全？](https://mp.weixin.qq.com/s/2lUjSnidY_RVQ4jNWGHvLw): 本文总结 3 种最根本的 IO 安全的方式，分别是 O_DIRECT 写，标准 IO + Sync 方式，mmap 写 + msync 方式。要么每次都是同步写盘，要么就是每次写完，再调用 sync 主动刷，才能保证数据安全；注意硬盘也有缓存，这个也是易失性的，必须要考虑在内，可以通过 hdparm 命令开关；(非易失性的存储介质、mmap减少数据在用户空间和内核空间之间的拷贝操作)
- [存储基础 — 文件描述符 fd 究竟是什么？](https://mp.weixin.qq.com/s/hLq7Pp8CkJD9B-Xqym50dA): file 是进程出发创建的，进程 open 同一个文件会导致多个 file ，指向同一个 inode

## 网络
- [42张图详解 NAT : 换个马甲就能上网](https://mp.weixin.qq.com/s/OCuLr3ZGAaYXwXkkNKlTwg): 基本NAT、NAPT、Easy IP、NAT Server、NAT ALG
- [带宽、延时、吞吐率、PPS 这些都是啥？](https://mp.weixin.qq.com/s/uud_LciJ_9MaRTXgryKQ5A)
- [为什么 TCP 协议有 TIME_WAIT 状态](https://mp.weixin.qq.com/s/QTZJdxVzDNEvz7htDgGU-w): 为什么系列。 [time_wait的含义](./network/q.md#time_wait)
- [**为什么 TCP 建立连接需要三次握手**](https://mp.weixin.qq.com/s/XGpIjrnxAAuHa8EVSotBQw): 『两次握手』：无法避免历史错误连接的初始化，浪费接收方的资源；『四次握手』：TCP 协议的设计可以让我们同时传递 ACK 和 SYN 两个控制信息，减少了通信次数，所以不需要使用更多的通信次数传输相同的信息；
- [网络](https://note.grianchan.com/%E7%BD%91%E7%BB%9C/%E7%BD%91%E7%BB%9C.html): 一些网络常见问题与总结！**重点**
- [动图图解！既然IP层会分片，为什么TCP层也还要分段？](https://mp.weixin.qq.com/s/LkuDO0Wc2c4ksgukO2NFqA):
    - MSS：Maximum Segment Size 。TCP 提交给 IP 层最大分段大小，不包含 TCP Header 和  TCP Option，只包含 TCP Payload ，MSS 是 TCP 用来限制应用层最大的发送字节数。
    - MTU: Maximum Transmit Unit，最大传输单元。其实这个是由数据链路层提供，为了告诉上层IP层，自己的传输能力是多大。IP层就会根据它进行数据包切分。一般 MTU=1500 Byte。一般情况下MSS + 20（TCP头）+ 20（IP头）= MTU
    - 数据在TCP分段，就是为了在IP层不需要分片，同时发生重传的时候只重传分段后的小份数据。
- [tcp_tw_recycle](https://blog.csdn.net/whatday/article/details/113427085): 比较详细的方案分析，附带源码介绍。

- [高并发服务遇redis瓶颈引发time-wait事故](http://xiaorui.cc/archives/7175):
    - tcp_tw_reuse和ip_local_port_range调整。
    - 拿不到连接则 new 一个新连接，连接用完了后需要归还连接池，如果这时候连接池已经满了，那么该连接会主动进行 close 关闭： 一直阻塞等待其他人归还连接, 或者直接报错。
    - redis 的 qps 性能瓶颈: 扩容 redis 节点，迁移 slot 使其分担流量。尽量把程序中 redis 的请求改成批量模式。pipeline worker 触发条件是满足 3 个 command 或 5ms 超时，定时器采用分段的时间轮。

## 文件系统
- [理解Linux的文件描述符FD与Inode](https://zhuanlan.zhihu.com/p/143430585): 有具体的进程打开文件的各种操作导致的关系说明。 [文件描述符](./common/文件描述符.md)

---
# 网络
- **[network](./network/readme.md): 摘抄与总结**

- [谈半同步/半异步网络并发模型](https://zhuanlan.zhihu.com/p/58860015): 这篇文章，总结了半同步/半异步与半同步/半反应堆的区别（架构队列设计,I/O发生的地方），也体现了reactor的含义，让人打通所有的概念的联系
- [如何深刻理解Reactor和Proactor？](https://www.zhihu.com/question/26943938/answer/1856426252): 总结明了
- [nginx不是使用epoll么? epoll貌似是同步的吧! 那nginx的异步非阻塞到底异步在哪里?](https://www.zhihu.com/question/63193746/answer/206682206): 这里有说到：开发者必须保证每一个事件handler都不得包含任何阻塞调用
- [重大事故！IO问题引发线上20台机器同时崩溃](https://juejin.im/post/6875176737274724366): 这篇文章写得很好，值得多读。该博主也经常分析性能调优的文章。
- [Linux的五种IO模型](https://juejin.cn/post/6844903687626686472): 这篇文章讲得很好！
- [Node.js 线程你理解的可能是错的](https://juejin.im/post/5b1e55cbe51d45067e6fcb84): 从问题出发，解析线程与异步操作
- [**不要阻塞你的事件循环**](https://nodejs.org/zh-cn/docs/guides/dont-block-the-event-loop/): 对事件循环有很详细的介绍，适合多读
- [网络库libevent、libev、libuv对比](https://blog.csdn.net/lijinqi1987/java/article/details/71214974)

- [通过实例理解Go标准库http包是如何处理keep-alive连接的](https://tonybai.com/2021/01/08/understand-how-http-package-deal-with-keep-alive-connection/): keep-alive的基本使用、idletimeout。TODO: 长连接、底层TCP的状态是怎么样的？
- [Socket粘包问题终极解决方案—Netty版（2W字）！](https://juejin.cn/post/6917043797684584461): netty的源码分析
- [详解HTTP 与TCP中Keep-Alive机制的区别](https://cloud.tencent.com/developer/article/1430022) 、 [HTTP keep-alive和TCP keepalive的区别，你了解吗？](https://zhuanlan.zhihu.com/p/224595048)
- [K8s中Pod的服务发现](https://mp.weixin.qq.com/s/tjKSq79nrzOt9mLX24dblQ): 简单介绍iptable的概念、具体的代码例子介绍k8s的网络链
- [线上大量CLOSE_WAIT的原因深入分析](https://juejin.cn/post/6844903734300901390):
    - 一次 MySQL 主动关闭，导致服务出现大量 CLOSE_WAIT 的全流程排查过程。
    - 从问题分析到解决思路，文章都写得很有条理。**火焰图分析**。
    - MySQL负载均衡器 给我的服务发送 FIN 包，我进行了响应，此时我进入了 CLOSE_WAIT 状态，但是后续作为被动关闭方的我，并没有发送 FIN，导致我服务端一直处于 CLOSE_WAIT 状态，无法最终进入 CLOSED 状态。
    - getMapNil 返回了nil，但是下面的判断条件没有进行回滚。
- [解决Linux TIME_WAIT过多造成的问题](https://blog.csdn.net/zhangjunli/article/details/89321202): 具体源码分析。

## rpc
- [思考gRPC ：为什么是HTTP/2 | 横云断岭的专栏](https://hengyun.tech/thinking-about-grpc-http2/)
- [gRPC系列(三) 如何借助HTTP2实现传输 - 知乎](https://zhuanlan.zhihu.com/p/161577635)

---
# 算法
- [经典智力面试题：一家人过桥](https://mp.weixin.qq.com/s/SLLg5XxTSacrADHMWtMBJQ): 如何利用最大的复用时间过桥
- [字节一面：如何从 100 亿 URL 中找出相同的 URL？](https://mp.weixin.qq.com/s/0OyiLxlZkhUQ605IQRliVg)
- [场景设计题](https://blog.nowcoder.net/n/33d0033550d24bf49841858f1b2091aa)

---
# 其他
- [如何写出安全的、基本功能完善的Bash脚本](https://mp.weixin.qq.com/s/ZO5jKzQGDy1Di1WDl49d_g): 一个比较实用的模板
- [高效的数据压缩编码方式 Protobuf](https://mp.weixin.qq.com/s/Llg1Rb11KRNS1N-seqjeLg )、 [高效的序列化/反序列化数据方式 Protobuf](https://mp.weixin.qq.com/s/22p3VucucXkxxhDq--AYaw ) TODO 如何高效
- TODO prometheus的时序时间库原理
- [用Gitbook和Github轻松打造属于自己的出版平台](http://self-publishing.ebookchain.org/index.html)

---
# 设计模式
- [ORM is an anti-pattern](https://seldo.com/posts/orm_is_an_antipattern): ORM的一些对比和作者说其反模式的理解
- [我们为什么要用IoC和AOP](https://www.jianshu.com/p/feb9521388cf): 本质是组件的调用方参与了组件的创建和配置工作。
- [如何来一次说干就干的重构 (流程篇)](https://cloud.tencent.com/developer/article/1415577): 重构的级别。架构级别重构，如通过分层使业务解耦，引入缓存设计提升系统高并发等。
