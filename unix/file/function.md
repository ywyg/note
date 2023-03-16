## `UNIX`文件操纵函数

### `stat`、`fstat`、`fstatat`、`lstat`

 ```c
 #include <sys/stat.h>
 int stat(const char *restrict pathname, struct stat *restrict buf);
 int fstat(int fd, struct stat *restrict buf);
 int fstatat(const char *restrict pathname, struct stat *restrict buf);
 int lstat(int fd, const char *restrict pathname, struct stat *restrict buf, int flag);
 ```

#### `pathname`

- `stat`

当给定`pathname`，`stat`函数返回与此文件命名有关的信息结构

- `fstat`

`fstat`函数获取fd打开文件的有关信息

- `lstat`

类似于`stat`，但是当命名的文件是一个符号链接时，并不返回符号链接文件的信息，而是返回符号链接的有关信息

- `fstatat`

`fstatat`为fd指定的目录返回文件统计信息，flag参数表明是否跟随符号链接（找到符号链接链接文件），默认跟随。

如果fd的参数是`F_FDCWD`，并且`pathname`是相对路径，会计算当前目录`pathname`参数，如果是绝对路径，fd参数会被忽略。

#### `buf`

`buf`是一个指针，指向一个必须提供的结构，函数会填充这个结构内字段，大致结构如下：

```c
struct stat{
  mode_t		st_mode;						/*文件类型和权限类型*/
  ino_t			st_ino;							/*i-mode num*/
  dev_t			st_dev;							/*device num (file system)*/
  dev_t			st_rdev;						/*device num for special file*/
  nlink_t		st_nlink;						/*number of links*/
  uid_t			st_uid;							/*user id of owner*/
  gid_t			st_gid;							/*group id of owner*/
  off_t			st_size;						/*普通文件字节数*/
  struct timespec		st_atime;		/*最近一次访问*/
  struct timespec		st_mtime;		/*最近一次修改*/
  struct timespec		st_ctime;		/*最近一次文件状态变化*/
  blksize_t			st_blksize;			/*best IO block size*/
  blkcnt_t			st_blocks;	/*number of disk blocks allocted */
}
```

### `access` 、`faccessat`

我们知道打开文件时系统会使用有效角色进行权限检查，但是有时候我们需要测试实际用户的权限，那么就可以使用这两个函数

```c
#include <unistd.h>

int access(const char *pathname,int mode);
int faccessat(int fd, const *pathname, int mode, int flag);
```

| mode | 说明     |
| ---- | -------- |
| F_OK | 是否存在 |
| R_OK | 读权限   |
| W_OK | 写权限   |
| X_OK | 执行权限 |

当`pathname`为绝对路径或者当fd = `AT_FDCWD` & `pathname`为相对路径，两个函数的功能相同

但是当`faccessat`函数的`flag`=`AT_EACCESS`时，检查的依旧是有效角色，而不是实际角色

### `Unmask`



## 文件类型

- 普通文件
- 目录文件
- 块文件
- 字符文件
- 管道文件
- 套接字文件
- 符号链接

## 文件的权限

文件的权限分为三个角色

- 用户
- 组
- 其他

其中每个角色又有三种权限

- 读
- 写
- 执行

当进程准备打开文件时，系统进行如下检查

1. 超级用户给予充分的权限
2. 文件所有者打开文件，检查权限
3. 进程属于用户没有权限，检查进程所属组是否有权限
4. 文件的其他角色权限设置是否允许此种访问方式，按照权限放行

文件的权限保存在文件信息的 `mode_t`模块中

新建文件用户角色与当前用户相同，组和其他角色由目录继承

## 设置用户与组

| 实际用户<br />实际组             | 实际角色 |
| -------------------------------- | -------- |
| 有效用户<br />有效组<br />附属组 | 有效角色 |
| 设置用户<br />设置组             | 设置角色 |

实际角色：登录时角色

有效角色：文件权限检查使用角色，通常与实际角色相同，但是可以通过设置角色，例如：root用户设置文件的设置角色为root，那么不管是哪个用户执行，都拥有和root一样的权限

设置角色：文件设置角色位，由exec函数设置





### 





