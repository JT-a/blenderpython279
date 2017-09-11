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
# Pontiac, Fourmadmen, varkenvarken, tuga3d, meta-androcto, metalliandy, dreampainter & cotejrp1#

bl_info = {
    "name": "AF: Edge Profiles",
    "author": "Meta-Androcto",
    "version": (0, 1),
    "blender": (2, 6, 4),
    "location": "View3D > Add > Mesh > Edge Profiles",
    "description": "Add Edge Profile types",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"
    "Scripts/",
    "tracker_url": "",
    "category": "Addon Factory"}


if "bpy" in locals():
    import imp
    imp.reload(add_mesh_bevel_1)
    imp.reload(add_mesh_bevel_2)
    imp.reload(add_mesh_car)
    imp.reload(add_mesh_cornice)
    imp.reload(add_mesh_double)
    imp.reload(add_mesh_inlay_1)
    imp.reload(add_mesh_inlay_2)
    imp.reload(add_mesh_inlay_3)
    imp.reload(add_mesh_norman)
    imp.reload(add_mesh_nose_1)
    imp.reload(add_mesh_nose_2)
    imp.reload(add_mesh_quad)
    imp.reload(add_mesh_round_50)
    imp.reload(add_mesh_round_75)
    imp.reload(add_mesh_round_100)
    imp.reload(add_mesh_round_up)
    imp.reload(add_mesh_shoe)
    imp.reload(add_mesh_smooth)
else:
    from . import add_mesh_bevel_1
    from . import add_mesh_bevel_2
    from . import add_mesh_car
    from . import add_mesh_cornice
    from . import add_mesh_double
    from . import add_mesh_inlay_1
    from . import add_mesh_inlay_2
    from . import add_mesh_inlay_3
    from . import add_mesh_norman
    from . import add_mesh_nose_1
    from . import add_mesh_nose_2
    from . import add_mesh_quad
    from . import add_mesh_round_50
    from . import add_mesh_round_75
    from . import add_mesh_round_100
    from . import add_mesh_round_up
    from . import add_mesh_shoe
    from . import add_mesh_smooth
import bpy


class INFO_MT_mesh_profiles_add(bpy.types.Menu):
    # Define the "Extras" menu
    bl_idname = "INFO_MT_mesh_profiles_add"
    bl_label = "Edge Profiles"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.bevel_1", text="Bevel_1")
        layout.operator("mesh.bevel_2", text="Bevel_2")
        layout.operator("mesh.car", text="Car")
        layout.operator("mesh.cornice", text="Cornice")
        layout.operator("mesh.double", text="Double")
        layout.operator("mesh.inlay_1", text="Inlay_1")
        layout.operator("mesh.inlay_2", text="Inlay_2")
        layout.operator("mesh.inlay_3", text="Inlay_3")
        layout.operator("mesh.norman", text="Norman")
        layout.operator("mesh.nose_1", text="Nose_1")
        layout.operator("mesh.nose_2", text="Nose_2")
        layout.operator("mesh.quad", text="Quad")
        layout.operator("mesh.round_50", text="round_50")
        layout.operator("mesh.round_75", text="round_75")
        layout.operator("mesh.round_100", text="round_100")
        layout.operator("mesh.round_up", text="round_up")
        layout.operator("mesh.shoe", text="Shoe")
        layout.operator("mesh.smooth", text="Smooth")
# Register all operators and panels

# Define "Extras" menu


def menu_func(self, context):
    self.layout.menu("INFO_MT_mesh_profiles_add", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)

    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)

    # Remove "Extras" menu from the "Add Mesh" menu.
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
