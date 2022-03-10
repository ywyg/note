五种IO模型：

* 阻塞IO

  > 调用recvfrom，阻塞等待数据返回

* 非阻塞IO

  > 调用recvfrom，每次调用都会有返回，没有数据返回EWOULDBLOCK的错误

* IO复用

  > （轮训）系统提供select/poll，进程将多个fd传递给select/poll，阻塞在select操作上，由select检测fd是否就绪）
  >
  > （回调）epoll支持回调，当有fd就绪时，立即执行rollback方法

* 信号驱动IO

  > 执行sigaction信号函数，然后系统正常工作，当fd就绪时，信号回调，通知主函数处理recvfrom数据

* 异步IO

  > 异步IO流程和信号驱动IO相似，不同之处在于，信号驱动IO回调的时候意味着我们可以处理recvfrom的数据了，异步IO回调的时候意味着数据已经从内核空间复制到了用户空间