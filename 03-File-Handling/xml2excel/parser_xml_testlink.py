#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/9 16:06
# @Author:  haiyong
# @File:    parser_xml.py

import xml.etree.ElementTree as ET

from collections import Counter

class XmlParser():
    def read_xml(self):
        potholes_by_zip = Counter()

        tree_data = ET.parse('二层交换机基线.testproject-deep.xml')
        root = tree_data.getroot()
        for child in root:
            print(child)
        for pothole in data:
            potholes_by_zip[pothole.findtext('zip')] += 1
        for zipcode, num in potholes_by_zip.most_common():
            print(zipcode, num)


if __name__ == '__main__':
    xp = XmlParser()
    xp.read_xml()
