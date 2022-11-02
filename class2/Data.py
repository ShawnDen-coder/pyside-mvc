# -*- coding: utf-8 -*-
"""
@File    :  Data.py
@Time    :  2022/11/2 6:01 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""


class Node:
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

    @property
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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
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

    @property
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
    def shakeIntensity(self, value):
        self._shakeIntensity = value

    @property
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

    @property
    def typeInfo(self):
        return "LIGHT"
