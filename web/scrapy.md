In some cases you may be interested in passing arguments to those callback functions so you can receive the arguments later, in the second callback. You can use the Request.meta attribute for that.

Here’s an example of how to pass an item using this mechanism, to populate different fields from different pages:
```
def parse_page1(self, response):
    item = MyItem()
    item['main_url'] = response.url
    request = scrapy.Request("http://www.example.com/some_page.html",
                             callback=self.parse_page2)
    request.meta['item'] = item
    return request

def parse_page2(self, response):
    item = response.meta['item']
    item['other_url'] = response.url
    return item
```

mongodb的例子在item pipeline中有一个，说明如何使用 from_crawler ;         Write items to MongoDB

ImagesPipeline
http://scrapy-chs.readthedocs.org/zh_CN/1.0/topics/images.html?highlight=%E5%9B%BE%E7%89%87
下载项目图片

```

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


```

状态收集器？？

crawlspider的set_crawler	http://stackoverflow.com/questions/29762151/what-is-the-function-of-set-crawler-and-from-crawler-in-crawl-py-in-scrapy

Usually you don't need to override these functions, but it depends on what you want to do.

The from_crawler method (with the @classmethod decorator) is a factory method that will be used by Scrapy to instantiate the object (spider, extension, middleware, etc) where you added it.

It's often used for getting a reference to the crawler object (that holds references to objects like settings, stats, etc) and then either pass it as arguments to the object being created or set attributes to it.

In the particular example you've pasted, it's being used to read the value from a CRAWLSPIDER_FOLLOW_LINKS setting and set it to a _follow_links attribute in the spider.

You can see another simple example of usage of the from_crawler method in this extension that uses the crawler object to get the value of a setting and passing it as parameter to the extension and to connect some signals to some methods.

The set_crawler method has been deprecated in the latest Scrapy versions and should be avoided.


scrapy-redis 的pipelines里面的process_item里面用到
deferToThread:twisted
什么是twisted？http://blog.sina.com.cn/s/blog_704b6af70100py9n.html

twisted是一个用python语言写的事件驱动的网络框架，他支持很多种协议，包括UDP,TCP,TLS和其他应用层协议，比如HTTP，SMTP，NNTM，IRC，XMPP/Jabber。 非常好的一点是twisted实现和很多应用层的协议，开发人员可以直接只用这些协议的实现。其实要修改Twisted的SSH服务器端实现非常简单。很多时候，开发人员需要实现protocol类。

```
scrapy-redis 理解(项目地址https://github.com/rolando/scrapy-redis):
	/example-project （可参考https://github.com/younghz/sr-chn）：
	/scrapy-redis
		/pipelines.py	将处理的items以spider.name:items 作为key 存储在redis队列中，以实现post-processing
				重写example里面的process_item.py来实现分布式处理item
		/scheduler.py	调度器
		/queue.py	实现爬虫队列策略

```
#不清空redis queue，允许爬取过程中暂停并恢复
SCHEDULER_PERSIST = True


```
如何访问设定(How to access settings)

设定可以通过Crawler的 scrapy.crawler.Crawler.settings 属性进行访问。其由插件及中间件的 from_crawler 方法所传入:

class MyExtension(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        if settings['LOG_ENABLED']:
            print "log is enabled!"

```

使用bloomfilter 来进行去重

```

from pybloom import BloomFilter
from scrapy.utils.job import job_dir
from scrapy.dupefilter import BaseDupeFilter

class BLOOMDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, path=None):
        self.file = None
        self.fingerprints = BloomFilter(2000000, 0.00001)

    @classmethod
    def from_settings(cls, settings):
        return cls(job_dir(settings))

    def request_seen(self, request):
        fp = request.url
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)

    def close(self, reason):
        self.fingerprints = None



# Somewhere in settings.py
DUPEFILTER_CLASS = "project_name.bloom_filter.BLOOMDupeFilter"

```


有关分布式爬虫和scrapy-redis的问题？去重策略和怎么爬取整个网站？
爬虫的问题：
从首页里的链接一层一层爬取整个网站的页面。
那如何停止的？（判断把整个网站爬取完的条件是什么？）
scrapy-redis的疑问：
去重问题：
dupefilter.py里面的源码：
```

def request_seen(self, request):
        fp = request_fingerprint(request)
        added = self.server.sadd(self.key, fp)
        return not added
```

去重是把request 的fingerprint存在redis上来实现的吧？那大规模抓取不就很耗费内存？每条没读过的链接都存。
有没有人试过用bloomfilter结合scrapy—redis来去重。有没有必要？
