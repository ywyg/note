# 故事的开始

1. 物理机
2. 虚拟机
3. 容器化

## 基本概念

* 镜像
* 容器
* Docker Server daemon
* Registry
* Docker Client
* 宿主机与容器

## DOCKER 执行流程

## Docker 生命周期

![image-20220201154846831](https://tva1.sinaimg.cn/large/008i3skNly1gyy26qcyuaj31h00scwhn.jpg)

## Dockerfile 构建镜像

```doc
FROM tomcat:latest  基准镜像
MAINTANIER 镜像维护机构
WORKDIR 切换工作目录
ADD 文件复制到镜像指定目录下
ENV 设置环境变量
RUN 在构建时执行命令
CMD 容器启动时执行默认命令或参数
ENTRYPOINT 容器启动时执行命令
```

构建镜像：

docker build -t 机构/镜像<:tags> Dockerfile目录

## 基础命令

docker pull image - name <:tags> --下载镜像

docker  images --查看本地镜像

docker run -d  -p image-name <:tags> -- 运行镜像，<-d> 后台运行，<-p>宿主机端口:docker 端口 ， PS:如果本地不存在会从仓库拉取后启动

docker ps --查看正在运行的镜像

docker rm <-f> 容器ID --删除容器 <-f>运行中删除

docker rmi <-f> image-name <:tags> 删除镜像 <-f> 存在存在容器镜像

Docker image rm -f image-name --强制删除镜像

Docker exec -it 容器Id 命令

## 示例（部署TOMCAT）

> https://hub.docker.com/ docker 镜像仓库

## 命令

netstat -tulpn 查看端口使用详情

/var/lib/docker  

