# 副本测试

```yaml

    <zookeeper>
        <node index="1">
            <host>zookeeper</host>
            <port>2181</port>
        </node>
    </zookeeper>

    <macros>
        <cluster>company_cluster</cluster>
        <shard>${SHARD}</shard>
        <replica>clickhouse${REPLICA}</replica>
    </macros>

```


```sql
-- clickhouse01
CREATE TABLE events (
    time DateTime,
    uid  Int64,
    type LowCardinality(String)
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/table', '{replica}')
PARTITION BY toDate(time)
ORDER BY (uid);


INSERT INTO events VALUES
    ('2020-01-01 10:00:00', 100, 'view'),
    ('2020-01-01 10:05:00', 101, 'view'),
    ('2020-01-01 11:00:00', 100, 'contact'),
    ('2020-01-01 12:10:00', 101, 'view'),
    ('2020-01-02 08:10:00', 100, 'view'),
    ('2020-01-03 13:00:00', 103, 'view');

INSERT INTO events  select now(), number, number from system.numbers limit 1000;

-- clickhouse02再次创建events，作为副本

select  * from events
```

> clickhouse02副本数据会自动同步

```sql
-- clickhouse03再次创建events，作为副本
```

> 在clickhouse03创建events表，并不能同步，因为宏定义为分片02

通过查询zk得到现在的副本信息:
```sql
SELECT * FROM system.zookeeper where path = '/clickhouse/tables/company_cluster/01/table/replicas'\G
```

## Q: 改表操作能同步到副本吗？


```sql
-- clickhouse01更改表
alter table events MODIFY COLUMN `type` String;

-- clickhouse03更改表
alter table events MODIFY COLUMN `type` LowCardinality(String);

```

A: 相关副本都能进行同步更改改表操作

> 先停掉副本的一个节点，更改主副本其他的表结构，再恢复副本。该副本也是能同步数据和表结构。

## 同名副本

ReplicatedMergeTree('zk_path','replica_name')，如果在另一台机器上创建一个已经在zk注册上的同一个replica_name，新表的数据并不会进行同步。

### Q: 新数据的插入会同步到同步副本上吗？？
A: 只会同步到第一个启动的同名副本上。

### Q: 停掉第一个启动启动的同步副本呢？后启动的同步副本会同步数据吗？
A: 不会，后启动的副本依然没有数据。插入副本也不会同步到相关的后启动副本。

### Q: 插入后启动的同名副本的数据，会同步到其他副本上吗？
A: 插入后启动的同名副本不会同步到其他副本上，

结论： 如果在另一台机器上创建一个已经在zk注册上的同一个replica_name。表现为该表是一个跟其他表毫无关联的表。


## Q： drop table 会影响其他副本的数据吗？
A： 并不能。需要集群操作了。

## Q: replace partition 会影响其他副本的数据吗？

```sql
CREATE TABLE events_2
(
    `time` DateTime,
    `uid` Int64,
    `type` LowCardinality(String)
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/table_2', '{replica}')
PARTITION BY toDate(time)
ORDER BY uid

INSERT INTO events_2 VALUES
    ('2020-01-01 10:00:00', 200, 'view'),
    ('2020-01-01 10:05:00', 201, 'view'),
    ('2020-01-01 11:00:00', 200, 'contact'),
    ('2020-01-01 12:10:00', 201, 'view'),
    ('2020-01-02 08:10:00', 200, 'view'),
    ('2020-01-03 13:00:00', 203, 'view');

ALTER TABLE events REPLACE PARTITION '2020-01-01' FROM events_2

ALTER TABLE events_2 move PARTITION '2020-01-02' to table events
```

A: 可以看到events的主从副本的相关分区都正常变成event2的数据。证明分区操作可以正常应用。
