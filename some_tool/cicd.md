# CI/CD流程

## 什么是CI/CD

> CI/CD是指持续集成（Continuous Integration）和持续交付/部署（Continuous Delivery/Deployment）的缩写。
>
> 持续集成（CI）是指将开发人员的代码变更自动集成到共享代码仓库中，并通过自动化测试、编译和构建等过程对代码进行验证和构建，以便快速发现和解决代码问题。 CI有助于加快代码交付的速度和质量，并提高开发团队的协作效率。
>
> 持续交付/部署（CD）是指将经过CI验证的代码自动部署到生产环境中，以便实现更快速的交付和响应需求。 CD包括自动化测试、构建、部署和监控等步骤，以确保交付的代码是稳定、可靠和安全的。
>
> CI/CD流程可以帮助开发团队更快速、更可靠地交付高质量的软件，同时减少代码错误和手动操作所引起的风险

## CI/CD的步骤是什么

1. 版本控制：使用一个版本控制系统（如Git）来存储所有的代码和文档，以便可以追踪和管理所有的变更和版本历史。
2. 自动化测试：使用自动化测试工具（如JUnit、Selenium等）来编写和运行测试用例，以便在代码修改后自动运行这些测试用例，以确保代码的正确性。
3. 构建自动化：使用构建工具（如Maven、Gradle等）来构建和打包应用程序，并将其部署到测试和生产环境中。
4. 自动化部署：使用自动化部署工具（如Jenkins、GitLab CI/CD、Travis CI等）来自动化部署应用程序到测试和生产环境中，以确保交付的代码是稳定、可靠和安全的。
5. 监控和日志记录：使用监控工具（如Prometheus、Grafana等）和日志记录工具（如ELK Stack）来监控应用程序的性能和运行情况，以及记录应用程序的日志信息，以便进行故障排查和问题分析。
6. 自动化回滚：在出现问题时，使用自动化回滚工具（如Rollback Wardog）来快速回滚到上一个稳定的版本，以避免影响用户体验和业务流程。

## 使用GitLab实现CI/CD

在此篇介绍中，我们使用`gitlab`作为我们的自动化部署工具，部署一个简单的web项目作为我们的测试用例

1. 创建GitLab项目：在GitLab中创建一个新项目，并将项目代码推送到GitLab仓库中。
2. 配置GitLab Runner：GitLab Runner是用于执行CI/CD任务的工具，可以在Linux、Windows或macOS上运行。需要在GitLab中注册一个Runner，并配置Runner运行的环境。
3. 配置CI/CD流水线：在GitLab项目中创建一个.gitlab-ci.yml文件，定义CI/CD流水线的各个阶段、任务和步骤。可以使用不同的脚本语言和命令，例如Shell脚本、Python、Ruby等。
4. 触发CI/CD流水线：在GitLab项目中进行代码提交或合并请求时，会自动触发CI/CD流水线的执行。也可以手动触发流水线的执行，以便进行测试、构建和部署。
5. 监控和管理CI/CD流水线：可以在GitLab中查看流水线的执行状态、日志和输出信息，以便进行故障排查和问题分析。还可以管理流水线的参数、环境变量、定时任务等。
6. 配置CD环境和自动化部署：可以使用GitLab CI/CD的自动化部署功能，将代码部署到测试、预生产和生产环境中。还可以使用其他CD工具，例如Kubernetes、Docker Swarm等，来实现自动化部署和容器编排。

## 配置GitLab Runner

具体步骤参见[此文章](https://happygao.top/index.php/2023/05/09/gitlab_runner%e6%b3%a8%e5%86%8c/)

## 创建项目

1. 登陆gitlab，选择create blank project，填写一下项目信息，我这里填的项目名是`CICDDemo`，添加SSH，克隆项目到本地，添加一个基本java项目，监听8080端口，对于任何请求，返回`Hello CI CD`

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230419193031777.png" alt="image-20230419193031777" style="zoom:50%;" />

1. 添加.gitlab-ci.yml和Dockerfile文件，具体内容如下

   .gitlab-ci.yml

   ```yaml
   image: docker:23.0-git
   
   stages:
     - build
     - deploy
   
   build-job:
     stage: build
     script:
       - mkdir $HOME/.ssh
       - echo "$SSH_PRIVATE_KEY" > $HOME/.ssh/id_rsa
       - "chmod 400 $HOME/.ssh/id_rsa"
       - "eval `ssh-agent -s`"
       - ssh-keyscan -H "gitlab.com" >> $HOME/.ssh/known_hosts
       - ssh-add $HOME/.ssh/id_rsa
       - git clone git@gitlab.com:ywyg/cicddemo.git
       - cd cicddemo
       - docker build -t cdemo .
       - docker tag cdemo happygao.top:5000/cdemo
       - docker push happygao.top:5000/cdemo
     only:
       refs:
         - tags
   
   deploy-job:
     stage: deploy
     environment: production
     script:
       - mkdir $HOME/.ssh
       - echo "$TC_KEY" > $HOME/.ssh/TC_login.pem
       - ssh -T -i $HOME/.ssh/TC_login.pem root@101.43.238.234
       - docker pull happygao.top:5000/cdemo
       - docker run -d -p 8080:8080 happygao.top:5000/cdemo --name cdemo
     only:
       refs:
         - tags
   ```

   Dockerfile

   ```dockerfile
   FROM maven:3.8.4-jdk-11-slim AS build
   COPY . /app
   WORKDIR /app
   RUN mvn clean package
   
   FROM adoptopenjdk/openjdk11:alpine-jre
   WORKDIR /app
   COPY --from=build /app/target/*.jar /app/cdemo.jar
   EXPOSE 8080
   ENTRYPOINT ["java","-jar","/app/cdemo.jar"]
   ```

### .gitLab-ci.yml

- image: docker:23.0-git

  image标签指定gitlab-runner所用镜像，当gitLab-ci.yml文件不指定镜像时，会使用配置GitLab Runner步骤过程选择的默认镜像，后续的所有脚本都会在这个镜像启动的容器内部运行

- stages:

  stages标签表明当前CI/CD流程存在的具体步骤，我这个项目包含build和deploy两个步骤

- build-job:

  stage表明当前job所属stage

  script:

  当前job需要执行的脚本，

```
    - mkdir $HOME/.ssh  #创建目录，用于存放ssh私钥文件
    - echo "$SSH_PRIVATE_KEY" > $HOME/.ssh/id_rsa #SSH_PRIVATE_KEY是一个变量，可以在gitlab项目setting-setting-variables处设置，此处表示的是私钥文件内容
    - "chmod 400 $HOME/.ssh/id_rsa" #添加读取权限
    - "eval `ssh-agent -s`" #启动ssh-agent代理程序
    - ssh-keyscan -H "gitlab.com" >> $HOME/.ssh/known_hosts
    # 获取gitlab.com的公钥信息并保存到known_hosts
    - ssh-add $HOME/.ssh/id_rsa #将私钥添加到 SSH agent 的进程中，后续链接gitlab.com不再需要使用密码
    - git clone git@gitlab.com:ywyg/cicddemo.git #clone项目到本地
    - cd cicddemo #进入项目目录
    - docker build -t cdemo . #构建镜像
    - docker tag cdemo happygao.top:5000/cdemo #对镜像打上目标仓库tag
    - docker push happygao.top:5000/cdemo #推送到私有仓库
  only: #只有以下分支才会触发ci流程
    refs:
      - tags
```













