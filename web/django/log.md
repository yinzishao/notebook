# 默认log

django默认logging的配置位置:django/utils/log.py:18


loggers是django的作用域：

在django层次结构中捕获全部消息的logger。 没有使用此名称发布的消息，而是使用下面的logger之一(例如django.request)。

handlers有两个，一个是标准输出(require_debug_true);一个是mail_admins，应该是用来发送**ERROE**级别信息到后台邮件的

例如django.request，默认的Django配置是没有该logger，也就是没有设propagate为Fasle。所以会传递给父级logger,django。

django.server,Django中的新功能1.10。记录与由runserver命令调用的服务器接收到的请求的处理相关的消息。 HTTP 5XX响应记录为ERROR消息，4XX响应记录为WARNING消息，其他所有内容都记录为INFO。propagate 为False，不会传给django父级logger

---

logging 默认模块的logger是啥模式的?

当没有logging配置的时候，拿的是系统默认的配置，等级应该是warning级别的，输出。supervisor进行监控和重定向。
也就是
```
this_module = __name__.split(".")[-2]
logger = logging.getLogger(this_module)
```
会输出，但是不会有sentry的报警

# 层级

name 一般是句点分割的层级值, 像``foo.bar.baz`` (尽管也可以只是普通的 foo)。层次结构列表中位于下方的记录器是列表中较高位置的记录器的子级。

例如，有个名叫 foo 的记录器，而名字是 foo.bar，foo.bar.baz，和 foo.bam 的记录器都是 foo 的子级。

记录器的名字分级类似 Python 包的层级，如果您使用建议的结构 logging.getLogger(__name__) 在每个模块的基础上组织记录器，则与之完全相同。这是因为在模块里，__name__ 是该模块在 Python 包命名空间中的名字。

django.server会往父级django的上传该这个的记录。通过propagate属性控制。

> 所以应该是统一__name__，基础就是你的apps是比较独立的。这样子就可以通过配置层级进行控制了。

# 过滤器

可以自定义一下过滤器。是否进行过滤

一个django的slow queries的
```
'slow_log': {
    '()': 'django.utils.log.CallbackFilter',
    'callback': lambda record: record.duration > 2 # output slow queries only
}

```

# 处理器对象
handlers：例如sentry，自定义发送邮件，prometheus监控

https://github.com/korfuri/python-logging-prometheus/blob/master/logging_prometheus/__init__.py

# 格式化对象

---

参考链接：

- https://stackoverflow.com/a/5439502
