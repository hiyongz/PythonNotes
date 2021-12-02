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

    def multiple_lang_detect(self):
        img = Image.open('test.png')
        config = r'-l chi_sim+eng --psm 6'
        print(pytesseract.image_to_string(img, config=config))

    def osd_demo(self):
        img = Image.open('osd-example.png')
        osd = pytesseract.image_to_osd(img,config='--psm 0 -c min_characters_to_try=5')
        print(osd)
        angle = re.search('(?<=Rotate: )\d+', osd).group(0)
        script = re.search('(?<=Script: )\w+', osd).group(0)
        print("angle: ", angle)
        print("script: ", script)

    def detect_digit(self):
        img = Image.open('number-example.png')
        config = r'--oem 3 --psm 6 outputbase digits'
        osd = pytesseract.image_to_string(img, config=config)
        print(osd)

    def whitelist_characters(self):
        img = Image.open('number-example.png')
        config = r'-c tessedit_char_whitelist=0123456789 --psm 6'
        print(pytesseract.image_to_string(img, config=config))

    def blacklist_characters(self):
        img = Image.open('number-example.png')
        config = r'-c tessedit_char_blacklist=0123456789 --psm 6'
        print(pytesseract.image_to_string(img, config=config, lang='chi_sim'))


if __name__ == '__main__':
    tes = TesseractDemo()
    tes.multiple_lang_detect()
    # tes.osd_demo()
    # tes.detect_digit()
    # tes.whitelist_characters()
    # tes.blacklist_characters()
