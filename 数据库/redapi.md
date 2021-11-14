# redapi

## 背景

类似redash查询, API返回筛选后数据.查询配置直接从redash同步来， 每隔5分钟同步最新的redash的sql语句.

- [redapi代码地址](https://git.umlife.net/adxmi/migo/-/tree/master/cmd/redapi)
- [redapi相关redash查询列表](https://redash-alishh.umlife.net/queries/794)

## 部署方式

- 国内正式环境
    - 国内的流量入口在ag-web-00的nginx上，相关配置文件: /etc/nginx/sites-enabled/redapi.y.cn
    - 负载均衡到ag-web-00 ag-web-01的两个服务上, 部署相关配置文件: /etc/supervisor/conf.d/redapi.conf
    - [正式环境的apollo配置](https://apollo-alishh.umlife.net/config.html?#/appid=migo)

- 国内在k8s部署了一套测试环境，方便本地和灰度对接：
    - [redapi测试环境的rancher部署地址](https://rancher-alishh.umlife.net/p/c-s8djr:p-5wqhf/workload/deployment:ag-test:test-redapi-deployment)
    - [测试环境的apollo配置](https://apollo-alishh.umlife.net/config.html#/appid=migo&env=DEV&cluster=test)
    - [api-ag-test-public的Virtual Service](https://rancher-alishh.umlife.net/p/c-s8djr:p-5wqhf/istio/virtual-service/ag-test:api-ag-test-public/edit?group=namespace)

- 国外正式环境
    - 国内的流量入口在web-00.ag.awsor的nginx上，相关配置文件: /etc/nginx/sites-enabled/redapi-ag-awsor.y.cn
    - 负载均衡到web-00.ag.awsor web-01.ag.awsor的两个服务上, 部署相关配置文件: /etc/supervisor/conf.d/migo.conf
    - [正式环境的apollo配置](https://apollo-alishh.umlife.net/config.html#/appid=migo&env=DEV&cluster=awsor)


相关测试例子:

```shell
## 本地机器请求测试环境，需要带上token值
curl -H 'Authorization: mjJ2CXRh!F2kxj83Q0wtmBDP^#KwUkf9DM2v' "https://api-ag-test-public.umlife.net/redapi/queries/ag-ec-product-sold-rank-first-seen?p_m=6&p_min_qs=50&p_n=3&p_site_id=10501,10502,20902,11001,10201"

## 主动刷新redash更改语句的语句同步, 否则需要等待配置相应的时间reloadinterval: 5m。
curl -i -X POST "http://web-01.ag.alishh:8000/-/reload"
curl -i -X POST "http://web-00.ag.alishh:8000/-/reload"
```

## 相关监控

- [redapi相关监控](https://redash-alishh.umlife.net/queries/9128/source?p_selection=%5B%22m_redapi%22%5D)
    - [redapi-nginx-query-stat-trend](https://redash-alishh.umlife.net/queries/7122): 平均请求时间、p90、p99，需要定期或者补充相关监控进行优化。

## 发布审核流程

现在是任何一个人在redash上打上redapi的标签（海外还需要打上awsor标签）就可以同步到redapi上了，但是如果是新的数据源，相关的apollo配置需要先添加上新的数据源, 并重启redapi服务。

相关redash的查询接口，相关负责人需要进行审核一下，详情见[redapi相关规范](https://conf.umlife.net/pages/viewpage.action?pageId=85511538)

比较要注意的点：
- 禁止过于灵活的参数，例如表名、列名作为请求参数，难以分析sql的含义。
- 相关查询要尽量命中索引，不能大批量数据的扫描或者返回。但有时候某些场景下，业务方可能会有一些预设的条件，例如A/B参数肯定会有一个非空，但是因为暂时做不到代码的限制，如果有些特殊情况下，请求参数异常了，会导致慢查询。需要判断接口是否需要拆成多个接口，让每个接口能限制命中索引。


## python sdk

方便python端web开发的调用，通过redash的源库的元信息进行一个python版本的sdk的生成。后续文档生成也可以类似这样的方式。

- [项目代码地址](https://git.umlife.net/mt-service/utils/-/tree/master/redapi)
- [通过"CI自动生成"的job自动生成最新版本的client](https://git.umlife.net/mt-service/utils/-/blob/master/.gitlab-ci.yml#L5)


## 相关问题排查

- 个别5xx的一般问题是慢查询超时导致，需要定期留意监控面板。
- 某段时间的大量5xx请求，或者异常重启，可以通过nginx的access log 分析一下前后异常请求，有可能是sql返回大量数据导致的内存溢出。
- 还有一个经常遇到的问题是缓存异常。可能是因为当时的数据库不正确(或者代码bug?)，而缓存的数据是异常的错误快照。但是因为没有相关释放缓存的接口，只能通过以下方式之一释放了：
    - 清空所有的redis key，因为key是query的hash，但没有接口名称的前缀标识。
    - 更改单独接口的query语句（增加或删除一个换行），通过reload接口更新服务的最新的sql，让其生成新的hash进行缓存。

## TODO List

- [ ] 返回数据量级需要进行限制，避免返回数据内存无限扩张
- [ ] 单独接口的缓存释放接口暴露，避免直接redis清理缓存
- [ ] redapi文档生成流程, 接入yapi提供mock给前端。
- [ ] 完善发布流程。打标签发布的审核流程与规范。
- [ ] redapi收录到代码仓库，进行单元测试流程。
- [ ] 迁移到k8s上
- [ ] SOD-976: redapi带缓存的相同查询加锁/支持限制同数据源并发查询数。 clickhouse可以通过单独配置redash用户，限制用户的查询资源限制。
- [ ] redapi慢查询接口的监控与定期优化


## 展望

> 有兴趣看看《大数据之路：阿里巴巴大数据实践》的数据服务章节是怎么吹牛逼的～

DWSOA 是数据服务的第一个阶段，也就是将业务方对数据的需求通过 SOA 服务的方式暴露出去。**由需求驱动，一个需求开发一个或者几个接口，编写接口文档，开放给业务方调用**。这种架构实现起来比较简单，但是其缺陷也是特别明显的。

- 一方面，接口粒度比较粗，灵活性不高，扩展性差，复用率低。随着业务方对数据服务的需求增加，接口的数量也会很快从一位数增加到两位数，从两位数增加到三位数，其维护成本可想而知。
- 另一方面 开发效率不高无法快速响应业务。一个接口从需求开发、测试到最终的上线，整个流程走完至少需要1天的时间，即使有时候仅仅是增加一、两个返回字段，也要走一整套流程，所以开发效率比较低，投入的人力成本较高。

DWSOA 阶段存在的明显问题，就是烟囱式开发，导致接口众多不好维护，因此需要想办法降低接口的数量。当时我们对这些需求做了调研分析，发现实现逻辑基本上就是从 DB 取数，然后封装结果暴露服务，并且很多接口其实是可以合并的。

OpenAPI 就是数据服务的第二个阶段。**具体的做法就是将数据按照其统计粒度进行聚合，同样维度的数据，形成一张逻辑表，采用同样的接口描述**。以会员维度为例 把所有以会员为中心的数据做成 张逻宽表，只要是查询会员粒度的数据，仅需要调用会员接口即可。通过段时间的实施，结果表明这种方式有效地收敛了接口数量。

然而，数据的维度并没有我们想象的那么可控，随着时间的推移，大家对数据的深度使用，分析数据的维度也越来越多，当时 OpenAPI生产已有近 100 个接口：同时也带来大量对象关系映射的维护工作量。于是，**在 OpenAPI 的基础上，再抽象一层，用 DSL (Domain SpecificLanguage ，领域专用语言）来描述取数需求**。新做一套 DSL 然有一定的学习成本 ，因此采用标准的 SQL 语法，在此基础上做了一些 限制和特殊增强 ，以降低学习成本。同时也封装了标准 DataSource ，可以使ORM (Object Relation Mapping ，对象关系映射）框架（目前比较主流的框架有 Hibernate MyBatis 等）来解决对象关系映射问题。

至此，所有的简单查询服务减少到只有一个接口 ，这大大降低了数据服务的维护成本。传统的方式查问题需要翻源码，确认逻辑：而 SmartDQ 只需要检查 SQL 的工作量，并且可以开放给业务方通过写 SQL 的方式对外提供服务 ，由服务提供者自己来维护 SQL ，也算是服务走向 DevOps个里程碑吧。

逻辑表虽然在 OpenAPI 阶段就已经存在，但是在SmartDQ 阶段讲更合适，因为 SmartDQ 把逻辑表的作用真正发挥出来了。 SQL 提供者只需关心逻辑表的结构，不需要关心底层由多少物理表组成，甚至不需要关心这些物理表是 HBase 还是 MySQL 的，是单表还是分库分表，**因为 SmartDQ 已经封装了跨异构数据源和分布式查询功能**。 此外，数据部门字段的变更相对比较频繁，这种底层变更对应用层来说应该算是最糟糕的变更之一了。 而逻辑表层的设计很好地规避了这个痛点，**只变更逻辑表中物理字段的映射关系**，并且即刻生效，对调用方来说完全无感知。

小结：接口易上难下，即使一个接口 也会绑定－批人（业务方、接口开发维护人员、调用方）。所以对外提供的数据服务接口 定要尽可能抽象，接口的数量要尽可能收敛，最后在保障服务质量的情况下，尽可能减少维护工作量。现在 SmartDQ 提供 300 多个 SQL 模板，每条 SQL承担多个接口 的需求，而我们只用一位同学来维护 SmartDQ

第四个阶段是统一的数据服务层（即 OneService ）。大家心里可能会有疑问： SQL 并不能解决复杂的业务逻辑啊。确实， SmartDQ只满足了简单的查询服务需求。我们遇到的场景还有这么几类：**个性化的垂直业务场景、实时数据推送服务、定时任务服务**。所以 OneService主要是提供多种服务类型来满足用户需求，分别是 OneService-SmartDQ、OneService-Lego 、OneService-iPush 、OneService-uTiming上面提到过， SmartDQ 不能满足个性化的取数业务场 ，可以使用Lego Lego 采用插件化方式开发服务，一类需求开发一个插件，目共生产5个插件。为了避免插件之间相互影响，我们将插件做成微服务，使用 Docker 做隔离。

> 第一个阶段： 根据需求驱动。 第二个阶段： 抽象到逻辑表层。 第三个阶段： SQL中间件。我们需要的是当前最合适的方案。
