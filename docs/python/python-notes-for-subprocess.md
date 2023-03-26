# Python中 os.popen、os.system和subprocess.popen方法介绍
Python 提供了多种与操作系统交互的方法，比如os模块中的popen和system方法，此外，Python subprocess模块中的Popen类也提供了与操作系统交互的方法，使用起来更加灵活，本文将简单介绍这几种方法。

<!--more-->


## os.popen方法

`os.popen`方法语法格式：

```python
os.popen(cmd, mode, buffering)
```

- `cmd`：要执行的命令
- `mode`：默认`mode="r"`，表示输出文件可读，`w` 表示可写
- `buffering`：缓存区数据大小

示例：

```python
import os

command = "netsh interface ip show address WAN | findstr IP"
p = os.popen(command, 'r')
print(p.read())
```

输出：

```bash
    IP 地址:                           192.168.0.104
```



Python2 os模块另外还提供了popen2、popen3和popen4方法与操作系统交互。

`os.popen2` 与 `os.popen`方法的区别是`os.popen2`返回了一个用于stdin和用于stdout的两个文件对象。`os.popen3` 多了错误输出`stderr`，`os.popen4` 将标准输出和错误输出合并：

```python
stdout                = os.popen(cmd, mode, bufsize)
stdin, stdout         = os.popen2(cmd, mode, bufsize)
stdin, stdout, stderr = os.popen3(cmd, mode, bufsize)
stdin, stdout_stderr  = os.popen4(cmd, mode, bufsize)
```

这些方法这里不做更多介绍了，它们都可以使用 `subprocess.Popen` 来替代：

```python
## os.popen
pipe = subprocess.Popen(cmd, shell=True, bufsize=bufsize, stdout=PIPE).stdout
pipe = subprocess.Popen(cmd, shell=True, bufsize=bufsize, stdin=PIPE).stdin
## os.popen2
p = Popen(cmd, shell=True, bufsize=bufsize, stdin=PIPE, stdout=PIPE, close_fds=True)
stdin  = p.stdin
stdout = p.stdout
## os.popen3
p = Popen(cmd, shell=True, bufsize=bufsize, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
stdin  = p.stdin
stdout = p.stdout
stderr = p.stderr
## os.popen4
p = Popen(cmd, shell=True, bufsize=bufsize,stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
stdin  = p.stdin
stdout_stderr = p.stdout
```

## os.system方法

`os.system` 方法调用C函数`system()`，只会返回状态码，命令产生的输出会发送到控制台。

```python
import os

command = "netsh interface ip show address WAN | findstr IP"
p = os.system(command)
print(p)  
```

输出：

```bash
    IP 地址:                           192.168.0.104
0
```

## susbprocess.Popen方法

susbprocess模块提供了`Popen`类，是`os.system` 和 `os.popen` 方法的超集，可替代`os.system` 和 `os.popen` 方法，语法格式如下：

```bash
subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None, text=None)
```

### 替代 `os.popen()` 方法

替代 `os.popen(command, 'r')` 方法

```python
import subprocess

command = "netsh interface ip show address WAN | findstr IP"
p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
print(p.read().decode('gbk'))
```

输出：

```bash
    IP 地址:                           192.168.0.104
```



### 替代 `os.system()` 方法

替代 `os.system(command)` 方法：

```python
command = "netsh interface ip show address WAN | findstr IP"
p = subprocess.Popen(command, shell=True).wait()
print(p)
```

输出：

```bash
    IP 地址:                           192.168.0.104
0
```



susbprocess模块除了可以替代`os.system` 和 `os.popen` 方法以及前面介绍的popen2、popen3和popen4方法外，还可以替代 `os.spawn` 。

### 管道命令

除了将管道符`|`直接写入命令中以外，也可以使用以下方式实现管道命令：

```python
import subprocess

p1 = subprocess.Popen('netsh interface ip show address WAN', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p2 = subprocess.Popen('findstr IP', shell=True, stdin=p1.stdout, stdout=subprocess.PIPE).stdout
print(p2.read().decode('gbk'))

## 或者
p1 = subprocess.Popen('netsh interface ip show address WAN', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p2 = subprocess.Popen('findstr IP', shell=True, stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
out, err = p2.communicate() 
print(out.decode('gbk'))

## 或者使用 subprocess.check_output 方法
output = subprocess.check_output("netsh interface ip show address WAN | findstr IP", shell=True)
print(output.decode('gbk'))
```



### 执行多条命令

可使用如下方式连续执行多个命令：

```python
import subprocess

commands = ['mkdir log', 'cd log','echo "test" > test.txt','dir']
p = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
for cmd in commands:
    p.stdin.write((cmd + "\n").encode('utf-8'))
p.stdin.close()

print(p.stdout.read().decode('gbk'))
```



### Popen方法

在前面的例子中使用到了Popen类提供的 `communicate()`、`wait()`方法，主要有以下方法：

| 方法                                        | 描述                                                         |
| :------------------------------------------ | :----------------------------------------------------------- |
| Popen.poll()                                | 检查进程是否终止                                             |
| Popen.wait(timeout=None)                    | 等待进程终止                                                 |
| Popen.communicate(input=None, timeout=None) | 与进程交互：发送数据到stdin。从stdout和stderr读取数据。等待进程终止并设置returncode属性。 |
| Popen.send_signal(signal)                   | 向进程发送signal                                             |
| Popen.terminate()                           | 终止进程                                                     |
| Popen.kill()                                | 杀死进程                                                     |

## 总结

本文只是简单介绍了os.popen、os.system和subprocess.popen这三个方法，subprocess.popen还有更多的用法，它提供了对进程更细粒度的控制。subprocess.popen方法可以替代os.popen、os.system方法，subprocess.popen是他们的超集，如果只是简单的cmd命令调用可以直接使用os.popen和os.system，更复杂的控制可以选用subprocess.popen方法，按照自己实际情况进行选择。



参考文档：

1. [https://docs.python.org/zh-cn/3.7/library/subprocess.html](https://docs.python.org/zh-cn/3.7/library/subprocess.html)
2. [https://docs.python.org/3/library/subprocess.html#replacing-os-system](https://docs.python.org/3/library/subprocess.html#replacing-os-system)





