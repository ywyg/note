# Docker私有仓库

本文件记录docker私有仓库的创建流程，使用docker镜像创建

1. 执行仓库镜像

   ```shell
   docker run -d -p 5000:5000 --name registry_name registry:2
   ```

2. 拉取镜像测试

   ```shell
   docker pull ubuntu
   ```

3. 对新拉取镜像打标签

   ```shell
   docker image tag ubuntu localhost:5000/myimage
   ```

4. 推送到仓库

   ```shell
   docker push localhost:5000/myimage
   ```

5. 删除本地镜像

   ```shell
   docker image rm myimage
   ```

6. 从仓库拉取镜像

   ```shell
   docker pull localhost:5000/myimage
   ```

7. 查看镜像

   ```shell
   docker image list
   ```

8. 停止容器

   ```shell
   docker stop registry_name
   ```

   

增加远程访问支持，本方案使用SSL协议

1. 新建文件夹

   ```shell
   mkdir /var/lib/docker/certs
   cd /var/lib/docker
   mv XXX.crt ./certs
   mv XXX.key ./certs
   ```

2. 启动仓库镜像

   ```shell
   sudo docker run -d -p 5000:5000 --restart=always --name my-registry -v `pwd`/certs:/certs -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key registry:2
   ```

3. 对ubuntu镜像打新标签

   ```shell
   docker tag ubuntu happygao.top:5000/second_image
   ```

4. 推送到仓库

   ```shell
   docker push happygao.top:5000/second_image
   ```

5. 删除本地镜像

   ```shell
   docker image rm  happygao.top:5000/second_image
   ```

6. 重新拉取镜像

   ```shell
   docker pull happygao.top:5000/second_image
   ```

7. 查看镜像

   ```shell
   docker images
   ```

   