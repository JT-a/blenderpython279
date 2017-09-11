#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PySide import QtGui, QtCore, QtWebKit, QtNetwork

class myWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)

        self.button = QtGui.QPushButton(self)
        self.button.setText("Show Dialog")
        self.button.installEventFilter(self)  # 追加分

        # self.dialog = QtGui.QDialog(self)
        # self.dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.dialog.installEventFilter(self)

        # self.button.clicked.connect(self.dialog.show)

        self.setCentralWidget(self.button)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            print('event', event.type())
            self.setTopLevelWindow()
            # self.dialog.close()

            return True

        return False

    def setTopLevelWindow(self):
        if self.windowState() != QtCore.Qt.WindowMaximized:
            self.showMaximized()
            self.showNormal()

        else:
            self.showNormal()
            self.showMaximized()

        self.raise_()
        self.activateWindow()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myWindow')

    main = myWindow()
    main.show()

    sys.exit(app.exec_())