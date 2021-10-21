# 正则表达式实现跨行匹配


正则表达式（Regular expression）可用来检查文本中是否包含指定模式的字符串，通常是按行来处理（POSIX标准），因为`.`操作符通常不匹配换行符，如果要匹配多行怎么处理呢？本文介绍正则表达式跨行匹配实现方法。

<!--more-->

## 1. sed 命令删除多行

测试文档test.txt内容如下：
```bash
start
test1
test2
end
```
删除 `start` 和 `end` 之间的内容
```bash
# 包括`start` 和 `end`
sed -i '/start/,/end/d' test.txt  

# 不包括`start` 和 `end`
sed -i '/start/,/end/{{//!d;};}' test.txt 
```

## 2. Python正则表达式匹配多行

Python中匹配多行方法如下：

### ① `re.DOTALL` 或者 `re.S` 参数

```python
import re

data = "1\nstart\ntest1\ntest2\nend\n2"

reg1 = r"start.*end"
reg2 = r"start(.*)end"
res1 = re.findall(reg1, data, flags=re.S)
print(res1)
res2 = re.findall(reg2, data, flags=re.DOTALL)
print(res2)
```

执行结果：

```python
['start\ntest1\ntest2\nend']
['\ntest1\ntest2\n']
```

### ② 表达式 `(.|\n|\r)*`

```python
import re
data = "1\nstart\ntest1\ntest2\nend\n2"

reg3 = r"start((.|\n|\r)*)end"
res = re.findall(reg3, data)
print(res)
```

执行结果：

```python
[('\ntest1\ntest2\n', '\n')]
```

### ③ 表达式  `[\s\S]*`

```python
import re
data = "1\nstart\ntest1\ntest2\nend\n2"

reg4 = r"start([\s\S]*)end"
res = re.findall(reg4, data)
print(res)
```
执行结果：

```python
['\ntest1\ntest2\n']
```

### ④ 表达式 `(?s)`

```python
import re
data = "1\nstart\ntest1\ntest2\nend\n2"

reg5 = r"(?s)start(.*)end"
res = re.findall(reg5, data)
print(res)
reg5 = r"(?s)start.*end"
res = re.findall(reg5, data)
print(res)
```
执行结果：

```python
['\ntest1\ntest2\n']
['start\ntest1\ntest2\nend']
```

**参考：**

1. [https://stackoverflow.com/questions/159118/how-do-i-match-any-character-across-multiple-lines-in-a-regular-expression](https://stackoverflow.com/questions/159118/how-do-i-match-any-character-across-multiple-lines-in-a-regular-expression)



