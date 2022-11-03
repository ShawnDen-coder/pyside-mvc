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
import sys

from PySide2.QtCore import Qt, QSortFilterProxyModel
from PySide2.QtWidgets import QWidget, QLineEdit, QVBoxLayout, \
    QTreeView, QScrollArea, QFrame, QDataWidgetMapper, QApplication

from class2.Data import TransformNode, Node, LightNode, CameraNode
from class2.Models import SceneGraphModel
from class2.Views.CameraUI import CameraUI
from class2.Views.LightUI import LightUI
from class2.Views.NodeUI import NodeUI
from class2.Views.PropertiesUI import PropertiesUI
from class2.Views.TransformUI import TransformUI


class NodeEditor(NodeUI):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)

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


class CameraEditor(CameraUI):
    def __init__(self, parent=None):
        super(CameraEditor, self).__init__(parent)
        # -------------------------< data mapper >------------------------- #
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        self._dataMapper.addMapping(self.motionBlur_edit, 2)
        self._dataMapper.addMapping(self.shakeInternsity_edit, 3)
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


class LightEditor(LightUI):
    def __init__(self, parent=None):
        super(LightEditor, self).__init__(parent)
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


class TransformEditor(TransformUI):
    def __init__(self, parent=None):
        super(TransformEditor, self).__init__(parent)
        # -------------------------< data mapper >------------------------- #
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        self._dataMapper.addMapping(self.positionX_edit, 2)
        self._dataMapper.addMapping(self.positionY_edit, 3)
        self._dataMapper.addMapping(self.positionZ_edit, 4)
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


class PropertiesEditor(PropertiesUI):
    def __init__(self, parent=None):
        super(PropertiesEditor, self).__init__(parent)
        self.addWidget()
        self._proxyModel = None


    def addWidget(self):
        # -------------------------< properties box add widget >------------------------- #
        self._nodeEditor = NodeEditor(self)
        self._lightEditor= LightEditor(self)
        self._cameraEditor = CameraEditor(self)
        self._transformEditor = TransformEditor(self)

        self.boxHLayout.addWidget(self._nodeEditor)
        self.boxHLayout.addWidget(self._lightEditor)
        self.boxHLayout.addWidget(self._cameraEditor)
        self.boxHLayout.addWidget(self._transformEditor)

        # -------------------------< hide widget >------------------------- #
        self._lightEditor.setVisible(False)
        self._cameraEditor.setVisible(False)
        self._transformEditor.setVisible(False)

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel

        self._nodeEditor.setModel(proxyModel)
        self._lightEditor.setModel(proxyModel)
        self._cameraEditor.setModel(proxyModel)
        self._transformEditor.setModel(proxyModel)

    def setSelection(self, current, old):
        """
        :param current: QModelIndex
        :return:
        """

        current = self._proxyModel.mapToSource(current)
        node = current.internalPointer()
        if node is not None:
            typeInfo = node.typeInfo

        if typeInfo == "CAMERA":
            self._lightEditor.setVisible(False)
            self._cameraEditor.setVisible(True)
            self._transformEditor.setVisible(False)

        elif typeInfo == "LIGHT":
            self._lightEditor.setVisible(True)
            self._cameraEditor.setVisible(False)
            self._transformEditor.setVisible(False)

        elif typeInfo == "TRANSFORM":
            self._lightEditor.setVisible(False)
            self._cameraEditor.setVisible(False)
            self._transformEditor.setVisible(True)

        else:
            self._lightEditor.setVisible(False)
            self._cameraEditor.setVisible(False)
            self._transformEditor.setVisible(False)

        self._nodeEditor.setSelection(current)
        self._lightEditor.setSelection(current)
        self._cameraEditor.setSelection(current)
        self._transformEditor.setSelection(current)


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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CameraEditor()
    ui.show()
    sys.exit(app.exec_())