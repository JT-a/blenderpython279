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
#    "name": "Workstation Origin",
#    "author": "mkbreuer",
#    "version": (0, 1, 0),
#    "blender": (2, 76, 0),
#    "location": "View3D > Toolbar > Panel",
#    "warning": "",
#    "description": "Origin Operator for the Main Panel",
#    "wiki_url": "",
#    "category": ""Workstation",
#}


import bpy
from bpy import*


# Menus Origin  #######-------------------------------------------------------

class OriginRetopoMenu(bpy.types.Menu):
    """Origin Retopo Menu"""
    bl_label = "Origin Retopo Menu"
    bl_idname = "origin.retopo_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.label("Object Origin")

        layout.operator("mesh.emptyroom_cen", text="-> Center", icon='LAYER_ACTIVE')
        layout.operator("mesh.emptyroom_sel", text="-> Selected", icon='LAYER_ACTIVE')
        layout.operator("mesh.emptyxroom_cen", text="-> Center mirrored", icon='MOD_MIRROR')
        layout.operator("mesh.emptyxroom_sel", text="-> Selected mirrored", icon='MOD_MIRROR')


bpy.utils.register_class(OriginRetopoMenu)


class OriginSetupMenu_obm(bpy.types.Menu):
    """Origin Setup Menu"""
    bl_label = "Origin Setup Menu"
    bl_idname = "origin.setupmenu_obm"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.label("Origin to...", icon="LAYER_ACTIVE")

        layout.operator("object.origin_set", text="to Geometry").type = 'ORIGIN_GEOMETRY'
        layout.operator("object.origin_set", text="to 3D Cursor").type = 'ORIGIN_CURSOR'
        layout.operator("object.origin_set", text="to Center of Mass").type = 'ORIGIN_CENTER_OF_MASS'

        layout.separator()

        layout.operator("object.origin_set", text="Geometry to Origin").type = 'GEOMETRY_ORIGIN'

        layout.separator()

        layout.label("Bounding Box Origin", icon="LAYER_ACTIVE")
        layout.menu("object.bbox_origin_side_menu", "Side", icon="FACESEL")
        layout.menu("object.bbox_origin_edge_menu", "Edge", icon="EDGESEL")
        layout.menu("object.bbox_origin_corner_menu", "Corner", icon="VERTEXSEL")


bpy.utils.register_class(OriginSetupMenu_obm)


class OriginSetupMenu_edm(bpy.types.Menu):
    """Origin Setup Menu"""
    bl_label = "Origin Setup Menu"
    bl_idname = "origin.setupmenu_edm"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.label("Origin to Selected", icon="RESTRICT_SELECT_OFF")

        layout.operator("object.originedm", "to Editmode")
        layout.operator("object.originobm", "to Objectmode")


bpy.utils.register_class(OriginSetupMenu_edm)


class OriginSetupMenu_all_edm(bpy.types.Menu):
    """Origin Setup Menu"""
    bl_label = "Origin Setup Menu"
    bl_idname = "origin.setupmenu_alledm"

    def draw(self, context):
        layout = self.layout

        layout.label("Set Origin to Selected", icon="LAYER_ACTIVE")

        layout.operator("object.originedm", "to Editmode")
        layout.operator("object.originobm", "to Objectmode")

bpy.utils.register_class(OriginSetupMenu_all_edm)


######  set Origin  ##################################################################################

class OriginObm(bpy.types.Operator):
    """set origin to selected / stay in objectmode"""
    bl_idname = "object.originobm"
    bl_label = "origin to selected / in objectmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

bpy.utils.register_class(OriginObm)


class OriginEdm(bpy.types.Operator):
    """set origin to selected / stay in editmode"""
    bl_idname = "object.originedm"
    bl_label = "origin to selected in editmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

bpy.utils.register_class(OriginEdm)


# Origin  #######-------------------------------------------------------

class Origin_OBM(bpy.types.Operator):
    """set origin to selected / objectmode"""
    bl_idname = "object.origin_obm"
    bl_label = "origin to selected / in objectmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class OriginEDM(bpy.types.Operator):
    """set origin to selected / editmode / tip: change for local rotation"""
    bl_idname = "object.origin_edm"
    bl_label = "origin to selected in editmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class OriginObm(bpy.types.Operator):
    """set origin to selected / stay in objectmode"""
    bl_idname = "object.originobm"
    bl_label = "origin to selected / in objectmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class OriginEdm(bpy.types.Operator):
    """set origin to selected / stay in editmode"""
    bl_idname = "object.originedm"
    bl_label = "origin to selected in editmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class OriginSetupMenu_edm(bpy.types.Menu):
    """Origin: Set to Selection & Set to BBox in Editmode / Objectmode"""
    bl_label = "Origin Setup Menu"
    bl_idname = "originsetupmenu_edm"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.label("to Selected...", icon="RESTRICT_SELECT_OFF")

        layout.operator("object.originedm", "in Editmode")
        layout.operator("object.originobm", "in Objectmode")


# registering and menu integration
def register():

    bpy.utils.register_module(__name__)


# unregistering and removing menus
def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
