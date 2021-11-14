# 配置

- [配置文件说明](https://www.cnblogs.com/zhoujinyi/p/12627780.html): 配置的相关文档与实践配置
- [配置reload](https://clickhouse.tech/docs/en/operations/configuration-files/#implementation-details): 默认会自动加载配置变更后的选项

```sql
SELECT name, value FROM system.settings WHERE name LIKE 'max_threads';
SELECT name, value FROM system.settings WHERE name LIKE 'log_queries';
```

## query_log

1. ClickHouse 默认的情况下 query_log 表是未开启的状态，必须将其开启，修改配置文件 users.xml，路径为 /etc/clickhouse-server/，新增配置项`<log_queries>1</log_queries>`，当查询日志服务器参数 log_queries=1 时，ClickHouse 才会创建此表。

2. 每个查询在 query_log 表中会创建一条或两条记录，具体取决于查询的状态：

- 如果查询执行成功，则会分别创建事件类型为 1 和 2 的两条记录；
- 如果在查询处理期间发生错误，则会分别创建事件类型为 1 和 4 的两条记录；
- 如果在查询启动之前发生错误，则会创建事件类型为 3 的单条记录。

3. 表 query_log 中的记录，存储的是历史查询在集群中的各个节点的状态，其中包括查询 query_id 的父子关系及对应的节点信息、各个节点的查询脚本、查询开始时间、查询日期、查询时间、查询耗时、查询行数、查询结果的字节大小、请求使用的内存、高峰使用的内存、参与查询的线程数、堆栈跟踪以及查询异常信息等。


```sql
--
select * from system.query_log;
SELECT  user,
    client_hostname AS host,
    client_name AS client,
    formatDateTime(query_start_time, '%T') AS started,
    query_duration_ms / 1000 AS sec,
    round(memory_usage / 1048576) AS MEM_MB,
    result_rows AS RES_CNT,
    toDecimal32(result_bytes / 1048576, 6) AS RES_MB,
    read_rows AS R_CNT,
    round(read_bytes / 1048576) AS R_MB,
    written_rows AS W_CNT,
    round(written_bytes / 1048576) AS W_MB,
    query
  FROM system.query_log
WHERE type = 2
ORDER BY query_duration_ms DESC
LIMIT 10
```

### settings-log-comment

指定system.query_log表的log_comment字段的值和服务器日志的注释文本。

它可用于提高服务器日志的可读性。此外，它还可以在运行clickhouse-test之后从system.query_log中选择与测试相关的查询。

```sql
SET log_comment = 'log_comment test', log_queries = 1;
SELECT 1;
SYSTEM FLUSH LOGS;
SELECT type, query FROM system.query_log WHERE log_comment = 'log_comment test' AND event_date >= yesterday() ORDER BY event_time DESC LIMIT 2;
```

### 参考链接
- [settings-log-comment](https://clickhouse.tech/docs/en/operations/settings/settings/#settings-log-comment)
- [system-tables](https://clickhouse.tech/docs/en/operations/system-tables/#system-tables)
- [server_configuration_parameters-query-log](https://clickhouse.tech/docs/en/operations/server-configuration-parameters/settings/#server_configuration_parameters-query-log)
- [settings-log-queries](https://clickhouse.tech/docs/en/operations/settings/settings/#settings-log-queries)

- [sql-for-clickhouse-dba](https://altinity.com/blog/2020/5/12/sql-for-clickhouse-dba)
- [苏宁基于 ClickHouse 的大数据全链路监控实践](https://cloud.tencent.com/developer/article/1696928)

> 20版本才加engine配置、21版本才加ttl配置。先手动加上ttl。

```sql

ALTER TABLE system.query_log MODIFY TTL event_date + INTERVAL 1 DAY;
```

---

## max_memory_usage_for_all_queries

2020版本废弃：

添加了设置max_server_memory_usage以限制服务器的总内存使用量。现在，可以无度量地计算指标“ MemoryTracking”。设置max_memory_usage_for_all_queries现在已过时且不执行任何操作

> 而且在本地测试发现，在这个配置下，19版本的并发查询还是会超过该设置，导致OOM。

## max_bytes_in_join

默认情况下，ClickHouse使用哈希连接算法。ClickHouse获取<right table>并在RAM中为它创建一个哈希表。在内存消耗达到一定阈值后，ClickHouse会返回到merge-join算法。如果需要限制联接操作内存消耗

Code: 191. DB::Exception: Received from localhost:9000. DB::Exception: Limit for JOIN exceeded, max bytes: 95.37 MiB, current bytes: 96.00 MiB.

如果将join设置得比**允许的内存**大，则不允许在磁盘上join。如果您不希望此类查询的性能受到影响，而希望使用异常，那么这种情况本身就很有用。

这里的另一点是，max_bytes_in_join/max_rows_in_join设置会分别影响查询中的每个JOIN。因此，如果您有**2个联接并且限制为1Gb**，则**最多**可能会吃掉2Gb。

- [max_bytes_in_join](https://github.com/ClickHouse/ClickHouse/issues/9702): join的消费内存比配置的内存要大
- [join:memory-limitations](https://clickhouse.tech/docs/en/sql-reference/statements/select/join/#memory-limitations): join的hashtable的内存限制
- [partial_merge_join_optimizations](https://clickhouse.tech/docs/en/operations/settings/settings/#partial_merge_join_optimizations)

```sql

set max_memory_usage=1000000000;

SELECT number
FROM numbers(1) AS a
ANY LEFT JOIN numbers(100000000) AS b USING (number);

```

> 并发情况下，Memory limit (total) 也是会正常触发的

## max_bytes_before_external_group_by

在进行group by的时候，内存使用量已经达到了max_bytes_before_external_group_by的时候就进行写磁盘(基于磁盘的group by相对于基于磁盘的order by性能损耗要好很多的)，如果设置为0（默认值），则将其禁用。一般max_bytes_before_external_group_by设置为max_memory_usage / 2，原因是在clickhouse中聚合分两个阶段：

- 查询并且建立中间数据；

- 合并中间数据

写磁盘在第一个阶段，如果无须写磁盘，clickhouse在第一个和第二个阶段需要使用相同的内存。

这些内存参数强烈推荐配置上，增强集群的稳定性避免在使用过程中出现莫名其妙的异常。

> 这个配置是数据溢出的内存配置?没搞懂！一个原则就是配置为max_memory_usage / 2

- [select-group-by-in-external-memory](https://clickhouse.tech/docs/en/sql-reference/statements/select/group-by/#select-group-by-in-external-memory): RAM的最大消耗仅略大于max_bytes_before_external_group_by


## max_execution_speed

每秒最大执行行数。当“ timeout_before_checking_execution_speed”到期时，检查每个数据块。如果执行速度很高，执行速度将降低

- [max-execution-speed](https://clickhouse.tech/docs/en/operations/settings/query-complexity/#max-execution-speed)


### merge-max-block-size

The number of rows that are read from the merged parts into memory.

> 合并从merge_max_block_size行的块中的parts读取行，然后合并并将结果写入新parts。读取的块放置在RAM中，因此merge_max_block_size影响合并所需的RAM大小。因此，对于行非常宽的表，合并会消耗大量RAM（如果平均行大小为100kb，则合并10个parts时：(100kb * 10 * 8192) = ~ 8GB of RAM).。通过减少merge_max_block_size，可以减少合并所需的RAM数量，但会降低合并速度。

- [merge-max-block-size](https://clickhouse.tech/docs/en/operations/settings/merge-tree-settings/#merge-max-block-size)


## uncompressed_cache_size

合并树中表引擎使用的未压缩数据的缓存大小

服务器有一个共享缓存。内存按需分配。如果启用了“use_uncompressed_cache”选项，则使用缓存。

在个别情况下，未压缩缓存对于非常短的查询是有利的。

- [uncompressed_cache_size](https://clickhouse.tech/docs/en/operations/server-configuration-parameters/settings/#server-settings-uncompressed_cache_size)

### use_uncompressed_cache

是否使用未压缩块的缓存。接受0或1。默认情况下，0（禁用）。

在处理大量短查询时，使用未压缩缓存（仅适用于MergeTree系列中的表）可以显著**减少延迟并提高吞吐量**。为**频繁发送短请求**的用户启用此设置。还要注意 uncompressed_cache_size配置参数（仅在配置文件中设置）–未压缩缓存块的大小。默认情况下，它是8 GiB。根据需要填充未压缩的缓存，并自动删除最少使用的数据。

对于读取的数据量至少有点大（一百万行或更多）的查询，将**自动禁用未压缩缓存**，以便为真正的小查询节省空间。这意味着您可以将“use_uncompressed_cache”设置始终设置为1。

> 导致clickhouse占用了8G常驻内存空间进行未压缩的数据的缓存。可是在19版本并没有开启use_uncompressed_cache，还是常驻了8G

- [use_uncompressed_cache](https://clickhouse.tech/docs/en/operations/settings/settings/#setting-use_uncompressed_cache)



---
# 排查cpu

```bash
sudo perf top -p $(pidof clickhouse-server)
sudo gdb -p $(pidof clickhouse-server) + thread apply all bt
```
---
# python的client

- [clickhouse-driver](https://clickhouse-driver.readthedocs.io/en/latest/)

ClickHouse服务器提供程序用于通信的两个协议：HTTP协议和Native（TCP）协议。

每种协议都有各自的优缺点。这里我们重点介绍本机协议的优点：

- Native协议更易于通过各种设置进行配置。

- 二进制数据传输比文本数据更紧凑。

- 从二进制数据构建python类型比从文本数据构建python类型更有效。

- LZ4压缩比gzip快。在HTTP协议中使用Gzip压缩。

- 查询配置文件信息可通过本机协议获得。例如，我们可以读取limit metric之前的行

- 需要注意时间的格式，不支持字符。而且类型强校验，字符不能是int。跳过类型校验, 可以直接通过curl命令直接执行，不经过client


---
