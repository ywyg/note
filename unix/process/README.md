- [名词解释](./express_word.md)
- [PCB](./pcb.md)
- [进程的基本概念](./process_conceptual_framework.md)
- [进程的状态切换](./create_process.md)
- [进程同步](./process_synchronization.md)

每个进程都有一个工作目录（当前目录），所有的相对路径都是从工作目录开始解释

OS对进程的管理是通过建立和维护各种数据结构来完成的，其实也不止是对进程的管理，OS对系统内所有的东西管理都是这样的，例如`IpTable`,`PCB`等等

对进程而言：PCB就是其中的关键