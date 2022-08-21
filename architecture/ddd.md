# 领域驱动设计(DDD)编码实践
> - [后端开发实践系列——领域驱动设计(DDD)编码实践 - Thoughtworks洞见](https://insights.thoughtworks.cn/backend-development-ddd/)

ApplicationService需要遵循以下原则：

*   业务方法与业务用例一一对应：前面已经讲到，不再赘述。
*   业务方法与事务一一对应：也即每一个业务方法均构成了独立的事务边界，在本例中，`OrderApplicationService.changeProductCount()`方法标记有Spring的`@Transactional`注解，表示整个方法被封装到了一个事务中。
*   本身不应该包含业务逻辑：业务逻辑应该放在领域模型中实现，更准确的说是放在聚合根中实现，在本例中，`order.changeProductCount()`方法才是真正实现业务逻辑的地方，而ApplicationService只是作为代理调用`order.changeProductCount()`方法，因此，ApplicationService应该是很薄的一层。
*   与UI或通信协议无关：ApplicationService的定位并不是整个软件系统的门面，而是领域模型的门面，这意味着ApplicationService不应该处理诸如UI交互或者通信协议之类的技术细节。在本例中，Controller作为ApplicationService的调用者负责处理通信协议(HTTP)以及与客户端的直接交互。这种处理方式使得ApplicationService具有普适性，也即无论最终的调用方是HTTP的客户端，还是RPC的客户端，甚至一个Main函数，最终都统一通过ApplicationService才能访问到领域模型。
*   接受原始数据类型：ApplicationService作为领域模型的调用方，领域模型的实现细节对其来说应该是个黑盒子，因此ApplicationService不应该引用领域模型中的对象。此外，ApplicationService接受的请求对象中的数据仅仅用于描述本次业务请求本身，在能够满足业务需求的条件下应该尽量的简单。因此，ApplicationService通常处理一些比较原始的数据类型。在本例中，`OrderApplicationService`所接受的Order ID是Java原始的String类型，在调用领域模型中的Repository时，才被封装为`OrderId`对象。


## 聚合根的家——资源库

通俗点讲，资源库(Repository)就是用来持久化聚合根的。从技术上讲，Repository和DAO所扮演的角色相似，不过DAO的设计初衷只是对数据库的一层很薄的封装，而Repository是更偏向于领域模型。另外，在所有的领域对象中，只有聚合根才“配得上”拥有Repository，而DAO没有这种约束。


