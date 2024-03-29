### IO操作常用函数

- open

  > 调用函数open可以打开或者创建一个文件
  >
  > ```c
  > #include <fcntl.h>
  > 
  > int open(char *path,int flag,.... );
  > int openat(int fd,char *path,int flag,....);
  > ```
  >
  > flag参数支持多种选项，例如`O_RDONLY`、`O_RDWR`、`O_CREAT`等，并且可以使用`或`运算构成新的参数，例如`O_RDONLY|O_CREAT` 表示文件不存在时创建并以只读形式打开

- create

  > 创建一个文件
  >
  > ```c
  > #Include <fcntl.h>
  > int create(char *path，mode_t mode);
  > ```
  >
  > mode - 创建文件时选择的格式
  >
  > create 创建的文件默认是以只写的形式创建的

- read

  > 从打开的文件中读取数据
  >
  > ```c
  > ssize_t read(int fd, void *buf, size_t nbytes);
  > ```
  >
  > 如果read成功，则返回读到的字节数，到达文件尾端时返回0 ，返回-1代表出错
  >
  > - 读普通文件时，在读到要求的字节数之前达到了尾端，返回实际字节数
  > - 从终端读取时，通常一次读取最多一行
  > - 网络读时，由于网络缓冲机制可能造成返回值小于所要求读的字节数
  > - 管道读或者队列读，若是管道内字节小雨所要求的字节，返回实际读取字节数
  > - 

- write

  > 向打开的文件中写数据
  >
  > ```c
  > ssize_t write(int fd,const void * buf,size_t nbytes);
  > ```
  >
  > 如果写成功，返回已写字节数，若出错，返回-1
  >
  > 常见出错：
  >
  > - 磁盘已满
  > - 超过进程文件长度限制
  >
  > 对于普通文件，写操作从文件的当前偏移量开始，如果打开文件时指定了O_APPEND选项，则在每次写操作之前，将文件的偏移量设置在文件的当前结尾处，在每次写成功后，文件偏移量增加实际写的字节数。

- close

  > 关闭打开的文件
  >
  > ```c
  > #include <fcntl.h>
  > int close(int fd);
  > ```
  >
  > 
  >
  > 关闭文件会释放文件上的所有记录锁；进程结束时，内核自动关闭进程打开的所有文件

- lseek

  > 我们现在有两个文件，分别是`A.txt`和`B.txt`，其中A文件有如下内容
  >
  > > Hello Lseek
  >
  > B文件则是空白文件，显然这两个文件的内容不同，那么我们怎样标记这个不同呢？
  >
  > 答案就是`当前文件偏移量`，
  >
  > 通常打开文件时，读写操作都从文件偏移量开始，并使偏移量增加本次打开所读写的字节数，可以通过
  >
  > ```c
  > #include <fcntl.h>
  > off_t lseek(int fd, off_t offset, int whence)
  > ```
  >
  > 设置该值

- dup和dup2

  > ```c
  > int dup(int fd);
  > int dup2(int fd,int fd2);
  > ```
  >
  > 两个函数均可以复制fd，得到一个新的fd，出错时返回-1；
  >
  > `dup`正常返回系统可用最小fd
  >
  > `dup2`返回`fd2`指定文件描述符，若`fd2`正在使用，那就关闭原有，复制`fd`到`fd2`并返回

- sync、fsync和fdatasync

  通常情况下，传统UNIX操作系统通常存在一个高速缓冲区，磁盘IO均通过该缓冲区进行，当我们向文件写入数据，通常先保存到该缓存区域，进入磁盘写队列，这种方式称为延迟写（delayed write），如果缓存区域需要存别的数据，系统会将缓存区域所有数据全部写入磁盘后清空缓存。

  > ```c
  > #include <unistd.h>
  > void sync(void);
  > int fsync(int fd);
  > int fdatasync(int fd);
  > ```
  >
  > 如果有返回值并且方法执行成功，返回0，否则返回-1
  >
  > `sync`
  >
  > 将所有有改动的缓冲区放到磁盘写队列，不等待写操作成功就返回
  >
  > `fsync`
  >
  > 只对参数中fd指定的文件起作用，等待文件写入磁盘后返回结果
  >
  > `fdatasync`
  >
  > 只对参数中fd指定的文件起作用，等待文件写入磁盘后返回结果，是`faync`的弱化版本，只影响数据，对于文件属性没有影响

- fcntl

  > ```c
  > #include <fcntl.h>
  > int fcntl(int fd,int cmd,.../* int arg */)
  > ```
  >
  > fcntl有这些功能，取决于cmd的取值：
  >
  > - 复制fd	（F_DUPFD 或 F_DUPFD_CLOEXEC）
  > - 获取/设置fd   （F_GETFD或F_SETFD）
  > -  获取/设置文件状态   （F_GETFL或F_SETFL）
  > -  获取/设置异步IO所有权    （F_GETOWN或F_SETOWN）
  > -  获取/设置记录锁    （F_GETLK、F_SETLK或F_SETLKW）
  >
  > 对于当前函数内CMD参数的各种可能，可查阅[此篇博客](https://www.cnblogs.com/xuyh/p/3273082.html)

- 

### [文件描述符](./express_word.md)

**文件描述符的获取：**当打开或者新建文件时，内核向进程返回一个文件描述符

**文件描述符的使用：**当使用read或者write函数时，参数使用文件描述符

**文件描述符的范围：**取决于每个进程允许打开的文件数上限（不同的操作系统或有不同）

### IO的效率

使用read和write复制一个文件[copy_file](./copy_file.txt)，代码见[copy](./copy.c)，`MAC`无法编译代码的查看[这篇博客](https://blog.csdn.net/wallace89/article/details/124956235)

其中BUFFER_SIZE的值，由于大多数文件系统都会进行预读进而提高效率

### 文件的共享

内核使用三种数据结构表示打开文件，这三种结构决定了一个进程打开文件对另一个进程的影响

- 每个进程在进程表有个记录项，包含

  - 打开文件描述符表，每个文件描述符占一个

    文件描述符内容

    - 文件描述符标识
    - 指向文件表指针

- 内核对每个打开的文件，维持一个文件表，每个文件表项包含

  - 文件状态标识
    - 读｜写｜追加写｜阻塞等状态
  - 当前文件的偏移量
  - 指向该文件 V-节点 表项的指针

- 每个打开的文件都有V-节点结构，这个结构包含

  - 文件类型
  - 对文件的各种操作函数指针
  - i节点，i节点包含文件所有者，文件长度，文件在磁盘位置信息等

​	这些信息是在文件打开时读入到内存的，上面的关系画图标表示如下：

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230314172946188.png" alt="image-20230314172946188" style="zoom:50%;" />

当两个进程打开同一个文件，关系如下：

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230314173300886.png" alt="image-20230314173300886" style="zoom:50%;" />

当前情况下，文件描述符50和51打开了同一个文件，每个文件描述符都有一个自己的文件表项，但是却是指向同一个 V节点表项，之所以每个文件都有自己的文件表项，是为了让每个进程都有自己的文件偏移量

- 在每次写完成后，都在自己的文件表项中增加文件偏移量，如果超过i节点中当前文件长度，那么增加i节点中的当前文件长度。
- 如果使用O_APPEND标志打开文件，那么文件偏移量直接移动到i节点的当前文件长度
- lseek函数只改变文件表项中的文件偏移量，不做任何IO操作

### 文件原子操作

正常的写操作需要先调用`Lseek`将文件偏移量已到文件尾端，然后开始追写，由于这是两个操作，如果两个进程同时做这个操作，由于CPU会对进程进行调度，可能会导致线程A的文件表项的文件偏移量设置好后，B进程更新了整个文件的文件长度，导致A进程再次获取CPU时写的数据覆盖了B进程写入的数据。

使用下面三种方式可以将上述操作变成原子操作：

- 打开文件时使用O_APPEND
- 使用pread函数读取
- 使用pwrite函数写入
