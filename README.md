| [JAVA](./java/README.md)       | [Spring](./Spring/README.md)   | [MySQL](./MySQL/README.md) |
| ------------------------------ | ------------------------------ | -------------------------- |
| [OS](./Unix/README.md)         | [NoSQL](./NoSQL/README.md)     | 云原生                     |
| [大数据](./big_data/README.md) | [RPC](./rpc/README.md)         | Muliti_Language            |
| Unity                          | [network](./network/README.md) | MQ                         |

## 什么是开发

所有的软件系统，目前都没有脱离冯诺依曼体系，都是由输入输出设备，存储设备，计算设备组成

不同的语言只是一层层的包装，他们能提供的功能只能是系统内核已经提供的，同样是一堆积木，有的人把他拼成了飞机，有的把他拼成了房子，语言也是这样

不同的中间件只是一种数据的组织方式，就像队列适合先进先出，栈属于后进先出这样，redis他就是把自己的数据结构维护成了容易存储的样子，因为满足了容易存储这个条件，所以就很难在满足随意删选这个功能，又比如elasticsearch，他把数据维护成了倒排索引的方式，确实满足了对文档内容的快速检索，但是又失去了插入时的便捷性，所以一个成功的中间件并不是要做的大而全，因为这是不可能的，做好自己擅长的那部分就可以，也正是因为上面的这个原因，我们有必要使用消息队列，因为我们需要把数据组织成不同的方式，而一个适合的消息队列可以让所有的组织方式都能获取到原始的数据，

软件的发展好像就是在追求更快的存取
所以我们就有了各种非关系型数据库，各种大数据搜索引擎，各种分布式中间件

同时软件的发展也在追求简单，追求开发简单，维护简单
因为追求开发简单，所以我们有了springboot,有了netty,有了spring-cloud
因为追求维护简单，所以我们有了容器化，有了ci/cd，有了各种服务编排工具

计算机的发展不就是这样吗？

好的，现在我们有了很多的语言，有了很多的存储方式，有了自动化工具，然后就发展出了下一个问题

上面提到这些东西是不是都会过时，都会故障
答案是肯定的

语言肯定会过时，这是毫无疑问的，肯定会向着对人越来越友好的方向发展，以后肯定不需要考虑npe问题了，但是语言的本质是什么？
我们上面提到了，是积木，是内核提供的方法，是可以调用寄存器，调用cpu，调用硬盘的命令集合，理解到了这里是不是应该对语言有一些别的认知呢？

然后我们再说各种存储，不管是哪种存储方式，都会有两个问题

1. 存不下了， 我觉得存不下应该有两种理解，一种是满了，一种是存储与查询相比的性价比太低了，如果1s存储，10s才能读出来，我认为这可以称之为存不小了

2. 数据丢了， 存储引擎，存了数据然后数据丢了，我觉得是一件很正常的事情，这也是体现维护人员重要性的一点，多做备份嘛，丢了一个还有二个，我会怕丢？

但是在各种中间件层次，开发者肯定也想到了这个问题，所以才会分布式，主从，分片等等结构的数据，都是为了处理上面的两个问题

今天北京的雨好大，很美

我这个水平目前也只能想到这里了，2022/9/3 于冠庭园出租小屋