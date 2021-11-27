#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/27 17:47
# @Author:  haiyong
# @File:    pytesseract_demo.py

import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

# 列出支持的语言
print(pytesseract.get_languages(config=''))

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
print(pytesseract.image_to_string(Image.open('test.png'), lang='chi_sim+eng'))