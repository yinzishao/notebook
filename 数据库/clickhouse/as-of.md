- [five-ways-to-handle-as-of-queries-in-clickhouse](https://altinity.com/blog/2020/4/8/five-ways-to-handle-as-of-queries-in-clickhouse)


```sql
CREATE TABLE billy.readings (
    sensor_id Int32 Codec(DoubleDelta, LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    temperature Decimal(5,2) Codec(T64, LZ4)
) Engine = MergeTree
PARTITION BY toYYYYMM(time)
ORDER BY (sensor_id, time);

```

# Join approach

```sql
SELECT *
FROM readings
INNER JOIN
(
    SELECT
        sensor_id,
        max(time) AS time
    FROM readings
    WHERE (sensor_id = 12345) AND (date <= '2019-08-01')
    GROUP BY sensor_id
) AS last USING (sensor_id, time)
WHERE sensor_id = 12345
```

```
┌─sensor_id─┬────────────────time─┬─temperature─┐
│     12345 │ 2019-08-01 23:59:00 │       40.38 │
└───────┴─────────────────────┴─────────────┘
1 rows in set. Elapsed: 0.062 sec. Processed 1.98 million rows, 19.82 MB (31.91 million rows/s., 319.07 MB/s.)
```

# Tuple IN approach

```sql
SELECT *
FROM readings
WHERE (sensor_id, time) IN
(
    SELECT
        sensor_id,
        max(time)
    FROM readings
    WHERE (sensor_id = 12345) AND (date <= '2019-08-01')
    GROUP BY sensor_id
)
```

```
┌─sensor_id─┬────────────────time─┬─temperature─┐
│     12345 │ 2019-08-01 23:59:00 │       40.38 │
└───────────┴─────────────────────┴─────────────┘
1 rows in set. Elapsed: 0.030 sec. Processed 8.19 thousand rows, 98.30 KB (269.64 thousand rows/s., 3.24 MB/s.)

```

# Aggregate function approach

```sql
SELECT
    sensor_id,
    max(time),
    argMax(temperature, time)
FROM readings
WHERE (sensor_id = 12345) AND (date <= '2019-08-01')
GROUP BY sensor_id
```


```
┌─sensor_id─┬───────────max(time)─┬─argMax(temperature, time)─┐
│     12345 │ 2019-08-01 23:59:00 │                     40.38 │
└───────────┴─────────────────────┴───────────────────────────┘
1 rows in set. Elapsed: 0.054 sec. Processed 991.23 thousand rows, 11.89 MB (18.26 million rows/s., 219.17 MB/s.)
```

# ASOF JOIN

```sql
SELECT readings.*
FROM
(
    SELECT
        toInt32(12345) AS sensor_id,
        toDateTime('2019-08-01 23:59:00') AS time
) AS base
ASOF INNER JOIN readings USING (sensor_id, time)
WHERE readings.sensor_id = 12345
```

```
┌─readings.sensor_id─┬───────readings.time─┬─temperature─┐
│              12345 │ 2019-08-01 23:59:00 │       40.38 │
└────────────────────┴─────────────────────┴─────────────┘
1 rows in set. Elapsed: 0.069 sec. Processed 991.23 thousand rows, 11.89 MB (14.31 million rows/s., 171.76 MB/s.)
```

- [asof-join-usage](https://clickhouse.tech/docs/en/sql-reference/statements/select/join/#asof-join-usage): 当需要连接不完全匹配的记录时，ASOF JOIN很有用。

注意：
1. 对于使用asof_column 字段的使用有两点需要注意:asof_column 必须是整形，浮点型和日期类型 这种有序序列的数据类型
2. asof_column 不能是数据表内的唯一字段 即连接JOIN KEY 和ASOF_column 不能是同一个字段。


```sql
select * from
(
    SELECT
        119731843 AS ad_id,
        toDateTime('2020-12-12 00:47:23') AS modify_time
) AS base
ASOF LEFT JOIN mt.ad_effect
on (
    ad_effect.ad_id = base.ad_id
    and ad_effect.stat_time = '2020-12-11'
) and ad_effect.modify_time <= base.modify_time
where stat_time = '2020-12-11' and ad_id in (119731843, 127855423)  order by ad_id, modify_time
```
> 需要ad_id索引？否则是全量的，stat_time分区因为是join的，所有分区过滤都没有命中？执行计划有点问题，有点难使用。


# LIMIT BY
```sql
SELECT *
FROM readings
WHERE (sensor_id = 12345) AND (date <= '2019-08-01')
ORDER BY
    sensor_id ASC,
    time DESC
LIMIT 3 BY sensor_id
```

```
┌─sensor_id─┬────────────────time─┬─temperature─┐
│     12345 │ 2019-08-01 23:59:00 │       40.38 │
└───────────┴─────────────────────┴─────────────┘
1 rows in set. Elapsed: 0.095 sec. Processed 991.23 thousand rows, 11.89 MB (10.39 million rows/s., 124.63 MB/s.)
```

在这篇简短的文章中，我们展示了时间序列应用程序中典型的as-of-query的不同方法。
- 具有良好匹配索引的最快方法是IN方法＃2。
- 而具有argMax聚合功能的＃3更通用，可以与聚合实例化视图一起使用。

其他方法更具局限性，但在某些场景更有效率。
- 当按条件查询扩展到其他要求时，例如将两个时间序列与ASOF JOIN拼接在一起
- 或返回多个而不是返回单个时，用LIMIT BY效率更高。
