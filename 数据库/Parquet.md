- [深入分析 Parquet 列式存储格式](https://www.infoq.cn/article/in-depth-analysis-of-parquet-column-storage-format)
- [深入分析 Parquet 列式存储格式(注释)](https://blog.csdn.net/worldchinalee/article/details/82781263)

# 背景
关系型数据的列式存储，可以将每一列的值直接排列下来，不用引入其他的概念，也不会丢失数据。关系型数据的列式存储比较好理解，而嵌套类型数据的列存储则会遇到一些麻烦。

嵌套数据类型的特点是一个 record 中的 column 除了可以是 Int, Long, String 这样的原语（primitive）类型以外，还可以是 List, Map, Set 这样的**复杂类型**。

在行式存储中一行的多列是连续的写在一起的，在列式存储中数据按列分开存储，例如可以只读取 A.B.C 这一列的数据而不去读 A.E 和 A.B.D，那么如何根据读取出来的各个列的数据重构出一行记录呢？

# 作用
Google 的 Dremel 系统解决了这个问题，核心思想是**使用“record shredding and assembly algorithm”来表示复杂的嵌套数据类型，同时辅以按列的高效压缩和编码技术，实现降低存储空间，提高 IO 效率，降低上层应用延迟**。Parquet 就是基于 Dremel 的数据模型和算法实现的。


例如 parquet-mr 项目里的 parquet-pig 项目就是负责把**内存中的** Pig Tuple **序列化并按列存储成** Parquet 格式，以及反过来把 Parquet 文件的数据反序列化成 Pig Tuple。

这里需要注意的是 Avro, Thrift, Protocol Buffers 都有他们**自己的存储格式**，但是 Parquet 并没有使用他们，而是使用了自己在 parquet-format 项目里定义的存储格式。所以如果你的应用使用了 Avro 等对象模型，这些数据序列化到磁盘还是使用的 parquet-mr 定义的转换器把他们转换成 Parquet 自己的存储格式。

# Parquet数据模型
每个 schema 的结构是这样的：根叫做 message，message 包含多个 fields。每个 field 包含三个属性：repetition, type, name。repetition 可以是以下三种：required（出现 1 次），optional（出现 0 次或者 1 次），repeated（出现 0 次或者多次）。type 可以是一个 group 或者一个 primitive 类型。

```bash
message AddressBook {
 required string owner;
 repeated string ownerPhoneNumbers;
 repeated group contacts {
   required string name;
   optional string phoneNumber;
 }

```

Parquet 文件在磁盘上的分布情况如图 5 所示。所有的数据被水平切分成 Row group，一个 Row group 包含这个 Row group 对应的区间内的所有列的 column chunk。一个 column chunk 负责存储某一列的数据，这些数据是这一列的 Repetition levels, Definition levels 和 values（详见后文）。一个 column chunk 是由 Page 组成的，Page 是压缩和编码的单元，对数据模型来说是透明的。一个 Parquet 文件最后是 Footer，存储了文件的元数据信息和统计信息。Row group 是数据读写时候的缓存单元，所以推荐设置较大的 Row group 从而带来较大的并行度，当然也需要较大的内存空间作为代价。一般情况下推荐配置一个 Row group 大小 1G，一个 HDFS 块大小 1G，一个 HDFS 文件只含有一个块。

# Striping/Assembly 算法
对于嵌套数据类型，我们除了存储数据的 value 之外还需要两个变量 **Repetition Level(R), Definition Level(D)** 才能**存储其完整的信息用于序列化和反序列化嵌套数据类型**。Repetition Level 和 Definition Level 可以说是为了支持嵌套类型而设计的，但是它同样适用于简单数据类型。在 Parquet 中我们只需定义和存储 schema 的叶子节点所在列的 Repetition Level 和 Definition Level。

## Definition Level
嵌套数据类型的特点是有些 field 可以是空的，也就是没有定义。如果一个 field 是定义的，那么它的所有的父节点都是被定义的。从根节点开始遍历，当某一个 field 的路径上的节点开始是空的时候我们记录下当前的深度作为这个 field 的 Definition Level。如果一个 field 的 Definition Level 等于这个 field 的最大 Definition Level 就说明这个 field 是有数据的。对于 required 类型的 field 必须是有定义的，所以这个 Definition Level 是不需要的。在关系型数据中，optional 类型的 field 被编码成 0 表示空和 1 表示非空（或者反之）。

## Repetition Level
记录该 field 的值是在哪一个深度上重复的。只有 repeated 类型的 field 需要 Repetition Level，optional 和 required 类型的不需要。Repetition Level = 0 表示开始一个新的 record。在关系型数据中，repetion level 总是 0。

## 具体事例
见参考链接
> R=0 表示一个新的 record，根据 schema 创建一个新的 nested record 直到 Definition Level=0，也就是创建一个 AddressBook 根节点。

# 总结
可以看出在 Parquet 列式存储中，**对于一个 schema 的所有叶子节点会被当成 column 存储，而且叶子节点一定是 primitive 类型的数据**。对于这样一个 primitive 类型的数据会衍生出三个 sub columns (R, D, Value)，也就是从逻辑上看除了数据本身以外会存储大量的 Definition Level 和 Repetition Level。

### 那么这些 Definition Level 和 Repetition Level 是否会带来额外的存储开销呢？

实际上这部分额外的存储开销是可以忽略的。因为对于一个 schema 来说 level 都是有上限的，而且非 repeated 类型的 field 不需要 Repetition Level，required 类型的 field 不需要 Definition Level，也可以缩短这个上限。例如对于 Twitter 的 7 层嵌套的 schema 来说，只需要 3 个 bits 就可以表示这两个 Level 了。

对于存储关系型的 record，record 中的元素都是非空的（NOT NULL in SQL）。Repetion Level 和 Definition Level 都是 0，所以这两个 sub column 就完全不需要存储了。所以在存储非嵌套类型的时候，Parquet 格式也是一样高效的。

上面演示了一个 column 的写入和重构，那么在不同 column 之间是怎么跳转的呢，这里用到了有限状态机的知识，详细介绍可以参考 [Dremel](http://blog.sae.sina.com.cn/archives/794) 。

## 数据压缩算法
列式存储给数据压缩也提供了更大的发挥空间，除了我们常见的 snappy, gzip 等压缩方法以外，由于列式存储同一列的数据类型是一致的，所以可以使用更多的压缩算法。

# 压缩算法

使用场景
- Run Length Encoding 重复数据
- Delta Encoding 有序数据集，例如 timestamp，自动生成的 ID，以及监控的各种 metrics
- Dictionary Encoding 小规模的数据集合，例如 IP 地址
- Prefix Encoding Delta Encoding for strings
