# Python日志系统logging使用介绍
日志记录对于软件开发调试和运行都非常重要。Python标准库提供了一个日志记录系统，可以很方便的在python项目中添加日志记录。本文将详细介绍如何使用python的 `logging` 模块来记录日志。

<!--more-->


## 基础使用

### 日志级别

主要包括了5种日志级别，代表5种严重级别（严重程度由低到高）：

- DEBUG：提供详细的详细
- INFO：程序运行的关键步骤信息
- WARNING：警告信息
- ERROR：程序错误，某个功能无法执行
- CRITICAL：严重错误，可能整个程序无法执行

Logger提供了一个默认的记录器，称为root Logger。

```python
import logging

logging.debug('Debug 级别日志信息')
logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息')
logging.error('Error 级别日志信息')
logging.critical('Critical 级别日志信息')
```

输出：

```bash
WARNING:root:Warning 级别日志信息
ERROR:root:Error 级别日志信息
CRITICAL:root:Critical 级别日志信息
```

默认打印WARNING及更高严重级别的日志。

### 基本配置

可以使用`basicConfig(**kwargs)`方法对日志系统进行配置。常用参数如下:

- level: 指定严重级别。
- filename: 指定文件。
- filemode: 如果指定了filename，则以该模式打开文件。默认是a，表示追加。
  - a：追加
  - w：覆盖
- format:日志信息的格式。默认levelname, name和message属性，用冒号分隔。

注意：`basicConfig`函数只能被调用一次。

level参数可以设置要记录的日志消息的严重级别:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug('Debug 级别日志信息')
logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息')
logging.error('Error 级别日志信息')
logging.critical('Critical 级别日志信息')
```

输出：

```bash
DEBUG:root:Debug 级别日志信息
INFO:root:Info 级别日志信息
WARNING:root:Warning 级别日志信息
ERROR:root:Error 级别日志信息
CRITICAL:root:Critical 级别日志信息
```

### 保存日志到文件

```python
import logging

logging.basicConfig(filename='test.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.debug('Debug 级别日志信息')
logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息')
logging.error('Error 级别日志信息')
logging.critical('Critical 级别日志信息')
```

### 格式化输出

`format` 参数用于格式化输出设置，除了默认设置levelname, name和message属性：

| 属性名          | 使用格式              | 描述                                                         |
| :-------------- | :-------------------- | :----------------------------------------------------------- |
| asctime         | `%(asctime)s`         | 时间，默认格式为 ‘2003-07-08 16:49:45,896’                   |
| created         | `%(created)f`         | 时间戳                                                       |
| relativeCreated | `%(relativeCreated)d` | 相对于加载日志模块的时间(以毫秒为单位)。                     |
| msecs           | `%(msecs)d`           | 日志创建时间的毫秒部分                                       |
| filename        | `%(filename)s`        | 脚本文件名称                                                 |
| funcName        | `%(funcName)s`        | 调用日志记录的函数名称                                       |
| module          | `%(module)s`          | 脚本模块名                                                   |
| pathname        | `%(pathname)s`        | 脚本文件绝对路径名                                           |
| name            | `%(name)s`            | 记录器名称，默认logger名为root                               |
| levelname       | `%(levelname)s`       | 文本类型的日志级别 (`'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`). |
| levelno         | `%(levelno)s`         | 数字类型的日志级别 (10, 20, 30, 40, 50).                     |
| lineno          | `%(lineno)d`          | 日志调用的代码所在行号                                       |
| message         | `%(message)s`         | 日志信息                                                     |
| process         | `%(process)d`         | 进程ID                                                       |
| processName     | `%(processName)s`     | 进程名称                                                     |
| thread          | `%(thread)d`          | 线程ID                                                       |
| threadName      | `%(threadName)s`      | 线程名                                                       |

其中 `asctime` 时间格式可以使用 `datefmt` 属性更改，语法格式与python datetime模块的格式化函数相同，例如:

```python
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%Y%m%d-%H:%M:%S')

logging.debug('Debug 级别日志信息')
logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息')
logging.error('Error 级别日志信息')
logging.critical('Critical 级别日志信息')
```

输出：

```bash
20230228-22:13:05 - Debug 级别日志信息
20230228-22:13:05 - Info 级别日志信息
20230228-22:13:05 - Warning 级别日志信息
20230228-22:13:05 - Error 级别日志信息
20230228-22:13:05 - Critical 级别日志信息
```



除了以上属性外，还支持自定义属性，使用 `extra` 参数传递：

```python
import logging

FORMAT = '%(asctime)s - %(clientip)s - %(message)s'
logging.basicConfig(format=FORMAT)
clientip = '192.168.0.1'
d = {'clientip':clientip}

logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息', extra=d)
```

输出：

```bash
2023-03-04 11:21:23,459 - 192.168.0.1 - Warning 级别日志信息
```

### 捕获异常信息

设置 `exc_info` 参数为 `True` 可以输出信息报错信息：

```python
import logging

try:
  res = 1 / 0
except Exception as e:
  logging.error(e, exc_info=True)
```

输出：

```bash
ERROR:root:division by zero
Traceback (most recent call last):
  File "d:\logging\log_demo3.py", line 4, in <module>
    res = 1 / 0
ZeroDivisionError: division by zero
```

也可以使用 `logging.exception()` 方法，效果一样：

```python
logging.exception(e)
```

另外，`stack_info` 参数设置为 `True` 是可以打印堆栈信息。



## 自定义logger

可以通过创建logger类的对象来定义自己的记录器。

### 日志模块四大组件

日志模块最常用的类:

- **Logger**：公开了一个接口，代码通过使用该接口记录日志消息。
- **Handler**：处理器，将logger创建的日志发送到目的地（控制台或文件）。常用的处理程序包括:
  - FileHandler:用于将日志消息发送到文件
  - StreamHandler:用于向输出流(如stdout)发送日志消息
  - SyslogHandler:用于向syslog守护进程发送日志消息
  - HTTPHandler:用于使用HTTP协议发送日志消息
- **Filter**：过滤器，提供一种机制来确定记录哪些日志。
- **Formatter**：格式器，决定日志消息的输出格式。

Logger类是入口，使用模块级别函数 `logging.getLogger(name)` 实例化，最终由Handler来对日志进行处理，Handler会调用Filter和Formatter来对日志进行过滤和格式化。

```python
import logging

logger = logging.getLogger('mylogger')

logger.debug('Debug 级别日志信息')
logger.info('Info 级别日志信息')
logger.warning('Warning 级别日志信息')
logger.error('Error 级别日志信息')
logger.critical('Critical 级别日志信息')
```

自定义logger不能使用 `basicConfig()` 来配置，需要使用 处理器（Handler）和 格式器（Formatter）来配置。

### 处理器

可以使用处理器（Handler）来配置自定义logger将日志保存到文件、输出到控制台、通过HTTP发送或者通过邮件发送。

处理器也可以设置日志严重级别，为文件处理器(`FileHandler`)和控制台处理器(`StreamHandler`)设置不同的日志级别。

```python
## 创建处理器 handlers
console_handler = logging.StreamHandler() # 输出到控制台
file_handler    = logging.FileHandler(logname) # 输出到文件
console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.ERROR)
```

### 格式器

格式器（Formatter）用来配置格式化输出。
```python
## 创建格式器
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s', '%Y%m%d-%H:%M:%S')
file_format    = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y%m%d-%H:%M:%S')
```

### 过滤器

过滤器（Filter）可实现日志过滤操作，

```python
import logging
import sys
import os

class failureFilter(logging.Filter):
    def filter(self, record):
        if 'Failure' in record.msg:
            return True
        return False

logger = logging.getLogger(__name__)  
console_handler = logging.StreamHandler(stream=sys.stdout) # 输出到控制台
## 添加filter
loggingFiletr = failureFilter()
console_handler.addFilter(loggingFiletr)

logger.addHandler(console_handler)
logger.info('Info 级别日志信息')
logger.error('Failure')
```

### 示例

自定义logger示例脚本：

```python
import logging
import sys
import os

class failureFilter(logging.Filter):
    def filter(self, record):
        if 'Failure' in record.msg:
            return True
        return False

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
logname = os.path.join(abspath, 'file.log')

## 创建处理器 handlers
console_handler = logging.StreamHandler(stream=sys.stdout) # 输出到控制台
file_handler    = logging.FileHandler(logname) # 输出到文件
console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.ERROR)

## 添加filter
loggingFiletr = failureFilter()
console_handler.addFilter(loggingFiletr)
file_handler.addFilter(loggingFiletr)

## 创建格式器
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s', '%Y%m%d-%H:%M:%S')
file_format    = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y%m%d-%H:%M:%S')

## 将格式器添加到处理器中
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

## 将处理器添加到logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info('Info 级别日志信息')
logger.error('Failure')
```

## 其他配置方法

除了前面介绍的 `basicConfig()` 方法、logger、handler和formatter来配置日志记录器外，还可以使用 `fileConfig()` 或 `dictConfig()` 方法来加载配置文件或字典实现日志记录器的配置。

### fileConfig()方法

配置文件（可使用configparser类读取）格式如下，此配置文件配置了控制台和文件输出两种方式：

```ini
[loggers]
keys=root,mylogger

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=sampleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_mylogger]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=mylogger
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=sampleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=sampleFormatter
args=("config.log", "a")

[formatter_sampleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
qualname=mylogger

```

使用 `fileConfig` 方法来加载配置：

```python
import logging
import logging.config
import os

abspath = os.path.dirname(os.path.abspath(__file__)) 
confpath = os.path.join(abspath, 'logging.conf')

if os.path.exists(confpath):
    logging.config.fileConfig(fname=confpath, disable_existing_loggers=False)

## create logger
logger = logging.getLogger("mylogger")

logger.debug('Debug 级别日志信息')
logger.info('Info 级别日志信息')
```

### dictConfig()方法

配置字典可以使用yaml或者json代码来编写。

#### 1. yaml配置文件

创建`logging.yaml`：

```yaml
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt: '%Y-%m-%d %H:%M:%S'
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout
  fileHandler:
    class: logging.FileHandler
    level: DEBUG
    formatter: simple
    filename: yaml.log
    encoding: utf8
loggers:
  mylogger:
    level: DEBUG
    handlers: [console,fileHandler]
    propagate: no
root:
  level: DEBUG
  handlers: [console]
```

调用示例：

```python
import logging
import logging.config
import os
import yaml

abspath = os.path.dirname(os.path.abspath(__file__))
confpath = os.path.join(abspath, 'logging.yaml')

if os.path.exists(confpath):
    with open(confpath, 'r') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('mylogger')

logger.debug('Debug 级别日志信息')
logger.info('Info 级别日志信息')
```

#### 2. json配置文件

创建`logging.json`：

```json
{
    "version":1,
    "disable_existing_loggers":false,
    "formatters":{
        "simple":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt":"%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "level":"DEBUG",
            "formatter":"simple",
            "stream":"ext://sys.stdout"
        },
        "fileHandler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"INFO",
            "formatter":"simple",
            "filename":"json.log",
            "maxBytes":10485760,
            "backupCount":10,
            "encoding":"utf8"
        }
    },
    "loggers":{
        "mylogger":{
            "level":"INFO",
            "handlers":["fileHandler"],
            "propagate":"no"
        }
    },
    "root":{
        "level":"INFO",
        "handlers":["console","fileHandler"]
    }
}
```

调用示例：

```python
import logging
import logging.config
import os
import json

abspath = os.path.dirname(os.path.abspath(__file__)) 
confpath = os.path.join(abspath, 'logging.json')

if os.path.exists(confpath):
    with open(confpath, 'r') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger("mylogger")

logger.debug('Debug 级别日志信息')
logger.info('Info 级别日志信息')
```



参考文档：

1. [https://docs.python.org/zh-cn/3.7/library/logging.html](https://docs.python.org/zh-cn/3.7/library/logging.html)


