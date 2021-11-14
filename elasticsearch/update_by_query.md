
# update_by_query

提起es的Update By Query很多人一定也不陌生，它对应的就是关系型数据库的update set ... where...语句，这对应一般的存储引擎而言算是最基本的功能，但它的坑确不少，多到让你使用起来很奔溃，比如**批量更新时非事务模式执行（允许部分成功部分失败）、大批量操作会超时、频繁更新会报错（版本冲突）、脚本执行太频繁时又会触发断路器等**。


#### 1. 非事务模式执行

在前面update_by_query相关文章也大概讲过，所有更新和查询失败都会导致_update_by_query中止，并在响应失败时返回。已执行的更新仍然存在。换句话说，该过程不会回滚，只会中止。

#### 2. java.io.IOException: listener timeout

在前面的文章中也讲过，默认是30000ms，但补充一点：修改超时时间并非真正的解决方案。

#### 3. VersionConflictEngineException

由于es是准实时的，默认refresh_interval: "1s"，_update_by_query在索引启动时获取索引的快照，这意味着**如果文档在拍摄快照的时间和处理索引请求之间发生更改，则会出现版本冲突**。说白了，1s内多次修改同一个document就会发生，你通过设置version_conflicts=false（会忽略错误），但并未解决问题啊，当然了，你还能有2中方式解决该问题：

retries，一直重试，UpdateByQueryRequestBuilder中默认为11次，可见对es是有一定的压力的

refresh=true，一直去刷盘，当然可以解决准实时的问题，但磁盘消耗是很多的
#### 4. IllegalArgumentException: failed to execute script

Too many dynamic script compilations within, max: [75/5m]，看意思就懂，script修改语句只能接受5分钟内75次，what？具体可参与官方script-compilation-circuit-breaker，怎么滴也得配置个十几万次吧。
> 需要提前通过put _script 编译好

总结，使用Update By Query要重点关注上面的4个问题，特别是涉及到大批量的修改，特别要关注监控信息（`GET _tasks?detailed=true&actions=*byquery`），个人建议要限流，比如：可通过前置mongodb（定时定量去更新）或者**更新失败后记录到新的index中后续定时定量去补偿**。

- [关于ElasticSearch的Update By Query的那些著名的坑](https://blog.csdn.net/alex_xfboy/article/details/99715217)


---
## scroll_size

默认情况下，_update_by_query使用1000个滚动批。您可以使用scroll_size URL参数更改批大小。

## requests_per_second
requests_per_second可以设置为任意正十进制数（1.4、6、1000等），并通过在每个批中填充等待时间来限制_update_by_query发出批索引操作的速率。通过将每秒请求数设置为-1，可以禁用限制。
> 限制更新速率

限制是通过在批之间等待来完成的，这样就可以为内部使用的滚动_update_by_query指定一个考虑到填充的超时时间。填充时间是批大小除以每秒请求数与写入时间之差。默认情况下，批大小为1000，因此如果每秒请求数设置为500:

```
target_time = 1000 / 500 per second = 2 seconds
wait_time = target_time - delete_time = 2 seconds - .5 seconds = 1.5 seconds
```
> 例子理解：requests_per_second设定的是预想的rps。所以等待时间会根本插入时间变化而变化，上面的例子是想达到500的rps，因为每批次是1000, 所以要在两秒内完成。但是因为写入只用了0.5s，所以会等待1.5s。

## slice
**支持切片滚动来并行更新过程**。这可以提高效率，并提供一种方便的方法将请求分解为更小的请求零件.设置切片auto会为大多数数据流和索引选择一个合理的数目。

- 当切片数等于索引或备份索引中的分片数时，查询性能最有效。如果该数字较大（例如，500），请选择较小的数字，因为切片太多会影响性能。将切片设置为高于碎片数通常不会提高效率并增加开销
- 使用切片数在可用资源中线性扩展更新性能

运行时主导查询或更新性能，取决于重新索引的文档和集群资源。

虽然能加快任务速度，但要注意**并发导致的CPU增加**。

---
## sliced-scroll

```bash
GET /twitter/tweet/_search?scroll=1m
{
    "slice": {
        "id": 0,
        "max": 2
    },
    "query": {
        "match" : {
            "title" : "elasticsearch"
        }
    }
}
GET /twitter/tweet/_search?scroll=1m
{
    "slice": {
        "id": 1,
        "max": 2
    },
    "query": {
        "match" : {
            "title" : "elasticsearch"
        }
    }
}
```

上面的栗子，第一个请求返回的是第一个切片（id : 0）的文档，第二个请求返回的是第二个切片的文档。因为我们设置了最大切片数量是 2 ，所以两个请求的结果等价于一次不切片的 scroll 查询结果。


- [sliced-scroll](https://www.elastic.co/guide/en/elasticsearch/reference/5.4/search-request-scroll.html#sliced-scroll)
- [Scroll(示例代码)](https://www.136.la/tech/show-804943.html)

---
## update_by_query
查询更新操作会发生版本冲突，这时候可以通过`conflicts=proceed`参数进行继续，否则会中止该操作，但不会回滚之前所做的更新操作

并没有Retry on conflicts, 原因是因为版本冲突后，不能确认已经被更新后的文档是否适合之前的查询。除非再次查询，然后retry，ES社区并不打算提供，因为比较繁琐。所以他的建议是程序里做相应的这个逻辑，**如果有冲突，重新执行update_by_query操作**.

疑问：上面说有retries的默认11, 这里又说没有，而且返回的retries是什么含义?
> 可以看一下存在版本冲突的请求任务，retries是否有值。retries应该跟版本冲突无关

`bulk is the number of bulk actions retried and search is the number of search actions retried.`

## 获取正在执行的更新语句

```
GET _tasks?detailed=true&actions=*byquery
```


参考链接:
* <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update-by-query.html>
* <https://github.com/elastic/elasticsearch/issues/19632>


---

## 单文档更新
> 记录之前的思考

单进程，update某个文档不会有冲突。

多进程，update同个文档会是怎么样的情况（前提：refresh_interval是很大的情况下）：

A进程拿取但文档并更新到内存之后，B进程再更新，应该是没有问题的？也就是交叉更新。因为B进程更新拿到的是内存的文档？而不是search的文档？或者单文档的更新是能获取到最新的。

A、B进程同步并发处理：A、B的更新线程同时拿到同一个版本的文档，会发生冲突？加上重试后就好，如果不断有更新的任务，即使重试也会一样发送冲突。

## 搜索更新

多进程搜索更新：refresh_interval内拿到的都是旧数据，A进程更新后，B进程的更新操作能拿到A更新后的版本？所以会很容易发生冲突？这样重试有作用吗？还是说冲突后，会刷新冲突的数据？待测试
