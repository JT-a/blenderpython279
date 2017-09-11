# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'splash2.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(519, 585)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = Hoge(Dialog)
        # self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setMinimumSize(QtCore.QSize(501, 282))
        self.graphicsView.setLineWidth(0)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.graphicsView.setBackgroundBrush(brush)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout_interaction = QtWidgets.QHBoxLayout()
        self.horizontalLayout_interaction.setObjectName("horizontalLayout_interaction")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_interaction.addItem(spacerItem)
        self.label_interaction = QtWidgets.QLabel(Dialog)
        self.label_interaction.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_interaction.setObjectName("label_interaction")
        self.horizontalLayout_interaction.addWidget(self.label_interaction)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_interaction.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_interaction)
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_links = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_links.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_links.setObjectName("verticalLayout_links")
        self.label_links = QtWidgets.QLabel(self.widget)
        self.label_links.setObjectName("label_links")
        self.verticalLayout_links.addWidget(self.label_links, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_home = QtWidgets.QPushButton(self.widget)
        # icon = QtGui.QIcon.fromTheme("edit-undo")
        icon = QtGui.QIcon('/home/sui/bf/blender/release/datafiles/blender_icons32_png/icon32_blender.png')
        self.pushButton_home.setIcon(icon)
        self.pushButton_home.setObjectName("pushButton_home")
        self.verticalLayout_links.addWidget(self.pushButton_home)
        self.pushButton_manual = QtWidgets.QPushButton(self.widget)
        self.pushButton_manual.setObjectName("pushButton_manual")
        self.verticalLayout_links.addWidget(self.pushButton_manual)
        self.pushButton_release = QtWidgets.QPushButton(self.widget)
        self.pushButton_release.setObjectName("pushButton_release")
        self.verticalLayout_links.addWidget(self.pushButton_release)
        self.pushButton_credits = QtWidgets.QPushButton(self.widget)
        self.pushButton_credits.setObjectName("pushButton_credits")
        self.verticalLayout_links.addWidget(self.pushButton_credits)
        self.pushButton_donations = QtWidgets.QPushButton(self.widget)
        self.pushButton_donations.setObjectName("pushButton_donations")
        self.verticalLayout_links.addWidget(self.pushButton_donations)
        self.pushButton_python = QtWidgets.QPushButton(self.widget)
        self.pushButton_python.setObjectName("pushButton_python")
        self.verticalLayout_links.addWidget(self.pushButton_python)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_recent = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_recent.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_recent.setObjectName("verticalLayout_recent")
        self.label_recent = QtWidgets.QLabel(self.widget1)
        self.label_recent.setObjectName("label_recent")
        self.verticalLayout_recent.addWidget(self.label_recent, 0, QtCore.Qt.AlignHCenter)
        self.listWidget = QtWidgets.QListWidget(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.verticalLayout_recent.addWidget(self.listWidget)
        self.horizontalLayout_recent_sub = QtWidgets.QHBoxLayout()
        self.horizontalLayout_recent_sub.setObjectName("horizontalLayout_recent_sub")
        self.pushButton_open = QtWidgets.QPushButton(self.widget1)
        self.pushButton_open.setObjectName("pushButton_open")
        self.horizontalLayout_recent_sub.addWidget(self.pushButton_open)
        self.pushButton_recover = QtWidgets.QPushButton(self.widget1)
        self.pushButton_recover.setObjectName("pushButton_recover")
        self.horizontalLayout_recent_sub.addWidget(self.pushButton_recover)
        self.verticalLayout_recent.addLayout(self.horizontalLayout_recent_sub)
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_info = QtWidgets.QHBoxLayout()
        self.horizontalLayout_info.setObjectName("horizontalLayout_info")
        self.label_info_data = QtWidgets.QLabel(Dialog)
        self.label_info_data.setObjectName("label_info_data")
        self.horizontalLayout_info.addWidget(self.label_info_data)
        self.verticalLayout.addLayout(self.horizontalLayout_info)

        self.retranslateUi(Dialog)
        self.listWidget.activated['QModelIndex'].connect(Dialog.accept)
        self.comboBox.activated['int'].connect(Dialog.accept)
        self.pushButton_open.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBox, self.pushButton_home)
        Dialog.setTabOrder(self.pushButton_home, self.pushButton_manual)
        Dialog.setTabOrder(self.pushButton_manual, self.pushButton_release)
        Dialog.setTabOrder(self.pushButton_release, self.pushButton_credits)
        Dialog.setTabOrder(self.pushButton_credits, self.pushButton_donations)
        Dialog.setTabOrder(self.pushButton_donations, self.pushButton_python)
        Dialog.setTabOrder(self.pushButton_python, self.pushButton_open)
        Dialog.setTabOrder(self.pushButton_open, self.pushButton_recover)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_interaction.setText(_translate("Dialog", "Interaction"))
        self.comboBox.setItemText(0, _translate("Dialog", "Blender"))
        self.comboBox.setItemText(1, _translate("Dialog", "3Dsmax"))
        self.comboBox.setItemText(2, _translate("Dialog", "Blender 2012 Experimental"))
        self.comboBox.setItemText(3, _translate("Dialog", "Maya"))
        self.label_links.setText(_translate("Dialog", "Links"))
        self.pushButton_home.setToolTip(_translate("Dialog", "http://www.blender.org"))
        self.pushButton_home.setText(_translate("Dialog", "Home site"))
        self.pushButton_manual.setText(_translate("Dialog", "Manual"))
        self.pushButton_release.setText(_translate("Dialog", "Release Log"))
        self.pushButton_credits.setText(_translate("Dialog", "Credits"))
        self.pushButton_donations.setText(_translate("Dialog", "Donations"))
        self.pushButton_python.setText(_translate("Dialog", "Python API"))
        self.label_recent.setText(_translate("Dialog", "Recent"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Dialog", "Untitled.blend"))
        item.setToolTip(_translate("Dialog", "/home/hoge/blender/27/Untitled.blend"))
        item = self.listWidget.item(1)
        item.setText(_translate("Dialog", "Untitled.002.blend"))
        item = self.listWidget.item(2)
        item.setText(_translate("Dialog", "Untitled.003.blend"))
        item = self.listWidget.item(3)
        item.setText(_translate("Dialog", "SOM12345654321234567543212345.004.blend"))
        item = self.listWidget.item(4)
        item.setText(_translate("Dialog", "test.001.blend"))
        item = self.listWidget.item(5)
        item.setText(_translate("Dialog", "test.002.blend"))
        item = self.listWidget.item(6)
        item.setText(_translate("Dialog", "test.blend"))
        item = self.listWidget.item(7)
        item.setText(_translate("Dialog", "splash.blend"))
        item = self.listWidget.item(8)
        item.setText(_translate("Dialog", "SOM.blend"))
        item = self.listWidget.item(9)
        item.setText(_translate("Dialog", "Holder.blend"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_open.setText(_translate("Dialog", "Open"))
        self.pushButton_recover.setText(_translate("Dialog", "Recover Last"))
        self.label_info_data.setText(_translate("Dialog", "Data: 2016-06-01 00:00, Hash: abcdef0, Branch: master"))

import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtGui import QIcon


class Hoge(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_image()

    def resizeEvent(self, event):
        view_size = self.viewport().size()
        image_size = self.pixmap.size()
        f = view_size.width() / image_size.width()
        if view_size.height() < image_size.height() * f:
            f = view_size.height() / image_size.height()
        f = min(1.0, f)
        self.resetTransform()
        t = self.transform()
        t.scale(f, f)
        self.setTransform(t)

        super().resizeEvent(event)

    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #
    #     pix = QtGui.QPixmap(self.pixmap)
    #     view = self.viewport()
    #     p = pix.scaled(view.width(), view.height(),
    #                              # QtCore.Qt.KeepAspectRatio,
    #                              QtCore.Qt.KeepAspectRatioByExpanding,
    #                              QtCore.Qt.SmoothTransformation)
    #     # self.scene.removeItem(self.pixmap_item)
    #     # self.scene.addItem(p)
    #     # self.viewport().update()
    #     # print(p)
    #
    #     # pixmap = QtGui.QPixmap('/home/sui/bf/patch/splash.png')
    #     # self.pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
    #     # self.scene = QtWidgets.QGraphicsScene(self)
    #     # self.scene.addItem(self.pixmap_item)
    #     # self.setScene(self.scene)
    #
    #     # paint = QtGui.QPainter(self.viewport())
    #     # # paint.setBackground()
    #     # brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
    #     # brush.setStyle(QtCore.Qt.SolidPattern)
    #     # paint.setBackground(brush)
    #     # paint.setBackgroundMode(QtCore.Qt.TransparentMode)
    #     # print(dir(paint))
    #     # view = self.viewport()
    #     # # QtGui.QPixmap(self.m_img)
    #     # qimg = self.m_img.scaled(view.width(), view.height(),
    #     #                          # QtCore.Qt.KeepAspectRatio,
    #     #                          QtCore.Qt.KeepAspectRatioByExpanding,
    #     #                          QtCore.Qt.SmoothTransformation)
    #     # paint.drawImage(0, 0, qimg)
    #     pass

    def set_image(self):
        self.pixmap = QtGui.QPixmap('/home/sui/Pictures/Game/ぱれっと/Ckl5l6uUUAAWR7T.png')
        self.pixmap_item = QtWidgets.QGraphicsPixmapItem(self.pixmap)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.addItem(self.pixmap_item)
        self.setScene(self.scene)


class Splash(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.retranslateUi(self)

        # pixmap = QtGui.QPixmap('/home/sui/bf/patch/splash.png')
        # self.pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        # self.scene = QtWidgets.QGraphicsScene(self)
        # self.scene.addItem(self.pixmap_item)
        # self.graphicsView.setScene(self.scene)

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        # self.graphicsView.set_image()
        self.show()

        # self.scene.sceneRectChanged.connect(self.func)
        # self.graphicsView.fitInView(self.pixmap_item)

    def func(self):
        print(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.reject()
            return True
        # if event.type() == QtCore.QEvent.MouseMove:
        #     return True
        return False


# app = QApplication.instance()
# if not app:
#     print('new')
#     app = QApplication(sys.argv)
# splash = Splash()
# app.installEventFilter(splash)
# app.exec_()