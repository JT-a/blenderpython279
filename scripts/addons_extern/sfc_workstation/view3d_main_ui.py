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

# <pep8-80 compliant>

import bpy
from bpy import*
### Import different UI ###

from wkst_workstation.view3d_curve_ui import (draw_wkst_curve_ui)
from wkst_workstation.view3d_lattice_ui import (draw_wkst_lattice_ui)
from wkst_workstation.view3d_object_ui import (draw_wkst_object_ui)
from wkst_workstation.view3d_sculpt_ui import (draw_wkst_sculpt_ui)
from wkst_workstation.view3d_edit_ui import (draw_wkst_edit_ui)


### Panel ###
class MKBToolsPanel(bpy.types.Panel):
    bl_category = "Tools+"
    bl_idname = "VIEW3D_PT_tools"
    bl_label = "Tools+"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_SURFACE', 'EDIT_CURVE', 'EDIT_MESH', 'OBJECT', 'EDIT_LATTICE', 'SCULPT'}

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'


###-----### Objectmode Panel ###
        if context.mode == 'OBJECT':

            # 1 #
            draw_wkst_object_ui(self, context, layout)

            # 2 #
            # draw_surface_constraint_ui(layout)


###-----### Editmode Panel ###
        if context.mode == 'EDIT_MESH':

            # 1 #
            draw_wkst_edit_ui(self, context, layout)

            # 2 #
            # draw_shrinkwrap_ui(layout)

            # 3 #
            # draw_smooth_vertices_ui(layout)

            # 4 #
            # draw_mesh_brush_ui(layout)

            # 5 #
            # draw_surface_constraint_ui(layout)


###-----### Curvemode Panel ###
        if context.mode == 'EDIT_CURVE':

            # 1 #
            draw_wkst_curve_ui(self, context, layout)


###-----### Latticemode Panel ###
        if context.mode == 'EDIT_LATTICE':

            # 1 #
            draw_wkst_lattice_ui(self, context, layout)


###-----### Sculptmode Panel ###
        if context.mode == 'SCULPT':

            # 1 #
            draw_wkst_sculpt_ui(self, context, layout)


def register():
    bpy.utils.register_class(MKBToolsPanel)


def unregister():
    bpy.utils.unregister_class(MKBToolsPanel)


if __name__ == "__main__":
    register()
