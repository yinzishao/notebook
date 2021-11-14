# elastic-py

## ConnectionSelector
位置：elasticsearch.connection_pool.ConnectionSelector

负责如何拿连接池里面的连接，继承该类的有两种：RandomSelector、RoundRobinSelector

RoundRobinSelector通过threading.local()进行轮询。

## ConnectionPool
位置：[elasticsearch.connection_pool.ConnectionPool](https://elasticsearch-py.readthedocs.io/en/master/connection.html#connection-pool)

作用：保存连接（Connection）实例、管理选择过程（通过ConnectionSelector）和死连接（dead connections）的容器。

在每次请求时，传输将通过get_Connection方法请求连接。如果连接失败（它的perform_request引发ConnectionError），它将被标记为dead（通过mark_dead）并设置一个超时（如果它连续失败N次，则超时时间成倍延长-公式为默认的`default_timeout * 2 ** (fail_count - 1)`。超时后，连接将恢复并返回到活动池。一个先前被标记为死亡并成功的连接将被标记为活动（它的失败计数将被删除）。

通过一个优先队列的形式保存死链接，优先级是timeout的时间，拿第一个时间不符合条件（超时时间未到）则不处理。
- [代码链接](https://github.com/elastic/elasticsearch-py/blob/master/elasticsearch/connection_pool.py#L180)

### resurrect

调用者： get_connection

作用： 尝试从死区恢复连接。它将尝试找到一个（不是全部）符合条件（超时已过）的连接，以返回到活动池。任何复活的连接也会被返回。

### get_connection

使用ConnectionSelector实例从池中返回连接。

它尝试恢复符合条件的连接（resurrect），在没有可用连接时强制恢复（因为timeout不符合条件的连接不恢复），并将活动连接列表传递给选择器实例以供选择。

返回连接实例及其当前失败计数。

> 连接池类较简单，并没有去尝试连接是否会成功？和删除死连接的操作？只会一直延长时间重试？

## Transport
位置： [elasticsearch.transport.Transport](https://elasticsearch-py.readthedocs.io/en/master/connection.html#transport)

作用：封装传输逻辑相关。处理各个连接的实例化，并创建一个连接池来保存它们。主接口是perform_request方法。

### sniff
作用：你可以设置client.transport.sniff为true来使客户端去**嗅探整个集群的状态**，把集群中其它机器的ip地址加到客户端中。这样做的好处是，一般你**不用手动设置集群里所有集群的ip到连接客户端**，它会自动帮你添加，并且自动发现新加入集群的机器

- sniff_timeout: 用于嗅探请求的超时-它应该是一个快速的api调用，而且我们正在与更多的节点进行潜在的对话，因此我们希望很快失败。

在last_sniff+sniff_timeout之前不会进行嗅探。

- sniff_on_connection_fail: 控制连接失败是否触发嗅探的标志

### set_connections
作用：实例化所有连接并创建新的连接池来保存它们。尝试识别未更改的主机并重新使用现有的连接实例。

通过传进来的hosts进行各个host的实例化连接。

> 所以这个连接池指的是集群各台机器的连接汇总，而不是单台机器上的多个连接？因为不是面对多线程的库？所以连接池进行连接复活的时候也不会进行删除，一定要重试到能进行复活成功。

### perform_request
作用：执行实际请求。从连接池中检索连接，将所有信息传递给它的perform_request方法并返回数据。如果引发异常，请将连接标记为失败，然后重试（最多重试次数为最多次）。如果操作成功，并且使用的连接先前标记为dead，请将其标记为live，并重置其故障计数。

> 也就是上面复活的连接，在这里进行重新的请求，以此能重新将该连接进行mark_live的过程。

### sniff_hosts
调用者：get_connection

作用： 从集群获取节点列表，并使用检索到的信息创建新的连接池。

通过嗅探获取到新的集群hosts集合，并进行重新连接池的初始化，以此废弃无用的节点的连接。

- sniff_on_connection_fail：连接失败是否进行重新的嗅探，以判断是否是节点的变更？
