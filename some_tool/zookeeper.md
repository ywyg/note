# 概要

> Zookeeper 是一个分布应用协调器，

## 下载

在apache镜像下载：[zookeeper](http://zookeeper.apache.org/releases.html)

## 单机启动

1. 解压下载文件

2. 在conf目录下新建`zoo.cfg`配置文件

   ```properties
   tickTime=2000
   dataDir=/你的路径
   clientPort=2181
   ```

   - tickTime：单位毫秒，用于心跳检测，超时判断是大于两倍tickTime，
   - dataDir：数据快照和
   - clientPort：监听端口

3. 启动服务

   ```shell
     bin/zkServer.sh start
   ```

4. 链接 zookeeper

   ```shell
   bin/zkCli.sh -server 127.0.0.1:2181
   ```

5. 简单交互

   1. 查看当前根节点目录

      ```shell
      [zk: 127.0.0.1:2181(CONNECTED) 1] ls /
      [zookeeper]
      ```

   2. 新建节点

      ```shell
      [zk: 127.0.0.1:2181(CONNECTED) 2] create /zk_test my_data
      Created /zk_test
      [zk: 127.0.0.1:2181(CONNECTED) 3] ls /
      [zk_test, zookeeper]
      [zk: 127.0.0.1:2181(CONNECTED) 4] get /zk_test
      my_data
      ```

   3. 更新节点

      ```shell
      [zk: 127.0.0.1:2181(CONNECTED) 5] set /zk_test junk
      [zk: 127.0.0.1:2181(CONNECTED) 6] get /zk_test
      junk
      ```

   4. 删除节点

      ```shell
      [zk: 127.0.0.1:2181(CONNECTED) 7] delete /zk_test
      [zk: 127.0.0.1:2181(CONNECTED) 9] ls /
      [zookeeper]
      ```

## 集群启动

1. 建立三个目录

   ```shell
   drwxr-xr-x  4 XX  staff   128B  3 24 14:32 clu1
   drwxr-xr-x  4 XX  staff   128B  3 24 14:32 clu2
   drwxr-xr-x  4 XX  staff   128B  3 24 14:32 clu3
   ```

2. 后续操作需要同时在`clu1` `clu2` `clu3`执行

3. 分别解压缩下载镜像

   ```shell
   XX  ~/local/program/zookeeper/cluster/clu1 > ll
   total 19320
   drwxr-xr-x  12 XX  staff   384B  3 24 15:06 apache-zookeeper-3.5.10-bin
   ```

4. 在conf目录下新建`zoo.cfg`配置文件

   ```properties
   tickTime=2000
   dataDir=/你的路径
   //clientPort 分别为 2181 2182 2183
   clientPort=2181 
   initLimit=5
   syncLimit=2
   server.1=127.0.0.1:2888:3888
   server.2=127.0.0.1:2889:3889
   server.3=127.0.0.1:2890:3890
   ```

5. 在dataDir目录下新建myid文件

   ```shell
   touch ${dataDir}/myid
   // 三个节点分别写入 1、2、3
   echo "1" > ${dataDir}/myid
   ```

6. 启动集群

   ```shell
    bin/zkServer.sh start
   ```

7. 观察集群状态

   ```shell
    bin/zkServer.sh status
   ```

8. 效果测试

   - 客户端链接

     ```shell
     > bin/zkCli.sh -server 127.0.0.1:2181
     ```

   - 查看节点

     ```shell
     [zk: 127.0.0.1:2181(CONNECTED) 0] ls /
     [zookeeper]
     ```

   - 创建新节点

     ```shell
     [zk: 127.0.0.1:2181(CONNECTED) 1] create /cluster cluster2181
     Created /cluster
     [zk: 127.0.0.1:2181(CONNECTED) 2] ls /
     [cluster, zookeeper]
     [zk: 127.0.0.1:2181(CONNECTED) 3] get /cluster
     cluster2181
     ```

   - 关闭2181对应的server

     ```shell
     bin/zkServer.sh stop
     ```

     同时，我们收到client refuse消息

     ```shell
     [main-SendThread(127.0.0.1:2181):ClientCnxn$SendThread@1261] - Socket error occurred: localhost/127.0.0.1:2181: Connection refused
     ```

   - 链接到server

     ```shell
     bin/zkCli.sh -server 127.0.0.1:2182
     ```

   - 查看节点

     ```shell
     [zk: 127.0.0.1:2182(CONNECTED) 0] ls /
     [cluster, zookeeper]
     [zk: 127.0.0.1:2182(CONNECTED) 1] get /cluster
     cluster2181
     ```

   - 可以看到，我们在2181创建的节点已经被同步过来了，证明集群运行正常

## zookeeper命令集

zxid ：事务id，64位，高32位表示leader任期，低32位表示事务序列号

- create： 创建一个新的节点，并设置它的值和属性
- get：获取节点的值和属性
- set：设置节点的值和属性
- delete：删除指定的节点
- ls：列出指定节点的子节点
- stat：获取指定节点的状态信息

### `stat` 指令

- cZxid ：znode-id，64位，高32位单调递增，低32位表示会话id
- ctime ：创建时间
- mZxid ：最后一次修改该节点的zxid
- mtime ：最后一次修改时间
- pZxid ：父节点事务id
- cversion ：子节点版本号
- dataVersion ：数据版本号
- aclVersion ：ACL版本号
- ephemeralOwner ：临时节点所有者，如果值为0，表示持久节点

```shell
[zk: 127.0.0.1:2182(CONNECTED) 4] stat /cluster
cZxid = 0x100000002
ctime = Fri Mar 24 15:21:35 CST 2023
mZxid = 0x100000002
mtime = Fri Mar 24 15:21:35 CST 2023
pZxid = 0x100000002
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 11
numChildren = 0
```

### `create` 指令

- `-s`：有序节点
- `-e`：临时节点
- `-c`：容器节点（目录）
- `-d`：持久化节点

### `get` 指令

- `-s`：详细信息，包含内容和状态信息
- `-w`：内容信息

### `set` 指令

- `-s`：内容设置为字符串
- `-v`：同时设置版本

### `delete` 指令

- `-v`：版本匹配才删除

### `ls` 指令

- `-s`：详细信息，包含内容和状态信息
- `-w`：内容信息
- `-R`：递归列出节点信息

## 工作原理探究

特性：

> 最终一致性
>
> 可用性
>
> 半数原则

正如博客开始的地方写到，zookeeper是一个分布组件协调器，所以zookeeper是整个分布式服务的一个重要部分，那么它又是怎么完成这部分工作的呢？

- 集群

  如果zookeeper是单机的，当zookeeper发生网络中断、服务宕机等突发情况时，所有依赖zookeeper的应用都会产生问题，为了避免单点故障，zookeeper必须设置为集群形式。

首先我们了解一下zookeeper集群中都有哪些角色

- Leader

  Leader 是在集群中是核心且唯一的，复制集群状态的同步，数据同步，对外通信等

- Follower

  Follower节点是Leader节点的追随者，负责接收读请求，与Leader节点之间通过心跳链接，写请求将会转发给Leader节点，参与投票

- Observer

  Observer节点可以理解为不参与投票的的Follower节点，用来缓解Follower的压力

角色的分配由选举产生。

至此，我们知晓集群内有哪些角色，接下来分析如果保证数据一致性

### 数据一致性

数据一致性是分布式系统必须要面对和解决的问题，在zookeeper中通过一些措施来保证这点

- 只有Leader节点可以写入数据

  所有的写请求都会汇聚到Leader节点，由于Leader节点是单机的，所以可以解决并发写入问题

- 心跳机制

  Follower和Observer使用心跳机制探测自身与Leader节点的通信情况，保证自身数据是最新的

上述两点，在不出问题的情况下，可以保证数据肯定是最新的，但是在一些特殊情况下会出现问题

- Leader节点宕机或者服务崩溃

  当Follower在超过`initLimit*tickTime`时间内无法与Leader通信时，Follower会发起选举，选择一个新的Leader主持集群工作，这种情况下集群服务会暂时不可用，待选举完成后集群内部节点同步完成后恢复可用状态

- Follower宕机或者服务崩溃

  集群反应：Leader一段时间没有收到Follower的心跳信号，会把该Follower移出集群，并通知到其他的Follower

  宕机Follower反应：

  - 服务崩溃：无反应，待修复后重启加入集群
  - 网络波动：向其他Follower发起选举请求，但由于其他节点已经从Leader得知该Follower宕机或者其他节点可以正常同Leader节点通信，所以会抛弃这次选举请求

显然，那怕是最坏的结果也是Leader服务不可用，此时只需经过重新选举得到新Leader即可，选举的具体过程是怎样的呢？

1. 所有的Follower进行Looking状态，每个服务准备自己的选票信息（包含自身服务id、zxid、选举轮次、自身状态、ip和port）
2. 发送选票信息到其他的Follower，并接受其他服务的选票
3. 检查选票信息，判断哪个节点应该成为新的Leader，每个服务拿到的都是一样的数据，所以会产生相同的判断，也就是Leader是公认的
   1. 比较zxid
   2. 比较sid
4. 选举结束后新Leader昭告天下，其他的Follower变成该Leader的Follower，选举轮次 + 1，同步数据
5. 集群提供服务

为了更快的恢复服务，选举过程中，当多个节点都可以成为Leader时，服务Id（m yid文件内的值）最大的成为Leader，所以myid内文件的值在集群内必须唯一，这样暂时可以满足服务快速恢复需求

### 消息的同步

zookeeper消息的同步主要是利用ZAB（Zookeeper Atomic Broadcast）协议：

- 写请求到达Leader节点后，Leader并不会直接提交该事务，而是将此次写请求广播到所有的Follower节点，Follower节点执行相同的操作并返回结果到Leader
- Leader收到超过半数Follower节点完成消息后，Leader将数据写入自己数据库，并生成一条新的zxid，并告知到所有的Follower和Observer节点执行相同操作

通过两段提交方式来保障数据的最终一致性，由于Follower和Leader之间通过心跳来检查通信，所以可能出现在一次心跳间隔内数据没有同步到Follower，导致查询Follower获取到旧数据，不满足实时性

## 配置中心

## 分布式锁























