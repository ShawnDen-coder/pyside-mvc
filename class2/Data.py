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
from enum import Enum, unique

from PySide2 import QtXml

@unique
class LIGHT_SHAPES(Enum):
    Poiont = 1
    Spot = 2
    Directional =3
    Area = 4
    Volumetric = 5
    End = 6


class Node:
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

    def attrs(self):
        kv = {}
        for cls in self.__class__.__mro__:
            for k, v in cls.__dict__.items():
                if isinstance(v, property):
                    kv[k] = v.fget(self)

        return kv

    def asXml(self):
        doc = QtXml.QDomDocument()

        node = doc.createElement(self.typeInfo())
        doc.appendChild(node)

        for i in self._children:
            i._recurseXml(doc, node)
        return doc.toString(indent=4)

    def _recurseXml(self, doc, parent):

        node = doc.createElement(self.typeInfo())
        parent.appendChild(node)

        attrs = self.attrs()
        for k, v in attrs.items():
            node.setAttribute(k, v)

        for i in self._children:
            i._recurseXml(doc, node)

    def typeInfo(self):
        return "Node"

    def addChild(self, child):
        self._children.append(child)
        child._parent = self

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
    def name(self, value):
        self._name = value

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

    def data(self, column):
        if column is 0:
            return self.name
        elif column is 1:
            return self.typeInfo()

    def setData(self, column, value):
        if column is 0:
            self.name = value
        if column is 1:
            pass

    def resource(self):
        return None


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

    def data(self, column):
        r = super(TransformNode, self).data(column)
        if column is 2:
            r = self.x
        elif column is 3:
            r = self.y
        elif column is 4:
            r = self.z

        return r

    def setData(self, column, value):
        super(TransformNode, self).setData(column, value)

        if column is 2:
            self.x = value
        elif column is 3:
            self.y = value
        elif column is 4:
            self.z = value

    @property
    def resource(self):
        return 'Resources/三维对象.png'


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


    def typeInfo(self):
        return "CAMERA"

    def data(self, column):
        r = super(CameraNode, self).data(column)
        if column is 2:
            r = self.motionBlur
        elif column is 3:
            r = self.shakeIntensity

        return r

    def setData(self, column, value):
        super(CameraNode, self).setData(column, value)

        if column is 2:
            self.motionBlur = value
        elif column is 3:
            self.shakeIntensity = value

    @property
    def resource(self):
        return 'Resources/三维坐标.png'


class LightNode(Node):
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)

        self._lightIntensity = 1.0
        self._nearRange = 40.0
        self._farRange = 80.0
        self._castShadows = True
        self._shape = LIGHT_SHAPES.Directional.name

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
    @property
    def shape(self):
        return self._shape

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

    @shape.setter
    def shape(self,value):
        self._shape = value


    def typeInfo(self):
        return "LIGHT"

    def data(self, column):
        r = super(LightNode, self).data(column)
        if column is 2:
            r = self.lightIntensity
        elif column is 3:
            r = self.nearRange
        elif column is 4:
            r = self.farRange
        elif column is 5:
            r = self.castShadows
        elif column is 6:
            r = LIGHT_SHAPES[self._shape].value

        return r

    def setData(self, column, value):
        super(LightNode, self).setData(column, value)
        print(column,value)

        if column is 2:
            self.lightIntensity = value
        elif column is 3:
            self.nearRange = value
        elif column is 4:
            self.farRange = value
        elif column is 5:
            self.castShadows = value
        elif column is 6:
            self._shape = LIGHT_SHAPES[value].name
            print(self._shape)

    @property
    def resource(self):
        return 'Resources/三维分析.png'


if __name__ == '__main__':
    light = LightNode("Test")
    print(light.shape)
    print(LIGHT_SHAPES("Poiont").name)

