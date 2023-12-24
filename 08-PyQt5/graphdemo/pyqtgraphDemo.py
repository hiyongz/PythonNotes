import os
import random
import pyqtgraph  as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5 import uic

import sys
import math

from random import randint
import numpy as np

class pyqtgraphDemo:
    def __init__(self):
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pyqtgraphDemo.ui') # 当前ui文件的名称
        self.ui = uic.loadUi(file_name) # 加载ui文件
        self.ui.pushButton_plot.clicked.connect(lambda:self.draw())  
        self.ui.pushButton_clear.clicked.connect(lambda:self.clear())  
        # 更改绘图界面的背景颜色 
        self.ui.graphicsView.setBackground('w') # 更改背景颜色为白色  

    # def update_plot(self):
    #     self.time = self.time[1:]
    #     self.time.append(self.time[-1] + 1)
    #     self.temperature = self.temperature[1:]
    #     self.temperature.append(randint(20, 40))
    #     self.line.setData(self.time, self.temperature)  
        
    def draw(self):
        self.clear()
        p1 = self.ui.graphicsView.addPlot(title="第一幅图片")
        p1.addLegend((1,1)) # 创建图例并设置图例位置
        self.ui.graphicsView.nextRow() # 切换到下一行 将两幅图片设置为一列
        # self.ui.graphicsView.nextColumn() # 切换到下一列
        p2 = self.ui.graphicsView.addPlot(title="第二幅图片")
        self.ui.graphicsView.nextRow()
        p3 = self.ui.graphicsView.addPlot(title="第三幅图片")
      
        # 设置X和Y轴坐标，将图片显示到绘图界面中

        # 数据1：时间（s）- 距离(km)
        time_list = list(range(0, 500, 5))
        initial_value = 1000  # 初始值km
        length = 100  # 生成列表的长度
        distance_list = []
        # accumulated_list = [initial_value + randint(15 , 30) for i in range(length)]
        for i in range(length):
            initial_value = initial_value + randint(15 , 30)
            distance_list.append(initial_value)

        # 数据2：距离(km) — 自由空间传输损耗（dB）
        fspl_list = list(map(self.fspl, distance_list))
        print(fspl_list)

        x = time_list
        y = distance_list
        # x = list(range(100)) # X轴坐标
        # y = [randint(0 , 100) for _ in range(100)] # Y轴坐标
        self.time = x
        self.temperature = y
        # 更改曲线的颜色、宽度
        # pen1 = pg.mkPen(color = (255 , 0 , 0))
        # pen2 = pg.mkPen(color = (0 , 0 , 255))
        pen1 = pg.mkPen(color = (255 , 0 , 0),width = 2)
        pen2 = pg.mkPen(color = (0 , 0 , 255),width = 2)
        # 设置X轴和Y轴的标签
        p1.setLabel('bottom'  , '时间', units='S') # 设置底部X的标签名字为温度
        p1.setLabel('left'  , '距离', units='Km') # 设置底部Y的标签名字为功率
        # 设置Y轴 刻度 范围
        p1.setXRange(min=0, max=510)
        p1.setYRange(min=900, max=4000)

        # 增加背景网格
        p1.showGrid(x = True , y = True)
        p2.showGrid(x = True , y = True)
        p1.plot(time_list, distance_list, pen =pen1, name="红色")
        
        # x2 = list(range(100)) # X轴坐标
        # y2 = [randint(0 , 100) for _ in range(100)] # Y轴坐标
        # p1.plot(x2,y2, pen=(0,255,0), name="绿色", symbol='+', symbolSize=3, symbolBrush=('r')) # 同一图形显示多条曲线、增加标识
        # # 如果log为 True，则以对数刻度显示刻度并相应地调整值。（x轴的单位可以自动调整ms us 。。。）
        # p1.setLogMode(x=True, y=False)
        p2.setLabel('left'  , '自由空间传输损耗', units='dB') # 设置底部X的标签名字为温度
        p2.setLabel('bottom'  , '距离', units='Km') # 设置底部Y的标签名字为功率
        self.line = p2.plot(distance_list, fspl_list, pen =pen2)
        ay = p2.getAxis('bottom')
        print(distance_list)
        distance_ticks = list(range(1000, 4001, 100))
        ay.setTicks([[(v, str(v)) for v in distance_ticks ]])
        # Add a timer to simulate new temperature measurements 动态画图
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(300)
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start()  

        # 柱状图
        x2 = list(range(20)) # X轴坐标
        y2 = [randint(0 , 20) for _ in range(20)] # Y轴坐标
        bg1 = pg.BarGraphItem(x=x2, height=y2, width=0.3, brush='r')
        # self.ui.graphicsView.nextRow()
        p3.addItem(bg1)
 

    # 创建Pie chart
    def create_piechart(self):
    
        series = QPieSeries()    
        # 
        series.append("A ", 8)
        series.append("B", 6)
        series.append("C", 5)
        series.append("D", 4)
        series.append("E", 3)

        # series.hovered.connect(self.on_hover)

        # 创建QChart实例
        chart = QChart()    
    
        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置动画效果
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # 设置标题
        chart.setTitle("饼图示例")

        # 显示图例
        chart.legend().setVisible(True)

        # 对齐方式
        chart.legend().setAlignment(Qt.AlignBottom)

        # 创建ChartView，它是显示图表的控件
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        
        return chartview

    # 事件处理
    def on_hover(self, slice):
        line_plot.setData([random.random()*10 for i in range(7)],pen='b')
        slice.setExploded(not slice.isExploded)
        slice.setLabelVisible(not slice.isLabelVisible())

    def clear(self):
        self.ui.graphicsView.clear()

    # 显示界面
    def show(self): 
        self.ui.show()
    
    def fspl(self, distance):
        # 发射功率固定为28GHz
        # FSPL = 20×lg(df) + 32.44        
        return 20 * math.log10(distance * 28000) + 32.44

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = pyqtgraphDemo()
    window.show()
    app.exec()