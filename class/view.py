# -*- coding: utf-8 -*-
"""
@File    :  view.py
@Time    :  2022/10/31 4:37 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QTreeView, QApplication, QWidget, \
    QLabel, QSpinBox, QCheckBox,QDoubleSpinBox


class uiMainWindow(QWidget):
    def __init__(self):
        super(uiMainWindow, self).__init__()
        self.resize(400, 500)
        self.nodeInfoUI()

    def nodeInfoUI(self):
        fLayout = QFormLayout()
        self.setLayout(fLayout)
        fLayout.setLabelAlignment(Qt.AlignLeft)


        # -------------------------< node info UI >------------------------- #
        self.name_edit = QLineEdit(self)
        self.typeInfo_edit = QLineEdit(self)
        fLayout.addRow('Name', self.name_edit)
        fLayout.addRow('Name', self.typeInfo_edit)
        # -------------------------< Light UI >------------------------- #
        self.lightInternsity_edit = QSpinBox(self)
        self.lightInternsity_edit.setMinimumWidth(self.name_edit.width() + 30)
        self.lightInternsity_edit.setMinimumHeight(self.name_edit.height())
        self.nearRange_edit = QSpinBox(self)
        self.nearRange_edit.setMinimumWidth(self.name_edit.width() + 30)
        self.nearRange_edit.setMinimumHeight(self.name_edit.height())
        self.farRange_edit = QSpinBox(self)
        self.farRange_edit.setMinimumWidth(self.name_edit.width() + 30)
        self.farRange_edit.setMinimumHeight(self.name_edit.height())
        self.castShadows_edit = QCheckBox(self)

        fLayout.addRow('Light Internsity', self.lightInternsity_edit)
        fLayout.addRow('Near Range', self.nearRange_edit)
        fLayout.addRow('Far Range', self.farRange_edit)
        fLayout.addRow("Cast Shadows",self.castShadows_edit)

        # -------------------------< camera Node UI >------------------------- #
        self.motionBlur_edit = QCheckBox(self)
        self.shakeInternsity_edit = QDoubleSpinBox(self)
        self.shakeInternsity_edit.setMinimumWidth(self.name_edit.width() + 30)
        self.shakeInternsity_edit.setMinimumHeight(self.name_edit.height())

        fLayout.addRow('Motion Blur', self.motionBlur_edit)
        fLayout.addRow("Shake Internsity",self.shakeInternsity_edit)

        # -------------------------< position UI >------------------------- #
        positionLayout = QHBoxLayout()
        self.positionX_edit = QDoubleSpinBox(self)
        self.positionX_edit.setMinimumWidth((self.name_edit.width() + 30)/4)
        self.positionX_edit.setMinimumHeight(self.name_edit.height())

        self.positionY_edit = QDoubleSpinBox(self)
        self.positionY_edit.setMinimumWidth((self.name_edit.width() + 30)/4)
        self.positionY_edit.setMinimumHeight(self.name_edit.height())

        self.positionZ_edit = QDoubleSpinBox(self)
        self.positionZ_edit.setMinimumWidth((self.name_edit.width() + 30)/4)
        self.positionZ_edit.setMinimumHeight(self.name_edit.height())

        positionLayout.addWidget(self.positionX_edit)
        positionLayout.addWidget(self.positionY_edit)
        positionLayout.addWidget(self.positionZ_edit)


        fLayout.addRow("Position",positionLayout)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = uiMainWindow()
    win.show()
    sys.exit(app.exec_())
