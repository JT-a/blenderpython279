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
    "name": "Display Vertex Group Menu",
    "author": "Multiple Authors, mkbreuer",
    "version": (0, 1, 0),
    "blender": (2, 7, 2),
    "location": "View3D",
    "description": "[<] Vertex Group for Selection / Editing / Pinning / Weight / etc.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Display"}


import bpy
from bpy import *


######  Main Menu  ##############################

class VIEW3D_WKST_VertexGroupMenu(bpy.types.Menu):
    """Vertex Group Menu"""
    bl_label = "Vertex Group Menu"
    bl_idname = "wkst_menu.vertex_group"

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.prop(context.object, "vertex_groups", icon="INFO")
        layout.prop(context.object.vertex_groups, "active_index")

        if context.mode == 'EDIT_MESH':

            layout.separator()

            layout.operator("object.vertex_group_select", text="Select Group", icon="RESTRICT_SELECT_OFF")
            layout.operator("object.vertex_group_deselect", text="Deselect Group", icon="RESTRICT_SELECT_ON")

            layout.separator()

            layout.operator("object.vertex_group_assign", text="Assign to Group", icon="DISCLOSURE_TRI_RIGHT")
            layout.operator("object.vertex_group_remove_from", text="Remove from Group", icon="DISCLOSURE_TRI_DOWN")

        layout.separator()

        layout.operator("object.vertex_group_add", text="Add Vertex Group", icon='ZOOMIN')
        layout.operator("object.vertex_group_remove", text="Remove Vertex Group", icon='ZOOMOUT').all = False

        if context.mode == 'EDIT_MESH':

            layout.separator()

            layout.prop(context.tool_settings, "vertex_group_weight", text="Weight")

        layout.separator()

        layout.menu("MESH_MT_vertex_group_specials", icon='TRIA_RIGHT', text="Vertex Group Specials")

        # layout.separator()

        #layout.operator("object.vertex_group_move", icon='TRIA_UP', text="Index UP").direction = 'UP'
        #layout.operator("object.vertex_group_move", icon='TRIA_DOWN', text="Index DOWN").direction = 'DOWN'


######  Registry  #######################################

def register():

    bpy.utils.register_class(VIEW3D_WKST_VertexGroupMenu)

    # bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_class(VIEW3D_WKST_VertexGroupMenu)

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
