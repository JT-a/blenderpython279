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


# Hook  #######-------------------------------------------------------

class VIEW3D_MTK_Hook(bpy.types.Menu):
    """Hook Menu"""
    bl_label = "Hook"
    bl_idname = "wkst.vertices_hook"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text="Hook use Modifier")

        layout.operator("object.hook_add_newob", text="New", icon="HOOK")
        layout.operator("object.hook_add_selob", text="to Select").use_bone = False
        layout.operator("object.hook_add_selob", text="to Bone").use_bone = True

        layout.operator("object.hook_select", text="Select")
        layout.operator("object.hook_reset", text="Reset")
        layout.perator("object.hook_recenter", text="Recenter")

# bpy.utils.register_class(VIEW3D_MTK_Hook)

# Menus Relations  #######-------------------------------------------------------


class VIEW3D_MT_Relation_Menu(bpy.types.Menu):
    """Relation Menu"""
    bl_label = "Relation Menu"
    bl_idname = "wkst.relation_menu"

    def draw(self, context):
        layout = self.layout

        obj = context
        if obj and obj.mode == 'OBJECT':

            layout.menu("wkst_parent", icon="CONSTRAINT")
            layout.menu("wkst_group")
            layout.menu("wkst_constraint")

            layout.separator()

            layout.menu("VIEW3D_MT_make_links", text="M.Links", icon="LINKED")
            layout.menu("VIEW3D_MT_make_single_user", text="Single User")

            layout.separator()

            layout.operator("object.visual_transform_apply", icon="NDOF_DOM")

            layout.separator()

            layout.operator("object.duplicates_make_real")

            layout.separator()

            layout.operator("help.relation", text="make single from dupli", icon="INFO")

        obj = context
        if obj and obj.mode == 'EDIT_ARMATURE':
            layout.menu("VIEW3D_MT_edit_armature_parent", icon='CONSTRAINT')

        obj = context
        if obj and obj.mode == 'POSE':
            arm = context.active_object.data

            layout.menu("VIEW3D_MT_object_parent", icon='CONSTRAINT')
            layout.menu("VIEW3D_MT_pose_ik")
            layout.menu("VIEW3D_MT_pose_constraints")

bpy.utils.register_class(VIEW3D_MT_Relation_Menu)


class help_text(bpy.types.Operator):
    """Help Text"""
    bl_idname = "help.relation"
    bl_label = "Help Text"

    def draw(self, context):
        layout = self.layout
        layout.label('1. parent selected to activ')
        layout.label('2. apply Make Duplicates Real')
        layout.label('3. clear Parent / 4. to Join > selected Linked Object Data')

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=300, height=400)

bpy.utils.register_class(help_text)


# Menus Constraint  ######-------------------------------------

class VIEW3D_MT_Constraint_Menu(bpy.types.Menu):
    """Constraint Menu"""
    bl_label = "Constraint Menu"
    bl_idname = "wkst.constraint_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator_menu_enum("object.constraint_add", "type", text="  Constraint", icon="CONSTRAINT_DATA")
        #layout.operator("object.track_set",text=">>>  Track  <<<")

        layout.separator()

        layout.label(text="to Selected:", icon="LAYER_ACTIVE")
        layout.operator("track.to", text="-> Track To")
        layout.operator("damped.track", text="-> Damped Track")
        layout.operator("lock.track", text="-> Lock Track")

        layout.separator()

        layout.label(text="to CursorPos+Empty:", icon="LAYER_ACTIVE")
        layout.operator("track.toempty", text="-> Track To")
        layout.operator("damped.trackempty", text="-> Damped Track")
        layout.operator("lock.trackempty", text="-> Lock Track")

bpy.utils.register_class(VIEW3D_MT_Constraint_Menu)


# Menus Parent  ######-------------------------------------

class VIEW3D_MT_Parent_Menu(bpy.types.Menu):
    """Parent Menu"""
    bl_label = "Parent Menu"
    bl_idname = "wkst.parent_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.parent_set", text="Set")

        layout.separator()

        layout.operator("object.parent_clear").type = "CLEAR"
        layout.operator("object.parent_clear", text="Clear Inverse").type = "CLEAR_INVERSE"
        layout.operator("object.parent_clear", text="Clear Keep Transform").type = "CLEAR_KEEP_TRANSFORM"

bpy.utils.register_class(VIEW3D_MT_Parent_Menu)


# Menus Group  ######-------------------------------------

class VIEW3D_MT_Group_Menu(bpy.types.Menu):
    """Group Menu"""
    bl_label = "Group Menu"
    bl_idname = "wkst.group_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("group.create", text="Group")
        layout.operator("group.objects_add_active", text="-> to Active")

        layout.separator()

        layout.operator("group.objects_remove", text="Remove")
        layout.operator("group.objects_remove_active", text="-> from Active")

bpy.utils.register_class(VIEW3D_MT_Group_Menu)


############------------############
############  REGISTER  ############

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
