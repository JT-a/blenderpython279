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


import bpy
from bpy import*


class VIEW3D_WKST_Modifier(bpy.types.Menu):
    """Modifier Menu"""
    bl_label = "Modifier Menu"
    bl_idname = "wkst.modispace"
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator_menu_enum("object.modifier_add", "type", icon='MODIFIER')

        layout.menu("space_arraymodifier", icon='MOD_ARRAY')

        layout.menu("htk_modivisual", text="Visual Modifier", icon='RESTRICT_VIEW_OFF')

        layout.separator()

        layout.label(text="Subsurf-Level", icon='MOD_SUBSURF')

        layout.operator("view3d.modifiers_subsurf_level_0", text="0-Level")
        layout.operator("view3d.modifiers_subsurf_level_1", text="1-Level")
        layout.operator("view3d.modifiers_subsurf_level_2", text="2-Level")
        layout.operator("view3d.modifiers_subsurf_level_3", text="3-Level")
        layout.operator("view3d.modifiers_subsurf_level_4", text="4-Level")
        layout.operator("view3d.modifiers_subsurf_level_5", text="5-Level")
        layout.operator("view3d.modifiers_subsurf_level_6", text="6-Level")

        layout.separator()

        layout.operator("view3d.fullmirror", icon='MOD_MIRROR', text="Clip-Mirror X")
        layout.operator("view3d.fullmirrory", icon='MOD_MIRROR', text="Clip-Mirror Y")
        layout.operator("view3d.fullmirrorz", icon='MOD_MIRROR', text="Clip-Mirror Z")


class VIEW3D_WKST_MirrorCut_Menu(bpy.types.Menu):
    """MirrorCut Menu"""
    bl_label = "MirrorCut Menu"
    bl_idname = "wkst.mirrorcut"
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("object.automirror", text="Execute MirrorCut", icon="MOD_WIREFRAME")

        layout.separator()

        ###space###
        if context.mode == 'OBJECT':
            layout.label("Mesh Cut only", icon="TRIA_DOWN")

            layout.operator("modifier.positiv_x_cut_obm", text="+X")
            layout.operator("modifier.positiv_y_cut_obm", text="+Y")
            layout.operator("modifier.positiv_z_cut_obm", text="+Z")

            layout.operator("modifier.negativ_x_cut_obm", text="-X")
            layout.operator("modifier.negativ_y_cut_obm", text="-Y")
            layout.operator("modifier.negativ_z_cut_obm", text="-Z")

        ###space###
        if context.mode == 'EDIT_MESH':
            layout.label("Mesh Cut only", icon="TRIA_DOWN")

            layout.operator("modifier.positiv_x_cut", text="+X")
            layout.operator("modifier.positiv_y_cut", text="+Y")
            layout.operator("modifier.positiv_z_cut", text="+Z")

            layout.operator("modifier.negativ_x_cut", text="-X")
            layout.operator("modifier.negativ_y_cut", text="-Y")
            layout.operator("modifier.negativ_z_cut", text="-Z")


######------------##############################
######  Registry  ##############################

def register():

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
