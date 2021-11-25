NIO优点：

1. 客户端的连接是异步
2. 读写异步
3. 线程模型的优化，不是一个连接一个线程

nio-v1.0示例代码

Server

```java
package channel;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Date;
import java.util.Iterator;
import java.util.Set;

/**
 * @author saijie.gao
 * @date 2021/11/22
 */
public class ServerChannel {


    public static void main(String[] args) throws IOException {

        //监听客户端链接
        ServerSocketChannel socketChannel = ServerSocketChannel.open();
        //绑定监听端口
        socketChannel.socket().bind(new InetSocketAddress(9000), 1024);
        //设置为非阻塞
        socketChannel.configureBlocking(false);
        //创建select,并注册到channel
        Selector selector = Selector.open();
        socketChannel.register(selector, SelectionKey.OP_ACCEPT);
        //输出日志
        System.out.println("Server is start in port :" + 9000);
        while(true){
            //selector 设置超时时间
            selector.select(1000);
            //获取所有的key(新的连接请求，消息发送请求)
            Set<SelectionKey> selectionKeys = selector.selectedKeys();
            //遍历 key
            Iterator<SelectionKey> iterator = selectionKeys.iterator();
            SelectionKey key = null;
            while (iterator.hasNext()) {
                key = iterator.next();
                //不移除会重复处理
                iterator.remove();
                //key的合法性判断
                if (key.isValid()) {
                    //新的连接
                    if (key.isAcceptable()) {
                        ServerSocketChannel channel = (ServerSocketChannel) key.channel();
                        SocketChannel socket = channel.accept();
                        socket.configureBlocking(false);
                        socket.register(selector, SelectionKey.OP_READ);
                    }
                    //客户端消息
                    if (key.isReadable()) {
                        SocketChannel channel = (SocketChannel) key.channel();
                        ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
                        int line = channel.read(byteBuffer);
                        if (line > 0) {
                            byteBuffer.flip();
                            byte[] bytes = new byte[byteBuffer.remaining()];
                            byteBuffer.get(bytes);
                            String body = new String(bytes, "UTF-8");
                            System.out.println("The server receive order : " + body);
                            String currentTime = new Date(System.currentTimeMillis()).toString();
                            ByteBuffer write = ByteBuffer.allocate(currentTime.getBytes().length);
                            write.put(currentTime.getBytes());
                            write.flip();
                            channel.write(write);
                        }
                    }
                }
            }
        }
    }
}


```

Client

```java
package channel;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;

/**
 * @author saijie.gao
 * @date 2021/11/25
 */
public class ClientChannel {


    public static void doWrite(SocketChannel socketChannel) throws IOException {
        byte[] req = "HELLO NIO".getBytes();
        ByteBuffer writeBuffer = ByteBuffer.allocate(req.length);
        writeBuffer.put(req);
        writeBuffer.flip();
        socketChannel.write(writeBuffer);
    }

    public static void main(String[] args) throws IOException {
        //Socket通道
        SocketChannel socketChannel = SocketChannel.open();
        //设置非阻塞模型
        socketChannel.configureBlocking(false);
        //创建select,并检测连接状态
        Selector selector = Selector.open();
        boolean connect = socketChannel.connect(new InetSocketAddress("127.0.0.1", 9000));
        if (connect) {
            //如果已经连接，注册READ到selector
            socketChannel.register(selector, SelectionKey.OP_READ);
            doWrite(socketChannel);
        } else {
            //没有连接，注册connect到连接状态
            socketChannel.register(selector, SelectionKey.OP_CONNECT);
        }
        while (true) {
            //阻塞
            selector.select(1000);
            //事件检测
            Set<SelectionKey> selectionKeys = selector.selectedKeys();
            Iterator<SelectionKey> iterator = selectionKeys.iterator();
            SelectionKey key = null;
            while (iterator.hasNext()) {
                key = iterator.next();
                iterator.remove();
                //事件合法性校验
                if (key.isValid()) {
                    //获取事件通道
                    SocketChannel sc = (SocketChannel) key.channel();
                    //连接事件
                    if (key.isConnectable()) {
                        //连接完成
                        if (sc.finishConnect()) {
                            //READ事件注册
                            sc.register(selector, SelectionKey.OP_READ);
                            //写请求
                            doWrite(sc);
                        } else {
                            System.exit(-1);
                        }
                    }
                    //READ事件
                    if (key.isReadable()) {
                        ByteBuffer readBuffer = ByteBuffer.allocate(1024);
                        int readBytes = sc.read(readBuffer);
                        if (readBytes > 0) {
                            readBuffer.flip();
                            byte[] bytes = new byte[readBuffer.remaining()];
                            readBuffer.get(bytes);
                            String body = new String(bytes, "UTF-8");
                            System.out.println("Body: " + body);
                        }else{
                            key.cancel();
                            sc.close();
                        }
                    }
                }
            }
        }
    }
}

```

