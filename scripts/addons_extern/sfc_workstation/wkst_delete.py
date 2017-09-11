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
import re
from bpy import *

#######  Delete Menus  #################


class VIEW3D_WKST_Delete(bpy.types.Menu):
    """Clear Scene & Data"""
    bl_label = "Delete"
    bl_idname = 'object.wkstdelete'

    def draw(self, context):
        layout = self.layout

        layout.operator("object.delete", icon="PANEL_CLOSE")
        layout.operator("ba.delete_scene_obs")

        layout.separator()

        layout.operator("mesh.removedouble", "Remove all Double", icon="PANEL_CLOSE")

        layout.separator()

        layout.operator("meshlint.select", "Meshlint > Mesh Data")

        layout.separator()

        scn = context.scene
        layout.operator("ba.delete_data_obs")
        layout.prop(scn, "mod_list", "")

        layout.separator()

        layout.operator("material.remove", text="Clear Materials")

        layout.separator()

        layout.menu("VIEW3D_MT_object_clear", text="Clear Location", icon='EMPTY_DATA')

        layout.separator()

        layout.menu("clearparent", text="Clear Parenting", icon='CONSTRAINT')
        layout.menu("cleartrack", text="Clear Tracking")
        layout.operator("object.constraints_clear", text="Clear Constraint")

        layout.separator()
        layout.operator("anim.keyframe_clear_v3d", text="Clear Keyframe", icon='KEY_DEHLT')
        layout.operator("object.game_property_clear")


bpy.utils.register_class(VIEW3D_WKST_Delete)


class CleanDelete(bpy.types.Menu):
    """Clean Up Mesh"""
    bl_label = "Clean Up & Delete Mesh"
    bl_idname = 'mesh.cleandelete'

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.delete", "Vertices", icon="SNAP_VERTEX").type = "VERT"
        layout.operator("mesh.dissolve_verts")
        layout.operator("mesh.remove_doubles")

        layout.separator()

        layout.operator("mesh.delete", "Edges", icon="SNAP_EDGE").type = "EDGE"
        layout.operator("mesh.dissolve_edges")
        layout.operator("mesh.delete_edgeloop", text="Remove Edge Loop")

        layout.separator()

        layout.operator("mesh.delete", "Faces", icon="SNAP_FACE").type = "FACE"
        layout.operator("mesh.dissolve_faces")
        layout.operator("mesh.delete", "Remove only Faces").type = "ONLY_FACE"

        layout.separator()

        layout.operator("mesh.dissolve_limited", icon="MATCUBE")
        layout.operator("mesh.dissolve_degenerate")
        layout.operator("mesh.delete", "Remove Edge & Faces").type = "EDGE_FACE"

        layout.separator()

        layout.operator("mesh.fill_holes", icon="RETOPO")
        layout.operator("mesh.delete_loose")
        layout.operator("mesh.edge_collapse")
        layout.operator("mesh.vert_connect_nonplanar")

        layout.separator()
        layout.operator("meshlint.select", "Meshlint > Mesh Data")


class ObjClearDelete(bpy.types.Menu):
    """Clear Menu"""
    bl_label = "Clear Menu"
    bl_idname = 'object.cleandelete'

    def draw(self, context):
        layout = self.layout

        layout.operator("object.hide_view_clear", text="Clear Hide")
        layout.operator("material.remove", text="Clear Materials")

        layout.separator()

        layout.menu("VIEW3D_MT_object_clear", text="Clear Location")
        layout.menu("clearparent", text="Clear Parenting")
        layout.menu("cleartrack", text="Clear Tracking")

        layout.separator()

        layout.operator("object.constraints_clear", text="Clear Constraint")
        layout.operator("anim.keyframe_clear_v3d", text="Clear Keyframe")
        layout.operator("object.game_property_clear")


#######  Operator ##################


class deleteMat(bpy.types.Operator):
    """delete materials with an value slider"""
    bl_idname = "material.remove"
    bl_label = "Delete all Material"
    bl_options = {'REGISTER', 'UNDO'}

    deleteMat = bpy.props.IntProperty(name="Delete all Material", description="How much?", default=100, min=1, soft_max=5000, step=1)

    def execute(self, context):
        for i in range(self.deleteMat):
            bpy.ops.object.material_slot_remove()
        return {'FINISHED'}


class GRP_Purge(bpy.types.Operator):
    """purge grease pencil layer"""
    bl_idname = "wkst_grp.purge"
    bl_label = "Purge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.gpencil.data_unlink()
        bpy.context.scene.mod_list = 'grease_pencil'
        bpy.ops.ba.delete_data_obs()

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator("material.remove", text="Delete All Material", icon='DISCLOSURE_TRI_DOWN')


# REGISTER / UNREGISTER

def register():
    bpy.utils.register_class(deleteMat)
    bpy.utils.register_module(__name__)
    bpy.types.MATERIAL_MT_specials.append(menu_func)


def unregister():
    bpy.utils.unregister_class(deleteMat)
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
