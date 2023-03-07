## 函数的参数

### 默认参数

要求：

- 必须参数在前，默认参数在后
- 当不按照顺序提供默认参数时，调用时需要加上参数名
- 默认参数指向不变对象

> ```python
> ## 第二个参数默认是2
> def power(x, n=2):
>     s = 1
>     while n > 0:
>         n = n - 1
>         s = s * x
>     return s
> ```

### 可变参数

> ```python
> ## 可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple
> ## 对于list调用，可以简写
> ## list = [1,2,3]
> ## sum = calc(*list)
> def calc(*numbers):
>     sum = 0
>     for n in numbers:
>         sum = sum + n * n
>     return sum
> ```

### 关键字参数

提示：

- 关键字参数其实就是map参数

- map可以指定必须有哪些key

  > ```python
  > ## 这种方式只接受key为 city或者job的map
  > def person(name, age, *, city, job):
  >     print(name, age, city, job)
  > ## 同样可以设置默认值
  > def person(name, age, *, city='Beijing', job):
  >     print(name, age, city, job)
  > ```

> ```python
> ## 可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。而关键字参数允许你传入0个或任意个含参数名的参数，
> ## 对于dict调用，可以简写
> ## extra = {'city': 'Beijing', 'job': 'Engineer'}
> ## person('Jack', 24, **extra)
> def person(name, age, **kw):
>     print('name:', name, 'age:', age, 'other:', kw)
> ```

### 参数组合

上面的这些参数形式可以在一个函数内全部定义，但是要满足以下顺序

1. 必须参数
2. 默认参数
3. 可变参数
4. 命名关键字参数
5. 关键字参数