```sql

-- 当前时间戳
select strftime('%s', 'now')

-- typeOf
select typeOf(t1.post_time) from cached_query_8932 t1 limit 1

-- 时间类型都是text
select post_time, datetime(post_time) as b, typeOf(datetime(post_time)) ,  typeOf(datetime(1092941466, 'unixepoch')), typeOf(strftime('%s','now')) from cached_query_8932 t1 limit 1

select post_time, strftime('%s', datetime(post_time)), strftime('%s', '1970-01-01 08:00:01') from cached_query_8932 t1 limit 1
```

- [sqlite](https://www.sqlite.org/lang_datefunc.html)
