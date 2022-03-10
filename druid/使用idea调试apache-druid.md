# 使用Idea 调试 apache-druid

## 准备工作

1. JDK 8, 8u92+
2. [Maven version 3.x](http://maven.apache.org/download.cgi)
3. Distribution builds require Python 3.x and the `pyyaml` module
4. Zookeeper

## 下载

```git
git clone git@github.com:apache/druid.git
cd druid
```

## 编译

```mvn
mvn clean install -Pdist -DskipTests
```

提示：

> 如果出现错误，可以分别进入子模块编译

## 导入到Idea

1. 打开Idea后选择Open，选择 druid -> pom.xml ，点击打开

   提示：

   > 若是没有出现 druid 项目目录，选择 File -> Project Structure -> Modules -> import module 
   >
   > ​	选择 druid

2. 修改Idea配置

   1. File -> Project Structure 

      <font color="red">下图name处必须是1.8</font>

      ![image-20220310170038076](https://tva1.sinaimg.cn/large/e6c9d24ely1h04w6uw1whj21460u07bd.jpg)

   2. 设置 `Configuration Templates` ,选择左侧`JUnit`，`Choose coverage runner ` 选择`JaCoCo`

      提示: 

      > 如果没有这个选项，点击 `Modify options`  勾选`Show code coverage options`

   ![image-20220310170247320](https://tva1.sinaimg.cn/large/e6c9d24ely1h04w93df1pj210z0u077w.jpg)



## 配置

1. 打开.idea目录，检查是否存在`runConfigurations`目录，没有就创建一个

2. 新建文件

   * Historical.xml

     ```xml
     <component name="ProjectRunConfigurationManager">
       <configuration default="false" name="Historical" type="Application" factoryName="Application">
         <option name="ALTERNATIVE_JRE_PATH" value="1.8" />
         <option name="MAIN_CLASS_NAME" value="org.apache.druid.cli.Main" />
         <module name="druid-services" />
         <option name="PROGRAM_PARAMETERS" value="server historical" />
         <option name="VM_PARAMETERS" value="-server -Duser.timezone=UTC -Dfile.encoding=UTF-8 -Xmx2G -XX:MaxJavaStackTraceDepth=9999 -XX:+UseG1GC -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Dorg.jboss.logging.provider=slf4j -Dlog4j.configurationFile=$PROJECT_DIR$/examples/conf/druid/single-server/micro-quickstart/_common/log4j2.xml -Ddruid.host=localhost -Ddruid.service=historical -Ddruid.processing.buffer.sizeBytes=100000000 -Ddruid.extensions.hadoopDependenciesDir=$PROJECT_DIR$/distribution/target/hadoop-dependencies/ -Ddruid.extensions.directory=$PROJECT_DIR$/distribution/target/extensions/ -Ddruid.historical.cache.useCache=false -Ddruid.historical.cache.populateCache=false -Ddruid.segmentCache.locations=&quot;[{\&quot;path\&quot;:\&quot;/tmp/druid/indexCache\&quot;,\&quot;maxSize\&quot;:10000000000}]&quot; -Ddruid.zk.service.host=localhost -Ddruid.processing.numThreads=1 -Ddruid.server.http.numThreads=50 -Ddruid.serverview.type=batch -Ddruid.emitter=noop -Ddruid.metadata.storage.type=derby -Ddruid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/var/druid/metadata.db;create=true -Ddruid.metadata.storage.connector.host=localhost -Ddruid.metadata.storage.connector.port=1527" />
         <method v="2">
           <option name="Make" enabled="true" />
         </method>
       </configuration>
     </component>
     ```

   * Coordinator.xml

     ```xml
     <component name="ProjectRunConfigurationManager">
       <configuration default="false" name="Coordinator" type="Application" factoryName="Application">
         <option name="ALTERNATIVE_JRE_PATH" value="1.8" />
         <option name="MAIN_CLASS_NAME" value="org.apache.druid.cli.Main" />
         <module name="druid-services" />
         <option name="PROGRAM_PARAMETERS" value="server coordinator" />
         <option name="VM_PARAMETERS" value="-server -Xms2048m -Xmx2048m -XX:MaxDirectMemorySize=15360m -XX:+ExitOnOutOfMemoryError -XX:+UseG1GC -Duser.timezone=UTC -Dfile.encoding=UTF-8 -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Ddruidrole=coo -Djava.io.tmpdir=$USER_HOME$/local/tmp -Ddruid.service=coordinator -Dderby.stream.error.file=$USER_HOME$/local/druid/derby.log -Ddruid.plaintextPort=8081 -Ddruid.coordinator.startDelay=PT10S -Ddruid.coordinator.period=PT5S -Ddruid.coordinator.asOverlord.enabled=true -Ddruid.coordinator.asOverlord.overlordService=overlord -Ddruid.indexer.queue.startDelay=PT5S -Ddruid.indexer.storage.type=metadata -Ddruid.host=localhost -Ddruid.startup.logging.logProperties=true -Ddruid.zk.service.host=localhost -Ddruid.zk.paths.base=/druid -Ddruid.serverview.type=batch -Ddruid.metadata.storage.type=derby -Ddruid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/var/druid/metadata.db;create=true -Ddruid.metadata.storage.connector.host=localhost -Ddruid.metadata.storage.connector.port=1527 -Ddruid.storage.type=local -Ddruid.storage.storageDirectory=$USER_HOME$/local/druid/segments -Ddruid.indexer.logs.type=file -Ddruid.indexer.logs.directory=$USER_HOME$/local/druid/indexing-logs -Ddruid.selectors.indexing.serviceName=overlord -Ddruid.selectors.coordinator.serviceName=coordinator -Ddruid.emitter=noop -Ddruid.indexing.doubleStorage=double -Ddruid.sql.enable=true -Ddruid.sql.planner.useGroupingSetForExactDistinct=true -Ddruid.lookup.enableLookupSyncOnStartup=false -Ddruid.expressions.useStrictBooleans=true -Dorg.jboss.logging.provider=slf4j -Dlog4j.configurationFile=$PROJECT_DIR$/examples/conf/druid/single-server/micro-quickstart/_common/log4j2.xml" />
         <method v="2">
           <option name="Make" enabled="true" />
         </method>
       </configuration>
     </component>
     ```

   * Broker.xml

     ```xml
     <component name="ProjectRunConfigurationManager">
       <configuration default="false" name="Broker" type="Application" factoryName="Application">
         <option name="ALTERNATIVE_JRE_PATH" value="1.8" />
         <option name="MAIN_CLASS_NAME" value="org.apache.druid.cli.Main" />
         <module name="druid-services" />
         <option name="PROGRAM_PARAMETERS" value="server broker" />
         <option name="VM_PARAMETERS" value="-server -Xms2048m -Xmx2048m -XX:MaxDirectMemorySize=2048m -XX:+ExitOnOutOfMemoryError -XX:+UseG1GC -Duser.timezone=UTC -Dfile.encoding=UTF-8 -Ddruidrole=broker -Djava.io.tmpdir=$USER_HOME$/local/tmp -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Ddruid.service=broker -Ddruid.plaintextPort=8082 -Ddruid.server.http.numThreads=12 -Ddruid.broker.http.numConnections=10 -Ddruid.broker.http.maxQueuedBytes=5MiB -Ddruid.processing.buffer.sizeBytes=100MiB -Ddruid.processing.numMergeBuffers=2 -Ddruid.processing.tmpDir=$USER_HOME$/local/druid/processing -Ddruid.broker.cache.useCache=false -Ddruid.broker.cache.populateCache=false -Ddruid.host=localhost -Ddruid.startup.logging.logProperties=true -Ddruid.zk.service.host=localhost -Ddruid.zk.paths.base=/druid -Ddruid.serverview.type=batch -Ddruid.metadata.storage.type=derby -Ddruid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/var/druid/metadata.db;create=true -Ddruid.metadata.storage.connector.host=localhost -Ddruid.metadata.storage.connector.port=1527 -Ddruid.storage.type=local -Ddruid.storage.storageDirectory=$USER_HOME$/local/druid/segments -Ddruid.indexer.logs.type=file -Ddruid.indexer.logs.directory=$USER_HOME$/local/druid/indexing-logs -Ddruid.selectors.indexing.serviceName=overlord -Ddruid.selectors.coordinator.serviceName=coordinator -Ddruid.emitter=noop -Ddruid.indexing.doubleStorage=double -Ddruid.sql.enable=true -Ddruid.sql.planner.useGroupingSetForExactDistinct=true -Ddruid.lookup.enableLookupSyncOnStartup=false -Ddruid.expressions.useStrictBooleans=true -Dorg.jboss.logging.provider=slf4j -Dlog4j.configurationFile=$PROJECT_DIR$/examples/conf/druid/single-server/micro-quickstart/_common/log4j2.xml" />
         <method v="2">
           <option name="Make" enabled="true" />
         </method>
       </configuration>
     </component>
     ```

   * Router.xml

     ```xml
     <component name="ProjectRunConfigurationManager">
       <configuration default="false" name="Router" type="Application" factoryName="Application">
         <option name="ALTERNATIVE_JRE_PATH" value="1.8" />
         <option name="MAIN_CLASS_NAME" value="org.apache.druid.cli.Main" />
         <module name="druid-services" />
         <option name="PROGRAM_PARAMETERS" value="server router" />
         <option name="VM_PARAMETERS" value="-server -Xms2048m -Xmx2048m -XX:+UseG1GC -XX:MaxDirectMemorySize=2048m -XX:+ExitOnOutOfMemoryError -Duser.timezone=UTC -Dfile.encoding=UTF-8 -Ddruidrole=router -Djava.io.tmpdir=$USER_HOME$/local/tmp -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Ddruid.service=druid/router -Ddruid.plaintextPort=8888 -Ddruid.router.http.numConnections=50 -Ddruid.router.http.readTimeout=PT5M -Ddruid.router.http.numMaxThreads=100 -Ddruid.server.http.numThreads=100 -Ddruid.router.defaultBrokerServiceName=broker -Ddruid.router.coordinatorServiceName=coordinator -Ddruid.router.managementProxy.enabled=true -Ddruid.host=localhost -Ddruid.startup.logging.logProperties=true -Ddruid.zk.service.host=localhost -Ddruid.zk.paths.base=/druid -Ddruid.serverview.type=batch -Ddruid.metadata.storage.type=derby -Ddruid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/var/druid/metadata.db;create=true -Ddruid.metadata.storage.connector.host=localhost -Ddruid.metadata.storage.connector.port=1527 -Ddruid.storage.type=local -Ddruid.storage.storageDirectory=$USER_HOME$/local/druid/segments -Ddruid.indexer.logs.type=file -Ddruid.indexer.logs.directory=$USER_HOME$/local/druid/indexing-logs -Ddruid.selectors.indexing.serviceName=overlord -Ddruid.selectors.coordinator.serviceName=coordinator -Ddruid.emitter=noop -Ddruid.indexing.doubleStorage=double -Ddruid.sql.enable=true -Ddruid.sql.planner.useGroupingSetForExactDistinct=true -Ddruid.lookup.enableLookupSyncOnStartup=false -Ddruid.expressions.useStrictBooleans=true -Dorg.jboss.logging.provider=slf4j -Dlog4j.configurationFile= -Dlog4j.configurationFile=$PROJECT_DIR$/examples/conf/druid/single-server/micro-quickstart/_common/log4j2.xml" />
         <method v="2">
           <option name="Make" enabled="true" />
         </method>
       </configuration>
     </component>
     ```

   * MiddleManager.xml

     ```xml
     <component name="ProjectRunConfigurationManager">
       <configuration default="false" name="MiddleManager" type="Application" factoryName="Application">
         <option name="ALTERNATIVE_JRE_PATH" value="1.8" />
         <option name="MAIN_CLASS_NAME" value="org.apache.druid.cli.Main" />
         <module name="druid-services" />
         <option name="PROGRAM_PARAMETERS" value="server middleManager" />
         <option name="VM_PARAMETERS" value="-server -Xms2048m -Xmx2048m -XX:+ExitOnOutOfMemoryError -XX:+UseG1GC -Duser.timezone=UTC -Dfile.encoding=UTF-8 -Ddruidrole=mid -Djava.io.tmpdir=$USER_HOME$/local/tmp -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Ddruid.service=middleManager -Ddruid.plaintextPort=8091 -Ddruid.worker.capacity=2 -Ddruid.indexer.runner.javaOpts=-server -Xms1g -Xmx1g -XX:MaxDirectMemorySize=1g -Duser.timezone=UTC -Dfile.encoding=UTF-8 -XX:+ExitOnOutOfMemoryError -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Ddruid.indexer.task.baseTaskDir=$USER_HOME$/local/druid/task -Ddruid.server.http.numThreads=12 -Ddruid.indexer.fork.property.druid.processing.numMergeBuffers=2 -Ddruid.indexer.fork.property.druid.processing.buffer.sizeBytes=100MiB -Ddruid.indexer.fork.property.druid.processing.numThreads=1 -Ddruid.indexer.task.hadoopWorkingPath=$USER_HOME$/local/druid/hadoop-tmp -Ddruid.host=localhost -Ddruid.startup.logging.logProperties=true -Ddruid.zk.service.host=localhost -Ddruid.zk.paths.base=/druid -Ddruid.serverview.type=batch -Ddruid.metadata.storage.type=derby -Ddruid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/var/druid/metadata.db;create=true -Ddruid.metadata.storage.connector.host=localhost -Ddruid.metadata.storage.connector.port=1527 -Ddruid.storage.type=local -Ddruid.storage.storageDirectory=$USER_HOME$/local/druid/segments -Ddruid.indexer.logs.type=file -Ddruid.indexer.logs.directory=$USER_HOME$/local/druid/indexing-logs -Ddruid.selectors.indexing.serviceName=overlord -Ddruid.selectors.coordinator.serviceName=coordinator -Ddruid.emitter=noop -Ddruid.emitter.logging.logLevel=info -Ddruid.indexing.doubleStorage=double -Ddruid.sql.enable=true -Ddruid.sql.planner.useGroupingSetForExactDistinct=true -Ddruid.lookup.enableLookupSyncOnStartup=false -Ddruid.expressions.useStrictBooleans=true -Dorg.jboss.logging.provider=slf4j -Dlog4j.configurationFile=$PROJECT_DIR$/examples/conf/druid/single-server/micro-quickstart/_common/log4j2.xml" />
         <method v="2">
           <option name="Make" enabled="true" />
         </method>
       </configuration>
     </component>
     ```

提示:

> 需要建立 $USER_HOME$/local/tmp  目录

## 运行

* 打开ZooKeeper
* 依此运行5个节点任务



## 测试

打开浏览器，输入：http://localhost:8888 进入控制台

选择Load data -> paste Data ,粘贴测试数据

```
action_time,app_name,app_version,country,location,img_living_days,img_show_cnt,img_click_cnt,img_192_196_click_cnt,img_192_196_complete_cnt
2021-1-3,aiolos_gp,18,IN,new_coming,6,33,0,0,0
2020-1-4,aiolos_ip,23,US,new_comming2,1,0,0,0,0
2022-1-3,aiolos_gp,18,EG,new_coming,1,6,0,0,0
2022-1-3,aiolos_gp,18,US,picture,2,173,0,0,0
2022-1-3,aiolos_ip,22,JP,new_coming,10,1,0,0,0
2022-1-4,aiolos_gp,18,GB,new_coming,13,20,0,0,0
2022-1-3,aiolos_ip,23,GB,picture,32,8,0,0,0
2022-1-3,aiolos_ip,23,GB,picture,29,6,0,0,0
2022-1-4,aiolos_gp,18,DE,picture,53,4,0,0,0
2022-1-3,aiolos_ip,23,JP,picture,4,12,0,0,0
2022-1-4,aiolos_ip,23,US,for_you,21,0,0,0,0
2022-1-3,aiolos_ip,23,US,picture,354,1,0,0,0
2021-12-31,aiolos_gp,18,IN,new_coming,0,3,0,0,0
2022-1-4,aiolos_ip,23,BR,picture,4,9,0,0,0
2021-12-31,aiolos_ip,21,US,picture,5,1,0,0,0
2022-1-4,aiolos_ip,23,US,new_comming2,1,0,0,0,0
2022-1-3,aiolos_gp,18,MX,new_coming,2,147,0,0,0
2022-1-4,aiolos_gp,18,PL,picture,2,1,0,0,0
2022-1-3,aiolos_ip,23,JP,new_comming2,0,0,0,0,0
```

一路下一步，提交任务，完成摄取

![image-20220310163639639](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vhyh9nqj21c20u079d.jpg)

![image-20220310163746073](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vj1zf4nj21c00u079u.jpg)

![image-20220310163714131](https://tva1.sinaimg.cn/large/e6c9d24ely1h04wx0gxhyj21bm0u0jyc.jpg)

![image-20220310163801281](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vjbb4iqj21c00u0gr6.jpg)

![image-20220310163813127](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vjiwxqpj21c00u00y8.jpg)

![image-20220310163823298](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vjpfzanj21c00u0dmq.jpg)

![image-20220310163840968](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vk064frj21c00u00w0.jpg)

![image-20220310163856588](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vk9z1qrj21c00u0whd.jpg)

![image-20220310163921312](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vkph82zj21by0u0adj.jpg)

![image-20220310164108553](https://tva1.sinaimg.cn/large/e6c9d24ely1h04vmkg1w8j21c00u078i.jpg)

## 【参考资料】

* [源码构建druid](https://github.com/apache/druid/blob/master/docs/development/build.md)
* [在IDEA中运行druid](https://github.com/apache/druid/blob/master/dev/intellij-setup.md)