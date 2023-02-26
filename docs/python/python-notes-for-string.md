# 字符串操作
本文记录一些Python字符串相关操作。
<!--more-->

## 判断字符串中是否包含指定字符串

1、`in` 操作符

```python
text   = "hello world!"
result = 'world' in text
```

2、`index`方法

```python
>>> text   = "hello world!"
>>> text.index('world')
6
>>> text.index('world',6)  # 从第7个字符串开始查找
6
>>> text.index('nihao')  # 不存在会报 ValueError 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: substring not found
```

3、`rindex`方法

```python
>>> text.rindex('l')
9
```

4、`find`方法

```python
>>> text.find('world')
6
>>> text.find('world',6,len(text)-1)  # 指定起始位置
6
```

5、`rfind`方法：返回最后一次出现的位置

```python
>>> text.rfind('l')
9
```

6、正则表达式

`re.search` 方法

```python
>>> import re
>>> text   = "hello world!"
>>> re.search(r"world", text)
<re.Match object; span=(6, 11), match='world'>
>>> res =re.search(r"wor\w+", text)
>>> res
<re.Match object; span=(6, 11), match='world'>
>>> res.group()
'world'
>>> res.span()
(6, 11)
```

`re.findall`查找所有匹配到的字符，没有位置信息

```python
>>> re.findall(r"l\w+", text)
['llo', 'ld']
>>>
```

`re.finditer` 方法可以查找所有匹配到的字符，并且提供位置信息

```python
>>> for match in re.finditer(r"l\w+", text):
...     print(match)
...
<re.Match object; span=(2, 5), match='llo'>
<re.Match object; span=(9, 11), match='ld'>
```

正则表达式语法很多，更多用法可参考[正则表达式介绍及Python使用方法](https://blog.csdn.net/u010698107/article/details/111568817) 。

## 统计字符串中某个单词的出现的次数

```python
a = 'test 123 dfg test'
## 方法1
len([i for i in a.split(' ') if i == test])

## 方法2
len(a.split('test'))-1
```

## Python提取两个字符串之间的内容
```python
import re 
str = '''/begin MEASUREMENT
100
LINK
DISPLAY
SYMBOL
/end MEASUREMENT'''
 
regex = r'/begin MEASUREMENT([\s\S]*)/end MEASUREMENT'
matches = re.findall(regex, str)
for match in matches:
    print(match)
```

```python
import re 
str = 'test:100      end' 
regex = r'test:([\s\S]*)/end'
matches = re.findall(regex, str)
test = matches[0].strip()
```

## 字符删除、替换
### 删除空格
```python
s = ' 123abcd456  '
# 删除两边的空格
print(s.strip())
# 删除右边空格
print(s.rstrip()) 
# 删除左边空格
print(s.lstrip())
# 删除两边的数字
print(s.strip(' ').strip('123456'))
# 删除两边的引号
s = "'123abcd456'"
print(s.strip("'"))
```

分割并去除空格
```python
string = " hello , world !"
string = [x.strip() for x in string.split(',')]
```
### 将格式化字符转换为字典
```python
string = "dst='192.168.0.1',src='192.168.1.2'"
fields = dict((field.split('=') for field in string.split(',')))
fields = dict(((lambda a:(a[0].strip("'"),a[1].strip("'"))) (field.split('=')) for field in string.split(',')))
```

```python
>>> fields
{'dst': "'192.168.0.1'", 'src': "'192.168.1.2'"}
```

### 删除(替换)任意位置字符
```python
s = '11233aabcdd41556'
# 删除某个特定字符
print(ss.replace('1', ''))
# 同时删除不同字符
import re
print(re.sub('[1a]', '', s))
```

