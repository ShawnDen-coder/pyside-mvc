# -*- coding: utf-8 -*-
"""
@File    :  Models.py
@Time    :  2022/11/2 5:58 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
from PySide2.QtCore import QAbstractItemModel, Qt, QModelIndex
from PySide2.QtGui import QIcon


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
                    return node.castShadows

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
                    return QIcon('Resources/三维分析.png')
                if typeInfo == "CAMERA":
                    return QIcon('Resources/三维坐标.png')
                if typeInfo == "TRANSFORM":
                    return QIcon('Resources/三维对象.png')

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
                    node.castShadows = value

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