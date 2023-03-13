## HTTP的方法类型

#### GET

> get 用于向服务器指定的资源请求数据

get 请求可以在请求`URL`中添加`key-value`发送请求

get请求的一些特点：

- 可以被缓存
- 可以被浏览器记录
- 可以被当作书签
- 在处理敏感信息的时候千万不要使用get
- 有长度限制
- 不应当在更新数据需求的时候使用get
- 仅仅用作查询数据使用

#### POST

> post请求用于发送一些新建或者更新资源的数据到服务器

post 请求向服务端发送的数据存储在request-body中

post请求的一些特点：

- 从不被缓存
- 不会被浏览器记住
- 不能当作书签
- 没有长度限制

|               | GET                                 | POST                                                         |
| ------------- | ----------------------------------- | ------------------------------------------------------------ |
| 刷新或者返回  | 随意，无影响                        | 请求会被重新提交，                                           |
| Encoding type | application/x-www-form-urlencoded   | application/x-www-form-urlencoded or multipart/form-data. Use multipart encoding for binary data |
| 长度限制      | 2048个字符                          | 无限制                                                       |
| 数据类型限制  | 只允许ASCII编码（待确认）           | 无限制，二进制也可以                                         |
| 安全性        | 不安全，不要使用get发送任何敏感信息 | 比get安全一些                                                |
| 是否可见      | 可见，就在URL里面                   | 不可见                                                       |

#### PUT

> put请求用于发送一些新建或者更新资源的数据到服务器

put与post相比，put是幂等，也就是重复调用不会造成影响，而重复调用post会产生重复创建资源的影响

#### DELETE

> delete 请求用于删除指定的资源

#### HEAD

#### PATCH

#### OPTIONS

#### CONNECT

#### TRACE



