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

# <pep8 compliant>

bl_info = {
    "name": "Dynamic Parent",
    "author": "Roman Volodin, roman.volodin@gmail.com - Eibriel, eibriel@eibriel.com",
    "version": (0, 15),
    "blender": (2, 67, 0),
    "location": "View3D > Tool Panel",
    "description": "Allows to create and disable an animated ChildOf constraint",
    "warning": "It's very first beta! The addon is in progress!",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animation"}

import bpy
import mathutils


def dp_keyframe_insert(obj):
    obj.keyframe_insert(data_path="location")
    if obj.rotation_mode == 'QUATERNION':
        obj.keyframe_insert(data_path="rotation_quaternion")
    elif obj.rotation_mode == 'AXIS_ANGLE':
        obj.keyframe_insert(data_path="rotation_axis_angle")
    else:
        obj.keyframe_insert(data_path="rotation_euler")
    obj.keyframe_insert(data_path="scale")


def dp_create_dynamic_parent_obj(context):
    obj = bpy.context.active_object
    scn = bpy.context.scene
    current_frame = scn.frame_current
    list_selected_obj = bpy.context.selected_objects

    if len(list_selected_obj) == 2:
        i = list_selected_obj.index(obj)
        list_selected_obj.pop(i)
        parent_obj = list_selected_obj[0]
    else:
        return False
        # print("Warning! 2 objects must be selected")

    dp_keyframe_insert(obj)
    bpy.ops.object.constraint_add_with_targets(type='CHILD_OF')
    last_constraint = obj.constraints[-1]

    if parent_obj.type == 'ARMATURE':
        last_constraint.subtarget = parent_obj.data.bones.active.name
        last_constraint.name = "DP_" + last_constraint.target.name + "." + last_constraint.subtarget
    else:
        last_constraint.name = "DP_" + last_constraint.target.name

    override = context.copy()
    override['constraint'] = bpy.context.active_pose_bone.constraints[last_constraint.name]
    bpy.ops.constraint.childof_set_inverse(override, constraint="" + last_constraint.name + "", owner='OBJECT')

    fcrv = obj.animation_data.action.fcurves.new(data_path='constraints["' + last_constraint.name + '"].influence')
    curr_frame = scn.frame_current
    scn.frame_current = curr_frame - 1
    obj.constraints[last_constraint.name].influence = 0
    obj.keyframe_insert(data_path='constraints["' + last_constraint.name + '"].influence')

    scn.frame_current = curr_frame
    obj.constraints[last_constraint.name].influence = 1
    obj.keyframe_insert(data_path='constraints["' + last_constraint.name + '"].influence')

    return True


def dp_create_dynamic_parent_pbone(context):
    obj_obj = bpy.context.active_object
    obj = bpy.context.active_pose_bone
    scn = bpy.context.scene
    current_frame = scn.frame_current
    list_selected_obj = bpy.context.selected_objects

    if len(list_selected_obj) == 2:
        i = list_selected_obj.index(obj_obj)
        list_selected_obj.pop(i)
        parent_obj = list_selected_obj[0]
    else:
        return False
        # print("Warning! 2 objects must be selected")

    dp_keyframe_insert(obj)
    bpy.ops.pose.constraint_add_with_targets(type='CHILD_OF')
    last_constraint = obj.constraints[-1]

    if parent_obj.type == 'ARMATURE':
        last_constraint.subtarget = parent_obj.data.bones.active.name
        last_constraint.name = "DP_" + last_constraint.target.name + "." + last_constraint.subtarget
    else:
        last_constraint.name = "DP_" + last_constraint.target.name

    override = context.copy()
    override['constraint'] = bpy.context.active_pose_bone.constraints[last_constraint.name]
    bpy.ops.constraint.childof_set_inverse(override, constraint="" + last_constraint.name + "", owner='BONE')

    fcrv = obj_obj.animation_data.action.fcurves.new(data_path='constraints["' + last_constraint.name + '"].influence')
    curr_frame = scn.frame_current
    scn.frame_current = curr_frame - 1
    obj.constraints[last_constraint.name].influence = 0
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].constraints["' + last_constraint.name + '"].influence')

    scn.frame_current = curr_frame
    obj.constraints[last_constraint.name].influence = 1
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].constraints["' + last_constraint.name + '"].influence')

    return True


def dp_disable_dynamic_parent_obj():
    obj = bpy.context.active_object
    scn = bpy.context.scene
    current_frame = scn.frame_current
    last_constraint = obj.constraints[-1]

    for fcrv in obj.animation_data.action.fcurves:
        if fcrv.data_path == "constraints[" + last_constraint.name + "].influence":
            fcurve = fcrv

    curr_frame = scn.frame_current
    scn.frame_current = curr_frame - 1
    obj.constraints[last_constraint.name].influence = 1
    obj.keyframe_insert(data_path='constraints["' + last_constraint.name + '"].influence')

    scn.frame_current = curr_frame
    obj.constraints[last_constraint.name].influence = 0
    obj.keyframe_insert(data_path='constraints["' + last_constraint.name + '"].influence')

    loc_old = obj.location
    rot_old = obj.rotation_euler
    scale_old = obj.scale

    loc, rot, scale = obj.matrix_world.decompose()
    rot_euler = rot.to_euler()

    fcurves = obj.animation_data.action.fcurves

    curr_frame = scn.frame_current
    scn.frame_current = curr_frame - 1
    obj.keyframe_insert(data_path='location')
    obj.keyframe_insert(data_path='rotation_euler')
    obj.keyframe_insert(data_path='scale')

    scn.frame_current = curr_frame
    obj.location = loc
    obj.rotation_euler = rot_euler
    obj.scale = scale
    obj.keyframe_insert(data_path='location')
    obj.keyframe_insert(data_path='rotation_euler')
    obj.keyframe_insert(data_path='scale')

    return True


def dp_disable_dynamic_parent_pbone():
    obj_obj = bpy.context.active_object
    obj = bpy.context.active_pose_bone
    scn = bpy.context.scene
    current_frame = scn.frame_current
    last_constraint = obj.constraints[-1]

    for fcrv in obj_obj.animation_data.action.fcurves:
        if fcrv.data_path == 'pose.bones["' + obj.name + '"].constraints["' + last_constraint.name + '"].influence':
            fcurve = fcrv

    curr_frame = scn.frame_current
    scn.frame_current = curr_frame - 1
    obj.constraints[last_constraint.name].influence = 1
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].constraints["' + last_constraint.name + '"].influence')

    scn.frame_current = curr_frame
    obj.constraints[last_constraint.name].influence = 0
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].constraints["' + last_constraint.name + '"].influence')

    loc_old = obj.location
    rot_old = obj.rotation_quaternion
    scale_old = obj.scale

    final_matrix = obj.matrix * obj_obj.matrix_world

    fcurves = obj_obj.animation_data.action.fcurves

    curr_frame = scn.frame_current
    scn.frame_current = curr_frame - 1
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].location')
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].rotation_quaternion')
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].scale')

    scn.frame_current = curr_frame
    obj.matrix = final_matrix
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].location')
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].rotation_quaternion')
    obj_obj.keyframe_insert(data_path='pose.bones["' + obj.name + '"].scale')

    return True


class DpCreateConstraint(bpy.types.Operator):
    """Create a new animated Child Of constraint"""
    bl_idname = "dp.create"
    bl_label = "Create Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object

        if obj.type == 'ARMATURE':
            obj = bpy.context.active_pose_bone

            if len(obj.constraints) == 0:
                if not dp_create_dynamic_parent_pbone(context):
                    self.report({'ERROR'}, "Error parenting bones")
                    return {'CANCELLED'}
            else:
                if obj.constraints[-1].influence == 1:
                    dp_disable_dynamic_parent_pbone()
                if not dp_create_dynamic_parent_pbone(context):
                    self.report({'ERROR'}, "Error parenting bones")
                    return {'CANCELLED'}
        else:
            if len(obj.constraints) == 0:
                if not dp_create_dynamic_parent_obj(context):
                    self.report({'ERROR'}, "Error parenting objects")
                    return {'CANCELLED'}
            else:
                if obj.constraints[-1].influence == 1:
                    dp_disable_dynamic_parent_obj()
                if not dp_create_dynamic_parent_obj(context):
                    self.report({'ERROR'}, "Error parenting objects")
                    return {'CANCELLED'}

        return {'FINISHED'}


class DpDisableConstraint(bpy.types.Operator):
    """Disable the current animated Child Of constraint"""
    bl_idname = "dp.disable"
    bl_label = "Disable Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'ARMATURE':
            dp_disable_dynamic_parent_pbone()
        else:
            dp_disable_dynamic_parent_obj()
        return {'FINISHED'}


class DinamicParentUI(bpy.types.Panel):
    """User interface for Dynamic Parent addon"""
    bl_label = "Dynamic Parent"
    bl_idname = "dp.ui"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = 'Relate'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("dp.create", text="Create", icon="KEY_HLT")
        col.operator("dp.disable", text="Disable", icon="KEY_DEHLT")


def register():
    bpy.utils.register_class(DpCreateConstraint)
    bpy.utils.register_class(DpDisableConstraint)
    bpy.utils.register_class(DinamicParentUI)

    pass


def unregister():
    bpy.utils.unregister_class(DpCreateConstraint)
    bpy.utils.unregister_class(DpDisableConstraint)
    bpy.utils.unregister_class(DinamicParentUI)

    pass

if __name__ == "__main__":
    register()
