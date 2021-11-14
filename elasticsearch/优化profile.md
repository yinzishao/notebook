# Profile API 性能分析

平时开发的过程中我们可能需要对一些查询操作进行优化，而优化之前的工作就是要对操作的性能进行分析，而ES提供了Profile API来帮助用户进行性能分析。它让用户了解如何在较低的级别执行搜索请求，这样用户就可以理解为什么某些请求比较慢，并采取措施改进它们。

需要注意的是Profile API**不测量网络延迟、搜索资源获取阶段、请求在队列中花费的时间或在协调节点上合并碎片响应时花费的时间**。

需要注意的是开启性能分析会给查询带来非常大的性能开销。所以不要尝试将一个开启了性能分析的请求和为开启性能分析的请求比对时间效率。

## breakdown参数的意义

参数名称 | 说明
----|----
create_weight | Lucene中的查询必须能够跨多个IndexSearchers重用，而很多查询**需要统计和它对应的索引相关的信息**，所以Lucene要求每个查询生成一个Weight对象，它作为一个临时上下文对象来保存与相关联的状态。此参数表示创建这个对象花费的时间
build_scorer | 构建一个计分器所花费的时间
next_doc | Lucene中next_doc方法，统计的是**确定下一个匹配文档所需的时间**
advance | Lucene中advance方法，next_doc的低级版本，**用来查找下一个匹配的文档**。因为并不是所有查询使用next_doc，所以advance也统计了此类查询的时间
match | 有些查询比如短语查询（phrase queries）需要**对文档进“近似地”匹配**，此时查询过程中会存在第二阶段检查。其作用是匹配统计量的度量
score | 统计了**为文档打分的时间**
*_count | 记录特定方法的调用次数。例如，“next_doc_count”:2，表示在两个不同的文档上调用了nextDoc()方法。这可以通过比较不同查询组件之间的计数来**帮助判断查询的选择性**。

## rewrite_time（重写时间）

Lucene中的所有查询都要**经历一次或者多次“重写”过程**。这个过程将一直持续下去，直到查询停止变化。这个过程允许Lucene执行优化，例如删除冗余子句，替换一个查询以获得更有效的执行路径等等。这个值是**包含所有被重写查询的总时间**。

## Profiling存在的局限

- 性能分析不能获取搜索数据获取以及网络开销
- 性能分析也不考虑在队列中花费的时间、合并协调节点上的shard响应，或诸如构建全局序数之类的额外工作
- 性能分析目前无法应用于搜索建议（suggestions），高亮搜索（highlighting）
- 目前reduce阶段无法使用性能分析统计结果

## 参考链接
- [Elasticsearch查询——Profile API（性能分析）](https://blog.csdn.net/qq330983778/article/details/103657930)
- [官方文档：search-profile](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-profile.html)

---
# Elasticsearch慢查询故障诊断

> - [**Elasticsearch慢查询故障诊断**](https://www.cnblogs.com/zhq1007/p/11744102.html)

- build_scorer:构造一个scorer的耗时。scorer主要用于对matching的doc进行打分和排序。build_scorer内部构造了迭代器，这个迭代器可以遍历所有matched document，**构造迭代器是非常耗时的操作**，因为涉及到对各**子查询的docId结果集构造倒排链或bitset**，并且做**conjunction**生成最终可被迭代的docId bitset或倒排链。**大多数查询主要耗时在这一步**。

- next_doc: 寻找下一个匹配的document Id。这里keyword, text等文本类型的字段会利用**skipList**，数值类型的数据会利用**Tree结构**快速找的下一个匹配的docoument Id。同时，这里会记录该doc命中的子查询数量，用于最终的min_should_match之类的过滤。

- advance: **类似于一个low level的next_doc**。并不是所有的query都能实现next_doc，比如must查询走的advance去找下一个匹配的文档。

- score: 记录socrer中对文档打分的耗时，通过**Freq，normal**等数据结合tf-idf等算法计算出得分。

- match: **记录第二阶段打分的耗时**。有些查询需要两阶段打分，比如**短语查询**(phrase query) "chinese love china", 第一阶段先找所有包含“chinese”、“love”、“china”三个term的文档。第二阶段再在第一阶段匹配到到的所有文档中计算“chinese”,"love","china"三个单词的**位置和顺序**是否满足条件，这一操作**非常耗时**，所以通过第一阶段缩小匹配文档的范围。

- create_weight: 创建weight过程的耗时，weight就相当于lucene查询的context，里面包含了query，collector，indexreader等。

- *_count: 记录方法调用次数，比如next_doc_count:2，代表next_doc方法被调用了两次。

除了query过程的详细统计，还包括：

- rewrite_time: **query语句被重写的耗时**，lucene自己维护了一套查询语句重写逻辑，比如terms查询中如果要查询的**terms个数小于16**，会被重写成多个TermQuery做**or结合**；如果大于16会被重写成**TermInSetQuery**。

- collector: query数据收集阶段的各种指标。包括query用到的collector的个数，类型和耗时。ES默认使用的是SimpleTopScoreDocCollector。lucene的collector主要通过reduce方法对每个segment上匹配的结果进行**合并和排序**，返回topN。
