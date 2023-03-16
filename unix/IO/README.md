- [名词解释](./express_word.md)
- [文件IO](./file_IO.md)

### 系统函数

一般情况，如果返回值是数值型，-1 总是代表异常情况

### 关于IO

对操作系统来说，IO的方向是多样的，以读为例：

- cache
- terminal
- network
- disk
- pipleline
- file

同样的，我们可以发现，输出介质好像上面这个也是都可以的，所以在unix系统中，当函数持有fd,便可以做很多的操作，继续以读为例，我们可以需要这样的功能：

- read only

- read lock

  