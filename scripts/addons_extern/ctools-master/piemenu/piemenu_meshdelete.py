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
    "name": "Delte: Key: 'X key'",
    "location": "X key",
    "category": "Mesh",
}


import bpy

from ..utils import addongroup

import pie_menu


class PieMenuMeshDeleteAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class MeshDelete:
    idname = 'mesh_delete'
    label = 'Delete'
    item_order = 'CW6'
    # quick_action = 'W'

    def init(self, context):
        self.menu_items = []

        item = Empty(label='Vertices')
        item.icon = 'VERTEXSEL'
        item.execute = "mesh.delete(type='VERT')"
        self.menu_items.append(item)

        item = Empty(label='Edge Loop')
        item.icon = 'EDGESEL'
        item.execute = 'mesh.delete_edgeloop()'
        self.menu_items.append(item)

        item = Empty(label='Edges')
        item.icon = 'EDGESEL'
        item.execute = "mesh.delete(type='EDGE')"
        self.menu_items.append(item)

        item = Empty(label='Only Edges & Faces')
        item.icon = 'FACESEL'
        item.execute = "mesh.delete(type='EDGE_FACE')"
        self.menu_items.append(item)

        item = Empty(label='Faces')
        item.icon = 'FACESEL'
        item.execute = "mesh.delete(type='FACE')"
        self.menu_items.append(item)

        item = Empty(label='Only Faces')
        item.icon = 'FACESEL'
        item.execute = "mesh.delete(type='ONLY_FACE')"
        self.menu_items.append(item)

        item = Empty(label='Dissolve ...')
        item.menu = 'mesh_delete_sub'
        item.icon = 'COLLAPSEMENU'
        self.menu_items.append(item)

        item = Empty()
        item.icon = 'EDGESEL'
        item.execute = 'mesh.edge_collapse'
        self.menu_items.append(item)


class MeshDeleteSub:
    idname = 'mesh_delete_sub'
    label = 'Delete Sub'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []

        item = Empty()
        item.icon = 'VERTEXSEL'
        item.execute = 'mesh.dissolve_verts'
        self.menu_items.append(item)

        item = Empty()
        item.icon = 'EDGESEL'
        item.execute = 'mesh.dissolve_edges'
        self.menu_items.append(item)

        item = Empty()
        item.icon = 'FACESEL'
        item.execute = 'mesh.dissolve_faces'
        self.menu_items.append(item)

        item = Empty()
        item.execute = 'mesh.dissolve_limited'
        self.menu_items.append(item)


PieMenuMeshDeleteAddonPreferences.menus = [
    MeshDelete,
    MeshDeleteSub,
]

menu_keymap_items = {
    "mesh_delete": [
        ["Mesh", {"type": 'X', "value": 'PRESS'}],
    ],
}


classes = [
    PieMenuMeshDeleteAddonPreferences
]


@PieMenuMeshDeleteAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuMeshDeleteAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuMeshDeleteAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuMeshDeleteAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
