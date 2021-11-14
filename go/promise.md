go 如何实现类似node的promise呢？

最简单的异步转同步
```go
done := make(chan struct{})
go func() {
	// do work asynchronously here
	//
	close(done)
}()
<-done
```

封装一层

```go
// Represent the promise
type Promise struct {
	done chan struct{}
	res  interface{}
	err  error
}

type WorkFunc func() (interface{}, error)

func NewPromise(workFunc WorkFunc) *Promise {
	promise := Promise{done: make(chan struct{})}
	go func() {
		defer close(promise.done)
		promise.res, promise.err = workFunc()
	}()
	return &promise
}

func (p *Promise) Done() (interface{}, error) {
	<-p.done
	return p.res, p.err
}

func (p *Promise) Then(successHandler SuccessHandler, errorHandler ErrorHandler) *Promise {
	newPromise := &Promise{done: make(chan struct{})}
	go func() {
		res, err := p.Done()
		defer close(newPromise.done)
		if err != nil {
			if errorHandler != nil {
				newPromise.res = errorHandler(err)
			} else {
				newPromise.err = err
			}
		} else {
			if successHandler != nil {
				newPromise.res, newPromise.err = successHandler(res)
			} else {
				newPromise.res = res
			}
		}
	}()

	return newPromise
}

```

思路主要是:  new 一个含有chan的属性的对象，然后把方法传近去，调用done的时候返回相应的方法结果。然后链式的方法是then里面再new一个promise，调用上一个promise的done进行同步，然后异步相应的成功和失败函数，后通过done捕获相应的异步结果。

---
## Active Object

Active Object设计模式解耦了方法的调用和方法的执行，方法的调用和方法的执行运行在不同的线程之中(或者纤程、goroutine, 后面不再一一注释)。它引入了异步方法调用，允许应用程序可以并发的处理多个客户端的请求，通过调度器进行调用并发的方法执行，提供了并发执行方法的能力。

并发对象需要在各个线程之间共享，免不了要使用锁等同步方式控制并发对象的访问，这就要求我们为了保证服务的质量，需要设计程序满足：

- 对并发对象的方法调用不应该阻塞完整的处理流程
- 同步访问并发对象应该设计简单
- 应用程序应该透明的使用软硬件的并发能力


```go
type MethodRequest int

const (
	Incr MethodRequest = iota
	Decr
)

type Service struct {
	queue chan MethodRequest
	v     int
}

func New(buffer int) *Service {
	s := &Service{
		queue: make(chan MethodRequest, buffer),
	}
	go s.schedule()
	return s
}

func (s *Service) schedule() {
	for r := range s.queue {
		if r == Incr {
			s.v++
		} else {
			s.v--
		}
	}
}

func (s *Service) Incr() {
	s.queue <- Incr
}

func (s *Service) Decr() {
	s.queue <- Decr
}
```

可以看到思路大概是，new一个chan，然后go异步监听这个队列的信息，然后通过调用相应的函数，传递相应的信息给chan，达到并发同步执行的目的。

它将上下文(请求参数和返回)封装成一个Call对象, call对象的done字段提供了future的功能。你可以利用它获取方法是否已经执行完毕。

思路应该是立刻返回一个上下文的对象，但是该对象是包含相应chan的，需要获取结果的时候，调用/监听相应的chan.done() 来判断同步获取异步数据。


如果有一个常驻协程在异步的处理任务，而且是FIFO的，那么这其实是相当于一个无锁的设计，可以简化对临界资源的操作。

思路： actor.do(work_fun)返回一个promise，该promise包成一个methodRequest发送到一个actor.queue的队列里面。`actor.queue <- methodRequest`然后在永远执行的异步任务里面去对promise进行监听进行同步执行，并附带相应的结果回到对象里面，然后close掉promise的chan，达到promise.Done()的时候，能监听到何时执行完，同步获取到结果。

---
## 批量处理

在for循环每次select的时候，都会实例化一个一个新的定时器。该定时器在3分钟后，才会被激活，但是激活后已经跟select无引用关系，被gc给清理掉。 

time.After(d)在d时间之后就会fire，然后被GC回收，不会造成资源泄漏的。但是如果一直for 创建，会一直堆积。可以通过创建后删除的方法。

在go代码中，在for循环里不要使用select + time.After的组合，可以使用time.NewTimer替代

```go
package main

import "time"

func main() {
    for {
        t := time.NewTimer(3*time.Second)

        select {
        case <- t.C:
        default:
            t.Stop()
        }
    }
}
```
那能去到t.C上吗？


---
## 参考链接：
- [如何把golang的Channel玩出async和await的feel](https://juejin.im/post/5e4175a36fb9a07ca80a9c77)
- [Go并发设计模式之 Active Object](https://mp.weixin.qq.com/s/D-3-Bpl5UZ_w_tnUHh6UaA)
- [如何用Golang的channel实现消息的批量处理](https://juejin.im/post/5d8c6775e51d45781332e91f)
- [GOLANG中time.After释放的问题](https://studygolang.com/articles/10528)