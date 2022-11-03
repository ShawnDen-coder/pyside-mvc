# -*- coding: utf-8 -*-
"""
@File    :  NodeUI.py
@Time    :  2022/11/2 6:04 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QFormLayout, QLineEdit


class NodeUI(QWidget):
    def __init__(self, parent=None):
        super(NodeUI, self).__init__(parent)
        self.nodeInfoUI()

    def nodeInfoUI(self):
        fLayout = QFormLayout()
        self.setLayout(fLayout)
        fLayout.setLabelAlignment(Qt.AlignLeft)

        # -------------------------< node info UI >------------------------- #
        self.name_edit = QLineEdit(self)
        self.typeInfo_edit = QLineEdit(self)
        self.typeInfo_edit.setReadOnly(True)
        fLayout.addRow('Name', self.name_edit)
        fLayout.addRow('Type Info', self.typeInfo_edit)
