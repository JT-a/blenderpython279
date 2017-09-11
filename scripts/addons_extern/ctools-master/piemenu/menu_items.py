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


from collections import OrderedDict
import enum
# import importlib
import inspect
import os
import math
import re

import bpy
import blf
from bpy import props

# from ..utils import addongroup
from ..utils import vaprops
from ..utils import vawm

# from . import stubs
from . import oputils
from . import operators as ops
from . import custom_icons
from .stubs import cross2d

try:
    import pie_menu
except:
    pie_menu = None


translate_iface = bpy.app.translations.pgettext_iface


IGNORE_EMPTY_SPACE = True


class EnumDrawType(enum.IntEnum):
    SIMPLE = 0
    BOX = 1
    CIRCLE = 2

    SIMPLE_BOX = 3
    SIMPLE_CIRCLE = 4


class EnumQuickAction(enum.IntEnum):
    NONE = -1
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7
    LAST = 8


class EnumHighlight(enum.IntEnum):
    NONE = -1
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7
    LAST = 8


all_icon_identifiers = {
    item.identifier: item.value for item in
    bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].enum_items}


def indented_layout(layout):
    sp = layout.split(0.025)
    sp.column()
    return sp.column()


def draw_separator(layout):
    row = layout.row()
    # row.active = False  # To make the color thinner
    row.label("…" * 200)


def draw_property(layout, obj, attr, text=None, unset=False,
                  paste=False, context_attr="", active=None):
    p = obj.bl_rna.properties[attr]
    if p.type in {'BOOLEAN', 'FLOAT', 'INT'} and not p.is_array:
        split = False
    else:
        split = True
    # is_property_set() is always True if property has get function
    is_property_set = attr in obj

    row = layout.row()
    if active is not None:
        row.active = active
    else:
        if unset and not is_property_set:
            row.active = False
    if split and text != "":
        sp = row.split(1 / 3)  # 基本的にこの比率
        row1 = sp.row()
        text_ = p.name if text is None else text
        row1.label(translate_iface(text_) + ":")
        row2 = sp.row()
        row2_sub = row2.row(align=True)
        row2_sub.prop(obj, attr, text="")
    else:
        row2 = row.row()
        row2_sub = row2.row(align=True)
        kwargs = {} if text is None else {"text": text}
        row2_sub.prop(obj, attr, **kwargs)
    if paste:
        op = row2_sub.operator(ops.WM_OT_pie_menu_text_paste.bl_idname,
                               text="", icon='PASTEDOWN')
        op.data_path = context_attr + "." + attr
    if unset and is_property_set:
        row2_sub = row2.row()
        row2_sub.alignment = 'RIGHT'
        op = row2_sub.operator(ops.WM_OT_pie_menu_property_unset.bl_idname,
                               text="", icon='X', emboss=False)
        op.data = context_attr
        op.property = attr



class ExecuteString:
    def exec_string_data(self, string, context, event):
        """data: function or str"""
        if not string:
            return None

        if event is None:
            event = oputils.events.get(context.window.as_pointer())
        kwargs = {"self": self, "context": context, "event": event}
        return oputils.execute(string, kwargs)

    def exec_string(self, key, context, event):
        string = getattr(self, key)
        if string:
            return self.exec_string_data(string, context, event)


class PieMenuItem(ExecuteString):
    def __getattribute__(self, key):
        if key in ("_data", "_overwrite", "poll", "execute"):
            return super().__getattribute__(key)

        overwrite = super().__getattribute__("_overwrite")
        if key in overwrite:
            return super().__getattribute__(key)

        data = super().__getattribute__("_data")
        if hasattr(data, key):
            return getattr(data, key)

        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self._overwrite.add(key)

    def __init__(self, data):
        self._overwrite = set()
        self._data = data

        if getattr(data, "shift", None):
            self.shift = PieMenuItem(data.shift)
        if getattr(data, "ctrl", None):
            self.ctrl = PieMenuItem(data.ctrl)

        # 描画等で使う
        self.enabled = False
        self.icon_box_rect = []
        self.text_box_rect = []
        self.direction = 'NONE'

    icon = ""
    menu = ""
    undo_push = False
    shortcut = ""
    translate = True

    shift = None
    ctrl = None

    @property
    def label(self):
        text = ""
        if hasattr(self._data, "label"):
            text = self._data.label
        else:
            execute = getattr(self._data, "execute", None)
            if execute and isinstance(execute, str):
                op_rna = oputils.get_operator_rna(execute)
                if op_rna:
                    text = op_rna.bl_rna.name
                    if self.translate:
                        text = translate_iface(text, "Operator")
        return text

    @property
    def description(self):
        text = ""
        if hasattr(self._data, "description"):
            text = self._data.label
        else:
            execute = getattr(self._data, "execute", None)
            if execute and isinstance(execute, str):
                op_rna = oputils.get_operator_rna(execute)
                if op_rna:
                    text = op_rna.bl_rna.description
                    if self.translate:
                        text = translate_iface(text, "")
        return text

    def poll(self, context):
        func = getattr(self._data, "poll", None)
        if func:
            if isinstance(func, str):
                return bool(self.exec_string_data(func, context, None))
            else:
                return bool(func(context))
        else:
            execute = getattr(self._data, "execute", None)
            if execute and isinstance(execute, str):
                op = oputils.get_operator(execute)
                if op:
                    return op.poll()
            return True

    def execute(self, context, event=None):
        func = getattr(self._data, "execute", None)
        if func:
            if isinstance(func, str):
                return self.exec_string_data(func, context, event)
            else:
                try:
                    sig = inspect.signature(func)
                    use_event = "event" in sig.parameters
                except:
                    use_event = False
                if use_event:
                    if not event:
                        event = oputils.events.get(context.window.as_pointer())
                    return func(context, event)
                else:
                    return func(context)
        else:
            return None

    def get_execute_string(self):
        execute = getattr(self._data, "execute", None)
        if execute:
            if isinstance(execute, str):
                return execute
            else:
                try:
                    text = inspect.getsource(execute)
                    lines = text.split("\n")[1:]
                    indent = None
                    for line in lines:
                        m = re.match("( *)(.*)", line)
                        if m.group(2):
                            n = len(m.group(1))
                            if indent is None or n < indent:
                                indent = n
                    if indent is None:
                        indent = 0
                    return "\n".join([line[indent:] for line in lines])
                except:
                    return ""
        else:
            return ""


class PieMenu(ExecuteString):
    DEFAULT_RADIUS = 50
    DEFAULT_DRAW_TYPE = 'BOX'

    # {idname: index, ...}
    _last_item_direction = {}

    def __getattribute__(self, key):
        if key in ("_data", "_overwrite", "init", "poll"):
            return super().__getattribute__(key)

        overwrite = super().__getattribute__("_overwrite")
        if key in overwrite:
            return super().__getattribute__(key)

        data = super().__getattribute__("_data")
        if hasattr(data, key):
            return getattr(data, key)

        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        try:
            super().__setattr__(key, value)
        except:
            raise
        else:
            self._overwrite.add(key)

    def __init__(self, data):
        self._overwrite = set()
        self._data = data

        # 描画等で使用
        self.current_items_indices = []
        self.item_boundary_angles = []
        self.active_index = -1
        self.active_item_index = -1
        self.is_valid_click = True
        self.co = [0, 0]
        self.current_items_type = ""  # "", "shift", "ctrl", "alt", "oskey"
        self.radius_ = 0

    idname = ""
    label = ""
    menu_items = []
    item_order = 'OFFICIAL'
    quick_action = 'NONE'  # 'NONE', 'LAST', 'N', 'NE', ...
    highlight = 'NONE'  # 'NONE', 'LAST', 'N', 'NE', ...
    icon_scale = 1.0
    icon_expand = 0.0
    translate = True
    next = ""
    prev = ""

    @property
    def radius(self):
        if pie_menu and pie_menu.addon_preferences:
            radius = pie_menu.addon_preferences.menu_radius
        else:
            radius = self.DEFAULT_RADIUS
        return radius

    @property
    def draw_type(self):
        if pie_menu and pie_menu.addon_preferences:
            draw_type = pie_menu.addon_preferences.draw_type
        else:
            draw_type = self.DEFAULT_DRAW_TYPE
        if draw_type == 'SIMPLE_BOX':
            if self.icon_scale > 1.0:
                draw_type = 'BOX'
            else:
                draw_type = 'SIMPLE'
        elif draw_type == 'SIMPLE_CIRCLE':
            if self.icon_scale > 1.0:
                draw_type = 'CIRCLE'
            else:
                draw_type = 'SIMPLE'
        return draw_type

    def poll(self, context):
        func = getattr(self._data, "poll", None)
        if func:
            if isinstance(func, str):
                return bool(self.exec_string_data(func, context, None))
            else:
                return bool(func(context))
        else:
            return True

    def init(self, context):
        func = getattr(self._data, "init", None)
        if func:
            if isinstance(func, str):
                return self.exec_string_data(func, context, None)
            else:
                func(context)

        if len(self._data.menu_items) > 8:
            print("Warning: Pie menus with more than 8 items are currently "
                  "unsupported")

        items = []
        for item in self._data.menu_items:
            if item is None:
                items.append(None)
            else:
                items.append(PieMenuItem(item))
        self.menu_items = items

    @property
    def current_items(self):
        mod = self.current_items_type

        items = []
        for item in self.menu_items:
            if item is None:
                items.append(item)
            else:
                if mod == "shift" and item.shift:
                    items.append(item.shift)
                elif mod == "ctrl" and item.ctrl:
                    items.append(item.ctrl)
                else:
                    items.append(item)

        ls = []
        for i in self.current_items_indices:
            if i == -1:
                ls.append(None)
            else:
                item = items[i]
                if item is None:
                    ls.append(None)
                else:
                    ls.append(item)
        return ls

    @staticmethod
    def calc_item_indices(item_order, num):
        def sort_cw():
            for n in (4, 8):
                if num <= n:
                    return list(range(num)) + [-1] * (n - num)

        def sort_cw6():
            indices = sort_cw()
            n = int(len(indices) / 2)
            indices = indices[n:] + indices[:n]
            return indices

        def sort_official_modified(modified=False):
            if modified:
                if num <= 4:
                    order = [3, 1, 2, 0]
                else:
                    order = [3, 7, 1, 5, 2, 4, 0, 6]
            else:
                if num <= 4:
                    order = [3, 1, 2, 0]
                else:
                    order = [3, 5, 1, 7, 2, 6, 0, 4]

            indices = list(range(num)) + [-1] * (len(order) - num)

            return [indices[i] for i in order]

        if num > 8:
            raise ValueError()
        if item_order == 'CW':
            indices = sort_cw()
        elif item_order == 'CW6':
            indices = sort_cw6()
        elif item_order == 'OFFICIAL':
            indices = sort_official_modified()
        else:  # elif self.item_order == 'MODIFIED':
            indices = sort_official_modified(True)

        return indices

    def update_item_directions(self):
        items = self.menu_items

        if len(items) <= 4:
            directions = ['N', 'E', 'S', 'W']
        else:
            directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

        for i, index in enumerate(self.current_items_indices):
            if index != -1:
                item = items[index]
                if item is not None:
                    item.direction = directions[i]
                    if item.shift is not None:
                        item.shift.direction = directions[i]
                    if item.ctrl is not None:
                        item.ctrl.direction = directions[i]

    def update_current_items(self, context, op):
        mod = op.last_modifier()
        self.current_items_type = mod

        num = min(len(self.menu_items), 8)
        indices = self.calc_item_indices(self.item_order, num)
        self.current_items_indices = indices

        self.update_item_directions()

        current_items = self.current_items

        # poll()
        for item in current_items:
            if item is not None:
                item.enabled = item.poll(context)

        # calc boundaries
        num = len(current_items)
        pie_angle = math.pi * 2 / num
        item_boundary_angles = [[0.0, 0.0] for i in range(num)]

        if IGNORE_EMPTY_SPACE:
            for i, item in enumerate(current_items):
                if item is None:
                    continue
                angle = math.pi * 0.5 - pie_angle * i
                if angle < -1e-5:
                    angle += math.pi * 2
                # CCW side
                for k in range(1, num + 1):
                    if current_items[i - k]:
                        ang = angle + pie_angle * k * 0.5
                        item_boundary_angles[i][0] = ang
                        break
                # CW side
                for k in range(1, num + 1):
                    if current_items[(i + k) % num]:
                        ang = angle - pie_angle * k * 0.5
                        item_boundary_angles[i][1] = ang
                        break
        else:
            for i, item in enumerate(current_items):
                if item is None:
                    continue
                angle = math.pi * 0.5 - pie_angle * i
                if angle < -1e-5:
                    angle += math.pi * 2
                item_boundary_angles[i] = [angle + pie_angle * 0.5,
                                           angle - pie_angle * 0.5]
        self.item_boundary_angles = item_boundary_angles

    def correct_radius(self):
        """Item同士が重ならないようにMenu半径を大きくする。
        値は redius_ に格納する
        """

        addon_prefs = pie_menu.addon_preferences
        # radius = self.get("radius", addon_prefs.menu_radius)
        radius = self.radius

        current_items = self.current_items
        num = len(current_items)
        if num == 0:
            return

        # 8個を最小とする
        num = max(8, num)

        pie_angle = math.pi * 2 / num
        widget_unit = vawm.widget_unit()

        if self.draw_type == 'SIMPLE':
            n = num / 4
            r = widget_unit * (n - 0.5) + addon_prefs.item_min_space * n
            self.radius_ = max(r, radius)
        else:
            icon_box_size = widget_unit * self.icon_scale
            if self.draw_type == 'CIRCLE':
                # >>> (r + icon_size / 2) * math.sin(pie_angle / 2) = \
                # (icon_size + item_min_space) / 2
                r = (icon_box_size + addon_prefs.item_min_space) / 2 / \
                    math.sin(pie_angle / 2) - icon_box_size / 2
                self.radius_ = max(r, radius)
            else:  # 'BOX'
                # >>> (r + icon_size / 2) * math.sin(pie_angle) = \
                # icon_size + item_min_space
                r = (icon_box_size + addon_prefs.item_min_space) / \
                    math.sin(pie_angle) - icon_box_size / 2
                self.radius_ = max(r, radius)

    def calc_active(self, mco):
        """:rtype: (int, int)"""
        addon_prefs = pie_menu.addon_preferences

        current_items = self.current_items

        if not current_items:
            return -1, -1

        vec = mco - self.co
        if vec.length < addon_prefs.menu_radius_center:
            active_index = -1
        else:
            angle = math.pi * 0.5
            pie_angle = math.pi * 2 / len(current_items)
            for i, item in enumerate(current_items):
                if IGNORE_EMPTY_SPACE:
                    a1 = angle + pie_angle / 2 + 1e-4
                    a2 = angle - pie_angle / 2 - 1e-4
                else:
                    if not item:
                        continue
                    a1, a2 = self.item_boundary_angles[i]
                v1 = (math.cos(a1), math.sin(a1))
                v2 = (math.cos(a2), math.sin(a2))
                if cross2d(v2, vec) >= 0 and cross2d(vec, v1) >= 0:
                    active_index = i
                    break
                angle -= pie_angle
            else:
                active_index = -1

        def direction_to_index(direction):
            if len(current_items) <= 4:
                directions = ['N', 'E', 'S','W']
            else:
                directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            for i, direction_ in enumerate(directions):
                if direction == direction_:
                    return i
            return -1  # 'NONE'

        active_item_index = -1
        if active_index == -1:
            if self.quick_action == 'NONE':
                pass
            elif self.quick_action == 'LAST':
                last_item_direction = self.get_last_item_direction()
                i = direction_to_index(last_item_direction)
                if i != -1 and current_items[i]:
                    active_item_index = i
            else:
                i = direction_to_index(self.quick_action)
                if i != -1 and current_items[i]:
                    active_item_index = i
        else:
            item = current_items[active_index]
            if item:
                active_item_index = active_index

        return active_index, active_item_index

    def update_active(self, mco, mco_press):
        """active_indexとactive_itemを更新。
        """
        self.active_index, self.active_item_index = self.calc_active(mco)
        if mco_press is not None:
            i, _ = self.calc_active(mco_press)
            self.is_valid_click = i == self.active_index
        else:
            self.is_valid_click = True

    def get_last_item_direction(self):
        return self._last_item_direction.get(self.idname, 'NONE')

    def set_last_item_direction(self, direction):
        self._last_item_direction[self.idname] = direction

    def clear_last_item_direction(self):
        if self.idname in self._last_item_direction:
            del self._last_item_direction[self.idname]
