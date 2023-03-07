class文件是一种与语言平台均无关的字节码文件，可以由不同的语言经过各自的编译器编译而来，均在JVM上运行

## class文件结构

| 类型    | 名称                            | 数量                  |
| ------- | ------------------------------- | --------------------- |
| u4      | 魔数                            | 1                     |
| u2      | 小版本                          | 1                     |
| u2      | 大版本                          | 1                     |
| u2      | 常量池数量(constant-pool-count) | 1                     |
| cp_info | 常量池                          | constant-pool-count-1 |
| u2      | 访问标记                        | 1                     |
| u2      | 当前类引用(this_class)          | 1                     |
| u2      | 父类引用(super_class)           | 1                     |
| u2      | 接口数量(interfaces_count)      | 1                     |
| u2      | interfaces                      | interfaces_count -1   |
| u2      | fields_count                    |                       |
|         |                                 |                       |
|         |                                 |                       |
|         |                                 |                       |
|         |                                 |                       |
|         |                                 |                       |

