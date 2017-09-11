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
    "name": "Manipulator: Key: 'Ctrl Space'",
    "location": "Ctrl Space",
    "category": "3D View",
}


import bpy

from ..utils import addongroup

import pie_menu


class PieMenuManipulatorAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Manipulator:
    idname = 'manipulator'
    label = 'Manipulator'
    quick_action = 'N'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []

        t = bpy.types.SpaceView3D
        prop = t.bl_rna.properties["transform_manipulators"]
        enum_items = prop.enum_items
        for i, name in enumerate(('translate', 'rotate', 'scale')):
            item = Empty(label=name.title())
            self.menu_items.append(item)
            item.description = enum_items[i].description
            item.icon = ['MAN_TRANS', 'MAN_ROT', 'MAN_SCALE'][i]
            text = ('bpy.ops.view3d.enable_manipulator('
                    '\'INVOKE_DEFAULT\', {}=True)\n'
                    'bpy.ops.wm.context_set_boolean(data_path='
                    '"space_data.show_manipulator", value=True)')
            item.execute = text.format(name)
            item.use_shift = True
            item.poll = 'return bpy.ops.view3d.enable_manipulator.poll()'

            sub = item.shift = Empty(label='+' + name.title())
            sub.description = item.description
            sub.icon = item.icon
            text = '\n'.join(
                ['v3d = context.space_data',
                 'enables = v3d.transform_manipulators',  # 'TRANSLATE','ROTATE','SCALE'
                 'if {0} in enables:',
                 '    if len(enables) > 1:',
                 '        enables.remove({0})',
                 'else:',
                 '    enables.add({0})',
                 'v3d.transform_manipulators = enables',
                 'bpy.ops.wm.context_set_boolean(',
                 '    data_path="space_data.show_manipulator", value=True)']
            )
            sub.execute = text.format("'" + name.upper() + "'")
            sub.poll = item.poll

        item = Empty(label='Toggle')
        self.menu_items.append(item)
        bl_rna = bpy.types.SpaceView3D.bl_rna
        item.description = bl_rna.properties['show_manipulator'].description
        item.icon = 'MANIPUL'
        item.execute = 'wm.context_toggle' \
                       '(data_path="space_data.show_manipulator")'
        item.poll = "return context.area.type == 'VIEW_3D'"


PieMenuManipulatorAddonPreferences.menus = [Manipulator]

menu_keymap_items = {
    "manipulator": [
        ["3D View", {"type": 'SPACE', "value": 'PRESS', "ctrl": True}],
    ],
}


classes = [
    PieMenuManipulatorAddonPreferences
]


@PieMenuManipulatorAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuManipulatorAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuManipulatorAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuManipulatorAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
