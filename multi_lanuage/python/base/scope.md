不像java中那样，无论是函数还是变量有着明确的访问限定修饰符，python中的作用域用法比较搞，下面以java为列。对照的解释

定义一个方法，输出 a 和 b 的和

> sum(int a,int b);

| java                        | python          |
| --------------------------- | --------------- |
| `public sum(int a, int b) ` | `def sum(a,b)`  |
| `private sum(int a, int b)` | `def _sum(a,b)` |
| `protect sum(int a, int b)` | `def sum(a,b)`  |
| `sum(int a, int b)`         | `def sum(a,b)`  |

并且，python 中就算设定为私有函数，并不是说在外部无法访问，只是不推荐访问而言，硬上也是可以

由于python每个文件都是一个模块，所以没有java那样的包限定符，子类限定符这些设定

对于属性而言，python可以在属性前添加两个下划线达到私有变量的效果

```python
class student:
  def __init__(self,name,age):
    ## 这里的__name无法被外部访问
    self.__name = name
    ## 这个又可以被外部访问了
    self.__age__ = age
```



