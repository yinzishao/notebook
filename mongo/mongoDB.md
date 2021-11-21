注意：书本是v2.4.0 最新为3.2.9
扩展：纵向扩展（使用计算机能力更强）与横向扩展（通过分区将数据分散到更多机器上）

为什么性能卓越：
- 对文档动态填充
- 也可以预分配数据文件，以换取稳定的性能
- 尽可能多的内存用作缓存
- 每次查询自动选择正确的索引

2.3 特殊语义的数据库
- admin "root"数据库，用户在admin 数据库，自动获得所有数据库的权限，一些命令只能amdin执行
- local 永远不会复制，本地集合存储在这
- config 分片设置


2.4
端口号：27017
28017	http://localhost:28017
2.5.3	基本操作

insert，find findOne，update，remove

2.6 数据类型

mongodb 比 json 有更多的数据类型
json支持的6种类型：null、布尔、数字、字符串、数组、对象

mongodb支持的类型：代码！

2.6.4 内嵌文档

好处：使信息的表示方式更加自然
坏处：更多数据的重复；需要对每个人分别修改错误。

2.7 连接数据库
mongo some-host:30000/myDB	#启动mongodb shell指定数据库
mongo --nodb			#启动mongodb shell无指定
conn = new Mongo("some-host:30000")
db = conn.getDB("myDB")
2.7.2 shell执行脚本
$mongo script1.js script2.js script3.js
$mongo --quiet server-1:30000/foo script1.js	#print()输出stdout，使用管道命令。--quiet不打印版本信息

##辅助函数

2.7.3
.mongorc.js,这个文件会在启动shell时自动运行。相当于.bashrc?
可以移除那些比较危险的shell辅助函数，改变数据库函数时，确保db变量和DB原型进行改变。
定制shell提示

2.7.5	编辑
EDITOR="/usr/bin/emacs"

2.7.6	集合命名
3.1.1 批量插入
batchInsert([])	接受一个数组
能接受插入48m的数据。会请求拆分。
插入过程中中间失败，之前可以，后面失败

文档必须小于16m

3.2
删除文档，db.foo.remove() 不行报错，应该是db.foo.remove({})

3.3
更新文档，使用"_id"作为查询条件比使用随机字段的速度更快
注意：文档替换的时候可以改变"_id"

3.3.2
$inc 不存在则创建,专门来增减数字的。
$set 不存在则创建
$push 向数组末尾加入一个元素 $each 子操作符 添加多个值  $slice 限定元素长度 $sort排序
集合保持数组内的元素不会重复 $ne，$addToSet（可以用$each插入多个）
$pop	按数组位置删除，{"$pop":{"key":-1}} 从头部删除
$pull	按特定条件删除，删除数组匹配的所有
一定要使用$开头的修改器来修改键/值对，不然会将整个文档用{}替换掉

修改器速度，填充因子(padding factor),为每个新文档预留的增长空间。
因为依次插入的文档在磁盘上的位置是相邻的，
运行db.coll.stats()查看因子，"paddingFactor"值为1.精准分配空间
所以修改导致文档增长，就会被移动到集合中的另外一个位置，并增加填充因子。

=========================================================================================================================
1.新的记录分配策略
MongoDB 3.0使用power of 2 allocation代替原来的动态记录分配，且弃用了paddingFactor。原来的分配策略在文档变大超过初始分配的大小的时候，MongoDB要分配一个新的记录，并要移动数据和更新索引，导致存储碎片。 power of 2 allocation的策略是分配的记录的大小都是2的次方（32, 64, 128, 256, 512 … 2MB），每个记录包括文档本身和额外的空间——padding，这个机制减少了文档增长的时候记录重新分配和数据移动的操作。显然新的策略在处理大文档和文档增长频繁的场景下效率更高，但如果只有插入操纵和所谓的in-place更新操作（不会增长文档大小）那么使用这种策略会很浪费空间，因此MongoDB 3.0允许你关闭这种策略。


----


进行插入和删除的时候进行大量的移动或者使经常打乱数据，可以使用userPowerOf2Sizes选项提高磁盘复用率。 p44

3.3.3 upsert	不存在则创建，原子性的！！！
db.hanalytics.update({"url":"/blog"},{"$inc":{"pageviews":1}},true)
update的第三个参数代表这是个upsert

$setOneInsert	创建文档的同时创建字段并为它赋值

save() 如果不存在创建，存在更新。


3.3.4 更新多个文档（update 第四个参数为true）
默认情况下，更新只能对符合匹配条件的第一个文档执行操作。
运行getLastError返回最后一次操作的相关信息，n为更新文档的数量
db.runCommand({getLastError:1})

3.3.5 返回更新的文档
竞态条件(线程)
findAndModify 能够在一个操作中返回匹配结果并且进行更新。
"update"和"remove"必须有一个。	其他参数：50

3.4 写入安全机制
应答式写入和非应答式写入
非应答式写入：对于一些不是很重要的数据
非应答式写入不返回数据库错误，但也需要做错误检查。
shell与客户端程序对非应答式写入的实际支持并不一样。shell若最后一个有效，并不会提示有错误

4.1.2
查询上有限制，不能引用文档中其他键的值

4.2查询条件
$lt $lte $gt $gte   < <= > >=
$ne !=
$in $nin
$or
$not 元条件句 $mod 取模运算符
#条件语句是内层文档的键，而修改器则是外层文档的键。
有一些"元操作符"也位于外层文档中，比如"$and"、"$or"和"$nor"

$and    {"x":[0,4]} 匹配 db.user.find({"$and":[{"x":{"$lt":1}},{"x":4}]})
        也就是小于1并且等于4
        效率更高：db.user.find({"x":{"$lt":1,"$in":[4]}})

4.3
4.3.1
null    不仅会匹配某个键的值为null，而且还会匹配不存在该值的文档
$exists db.c.find({"z":{"$in":[null],"$exists":true}})
4.3.2
正则      /joey?/i  正则表达式标志(i) 使用perl兼容的正则表达式(PCRE)

4.3.3
$all    多个元素来匹配数组
精确匹配，对于缺少元素或者元素冗余的情况就不太灵。顺序也是
$size   查询特定长度的数组
不能用$gt等一起使用，解决办法：每次向指定数组添加元素的时候，同时增加"size"的值。
但不能与"$addToSet"操作符同时使用

$slice 返回某个键匹配的数组元素的一个子集，返回文档中的所有键

4.返回一个匹配的数组元素   可以使用$操作符得到一个匹配的元素

5.
文档的标量(非数组元素)
##注意！数组的查询范围。范围会匹配任意多元素数组！！！！！

$elemMath   同时使用查询条件中的两个语句与一个数组元素进行比较。但不会匹配非数组元素！
解决办法：↓db.test.find({"x":{"$gt":10,"$lt":20}}).min({"x":10}).max({"x":20})
********************min max************************
min() max()效率高，只会遍历值位于10和20之间的索引
$gt/$lt，效率低，查询条件会与所有值进行比较
会查询每一个索引，而不仅仅是指定索引范围内的值
************************************************
4.3.4
查询内嵌文档
不应该用精确匹配，可以使用点表示法查询内嵌文档的键
注意：要正确地指定一组条件，而不必指定每个键，就必须使用"elemMath".
        也就是说，如果数组里面的多个符合查询范围，则查询符合。
        而不是把查询范围限定到单个内嵌文档。这跟上面数组的查询范围注意事项是一样的。

*********************$where***********************
例如:比较文档中的两个键的值是否相等，没有提供一个$条件语句来做这种查询。所以$where就要使用在此了。
4.4     $where   可以查询中执行任意的javscript
要严格限制或者消除$where语句的使用。应该禁止终端用户使用任意的$where语句
！慢很多：文档从BSON转换成javascript对象，然后通过$where表达式来运行。而且$where不能使用索引

如果可能的话，先使用常规查询、索引！进行过滤，然后再使用$where语句
************************************************

##服务器脚本
执行javascript注意安全性。注入攻击
使用作用域来传递值。
shell中没有包含作用域的代码类型。作用域只能在字符串或者javascript函数中使用

4.5 游标

执行查询，分配给一个局部变量cursor
cursor.hasNext()
cursor.next()
也可以通过foreach循环使用

4.5.1
limit   上限
sort    键值对：1升序、0降序
skip    略过
注意比较顺序。一个键的值可能使多种类型的。排序顺序使预先定义好的。具体的顺序参考p70

#4.5.2避免使用skip略过大量的结果
通常可以利用上次的结果来计算下一次查询条件
随机选取文档：可以增加一个字段，存储一个随机数。

4.5.3 高级查询选项
简单查询和封装查询？

4.5.4获取一致结果
文档保存回数据库的时候，文档变大了，预留空间不足，就会进行移动。通常将它们移动末尾，就会导致结果不一致。
解决办法是对查询进行快照snapshot。查询就在"_id"索引上遍历执行，这就保证每个文档只被返回一次。但速度变慢

作为替换方案，如果您的集合中有一个或者多个字段不会被更改，您可以在这个或者多个字段上使用*唯一性*索引来达到与:method:~cursor.snapshot()`相同的效果。查询的时候使用:method:`~cursor.hint() 声明强制走这个索引。

4.5.5游标生命周期
服务器端释放游标的情况：
游标遍历尽结果、客户端发来消息请求终止、客户端的游标已经不在作用域内了、超时(10分钟)
immortal函数或者机制告知数据库不要让游标超时。

4.6 数据库命令  (特殊的查询类型)
辅助函数封装数据库命令
工作原理：这些特殊的查询会在$cmd集合上执行。runCommand只是接受一个命令文档，并且执行与这个命令文档等价
的查询。mongodb服务器得到这个正在$cmd集合上的查询时，而是会使用特殊的逻辑对其进行处理。
        db.runCommand({"drop":"test"});
        等价于：
        db.$cmd.findOne({"drop":"test"});
管理员权限：db.adminCommand({"shutdown":1})
注意：数据库命令使少数与字段顺序相关的地方之一
第二部分 设计应用
第五章 索引！
======================================================================================
####explain() http://ultrasql.blog.51cto.com/9591438/1655359

可以使用explain()函数查看mongodb在执行查询的过程中所做的事情
注意：新的3.0版本已经有很大的改动了，db.collection.explain()
cursor.explain(verbose) 保持对旧版的兼容，"queryPlanner", "executionStats", and "allPlansExecution"
true as "allPlansExecution"详细
false as "queryPlanner"

- queryPlanner模式：MongoDB运行查询优化器选择评估操作的最优计划。
- executionStats模式：MongoDB运行查询优化器选择最优计划，执行最优计划来完成操作，并返回描述最优计划执行的统计信息。对于写操作，db.collection.explain()返回关于将会被执行的更新或删除操作的信息，但不应用修改到数据库。
- allPlansExecution模式：MongoDB运行查询优化器选择最优计划，执行最优计划来完成操作。在“allPlansExecution”模式，MongoDB返回描述最优计划的执行统计信息，也返回在计划选择期间其他备选计划的统计信息。

##Stage状态分析
对于普通查询，我们最希望看到的组合有这些：

Fetch+IDHACK

Fetch+ixscan

Limit+（Fetch+ixscan）

PROJECTION+ixscan

SHARDING_FILTER+ixscan
原理：查询优化器				p103
======================================================================================
创建索引:db.users.ensureIndex({"username":1})
另一个shell执行db.currentOp()或者检查mongodb的日志来查看索引创建的进度。

使用索引的代价：对于添加每一个索引，每一次写操作(插入，更新，删除)将耗费更多的时间。
mongodb限制每个集合最多只能有64个索引。
通常，在一个特定?的集合上，不应该拥有两个以上的索引。
管理员并不需要太在意查询耗费的时间

5.1.1 复合索引
复合索引就是一个建立在多个字段上的索引。
跟建立索引的顺序有关系。先按第一个索引的值升序建立，值相同的按照第二个索引进行升序排序。

*********************************索引值顺序******************************************************
##所以在实际的应用程序中，{"sortKey":1,"queryCriteria":1}。
原因：大多数应用程序在一次查询中只需要得到查询结果最前面的少数结果。
如果先排序键建立索引。那么就可以按顺序，找到符合该精确查询条件的限制数额就可以停止。
如果是先精确查询的话，会找到所有符合精确查询条件的文档，然后在内存中进行排序。所以效率大打折扣。

scanAndOrder为True:说明mongodb必须在内存中对数据进行排序。旧版
新版是查看stage的值：如果是sort代表是在内存中进行排序。

注意：nReturned=totalDocsExamined的基础上，让排序也使用index
###{精确匹配字段,排序字段,范围查询字段}这样的索引排序会更为高效。
************************************************************************************************

通过hint来强制使用某个特定的索引

点查询(point query)用于查找单个值，也就是说查找条件是单个值，而不是返回单个值。
多值查询(multi-value query)查找多个值相匹配的文档(介于**到**之间)

右平衡:只需在内存中保留这棵树最右侧的分支(最近的数据)，而不必将整棵树留在内存中。

mongoDB拒绝对超过32MB的数据进行排序。

5.1.2使用复合索引

您可以指定在索引的所有键或者部分键上排序。但是，排序键的顺序必须和它们在索引中的排列顺序 一致 。例如，索引 { a: 1, b: 1 } 可以支持排序 { a: 1, b: 1 } 但不支持 { b: 1, a: 1 } 排序。

此外，sort中指定的所有键的排序顺序(例如递增/递减）必须和索引中的对应键的排序顺序 完全相同, 或者 完全相反 。

>>选择键的方向：只有基于多个查询条件进行排序的时候，索引方向才是比较重要的。

>>覆盖索引：一个索引包含用户请求的所有字段
indexOnly为True
注意：如果一个含有数组的字段上做索引，这个索引永远也无法覆盖查询。即便剔除数组字段。
>>隐式索引:如果有一个拥有N个键的索引，那么你同时"免费"得到了所有这N个键的前缀组成的索引。
注意：一定是前缀！！！

5.1.3
>>低效率操作符：有一个"x"索引，如果要查询({"x":{"$exists":false}}),因为"x"字段不存在和等于null的存储方式是一样的，所以就需要遍历所有的文档去判断是不是真的不存在。
$exists、
通常来说取反效率比较低：$ne、$not、$nin(总全表扫描)
可以尝试找到另外一个能够使用索引的语句，将其添加到查询中，
这样可以在进行无索引匹配(non-indexed matching)将结果集的文档数量减到一个比较小的水平。

>>范围：先使用第一个索引建进行精确匹配，然后再使用第二个索引范围在内部进行搜索。
>>or查询：在一次查询中只会使用其中的一个索引！！但$or实际上是执行了两次查询然后结果集合并。
eg: ({"$or":[{"x":123},{"y":456}]})

5.1.4 索引对象和数组
>>索引嵌套文档：对嵌套文档本身建立索引，跟嵌套文档的某个字段建立索引是不同的。只有与进行与子文档字段！！顺序！！完全匹配！的子文档查询时，查询优化器才会使用嵌套文档的索引。
>>索引数组：实际是对数组中的每个元素建立索引，而不是对数组本身建立索引。
不包含任何位置信息。
！！一个索引中的数组字段最多只能有一个！！
原因：避免在多键索引中索引条目爆炸性增长。n*m个索引条目。
>>多键索引：索引键在某个文档中是一个数组
isMultikey:true

5.1.5 索引基数：基数排序

indexBound:{}
给出了索引的遍历范围

查询优化器：会从这些可能的索引子集为每个查询计划选择一个，这些查询计划并行执行，最早返回100个结果就是胜者终止其他的查询计划。
集合发生了比较大的数据变动，查询优化器就会重新挑选可行的查询计划，或者每执行1000次查询之后重新评估。

5.3
返回结果越大，索引速度越慢，因为需要两次查找：索引条目、根据索引指针去查找相应的文档。
返回集合内30%的文档(更多，可能在2%~60%之间变动)，需要进行索引和全表扫描的比较
索引适用情况：集合较大、文档较大、选择性查询
全表扫描适用情况：集合较小、文档较小、非选择性查询

可以用{"$natural":1}强制进行全表扫描.
************************************自然排序****************************************************
返回结果集中文档的顺序就是文档在磁盘上的顺序。
这对于一个活跃的集合是没有作用的。因为随着文档体积的增加或者缩小，文档会在磁盘中移动，然后新的文档会被写入到这些文档留下的空白位置。
但是！对于只需要进行插入的工作来说（文档不会被修改，所以体积也就不会增加或者缩小，也就不会移动）,如果要得到最新或者最早文档，使用$natural就非常有用了。
也可以跟固定集合一起使用。
************************************************************************************************
5.4
>>唯一索引 (_id)
>>复合唯一索引
创建索引的时候可以使用dropDups强制性建立唯一索引。保留第一个。
5.4.2
稀疏索引(sparse index):只是不需要将每个文档都作为索引条目。跟关系型数据库中的稀疏索引是完全不同的概念。
唯一索引会把null看做值。如果使用稀疏索引则可以是存在字段的时候值一定要不同
不能使用{"$exists":true/false},可以用hint作全表扫描

5.5管理索引：
所有数据库的索引信息都存储在system.indexes集合中。但只是保留集合，不能直接插入删除、只能通过ensureIndex或者dropIndexes进行操作
db.collectionName.getIndexes()
"v"字段只在内部使用。
5.5.1
索引命令形式:keyname1_dir1_keyname2_dir2
有长度限制，可以通过name进行命名

第6章 特殊的索引和集合
6.1固定集合：当固定集合被占满时，如果再插入新文档，固定集合会自动将最老的文档从集合中删除。
写入速度很快
可以将常规集合转换为固定集合，但不能逆转
************************************自然排序****************************************************
返回结果集中文档的顺序就是文档在磁盘上的顺序。
这对于一个活跃的集合是没有作用的。因为随着文档体积的增加或者缩小，文档会在磁盘中移动，然后新的文档会被写入到这些文档留下的空白位置。
但是！对于只需要进行插入的工作来说（文档不会被修改，所以体积也就不会增加或者缩小，也就不会移动）,如果要得到最新或者最早文档，使用$natural就非常有用了。
也可以跟固定集合一起使用。
************************************************************************************************
6.1.3
循环游标 mongodb shell 不支持
用于当文档被插入到"工作队列"（固定集合）对新插入！的文档进行处理，超过10分钟没有新的结果，循环游标就会释放！关闭时自动重新执行查询是非常重要！

6.1.4
autoIndexId选项
对于只有插入操作的集合来说，没有_id索引，的确可以带来速度的稍许提升。
注意：_id索引必须是唯一索引。若创建_id索引不符合规范，只能删除集合再重建了。先自己实践

6.2 TTL索引 time-to-live index具有生命周期的索引
expireAfterSecs选项
允许为每个文档设置一个时间。到达预设的老化程度后就会删除
TTL索引不能是复合索引，但是可以像普通索引一样用来优化排序和查询
6.3
全文本搜索
只会对字符串数据进行索引，其他的数据类型会被忽略。最多只能有一个全文本索引，但全文本索引可以包含多个字段，且字段顺序不重要。也可以分配权重。
"$**"所有字符串、whatever可以指代任何东西。

6.3.1
搜索语法 or - 双引号括起来进行精确查找(转义)
6.3.2
如何优化全文本索引：
一、可以创建一个由其他条件前缀和全文本字段组成的复合索引。（局部的全文本索引）对于符合特定前缀条件的文档进行全文本查询就会快很多。
二、可以使用其他的查询条件后缀，使索引能够覆盖查询。
注意：前缀和后缀不能是多键字段！！！
usePowerOf2Sizes选项控制空间的分配方式，提高写入速度，所以不要禁用它

default_language 指定语言

！6.4地理空间索引（第一次接触，陌生！）
2dsphere 允许使用GeoJSON格式，指定点、线和多边形
6.4.1地理空间查询类型
查询：交集、包含、接近
$getIntersects、$within、$near
{"$geometry":geoJsonDesc}
find("loc",{"$getIntersects":{"$geometry":eastVillage}})

复合地理空间索引：将那个能够过滤尽可能多的结果的字段放在前面

6.4.3 2d索引
"2d"索引只能对点进行索引。不会被当成线
不必带有$geometry子对象

6.5使用GridFS存储文件
用来存储大型二进制文件
理由：
1.简化栈。代替独立的文件存储工具
2.自动平衡已有的复制或者为mongodb设置的自动分片，故障转移和横向扩展
3.从容解决问题：同一目录下存储大量的文件
4.文件存储的集中度比较高。2g单位

缺点：
1.性能比较低
2.修改，只能删除然后重新保存

结论：如果有一些不常改变但是经常需要连续访问的大文件，使用GridFS最合适

使用mongofiles：put,list,get,search,delete

GirdFS理念：将大文件分割为各个比较大的块，将每个块作为独立的文档进行存储。
块默认的集合是fs.chunks(字段：files_id,n,data)
元信息的集合是fs.files(_id(对应块的file_id),length,chunkSize,uploadDate,md5)

理解GirdFS底层规范，实现一些没有提供的辅助功能：
db.fs.files.distinct("filename") 收集文件信息

第七章 聚合

7.1 聚合框架

可以对集合中的文档进行变换和组合。
通过多个构件创建一个管道(pipeline),对一连串的文档进行处理
筛选、投射、分组、排序、限制、跳过
投射只会在内存中存在，不会写进磁盘中
集合框架还不能对集合进行写入操作，因此所有结果必须返回给客户端，所以限制在16m之内（最大响应消息大小）

$match 不能使用地图空间操作符
尽可能放在最前：
1.快速过滤文档，减少管道的工作量。
2.如果投射和分组之前执行"$match"，查询可以使用索引！！

注意：

2.6 and 3.0 不能在集合管道覆盖索引，尽管通道使用了索引，依然需要访问实际存储的文档。
3.2 即使使用了索引，聚合依然需要访问实际存储的文档；比如索引不能满足聚合管道所需要的所有字段的时候。也就是说可以使用索引，覆盖所有字段。

$project
注意：对字段重命名之后，无法继续使用旧的索引。所以尽量在修改之前使用索引！！

管道表达式：p133-p136
数学表达式：$add,$subtract,$multiply,$divide,$mod
日期表达式：$month,$week 等
字符串表达式：$substr,$concat,$toLower,$toUpper
逻辑表达式：$cmd、$strcasecmp、 $eq/neq/gt
控制语句：$cond[0,1,2] 1 if 0 else 2
	$ifNull[expr,replaccementExpr]  expr if expr !=null else replacementExpr

！！注意接受的类型！！

！！两个操作符不支持流式$group和$sort，把分片结果发送到mongos进一步处理
7.2.3 $group

算术操作符:$sum、$avg
极值操作符:$max,$min,$first,$last
$max和$min会查看每一个文档。如果是无序的，这两个操作符就可以有效工作。
有序的话就没有直接使用$first,$last效率高
数组操作符：$addToSet $push
分组行为：$group 必须要等到所有文档之后才能进行分组。
	分片情况下：会在每个分片执行，然后各个分片的分组结果发送到mongos再进行最后的统一分组。
		   剩余的管道工作都会在mongos（而不是分片）上运行。

$unwind 拆分
将数组的每一个值拆分为单独的文档。

$sort 排序	无法使用流式工作方式的操作符
在管道的第一阶段进行排序，可以使用索引。否则会占用大量的内存

$limit、$skip

------------------------------------------------------------
##聚合管道的优化http://docs.mongoing.com/manual-zh/core/aggregation-pipeline-optimization.html
------------------------------------------------------------
$skip + $limit 顺序优化¶

如果你的管道中， $skip 后面跟着 $limit ，优化器会把 $limit 移到 $skip 前面，这个时候， $limit 的值会加上 $skip 的个数。$limit 的限定个数会增长。

原因：在经过$limit管道后，管道内的文档数量个数会“提前”减小，这样会节省内存，提高内存利用效率

$sort + $match 顺序优化

如果你的管道中， $sort 后面跟着 $match ，把 $match 移到 $sort 前面可以减少需要排序的对象个数。

$project + $skip or $limit Sequence Optimization¶

如果你的管道中，$project后面跟着$skip or $limit，把 $skip or $limit 移到 $project 前面

$limit + $limit 合并

当 $limit 操作后面还有一个 $limit 操作，这两步可以合并成一个单独的 $limit 操作，此时限制的个数是前面两个限制个数中较小的值。

$skip + $skip 合并

当 $skip 操作后面还有一个 $skip 操作，这两步可以合并成一个单独的 $skip 操作，此时跳过的个数是前面两个跳过个数的和。


$match + $match 合并

当 $match 操作后面还有一个 $match 操作，可以将这两步中的条件使用 $and 表达式合并成一个单独的 $match 操作。

$limit + $skip + $limit + $skip 顺序

会先通过$skip + $limit 顺序优化,然后将两个$skip合并$limit合并.
------------------------------------------------------------
7.2.8 使用管道
尽量在开始阶段(执行$project,$group,$unwind)尽可能多的文档和字段过滤掉。$match
尝试对操作进行排序，以便有效使用索引
不能占用过高的内存20%，输出错误
支持输出结果放入一个集合中方便以后使用。（将所需内存减到最小）
$match迅速减少结果集的大小，可以使用管道进行实时聚合。
由于管道不断包含更多文档，越来越复杂，几乎不可能实时得到管道的操作结果。

7.3 MapReduce
mapreduce
使用JavaScript作为"查询语言"，因此它能够表达任意复杂的逻辑。
但每个传递给map函数的文档都要先反序列化，从Bson对象转换为JavaScript对象，这过程好耗时。
所以可能先对文档进行过滤。"query","limit","sort"

MapReduce 的过程：
映射(map) 将操作映射到集合的每个文档
洗牌(shuffle)按照键分组，将产生的键值组成！！列表！！放到对应的键中
化简(reduce) 把列表中的值化简成一个单值。接着洗牌，直到每个键的列表只有一个值为止。

例子可以参考官网的例子，书上写得例子第一次很难理解：https://docs.mongodb.com/manual/core/map-reduce/

MapReduce 可选的键：
finalize 将结果发送给这个键
keeptemp 保存临时结果
out 输出集合的名称，自动保存
query 执行条件过滤
sort 排序
limit 上限
scope 可以在javascript使用的变量
verbase 记录详细的服务器日志

mapReduce 还可以对增量的文档执行
设置：
通过query过滤新的文档。
out: { reduce: "session_stat" }
reduce指定参数，之前保存的结果集。

sort 和limit一起使用的时候通常可以发挥非常大的作用
如果不使用limit的话，sort就不能有效发挥作用了

7.4 聚合命令

count 不管集合有多大，都会很快返回总的文档数量
但是增加查询条件会使count变慢，索引并没有足够的元数据供count使用，所以不如直接使用查询来得快

distinct 用来 找出给定键的所有不同值。指定集合和键
db.runCommand({"distinct":"people","key":"age"})


group
注意：由于精度问题，实际使用不要以浮点数的方式存储。

ns:	指定要进行分组的集合
key:	分组依据的键
initial	会作为初始文档传递给后续的过程。（prev.** 获取）
reduce 会在集合内的每个文档上执行。当前文档和累加器文档。每一组都有独立的累加器
condition 进行过滤	"day":{"$exists":true}	排除不包含指定用于分组的键的文档
完成器：每组结果传递到客户端之前调用一次
$keyf	依据各种复杂的条件进行分组


---
第8章 应用程序设计
8.1
范式化：将数据分散到多个不同的集合，不同集合之间可以互相引用数据。但是mongodb没有提供连接(join)工具
反范式化：将每个文档所需的数据都嵌入在文档内部。
	  缺点：信息变化，所有相关文档都需要进行更新，占用更多的空间。但查询一次就能得到数据。
可以混合使用内嵌数据和引用数据。子文档数组保存常用信息，更详细信息时，则通过引用找到实际的文档。

内嵌文档，更新文档的时候，需要设置一个定时任务(cron job)，以确保更新所有文档。

内嵌与引用数据的比较：
>>内嵌：字段是文档数据的一部分。子文档较小。不会定期改变。最终数据一致即可。文档数据小幅增加。数据通常执行两次查询才能获得。快速读取
>>引用：字段在查询文档的时候经常需要排除。


8.1.3
following followers 字段不需要返回，频繁改变导致大量的碎片。
范式化 followers，使用户文档比较精简，需要额外的查询才能得到粉丝列表，必须查询整个followers的集合。
数组大小经常发生变化，可以启用usePowerOf2Size,以确保users集合尽可能小。不过多影响users集合的前提下对其进行压缩。

特殊情况：可能粉丝列表的文档溢出！可以用一个"tbc(to be continued)"数组取数据!!!!

8.2 优化数据库操作！！！
读取操作：正确使用索引，尽可能将所需信息放在单个文档中返回。
写入操作：减少索引数量以及尽可能提高更新效率。
考虑频繁程度：为了执行1次写入，要1000次读取

8.2.1
- 更新文档，如果知道文档的体积会增大，可以通过填充因子，提高写入操作。
- 可以在文档最后添加一个大字段（或者upsert使用"$setOnInsert"），然后更新文档时，总是用"$unset"移除"garbage"字段！！赞！
- 把字段需要增长，尽可能放在文档最后。

8.2.2 删除旧数据
1. 固定集合
2. TTL集合
3. 多个集合。例如：每月一个集合

8.3 数据库和集合的设计

- mongodb 通常不允许使用多个集合进行数据组合。所以进行集中查询或者集合的时候，尽管结构非常不同，但也应该把它们位于同一个集合内。
- 最大的问题是锁机制（每个数据库都有一个读/写锁）和存储
- mongodb 通常不允许直接将数据从一个数据库移动另一个数据库。例如：无法MapReduce和renameCollection
- 尽可能保证那些需要在一个原子操作内进行修改的字段定义在同一个文档里面。
8.4 一致性管理
- MongoDB内部机制：每个数据库维护一个请求列表。一个连接拥有一个一致的数据库视图，可以读取读到最新写入数据。
注意：一些语言的驱动程序使用连接池，通过不同的连接发送到服务器。但有各自的机制保证请求给同一个连接处理。
- 副本落后，不一致。解决办法：所有读取请求发送到主数据库；

8.5 模式迁移：
原因：每个版本的模式之间有冲突。
解决办法：
>>包含一个"version"字段。但也必须对多个文档都有效
>>模式变化，将数据进行迁移。但要确保所有文档都被更新

8.6
- MongoDB不支持事务。（执行操作前先检查锁）
- 不支持连接(join)
- 有些工具不支持MongoDB

#第三部分 复制

复制：将数据副本保存到多台服务器上。一台主服务器（primary），多个备份服务器（secondary）
	主服务器崩溃了，备份服务器会自动将其中一个成员升级为新的主服务器
- 建立副本集
  replicaSet = new ReplSetTest({"nodes":3})
  replicaSet.startSet()
  replicaSet.initiate()
  primaryDB.isMaster()
-自动故障转移(automatic failover)
  primaryDB.adminCommand({"shutdown":1})	关掉
  replicaSet.stopSet()
注意：
- 客户端在单台服务器上可以执行的请求，都可以发送到主节点执行。
- 客户端不能在备份节点上执行写操作。只能通过复制功能写入数据。
- 客户端不能从备份节点上读取数据。除非显式地执行setSlaveOk

9.3 配置副本集
mongod --reolSet spock -f mongod.conf --fork
可以将配置文件发送给副本集的任何一个成员，但必须发送给已经有一个有数据的成员，不止一个则无法初始化副本集。
成员配置完成后，它们会自动选出一个主节点。

9.4
rs.add()
rs.config()
rs.config.members[1].host = "***" #修改
rs.reconfig()

9.5 设计副本集
"大多数"(majority)：选择主节点时需要由大多数决定。副本集一半以上的成员。基于副本集的配置来计算
为了避免出现多个主节点。
配置方式：
- 大多数成员放在同一个数据中心
- 两个数据中心各自防止数量相等的成员。在第三方位置放置仲裁者

多个主节点：需要处理多线程写入冲突。手工解决冲突或系统任选一个。但都不容易实现
一个主节点：易于开发，当副本集被设为只读时，将导致程序无法写入数据。

###选举机制
备份节点1无法与主节点连通，毛遂自荐。但其他副本集成员会做：
- 与主节点是否连通
- 备份节点1是否最新
- 有没有其他更高优先级的成员

复制操作，候选人的最后一条操作必须比其他所有成员要更晚。
否决票相当于10 000张赞成票

9.6 成员配置选项
- 不希望对客户端可见
- 拥有优先成为主节点的权力

9.6.1 选举仲裁者 arbiter
唯一作用就是参与选举。并不保存数据，也不会为客户端提供服务
- 最多只能使用一个仲裁者
- 若是奇数就不需要额外的仲裁者了。原因：导致选举耗时变长。不是导致出现平票的。
- 不知道应该将一个成员作为数据节点还是仲裁者，优先数据节点。避免：仅剩一个节点，进行应用程序请求，而且还要复制到另一个新的服务器上。
- 尽可能使用奇数个数据成员，而不要使用仲裁者

9.6.2
优先级可以在0-100 默认为1，0（被动成员）代表永远不能成为主节点。
- 修改副本集配置时，新的配置必须要发送给新配置下可能成为主节点的成员。
- 无法在一次reconfig 中将当前主节点的优先级设置为0，也不能对所有成员优先级都为0的副本集执行reconfig。

9.6.3 隐藏成员
客户端不会向隐藏成员发送请求，也不会作为复制源。（尽管其他不可用使也会被使用）
隐藏成员只对isMaster()不可见，客户端连接到副本集，会调用isMaster()来查看可用成员。

9.6.4 延迟备份节点
slaveDelay
要求成员的优先级为0，而且应该将延迟备份节点隐藏掉，如果请求被路由到备份节点。

9.6.5
buildIndexs:false 阻止备份节点创建索引。要求优先级为0。并且是永久选项。

第十章 副本集的组成
10.1 同步
oplog：包含了主节点的每一次操作。local数据库中的一个固定集合(大小固定)
备份节点从同步源获取需要执行的操作，然后执行，最后写入自己的oplog。
将oplog中的同一个操作执行多次，与只执行一次的效果是一样的。
通常oplog使用空间的增长速度跟系统处理写请求的速率近乎相同。
例外情况：单词请求能够影响到多个文档（删除多个文档或者更新多文档）

10.1.1 初始化同步！！！p190
初始化同步：它会尝试从副本的另一个成员那里进行完整的数据复制。
步骤：
...



克隆会损坏同步源的工作集。初始化同步会把常驻内存的数据子集，强制将当前成员的所有数据分页加载到内存中。
克隆或者创建索引耗费太长的时间。可能会导致新成员与同步源的oplog“脱节”：新成员远远落后于同步源。

10.1.2 陈旧数据
原因：备份节点曾经停机过，写入量超过了自身处理能力，或者有太多的读请求。
如果任何一个oplog都没有参考价值，那么这个成员上的复制操作就会终止，重新进行完全同步。
如何避免：让主节点使用比较大的oplog保存足够多的操作日志。(磁盘越来越便宜)

10.2 心跳
每隔2秒向其他成员发送一个心跳请求(heartbeat request)
功能之一：让主节点知道自己是否满足集合"大多数"的条件。
常见状态：STARTUP STARTUP2 RECOVERING ARBITER DOWN UNKOWN REMOVED ROLLBACK FATAL


10.3 选举
备份节点1无法与主节点连通，毛遂自荐。但其他副本集成员会做：
- 与主节点是否连通
- 备份节点1是否最新
- 有没有其他更高优先级的成员

心跳会在最多20秒之后超时。
如果打成平局，要等30秒才能开始下一次选举。

10.4 回滚
新的主节点比旧的主节点落后，旧的主节点就要回滚。将未被新的主节点复制的操作撤销。
服务器会查看这些没有被复制的操作，将受这些操作影响的文档写入一个.bson文件，并保存在数据目录下的rollback目录中。然后从当前主节点中复制这个文档

p198！

回滚失败：数据量大于300MB，回滚30分钟以上的操作。
回滚失败，必须重新同步
如何避免：保持备份节点的数据尽可能最新。

第11章 应用程序连接副本集
11.1
驱动程序使用与MongoClient等价的对象，提供希望连接到的副本集种子(seed)列表。
种子，副本集成员。驱动程序通过某个种子服务器，得到其他成员的地址。

主节点挂了，还没选出新的主节点，不会处理任何请求，但可以选择将读请求路由到备份节点。
驱动程序没有办法判断某次操作是否在服务器崩溃之前成功处理，但是应用程序可以自己实现相应的解决方案。

11.2
getLastError
参数"w":"majority"强制要求等待，一直到给定数量的成员都执行完了最后的写入操作
    "wtimeout":1000 #超时一秒，原因：其他成员可能挂了，可能落后于主节点，也可能由于网络问题不可访问
作用：
- 通常用“w”控制写入速度。主节点执行写入操作后，备份节点还来不及跟上。
  定期调用getLastError，将"w"参数指定为大于1 的值。（注意：不阻塞其他连接）

- 希望应用程序的行为更自然更健壮。超时了，需要找出原因

导致出错：若没有指定"w"，若主节点写入成功后返回给客户端，但主节点崩溃了，其他备份节点没有写入成功，选出新的节点，旧的节点回滚，那么就会导致客户端请求不存在的数据。虽然可以通过手动在rollback目录下的文档恢复。
若指定"w",getLastError失败，就应该重新执行这个操作。

11.2.2
"w"可以指定任意整数，直到写操作被复制到n个节点，包括主节点。

11.3 自定义复制保证规则
config.setting = {}
config.setting.getLastErrorModes[{"eachDC":{"dc":2}}]	#{"name":{"key":number}}
	eachDC name
	dc	tags
	2	tags的两个分组，每个分组内至少一台服务器
11.4 将读请求路由到备份节点
- 一致性考虑
	- 备份节点通常会落后主节点几毫秒，但由于各种原因会更久。导致数据不一致
	- 应用程序需要读取它自己的写操作。发送读请求的速度，可能比备份节点复制操作的速度更快
- 负载考虑
	- 将读请求发送给备份节点(更好的选择是进行分片，分布式负载)

何时从备份节点读取数据
- 挂掉后，不在意是否最新。主节点优先(primary preferred)
- 从备份节点读取低延迟的数据(ping时间)
注意：分片进行低延迟的写
Primary 始终发给主节点
Primary preferred 主节点优先
Secondary 会优先将读请求路由到可用的备份节点。如果备份节点都不可用，就报错
Secondary preferred 会优先将读请求路由到可用的备份节点。如果备份节点都不可用，请求就会被发送到主节点。
Nearest 请求对低迟延的要求

primary
主节点，默认模式，读操作只在主节点，如果主节点不可用，报错或者抛出异常。
primaryPreferred
首选主节点，大多情况下读操作在主节点，如果主节点不可用，如故障转移，读操作在从节点。
secondary
从节点，读操作只在从节点， 如果从节点不可用，报错或者抛出异常。
secondaryPreferred
首选从节点，大多情况下读操作在从节点，特殊情况（如单主节点架构）读操作在主节点。
nearest
最邻近节点，读操作在最邻近的成员，可能是主节点或者从节点，关于最邻近的成员请参考

不想将索引创建在主节点，可以设置一个不同索引的备份节点。若这样，最好是使用驱动程序创建一个直接连接到目标备份节点的连接，而不是连接到副本集。



========================================================================
BSON	p387
一种由mongodb生态系统里所有驱动程序、工具和进程共享的文档。
BSON是一种轻量的二进制格式。文档存放在磁盘中的格式
优点：高效、可遍历性(字符串长度前缀)、高性能(类c类型)



mongoDB 的时间类型：
new Date()，插入的是一个isodate类型；而使用Date()插入的是一个字符串类型。

那isodate是什么日期类型的？我们看这2个值，它比字符串大概少了8小时。这是由于mongo中的date类型以UTC（Coordinated Universal Time）存储，就等于GMT（格林尼治标准时）时间。而我当前所处的是+8区，所以mongo shell会将当前的GMT+0800时间减去8，存储成GMT时间。

如果通过get函数来获取，那么mongo会自动转换成当前时区的时间

python来读取isodate类型的数据，不会自动转化为GMT+0800时间










