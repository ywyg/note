# 为了完成k8s的学习，我们需要完成以下步骤(MAC OS)

1. 创建一个k8s集群
2. 部署应用程序
3. 应用程序的探索
4. 暴露应用
5. 拓展应用
6. 升级应用

## 创建一个k8s集群

### k8s 集群

k8s协调一个高可用计算机集群，每台计算机作为一个独立单元相互连接，可以将应用部署到集群，而无需考虑应用部署到了哪台机器上，解除原来应用与机器的绑定关系。k8s可以自主的调节调度集群内应用容器。

一个k8s集群需要两种资源

- **Master** 调度整个集群
- **Node** 负责运行项目
- 容器运行时：Kubernetes可以与众多容器运行时（例如Docker、rkt）一起工作，以提供应用程序运行的环境。
- 网络插件：Kubernetes需要使用网络插件来提供容器之间的网络通信，常见的网络插件包括Flannel、Calico、Weave Net等。
- 存储插件：Kubernetes可以使用各种存储插件来为应用程序提供持久化存储支持，例如 NFS、GlusterFS、Ceph、Rook等。
- 控制器：Kubernetes中的控制器用于确保群集的状态与期望的状态匹配，例如 Deployment、StatefulSet、DaemonSet、Job、CronJob等。

#### **Master **

Master 负责管理整个集群。 Master 协调集群中的所有活动，例如调度应用、维护应用的所需状态、应用扩容以及推出新的更新。

#### **Node** 

Node 是一个虚拟机或者物理机，它在 Kubernetes 集群中充当工作机器的角色，每个Node都有 Kubelet , 它管理 Node 并且是 Node 与 Master 通信的代理。 Node 还应该具有用于处理容器操作的工具，例如 Docker 或 rkt 。处理生产级流量的 Kubernetes 集群至少应具有三个 Node，因为如果一个 Node 出现故障其对应的 etcd 成员和控制平面实例都会丢失，并且冗余会受到影响。 你可以通过添加更多控制平面节点来降低这种风险 。

#### 容器运行时(container running)

K8S集群通过将起容器的方式运行应用，一般使用Docker作为容器，较新版本的K8S使用 containerd 或者 CRI- O。

在 Kubernetes 上部署应用时，你告诉 Master 启动应用容器。 Master 就编排容器在集群的 Node 上运行。 **Node 使用 Master 暴露的 Kubernetes API 与 Master 通信。**终端用户也可以使用 Kubernetes API 与集群交互。

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230406141247131.png" alt="image-20230406141247131" style="zoom:50%;" />

### 下载 **Minikube**

```shell
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

由于**Minikube**运行依赖**Docker**，所以还需要下载Docker。

```shell
brew install --cask --appdir=/Applications docker
```

由于我们使用Kubectl与Minikube进行交互，所以还需要安装Kubectl，参考官网的[安装](https://kubernetes.io/zh-cn/docs/tasks/tools/install-kubectl-macos/)方式。

### 启动Minikube

1. 启动mini集群

```shell
minikube start
```

2. 集群状态

```shell
## 集群版本
minikube version
## kubectl 版本
kubectl version
```

3. kubectl连接到集群

   kubectl连接信息依赖与`~/.kube/config`文件，该文件会在 [kube-up.sh](https://github.com/kubernetes/kubernetes/blob/master/cluster/kube-up.sh) 创建集群或者成功部署一个 Minikube 集群时自动生成

   config文件内容

   - cluster：描述集群信息
   - context：集群上下文环境
   - user：用户信息

   ```shell
   ## 查看配置，这种查看方式会展示所有config合并的结果，可以指定 --kubeconfig 参数查看某一个config内容，当有多个k8s集群时方便使用
   kubectl config view
   ```

   1. 如果你只部署了Minikube，那么可以直接查看集群状态

      ```shell
      ## 集群信息
      kubectl cluster info
      ## 集群nodes
      kubectl get nodes
      ```

   2. 如果有多个集群需要连接，那么需要配置多集群环境。

      > 假如本地的~/.kube/config已经配置了集群环境，部署Minikube时会再此基础上追加一个Minikube的配置

      具体配置参考[官方文档](https://kubernetes.io/zh-cn/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)

   3. 使用命令切换上下文就可以切换kubectl连接的集群

      ```shell
      kubectl config  use-context minikube|other
      ```

## 部署应用

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230407113401946.png" alt="image-20230407113401946" style="zoom:50%;" />

此次我们会部署一个官方提供的示例项目

1. 使用`kubectl create deployment`创建`deployment`对象（这个过程需要一段时间）

```shell
kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1
## 启动服务
kubectl expose deployment/kubernetes-bootcamp --type="ClusterIP" --port 80
```

2. 查看`deployment`对象状态

```shell
kubectl get deployment
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   1/1     1            1           6m58s
```

3. 对外暴露应用

   此时应用运行在Docker容器内部，无法从外部访问，当你尝试访问，会收到如下回复。

   ```shell
   curl http://localhost:8001/version
   curl: (7) Failed to connect to localhost port 8001: Connection refused
   ```

   但是我们可以使用`kubectl`访问到集群，实际上是通过 API访问的集群，这些配置可以在启动集群那部分内容的 config 配置中查看。

   想要通过Http访问，我们可以使用k8s的代理服务，转发请求，具体如下：

   ​		打开一个新的终端

   ```shell
   输入：kubectl proxy
   ```

   ​		在第一个终端中继续请求

   ```shell
   curl http://localhost:8001/version
   {
     "major": "1",
     "minor": "26",
     "gitVersion": "v1.26.3",
     "gitCommit": "9e644106593f3f4aa98f8a84b23db5fa378900bd",
     "gitTreeState": "clean",
     "buildDate": "2023-03-15T13:33:12Z",
     "goVersion": "go1.19.7",
     "compiler": "gc",
     "platform": "linux/amd64"
   }%
   ```

   在这个过程中，首先使用`kubectl proxy`在本地开启一个`Http`代理服务器，可以像使用`kubectl`那样访问到集群，然后就可以访问了

   API Server同样会为每个pod根据pod名创建一个端点，我们也可以通过这个查看pod信息

   ```shell
   export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
   echo Name of the Pod: $POD_NAME
   ```

   这个命令会获取所有pod的名称，并保存到`POD_NAME`，然后打印出`POD_NAME`

   ```shell
   curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME/
   ```

   通过pod name打印pod所有信息

## 应用程序的探索

在上一节的部署中，deployment对象生成了一个pod用来运行应用，那么pod是什么？

最直白的理解，pod就是一台主机。当然不能这么简单的理解，实际上，pod是一组应用的容器和这些容器的共享资源，pod位于工作节点。

- 共享存储，当作卷
- 网络，作为唯一的集群 IP 地址
- 有关每个容器如何运行的信息，例如容器镜像版本或要使用的特定端口

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230407143845007.png" alt="image-20230407143845007" style="zoom:50%;" />

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230407143938388.png" alt="image-20230407143938388" style="zoom:50%;" />

接下来，我们通过一些命令来查看node或pod的具体信息

查看pod

```shell
kubectl get pods
NAME(pod name)	                       READY   STATUS    RESTARTS(重启次数)   AGE(运行时间)
kubernetes-bootcamp-5485cc6795-scn7p   1/1     Running   0          48m
```

pod详细信息

```shell
kubectl describe pods
```

​		在这个命令的结果里，我们可以看到pod的容器：IP、port和pod的生命周期等信息

服务信息

1. 启动代理

```shell
kubectl proxy
```

2. 查看服务

```shell
curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME:80/proxy/
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-5485cc6795-scn7p | v=1
```

pod日志信息

```shell
kubectl logs $POD_NAME
```

容器执行命令

```shell
kubectl exec $POD_NAME -- /bin/sh | curl --XX
```

​		在后面跟的参数就是容器要执行的命令，如果是/bin/sh，会进入容器内部，进入命令行模式

## 使用 Service 暴露你的应用

在这一节，我们需要了解一下Service的概念，K8S集群中，pod依赖于node的存在，如果node主机宕机或者其他故障，都会造成pod出错，其中的应用无法继续提供服务，所以需要启动新的pod使集群回到目标状态。Service就是为了解决这个问题提出的，简单理解，Service描述了集群的目标状态，包括需要启动的pod数量，如何对外提供服务等，Service可以理解为一个定义，定义了集群的目标状态，Service通常使用YAML [(更推荐)](https://kubernetes.io/zh-cn/docs/concepts/configuration/overview/#general-configuration-tips) 或者 JSON来定义。

尽管每个 Pod 都有一个唯一的 IP 地址，但是如果没有 Service ，这些 IP 不会暴露在集群外部。Service 允许你的应用程序接收流量。Service 也可以用在 ServiceSpec 标记`type`的方式暴露。

- *ClusterIP* (默认) - 在集群的内部 IP 上公开 Service 。这种类型使得 Service 只能从集群内访问。
- *NodePort* - 使用 NAT 在集群中每个选定 Node 的相同端口上公开 Service 。使用`<NodeIP>:<NodePort>` 从集群外部访问 Service。是 ClusterIP 的超集。
- *LoadBalancer* - 在当前云中创建一个外部负载均衡器(如果支持的话)，并为 Service 分配一个固定的外部IP。是 NodePort 的超集。
- *ExternalName* - 通过返回带有该名称的 CNAME 记录，使用任意名称(由 spec 中的`externalName`指定)公开 Service。不使用代理。这种类型需要`kube-dns`的v1.7或更高版本。

使用8080端口暴露Service

```shell
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
```

查看Service详细信息

```shell
kubectl describe services/kubernetes-bootcamp
```

获取Service端口

```shell
export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
echo NODE_PORT=$NODE_PORT
```

通过端口请求服务，因为服务已经对外暴露，所以可以通过ip+端口的形式访问

