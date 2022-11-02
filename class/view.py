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

from PySide2.QtCore import Qt, QAbstractListModel, QModelIndex, QAbstractTableModel, QAbstractItemModel, \
    QSortFilterProxyModel, QSize, QObject, SIGNAL
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QTreeView, QApplication, QWidget, \
    QLabel, QSpinBox, QCheckBox, QDoubleSpinBox, QGroupBox, QDataWidgetMapper, QSizePolicy, QScrollArea, QFrame, \
    QAbstractScrollArea

from PySide2.QtGui import QColor, Qt, QPixmap, QIcon
from PySide2.QtWidgets import QListView, QApplication, QComboBox, QTreeView, QTableView, QWidget, QVBoxLayout, QLineEdit


from data import *

LineWidth = 100
LineHeight = 30


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


class CameraEditor(QWidget):
    def __init__(self, parent=None):
        super(CameraEditor, self).__init__(parent)
        self.nodeInfoUI()

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


class TransformEditor(QWidget):
    def __init__(self, parent=None):
        super(TransformEditor, self).__init__(parent)
        self.nodeInfoUI()

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

    def nodeInfoUI(self):
        fLayout = QFormLayout()
        self.setLayout(fLayout)
        fLayout.setLabelAlignment(Qt.AlignLeft)

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


# -------------------------< UI >------------------------- #
class PropertiesEditor(QWidget):
    def __init__(self, parent=None):
        super(PropertiesEditor, self).__init__(parent)
        self.initUI()
        self._proxyModel = None

    def initUI(self):

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        box = QGroupBox(self)
        main_layout.addWidget(box)

        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        box.setTitle("Properties")
        boxHLayout = QVBoxLayout()
        box.setLayout(boxHLayout)

        # -------------------------< properties box add widget >------------------------- #
        self._nodeEditor = NodeEditor(self)
        self._lightEditor = LightEditor(self)
        self._cameraEditor = CameraEditor(self)
        self._transformEditor = TransformEditor(self)

        boxHLayout.addWidget(self._nodeEditor)
        boxHLayout.addWidget(self._lightEditor)
        boxHLayout.addWidget(self._cameraEditor)
        boxHLayout.addWidget(self._transformEditor)

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
            typeInfo = node.typeInfo()

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
    ui = uiMainWindow()
    ui.show()
    sys.exit(app.exec_())
