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


import enum
import math
import re
import inspect
import traceback

import bpy
from mathutils import Vector

from ..utils import vawm

import piemenus

from . import oputils
from .preferences import PieMenuPreferences
from . import stubs
from .stubs import cross2d


translate_iface = bpy.app.translations.pgettext_iface
translate_tip = bpy.app.translations.pgettext_tip


class bimethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        import functools
        return functools.partial(self.func, instance, cls)


class DrawType(enum.Enum):
    SIMPLE = 1
    BOX = 2
    CIRCLE = 3

    SIMPLE_BOX = 4
    SIMPLE_CIRCLE = 5


class QuickAction(enum.Enum):
    NONE = 1
    LAST = 2
    FIXED = 3


class Highlight(enum.Enum):
    NONE = 1
    LAST = 2
    FIXED = 3


class ItemOrder(enum.Enum):
    CW = 1
    CW6 = 2
    OFFICIAL = 3
    MODIFIED = 4


class DataGetter:
    data = None

    def has_data(self, key):
        if self.data is None:
            return False
        elif isinstance(self.data, dict):
            return key in self.data
        else:
            return hasattr(self.data, key)

    def get_data(self, key):
        if self.data is None:
            return None
        elif isinstance(self.data, dict):
            return self.data.get(key)
        else:
            return getattr(self.data, key, None)

    @classmethod
    def call_function_data(cls, obj, func, context, event, as_class=False):
        """data: function or str"""
        if obj is None or func is None:
            return None

        if event is None:
            event = oputils.events.get(context.window.as_pointer())
        if isinstance(func, str):
            if not func:
                return
            kwargs = {"context": context, "event": event}
            if as_class:
                kwargs["cls"] = obj
            else:
                kwargs["self"] = obj
            return oputils.execute(func, kwargs)
        else:
            try:
                sig = inspect.signature(func)
                use_event = "event" in sig.parameters
            except:
                use_event = False
            try:
                if use_event:
                    return func(context, event)
                else:
                    return func(context)
            except:
                traceback.print_exc()

    def call_function(self, key, context, event):
        obj = self.data
        func = None
        if self.has_data(key):
            func = self.get_data(key)
        if func is not None:
            return self.call_function_data(obj, func, context, event)


class Item(DataGetter):
    attributes = [
        "icon", "menu", "undo_push", "shortcut", "translate"
    ]
    overwrote = None
    """:type: set"""

    def __getattribute__(self, name):
        attributes = super().__getattribute__("attributes")
        overwrote = super().__getattribute__("overwrote")
        has_data = super().__getattribute__("has_data")
        if name in attributes and has_data(name):
            if overwrote is not None and name not in overwrote:
                return self.get_data(name)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if self.overwrote is not None:
            self.overwrote.add(name)

    def __delattr__(self, name):
        if self.overwrote is not None:
            self.overwrote.discard(name)
        super().__delattr__(name)

    def __init__(self, data, menu):
        self.data = data
        self.owner = menu
        """:type: Menu"""

        self.label = ""
        self.description = ""
        self.icon = None
        self.menu = ""
        self.undo_push = False
        self.shortcut = ""
        self.translate = None
        self._label = None
        self._description = None

        self.enabled = True

        self.overwrote = set()

    def get_execute_string(self):
        execute = self.get_data("execute")

        if execute is None:
            return None
        elif isinstance(execute, str):
            return execute
        else:
            try:
                string = inspect.getsource(execute)
            except:
                # traceback.print_exc()
                return None
            string = string.strip("\n")
            lines = string.split("\n")
            if len(lines) == 1:
                return string
            else:  # 先頭行とインデントを一段消す
                indent = []
                for line in lines[1:]:
                    m = re.match("(\s*).*", line)
                    indent.append(len(m.group(1)))
                lines = [line[min(indent):] for line in lines[1:]]
                text = "\n".join(lines)
                if text == "pass":
                    return None
                else:
                    return text

    @property
    def label(self):
        text = ""
        op = None
        if self._label is not None:
            text = self._label
        elif self.has_data("label"):
            text = self.get_data("label")
        else:
            execute_string = self.get_execute_string()
            if execute_string:
                op_rna = oputils.get_operator_rna(execute_string)
                if op_rna:
                    text = op_rna.name
        if self.translate or self.translate is None and self.owner.translate:
            text_ = text
            text = translate_iface(text, "Operator")
            if text == text_ and not op:
                text = translate_iface(text, "*")
        return text

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def description(self):
        text = ""
        if self._description is not None:
            text = self._description
        elif self.has_data("description"):
            text = self.get_data("description")
        else:
            execute_string = self.get_execute_string()
            if execute_string:
                op_rna = oputils.get_operator_rna(execute_string)
                if op_rna:
                    text = op_rna.bl_rna.description
        if self.translate or self.translate is None and self.owner.translate:
            text = translate_tip(text)
        return text

    @description.setter
    def description(self, description):
        self._description = description

    def poll(self, context):
        if self.has_data("poll"):
            result = self.call_function("poll", context, None)
            enabled = bool(result)
        else:
            enabled = True
        return enabled

    def execute(self, context, event):
        if self.has_data("execute"):
            result = self.call_function("execute", context, event)
        else:
            result = None
        return result


def porp_enum_get(self, attr, enum_class, default_value):
    _attr = "_" + attr
    val = getattr(self, _attr)
    if val is not None:
        value = val
    elif self.has_data(attr):
        value = self.get_data(attr)
        if isinstance(value, enum_class):
            pass
        else:
            value = enum_class[value.upper()]
    else:
        value = default_value
    return value


class Menu(DataGetter):
    # {idname: index, ...}
    _last_item_index = {}

    _last_item_direction = {}

    attributes = [
        "idname", "icon_scale", "icon_expand", "radius", "next", "prev",
        "quick_action_index", "highlight_index", "translate",
        # "keymap_items",
    ]
    overwrote = None
    """:type: set"""

    def __getattribute__(self, name):
        attributes = super().__getattribute__("attributes")
        overwrote = super().__getattribute__("overwrote")
        has_data = super().__getattribute__("has_data")
        if name in attributes and has_data(name):
            if overwrote is not None and name not in overwrote:
                return self.get_data(name)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if self.overwrote is not None:
            self.overwrote.add(name)

    def __delattr__(self, name):
        if self.overwrote is not None:
            self.overwrote.discard(name)
        super().__delattr__(name)

    @classmethod
    def get_menu(cls, idname):
        return piemenus.get_menu(idname)

    def __init__(self, context, data):
        if isinstance(data, dict):
            self.data = data
        else:
            self.data = data(context)
        self.call_function("init", context, None)

        self.idname = ""
        self.icon_scale = 1.0  # size of box or circle
        self.icon_expand = 0.0  # 0.0: default, -1.0 min, 1.0: max
        self.radius = 0
        self.next = ""
        self.prev = ""
        self.items = []
        self.shift_items = []
        self.ctrl_items = []
        self.alt_items = []
        self.oskey_items = []
        self.quick_action_index = 0
        self.highlight_index = 0
        self.translate = True
        # self.keymap_items = []  # [["3D View", {"type": 'A', ...}], ...]

        self._label = None
        self._draw_type = None
        self._quick_action = None
        self._highlight = None
        self._item_order = None

        self.item_boundary_angles = []  # [[ang, ang], ...] 前・次のアイテムとの境界
        self.active_index = -1
        self.active_item = None
        self.is_valid_click = True
        self.co = Vector([0.0, 0.0])
        self.current_items = []
        self.current_items_type = ""  # "", "shift", "ctrl", "alt", "oskey"

        self.overwrote = set()

        self.init_items(context)

    @property
    def label(self):
        if self._label is not None:
            text = self._label
        elif self.has_data("label"):
            text = self.get_data("label")
        else:
            text = ""
        if self.translate:
            text_ = text
            text = translate_iface(text, "*")
            if text == text_:
                text = translate_iface(text, "Operator")
        return text

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def draw_type(self):
        dt = DrawType[stubs.addon_preferences.draw_type]
        draw_type = porp_enum_get(self, "draw_type", DrawType, dt)
        if self.icon_scale > 1.0:
            if draw_type == DrawType.SIMPLE_BOX:
                draw_type = DrawType.BOX
            elif draw_type == DrawType.SIMPLE_CIRCLE:
                draw_type = DrawType.CIRCLE
        return draw_type

    @draw_type.setter
    def draw_type(self, draw_type):
        self._draw_type = DrawType(draw_type)

    @property
    def quick_action(self):
        return porp_enum_get(self, "quick_action", QuickAction,
                             QuickAction.NONE)

    @quick_action.setter
    def quick_action(self, quick_action):
        self._quick_action = QuickAction(quick_action)

    @property
    def highlight(self):
        return porp_enum_get(self, "highlight", Highlight, Highlight.NONE)

    @highlight.setter
    def highlight(self, highlight):
        self._highlight = Highlight(highlight)

    @property
    def item_order(self):
        return porp_enum_get(self, "item_order", ItemOrder, ItemOrder.OFFICIAL)

    @item_order.setter
    def item_order(self, item_order):
        self._item_order = ItemOrder(item_order)

    @classmethod
    def poll(cls, context, idname):
        menu_data = cls.get_menu(idname)

        if menu_data is None:
            return None

        if isinstance(menu_data, dict):
            func = menu_data.get("poll")
        else:
            func = getattr(menu_data, "poll", None)
        if func:
            if not cls.call_function_data(menu_data, func, context, None,
                                          as_class=True):
                return False
        return True

    def init_items(self, context):
        """インスタンス生成時とメニュー切替時に呼ぶ"""

        def sort_cw(items):
            num = len(items)
            if num <= 16:
                for n in (4, 8, 16):
                    if num <= n:
                        return list(items) + [None] * (num - n)
            else:
                raise ValueError("未対応")

        def sort_cw6(items):
            num = len(items)
            if num <= 16:
                for n in (4, 8, 16):
                    if num <= n:
                        items = list(items) + [None] * (num - n)
                        break
            else:
                raise ValueError("未対応")
            num = len(items)
            n = int(num / 2)
            items = items[n:] + items[:n]

            for attr in ["quick_action_index", "highlight_index"]:
                if self.has_data(attr):
                    index = self.get_data(attr)
                    if 0 <= index < num:
                        i = index - n
                        if i < 0:
                            i += num
                        setattr(self, attr, i)
            return items

        def sort_official_modified(items, modified=False):
            num = len(items)
            if modified:
                if num <= 4:
                    order = [3, 1, 2, 0]
                elif num <= 8:
                    order = [3, 7, 1, 5, 2, 4, 0, 6]
                    # elif num <= 12:
                    #     order = [3, 12, 7, 11, 5, 9, 2, 8, 4, 0, 6, 11]
                elif num <= 16:
                    order = [3, 15, 7, 11, 1, 9, 5, 13, 2, 12, 4, 8, 0, 10, 6,
                             14]
                else:
                    raise ValueError("未対応")
            else:
                if num <= 4:
                    order = [3, 1, 2, 0]
                elif num <= 8:
                    order = [3, 5, 1, 7, 2, 6, 0, 4]
                elif num <= 16:
                    order = [3, 15, 5, 11, 1, 9, 7, 13, 2, 12, 6, 8, 0, 10, 4,
                             14]
                else:
                    raise ValueError("未対応")

            while len(items) < len(order):
                items.append(None)

            num = len(items)
            for attr in ["quick_action_index", "highlight_index"]:
                if self.has_data(attr):
                    index = self.get_data(attr)
                    if 0 <= index < num:
                        setattr(self, attr, order.index(index))

            def func(ob):
                return order.index(ob[0])

            return [ob[1] for ob in sorted(enumerate(items), key=func)]

        for attr in ["items", "shift_items", "ctrl_items", "alt_items",
                     "oskey_items"]:
            items = self.get_data(attr)
            if items is None:
                setattr(self, attr, [])
                continue
            items_ = []
            for item in items:
                if item is None:
                    items_.append(None)
                else:
                    items_.append(Item(item, self))

            if items_:
                if self.item_order == ItemOrder.CW:
                    items_ = sort_cw(items_)
                elif self.item_order == ItemOrder.CW6:
                    items_ = sort_cw6(items_)
                elif self.item_order == ItemOrder.OFFICIAL:
                    items_ = sort_official_modified(items_)
                elif self.item_order == ItemOrder.MODIFIED:
                    items_ = sort_official_modified(items_, True)
                else:
                    msg = "item_order must be in ['CW', 'CW6', 'OFFICIAL', " \
                          "'MODIFIED']. got '{}'"
                    raise ValueError(msg.format(self.item_order))
            else:
                if attr == "items":
                    items_ = [None] * 4
                else:
                    items_ = []

            setattr(self, attr, items_)

    def update_current_items(self, context, op):
        """current_itemsの更新とpollの実行"""

        mod = op.last_modifier()
        # op.event_history
        items = []
        if mod == "shift":
            items = self.shift_items
            self.current_items_type = "shift"
        elif mod == "ctrl":
            items = self.ctrl_items
            self.current_items_type = "ctrl"
        elif mod == "alt":
            items = self.alt_items
            self.current_items_type = "alt"
        elif mod == "oskey":
            items = self.oskey_items
            self.current_items_type = "oskey"
        if not items:
            items = self.items
            self.current_items_type = ""
        num = len(items)

        if num % 4 != 0 or num == 0:
            raise ValueError("num % 4 != 0 or num == 0")

        for item in items:
            if item is not None:
                item.enabled = item.poll(context)
        self.current_items = items

        pie_angle = math.pi * 2 / num

        self.item_boundary_angles = [[0.0, 0.0] for i in range(num)]

        for i, item in enumerate(items):
            if not item:
                continue
            angle = math.pi * 0.5 - pie_angle * i
            if angle < -1e-5:
                angle += math.pi * 2
            # CCW side
            for j in range(1, num + 1):
                if items[i - j]:
                    ang = angle + pie_angle * j * 0.5
                    self.item_boundary_angles[i][0] = ang
                    break
            # CW side
            for j in range(1, num + 1):
                if items[(i + j) % num]:
                    ang = angle - pie_angle * j * 0.5
                    self.item_boundary_angles[i][1] = ang
                    break

    def correct_radius(self):
        """Item同士が重ならないようにMenu半径を大きくする。
        redius を変更する
        """
        addon_prefs = PieMenuPreferences.get_instance()

        if self.has_data("radius"):
            radius = self.get_data("radius")
        else:
            # radius = self.radius
            radius = addon_prefs.menu_radius
        if radius <= 0:
            self.radius = radius = addon_prefs.menu_radius

        if len(self.current_items) == 0:
            return

        pie_angle = math.pi * 2 / len(self.current_items)
        widget_unit = vawm.widget_unit()

        if self.draw_type == DrawType.SIMPLE:
            n = len(self.current_items) / 4
            r = widget_unit * (n - 0.5) + addon_prefs.item_min_space * n
            self.radius = max(r, radius)
        else:
            icon_box_size = widget_unit * self.icon_scale
            if self.draw_type == DrawType.CIRCLE:
                # >>> (r + icon_size / 2) * math.sin(pie_angle / 2) = \
                # (icon_size + item_min_space) / 2
                r = (icon_box_size + addon_prefs.item_min_space) / 2 / \
                    math.sin(pie_angle / 2) - icon_box_size / 2
                self.radius = max(r, radius)
            else:  # DrawType.CIRCLE
                # >>> (r + icon_size / 2) * math.sin(pie_angle) = \
                # icon_size + item_min_space
                r = (icon_box_size + addon_prefs.item_min_space) / \
                    math.sin(pie_angle) - icon_box_size / 2
                self.radius = max(r, radius)

    def calc_active(self, mco):
        addon_prefs = PieMenuPreferences.get_instance()
        items = self.current_items

        if not items:
            return -1, None

        vec = mco - self.co
        if vec.length < addon_prefs.menu_radius_center:
            active_index = -1
        else:
            idx = 0
            for i, item in enumerate(items):
                if item is None:
                    continue
                idx = i
                a1, a2 = self.item_boundary_angles[i]
                v1 = (math.cos(a1), math.sin(a1))
                v2 = (math.cos(a2), math.sin(a2))
                if cross2d(v2, vec) >= 0 and cross2d(vec, v1) >= 0:
                    active_index = i
                    break
            else:
                active_index = idx

        active_item = None
        if active_index == -1:
            if self.quick_action == QuickAction.LAST:
                last_item_index = self.get_last_item_index()
                if 0 <= last_item_index < len(items):
                    if items[last_item_index]:
                        active_item = items[last_item_index]
            elif self.quick_action == QuickAction.FIXED:
                if 0 <= self.quick_action_index < len(items):
                    if items[self.quick_action_index]:
                        active_item = items[self.quick_action_index]
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

    def get_last_item_index(self):
        if 0:
            d = self._last_item_index.get(self.idname, {})
            return d.get(self.current_items_type, -1)
        else:
            return self._last_item_index.get(self.idname, -1)

    def set_last_item_index(self, index):
        if 0:
            d = self._last_item_index.setdefault(self.idname, {})
            d[self.current_items_type] = index
        else:
            self._last_item_index[self.idname] = index

    def clear_last_item_idnex(self):
        if self.idname in self._last_item_index:
            del self._last_item_index[self.idname]
