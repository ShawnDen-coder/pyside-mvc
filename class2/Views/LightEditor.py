# -*- coding: utf-8 -*-
"""
@File    :  LightEditor.py
@Time    :  2022/11/2 6:04 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QDataWidgetMapper, QFormLayout, QCheckBox, QSpinBox

from class2.Views import LineWidth, LineHeight

class LightEditor(QWidget):
    def __init__(self, parent=None):
        super(LightEditor, self).__init__(parent)
        self.nodeInfoUI()

        # -------------------------< data mapper >------------------------- #
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        self._dataMapper.addMapping(self.lightInternsity_edit, 2)
        self._dataMapper.addMapping(self.nearRange_edit, 3)
        self._dataMapper.addMapping(self.farRange_edit, 4)
        self._dataMapper.addMapping(self.castShadows_edit, 5)
        # self._dataMapper.toFirst()

    def setSelection(self, current):
        """
        :param current: QModelIndex
        :param old: QModelIndex
        :return:
        """
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)

        self._dataMapper.setCurrentModelIndex(current)

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

        fLayout.addRow('Light Internsity', self.lightInternsity_edit)
        fLayout.addRow('Near Range', self.nearRange_edit)
        fLayout.addRow('Far Range', self.farRange_edit)
        fLayout.addRow("Cast Shadows", self.castShadows_edit)
