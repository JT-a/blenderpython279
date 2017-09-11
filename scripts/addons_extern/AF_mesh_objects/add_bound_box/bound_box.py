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
    "name": "Bound Box",
    "author": "Multiple Authors",
    "version": (0, 3, 0),
    "blender": (2, 74, 5),
    "location": "View3D > Add > Mesh",
    "description": "Add Bound Box Options",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

if "bpy" in locals():
    import importlib
    importlib.reload(create_multi_bound_box)
    importlib.reload(add_bound_box)
    importlib.reload(object_bounding_box)


else:
    from . import create_multi_bound_box
    from . import add_bound_box
    from . import object_bounding_box

import bpy


class INFO_MT_mesh_boundbox_add(bpy.types.Menu):
    # Define the "Ice" menu
    bl_idname = "INFO_MT_mesh_boundbox_add"
    bl_label = "Bound Box Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.boundbox_add",
                        text="Bound Box Add")
        layout.operator("mesh.multi_boundbox_add",
                        text="Multi Bound Box Add")
        layout.operator("object.min_bounds",
                        text="Minimum Bounds")

# Define "Extras" menu


def menu_func(self, context):
    self.layout.separator()
    self.layout.menu("INFO_MT_mesh_boundbox_add", text="Bound Box", icon="LATTICE_DATA")


def register():
    bpy.utils.register_module(__name__)

    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    # Remove "Extras" menu from the "Add Mesh" menu.
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
