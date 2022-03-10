## 启动

### ES

执行`bin/elasticsearch`

访问`localhost:9200`，获得如下结果

```json
{
  "name" : "gaosaijiedeMacBook-Pro.local",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "-SPmSA4aTWKQNultuONpPw",
  "version" : {
    "number" : "7.16.3",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "4e6e4eab2297e949ec994e688dad46290d018022",
    "build_date" : "2022-01-06T23:43:02.825887787Z",
    "build_snapshot" : false,
    "lucene_version" : "8.10.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

### kibana

> 启动`kibana`必须先启动`ES`
>
> 如果ES启动时不是默认地址端口，需要在`kibana`修改`ES`配置文件/

#### **关闭**

> lsof -i :5601

#### 常见问题

![image-20220126112827870](https://tva1.sinaimg.cn/large/008i3skNly1gyqwy101knj314u0p8add.jpg)