# JWT

## 第一部分 JWT Header
它是一个 JSON 对象，表示这个整个字符串的类型和加密算法，比如

{
  "typ":"JWT",
  "alg":"HS256"
}
经过 base64url 加密之后变成

eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9


## 第二部分 JWT Claims Set
它也是一个 JSON 对象，能唯一表示一个用户，比如

{
  "iss": "123",
  "exp": 1441593850
}
经过 base64url 加密之后变成

eyJpc3MiOiIxMjMiLCJleHAiOjE0NDE1OTM4NTB9

## 第三部分 JWS Signature
这个签名的计算跟第一部分中的 alg 属性有关，假如是 HS256，那么服务端需要保存一个私钥，比如 secret 。然后，把第一部分和第二部分生成的两个字符串用 点 连接之后，再结合私钥，用 **HS256 加密**可以得到如下字符串

AOtbon6CebgO4WO9iJ4r6ASUl1pACYUetSIww-GQ72w
现在就集齐三个部分了，用 . 连接，得到完整的 token 。


---
# 对比

> - [讲真，别再使用JWT了！](https://juejin.im/entry/5993a030f265da24941202c2)


## 优势

1.无状态，该方案更易于水平扩展。

服务端水平扩展的时候，就不用处理session复制（session replication）/ session黏连（sticky session）或是引入外部session存储了。

2.该方案可防护CSRF攻击

作者观点： 如果放在Local Storage，则可能受到XSS攻击。
> xss攻击存在放在哪里都是有问题。

在向服务端发起请求时，用Javascript取出JWT。

[csrf参考#问题](./csrf.md)

3.跨域??

4.移动端：对于无法使用 cookie 的一些移动端，JWT 能够正常使用


## 劣势

无状态带来的好与不好

1. 无法作废已颁布的令牌

2. 不易应对数据过期

作者认为适合的场景是：一次性的场景。例如，票据一般都是“一次性”使用的，在访问到对应的资源后，该票据一般会被资源持有方收回留底，用于后续的审计、追溯等用途。为什么作为请假单的时候你的jwt可以“收回”但作为session的时候就不行？颁布一个**很短过期时间**的JWT给浏览器。

---

# 讨论
1、安全性问题，不使用https，其他认证方式也存在文章说的问题；应该是xss，不是https的问题。

2、jwt主动过期问题，完全可以实现，使用黑名单即可；分成两点，客户端要求失效，服务端记录token到黑名单；用户重置密码，服务端记录**uid-time**键值对，在此之前的token全部失效；

3、jwt续签问题，一种解决方式是jwt中存储过期时间，服务端设置刷新时间，请求是判断是否在过期时间或刷新时间，在刷新时间内进行token刷新，失效token记入黑名单；而黑名单过大问题，可以采用记录UID-刷新时间方式解决，判断jwt签发时间，jwt签发时间小于UID-刷新时间的记为失效。

"不过，把jwt变成有状态替代session确实没啥必要。"


续签问题：完善 refreshToken，借鉴 oauth2 的设计，返回给客户端一个 refreshToken，允许客户端主动刷新 jwt。一般而言，jwt 的过期时间可以设置为数小时，而 refreshToken 的过期时间设置为数天。我认为该方案并可行性是存在的，但是为了解决 jwt 的续签把整个流程改变了，为什么不考虑下 oauth2 的 password 模式和 client 模式呢？

- [理解JWT的使用场景和优劣](http://blog.didispace.com/learn-how-to-use-jwt-xjf/)
- [如何通过JWT防御CSRF](https://segmentfault.com/a/1190000003716037)

---

# 项目使用

之前使用jwt，是放在header的

- 第一可扩展，无状态
- 第二是方便跨域(?)，并且能防止跨域攻击
- 第三就是保存一些基本信息在这里，给前端进行使用。
- 第四就是前后端分离后，对后续的微信开发可以更兼容、友好

但因为还需要进行单点登录的限制，所以我们还是将jwt进行有状态，存了session在mysql上（待迁移redis），每次校验需要进行当前session的校验，也就没有上面所说的过期与黑名单问题。其实上面的uid-time键值对这个思路也是差不多，不过提供了另一个思路。

没有续签问题，过期一个月。

但是因为重新放在cookie上了，会有跨域攻击的风险。见[csrf](./csrf.md)
