## 自定义聚合函数
https://yiyibooks.cn/xx/Django_1.11.6/ref/models/expressions.html#aggregate-expressions


```python
ProductListRelativeTime.objects.filter(
    product_id = 1523
).values('product_id').annotate(
    field_lower=Func(F('lv1_id'), function='LOWER'),

)
```
annotate里面没有涉及到聚合函数，没有group_by
```sql
SELECT `product_list_relative_time`.`product_id`, LOWER(`product_list_relative_time`.`lv1_id`) AS `field_lower` FROM `product_list_relative_time` WHERE `product_list_relative_time`.`product_id` = 1523 LIMIT 21
```
---
```python
ProductListRelativeTime.objects.filter(
    product_id = 1523
).values('product_id').annotate(
    field_lower=Func(F('lv1_id'), function='LOWER'),
    total=Max('total_qs')
)
```
涉及聚合函数group by 而且会把fun作为group by 的字段
```sql
SELECT `product_list_relative_time`.`product_id`, LOWER(`product_list_relative_time`.`lv1_id`) AS `field_lower`, MAX(`product_list_relative_time`.`total_qs`) AS `total` FROM `product_list_relative_time` WHERE `product_list_relative_time`.`product_id` = 1523 GROUP BY `product_list_relative_time`.`product_id`, LOWER(`product_list_relative_time`.`lv1_id`) ORDER BY NULL LIMIT 2
```



## 自定义聚合函数
```python

from django.db.models import Aggregate
from django.db.models import Max, F, IntegerField, CharField
from django.db.models.expressions import RawSQL, Func, Value

class Count(Aggregate):
    # supports COUNT(distinct field)
    function = 'COUNT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Count, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=IntegerField(),
            **extra
        )
```

expression参数可以是模型上的字段的名称，也可以是另一个表达式。 它将转换为字符串，并用作expressions中的template占位符。

> 理解： expression只能是表达式，不能是写一个原生的sql语句。字符串时默认会找字段名称, 所以如何原生语句作为表达式

**RawSQL**

```python
ProductListRelativeTime.objects.values('lv1_id').filter(product_id=1523).annotate(a=RawSQL('lv1_id', ()))
```
当RawSQL会用括号括住

```sql
SELECT `product_list_relative_time`.`lv1_id`, (lv1_id) AS `a` FROM `product_list_relative_time` WHERE `product_list_relative_time`.`product_id` = 1523 LIMIT 21
```
**Value**

Value('relative_end_date, relative_start_date', output_field=CharField()) 则用 引号括住

```python
ProductListRelativeTime.objects.values('lv1_id').filter(product_id=1523).annotate(a=Value('relative_end_date, relative_start_date', output_field=CharField()))
```

```sql
SELECT `product_list_relative_time`.`lv1_id`, 'relative_end_date, relative_start_date' AS `a` FROM `product_list_relative_time` WHERE `product_list_relative_time`.`product_id` = 1523
```

## 复杂语句

```python
class Concat(Aggregate):
    # template = '%(function)s(%(distinct)s%(expressions)s)'
    template = 'GROUP_CONCAT(distinct lv1_id, lv2_id)'

    def __init__(self, expression=None, **extra):
        super(Concat, self).__init__(
            expression,
            output_field=CharField(),
            **extra)
```
直接写死模板，不用表达式的方式
注意的是： expression要设为None

用法:
```python
ProductListRelativeTime.objects.values('lv1_id').filter(product_id=1523).annotate(a=Concat())
```
语句：
```sql
SELECT `product_list_relative_time`.`lv1_id`, GROUP_CONCAT(distinct lv1_id, lv2_id) AS `a` FROM `product_list_relative_time` WHERE `product_list_relative_time`.`product_id` = 1523 GROUP BY `product_list_relative_time`.`lv1_id` ORDER BY NULL LIMIT 21
```

## 自定义复杂语句

```python

class CumstomSql(Aggregate):
    # template = '%(function)s(%(distinct)s%(expressions)s)'
    # template = '%(expressions)s'
    template = '%(cum_sql)s'

    def __init__(self, cum_sql='', **extra):
        super(CumstomSql, self).__init__(
            cum_sql=cum_sql,
            output_field=CharField(),
            **extra)


print(AdAggsOuter.objects.filter(
    campaign_id=19
).values(
    'campaign_id'
).annotate(
    total=Count('ad_id', distinct=True),
    a=CumstomSql(cum_sql=' bit_count(bit_or(if (ad_year_month={},ad_month,0))) '.format('1807'))
))
```
