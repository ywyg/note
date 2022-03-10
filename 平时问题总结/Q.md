常见问题总结：

1. idea新导入项目不展示目录结构

> https://blog.csdn.net/qq_19642249/article/details/88681510

2. 端口占用

> ps -ef | grep port
>
> kill -9 threadNo

3. Idea 新建package没有新建类

> package不能使用关键字

4. 打包出现 BOOT-INF文件夹

> ```sh
> <plugin>
> <groupId>org.springframework.boot</groupId>
> <artifactId>spring-boot-maven-plugin</artifactId>
> <configuration>
> <skip>true</skip>
> </configuration>
> </plugin>
> ```

