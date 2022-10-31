# -*- coding: utf-8 -*-
"""
@File    :  View.py
@Time    :  2022/10/31 3:39 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
import sys

from PySide2.QtWidgets import *


class uiMainWindow(QWidget):
    def __init__(self):
        super(uiMainWindow, self).__init__()
        self.resize(400, 500)
        self.initUI()

    def initUI(self):
        vLayout = QVBoxLayout()
        self.setLayout(vLayout)

        uiFilter = QLineEdit(self)
        uiTree = QTreeView(self)
        vLayout.addWidget(uiFilter)
        vLayout.addWidget(uiTree)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = uiMainWindow()
    win.show()
    sys.exit(app.exec_())
