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
### Import different UI ###
from ..layouts.mesh_brush.mesh_brush_ui import draw_mesh_brush_ui
from ..layouts.shrinkwrap.shrinkwrap_ui import draw_shrinkwrap_ui
from ..layouts.surface_constraint.surface_constraint_ui import (draw_surface_constraint_ui)
from ..layouts.smooth_vertices.smooth_vertices_ui import (draw_smooth_vertices_ui)
from ..layouts.retopo_object.retopo_object_ui import (draw_retopo_object_ui)
from ..layouts.retopo_edit.retopo_edit_ui import (draw_retopo_edit_ui)
from ..layouts.retopo_sculpt.retopo_sculpt_ui import (draw_retopo_sculpt_ui)
from ..layouts.retopo_lattice.retopo_lattice_ui import (draw_retopo_lattice_ui)
from ..layouts.retopo_curve.retopo_curve_ui import (draw_retopo_curve_ui)


def draw_A_history_tools(layout):

    box = layout.box().column(1)
    row = box.row(1)
    row.operator('wm.path_open', text='', icon='FILESEL').filepath = "C:\\Users\Public\Documents"
    row.operator("view3d.ruler", text="Ruler")
    row.operator("ed.undo_history", text="History")
    row.operator("ed.undo", text="", icon="LOOP_BACK")
    row.operator("ed.redo", text="", icon="LOOP_FORWARDS")


### Panel ###
class SurfaceConstraintToolsPanel(bpy.types.Panel):
    bl_category = "SFC Retopo"
    bl_idname = "VIEW3D_PT_surface_constraint_tools"
    bl_label = "SFC Retopo"  # "Surface Constraint Tools Ext."
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom"

    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_CURVE', 'EDIT_MESH', 'OBJECT', 'EDIT_LATTICE', 'SCULPT'}

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'


###-----### Objectmode Panel ###
        if context.mode == 'OBJECT':

            # 1 #
            draw_retopo_object_ui(self, context, layout)

            # 2 #

            obj = context.active_object
            if obj:
                obj_type = obj.type

                if obj_type in {'MESH'}:
                    draw_surface_constraint_ui(layout)

            obj = context.active_object
            if obj:
                obj_type = obj.type
                ###space###
                if obj_type in {'MESH'}:
                    ###space###
                    box = layout.box().column(1)
                    row = box.row(1)
                    row.operator("object.convert", text="Convert to Curve", icon="CURVE_DATA").target = "CURVE"

                    row = box.row(1)
                    row.prop(bpy.context.scene, "Preserve_Location_Rotation_Scale", "", icon="NDOF_DOM")
                    row.operator("objects.multiedit_enter_operator", icon="GROUP")

                if obj_type in {'CURVE'}:
                    box = layout.box().column(1)

                    row = box.row(1)
                    row.prop(context.object.data, "dimensions", expand=True)

                    row = box.row(1)
                    row.operator("object.convert", text="Convert to Mesh", icon="OUTLINER_DATA_MESH").target = "MESH"


###-----### Editmode Panel ###
        if context.mode == 'EDIT_MESH':

            # 1 #
            draw_retopo_edit_ui(self, context, layout)

            # 2 #
            draw_shrinkwrap_ui(layout)

            # 3 #
            draw_smooth_vertices_ui(layout)

            # 4 #
            draw_mesh_brush_ui(layout)

            # 5 #
            draw_surface_constraint_ui(layout)

            box = layout.box()
            row = box.row(1)
            row.prop(bpy.context.scene, "Preserve_Location_Rotation_Scale", "", icon="NDOF_DOM")
            row.operator("objects.multiedit_exit_operator", icon="GROUP")


###-----### Curvemode Panel ###
        if context.mode == 'EDIT_CURVE':

            # 1 #
            draw_retopo_curve_ui(self, context, layout)


###-----### LATTCIEmode Panel ###
        if context.mode == 'EDIT_LATTICE':

            # 1 #
            draw_retopo_lattice_ui(self, context, layout)


###-----### Sculptmode Panel ###
        if context.mode == 'SCULPT':

            # 1 #
            draw_retopo_sculpt_ui(self, context, layout)

        draw_A_history_tools(layout)
