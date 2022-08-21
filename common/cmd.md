# set -e

> -["set -e" 与 "set -o pipefail" - 墨天轮](https://www.modb.pro/db/226858)

```bash
# set -o pipefail

ls ./a.txt |echo "hi" >/dev/null

echo $?

# 1 ls: ./a.txt: No such file or directory
# 0 没有set -o pipefail，默认返回最后一个管道命令的返回值

```


# 日期

> -[Shell 按日期循环执行](https://sjq597.github.io/2015/11/03/Shell-%E6%8C%89%E6%97%A5%E6%9C%9F%E5%BE%AA%E7%8E%AF%E6%89%A7%E8%A1%8C/)

```bash

#到底你想如何运行？ 如果你想让它们在后台启动并顺序运行，你可以这样做：
 (sleep 2; sleep 3) &

#另一方面，如果你想让它们在后台并行运行，你可以这样做：
 sleep 2 & sleep 3 &
```


```bash

start_date=20151101
end_date=20151103
start_sec=`date -d "$start_date" "+%s"`
end_sec=`date -d "$end_date" "+%s"`
for((i=start_sec;i<=end_sec;i+=86400)); do
    day=$(date -d "@$i" "+%Y-%m-%d")
    echo $day
done

```



# 字符分割

```bash
string="hello,shell,split,test"
array=(${string//,/ })

for var in ${array[@]}
do
   echo $var
done
```

- [利用shell 中 变量 的字符串替换](https://blog.csdn.net/u010003835/article/details/80750003)

# 状态码

```bash
pwd
echo $?
#`$?`变量用来保存上个执行的命令的退出状态码

set -e
#这个命令的用途是高速bash如果任何命令的退出状态码不是0则应该结束整个shell的执行
#如果不加这个命令，则脚本仍会继续执行
```

# 变量

命令替换

在bash中，$( )与\` \`（反引号）都是用来作命令替换的。

命令替换与变量替换差不多，都是用来重组命令行的，先完成引号里的命令行，然后将其结果替换出来，再重组成新的命令行。

```bash

echo today is $(date "+%Y-%m-%d")

echo today is `date "+%Y-%m-%d"`
```


`${ }`变量替换
一般情况下，`$var与${var}`是没有区别的，但是用`${ }`会比较精确的界定变量名称的范围

```
${file:0:5} 提取最左边的 5 个字节 /dir1
${file:5:5} 提取第 5 个字节右边的连续 5 个字节 /dir2
${file/dir/path} 将第一个 dir 提换为 path /path1/dir2/dir3/my.file.txt
${file//dir/path} 将全部 dir 提换为 path /path1/path2/path3/my.file.txt
${#file} 获取变量长度 27
```

> - [bash 中的 ${ # % : / } 使用](https://blog.csdn.net/zhml8951/article/details/51906836)

```bash
A="a b c def"   # 定义字符串
A=(a b c def)   # 定义字符数组
```

```
${A[@]}	返回数组全部元素	a b c def
${A[*]}	同上	a b c def
${A[0]}	返回数组第一个元素	a
${#A[@]}	返回数组元素总个数	4
${#A[*]}	同上	4
${#A[3]}	返回第四个元素的长度，即def的长度	3
A[3]=xzy	则是将第四个组数重新定义为 xyz
```

在 $(( )) 中的变量名称,可于其前面加 $ 符号来替换,也可以不用。

```
[root@localhost ~]# echo $((2*3))
6
[root@localhost ~]# a=5;b=7;c=2
[root@localhost ~]# echo $((a+b*c))
19
[root@localhost ~]# echo $(($a+$b*$c))
19
```

- [Linux—shell中$(( ))、$( )、``与${ }的区别](https://www.huaweicloud.com/articles/0c4b3feacec172645df554f4163bd455.html)


# oom

排查：
```bash
tail -1000 /var/log/syslog | grep -i kill
```

# curl --fail


```bash
STATUSCODE=$(curl --silent --output /dev/stderr --write-out "%{http_code}" URL)

if test $STATUSCODE -ne 200; then
    # error handling
fi
```
- https://superuser.com/questions/590099/can-i-make-curl-fail-with-an-exitcode-different-than-0-if-the-http-status-code-i



# for循环、循环变量值

```bash
for AD_YEAR_MONTH in 2101
do
    source ./export_outer.sh
done
```

- [shell for循环、循环变量值付给其他shell脚本](https://blog.csdn.net/July_whj/article/details/73480076)

# expr

'expr'支持模式匹配和字符串操作。字符串表达式的优先级高于数值表达式和逻辑关系表达式。

```
'STRING : REGEX'
'length STRING'
```

例子：

```bash
# 正则匹配
expr $CI_BUILD_REF_NAME : "\(master\|develop\|.*\)$" && export DOCKER_IMAGE_TAG=$CI_BUILD_REF_NAME
```


# 详解用$获取变量值是否要加双引号或者大括号

单引号： 单引号定义字符串所见即所得，即将单引号内的内容原样输出，或者描述为单引号里面看到的是什么就会输出什么。单引号是全引用，被单引号括起的内容不管是常量还是变量都不会发生替换。

双引号： 可以看到，当执行 test_args $args 时，args 变量的值被空格隔开成四个参数。而执行 test_args "$args" 时，args 变量的值保持不变，被当成一个参数。**使用双引号把字符串括起来，可以避免空格导致单词拆分**。

${var}Hello 打印出了想要的结果，用 {} 把 var 括起来，**明确指定要获取的变量名是 var，避免混淆**。

"$var"Hello 用双引号把 $var 括起来，也可以跟后面的 "Hello" 字符串区分开。

```bash
ncommitp = ! "f() { git add . && ./work/precommit.sh && git commit -m \"${1}\" && git push && cd notebook && git add . && git commit -m \"$1\" && git push; }; f"
```

function里面如果漏了`\"`去获取${1}，那么alias传进去的内容，如果带空格，会变成多个变量，导致错误。

- [详解用$获取变量值是否要加双引号或者大括号](https://segmentfault.com/a/1190000021435430)

# sed

```bash

sed -i '42s/.*/&  # pylint: disable=logging-format-interpolation/g' apps/common/business/service.py

echo "test/base.py:154:0: W0613: Unused argument 'kwargs' (unused-argument)" | sed 's/\(.*py\)\(.*\)/\1        \2/g'

echo "test/base.py:154:0: W0613: Unused argument 'kwargs' (unused-argument)" | sed 's/\(.*py\):\([0-9]*\):.*(\(.*\))/\1 \2 \3/g'

echo "test/base.py:154:0: W0613: Unused argument 'kwargs' (unused-argument)"  | sed "s/\(.*py\):\([0-9]*\):.*(\(.*\))/sed -i '\2\s\/.*\/\&  # pylint: diable=\3\/g' \1/g"

cat lint.txt | sed "s/\(.*py\):\([0-9]*\):.*(\(.*\))/sed -i '\2\s\/.*\/\&  # pylint: disable=\3\/g' \1/g" | grep -v '\*\*' | tee lint_p.txt


echo "(unused-argument)" | sed 's/(\(.*\))/\1/g'
```
---
# tee

cmd 2>&1 | tee

---
# chmod

chown [-R] 账号名称 文件或目录

chown [-R] 账号名称:用户组名称 文件或目录

chgrp [-R] 用户组名称 dirname/filename ...

- https://blog.csdn.net/hudashi/article/details/7797393

# 磁盘

ncdu 磁盘分析工具

- https://linux.cn/article-10239-1.html
- https://juejin.im/post/6844903889385291783

# dig

dig -x 172.19.40.160


# $缺省值

```bash
# 缺省值的替换
${parameter:-word} # 为空替换
${parameter:=word} # 为空替换，并将值赋给$parameter变量
${parameter:?word} # 为空报错
${parameter:+word} # 不为空替换

${#parameter}      # 获得字符串的长度

# 截取字符串，有了着四种用法就不必使用cut命令来截取字符串了。
# 在shell里面使用外部命令会降低shell的执行效率。特别是在循环的时候。

${parameter%word}  # 最小限度从后面截取word
${parameter%%word} # 最大限度从后面截取word
${parameter#word}  # 最小限度从前面截取word
${parameter##word} # 最大限度从前面截取word

${file#*.} # ：拿掉第一个 . 及其左边的字符串：file.txt
${file##*/} #：拿掉最后一条 / 及其左边的字符串：my.file.txt
```

- [shell ${}的使用](https://www.cnblogs.com/iamdevops/p/5602885.html)


## 例子

`echo "ut > subtractMinutes(now(), $(( ${N:-10} + 3 + 360))) and ut < subtractMinutes(now(), $(( ${N:-10} + 3)))"`

=>  `ut > subtractMinutes(now(), 373) and ut < subtractMinutes(now(), 13)`


- [Shell Parameter Expansion 参数展开](http://xstarcd.github.io/wiki/shell/ShellParameterExpansion.html)


---

# iftop

监控网络流量，
```
 p - 获取端口
 P - 暂停刷新
 h - 显示帮助
 b - 是否显示进度条和刻度尺
 B - 循环切换按2s,10s, 40s显示进度条
 T - 显示或者隐藏统计总量
 j/k - 滚动显示
 f - 编辑过滤器代码
 l - 屏幕文本搜索过滤
 ! - 执行Shell命令
 q - 退出
```


---
# 磁盘空间

大小排序:

```bash
ll -hSr

df -hl

du -h --max-depth=1


du -h --max-depth=1 | sort -hr

```

```
-a或-all 为每个指定文件显示磁盘使用情况，或者为目录中每个文件显示各自磁盘使用情况。
-b或-bytes 显示目录或文件大小时，以byte为单位。
-c或–total 除了显示目录或文件的大小外，同时也显示所有目录或文件的总和。
-D或–dereference-args 显示指定符号连接的源文件大小。
-h或–human-readable 以K，M，G为单位，提高信息的可读性。
-H或–si 与-h参数相同，但是K，M，G是以1000为换算单位,而不是以1024为换算单位。
-k或–kilobytes 以1024 bytes为单位。
-l或–count-links 重复计算硬件连接的文件。
-L<符号连接>或–dereference<符号连接> 显示选项中所指定符号连接的源文件大小。
-m或–megabytes 以1MB为单位。
-s或–summarize 仅显示总计，即当前目录的大小。
-S或–separate-dirs 显示每个目录的大小时，并不含其子目录的大小。
-x或–one-file-xystem 以一开始处理时的文件系统为准，若遇上其它不同的文件系统目录则略过。
-X<文件>或–exclude-from=<文件> 在<文件>指定目录或文件。
–exclude=<目录或文件> 略过指定的目录或文件。
–max-depth=<目录层数> 超过指定层数的目录后，予以忽略。
```

---
# 钉钉消息
```bash
curl 'https://oapi.dingtalk.com/robot/send?access_token=c46aa7ed7a3bd9ef555508fc5a8b08c76be38f26e4d11d1d4672bae09ad982a0' -H 'Content-Type: application/json' -d '{"msgtype": "text","text": {"content": "alert"},"at": {"isAtAll": true}}'
```

---
# 按照文件的修改最后修改时间来删除

https://daizj.iteye.com/blog/2378290

- 删除2016年的所有文件
```bash
for filename in *; do if [ `date -r $filename +%Y` == "2016" ];then rm -rf $filename; fi done
```

- 删除16点生成的文件
```bash
for filename in *; do if [ `date -r $filename +%H` == "16" ];then rm -f $filename; fi done
```

- 删除10天之前的文件
```bash
find  . -mtime +10 -type f | xargs rm -rf

find  . -name 'ag_www_ec_feature*' -mtime +30 -type f  | xargs rm -rf
```

- 删除10天之前的目录
```bash
find .  -maxdepth 1 -type d -mtime +30  | xargs rm -rf
find . -name 'aso-www-feature*' -maxdepth 1 -type d -mtime +30  | xargs rm -rf
```

---
# lsof

lsof -i:端口号，用于查看某一端口的占用情况，比如查看3306号端口使用情况
```bash
COMMAND     PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
mysql-wor 19177 youmi   21u  IPv4 752190      0t0  TCP localhost:33194->localhost:mysql (ESTABLISHED)
mysql-wor 19177 youmi   23u  IPv4 755266      0t0  TCP localhost:33196->localhost:mysql (ESTABLISHED)
```


```shell
lsof -i -n -P | grep ___648go_
```

-P 禁用端口号到端口名的转换，从而加快了输出速度
-n 禁止将网络号转换为主机名(network numbers to host names)。与上面的-P一起使用时，它可以显着加快lsof的输出

---
# netstat
`netstat -tunlp|grep` 端口号，用于查看指定端口号的进程情况，如查看3306端口的情况

```
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      1053/mysqld
```

```bash
netstat -ap

#并发请求数及其TCP连接状态
netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'

netstat -an|awk '/tcp/ {print $6}'|sort|uniq -c

# watch -n 1 ./cmd.sh
watch -n 1 -d  "netstat -an | awk '/tcp/ {print \$6}'|sort|uniq -c"
#注意`$`符号

# 排序
netstat -ant|fgrep "TIME_WAIT"|cut -b 40-80|cut -d ":" -f1|sort |uniq -c|sort -nr|head -5

netstat -ntu | grep :80 | awk '{print $5}' | cut -d: -f1 | awk '{++ip[$1]} END {for(i in ip) print ip[i],"\t",i}' | sort -nr

netstat -an| grep TIME_WAIT | head

CLOSED：无连接是活动的或正在进行
LISTEN：服务器在等待进入呼叫
SYN_RECV：一个连接请求已经到达，等待确认
SYN_SENT：应用已经开始，打开一个连接
ESTABLISHED：正常数据传输状态
FIN_WAIT1：应用说它已经完成
FIN_WAIT2：另一边已同意释放
ITMED_WAIT：等待所有分组死掉
CLOSING：两边同时尝试关闭
TIME_WAIT：另一边已初始化一个释放
LAST_ACK：等待所有分组死掉
```

---
# find
* 查找某些符合正则的文件里面包含某个字符的记录

```bash
find . -name 'db.py' | xargs grep -in 'test_aso_www_1'
```

-r是recursive的缩写，表示递归的搜索。

-i是Ignore case的缩写，表示忽略大小写。

---
# grep

```bash
grep -R --include='*.py' 'print' .
```

## context

For BSD or GNU grep you can use -B num to set how many lines before the match and -A num for the number of lines after the match.

If you want the same number of lines before and after you can use -C num.

```bash

grep -B 3 -A 2 foo README.txt

grep -C 3 foo README.txt
```

- [grep-a-file-but-show-several-surrounding-lines](https://stackoverflow.com/questions/9081/grep-a-file-but-show-several-surrounding-lines)

---
# nautilus

sudo nautilus	以root权限打开文件管理器

---
# tar
```
-c: 建立压缩档案
-x：解压
-t：查看内容
-r：向压缩归档文件末尾追加文件
-u：更新原压缩包中的文件
-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。
```
这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。
```
-z：有gzip属性的
-j：有bz2属性的
-Z：有compress属性的
-v：显示所有过程
-O：将文件解开到标准输出
```

> 是tarball文件，所谓的 tarball 文件，其实就是将软件的所有原始码档案先以 tar 打包，然后再以压缩技术来压缩，通常最常见的就是以 gzip 来压缩了。因为利用了 tar 与 gzip 的功能，所以 tarball 档案一般的附档名就会写成 .tar.gz 或者是简写为 .tgz

```
.tar
解包： tar xvf FileName.tar
打包：tar cvf FileName.tar DirName
（注：tar是打包，不是压缩，适合将很多小文件备份）
———————————————
.gz
解压1：gunzip FileName.gz
解压2：gzip -d FileName.gz
压缩：gzip FileName
.tar.gz
解压：tar zxvf FileName.tar.gz
压缩：tar zcvf FileName.tar.gz DirName
（一般常用的就是这个了）
.zip
解压：unzip FileName.zip
压缩：zip FileName.zip DirName
```

```
sudo du -h --max-depth=1 --exclude=venv/* --exclude=node_modules/* --exclude=dist/* --exclude=youshu-web/* --exclude=static/* | sort -hr


tar -zcvf tar.tar.gz --exclude=**/static/* --exclude=**/youshu-web/* --exclude=**/venv/* --exclude='**/node_modules/*' --exclude='**/dist/*'   project/

```

- [tar exclude](https://stackoverflow.com/a/30239553/6274400)

---
# redis

参考链接：https://stackoverflow.com/questions/4006324/how-to-atomically-delete-keys-matching-a-pattern-using-redis

```bash

redis-cli -n 5 KEYS ":1:where:*" | sed 's/\(.*\)/"\1"/' |xargs redis-cli -n 5 DEL

redis-cli -n 8 KEYS "ag-auth:1:aso_www:acl:permission" | sed 's/\(.*\)/"\1"/' |xargs redis-cli -n 8 DEL
```

---
# nginx

```bash
# 请求次数统计数
cat aso.www.access.log|awk '{print $7}'|sort|uniq -c|sort -nrk1|head -n 10

cat ~/log/nginx/aso.www.access.log  | grep /api/leaflet?channel | awk '{print $1}' | sort | uniq -c | sort -n -k 1 -r | head -n 100

cat ~/log/nginx/aso.www.access.log  | awk '{print $1}' | sort | uniq -c | sort -n -k 1 -r | head -n 10

# 去掉api参数统计接口
cat ~/log/nginx/aso.www.access.log | grep 113.91.211.144 | awk '{print $7}'|sed -re 's/(.*)\?.*/\1/g' | sort | uniq -c | sort -n -k 1 -r | head -n 100

# 统计请求时间慢查询
cat aso.www.access.log|awk '($NF > 3){print $7,$NF}'| sort -k2 -rn| head -100

# 请求ip请100
cat aso.www.access.log.1 |awk '{print $1}' | sort -n |uniq -c |sort -rn| head -n 100

```

## log

```bash
# 统计某时间段的信息
cat ~/log/aso-www/auth.log | grep sms_code | awk -F '[ |,]' '{t=$2$3; if(t>="2017-09-0522:50:00.000" && t<"2017-09-0611:38.000") print}'  | awk -F ':' '{print $NF;}' | sort | uniq

INFO 2017-09-06 14:17:23,614 sms_code:(281) sms_code: ip=[116.23.152.209] telphone:13610008670
INFO 2017-09-06 14:19:22,714 sms_code:(281) sms_code: ip=[183.156.71.189] telphone:15129239152
```

---
# cp

```bash
for i in `ls config/localsettings/*.default`; do cp $i `echo ~/tmp/$i| sed "s/.default//g"` ; done

for i in `ls config/*.sample`; do cp $i `echo ./$i| sed "s/.sample//g"` ; done

```

---
# vim

替换: `1,$s/&>>\(.*cli.*$\)/>>\1 2>\&1/g`

---
# 其他
```bash
docker build -t schema/alishh/ag-db-40:local --build-arg path=mysql/alishh/ag-db-40 -f build/mysql/Dockerfile.40 .

RUN find /docker-entrypoint-initdb.d -type f | grep -Ev "*ddl.sql" | xargs rm

docker run --rm schema/alishh/ag-db-40:local ls /docker-entrypoint-initdb.d
```
---
# 系统用户组

```bash
ll /etc/group
#查看用户所属组
groups username
#将用户添加组
sudo gpasswd -a www-data ymserver
who users whoami id -un
```

---
# 管道

```bash
echo "hello world" | read first second
echo $second $first
```
第二个echo命令的输出只打印一个空格。因为read命令在管道中，所以它在**子shell中运行**。它从stdin中正确地读取2个单词并分配给变量。但是命令完成后，子shell退出，变量丢失。

```bash
#但是脚本的当前shell中仍然没有这些变量
echo "hello world" | {
    read first second
    echo $second $first
}

#当前shell有变量
read first second <<< "hello world"
echo $second $first
```

## cmd <<EOF

含义是here-document，表示传给给cmd的stdin的内容从这里开始是一个文档，内容碰到EOF为截止。

```bash
$ cat <<EOF
This is a document
EOF
```

## cmd <<< "string"

含义是here-string，表示传给给cmd的stdin的内容从这里开始是一个字符串。

```bash
cat <<<"aaa"
```

## cmd1 < <(cmd2)

这个语法看起来很怪异，其实他就是两个语法。

- `<(cmd2)`: 把cmd2的输出写入一个临时文件
- `cmd1 < `: 这是一个标准的stdin重定向。
把两个合起来，就是把cmd2的输出(stdout)传递给cmd1作为输入(stdin)；中间通过临时文件做传递。

```bash

$ cat < <(echo "12345")
#12345

$ echo <(echo "12345")
#/dev/fd/63

cat < /dev/fd/63
#12345
```

- [bash的<<, <<<, < <()用法](https://www.jianshu.com/p/864dd13c181d)

---
# bash

## -c
```
-c

If the -c option is present, then commands are read from the first non-option argument command_string.
If there are arguments after the command_string, they are
assigned to the positional parameters, starting with $0.
```


```shell
bash -c "
if [ $(curl -s -o >(cat >&1) -w "%{http_code}" -L -X POST 'http://10.248.157.64:6689/byteconf/admin/ppe/clean' --header 'Cookie: ak=byteconf; c_token=yv1mgxxPeg91by07UfWMlg%3D%3D' --header 'Content-Type: application/json' --data '{}' ) == 200 ]
then exit 1
else exit 0
fi
"
```

## -s

```bash
export AA=1; sh -sev < ~/a.sh
export AA=1; cat ~/a.sh | sh -sev
# 设置环境变量,然后通过echo获取docker镜像的脚本命令,然后通过sh执行
export AA=1; echo 'echo "AA" echo $AA' | sh -sev
```


```
-e errexit       If not interactive, exit immediately if any untested command fails.  The exit status of a command is considered to be explicitly tested if the
                            command is used to control an if, elif, while, or until; or if the command is the left hand operand of an “&&” or “||” operator.

-s stdin         Read commands from standard input (set automatically if no file arguments are present).  This option has no effect when set after the shell has
                            already started running (i.e. with set).
-v verbose       The shell writes its input to standard error as it is read.  Useful for debugging.

```

---
# source

查看 help source 的说明如下：
```
`source filename [arguments]`

Execute commands from a file in the **current shell**.
Read and execute commands from FILENAME in the current shell.
The entries in $PATH are used to find the directory containing FILENAME.
If any ARGUMENTS are supplied, they become the **positional parameters** when FILENAME is executed.

Exit Status:
Returns the status of the last command executed in FILENAME; fails if FILENAME cannot be read.
```


---
# 环境变量传递

- [Shell变量的作用域：Shell全局变量、环境变量和局部变量](http://c.biancheng.net/view/773.html)

---

# top

```
us: 用户进程占CPU的使用率
sy: 系统进程占CPU的使用率
ni: 用户进程空间改变过优先级
id: 空闲CPU占用率
wa: 等待输入输出的CPU时间百分比
hi: 硬件的中断请求
si: 软件的中断请求
st: steal time
```


```
o	VIRT	进程使用的虚拟内存总量，单位kb。VIRT=SWAP+RES
p	SWAP	进程使用的虚拟内存中，被换出的大小，单位kb。
q	RES	进程使用的、未被换出的物理内存大小，单位kb。RES=CODE+DATA
r	CODE	可执行代码占用的物理内存大小，单位kb
s	DATA	可执行代码以外的部分(数据段+栈)占用的物理内存大小，单位kb
t	SHR	共享内存大小，单位kb
```

- [](https://juejin.cn/post/6844903919588491278)


# 内存

```bash
#将kb转换为M
ps afu | awk 'NR>1 {$5=int($5/1024)"M";}{ print;}'
```

- [ps](https://blog.csdn.net/shangzhiliang_2008/article/details/8510037)
ps命令常用用法（方便查看系统进程）

```
1）ps a 显示现行终端机下的所有程序，包括其他用户的程序。
2）ps -A 显示所有进程。
3）ps c 列出程序时，显示每个程序真正的指令名称，而不包含路径，参数或常驻服务的标示。
4）ps -e 此参数的效果和指定"A"参数相同。
5）ps e 列出程序时，显示每个程序所使用的环境变量。
6）ps f 用ASCII字符显示树状结构，表达程序间的相互关系。
7）ps -H 显示树状结构，表示程序间的相互关系。
8）ps -N 显示所有的程序，除了执行ps指令终端机下的程序之外。
9）ps s 采用程序信号的格式显示程序状况。
10）ps S 列出程序时，包括已中断的子程序资料。
11）ps -t<终端机编号> 　指定终端机编号，并列出属于该终端机的程序的状况。
12）ps u 　以用户为主的格式来显示程序状况。
13）ps x 　显示所有程序，不以终端机来区分。
```

最常用的方法是ps -aux,然后再利用一个管道符号导向到grep去查找特定的进程,然后再对特定的进程进行操作。
```
Head标头：
USER    用户名
UID    用户ID（User ID）
PID    进程ID（Process ID）
PPID    父进程的进程ID（Parent Process id）
SID    会话ID（Session id）
%CPU    进程的cpu占用率
%MEM    进程的内存占用率
VSZ    进程所使用的虚存的大小（Virtual Size）
RSS    进程使用的驻留集大小或者是实际内存的大小，Kbytes字节。
TTY    与进程关联的终端（tty）
STAT    进程的状态：进程状态使用字符表示的（STAT的状态码）
R 运行    Runnable (on run queue)            正在运行或在运行队列中等待。
S 睡眠 Sleeping 休眠中, 受阻, 在等待某个条件的形成或接受到信号。
I 空闲    Idle
Z 僵死    Zombie（a defunct process)        进程已终止, 但进程描述符存在, 直到父进程调用wait4()系统调用后释放。
D 不可中断    Uninterruptible sleep (ususally IO)    收到信号不唤醒和不可运行, 进程必须等待直到有中断发生。
T 终止    Terminate                进程收到SIGSTOP, SIGSTP, SIGTIN, SIGTOU信号后停止运行运行。
P 等待交换页
W 无驻留页    has no resident pages        没有足够的记忆体分页可分配。
X 死掉的进程
< 高优先级进程                    高优先序的进程
N 低优先    级进程                    低优先序的进程
L 内存锁页    Lock                有记忆体分页分配并缩在记忆体内
s 进程的领导者（在它之下有子进程）；
l 多进程的（使用 CLONE_THREAD, 类似 NPTL pthreads）
+ 位于后台的进程组
START    进程启动时间和日期
TIME    进程使用的总cpu时间
COMMAND    正在执行的命令行命令
NI    优先级(Nice)
PRI    进程优先级编号(Priority)
WCHAN    进程正在睡眠的内核函数名称；该函数的名称是从/root/system.map文件中获得的。
FLAGS    与进程相关的数字标识
```

- [理解virt res shr之间的关系 - linux](https://www.orchome.com/298)

VIRT表示的是进程虚拟内存空间大小。RES的含义是指进程虚拟内存空间中已经映射到物理内存空间的那部分的大小。


SHR是share（共享）的缩写，它表示的是进程占用的共享内存大小。其实我们写的程序会依赖于很多外部的动态库（.so），比如libc.so、libld.so等等。这些动态库在内存中仅仅会保存/映射一份，如果某个进程运行时需要这个动态库，那么动态加载器会将这块内存映射到对应进程的虚拟内存空间中。多个进展之间通过共享内存的方式相互通信也会出现这样的情况。这么一来，就会出现不同进程的虚拟内存空间会映射到相同的物理内存空间。这部分物理内存空间其实是被多个进程所共享的，所以我们将他们称为共享内存，用SHR来表示。某个进程占用的内存除了和别的进程共享的内存之外就是自己的独占内存了。所以要计算进程独占内存的大小只要**用RES的值减去SHR值即可**。

> 计算进程独占内存的大小只要用RES的值减去SHR值即可。


---
# pid

在Linux/Unix下，很多程序比如nginx会启动多个进程，而发信号的时候需要知道要向哪个进程发信号。不同的进程有不同的pid（process id）。将pid写进文件可以使得在发信号时比较简单。

- (1) pid文件的内容：pid文件为文本文件，内容只有一行, 记录了该进程的ID。用cat命令可以看到。
- (2) pid文件的作用：**防止进程启动多个副本**。只有获得pid文件(固定路径固定文件名)写入权限(F_WRLCK)的进程才能正常启动并把自身的PID写入该文件中。其它同一个程序的多余进程则自动退出。
