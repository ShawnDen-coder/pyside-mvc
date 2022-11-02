# -*- coding: utf-8 -*-
"""
@File    :  data.py
@Time    :  2022/10/19 12:46 AM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""

import sys

import PySide2
from PySide2.QtCore import QAbstractListModel, QModelIndex, QAbstractTableModel
from PySide2.QtGui import QColor, Qt, QPixmap, QIcon
from PySide2.QtWidgets import QListView, QApplication, QComboBox, QTreeView, QTableView


class PaleteTableModel(QAbstractTableModel):
    def __init__(self, colors=[[]], headers=[], parent=None):
        super(PaleteTableModel, self).__init__(parent)
        self._colors = colors
        self._headers = headers

    def headerData(self, section, orientation, role):
        """
        行、列的头部展示
        :param section: 行索引
        :param orientation: 水平垂直的标识
        :param role: 角色
        :return: 返回水平、垂直的表头
        """
        if role == Qt.DisplayRole:
            # 方向的筛选
            if orientation == Qt.Horizontal:
                # 设置水平的header
                # 当插入列时候，会新增header，所以这里我们也要判断一下，临时给一个header
                if section < len(self._headers):
                    return self._headers[section]
                else:
                    return 'Temp'
            else:
                # 设置垂直的header
                return 'Color {}'.format(section)

    def rowCount(self, parent):
        """
        整个表格的行数
        :param parent:
        :return: int
        """
        return len(self._colors)

    def columnCount(self, parent):
        """
        整个列表的列数
        :param parent:
        :return: int
        """
        return len(self._colors[0])

    def data(self, index, role):
        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            return self._colors[row][col].name()

        if role == Qt.EditRole:
            return self._colors[row][col].name()

        if role == Qt.DecorationRole:
            value = self._colors[row][col]
            pixmap = QPixmap(26, 26)
            pixmap.fill(value.name())
            return QIcon(pixmap)

        if role == Qt.ToolTipRole:
            return "Hex code:" + self._colors[row][col].name()

    def flags(self, index):
        """
        :param index:
        :return: 返回数值展示的功能
        """
        # 这个方法实现了这个模型是可编辑、默认启用、可选中的
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role=Qt.EditRole):
        """
        对展示的数据进行二次编辑
        :param index: 每一行的对象
        :param value: 具体的数值
        :param role: 可编辑类型
        :return:
        """
        if role == Qt.EditRole:
            row = index.row()
            col = index.column()
            color = QColor(value)
            if color.isValid():
                self._colors[row][col] = color
                self.dataChanged.emit(index, index)
                return True
            return False

    def insertRows(self, row, count, parent=QModelIndex()):
        """
        插入行的实现
        :param row: 需要插入的位置
        :param count: 插入多少个
        :param parent: 父节点
        :return:
        """
        # 当我们重写这个函数的时候，我们必须调用一下两个父类方法
        # self.beginInsertRows()
        # 实现内容
        # self.endInsertRows()

        self.beginInsertRows(parent, row, row + count - 1)

        for i in range(count):
            defaultValue = [QColor('#000000') for i in range(self.columnCount(None))]
            self._colors.insert(row, defaultValue)

        self.endInsertRows()
        return True

    def insertColumns(self, column, count, parent=QModelIndex()):
        """
        插入行的实现
        :param column: 需要插入的位置
        :param count: 插入多少个
        :param parent: 父节点
        :return:
        """
        # 当我们重写这个函数的时候，我们必须调用一下两个父类方法
        # self.beginInsertRows()
        # 实现内容
        # self.endInsertRows()

        self.beginInsertColumns(parent, column, column + count - 1)

        rowCount = len(self._colors)
        for i in range(count):
            for j in range(rowCount):
                self._colors[j].insert(column, QColor('#000000'))

        self.endInsertColumns()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        """
        删除行的实现
        :param row:
        :param count:
        :param parent:
        :return:
        """
        # 当我们重写这个函数的时候，我们必须调用一下两个父类方法
        # self.beginRemoveRows()
        # 实现内容
        # self.endRemoveRows()

        self.beginRemoveRows(parent, row, count + row - 1)

        for i in range(count):
            value = self._colors[row]
            self._colors.remove(value)

        self.endRemoveRows()

        return True

    def removeColumns(self, column, count, parent=QModelIndex()):
        """
        删除行的实现
        :param column:
        :param count:
        :param parent:
        :return:
        """
        # 当我们重写这个函数的时候，我们必须调用一下两个父类方法
        # self.beginRemoveRows()
        # 实现内容
        # self.endRemoveRows()

        self.beginRemoveRows(parent, column, count + column - 1)

        for i in range(count):
            for j in range(self.rowCount(None)):
                value = self._colors[j][i]
                self._colors[j].remove(value)

        self.endRemoveRows()

        return True


class PaleteListModel(QAbstractListModel):
    def __init__(self, colors=[], parent=None):
        super(PaleteListModel, self).__init__(parent)
        self._colors = colors

    def headerData(self, section, orientation, role):
        """
        行、列的头部展示
        :param section: 行索引
        :param orientation: 水平垂直的标识
        :param role: 角色
        :return: 返回水平、垂直的表头
        """
        if role == Qt.DisplayRole:
            # 方向的筛选
            if orientation == Qt.Horizontal:
                # 设置水平的header
                return 'Palette'
            else:
                # 设置垂直的header
                return 'Color {}'.format(section)

    def rowCount(self, parent):
        """
        用于返回数据有多行的，必须实现的抽象函数
        :param parent: 用于标识夫控件，例如可以下拉的listwidget的控件
        :return: int 返回整个数据有多少行
        """
        return len(self._colors)

    def data(self, index, role):
        """
        返回具体的每行的数据，返回的多个会一起渲染
        :param index: 这个用于标识索引数据
        :param role: 角色，没太理解
        :return: 返回需要绘制的内容
        """

        row = index.row()
        value = self._colors[row]

        if role == Qt.EditRole:
            # 当为编辑状态的时候，依旧保留原数值，对原数值进行编辑，否则编辑框为空
            return self._colors[row].name()

        if role == Qt.ToolTipRole:
            # 设置提示信息
            return "Hex code:{}".format(self._colors[row].name())

        if role == Qt.DecorationRole:
            # 填充颜色
            pixmap = QPixmap(26, 26)
            pixmap.fill(value)
            icon = QIcon(pixmap)
            return icon

        if role == Qt.DisplayRole:
            # 显示每行的数值
            return value

    def flags(self, index):
        """
        :param index:
        :return: 返回数值展示的功能
        """
        # 这个方法实现了这个模型是可编辑、默认启用、可选中的
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role=Qt.EditRole):
        """
        对展示的数据进行二次编辑
        :param index: 每一行的对象
        :param value: 具体的数值
        :param role: 可编辑类型
        :return:
        """
        if role == Qt.EditRole:
            row = index.row()
            color = QColor(value)
            if color.isValid():
                self._colors[row] = color
                self.dataChanged.emit(index, index)
                return True
            return False

    def insertRows(self, row, count, parent=QModelIndex()):
        """
        插入行的实现
        :param row: 需要插入的位置
        :param count: 插入多少个
        :param parent: 父节点
        :return:
        """
        # 当我们重写这个函数的时候，我们必须调用一下两个父类方法
        # self.beginInsertRows()
        # 实现内容
        # self.endInsertRows()

        self.beginInsertRows(parent, row, row + count - 1)

        for i in range(count):
            self._colors.insert(row, QColor("#000000"))

        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        """
        删除行的实现
        :param row:
        :param count:
        :param parent:
        :return:
        """
        # 当我们重写这个函数的时候，我们必须调用一下两个父类方法
        # self.beginRemoveRows()
        # 实现内容
        # self.endRemoveRows()

        self.beginRemoveRows(parent, row, count + row - 1)

        for i in range(count):
            value = self._colors[row]
            self._colors.remove(value)

        self.endRemoveRows()

        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)

    data = ["one", "two", "three", "four", "five"]

    # -------------------------< show widget >------------------------- #

    list_view = QListView()
    list_view.show()

    tree_view = QTreeView()
    tree_view.show()

    ComboBox = QComboBox()
    ComboBox.show()

    table_view = QTableView()
    table_view.show()

    # -------------------------< color >------------------------- #
    red = QColor(255, 0, 0)
    green = QColor(0, 255, 0)
    blue = QColor(0, 0, 255)

    # -------------------------< table data >------------------------- #
    rowCount = 4
    columnCount = 6
    headers = ['Pallete0', 'Colors', 'Brushes', 'Omg', 'Technical', 'Artist']
    tableData0 = [
        [QColor("#FFFF00") for i in range(columnCount)] for j in range(rowCount)
    ]

    # -------------------------< modle >------------------------- #
    # model = PaleteListModel([red, green, blue])
    model = PaleteTableModel(tableData0, headers)

    # -------------------------< set model >------------------------- #
    list_view.setModel(model)
    tree_view.setModel(model)
    ComboBox.setModel(model)
    table_view.setModel(model)

    # -------------------------< add rows and remove rows >------------------------- #
    # model.insertRows(1, 5, QModelIndex())
    # model.removeRows(1, 5, QModelIndex())

    # -------------------------< table insert and remove >------------------------- #
    model.insertRows(0, 2)
    model.insertColumns(0, 2)
    #
    model.removeRows(0, 3)
    model.removeColumns(0, 1)

    sys.exit(app.exec_())