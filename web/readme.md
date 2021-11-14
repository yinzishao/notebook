---
# web

## [csrf](csrf.md)

- 什么是跨域请求
- 跨域请求的安全问题
- csrf攻击
  - [限制跨域请求](安全.md)
  - 需要注意form表单是安全的，也就导致了form表单的攻击场景
  - 如何防止跨域请求
- django的csrf的源码解析
  - 随机secret和salt hash方式加密生成csrftoken
  - 随机secret和salt hash方式加密生成隐藏csrfmiddlewaretoken字段
  - secret而不是完整的token与cookie值中的secret进行比较
  - 一些问题和解答。
    - 避免重放攻击
    - 前后端分离如何避免。JWT不应该放在cookie里面。引出实际的安全漏洞
    - 可以任意伪造，是否是漏洞
  - 实际项目的使用与漏洞

## [安全](csrf.md)

- xss跨站脚本攻击。输入框文本检测、输出纯文本
- csrf
- 点击劫持

## [JWT](jwt.md)

- 组成部分 Header、claim、signature
- 优势
- 劣势
- 自身项目使用情况

## [浏览器缓存](浏览器缓存.md)
- 浏览器缓存过程
- 强制缓存。各种Cache-Control的值的含义
- 内存缓存、磁盘缓存
- 协商缓存。304响应。Etag、Last-Modified


## [uwsgi](../python/uwsgi.md)[](#bookmark)
- CGI是什么
- WSGI是什么。网关接口，一种规范。
- uWSGI是什么。web服务器，包含各种协议。
- uwsgi是什么。链路协议。作用是什么，与nginx，Python应用之间的关系是怎么样的。
- web模型。http server、wsgi server、wsgi application是什么。为什么要这样分。
- 异步框架的说明和对比。
- http、http-socket、socket之间的区别。

## [发布](发布.md)

- 各种发布方式的对比和应用场景。

## [sqlmap](sqlmap.md)

- sqlmap如何使用。
- 请求做了什么操作
- 五种注入模式
- 如何从响应中判断是否有漏洞
- 测试用例的书写。test和boundary组合生成payload

## [hash冲突](hash冲突.md)
- 开放定址法
 - 线性探测再散列
 - 二次探测再散列
 - 伪随机探测再散列
- 再哈希法。不易产生聚集，但增加了计算时间。
- 链地址法。适用于经常进行插入和删除的情况
- 建立公共溢出区
- 拉链法与开放地址法相比的优缺点

## [布隆过滤器.md](布隆过滤器.md)
- 作用是什么，优缺点。
- 原理是怎样的。
- 使用场景、实现。
- 布谷鸟过滤器的结构原理。

## [缓存](缓存.md)
- 缓存穿透。是什么，如何解决的
- 缓存击穿。是什么，如何解决的
- 缓存雪崩。是什么，如何解决的
- 热点数据集中失效
- 缓存一致性问题
- 实际项目的使用场景


## [延迟队列.md](延迟队列.md)
- redis的sortedset。轮训任务。优缺点。
- RabbitMQ。DLX，优缺点
- 时间轮算法。优缺点

## [秒杀系统](秒杀系统)
