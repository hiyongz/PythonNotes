import et
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
import sys
import os
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsObject,
        QGraphicsScene, QGraphicsView)
from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
        QPixmap, QPainterPath)
from PyQt5.QtCore import (QEasingCurve, QFileInfo, QLineF, QMimeData,
        QPoint, QPointF, QPropertyAnimation, QRectF, Qt)
 
 
mylist_16=[['XXX_IC','I','II','III','IV','V','VI','VII','VIII','IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI'],
        ['74LS138','A', 'B', 'B', 'G2A', 'G2B', 'G1', 'Y7', 'GND', 'Y6', 'Y5', 'Y4', 'Y3', 'Y2', 'Y1', 'Y0', 'VCC'],
        ['74LS161', '*R', 'CP', 'P0', 'P1', 'P2', 'P3', 'CEP', 'GND', 'PE-', 'CET', 'Q3', 'Q2', 'Q1', 'Q0', 'TC', 'VCC']]
mylist_14=[['XXX_IC','I','II','III','IV','V','VI','VII','VIII','IX', 'X', 'XI', 'XII', 'XIII', 'XIV'],
        ['74LS00','1A', '1B', '1Y', '2A', '2B', '2Y', 'GND', '3Y', '3A', '3B', '4Y', '4A', '4B', 'VCC']]
#  https://www.cnblogs.com/caiya/p/10328010.html
 
class my_mainwindow(QtWidgets.QMainWindow, et.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.name_list_16=['XXX_IC','74LS138','74LS161']
        self.name_list_14 = ['XXX_IC', '74LS00']
        self.comboBox.addItems(self.name_list_16)
        self.comboBox_2.addItems(self.name_list_14)
        self.afterGenerationConfig()
        self.pushButton.clicked.connect(self.task_pushbutton)
        self.pushButton_2.clicked.connect(self.task_pushbutton_2)
 
    def afterGenerationConfig(self):
 
        self.graphicsView.scene = QtWidgets.QGraphicsScene(0, 0, 1024, 768)
        self.orb=OrbitalSimulation(self.graphicsView.scene)
        self.graphicsView.setScene(self.graphicsView.scene)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graphicsView.setSceneRect(0, 0, 1024, 768)  # fix scene size 500 500
        self.graphicsView.setRenderHint(QPainter.Antialiasing)  ##设置视图的抗锯齿渲染模式。
 
    def task_pushbutton(self):
        name=self.comboBox.currentText()
        self.graphicsView.scene.removeItem(self.orb.item1)
        del self.orb.item1
        self.orb.createIC16TypeItem(name)
    def task_pushbutton_2(self):
        name=self.comboBox_2.currentText()
        self.graphicsView.scene.removeItem(self.orb.item2)
        del self.orb.item2
        self.orb.createIC14TypeItem(name)
 
 
class IC16TypeItem(QGraphicsItem):
 
    def __init__(self, PlanetType):
        super(IC16TypeItem, self).__init__()
 
        self.type = PlanetType
        self.sequence=0
        for i in range(3):
            if self.type==mylist_16[i][0]:
                self.sequence=i
 
    def boundingRect(self):##这个纯虚函数将图元的外边界定义为矩形; 所有绘画必须限制在图元的边界矩形内。
        return QRectF(-10, -20, 250, 130)
 
    def paint(self, painter, option, widget):
        painter.setPen(QColor(166,66,250))##.NoPen)
        painter.setBrush(Qt.red)##.darkGray)
        for i in range(8):
            point1=30*i+0
            painter.drawEllipse(point1, 80, 10, 10)
            painter.drawText(point1+2, 110, "%d"%(i+1))
            painter.drawText(point1 + 2, 75, "%s" % (mylist_16[self.sequence][i+1]))
        for i in range(8):
            point1 = 30 * i + 0
            painter.drawEllipse(point1, 0, 10, 10)
            painter.drawText(point1 + 2, -10, "%d" % (16-i))
            painter.drawText(point1 + 2, 23, "%s" % (mylist_16[self.sequence][16-i]))
        painter.setPen(QColor(1, 66, 250))  ##.NoPen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(-5,-5,240,100)
        painter.drawArc(-15,35,20,20,-90*16,180*16)
        painter.setPen(QColor(200, 166, 250))
        painter.drawText(80, 50, "%s"%mylist_16[self.sequence][0])
 
        '''
                .drawPie(0,0,95,95,0*16,120*16)绘制扇形
                .drawArc(0,0,95,95,30*16,120*16)绘制圆弧
                .drawText(50,50,"文字")绘制文本
                .drawRect(0,0,95,95)绘制矩形
                .drawLine(0,0,0,95)  绘制直线
                .drawEllipse(0, 0, 95, 95)绘制椭圆'''
 
class IC14TypeItem(QGraphicsItem):
 
    def __init__(self, PlanetType):
        super(IC14TypeItem, self).__init__()
 
        self.type = PlanetType
        self.sequence=0
        for i in range(2):
            if self.type==mylist_14[i][0]:
                self.sequence=i
 
    def boundingRect(self):##这个纯虚函数将图元的外边界定义为矩形; 所有绘画必须限制在图元的边界矩形内。
        return QRectF(-10, -20, 250, 130)
 
    def paint(self, painter, option, widget):
        painter.setPen(QColor(166,66,250))##.NoPen)
        painter.setBrush(Qt.red)##.darkGray)
        for i in range(7):
            point1=30*i+0
            painter.drawEllipse(point1, 80, 10, 10)
            painter.drawText(point1+2, 110, "%d"%(i+1))
            painter.drawText(point1 + 2, 75, "%s" % (mylist_14[self.sequence][i+1]))
        for i in range(7):
            point1 = 30 * i + 0
            painter.drawEllipse(point1, 0, 10, 10)
            painter.drawText(point1 + 2, -10, "%d" % (14-i))
            painter.drawText(point1 + 2, 23, "%s" % (mylist_14[self.sequence][14-i]))
        painter.setPen(QColor(1, 66, 250))  ##.NoPen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(-5,-5,210,100)
        painter.drawArc(-15,35,20,20,-90*16,180*16)
        painter.setPen(QColor(200, 166, 250))
        painter.drawText(80, 50, "%s"%mylist_14[self.sequence][0])
 
        '''
                .drawPie(0,0,95,95,0*16,120*16)绘制扇形
                .drawArc(0,0,95,95,30*16,120*16)绘制圆弧
                .drawText(50,50,"文字")绘制文本
                .drawRect(0,0,95,95)绘制矩形
                .drawLine(0,0,0,95)  绘制直线
                .drawEllipse(0, 0, 95, 95)绘制椭圆'''
 
 
class CoordTypeItem(QGraphicsItem):
 
    def __init__(self, PlanetType="sun"):
        super(CoordTypeItem, self).__init__()
        self.type = PlanetType
 
    def boundingRect(self):
        return QRectF(0, 0, 1000, 750)
 
    def paint(self, painter, option, widget):
        painter.setPen(QColor(1,66,250))
        painter.drawLine(0,0,0,700)
        painter.drawLine(0, 0, 800, 0)
        painter.drawLine(800, 0, 800, 700)
        painter.drawLine(0, 700, 800, 700)
        painter.setPen(QColor(100, 200, 3))
        painter.drawText(700,120,"led灯")
        painter.drawText(700, 350, "芯片插槽")
        painter.drawText(700, 515, "按键")
        '''
                .drawPie(0,0,95,95,0*16,120*16)绘制扇形
                .drawArc(0,0,95,95,30*16,120*16)绘制圆弧
                .drawText(50,50,"文字")绘制文本
                .drawRect(0,0,95,95)绘制矩形
                .drawLine(0,0,0,95)  绘制直线
                .drawEllipse(0, 0, 95, 95)绘制椭圆
        '''
 
class LEDTypeItem(QGraphicsItem):
 
    def __init__(self, PlanetType):
        super(LEDTypeItem, self).__init__()
        self.type = PlanetType
 
    def boundingRect(self):
        return QRectF(0, 0, 100, 100)
 
    def paint(self, painter, option, widget):
        painter.setPen(QColor(100,66,250))
        painter.setBrush(Qt.red)
        painter.drawEllipse(0, 0, 20, 20)
        painter.drawLine(2, 5, 17, 17)
        painter.drawLine(2, 17, 17, 5)
        painter.setPen(QColor(245, 12, 231))
        painter.drawText(0,-10,"%s"%self.type)
        '''
                .drawPie(0,0,95,95,0*16,120*16)绘制扇形
                .drawArc(0,0,95,95,30*16,120*16)绘制圆弧
                .drawText(50,50,"文字")绘制文本
                .drawRect(0,0,95,95)绘制矩形
                .drawLine(0,0,0,95)  绘制直线
                .drawEllipse(0, 0, 95, 95)绘制椭圆
        '''
 
class KEYTypeItem(QGraphicsItem):
 
    def __init__(self, PlanetType):
        super(KEYTypeItem, self).__init__()
        self.type = PlanetType
 
    def boundingRect(self):
        return QRectF(0, 0, 35, 35)
 
    def paint(self, painter, option, widget):
        painter.setPen(QColor(100,66,250))
        painter.drawRect(0,0,30,20)
        painter.setPen(QColor(100, 166, 250))
        painter.setBrush(Qt.black)
        painter.drawRect(5, 5, 20, 10)
        painter.setPen(QColor(245, 12, 231))
        painter.drawText(4,-10,"%s"%self.type)
 
        '''
                .drawPie(0,0,95,95,0*16,120*16)绘制扇形
                .drawArc(0,0,95,95,30*16,120*16)绘制圆弧
                .drawText(50,50,"文字")绘制文本
                .drawRect(0,0,95,95)绘制矩形
                .drawLine(0,0,0,95)  绘制直线
                .drawEllipse(0, 0, 95, 95)绘制椭圆'''
 
class WireypeItem(QGraphicsItem):
 
    def __init__(self, PlanetType="sun"):
        super(WireypeItem, self).__init__()
        self.type = PlanetType
 
    def boundingRect(self):
        return QRectF(0, 0, 35, 35)
 
    def paint(self, painter, option, widget):
        #painter.setPen(QColor(250,66,250))
        painter.setPen(Qt.DashLine)  # QColor(1,66,250)
        painter.drawLine(0,0,0,-195)
        painter.drawLine(0, -195, 150, -195)
 
        '''
                .drawPie(0,0,95,95,0*16,120*16)绘制扇形
                .drawArc(0,0,95,95,30*16,120*16)绘制圆弧
                .drawText(50,50,"文字")绘制文本
                .drawRect(0,0,95,95)绘制矩形
                .drawLine(0,0,0,95)  绘制直线
                .drawEllipse(0, 0, 95, 95)绘制椭圆'''
 
 
class OrbitalSimulation():
 
    def __init__(self, scene):
        self.scene = scene
        self.createIC16TypeItem('74LS138')
        self.createIC14TypeItem('74LS00')
        self.createLEDTypeItem()
        self.createKEYTypeItem()
        self.createWireTypeItem()
 
        ##坐标系
        self.item=CoordTypeItem()
        self.item.setPos(0,0)
        self.scene.addItem(self.item)
 
    def createIC16TypeItem(self,name):
        self.item1 = IC16TypeItem("%s"%name)
        self.item1.setPos(50, 300)
        self.scene.addItem(self.item1)
 
    def createIC14TypeItem(self,name):
        self.item2 = IC14TypeItem("%s"%name)
        self.item2.setPos(350, 300)
        self.scene.addItem(self.item2)
 
 
    def createLEDTypeItem(self):
        for i in range(8):  ##range(2)=[0 1]
            item = LEDTypeItem('LED%d'%i)## if i else PointTypeItem("sun")
            point1 = 40 * i  +200.0
            item.setPos(point1,100)  ##举例：setPos（50,50）是把（图元坐标）item坐标点(0,0)设置为与（场景坐标）scene坐标点(50,50)重合
            self.scene.addItem(item)
 
    def createKEYTypeItem(self):
        for i in range(8):  ##range(2)=[0 1]
            item=KEYTypeItem('KEY%d'%i)
            #item.setFlag(QGraphicsItem.ItemIsMovable)
            point1 = 50 * i + 200.0
            item.setPos(point1,500)
            self.scene.addItem(item)
 
    def createWireTypeItem(self):
        item=WireypeItem()
        item.setPos(55,300)
        self.scene.addItem(item)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = my_mainwindow()
    myApp.show()
    sys.exit(app.exec_())