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


class LinearAlignToolVert:
    idname = 'linear_align_tool_vert'
    label = 'Align Vertices'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []

        for axis in ('X', 'Y', 'Z'):
            text = "at.align_to_plane(space='{}', axis='{}')"
            item = Empty(label=axis)
            item.execute = text.format('GLOBAL', axis)
            self.menu_items.append(item)
            sub = item.shift = Empty(label='Local ' + axis)
            sub.execute = text.format('LOCAL', axis)

        item = Empty(label='View X')
        item.execute = "at.align_to_plane(space='VIEW', axis='X')"
        self.menu_items.append(item)

        item = Empty(label='View Y')
        item.execute = "at.align_to_plane(space='VIEW', axis='Y')"
        self.menu_items.append(item)

        item = Empty(label='Plane')
        item.execute = "at.align_to_plane(space='PLANE', axis='Z')"
        self.menu_items.append(item)

        item = Empty(label='Custom')
        item.execute = "at.align_to_plane(space='AXIS')"
        self.menu_items.append(item)


class LinearAlignToolEdge:
    idname = 'linear_align_tool_edge'
    label = 'Align Edges'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []
        item = Empty(label='Expand')
        item.execute = "at.edge_align_to_plane(mode='expand')"
        self.menu_items.append(item)

        item = Empty(label='Move')
        item.execute = "at.edge_align_to_plane(mode='move')"
        self.menu_items.append(item)

        item = Empty(label='Add Verts')
        item.execute = "at.edge_align_to_plane(mode='add')"
        self.menu_items.append(item)

        item = Empty(label='Add / Subdivide')
        item.execute = "at.edge_align_to_plane(mode='subdivide')"
        self.menu_items.append(item)


class LinearAlignToolSub:
    idname = 'linear_align_tool_sub'
    label = 'Linear Align Tool Sub'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []
        self.prev = 'linear_align_tool'

        item = Empty(label='Edge Unbend')
        item.execute = 'at.edge_unbend'
        self.menu_items.append(item)

        item = Empty(label='Edge Intersect')
        item.execute = 'at.edge_intersect'
        self.menu_items.append(item)

        item = Empty(label='Shift Tangent')
        item.execute = "at.shift(mode='tangent')"
        self.menu_items.append(item)

        item = Empty(label='Shift Normal')
        item.execute = "at.shift(mode='normal')"
        self.menu_items.append(item)


class LinearAlignTool:
    idname = 'linear_align_tool'
    label = 'Linear Align Tool'
    item_order = 'CW6'

    keymap_items = [['Mesh', {'type': 'A', 'ctrl': True}]]

    def init(self, context):
        self.menu_items = []
        self.next = 'linear_align_tool_sub'

        item = Empty(label='Align Vertices')
        item.menu = 'linear_align_tool_vert'
        self.menu_items.append(item)

        item = Empty(label='Align Edges')
        item.menu = 'linear_align_tool_edge'
        self.menu_items.append(item)

        item = Empty(label='Set Plane')
        item.execute = 'at.set_plane'
        self.menu_items.append(item)

        item = Empty(label='Set Axis')
        item.execute = 'at.set_axis'
        self.menu_items.append(item)


PieMenuLinearAlignToolsAddonPreferences.menus = [
    LinearAlignTool,
    LinearAlignToolSub,
    LinearAlignToolVert,
    LinearAlignToolEdge,

]

menu_keymap_items = {
    "linear_align_tool": [
        ["Mesh", {"type": 'A', "value": 'PRESS', "ctrl": True}],
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
