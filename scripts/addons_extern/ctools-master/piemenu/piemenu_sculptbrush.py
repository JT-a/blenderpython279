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
    "name": "Brushes: Key: 'D', 'C', 'S', 'G'",
    "location": "D, C, S, G",
    "category": "Sculpt",
}


from types import MethodType

import bpy

from ..utils import addongroup

import pie_menu


ICON_SCALE = 2.0


class PieMenuSculptBrushAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def index_to_direction(index):
    # directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']  # CW
    # directions = ['W', 'E', 'S', 'N', 'NW', 'NE', 'SW', 'SE']  # OFFICIAL
    directions = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']
    return directions[index]


def direction_to_index(direction):
    # directions = ['N', 'E', 'S', 'N', 'NW', 'NE', 'SW', 'SE']
    directions = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']
    return directions.index(direction)


class SculptBrushDraw:
    idname = 'sculpt_brush_draw'
    label = 'Brush Select'
    quick_action = 'NONE'
    icon_scale = ICON_SCALE
    icon_expand = 1.0
    item_order = 'CW6'

    brush_types = ['DRAW', 'CLAY', 'CLAY_STRIPS', 'INFLATE', 'BLOB',
                   'LAYER', 'CREASE']
    quick_brush_type = 'DRAW'

    def gen_submenu(self, context, sculpt_tool, sculpt_tool_name):
        menu = Empty()
        menu.menu_items = []
        menu.idname = "sculpt_brush_sub_" + sculpt_tool_name
        menu.label = sculpt_tool_name
        menu.quick_action = 'W'
        menu.icon_scale = self.icon_scale
        menu.icon_expand = self.icon_expand
        menu.item_order = 'CW6'
        brushes = [b for b in bpy.data.brushes if b.use_paint_sculpt and
                   b.sculpt_tool == sculpt_tool]
        brush = context.tool_settings.sculpt.brush
        if brush in brushes:
            i = brushes.index(brush)
        else:
            i = 0
        menu.quick_action = index_to_direction(i)
        for brush in brushes:
            if sculpt_tool == 'DRAW':
                icon = 'BRUSH_SCULPT_DRAW'
            else:
                icon = 'BRUSH_' + sculpt_tool
            item = Empty(label=brush.name)
            item.icon = icon
            item.execute = ('brush = bpy.data.brushes[self.label]\n'
                            'context.tool_settings.sculpt.brush = brush')
            menu.menu_items.append(item)
        for _ in range(8 - len(menu.menu_items)):
            menu.menu_items.append(None)

        for m in PieMenuSculptBrushAddonPreferences.menus:
            if m.idname == menu.idname:
                PieMenuSculptBrushAddonPreferences.menus.remove(m)
                break
        PieMenuSculptBrushAddonPreferences.menus.append(menu)

        return menu.idname

    def init(self, context):
        self.menu_items = []

        def poll(self, context):
            num = 0
            for brush in bpy.data.brushes:
                if (brush.use_paint_sculpt and
                        brush.sculpt_tool == self.sculpt_tool):
                    num += 1
            if num > 1:
                self.menu = self.main_menu.gen_submenu(
                    context, self.sculpt_tool, self.sculpt_tool_name)
            else:
                self.menu = ""
            return True

        def execute(self, context, event):
            if not self.menu or event.type not in (
                    'LEFTMOUSE', 'SPACE', 'RET', 'NUMPAD_ENTER'):
                bpy.ops.paint.brush_select(
                    True, paint_mode='SCULPT',
                    sculpt_tool=self.sculpt_tool)
                self.menu = ""

        prop = bpy.types.Brush.bl_rna.properties['sculpt_tool']
        for i, brush_type in enumerate(self.brush_types):
            enum_item = prop.enum_items[brush_type]
            item = Empty(label=enum_item.name)
            item.description = "Release key: decide, Press LeftMouse: sub menu"
            item.icon = enum_item.icon
            item.sculpt_tool_name = enum_item.name
            item.sculpt_tool = enum_item.identifier
            item.main_menu = self
            item.poll = MethodType(poll, item)
            item.execute = MethodType(execute, item)
            if brush_type == self.quick_brush_type:
                self.quick_action = index_to_direction(i)
            self.menu_items.append(item)


class SculptBrushClay(SculptBrushDraw):
    idname = "sculpt_brush_clay"
    quick_brush_type = 'CLAY'


class SculptBrushSmooth(SculptBrushDraw):
    idname = "sculpt_brush_smooth"
    quick_brush_type = 'SMOOTH'

    brush_types = ['SMOOTH', 'FLATTEN', 'FILL', 'SCRAPE', 'PINCH']


class SculptBrushGrub(SculptBrushDraw):
    idname = "sculpt_brush_grub"
    quick_brush_type = 'GRAB'

    brush_types = ['GRAB', 'ROTATE', 'THUMB', 'SNAKE_HOOK', 'NUDGE', 'MASK']


PieMenuSculptBrushAddonPreferences.menus = [
    SculptBrushDraw,
    SculptBrushClay,
    SculptBrushSmooth,
    SculptBrushGrub,
]


menu_keymap_items = {
    "sculpt_brush_draw": [
        ["Sculpt", {"type": 'D', "value": 'PRESS'}],
    ],
    "sculpt_brush_clay": [
        ["Sculpt", {"type": 'C', "value": 'PRESS'}],
    ],
    "sculpt_brush_smooth": [
        ["Sculpt", {"type": 'S', "value": 'PRESS'}],
    ],
    "sculpt_brush_grub": [
        ["Sculpt", {"type": 'G', "value": 'PRESS'}],
    ],
}


classes = [
    PieMenuSculptBrushAddonPreferences
]


@PieMenuSculptBrushAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuSculptBrushAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuSculptBrushAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuSculptBrushAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
