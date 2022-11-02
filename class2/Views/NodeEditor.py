# -*- coding: utf-8 -*-
"""
@File    :  NodeEditor.py
@Time    :  2022/11/2 6:04 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QDataWidgetMapper, QFormLayout, QLineEdit



class NodeEditor(QWidget):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.nodeInfoUI()

        # -------------------------< data mapper >------------------------- #
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        self._dataMapper.addMapping(self.name_edit, 0)
        self._dataMapper.addMapping(self.typeInfo_edit, 1)
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

        # -------------------------< node info UI >------------------------- #
        self.name_edit = QLineEdit(self)
        self.typeInfo_edit = QLineEdit(self)
        self.typeInfo_edit.setReadOnly(True)
        fLayout.addRow('Name', self.name_edit)
        fLayout.addRow('Type Info', self.typeInfo_edit)

