# atomic

> [Go：有了 sync 为什么还有 atomic？](https://mp.weixin.qq.com/s?__biz=MzAxMTA4Njc0OQ==&mid=2651451642&idx=1&sn=8626afd9df7dbbf63855784a6e628368&scene=21#wechat_redirect)

atomic 不是灵丹妙药，它显然不能替代互斥锁，但是当涉及到可以使用读取-复制-更新[1]模式管理的共享资源时，它非常出色。在这种技术中，我们通过引用获取当前值，当我们想要更新它时，我们不修改原始值，而是替换指针（因此没有人访问另一个线程可能访问的相同资源）。前面的示例无法使用此模式实现，因为它应该随着时间的推移扩展现有资源而不是完全替换其内容，但在许多情况下，读取-复制-更新是完美的。


> 只有一个地方写，多个地方读，可以直接通过cow的方式进行原子指针赋值操作减少并发竞争状态

# unused

golang有什么轮子能找到从未被调用的函数和逻辑么 手动清理没调用的函数太累了


https://github.com/dominikh/go-tools/tree/master/unused


golangci-lint / staticcheck 里有个叫 unused 的 checker


## pprof

> - [golang 内存分析/内存泄漏](https://cloud.tencent.com/developer/article/1703742)

## 内存泄露

内存泄露指的是程序运行过程中已不再使用的内存，没有被释放掉，导致这些内存无法被使用，直到程序结束这些内存才被释放的问题。

内存profiling记录的是堆内存分配的情况，以及调用栈信息，并不是进程完整的内存情况。基于抽样和它跟踪的是已分配的内存，而不是使用中的内存，（比如有些内存已经分配，看似使用，但实际以及不使用的内存，比如内存泄露的那部分），所以不能使用内存profiling衡量程序总体的内存使用情况。

**只能通过heap观察内存的变化，增长与减少，内存主要被哪些代码占用了，程序存在内存问题，这只能说明内存有使用不合理的地方，但并不能说明这是内存泄露。**

heap在帮助定位内存泄露原因上贡献的力量微乎其微。能通过heap找到占用内存多的位置，但这个位置通常不一定是内存泄露，就算是内存泄露，也只是内存泄露的结果，并不是真正导致内存泄露的根源。

### （1）怎么用heap发现内存问题

使用pprof的heap能够获取程序运行时的内存信息，在程序平稳运行的情况下，每个一段时间使用heap获取内存的profile，然后使用base能够对比两个profile文件的差别，就像diff命令一样显示出增加和减少的变化：


### （2）goroutine泄露怎么导致内存泄露

每个goroutine占用2KB内存，泄露1百万goroutine至少泄露2KB \* 1000000 = 2GB内存。此外goroutine执行过程中还存在一些变量，如果这些变量指向堆内存中的内存，GC会认为这些内存仍在使用，不会对其进行回收，这些内存谁都无法使用，造成了内存泄露。

所以goroutine泄露有2种方式造成内存泄露：

*   goroutine本身的栈所占用的空间造成内存泄露。
*   goroutine中的变量所占用的堆内存导致堆内存泄露，这一部分是能通过heap profile体现出来的。

**分析goroutine本身的栈所占用的空间造成内存泄露，可以通过pprof来查找，方法与heap类似，都是取两次采样做比较。**



cum: 累计量。指该函数加上该函数调用的函数总耗时






----


## 类型转换

（1）、语法：<结果类型> := < 目标类型 > ( < 表达式 > )

（1）语法：

　　<目标类型的值>，< 布尔参数 > := < 表达式 >.(目标类型) // 安全类型断言

　　<目标类型的值> := < 表达式 >.(目标类型)　　// 非安全类型断言


t,ok := i.(T)
这种写法下，如果发生接口未实现时，将会把 ok 置为 false，t 置为 T 类型的 0 值。正常实现时，ok 为 true。这里 ok 可以被认为是：i 接口是否实现 T 类型的结果。

---
## gvm



gvm 需要先安装1.4以上。 只能通过二进制安装

gvm install go1.4 -b

```
gvm install go1.8.3

gvm list

gvm use go1.11 --default

go clean -modcache

gvm uninstall go1.12.13
```
gvm install 其实是先clone github的goland/go项目到 ~/.gvm/archive/go/ 目录下

---
## cmd

go env

---
## GOROOT
GOROOT在GO语言中表示的是go语言编译、工具、标准库等的安装路径

你的 Go 安装目录（$GOROOT）的文件夹结构应该如下所示：

README.md, AUTHORS, CONTRIBUTORS, LICENSE

```
/bin：包含可执行文件，如：编译器，Go 工具
/doc：包含示例程序，代码工具，本地文档等
/lib：包含文档模版
/misc：包含与支持 Go 编辑器有关的配置文件以及 cgo 的示例
/os_arch：包含标准库的包的对象文件（.a）
/src：包含源代码构建脚本和标准库的包的完整源代码（Go 是一门开源语言）
/src/cmd：包含 Go 和 C 的编译器和命令行脚本
```

## GOPATH
GOPATH环境变量则表示go的工作目录，这个目录指定了需要从哪个地方寻找GO的包、可执行程序等，这个目录可以是多个目录表示。

bin目录包含了可执行程序，注意是可执行的，不需要解释执行。

pkg目录用于存放通过go install 命令安装某个包后的归档文件。归档文件是指那些名称以“.a”结尾的文件。

src里面包含了go的代码源文件，其中仍按包的不同进行组织。


---
## build

go build 命令来测试该包的编译
`go build github.com/user/stringutil`


使用“go build+文件列表”方式编译时，可执行文件默认选择文件列表中第一个源码文件作为可执行文件名输出。

如果需要指定输出可执行文件名，可以使用-o参数

- https://go-zh.org/doc/code.html
- http://c.biancheng.net/view/120.html


---
## package

 包只是一个包含一些代码文件的**目录**，它可以从同一个入口引入并可以使用其中的代码或变量（ features ）

 > 包简单理解成是一个包含了多个 .go 文件的目录

## install

go install <package> 命令后，系统会尝试在指定的包目录里寻找带有 **main** 包声明的文件。找到之后，Go 就知道这是可执行的程序，需要被编译为二进制文件。一个包里可以有很多文件，但是**只能其中一个文件里有 main 函数**，标志着这个文件是程序的入口文件。

如果一个包中没有带有 main 包声明的文件，那么，Go 就会在 **pkg 目录中创建一个 包管理 (.a) 文件**。 这不是一个二进制文件，因此是不可执行的。


Go源文件中的第一个语句必须是

`package 名称`

这里的 名称 即为导入该包时使用的默认名称。 （**一个包中的所有文件都必须使用相同的 名称**。）

Go的约定是包名为导入路径的最后一个元素：作为 “crypto/rot13” 导入的包应命名为 rot13

包的名字应避免使用下划线，中划线或掺杂大写字母。


### scope

scope 是指代码块中可以访问已定义变量的区域。包的 scope 是指在一个包中 (包括**包里的所有文件**) 可以访问已定义变量的区域。这个区域是包中所有文件的顶层块。

如果变量 a 依赖于变量 b，那么就要先初始化变量 b，否则程序就无法编译。Go 在函数内部会遵循这个原则。但是在包的 scope 中定义的变量，它们**在初始化周期中就已经被声明了**。

关于包 scope 的另一个例子就是，可以在另一个文件中的函数 f 中引用入口文件的变量 c。

> 相当于python默认把包内的所有文件import，并能试用各个文件的scope变量

### init 函数
跟 main 函数一样，当**初始化包的时候，init 函数也会被执行**。它**没有参数，也没有返回值**。init 函数是由 Go 来声明的，你无法引用这个函数（ 也不能用类似 *init()* 的方式调用它）。你可以在一个文件或一个包中定义多个 init 函数。在同一个文件中，init 函数是按照**它们被定义的先后顺序被执行的**。

> `init` 函数 的主要工作就是，初始化无法在全局范围内初始化的全局变量 。例如，初始化数组。

```
go run *.go
├── 执行 Main 包
├── 初始化所有引用的包
|  ├── 初始化所有引用的包 (recursive definition)
|  ├── 初始化全局变量
|  └── 以词法文件名的顺序调用 init 函数
└── 初始化 Main 包
   ├── 初始化全局变量
   └── 以词法文件名的顺序调用 init 函数
```

- [golang 之 import 和 package 的使用](https://segmentfault.com/a/1190000018235929)
- [Go 语言包管理（Package）必知必会](https://learnku.com/golang/t/27649#3b424b)


### import

> golang 使用包 package 来管理定义模块，可以使用 import 关键字来导入使用。

如果导入的是 go 自带的包，则会去安装目录 $GOROOT/src 按包路径加载，如 fmt 包

如果是我们 go get 安装或自定义的包，则会去`$GOPATH/src`下加载

_ 是包引用操作，只会执行包下各模块中的 init 方法，并不会真正的导入包，所以不可以调用包内的其他方法


`go get` 就会自动地获取、构建并安装它, -d 只下载 不安装  -x 显示相关的调试日志。

指定的包不在工作空间中，go get 就会将会将它放到 GOPATH 指定的第一个工作空间内

Go 能够辨别出 entry.go 是应用的入口文件，因为它里面有 main 函数


import 其实是导入目录，而不是定义的 package 名字，虽然我们一般都会保持一致，但其实是可以随便定义目录名，只是使用时会很容易混乱，不建议这么做。

例如：package big ，我们 import “math/big” ，其实是在 src 中的 src/math 目录。在代码中使用 big.Int 时，big 指的才是 Go 文件中定义的 package 名字。



---
###  go mod

安装后，我们可以通过以下两种方式之一激活模块支持：

- 在$GOPATH/src 之外的目录中调用 go 命令，且当前目录或其任何父目录中使用有效的 go.mod 文件，并且环境变量 GO111MODULE 未设置（或显式设置为auto）。
- 在环境变量集上设置 GO111MODULE = on 后，调用go命令。

`go build ./...`  ./... 模式匹配当前模块中的所有包

`go mod vendor` 回到 godep 或 govendor 使用的 vendor 目录进行包管理的方式

`go build -mod=vendor `来构建项目

> 当modules 功能启用时，依赖包的存放位置变更为$GOPATH/pkg，允许同一个package多个版本并存，且多个项目可以共享缓存的 module。


使用 internal package 的方法跟以前已经不同了，由于 go.mod会扫描同工作目录下所有 package 并且变更引入方法，必须将 helloworld（对应go mod init XX ）当成路径的前缀，也就是需要写成 import helloworld/api，以往 GOPATH/dep 模式允许的 import ./api 已经失效

modules 可以通过在 go.mod 文件中使用 replace 指令替换成github上对应的库


问题一：依赖的包下载到哪里了？还在GOPATH里吗？

不在。使用Go的包管理方式，依赖的第三方包被下载到了$GOPATH/pkg/mod路径下。

如果你成功运行了本例，可以在您的$GOPATH/pkg/mod 下找到一个这样的包 github.com/astaxie/beego@v1.11.1

Q: 为什么在$GOPATH/pkg/mod的目录里找不到go-clean-arch自身调用的源代码

A: 因为在go.mod上声明了module github.com/bxcodec/go-clean-arch ， 故import调用的就是go-clean-arch的代码，vs code的跳转也说明了这个问题。

vs code如何支持mod的跳转: https://github.com/Microsoft/vscode-go/wiki/Go-modules-support-in-Visual-Studio-Code


用 go help module-get 和 go help gopath-get分别去了解 Go modules 启用和未启用两种状态下的 go get 的行为

goland 的配置，好像得设一下代理: https://goproxy.io



参考链接:

- [go mod 使用](https://juejin.im/post/5c8e503a6fb9a070d878184a)
- [Go的包管理工具（三）：Go Modules](https://juejin.im/post/5c7fc2b1f265da2dac4575fc)
- [拜拜了，GOPATH君！新版本Golang的包管理入门教程](https://juejin.im/post/5c9c8c4fe51d450bc9547ba1)
- [干货满满的 Go Modules 和 goproxy.cn](https://juejin.im/post/5d8ee2db6fb9a04e0b0d9c8b#heading-10)
- [go-module](http://wjp2013.github.io/go/go-module/)


---
# vendor

go get git.com/XX 会把项目拉到src目录里，vscode也会相应得去完成找。
如果有vendor目录也会找该目录下面的源。

Go get 命令默认禁用terminal prompt，即终端提示

`export GIT_TERMINAL_PROMPT=1`

> 主要是没理解是怎么找源的、go get 的原理


`git config --global url."git@git.umlife.net:".insteadOf "https://git.umlife.net/"`


`go get -u -v  git.umlife.net/mt-service/anti-crawler-control`
相当于git clone  git@git.umlife.net:mt-service/anti-crawler-control.git

https 则需要生成access-token VNdA5Ym5WhvsWygy8NQZ

- [如何使用 go get 下载 gitlab 私有项目](https://tangxusc.github.io/blog/2019/03/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8-go-get-%E4%B8%8B%E8%BD%BD-gitlab-%E7%A7%81%E6%9C%89%E9%A1%B9%E7%9B%AE/)
- [access-token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
)


---

# TODO: Go语言如何进阶？

- [Go语言如何进阶？](https://www.zhihu.com/question/399923003/answer/1300151492)

---

# archive

- [Go编程时光](http://golang.iswbm.com/en/latest/)

第二章：面向对象，第四章：并发编程。讲的都是比较贴切实际。特别是context的介绍。可以用作go的常见查阅资料。

---


# 那如何判断动态值是否为空？

> https://blog.csdn.net/lanyang123456/article/details/83715090

可以借助反射来判断。

```go
func IsNil(i interface{}) bool {
    defer func() {
        recover()
    }()
    vi := reflect.ValueOf(i)
    return vi.IsNil()
}

```

其中，`IsNil`定义如下：

```go
func (v Value) IsNil() bool

```

参数v必须是`chan, func, interface, map, pointer, or slice`，否则会panic。

如果调用IsNil的不是一个指针，会出现异常，需要捕获异常。
或者修改成这样：

```go
func IsNil(i interface{}) bool {
    vi := reflect.ValueOf(i)
    if vi.Kind() == reflect.Ptr {
        return vi.IsNil()
    }
    return false
}

```

## 总结

一个接口包括动态类型和动态值。 如果一个接口的动态类型和动态值都为空，则这个接口为空的。

> 应该尽量避免使用这样的场景

---
# panic: assignment to entry in nil map


> - [panic: assignment to entry in nil map](https://www.cnblogs.com/liuqun/p/14161134.html)

golang中map是引用类型，应用类型的变量未初始化时默认的zero value是nil。直接向nil map写入键值数据会导致运行时错误

panic: assignment to entry in nil map

因为在声明alphabetMap后并未初始化它，所以它的值是nil, 不指向任何内存地址。需要通过make方法分配确定的内存地址。程序修改后即可正常运行:

同为引用类型的slice，在使用append 向nil slice追加新元素就可以，原因是append方法在底层为slice重新分配了相关数组让nil slice指向了具体的内存地址


----
# Go内存管理之代码的逃逸分析

- [Go内存管理之代码的逃逸分析](https://mp.weixin.qq.com/s?__biz=MzUzNTY5MzU2MA==&mid=2247485579&idx=1&sn=f481cff4ffccacc186a020e45e884924&scene=21#wechat_redirect)

Q：如何得知变量是分配在栈（stack）上还是堆（heap）上？

A: 准确地说，你并不需要知道。Golang 中的变量只要被引用就一直会存活，存储在堆上还是栈上**由内部实现决定**而和具体的语法没有关系。知道变量的存储位置确实对程序的效率有帮助。如果可能，Golang 编译器会将函数的局部变量分配到函数栈帧（stack frame）上。然而，如果编译器**不能确保变量在函数 return 之后不再被引用，编译器就会将变量分配到堆上**。而且，如果**一个局部变量非常大**，那么它也应该被分配到堆上而不是栈上。当前情况下，**如果一个变量被取地址**，那么它就有可能被分配到堆上。然而，还要对这些变量做逃逸分析，如果函数 return 之后，变量不再被引用，则将其分配到栈上

简单来说，逃逸分析也是了解我们应该如何优化应用程序性能的一种方式。通过上面的分析可以看出来，**虽然指针能够减少变量在函数间传递时的数据值拷贝问题**，但是也不应该所有类型的数据都应该返回其指针。**如果分配到堆上的共享变量太多的话也无形中增加了GC的压力。**

- [生产环境Go程序内存泄露，用pprof如何快速定位](https://mp.weixin.qq.com/s/PEpvCqpi9TPhVuPdn3nyAg)


---
# 切片

- [Go 切片这道题，吵了一个下午！](https://mp.weixin.qq.com/s?__biz=MzUxMDI4MDc1NA==&mid=2247491675&idx=1&sn=5a887e874999251201c90744434d2471&scene=21#wechat_redirect)

```go
func main() {
 sl := make([]int, 0, 10)
 var appenFunc = func(s []int) {
  s = append(s, 10, 20, 30)
 }
 appenFunc(sl)
 fmt.Println(sl)
 fmt.Println(sl[:10])
}

```

结果：
```
[]
[10 20 30]
[]
[10 20 30 0 0 0 0 0 0 0]
```

go的切片传递，更改了数据会影响外层，但是外层的len没有变化。



- [又吵起来了，Go 是传值还是传引用？](https://mp.weixin.qq.com/s?__biz=MzUxMDI4MDc1NA==&mid=2247489302&idx=1&sn=c787d1fa4546e12c7e55e880da73c91f&scene=21#wechat_redirect)

```go
func main() {
 m := make(map[string]string)
 m["脑子进煎鱼了"] = "这次一定！"
 fmt.Printf("main 内存地址：%p\n", &m)
 hello(m)

 fmt.Printf("%v", m)
}

func hello(p map[string]string) {
 fmt.Printf("hello 内存地址：%p\n", &p)
 p["脑子进煎鱼了"] = "记得点赞！"
}
```

结果:
```
main 内存地址：0xc00000e028
hello 内存地址：0xc00000e038
map[脑子进煎鱼了:记得点赞！]
```

`func makemap(t *maptype, hint int, h *hmap) *hmap {}`。这是创建 map 类型的底层 runtime 方法，注意其返回的是 *hmap 类型，是一个指针。也就是 Go 语言通过对 map 类型的相关方法进行封装，达到了用户需要关注指针传递的作用。


留意到代码 value.Pointer，标准库进行了特殊处理，直接对应的值的指针地址，当然就不需要取地址符了。其在内部转换的 Data 属性，正正是 Go 语言中 slice 类型的运行时表现 SliceHeader。我们在调用 %p 输出时，是在输出 slice 的底层存储数组元素的地址。


---
# Go单测
- [Go单测从零到溜系列—6.编写可测试的代码](https://mp.weixin.qq.com/s/hzVIMDhPQXtWoBIj0Aueug)

不要隐式引用外部依赖（全局变量、隐式输入等），而是通过依赖注入的方式引入依赖。经过这样的修改之后，构造函数NewServer 的依赖项就很清晰，同时也方便我们编写 mock 测试代码。



----
# GO 错误

- [go1.13中的错误处理(2019) - Go语言学习笔记](https://skyao.io/learning-go/feature/error/go1.13-errors.html)
- [Working with Errors in Go 1.13 - The Go Programming Language](https://go.dev/blog/go1.13-errors)

## 是否封装


当向 error 添加额外的上下文时，无论是使用 fmt.Errorf 还是通过实现自定义类型，您都需要决定新的 error 是否应该封装原始 error。这个问题没有唯一的答案，它取决于创建新 error 的上下文。封装一个error 以将其暴露给调用者。如果这样做会暴露实现细节，则不要包装error。

这时，如果你不想破坏你的客户端，即使你切换到不同的数据库包，函数必须总是返回 sql.ErrNoRows 。换句话说，包装一个错误使该错误成为你的API的一部分。如果你不想承诺在未来支持该错误作为你的API的一部分，你就不应该包装该错误。


重要的是要记住，无论你是否封装，错误文本都是一样的。试图理解该错误的人无论用哪种方式都会得到相同的信息；选择封装是为了给程序提供额外的信息，以便他们能够做出更明智的决定，还是**为了保留抽象层而不提供该信息**。

> 封装原始的错误信息，造成的影响就是外部必须依赖该原始错误，无法替换掉原始基础库。高耦合。




---
# gock


- [gock:mock http 请求的实现原理及使用 - 简书](https://www.jianshu.com/p/57bb30073663)
- [h2non/gock: HTTP traffic mocking and testing made easy in Go ༼ʘ̚ل͜ʘ̚༽](https://github.com/h2non/gock)
- [Go单测从零到溜系列—1.mock网络测试](https://mp.weixin.qq.com/s?__biz=MzU5MjAxMDc1Ng==&mid=2247484588&idx=1&sn=6e640ea9c988a3abe4d08adc6c1cd18d&chksm=fe270fc7c95086d1379edbe1a98120ca6278c0329ee527d4490c9738a4fe15ba1b29c8b7dd88&cur_album_id=1338144742571458563&scene=189#wechat_redirect)

其实 gock 主要是是改变了request Client 的 Transport。gock 定义了一个新的 Transport 替换了request Client 的 Transport (http.DefaultTransport )，新的 Transport 结构体重写了 RoundTrip 方法，主要是在这个方法对 http request 进行拦截，去匹配 mock 的 request.


---
# gorm

> - [go - GORM doesnt update boolean field to false - Stack Overflow](https://stackoverflow.com/questions/56653423/gorm-doesnt-update-boolean-field-to-false)


```go
// Update attributes with `struct`, will only update non-zero fields
db.Model(&user).Updates(User{Name: "hello", Age: 18, Active: false})
// UPDATE users SET name='hello', age=18, updated_at = '2013-11-17 > 21:34:10' WHERE id = 111;

// Update attributes with `map`
db.Model(&user).Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
// UPDATE users SET name='hello', age=18, actived=false, updated_at='2013-11-17 21:34:10' WHERE id=111;
NOTE When upda
```


---
# 值复制成本
- [值复制成本 - Go语言101（通俗版Go白皮书）](https://gfw.go101.org/article/value-copy-cost.html)

为了防止在函数传参和通道操作中因为值复制代价太高而造成的性能损失，我们**应该避免使用大尺寸的结构体和数组类型做为参数类型和通道的元素类型**，应该在这些场合下使用基类型为这样的大尺寸类型的指针类型。 另一方面，我们也要考虑到**太多的指针将会增加垃圾回收的压力**。所以到底应该使用大尺寸类型还是以大尺寸类型为基类型的指针类型做为参数类型或通道的元素类型取决于具体的应用场景。

如果一个数组或者切片的元素类型是一个大尺寸类型，我们应该避免在for-range循环中使用双循环变量来遍历这样的数组或者切片类型的值中的元素。 因为，在遍历过程中，每个元素将被复制给第二个循环变量一次。

---
# Go中的nil
- [Go中的nil - Go语言101（通俗版Go白皮书）](https://gfw.go101.org/article/nil.html)

同一个类型的两个nil值可能不能相互比较
在Go中，映射类型、切片类型和函数类型是不支持比较类型。 比较同一个不支持比较的类型的两个值（包括nil值）是非法的。 比如，下面的几个比较都编译不通过。

```
var _ = ([]int)(nil) == ([]int)(nil)
var _ = (map[string]int)(nil) == (map[string]int)(nil)
var _ = (func())(nil) == (func())(nil)
```
但是，映射类型、切片类型和函数类型的任何值都可以和类型不确定的裸nil标识符比较。
```
// 这几行编译都没问题。
var _ = ([]int)(nil) == nil
var _ = (map[string]int)(nil) == nil
var _ = (func())(nil) == nil
```
