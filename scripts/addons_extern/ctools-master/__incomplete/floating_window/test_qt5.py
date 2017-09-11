import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QWidget, QApplication


# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#     def initUI(self):
#         self.setGeometry(300, 300, 250, 150)
#         self.setWindowTitle('Event handler')
#         self.show()
#
#         # eventFilter()と関連
#         # self.button.installEventFilter(self)
#
#     def eventFilter(self, obj, event):
#         return False
#
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Escape:
#             self.close()
#
#     def mousePressEvent(self, event):
#         pass
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())

def gen_qt():
    """
    PyQt4 のメインウィンドウの構成を把握する: http://t2y.hatenablog.jp/entry/20100917/1284652234
    http://stackoverflow.com/questions/22234671/pyqt-how-to-stick-a-widget-to-the-bottom-edge-of-dialog
    レイアウトのお話: http://vivi.dyndns.org/vivi/docs/Qt/layout.html

    """
    import sys
    import time
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtWidgets import QAction, qApp, QApplication
    from PyQt5.QtGui import QIcon


    class Window(QtWidgets.QMainWindow):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.init_ui()

        def init_ui(self):
            exitAction = QAction(QIcon('exit.png'), '&Exit', self)
            exitAction.setShortcut('Ctrl+Q')
            exitAction.setStatusTip('Exit application')
            # exitAction.triggered.connect(qApp.quit)
            exitAction.triggered.connect(self.close)

            statusbar = self.statusBar()
            statusbar.showMessage('Ready')

            menubar = self.menuBar()
            fileMenu = menubar.addMenu('&File')
            fileMenu.addAction(exitAction)

            self.toolbar = self.addToolBar('Exit')
            self.toolbar.addAction(exitAction)

            timer = QtCore.QTimer(self)
            timer.timeout.connect(self.timer_event)
            timer.start(100)

            widget = QtWidgets.QWidget(self)
            layout = QtWidgets.QVBoxLayout(widget)
            widget.setLayout(layout)

            self.label = QtWidgets.QLabel(self)

            layout.addWidget(self.label)
            layout.addStretch()

            self.setCentralWidget(widget)  # self.centralWidget()で取得可

            self.setGeometry(300, 300, 300, 200)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.setWindowTitle('QT Test')

            self.show()

        def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key_Escape:
                self.close()

        def timer_event(self):
            self.label.setText(str(time.time()))
            self.label.adjustSize()

        def closeEvent(self, event):
            pass

    app = QApplication.instance()
    if not app:
        print('new')
        app = QApplication(sys.argv)
    win = Window()
    app.exec_()


    print(dir(app))

gen_qt()



