## 背景：
测试的数据表创建不正确，也可以说是migrate不正确。

apps.的模型没有创建，原因是：模型的managed 设为了false。会在所有db创建所有的表，这些表是包括自带的auth和djcelery这些install_app

apps.的模型没有创建，如何解决： 如何测试的时候创建managed为False的表，在测试启动时（DiscoverRunner）重写建立环境的方法

- https://dev.to/patrnk/testing-against-unmanaged-models-in-django

会在所有db创建所有的表，原因多数据路由的配置不正确。

我们之前的数据库路由没有重写allow_migrate方法(定义迁移操作是否允许在别名为db的数据库上运行)：

- http://python.usyiyi.cn/documents/django_182/topics/db/multi-db.html#allow_migrate

```
def allow_migrate(self, db, app_label, model_name=None, **hints):
    print(db, app_label, model_name, hints)
    if app_label == 'auth' and model_name == 'user':
        return False
    if hasattr(hints.get('model', None), 'connection_name'):
        db_name = hints.get('model', None).connection_name
    else:
        db_name = 'default'
    print(db_name)
    return db == db_name
```

其中遇到一个问题：
apps.auth2.AuthUserBaseinfo 表需要跟user表建立OneToOneField(settings.AUTH_USER_MODEL,

则报错，原因应该是自身的apps的模型先创建，原生的user模型还没创建。

但是ForeignKey(settings.AUTH_USER_MODEL 则没有问题。临时的解决办法就是在allow_migrate把原生的user表不创建。

```
if app_label == 'auth' and model_name == 'user':
    return False
```
还需研究路由的apps顺序

multi_db 为每个数据库创建不同的事务，否则的话，另一个库的数据不会回滚成功


```


class TRTestCase(TestCase):
    # multi_db = True

    def setUp(self):
        self.company_name = '有米科技'
        self.created_at = datetime.now()

        # 新建一个企业
        col = AuthUserCollection.objects.create(
            name=self.company_name,
            account_num=10,
            area='广州',
            created_at=self.created_at
        )
        Keywords.objects.create(keyword='tttttttttttttt', createdat='2018-06-01')

        # AdFormat.objects.create(adid=999999, format=999999)

```
Keywords 的数据会保留， multi_db = True 则不会

但是：

> The multi_db flag also affects into which databases the TransactionTestCase.fixtures are loaded. By default (when multi_db=False), fixtures are only loaded into the default database. If multi_db=True, fixtures are loaded into all databases.
