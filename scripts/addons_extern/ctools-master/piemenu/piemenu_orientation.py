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
    "name": "Orientation: Key: 'Alt Space'",
    "location": "Alt Space",
    "category": "3D View",
}


import bpy

from ..utils import addongroup

import pie_menu


class PieMenuOrientationAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Orientation:
    idname = 'orientation'
    label = 'Orientation'
    item_order = 'CW6'

    def init(self, context):
        current_orientation = context.space_data.transform_orientation

        # 標準の座標系
        self.menu_items = []
        icons = {'GLOBAL': 'GRID',
                 'LOCAL': 'OBJECT_DATA',
                 'NORMAL': 'FACESEL',
                 'GIMBAL': 'MAN_ROT',
                 'VIEW': 'RESTRICT_VIEW_OFF',
                 'GRID': 'GRID',
                 }
        order = ['GLOBAL', 'LOCAL', 'GRID', 'NORMAL', 'VIEW','GIMBAL']

        t = bpy.types.SpaceView3D
        enum_items = t.bl_rna.properties['transform_orientation'].enum_items
        # enum_items.sort(key=lambda e: order.index(e.identifier))
        for i, enum_item in enumerate(enum_items):
            if enum_item.identifier == 'CUSTOM':
                continue
            item = Empty(label=enum_item.name)
            self.menu_items.append(item)
            item.description = enum_item.description
            item.icon = icons[enum_item.identifier]
            item.execute = 'wm.context_set_enum(' \
                           'data_path="space_data.transform_orientation", ' \
                           'value="{}")'.format(enum_item.identifier)
            item.identifier = enum_item.identifier

        for _ in range(8 - len(self.menu_items)):
            self.menu_items.append(None)

        directions = ['W', 'E', 'N', 'S', 'NW', 'NE', 'SW', 'SE']
        for i, item in enumerate(self.menu_items):
            if item and item.identifier == current_orientation:
                self.highlight = directions[i]

        # # ユーザー定義の座標系
        # prev = self
        # menu = None
        # num = 8
        # for i, orientation in enumerate(context.scene.orientations):
        #     if i % num == 0:
        #         j = i // num + 1
        #         menu = Menu(context)
        #         menu.idname = 'orientation_{}'.format(j)
        #         menu.label = 'Orientation {}'.format(j)
        #         prev.next = menu
        #         menu.prev = prev
        #         prev = menu
        #         menu.clear_last_item_direction()
        #     item = menu.add_item(orientation.name)
        #     item.execute = 'transform.select_orientation(\'EXEC_DEFAULT\', ' \
        #                    'orientation=\'{}\')'.format(orientation.name)
        #     if orientation.name == current_orientation:
        #         menu.set_last_item_index(len(menu.items) - 1)
        # if menu and len(menu.items) < num:
        #     menu.items.extend([None] * (num - len(menu.items)))


PieMenuOrientationAddonPreferences.menus = [Orientation]

menu_keymap_items = {
    "orientation": [
        ["3D View", {"type": 'SPACE', "value": 'PRESS', "alt": True}],
    ],
}


classes = [
    PieMenuOrientationAddonPreferences
]


@PieMenuOrientationAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuOrientationAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuOrientationAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuOrientationAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
