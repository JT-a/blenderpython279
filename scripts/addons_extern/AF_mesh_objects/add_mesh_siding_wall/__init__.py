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
# Contributed to by
# #

bl_info = {
    "name": "Siding & Floor",
    "author": "Various",
    "version": (0, 1, 0),
    "blender": (2, 74, 0),
    "location": "View3D > Add > Mesh",
    "description": "Add Siding & Floor Types",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/Add_Mesh/Add_Extra",
    "category": "Add Mesh",
}

if "bpy" in locals():
    import importlib
    importlib.reload(add_mesh_drystone)
    importlib.reload(add_mesh_floor_planks)
    importlib.reload(add_mesh_plancher)
    importlib.reload(add_mesh_siding)


else:
    from . import add_mesh_drystone
    from . import add_mesh_floor_planks
    from . import add_mesh_plancher
    from . import add_mesh_siding

import bpy


class INFO_MT_mesh_floorwall_add(bpy.types.Menu):
    # Define the "Ice" menu
    bl_idname = "INFO_MT_mesh_floorwall_add"
    bl_label = "Floors & Walls"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_add_siding",
                        text="Siding")
        layout.operator("mesh.drystone",
                        text="Drystone")
        layout.operator("mesh.floor_boards_add",
                        text="Floor Boards")
        layout.operator("mesh.ajout_primitive",
                        text="Plancher")

# Register all operators and panels

# Define "Extras" menu


def menu_func(self, context):
    self.layout.menu("INFO_MT_mesh_floorwall_add", text="Floors & Walls", icon="UV_ISLANDSEL")


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
