#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/9 16:24
# @Author:  haiyong
# @File:    parser_xml2.py
import re
import xml.etree.ElementTree as ET
from lxml import etree


class XmlParser():
  def read_xml(self):
    reg = r"([0-9a-fA-F]{2})(([/\s:][0-9a-fA-F]{2}){5})"
    for event, element in etree.iterparse("output2.xml", tag="kw"):

      for child in element:
        if child.tag == "msg":
          if child.text == "REBOOT-TESTERR":
            print(child.tag, child.text)
          res = re.findall(reg, child.text)
          if res:
            print(child.tag, child.text)

  def read_xml2(self):
    reg = r"^([0-9a-fA-F]{2})(([/\s:][0-9a-fA-F]{2}){5})"
    res_list = []
    parser = etree.XMLParser(encoding='utf-8')
    for event, element in etree.iterparse("output.xml", tag="kw"):
      for child in element:
        if child.tag == "msg":
          res = re.findall(reg, child.text)
          if res or child.text == "REBOOT-TESTERR":
            # print(child.tag, child.text)
            res_list.append(child.text)
    # print(res_list)

    err_mac_list = []
    for index, content in enumerate(res_list):
      if content == "REBOOT-TESTERR":
        err_mac_list.append(res_list[index+1])
    print(err_mac_list)
    # element.clear()

if __name__ == '__main__':
    xp = XmlParser()
    xp.read_xml2()