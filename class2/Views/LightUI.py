# -*- coding: utf-8 -*-
"""
@File    :  LightUI.py
@Time    :  2022/11/2 6:04 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QFormLayout, QCheckBox, QSpinBox, QComboBox

from class2.Views import LineWidth, LineHeight


class LightUI(QWidget):
    def __init__(self, parent=None):
        super(LightUI, self).__init__(parent)
        self.nodeInfoUI()

    def nodeInfoUI(self):
        fLayout = QFormLayout()
        self.setLayout(fLayout)
        fLayout.setLabelAlignment(Qt.AlignLeft)

        # -------------------------< Light UI >------------------------- #
        self.lightInternsity_edit = QSpinBox(self)
        self.lightInternsity_edit.setMinimumWidth(LineWidth + 30)
        self.lightInternsity_edit.setMinimumHeight(LineHeight)
        self.nearRange_edit = QSpinBox(self)
        self.nearRange_edit.setMinimumWidth(LineWidth + 30)
        self.nearRange_edit.setMinimumHeight(LineHeight)
        self.farRange_edit = QSpinBox(self)
        self.farRange_edit.setMinimumWidth(LineWidth + 30)
        self.farRange_edit.setMinimumHeight(LineHeight)
        self.castShadows_edit = QCheckBox(self)
        self.castShadows_edit.setFocusPolicy(Qt.StrongFocus)
        self.uiShape = QComboBox(self)
        self.uiShape.setFocusPolicy(Qt.StrongFocus)

        fLayout.addRow('Light Internsity', self.lightInternsity_edit)
        fLayout.addRow('Near Range', self.nearRange_edit)
        fLayout.addRow('Far Range', self.farRange_edit)
        fLayout.addRow("Cast Shadows", self.castShadows_edit)
        fLayout.addRow("Shape", self.uiShape)
