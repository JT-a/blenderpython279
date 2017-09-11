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
    "name": "Vertex Group Cleaner",
    "author": "IRIE Shinsuke",
    "version": (0, 5),
    "blender": (2, 65, 0),
    "location": "View3D > Tool Shelf > VGroup Cleaner",
    "description": "Clean vertex groups or delete empty vertex groups in selected objects",
    "tracker_url": "https://github.com/iRi-E/blender_vgroup_cleaner/issues",
    "category": "Mesh"}

import bpy
import re


# clean vertex groups
def zero_verts(obj, grp, th):
    ids = []

    for v in obj.data.vertices:
        try:
            if grp.weight(v.index) <= th:
                ids.append(v.index)
        except RuntimeError:
            pass

    return ids


def remove_verts(obj, grp, ctx):
    ids = zero_verts(obj, grp, ctx.scene.VGCThreshold)

    if ids:
        print("remove %d vertices from vertex group %s" % (len(ids), grp.name))
        grp.remove(ids)

        # toggle edit mode, to force correct drawing
        bpy.ops.object.mode_set(mode="EDIT", toggle=True)
        bpy.ops.object.mode_set(mode="EDIT", toggle=True)


class CleanActiveVgroup(bpy.types.Operator):
    """Remove vertices with weight=0 from active vertex group in active object"""
    bl_idname = "vgroup_cleaner.clean_active_vgroup"
    bl_label = "Clean Active Vertex Group"

    def execute(self, context):
        obj = context.active_object
        if obj in context.selected_objects:
            print("Object %s:" % obj.name)
            idx = obj.vertex_groups.active_index
            if idx >= 0:
                remove_verts(obj, obj.vertex_groups[idx], context)
        return {'FINISHED'}


class CleanAllVgroups(bpy.types.Operator):
    """Remove vertices with weight=0 from all vertex groups in all selected objects"""
    bl_idname = "vgroup_cleaner.clean_all_vgroups"
    bl_label = "Clean Vertex Groups"

    def execute(self, context):
        for obj in context.selected_objects:
            print("Object %s:" % obj.name)
            for grp in obj.vertex_groups:
                remove_verts(obj, grp, context)
        return {'FINISHED'}


# delete vertex groups
def is_empty(obj, grp):
    for v in obj.data.vertices:
        try:
            grp.weight(v.index)
            return False
        except RuntimeError:
            pass

    return True


def remove_vgrp(obj, grp):
    print("delete vertex group %s" % grp.name)
    obj.vertex_groups.remove(grp)


class DeleteEmptyVgroups(bpy.types.Operator):
    """Delete empty vertex groups in selected objects"""
    bl_idname = "vgroup_cleaner.delete_empty_vgroups"
    bl_label = "Delete Empty Vertex Groups"

    def execute(self, context):
        re_L = re.compile("^(.+[._])L(\.\d+)?$")
        re_R = re.compile("^(.+[._])R(\.\d+)?$")

        for obj in context.selected_objects:
            print("Object %s:" % obj.name)
            grps_LR = {}

            for grp in obj.vertex_groups:
                m = re_L.match(grp.name)
                if m or re_R.match(grp.name):

                    if m:
                        name_R = m.group(1) + "R" + (m.group(2) or "")
                    else:
                        name_R = grp.name

                    if name_R in grps_LR:
                        if is_empty(obj, grp) and is_empty(obj, grps_LR[name_R]):
                            remove_vgrp(obj, grp)
                            remove_vgrp(obj, grps_LR[name_R])
                        del grps_LR[name_R]
                    else:
                        grps_LR[name_R] = grp

                elif is_empty(obj, grp):
                    remove_vgrp(obj, grp)

            for grp in grps_LR.values():
                if is_empty(obj, grp):
                    remove_vgrp(obj, grp)

        return {'FINISHED'}


# clear vertex groups assigned to selected pose bones
class ClearBoneWeights(bpy.types.Operator):
    """Remove selected vertices from vertex groups assigned to selected pose bones"""
    bl_idname = "vgroup_cleaner.clear_bone_weights"
    bl_label = "Clear Bone Weights"

    def execute(self, context):
        obj = context.object
        parent = obj.parent
        mode = context.mode
        if mode in ["EDIT_MESH", "PAINT_WEIGHT"] and parent and parent.type == "ARMATURE":
            print("Object %s:" % obj.name)
            mesh = obj.data

            if mode == "EDIT_MESH":
                bpy.ops.object.mode_set(mode="EDIT", toggle=True)

            for grp in obj.vertex_groups:
                for bone in parent.pose.bones:
                    if bone.bone.select and grp.name == bone.name:
                        if mode == "EDIT_MESH" or mesh.use_paint_mask or mesh.use_paint_mask_vertex:
                            igrp = grp.index
                            ids = [v.index for v in mesh.vertices if v.select for g in v.groups if g.group == igrp]
                        else:
                            ids = [v.index for v in mesh.vertices]

                        if ids:
                            print("remove %d vertices from vertex group %s" % (len(ids), grp.name))
                            grp.remove(ids)

            bpy.ops.object.mode_set(mode="EDIT", toggle=True)

            if mode == "PAINT_WEIGHT":
                bpy.ops.object.mode_set(mode="EDIT", toggle=True)

        return {'FINISHED'}


# main class
class VGroupCleanerPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_label = "VGroup Cleaner"
    bl_context = "mesh_edit"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return not context.edit_object or context.mode == "EDIT_MESH"

    def draw(self, context):
        layout = self.layout

        if not context.edit_object:
            col = layout.column(align=True)
            col.operator("vgroup_cleaner.clean_active_vgroup", text="Clean Active VGroup")
            col.operator("vgroup_cleaner.clean_all_vgroups", text="Clean All VGroups")
            col.prop(context.scene, "VGCThreshold")

            col = layout.column()
            col.operator("vgroup_cleaner.delete_empty_vgroups", text="Delete Empty VGroups")

        if context.mode in ["EDIT_MESH", "PAINT_WEIGHT"]:
            col = layout.column()
            parent = context.object.parent
            col.active = parent is not None and parent.type == "ARMATURE"
            col.operator("vgroup_cleaner.clear_bone_weights", text="Clear Bone Weights")


# register the class
def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.VGCThreshold = bpy.props.FloatProperty(
        name="Threshold",
        description="Maximum value of vertex weight that vertices will be removed from vertex group",
        min=0.0,
        max=1.0,
        default=0.000999)


def unregister():
    del bpy.types.Scene.VGCThreshold

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
