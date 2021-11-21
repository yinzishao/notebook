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


`go get` 就会自动地获取、构建并安装它, -d 只下载 不安装

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
