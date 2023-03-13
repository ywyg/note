## Content-Type

### 定义

Content-Type : 一般用于定义网络文件的类型和网页的编码，决定浏览器将以什么形式，什么编码读取这个文件，

Content-Type : 标头告诉客户端实际返回内容的内容类型 

### 语法格式

```html
Content-Type:text/html;charset=utf-8
Content-Type: multipart/form-data; boundary={文件长度(字节)}
```

### 消息类型

消息类型通用结构

> type/struct

#### 常见 type 类型

| 类型        | 简单描述                                   |
| ----------- | ------------------------------------------ |
| text        | 理论上文件时人类可读的                     |
| image       | 图像文件，不包含视频，但是包含动态图(.gif) |
| audio       | 音频文件                                   |
| video       | 视频文件                                   |
| application | 二进制文件                                 |

#### 常见消息类型

| 类型                              | 内容                                     |
| --------------------------------- | ---------------------------------------- |
| text/html                         | HTML格式                                 |
| text/plain                        | 纯文本格式                               |
| text/xml                          | XML格式                                  |
| image/gif                         | gif图片格式                              |
| image/jpeg                        | jpg图片格式                              |
| image/png                         | png图片格式                              |
|                                   |                                          |
| application/xml                   | XML数据格式                              |
| application/json                  | JSON数据格式                             |
| application/pdf                   | PDF数据格式                              |
| application/msword                | WORD文档格式                             |
| application/x-www-form-urlencoded | 默认格式，表单提交使用                   |
| multipart/form-data               | 需要在表单中上传文件时，就需要使用该格式 |

