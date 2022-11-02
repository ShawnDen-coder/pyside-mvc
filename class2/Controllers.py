# -*- coding: utf-8 -*-
"""
@File    :  Controllers.py
@Time    :  2022/11/2 6:02 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""


from PySide2.QtCore import Qt, QSortFilterProxyModel
from PySide2.QtWidgets import QWidget, QLineEdit, QVBoxLayout, \
    QTreeView, QScrollArea, QFrame

from class2.Data import TransformNode, Node, LightNode, CameraNode
from class2.Models import SceneGraphModel
from class2.Views.PropertiesEditor import PropertiesEditor


class uiMainWindow(QWidget):
    def __init__(self):
        super(uiMainWindow, self).__init__()
        self.resize(400, 500)

        # -------------------------< data >------------------------- #
        rootNode = Node("Hips")
        childNode0 = TransformNode('a', rootNode)
        childNode1 = LightNode('b', rootNode)
        childNode2 = CameraNode('c', rootNode)
        childNode3 = TransformNode('d', rootNode)
        childNode4 = LightNode('e', rootNode)
        childNode5 = CameraNode('f', rootNode)
        childNode6 = TransformNode('g', childNode5)
        childNode7 = LightNode('h', childNode6)
        childNode8 = CameraNode('i', childNode7)

        # -------------------------< proxy modle >------------------------- #
        self._model = SceneGraphModel(rootNode)

        # View <----> proxyModel <----> Data model
        self._proxyModel = QSortFilterProxyModel(self)

        # self.model.insertLightRows(0, 10)

        self._proxyModel.setSourceModel(self._model)

        # 动态排序
        self._proxyModel.setDynamicSortFilter(True)
        # 不区分大小写
        self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # 设置自定义的filter和sort
        self._proxyModel.setSortRole(SceneGraphModel.sortRole)
        self._proxyModel.setFilterRole(SceneGraphModel.filterRole)
        self._proxyModel.setFilterKeyColumn(0)

        self.initUI()

    def initUI(self):
        self.vLayout = QVBoxLayout()
        self.setLayout(self.vLayout)
        self.uiFilter = QLineEdit(self)
        self.uiTree = QTreeView(self)

        self.uiTree.setModel(self._proxyModel)
        # 设置排序
        self.uiTree.setSortingEnabled(True)
        # 获取输入的filter text
        self.uiFilter.textChanged.connect(
            lambda text: self._proxyModel.setFilterRegExp(text))

        self.vLayout.addWidget(self.uiFilter)
        self.vLayout.addWidget(self.uiTree)

        self.slider = QScrollArea()
        self.slider.setWidgetResizable(True)
        self.slider.setFrameShape(QFrame.NoFrame)

        self._propEditor = PropertiesEditor(self)
        self.slider.setWidget(self._propEditor)

        self.vLayout.addWidget(self.slider)
        self._propEditor.setModel(self._proxyModel)
        self.uiTree.selectionModel().currentChanged.connect(
            lambda index1, index2: self._propEditor.setSelection(index1, index2))
