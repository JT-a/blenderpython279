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
    "name": "Pivot Point: Key: 'F16 key'",
    "location": "F16 key",
    "category": "Mesh",
}


from collections import OrderedDict

import bpy

from ..utils import addongroup

import pie_menu


class PieMenuPivotPointAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def index_to_direction(index):
    # directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    directions = ['W', 'E', 'S', 'N', 'NW', 'NE', 'SW', 'SE']
    return directions[index]


class PivotPoint:
    idname = 'pivot_point'
    label = 'Pivot Point'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []
        icons = OrderedDict([('BOUNDING_BOX_CENTER', 'ROTATE'),
                             ('INDIVIDUAL_ORIGINS', 'ROTATECOLLECTION'),
                             ('MEDIAN_POINT', 'ROTATECENTER'),
                             ('CURSOR', 'CURSOR'),
                             ('ACTIVE_ELEMENT', 'ROTACTIVE')])

        self.highlight = 'NONE'
        if context.area.type == 'VIEW_3D':
            v3d = context.space_data
        else:
            v3d = None

        p = bpy.types.SpaceView3D.bl_rna.properties["pivot_point"]
        for i, enum_item in enumerate(p.enum_items):
            item = Empty(label=enum_item.name)
            item.description = enum_item.description
            item.icon = icons[enum_item.identifier]
            item.execute = (
                "wm.context_set_enum(data_path='space_data.pivot_point', "
                "value='{}')".format(enum_item.identifier))
            self.menu_items.append(item)

            # if v3d and enum_item.identifier == v3d.pivot_point:
            #     self.highlight = index_to_direction(i)

        p = bpy.types.SpaceView3D.bl_rna.properties["use_pivot_point_align"]
        item = Empty(label="Toggle Align")
        item.execute = ("wm.context_toggle("
                        "data_path='space_data.use_pivot_point_align')")
        item.description = p.description
        item.icon = 'ALIGN'
        self.menu_items.append(item)

        # self.menu_items.insert(1, None)
        # self.menu_items.insert(3, None)
        self.menu_items.insert(5, None)


PieMenuPivotPointAddonPreferences.menus = [
    PivotPoint,
]

menu_keymap_items = {
    "pivot_point": [
        ["3D View", {"type": 'F16', "value": 'PRESS'}],
        # ["3D View", {"type": 'PERIOD', "value": 'PRESS'}],
        # ["3D View", {"type": 'COMMA', "value": 'PRESS'}]
    ],
}


classes = [
    PieMenuPivotPointAddonPreferences
]


@PieMenuPivotPointAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuPivotPointAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuPivotPointAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuPivotPointAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
