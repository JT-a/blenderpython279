
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


#######  Menus  ###################

class WKST_CopyDupli(bpy.types.Menu):
    """Duplicate Tools"""
    bl_label = "Copy"
    bl_idname = "wkst.copy_dupli"

    def draw(self, context):
        layout = self.layout

        if context.mode == 'OBJECT':

            layout.operator("object.duplicate_move", "Duplicate", icon="MOD_ARRAY")
            layout.operator("object.duplicate_move_linked", "Duplicate Linked")

            layout.separator()

            layout.operator("mft.radialclone", text="Radial Clone", icon="FILE_REFRESH")
            layout.operator("object.simplearewo", text="Replicator", icon="NEXT_KEYFRAME")
            layout.operator("object.cursor_array", text="Copy 2 Cursor", icon="NEXT_KEYFRAME")

            layout.separator()

            layout.operator("object.copy_selected_modifiers", text="Copy Modifier", icon="PASTEFLIPDOWN")
            layout.operator("switch.mod_display", "Copy Modifier Display", icon="PASTEFLIPDOWN")

        elif context.mode == 'EDIT_MESH':

            layout.operator("mesh.duplicate_move", "Duplicate", icon="MOD_ARRAY")

            layout.operator("object.cursor_array", text="Copy 2 Cursor", icon="FORCE_FORCE")


class WKST_CopyLink(bpy.types.Menu):
    """Instance Tools"""
    bl_label = "Instance"
    bl_idname = "wkst.copy_link"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.make_links_data", "Set Instance", icon="LINKED").type = 'OBDATA'
        layout.operator("object.makesingle", "Clear Instance", icon="UNLINKED")


class WKST_CopyLink_Data(bpy.types.Menu):
    """Link Data Tools"""
    bl_label = "Link Data"
    bl_idname = "wkst.copy_links_data"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.select_linked", text="Select Linked", icon="RESTRICT_SELECT_OFF")
        layout.operator_menu_enum("object.make_links_data", "type", " Make Links Data", icon="CONSTRAINT")


#######  Operator  ##################

class MakeSingle(bpy.types.Operator):
    """Make Single User for all Linked (Object Data)"""
    bl_idname = "object.makesingle"
    bl_label = "Make Single"

    def execute(self, context):
        bpy.ops.object.select_linked(type='OBDATA')
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)
        return {'FINISHED'}


class Copy2Cursor(bpy.types.Operator):
    """Copy selected object to cursor direction"""
    bl_idname = "object.cursor_array"
    bl_label = "Copy 2 Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active

        for i in range(self.total):
            obj_new = obj.copy()
            scene.objects.link(obj_new)

            factor = i / self.total
            obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

        return {'FINISHED'}


###### Register #######################

def register():
    bpy.utils.register_class(MakeSingle)
    bpy.utils.register_class(Copy2Cursor)
    bpy.utils.register_class(WKST_CopyDupli)
    bpy.utils.register_class(WKST_CopyLink)
    bpy.utils.register_class(WKST_CopyLink_Data)


def unregister():
    bpy.utils.unregister_class(MakeSingle)
    bpy.utils.unregister_class(Copy2Cursor)
    bpy.utils.unregister_class(WKST_CopyDupli)
    bpy.utils.unregister_class(WKST_CopyLink)
    bpy.utils.unregister_class(WKST_CopyLink_Data)

if __name__ == "__main__":
    register()
