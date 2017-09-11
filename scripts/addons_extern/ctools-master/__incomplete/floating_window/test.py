# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtGui import QIcon

import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(80, 40, 101, 34))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(110, 140, 256, 192))
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(110, 90, 101, 21))
        self.checkBox.setObjectName("checkBox")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(100, 370, 124, 21))
        self.radioButton.setObjectName("radioButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(20, 30))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "col1"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "col2"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "col3"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "A1"))
        self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow", "A2"))
        self.treeWidget.topLevelItem(0).setText(2, _translate("MainWindow", "A3"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "B1"))
        self.treeWidget.topLevelItem(1).setText(1, _translate("MainWindow", "B2"))
        self.treeWidget.topLevelItem(1).setText(2, _translate("MainWindow", "B3"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.radioButton.setText(_translate("MainWindow", "RadioButton"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

class Window(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.restore_settings()
        self.show()

    def closeEvent(self, event):
        print('closeEvent')
        self.save_settings()

    def save_settings(self):
        p = os.path.join(os.path.dirname(__file__), 'test.dat')
        settings = QtCore.QSettings(p, QtCore.QSettings.IniFormat)
        # settings.setIniCodec('utf-8')
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('state', self.saveState())

    def restore_settings(self):
        p = os.path.join(os.path.dirname(__file__), 'test.dat')
        settings = QtCore.QSettings(p, QtCore.QSettings.IniFormat)
        # settings.setIniCodec('utf-8')
        geom = settings.value('geometry')
        if geom is not None:
            self.restoreGeometry(geom)
        state = settings.value('state')
        if state is not None:
            print('restore')
            self.restoreState(state)


# def run():
#     app = QApplication.instance()
#     if not app:
#         app = QApplication(['blender'])
#     win = Window()
#     app.installEventFilter(win)
#     app.exec()
#
# if __name__ == '__main__':
#     run()


import sys

class MyTreeView(QtWidgets.QTreeView):
    def __init__(self,parent=None):
        super(MyTreeView,self).__init__(parent)
        model = QtWidgets.QFileSystemModel()
        model.setRootPath('')
        self.setModel(model)
        self.setRootIndex(model.index(os.path.expanduser('~')))


def main():
    app = QApplication(sys.argv)

    view = MyTreeView()
    view.show()

    app.exec_()

if __name__ == '__main__':
    main()