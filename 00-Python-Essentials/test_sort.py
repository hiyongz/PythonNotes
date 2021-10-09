#!/usr/bin/python3
# -*-coding:utf-8-*-
a = None
for i in a:
    print("666",i)
d = {"a":24, "g":52, "i":12,"k":33}

a = sorted(d.items(),key=lambda x:x[1], reverse=True)
print(a)

b = sorted(d.items())
print(b)
