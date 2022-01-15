
# HTTP/2.0 Flow Control


> [HTTP/2.0 Flow Control | 老青菜](https://laoqingcai.com/http2-flowcontrol/)

根据[rfc7540#section-5.2](https://tools.ietf.org/html/rfc7540#section-5.2)的描述，使用流进行多路复用会导致争用TCP连接，导致流阻塞。流量控制方案确保同一连接上的流不会破坏性地互相干扰。流量控制可以作用于单个流或者整个连接，是逐跳的，而且流量控制仅仅作用于Data Frame。

## 控制原理

和[TCP Sliding Window](https://laoqingcai.com/tcp-slidingwindow/index.html)原理差不多，HTTP/2.0的Flow Control针对每个Stream也有一个Window窗口，只不过没有SEQ、ACK。
流量控制窗口Window是一个简单的整数，指示允许发送方能传输多少个八位字节。因此，窗口的大小间接衡量了接收者缓冲区的容量。
