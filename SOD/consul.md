```
docker run --name=node1 --restart=always \
             -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' \
             -p 8300:8300 \
             -p 8301:8301 \
             -p 8301:8301/udp \
             -p 8302:8302/udp \
             -p 8302:8302 \
             -p 8400:8400 \
             -p 8500:8500 \
             -p 8600:8600 \
             -h node1 \
             consul agent -server -bind=172.16.8.4 -bootstrap-expect=3 -node=node1 \
             -data-dir=/tmp/data-dir -client 0.0.0.0 -ui

docker run -d --name=registrator \
             -v /var/run/docker.sock:/tmp/docker.sock \
             --net=host \
             gliderlabs/registrator -ip="172.16.8.4" consul://172.16.8.4:8500


```
- [基于Docker + Consul + Registrator的服务注册与发现集群搭建](https://juejin.cn/post/6844903623084736520)

什么是Registrator

Registrator是一个独立于服务注册表的自动服务注册/注销组件，一般以Docker container的方式进行部署。Registrator会自动侦测它所在的宿主机上的所有Docker容器状态（启用/销毁），并根据容器状态到对应的服务注册列表注册/注销服务。

事实上，Registrator通过读取同一台宿主机的其他容器Container的环境变量进行服务注册、健康检查定义等操作。

Registrator支持可插拔式的服务注册表配置，目前支持包括Consul, etcd和SkyDNS 2三种注册工具。


---

```
# consul本地启动命令
docker run -d -rm -p 8500:8500 -v ~/data/consul:/consul/data -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_1 consul agent -server -bootstrap -ui -node=1 -client='0.0.0.0'

```
-client：表示 Consul 将绑定客户端接口的地址，0.0.0.0 表示所有地址都可以访问

容器启动的服务，注册后得到: http://172.19.0.7:8001/  也就是dj能通过172.16.6.111本机的网络去访问consul。但是因为注册的ip是自己compose网络的。所以consul无法到达172.19.0.7，即使本机是能到达的。需要通过设为本机的网络：--network=host: 跨容器好像也不能连接？需要加上bind？含义是啥？

```
docker run -d --network=host --rm -v ~/data/consul:/consul/data --name=consul_server_1 consul agent -server -bootstrap -ui -node=1 -client='0.0.0.0' -bind 172.16.6.111
```

```
docker exec consul_server_1 consul members

docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_2 consul agent -server -node=2  -join='172.17.0.3'

docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_3 consul agent -server -node=3  -join='172.17.0.3'


docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_4 consul agent -client -node=4 -join='172.17.0.3' -client='0.0.0.0'

docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_5 consul agent -client -node=5 -join='172.17.0.3' -client='0.0.0.0'


docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_6 consul agent -client -node=5 -join='172.17.0.3' -client='0.0.0.0'


docker exec consul_server_1 consul members Node Address Status Type Build Protocol DC Segment 1

```
- [Docker - 容器部署 Consul 集群](https://www.cnblogs.com/lfzm/p/10633595.html)

---


registrator来监控每个service web的状态。当有新的service web启动的时候，registrator会把它注册到consul这个注册中心上。由于consul_template已经订阅了该注册中心上的服务消息，此时consul注册中心会将新的service web信息推送给consul_template，consul_template则会去修改nginx.conf的配置文件，然后让nginx重新载入配置以达到自动修改负载均衡的目的。同样当一个service web挂了，registrator也能感知到，进而通知consul做出响应。


curl http://127.0.0.1/getRemoteIp


/home/youmi/vhost/docker/consul/consul.yml

Consul-template 说明

Consul-Template是基于Consul的自动替换配置文件的应用。在Consul-Template没出现之前，大家构建服务发现系统大多采用的是Zookeeper、Etcd+Confd这样类似的系统。

Consul-Template提供了一个便捷的方式从Consul中获取存储的值，Consul-Template守护进程会查询Consul实例来更新系统上指定的任何模板。当更新完成后，模板还可以选择运行一些任意的命令。

```
# 定义service-web的负载均衡，
# 从consul cluster获取对应的注册服务器的ip与port
# 监听consul cluster 服务变化，一旦发生变化会自动更新服务列表
upstream app {
  {{range service "service-web"}}server {{.Address}}:{{.Port}} max_fails=3 fail_timeout=60 weight=1;
  {{else}}server 127.0.0.1:65535; # force a 502{{end}}
}
```

一旦监听的服务列表发生变化，触发nginx重加载.见consul-template.service

```
#!/bin/sh
exec consul-template \
     -consul-addr=consul:8500 \
     -template "/etc/consul-templates/nginx.conf:/etc/nginx/conf.d/app.conf:nginx -s reload"
```
`
docker-compose  -f consul.yml up -d --scale serviceweb=3
`



- [基于Docker实现服务治理（一）](https://www.zhihu.com/people/chen-feng-xie-70/posts)
- [基于Docker实现服务治理（三）](https://zhuanlan.zhihu.com/p/36834989)


