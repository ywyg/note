<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230316191422283.png" alt="image-20230316191422283" style="zoom:50%;" />

## 请求

```http
GET /index.html HTTP/1.1
Host: www.sina.com.cn
Connection: Keep-Alive
```

`GET /index.html HTTP/1.1`：起始行

`Host: www.sina.com.cn
Connection: Keep-Alive`：首部

## 响应

```http
HTTP/1.1 200 OK
Content-length: 105
Content-type: text/html
```



## 请求体

上述介绍通过查询HTTP消息结构就能了解到每部分的作用，所以就不再多说，由于我们的WEB开发常常是接受各种各样的WEB请求，所以我们看一下不同的请求体之间有什么差别：

我们以`post-man`发送请求，手动写一个TCP Server接受请求并打印

```java
public static void receiveTcpClient() throws IOException {
        ServerSocket ss = new ServerSocket();
        ss.bind(new InetSocketAddress(80));
        while (true) {
            Socket accept = ss.accept();
            InputStream inputStream = accept.getInputStream();
            byte[] bytes = new byte[1024];
            while (inputStream.read(bytes) > 0) {
                String s = new String(bytes);
                System.out.println(s);
            }
            inputStream.close();
            accept.close();
        }
    }

```

### GET请求

#### param

请求内容

```sh
curl --location --request GET 'localhost:80?param=value'
```

包装后内容

```http
GET /?param=value HTTP/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: cf4d3fe6-1fb3-402e-ab8b-6e02a369344f
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

#### body:form-data

请求内容

```sh
curl --location --request GET 'localhost:80' \
--form 'form="value"'
```

包装后内容

```http
GET / HTTP/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: ff0bdefd-c795-4b3d-892e-46f4e31be309
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: multipart/form-data; boundary=--------------------------761766213607993473634996
Content-Length: 164

----------------------------761766213607993473634996
Content-Disposition: form-data; name="form"

value
----------------------------761766213607993473634996--
```

#### body:x-www-form-urlencoded

请求内容

```sh
curl --location --request GET 'localhost:80' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'x-www-lencoded=value'
```

包装后内容

```http
GET / HTTP/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: c957788a-7321-4ed1-9f6c-4373b4753ad1
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 20

x-www-lencoded=value
```

#### body:text

请求内容

```sh
curl --location --request GET 'localhost:80' \
--header 'Content-Type: text/plain' \
--data-raw '{
    "text":"value"
}'
```

包装后内容

```http
GET / HTTP/1.1
Content-Type: text/plain
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: ac787ddb-a6bb-48e6-bb3a-dca9d12b64e9
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 22

{
    "text":"value"
}
```

#### body:json

请求内容

```sh
curl --location --request GET 'localhost:80' \
--header 'Content-Type: application/json' \
--data-raw '{
    "json":"value"
}'
```

包装后内容

```http
GET / HTTP/1.1
Content-Type: application/json
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 728640ad-aa1c-4003-af3b-db6a40b1ca06
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 22

{
    "json":"value"
}
```

#### body:xml

请求内容

```sh
curl --location --request GET 'localhost:80' \
--header 'Content-Type: application/xml' \
--data-raw '{
    "xml":"value"
}'
```

包装后内容

```http
GET / HTTP/1.1
Content-Type: application/xml
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 99f9d105-64fc-4eba-90d4-5891505a175d
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 21

{
    "xml":"value"
}
```

#### binary

请求内容

```sh
curl --location --request GET 'localhost:80' \
--header 'Content-Type: application/zip' \
--data-binary '@/path/test.json.zip'
```

包装后内容

```http
GET / HTTP/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: d768add1-c1e3-4c19-9a17-000b2b2f5df6
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 782
Content-Type: application/zip

�Ћ�׵������Rl�T���5�٪{�:� ��xɍm
 ��d��d��dux �     PK      �
   -    P/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: d768add1-c1e3-4c19-9a17-000b2b2f5df6
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 782
Content-Type: application/zip

�Ћ�׵������Rl�T���5�٪{�:� ��xɍm
 ��d��d��dux �     PK      �
```

### POST请求

#### param

请求内容

```sh
curl --location --request POST 'localhost:80?param=value'
```

包装后内容

```http
POST /?param=value HTTP/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 620b1191-8cbf-4e67-a119-a54d62da4448
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 0
```

#### body:form-data

请求内容

```sh
curl --location --request POST 'localhost:80' \
--form 'form="value"'
```

包装后内容

```http
POST / HTTP/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: ccace6a9-6a8c-46a6-8dbf-fdff591f82ff
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: multipart/form-data; boundary=--------------------------596407557865606089370318
Content-Length: 164

----------------------------596407557865606089370318
Content-Disposition: form-data; name="form"

value
----------------------------596407557865606089370318--
```

#### body:x-www-form-urlencoded

请求内容

```sh
curl --location --request POST 'localhost:80' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'x-www-lencoded=value'
```

包装后内容

```http
POST / HTTP/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 5e3328c8-6127-43a6-bc27-3720a056d744
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 20

x-www-lencoded=value
```

#### body:text

请求内容

```sh
curl --location --request POST 'localhost:80' \
--header 'Content-Type: text/plain' \
--data-raw '{
    "text":"value"
}'
```

包装后内容

```http
POST / HTTP/1.1
Content-Type: text/plain
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 2453aa5f-4216-47eb-a0ee-ad7809d3f955
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 22

{
    "text":"value"
}
```

#### body:json

请求内容

```sh
curl --location --request POST 'localhost:80' \
--header 'Content-Type: text/json' \
--data-raw '{
    "json":"value"
}'
```

包装后内容

```http
POST / HTTP/1.1
Content-Type: application/json
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 61eb63be-9444-495f-bce7-93bfb64af6ce
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 22

{
    "json":"value"
}
```

#### body:xml

请求内容

```sh
curl --location --request POST 'localhost:80' \
--header 'Content-Type: application/xml' \
--data-raw '{
    "xml":"value"
}'
```

包装后内容

```http
POST / HTTP/1.1
Content-Type: application/xml
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 1d758c38-a4c7-43ef-868b-aaf49c652af2
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 21

{
    "xml":"value"
}
```

#### binary

请求内容

```sh
curl --location --request POST 'localhost:80' \
--header 'Content-Type: application/zip' \
--data-binary '@/path/test.json.zip'
```

包装后内容

```http
POST / HTTP/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 211fc814-4d87-427e-9358-07673167d8c2
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 782
Content-Type: application/zip

�Ћ�׵������Rl�T���5�٪{�:� ��xɍm
 ��d��d��dux �     PK      
�   -    P/1.1
User-Agent: PostmanRuntime/7.28.4
Accept: */*
Postman-Token: 211fc814-4d87-427e-9358-07673167d8c2
Host: localhost:80
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 782
Content-Type: application/zip

�Ћ�׵������Rl�T���5�٪{�:� ��xɍm
 ��d��d��dux �     PK      

```

### 
