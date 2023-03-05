# Python文件及目录处理方法
Python可以用于处理文本文件和二进制文件，比如创建文件、读写文件等操作。本文介绍Python处理目录以及文件的相关方法。

<!--more-->


下面先来介绍python目录处理相关方法。

## 目录操作

### 1. 获取当前代码路径

test_folder.py

```python
import os
import sys

print(__file__)
print(sys.argv[0])
print(os.path.realpath(__file__))
print(os.path.abspath(sys.argv[0]))
```

Out：
```bash
D:/ProgramWorkspace/PythonNotes/03-File-Handling/test_folder.py
D:/ProgramWorkspace/PythonNotes/03-File-Handling/test_folder.py
D:\ProgramWorkspace\PythonNotes\03-File-Handling\test_folder.py
D:\ProgramWorkspace\PythonNotes\03-File-Handling\test_folder.py
```

### 2. 获取当前文件`__file__`的所在目录

```python
print(os.getcwd())
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.split(os.path.realpath(__file__))[0])
path = os.path.dirname(os.path.realpath(__file__))
```
Out：
```bash
D:\ProgramWorkspace\PythonNotes\03-File-Handling
D:\ProgramWorkspace\PythonNotes\03-File-Handling
D:\ProgramWorkspace\PythonNotes\03-File-Handling
```

### 3. 获取当前文件名名称

```python
print(os.path.basename(sys.argv[0])) # 当前文件名名称
print(os.path.basename(__file__))

```
Out：
```python
test_folder.py
test_folder.py
```

### 4. 拼接路径

```python
path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.basename(__file__)
abspath = os.path.join(path, filename)
print(abspath)
```
Out：
```bash
D:\ProgramWorkspace\PythonNotes\03-File-Handling\test_folder.py
```

获取上级目录：

```python
dirpath     = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(dirpath, ".."))
```



### 5. 创建目录

判断目录是否存在：

```python
os.path.exists(path)
```

创建目录

```python
if not os.path.exists(path): 
    print(f"创建文件夹: {path}")
    os.makedirs(path)
```

### 6. 获取目录下所有文件

有两种方式可以用来获取目录的文件：

1. `os.walk` : 返回当前目录下的文件及子目录的内容
2. `os.listdir`: 只返回当前目录中所包含的内容

```python
import os

for root, dirs, files in os.walk(os.getcwd()):
	print(root)
	print(dirs)
	print(files)
	print("#" * 10)
print(os.listdir(os.getcwd()))
```



## 文件操作

### 1. 创建文本文件

```python
text = "Hello World!"
newfilepath = os.path.join(path, "newfile.txt")
file = open(newfilepath, 'w')
file.write(text)  # 写入内容信息
file.close()
```

### 2. 判断文件是否存在

```python
print(os.path.isfile(path)) 
print(os.path.isfile(newfilepath))
print(os.path.exists(newfilepath))
```

Out：

```python
False
True
True
```

`os.path.isfile` 用于判断是否为文件且是否存在，`os.path.exists` 也可以用于判断文件是否存在，但还是建议使用`os.path.isfile` 判断文件，`os.path.exists` 判断目录是否存在。比如，某个文件为newfile，使用这两个方法都会返回True，无法判断到底是文件还是目录。

### 3. 判断文件属性

```python
print(os.access(newfilepath,os.F_OK)) # 文件是否存在
print(os.access(newfilepath,os.R_OK)) # 文件是否可读
print(os.access(newfilepath,os.W_OK)) # 文件是否可以写入
print(os.access(newfilepath,os.X_OK)) # 文件是否有执行权限
```

Out：

```python
True
True
True
True
```

`os.access(newfilepath,os.F_OK)` 也可以用于判断文件是否存在。

### 4. 获取文件后缀

获取文件名：

```python
fpath, fname = os.path.split("D:\\test\\newfile.txt")
print(fpath) # D:\test
print(fname) # newfile.txt
```

获取文件后缀

```python
fname, fextension = os.path.splitext("D:\\newfile.txt")
print(fname) # D:\test\newfile
print(fextension) # .txt
```

### 5. 打开文件

打开文本文件或者二进制文件可以使用 `open()` 方法:

```python
f = open(filename, mode)
```

几种文件打开模式：

- `b`：二进制模式
- `t`：文本模式(默认)
- `r`: 打开存在的文件，读操作(默认)。
- `w`: 打开文件，写操作，先前文件中的内容会被删除。如果文件不存在会自动创建。 
- `a`: 打开文件，追加操作，不会删除先前文件中的内容。如果文件不存在会自动创建。 
- `x`：创建新文件，写操作，使用此模式打开存在的文件会抛出异常。
- `r+`: 读、写操作，不会删除先前文件中的内容，但是会覆盖内容。
- `w+`: 写、读操作，会删除先前文件中的内容。
- `a+`: 追加、读操作，不会删除和覆盖先前文件中的内容。
- `x+` ：创建新文件，读写操作。

`open()`方法的默认模式为 `rt` 模式，也就是读文本文件。

另外需要注意filename的写法，比如文件路径是：`D:\test.txt` ，其中`\t` 可能会被转义，需要自前面加一个 `r` ：

```python
f = open(r"D:\test.txt", "w")
```



### 6. 写文件

读写文件都需要先打开文件，返回一个文件对象，然后对文件对象进行读写操作。写文件需要设置写权限，比如 `w`、`w+`、`a` 模式。

写文件主要包括两种方法：

- `file.write(str)`：写入字符串
- `file.writelines(list)`：写入字符串列表，用于同时插入多个字符串。

举个栗子：

```python
file = open("newfile.txt", 'w')
text1 = "Hello World!\n你好，世界！\r"
file.write(text1)  # 写入内容信息

text2 = ["To the time to life, \n", "rather than to life in time.\r"]
file.writelines(text2)

file.close()
```

`w` 模式会删除先前文件中的内容，如果不想删除，需要直接追加到后面，可以使用`a` 和 `a+` 模式：

```python
file = open("newfile.txt", 'a')
```



### 7. 读文件

常见的读取文件方法有以下几种：

- in操作符
- read()：读取所有数据，返回一个字符串。
- readline()：读取第一行
- readlines()：读取所有行，每行保存为列表的一个元素。

```python
## 打开并读取文件
file = open("newfile.txt", 'r')

for line in file:
	print(line)
print()

file.seek(0, 0)
print(file.read(5))  # 
print()

file.seek(0, 0)
print(file.readline(12))
print()

file.seek(0, 0)
print(file.readlines())
print()

file.close()
```

执行结果：

```python
Hello World!

你好，世界！

To the time to life, 

rather than to life in time.


Hello

Hello World!

['Hello World!\n', '你好，世界！\n', 'To the time to life, \n', 'rather than to life in time.\n']
```

读取file对象的所有内容后，文本的光标会移动到最后，再次读取file需要将光标移到前面，使用 `file.seek(0, 0)` 方法可以将光标移到前面。还有一种解决方案是将读取的内容存一个在局部变量中。

### 8. 删除文件

删除某个文件：

- `os.remove(path)`
- `os.unlink(path)`




### 9. with语句

with语句可用于异常处理，可以确保资源的适当获取及自动释放。使用with语句后就不需要调用`file.close()` 语句了，它会自动释放。

```python
text1 = "Hello World!\n你好，世界！\r"
text2 = ["To the time to life, \n", "rather than to life in time.\r"]
## 写
with open("newfile.txt", "w") as file:
    file.write(text1)
    file.writelines(text2)

## 读
with open("newfile.txt", "r+") as file:
	print(file.read())
```

with语句对处理大文件非常有用，比如10G大小的文件， with语句会进行上下文管理。



## shutil目录和文件操作

Python shutil库提供了对文件和目录复制、移动、删除、压缩、解压等操作。

### 1. 复制文件或目录

- `shutil.copy(src, dst)`：复制文件或目录
- `shutil.copyfile(src, dst)`：复制文件，src和dst只能是文件
- `shutil.copytree(src, dst, dirs_exist_ok=False)`：复制目录，默认dst目录不存在，否则会报错。

示例：

```python
import os
import shutil

dirpath    = os.path.dirname(os.path.realpath(__file__))
sourcedir  = os.path.join(dirpath, "shutil_a")
sourcefile = os.path.join(dirpath, "shutil_a", "test.txt")        
destdir    = os.path.join(dirpath, "shutil_b")
destfile   = os.path.join(dirpath, "shutil_b", "test2.txt")
## 复制文件或目录
shutil.copy(sourcefile, destdir)        
## 复制文件
shutil.copyfile(sourcefile, destfile) 
## 复制目录
shutil.copytree(sourcedir, destfile, dirs_exist_ok=True) 
```



### 2. 移动文件或目录

语法：`shutil.move(src, dst)`

示例：

```python
import os
import shutil

dirpath    = os.path.dirname(os.path.realpath(__file__))
sourcedir  = os.path.join(dirpath, "shutil_a")
sourcefile = os.path.join(dirpath, "shutil_a", "test.txt")        
destdir    = os.path.join(dirpath, "shutil_b")
shutil.move(sourcefile, destdir)
shutil.move(destdir, sourcedir)
```

### 3. 删除文件和目录

删除某个文件使用 `os` 模块提供的remove和unlink方法：

- `os.remove(path)`
- `os.unlink(path)`

删除目录使用 `shutil.rmtree` 方法：

```python
import os
import shutil

dirpath    = os.path.dirname(os.path.realpath(__file__))     
destdir    = os.path.join(dirpath, "shutil_b")
shutil.rmtree(destdir)
```

## shutil文件压缩、解压

shutil库也支持文件压缩、解压操作，这个功能在Python 3.2版本引入。

### 1. 压缩文件

语法格式：

```python
shutil.make_archive(base_name, format[, root_dir[, base_dir[, verbose[, dry_run[, owner[, group[, logger]]]]]]])
```

- base_name：压缩包文件名
- format：压缩包格式，支持zip，tar，bztar，gztar，xztar格式，可使用`shutil.get_archive_formats()`方法查看
- root_dir：要压缩文件路径的根目录（默认当前目录）
- base_dir：相对于root_dir的压缩文件路径（默认当前目录）

示例：

```python
import os
import shutil

dirpath    = os.path.dirname(os.path.realpath(__file__))
archive_name  = os.path.join(dirpath, "shutil_a")
root_dir = archive_name
shutil.make_archive(archive_name, 'zip', root_dir)
```



### 2. 解压文件
语法格式：
```python
shutil.unpack_archive(filename[, extract_dir[, format]])
```

示例：

```python
import os
import shutil

dirpath      = os.path.dirname(os.path.realpath(__file__))
archive_name = os.path.join(dirpath, "shutil_a.zip")
extract_dir  = os.path.join(dirpath, "shutil_a")   
shutil.unpack_archive(archive_name, extract_dir, 'zip')
```



参考文档：

1. [https://docs.python.org/3/library/shutil.html](https://docs.python.org/3/library/shutil.html)








