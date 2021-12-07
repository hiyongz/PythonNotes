# Python上下文管理器


在代码执行过程中会进行频繁的I/O操作，而计算资源往往是有限的，需要进行资源管理，保证这些资源在使用过后得到释放，防止发生资源泄露。Python中使用上下文管理器（context manager）进行资源管理，比如我们经常用到的`with`关键字，上下文管理器可以进行自动分配并且释放资源。


下面先来介绍一下with关键字在文件读写中的应用，简单了解上下文管理器的功能。

## with语句

在[Python文件及目录处理方法](https://blog.csdn.net/u010698107/article/details/121593923)中介绍了读写大文件建议使用with语句，with语句会进行资源的自动管理。文件很多的情况下也会导致资源泄露，下面来打开100000个文件，不进行文件关闭操作：

```python
for x in range(100000):
    file = open('test.txt', 'w')
    file_descriptors.append(file)
```

执行会报如下错误：

```python
OSError: [Errno 24] Too many open files: 'test.txt'
```

原因就是打开了太多文件而没有及时关闭导致了资源泄露，造成系统崩溃。完成处理后需要对文件进行关闭操作：

```python
file_descriptors = []
for x in range(10000):
	file = open('test.txt', 'w')
	try:
		file_descriptors.append(file)
	finally:
		file.close()
```

使用 with 语句可以完成自动分配并且释放资源，比上面的写法更加简洁：

```python
file_descriptors = []
for x in range(10000):
	with open('test.txt', 'w') as file:
		file_descriptors.append(file)
```

## 上下文管理器创建

### 基于类的上下文管理器

可以使用类来创建上下文管理器，需要保证这个类包括两个方法：`__enter__()` 和` __exit__()`。其中，方法 `__enter__()` 返回需要被管理的资源，方法 `__exit__()` 进行资源释放、清理操作。

下面来模拟 Python 的打开、关闭文件操作：
```python
class FileManager:
    def __init__(self, name, mode):
        print('__init__ method called')
        self.name = name
        self.mode = mode
        self.file = None

    def __enter__(self):
        print('__enter__ method called')
        self.file = open(self.name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('__exit__ method called')
        if self.file:
            self.file.close()
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_traceback}')
        return True
            

with FileManager('test.txt', 'w') as f:
	print('开始写操作')
	f.write('hello world !')
    
print(f.closed)
```

执行结果：
```python
__init__ method called
__enter__ method called
开始写操作
__exit__ method called
exc_type: <class 'Exception'>
exc_value: exception raised
exc_traceback: <traceback object at 0x000001B43C2444C8>
True
```

可以看到执行顺序为：

- `__init__()`：初始化对象 FileManager

- `__enter__()`：打开文件，返回 FileManager 对象

- with中的代码

- `__exit__()`：关闭打开的文件流

`__exit__()`方法中的参数`exc_type`, `exc_value`, 和 `exc_traceback` 用于管理异常。

### @contextmanager 装饰器

可以使用 `contextlib.contextmanager` 装饰器而不使用类的方式来实现上下文管理器，它是基于生成器的上下文管理器，用以支持 with 语句。

仍以打开、关闭文件为例：

```python
from contextlib import contextmanager

@contextmanager
def file_manager(name, mode):
    try:
        f = open(name, mode)
        yield f
    finally:
        f.close()
        
with file_manager('test.txt', 'w') as f:
    f.write('hello world !')
```

其中 `file_manager()` 函数是一个生成器，yield 之前可以看成是`__enter__ `方法中的内容，yield 后面的是 `__exit__()` 内容。加上`@contextmanager`装饰器，使用基于生成器的上下文管理器时，不需要定义`__enter__()`和`__exit__()`方法。

## 小结

上下文管理器可确保用过的资源得到迅速释放，通常和 with 语句一起使用，大大提高了程序的简洁度。另外需要注意的是，编写基于类或者生成器的上下文管理器时，记住不要忘记释放资源。

