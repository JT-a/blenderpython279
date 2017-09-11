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
    "name": "View Selected: Key: 'Numpad . key', 'Button 5 Mouse'",
    "location": "Numpad . key, Button 5 Mouse",
    "category": "3D View"
}


from types import MethodType

import bpy

from ..utils import addongroup

import pie_menu


class PieMenuViewSelectedAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


def get_enum_items(obj, prop_name):
    prop = obj.bl_rna.properties[prop_name]
    return list(prop.enum_items)


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ViewSelected:
    idname = 'view_selected'
    label = 'View Selected'
    quick_action = 'S'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []

        # View Selected (Numpad .)
        item = Empty()
        item.icon = 'ZOOM_SELECTED'
        item.execute = "view3d.view_selected"
        self.menu_items.append(item)

        # Center View to Mouse (Alf F)
        item = Empty()
        item.icon = 'RESTRICT_SELECT_OFF'
        item.execute = 'view3d.view_center_pick'
        item.shortcut = 'MIDDLEMOUSE'
        self.menu_items.append(item)

        # Center View to Cursor (Alt Home)
        item = Empty()
        item.icon = 'CURSOR'
        item.execute = "view3d.view_center_cursor"
        self.menu_items.append(item)

        # View All (Home)
        item = Empty()
        item.icon = 'RESTRICT_VIEW_OFF'
        item.execute = "view3d.view_all"
        self.menu_items.append(item)

        # View All (Ctrl Home)
        item = Empty()
        item.label = "View All (All Regions)"
        item.icon = 'RESTRICT_VIEW_OFF'
        item.execute = "view3d.view_all(use_all_regions=True)"
        self.menu_items.append(item)

        # View All (Shift C)
        item = Empty()
        item.label = "View All (Center))"
        item.icon = 'RESTRICT_VIEW_OFF'
        item.execute = "view3d.view_all(center=True)"
        self.menu_items.append(item)

        item = Empty(label='Center View to Selected')
        item.icon = 'ARROW_LEFTRIGHT'
        item.execute = '\n'.join(
            ["co = list(context.space_data.cursor_location)",
             "bpy.ops.view3d.snap_cursor_to_selected()",
             "bpy.ops.view3d.view_center_cursor()",
             "context.space_data.cursor_location = co"])
        self.menu_items.append(item)

        self.menu_items.append(None)


PieMenuViewSelectedAddonPreferences.menus = [
    ViewSelected
]


menu_keymap_items = {
    "view_selected": [
        ["3D View",  {"type": 'NUMPAD_PERIOD', "value": 'PRESS'}],
        ["3D View",  {"type": 'BUTTON5MOUSE', "value": 'PRESS'}]
    ],
}


classes = [
    PieMenuViewSelectedAddonPreferences
]


@PieMenuViewSelectedAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuViewSelectedAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname



@PieMenuViewSelectedAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuViewSelectedAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
