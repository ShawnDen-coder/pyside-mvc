# -*- coding: utf-8 -*-
"""
@File    :  main.py
@Time    :  2022/11/2 6:11 PM
@Author  :  ShawnDeng
@Contact :  88145482@qq.com
@License :  (C)Copyright 2019-2022
@Desc    :  None
@Version : 0.0.0
# @Software : PyCharm
"""
import sys

from PySide2.QtWidgets import QApplication
from class2.Controllers import uiMainWindow


def run():
    app = QApplication(sys.argv)
    ui = uiMainWindow()
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()