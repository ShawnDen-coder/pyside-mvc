# -*- coding: utf-8 -*-
"""
@File    :  PropertiesEditor.py
@Time    :  2022/11/2 6:10 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QDataWidgetMapper, QFormLayout, QLineEdit, QSizePolicy, QGroupBox, QVBoxLayout

from class2.Views.CameraEditor import CameraEditor
from class2.Views.LightEditor import LightEditor
from class2.Views.NodeEditor import NodeEditor
from class2.Views.TransformEditor import TransformEditor


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
