import os
import random
import pyqtgraph  as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication,QTimer


import sys
import math

from random import randint
import numpy as np

class QMessageBoxDemo:
    def __init__(self):

        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'QMessageBoxDemo.ui') # 当前ui文件的名称
        self.ui = uic.loadUi(file_name) # 加载ui文件
        self.ui.pushButton_clear.clicked.connect(lambda:self.draw())  
        # 更改绘图界面的背景颜色 
        self.ui.graphicsView.setBackground('w') # 更改背景颜色为白色  
        self.timer = QTimer()
        self.msg_box_hint = None

        
    def draw(self):
        self.show_message_box()
        print("111222")
        
        self.close_message_box()

    # 显示界面
    def show(self): 
        self.ui.show()
    
    #定义关闭函数
    def close_message_box(self):
        self.msg_box_hint.close()
    #定义自动关闭对话框函数
    def show_message_box(self):
        self.msg_box_hint = QMessageBox()
        self.msg_box_hint.setIcon(QMessageBox.Information)
        self.msg_box_hint.setWindowTitle('xx')
        self.msg_box_hint.setText('正在处理中，请稍后...')
        self.msg_box_hint.show()
        # self.timer.setSingleShot(True)
        # self.timer.timeout.connect(self.close_message_box)
        # self.timer.start(3000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMessageBoxDemo()
    window.show()
    app.exec()