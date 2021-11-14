Linux 操作系统的启动首先从 BIOS 开始，接下来进入 boot loader，由 bootloader 载入内核，进行内核初始化。内核初始化的最后一步就是启动 pid 为 1 的 init 进程。这个进程是系统的第一个进程。它负责产生其他所有用户进程。

# [启动过程](https://wiki.archlinux.org/index.php/Arch_boot_process_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

所谓 BIOS 或 Basic Input-Output System, 就是开机时第一个被执行的程序，又名固件。一般来说它储存在主板上的一块闪存中，与硬盘彼此独立。

BIOS 被启动后，会按启动顺序加载磁盘的前 512 字节，即主引导记录，前 440 字节包含某个启动引导器，像 GRUB 、Syslinux 和 LILO 之类的第一启动阶段代码。因为空间太小了，后续的启动代码保存在磁盘上，最后启动引导器又通过「链式引导」，或是直接加载内核，以加载一个操作系统。


UEFI 不仅能读取分区表，还能自动支持文件系统。所以它不像 BIOS，已经没有仅仅 440 字节可执行代码即 MBR 的限制了，它完全用不到 MBR。

不管第一块上有没有 MBR，UEFI 都不会执行它。相反，它依赖分区表上的一个特殊分区，叫 EFI 系统分区，里面有 UEFI 所要用到的一些文件。计算机供应商可以在 <EFI 系统分区>/EFI/<VENDOR NAME>/ 文件夹里放官方指定的文件，还能用固件或它的 shell，即 UEFI shell，来启动引导程序。EFI 系统分区一般被格式化成 FAT32，或比较非主流的 FAT16。




启动加载器是 BIOS 或 UEFI 启动的第一个程序。它负责使用正确的内核参数加载内核, 并根据配置文件加载初始化 RAM disk。


安装遇到的问题

base-devel 落后，需要安装官网按照

dhcpcd 需要自己安装后eable

---


启动过程

BIOS=》MBR (master boot record)=》boot loader=》kernel


- 计算机会自动从主板的BIOS(Basic Input/Output System)读取其中所存储的程序
- 计算机将从你所选择的存储设备中读取起始的512个字节(bytes),主引导记录MBR。 MBR会告诉电脑从该设备的**某一个分区**(partition)来**装载引导加载程序**(boot loader)
- 引导加载程序**储存有操作系统(OS)的相关信息**，比如操作系统名称，操作系统内核 (内核)所在位置等。常用的引导加载程序有GRUB和LILO。
- 内核实际上是一个用来操作计算机的程序，它是计算机操作系统的内核，主要的任务是管理计算机的硬件资源，充当软件和硬件的接口。操作系统上的任何操作都要通过内核传达给硬件。

> 实际上，我们可以在多个分区安装引导加载程序，每个引导加载程序对应不同的操作系统，在读取MBR的时候选择我们想要启动的引导加载程序。这就是多操作系统的原理。

* [Linux开机启动(bootstrap)](https://www.cnblogs.com/vamei/archive/2012/09/05/2672039.html)

---
# sysvinit

内核初始化的最后一步就是启动 pid 为 1 的 init 进程。init 以守护进程方式存在，是所有其他进程的祖先。Sysvinit 用术语 runlevel 来定义"预订的运行模式"。

sysvinit脚本严格按照启动数字的大小顺序执行，一个执行完毕再执行下一个，这非常有益于错误排查，但是串行地执行脚本导致 sysvinit 运行效率较慢。

Sysvinit 它**必须一次性把所有可能用到的服务都启动起来**，即使打印机并没有连接到系统，CUPS 服务也必须启动。

# UpStart

UpStart 基于**事件机制**，比如 U 盘插入 USB 接口后，udev 得到内核通知，发现该设备，这就是一个新的事件。**UpStart 在感知到该事件之后触发相应的等待任务**，比如处理/etc/fstab 中存在的挂载点。采用这种事件驱动的模式，upstart 完美地解决了即插即用设备带来的新问题。

采用事件驱动机制也带来了一些其它有益的变化，比如加快了系统启动时间。sysvinit 运行时是同步阻塞的。一个脚本运行的时候，后续脚本必须等待。这意味着所有的初始化步骤都是串行执行的，而实际上很多服务彼此并不相关，完全可以并行启动，从而减小系统的启动时间。

# Systemd

Systemd 能够更进一步提高并发性，即便对于那些 UpStart 认为**存在相互依赖而必须串行的服务**，比如 Avahi 和 D-Bus 也可以并发启动.

Systemd 可以提供按需启动的能力，只有在某个服务被真正请求的时候才启动它。当该服务结束，systemd 可以关闭它，等待下次需要时再次启动它。

UpStart 通过 strace 来跟踪 fork、exit 等系统调用，但是这种方法很笨拙，且缺乏可扩展性。systemd 则利用了 Linux 内核的特性即 **CGroup 来完成跟踪的任务**。当停止服务时，通过查询 CGroup，systemd 可以确保找到所有的相关进程，从而干净地停止服务。

Systemd 内建了自动挂载服务，无需另外安装 autofs 服务，可以直接使用 systemd 提供的自动挂载管理能力来实现 autofs 的功能。

systemd 维护一个"事务一致性"的概念，保证所有相关的服务都可以正常启动而不会出现互相依赖，以至于死锁的情况。

Systemd 用配置单元定义文件中的关键字来描述配置单元之间的依赖关系。比如：unit A 依赖 unit B，可以在 unit B 的定义中用"require A"来表示。这样 systemd 就会保证先启动 A 再启动 B。

循环依赖：required 是强依赖；want 则是弱依赖，systemd 将去掉 wants 关键字指定的依赖看看是否能打破循环。如果无法修复，systemd 会报错

## 并发启动原理

### 解决 socket 依赖

Linux 操作系统有一个特性，当进程调用 fork 或者 exec 创建子进程之后，所有**在父进程中被打开的文件句柄 (file descriptor) 都被子进程所继承**。套接字也是一种文件句柄，进程 A 可以创建一个套接字，此后当进程 A 调用 exec 启动一个新的子进程时，只要确保该套接字的 close_on_exec 标志位被清空，那么新的子进程就可以继承这个套接字。子进程看到的套接字和父进程创建的套接字是同一个系统套接字，就仿佛这个套接字是子进程自己创建的一样，没有任何区别。

和 inetd 类似，systemd 是所有其他进程的父进程，它可以先建立所有需要的套接字，然后在调用 exec 的时候将该套接字传递给新的服务进程，而新进程直接使用该套接字进行服务即可。

### 解决 D-Bus 依赖

D-Bus 是 desktop-bus 的简称，是一个低延迟、低开销、高可用性的进程间通信机制。它越来越多地用于应用程序之间通信，也用于应用程序和操作系统内核之间的通信。

D-Bus 支持所谓"bus activation"功能。如果服务 A 需要使用服务 B 的 D-Bus 服务，而服务 B 并没有运行，则 D-Bus 可以在服务 A 请求服务 B 的 D-Bus 时自动启动服务 B。而服务 A 发出的请求会被 D-Bus 缓存，服务 A 会等待服务 B 启动就绪。利用这个特性，依赖 D-Bus 的服务就可以实现并行启动。

### 解决文件系统依赖

Systemd 集成了 autofs 的实现，对于系统中的挂载点，比如/home，当系统启动的时候，systemd 为其**创建一个临时的自动挂载点**。在这个时刻/home 真正的挂载设备尚未启动好，真正的挂载操作还没有执行，文件系统检测也还没有完成。

- [浅析 Linux 初始化 init 系统](https://www.ibm.com/developerworks/cn/linux/1407_liuming_init1/index.html?ca=drs-)

---
# PMA

 PMA(Pluggable Authentication Module)是一个可插入式认证模块,在Linux系统中,各种不同的应用程序都需要完成认证功能,为了实现统一调配,把所有需要认证的功能做成一个模 块(认证机制特别复杂的除外,如:https),当特定的程序需要完成认证功能的时候,就去调用PMA的认证模块

## 第一个字段:验证类别(Type)

- auth是用来认证用户的身份信息的,如果auth认证的时候需要用到多个模块,就依次检查各个模块,这个模块通常最终都是是需要密码来检验的,所以这个模块之后的下一个模块是用来检验用户身份的.如果帐号没问题,就授权
- account大部分是用来检查权限的,比如检查账户和密码是否过期等,如果你使用一个过期的账户或密码就不允许验证通过.如果有多个模块,也依次检查各个模块.
- 修改密码需要用到的,如果用户不修改密码,几乎用不到这个模块.
- session限定会话限制的,比如:vsftpd下午6点不允许访问,那6点过后用户再去访问的话就会被限制,或内存  不足不允许访问等,session就是限定这种类型的

## 第二个字段:验证控制标志(control flag)

- required 此验证如果成功则带有success的标志,如果失败则带有failure的标志,此验证如果失败了,就一定会 返回失败的标志,但是不会立即返回,而是等所有模块验证完成后才返回,所以它不论验证成功或失败   都会继续向后验证其他的流程.

- requisite如果验证失败则立即返回failure的标志,并终止后续的验证流程,如果验证带有success标志,则继续  后面的流程.

- sufficient与requisite正好相反,此验证如果成功则带有success的标志,并立即终止后续的流程,如果验证带有  failure的标志,则继续后面的流程.

- optional
- include 包含进来指定的其他配置文件中的同名栈中的规则,并以之进行检测.
- substack
## 第三个字段:PAM的模块与该模块的参数

PAM模块路径：
- /etc/pam.d/*:每个程序个别的PAM的配置文件;
- /lib/security/*:PAM模块档案的实际放置目录;
- /etc/security/*:其他PAM环境的配置文件;
- /usr/share/doc/pam-*/:详细的PAM说明文件;

* [Pma模块详解](https://www.cnblogs.com/anruy/p/7680541.htmlhttps://www.cnblogs.com/anruy/p/7680541.html)


# 参考链接

- [Arch compared to other distributions (简体中文)](https://wiki.archlinux.org/index.php/Arch_compared_to_other_distributions_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
- [Arch Linux 安装手册/傻瓜书/教程/指南pacm    ](https://www.jianshu.com/p/6fe59c24b3df)
- [如何在 VirtualBox 内安装 Arch Linux](https://pk.cli.ee/archlinux-virtualbox)
- [使用dd命令制作U盘启动盘](https://blog.csdn.net/liuqinglong_along/article/details/78458100)
- [在 VirtualBox 里安装 Arch Linux 操作系统](https://www.jianshu.com/p/98b8965b1d10)
- [Arch Linux 安装指南](https://www.jianshu.com/p/7c78dc4c53e5)
- [以官方Wiki的方式安装ArchLinux](https://www.viseator.com/2017/05/17/arch_install/)
