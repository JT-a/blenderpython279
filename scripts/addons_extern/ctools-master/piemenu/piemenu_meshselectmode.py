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
    "name": "Delte: Key: 'Ctrl Tab'",
    "location": "X key",
    "category": "Mesh",
}


import bpy

from ..utils import addongroup

import pie_menu


class PieMenuMeshSelectModeAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class MeshSelectMode:
    idname = 'mesh_select_mode'
    label = 'Mesh Select Mode'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []
        desc_vert = "Vertex select - Shift-Click for multiple modes"
        desc_edge = "Edge select - Shift-Click for multiple modes, " \
                    "Ctrl-Click expands selection"
        desc_face = "Face select - Shift-Click for multiple modes, " \
                    "Ctrl-Click expands selection"

        item = Empty(label="Vertex")
        item.description = desc_vert
        item.icon = 'VERTEXSEL'
        item.execute = "mesh.select_mode(type='VERT')"
        self.menu_items.append(item)

        item = Empty(label="Edge")
        item.description = desc_edge
        item.icon = 'EDGESEL'
        item.execute = "mesh.select_mode(type='EDGE')"
        self.menu_items.append(item)

        item = Empty(label="Face")
        item.description = desc_face
        item.icon = 'FACESEL'
        item.execute = "mesh.select_mode(type='FACE')"
        self.menu_items.append(item)

        prop = bpy.types.SpaceView3D.bl_rna.properties["use_occlude_geometry"]
        item = Empty(label=prop.name)
        item.description = prop.description
        item.icon = 'ORTHO'
        item.execute = 'wm.context_toggle(data_path=' \
                       "'space_data.use_occlude_geometry')"
        self.menu_items.append(item)


PieMenuMeshSelectModeAddonPreferences.menus = [
    MeshSelectMode,
]


menu_keymap_items = {
    "mesh_select_mode": [
        ["Mesh", {"type": 'TAB', "value": 'PRESS', "ctrl": True}],
    ],
}


classes = [
    PieMenuMeshSelectModeAddonPreferences
]


@PieMenuMeshSelectModeAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuMeshSelectModeAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuMeshSelectModeAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuMeshSelectModeAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
