gRPC-Go通过HTTP2+Protobuf为基础，通过统一定义的RPC服务描述，配合多语言的SDK，可以轻松实现跨语言的高性能RPC调用。

核心层：提供在RPC调用过程中的寻址，消息编解码，网络收发、连接管理，故障重试等功能

扩展：通过插件的方式，扩展服务发现、负载均衡、鉴权以及链路跟踪等治理能力

[#131 gRPC-Go 基于 Polaris 北极星的服务治理实践【Go 夜读】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1VY411j7ty?vd_source=6f02b7c9688e8efcfc13a5c6ed7d2b10)
