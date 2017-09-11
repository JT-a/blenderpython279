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

# bl_info = {
#    "name": "Workstation Pivot",
#    "author": "mkbreuer",
#    "version": (0, 1, 0),
#    "blender": (2, 76, 0),
#    "location": "View3D > Toolbar > Panel",
#    "warning": "",
#    "description": "Pivot Operator for the Main Panel",
#    "wiki_url": "",
#    "category": ""Workstation",
#}


import bpy
from bpy import*


# Menus Pivot  #######-------------------------------------------------------

class PivotType(bpy.types.Menu):
    """Pivot Type"""
    bl_label = "Pivot Type"
    bl_idname = "wkst.pivottype"

    def draw(self, context):
        layout = self.layout

        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("view3d.pivot_bounding_box", "Bounding Box", icon="ROTATE")
        layout.operator("view3d.pivot_median", "Median", icon="ROTATECENTER")
        layout.operator("view3d.pivot_3d_cursor", "3D Cursor", icon="CURSOR")
        layout.operator("view3d.pivot_active", "Active", icon="ROTACTIVE")
        layout.operator("view3d.pivot_individual", "Individual", icon="ROTATECOLLECTION")

bpy.utils.register_class(PivotType)


class PivotOrient(bpy.types.Menu):
    """Pivot Orientation"""
    bl_label = "Pivot Orientation"
    bl_idname = "wkst.pivotorient"

    def draw(self, context):
        layout = self.layout

        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("space.global", "Global")
        layout.operator("space.local", "Local")
        layout.operator("space.normal", "Normal")
        layout.operator("space.gimbal", "Gimbal")
        layout.operator("space.view", "View")

bpy.utils.register_class(PivotOrient)


#####  Pivot Point  ############################################################################################

class pivotBox(bpy.types.Operator):
    """Set pivot point to Bounding Box"""
    bl_label = "Set pivot point to Bounding Box"
    bl_idname = "view3d.pivot_bounding_box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
        return {"FINISHED"}


class pivotCursor(bpy.types.Operator):
    """Set pivot point to 3D Cursor"""
    bl_label = "Set pivot point to 3D Cursor"
    bl_idname = "view3d.pivot_3d_cursor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.pivot_point = 'CURSOR'
        return {"FINISHED"}


class pivotMedian(bpy.types.Operator):
    """Set pivot point to Median Point"""
    bl_label = "Set pivot point to Median Point"
    bl_idname = "view3d.pivot_median"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
        return {"FINISHED"}


class pivotActive(bpy.types.Operator):
    """Set pivot point to Active"""
    bl_label = "Set pivot point to Active"
    bl_idname = "view3d.pivot_active"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
        return {"FINISHED"}


class pivotIndividual(bpy.types.Operator):
    """Set pivot point to Individual"""
    bl_label = "Set pivot point to Individual Point"
    bl_idname = "view3d.pivot_individual"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        return {"FINISHED"}


class pivotCursor3d(bpy.types.Operator):
    """place the origin between all selected with 3d cursor"""
    bl_label = "Set origin between selected with 3d cursor"
    bl_idname = "view3d.origin_3dcursor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.space_data.pivot_point = 'CURSOR'

        return {"FINISHED"}


class pivotCursor3d2(bpy.types.Operator):
    """place the origin of the active to cursor with 3d cursor"""
    bl_label = "place the origin to cursor with 3d cursor"
    bl_idname = "view3d.origin_3dcursor2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.space_data.pivot_point = 'CURSOR'

        return {"FINISHED"}


class pivotCursor3d3(bpy.types.Operator):
    """origin to geometry with median pivot"""
    bl_label = "origin to geometry"
    bl_idname = "view3d.origin_3dcursor3"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'

        return {"FINISHED"}


# registering and menu integration
def register():

    bpy.utils.register_module(__name__)


# unregistering and removing menus
def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
