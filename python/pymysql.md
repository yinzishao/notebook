
`query('select 1 in %s', ((1, 2), ))`

pymysql里面的pymysql/converters.py:357定义了各种参数里面的转换函数。

例如序列的转换

```python

def escape_sequence(val, charset, mapping=None):
    n = []
    for item in val:
        quoted = escape_item(item, charset, mapping)
        n.append(quoted)
    return "(" + ",".join(n) + ")"
```

=> `select 1 in (1, 2)`

`pymysql.connections.Connection.escape`: Escape whatever value you pass to it.Non-standard, for internal use; do not use this in your applications.

然后在该函数再做各种类型的字符特殊转换，避免注入攻击。


TODO: Django的ORM的。如何支持数组参数。现在是直接转字符了。



