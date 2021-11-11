#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/9 16:06
# @Author:  haiyong
# @File:    parser_xml.py

from xml.etree.ElementTree import iterparse

from collections import Counter

class XmlParser():
    def read_xml(self):
        potholes_by_zip = Counter()

        data = self.parse_and_remove('output.xml', '')
        for pothole in data:
            potholes_by_zip[pothole.findtext('zip')] += 1
        for zipcode, num in potholes_by_zip.most_common():
            print(zipcode, num)


    def parse_and_remove(self,filename, path):
        path_parts = path.split('/')
        doc = iterparse(filename, ('start', 'end'))
        # Skip the root element
        next(doc)

        tag_stack = []
        elem_stack = []
        for event, elem in doc:
            if event == 'start':
                tag_stack.append(elem.tag)
                elem_stack.append(elem)
            elif event == 'end':
                if tag_stack == path_parts:
                    yield elem
                    elem_stack[-2].remove(elem)
                try:
                    tag_stack.pop()
                    elem_stack.pop()
                except IndexError:
                    pass

if __name__ == '__main__':
    xp = XmlParser()
    xp.read_xml()