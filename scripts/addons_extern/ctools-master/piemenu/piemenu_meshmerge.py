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
    "name": "Merge: Key: 'Alt M', 'F14'",
    "location": "Alf M, F14",
    "category": "Mesh",
}


from collections import OrderedDict
from types import MethodType

import bpy

from ..utils import addongroup

import pie_menu


class PieMenuMeshMergeAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = []


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class MeshMerge:
    idname = 'mesh_merge'
    label = 'Merge'
    quick_action = 'LAST'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []
        bl_rna = bpy.ops.mesh.merge.get_rna().bl_rna
        prop = bl_rna.properties['type']
        icons = ['BACK', 'FORWARD' , 'ROTATECENTER', 'CURSOR',
                 'ROTATECOLLECTION']
        for enum_item, icon in zip(prop.enum_items, icons):
            item = Empty(label=enum_item.name)
            item.description = enum_item.description
            item.icon = icon
            item.execute = "mesh.merge(type='{}')".format(enum_item.identifier)
            self.menu_items.append(item)

            def poll(self, context):
                import bmesh
                bm = bmesh.from_edit_mesh(context.active_object.data)
                f = l = False
                history = bm.select_history
                if history:
                    if isinstance(history[0], bmesh.types.BMVert):
                        f = True
                    if isinstance(history[-1], bmesh.types.BMVert):
                        l = True
                if 'FIRST' in self.execute and not f:
                    return False
                if 'LAST' in self.execute and not l:
                    return False
                return True
            item.poll = MethodType(poll, item)

        for i in range(8 - len(self.menu_items)):
            self.menu_items.append(None)


PieMenuMeshMergeAddonPreferences.menus = [
    MeshMerge,
]

menu_keymap_items = {
    "mesh_merge": [
        ["Mesh", {"type": 'M', "value": 'PRESS', "alt": True}],
        ["Mesh", {"type": 'F14', "value": 'PRESS', "alt": True}],
    ],
}


classes = [
    PieMenuMeshMergeAddonPreferences
]


@PieMenuMeshMergeAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuMeshMergeAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuMeshMergeAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuMeshMergeAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
