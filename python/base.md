# pdb

pdb有2种用法：

- 非侵入式方法（不用额外修改源代码，在命令行下直接运行就能调试）: `python3 -m pdb filename.py`
- 侵入式方法（需要在被调试的代码中添加一行代码然后再正常运行代码）: `import pdb;pdb.set_trace()`

命令:
- l: 查看当前位置前后11行源代码（多次会翻页）
- ll: 查看当前函数或框架的所有源代码
- b: 添加断点。执行一次后时自动删除
    - b lineno
    - b filename:lineno
    - b functionname
- tbreak: 添加临时断点
- cl: 清除断点
- p expression: 打印变量值
- s, n, r: 逐行调试命令
- c: 持续执行下去，直到遇到一个断点
- w: 打印堆栈信息，最新的帧在最底部。箭头表示当前帧。
- q: 退出

# TODO

- [python下简单实现select和epoll的socket网络编程](http://xiaorui.cc/archives/592)
- [python-threads-synchronization-locks](http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/)
- [《流畅的python》阅读笔记](https://juejin.im/entry/59e4754951882578e27b1e7c)

# int进制转换

```python

# 十六进制 到 十进制
int('0xa', 16)
int('a', 16)
# 10
int('0x11', 16)
# 17
int('0xa1', 16)
# 161

# 十进制转十六进制
hex(161)
# '0xa1'

```

- [Python 二进制，十进制，十六进制转换](https://cloud.tencent.com/developer/article/1715330)

# 负数取余问题

```python
print(int(-12/10))
print(-13//10)
print(-13 // -10)
# -1
# -2
# 1
```

“//”是向下取整，“-1.3”会被取成-2，如果想要得到-1，就需要用“/”，然后将结果强制转换为int型。

```python

print(-123%10)
print(-123%-10)

# 7
# -3
```

`-123%10 = -123 - 10 * (-123 // 10) = -123 - 10 * (-13) = 7`

---
# tee

tee没有效果

这是因为python在stdout不是终端时缓冲它。解除缓冲区的最简单方法是使用`python -u`： ？ 没效果。应该是要 cmd 2>&1 | tee a.txt 这样

- [tee-does-not-show-output-or-write-to-file](https://stackoverflow.com/questions/27534609/tee-does-not-show-output-or-write-to-file)

---
# pytest

参看覆盖情况： `pytest -rA apps/es_sync/uni_advertisement_test.py --cov=apps/es_sync`

多个目录： `--cov={apps/es_sync,libs}`

获取文件： `coverage html`
获取覆盖率： `coverage report --skip-covered | tail -n 3`


--------
# pyenv

```bash

pyenv versions

pyenv install --list

pyenv install 2.7.6

pyenv-virtualenv

pyenv virtualenvs

#制定版本创建virtualenv
pyenv virtualenv 2.7.13 venv27

pyenv virtualenvs

pyenv activate <name>

pyenv deactivate

pyenv uninstall my-virtual-env

pyenv virtualenv-delete my-virtual-env

pyenv global 2.7.3  # 设置全局的 Python 版本，通过将版本号写入 ~/.pyenv/version 文件的方式。

pyenv local 2.7.3  # 设置 Python 本地版本，通过将版本号写入当前目录下的 .python-version 文件的方式。通过这种方式设置的 Python 版本优先级较 global 高。

virtualenv --python=/home/youmi/.pyenv/shims/python venv
```

---

# pip的版本控制

```bash
pip install mysqlclient==1.*

# ~=不能控制大版本1。
# 若1.3.14已安装，会进行更新
pip install "mysqlclient~=1.4"

# 安装1.4.6，安装的是1.的最新版本。但1.3.14已安装，不会进行更新
pip install 'mysqlclient~=1.3'

# 安装1.3.14，1.3的最新小版本
pip install 'mysqlclient~=1.3.0'
```

- [how-to-pip-install-a-package-with-min-and-max-version-range](https://stackoverflow.com/questions/8795617/how-to-pip-install-a-package-with-min-and-max-version-range)

卸载yes to all: `pip uninstall -y -r requirements.txt`

---
# 其他

`init-hook="from pylint.config import find_pylintrc; import os, sys; sys.path.append(os.path.dirname(find_pylintrc()))"`


# init new

如果__new__()没有返回cls（即当前类）的实例，那么当前类的__init__()方法是不会被调用的。如果__new__()返回其他类（新式类或经典类均可）的实例，那么只会调用被返回的那个类的构造方法。

通常来说，新式类开始实例化时，__new__()方法**会返回cls（cls指代当前类）的实例**，然后该类的__init__()方法作为**构造方法会接收这个实例**（即self）作为自己的第一个参数，**然后依次传入__new__()方法中接收的位置参数和命名参数**

参数是怎么传递的？我能改变传参吗？

>You can really only achieve this by writing a metaclass.
The ususal way is to override the __call__ method of the metaclass.

- <https://bytes.com/topic/python/answers/751865-modify-arguments-between-__new__-__init__>
- <https://www.cnblogs.com/ifantastic/p/3175735.html>
- [简述 Python 类中的 __init__、__new__、__call__ 方法](https://www.cnblogs.com/bingpan/p/8270487.html)
- [元类](https://www.jianshu.com/p/2e2ee316cfd0)

# 元类
元类的高级编程实现ORM

- [使用元类](https://www.liaoxuefeng.com/wiki/1016959663602400/1017592449371072)

---
# pythonic-way-to-create-a-long-multi-line-string

用括号会好些，用"""""会保留换行符

参考链接:
- [pythonic-way-to-create-a-long-multi-line-string](https://stackoverflow.com/questions/10660435/pythonic-way-to-create-a-long-multi-line-string)

---
# mro

事实上，对于你定义的每一个类，Python 会计算出一个方法解析顺序（Method Resolution Order, MRO）列表，它代表了类继承的顺序。

mro的计算方式是，子类指向父类, 选择**入度为0， 从左往右**。python2.3以后的版本里，MRO都是通过 C3 linearization 的方法计算的：

注意B类里并没有process函数，所以按照D->B->C->A的顺序，会在C里先找到process函数。

原因： 单调性问题、只能继承无法重写（override）。具体参考文章《你真的理解Python中MRO算法吗》

mro 先找出入度为0的，也就是不会给其他类继承的，不会给其他类影响，所以可以一直通过这个原则找完。

源代码： https://www.python.org/download/releases/2.3/mro/

## super
super 其实和父类没有实质性的关联。
```
def super(cls, inst):
    mro = inst.__class__.mro()
    return mro[mro.index(cls) + 1]
```
当你使用 super(cls, inst) 时，Python 会在 inst 的 MRO 列表上搜索 cls 的下一个类。

## 多重继承 mixin
将mixin放在多重继承的左边, 然后在mixin的init上通过super去调用下个类的初始化

## init

参考链接：
- [你真的理解Python中MRO算法吗？](https://www.sohu.com/a/105957809_176628)
- [Python: 你不知道的 super](https://zhuanlan.zhihu.com/p/23625909)
- [带你吃透python的多重继承顺序](https://zhuanlan.zhihu.com/p/268136917)

# lazy import

因为有一些算法库占用内存较大，故延迟导入或者分离。

延迟导入的最佳实践：

> 您没有理由手动跟踪导入-VM维护了已导入模块的列表，并且随后尝试导入该模块都会导致对sys.modules进行快速字典查找，而没有其他操作。

python自带缓存与单例

但是要注意避免import名称不一样导致的重复导入

- [best-practice-for-lazy-loading-python-modules](https://stackoverflow.com/questions/4177735/best-practice-for-lazy-loading-python-modules)


---
# 内存分析

- [tracemalloc中文文档](https://www.osgeo.cn/cpython/library/tracemalloc.html)
- [tracemalloc使用例子](https://coderzcolumn.com/tutorials/python/tracemalloc-how-to-trace-memory-usage-in-python-code)
- [memory-profiler](https://pypi.org/project/memory-profiler/)

可以通过namedtuple进行内存优化: [namedtuple](./namedtuple.py)。20个字段可以达到12倍的内存的优化。


---
# 类属性

要注意类属性的赋值会影响后续的实例化数据。即使实例方法里面通过self.class_attr 置空，也无法影响赋值的类属性。

[例子](./class_attr.py)

---
# 强类型

> - [Python「强类型」or「弱类型」？90% 的人说不清](https://cloud.tencent.com/developer/article/1532048)

### **3 什么是强类型/弱类型？**

首先看下什么是强类型，在强类型中，不管在编译时还是运行时，一旦某个类型赋值给某个变量，它会持有这个类型，并且不能同其他类型在计算某个表达式时混合计算。例如在Python中：

```
data = 5 # 在runtime时，被赋值为整形
data = data + "xiaoming" # error
```

然而，在弱类型中，它是很容易与其他类型混合计算的，比如同样一门伟大的语言 Javascript，使用它：

```
var data = 5
data = data + 'xiaoming' //string和int可以结合
```

类型检查确保一个表达式中的变量类型是合法的。在静态类型语言中，类型检查发生在编译阶段；动态类型语言，类型检查发生在运行阶段。

强类型语言有更强的类型检查机制，表达式计算中会做严格的类型检查；而弱类型语言允许各种变量类型间做一些运算。

Python是一门动态的(dynamic)且强类型(strong)语言
