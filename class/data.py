# -*- coding: utf-8 -*-
"""
@File    :  data.py
@Time    :  2022/10/31 10:44 AM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""

from PySide2.QtCore import QModelIndex, QAbstractItemModel
from PySide2.QtGui import Qt, QIcon


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
        self._x = 0
        self._y = 0
        self._z = 0

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @z.setter
    def z(self, value):
        self._z = value

    def typeInfo(self):
        return "TRANSFORM"


class CameraNode(Node):
    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)
        self._motionBlur = True
        self._shakeIntensity = 50.0

    @property
    def motionBlur(self):
        return self._motionBlur

    @property
    def shakeIntensity(self):
        return self._shakeIntensity

    @motionBlur.setter
    def motionBlur(self, value):
        self._motionBlur = value

    @shakeIntensity.setter
    def motionBlur(self, value):
        self._shakeIntensity = value

    def typeInfo(self):
        return "CAMERA"


class LightNode(Node):
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)

        self._lightIntensity = 1.0
        self._nearRange = 40.0
        self._farRange = 80.0
        self._castShadows = True

    @property
    def lightIntensity(self):
        return self._lightIntensity

    @property
    def nearRange(self):
        return self._nearRange

    @property
    def farRange(self):
        return self._farRange

    @property
    def castShadows(self):
        return self._castShadows

    @lightIntensity.setter
    def lightIntensity(self, value):
        self._lightIntensity = value

    @nearRange.setter
    def nearRange(self, value):
        self._nearRange = value

    @farRange.setter
    def farRange(self, value):
        self._farRange = value

    @castShadows.setter
    def castShadows(self, value):
        self._castShadows = value

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
        typeInfo = node.typeInfo()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return node.name()
            if index.column() == 1:
                return node.typeInfo()
            if typeInfo == "CAMERA":
                if index.column() == 2:
                    return node.motionBlur
                if index.column() == 3:
                    return node.shakeIntensity
            if typeInfo == "LIGHT":
                if index.column() == 2:
                    return node.lightIntensity
                if index.column() == 3:
                    return node.nearRange
                if index.column() == 4:
                    return node.farRange
                if index.column() == 5:
                    return node.castRange

            if typeInfo == "TRANSFORM":
                if index.column() == 2:
                    return node.x
                if index.column() == 3:
                    return node.y
                if index.column() == 4:
                    return node.z

        if role == Qt.DecorationRole:
            if index.column() == 0:
                if typeInfo == "LIGHT":
                    return QIcon('../Icon/三维分析.png')
                if typeInfo == "CAMERA":
                    return QIcon('../Icon/三维坐标.png')
                if typeInfo == "TRANSFORM":
                    return QIcon('../Icon/三维对象.png')

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
            node = index.internalPointer()
            typeInfo = node.typeInfo()
            print(typeInfo)
            if role == Qt.EditRole:
                if index.column() == 0:
                    node.setName(value)

            if typeInfo == "CAMERA":
                if index.column() == 2:
                    node.motionBlur = value
                if index.column() == 3:
                    node.shakeIntensity = value
            if typeInfo == "LIGHT":
                if index.column() == 2:
                    node.lightIntensity = value
                if index.column() == 3:
                    node.nearRange = value
                if index.column() == 4:
                    node.farRange = value
                if index.column() == 5:
                    node.castRange = value

            if typeInfo == "TRANSFORM":
                if index.column() == 2:
                    node.x = value
                if index.column() == 3:
                    node.y = value
                if index.column() == 4:
                    node.z = value

            self.dataChanged.emit(index, index)
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


if __name__ == '__main__':
    pass
