# **「Mybatis-plus」**多数据源

## 多数据源配置

1. 添加依赖

   ```xml
   <dependency>
     <groupId>com.baomidou</groupId>
     <artifactId>dynamic-datasource-spring-boot-starter</artifactId>
     <version>${version}</version>
   </dependency>
   ```

2. 在配置文件增加数据源配置信息

   ```yaml
   spring:
     datasource:
       dynamic:
         primary: master #设置默认的数据源或者数据源组,默认值即为master
         strict: false #严格匹配数据源,默认false. true未匹配到指定数据源时抛异常,false使用默认数据源
         datasource:
           master:
             url: jdbc:mysql://xx.xx.xx.xx:3306/write
             username: root
             password: 123456
             driver-class-name: com.mysql.jdbc.Driver # 3.2.0开始支持SPI可省略此配置
           slave:
             url: jdbc:mysql://xx.xx.xx.xx:3307/read
             username: root
             password: 123456
             driver-class-name: com.mysql.jdbc.Driver
   ```

3. 使用`「@DS」`注解

   > 使用方式：`@DS("master|slave")` 

   1. 作用于类上
   2. 作用于方法上

   此注解有就近原则，可以影响方法内部的 `XXXmapper` 对象，作用于方法上时会覆盖作用于类上效果

## 多数据源实现原理

### 代理Mapper

**「Mybatis-plus」**会为继承BaseMapper的接口生成代理对象，代理对象包含常用的CRUD方法。这些常用方法被纳入JdkDynamicAopProxy管理，使用反射方式执行。

### 实现步骤

Mybatis-plus执行SQL执行过程中，需要从`DataSource`类中获取数据库连接，通过该连接执行语句。具体执行过程如下：

1. 添加数据源，根据yml获取多个数据源

```java
new YmlDynamicDataSourceProvider(properties.getDatasource());
```

2. 将第一步获取的数据源保存到`DynamicRoutingDataSource`的	`dataSourceMap`

```java
 public synchronized void addDataSource(String ds, DataSource dataSource) {
        DataSource oldDataSource = dataSourceMap.put(ds, dataSource);
        // other code
    }
```

3. 在执行查询链路过程中，有获取连接步骤

```java
 private Statement prepareStatement(StatementHandler handler, Log statementLog) throws SQLException {
    // other code
    Connection connection = getConnection(statementLog);
   	// other code
    return stmt;
  }
```

4. 获取连接

```java
/**
* @ds 数据源名称 
**/
public DataSource getDataSource(String ds) {
   	// other code
        if (dataSourceMap.containsKey(ds)) {
            // other code
            return dataSourceMap.get(ds);
        }
    }
```

上述实现步骤就是mybatis实现数据源动态切换的核心过程，但是，在上述过程中第三步和第四步之间没有说明`getDataSource(String ds)`参数的来源，所以在这里补充一下：

查询过程中，mybatis-plus使用动态代理的方式去执行方法，在执行前夕会检查方法的注解：

```java
public Object invoke(MethodInvocation invocation) throws Throwable {
  			// dsKey 就是@DS注解内部参数
        String dsKey = determineDatasourceKey(invocation);
  			// 将dsKey 放到了ThreadLocal里面
  			DynamicDataSourceContextHolder.push(dsKey);
       	// other code
    }

    private String determineDatasourceKey(MethodInvocation invocation) {
        String key = dataSourceClassResolver.findKey(invocation.getMethod(), invocation.getThis());
        // other code 
    }
```

执行完这个方法，在后续步骤中就随时可以拿到`ds`的内容了

### 注意事项

- 由于切换数据源时会获取新的连接，如果再使用了Spring事务，需要在切换时指定事务传播级别为`Propagation.REQUIRES_NEW`，也就是需要新起一个事务。
- 在处理DS-KEY，也就是数据源名称时，尽量使用单词等常规字符，对于`#`或其他字符，在`determineDatasourceKey`方法中可能有特殊处理
- 切换数据源时依赖`DynamicDataSourceAnnotationInterceptor.invoke方法的执行`，但是被`@Test`修饰的方法不会执行这个方法，导致ThreadLocal里没有正确的DS-KEY，只能使用默认数据源





