## Netty核心组件

> netty是完全异步的和事件驱动的

### Channel（网络操作抽象类）

> 一个到实体的连接，比如读写操作的数据载体，可以被打开或者关闭

### 回调

> 操作结束后通知操作调用方

### ChannelFuture（操作执行结果）

> 异步操作结果的占位符，提供对异步完成的结果的访问，如果子啊ChannelFutureListener被添加到ChannelFuture时，ChannelFuture已经完成则会立即返回

### ChannelHandler（消息处理器）

> ChannelHandler 是专为支持广泛的用途而设计的，可以将它看作是处理往来 Channel-
>
> Pipeline 事件(包括数据)的任何代码的通用容器

### <font color="red">ChannelPipeline（ChannelHandler对象链表）</font>

> netty使用<font color="red">不同的事件</font>来通知我们状态的改变或者是操作的状态，让我们可以基于事件触发适当的动作

​											事件被事件处理链处理

![image-20211201102846074](https://tva1.sinaimg.cn/large/008i3skNly1gwy4inc2o7j31660cedh5.jpg)

### 选择器

### EventLoop（事件循环）

> netty为每个Channel分配一个EventLoop用以处理所有的事件
>
> 1. 一个EventLoopGroup 包含一个或多个EventLoop
> 2. 一个EventLoop在他的生命周期内只有一个Thread绑定
> 3. 所有的EventLoop处理的I/O事件都在他的专有Thread上处理
> 4. 一个Channel在它的生命周期只注册一个EventLoop
> 5. 一个EventLoop可能会被分配给多个Channl

“一个Channel对应一个线程，不会出现顺序错乱”





### Bytebuf（字节容器）

### Bootstrap/ServerBootstrap（启动引导类）

### 

### 

### 

### 















