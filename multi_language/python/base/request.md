Python中request模块是一个很常用的模块，常用于一些简单的web测试，发送HTTP请求等

### 安装request模块

> pip(3) install requests

### 主要语法：

```python
requests.methodname(params)
```

#### methodname list

| methodname                 | 描述           |
| -------------------------- | -------------- |
| `delete(url,args)`         | delete request |
| `get(url,params,args)`     | get request    |
| `post(url,data,json,args)` | post request   |
| `put(url,data,args)`       | put request    |
| `patch(url,data,args)`     | patch request  |
| `head(url,args)`           | head request   |
| `request(method,url,args)` | request        |

#### 示例

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230314155530022.png" alt="image-20230314155530022" style="zoom:50%;" />

#### 参数分析

- data

  > 当你使用 `data={'key':'value'}`作为方法的参数时，数据将会作为表单数据被提交，例如：
  >
  > ```python
  > r = requests.post('https://httpbin.org/post', data={'key': 'value'})
  > ```

- params

  > 当你使用 `params={'key':'value'}`作为方法的参数时，数据将会拼接在URL后使用，例如：
  >
  > ```python
  > r = requests.get('https://httpbin.org/get', params=params)
  > == 
  > https://httpbin.org/get?key=value
  > ```

- json

  注意，当请求参数中出现data|files，json参数将被忽略

  > 当你使用`json={'key':'value'}`作为方法参数时，数据将会以json 格式发送，例如：
  >
  > ```python
  > url = 'https://api.github.com/some/endpoint'
  > payload = {'some': 'data'}
  > r = requests.post(url, json=payload)
  > ```

- file

  > 当需要发送二进制数据时，使用json参数，例如：
  >
  > ```python
  > r = requests.post(url, files=open('path/file_name','rb'))
  > ```

### Response

- status_code

  > ```python
  > >>> r = requests.get('https://httpbin.org/get')
  > >>> r.status_code
  > >>> r.status_code == requests.codes.ok
  > ```

- raise_for_status

  > 请求返回错误时异常会记录在这里
  >
  > ```python
  > >>> r.raise_for_status()
  > ```