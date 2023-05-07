## Tomcat目录介绍

![image-20230316192230875](/Users/saijie.gao/Library/Application%20Support/typora-user-images/image-20230316192230875.png)

这是tomcat 安装好之后的目录

- bin：包含二进制文件和脚本
- conf：配置文件
- lib：项目所需jar文件，比如JDBD等
- logs：日志文件，报错信息在这里面
- temp：运行过程中产生的临时文件
- webapps：放置着你需要部署的项目war包
- work：工作目录

### conf

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230316192725788.png" alt="image-20230316192725788" style="zoom:50%;" />

这里面最主要的配置文件有三个，分别是`context.xml`、`server.xml`、`web.xml`

`server.xml`

> 运行时服务端配置

`web.xml`

> HTTP请求处理配置

`context.xml`

> tomcat运行时上下文配置，可修改为热部署(只对静态资源有效，servlet无效)，生产环境不推荐

### 新建WEB服务

1. 在web-apps目录下建立`hello/WEB-INF/classes`目录
   - hello目录是项目的根目录，所有的可查看资源都在这层目录下面
   - WEB-INF目录下保存web.xml文件，这部分内容用户是无法查看的
   - classes目录保存java class

2. 在hello目录下新建`HelloHome.html`

   ```html
   <!DOCTYPE html>
   <html>
     <head><title>My Home Page</title></head>
     <body>
       <h1>Hello, world!</h1>
       <p>My Name is so and so. This is my HOME.</p>
     </body>
   </html>
   ```

   <img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230316194812845.png" alt="image-20230316194812845" style="zoom:50%;" />

​	此时，访问 `http://localhost:9999/hello/HelloHome.html `，就可以看到上面写的页面。并且，如果将`HelloHome.html`修改为`index.html`,那么访问`http://localhost:9999/hello`也能访问到上述页面。

3. 使用java程序编写的`servlet`

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230316195750266.png" alt="image-20230316195750266" style="zoom:50%;" />

在classes目录下新建`HelloServlet.java`

使用`javac`编译代码

```java
javac -cp ./XXX/lib/servlet-api.jar HelloServlet.java
```

生成`HelloServlet.class`

```java

// To save as "<TOMCAT_HOME>\webapps\hello\WEB-INF\classes\HelloServlet.java"
import java.io.*;
import jakarta.servlet.*;             // Tomcat 10
import jakarta.servlet.http.*;        // Tomcat 10
import jakarta.servlet.annotation.*;  // Tomcat 10
//import javax.servlet.*;             // Tomcat 9
//import javax.servlet.http.*;        // Tomcat 9
//import javax.servlet.annotation.*;  // Tomcat 9
 
@WebServlet("/sayhello")   // Configure the request URL for this servlet (Tomcat 7/Servlet 3.0 upwards)
public class HelloServlet extends HttpServlet {

   // The doGet() runs once per HTTP GET request to this servlet.
   @Override
   public void doGet(HttpServletRequest request, HttpServletResponse response)
         throws IOException, ServletException {
 
      // Set the response MIME type of the response message
      response.setContentType("text/html");
      // Allocate a output writer to write the response message into the network socket
      PrintWriter out = response.getWriter();
 
      // Write the response message, in an HTML page
      out.println("<!DOCTYPE html>");
      out.println("<html>");
      out.println("<head><title>Hello, World</title></head>");
      out.println("<body>");
      out.println("<h1>Hello, world!</h1>");  // says Hello
      // Echo client's request information
      out.println("<p>Request URI: " + request.getRequestURI() + "</p>");
      out.println("<p>Protocol: " + request.getProtocol() + "</p>");
      out.println("<p>PathInfo: " + request.getPathInfo() + "</p>");
      out.println("<p>Remote Address: " + request.getRemoteAddr() + "</p>");
      // Generate a random number upon each request
      out.println("<p>A Random Number: <strong>" + Math.random() + "</strong></p>");
      out.println("</body></html>");
      out.close();  // Always close the output writer
   }
}
```

重启Tomcat服务，输入`http://localhost:9999/hello/sayhello`查看`Servlet`返回页面

4. 包含SQL查询的Servlet服务

首先，本地需要安装mysql

```mysql
create database if not exists ebookshop;

use ebookshop;

drop table if exists books;
create table books (
   id     int,
   title  varchar(50),
   author varchar(50),
   price  float,
   qty    int,
   primary key (id));

insert into books values (1001, 'Java for dummies', 'Tan Ah Teck', 11.11, 11);
insert into books values (1002, 'More Java for dummies', 'Tan Ah Teck', 22.22, 22);
insert into books values (1003, 'More Java for more dummies', 'Mohammad Ali', 33.33, 33);
insert into books values (1004, 'A Cup of Java', 'Kumar', 55.55, 55);
insert into books values (1005, 'A Teaspoon of Java', 'Kevin Jones', 66.66, 66);

select * from books;
```

下载`Mysql-JDBC`驱动到lib目录下，[下载地址](https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.11/mysql-connector-java-8.0.11.jar)

编写`querybook.html`代码

```html
<!DOCTYPE html>
<html>
<head>
  <title>Yet Another Bookshop</title>
</head>
<body>
  <h2>One More Bookshop</h2>
  <form method="get" action="http://localhost:9999/hello/query">
    <b>Choose an author:</b>
    <input type="checkbox" name="author" value="Tan Ah Teck" />Ah Teck
    <input type="checkbox" name="author" value="Mohammad Ali" />Ali
    <input type="checkbox" name="author" value="Kumar" />Kumar
    <input type="submit" value="Search" />
  </form>
</body>
</html>
```

`querybook`请求服务开发

```java
// To save as "<TOMCAT_HOME>\webapps\hello\WEB-INF\classes\QueryServlet.java".
import java.io.*;
import java.sql.*;
import jakarta.servlet.*;             // Tomcat 10
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
//import javax.servlet.*;             // Tomcat 9
//import javax.servlet.http.*;
//import javax.servlet.annotation.*;

@WebServlet("/query")   // Configure the request URL for this servlet (Tomcat 7/Servlet 3.0 upwards)
public class QueryServlet extends HttpServlet {

   // The doGet() runs once per HTTP GET request to this servlet.
   @Override
   public void doGet(HttpServletRequest request, HttpServletResponse response)
               throws ServletException, IOException {
      // Set the MIME type for the response message
      response.setContentType("text/html");
      // Get a output writer to write the response message into the network socket
      PrintWriter out = response.getWriter();

      // Print an HTML page as the output of the query
      out.println("<!DOCTYPE html>");
      out.println("<html>");
      out.println("<head><title>Query Response</title></head>");
      out.println("<body>");

      try (
         // Step 1: Allocate a database 'Connection' object
         Connection conn = DriverManager.getConnection(
               "jdbc:mysql://localhost:3306/ebookshop?allowPublicKeyRetrieval=true&useSSL=false&serverTimezone=UTC",
               "你的登陆名", "你的密码");   // For MySQL
               // The format is: "jdbc:mysql://hostname:port/databaseName", "username", "password"

         // Step 2: Allocate a 'Statement' object in the Connection
         Statement stmt = conn.createStatement();
      ) {
         // Step 3: Execute a SQL SELECT query
         String sqlStr = "select * from books where author = "
               + "'" + request.getParameter("author") + "'"   // Single-quote SQL string
               + " and qty > 0 order by price desc";

         out.println("<h3>Thank you for your query.</h3>");
         out.println("<p>Your SQL statement is: " + sqlStr + "</p>"); // Echo for debugging
         ResultSet rset = stmt.executeQuery(sqlStr);  // Send the query to the server

         // Step 4: Process the query result set
         int count = 0;
         while(rset.next()) {
            // Print a paragraph <p>...</p> for each record
            out.println("<p>" + rset.getString("author")
                  + ", " + rset.getString("title")
                  + ", $" + rset.getDouble("price") + "</p>");
            count++;
         }
         out.println("<p>==== " + count + " records found =====</p>");
      } catch(Exception ex) {
         out.println("<p>Error: " + ex.getMessage() + "</p>");
         out.println("<p>Check Tomcat console for details.</p>");
         ex.printStackTrace();
      }  // Step 5: Close conn and stmt - Done automatically by try-with-resources (JDK 7)
 
      out.println("</body></html>");
      out.close();
   }
}
```

```java
javac -cp ./XXX/lib/servlet-api.jar QueryServlet.java
```

现在可以访问

```sh
http://localhost:9999/hello/query
```

查看服务



