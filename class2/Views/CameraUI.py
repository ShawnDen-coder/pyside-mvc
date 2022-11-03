# -*- coding: utf-8 -*-
"""
@File    :  CameraUI.py
@Time    :  2022/11/2 6:04 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QFormLayout, QDoubleSpinBox, QCheckBox

from class2.Views import LineWidth, LineHeight


class CameraUI(QWidget):
    def __init__(self, parent=None):
        super(CameraUI, self).__init__(parent)
        self.nodeInfoUI()

    def nodeInfoUI(self):
        fLayout = QFormLayout()
        self.setLayout(fLayout)
        fLayout.setLabelAlignment(Qt.AlignLeft)

        # -------------------------< camera Node UI >------------------------- #
        self.motionBlur_edit = QCheckBox(self)
        self.shakeInternsity_edit = QDoubleSpinBox(self)
        self.shakeInternsity_edit.setMinimumWidth(LineWidth + 30)
        self.shakeInternsity_edit.setMinimumHeight(LineHeight)

        fLayout.addRow('Motion Blur', self.motionBlur_edit)
        fLayout.addRow("Shake Internsity", self.shakeInternsity_edit)

        # -------------------------< position UI >------------------------- #
        positionLayout = QHBoxLayout()
        self.positionX_edit = QDoubleSpinBox(self)
        self.positionX_edit.setMinimumWidth((LineWidth + 30) / 3)
        self.positionX_edit.setMinimumHeight(LineHeight)

        self.positionY_edit = QDoubleSpinBox(self)
        self.positionY_edit.setMinimumWidth((LineWidth + 30) / 3)
        self.positionY_edit.setMinimumHeight(LineHeight)

        self.positionZ_edit = QDoubleSpinBox(self)
        self.positionZ_edit.setMinimumWidth((LineWidth + 30) / 3)
        self.positionZ_edit.setMinimumHeight(LineHeight)

        positionLayout.addWidget(self.positionX_edit)
        positionLayout.addWidget(self.positionY_edit)
        positionLayout.addWidget(self.positionZ_edit)

        fLayout.addRow("Position", positionLayout)
