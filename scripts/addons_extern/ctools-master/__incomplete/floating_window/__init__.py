# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
変換方法 http://kuroneko0208.hatenablog.com/entry/2013/02/17/025452
% pyuic5 input.ui -o output.py

ui読み込み http://log.noiretaya.com/259
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # Ui Loader
    loader = QtUiTools.QUiLoader()
    # Ui ファイルを読み込んでオブジェクトを取得
    ui = loader.load(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Ui.ui")
    # 表示
    ui.show()
    # 各ウィジェットなどは、デザイナーで設定した名前でアクセスできる
    ui.exit_action.triggered.connect(app.quit)

    sys.exit(app.exec_())
"""

# TODO: modalオペレータ中では実行出来ない物がある
# TODO: ショートカット

bl_info = {
    'name': 'Floating Window',
    'author': 'chromoly',
    'version': (0, 2),
    'blender': (2, 77, 0),
    'location': 'View3D',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View',
}


import ctypes as ct
import importlib
import threading
import queue
import time
import sys
import multiprocessing
import re
import os
import traceback

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtGui import QIcon

import bpy

try:
    importlib.reload(utils)
    importlib.reload(structures)
    importlib.reload(dialog2)
except NameError:
    from . import structures
    from . import dialog2
    from . import splash
from .utils import AddonPreferences, SpaceProperty, AddonKeyMapUtility


class FloatingWindowPreferences(
        AddonKeyMapUtility,
        AddonPreferences,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        super().draw(context, layout.column())


EPS = 0.005

TIMER_STEP = 0.01
QT_TIMER_STEP = 0.05

bl_queue_mp = multiprocessing.Queue()
qt_queue_mp = multiprocessing.Queue()
qt_lock_mp = multiprocessing.Lock()

condition = threading.Condition()


class Window(dialog2.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.retranslateUi(self)

        self.lineEdit.textChanged.connect(self.set_tree_items)
        self.checkBox_re.clicked.connect(self.set_tree_items)
        self.checkBox_category.clicked.connect(self.set_tree_items)
        self.checkBox_name.clicked.connect(self.set_tree_items)
        self.checkBox_descrption.clicked.connect(self.set_tree_items)
        self.checkBox_idname.clicked.connect(self.set_tree_items)

        self.treeWidget.itemDoubleClicked.connect(self.accept)

        self.gen_operator_list()
        self.set_tree_items('')
        self.init_tree_column_width()

        self.init_ui()

        self.mco_press = None

        self.restore_settings()
        self.treeWidget.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)

    def init_ui(self):
         geom = self.geometry()
         width = geom.width()
         height = geom.height()
         p = QtGui.QCursor().pos()
         self.move(p.x() - width / 2, p.y() - height / 2)
         self.setWindowFlags(
             QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
         self.show()

    def gen_operator_list(self):
        def get_operator_type(pyop):
            opinst = pyop.get_instance()
            pyrna = ct.cast(ct.c_void_p(id(opinst)),
                            ct.POINTER(structures.BPy_StructRNA)).contents
            op = ct.cast(ct.c_void_p(pyrna.ptr.data),
                         ct.POINTER(structures.wmOperator)).contents
            return op.type.contents

        self.operators = []

        for mod in dir(bpy.ops):
            for func in dir(getattr(bpy.ops, mod)):
                pyop = getattr(getattr(bpy.ops, mod), func)
                ot = get_operator_type(pyop)
                # if bool(ot.flag & structures.OPTYPE_INTERNAL):
                #     continue
                rna_type = pyop.get_rna().rna_type
                # self.treeWidget.addTopLevelItem()でも可？
                m = pyop.idname_py().split('.')[0]
                self.operators.append(
                    {'idname': pyop.idname_py(),
                     'category': ' '.join([s.title() for s in m.split('_')]),
                     'name': rna_type.name,
                     'description': rna_type.description,
                     'internal': bool(ot.flag & structures.OPTYPE_INTERNAL),
                     'poll': pyop.poll()
                     }
                )

    def set_tree_items(self, _text):
        self.treeWidget.clear()

        text = self.lineEdit.text()
        try:
            pattern = re.compile(text)
        except Exception:
            pattern = None
            traceback.print_exc()
        text = text.replace('　', ' ').lower()
        text_ls = [t for t in text.split(' ') if t]

        use_re = self.checkBox_re.isChecked()
        use_category = self.checkBox_category.isChecked()
        use_name = self.checkBox_name.isChecked()
        use_description = self.checkBox_descrption.isChecked()
        use_idnamee = self.checkBox_idname.isChecked()
        def match(op):
            if use_re:
                if pattern is None:
                    return False
                if use_category:
                    if re.match(pattern, op['category']):
                        return True
                if use_name:
                    if re.match(pattern, op['name']):
                        return True
                if use_description:
                    if re.match(pattern, op['description']):
                        return True
                if use_idnamee:
                    if re.match(pattern, op['idname']):
                        return True
                return False
            else:
                for t in text_ls:
                    find = False
                    if use_category:
                        if t in op['category'].lower():
                            find = True
                    if use_name:
                        if t in op['name'].lower():
                            find = True
                    if use_description:
                        if t in op['description'].lower():
                            find = True
                    if use_idnamee:
                        if t in op['idname'].lower():
                            find = True
                    if not find:
                        return False
                return True

        for op in self.operators:
            if op['internal'] or not op['poll']:
                continue
            if text:
                if not match(op):
                    continue
            item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item.setText(0, op['category'])
            item.setText(1, op['name'])
            item.setText(2, op['description'])
            item.setText(3, op['idname'])
            tooltip = '\n'.join(
                [op['name'],
                 '',
                 op['description'],
                 '',
                 'Python: bpy.ops.{}()'.format(op['idname'])])
            for i in range(3):
                item.setToolTip(i, tooltip)

    def init_tree_column_width(self):
        for i in [0, 1, 3]:
            self.treeWidget.resizeColumnToContents(i)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.reject()
            return True
        # if event.type() == QtCore.QEvent.MouseMove:
        #     return True
        return False

    def keyPressEvent(self, event):
        if event.key() in {QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return}:
            self.accept()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.reject()

    def mousePressEvent(self, event):
        # print(QtCore.Qt.LeftButton & event.buttons())
        if event.button() == QtCore.Qt.LeftButton:
            self.mco_press = event.pos()

    def mouseReleaseEvent(self, event):
        self.mco_press = None

    def mouseMoveEvent(self, event):
        if self.mco_press:
            self.move(event.globalPos() - self.mco_press)

    def timer_event(self):
        try:
            q = bl_queue_mp
            while True:
                item = q.get_nowait()
                if item is None:
                    self.close()
                    break
        except queue.Empty:
            return

    def accept(self):
        self.save_settings()
        items = self.treeWidget.selectedItems()
        if items:
            item = items[0]
            idname = item.text(3)
            op = eval('bpy.ops.' + idname)
            if op.poll():
                op(bpy.context.copy(), 'INVOKE_DEFAULT', True)
        qt_queue_mp.put(None)
        super().accept()

    def reject(self):
        self.save_settings()
        qt_queue_mp.put(None)
        super().reject()

    def closeEvent(self, event):
        print('closeEvent')
        self.save_settings()
        q = qt_queue_mp
        q.put(None)

    def save_settings(self):
        p = os.path.join(os.path.dirname(__file__), 'settings.dat')
        settings = QtCore.QSettings(p, QtCore.QSettings.IniFormat)
        settings.setIniCodec('utf-8')
        settings.setValue('geometry', self.saveGeometry())

    def restore_settings(self):
        p = os.path.join(os.path.dirname(__file__), 'settings.dat')
        settings = QtCore.QSettings(p, QtCore.QSettings.IniFormat)
        settings.setIniCodec('utf-8')
        geom = settings.value('geometry')
        if geom is not None:
            self.restoreGeometry(geom)

class QTWindowBase:
    def __init__(self):
        self.prev_time = 0.0
        self.data = {}
        self.process = None
        self.timer = None
        self.app = self.win = self.event_loop = None
        self.invalid = False

    def init_queue(self):
        global bl_queue_mp, qt_queue_mp
        bl_queue_mp = multiprocessing.Queue()
        qt_queue_mp = multiprocessing.Queue()

    def timer_add(self, context):
        wm = context.window_manager
        self.timer = wm.event_timer_add(TIMER_STEP, context.window)

    def timer_remove(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self.timer)
        self.timer = None


class QTWindow(QTWindowBase, bpy.types.Operator):
    bl_idname = 'wm.qt_window'
    bl_label = 'QT Test'

    bl_options = {'REGISTER'}

    win = None

    def cancel(self, context):
        print('cancel')
        self.timer_remove(context)
        bl_queue_mp.put(None)
        # self.app.quit()
        # self.event_loop.quit()
        # del self.app
        # del self.event_loop

    def modal(self, context, event):
        if self.invalid:
            if event.type != 'WINDOW_DEACTIVATE':
                self.invalid = False
                return {'CANCELLED'}
        t = time.perf_counter()
        if event.type != 'TIMER' or t - self.prev_time + EPS < TIMER_STEP:
            return {'PASS_THROUGH'}

        self.prev_time = t

        self.event_loop.processEvents()
        # self.app.sendPostedEvents(None, 0)

        # actob = context.active_object
        # name = actob.name if actob else ''
        # if name != self.data.get('name'):
        #     bl_queue_mp.put(name)
        #     self.data['name'] = name

        try:
            while True:
                item = qt_queue_mp.get_nowait()
                if item is None:
                    self.cancel(context)
                    self.invalid = True
                    return {'PASS_THROUGH'}
                    # return {'CANCELLED'}
        except queue.Empty:
            return {'PASS_THROUGH'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        """
        :param context: bpy.types.Context
        :param event: bpy.types.Event
        """

        cls = self.__class__

        wm = context.window_manager
        wm.modal_handler_add(self)
        self.timer_add(context)
        self.prev_time = time.perf_counter()

        self.init_queue()
        app = QApplication.instance()
        if not app:
            app = QApplication(['blender'])
        self.app = app

        self.event_loop = QtCore.QEventLoop()

        cls.win = Window()
        app.installEventFilter(cls.win)

        return {'RUNNING_MODAL'}


def qt_app_mp():
    app = QApplication.instance()
    if not app:
        app = QApplication(['blender'])
    win = Window()
    app.installEventFilter(win)
    app.exec()


class QTWindowMP(QTWindowBase, bpy.types.Operator):
    bl_idname = 'wm.qt_window_mp'
    bl_label = 'QT Test MP'

    bl_options = {'REGISTER'}

    def cancel(self, context):
        self.timer_remove(context)
        bl_queue_mp.put(None)
        self.process.join()
        self.process = None

    def modal(self, context, event):
        t = time.perf_counter()
        if event.type != 'TIMER' or t - self.prev_time + EPS < TIMER_STEP:
            return {'PASS_THROUGH'}

        self.prev_time = t

        actob = context.active_object
        name = actob.name if actob else ''
        if name != self.data.get('name'):
            bl_queue_mp.put(name)
            self.data['name'] = name

        try:
            while True:
                item = qt_queue_mp.get_nowait()
                if item is None:
                    self.cancel(context)
                    return {'CANCELLED'}
        except queue.Empty:
            return {'PASS_THROUGH'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        """
        :param context: bpy.types.Context
        :param event: bpy.types.Event
        """

        wm = context.window_manager
        wm.modal_handler_add(self)
        self.timer_add(context)
        self.prev_time = time.perf_counter()

        self.init_queue()
        self.process = multiprocessing.Process(target=qt_app_mp)
        self.process.daemon = True
        self.process.start()

        return {'RUNNING_MODAL'}


classes = [
    FloatingWindowPreferences,
    QTWindow,
    QTWindowMP,
]

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        addon_prefs = FloatingWindowPreferences.get_instance()
        """:type: FloatingWindowPreferences"""
        # km = addon_prefs.get_keymap('Screen Editing')
        # kmi = km.keymap_items.new('view3d.quadview_move', 'LEFTMOUSE', 'PRESS',
        #                           head=True)
        # addon_keymaps.append((km, kmi))
        addon_prefs.register_keymap_items(addon_keymaps)


def unregister():
    addon_prefs = FloatingWindowPreferences.get_instance()
    """:type: FloatingWindowPreferences"""
    addon_prefs.unregister_keymap_items()

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()


# def top():
#     """http://stackoverflow.com/questions/1925015/pyqt-always-on-top"""
#     import sys
#     # from PyQt4 import QtGui, QtCore
#     from PySide import QtGui, QtCore
#
#     class mymainwindow(QtGui.QMainWindow):
#         def __init__(self):
#             # QtGui.QMainWindow.__init__(self, None,
#             #                            QtCore.Qt.WindowStaysOnTopHint)
#             super().__init__()
#
#             # メニューバー作成
#             menubar = QtGui.QMenuBar()
#             # メニュー作成
#             file_menu = QtGui.QMenu('ファイル', self)
#             # アクション追加
#             exit_action = file_menu.addAction('閉じる')
#             # ショートカットを設定
#             exit_action.setShortcut('Ctrl+Q')
#             # 閉じるのアクションが発火したときはアプリを終了するように
#             exit_action.triggered.connect(QtGui.qApp.quit)
#             # メニューバーにメニューを追加
#             menubar.addMenu(file_menu)
#             # MainWindow にメニューバーを設定
#             self.setMenuBar(menubar)
#
#             self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#             # self.setWindowFlags(
#             #     QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
#
#     app = QtGui.QApplication(sys.argv)
#     mywindow = mymainwindow()
#     mywindow.setWindowTitle("Hello, World!")
#     mywindow.show()
#     app.exec_()


# def test():
#     import sys
#     from PySide import QtGui, QtCore
#
#     app = QtGui.QApplication(sys.argv)
#
#     win = QtGui.QWidget()
#
#     win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#     win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
#
#
#     win.resize(320, 240)
#     win.setWindowTitle("Hello, World!")
#     win.show()
#
#     # sys.exit(app.exec_())
#     app.exec_()