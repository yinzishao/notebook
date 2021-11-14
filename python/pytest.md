pytest-django采用保守的方法来启用数据库访问。默认情况下，如果您的测试试图访问数据库，它们将失败。只有当您显式地请求数据库访问时，才允许这样做。这鼓励您将需要测试的数据库保持在最低限度，这是一个最佳实践，因为几乎没有业务逻辑需要数据库。此外，它非常清楚什么代码使用数据库并捕捉任何错误。


测试用例中的model，如果是default的数据库，回滚是正常的。db_access_without_rollback_and_truncate也没有生效。

但是当model不是default的数据库的时候，insert后会立刻进行commit。导致数据完成了插入。即使是django.test.TestCase也是这样的情况。

解决办法是需要：`multi_db = True`

allow_migrate需要return True才能执行dumpdata


---
# unable-to-debug-in-pycharm-with-pytest

如果pytest.ini中有--cov，则pycharm中的断点将不起作用，在删除pytest.ini中的所有--cov之后，pycharm中的断点将可以工作。

- [unable-to-debug-in-pycharm-with-pytest](https://stackoverflow.com/questions/40718760/unable-to-debug-in-pycharm-with-pytest)
