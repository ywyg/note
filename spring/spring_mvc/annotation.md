- `@RequestParam`

  与此注解对应的请求头应该是`application/json`
  
  > 此注解与请求的body绑定，spring 通过HttpMessageConverters转换将request body 转成被`@RequestParam`修饰的方法的参数并完成绑定
  >
  > 可以接受的参数类型：
  >
  > - json
  >
  > - xml
  >
  >   具体是哪一种取决于`content-type`
  >
  > ```js
  > $scope.user = {
  >             username: "foo",
  >             auth: true,
  >             password: "bar"
  >         };    
  > $http.post('http://localhost:7777/scan/l/register', $scope.user).
  >                         success(function (data, status, headers, config) {
  >                             ...
  >                         })
  > ```
  >
  > ```java
  > @RequestMapping(method = RequestMethod.POST, produces = "application/json", 
  >                 value = "/register")
  > public Map<String, String> register(Model uiModel,
  >                                     @RequestBody User user,
  >                                     HttpServletRequest httpServletRequest)
  > ```
  >
  > 

- `@RequestParam`

  与此注解对应的请求头应该是`application/x-www-form-urlencoded`

  > 此注解与特定的URL绑定，URL中的参数的值被转换成`@RequestParam`修饰方法的参数值，表明方法的参数应该在web请求的参数中
  >
  >  可以接受的参数类型：
  >
  > - query parameters   //URL内参数
  > -  form data  //表单参数
  > - parts in multipart requests //文件上传参数
  >
  > `RequestParam` is likely to be used with name-value form fields，总是通过name完成绑定
  >
  > ```js
  > $http.post('http://localhost:7777/scan/l/register?username="Johny"&password="123123"&auth=true')
  >       .success(function (data, status, headers, config) {
  >                         ...
  >                     })
  > ```
  >
  > ```java
  > @RequestMapping(method = RequestMethod.POST, value = "/register")
  > public Map<String, String> register(Model uiModel,
  >                                     @RequestParam String username,
  >                                     @RequestParam String password,
  >                                     @RequestParam boolean auth,
  >                                     HttpServletRequest httpServletRequest)
  > ```

- `@RequestPart`

  与此注解对应的请求头应该是`multipart/form-data`

  > 通常与文件上传等复杂类型一同使用