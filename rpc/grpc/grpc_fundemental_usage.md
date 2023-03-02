# gRPC

## 背景

* gRPC 一开始由 google 开发，是一款语言中立、平台中立、开源的远程过程调用(RPC)系统

* 支持语言

  * C++
  * Java
  * Python
  * C#
  * Go ....

* 开发理念：定义一个<b>*服务*</b>，指定其能够被远程调用的方法（包含参数和返回类型）。在服务端实现这个接口，并运行一个 gRPC 服务器来处理客户端调用。在客户端拥有一个*存根*能够像服务端一样的方法。

  > ![img](https://www.grpc.io/img/grpc_concept_diagram_00.png)

* 特点：

  * 使用 *proto files*  创建 gRPC 服务
  * 使用 Protocol buffers（数据格式，例如 Json）定义参数和返回值类型

## Quick Start

1. 下载 grpc

```sh
git clone -b v1.40.1 https://github.com/grpc/grpc-java
```

2. 进入examples

```sh
cd grpc-jave/example
```

3. 编译

```sh
./gradlew installDist
```

4. 项目导入IDEA

   * File - > Open  选中 example 目录

   * File - > Project Structure -> Modules 

     * 选中中间加号

       > ![截屏2021-09-17 上午11.27.10](/Users/saijie.gao/Desktop/截屏2021-09-17 上午11.27.10.png)

     * Import Module

       * 选择项目中的 build.gradle

5. 声明服务

   * grpc 使用 *.proto 声明服务,在该样例中使用 helloworld.proto
   * 其中Service 方法声明 Server 端，类似于注册中心
   * HelloRequest 声明请求参数
   * HelloReply 声明返回值类型

6. 启动Server端

   * 执行HelloWorldServer 启动Server 端
   * 出现 Server started, listening on 50051

7. 启动客户端

   * 执行HelloWorldClient  启动客户端

   * 出现 

        Will try to greet world ...

     ​	Greeting: Hello world

## 服务类型

grpc支持四种请求格式，分别如下：

* 单项RPC

  > 客户端向服务端发送一次请求，然后从服务端获取一次应答
  >
  > 类似于与普通的函数调用
  >
  > eg .
  >
  > ​	rpc Server(HelloRequse) return (HelloResponse){}

* 服务端流式RPC

  > 客户端向服务端发送一次请求，然后从服务端获取一个数据流
  >
  > eg.
  >
  > ​	rpc Server(HelloRequse) return ( stream HelloResponse){}

* 客户端流式RPC

  > 客户端提供一个数据流写入并发送到服务端，然后等待服务端读取后返回应答
  >
  > eg.
  >
  > ​	rpc Server(stream HelloRequse) return (HelloResponse){}

* 双向流式RPC

  > 客户端和服务端双向使用流式发送或者接受信息
  >
  > eg.
  >
  > ​	rpc Server(stream HelloRequse) return (stream HelloResponse){}

## 自定义gRPC (单项RPC)

1. 新建iden项目，构建方式选择 gradle

2. 在 src -> main 目录下新建文件夹 proto

3. 在proto 下新建文件 add.proto

   ```protobuf
   //语法格式
   syntax = "proto3";
   
   option java_multiple_files = true;
   
   // 生成服务所在包和类名
   option java_package = "AddRPC";
   option java_outer_classname = "AddService";
   
   //提供的服务方法
   service add{
     rpc addNum(Request) returns (Response){}
   }
   
   //定义参数 ，a,b 的值不可以相等
   message Request {
       int32 a = 1 ;
       int32 b = 2 ;
   }
   
   //定义返回值
   message Response{
     int32 c = 1;
   }
   ```

4. 打开 build.gradle

   ```groovy
   plugins {
       // Java 插件
       id 'java'
     	// protobuf 插件
       id 'com.google.protobuf' version '0.8.17'
   }
   
   group 'com.gs'
   version '1.0-SNAPSHOT'
   
   repositories {
       maven { // The google mirror is less flaky than mavenCentral()
           url "https://maven-central.storage-download.googleapis.com/maven2/" }
       mavenCentral()
   }
   
   def grpcVersion = '1.40.1' // CURRENT_GRPC_VERSION
   def protobufVersion = '3.17.2'
   def protocVersion = protobufVersion
   
   
   // 引入google处理
   protobuf {
       protoc { artifact = "com.google.protobuf:protoc:${protocVersion}" }
       plugins {
           grpc { artifact = "io.grpc:protoc-gen-grpc-java:${grpcVersion}" }
       }
       generateProtoTasks {
           all()*.plugins { grpc {} }
       }
   }
   
   dependencies {
       implementation "io.grpc:grpc-protobuf:${grpcVersion}"
       implementation "io.grpc:grpc-stub:${grpcVersion}"
       compileOnly "org.apache.tomcat:annotations-api:6.0.53"
       implementation "com.google.protobuf:protobuf-java-util:${protobufVersion}"
       runtimeOnly "io.grpc:grpc-netty-shaded:${grpcVersion}"
       testImplementation "io.grpc:grpc-testing:${grpcVersion}"
       testImplementation "junit:junit:4.12"
       testImplementation "org.mockito:mockito-core:3.4.0"
   }
   //定义编译完成的输出路径
   sourceSets {
       main {
           java {
               srcDirs 'build/generated/source/proto/main/grpc'
               srcDirs 'build/generated/source/proto/main/java'
           }
       }
   }
   test {
       useJUnitPlatform()
   }
   ```

5. 编译，生成 gRPC服务

   > 选择 gradle 菜单，选择 Task -> other -> generateProto，双击
   >
   
6. 在main->java目录下添加包 AddRPC

   1. 在 AddRPC包下添加 AddServer

   ```java
   package AddRPC;
   
   /**
    * @author saijie.gao
    * @date 2021/9/18
    */
   
   //addGrpc.addImplBase 该 class 是抽象类，需要自定义实现，也就是需要实现Server中定义的 addNum
   public class AddServer extends addGrpc.addImplBase {
   
       @Override
       public void addNum(Request request, StreamObserver<Response> responseObserver) {
   			//产生客户端响应信息
           Response reply = Response.newBuilder().setC(request.getA()+request.getB()).build();
         	//响应客户端
           responseObserver.onNext(reply);
         	//向客户端返回响应完成
           responseObserver.onCompleted();
       }
   
       public static void main(String[] args) throws InterruptedException, IOException {
         	//开启服务监听9090端口，gRPC Server端是新开一个线程去执行监听作业，没有使用main线程，所以需要start,
            ServerBuilder.forPort(9090).addService(new AddServer()).build().start();
         //因为Server 是后台线程，所以main线程不关闭
           while (true){}
       }
   }
   
   ```

   2. 在 AddRPC包下添加 AddClient

   ```java
   package AddRPC;
   
   import io.grpc.ManagedChannel;
   import io.grpc.ManagedChannelBuilder;
   import io.grpc.stub.CallStreamObserver;
   
   /**
    * @author saijie.gao
    * @date 2021/9/18
    */
   public class AddClient {
   
       public static void main(String[] args) {
          //服务配置等信息
          ManagedChannel managedChannel = ManagedChannelBuilder
           .forTarget("localhost:9090").usePlaintext().build();
          //addGrpc.addBlockingStub 该对象负责 Client 与服务的交互，所以要将配置信息给到此对象
         	addGrpc.addBlockingStub addBlockingStub = addGrpc.newBlockingStub(managedChannel);
          //配置请求信息
          Request request = Request.newBuilder().setA(100).setB(2).build();
          //得到响应结果
          Response response = addBlockingStub.addNum(request);
          //输出响应结果	
          System.out.println(response.getC());
       }
   }
   ```

## 自定义RPC（双向流式RPC）

1. 新建iden项目，构建方式选择 gradle

2. 在 src -> main 目录下新建文件夹 proto

3. 在proto 下新建文件 encrypt

   ```protobuf
   syntax = "proto3" ;
   
   option java_multiple_files = true ;
   option java_package = "com.gv.streamGRPC" ;
   option java_outer_classname = "Encrypt";
   
   message Request{
     int32 id = 1;
     string name = 2;
   }
   
   message Response{
     string nameAfterEncrypt = 1;
   }
   
   service encryptService{
     rpc encrypting (stream Request) returns (stream Response){}
   }
   ```

4. 打开 build.gradle

   ```groovy
   plugins {
       // Java 插件
       id 'java'
     	// protobuf 插件
       id 'com.google.protobuf' version '0.8.17'
   }
   
   group 'com.gs'
   version '1.0-SNAPSHOT'
   
   repositories {
       maven { // The google mirror is less flaky than mavenCentral()
           url "https://maven-central.storage-download.googleapis.com/maven2/" }
       mavenCentral()
   }
   
   def grpcVersion = '1.40.1' // CURRENT_GRPC_VERSION
   def protobufVersion = '3.17.2'
   def protocVersion = protobufVersion
   
   
   // 引入google处理
   protobuf {
       protoc { artifact = "com.google.protobuf:protoc:${protocVersion}" }
       plugins {
           grpc { artifact = "io.grpc:protoc-gen-grpc-java:${grpcVersion}" }
       }
       generateProtoTasks {
           all()*.plugins { grpc {} }
       }
   }
   
   dependencies {
       implementation "io.grpc:grpc-protobuf:${grpcVersion}"
       implementation "io.grpc:grpc-stub:${grpcVersion}"
       compileOnly "org.apache.tomcat:annotations-api:6.0.53"
       implementation "com.google.protobuf:protobuf-java-util:${protobufVersion}"
       runtimeOnly "io.grpc:grpc-netty-shaded:${grpcVersion}"
       testImplementation "io.grpc:grpc-testing:${grpcVersion}"
       testImplementation "junit:junit:4.12"
       testImplementation "org.mockito:mockito-core:3.4.0"
   }
   //定义编译完成的输出路径
   sourceSets {
       main {
           java {
               srcDirs 'build/generated/source/proto/main/grpc'
               srcDirs 'build/generated/source/proto/main/java'
           }
       }
   }
   test {
       useJUnitPlatform()
   }
   ```

5. 编译，生成 gRPC服务

   > 选择 gradle 菜单，选择 Task -> other -> generateProto，双击
   >
   
6. 在main->java目录下添加包 com.gv

   1. 在 com.gv 包下添加 RpcServer

   ```java
   package com.gv;
   
   /**
    * @author saijie.gao
    * @date 2021/9/18
    */
   public class RpcServer {
   
       private Server server;
   
       public static void main(String[] args) throws IOException, InterruptedException {
           RpcServer streamGRPC = new RpcServer();
           //rpc Server Service
           RpcServerStream rpcServer = new RpcServerStream();
           streamGRPC.server = ServerBuilder.forPort(9090).addService(rpcServer).build();
           //开始监听
           streamGRPC.server.start();
           System.out.println("开始监听");
           //保持活跃状态
           streamGRPC.server.awaitTermination();
       }
   }
   
   ```

   2. 新建 RpcServerStream class

   ```java
   package com.gv;
   
   import com.gv.streamGRPC.Request;
   import com.gv.streamGRPC.Response;
   import com.gv.streamGRPC.encryptServiceGrpc;
   import io.grpc.stub.ServerCallStreamObserver;
   import io.grpc.stub.StreamObserver;
   
   /**
    * @author saijie.gao
    * @date 2021/9/18
    */
   public class RpcServerStream extends encryptServiceGrpc.encryptServiceImplBase {
   
       @Override
       public StreamObserver<Request> encrypting(StreamObserver<Response> responseObserver) {
   
           //stream
           final ServerCallStreamObserver<Response> serverCall = (ServerCallStreamObserver<Response>) responseObserver;
   
           //手动控制请求
           serverCall.disableAutoRequest();
   
           //流量控制对象
           final RpcServerReady rpcServerReady = new RpcServerReady(serverCall);
   
           //设置流量控制到当前 流式请求
           serverCall.setOnReadyHandler(rpcServerReady);
   
           //返回响应结果
           return new RpcServerStreamObServer(serverCall,responseObserver,rpcServerReady);
   
       }
   }
   
   ```
   3. 新建 RpcServerReady class

   ```java
   package com.gv;
   
   import com.gv.streamGRPC.Response;
   import io.grpc.stub.ServerCallStreamObserver;
   
   /**
    * @author saijie.gao
    * @date 2021/9/18
    */
   public class RpcServerReady implements Runnable{
   
       private ServerCallStreamObserver<Response> serverCallStreamObserver;
       public boolean isReady = false;
   
       public RpcServerReady(ServerCallStreamObserver<Response> streamObserver){
           this.serverCallStreamObserver = streamObserver;
       }
   
       @Override
       public void run() {
           if(serverCallStreamObserver.isReady() && !isReady){
               isReady = true;
               serverCallStreamObserver.request(1);
           }
       }
   }
   
   ```

   4. 新建 RpcServerStreamObServer class

   ```java
   package com.gv;
   /**
    * @author saijie.gao
    * @date 2021/9/18
    */
   public class RpcServerStreamObServer implements StreamObserver<Request> {
   
       private ServerCallStreamObserver<Response> serverCall ;
       private StreamObserver<Response> streamObserver;
       private RpcServerReady rpcServerReady;
   
       public RpcServerStreamObServer(ServerCallStreamObserver<Response> ser,
                                      StreamObserver<Response> stream,
                                      RpcServerReady rpcServerReady){
           this.serverCall = ser;
           this.streamObserver = stream;
           this.rpcServerReady = rpcServerReady;
       }
   
       @Override
       public void onNext(Request request) {
           try {
               String name = request.getName();
               Integer id = request.getId();
               String afterStr = EncryptService.afterEncrypt(name, id);
   
               System.out.println("++++++++++++THIS++++++++++");
               System.out.println(name + ":" + id);
   
               Response response = Response.newBuilder().
                       setNameAfterEncrypt(afterStr).build();
   
               streamObserver.onNext(response);
               if (serverCall.isReady()) {
                   serverCall.request(1);
               } else {
                   rpcServerReady.isReady = false;
               }
       }catch (Throwable throwable) {
           throwable.printStackTrace();
           streamObserver.onError(
                   Status.UNKNOWN.withDescription("Error handling request").withCause(throwable).asException());
       }
       }
   
       @Override
       public void onError(Throwable t) {
           streamObserver.onCompleted();
       }
   
       @Override
       public void onCompleted() {
           streamObserver.onCompleted();
       }
   }
   ```

   5. 新建 RpcClient class

   ```java
   package com.gv;
   
   /**
    * @author saijie.gao
    * @date 2021/9/18
    */
   public class RpcClient {
   
       public static void main(String[] args) throws InterruptedException {
           ManagedChannel channel = ManagedChannelBuilder.forTarget("localhost:9090").usePlaintext().build();
           encryptServiceGrpc.encryptServiceStub encryptService  = encryptServiceGrpc.newStub(channel);
           StreamObserver<Request> request =  encryptService.encrypting(new RpcClientStreamObserver());
           Thread.sleep(100000);
       }
   }
   ```

   6. 新建 RpcClientStreamObserver class

   ```java
   package com.gv;
   
   import com.gv.streamGRPC.Request;
   import com.gv.streamGRPC.Response;
   import io.grpc.stub.ClientCallStreamObserver;
   import io.grpc.stub.ClientResponseObserver;
   
   /**
    * @author saijie.gao
    * @date 2021/9/18
    */
   public class RpcClientStreamObserver implements ClientResponseObserver<Request, Response> {
   
       private ClientCallStreamObserver<Request> requestStream;
   
       @Override
       public void beforeStart(final ClientCallStreamObserver<Request> requestStream) {
           this.requestStream = requestStream;
         	
           //每次一条请求？
           requestStream.disableAutoRequestWithInitial(1);
         	//手动流量控制
           requestStream.setOnReadyHandler(new Runnable() {
               @Override
               public void run() {
                   int i = 0;
                   System.out.println("this"+requestStream.isReady());
                   while(requestStream.isReady()){
                       if(i++ < 10){
                           String name = name();
                           System.out.println(i+name);
                         	//请求对象
                           Request request = Request.newBuilder().setId(i).setName(name).build();
                           //发送请求对象
                         	requestStream.onNext(request);
                           System.out.println("请求已经发送");
                       }else{
                           requestStream.onCompleted();
                       }
                   }
               }
           });
       }
   
       @Override
       public void onNext(Response value) {
           System.out.println("<-----" + value.getNameAfterEncrypt());
           requestStream.request(1);
       }
   
       @Override
       public void onError(Throwable t) {
           requestStream.request(1);
       }
   
       @Override
       public void onCompleted() {
           System.out.println(".........OVER.........");
       }
   
       public Integer id(){
           return Math.round(1000f);
       }
   
       public String name(){
           int begin = 'A';
           return  "" + (char)(begin + id()%26 + +id()%6);
       }
   }
   
   ```

   