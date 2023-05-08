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

### 创建项目

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230419193031777.png" alt="image-20230419193031777" style="zoom:50%;" />

选择Create black project，填写一下项目信息，我这里填的项目名是`CICDDemo`，添加SSH，克隆项目到本地，添加一个基本java项目，监听80端口，返回`Hello CI CD`

1. 新建项目
2. 添加Dockerfile

## 配置GitLab Runner

由于我使用的`MAC OS`，所以这里就以此系统为例演示：其他操作可参考[官方文档](https://docs.gitlab.com/runner/install/)

1. 下载`GitLab Runner`可执行文件

   ```shell
   sudo curl --output /usr/local/bin/gitlab-runner "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-darwin-amd64"
   ```

2. 添加权限

   ```shell
   sudo chmod +x /usr/local/bin/gitlab-runner
   ```

3. 启动`GitLab Runner`

   ```shell
   gitlab-runner install
   gitlab-runner start
   ```

4. 重启计算机

5. 注册`GitLab Runner`到`GitLab`

   1. 打开GitLab页面，点击project->setting->CI/CD

   2. 选择Runner，expand

      <img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230420100340710.png" alt="image-20230420100340710" style="zoom:50%;" />

   3.  复制「And this registration token」内容

      ```shell
      sudo gitlab-runner register --url https://gitlab.com/ --registration-token $REGISTRATION_TOKEN 
      ```

   4. 在安装GitLab Runner的机器上执行命令，使用刚才复制的「And this registration token」替换 `$REGISTRATION_TOKEN `

      ```shell
      sudo gitlab-runner register --url https://gitlab.com/ --registration-token $REGISTRATION_TOKEN 
      ```

   5. 按要求输入一些配置信息，完成后可以在GitLab Runner处看到配置的Runner信息

      

      

      

      






