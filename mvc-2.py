# -*- coding: utf-8 -*-
"""
@File    :  mvc-2.py
@Time    :  2022/10/31 10:44 AM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
import sys

import PySide2
import typing
from PySide2.QtCore import QAbstractListModel, QModelIndex, QAbstractTableModel, QAbstractItemModel, QSortFilterProxyModel
from PySide2.QtGui import QColor, Qt, QPixmap, QIcon
from PySide2.QtWidgets import QListView, QApplication, QComboBox, QTreeView, QTableView, QWidget, QVBoxLayout, QLineEdit


class Node:
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return "Node"

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        child._parent = None
        return True

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tablevel=-1):
        output = ""
        tablevel += 1

        for i in range(tablevel):
            output += '\t'

        output += "|---- {}\n".format(self._name)

        for child in self._children:
            output += child.log(tablevel)

        tablevel += 1
        output += '\n'
        return output

    def __repr__(self):
        return self.log()


class TransformNode(Node):
    def __init__(self, name, parent=None):
        super(TransformNode, self).__init__(name, parent)
        self._name = name
        self._children = []
        self._parent = parent

    def typeInfo(self):
        return "TRANSFORM"


class CameraNode(Node):
    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)
        self._name = name
        self._children = []
        self._parent = parent

    def typeInfo(self):
        return "CAMERA"


class LightNode(Node):
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)
        self._name = name
        self._children = []
        self._parent = parent

    def typeInfo(self):
        return "LIGHT"


class SceneGraphModel(QAbstractItemModel):
    sortRole = Qt.UserRole
    filterRole = Qt.UserRole

    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        """
        :param parent:
        :return:
        """
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        """

        :param parent:
        :return:
        """
        return 1

    def data(self, index, role):
        """

        :param index:
        :param role:
        :return:
        """
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return node.name()
            if index.column() == 1:
                return node.typeInfo()

        if role == Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()
                if typeInfo == "LIGHT":
                    return QIcon('Icon/三维分析.png')
                if typeInfo == "CAMERA":
                    return QIcon('Icon/三维坐标.png')
                if typeInfo == "TRANSFORM":
                    return QIcon('Icon/三维对象.png')

        if role == SceneGraphModel.sortRole:
            return node.typeInfo()

        if role == SceneGraphModel.filterRole:
            return node.typeInfo()



    def setData(self, index, value, role=Qt.EditRole):
        """

        :param index:
        :param value:
        :param role:
        :return:
        """
        if index.isValid():
            if role == Qt.EditRole:
                node = index.internalPointer()
                node.setName(value)
                return True
        else:
            return False

    def headerData(self, section, orientation, role):
        """

        :param section:
        :param orientation:
        :param role:
        :return:
        """
        if role == Qt.DisplayRole:
            if section == 0:
                return 'Scenegraph'
            else:
                return 'Type info'

    def flags(self, index):
        """

        :param index:
        :return:
        """
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def index(self, row, column, parent):
        """
        :param row:行
        :param column:列
        :param parent:父节点
        :return:
        """

        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        """

        :return:
        """
        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def getNode(self, index):
        """
        自定义方法，获取父节点
        :param index:
        :return:
        """
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode

    def insertRows(self, rows, count, parent=QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, rows, rows + count - 1)
        for row in range(count):
            childCount = parentNode.childCount()
            childNode = Node('untitled {}'.format(childCount))
            success = parentNode.insertChild(rows, childNode)
        self.endInsertRows()
        return success

    def insertLightRows(self, rows, count, parent=QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, rows, rows + count - 1)
        for row in range(count):
            childCount = parentNode.childCount()
            childNode = LightNode('Light {}'.format(childCount))
            success = parentNode.insertChild(rows, childNode)
        self.endInsertRows()
        return success

    def removeRows(self, rows, count, parent=QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, rows, rows + count - 1)
        for row in range(count):
            success = parentNode.removeChild(rows)
        self.endRemoveRows()

        return success


# -------------------------< UI >------------------------- #
class uiMainWindow(QWidget):
    def __init__(self):
        super(uiMainWindow, self).__init__()
        self.resize(400, 500)
        self.initUI()

        # -------------------------< data >------------------------- #
        rootNode = Node("Hips")
        childNode0 =TransformNode('a',rootNode)
        childNode1 =LightNode('b',rootNode)
        childNode2 =CameraNode('c',rootNode)
        childNode3 =TransformNode('d',rootNode)
        childNode4 =LightNode('e',rootNode)
        childNode5 =CameraNode('f',rootNode)
        childNode3 =TransformNode('g',rootNode)
        childNode4 =LightNode('h',rootNode)
        childNode5 =CameraNode('i',rootNode)

        # -------------------------< proxy modle >------------------------- #
        self._proxyModel = QSortFilterProxyModel()
        """ View <----> proxyModel <----> Data model"""
        self.model = SceneGraphModel(rootNode)
        # self.model.insertLightRows(0, 10)

        self._proxyModel.setSourceModel(self.model)
        # 设置排序
        self.uiTree.setSortingEnabled(True)
        # 动态排序
        self._proxyModel.setDynamicSortFilter(True)
        # 不区分大小写
        self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # 设置自定义的filter和sort
        self._proxyModel.setSortRole(SceneGraphModel.sortRole)
        self._proxyModel.setFilterRole(SceneGraphModel.filterRole)

        self._proxyModel.setFilterKeyColumn(0)


        self.uiTree.setModel(self._proxyModel)
        # 获取输入的filter text
        self.uiFilter.textChanged.connect(
            lambda text: self._proxyModel.setFilterRegExp(text))

    def initUI(self):
        vLayout = QVBoxLayout()
        self.setLayout(vLayout)
        self.uiFilter = QLineEdit(self)
        self.uiTree = QTreeView(self)
        vLayout.addWidget(self.uiFilter)
        vLayout.addWidget(self.uiTree)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = uiMainWindow()
    win.show()
    sys.exit(app.exec_())
