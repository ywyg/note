## 程序顺序执行的特征

- 顺序性

  > 处理机需要严格按照程序规定的顺序进行

- 封闭性

  > 程序运行时独占全机资源，

- 可再现性

  > 只要是在相同的环境和资源下，每次执行得到的结果都应该是相同的

并发执行的程序可能会影响封闭性和可再现性，并且只有没有依赖关系的程序才可以并发执行

## 进程与程序

进程是程序的一次执行

进程是一个程序及其数据在处理机上顺序执行时所发生的活动

进程时具有独立功能的程序在一个数据集合上运行的过程，他是系统进行资源分配和调度的基本单位



程序是代码，是指令集合



## 进程

### 进程状态（基本）

- 就绪

  > 已经分配到除CPU外的所有资源，进入就绪队列，就绪队列内任务进程只要获取CPU就可以执行

- 执行

  > 已经获取CPU，正在执行的状态

- 阻塞

  > 正在执行的程序，由于发生啦类似于I/O请求、申请缓冲失败这样的事件，无法继续执行时的状态，此时引起进程调度，OS会把处理机分配给其他就绪态进程，当前进程进入阻塞队列，一般会根据不同的阻塞原因进入不同的阻塞队列

  <img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230304142934185.png" alt="image-20230304142934185" style="zoom:50%;" />

​									  									图      pcf-01

### 进程状态（补充）

- 创建

  > 创建状态的引入是为了保证进程调度必须在进程创建工作完成之后，保证进程控制的完整性
  >
  > 流程：
  >
  > - 申请空白PCB
  > - 填写PCB
  > - 进程运行资源分配
  > - 进程转为就绪态
  > - 插入创建进程到就绪列表

- 终止

  > 当一个进程到达自然结束点，抑或是无法处理的错误，或被其他进程所终止，都会进入终止状态。
  >
  > 进入终止状态的程序不能再被执行，但在OS中仍保留记录，保存`状态吗`和一些`计时信息`以供其他进程分析，一旦其他进程完成了这个信息的收集，OS将删除该进程：
  >
  > - PCB清零
  > - PCB返回OS

  <img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230304144012202.png" alt="image-20230304144012202" style="zoom:50%;" />

​									  									图      pcf-02

### 进程状态（额外）

- 挂起

  > 为了系统和用户观察和分析需要，引入挂起状态，当挂起作用于执行状态进程时，该进程将被挂起，处于静止状态，当挂起作用于就绪状态，该进程暂不接受调度，与之对应的激活操作

- 激活

  > 激活处于挂起状态的线程

抛开额外的两个状态，进程共包含5种状态，这5种进程状态之间的切换我们从`图pcf-02`可以清楚的看到，增加额外两种状态后进程状态增加如下几种：

- 静态就绪
- 活动就绪
- 静态阻塞
- 活动阻塞

其中静态意味着被挂起，活动就是`图pcd-02`5种状态，静态 -> 活动 需要激活，我们可以在除阻塞和终止之外的任何状态选择挂起线程，均会进入静态就绪，静态阻塞线程阻塞条件得到后也会进入静态就绪。

可以这样理解，挂起操作是一把锁，进程运行时必须得到这个锁，其他的状态切换可以不获得这个锁，所以挂起不影响其他状态切换，只会影响运行状态。


