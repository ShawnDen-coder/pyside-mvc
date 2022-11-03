# -*- coding: utf-8 -*-
"""
@File    :  PropertiesUI.py
@Time    :  2022/11/2 6:10 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
from PySide2.QtWidgets import QWidget, QSizePolicy, QGroupBox, QVBoxLayout


class PropertiesUI(QWidget):
    def __init__(self, parent=None):
        super(PropertiesUI, self).__init__(parent)
        self.initUI()


    def initUI(self):

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        box = QGroupBox(self)
        main_layout.addWidget(box)

        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        box.setTitle("Properties")
        self.boxHLayout = QVBoxLayout()
        box.setLayout(self.boxHLayout)



