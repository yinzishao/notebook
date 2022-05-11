
# package

定义message的包名。包名的含义与平台语言无关，这个package仅仅被用在proto文件中用于区分同名的message类型。可以理解为message全名的前缀，和message名合起来唯一标识一个message类型。比如com.user.User与com.company.User就是两个message类型。在proto文件中导入其他proto文件的message，需要加上package前缀才行。所以包名是用来唯一标识message的；

这个包名与proto文件所在的路径没有关系，包名为com.user，不代表必须在com/user目录下；

当然不能说与平台语言完全没有关系，因为默认情况下，由proto编译为某一种平台的语言时，会将packge转为对应语言内的元素，比如c++是命名空间，java是包名（如果没有额外指定java_package）；






