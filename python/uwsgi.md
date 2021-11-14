# uWSGI

> - [uWSGI 服务器的 uwsgi 协议究竟用在何处？](https://www.zhihu.com/question/46945479/answer/104066078)

## CGI

CGI即通用网关接口(Common Gateway Interface)，是外部应用程序（CGI程序）与Web服务器之间的接口标准，是在**CGI程序和Web服务器之间传递信息的规程**。

于是Web服务器可以**解析**这个HTTP请求，然后把这个请求的各种参数写进进程的环境变量，比如REQUEST_METHOD，PATH_INFO之类的。之后呢，**服务器会调用相应的程序**来处理这个请求，这个程序也就是我们所要写的CGI程序了。它会负责生成动态内容，然后返回给服务器，再由服务器转交给客户端。服务器和CGI程序之间通信，一般是通过**进程的环境变量和管道**。


## wsgi
PythonWeb服务器网关接口（Python Web Server Gateway Interface，缩写为WSGI)是**Python应用程序或框架和Web服务器之间的一种接口**，已经被广泛接受, 它已基本达成它的可移植性方面的目标。定义了 web服务器和 web应用之间的接口规范。也就是说，只要 web服务器和 web应用都遵守WSGI协议，那么 web服务器和 web应用就可以随意的组合。

WSGI是一种Web服务器**网关接口**。它是一个Web服务器（如nginx，uWSGI等服务器）与web应用（如用Flask框架写的程序）通信的一种规范。

uWSGI是一个**Web服务器**，它实现了WSGI协议、uwsgi、http等协议。Nginx中HttpUwsgiModule的作用是与uWSGI服务器进行交换。

要注意 WSGI / uwsgi / uWSGI 这三个**概念的区分**。
- WSGI看过前面小节的同学很清楚了，是一种通信协议。
- uwsgi是一种**线路协议**而不是通信协议，在此常用于在uWSGI服务器与其他网络服务器的数据通信。
- 而uWSGI是实现了uwsgi和WSGI两种协议的Web服务器。

uwsgi协议是一个uWSGI服务器**自有的协议**，它用于定义**传输信息的类型**（type of information），每一个uwsgi packet前4byte为传输信息类型描述，它与WSGI相比是两样东西。

uwsgi 是一种链路协议.类似于**fastcgi协议**， 用于httpServer与ApplicationServer通信。

为什么使用uwsgi来隔离 framework 和webserver？如果在nginx中直接用WSGI， 那么 nginx线程中就要**启动python解释器**，

> 也就是说WSGI是python相关的协议，需要python相关的程序一种接口。nginx无法直接通讯。但是uWSGI实现了**中间人**的作用。

### uWSGI 是一个 WSGI 协议的实现，

uWSGI 包括四个部分：

- 实现了 **uwsgi协议，** 与web server（Nginx） 通信
- web server 内置支持协议模块:
- application server协议支持模块: **实现了 WSGI**， 与 python 框架交互
- 进程控制程序: 为web request 的处理创建工作进程

参考链接：
- https://www.jianshu.com/p/487cc605868f

但是跟反向代理比起来，fastcgi显然也是有好处的，最重要的好处在于**解析HTTP协议的部分被offload到了前端服务器一级**，后端服务器不再解析HTTP协议，这样就减轻了后端的压力，由于前端是nginx这样用C/C++高性能实现的服务器，比起在后端的Python当中使用脚本语言解析HTTP协议，**效率要高不少**。

uwsgi想要继承fastcgi的这种好处，它通过将**消息分片的方式**，可以在一个**socket上并发传输多个请求**，这样就解决了一个连接上一次只能传输一个请求的问题。熟悉HTTP2.0的话会发现这个分片机制跟HTTP2.0很像。

> uwsgi协议的目的： 前置解析HTTP协议，分片机制，socket并发传输多个请求


---
# web 模型
> - [web 模型](https://www.v2ex.com/t/347421#r_4135228)


### 说下我对这 python 这几种 web 模型的理解吧：

首先是 **http server + wsgi server(container) + wsgi application** 这种传统模型吧：
- http server 指的是类似于 nginx 或 apache 的服务
- wsgi server 指的是类似 gunicorn 和 uwsgi 这样的服务
- wsgi application 指的是 flask django 这样的基于 wsgi 接口的框架运行起来的实例
最初这种模型只是为了方便 web 框架的开发者，**不需要每个框架层面都去实现一遍 http server ，就增加了一个 WSGI 中间层协议**，框架只要实现这个协议的客户端就可以，然后用**wsgi server 去实现 http 协议的解析并去调用客户端(wsgi application)**。

> 统一解析http，所以抽取了一个wsgi server

### 为了方便开发，每个框架都内置了一个简易的 wsgi server ，为什么还要用专门的 wsgi server 呢？

**wsgi 除了解析 http 协议以及 http 端口侦听外，还负责了流量转发以及 wsgi application 进程管理的功能**。

一般 wsgi 框架内置的 wsgi server 都是一个单进程，**一次只能处理一个请求**。而目的通用的 wsgi server(gunicorn, uwsgi)都至少支持**pre fork**模型，这种模型会起一个 master 来侦听请求，并启动多个 slave(每个 slave 是一个 wsgi application)， master 负责把请求转发到空闲的 slave 上。除了这种传统的基于进程的 pre fork 同步模型，不同的 wsgi server 也会支持一些其它模型，有**基于线程的同步模型，也有基于 asyncio 的异步模型**。

> 并发与负载均衡


### 这种模型下怎样写异步代码呢？

1. 直接用传统的异步编程(进程，线程，协程)，虽然有些 wsgi server 支持 asynio 模型，但是这也需要用户所写的代码做相应的支持。这就导致了如果我们在 wsgi application 的时候不能随便使用线程和异步 IO ，如果用了就需要配置 wsgi server 使其支持我们自己的写法。因此为了使得我们缩写的 application 能部署在任意的 wsgi server(container)中，我们就只能写同步代码了。
2. 使用分布式异步编程，使用类似 celery 的方式，将需要异步处理的东西发送到 worker 去处理。

### 既然有了 wsgi server ，为什么还要有一个 http server 呢？

主要是因为 wsgi server **支持的并发量比较低**，一般会用一个专门的 http server 来**做一层缓冲，避免并发量过大时直接服务挂掉**。

因为nginx具备优秀的**静态内容处理能力**，然后将动态内容转发给uWSGI服务器，这样可以达到很好的客户端响应。 Nginx 通过 httpuwsgimodule 与 uWSGI 服务器进行交换

python 传统的这种 wsgi 模型，主要是为了**方便框架开发者只需要专注框架层面**，而非 http 处理层面。但这样却增加了服务部署的复杂度，需要同时部署和配置 http server 和 wsgi server ，如果想支持异步还要部署 worker ，而使用 tornado 或 go 开发的应用因为自己实现了高效 http 处理的应用只需要部署自己就可以了。

> CGI，通用网关协议。WSGI，Python web服务网关协议。

> uWSGI，wsgi server ，存在的理由:1. 如果在nginx中直接用WSGI， 那么 nginx线程中就要启动python解释器 2. 统一解析 http 协议以及 http 端口侦听外，还负责了流量转发以及 wsgi application 进程管理的功能

>> http sever，nginx。缓冲与静态内容处理。

## 异步框架

### 接下来是 tornado 和 twisted 这种模型：
这种模型和上面的传统模型处于一个时期，这种模型和 nodejs 差不多，都是**基于回调的模型**，适用于**高 IO 低 CPU** 的场景。这种模型自己实现了一个基于回调 http server(event loop)，每一个请求都被注册成一个异步函数来处理，然后主循环来不断的循环这些函数。这样就和 pre fork 模型有了区别， **pre fork 模型中每一个 slave 都是一个 wsgi application**，一个 wsgi application 都只能处理一个请求，而回调模型**只有一个线程**，不仅**极大的减少了内存的分配还减小了进城以及线程间的切换开销**，从而可以**支持高 IO 并发**。但是这种模型也有很明显的缺点，就是**一旦应用程序有大量的 CPU 计算，就会让这个线程堵住，所有的请求都会收到影响**，如果应用在处理一个请求时崩溃，所有的请求也都会收到影响。

> 事件循环(回调写法)与同步进程模式的对比

> Tornado中推荐使用 **协程** 写异步代码. 协程使用了Python的 `yield` 关键字代替链式回调来将程序挂起和恢复执行。Python 3.5 引入了 `async` 和 `await` 关键字(使用这些关键字的 函数也被称为”原生协程”). 从Tornado 4.3, 你可以用它们代替 `yield` 为基础的协程.

### 接下来时 aiohttp/sanic 这种模型：
这种模型和 tornada 模型的**改进**，但实质上是一样的，因为回调的写法不易读也容易出错，于是将回调的写法改成了**同步的写法**。这种模型和 koa2 和 go net/http 查不多， asyncio 提供了类似 go coroutine 的功能和写法，而 aiohttp 则提供了类似 go 中的 net/http 的 http 处理库。

> 同步写法

---
# uWSGI

uWSGI原生支持HTTP, FastCGI, SCGI及其特定的名为”uwsgi”的协议 (是哒，错误的命名选择)。最好的协议显然是uwsgi，nginx和Cherokee已经支持它了 (虽然有各种Apache模块可用)

一个常用的nginx配置如下：
```
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:3031;
}
```
这表示“传递每一个请求给绑定到3031端口并使用uwsgi协议的服务器。

uwsgi_pass使用uwsgi协议。 proxy_pass使用普通的HTTP与uWSGI服务器联系。uWSGI文档声称该协议更好，更快，并且可以从uWSGI的所有特殊功能（插件uWSGI plugin）中受益。


---
## 添加鲁棒性：Master进程

高度推荐在生产应用上总是运行master进程。

它将不断监控你的进程/线程，并且会添加有趣的特性，例如 uWSGI Stats服务器

要启用master，只需添加–master

---
## 重载服务器

> - [重载服务器](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/Management.html#id3)
当运行在 master 进程模式下时，uWSGI服务器可以在无需关闭主socket的情况下优雅地重启。

这个功能允许你在无需关闭与web服务器的连接以及丢失请求的情况下修补/更新uWSGI服务器。

当你**发送 SIGHUP 给主进程时，它会试着优雅地停止所有的worker，等待任何当前运行中的请求完成**。

然后，它关闭所有与uWSGI无关的最终打开的文件描述符。

最后，它使用一个新的来二进制修补 (使用 execve()) uWSGI进程镜像，继承所有之前的文件描述符。

服务器将会知道它是一个已重载的实例，并且会跳过所有的socket初始化，重用之前的。

> 发送 SIGTERM 信号将会获得与优雅地重载相同的结果，但将**不会等待运行中的请求的完成**。

---

> 如果你看到你的测试在更高的并发速率下失败了，那么你可能到达了你的OS socket backlog**队列限制** (在Linux中最高是128个槽，可以通过 /proc/sys/net/somaxconn 和 /proc/sys/net/ipv4/tcp_max_syn_backlog 对TCP socket进行调整)。

> 你可以使用 listen 配置选项，在uWSGI中设置这个值。

---

## 为什么不简单地使用HTTP作为协议？
一个好问题，它有一个简单的答案：**HTTP解析很慢**，真的很慢。为嘛我们应该做一个复杂的任务两次呢？web服务器已经解析请求了！ uwsgi protocol 对机器而言，是非常容易解析的，而HTTP对人类而言，是非常容易解析的。一旦人类被当成服务器使用，我们会放弃uwsgi协议，支持HTTP协议。这就是说，你也可以通过 原生HTTP支持, FastCGI, ZeroMQ 和其他协议使用uWSGI。

---

## http http-socket

http 和 http-socket的使用上有一些区别:

- http: 自己会产生一个**额外的http进程**(可以认为与nginx同一层, 有路由器/代理/负载均衡器)负责路由http请求给worker, http进程和worker之间使用的是uwsgi协议
- http-socket: 不会产生http进程, 一般用于在前端webserver不支持uwsgi而仅支持http时使用, 他**产生的worker使用的是http协议**。(诸如Webfaction或者Heroku这样的服务来托管你的应用)
- socket:  客户端的请求支持uwsgi, 则直接使用socket即可(tcp or unix)

Official documents recommend using http for a public server and http-socket for web-server after Nginx or Apache if you want use http in network.

因此, http 一般是作为独立部署的选项; http-socket 在前端webserver不支持uwsgi时使用,

如果前端webserver支持uwsgi, 则直接使用socket即可(tcp or unix)

uwsgi://127.0.0.1:8091


```
socket = /home/youmi/tmp/ag-auth.sock
http = 0.0.0.0:10181
启动得到:
uWSGI http bound on 0.0.0.0:10181 fd 3
uwsgi socket 0 bound to UNIX address /home/youmi/tmp/ag-auth.sock fd 6
...
spawned uWSGI master process (pid: 28872)
spawned uWSGI worker 1 (pid: 28876, cores: 1)
spawned uWSGI worker 2 (pid: 28877, cores: 1)
spawned uWSGI http 1 (pid: 28878)


---
socket = /home/youmi/tmp/ag-auth.sock
http-socket = 0.0.0.0:10181
启动得到:
uwsgi socket 0 inherited UNIX address /home/youmi/tmp/ag-auth.sock fd 6
uwsgi socket 1 bound to TCP address 0.0.0.0:10181 fd 3
...
gracefully (RE)spawned uWSGI master process (pid: 28872)
spawned uWSGI worker 1 (pid: 28955, cores: 1)
spawned uWSGI worker 2 (pid: 28956, cores: 1)

```

- [原生HTTP支持](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/HTTP.html)
- [The uwsgi Protocol](https://uwsgi-docs.readthedocs.io/en/latest/Protocol.html)
- [Nginx支持uwsgi](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/Nginx.html)
- [difference-between-uwsgi-pass-and-proxy-pass-in-nginx](https://stackoverflow.com/questions/34562730/difference-between-uwsgi-pass-and-proxy-pass-in-nginx)

---
# Gunicorn的作用是什么？

- 只有一个应用，不需要负载均衡
- 只提供api服务，没有静态文件
- 不需要额外的访问控制等功能。限流、黑名单等

nginx可以缓冲请求和响应。如果让Gunicorn直接提供服务，浏览器发起一个请求，鉴于浏览器和网络情况都是未知的，http请求的发起过程可能比较慢，而Gunicorn只能等待请求发起完成后，才去真正处理请求，处理完成后，等客户端完全接收请求后，才继续下一个。

nginx**缓存客户端发起的请求，直到收完整个请求，转发给Gunicorn，等Gunicorn处理完成后，拿到响应，再发给客户端**，这个流程是nginx擅长处理，而Gunicorn不擅长处理的。

- [Nginx、Gunicorn在服务器中分别起什么作用？](https://www.zhihu.com/question/38528616/answer/117946381)
- [为什么nginx可以直接部署，还要uWSGI，gunicorn等中间件？](https://www.zhihu.com/question/342967945/answer/804493384)
- [深入理解uwsgi和gunicorn网络模型[上]](http://xiaorui.cc/archives/4264): 这篇文章比较深入，提了问题也很到位，有助思考
- [去 async/await 之路](https://zhuanlan.zhihu.com/p/45996168): 说明python的异步的一些方式和对比。

