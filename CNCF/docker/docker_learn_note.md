[TOC]

## 这是Docker

> *an open-source project that automates the deployment of software applications inside* **containers** *by providing an additional layer of abstraction and automation of* **OS-level virtualization** *on Linux.*      
>
> -- from wikipedia



换句话说，Docker可以使开发者们可以在Linux这些的常见系统上轻松的部署应用，Docker的强大之处在于允许开发者把打包部署操作转换成编辑文件，在这个文件中，你可以填入项目的所有依赖，而不像虚拟机那样，因为可以更加高效的使用系统和资源，所以容器化不需要很大的开销。

现在的行业标准是使用虚拟机运行应用，虚拟机在操作系统提供的虚拟硬件设备上运行运行应用。虚拟机提供了非常好的应用隔离，主机上的其他应用与虚拟机上的应用几乎不会互相影响，但是为了主机需要维持虚拟机的稳定会产生巨大的资源消耗。容器则是采用了不同的方案，通过主机操作系统的低级隔离机制，容器使用计算的方式实现虚拟机上的绝大多的隔离效果。

容器提供了一种将应用从运行环境抽象出来的打包机制，这种机制使得应用的部署更加简单并且始终如一，无论最终应用需要部署在什么环境，是云服务器亦或者个人主机，用户都清楚部署完成效果，并且不会对主机上的其他应用产生影响。

鉴于Docker的种种优点，Docker得到了广泛使用，各大公司利用Docker提高大型工程团队的效率和对计算资源的利用率，并且，Google把缩减整个数据中心的功劳归功于Docker。



## 还没开始？

本次学习除了基础的命令行和文件编辑之外，不需要你有什么更高级的水平，本次教程需要使用的内容包含git以及AWS和DockerHub账号，所以你可以提前注册，

- [Amazon Web Services](http://aws.amazon.com/)
- [Docker Hub](https://hub.docker.com/)

### 安装并且启动看看

学习Docker的第一步一定是安装Docker，你可以通过这些教程在你的设备上安装Docker [Mac](https://docs.docker.com/docker-for-mac/install), [Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu) 和 [Windows](https://docs.docker.com/docker-for-windows/install).

当你完成了安装，测试一下是否成功，像这样

```shell
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
719385e32844: Pull complete
Digest: sha256:fc6cf906cbfa013e80938cdf0bb199fbdbb86d6e3e013783e5a766f50f5dbce0
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### 看个例子！

当你正确打印出来`hello_world`，意味着你可以安装任何软件了，现在体验第一个Docker项目的安装吧！

[BusyBox](https://baike.baidu.com/item/busybox/427860) 是这次需要安装的项目，第一步：

```shell
$ docker pull busybox
```

使用Docker拉`busybox`镜像，如果遇到 *permission denied* 问题，尝试使用*sudo* 

看一下拉取结果

```shell
$ docker imges
REPOSITORY  TAG  	IMAGE ID  		CREATED   			SIZE
busybox   latest af2c3e96bcf1   3days ago      4.86MB
```

看上去没有任何问题，让我们使用`docker run`启动一下

```shell
$ docker run busybox
$
```

Wow! 没有任何输出，是出了什么问题吗？显然不是，当我们执行`docker run busybox`命令时，Docker在后台做了很多工作，首先Docker会在images中找到对应的image(在这个例子是busybox)，然后装载容器，并执行命令，由于我们并没有提供任何命令，所以busybox再启动之后发现没有任务需要做就直接退出了，现在我们给他一个命令

```shell
$ docker run busybox echo "hello-docker"
hello-docker
```

可能你也发现了，Docker运行busybox的速度是很快的，确实不向虚拟机那样臃肿，这确实很酷。接下来，我们熟悉下一个命令`docker ps`

```shell
$ docker ps
CONTAINER ID   IMAGE  COMMAND  CREATED        STATUS      PORTS     NAMES
```

由于现在没有应用再跑，所以我们只能看到一些标题，使用`docker ps -a`查看更多

```shell
$ docker ps -a
CONTAINER ID   IMAGE  	COMMAND  							CREATED    STATUS      							PORTS     NAMES
20b6761e1e95   busybox  "echo hello-docker"  5 minutes ago Exited (0) 5 minutes ago                              				recursing_bell
224b0ca266b8   busybox  "sh"  							11 minutes ago Exited (0)11 minutes ago                      				exciting_williamson
```

使用`docker ps -a`，可以直观的看到我们刚才运行的容器，并且在 *STATUS* 可以发现它们都在几分钟前退出了。

或许可以看看容器内部到底是什么？

```shell
$ docker run -it busybox sh
/ # pwd
/
/ # ls
bin    dev    etc    home   lib    lib64  proc   root   sys    tmp    usr    var
/ # uptime
 09:14:27 up 6 days,  2:43,  0 users,  load average: 0.00, 0.00, 0.00
```

在`run`命令上使用 *- it* 参数可以打开一个交互终端，在这个终端执行任何命令，包括`rm -rf /`当然你得再确认一下你是在容器内部还是你的主机上，不然的话，一切都晚了～～～

假设你的PC上有一些不会再用到的东西，你肯定会选择删除，在Docker这里也是一样，使用`docker ps -a`看到了好多容器遗骸，正确的决定显然是删除他们，试一下

```shell
$ docker rm 20b6761e1e95 224b0ca266b8
20b6761e1e95
224b0ca266b8
$ docker ps -a 
CONTAINER ID   IMAGE  COMMAND  CREATED        STATUS      PORTS     NAMES
```

在这个例子中我们只有两个容器需要删除，简单的复制粘贴也很容易，但是如果有很多的容器需要删除，就需要想别的办法了，比如通过选择的方式

```shell
$ docker rm $(docker ps -a -q -f status=exited)
```

*-a* 的作用我们已经知道，*-q* 、*-f*  的作用也很简单，*-q* 的作用是只返回Container ID，*-f*  的作用是添加一个filter，在当前例子中，filter过滤status=exited的容器，所以整个命令的含义是删除所有 status=exited 的容器，当然，我们也可以在`run`命令时指定*--rm* ，表示容器结束后自动删除，就像这样

```shell
$ docker run --rm busybox
```

在最新版的Docker中，你甚至可以使用`docker container prune`代替`docker rm $(docker ps -a -q -f status=exited) `

当然，如果你要删除image，可以使用`docker rmi`命令

### 是不是有点迷惑？

上面的例子提到了很多专有名词，像image、container ... 你可能会有些迷惑，这都是啥？在继续学习之前，我们还是需要了解一下这些概念的

- *Image* : 镜像是应用的描述文件，如果你是一个Javaer，可以把镜像理解为Class，他只是一堆静态的文件集合，在我们的例子中，`docker pull busybox` 拉取的就是image。
- *Containers* : 容器是实际跑起来的应用，可以理解为Java中的对象，可以根据Class产生，在我们的例子中，`docker run busybox`中`run`起来的是容器，可以使用`docker ps`查看正在运行的容器，
- *Docker Daemon* : 守护进程是管理Docker Containers的后台进程，运行在与客户端交互的主机上。
- *Docker Client* : Docker 客户端是与守护进程通讯的命令行终端，当然 [Kitematic](https://kitematic.com/) 是图形化的客户端。
- *Docker Hub* : Docker仓库，存放常见的image，当使用`docker run`运行本地不存在镜像时，Docker会从Docker Hub拉取新的镜像并且运行。

## 可以开始了！！！

在上面的例子中，我们启动的都是一些demo程序，通过那些demo，你应该也明白了一些概念，现在是时候实地演练一番了。

`prakhar1989/static-site`是一个非常简单的静态网站应用，启动这个项目

```shell
$ docker run --rm -it prakhar1989/static-site
Unable to find image 'prakhar1989/static-site:latest' locally
......
Status: Downloaded newer image for prakhar1989/static-site:latest
Nginx is running...
```

经过之前的学习，这行命令的作用你肯定十分清楚，*--rm* 表示容器结束后删除容器，*-it* 表示开启一个交互式终端，因为我们本地没有这个镜像，所以Docker会去仓库拉取。当启动完成，可以在终端看到`Nginx is running...`既然是一个网站，肯定应该提供接受请求的端口，但是使用`docker run --rm -it prakhar1989/static-site`启动并没有看到这些信息，使用`Ctrl+C`关闭容器，使用一条新的命令启动

```shell
$ docker run -d -P --name static-site prakhar1989/static-site
```

又有新的参数出现，不要急，*-d* 是让容器在后台运行，如果不使用这个参数，在终端启动的容器会随着终端的关闭而退出，显然容器与终端的绑定关系是我们不需要的。*-P* 是让应用暴露的端口与主机上随机的一个端口进行绑定，这样我们就可以通过访问主机上的端口进而访问到容器内的应用。*--name* 则是给此刻运行的容器命名。使用*-P* 暴露的端口可以使用`docker port [container_name]`查看。

```shell
$ docker port static-site
443/tcp -> 0.0.0.0:55000
80/tcp -> 0.0.0.0:55001
```

现在，可以访问http://localhost:55001访问应用，试一下吧～

如果不想使用随机的端口，则可以手动指定映射的端口，就像这样

```shell
$ docker stop static-site
$ docker rm static-site
$ docker run -d -p 8888:80 --name static-site prakhar1989/static-site
```

现在，可以访问http://localhost:8888访问试一下～ 在刚才手动指定映射端口之前，先停止了之前的服务，然后删除，是的，很简单的逻辑，不过可以补充一下，`docker stop `后面还可以使用` container_id`，`docker rm`也是。

## 有自己的镜像会很酷

在前面的学习中，我们学习了一些知识，不过当你学完这一节，肯定会对镜像有更加深入的理解。

镜像是容器的基本，先看一下本地都有哪些镜像

```shell
$ docker images
REPOSITORY                      TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
prakhar1989/catnip              latest              c7ffb5626a50        2 hours ago         697.9 MB
prakhar1989/static-site         latest              b270625a1631        21 hours ago        133.9 MB
python                          3-onbuild           cf4002b2c383        5 days ago          688.8 MB
martin/docker-cleanup-volumes   latest              b42990daaca2        7 weeks ago         22.14 MB
ubuntu                          latest              e9ae3c220b23        7 weeks ago         187.9 MB
busybox                         latest              c51f86c28340        9 weeks ago         1.109 MB
hello-world                     latest              0a6ba66e537a        11 weeks ago  
```

`TAG`列记录的是镜像的快照版本，`IMAGE ID `则是镜像的唯一身份标识。如果不指定镜像的版本，Docker默认会拉取最新的镜像`Tag : latest`，两种方式的写法都很简单

```shell
$ docker pull ubuntu
$ docker pull ubuntu:18.04
```

### 镜像也分两种

- 基础镜像：系统级别镜像，如ubuntu、debian、python等这些镜像主要提供一个类似于主机的环境，在这些镜像的基础上，我们可以构建自己应用镜像。
- 应用镜像：提供各种各样的服务，如mysql、nginx、tomcat这些，提供一个应用本身的支持。

### 现在开始创建一个自己镜像

克隆`docker-curriculum.git`项目到本地

```shell
$ git clone https://github.com/prakhar1989/docker-curriculum.git
$ cd docker-curriculum/flask-app
```

### Dockerfile

我们应该如果做一个镜像呢？答案是使用Dockerfile文件，是的，文件名就是Dockerfile，Docker Client可以按照Dockerfile内容步骤执行，最终产生一个你想要的镜像，听上去并不困难，实际上也是这样，所以你可能关注如何编写Dockerfile？

`docker-curriculum.git`是一个应用，所以我们要创建一个应用镜像，正如上面提到的，应用镜像一般是在基于基础镜像构建，所以我们需要依赖一个基础镜像，`docker-curriculum.git`是用`Python`开发的，所以我们需要`Python`的基础镜像，在Dockerfile中添加对`Python`镜像的依赖

1. 新建一个Dockerfile文件然后添加下面内容

   ```dockerfile
   From python:3.8
   ```

2. 设置工作目录

   ```dockerfile
   WORKDIR /usr/src/app
   ```

3. 复制文件到容器内部

   ```dockerfile
   COPY . .
   ```

4. 安装Python依赖

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

5. 暴露应用对外端口，因为`docker-curriculum.git`运行在5000端口，所以我们对外暴露 5000端口

   ```dockerfile
   EXPOSE 5000
   ```

6. 最后是容器启动后执行的命令，这里我们启动应用

   ```dockerfile
   CMD ["python", "./app.py"]
   ```

完整的Dockerfile

```dockerfile
FROM python:3.8

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./app.py"]
```

在我们克隆下载项目中也有一个Dockerfile，可以和我们刚写的对比检查是否一致，把我们写的Dockerfile复制到`flask-app`目录下，下面就可以使用Docker Client来构建镜像了,

```shell
$ cd docker-curriculum/flask-app
$ docker build -t cutesquirrel/catnip .
```

使用`docker images`查看build结果，运行看看

```shell
$ docker run -p 8888:5000 cutesquirrel/catnip
```

点击http://localhost:8888 查看可爱小猫，没有人不会喜欢吧🐱～～～

## 分享给世界

文章开始的地方，有Docker Hub账号注册的链接，众所周知，Docker Hub是一个镜像仓库，所以当我们把自己镜像推送Docker Hub仓库，所有人都可以下载并且运行我们的镜像，这是一件很酷的事情，并且它并不复杂，只需要简单的几步。

### 登录，还是登录

想要推送镜像到仓库，第一步就是登录，很简单，使用`Docker login`命令就可以

```shell
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: cutesquirrel
Password:
Login Succeeded
```

现在就可以把我们制作的cutesquirrel/catnip推送到仓库了，很简单

```shell
$ docker push cutesquirrel/catnip
```

在[这里](https://hub.docker.com/repository/docker/cutesquirrel/catnip/general)可以看到刚刚的推送结果。现在我们的镜像已经分享给了世界，具体有多少人使用可能是一个玄学问题？任何一个人都可以运行我们的镜像，相比于过去的应用部署，使用Docker不知道简单了多少倍。

```shell
$ docker run -d -p 8888:5000 cutesquirrel/catnip
```

### 要AWS?

在上一步我们成功将镜像推送到Docker仓库，按照计划学习顺序，我们应该继续部署项目到云服务器上，方便所有人访问，遗憾的是，我并没有准备申请AWS账号，而我有一个腾讯云的服务器可以用，所以对于部署这部分内容，就不再讲解AWS部署过程，感兴趣的同学可以去[官网](https://docker-curriculum.com/#:~:text=first%20docker%20image.-,Docker%20on%20AWS,-What%20good%20is)查看，其实部署到腾讯云和本地部署并无差别，只是腾讯云可以被大家访问到，这点我的主机显然是做不到的。

- 登录我的腾讯云终端

  ```shell
  $ ssh -i local/my.pem root@xxx.xx.xxx.xxx
  ```

- 运行应用

  ```shell
  $ docker run -d -p 8080:5000 cutesquirrel/catnip
  ```

  因为我已经安装过Docker，所以直接使用`docker`命令，别忘了在防火墙打开8080端口，不要忘记我们是把镜像推送到Docker Hub，如果你本地或者云服务器的Docker修改了仓库源是找不到我们的镜像的，删除`/etc/docker/daemon.json`可使用默认仓库，即Docker Hub

- 看看效果http://101.43.238.234:8080，暴露收藏夹了😂

  ![image-20230516144159778](https://raw.githubusercontent.com/ywyg/photo/main/image-20230516144159778.png)

## 都是单体应用？

到这里你已经学会了一个简单的Docker镜像的创建、容器的运行、部署等等知识，但是，这些都是一个个单独的应用，真正的应用不是这样的，它们往往需要很多应用的配合，例如`MySQL`的持久存储、`Redis`记录等等，所以我们应该学习如何搭建一个真正的Docker项目。

这次我们以「FoodTrucks」项目为例，它使用`Elasticsearch`提供搜索服务，同样的，我们可以在github下载这个项目

```shell
$ git clone https://github.com/prakhar1989/FoodTrucks
$ cd FoodTrucks
$ tree -L 2
.
├── Dockerfile
├── README.md
├── aws-ecs
│   └── docker-compose.yml
├── docker-compose.yml
├── flask-app   
│   ├── app.py
│   ├── package-lock.json
│   ├── package.json
│   ├── requirements.txt
│   ├── static
│   ├── templates
│   └── webpack.config.js
├── setup-aws-ecs.sh
├── setup-docker.sh
├── shot.png
└── utils
    ├── generate_geojson.py
    └── trucks.geojson
```

`flask-app` 文件包含一些Python应用，`utils`包含一些将数据加载到`Elasticsearch`的程序。

就像我们提到的，我们需要一个`Elasticsearch`应用，还记得上面的`docker search`命令吗？试着在仓库搜索一下，看看有哪些镜像？

```shell
$ docker search elasticsearch
NAME                                               DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
elasticsearch                                      Elasticsearch is a powerful open source sear…   6066      [OK]
kibana                                             Kibana gives shape to any kind of data — str…   2598      [OK]
bitnami/elasticsearch                              Bitnami Docker Image for Elasticsearch          64                   [OK]
rapidfort/elasticsearch                            RapidFort optimized, hardened image for Elas…   10
bitnami/elasticsearch-exporter                     Bitnami Elasticsearch Exporter Docker Image     5                    [OK]
bitnami/elasticsearch-curator                                                                      2
......
```

果然存在`Elasticsearch`的官方镜像，用就用官方的，靠谱！！！

```shell
$ docker pull elasticsearch
Using default tag: latest
Error response from daemon: manifest for elasticsearch:latest not found: manifest unknown: manifest unknown
$ docker pull elasticsearch:7.17.9
```

使用`docker pull elasticsearch`拉取镜像时报错，镜像不存在，在Docker Hub查看发现没有提供latest标签镜像，所以手动添加`7.17.9`标签继续，注意，你在执行的时候可能`7.17.9`标签也不存在了，所以需要去[官网](https://hub.docker.com/_/elasticsearch/tags)查看可用标签。

拉取完成后就可以运行了，由于`Elasticsearch`一般使用集群模式启动，在这里我们不需要这样，所以指定一下以单节点模式`discovery.type=single-node`启动

```shell
$ docker run -d --name es -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.17.9
```

简单补充一下`Elasticsearch`的知识，`Elasticsearch`使用9200端口提供REST API ，通过访问 `http://localhost:9200`，可以与 Elasticsearch 进行交互，并执行各种操作，例如索引数据、搜索、检索集群状态等，`Elasticsearch`使用9300端口与其他`Elasticsearch`节点通信，保持集群的可用。

简单看一下`Elasticsearch`日志，观察服务状态

```shell
$ docker container logs es
```

![image-20230516163703073](https://raw.githubusercontent.com/ywyg/photo/main/image-20230516163703073.png)

请求Elasticsearch接口

```shell
$ curl localhost:9200
{
  "name" : "4153354ee798",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "NSPSL7QQSoWNWh3J__GiQA",
  "version" : {
    "number" : "7.17.9",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "ef48222227ee6b9e70e502f0f0daa52435ee634d",
    "build_date" : "2023-01-31T05:34:43.305517834Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

在我们「FoodTrucks」项目下还有有一个Dockerfile文件，内容是这样的

```dockerfile
# start from base
FROM ubuntu:18.04

LABEL maintainer="Prakhar Srivastav <prakhar@prakhar.me>"

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python3-pip python3-dev curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
RUN apt-get install -yq nodejs

# copy our application code
ADD flask-app /opt/flask-app
WORKDIR /opt/flask-app

# fetch app specific deps
RUN npm install
RUN npm run build
RUN pip3 install -r requirements.txt

# expose port
EXPOSE 5000

# start app
CMD [ "python3", "./app.py" ]
```

这个Dockerfile与前面的相比多了很多东西，让我们简单说明一下，不同于python:3.8，在这个Dockerfile文件中，我们使用ubuntu:18.04作为基础镜像，apt-get是ubuntu的包管理应用，使用它安装我们需要的依赖（node和python）, *-yqq* 可以帮助我们在apt-get命令执行过程中出现提示时自动处理。ADD 命令可以将「FoodTrucks」项目下的 flask-app目录拷贝到/opt/flask-app，使用WORKDIR设置/opt/flask-app为我们的工作目录。node安装完成后就可以使用npm命令了，它将按照flask-app/package.json定义的那样去运行build 命令，最后安装python的依赖包，暴露5000端口定义启动后的命令就完成了这个Dockerfile文件的内容。现在可以构建镜像了。

```shell
$ docker build -t cutesquirrel/foodtrucks-web .
```

首次执行肯定会慢一些，不过不用着急，等它结束，然后运行看看～～

```shell
$ docker run --rm -P 8888:5000 cutesquirrel/foodtrucks-web
Unable to connect to ES. Retying in 5 secs...
Unable to connect to ES. Retying in 5 secs...
Unable to connect to ES. Retying in 5 secs...
```

连不上ES，Why? 我们试着分析一下，现在，我们有两个容器，

- `foodtrucks-web`  暴露了5000端口，容器启动时把容器的5000端口与本地8888端口进行绑定，所以我们可以访问到5000端口

- `Elasticsearch`  暴露了9200端口，容器启动时把容器的9200端口与本地9200端口进行绑定，所以我们可以使用`curl localhost:9200`请求到ES应用信息

`foodtrucks-web` 是不能够访问到`curl localhost:9200`的，因为它的容器内部9200端口是空闲的，没有任务服务运行在这里，也就是下图这种关系

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230516172059855.png" alt="image-20230516172059855" style="zoom:40%;" />

现在的问题清楚了，那你可能会说，那启动`foodtrucks-web` 项目是添加一个端口映射不就好了，让Host的9200也和foodtrucks-web的9200完成绑定。我们可以试一下

```shell
$ docker run --rm -p 8888:5000 -p 9200:9200  cutesquirrel/foodtrucks-web
docker: Error response from daemon: driver failed programming external connectivity on endpoint focused_chatelet (6dfcb2aa143e2223bf7c9c78defeeec7cb5d5a74e1fd2310da0b9bef05492de8): Bind for 0.0.0.0:9200 failed: port is already allocated.
```

显然，Host的9200端口是不能重复使用的。那该怎么办呢？

我们先看一下app是怎么去链接ES的，在app.py中，可以看到

```python
es = Elasticsearch(host='es')
```

好像凭借之前的知识无法解决这个问题，那么这个问题Docker到底是怎么处理的呢？好的，我们需要一个新的命令`docker network ls`，当Docker安装的时候，它会同步的创建三条网络。

```shell
$ docker network ls
NETWORK ID     NAME       DRIVER    SCOPE
9b11ed9167ce   bridge     bridge    local
884e61cc18c6   host       host      local
12f4db5f72b8   none       null      local
```

容器启动时默认使用bridge网络，我们可以看一下是不是这样？

```shell
$ docker network inspect bridge
[
    {
        "Name": "bridge",
        "Id": "9b11ed9167ce9d437eaa18c2974b00a0f114f1aba37e679993a7396493c25c41",
        "Created": "2023-05-08T12:17:07.396263618Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16",
                    "Gateway": "172.17.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "4153354ee798554ac8071768586ed6664a3645a439beb65f935d8cb3e2020739": {
                "Name": "es",
                "EndpointID": "5ed677345a37e71c7f55deaf8c2dce0f2a97947cb7ec361657770bb7dfd5bb69",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]
```

在Containers属性下，有一个4153354ee79855... Id，这是哪个容器Id呢，我们查看一下

```shell
$ docker ps | grep 4153354ee
4153354ee798   elasticsearch:7.17.9              "/bin/tini -- /usr/l…"   About an hour ago   Up About an hour   0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   es
```

很显然，是`elasticsearch:7.17.9`容器，那么

```json
"MacAddress": "02:42:ac:11:00:02",
"IPv4Address": "172.17.0.2/16",
```

是这个容器的网络地址吗？我们进入容器检查一下

```shell
$ docker exec -it es /bin/sh
sh-5.0# curl 172.17.0.2:9200
{
  "name" : "4153354ee798",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "NSPSL7QQSoWNWh3J__GiQA",
  "version" : {
    "number" : "7.17.9",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "ef48222227ee6b9e70e502f0f0daa52435ee634d",
    "build_date" : "2023-01-31T05:34:43.305517834Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

没有问题，确实是它，但是，，，是不是没什么用？不过我们还是了解了一点关于Docker network的知识，Docker对于这种问题的解决方案是——允许连接到同一个桥接网络的容器进行通信，没有连接到同一个网络的相互隔离，所以我们新建一个网络连接。

```shell
$ docker network create foodtrucks-net 
$ docker network ls
NETWORK ID     NAME             DRIVER    SCOPE
9b11ed9167ce   bridge           bridge    local
34e94c2f066d   foodtrucks-net   bridge    local
884e61cc18c6   host             host      local
12f4db5f72b8   none             null      local
```

现在使用新建的网络连接

```shell
$ docker stop es
$ docker rm es
$ docker run -d -p 9200:9200 -p 9300:9300 --net foodtrucks-net --name es -e "discovery.type=single-node" elasticsearch:7.17.9
7167070c75662155930bdc88e2d50a49473a13fe5206a1360722485f03c317a5
$ docker network inspect foodtrucks-net
[
    {
        "Name": "foodtrucks-net",
        "Id": "34e94c2f066de52063273a8e084c474a28db1eaedb59e468908167bce2592a42",
        "Created": "2023-05-16T11:11:03.9095813Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "7167070c75662155930bdc88e2d50a49473a13fe5206a1360722485f03c317a5": {
                "Name": "es",
                "EndpointID": "f5e657bcf5b740442ad4775b890ae2139cd12b4a4fd8a4a2cd3f56d3d2013646",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

可以看到，ES使用了`foodtrucks-net`网络，

```shell
$ docker run --rm -p 8888:5000 --net foodtrucks-net cutesquirrel/foodtrucks-web
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
......
```

YES ！！！`cutesquirrel/foodtrucks-web`服务成功的运行起来了。让我们访问http://localhost:8888

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230516192420589.png" alt="image-20230516192420589" style="zoom:40%;" />

可能你觉得过去了很久，反正我认为有一段时间了，但是这个标题下，我们只执行了几行命令而已，Docker 就是很简洁

```shell
# build the flask container
$ docker build -t cutesquirrel/foodtrucks-web .

# create the network
$ docker network create foodtrucks-net

# start the ES container
$ docker run -d --name es --net foodtrucks-net -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.17.9

# start the flask app container
$ docker run -d --net foodtrucks-net -p 8888:5000 cutesquirrel/foodtrucks-web
```

这组命令可以在「FoodTrucks」项目下的setup-docker.sh中找到。

## 放松一下

了解到很多的Docker知识？还差的远呢，上面提到的都是Docker Client相关的知识，在Docker大家庭还有很多其他的服务值得探索。

- [Docker Machine](https://docs.docker.com/desktop/) : 创建你自己的Docker主机
- [Docker Compose](https://docs.docker.com/compose/) : 一个定义和管理Docker容器的额工具
- [Docker Swarm](https://docs.docker.com/swarm/) : 本地Docker集群解决方案
- [Kubernetes](https://kubernetes.io/) : 一个自动部署、伸缩和容器管理的开源系统

### 浅看一下Docker Compose

解决多个容器互相协作的问题，Docker 很强大，但是毕竟只是进程级别的应用，所以我们需要Docker Compose，使用`Docker run app` 代替 `Docker run container`的时代来了。

你再也不需要一个个的启动容器，搭建网络，使用Docker Compose，仅仅需要一个`docker-compose.yml`文件，所有的服务将会有条不紊的启动。又一个很酷的组件出现了。

让我们使用Docker Compose重新部署「FoodTrucks」项目，是不是真的那么厉害？

首先，如果你是Windows或者Mac用户，Docker Compose会在你安装Docker的时候一块安装，Linux 用户可以参考这个[教程](https://docs.docker.com/compose/install/)，或者使用`pip`安装`pip install docker-compose`，检查一下是否安装成功

```shell
$ docker-compose --version
docker-compose version 1.29.2, build 5becea4c
```

现在我们新建一个`docker-compose.yml`文件，用来实现「FoodTrucks」项目

```yaml
version: "3.8"
services: 
	es:
    image: elasticsearch:7.17.9
    container_name: es 
    environment:
      - discovery.type=single-node
    ports:
      - 9200:9200
    volumes:
      - esdata1:/usr/share/elasticsearch/data
  web:
    image: cutesquirrel/foodtrucks-web
    container_name: web
    command: python3 app.py
    depends_on:
      - es
    ports:
      - 5000:5000
    volumes:
      - ./flask-app:/opt/flask-app
volumes:
  esdata1:
    driver: local
```

对你来说，这个文件的内容有些陌生，不过不用着急，每一行都会解释到。

yaml文件首先定义了`version`、`services`、`volumes`三组父级属性，表示当前`docker-compose`的版本、需要启动的服务和服务挂载卷。

`es`和`web`是需要运行的两个服务，通过image参数指定镜像的版本

- container_name： 容器名
- environment：容器启动时环境变量
- ports：容器与主机端口映射
- volumes：挂载卷位置，当容器重启后可以保证数据的持久化
- command：容器启动后执行命令
- depends_on：依赖服务名，必须是依赖的服务启动完成才能启动自身服务

可以在[官网](https://docs.docker.com/compose/compose-file/#depends_on)参考更多参数

现在让我们停止「FoodTrucks」项目，并且使用`docker-compose启动服务`,不要进错目录，必须在「FoodTrucks」目录内执行命令。

```shell
$ docker stop es foodtrucks-web
$ docker rm es foodtrucks-web
$ docker-compose up
```

> 如果看到一下内容
>
> ```shell
> web_1  | Unable to connect to ES. Retrying in 5 secs...
> web_1  | Unable to connect to ES. Retrying in 5 secs...
> web_1  | Unable to connect to ES. Retrying in 5 secs...
> web_1  | Out of retries. Bailing out...
> ```
>
> 说明Web服务无法连接到ES，原因是ES此刻没能提供服务，按照正常的逻辑来讲，我们需要等ES服务跑起来再运行Web服务就行。所以我们修改一下Command命令
>
> `command: bash -c "while ! curl -s es:9200 > /dev/null; do echo waiting for es; sleep 3; done; python3 app.py"`

```shell
web_1  |  * Serving Flask app "app" (lazy loading)
web_1  |  * Environment: production
web_1  |    WARNING: This is a development server. Do not use it in a production deployment.
web_1  |    Use a production WSGI server instead.
web_1  |  * Debug mode: off
web_1  | /usr/local/lib/python3.6/dist-packages/requests/__init__.py:91: RequestsDependencyWarning: urllib3 (1.26.15) or chardet (3.0.4) doesn't match a supported version!
web_1  |   RequestsDependencyWarning)
web_1  | /usr/local/lib/python3.6/dist-packages/elasticsearch/connection/base.py:200: ElasticsearchWarning: Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.17/security-minimal-setup.html to enable security.
web_1  |   warnings.warn(message, category=ElasticsearchWarning)
web_1  |  * Running on all addresses.
web_1  |    WARNING: This is a development server. Do not use it in a production deployment.
web_1  |  * Running on http://172.24.0.3:5000/ (Press CTRL+C to quit)
```

这样，我们就通过docker-compose将服务重新运行起来，看一下状态http://localhost:5000

和Docker一样，Docker-compose也支持*-d* 后台启动，*ps* 查看容器状态

```shell
$ docker-compose up -d
Starting es ... done
Starting foodtrucks_web_1 ... done
$ docker-compose ps
      Name                    Command               State                Ports
--------------------------------------------------------------------------------------------
es                 /bin/tini -- /usr/local/bi ...   Up      0.0.0.0:9200->9200/tcp, 9300/tcp
foodtrucks_web_1   bash -c while ! curl -s es ...   Up      0.0.0.0:5000->5000/tcp
```

好的，现在我们看一下怎么关闭服务

```shell
$ docker-compose down -v
Stopping foodtrucks_web_1 ... done
Stopping es               ... done
Removing foodtrucks_web_1 ... done
Removing es               ... done
Removing network foodtrucks_default
Removing volume foodtrucks_esdata1
```

在Docker-compose中，我们不在需要手动执行`stop`、`rm`这些命令，只需要`docker-compose down -v`这样一行简单的命令就可以替代我们之前繁琐的工作。Greate!!!

做一下最后的梳理，在这个项目里Docker_Compose到底为我们做了什么？按照我们手工部署项目的经验，应该有这些工作被完成。

- 建立网络
- 启动ES
- 启动Web

是这样的吗？我们检验一下，首先删除`foodtrucks-net`

```shell
$ docker network rm foodtrucks-net
$ docker network ls
NETWORK ID          NAME                 DRIVER              SCOPE
c2c695315b3a        bridge               bridge              local
a875bec5d6fd        host                 host                local
ead0e804a67b        none                 null                local
```

使用`docker-compose up -d`启动服务

```shell
$ docker-compose up -d
Recreating es
Recreating foodtrucks_web_1

$ docker container ls
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS              PORTS                    NAMES
f50bb33a3242        yourusername/foodtrucks-web  "python3 app.py"         14 seconds ago      Up 13 seconds       0.0.0.0:5000->5000/tcp   foodtrucks_web_1
e299ceeb4caa        elasticsearch                "/docker-entrypoint.s"   14 seconds ago
```

网络呢？

```shell
$ docker network ls
NETWORK ID          NAME                 DRIVER
c2c695315b3a        bridge               bridge              local
f3b80f381ed3        foodtrucks_default   bridge              local
a875bec5d6fd        host                 host                local
ead0e804a67b        none                 null                local
```

显然，`foodtrucks_default`网络之前是不存在的，那么这个网络都有哪些容器接入呢？查询一下

```shell
$ docker network inspect foodtrucks_default
[
    {
        "Name": "foodtrucks_default",
        "Id": "f3b80f381ed3e03b3d5e605e42c4a576e32d38ba24399e963d7dad848b3b4fe7",
        "Created": "2018-07-30T03:36:06.0384826Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": true,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "7640cec7feb7f5615eaac376271a93fb8bab2ce54c7257256bf16716e05c65a5": {
                "Name": "foodtrucks_web_1",
                "EndpointID": "b1aa3e735402abafea3edfbba605eb4617f81d94f1b5f8fcc566a874660a0266",
                "MacAddress": "02:42:ac:13:00:02",
                "IPv4Address": "172.19.0.2/16",
                "IPv6Address": ""
            },
            "8c6bb7e818ec1f88c37f375c18f00beb030b31f4b10aee5a0952aad753314b57": {
                "Name": "es",
                "EndpointID": "649b3567d38e5e6f03fa6c004a4302508c14a5f2ac086ee6dcf13ddef936de7b",
                "MacAddress": "02:42:ac:13:00:03",
                "IPv4Address": "172.19.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {
            "com.docker.compose.network": "default",
            "com.docker.compose.project": "foodtrucks",
            "com.docker.compose.version": "1.21.2"
        }
    }
]
```

从Containers参数下可以清楚的看到，` "Name": "es"`，` "Name": "foodtrucks_web_1"`两个服务都接入了`foodtrucks_default`网络，和我们手动部署时的效果时一样。经过检查，Docker-Compose实现的效果和我们的猜想是一致的。没有问题 😊

### 怎么进入DEBUG模式呢？

DEBUG模式允许我们随时修改代码并且在容器内生效，首先让我们启动服务，并检查一下服务状态

```shell
$ docker-compose up -d
Creating network "foodtrucks_default" with the default driver
Creating volume "foodtrucks_esdata1" with local driver
Creating es ... done
Creating foodtrucks_web_1 ... done
$ curl http://localhost:5000
<!DOCTYPE html>
<html>
<head>
......
</head>
</html>
```

没问题，下一步，我们访问一下`hello`接口

```shell
$ curl http://localhost:5000/hello
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
$ curl http://localhost:5000/debug
```

`hello`接口不存在？是的，因为我们根本没有开发这个接口，在app.py中可以清楚的看到，只提供了三个接口的实现。

```python
@app.route('/')
@app.route('/debug')
@app.route('/search')
```

在当前状态下，即使我们在app.py添加hello接口也是不能提供服务的，因为服务已经启动，没办法重启读取app.py文件了。让我们试一下，首先在app.py增加

```python
@app.route('/hello')
def hello():
  return "hello world!"
```

增加完效果代码结构应该是这样的：

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230521103943678.png" alt="image-20230521103943678" style="zoom:50%;" />

保存后，继续访问http://localhost:5000/hello 看上去是不太行哦！所以DEBUG模式应该是怎样的呢？

让我们关闭服务`docker-compose down -v`，打开docker-compose.yml，修改web service内容：

```shell
version: "3.8"
services:
  es:
    image: elasticsearch:7.17.9
    container_name: es
    environment:
      - discovery.type=single-node
    ports:
      - 9200:9200
    volumes:
      - esdata1:/usr/share/elasticsearch/data
  web:
    build: .
    command: bash -c "while ! curl -s es:9200 > /dev/null; do echo waiting for es; sleep 3; done; python3 app.py"
    environment:
      - DEBUG=True 
    depends_on:
      - es
    ports:
      - 5000:5000
    volumes:
      - ./flask-app:/opt/flask-app
volumes:
    esdata1:
      driver: local
```

修改完成后删除对app.py增加的hello接口内容，使用`docker-compose up -d`启动服务，此时会重新build镜像，是正常的，稍等片刻，等服务启动后重新修改app.py，增加hello接口，继续访问测试http://localhost:5000/hello 

一切是是正常的，现在我们可以随时修改app.py文件，并且可以实时看到修改完成的效果哦～～

> 使用docker-compose 启动服务需要一定的时间，可以使用`docker ps`或者`docker-compose ps`查看服务状态。一切正常，没有故障，请放心测试

## 还差什么？

经过这个教程的简单学习，你肯定对Docker有了基本的了解，但是，这仅仅是开始，就像是海滩的贝壳，海里还有更漂亮，更美丽的贝壳，加油吧骚年，后面我们应该了解一下

- Dockerfile的编写
- Docker的原理
- ......











