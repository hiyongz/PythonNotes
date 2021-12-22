#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/12/14 10:12
# @Author:  haiyong
# @File:    python_dict.py

class GetDictValue():
    def get_dict_value(self, key, dic, value_list):
        """ 返回嵌套字典指定key的value

        :key: 目标key值

        :dic: 字典数据

        :value_list: 存储结果

        :return: list
        """
        # 输入参数判断
        if not isinstance(value_list, list):
            return 'value_list: 参数类型错误!'

        # 非字典类型(列表、元组)输入，进剥层处理
        if isinstance(dic, (list, tuple)):
            # 非字典类型，则遍历元素深入查找
            for v in dic:
                self.get_dict_value(key, v, value_list)
        # 字典类型输入，进行遍历查找处理
        if isinstance(dic, dict):
            # 查找本层字典
            if key in dic.keys():
                value_list.append(dic[key])  # 传入数据存在则存入tmp_list
            # 在本层字典的值中查找
            for value in dic.values():
                self.get_dict_value(key, value, value_list)
        return value_list

    def demo(self,key,dic,tmp_list):
        return self.get_dict_value(key,dic,tmp_list)

test_dic1 = {'v': [{'g': '6'},[{'g': '7'}, [{'g': 8}]]]}
test_dic2 = {'a': '1', 'g': '2', 'c': {'d': [{'e': [{'f': [{'v': [{'g': '6'}, [{'g': '7'}, [{'g': 8}]]]}, 'm']}]}, 'h', {'g': [10, 12]}]}}
test_dic3 = {'a':'1','g':{'g':'1'},'c':[{'g':'2'}],'d':{'a':['1',{'g':'a','b':4},{'g':['b',{'g':3},({'g':4},{'g':({'g':5})})]}]}}

g = GetDictValue()
result = g.demo('name',test_dic3,[])
# result = g.Get_Target_Value('name',test_dic5,[])
print(result)
