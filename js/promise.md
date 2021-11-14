#promise基本概念

>promise只有三种状态，未完成，完成(fulfilled)和失败(rejected)。

>promise的状态可以由未完成转换成完成，或者未完成转换成失败。

>promise的状态转换只发生一次

```

function getInitialPromise() {

  return defer.promise;

}



promiseSomething().then(function(fulfilled){

        //当promise状态变成fulfilled时，调用此函数

    },function(rejected){

        //当promise状态变成rejected时，调用此函数

    },function(progress){

        //当返回进度信息时，调用此函数

    });

```

## promise的传递

- then方法会返回一个promise，在下面这个例子中，我们用outputPromise指向then返回的promise。



- 当function(fulfilled)或者function(rejected)返回一个值，比如一个字符串，数组，对象等等，那么outputPromise的状态就会变成fulfilled。

- 当function(fulfilled)或者function(rejected)抛出异常时，那么outputPromise的状态就会变成rejected

- 当function(fulfilled)或者function(rejected)返回一个**promise**时，outputPromise就会成为这个新的promise.

这样做有什么意义呢? 主要在于聚合结果(Q.all)，管理延时，异常恢复等等

## 方法传递

- 方法传递有些类似于Java中的try和catch。当一个异常没有响应的捕获时，这个异常会接着往下传递。

方法传递的含义是当一个状态没有响应的回调函数，就会沿着then往下找。

- 如果inputPromise的状态由未完成变成fulfilled, 此时对fulfil的处理会由outputPromise来完成。

- 可以使用fail(function(error))来专门针对错误处理，而不是使用then(null,function(error))

- 可以使用progress(function(progress))来专门针对进度信息进行处理，而不是使用 then(function(success){},function(error){},function(progress){})



## promise链



- promise链提供了一种让函数顺序执行的方法。

函数顺序执行是很重要的一个功能。比如知道用户名，需要根据用户名从数据库中找到相应的用户，然后将用户信息传给下一个函数进行处理。



```

function foo(result) {
    console.log(result);
    return result+result;
}
//手动链接
Q('hello').then(foo).then(foo).then(foo);                                   //控制台输出： hello
                                                                            //             hellohello
                                                                            //             hellohellohello

//动态链接
var funcs = [foo,foo,foo];
var result = Q('hello');
funcs.forEach(function(func){
    result = result.then(func);
});
//精简后的动态链接
funcs.reduce(function(prev,current){
    return prev.then(current);
},Q('hello'));
```

我们可以通过Q.all([promise1,promise2...])将多个promise组合成一个promise返回。 注意：

1. 当all里面所有的promise都fulfil时，Q.all返回的promise状态变成fulfil

2. 当任意一个promise被reject时，Q.all返回的promise状态立即变成reject



## 结束promise链



通常，对于一个promise链，有两种结束的方式。

1. 返回最后一个promise

如 ```return foo().then(bar);```

2. 通过done来结束promise链

如 ```foo().then(bar).done()```

为什么需要通过done来结束一个promise链呢? 如果在我们的链中有错误没有被处理，那么在一个正确结束的promise链中，这个没被处理的错误会通过异常抛出。

﻿


####Promise是抽象异步处理对象以及对其进行各种操作的组件。


```js
var promise = new Promise(function(resolve, reject) {
    // 异步处理
    // 处理结束后、调用resolve 或 reject
});
```

