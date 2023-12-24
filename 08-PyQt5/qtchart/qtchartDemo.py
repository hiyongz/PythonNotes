from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout
)
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries
import pyqtgraph as pg
import random

## 先启动应用程序
app = QApplication([''])

## 定义顶层Widget
w = QWidget()

## 创建qt Widget
plot = pg.PlotWidget(PdmWidth=200)

## 创建初始绘图，点击饼图后，该图动态更新显示

line_plot=plot.plot([1,2,3,5,8,1,2],pen='r')
plot.setFixedSize(400,400)

## 创建布局(lyaout) 放入 widget
layout = QHBoxLayout()
w.setLayout(layout)

## 创建pie chart
# 事件处理
def on_hover(slice):
        line_plot.setData([random.random()*10 for i in range(7)],pen='b')
        slice.setExploded(not slice.isExploded)
        slice.setLabelVisible(not slice.isLabelVisible())
# 创建Pie chart
def create_piechart():
   
    series = QPieSeries()    
    # 
    series.append("A ", 8)
    series.append("B", 6)
    series.append("C", 5)
    series.append("D", 4)
    series.append("E", 3)

    series.hovered.connect(on_hover)

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

## 添加widget
layout.addWidget(plot)  #右侧，0行，1列，跨越3行,顶部对齐。

pie_plot=create_piechart()
pie_plot.setFixedSize(400,400)
layout.addWidget(pie_plot)  #右侧，0行，1列，跨越3行,顶部对齐。

## 显示
w.setWindowTitle('pyqtgraph 与 pie chart示例')
w.show()

## 开始事件循环
app.exec_()

 