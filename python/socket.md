# socket 编程

```python
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", int(port)))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = s.getsockname()[1]
        logging.info("listen port %s:%d", host, port)
```
SO_REUSEADDR的使用。

当socket关闭后，本地端用于该socket的端口号立刻就可以被重用。通常来说，只有经过系统定义一段时间后，才能被重用。
S.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。

> 本地绑定后立刻重启监听相同的端口还是会有端口占用的问题？

```python
for upstream in upstreams:
    conn = socket.create_connection(upstream)
    client_host, _ = conn.getsockname()
    if client_host:
        conn.close()
        return client_host
    conn.close()
```

consul获取hostname做法。这里涉及了一个知识点,python是如何注册consul的。为什么不能不填address则直接让服务端去获取请求的IP作为客户端的IP？

> 本机可能会因为多个网卡的情况下，有多个IP地址？所以需要建立一个consul的连接，然后根据tcp协议等，进行获取hostname?
