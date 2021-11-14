# 控制反转

控制反转（Inversion of Control，缩写为IoC），是面向对象编程中的一种设计原则，可以用来减低计算机代码之间的耦合度。其中最常见的方式叫做依赖注入（Dependency Injection，简称DI），还有一种方式叫“依赖查找”（Dependency Lookup）。通过控制反转，对象在被*创建*的时候，由一个调控系统内所有对象的外界实体将其所依赖的对象的*引用传递*给它。也可以说，依赖被注入到对象中。

> 简单来说，a依赖b，但a不控制b的创建和销毁，仅使用b，那么b的控制权交给a之外处理，这叫控制反转（IOC）

## 依赖注入

而a要依赖b，必然要使用b的instance，那么

- 通过a的接口，把b传入；
- 通过a的构造，把b传入；
- 通过设置a的属性，把b传入；
这个过程叫依赖注入（DI）。

## IOC Container
随着DI的频繁使用，要实现IOC，会有很多重复代码，甚至随着技术的发展，有更多新的实现方法和方案，那么有人就把这些实现IOC的代码打包成组件或框架，来避免人们重复造轮子。

所以实现IOC的组件或者框架，我们可以叫它IOC Container。


- [如何用最简单的方式解释依赖注入？依赖注入是如何实现解耦的?](https://www.zhihu.com/question/32108444/answer/220819349)
- [设计模式之—：控制反转IoC](https://www.jianshu.com/p/5aaaf24e6c09): 实例一则

---

# Why is IoC / DI not common in Python?

- [why-is-ioc-di-not-common-in-python](https://stackoverflow.com/questions/2461702/why-is-ioc-di-not-common-in-python)
- [我们为什么要用IoC和AOP](https://www.jianshu.com/p/feb9521388cf): 本质是组件的调用方参与了组件的创建和配置工作。


因此，DI容器只不过是动态脚本语言的解释器。实际上，让我重新表述一下：一个典型的Java/.netdi容器只不过是一个糟糕的动态脚本语言的蹩脚解释器，它的语法非常难看，有时是基于XML的。

所以，概括一下：DI/IoC的实践在Python中和在Java中一样重要，原因完全相同。然而，DI/IoC的实现是**内置于该语言中的**，并且常常是如此轻量级以至于它完全消失。

The best example is how you set up a Django application using settings.py:

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL + '/1',
    },
    'local': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'snowflake',
    }
```

部分原因是模块系统在Python中的工作方式。你可以**免费得到一种“单例”，只需从一个模块导入它**。在模块中定义一个对象的实际实例，然后任何客户机代码都可以导入它，并实际获得一个工作的、完全构造/填充的对象。

这与Java不同，Java不导入对象的实际实例。这意味着**您必须自己实例化它们**（或者使用某种IoC/DI风格的方法）。您可以通过使用**静态工厂方法**（或实际的工厂类）来减轻自己实例化所有内容的麻烦，但是**每次实际创建新的工厂方法仍然会带来资源开销**。

> python的依赖注入、控制反转内置于该语言中的，而且自带单例。java必须使用工厂方法来解耦，但是创建也会带来资源开销，所以才会有IOC Container
