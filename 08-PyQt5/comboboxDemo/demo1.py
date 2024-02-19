import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QComboBoxDemo(QWidget):
    def __init__(self):
        super(QComboBoxDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('下拉列表控件演示')
        self.resize(300, 100)
        layout = QVBoxLayout()  # 设置垂直布局
        self.label = QLabel('选择种类')  # label 1
        self.label1 = QLabel("选择需求")  # label 2

        self.cb = QComboBox()  # 创建下拉列表对象1
        self.cb1 = QComboBox()  # 创建下拉列表对象2
        self.cb.addItem('坚果')  # 添加单个控件
        self.cb.addItem('小球')
        self.cb.addItems(['螺母', '未知'])  # 一次添加多个控件

        # 当下拉复选框内容被选中时  发送信号
        self.cb.currentIndexChanged.connect(self.selectionChange)  # 获取当前选中元素的索引 并按照指定格式输出
        self.cb.activated[str].connect(self.change)  # 获取当前选中元素的索引

        # 把label和combobox 添加进 垂直布局
        layout.addWidget(self.label)
        layout.addWidget(self.cb)
        layout.addWidget(self.label1)
        layout.addWidget(self.cb1)
        self.setLayout(layout)

    def selectionChange(self, i):  # 默认传递两个参数 第二个当前选择的索引
        self.label.setText(self.cb.currentText())  # currentText 返回当前下拉复选框选择的内容
        self.label.adjustSize()
        for count in range(self.cb.count()):  # 获取所有的元素
            print('item' + str(count) + '=' + self.cb.itemText(count))
        print('current index', i, 'selection changed', self.cb.currentText())

    def change(self, s):
        self.cb1.clear()
        if s == "坚果":
            self.cb1.addItem('夏威夷果')  # 添加单个控件
        elif s == "小球":
            self.cb1.addItem('红球')
            self.cb1.addItems(['绿球', '蓝球'])  # 一次添加多个控件
        elif s == "螺母":
            self.cb1.addItem("M12")
        else:
            self.cb1.addItem("请重选")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QComboBoxDemo()
    main.show()
    sys.exit(app.exec_())

