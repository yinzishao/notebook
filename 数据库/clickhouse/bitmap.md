## 位图

位图对象的构造方法有2种。一个将由带有-State的聚合函数groupBitmap构造，另一个将由Array Object构造。也可以将位图对象转换为数组对象。

在实际存储位图对象时，RoaringBitmap被包装到一个数据结构中。当基数小于或等于32时，它使用Set objet。当基数大于32时，它使用RoaringBitmap对象。这就是为什么低基数集的存储速度更快。


### 使用场景
- 留存分析
- 新上榜数据（对比上一个维度的结果）
- 归档压缩

## 基本使用

### Array Object构造
```sql
WITH bitmapBuild([32, 65, 127, 1026]) AS bm
SELECT bm,toTypeName(bm);
```

┌─bm─┬─toTypeName(bm)─────────────────────────┐
│  A │ AggregateFunction(groupBitmap, UInt16) │
└────┴────────────────────────────────────────┘

### 将由带有-State的聚合函数groupBitmap构造
```sql

select groupBitmapState(id) as bm, toTypeName(bm)  from (
    select 1 as id, 100 as b
    union all
    select 2 as id, 100 as b
) group by b
```

┌─bm─┬─toTypeName(groupBitmapState(id))──────┐
│    │ AggregateFunction(groupBitmap, UInt8) │
└────┴───────────────────────────────────────┘

1 rows in set. Elapsed: 0.002 sec.


位图在CH中的本质是AggregateFunction(groupBitmap, UInt*)类型的（*由位图中的最大值弹性决定），即groupBitmap这个聚合函数产生的中间结果。

？： 根据聚合函数的combinator语法，可以结合-Merge后缀等。

---
# 生产案例

构造一个广告id位图字段，以此来表达mt.ad_log表

```sql
CREATE TABLE test_bit_ad_log
(
    `area` String,
    `ad_id_bm` AggregateFunction(groupBitmap, UInt32),
    `position` UInt32,
    `platform` UInt32,
    `format` Int32,
    `media` UInt32,
    `appid` UInt32,
    `channel` UInt32,
    `dt` Date
)
ENGINE = AggregatingMergeTree()
PARTITION BY dt
ORDER BY (dt, platform, format, media, appid, channel, position, area)

INSERT INTO test_bit_ad_log (dt, platform, format, media, appid, channel, position, area, ad_id_bm) SELECT
    dte,
    platform,
    format,
    media,
    appid,
    channel,
    position,
    area,
    groupBitmapState(ad_id)
FROM mt.test_ad_log
GROUP BY
    dte,
    platform,
    format,
    media,
    appid,
    channel,
    position,
    area;
```

## groupBitmapAndState

```sql
--  bitmapToArray 展开bitmap
select dt, platform, format, media, appid, channel, position, area, bitmapToArray(ad_id_bm)  from test_bit_ad_log;

-- groupBitmapOrState、 groupBitmapAndState 通过 -state 获取聚合的中间状态
select length(bitmapToArray(groupBitmapOrState(ad_id_bm))) from mt.test_bit_ad_log where dt = '2020-10-13' and platform = 1 group by dt

-- 等于上面
select count(distinct ad_id) from mt.ad_log where dt = '2020-10-13' and platform = 1
```

## 压缩成果：

```
┌─database─┬─table──┬─size─┬─ratio┬─partitions─┬─compression_ratio─┬─parts─┬─min_date─┬─max_date─┬ut─┬rows─┐
mt  ad_log  199.22 MiB  1.86%   100	0.10	100	2020-07-29	2020-12-13	2020-12-13 14:18:08     49,741,623
mt  ad_log_dt   12.05 MiB   0.11%   100	0.13	105	2020-07-29	2020-12-13	2020-12-13 19:10:35     2,571,216
mt  test_bit_ad_log 2.90 MiB    0.03%   100	0.50	100	2020-07-29	2020-12-13	2020-12-13 18:49:30     21,303
```
> 压缩率： 3/12=25%。不能跟ad_log进行对比，因为废弃了很多字段，特别是精确到秒时间。应该是跟按天维度的数据进行对比。

```
┌─database─┬─table──┬─size─┬─ratio┬─partitions─┬─compression_ratio─┬─parts─┬─min_date─┬─max_date─┬ut─┬rows─┐
mt  test_ad_log 285.93 MiB  2.44%   1	0.12	5	2020-12-01	2020-12-01	2020-12-20 20:56:38	48,852,386
mt  ad_log_dt   26.15 MiB   0.22%   1	0.18	4	2020-12-01	2020-12-01	2020-12-20 20:58:29	3,971,254
mt  test_bit_ad_log 11.86 MiB   0.1%    1	0.67	1	2020-12-01	2020-12-01	2020-12-20 20:59:56	53,667
```
> 压缩率： 11.86/26.15=45.35%

```
┌─database─┬─table──┬─size─┬─ratio┬─partitions─┬─compression_ratio─┬─parts─┬─min_date─┬─max_date─┬ut─┬rows─┐
mt  test_ad_log 830.90 MiB  6.73%   3	0.12	21	2020-12-01	2020-12-03	2020-12-20 21:12:25	138,779,440
mt  ad_log_dt   78.96 MiB   0.64%   3	0.18	11	2020-12-01	2020-12-03	2020-12-20 21:13:26	11,883,406
mt  test_bit_ad_log 35.38 MiB   0.29%   3	0.67	3	2020-12-01	2020-12-03	2020-12-20 21:13:58	159,698
```
> 压缩率： 35.38/78.96=44.80%



## 查询效率

```sql
-- 原始表获取
SELECT countDistinct(ad_id)
FROM mt.test_ad_log
WHERE (platform = 2) AND (format = 102) AND (media > 3)

┌─uniqExact(ad_id)─┐
│            83555 │
└──────────────────┘

1 rows in set. Elapsed: 0.597 sec. Processed 138.78 million rows, 685.49 MB (232.43 million rows/s., 1.15 GB/s.)
```

```sql
SELECT countDistinct(ad_id)
FROM mt.ad_log_dt
WHERE (platform = 2) AND (format = 102) AND (media > 3)

┌─uniqExact(ad_id)─┐
│            83555 │
└──────────────────┘

1 rows in set. Elapsed: 0.112 sec. Processed 11.88 million rows, 60.14 MB (106.37 million rows/s., 538.31 MB/s.)

```


```sql

-- 位图压缩表进行数据的获取。可能是量级不够多，稍微快了些。
SELECT groupBitmapOr(ad_id_bm)
FROM mt.test_bit_ad_log
WHERE (platform = 2) AND (format = 102) AND (media > 3)

┌─groupBitmapOr(ad_id_bm)─┐
│                   83555 │
└─────────────────────────┘

1 rows in set. Elapsed: 0.057 sec. Processed 24.58 thousand rows, 389.66 KB (430.72 thousand rows/s., 6.83 MB/s.)
```

> 优化速率还是挺大的: 0.057/0.112=50.89%

## 恢复，列拆行
```sql
-- 展开位图列，变成原始表
SELECT *
FROM
(
    SELECT
        dt,
        platform,
        format,
        media,
        appid,
        channel,
        position,
        area,
        bitmapToArray(groupBitmapOrState(ad_id_bm)) AS ad_ids
    FROM mt.test_bit_ad_log
    WHERE (platform = 2) AND (format = 102) AND (media > 3)
    GROUP BY
        dt,
        platform,
        format,
        media,
        appid,
        channel,
        position,
        area
)
ARRAY JOIN ad_ids
LIMIT 1

50939 rows in set. Elapsed: 0.096 sec. Processed 19.58 thousand rows, 287.52 KB (204.10 thousand rows/s., 3.00 MB/s.)

```


```sql
-- 获取原始表的数据
SELECT countDistinct(dt, platform, format, media, appid, channel, position, area, ad_id) AS cnt
FROM mt.ad_log
WHERE (platform = 2) AND (format = 102) AND (media > 3)


┌───cnt─┐
│ 50939 │
└───────┘

1 rows in set. Elapsed: 0.237 sec. Processed 49.74 million rows, 122.94 MB (209.49 million rows/s., 517.78 MB/s.)

```

---
## 聚合天
```sql
create table ad_log_dt
(
    area           String,
    ad_id          UInt32,
    ad_creative_id UInt32,
    position       UInt32,
    platform       UInt32,
    format         Int32,
    media          UInt32,
    appid          UInt32,
    channel        UInt32,
    dt             Date
) engine = MergeTree() partition by (dt) order by (ad_id);

INSERT INTO ad_log_dt (dt, platform, format, media, appid, channel, position, area, ad_id) SELECT
distinct
    dte,
    platform,
    format,
    media,
    appid,
    channel,
    position,
    area,
    ad_id
FROM mt.test_ad_log;

```

---
## 不足思考

问题： 只能获取基数或者列表。join相关的操作如何处理？场景：获取这些结果的其他属性的聚合值？

可以通过类似这样的操作：
```sql
select * from ad_effect where ad_id in (
    select bitmapToArray(ad_id) from ad_log
)
```

可是还有问题，一般的场景ad_log会获取附带的维度属性，并且要通过ad_effect的join一起获取过滤

```sql
select * from ad_effect where (ad_id, channel, platform, format) in (
    select bitmapToArray(ad_id), channel, platform, format from ad_log
)
```

这样的类似操作，应该不能？

只能在ad_log获取到位图后，重新展开。这样的性能应该会下降一个量级。还不如直接展开位图的ad_id聚合表呢。

> 还是得看使用场景。如果单纯拿列表，还是挺好的（单纯的新上榜过滤）。如果需要附带维度聚合，涉及到重新展开，效率应该不如。

---
总的来说，本方案的优点是：

- 存储小，极大地节约了存储；
- 查询快，利用bitmapCardinality、bitmapAnd、bitmapOr等位图函数快速计算用户数和满足一些条件的查询，将缓慢的join操作转化成位图间的计算；
- 适用于灵活天数的留存查询；
- 便于更新，用户操作数据和用户属性数据分开存储，便于后续属性的增加和数据回滚。


---
# 参考链接：
- [ClickHouse留存分析工具十亿数据秒级查询方案](https://mp.weixin.qq.com/s/Bh5aEvpBgSEDkTozpfMFkw): 通过位图的，优化留存用户的分析。有具体代码与总结、参考文献。
- [ClickHouse遇见RoaringBitmap](https://blog.csdn.net/nazeniwaresakini/article/details/108166089): 引出AggregateFunction、源码分析。
- [bitmap-functions](https://clickhouse.tech/docs/en/sql-reference/functions/bitmap-functions/): 官方文档

---
# 备忘录


```sql

insert into test_ad_log (dte, area, ad_id, ad_creative_id, ad_create, platform, format, media, appid, position, cnt, ut)
SELECT formatDateTime(toDateTime(dt), '%Y-%m-%d') as dte , area, ad_id, ad_creative_id, toUnixTimestamp(ad_create) as ad_create, platform, format, media, appid, position, cnt, toUnixTimestamp(ut) as ut
from mt.ad_log where dt = '2020-12-01';

```
