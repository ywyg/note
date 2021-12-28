## 安装Zookeeper

* 使用docker拉取zookeeper镜像

  ```do
  ➜  ~ docker pull zookeeper
  Using default tag: latest
          
  latest: Pulling from library/zookeeper
  eff15d958d66: Pull complete 
  66aa43e8673f: Pull complete 
  089381f525cd: Pull complete 
  c9594f4373c2: Pull complete 
  b0fe3d8db030: Pull complete 
  b2fdab4981df: Pull complete 
  9e187a3301cc: Pull complete 
  cb7e3b60859d: Pull complete 
  Digest: sha256:9580eb3dfe20c116cbc3c39a7d9e347d2e34367002e2790af4fac31208e18ec5
  Status: Downloaded newer image for zookeeper:latest
  docker.io/library/zookeeper:latest
  ```

* 建立 zookeeper工作目录和数据存储目录 

  ```shell 
  cd /usr/local && mkdir zookeeper && cd zookeeper && mkdir data
  ```

* 运行zookeeper镜像

  ```sh
  docker run -d -e TZ="Asia/Shanghai" -p 2181:2181 -v $PWD/data:/data --name zookeeper --restart always zookeeper
  ```

## Zookeeper结构及组件

### 结构

> Zookeeper是树状结构，与文件系统非常类似

### 组件

#### 节点

* 临时节点	-----	客户端连接断开后，临时节点会被删除
* 持久节点	-----	会被持久化
* 顺序节点	-----	每次创建顺序节点时，ZooKeeper都会在路径后面自动添加上10位的数字，从1开始，最大是2147483647 

#### 节点属性

> `cZxid` ：创建的事务标识。
>
> `ctime`：创建的时间戳
>
> `mZxid`：修改的事务标识，每次修改操作（`set`）后都会更新`mZxid`和`mtime`。
>
> `mtime`：修改的时间戳
>
> `pZxid`：直接子节点最后更新的事务标识，子节点有变化（创建`create`、修改`set`、删除`delete`，`rmr`）时，都会更新`pZxid`。
>
> `cversion` ：直接子节点的版本号。当子节点有变化（创建`create`、修改`set`、删除`delete`，`rmr`）时，`cversion` 的值就会增加1。
>
> `dataVersion`  ：节点数据的版本号，每次对节点进行修改操作（`set`）后，`dataVersion`的值都会增加1（即使设置的是相同的数据）。
>
> `aclVersion`  ：节点ACL的版本号，每次节点的ACL进行变化时，`aclVersion` 的值就会增加1。
>
> `ephemeralOwner`：当前节点是临时节点（`ephemeral node` ）时，这个`ephemeralOwner`的值是客户端持有的`session` id。
>
> `dataLength`：节点存储的数据长度，单位为 B （字节）。
>
> `numChildren`：直接子节点的个数。
>
> 作者：宗离
> 链接：https://juejin.cn/post/6844904167287291912
> 来源：稀土掘金
> 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

#### 纪元

-- zxid前32位，后32位是事务id，事务id用完的话，

-- 

-- 服务启动次数，服务第一次启动纪元为 1 ，重启之后变成 2

## Zookeeper常用命令

## Zookeeper客户端

