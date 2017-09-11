#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#
# ***** END GPL LICENCE BLOCK *****


import bpy
from bpy import*


###########  Menu  #######################
class DecimateFreeze_Menu(bpy.types.Menu):
    """Decimate Freeze"""
    bl_label = "Decimate Freeze"
    bl_idname = "object.decimatefreeze_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("boolean.freeze", text="Freeze")
        layout.operator("boolean.unfreeze", text="Unfreeze")


class BooleanOpsMenu(bpy.types.Menu):
    """Booleans"""
    bl_label = "Booleans"
    bl_idname = "object.boolean_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        if context.mode == 'OBJECT':

            layout.operator("object.join", text="Join", icon="FULLSCREEN_EXIT")

            union = layout.operator("mesh.boolean", "Union", icon='ZOOMIN')
            union.modOp = 'UNION'

            intersect = layout.operator("mesh.boolean", "Intersect", icon='PANEL_CLOSE')
            intersect.modOp = 'INTERSECT'

            difference = layout.operator("mesh.boolean", "Difference", icon='ZOOMOUT')
            difference.modOp = 'DIFFERENCE'

            layout.separator()

            layout.operator("boolean.clone", text="Clone")
            layout.operator("boolean.separate", text="Separate")

        else:
            layout.operator("mesh.intersect", "Intersect: Union", icon='ZOOMIN').use_separate = False
            layout.operator("mesh.intersect", "Intersect: Separate", icon='ZOOMOUT').use_separate = True


class GPencil_Menu(bpy.types.Menu):
    """GPencil_Menu"""
    bl_label = "GPencil_Menu"
    bl_idname = "draw.gpencil_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        if context.mode == 'OBJECT':
            layout.operator("grease.execution", text="Grease Cut", icon='SCULPTMODE_HLT')

        else:
            layout.operator("mesh.looptools_gstretch", "Gstretch Project", icon='SPHERECURVE')

        layout.separator()

        layout.operator("gpencil.draw", text="Line", icon="GREASEPENCIL").mode = 'DRAW_STRAIGHT'
        layout.operator("gpencil.draw", text="Draw", icon="BRUSH_DATA").mode = 'DRAW'
        layout.operator("gpencil.draw", text="Poly", icon="NOCURVE").mode = 'DRAW_POLY'
        layout.operator("gpencil.draw", text="Erase", icon="DISCLOSURE_TRI_DOWN").mode = 'ERASER'

        layout.separator()

        layout.prop(context.tool_settings, "grease_pencil_source", "")
        layout.prop(context.tool_settings, "use_grease_pencil_sessions", text="Continuous", icon="LOCKED")
        layout.prop(context.gpencil_data, "use_stroke_edit_mode", text="Enable Editing", icon='EDIT', toggle=True)

        layout.separator()

        layout.operator("boolean.purge_pencils", text='Purge Pencils', icon='PANEL_CLOSE')


class SCULPTOpsMenu(bpy.types.Menu):
    """Sculpt Edit Menu"""
    bl_label = "Sculpt Edit Menu"
    bl_idname = "sculpt.edit_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("sculpt.geometry_smooth", text="Smooth")
        layout.operator("sculpt.geometry_laplacian_smooth", text="Laplacian")

        layout.separator()

        layout.operator("sculpt.geometry_decimate", text="Decimate")
        layout.operator("sculpt.geometry_displace", text="Displace")

        layout.separator()

        layout.operator("sculpt.geometry_subdivide_faces", text="Subdiv")
        layout.operator("sculpt.geometry_subdivide_faces_smooth", text="Smoothdiv")

        layout.separator()

        layout.operator("sculpt.geometry_beautify_faces", text="Beautify")


############  REGISTER  #################

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
