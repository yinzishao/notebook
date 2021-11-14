# 基本命令

## 时间函数

```sql
select
    from_unixtime(1625414397, '%Y-%m-%d %H:%i:%s'),
    to_unixtime('2021-07-04 15:04:47')
```

```sql
-- 取小时级别数据
select 1612105800 - 1612105800%3600, (1612105200 + 600) %3600, 1612105200 + 3600
-- 1612105200	0	1612108800
```


```sql
-- 时间戳时间范围内的天数取值
select cast(ts as date) as dt
from (values (sequence( date_format(from_unixtime(1628783000), '%Y-%m-%d')  , date_format(from_unixtime(1628784001), '%Y-%m-%d') , interval 1 day))) as t1(date_array)
cross join unnest(date_array) as t2(ts)
order by dt desc limit 3
```


```sql
-- 生成小时级别数据行
select
  ts as beg_ts,
  ts + 600 as end_ts,
  date_format(from_unixtime(ts), '%Y-%m-%d') as dt,
  date_format(from_unixtime(ts), '%H') as hr
from
  (
    values
      (
        sequence(
          to_unixtime('2021-07-14 01:20:00'),
          to_unixtime('2021-07-15 11:00:00') -1,
          600
        )
      )
  ) as t1(date_array)
  cross join unnest(date_array) as t2(ts)

-- 取10分钟区间
select from_unixtime( floor(1626338140 / 600) * 600 ), sequence({{beg_ts}} - {{beg_ts}} % 600

-- 时间解析和转换
select date_format(date_sub(date_parse('{{dt}}', '%Y-%m-%d'), INTERVAL 1 DAY), '%y-%m-%d')

-- 获取开始结束时间的10分钟分割
select
  from_unixtime(beg_ts, '%Y-%m-%d %H:%i:%s'),
  from_unixtime(end_ts, '%Y-%m-%d %H:%i:%s'),
  from_unixtime({{beg_ts}}, '%Y-%m-%d %H:%i:%s'),
  from_unixtime({{end_ts}}, '%Y-%m-%d %H:%i:%s'),
  beg_ts, end_ts, date_format(from_unixtime(beg_ts), '%Y-%m-%d') as dt
from
  (
    select
      ts,
      if(
        floor(ts / 600) * 600 < {{beg_ts}},
        {{beg_ts}},
        floor(ts / 600) * 600
      ) as beg_ts,
      if(
        floor(ts / 600) * 600 + 600 > {{end_ts}},
        {{end_ts}},
        floor(ts / 600) * 600 + 600
      ) as end_ts
    from
      (
        /* 注意这里的beg_ts 取10分钟的整了，避免开始结束小于600秒且跨10分钟，只能有一条，无法正确拿到最新10分钟的截取和最新时间区间 *//
        values
          (sequence({{beg_ts}} - {{beg_ts}} % 600 , {{end_ts}}

          , 600))
      ) as t1(date_array)
      cross join unnest(date_array) as t2(ts)
  )

```



## 类型转换

转换函数

cast(value AS type) → type

显式把value转换到type类型。可用于把字符类型值转变为数值类型，反之亦然。

**typeof**(expr) → varchar

返回 expr 表达式的结果类型:

```sql
SELECT typeof(123); -- integer

SELECT typeof('cat'); -- varchar(3)

SELECT typeof(cos(2) + 1.5); -- double
```

## 一行拆多行

```sql
select dt from (
    select ARRAY [SUBDATE(current_date, 1), SUBDATE(current_date, 2)] as map_data
) cross join unnest(map_data) as t(dt)


SELECT t.m, t.n
FROM (
  SELECT MAP(ARRAY['foo', 'bar'], ARRAY[1, 2]) as map_data
)
CROSS JOIN unnest(map_data) AS t(m, n);

```

```sql

show partition test.quantity_sold

MSCK REPAIR TABLE test.quantity_sold
```

## 窗口函数
datax
```sql
-- 商品销量表（窗口函数展示）
select id, time, sales from
(
    values
    (1, '2020-07-26 00:00:00', 200), (1, '2020-07-26 01:00:00', 100),　(1, '2020-07-26 02:00:00', 300),　(1, '2020-07-26 03:00:00', 250),
    (1, '2020-07-26 04:00:00', 150), (2, '2020-07-26 00:00:00', 220),  (2, '2020-07-26 01:00:00', 400),  (2, '2020-07-26 02:00:00', 80)
) as t(id, time, sales)

-- 分组排名（窗口函数展示）
select id, time, sales, rank() over (partition by id order by sales desc) as rank from
(
    values
    (1, '2020-07-26 00:00:00', 200), (1, '2020-07-26 01:00:00', 100),　(1, '2020-07-26 02:00:00', 300),　(1, '2020-07-26 03:00:00', 250),
    (1, '2020-07-26 04:00:00', 150), (2, '2020-07-26 00:00:00', 220),  (2, '2020-07-26 01:00:00', 400),  (2, '2020-07-26 02:00:00', 80)
) as t(id, time, sales)

-- 分组取排序后的第一条/最后一条记录值（窗口函数展示）
select distinct id, first_value(sales) over (partition by id order by time) as sales from
(
    values
    (1, '2020-07-26 00:00:00', 200), (1, '2020-07-26 01:00:00', 100),　(1, '2020-07-26 02:00:00', 300),　(1, '2020-07-26 03:00:00', 250),
    (1, '2020-07-26 04:00:00', 150), (2, '2020-07-26 00:00:00', 220),  (2, '2020-07-26 01:00:00', 400),  (2, '2020-07-26 02:00:00', 80)
) as t(id, time, sales)

-- 取上一条/下一条记录值(计算差值)
select id, time, sales, lag(sales) over (partition by id order by time) as last_sales, lag(sales) over (partition by id order by time) - sales as incr from
(
    values
    (1, '2020-07-26 00:00:00', 200), (1, '2020-07-26 01:00:00', 100),　(1, '2020-07-26 02:00:00', 300),　(1, '2020-07-26 03:00:00', 250),
    (1, '2020-07-26 04:00:00', 150), (2, '2020-07-26 00:00:00', 220),  (2, '2020-07-26 01:00:00', 400),  (2, '2020-07-26 02:00:00', 80)
) as t(id, time, sales)

-- 聚合函数（窗口函数展示）
select id, time, sales, max(sales) over (partition by id order by time) as sales from
(
    values
    (1, '2020-07-26 00:00:00', 200), (1, '2020-07-26 01:00:00', 100),　(1, '2020-07-26 02:00:00', 300),　(1, '2020-07-26 03:00:00', 250),
    (1, '2020-07-26 04:00:00', 150), (2, '2020-07-26 00:00:00', 220),  (2, '2020-07-26 01:00:00', 400),  (2, '2020-07-26 02:00:00', 80)
) as t(id, time, sales)
```


## max_by

```
max_by(x, y, n) → array<[same as x]>
```

返回与 y 的前 n 个最大值相关的 x 值的数组。

此方法很强，例如 统计销量前五的供应商  max_by(供应商,销量,5)  ，可以替代一些使用row_number后再取前五的操作，会比row_number 性能更好 。

```sql
/* max_by  min_by  order by

没有order 则是 根据 partition by 拿到窗口的 最大最小值，然后赋值给每一行

注意order by的结果有些奇怪：

根据order by 进行排序，然后顺序维护一个窗口，找出相应的最大最少值？
*/
(
select
id, site_id, min_by(sales, sales) over (partition by id
-- order by site_id desc
) , max_by(sales, sales) over (partition by id
-- order by site_id desc
)
from
(
    values
    (1, 0, 200, 10501),
    (1, 1, 100, 10502),
    (1, 2, 300, 10501),
    (1, 3, 250, 10502),
    (1, 4, 150, 10501),

    (2, 2, 220, 10501),
    (2, 1, 400, 10501),
    (2, 0, 80, 10501)
) as t(id, time, sales, site_id)
)

```


---
## reduce

```sql
SELECT reduce(ARRAY [], 0, (s, x) -> s + x, s -> s); -- 0

SELECT reduce(ARRAY [5, 20, NULL, 50], 0, (s, x) -> s + COALESCE(x, 0), s -> s); -- 75

SELECT reduce(ARRAY [5, 6, 10, 20], -- calculates arithmetic average: 10.25
              CAST(ROW(0.0, 0) AS ROW(sum DOUBLE, count INTEGER)),
              (s, x) -> CAST(ROW(x + s.sum, s.count + 1) AS ROW(sum DOUBLE, count INTEGER)),
              s -> IF(s.count = 0, NULL, s.sum / s.count))
-- 10.25
--  s -> s  {sum=41.0, count=4}
```

- [reduce](https://zhuanlan.zhihu.com/p/379524622)


```sql

SELECT
  reduce(
    /* 落地页销量  精确销量  新增销量   */
    zip(
      ARRAY [220, 230, 230],
      ARRAY [null, 233, null],
      ARRAY [10, 10, 10]
    ),
    cast(
      ROW(ARRAY [200], 200) AS ROW(array ARRAY(BIGINT), last_qs BIGINT)
    ),
    (s, x) -> cast(
      ROW(
        s.array || if(
          x [2] is not null,
          greatest(x [2], nvl(element_at(s.array, -1), 0)),
          if(
            x [1] < 100,
            greatest(x [1], nvl(element_at(s.array, -1), 0)),
            /* 落地页销量大于库存新增销量与上次累计销量之和的，取落地页销量作为本次累计销量 */
            if(
              x [1] >= nvl(x [3], 0) + nvl(element_at(s.array, -1), 0),
              x [1],
              /* 库存新增销量与上次累计销量之和减落地页销量大于0且不超过100的，取库存新增销量与上次累计销量之和作为本次累计销量 */
              if(
                nvl(x [3], 0) + nvl(element_at(s.array, -1), 0) - x [1] <= 1000,
                nvl(x [3], 0) + nvl(element_at(s.array, -1), 0),
                /* 落地页销量大于上次累计销量的，取落地页销量作为本次累计销量，否则取上次累计销量作为本次累计销量 */
                if(
                  x [1] - nvl(element_at(s.array, -1), 0) > 0,
                  x [1],
                  nvl(element_at(s.array, -1), 0)
                )
              )
            )
          )
        ),
        s.last_qs + x [1]
      ) AS ROW(array ARRAY(BIGINT), last_qs BIGINT)
    ),
    s -> s
  )

```


# array

```sql
SELECT element_at(ARRAY [CAST(200 as bigint)] ,-1)

```

---
## ETL （数据仓库技术）

ETL，是英文Extract-Transform-Load的缩写，用来描述将数据从来源端经过抽取（extract）、转换（transform）、加载（load）至目的端的过程。ETL一词较常用在数据仓库，但其对象并不限于数据仓库。

## BI TOOL

Business intelligence 商业情报（BI）工具是一种应用软件，用于收集和处理来自内部和外部系统的大量**非结构化数据**，包括书籍、期刊、文档、健康记录、图像、文件、电子邮件、视频和其他业务源。虽然不像商业分析工具那样灵活，BI工具提供了一种收集数据的方式，主要通过查询来查找信息。这些工具还有助于为分析准备数据，以便您可以创建报表、仪表板和数据可视化。这些结果赋予员工和管理者加速和改进决策、提高运营效率、确定新的收入潜力、确定市场趋势、报告真正的关键绩效指标和确定新的商业机会的权力。

## DLA

数据湖分析 Data Lake Analytics（DLA）是无服务器（Serverless）化的云上交互式查询分析服务。无需ETL，就可通过DLA在云上通过标准JDBC直接对阿里云OSS，TableStore，RDS，MongoDB等不同数据源中存储的数据进行查询和分析。DLA无缝集成各类商业分析工具，提供便捷的数据可视化。

DLA提供了几大核心亮点：

- 轻松分析*多源数据*：OSS，TableStore，RDS等，让不同存储源中沉睡已久的数据，具备分析能力。

- 能够对*异构数据源*做关联分析。

- 全Serverless结构，无需长期持有成本，完全按需使用，更灵活，资源伸缩方便，升级无感知。


## 一键建仓
一键建仓是指通过DLA控制台配置数据源（RDS数据源、ECS自建数据库数据）和目标数据仓库（OSS数据仓库、AnalyticDB for MySQL数据仓库），系统按照您设定的数据同步时间自动、无缝的帮您把数据源中的数据同步到目标数据仓库，同时在数据仓库中创建与数据源表相同的表结构，在DLA中创建对应的数据仓库表结构。无需创建任何表，您可以基于目标数据仓库进行数据分析，不影响数据源端的线上业务运行。


## 阿里云 DLA 踩坑备忘
已知问题:

- 不支持中文partition
- 不支持avro.schema.literal的TBLPROPERTIES
- MySQL表需要每个指定创建
- 大表 MSCK REPAIR TABLE 会遇到问题
- 需要重复avro中字段定义, 不支持自动通过avsc mapping得到（验证已支持）
- 自动mapping建表使用的是第一个avro文件里的schema，对于后续schema有变化的avro，查询- 会有问题（有新增字段的新字段查不出来，有删除字段的直接报错）

## 相关链接
- https://zhuanlan.zhihu.com/p/74777672
- [Clickhouse 连 MySQL](https://conf.umlife.net/pages/viewpage.action?pageId=78612327)
- [DLA](https://help.aliyun.com/document_detail/71065.html)
- [Presto](https://prestosql.io/docs/current/functions.html)
- [CH](https://clickhouse.yandex/docs/en/query_language/functions/)
(是presto的)用cross join unnnest
