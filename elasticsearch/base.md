# 基本使用

## 常用命令

```bash
GET _cat/indices

GET _cluster/pending_tasks

GET _nodes/172.19.31.135
GET _nodes/hot_threads
GET _nodes/stats

GET /_tasks
GET /_tasks?nodes=nodeId1,nodeId2&actions=cluster:*&pretty
# 查看后台更新任务
GET /_tasks?detailed=true&actions=*byquery
GET /_tasks?nodes=85g-AxR1TeitmvHS7pRNMA
GET /_tasks/JgNKVH7_QGmOModx1VKJww:216610517
POST _tasks/To4q4mFAQLO7uzSs7PpLQg:103199051/_cancel

# 按组查询当前的查询语句 show processlist
GET /_tasks?group_by=parents&detailed=true&actions=*search*

# 每行列出索引的名称，分片号，它是主（p）还是副本（r）分片以及未分配的原因
GET /_cat/shards?h=index,shard,prirep,state,unassigned.reason
# 获取有关分片分配问题的更多信息
GET /_cluster/allocation/explain?pretty

# 查看各节点的limits配置
GET _nodes/stats/process?filter_path=**.max_file_descriptors

# 获取index的配置包括默认: https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html
GET advertisement/_settgitings?include_defaults

GET advertisement/_stats

POST /appinfo/_forcemerge?only_expunge_deletes=true
POST /appinfo/_forcemerge?max_num_segments=1
# 获取段大小
GET /_cat/segments
GET /_cat/segments?index=ag*&s=size:desc&v=true

GET _cat/thread_pool/force_merge?v&s=name

# 更改配置
PUT /*/_settings
{
  "index" : {
    "number_of_replicas" : 0
  }
}

POST /_aliases
{
    "actions" : [
        { "remove" : { "index" : "brand_v5.0.1", "alias" : "brand" } },
        { "add" : { "index" : "ag_brand_v8.0.0", "alias" : "brand" } }
    ]
}

POST /_cluster/reroute
{
  "commands": [
    {
      "allocate_replica": {
        "index": "slogan_v1.0.0",
        "shard": 0,
        "node": "node4-1"
      }
    }
  ]
}

curl  elastic:changeme@0.0.0.0:9200/_cat/indices
```

- [cluster-reroute](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/cluster-reroute.html)


## retry_on_conflict

找了一下bulk的更新操作的retry_on_conflict的配置，官方文档都需要在每个文档上面加上retry_on_conflict的配置。默认是0，先找一下全局的配置，避免每个文档都需要重复加上。

但是找不到。

解决办法：代码程序包一层以供默认值。

## slow slog

```bash
PUT advertisement_v9.0.1/_settings
{
  "index.search.slowlog.threshold.query.warn": "1s",
  "index.search.slowlog.threshold.query.info": "800ms",
  "index.search.slowlog.threshold.query.debug": "500ms",
  "index.search.slowlog.threshold.query.trace": "200ms",
  "index.search.slowlog.threshold.fetch.warn": "1s",
  "index.search.slowlog.threshold.fetch.info": "800ms",
  "index.search.slowlog.threshold.fetch.debug": "500ms",
  "index.search.slowlog.threshold.fetch.trace": "200ms",
  "index.search.slowlog.level": "warn",
  "index.indexing.slowlog.threshold.index.warn":"2s",
  "index.indexing.slowlog.threshold.index.info":"1s",
  "index.indexing.slowlog.threshold.index.debug":"800ms",
  "index.indexing.slowlog.threshold.index.trace":"500ms",
  "index.indexing.slowlog.level": "warn"
}

GET _all/_settings

```

## 慢查询kill掉

You can can kill/cancel a search query using standard task cancellation API:

```bash
curl -XPOST 'localhost:9200/_tasks/task_id:1/_cancel?pretty'
```

By default, a running search only checks if it is cancelled or not on segment boundaries, therefore the cancellation can be delayed by large segments. The search cancellation responsiveness can be improved by setting the dynamic cluster-level setting:

```
search.low_level_cancellation = true
```

However, it comes with an additional overhead of more frequent cancellation checks that can be noticeable on large fast running search queries. Changing this setting only affects the searches that start after the change is made.

- <https://www.quora.com/In-Elasticsearch-is-there-a-way-to-kill-a-query-that-is-taking-too-long-after-a-certain-time>


## es-sql
```bash
curl "http://es-test-ag-alishh.umlife.net/_sql" -H 'Content-Type: application/json' -d'select * from advertisement limit 10'
```

## 部分更新
```
POST /slogan/slogan_data/cf3690cd0b5c9da6efa63e3a32db82a0/_update
{
   "doc" : {
      "brand_id_list": [1]
   }
}
```

---
# 脚本相关

- [语法](https://www.elastic.co/guide/en/elasticsearch/painless/5.6/painless-specification.html)

## 脚本查询

```
"query": {
    "bool": {
        "must": [
            {
                "script": {
                    "script": "List x = new ArrayList(); for (v in doc['tag']) {if (Integer.parseInt(v) >= 100 && Integer.parseInt(v) <= 200) {x.add(v)}} return x.length ==  {{tag_length}};"
                }
            }
        ]
    }
},
```

## 脚本聚合
```
GET material_v1/data/_search
{
  "aggs": {
    "NAME": {
      "terms": {
        "script": {
          "inline": "List x = new ArrayList(); for (v in doc['tag']) {if (Integer.parseInt(v) >= 100 && Integer.parseInt(v) <= 200) {x.add(v)}} return x.length;"
        }
      }
    }
  }
}

```

## 脚本更新

```
POST test/type1/1/_update
{
    "script" : {
        "inline": "ctx._source.counter += params.count",
        "lang": "painless",
        "params" : {
            "count" : 4
        }
    }
}
```

- [docs-update](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html)


## _update_by_query
```
POST twitter/_update_by_query
{
  "script": {
    "inline": "ctx._source.likes++",
    "lang": "painless"
  },
  "query": {
    "term": {
      "user": "kimchy"
    }
  }
}

?requests_per_second=1000

?conflicts=proceed

```

- [docs-update-by-query](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/docs-update-by-query.html)

## scripted_upsert

- [scripted_upsert](https://stackoverflow.com/questions/38719549/using-elasticsearchs-script-upsert-to-create-a-document): 使用例子

```
POST /sessions/session/1/_update
{
  "scripted_upsert": true,
  "script": {
    "inline": "if (ctx.op == \"create\") ctx._source.numbers = newNumbers; else ctx._source.numbers += updatedNumbers",
    "params": {
      "newNumbers": [1,2,3],
      "updatedNumbers": [55]
    }
  },
  "upsert": {}
}
```

如果调用上面的命令，而索引不存在，它将创建索引，并在新文档中创建newNumbers值。如果再次调用完全相同的命令，数字值将变为1、2、3、55。

在您的例子中，您缺少了“upsert”：{}部分。

## list to set
``
```
Set myset = new HashSet(ctx._source[p.array_field]);
```

- https://stackoverflow.com/questions/53079144/elasticsearch-make-a-field-behave-like-set-instead-of-list

> 性能没啥提升-_-

---
# 其他
## keyword

```
"brand_id": {
  "type": "keyword"
}
```

存储的是字符串的数字，因为ES不支持大数bigint64。keyword字段的比较在数字层次还是可以比较成功的

`"gt": 0` 能符合预期

> 注意keyword和number类型的性能区别

---
## 阿里云产品定价

[产品定价](https://help.aliyun.com/document_detail/132255.html?spm=a2c4g.11186623.6.558.569f6525Uv6MCc)

---
## 调整 Amazon ES 域大小

- 计算存储要求
- 选择分片数量
- 选择实例类型和测试

-[调整 Amazon ES 域大小](https://docs.aws.amazon.com/zh_cn/elasticsearch-service/latest/developerguide/sizing-domains.html)

---
## es_rejected_execution_exception

### 简短描述
es_rejected_execution_exception[bulk] 是批量队列错误。当对 Elasticsearch 集群的请求数超过**批量队列大小** (threadpool.bulk.queue_size) 时，会发生此问题。每个节点上的批量队列可以容纳 50 到 200 个请求，具体取决于您使用的 Elasticsearch 版本。队列已满时，将拒绝新请求。

### 解决方法
注意：对于大多数 Amazon ES 版本，您并无法增加批量队列大小。之所以设置队列是为了将请求限制在可管理的数量之类。有关更多信息，请参阅 Elasticsearch 文档中的 Threadpool Section。

使用以下方法之一解决 es_rejected_execution_exception 错误：

- 添加更多节点：每个节点都有一个批量队列，因此**添加更多节点可以为您提供更大的队列容量**。要添加节点，请参阅配置 Amazon ES 域（控制台）。注意：如果**没有足够的活跃索引分片**分配到新节点，添加更多数据节点并无济于事。“活跃索引分片”是在**最近 5 分钟内收到至少一个索引请求的分片**。
- 切换到更大的实例类型：批量请求的每个节点上的线程池中的线程数等于**可用处理器的数量**。切换到具有更多虚拟 CPU (vCPU) 的实例可获取更多线程来处理批量请求。有关更多信息，请参阅选择实例类型和测试。
- 提高索引性能：**当文档索引速度更快时，批量队列达到容量限制的可能性就会降低**。有关性能调整的更多信息，请参阅如何提高我的 Elasticsearch 集群上的索引性能？



---
## time与request_timeout的区别

<https://elasticsearch-py.readthedocs.io/en/master/api.html#timeout>

Timeout:
Global timeout can be set when constructing the client (see Connection’s timeout parameter) or on a per-request basis using request_timeout (float value in seconds) as part of any API call, this value will get passed to the perform_request method of the connection class:

> timeout全局超时设置。每个请求的timeout可以通过request_timeout进行覆盖。

> 代码： elasticsearch/transport.py:303

## retry_on_timeout

注意设置这个参数后的影响，默认是False的，如果设成True，则查询/更新操作等操作耗时教久，timeout了，会进行重试。导致重复的高负载请求。

而retry_on_timeout只能在声明client的时候进行设置

retry_on_status支持特定错误码重试，如(502, 503, 504)

---
## nested

疑问： 怎么获取到nested里面的文档

答案： 通过params._source 获取，**会造成内存问题**

```
for ( i in params._source ) { params._agg.transactions[i['tag_id]]  = i['method']}
```
* <https://www.elastic.co/guide/en/elasticsearch/reference/5.5/search-aggregations-metrics-scripted-metric-aggregation.html>

例子：
```bash
GET advertisement/data/_search
{
  "query": {
    "bool": {
      "filter": {
        "range": {
          "createdAt": {
            "gte": "2020-12-25"
          }
        }
      },
      "must": [
        {
          "script": {
            "script": "params._source.ad_creative.size() > 10"
          }
        }
      ]
    }
  }
}

GET advertisement/data/_search
{
    "query": {
        "bool": {
            "must_not": [
                {
                    "nested": {
                        "path": "ad_creative",
                        "query": {
                            "exists": {
                                "field": "ad_creative"
                            }
                        }
                    }
                }
            ],
            "must": [
              {
                "bool": {
                  "filter": {
                    "range": {
                      "log_summary_list": {
                        "gte": "2021-01-01",
                        "lte": "2021-03-30"
                      }
                    }
                  }
                }
              }
            ]
        }
    }
}
```

---
## ES备份与恢复

```
GET _snapshot/_all
GET _snapshot/backup_ag/_all

oss备份目录设置
#PUT _snapshot/backup_ag
#{
#    "type": "oss",
#    "settings": {
#        "endpoint": "http://oss-cn-shanghai-internal.aliyuncs.com",
#        "access_key_id": "xxx",
#        "secret_access_key": "xxxx",
#        "bucket": "backup-ag",
#        "compress": true,
#        "base_path": "ag-es/snapshot"
#    }
#}

本地备份目录设置
PUT /_snapshot/backup_mh
{
    "type": "fs",
    "settings": {
        "compress": true,
        "location": "/data/es/backup"
    }
}

备份
#PUT _snapshot/backup_ag/log_20190219
#{
#    "indices": "mysql_slow_log_v1,ngx_user_log_v2,ks_sql_monitor_v2"
#}

恢复
POST _snapshot/backup_ag/ad_20190221/_restore
{
  "indices": "advertisement_v5.0.0",
  "rename_pattern": "(.+)",
  "rename_replacement": "ag_advertisement_industry"
}

# 测试ES需要设置
PUT /ag_advertisement_industry/_settings
{
  "index.number_of_replicas" : "0"
}

# 查看重建索引的进度：
GET restored_index_3/_recovery

```

参考链接：
- <http://cwiki.apachecn.org/pages/viewpage.action?pageId=9405386>
- <https://www.elastic.co/guide/cn/elasticsearch/guide/current/_restoring_from_a_snapshot.html>


---
## refresh_interval
设置刷新时间
```
PUT /ag_advertisement_test/_settings
{
    "index" : {
        "refresh_interval" : "-1"
    }
}
```
设置后，更新并不能通过_search是获取到最新的数据。

但是如果：**直接去获取单个文档的数据**（`GET ag_advertisement_test/data/1000003?parent=1900d3a59d00c93b26678287e6df0185`），
会发现最新的数据.并且发现_search的部分数据已经刷新到最新。

而且如果再次再次更新单个文档的， 会把旧的版本刷新到可搜素，**但仍不是最新的**，而且也发现_search的**部分数据**已经刷新到最新

测试脚本
```
def t():
    import random
    import time
    c = time.time()
    data = []
    for i in range(0, 100000):
        data.append({
            "_op_type": 'update',
            "_index": 'ag_update_test',
            "_type": 'data',
            "_id": i,
            "doc": {
                "heat": random.randint(0, 1000)
            },
            # "doc_as_upsert": True
        })
        if i % 5000 == 0:
            a = time.time()
            bulk_data_to_es(ES_CLIENT, data)
            b = time.time()
            logger.info(b-a)
            data = []
    if data:
        a = time.time()
        bulk_data_to_es(ES_CLIENT, data)
        b = time.time()
        logger.info(b - a)
    d = time.time()
    logger.info(d-c)
```

但是没有看到(refresh='false', refresh_interval: -1)对比(refresh='false', refresh_interval: 1s)有明显的优化，差不多每5000条1到2秒，：
> refresh='wait_for' 后如果refresh_interval设成-1会一直timeout.

设置成refresh='wait_for', refresh_interval: 1s后，明显慢了很多: 每5000条从1到2秒，变成10秒。总时间从41秒提升到208秒
> 因为bulk默认chunk_size是500 需要等10个refresh_interval

设置成refresh='wait_for', refresh_interval: 10s后，更慢了: 每5000条需要100秒

refresh='false', refresh_interval: 1s, 每5000条更新同3个文档的值("_id": i % 3)，会变得更慢: 变成每5000条13秒左右.总时间279，猜测是重复更新，需要执行refresh操作

不管设置成refresh='wait_for'还是refresh='false'，当瞬间有相同的请求都会有版本冲突
而refresh='false' or 'wait_for', refresh_interval: 1s, 在单进程顺序同步里面即使是有重复的也不会有版本冲突

之前把正式环境的refresh设成wait_for 是为了减少冲突，但其实也是会有小部分发生冲突，只是应该是更新慢了，导致能在同一瞬间更新同一个文档的几率降低了。

同步热度的，之前60万数据要大概1个小时，去掉wait_for后726秒。如果热度计算半衰期为半年，每天一次需要同步1000万数据，大概需要3到4个小时，应该可以凌晨的时候同步完成。

---
## 获取ES同步脚本
GET _cluster/state/metadata?pretty&filter_path=**.stored_scripts

---
# 聚合排序

多桶排序: 多桶指的是返回多个值，把数据按规则分开多个桶进行聚合

度量(metrics): 一般指的是最大值，平均值这些汇总成一行的

基于“深度”度量排序：

我们可以定义更深的路径，将度量用尖括号（ > ）嵌套起来，像这样： my_bucket>another_bucket>metric 。

> 注意是度量，嵌套路径上的每个桶都必须是 单值 的. 如果是多桶的，会报错: Sub-path [content] points to non single-bucket aggregation

## 问题: 如何根据nested聚合的值进行排序

相关问题：
- <https://github.com/elastic/elasticsearch/issues/16838>  6.1版本后的Bucket Sort Aggregation支持了？

nested聚合，得到的是个桶(doc_count)的，而不是度量(value)

方案： 通过反向聚合Reverse nested Aggregation？<https://www.elastic.co/guide/en/elasticsearch/reference/5.4/search-aggregations-bucket-reverse-nested-aggregation.html>

搜索关键词：  elasticsearch aggregation nested sort

参考链接:
- <https://www.elastic.co/guide/cn/elasticsearch/guide/current/_sorting_multivalue_buckets.html>

## Pipeline Aggregations

对同等级和父级的聚合结果进行聚合或者其他操作;

在6.1添加了Bucket Sort Aggregation功能，支持多桶聚合后的度量排序:
<https://www.elastic.co/guide/en/elasticsearch/reference/6.1/search-aggregations-pipeline-bucket-sort-aggregation.html>

> ES的聚合不精确且消耗资源，尽量减少ES的聚合查询

# 选型

> - [Elasticsearch(技术选型分析)](https://blog.csdn.net/u012921921/article/details/89324119)

## Elasticsearch 与 Solr 的比较总结

*   二者安装都很简单；
*   Solr 利用 Zookeeper 进行分布式管理，而 Elasticsearch 自身带有分布式协调管理功能;
*   Solr 支持更多格式的数据，而 Elasticsearch 仅支持json文件格式；
*   Solr 官方提供的功能更多，而 Elasticsearch 本身更注重于核心功能，高级功能多有第三方插件提供；
*   Solr 在传统的搜索应用中表现好于 Elasticsearch，但在处理实时搜索应用时效率明显低于 Elasticsearch。

Solr 是传统搜索应用的有力解决方案，但 Elasticsearch 更适用于新兴的实时搜索应用
