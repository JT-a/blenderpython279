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


bl_info = {
    'name': 'Pie Menu Old',
    'author': 'chromoly',
    'version': (0, 1, 0),
    'blender': (2, 78, 0),
    'location': 'UserPreferences > Input > Pie Menu',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'User Interface'
}

# texfill.png, texmask.png

import sys
import os
import importlib
from collections import OrderedDict
import time
import math
from contextlib import contextmanager
import ctypes
from ctypes import POINTER, addressof, cast, c_void_p
import types
import re
import inspect
import traceback

import bpy
from mathutils import Vector
import blf
import bgl

from ..utils import vagl as vagl
from ..utils.structures import *
from ..utils import vawm

# from . import drawicon
# from . import preferences
# from .preferences import PieMenuPreferences
#
# from . import oputils
try:
    importlib.reload(drawicon)
    importlib.reload(preferences)
    importlib.reload(oputils)
except NameError:
    from . import drawicon
    from . import preferences
    from . import oputils


config_dir_name = 'piemenus'

PIXEL_SIZE = 1.0

# icon_size = ICON_DEFAULT_HEIGHT * (PIXEL_SIZE * dpi / 72.0)
ICON_DEFAULT_HEIGHT = 16

CALC_TEXT_HEIGHT = 'W'  # text_height = blf.dimensions(0, CALC_TEXT_HEIGHT)[1]

DISABLE_CROSS_CURSOR = True


def is_instance(obj):
    return not (inspect.isroutine(obj) or inspect.isclass(obj))


def get_addon_preferences():
    """:rtype: preferences.PieMenuPreferences"""
    return preferences.PieMenuPreferences.get_instance()


def get_event():
    return WM_OT_pie_menu.event


###############################################################################
# Item, Menu
###############################################################################
class CallMethod:
    """
    class Hoge:
        call_method = CallMethod()

        def hoge(self, context):
            pass

        @classmethod
        def piyo(cls, context):
            pass

    hoge = Hoge()
    hoge.call_method('hoge', context)
    Hoge.call_method('piyo', context)

    """
    def __init__(self):
        pass

    def __get__(self, instance, cls):
        def call_method(name, context):
            if instance is not None:
                obj = getattr(instance, name)
            else:
                obj = getattr(cls, name)
            if isinstance(obj, str):
                if instance is not None:
                    kwargs = {'self': instance, 'context': context}
                else:
                    kwargs = {'cls': cls, 'context': context}
                return oputils.execute(obj, kwargs)
            else:
                return obj(context)

        return call_method


class Item:
    # label = None
    # description = None
    _label = None
    _description = None
    icon = ''
    shortcut = ''
    menu = ''
    """:type: str | Menu | T"""  # インスタンスとクラスのどちらでも可
    shift = None
    ctrl = None
    undo_push = False

    def __new__(cls, label=None):
        item = super().__new__(cls)
        item._label = label
        return item

    def poll(self, context):
        """poll属性は文字列か関数。boolを返す。"""
        return True

    """execute属性は文字列か関数。
    文字列を返すとそのメニューを呼ぶ。
    RUNNING_MODALは自動判定するのでここでは気にしなくていい。
    """
    def execute(self, context):
        pass

    def get_execute_string(self):
        if isinstance(self.execute, str):
            return self.execute
        else:
            try:
                string = inspect.getsource(self.execute)
            except:
                # traceback.print_exc()
                return None
            string = string.strip('\n')
            lines = string.split('\n')
            if len(lines) == 1:
                return string
            else:  # 先頭行とインデントを一段消す
                indent = []
                for line in lines[1:]:
                    m = re.match('(\s*).*', line)
                    indent.append(len(m.group(1)))
                lines = [line[min(indent):] for line in lines[1:]]
                text = '\n'.join(lines)
                if text == 'pass':
                    return None
                else:
                    return text

    @property
    def label(self):
        """空文字はそのまま返す"""
        if self._label is not None:
            return self._label
        else:
            execute_string = self.get_execute_string()
            if execute_string:
                op = oputils.get_operator(execute_string)
                if op:
                    bl_rna = op.get_rna().bl_rna
                    return bl_rna.name
            return ''

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def description(self):
        """空文字はそのまま返す"""
        if self._description is not None:
            return self._description
        else:
            execute_string = self.get_execute_string()
            if execute_string:
                op = oputils.get_operator(execute_string)
                if op:
                    bl_rna = op.get_rna().bl_rna
                    return bl_rna.description
            return ''

    @description.setter
    def description(self, description):
        self._description = description

    call_method = CallMethod()


class Menu:
    idname = ''
    label = ''
    items = None
    """:type: list"""
    next = ''
    """:type: str | Menu | T"""  # インスタンスとクラスのどちらでも可
    prev = ''
    """:type: str | Menu | T"""  # インスタンスとクラスのどちらでも可
    radius = 0
    center_action = 'last'  # 'none', 'last', 'fixed'
    center_index = 0
    icon_size = 0
    release_confirm = 1  # 0:無し, 1:中央以外, 2:全て
    keymap_items = []  # [['3D View', {'type': 'A', 'value': 'PRESS'}]]

    @classmethod
    def get_menu(cls, key):
        if isinstance(key, str):
            if key in cls.menus:
                return cls.menus[key]
            else:
                return None
        elif isinstance(key, Menu) or issubclass(key, Menu):
            return key
        else:
            raise ValueError()

    def __new__(cls, context):
        menu = super().__new__(cls)
        if menu.items is None:
            menu.items = []
        menu.current_items = []
        return menu

    def __init__(self, context):
        pass

    def __call__(self, context):
        """クラスとインスタンス両方で動作するように__call__を定義しておく"""
        return self

    @classmethod
    def poll(cls, context):
        return True

    # 以降は変更禁止属性

    def add_item(self, label=None, empty=False):
        if empty:
            item = None
        else:
            item = Item(label)
        self.items.append(item)
        return item

    def sort_items(self, official=False, sort_last_item_index=False):
        if len(self.items) not in [4, 8]:
            raise ValueError('item数は4か8')
        if len(self.items) == 4:
            if official:
                order = [2, 0, 3, 1]
            else:
                order = [0, 2, 1, 3]
        else:
            if official:
                order = [2, 6, 0, 4, 3, 5, 1, 7]
            else:
                order = [0, 4, 2, 6, 1, 5, 3, 7]  # 対角線で詰める
                # order = [0, 6, 2, 4, 1, 5, 3, 7]  # 上から詰める
                # order = [0, 4, 2, 6, 1, 7, 3, 5]  # 下から詰める
                order = [0, 4, 1, 5, 2, 6, 3, 7]  # 四方を時計回りに埋めてから残りを埋める
        items = list(self.items)
        self.items = [items[i] for i in order]
        if sort_last_item_index:
            i = self.get_last_item_index()
            if i != -1:
                if i < len(order):
                    self.set_last_item_index(order.index(i))

    _last_item_index = {}
    """クラス属性。idnameをキー、インデックスを値
    :type: dict[str, int]
    """
    @classmethod
    def get_last_item_index(cls):
        return cls._last_item_index.get(cls.idname, -1)

    @classmethod
    def set_last_item_index(cls, index):
        cls._last_item_index[cls.idname] = index

    @classmethod
    def clear_last_item_idnex(cls):
        if cls.idname in cls._last_item_index:
            del cls._last_item_index[cls.idname]

    menus = {}
    """全てのMenuを管理。クラス属性。idnameをキー、クラスを値
    :type: dict[str, T]
    """

    @classmethod
    def register_menu(cls, menu):
        cls.menus[menu.idname] = menu

    current_items = None
    """:type: list"""
    item_boundary_angles = []  # [[ang, ang], ...] 前・次のアイテムとの境界
    active_index = -1
    active_item = None
    is_valid_click = True
    co = Vector([0.0, 0.0])

    call_method = CallMethod()

    def update_current_items(self, context, shift, ctrl):
        """current_itemsの更新とpollの実行"""
        items = []
        for item in self.items:
            if item is not None:
                if shift and item.shift:
                    items.append(item.shift)
                elif ctrl and item.ctrl:
                    items.append(item.ctrl)
                else:
                    items.append(item)
            else:
                items.append(None)
        for item in items:
            if item is not None:
                item.enabled = item.call_method('poll', context)
        self.current_items = items

        num = len(self.items)
        pie_angle = math.pi * 2 / num
        prefs = get_addon_preferences()
        if prefs.tacho:
            zero = math.pi * 1.5
        else:
            zero = math.pi * 0.5

        if len(self.items) == 0:
            self.item_boundary_angles = []
        else:
            self.item_boundary_angles = [None] * num
            for i, item in enumerate(self.items):
                if item is None:
                    continue
                j = i + 1
                next_item = self.items[j % num]
                while next_item is None:
                    j += 1
                    next_item = self.items[j % num]
                a = zero - i * pie_angle
                b = zero - j * pie_angle
                c = (a + b) / 2
                self.item_boundary_angles[i] = [None, c % (math.pi * 2)]

            for i, item in enumerate(self.items):
                if item is None:
                    continue
                j = i - 1
                while True:
                    itm = self.item_boundary_angles[j]
                    if itm is not None:
                        a = itm[1]
                        break
                    j -= 1
                self.item_boundary_angles[i][0] = a

    def correct_radius(self):
        """Item同士が重ならないようにMenu半径を大きくする
        """
        prefs = get_addon_preferences()

        if self.radius <= 0:
            self.radius = prefs.menu_radius

        items = self.current_items
        num = len(items)

        if num <= 2:
            # 二個なら衝突しようがない
            return
        else:
            if num == 0:
                pie_angle = math.pi * 2
            else:
                pie_angle = math.pi * 2 / num

            widget_unit = vawm.widget_unit()
            if self.icon_size > 0:
                # icon_box_w = max(widget_unit, self.icon_size + 2)
                icon_box_w = max(widget_unit, self.icon_size)
            else:
                icon_box_w = widget_unit

            # 偶数の場合、icon_boxが最も接近するのは0と1番目のアイテム
            # 奇数なら、一番上の内のどちらか一方ととその下
            a = math.pi * 1.5
            angles = [(a, a + pie_angle)]
            if num % 2 == 1:
                a = math.pi * 0.5 + pie_angle * 0.5
                angles.append((a, a + pie_angle))
            f = 0.0
            for a1, a2 in angles:
                f1 = ((icon_box_w + prefs.item_min_space) /
                      abs(math.cos(a1) - math.cos(a2)))
                f2 = ((icon_box_w + prefs.item_min_space) /
                      abs(math.sin(a1) - math.sin(a2)))
                f = max(f, min(f1, f2))
            radius = f - icon_box_w / 2
            self.radius = max(self.radius, radius)

            # text_boxが最も接近するのは、奇数で12時に最も近いアイテムとその下
            # x * sin(a1) - x * sin(a2) >= widget_unit + item_min_space
            # x * (sin(a1) - sin(a2) >= widget_unit + item_min_space
            if num % 2 == 1:
                a1 = math.pi / 2 - pie_angle * 0.5
            else:
                a1 = math.pi / 2 - pie_angle
            a2 = a1 - pie_angle
            x = ((widget_unit + prefs.item_min_space) /
                 (math.sin(a1) - math.sin(a2)))
            radius = x - icon_box_w / 2
            self.radius = max(self.radius, radius)

    def calc_active(self, mco):
        prefs = get_addon_preferences()
        items = self.current_items

        vec = mco - self.co
        if vec.length < prefs.menu_radius_center:
            active_index = -1
        elif len(items) == 0:
            active_index = -1
        elif len(items) == 1 and items[0] is not None:
            active_index = 0
        else:
            for i, item in enumerate(self.items):
                if item is None:
                    continue
                a1, a2 = self.item_boundary_angles[i]
                v1 = (math.cos(a1), math.sin(a1))
                v2 = (math.cos(a2), math.sin(a2))
                if cross2d(v2, vec) >= 0 and cross2d(vec, v1) >= 0:
                    active_index = i
                    break
            else:
                active_index = 0

        active_item = None
        if active_index == -1:
            if self.center_action == 'last':
                last_item_index = self.get_last_item_index()
                if 0 <= last_item_index < len(items):
                    active_item = items[last_item_index]
            elif self.center_action == 'fixed':
                if 0 <= self.center_index < len(items):
                    active_item = items[self.center_index]
        else:
            active_item = items[active_index]

        return active_index, active_item

    def update_active(self, mco, mco_press):
        """active_indexとactive_itemを更新。
        """
        self.active_index, self.active_item = self.calc_active(mco)
        if mco_press is not None:
            i, _ = self.calc_active(mco_press)
            self.is_valid_click = i == self.active_index
        else:
            self.is_valid_click = True

    @classmethod
    def register_keymap_items(cls):
        import bpy_extras.keyconfig_utils

        kc = bpy.context.window_manager.keyconfigs.addon
        if not kc:
            return

        modal_keymaps = [
            'View3D Gesture Circle',
            'Gesture Border',
            'Gesture Zoom Border',
            'Gesture Straight Line',
            'Standard Modal Map',
            'Knife Tool Modal Map',
            'Transform Modal Map',
            'Paint Stroke Modal',
            'View3D Fly Modal',
            'View3D Walk Modal',
            'View3D Rotate Modal',
            'View3D Move Modal',
            'View3D Zoom Modal',
            'View3D Dolly Modal',
        ]

        def get(ls, keymap_name):
            for name, st, rt, sub in ls:
                if name == keymap_name:
                    is_modal = name in modal_keymaps
                    return kc.keymaps.new(name, space_type=st,
                                          region_type=rt, modal=is_modal)
                elif sub:
                    km = get(sub, keymap_name)
                    if km:
                        return km

        items = []
        for name, kwargs in cls.keymap_items:
            km = get(bpy_extras.keyconfig_utils.KM_HIERARCHY, name)
            d = {'value': 'PRESS', **kwargs}
            try:
                kmi = km.keymap_items.new('wm.pie_menu', **d)
                kmi.properties.idname = cls.idname
                items.append((km, kmi))
            except:
                traceback.print_exc()
        return items


###############################################################################
def cross2d(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


@contextmanager
def window_space(win):
    modelview_mat = bgl.Buffer(bgl.GL_DOUBLE, 16)
    projection_mat = bgl.Buffer(bgl.GL_DOUBLE, 16)
    bgl.glGetDoublev(bgl.GL_MODELVIEW_MATRIX, modelview_mat)
    bgl.glGetDoublev(bgl.GL_PROJECTION_MATRIX, projection_mat)

    matrix_mode = bgl.Buffer(bgl.GL_INT, 1)
    bgl.glGetIntegerv(bgl.GL_MATRIX_MODE, matrix_mode)

    viewport = bgl.Buffer(bgl.GL_INT, 4)
    bgl.glGetIntegerv(bgl.GL_VIEWPORT, viewport)

    bgl.glViewport(0, 0, win.width, win.height)
    bgl.glMatrixMode(bgl.GL_PROJECTION)
    bgl.glLoadIdentity()
    ofs = -0.01
    bgl.glOrtho(ofs, win.width + ofs, ofs, win.height + ofs, -100, 100)
    bgl.glMatrixMode(bgl.GL_MODELVIEW)
    bgl.glLoadIdentity()
    bgl.glMatrixMode(matrix_mode[0])

    yield

    bgl.glViewport(*viewport)

    bgl.glMatrixMode(bgl.GL_PROJECTION)
    bgl.glLoadMatrixd(projection_mat)
    bgl.glMatrixMode(bgl.GL_MODELVIEW)
    bgl.glLoadMatrixd(modelview_mat)
    bgl.glMatrixMode(matrix_mode[0])

    # PyOpenGLの場合
    # modelview_mat = (ctypes.c_double * 16)()
    # glGetDoublev(GL_MODELVIEW_MATRIX, ctypes.byref(modelview_mat))
    #
    # glMatrixMode()等でパラメーターにGLenumが要求される場合は
    # c_uintでなければならない
    # matrix_mode = ctypes.c_uint()
    # glGetIntegerv(GL_MATRIX_MODE, ctypes.byref(matrix_mode))
    # glMatrixMode(matrix_mode)


class DrawingManager:
    @property
    def prefs(self):
        return get_addon_preferences()

    @property
    def menu(self):
        return self.op.menu

    @property
    def icon_box_size(self):
        if self.menu.icon_size > 0:
            # return max(self.widget_unit, self.menu.icon_size + 2)
            return max(self.widget_unit, self.menu.icon_size)
        else:
            return self.widget_unit

    def __init__(self, context, op):
        # modal中で変更されるものは入れない
        if not context or not op:
            return
        U = context.user_preferences
        self.op = op

        self.widget_unit = vawm.widget_unit()
        self.dpi = context.user_preferences.system.dpi
        f = PIXEL_SIZE * self.dpi / 72
        # フォントの高さ。blf.dimensionsでは一定にならないのでこれを使う
        self.font_height = U.ui_styles[0].widget.points * f
        self.font_height_mono = U.ui_styles[0].widget.points * f
        # # フォント上端（下端）からwidgetまでの距離
        # self.font_space_y = (self.widget_unit - self.font_height) / 2
        # self.font_space_y_mono = (self.widget_unit - self.font_height_mono) / 2

        self.set_font_size(context)

        # グリフ高さの最大値を求める
        id0 = self.prefs.font_id
        id1 = self.prefs.font_id_mono
        blf.enable(id0, blf.WORD_WRAP)
        blf.enable(id1, blf.WORD_WRAP)
        blf.word_wrap(id0, -1)  # \nでのみ改行を行う
        blf.word_wrap(id1, -1)
        _, h1 = blf.dimensions(id0, '0')
        _, h2 = blf.dimensions(id0, '0\n0')
        self.max_glyph_height = (h2 - h1)
        _, h1 = blf.dimensions(id1, '0')
        _, h2 = blf.dimensions(id1, '0\n0')
        self.max_glyph_height_mono = (h2 - h1)
        blf.disable(id0, blf.WORD_WRAP)
        blf.disable(id1, blf.WORD_WRAP)

        # boxの丸め半径
        self.round_radius = self.widget_unit * 0.2
        # 通常アイコンの大きさ。widget_unit * 0.8 でも可
        self.icon_size = ICON_DEFAULT_HEIGHT * f

        # TODO: 暫定的な調整値
        self.ICON_TEXT_MARGIN = self.widget_unit * 0.1

    def update(self, context, op):
        self.__init__(context, op)

    def set_font_size(self, context):
        prefs = self.prefs
        U = context.user_preferences
        size = U.ui_styles[0].widget.points * int(PIXEL_SIZE)
        blf.size(prefs.font_id, size, self.dpi)
        blf.size(prefs.font_id_mono, size, self.dpi)

    def rect_update(self, rect, xmin, ymin, xmax, ymax):
        rect[0] = xmin if rect[0] is None else min(rect[0], xmin)
        rect[1] = ymin if rect[1] is None else min(rect[1], ymin)
        rect[2] = xmax if rect[2] is None else max(rect[2], xmax)
        rect[3] = ymax if rect[3] is None else max(rect[3], ymax)

    def round_corner(self, v, position):
        """丸めた座標のリストを返す"""
        def circle_verts_num(r):
            """描画に最適な？円の頂点数を求める"""
            n = 32
            threshold = 2.0  # pixcel
            while True:
                if r * 2 * math.pi / n > threshold:
                    return n
                n -= 4
                if n < 1:
                    return 1

        r = self.round_radius
        num = circle_verts_num(r)
        n = int(num / 4)
        if num <= 4:
            return [v]
        circle = [[v[0] + r * math.cos(a), v[1] + r * math.sin(a)]
                  for a in [math.pi * 2 / num * i for i in range(num)]]
        if position == 'top_right':
            verts = [[v[0] - r, v[1] - r] for v in circle[0: n + 1]]
            verts[0][0] = v[0]
            verts[-1][1] = v[1]
        elif position == 'top_left':
            verts = [[v[0] + r, v[1] - r] for v in circle[n: n * 2 + 1]]
            verts[0][1] = v[1]
            verts[-1][0] = v[0]
        elif position == 'bottom_left':
            verts = [[v[0] + r, v[1] + r] for v in circle[n * 2: n * 3 + 1]]
            verts[0][0] = v[0]
            verts[-1][1] = v[1]
        elif position == 'bottom_right':
            verts = [[v[0] - r, v[1] + r]
                     for v in (circle[n * 3:] + [circle[0]])]
            verts[0][1] = v[1]
            verts[-1][0] = v[0]

        return verts

    def gen_text_position(self, string, is_mono=False):
        """描画位置のY座標とboxの幅・高さを返すジェネレータ。
        sendメソッドでは (string, is_mono) か string を渡す。
        一行しかない場合、boxの高さはwidget_unitで固定される。
        Noneを渡すと終了。
        :param string: 改行文字を含む場合は複数行と見做し、
            返り値のY座標は最初の行の位置を表す。
        :type string: str:
        :param is_mono: 固定幅文字を使うなら真。
        :type is_mono: bool
        :return: (描画位置のY座標(boxの上端を基準にして負の方向に進む),
                  boxの幅, boxの高さ)
        :rtype tuple
        """
        y = 0
        width = height = 0

        widget_unit = self.widget_unit

        while True:
            if is_mono:
                font_id = self.prefs.font_id_mono
            else:
                font_id = self.prefs.font_id
            th = blf.dimensions(font_id, CALC_TEXT_HEIGHT)[1]
            if string is not None:
                for line in string.split('\n'):
                    if y == 0:
                        h = widget_unit / 2 + th / 2
                    else:
                        if is_mono:
                            h = self.max_glyph_height_mono
                        else:
                            h = self.max_glyph_height
                    y -= h
                    height += h
                    width = max(width, blf.dimensions(font_id, line)[0])
            h_under = widget_unit / 2 - th / 2
            if y == 0:  # 最初の呼び出しでstringが空文字の場合
                recv = (yield 0, widget_unit, widget_unit)
            else:
                recv = (yield y, width + widget_unit, height + h_under)

            if recv is None:
                string, is_mono = None, False
            elif isinstance(recv, str):
                string, is_mono = recv, False
            else:
                string, is_mono = recv

    def draw_box(self, x, y, w, h,
                 col_back=None, col_inner=None, col_outline=None,
                 back_show_shaded=False, back_shadetop=0, back_shadedown=0,
                 inner_show_shaded=False, inner_shadetop=0, inner_shadedown=0):
        round_radius = self.round_radius

        # アンチエイリアスの効き具合が変わってくるので揃える
        # x = int(x)
        # y = int(y)
        # w = int(w)
        # h = int(h)

        if col_back:
            if back_show_shaded:
                color_top, color_bottom = vagl.shade_color(
                    col_back, back_shadetop, back_shadedown)
                vagl.draw_rounded_box(x, y, w, h, round_radius, True,
                                      color_top, color_bottom)
            else:
                bgl.glColor4f(*col_back)
                vagl.draw_rounded_box(x, y, w, h, round_radius, True)
        if col_inner:
            if inner_show_shaded:
                color_top, color_bottom = vagl.shade_color(
                    col_inner, inner_shadetop, inner_shadedown)
                vagl.draw_rounded_box(x, y, w, h, round_radius, True,
                                      color_top, color_bottom)
            else:
                bgl.glColor4f(*col_inner)
                vagl.draw_rounded_box(x, y, w, h, round_radius, True)
        if col_outline:
            bgl.glColor4f(*col_outline)
            vagl.draw_rounded_box(x, y, w, h, round_radius)

    def draw_text_box(
            self, x, y, text, origin='lower_left',
            col_back=None, col_inner=None, col_outline=None, col_text=None,
            back_show_shaded=False, back_shadetop=0, back_shadedown=0,
            inner_show_shaded=False, inner_shadetop=0, inner_shadedown=0,
            is_mono=False):
        """
        :param origin: x, yの基準がboxのどこにあるか。
                enum in ['upper', 'upper_left', 'left', 'lower_left',
                         'lower', 'lower_right', 'right', 'upper_right']
        :type text: str
        """
        prefs = self.prefs
        widget_unit = self.widget_unit

        _, w, h = self.gen_text_position(text, is_mono).send(None)
        if 'right' in origin:
            x -= w
        elif 'left' not in origin:  # ['upper', 'lower']
            x -= w / 2
        if 'upper' in origin:
            y -= h
        elif 'lower' not in origin:  # ['left', 'right']
            y -= h / 2

        self.draw_box(x, y, w, h, col_back, col_inner, col_outline,
                      back_show_shaded, back_shadetop, back_shadedown,
                      inner_show_shaded, inner_shadetop, inner_shadedown)

        if is_mono:
            font_id = prefs.font_id_mono
        else:
            font_id = prefs.font_id
        lines = text.split('\n')
        if col_text:
            bgl.glColor4f(*col_text)
        g = self.gen_text_position(lines[0], is_mono)
        y2 = None
        for line in lines:
            if y2 is None:
                y2, _, _ = g.send(None)
            else:
                y2, _, _ = g.send(line)
            blf.position(font_id, x + widget_unit / 2, y + h + y2, 0)
            vagl.blf_draw(prefs.font_id, line)

    def draw_icon(self, icon, x, y, active, enabled):
        prefs = self.prefs
        colors = prefs.colors

        if self.menu.icon_size > 0:
            icon_size = max(self.menu.icon_size, self.icon_size)
            round_radius = self.round_radius
        else:
            icon_size = self.icon_size
            round_radius = 0.0

        drawn = False
        if icon:
            alpha = 1.0 if enabled else 0.5
            if isinstance(icon, (list, tuple)):
                drawicon.draw_fill(icon, x, y, icon_size, 1.0, round_radius)
                drawn = True
            else:
                drawn = drawicon.draw(icon, x, y, icon_size, alpha,
                                      round_radius)

        # アイコンがない場合は適当な円を描く
        if not drawn:
            if active and enabled:
                bgl.glColor4f(*vagl.thin_color(colors.item_text_sel, 0.5))
            else:
                bgl.glColor4f(*vagl.thin_color(colors.item_text, 0.5))
            bgl.glLineWidth(2.0)
            r = icon_size * 0.3
            vagl.draw_circle(x + icon_size / 2, y + icon_size / 2, r, 32)
            bgl.glLineWidth(1.0)

    def calc_item_rect(self, position, label):
        """Itemの描画位置を求める。
        icon_sizeが0以下('connected')の場合はicon_boxとtext_boxは重なる
        :param position: インデックスか、'top','bottom','right','left'
        :type position: int | str
        :param label: Item.label
        :type label: str
        :return: アイコンとテキスト部分のrect
        :rtype: ([float, float, float, float], [float, float, float, float])
        """
        prefs = self.prefs

        menu = self.menu
        num = len(menu.current_items)

        if num == 0:
            pie_angle = math.pi * 2
        else:
            pie_angle = math.pi * 2 / num
        if prefs.tacho:
            start_angle = math.pi * 1.5
        else:
            start_angle = math.pi * 0.5

        if menu.icon_size > 0:
            # icon_box_size = max(menu.icon_size, self.widget_unit - 2) + 2
            icon_box_size = max(menu.icon_size, self.widget_unit)
        else:
            icon_box_size = self.widget_unit

        if isinstance(position, int):
            angle = start_angle - pie_angle * position
            if position == 0:
                direction = 'bottom' if prefs.tacho else 'top'
            elif num % 2 == 0 and position == int(num / 2):
                direction = 'top' if prefs.tacho else 'bottom'
            elif position < num / 2:
                direction = 'left' if prefs.tacho else 'right'
            else:
                direction = 'right' if prefs.tacho else 'left'
        else:
            if position == 'top':
                angle = math.pi * 0.5
            elif position == 'bottom':
                angle = math.pi * 1.5
            elif position == 'left':
                angle = math.pi
            else:
                angle = 0.0
            direction = position

        v = Vector(((menu.radius + icon_box_size / 2) * math.cos(angle),
                    (menu.radius + icon_box_size / 2) * math.sin(angle)))
        icon_center = menu.co + v

        x = icon_center[0] - icon_box_size / 2
        y = icon_center[1] - icon_box_size / 2
        icon_box_rect = [x, y, x + icon_box_size, y + icon_box_size]

        tw = blf.dimensions(prefs.font_id, label)[0]
        if menu.icon_size > 0:
            if label:
                w = tw + self.widget_unit
                h = self.widget_unit
                if direction in ('top', 'bottom'):
                    if direction == 'top':
                        y = icon_box_rect[3] + 1
                    else:
                        y = icon_box_rect[1] - 1 - h
                    x = icon_center[0] - w / 2
                else:
                    if direction == 'left':
                        x = icon_box_rect[0] - 1 - w
                    else:
                        x = icon_box_rect[2] + 1
                    y = icon_center[1] - h / 2
                text_box_rect = [x, y, x + w, y + h]
            else:
                text_box_rect = None
        else:
            if label:
                h = self.widget_unit
                if direction in ('top', 'bottom'):
                    w = tw + self.widget_unit
                    if direction == 'top':
                        y = icon_box_rect[3] + prefs.item_box_ofsy  # TODO: 符号確認
                    else:
                        y = icon_box_rect[1] - prefs.item_box_ofsy - h
                    x = icon_center[0] - w / 2
                else:
                    w = tw + self.widget_unit * 1.5 + self.ICON_TEXT_MARGIN
                    if direction == 'right':
                        x = icon_box_rect[0]
                    else:
                        x = icon_box_rect[2] - w
                    y = icon_box_rect[1]
                text_box_rect = [x, y, x + w, y + h]
            else:
                text_box_rect = icon_box_rect[:]

        return icon_box_rect, text_box_rect

    def draw_active_item_background(self):
        prefs = self.prefs
        colors = prefs.colors
        menu = self.menu
        items = menu.current_items

        if menu.active_index == -1 or not menu.is_valid_click:
            return
        if not items[menu.active_index]:
            return

        if len(items) == 0:
            pie_angle = math.pi * 2
        else:
            pie_angle = math.pi * 2 / len(items)
        if prefs.tacho:
            angle = math.pi * 1.5
        else:
            angle = math.pi * 0.5
        r_icon = self.icon_box_size / 2

        i = menu.active_index
        subdiv = 32 if len(items) <= 2 else 16
        if 1:
            angle_end = angle - pie_angle * i - pie_angle / 2
            angle_start = angle_end + pie_angle
        else:
            angle_start, angle_end = menu.item_boundary_angles[i]
            if angle_start < angle_end:
                angle_start += math.pi * 2
        angle_subdiv = (angle_start - angle_end) / subdiv
        x, y = menu.co
        bgl.glColor4f(*colors.pie_sel)
        # r1 = prefs.menu_radius_center + (menu.radius - prefs.menu_radius_center) / 2
        r1 = menu.radius - 5
        r2 = menu.radius + r_icon * 2 + 5
        bgl.glBegin(bgl.GL_QUAD_STRIP)
        for m in range(subdiv + 1):
            ang = angle_start - angle_subdiv * m
            cosf = math.cos(ang)
            sinf = math.sin(ang)
            bgl.glVertex2f(x + r1 * cosf, y + r1 * sinf)
            bgl.glVertex2f(x + r2 * cosf, y + r2 * sinf)
        bgl.glEnd()

    def draw_guid_lines(self):
        prefs = self.prefs
        colors = prefs.colors
        menu = self.menu
        items = menu.current_items
        if len(items) == 0:
            pie_angle = math.pi * 2
        else:
            pie_angle = math.pi * 2 / len(items)
        if prefs.tacho:
            angle = math.pi * 1.5
        else:
            angle = math.pi * 0.5
        icon_box_size = self.icon_box_size
        r1 = prefs.menu_radius_center + (menu.radius - prefs.menu_radius_center) / 2
        # r1 = menu.radius
        r2 = menu.radius + icon_box_size + 5
        x, y = menu.co
        col1 = colors.separator
        bgl.glColor4f(*col1)

        if 1:
            for i in range(len(items)):
                if items[i] is None and items[(i + 1) % len(items)] is None:
                    continue
                ang = angle - pie_angle / 2 - i * pie_angle
                cosf = math.cos(ang)
                sinf = math.sin(ang)
                bgl.glBegin(bgl.GL_LINE_STRIP)
                bgl.glVertex2f(x + r1 * cosf, y + r1 * sinf)
                bgl.glVertex2f(x + r2 * cosf, y + r2 * sinf)
                bgl.glEnd()
        else:
            for angles in menu.item_boundary_angles:
                if not angles:
                    continue
                ang, _ = angles
                cosf = math.cos(ang)
                sinf = math.sin(ang)
                bgl.glBegin(bgl.GL_LINE_STRIP)
                bgl.glVertex2f(x + r1 * cosf, y + r1 * sinf)
                bgl.glVertex2f(x + r2 * cosf, y + r2 * sinf)
                bgl.glEnd()

        # 中心の円
        bgl.glColor4f(*colors.line)
        subdiv = 16 if prefs.menu_radius_center < 20 else 32
        vagl.draw_circle(menu.co[0], menu.co[1], prefs.menu_radius_center,
                         subdiv)

    def draw_titles(self):
        """メニュータイトルと、前、次、親メニューを描画"""
        prefs = self.prefs
        colors = prefs.colors
        widget_unit = self.widget_unit
        menu = self.menu

        _icon_box_rect, text_box_rect = self.calc_item_rect('top', 'DUMMY')
        w = blf.dimensions(prefs.font_id, menu.label)[0] + widget_unit
        h = widget_unit
        x = menu.co[0] - w / 2
        y = text_box_rect[3] + widget_unit

        col_kwargs = {
            'col_inner': colors.title_inner_sel,
            'col_outline': colors.title_outline,
            'col_text': colors.title_text_sel,
            'inner_show_shaded': colors.title_show_shaded,
            'inner_shadetop': colors.title_shadetop,
            'inner_shadedown': colors.title_shadedown,
        }
        self.draw_text_box(x, y, menu.label, **col_kwargs)
        self.rect_update(menu.rect, x, y, x + w, y + h)

        # Draw Shift & Ctrl
        has_shift = has_ctrl = False
        for item in menu.items:
            if item is not None:
                if item.shift:
                    has_shift = True
                if item.ctrl:
                    has_ctrl = True

        r = widget_unit * 0.2
        cx = x + w + r + 2
        cy = y + h / 2 + r + 1
        if has_shift:
            bgl.glColor4f(*colors.menu_inner)
            vagl.draw_circle(cx, cy, r, 16, True)
            if self.op.shift:
                bgl.glColor4f(*colors.item_inner_sel)
            else:
                bgl.glColor4f(*colors.item_inner)
            vagl.draw_circle(cx, cy, r, 16, True)
            bgl.glColor4f(*colors.item_outline)
            vagl.draw_circle(cx, cy, r, 16, False)
        cy = y + h / 2 - r - 1
        if has_ctrl:
            bgl.glColor4f(*colors.menu_inner)
            vagl.draw_circle(cx, cy, r, 16, True)
            if self.op.ctrl:
                bgl.glColor4f(*colors.item_inner_sel)
            else:
                bgl.glColor4f(*colors.item_inner)
            vagl.draw_circle(cx, cy, r, 16, True)
            bgl.glColor4f(*colors.item_outline)
            vagl.draw_circle(cx, cy, r, 16, False)

        # others
        col_kw = col_kwargs.copy()
        col_kw['col_inner'] = colors.title_inner
        col_kw['col_text'] = colors.title_text

        # Next
        if menu.next:
            sub_menu = Menu.get_menu(menu.next)
            if sub_menu:
                w2 = blf.dimensions(prefs.font_id, sub_menu.label)[0]
                w2 += widget_unit
                x2 = x + w + widget_unit
                self.draw_text_box(x2, y, sub_menu.label, **col_kw)
                self.rect_update(menu.rect, x2, y, x2 + w2, y + widget_unit)

        # Prev
        if menu.prev:
            sub_menu = Menu.get_menu(menu.prev)
            if sub_menu:
                w2 = blf.dimensions(prefs.font_id, sub_menu.label)[0]
                w2 += widget_unit
                x2 = x - widget_unit - w2
                self.draw_text_box(x2, y, sub_menu.label, **col_kw)
                self.rect_update(menu.rect, x2, y, x2 + w2, y + widget_unit)

        # History
        if self.op.menu_history:
            y2 = y + h + widget_unit / 2
            for sub_menu in self.op.menu_history[::-1]:
                w2 = blf.dimensions(prefs.font_id, sub_menu.label)[0]
                w2 += widget_unit
                x2 = menu.co[0] - w2 / 2
                self.draw_text_box(x2, y2, sub_menu.label, **col_kw)
                self.rect_update(menu.rect, x2, y2, x2 + w2, y2 + widget_unit)
                y2 += widget_unit * 1.5

    def draw_arrow(self):
        """マウスカーソルの方向を指す矢印"""
        prefs = self.prefs
        menu = self.menu
        vec = self.op.mco - menu.co
        r_center2 = prefs.menu_radius_center + 2
        if vec.length >= prefs.menu_radius_center:
            base_w = 16
            top_w = 3
            # handlength = menu.radius - r_center2
            # handlength = max(15, min(handlength, 40))
            # handlength = min(menu.radius - r_center2, self.widget_unit)
            # handlength = max(handlength, self.widget_unit / 2)
            handlength = self.widget_unit * 0.6
            v = vec.normalized()  # copy
            bgl.glColor4f(*prefs.colors.pointer)
            vagl.draw_trapezoid(menu.co + v * r_center2,
                                v * handlength, base_w, top_w, poly=True)
            bgl.glColor4f(*prefs.colors.pointer_outline)
            bgl.glLineWidth(2)
            vagl.draw_trapezoid(menu.co + v * r_center2,
                                v * handlength, base_w, top_w)
            bgl.glLineWidth(1)

    # def get_menu_inner_color(self, y):
    #     """Item.draw()から呼び出す"""
    #     menu = self.menu
    #     prefs = self.prefs
    #     colors = prefs.colors
    #     widget_unit = self.widget_unit
    #     icon_box_size = self.icon_box_size
    #     f = menu.radius + icon_box_size - prefs.item_box_ofsy + widget_unit
    #     menu_ymax = menu.co[1] + f
    #     menu_ymin = menu.co[1] - f
    #     col_menu_inner_top, col_menu_inner_bottom = vagl.shade_color(
    #         colors.menu_inner, colors.menu_shadetop, colors.menu_shadedown)
    #
    #     y = max(menu_ymin, min(y, menu_ymax))
    #     f = (y - menu_ymin) / (menu_ymax - menu_ymin)
    #     if colors.menu_show_shaded:
    #         return vagl.blend_color(col_menu_inner_top,
    #                                 col_menu_inner_bottom, f)
    #     else:
    #         return colors.menu_inner

    def draw_item(self, item, index, icon_center, active, enabled):
        prefs = self.prefs
        menu = self.menu

        colors = prefs.colors
        widget_unit = self.widget_unit

        num = len(menu.current_items)
        if index == 0:
            direction = 'bottom' if prefs.tacho else 'top'
        elif num % 2 == 0 and index == int(num / 2):
            direction = 'top' if prefs.tacho else 'bottom'
        elif index < num / 2:
            direction = 'left' if prefs.tacho else 'right'
        else:
            direction = 'right' if prefs.tacho else 'left'

        icon_box = item.icon_box_rect
        text_box = item.text_box_rect

        if active:
            col = colors.item_inner_sel
            if not enabled:
                col = vagl.thin_color(col, 0.5)  # TODO: 調整
        else:
            col = colors.item_inner
        if colors.item_show_shaded:
            col_box_top, col_box_bottom = vagl.shade_color(
                col, colors.item_shadetop, colors.item_shadedown)
        else:
            col_box_top = col_box_bottom = col

        u1, v1, u2, v2 = icon_box
        trapezoid = prefs.item_box_trapezoid
        if menu.icon_size > 0:
            icon_box_poly_coords = line_coords_icon = (
                self.round_corner([u1, v1], 'bottom_left') +
                self.round_corner([u2, v1], 'bottom_right') +
                self.round_corner([u2, v2], 'top_right') +
                self.round_corner([u1, v2], 'top_left')
            )
            icon_size = max(menu.icon_size, self.icon_size)
        else:
            if direction == 'top':
                # add icon box (左上から)
                icon_box_poly_coords = (
                    [[u1 - trapezoid, v2 + prefs.item_box_ofsy]] +
                    self.round_corner([u1, v1], 'bottom_left') +
                    self.round_corner([u2, v1], 'bottom_right') +
                    [[u2 + trapezoid, v2 + prefs.item_box_ofsy]]
                )
            elif direction == 'bottom':
                # add icon box (右下から)
                icon_box_poly_coords = (
                    [[u2 + trapezoid, v1 - prefs.item_box_ofsy]] +
                    self.round_corner([u2, v2], 'top_right') +
                    self.round_corner([u1, v2], 'top_left') +
                    [[u1 - trapezoid, v1 - prefs.item_box_ofsy]]
                )
            elif direction == 'right':
                icon_box_poly_coords = []
            else:
                icon_box_poly_coords = []
            line_coords_icon = []
            icon_size = self.icon_size

        if text_box:
            x1, y1, x2, y2 = text_box
            bottom_left = self.round_corner([x1, y1], 'bottom_left')
            bottm_right = self.round_corner([x2, y1], 'bottom_right')
            top_right = self.round_corner([x2, y2], 'top_right')
            top_left = self.round_corner([x1, y2], 'top_left')

            if menu.icon_size > 0:
                text_box_poly_coords = line_coords = (
                        top_left + bottom_left + bottm_right + top_right)
            else:
                if direction == 'top':
                    # text box (右下から半時計回り)
                    text_box_poly_coords = (
                        bottm_right + top_right + top_left + bottom_left)
                    line_coords = text_box_poly_coords + icon_box_poly_coords
                elif direction == 'bottom':
                    # text box (左上から)
                    text_box_poly_coords = (
                        top_left + bottom_left + bottm_right + top_right)
                    line_coords = text_box_poly_coords + icon_box_poly_coords
                elif direction == 'right':
                    line_coords = (
                        top_left + bottom_left + bottm_right + top_right)
                    text_box_poly_coords = line_coords
                else:
                    line_coords = (
                        top_left + bottom_left + bottm_right + top_right)
                    text_box_poly_coords = line_coords
        else:
            text_box_poly_coords = line_coords = []

        if colors.menu_show_shaded:
            _, text_box_rect_top = self.calc_item_rect('top', 'DUMMY')
            _, text_box_rect_down = self.calc_item_rect('down', 'DUMMY')
            menu_ymax = text_box_rect_top[3]
            menu_ymin = text_box_rect_down[1]
            col_menu_inner_top, col_menu_inner_bottom = vagl.shade_color(
                colors.menu_inner, colors.menu_shadetop, colors.menu_shadedown)

        def get_menu_inner_color(y):
            y = max(menu_ymin, min(y, menu_ymax))
            f = (y - menu_ymin) / (menu_ymax - menu_ymin)
            return vagl.blend_color(col_menu_inner_top,
                                    col_menu_inner_bottom, f)

        # Draw Back
        # menu back color
        bgl.glColor4f(*colors.menu_inner)
        if colors.menu_inner[3] > 0.0:
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for v in text_box_poly_coords:
                if colors.menu_show_shaded:
                    col = get_menu_inner_color(v[1])
                    bgl.glColor4f(*col)
                bgl.glVertex2f(*v)
            bgl.glEnd()
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for v in icon_box_poly_coords:
                if colors.menu_show_shaded:
                    col = get_menu_inner_color(v[1])
                    bgl.glColor4f(*col)
                bgl.glVertex2f(*v)
            bgl.glEnd()

        # item inner
        bgl.glColor4f(*col_box_top)
        if col_box_top[3] > 0.0 or col_box_bottom[3] > 0.0:
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for v in text_box_poly_coords:
                if colors.item_show_shaded:
                    f = (v[1] - text_box[1]) / widget_unit
                    col = vagl.blend_color(col_box_top, col_box_bottom, f)
                    bgl.glColor4f(*col)
                bgl.glVertex2f(*v)
            bgl.glEnd()

            # 上と下のIcon部分
            if direction == 'top':
                bgl.glColor4f(*col_box_bottom)
            else:
                bgl.glColor4f(*col_box_top)
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for v in icon_box_poly_coords:
                bgl.glVertex2f(*v)
            bgl.glEnd()

        # Draw Icon
        icon_x = icon_center[0] - icon_size / 2
        icon_y = icon_center[1] - icon_size / 2
        self.draw_icon(item.icon, icon_x, icon_y, active, enabled)

        # Draw Outline
        bgl.glColor4f(*colors.item_outline)
        bgl.glBegin(bgl.GL_LINE_LOOP)
        for v in line_coords:
            bgl.glVertex2f(*v)
        bgl.glEnd()
        bgl.glBegin(bgl.GL_LINE_LOOP)
        for v in line_coords_icon:
            bgl.glVertex2f(*v)
        bgl.glEnd()

        # Draw Text
        if text_box:
            if not enabled:
                col = vagl.thin_color(colors.item_text, 0.5)
            elif active:
                col = list(colors.item_text_sel)
            else:
                col = list(colors.item_text)
            bgl.glColor4f(*col)
            if direction in ('top', 'bottom'):
                x = text_box[0] + widget_unit * 0.5
            else:
                if direction == 'right':
                    if menu.icon_size > 0:
                        x = text_box[0] + widget_unit * 0.5
                    else:
                        x = text_box[0] + widget_unit + self.ICON_TEXT_MARGIN
                else:
                    x = text_box[0] + widget_unit * 0.5

            th = blf.dimensions(prefs.font_id, CALC_TEXT_HEIGHT)[1]
            y = text_box[1] + widget_unit / 2 - th / 2
            blf.position(prefs.font_id, x, y, 0)
            vagl.blf_draw(prefs.font_id, item.label)

        # Menu Marker
        if item.menu:
            b = math.sqrt(2)
            f = b * math.sin(math.pi / 4) / 2
            box = text_box or icon_box
            if direction == 'left':
                co = [box[0] + 2, box[1] + 2]
                v = [-f, -f]
            else:
                co = [box[2] - 2, box[1] + 2]
                v = [f , -f]
            if (menu.active_item == item and item.enabled and
                    menu.is_valid_click):
                l = 14
            else:
                l = 10
            v = [v[0] * l, v[1] * l]
            bgl.glColor4f(*colors.menu_inner)
            vagl.draw_triangle_relative(co, l * b, v, poly=True)
            bgl.glColor4f(*colors.menu_marker)
            vagl.draw_triangle_relative(co, l * b, v, poly=True)
            bgl.glColor4f(*colors.menu_marker_outline)
            vagl.draw_triangle_relative(co, l * b, v)

        # Shortcut
        ls = ('ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN',
              'EIGHT', 'NINE')
        if item.shortcut in ls:
            shortcut = str(ls.index(item.shortcut))
        else:
            shortcut = item.shortcut
        if shortcut and shortcut != 'NONE':
            if direction == 'left':
                tw = blf.dimensions(prefs.font_id, shortcut)[0]
                x = text_box[0] - widget_unit / 2 - tw
            else:
                x = text_box[2] + widget_unit / 2
            y = text_box[1] + widget_unit / 2 - th / 2
            blf.position(prefs.font_id, x, y, 0)
            if 0:
                bgl.glColor4f(0.0, 0.0, 0.0, 1.0 / (8 / 60))
                blf.blur(prefs.font_id, 5)
                vagl.blf_draw(prefs.font_id, shortcut)
                blf.blur(prefs.font_id, 0)
            bgl.glColor4f(*colors.text)
            vagl.blf_draw(prefs.font_id, shortcut)

    def draw_items(self):
        prefs = self.prefs
        menu = self.menu
        # アクティブな物を最後に描画
        idx_items = list(enumerate(menu.current_items))
        for i, item in idx_items:
            if i == menu.active_index:
                idx_items = idx_items[:i] + idx_items[i + 1:] + [idx_items[i]]
                break

        if len(menu.current_items) == 0:
            pie_angle = math.pi * 2
        else:
            pie_angle = math.pi * 2 / len(menu.current_items)
        if prefs.tacho:
            angle = math.pi * 1.5
        else:
            angle = math.pi * 0.5

        icon_box_size = self.icon_box_size
        for i, item in idx_items:
            if not item:
                continue
            ang = angle - pie_angle * i
            if ang < 0.0:
                ang += math.pi * 2

            v = Vector(((menu.radius + icon_box_size / 2) * math.cos(ang),
                        (menu.radius + icon_box_size / 2) * math.sin(ang)))
            icon_center = menu.co + v

            active = i == menu.active_index or item == menu.active_item
            if not menu.is_valid_click:
                active = False
            enabled = item.enabled
            self.draw_item(item, i, icon_center, active, enabled)

    def draw_tooltip(self, context):
        if not self.op.show_tooltip:
            return
        prefs = self.prefs
        colors = prefs.colors
        menu = self.menu
        if not menu.active_item or not menu.is_valid_click:
            return
        for item in menu.current_items:
            if item == menu.active_item:
                break
        else:
            return
        rect = item.text_box_rect or item.icon_box_rect

        if item.description:
            g = self.gen_text_position(item.description)
        else:
            g = self.gen_text_position(None)
        _y, w, h = g.send(None)
        execute_string = item.get_execute_string()
        if execute_string:
            ls = execute_string.split('\n')
            if len(ls) > 3:
                execute_string = '\n'.join(ls[:3] + ['...'])
            execute_string = oputils.format_execute_string(
                execute_string, True)
            exec_lines = execute_string.split('\n')
            execute_string = '\n'.join(['Python: ' + exec_lines[0]] +
                                  [' ' * 8 + s for s in exec_lines[1:]])
            _y, w, h = g.send((execute_string, True))
        else:
            execute_string = ''
        if item.menu:
            if isinstance(item.menu, str):
                menu_string = item.menu
            else:
                menu_string = item.menu.idname
            menu_string = 'Menu: ' + menu_string
            _y, w, h = g.send((menu_string, True))
        else:
            menu_string = ''

        g.close()
        minx = (rect[0] + rect[2]) / 2 - w / 2
        miny = rect[1] - self.widget_unit * 0.2 - h
        win = context.window
        if minx + w > win.width:
            minx = win.width - w
        if minx < 0:
            minx = 0
        if miny < 0:
            miny = 0
        if miny + h > win.height:
            miny = win.height - h
        self.draw_box(minx, miny, w, h,
                      col_inner=colors.tooltip_inner,
                      col_outline=colors.tooltip_outline,
                      inner_show_shaded=colors.tooltip_show_shaded,
                      inner_shadetop=colors.tooltip_shadetop,
                      inner_shadedown=colors.tooltip_shadedown)

        g = self.gen_text_position(None)
        g.send(None)
        maxy = miny + h
        if item.description:
            bgl.glColor4f(*colors.tooltip_text)
            for line in item.description.split('\n'):
                ty, w, h = g.send(line)
                blf.position(prefs.font_id,
                             minx + self.widget_unit / 2, maxy + ty, 0)
                blf.draw(prefs.font_id, line)

        if execute_string or menu_string:
            # 青みがかった色にする
            col_exec = list(colors.tooltip_text)
            if col_exec[0] > 0.2 or col_exec[1] > 0.2:
                col_exec[0] = max(0.0, col_exec[0] - 0.2)
                col_exec[1] = max(0.0, col_exec[1] - 0.2)
            else:
                col_exec[2] = min(1.0, col_exec[2] + 0.2)
            bgl.glColor4f(*col_exec)

            lines = [s for s in execute_string.split('\n') if s]
            if menu_string:
                lines.append(menu_string)
            for line in lines:
                ty, w, h = g.send((line, True))
                blf.position(prefs.font_id_mono,
                             minx + self.widget_unit / 2, maxy + ty, 0)
                blf.draw(prefs.font_id_mono, line)
        g.close()

    def draw(self, context):
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glLineWidth(1.0)
        bgl.glShadeModel(bgl.GL_SMOOTH)

        self.set_font_size(context)

        menu = self.menu
        menu.rect = [None] * 4
        for i, item in enumerate(menu.current_items):
            if item:
                item.rect = [None] * 4
                item.icon_box_rect, item.text_box_rect = self.calc_item_rect(
                    i, item.label)

        self.draw_active_item_background()
        self.draw_guid_lines()
        self.draw_titles()
        self.draw_items()
        self.draw_arrow()
        self.draw_tooltip(context)


dm = DrawingManager(None, None)


def gen_texture():
    textures = bgl.Buffer(bgl.GL_INT, 1)
    bgl.glGenTextures(1, textures)
    tex = textures[0]
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, tex)
    bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER,
                        bgl.GL_LINEAR)
    bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER,
                        bgl.GL_LINEAR)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)
    return tex


def gen_screenshot_texture(x, y, w, h, update=False):
    """window全体のスクショを撮る"""
    with vagl.GLSettings.push_attrib():
        bgl.glEnable(bgl.GL_SCISSOR_TEST)
        bgl.glScissor(x, y, w, h)
        tex = gen_texture()
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, tex)
        bgl.glCopyTexImage2D(bgl.GL_TEXTURE_2D, 0, bgl.GL_RGBA, 0, 0, w, h, 0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)
    return tex


def draw_texture(x, y, w, h, texture, mode=None):
    mode_bak = bgl.Buffer(bgl.GL_INT, 1)
    bgl.glGetIntegerv(bgl.GL_DRAW_BUFFER, mode_bak)
    if mode is not None:
        bgl.glDrawBuffer(mode)

    bgl.glEnable(bgl.GL_TEXTURE_2D)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture)

    bgl.glColor4d(1.0, 1.0, 1.0, 1.0)
    bgl.glBegin(bgl.GL_TRIANGLE_FAN)
    bgl.glTexCoord2d(0.0, 0.0)
    bgl.glVertex2i(x, y)
    bgl.glTexCoord2d(1.0, 0.0)
    bgl.glVertex2i(x + w, y)
    bgl.glTexCoord2d(1.0, 1.0)
    bgl.glVertex2i(x + w, y + h)
    bgl.glTexCoord2d(0.0, 1.0)
    bgl.glVertex2i(x, y + h)
    bgl.glEnd()

    bgl.glDisable(bgl.GL_TEXTURE_2D)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)

    if mode is not None:
        bgl.glDrawBuffer(mode_bak[0])


def is_overlap_region(context, area, region):
    U = context.user_preferences
    if U.system.use_region_overlap:
        if U.system.window_draw_method in {'AUTOMATIC', 'TRIPLE_BUFFER'}:
            if 'WM_is_draw_triple(context.window)':
                if area.type in {'VIEW_3D', 'SEQUENCE_EDITOR'}:
                    if region.type in {'TOOLS', 'UI', 'TOOL_PROPS'}:
                        return True
                elif area.type == 'IMAGE_EDITOR':
                    if region.type in {'TOOLS', 'UI', 'TOOL_PROPS', 'PREVIEW'}:
                        return True
    return False


def has_overlap_regions(context):
    for area in context.screen.areas:
        for region in area.regions:
            if region.id != 0:
                if is_overlap_region(context, area, region):
                    return True
    return False


###############################################################################
# Operator
###############################################################################
class WM_OT_pie_menu_exec(bpy.types.Operator):
    bl_idname = 'wm.pie_menu_exec'
    bl_label = 'Pie Menu Exec'
    bl_description = ''
    bl_options = {'INTERNAL'}

    item = result = None

    def execute(self, context):
        cls = self.__class__
        item = cls.item
        try:
            cls.result = item.call_method('execute', context)
        except:
            traceback.print_exc()
            cls.result = None
        return {'FINISHED'}


class WM_OT_pie_menu_exec_register(bpy.types.Operator):
    bl_idname = 'wm.pie_menu_exec_register'
    bl_label = 'Pie Menu Exec'
    bl_description = ''
    bl_options = {'REGISTER', 'INTERNAL'}

    item = result = None

    def execute(self, context):
        cls = self.__class__
        item = cls.item
        try:
            cls.result = item.call_method('execute', context)
            # 履歴のメッセージを任意の物にする為、bl_optionsには'UNDO'を入れずに
            # ここでundo_push()を行う。
            bpy.ops.ed.undo_push(message=item.label)
        except:
            traceback.print_exc()
            cls.result = None
        return {'FINISHED'}


class WM_OT_pie_menu(bpy.types.Operator):
    bl_idname = 'wm.pie_menu'
    bl_label = 'Pie Menu'
    bl_description = ''

    bl_options = {'INTERNAL'}

    idname = bpy.props.StringProperty(name='Menu', description='Menu idname')
    """:type: str"""

    space_types = {
        'CLIP_EDITOR': bpy.types.SpaceClipEditor,
        'CONSOLE': bpy.types.SpaceConsole,
        'DOPESHEET_EDITOR': bpy.types.SpaceDopeSheetEditor,
        'EMPTY': None,
        'FILE_BROWSER': bpy.types.SpaceFileBrowser,
        'GRAPH_EDITOR': bpy.types.SpaceGraphEditor,
        'IMAGE_EDITOR': bpy.types.SpaceImageEditor,
        'INFO': bpy.types.SpaceInfo,
        'LOGIC_EDITOR': bpy.types.SpaceLogicEditor,
        'NLA_EDITOR': bpy.types.SpaceNLA,
        'NODE_EDITOR': bpy.types.SpaceNodeEditor,
        'OUTLINER': bpy.types.SpaceOutliner,
        'PROPERTIES': bpy.types.SpaceProperties,
        'SEQUENCE_EDITOR': bpy.types.SpaceSequenceEditor,
        'TEXT_EDITOR': bpy.types.SpaceTextEditor,
        'TIMELINE': bpy.types.SpaceTimeline,
        'USER_PREFERENCES': bpy.types.SpaceUserPreferences,
        'VIEW_3D': bpy.types.SpaceView3D,
    }
    # draw_handlers = {}

    event = None  # get_event()用

    def __init__(self):
        context = bpy.context

        self.menu = None
        """:type: Menu"""

        self.timer = None
        """:type: bpy.types.Timer"""

        self.dpi = context.user_preferences.system.dpi

        self.mco = None
        """:type: mathutils.Vector"""
        self.mco_left = self.mco_middle = self.mco_right = None
        self.mco_left_prev = self.mco_middle_prev = self.mco_right_prev = None

        self.shift = False
        self.ctrl = False

        self.running_modal = False

        self.event_type = ''  # 起動時のevent.type
        self.last_action_time = time.perf_counter()
        self.show_tooltip = False
        self.mco_tooltip = None
        self.moving = False

        # {event.type: {'mco': Vector2D, 'shift': bool, ...}, ...}
        self.event_history = OrderedDict()

        # list of class
        self.menu_history = []

        self.texture = None
        self.handles = []
        self.region_tex = None
        self.region_pie = None

    # Draw Callback -----------------------------------------------------------
    def area_from_region(self, region):
        for area in region.id_data.areas:
            for r in area.regions:
                if r == region:
                    return area

    def draw_callback(self, context, region_tex=None, region_pie=None):
        win = context.window
        area = context.area
        region = context.region

        # regions = []
        # for sa in context.screen.areas:
        #     for ar in sa.regions:
        #         regions.append(ar)
        # print(regions.index(region), area.type, region.type)

        if not is_overlap_region(context, area, region):
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.texture)
            bgl.glCopyTexSubImage2D(
                bgl.GL_TEXTURE_2D, 0, region.x, region.y,
                region.x, region.y, region.width, region.height)
            # bgl.glFlush()
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)

        if region == region_tex:
            with vagl.GLSettings.push_attrib():
                with window_space(context.window):
                    bgl.glDisable(bgl.GL_SCISSOR_TEST)
                    draw_texture(0, 0, win.width, win.height,
                                 self.texture)

        area_pie = self.area_from_region(region_pie)
        regions_pie = list(area_pie.regions)
        if region == region_pie:
            with vagl.GLSettings.push_attrib():
                with window_space(context.window):
                    bgl.glDisable(bgl.GL_SCISSOR_TEST)
                    t = time.time()
                    dm.draw(context)
                    # print(time.time() - t)
        elif region in regions_pie:
            if regions_pie.index(region) > regions_pie.index(region_pie):
                with vagl.GLSettings.push_attrib():
                    with window_space(context.window):
                        dm.draw(context)

    def gen_texture(self, context):
        win = context.window
        w, h = win.width, win.height
        self.texture = gen_screenshot_texture(0, 0, w, h)

    def delete_textures(self):
        buf = bgl.Buffer(bgl.GL_INT, 1, [self.texture])
        bgl.glDeleteTextures(1, buf)

    def draw_handler_add(self, context):
        area_tex = region_tex = None
        area_pie = region_pie = None

        has_overlap = has_overlap_regions(context)
        for sa in context.screen.areas:
            for ar in sa.regions:
                if ar.id != 0:
                    if has_overlap:
                        if is_overlap_region(context, sa, ar):
                            area_pie = sa
                            region_pie = ar
                    else:
                        area_pie = sa
                        region_pie = ar
                    if not area_tex:
                        area_tex = sa
                        region_tex = ar

        if region_pie.type == 'WINDOW':
            for ar in area_pie.regions:
                if ar.id != 0:
                    if ar.type != 'WINDOW':
                        region_pie = ar

        self.draw_handler_remove()

        added = set()
        for sa in context.screen.areas:
            for ar in sa.regions:
                if ar.id != 0:
                    key = (sa.type, ar.type)
                    if key in added:
                        continue
                    handle = sa.spaces.active.draw_handler_add(
                        self.draw_callback,
                        (context, region_tex, region_pie),
                        ar.type, 'POST_PIXEL')

                    self.handles.append((handle, sa.type, ar.type))
                    added.add(key)

        self.region_tex = region_tex
        self.region_pie = region_pie

        # cython test
        #
        # addr = region.as_pointer()
        # ar = cast(c_void_p(addr), POINTER(ARegion)).contents
        # art = ar.type
        # lb = art.contents.drawcalls
        # handle = area.spaces.active.draw_handler_add(
        #     self.draw_callback_tex, (context,), region.type,
        #     'POST_PIXEL')
        # func = ctypes.pythonapi.PyCapsule_GetPointer
        # func.restype = c_void_p
        # p = func(ctypes.py_object(handle), b'RNA_HANDLE')
        # print('handle', p)
        # print('listbase', lb.first, lb.last)

    def draw_handler_remove(self):
        for handle, area_type, region_type in self.handles:
            space = self.space_types[area_type]
            space.draw_handler_remove(handle, region_type)
        self.handles.clear()

    # Event -------------------------------------------------------------------
    def event_history_add(self, event):
        """modal最後で実行
        :type event: bpy.types.Event
        """
        mco = Vector((event.mouse_x, event.mouse_y))
        values = {key: getattr(event, key)
                  for key in ('shift', 'ctrl', 'alt', 'oskey')}
        values['mco'] = mco
        if event.value == 'PRESS':
            if event.type in self.event_history:
                self.event_history.move_to_end(event.type)
            self.event_history[event.type] = values
        elif event.value == 'RELEASE':
            if event.type in self.event_history:
                del self.event_history[event.type]

    def modifiers_update(self, event):
        shift_bak = self.shift
        ctrl_bak = self.ctrl
        if event.type in ('LEFT_SHIFT', 'RIGHT_SHIFT'):
            if event.value == 'PRESS':
                self.shift = True
            elif event.value == 'RELEASE':
                self.shift = False
            # else:
            #     self.shift = event.shift
        elif event.type in ('LEFT_CTRL', 'RIGHT_CTRL'):
            if event.value == 'PRESS':
                self.ctrl = True
            elif event.value == 'RELEASE':
                self.ctrl = False
            # else:
            #     self.ctrl = event.ctrl
        return self.shift != shift_bak or self.ctrl != ctrl_bak

    def mco_left_middle_right_update(self, event):
        """mco_left, mco_middle, mco_right属性を更新
        """
        mco = Vector((event.mouse_x, event.mouse_y))

        self.mco_left_prev = self.mco_left
        self.mco_middle_prev = self.mco_middle
        self.mco_right_prev = self.mco_right

        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self.mco_left = mco.copy()
            elif event.value == 'RELEASE':
                self.mco_left = None
        elif event.type == 'MIDDLEMOUSE':
            if event.value == 'PRESS':
                self.mco_middle = mco.copy()
            elif event.value == 'RELEASE':
                self.mco_middle = None
        elif event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                self.mco_right = mco.copy()
            elif event.value == 'RELEASE':
                self.mco_right = None

    def set_menu(self, context, key, co=None):
        if co is None:
            co = self.menu.co

        # self.menu = menu = get_menu(context, idname_or_class)
        menu_class = Menu.get_menu(key)
        """:type: T"""

        if menu_class is None:
            return None

        if not menu_class.call_method('poll', context):
            return False

        menu = menu_class(context)
        """:type: Menu"""

        self.menu = menu
        # 更新
        menu.co = co.copy()
        menu.update_current_items(context, self.shift, self.ctrl)
        # menu.correct_icon_size()
        menu.correct_radius()
        menu.update_active(self.mco, self.mco_left)
        return True

    def regionruler_disable(self, context):
        try:
            import ctools.regionruler as regionruler
            p = context.user_preferences.addons[
                'ctools'].preferences.get_instance("regionruler")
            self.draw_cross_cursor = p.draw_cross_cursor
            simple_measure = regionruler.data.simple_measure
            regionruler.data.simple_measure = False
            regionruler.data.measure_points.clear()

            if DISABLE_CROSS_CURSOR and (self.draw_cross_cursor or
                                         simple_measure):
                if not context.screen.is_animation_playing:
                    p.draw_cross_cursor = False
                    if context.area.type in ('VIEW_3D', 'IMAGE_EDITOR'):
                        if context.region.type == 'WINDOW':
                            context.region.tag_redraw()
        except:
            # traceback.print_exc()
            pass

    def regionruler_restore(self, context):
        try:
            p = context.user_preferences.addons[
                'ctools'].preferences.get_instance("regionruler")
            p.draw_cross_cursor = self.draw_cross_cursor
        except:
            pass

    @classmethod
    def poll(cls, context):
        return True

    def modal(self, context, event):
        """
        LEFTMOUSEはRELEASE、それ以外はPRESSで確定する。
        """
        # if event.type != 'TIMER':
        #     print(event.type, event.value)
        if (event.type == 'INBETWEEN_MOUSEMOVE' or
                event.type == 'MOUSEMOVE' and
                event.mouse_x == event.mouse_prev_x and
                event.mouse_y == event.mouse_prev_y):
            return {'RUNNING_MODAL'}

        self.__class__.event = event  # get_event()用
        dm.update(context, self)

        prefs = get_addon_preferences()
        wm = context.window_manager
        self.mco = mco = Vector((event.mouse_x, event.mouse_y))
        current_time = time.perf_counter()

        if self.running_modal:
            return {'FINISHED', 'PASS_THROUGH'}

        menu = self.menu

        # マウス関連
        self.mco_left_middle_right_update(event)

        # 修飾キー属性更新
        do_update_current_items = self.modifiers_update(event)

        item_index = menu.active_index

        # メニューの各属性を更新・再計算

        if do_update_current_items:
            menu.update_current_items(context, self.shift, self.ctrl)
        menu.update_active(self.mco, self.mco_left_prev)

        # tooltip描画の判定
        if event.type.startswith('TIMER'):
            pass
        elif event.type == 'MOUSEMOVE':
            if (self.show_tooltip and
                    item_index == menu.active_index):
                pass
            else:
                self.last_action_time = current_time
        elif event.value == 'PRESS' and event.type in self.event_history:
            # キーリピートは無視する
            pass
        else:
            self.last_action_time = current_time

        if menu.active_index == -1:
            show_tooltip = False
        else:
            show_tooltip = (current_time - self.last_action_time >=
                            prefs.tooltip_time)
        if show_tooltip:
            if not self.show_tooltip:
                self.mco_tooltip = mco.copy()
            self.show_tooltip = True
        else:
            self.show_tooltip = False

        # Confirm -------------------------------------------------------------
        confirm = False
        click = False
        active_item = None
        item_shortcuts = {item.shortcut if item else ''
                          for item in menu.current_items}
        if event.type == self.event_type and event.value == 'RELEASE':
            if menu.active_index == -1:
                if menu.release_confirm == 2:
                    confirm = True
            elif menu.release_confirm >= 1:
                confirm = True
            self.event_type = ''
        elif (event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and
                'LEFTMOUSE' in self.event_history):
            if menu.is_valid_click:
                confirm = True
                click = True
        if not confirm:
            for item in menu.current_items:
                if item and item.shortcut:
                    if event.type == item.shortcut and event.value == 'PRESS':
                        confirm = True
                        active_item = item
                        self.event_type = event.type
                        self.set_lock_pie_event(context, event.type)
                        break
            # TODO: 起動時のショートカットにも反応してしまう
            # else:
            #     if event.type not in item_shortcuts:
            #         if event.type in ('SPACE', 'RET', 'NUMPAD_ENTER'):
            #             if event.value == 'PRESS':
            #                 confirm = True
        if confirm and not active_item:
            active_item = menu.active_item

        if confirm and active_item:
            retval = None

            if active_item.enabled:
                menu.set_last_item_index(menu.current_items.index(active_item))
                modal_handlers_pre = self.get_modal_handlers(context)

                if active_item.undo_push:
                    WM_OT_pie_menu_exec_register.item = active_item
                    bpy.ops.wm.pie_menu_exec_register(True)
                    result = WM_OT_pie_menu_exec_register.result
                else:
                    WM_OT_pie_menu_exec.item = active_item
                    bpy.ops.wm.pie_menu_exec(True)
                    result = WM_OT_pie_menu_exec.result

                modal_handlers_post = self.get_modal_handlers(context)
                running_modal = (addressof(modal_handlers_pre[0][0]) !=
                                 addressof(modal_handlers_post[0][0]))

                if active_item.menu or isinstance(result, str):
                    if active_item.menu:
                        sub_menu = active_item.menu
                    else:
                        sub_menu = result

                    co = None if prefs.lock_menu_location else mco
                    menu_test = self.set_menu(context, sub_menu, co)
                    if menu_test is None:
                        retval = {'FINISHED'}
                    elif not menu_test:  # poll()の結果がFalse
                        pass
                    else:
                        self.menu_history.append(menu)
                # elif self.test_grab_cursor(context):
                #     self.running_modal = True
                #     retval = {'RUNNING_MODAL'}
                elif running_modal:
                    self.running_modal = True
                    retval = {'RUNNING_MODAL'}
                else:
                    retval = {'FINISHED'}
            else:
                if not click:
                    menu.set_last_item_index(-1)
                    retval = {'CANCELLED'}

            if retval is not None:
                self.draw_handler_remove()
                self.delete_textures()
                wm.event_timer_remove(self.timer)
                self.regionruler_restore(context)
                self.redraw_all(context)
                return retval
            else:
                # areaやregionに変更が加えられた可能性があるので更新する
                self.draw_handler_add(context)

        # Cancel --------------------------------------------------------------
        cancel = False
        if event.type == 'RIGHTMOUSE':
            cancel = True
        elif event.type == 'ESC':
            if event.type not in item_shortcuts:
                cancel = True

        if cancel:
            self.draw_handler_remove()
            self.delete_textures()
            wm.event_timer_remove(self.timer)
            self.regionruler_restore(context)
            self.redraw_all(context)
            return {'CANCELLED'}

        # 移動
        if self.mco_middle and self.shift:
            menu.co = mco.copy()
            menu.update_active(self.mco, self.mco_left)
            menu.is_valid_click = False

        # 次/前のメニュー
        elif event.type in ('WHEELUPMOUSE', 'WHEELDOWNMOUSE'):
            if event.type == 'WHEELUPMOUSE':
                if menu.prev:
                    self.set_menu(context, menu.prev)
            elif event.type == 'WHEELDOWNMOUSE':
                if menu.next:
                    self.set_menu(context, menu.next)

        # 親メニューへ
        elif (event.type == 'MIDDLEMOUSE' and event.value == 'PRESS' and
                  not self.shift):
            if self.menu_history:
                parent = self.menu_history.pop(-1)
                # if prefs.lock_menu_location:
                #     self.set_menu(context, parent)
                # else:
                #     self.set_menu(context, parent, mco)
                self.set_menu(context, parent)

        # イベント履歴
        self.event_history_add(event)

        # 無駄な再描画をしない
        if 0:  # ScreenCastKeysで描画されない問題が起こる
            if event.type == 'TIMER':
                t = current_time - self.last_action_time
                if t < prefs.tooltip_time or t > prefs.tooltip_time + 0.5:
                    return {'RUNNING_MODAL'}

        dm.update(context, self)

        self.redraw(context)

        return {'RUNNING_MODAL'}

    @classmethod
    def redraw_all(cls, context):
        for area in context.screen.areas:
            area.tag_redraw()

    def redraw(self, context, init=False):
        self.region_tex.tag_redraw()
        self.region_pie.tag_redraw()
        if init:
            for area in context.screen.areas:
                for region in area.regions:
                    if is_overlap_region(context, area, region):
                        area.tag_redraw()
                        continue

    # 未使用
    """
    def get_lock_pie_event(self, context):
        addr = context.window.as_pointer()
        win = cast(c_void_p(addr), POINTER(wmWindow)).contents
        return win.lock_pie_event
    """

    def set_lock_pie_event(self, context, event_type):
        items = bpy.types.Event.bl_rna.properties['type'].enum_items
        # get(name)はEnumPropertyItemを、find(name)はインデックスを得る
        value = items.get(event_type).value
        win = wmWindow.cast(context.window)
        win.lock_pie_event = value

    # 未使用
    """
    def test_grab_cursor(self, context):
        addr = context.window.as_pointer()
        win = cast(c_void_p(addr), POINTER(wmWindow)).contents
        return win.grabcursor != 0
    """

    def get_modal_handlers(self, context):
        window = context.window
        return wmWindow.modal_handlers(window)

    def invoke(self, context, event):
        self.__class__.event = event  # get_event()用
        wm = context.window_manager
        if not self.idname or not Menu.get_menu(self.idname):
            self.report({'ERROR'}, "menu '{}' not found".format(self.idname))
            return {'CANCELLED'}

        # TODO: TABでのモード切り替えがCLICKなので暫定的な対処をした
        # menu = ctx.menu
        # shortcut = menu.shortcut
        # keymaps = wm.keyconfigs.active.keymaps
        # if shortcut['keymap']:
        #     km = keymaps.get(shortcut['keymap'])
        #     attrs = ['type', 'any', 'shift', 'ctrl', 'alt', 'oskey',
        #              'key_modifier']
        #     for kmi in km.keymap_items:
        #         if shortcut['value'] == 'PRESS':
        #             for attr in attrs:
        #                 if shortcut[attr] != getattr(kmi, attr):
        #                     break
        #             else:
        #                 if kmi.value == 'CLICK':
        #                     kmi.active = False

        self.event_type = event.type
        # ctypes
        if event.type in {'LEFTMOUSE'}:
            self.set_lock_pie_event(context, 'NONE')
        else:
            self.set_lock_pie_event(context, event.type)
        # win.last_pie_event = items.get('NONE').value

        dm.update(context, self)

        self.mco = Vector((event.mouse_x, event.mouse_y))
        self.mco_left_middle_right_update(event)
        self.modifiers_update(event)
        self.event_history_add(event)

        self.menu_history.clear()

        menu_test = self.set_menu(context, self.idname, self.mco)
        if menu_test is None :
            self.report({'ERROR'}, "menu '{}' not found".format(self.idname))
            return {'CANCELLED'}

        elif not menu_test:  # poll()でFalseを返す
            return {'CANCELLED', 'PASS_THROUGH'}

        wm.modal_handler_add(self)

        self.gen_texture(context)
        self.draw_handler_add(context)

        self.timer = wm.event_timer_add(0.1, context.window)

        self.regionruler_disable(context)

        context.area.tag_redraw()
        self.redraw(context, True)

        return {'RUNNING_MODAL'}


###############################################################################
# Register / Unregister
###############################################################################
user_modules = []


def register_user_moudle(mod):
    user_modules.append(mod)
    menus = mod.pie_menus
    for menu in menus:
        if hasattr(menu, 'idname'):
            Menu.register_menu(menu)


def import_user_pie_menus():
    path = bpy.utils.user_resource('CONFIG')
    sys.path.insert(0, path)
    try:
        piemenus = importlib.import_module(config_dir_name)
    except ImportError:
        traceback.print_exc()
        sys.path.pop(0)
        return
    for f in os.listdir(os.path.join(path, config_dir_name)):
        if f.startswith('_'):
            continue
        try:
            mod = importlib.import_module(
                      config_dir_name + '.' + os.path.splitext(f)[0])
        except:
            traceback.print_exc()
            continue
        try:  # F8でのリロード後にSnapメニューで問題が起こったので
            importlib.reload(mod)
        except:
            traceback.print_exc()
            continue
        register_user_moudle(mod)
    sys.path.pop(0)


classes = [
    WM_OT_pie_menu,
    WM_OT_pie_menu_exec,
    WM_OT_pie_menu_exec_register,
]


@preferences.PieMenuPreferences.register_addon
def register():
    preferences.register()
    drawicon.register()
    for cls in classes:
        bpy.utils.register_class(cls)

    import_user_pie_menus()

    for cls in Menu.menus.values():
        cls.register_keymap_items()

    # km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
    #
    # kmi = km.keymap_items.new('wm.pie_menu', 'SEMI_COLON', 'PRESS',
    #                           head=True)
    # kmi.properties.idname = 'test_menu'
    # pie_keymap_items.append((km, kmi))
    #
    # kmi = km.keymap_items.new('wm.pie_menu', 'SEMI_COLON', 'PRESS',
    #                           shift=True, head=True)
    # kmi.properties.idname = 'kill'
    # pie_keymap_items.append((km, kmi))


@preferences.PieMenuPreferences.unregister_addon
def unregister():
    preferences.unregister()
    drawicon.unregister()

    user_modules.clear()

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
