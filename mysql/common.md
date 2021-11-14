# max_binlog_cache_size

Multi-statement transaction required more than 'max_binlog_cache_size' bytes of storage; increase this mysqld variable and try again
panic: Error 1197: Multi-statement transaction required more than 'max_binlog_cache_size' bytes of storage; increase this mysqld variable and try again

```sql
show global VARIABLES like '%binlog%'

show global status like '%binlog%'
```

- [sysvar_binlog_cache_size](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_binlog_cache_size)
- [mysql-max-binlog-cache-size-vs-binlog-cache-size](https://stackoverflow.com/questions/37813819/mysql-max-binlog-cache-size-vs-binlog-cache-size): binlog_cache_size单个事务的内存最大值，超过会使用磁盘。 max_binlog_cache_size单个事务总的使用大小。
- [MySQL中binlog cache使用流程解惑](https://juejin.cn/post/6844903633394335752): 源码分析看不懂
- [MySQL binlog cache详解](https://zhuanlan.zhihu.com/p/108650249): 事务提交，整个binlog cache和binlog临时文件数据全部写入到binlog file中，同时释放binlog cache和binlog临时文件。


# GTID
> - [MySQL · 引擎特性 · 基于GTID复制实现的工作原理](http://mysql.taobao.org/monthly/2020/05/09/)

GTID (Global Transaction IDentifier) 是全局事务标识。它具有**全局唯一性，一个事务对应一个GTID**。唯一性不仅限于主服务器，GTID**在所有的从服务器上也是唯一的**。一个GTID在一个服务器上只执行一次，从而避免重复执行导致数据混乱或主从不一致。

在传统的复制里面，当发生故障需要主从切换时，服务器**需要找到binlog和pos点**，然后将其设定为新的主节点开启复制。相对来说比较麻烦，也容易出错。在MySQL 5.6里面，MySQL会通过内部机制**自动匹配GTID断点**，不再寻找binlog和pos点。我们只需要知道主节点的ip，端口，以及账号密码就可以自动复制。

GTID的生成和使用由以下几步组成：
- 主服务器更新数据时，会在事务前产生GTID，一同记录到binlog日志中。
- binlog传送到从服务器后，被写入到本地的relay log中。从服务器读取GTID，并将其设定为自己的GTID（GTID_NEXT系统）。
- sql线程从relay log中获取GTID，然后对比从服务器端的binlog是否有记录。
- 如果有记录，说明该GTID的事务已经执行，**从服务器会忽略**。
- 如果没有记录，从服务器就会从relay log中执行该GTID的事务，并记录到binlog。

> 可以理解成分布式事务的幂等性、序列号

## 参考链接
- [MySQL5.7杀手级新特性：GTID原理与实战](https://keithlan.github.io/2016/06/23/gtid/)

# prepared

prepared语句是可多次使用的已编译SQL语句。当我们向数据库引擎发送SQL时，**它需要解析SQL，这需要时间**。如果我们要**反复发送同一个SQL语句**，我们应该有礼貌，让数据库只解析一次粗糙的SQL语法。**缓存准备好的语句可以节省大量时间**。

- [making-sqlite-faster-in-go](https://turriate.com/articles/making-sqlite-faster-in-go)

---
# 命中页

**操作**： 查询条件放到子查询中，子查询只查主键ID，然后使用子查询中确定的主键关联查询其他的属性字段；

**原理**： 减少回表操作；

InnoDB中有buffer pool。里面存有**最近访问过的数据页，包括数据页和索引页**。所以我们需要运行两个sql，来比较buffer pool中的数据页的数量。

```sql
select index_name,count(*) from information_schema.INNODB_BUFFER_PAGE where INDEX_NAME in('val','primary') and TABLE_NAME like '%test%' group by index_name;
```

> 可以看出，此时buffer pool中关于test表有4098个数据页，208个索引页。

为了防止上次试验的影响，我们需要清空buffer pool，重启mysql。
```
mysqladmin shutdown
/usr/local/bin/mysqld_safe &
```

为了在**每次重启时确保清空buffer pool**，我们需要关闭innodb_buffer_pool_dump_at_shutdown和innodb_buffer_pool_load_at_startup，这两个选项能够控制数据库关闭时dump出buffer pool中的数据和在数据库开启时载入在磁盘上备份buffer pool的数据。

- [一次SQL查询优化原理分析（900W+数据，从17s到300ms）](https://www.jianshu.com/p/0768ebc4e28d)

---
# DES_ENCRYPT

The ENCRYPT(), DES_ENCRYPT() and DES_DECRYPT() functions based on the Data Encryption Standard (DES) have been deprecated in favor of Advanced Encryption Standard (AES) based functions, because AES provides much better security. (Deprecate the ENCRYPT, DES_ENCRYPT and DES_DECRYPT functions, WL#8126)


- [removal-and-deprecation-in-mysql-5-7](https://mysqlserverteam.com/removal-and-deprecation-in-mysql-5-7/)

# ALLOW_INVALID_DATES

背景：　`panic: Error 1292: Incorrect date value: '2017-07-13T00:00:00+08:00' for column 'first_date' at row 1`

当我们插入非法时间值时，虽然会被纠正，但是在严格模式下，不会插入数据，反而会报错：

- https://segmentfault.com/a/1190000018958236

原因：　NO_ZERO_DATE？

```

ONLY_FULL_GROUP_BY：
对于GROUP BY聚合操作，如果在SELECT中的列，没有在GROUP BY中出现，那么这个SQL是不合法的，因为列不在GROUP BY从句中

NO_AUTO_VALUE_ON_ZERO：
该值影响自增长列的插入。默认设置下，插入0或NULL代表生成下一个自增长值。如果用户 希望插入的值为0，而该列又是自增长的，那么这个选项就有用了。

STRICT_TRANS_TABLES：
在该模式下，如果一个值不能插入到一个事务表中，则中断当前的操作，对非事务表不做限制

NO_ZERO_IN_DATE：
在严格模式下，不允许日期和月份为零

NO_ZERO_DATE：
设置该值，mysql数据库不允许插入零日期，插入零日期会抛出错误而不是警告。

ERROR_FOR_DIVISION_BY_ZERO：
在INSERT或UPDATE过程中，如果数据被零除，则产生错误而非警告。如 果未给出该模式，那么数据被零除时MySQL返回NULL

NO_AUTO_CREATE_USER：
禁止GRANT创建密码为空的用户

NO_ENGINE_SUBSTITUTION：
如果需要的存储引擎被禁用或未编译，那么抛出错误。不设置此值时，用默认的存储引擎替代，并抛出一个异常

PIPES_AS_CONCAT：
将"||"视为字符串的连接操作符而非或运算符，这和Oracle数据库是一样的，也和字符串的拼接函数Concat相类似
ANSI_QUOTES：
启用ANSI_QUOTES后，不能用双引号来引用字符串，因为它被解释为识别符
```

---

# group by

注意group by 的case when ，如果case when 里面的as 字段，跟原来的一样，group by 了这字段，会用的是原来的值进行group by 。注意case when 要一个新的字段名，避免一些bug。


---
# 字符串char字段

待验证： char(32) 如果默认不为空，即使是空字符，当插入的时候，也会申请了空间。


---
# binlog
```
server-id               = 1
log_bin                 = /var/log/mysql/mysql-bin.log
expire_logs_days        = 10
max_binlog_size   = 1024M
binlog_format="ROW"
binlog_row_image="full"

show variables like '%log_bin%';
```

---
# 时区
```sql
SET GLOBAL time_zone = '+8:00';
```

---
# general log
```sql
show variables like 'general%';

SET GLOBAL general_log = 'on';
SET GLOBAL general_log_file = 'XX';

配置文件修改:
```

---
# mysqldump
导出表结构

```bash
mysqldump -C -uroot -proot --databases aso_www

--default-character-set=utf8

--single-transaction： 不加锁。
```

不加只读帐号会报错： mysqldump: Got error: 1044: Access denied for user 'aso_ro'@'%' to database 'adData' when doing LOCK TABLES

--quick

导数据库例子:
```bash
mysqldump -h 172.19.40.141 -uaso_ro -p adData ad_aggs_outer --single-transaction --no-create-info --where='ad_year_month=2101' > ./ad_aggs_outer.sql
mysql -h db-test.ag.alishh -A adData -uaso_ro -p -e 'source ./ad_aggs_outer.sql'
```
写数据会执行`LOCK TABLES `ad_aggs_outer` WRITE;` 需要单独给帐号的LOCK TABLES权限

定时执行任务： `while true; do ll -thr ad_aggs_outer.sql; date ; sleep 5; done`

```bash

mysqldump -u aso_ro -p --no-data adData_multi  > schema.sql

mysqldump --user=root -proot --host=localhost --port=3306  --no-data --skip-triggers --skip-add-drop-table --single-transaction --quick --databases "aso_www"

--result-file=/home/youmi/Documents/note/work/aso-www/mysql/data/ddl/aso_www.sql
```

去除一些分区代码
```bash

sed -i -e 's/ AUTO_INCREMENT=[0-9]*\b//g' -e 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//' /home/youmi/Documents/note/work/aso-www/mysql/data/ddl/aso_www.sql

#或者：

|  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > /home/youmi/Documents/note/work/aso-www/mysql/data/ddl/aso_www.sql
```
例子：

```bash
mysqldump --no-data  --user=aso_ro -p -h172.19.31.101 --skip-triggers --skip-add-drop-table --single-transaction --quick --databases "aso_www" |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/aso_www.sql

# 常量表删除表，直接覆盖
mysqldump --user=aso_ro -p -h172.19.31.111 --skip-triggers  --single-transaction --quick --databases "agconstants"  | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/agconstants.sql

# 10的asoData
mysqldump --no-data  --user=aso_ro -p -h172.19.31.111 --skip-triggers  --skip-add-drop-table --single-transaction --quick --databases "asoData"  |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/asoData_10.sql

# 20的asoData
mysqldump --no-data  --user=aso_ro -p -h172.19.30.120 --skip-triggers  --skip-add-drop-table --single-transaction --quick --databases "asoData"  |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/asoData_20.sql

# 20的asoDataKwr做了分表，导致有很多表，根据时间创建相应的表

# 41的adData
mysqldump --no-data  --user=aso_ro -p -h172.19.40.141 --skip-triggers  --skip-add-drop-table --single-transaction --quick --databases "adData"  |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/adData.sql
```

参考链接:
- https://dev.mysql.com/doc/refman/5.5/en/mysqldump.html


---
# 事务
瞬间有两个事务，分别插入唯一冲突的相同记录，另一个记录只会等待先行的事务结束才执行。但是后的事务会报重复插入的错误

---
# 基准测试
```bash
sysbench --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-password=root /usr/share/sysbench/oltp_common.lua --tables=10 --table_size=100000 --db-driver=mysql prepare

sysbench --mysql-host=127.0.0.1 --mysql-port=13306 --mysql-user=root --mysql-password=123456 /usr/share/sysbench/oltp_common.lua --tables=10 --table_size=100000 --db-driver=mysql prepare

sysbench --threads=4 --time=20 --report-interval=5 --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-password=root /usr/share/sysbench/oltp_read_write.lua --tables=10 --table_size=100000 --db-driver=mysql run

sysbench --threads=4 --time=20 --report-interval=5 --mysql-host=127.0.0.1 --mysql-port=13306 --mysql-user=root --mysql-password=123456 /usr/share/sysbench/oltp_read_write.lua --tables=10 --table_size=100000 --db-driver=mysql run
```

---
# partition


[大表加分区](https://dba.stackexchange.com/questions/65504/partitioning-large-mysql-table)

---
# ch, dla, presto

CH用array join

- [DLA](https://help.aliyun.com/document_detail/71065.html)
- [Presto](https://prestosql.io/docs/current/functions.html)
- [CH](https://clickhouse.yandex/docs/en/query_language/functions/)

(是presto的)用cross join unnnest

---
# 增量更新的套路

```sql

create table tbl (
    ...
    -- NOTE: 业务永远不要主动更新该字段, 利用数据库机制保证单调递增以及有变化才变更
    modify_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY idx_modify_time (modify_time),
) ...
;
-- 获取变更时间段及数据, 其中 @last_modify_time 每次消费完成后提交

-- NOTE: 不能取当前时间, 有漏消费数据的可能性
-- 原因： 取程序的时间戳有不准的问题，各个机器的时间是不同步的
-- 原因： 取数据库的时间有事务问题 严格点得整个读写整体开事物了 TODO: 询问具体场景
-- 其实简单点就每小时跑该小时的数据, 不用维护消费位置. 失败就同样时间段重跑
select max(modify_time) into @modify_time;
-- NOTE: 是右开左闭区间, 避免重复消费, 避免丢数据
select ... from tbl where modify_time > @last_modify_time and modify_time <= @modify_time;

```

疑问： 是假设这一秒之间内取了数据，但是这一秒又插入了数据。这时候select的这一秒会有遗漏，需要进行读写整体开事务。

`select ... from tbl where modify_time > @last_modify_time and modify_time <= now();`

那能通过now() - 1秒 去解决么？

每小时跑该小时的数据, 具体也有类似的错误？

结论： 无法解决，应该尽量避免长事务写入导致的遗漏。

----

# pt-online-schema-change

pt online schema change的工作原理是**创建要更改的表的空副本，根据需要对其进行修改，然后将行从原始表复制到新表中**。复制完成后，它将移走原始表并用新表替换。默认情况下，它还会删除原始表。

复制期间对原始表中数据的任何修改都将反映在新表中，因为该工具**会在原始表上创建触发器以更新新表中的相应行**。使用触发器意味着如果表中已经定义了任何触发器，则该工具将无法工作。

**外键使工具的操作复杂化，并带来额外的风险**。当外键引用表时，原子重命名原始表和新表使外键不起作用。架构更改完成后，工具必须更新外键以引用新表。该工具支持两种方法来实现这一点。您可以在--alter foreign keys方法的文档中阅读更多关于此的信息。

外键也会导致一些副作用。最终的表将具有与原始表相同的外键和索引（除非您在ALTER语句中指定了不同的外键和索引），但是对象的名称可能会稍微更改，以避免MySQL和InnoDB中的对象名称冲突。

为了安全起见，除非指定--execute选项（默认情况下未启用），否则该工具不会修改表。该工具支持多种其他措施来防止不需要的负载或其他问题，包括自动检测副本、连接到副本。

如果为--alter指定的语句试图添加唯一索引，请避免运行pt online schema change。由于pt online schema change使用INSERT IGNORE将行复制到新表中，如果正在写入的行产生重复的键，那么它将以静默方式失败，并且数据将丢失。
