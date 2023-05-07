- [常用注解](./annotation.md)

接口可以定义好方法，只需要找到实现类就会有实现方法，这样就能找到接口处理类

spring - mvc 的实现主要是通过`dispatcherServlet`，`dispatcherServlet`接受请求，分发到正确的资源

`Spring MVC `工作流程

<img src="https://raw.githubusercontent.com/ywyg/photo/main/image-20230316161213248.png" alt="image-20230316161213248" style="zoom:50%;" />

- 所有的请求都会被`DispatcherServlet`接收
- `DispatcherServlet`从`Handler Mapping`接受`Handler`与`Controller`映射关系，并转发到正确的`Controller`
- `Controller`返回正确的`ModelAndView`
- `DispatcherServlet`根据`Handler Mapping `找到`view`或者	`view resolver`资源

示例程序：

`Controller`

```java
@Controller
public class HelloController {
    @RequestMapping("/")
    public String display() {
        return "index";
    }
}
```

`web.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
         http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
  	<!--当有请求进入时，使用servlet-class标签内类处理-->
    <servlet>
        <servlet-name>spring</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>spring</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

