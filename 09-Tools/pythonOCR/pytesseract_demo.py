#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/27 17:47
# @Author:  haiyong
# @File:    pytesseract_demo.py
import re

import numpy as np
import pytesseract
from pytesseract import Output

import cv2

try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
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

    def demo_image_to_data(self):
        img = Image.open('testimg2.png')
        d = pytesseract.image_to_data(img, output_type=Output.STRING, lang='chi_sim')
        print(d)

        # d = pytesseract.image_to_data(img, lang='chi_sim')

        # font = ImageFont.truetype("simhei.ttf", 15, encoding="utf-8")

    def draw_bounding_boxes1(self):
        """
        识别字符并返回所识别的字符及它们的坐标
        :param im: 需要识别的图片
        :return data: 字符及它们在图片的位置
        """
        # img = Image.open('testimg2.png')
        img = cv2.imread('testimg2.png')
        data = {}
        d = pytesseract.image_to_data(img, output_type=Output.DICT, lang='chi_sim')
        for i in range(len(d['text'])):
            if d['text'][i] != '' and len(d['text'][i]) > 1:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                data[d['text'][i]] = ([d['left'][i], d['top'][i], d['width'][i], d['height'][i]])

                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                # 使用cv2.putText不能显示中文，需要使用下面的代码代替
                # cv2.putText(im, d['text'][i], (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

                pilimg = Image.fromarray(img)
                draw = ImageDraw.Draw(pilimg)

                # 参数1：字体文件路径，参数2：字体大小
                font = ImageFont.truetype("simhei.ttf", 15, encoding="utf-8")
                # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
                draw.text((x, y - 15), d['text'][i], (255, 0, 0), font=font)
                img = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)

        cv2.imshow("TextBoundingBoxes", img)

    def draw_bounding_boxes2(self):
        img = cv2.imread('testimg2.png')
        tess_text = pytesseract.image_to_data(img, output_type=Output.DICT, lang='chi_sim')
        for i in range(len(tess_text['text'])):
            if len(tess_text['text'][i]) > 1:
                (x, y, w, h) = (tess_text['left'][i], tess_text['top'][i], tess_text['width'][i], tess_text['height'][i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                im = Image.fromarray(img)
                draw = ImageDraw.Draw(im)
                font = ImageFont.truetype(font="simsun.ttc", size=18, encoding="utf-8")
                draw.text((x, y - 20), tess_text['text'][i], (255, 0, 0), font=font)
                img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        cv2.imshow("TextBoundingBoxes", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def draw_bounding_boxes3(self):
        img = cv2.imread('testimg2.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        width_list = []
        for c in cnts:
            _, _, w, _ = cv2.boundingRect(c)
            width_list.append(w)
            # cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 1)
        wm = np.median(width_list)
        tess_text = pytesseract.image_to_data(img, output_type=Output.DICT, lang='chi_sim')
        for i in range(len(tess_text['text'])):
            word_len = len(tess_text['text'][i])
            if word_len > 1:
                world_w = int(wm * word_len)
                (x, y, w, h) = (tess_text['left'][i], tess_text['top'][i], tess_text['width'][i], tess_text['height'][i])
                cv2.rectangle(img, (x, y), (x + world_w, y + h), (255, 0, 0), 1)
                im = Image.fromarray(img)
                draw = ImageDraw.Draw(im)
                font = ImageFont.truetype(font="simsun.ttc", size=18, encoding="utf-8")
                draw.text((x, y - 20), tess_text['text'][i], (255, 0, 0), font=font)
                img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        cv2.imshow("TextBoundingBoxes", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def demo_image_to_boxes(self):
        img = Image.open('testimg2.png')
        d = pytesseract.image_to_boxes(img, output_type=Output.DICT, lang='chi_sim')
        print(d)

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

    def image_to_pdf(self):
        pdf = pytesseract.image_to_pdf_or_hocr('testimg2.png', extension='pdf')
        with open('test.pdf', 'w+b') as f:
            f.write(pdf)
    def image_to_hocr(self):
        hocr = pytesseract.image_to_pdf_or_hocr('testimg2.png', extension='hocr')
        xml = pytesseract.image_to_alto_xml('testimg2.png')
        with open('test.xml', 'w+b') as f:
            f.write(xml)


if __name__ == '__main__':
    tes = TesseractDemo()
    # tes.multiple_lang_detect()
    # tes.demo_image_to_data()
    # tes.demo_image_to_boxes()
    # tes.osd_demo()
    # tes.detect_digit()
    # tes.whitelist_characters()
    # tes.blacklist_characters()
    # data = tes.recoText3()
    # tes.draw_bounding_boxes3()
    # tes.image_to_pdf()
    tes.image_to_hocr()

