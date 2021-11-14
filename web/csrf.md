参考链接:

- [什么是跨域请求以及实现跨域的方案](https://www.jianshu.com/p/f880878c1398)
- [详解js跨域问题](https://segmentfault.com/a/1190000000718840)

# 跨域请求

在 HTML 中，`<a>, <form>, <img>, <script>, <iframe>, <link>` 等标签以及 Ajax 都可以指向一个资源地址，而所谓的跨域请求就是指：**当前发起请求的域与该请求指向的资源所在的域不一样**。这里的域指的是这样的一个概念：我们认为若**协议 + 域名 + 端口号**均相同，那么就是同域。

## 同源策略(Same-origin Policy)

### 概述
- 同源策略是 Netscape 提出的一个著名的安全策略
- 同源策略是浏览器最核心最基础的安全策略
- 现在所有的可支持 Javascript 的浏览器都会使用这个策略
- web构建在同源策略基础之上，浏览器对非同源脚本的限制措施是对同源策略的具体实现

### 同源策略的含义
- DOM 层面的同源策略：限制了来自不同源的”Document”对象或 JS 脚本，对当前“document”**对象的读取或设置某些属性**
- Cookie和XMLHttprequest层面的同源策略：禁止 Ajax 直接发起跨域HTTP请求（其实可以发送请求，**结果被浏览器拦截**，不展示），同时 Ajax 请求不能携带与本网站不同源的 Cookie。
- **同源策略的非绝对性**：`<script><img><iframe><link><video><audio>`等带有src属性的标签可以从不同的域加载和执行资源。
- 其他插件的同源策略：flash、java applet、silverlight、googlegears等浏览器加载的第三方插件也有各自的同源策略，只是这些同源策略不属于浏览器原生的同源策略，如果有漏洞则可能被黑客利用，从而留下XSS攻击的后患

### 同源的具体含义
域名、协议、端口有一个不同就不是同源，三者均相同，这两个网站才是同源

## JSONP的优缺点

JSONP 本质上是利用 `<script><img><iframe> `等标签不受同源策略限制，可以从不同域加载并执行资源的特性，来实现数据跨域传输。

JSONP的优点是：
- 它不像XMLHttpRequest对象实现的Ajax请求那样受到同源策略的限制；
- 它的兼容性更好，在更加古老的浏览器中都可以运行，不需要XMLHttpRequest或ActiveX的支持；
- 并且在请求完毕后可以通过调用callback的方式回传结果。

JSONP的缺点则是：
- 它只支持GET请求而**不支持POST**等其它类型的HTTP请求；
- 它只支持跨域HTTP请求这种情况，不能解决不同域的两个页面之间如何进行JavaScript调用的问题。

> jsonp虽然是可以访问外域，但是请求默认不发送cookie信息，如果需要cookie，需要手动指定。标准的CORS请求不对cookies做任何事情，既不发送也不改变。如果希望改变这一情况，就需要将withCredentials设置为true。

## CORS

跨源资源共享 Cross-Origin Resource Sharing(CORS) 是一个新的 W3C 标准，它新增的一组HTTP首部字段，允许服务端其声明哪些源站有权限访问哪些资源。换言之，它允许浏览器向声明了 CORS 的跨域服务器，发出 XMLHttpReuest 请求，从而克服 Ajax 只能同源使用的限制。

另外，**规范也要求对于非简单请求，浏览器必须首先使用 OPTION 方法发起一个预检请求(preflight request)，从而获知服务端是否允许该跨域请求，在服务器确定允许后，才发起实际的HTTP请求**。对于简单请求、非简单请求以及预检请求的详细资料可以阅读HTTP访问控制（CORS） 。

### HTTP 协议 Header 简析
下面对 CORS 中新增的 HTTP 首部字段进行简析：

#### Access-Control-Allow-Origin

响应首部中可以携带这个头部表示服务器允许哪些域可以访问该资源，其语法如下：

`Access-Control-Allow-Origin: <origin> | *`

其中，origin 参数的值指定了**允许访问该资源的外域 URI**。对于不需要携带身份凭证的请求，服务器可以指定该字段的值为通配符，表示允许来自所有域的请求。

#### Access-Control-Allow-Methods

该首部字段用于预检请求的响应，指明实际请求所允许使用的HTTP方法。其语法如下：

```
Access-Control-Allow-Methods: <method>[, <method>]*
```
#### Access-Control-Allow-Headers

该首部字段用于预检请求的响应。指明了实际请求中允许携带的首部字段。其语法如下：

```
Access-Control-Allow-Headers: <field-name>[, <field-name>]*
```

#### Access-Control-Max-Age

该首部字段用于预检请求的响应，指定了预检请求能够被缓存多久，其语法如下：

```
Access-Control-Max-Age: <delta-seconds>
```

#### Access-Control-Allow-Credentials

该字段可选。它的值是一个布尔值，**表示是否允许发送Cookie**。默认情况下，Cookie不包括在CORS请求之中。设为true，即表示服务器明确许可，Cookie可以包含在请求中，一起发给服务器。其语法如下：

`Access-Control-Allow-Credentials: true`

另外，如果要把 Cookie 发送到服务器，**除了服务端要带上Access-Control-Allow-Credentials首部字段外，另一方面请求中也要带上withCredentials属性**。

但是需要注意的是：如果需要在 Ajax 中设置和获取 Cookie，那么Access-Control-Allow-Origin首部字段不能设置为* ，必须设置为具体的 origin 源站。

## CORS和JSONP对比

CORS与JSONP相比，无疑更为先进、方便和可靠。

1. JSONP只能实现GET请求，而CORS支持所有类型的HTTP请求。

2. 使用CORS，开发者可以使用普通的XMLHttpRequest发起请求和获得数据，比起JSONP有更好的错误处理。

3. JSONP主要被老的浏览器支持，它们往往不支持CORS，而绝大多数现代浏览器都已经支持了CORS。

## 跨域请求的安全问题
通常，浏览器会对上面提到的跨域请求作出限制。浏览器之所以要对**跨域请求作出限制**，是出于安全方面的考虑，因为跨域请求有可能被不法分子利用来发动 CSRF攻击。

### CSRF攻击
CSRF（Cross-site request forgery），中文名称：跨站请求伪造，也被称为：one click attack/session riding，缩写为：CSRF/XSRF。CSRF**攻击者在用户已经登录目标网站之后，诱使用户访问一个攻击页面，利用目标网站对用户的信任，以用户身份在攻击页面对目标网站发起伪造用户操作的请求，达到攻击目的**。

链接：
- [什么是跨域请求以及实现跨域的方案](https://www.jianshu.com/p/f880878c1398)

---
# 表单的跨域请求

- [表单可以跨域吗](https://github.com/frontend9/fe9-interview/issues/1)

浏览器就默认禁止了ajax跨域，服务端必须设置CORS才可以。

form表单确实是会带cookie的(?)，我认为的原因是, 同源策略主要是限制js行为,form表单提交的结果js是无法拿到,所以没有去限制.

当然不限制也是有漏洞了,csrf攻击就能利用form表单能带cookie的特点. 而**cookie的新属性SameSite**就能用来限制这种情况

> 表单的简单请求的cookie传递也是受同源策略配置限制。需要前后端都设置credentials，且后端设置指定的origin。

### 为什么form表单提交没有跨域问题，但ajax提交有跨域问题？

因为原页面用 form 提交到另一个域名之后，**原页面的脚本无法获取新页面中的内容**。所以浏览器认为这是安全的。而 AJAX 是可以读取响应内容的，因此浏览器不能允许你这样做。如果你细心的话你会发现，**其实请求已经发送出去了(?)**，你只是拿不到响应而已。所以浏览器这个策略的本质是，一个域名的 JS ，在未经允许的情况下，**不得读取另一个域名的内容**。但浏览器并不阻止你向另一个域名发送请求。

> form表单会刷新页面，不会把结果返回给js，所以相对安全。所以这里的表述有点问题。AJAX的跨域请求行为应该是收到同源策略的配置影响？

- [跨域](https://www.zhihu.com/question/31592553/answer/190789780)

---
# CORS

跨源资源共享 Cross-Origin Resource Sharing(CORS) 是一个新的 W3C 标准，它新增的一组HTTP首部字段，允许服务端其声明哪些源站有权限访问哪些资源。换言之，它允许浏览器向声明了 CORS 的跨域服务器，发出 XMLHttpReuest 请求，从而克服 Ajax 只能同源使用的限制。

某些请求不会触发 CORS 预检请求。**需预检的请求**”要求必须首先使用OPTIONS方法发起一个预检请求到服务器，以获知服务器是否允许该实际请求。"预检请求“的使用，可以避免跨域请求对服务器的用户数据产生未预期的影响。


## 简单请求
某些请求不会触发 CORS 预检请求。本文称这样的请求为“简单请求”，请注意，该术语并不属于 Fetch （其中定义了 CORS）规范。若请求满足所有下述条件，则该请求可视为“简单请求”：

使用下列方法之一：
- GET
- HEAD
- POST

除了被用户代理自动设置的首部字段（例如 Connection ，User-Agent）和在 Fetch 规范中定义为 禁用首部名称 的其他首部，允许人为设置的字段为 Fetch 规范定义的 对 CORS 安全的首部字段集合。该集合为：
- Accept
- Accept-Language
- Content-Language
- Content-Type （需要注意额外的限制）
- DPR
- Downlink
- Save-Data
- Viewport-Width
- Width

Content-Type 的值仅限于下列三者之一：
- text/plain
- multipart/form-data
- application/x-www-form-urlencoded

请求中的任意XMLHttpRequestUpload 对象均没有注册任何事件监听器；XMLHttpRequestUpload 对象可以使用 XMLHttpRequest.upload 属性访问。
请求中没有使用 ReadableStream 对象。

> 注意: 这些跨站点请求与浏览器发出的其他跨站点请求并无二致。如果服务器未返回正确的响应首部，则请求方不会收到任何数据。因此，那些不允许跨站点请求的网站无需为这一新的 HTTP 访问控制特性担心。

- [简单请求](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS)

> 注意post表单的简单请求，会有跨域攻击的风险。而且配置允许cookie

```
var invocation = new XMLHttpRequest();
var url = 'http://bar.other/resources/credentialed-content/';

function callOtherDomain(){
  if(invocation) {
    invocation.open('GET', url, true);
    invocation.withCredentials = true;
    invocation.onreadystatechange = handler;
    invocation.send();
  }
}
```

第 7 行将 XMLHttpRequest 的 withCredentials 标志设置为 true，从而向服务器发送 Cookies。**因为这是一个简单 GET 请求，所以浏览器不会对其发起“预检请求”**。但是，如果服务器端的响应中**未携带**` Access-Control-Allow-Credentials: true `，浏览器**将不会把响应内容返回给请求的发送者**。

> 小结一下： 对于简单请求，在前端GET请求主动带上withCredentials（指的是ajax请求？），携带cookie。，因为不会发起预检请求，而请求是能发送给服务端的，但是，如果服务器端的响应中**未携带**` Access-Control-Allow-Credentials: true `，浏览器**将不会把响应内容返回给请求的发送者**。而post表单请求则受cookie的SameSite属性的影响。在csrf攻击情况下，SameSite是None的设置，才能成立。而且表单请求是application/json等非简单请求，则根据预检查option返回的内容限制。

---
# 跨域资源共享 CORS 详解
> - [跨域资源共享 CORS 详解-阮一峰](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)

对于简单请求，浏览器直接发出CORS请求。具体来说，就是在头信息之中，增加一个Origin字段。

下面是一个例子，浏览器发现这次跨源AJAX请求是简单请求，就自动在头信息之中，添加一个Origin字段

上面的头信息中，Origin字段用来说明，本次请求来自哪个源（协议 + 域名 + 端口）。服务器根据这个值，决定是否同意这次请求。

如果Origin指定的源，不在许可范围内，服务器会返回一个正常的HTTP回应。浏览器发现，这个回应的头信息没有包含Access-Control-Allow-Origin字段（详见下文），就知道出错了，从而抛出一个错误，被XMLHttpRequest的onerror回调函数捕获。注意，这种错误无法通过状态码识别，因为HTTP回应的状态码有可能是200。

---

# 如何防止跨域请求

- [安全](./安全.md#CSRF)

---

# django的csrf源码

_salt_cipher_secret、_unsalt_cipher_token
```
1. Cipher = (Secret + Salt) mod N  return: Salt + Cipher =》 csrfmiddlewaretoken
2. (Cipher - Salt) mod N 会等于 Secret 所以： csrfmiddlewaretoken：能解码得到secret
```
疑问：这个算法有什么用。都能推出来的(知道一个token就能反推另一个了)。也没有私钥的加密。还不如直接用同一个值。前提都是建立在：csrftoken是黑客拿不到的。

A: 下面也讨论到了，这里只是为了增加csrfmiddlewaretoken的随机性而已？并且能跟csrftoken的secret进行比较，也避免了有状态。csrftoken跟随着登录的session。

- [算法例子](https://www.jianshu.com/p/eaf4a57bbca7)

如果`request.META["CRSF_COOKIE"]`不存在，就调用`_get_new_csrf_string()`函数来生成一串随机字符（32个字符，大小写字母和数字），赋给csrf_secret，再调用`_salt_cipher_secret(scrf_secret)`和随机生成的32位salt一起生成64个字符的字符串赋给`request.META[“CSRF_COOKIE”]`，而这个`request.META["CSRF_COOKIE"]`之后用来设置COOKIE 的csrf_token。

最后的返回值_salt_cipher_secret(csrf_secret)就渲染到POST表单的csrfmiddlewaretoken。值得一提的是_salt_cipher_secret(csrf_secret)每次的返回值都不一样，而csrf_secret == _unsalt_cipher_token(_salt_cipher_secret(csrf_secret))。

总的来说，涉及到三个值，csrf_token、csrfmiddlewaretoken和csrf_secret，还有两个函数，_unsalt_cipher_token(token)和_salt_cipher_secret(token)。

- [Django中CSRF防御全过程解析以及中间件作用机制](https://blog.csdn.net/Deft_MKJing/article/details/90348835)

---
## 工作原理
> - [它是如何工作的](https://yiyibooks.cn/xx/Django_1.11.6/ref/csrf.html)

跨站伪造保护基于以下几点：

- 1.一个基于随机secret值的CSRF cookie，其它站点无法获取到。

此Cookie由CsrfViewMiddleware设置。 它和每个响应一起发送，如果请求上没有设置，则调用django.middleware.csrf.get_token()（这个函数用于内部获取CSRF token）。

为了**防止BREACH攻击**，token不仅仅是secret；**一个随机的salt**被添加到secret中，并用来加扰它。


出于安全考虑，**每当用户登录时，secret的值都会更改**。

> csrf token基于一个随机生成的秘钥secret，并通过salt hash方式加密生成csrftoken，插入到Cookie中。该csrftoken在用户登录阶段生成，在session结束前保持不变。


- 2.所有传出POST表单中都有一个名为“csrfmiddlewaretoken”的隐藏表单字段。

 该字段的值还是这个secret的值，其中添加了salt并且用于加扰它。 在每次调用get_token()时重新生成salt，所以在每个响应中这个表单字段值都会改变。

> 每一个响应的POST表单中，都会插入一个隐藏的csrfmiddlewaretoken字段。该字段的值也是对1中的secret进行salt hash，每次请求表单页面都会使用一个随机的salt，所以每次响应中表单里面插入的csrfmiddlewaretoken都是不一样的。


3.对于所有未使用HTTP GET，HEAD，OPTIONS或TRACE的传入请求，必须存在CSRF cookie，并且“csrfmiddlewaretoken”字段必须存在且正确。 如果不是，用户将得到403错误。

  当验证'csrfmiddlewaretoken'字段值时，只将secret而不是完整的token与cookie值中的secret进行比较。 **这允许使用不断变化的token。 虽然每个请求可能使用自己的token，但是secret对所有人来说都是相同的。**

此检查由CsrfViewMiddleware完成。

> 小结一下： 一个随机生成的秘钥secret，并通过salt hash方式加密生成csrftoken。登录后放到cookie里面，后面的前提都是该cookie的token无法被其他窃取到。每一个响应的POST表单中，都会插入一个隐藏的csrfmiddlewaretoken字段。该字段的值也是对1中的secret进行salt hash，每次请求表单页面都会使用一个随机的salt，所以每次响应中表单里面插入的csrfmiddlewaretoken都是不一样的。而解码过程是把csrfmiddlewaretoken的secret的解出来，跟cookie的csrftoken解出来的secret比较。其实跟最简单的防御，cookie放到表单是一样的过程。只是表单的token能一直变化而已。

## 问题

Q: 如何避免重放攻击？

> 好像无法避免？token好像在登录状态下是可以无限用。只要泄露一个form的token就可以一直用，直到登录刷新cookie的secret key。怎么样才会泄露呢？

> 需要自己用一层session的操作？

[相关的讨论](https://stackoverflow.com/a/25527231)

原因：Multiple browser windows / tabs and REST。防止多个浏览器/tab的时候，造成token的拒绝服务。或者存储的过载和复杂性，因为要维护状态。

- 里面说的如何避免中间人攻击是什么意思？referer


Q： 前后端分离后，怎么避免csrf攻击？可以提交表单，但是无法获取内容？所以要有确认操作？因为上面的避免操作都是因为post的表单要带上token。是后端渲染表单的时候带上的。前后端分离后怎么操作？

1. 表单的获取cookie的token，作为表单的字段提交进行校验。

2. API接口JWT方式的Token认证？跨域的时候，JWT 就放在 POST 请求的数据体里面。[阮一峰](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)

> 引出的问题JWT: 客户端收到服务器返回的 JWT，可以储存在 Cookie 里面，也可以储存在 localStorage。此后，客户端每次与服务器通信，都要带上这个 JWT。你可以把它放在 Cookie 里面自动发送，但是**这样不能跨域**(这里的跨域应该是指token生成后，作为另一个域名的请求密钥)，所以更好的做法是放在 HTTP 请求的头信息Authorization字段里面。

攻击者只能通过csrf方式冒用真实用户的身份发送请求，这是浏览器的一种工作机制，攻击者并不能直接获取jwt信息，即使把jwt放入cookie，因为域的限制，攻击者也无法读取到jwt。但是如果攻击者通过监听、抓包等方式获取到用户的jwt之后就能以用户的身份作任何允许的操作，所以一定要使用https

总结： JWT的token不应该是放在cookie里面，因为这样子前后端分离的csrf的跨域表单攻击就能实现。除非你post请求把cookie的值放在请求体。而把jwt的token**放在header其实就是能避免表单这个攻击**。因为**跨域的网站无法获取到jwt的token并放在header的操作**。前端的工作分两方面，一是存储 jwt，二是在所有的请求头中增加 Authoriaztion 。从头至尾，整个过程没有涉及 cookie，所以 CSRF 是不可能发生的。

- [如何通过JWT防御CSRF](https://segmentfault.com/a/1190000003716037)
- [JSON Web Token 入门教程](http://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)

---

Q： breach攻击是啥?为什么可以防止breach攻击?

http://www.doc88.com/p-9139615174722.html


## 常见问题
### 发布一个任意的CSRF令牌对（cookie和POST数据）一个漏洞？

不，这是设计。 没有中间人的攻击，攻击者无法向受害者的浏览器发送CSRF令牌cookie，所以**成功的攻击需要通过XSS或类似的方式获取受害者的浏览器的cookie**，在这种情况下攻击者通常不需要CSRF攻击。

一些安全审核工具将此标记为问题，但如前所述，攻击者无法窃取用户浏览器的CSRF cookie。 使用Firebug、Chrome等开发工具等“窃取”或修改你自己的token 不是一个漏洞。

> 问题的意思应该是，可以伪造发布任意的一对令牌。是不是漏洞？回答就是无法向受害者的浏览器发送CSRF令牌cookie。就算你伪造了，post请求还需要用户的cookie，那你就只能通过xss漏洞获取到了。

> csrf的表单攻击形式只能说你请求表单的内容伪造了，但是你是无法进行cookie的设置。或者你也无法获取到cookie的csrftoken，然后进行伪造csrfmiddlewaretoken。


- [美团前端安全系列（二）：如何防止CSRF攻击？](https://www.freebuf.com/articles/web/186880.html)

----

# 本地项目测试

因为jwt存在cookie上，所以表单提交存在跨域的危险。
```html
<form action="http://172.16.8.4:8890/api/favorites/keywords/cancel" method="POST">
    <input type="text" id="keyword" name="keyword">
    <button type="submit" class="btn btn-primary">Login</button>
</form>

```
请求是带着cookie过来了。不过还好约定的内容是application/json，改成json就不是简单请求了，会有跨域问题。所以存在风险，但还没造成影响。

但一不小心支持表单的类型，伪造一个钓鱼网站，诱导AE点击一下，把我提交到某个企业里面。所以还是把风险关闭才行。改成header获取提交把token带上。


- [谈谈Json格式下的CSRF攻击](https://www.freebuf.com/articles/web/206407.html): 这种flash+307跳转攻击方法只能在旧版浏览器适用，在2018年后更新版本的几乎所有浏览器，307跳转的时候并没有把Content-Type传过去而导致csrf攻击失败。所以还望寻找一种新的攻击方法，本文的json csrf攻击方法仅仅是作为一种记录，在某些情况下还是能用到的。

---
# 参考链接

- [跨域资源共享 CORS 详解-阮一峰](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)
- [深度介绍：也许你对 Fetch 了解得不是那么多](https://segmentfault.com/a/1190000017742993), [Fetch API 教程](https://www.ruanyifeng.com/blog/2020/12/fetch-tutorial.html): fetch与cookie联系
- [浏览器系列之 Cookie 和 SameSite 属性 ](https://github.com/mqyqingfeng/Blog/issues/157): 阿里对SameSite的影响分析和研究。
