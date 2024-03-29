# List相关操作
List相关操作小例子
<!--more-->

## 获取list的下标和值
```python
>>> mylist = ['a', 'b', 'c', 'd']
>>> for index, value in enumerate(mylist):
...         print(index, value)
...
0 a
1 b
2 c
3 d
>>>
```

## 删除list中的空字符

```python
list1 = ['1', '','2', '3', '  ', ' 4  ', '  5', '    ','6 ', '', '     ',None, '7']
print(list1)
list2 = list(filter(None, list1)) 
print(list2) # ['1', '2', '3', '  ', ' 4  ', '  5', '    ', '6 ', '     ', '7']
list3 = [x.strip() for x in list2]
print(list3) # ['1', '2', '3', '', '4', '5', '', '6', '', '7']
list4 = list(filter(None, list3))  
print(list4) # ['1', '2', '3', '4', '5', '6', '7']
```

## 删除list元素
使用remove、pop和del方法参删除list中的某个元素
```python
>>> mylist = ['a', 'b', 'c', 'd','e','f','g','h']
>>> mylist.remove('a')
>>> mylist
['b', 'c', 'd', 'e', 'f', 'g', 'h']
>>> mylist.pop(0)
'b'
>>> mylist
['c', 'd', 'e', 'f', 'g', 'h']
>>> del mylist[0]
>>> mylist
['d', 'e', 'f', 'g', 'h']
>>> del mylist[0:2]
>>> mylist
['f', 'g', 'h']
>>> del mylist
>>> mylist
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'mylist' is not defined
>>>
```

## 计算中位数
```python
def get_median(data):
     data.sort()
     half = len(data) // 2
     return (data[half] + data[~half]) / 2
```

## 将字符串list转换为int
```python
>>> test_list = ['1', '4', '3', '6', '7']
>>> test_list = list(map(int, test_list))
>>> test_list
[1, 4, 3, 6, 7]
>>>
```

## 合并、连接字符串list
```python
>>> test_list = ['192', '168', '0', '1']
>>> test_list = '.'.join(test_list)
>>> test_list
'192.168.0.1'
>>>
```

## 取多个字符串/list交集
```python
>>> a = ['123','234','1253']
>>> list(reduce(lambda x,y : set(x) & set(y), a))
['2', '3']
>>> b = [[1,2,3],[1,2],[1,2,3,4],[12,1,2]]
>>> list(reduce(lambda x,y : set(x) & set(y), b))
[1, 2]
```

## 合并字典value值
```python
>>> mydict = {0:"hello ", 1:"world"}
>>> mylist =reduce(lambda x, y : x + y, mydict.values())
>>> mylist
'hello world'
>>> mydict = {0:[1,2,3,4], 1:[2,3,4,5,6]}
>>> mylist = list(reduce(lambda x, y : x + y, mydict.values()))
>>> mylist
[1, 2, 3, 4, 2, 3, 4, 5, 6]
>>> field_counters = dict(Counter(mylist))
>>> field_counters
{1: 1, 2: 2, 3: 2, 4: 2, 5: 1, 6: 1}
```
注意在python3中reduce需要导入：
```python
from functools import reduce
```
## 列表排列组合
列表排列组合可以使用迭代器模块itertools

## 列表排列
```python
import itertools

l = [1, 2, 3]
print(list(itertools.permutations(l, 2)))
print(list(itertools.permutations(l, 3)))
```
结果：
```python
[(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
[(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
```

## 组合
```python
import itertools

l = [1, 2, 3]
print(list(itertools.combinations(l, 2)))
```
结果：
```python
[(1, 2), (1, 3), (2, 3)]
```

## 多个列表元素组合：笛卡尔积
两个列表元素两两组合：
```python
import itertools

l = [1, 2, 3]
l1 = [11, 12, 13]
l2 = [21, 22, 23]
# 笛卡尔积
print(list(itertools.product(l, l)))
print(list(itertools.product(l, repeat=2)))
print(list(itertools.product(l1, l2)))
```
结果：
```python
[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
[(11, 21), (11, 22), (11, 23), (12, 21), (12, 22), (12, 23), (13, 21), (13, 22), (13, 23)]
```

## 列表倒序遍历

```python
# reverse方法
a = [1, 2, 3]
a.reverse()
for n in a:
    print(n)

# reversed
for n in reversed(a):
    print(n)  
    
# 切片
a = [1, 2, 3]
b = a[::-1]
```
