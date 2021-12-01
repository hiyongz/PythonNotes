#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/27 17:47
# @Author:  haiyong
# @File:    pytesseract_demo.py
import re

import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

class TesseractDemo():
    def demo(self):
        # 列出支持的语言
        print(pytesseract.get_languages(config=''))

        # If you don't have tesseract executable in your PATH, include the following:
        # pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
        # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

        # Simple image to string
        print(pytesseract.image_to_string(Image.open('test.png'), lang='chi_sim+eng'))

    def osd_demo(self):
        img = Image.open('osd-example.png')
        osd = pytesseract.image_to_osd(img,config='--psm 0 -c min_characters_to_try=5')
        print(osd)
        angle = re.search('(?<=Rotate: )\d+', osd).group(0)
        script = re.search('(?<=Script: )\w+', osd).group(0)
        print("angle: ", angle)
        print("script: ", script)

if __name__ == '__main__':
    tes = TesseractDemo()
    tes.osd_demo()
