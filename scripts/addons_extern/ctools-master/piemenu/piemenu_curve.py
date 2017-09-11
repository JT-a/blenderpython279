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
    "name": "Linear Align Tools: Key: 'Ctrl A'",
    "location": "Ctrl A",
    "category": "Mesh",
}


from collections import OrderedDict
from types import MethodType

import bpy

from ..utils import addongroup

import pie_menu


class PieMenuLinearAlignToolsAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class CurveHandleType:
    idname = "curve_handle_type"
    label = "Handle Type"
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []
        rna = bpy.ops.curve.handle_type_set.get_rna()
        for enum_item in rna.bl_rna.properties["type"].enum_items:
            item = Empty(label=enum_item.name)
            item.description = enum_item.description
            item.execute = "curve.handle_type_set(type='{}')".format(
                enum_item.identifier)
            self.menu_items.append(item)


class CurveDelete:
    idname = "curve_delete"
    label = "Delete"
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []

        item = Empty(label="Select")
        item.execute = "curve.delete('EXEC_DEFAULT')"
        self.menu_items.append(item)

        item = Empty(label="Segment")
        item.execute = "curve.delete('EXEC_DEFAULT', type='SEGMENT')"
        self.menu_items.append(item)

        item = Empty()
        item.execute = "curve.dissolve_verts"
        self.menu_items.append(item)


PieMenuLinearAlignToolsAddonPreferences.menus = [
    CurveHandleType,
    CurveDelete,
]

menu_keymap_items = {
    "curve_handle_type": [
        ["Curve", {"type": 'V', "value": 'PRESS'}],
    ],
    "curve_delete": [
        ["Curve", {"type": 'X', "value": 'PRESS'}],
    ],
}


classes = [
    PieMenuLinearAlignToolsAddonPreferences
]


@PieMenuLinearAlignToolsAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuLinearAlignToolsAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuLinearAlignToolsAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuLinearAlignToolsAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
