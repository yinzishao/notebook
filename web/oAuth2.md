第一步：引导用户到授权服务器

第二步：用户同意为第三方客户端授权

第三步：使用授权码向授权服务器申请令牌

第四步：向资源服务器申请资源

第五步：令牌延期
# refresh_token

你肯定对第四步返回的refresh_token比较好奇。

它是用来对令牌进行延期（刷新）的。为什么会有两种说法呢，因为可能授权服务器会重新生成一个令牌，也有可能对过期的令牌进行延期。

比如说，QQ互联平台为了安全性考虑，返回的access_token是有**时间限制**的，假如用户某天不想授权了呢，总不能给了个access_token你几年后还能用吧。我们上面模拟返回的令牌有效期为10小时。10小时后，用户打开浏览器逛简书，浏览器中用户的token对应的cookie已过期。简书发现浏览器没有携带token信息过来，就明白token失效了，需要**重新向认证平台申请授权**。如果让用户再点击QQ进行登录授权，这明显用户体验不好。咋搞呢？refresh_token就派上了用场，可以直接跳过前面申请授权码的步骤，当发现token失效了，简书从浏览器携带的cookie中的sessionid找到存储在数据库中的refresh_token，然后再使用refresh_token进行token续期（刷新）。


- [OAuth2.0 知多少 ](https://www.cnblogs.com/sheng-jie/p/6564520.html#autoid-2-0-0)


----
“能拿到access_token，拿到refresh_token就是轻而易举的事”这是不对的。因为access token随时都要用，这个token会伴随每次请求，相反refresh token只需要存储而不需要传输，所以获取refresh token的难度比获取access token的难度要高。

- [JWT为什么要设置2个token?](https://www.zhihu.com/question/316165120/answer/1185038196)
