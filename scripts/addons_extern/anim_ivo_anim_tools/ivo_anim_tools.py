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

#
#  Written by Ivo Grigull
#  http://ivogrigull.com
#  http://character-rigger.com
#

import bpy
import mathutils
from bpy.types import Operator, Panel


def refresh():
    bpy.context.scene.frame_current = bpy.context.scene.frame_current


def uniqifylist(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def deselect_all_posebones():
    ob = bpy.context.active_object
    for n in ob.pose.bones:
        n.bone.select = False


class deselect_all_bones(Operator):

    """Deselect all bones"""

    bl_idname = "object.deselect_bones"
    bl_label = "Deselect all bones"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        ob = context.active_object

        if ob.type == 'ARMATURE':
            for n in ob.data.bones:
                n.select = False

            ob.data.bones.active = None
            context.scene.frame_current = context.scene.frame_current

        return {'FINISHED'}


def select_posebone(bone):

    ob = bpy.context.active_object

    if isinstance(bone, bpy.types.PoseBone):
        bone = bone.bone  # get bone instead of posebone
    elif isinstance(bone, str):
        try:
            bone = ob.data.bones[bone]
        except:
            return

    deselect_all_posebones()
    bone.select = True
    ob.data.bones.active = bone


def select_opposite():

    posebone = bpy.context.active_pose_bone
    ob = posebone.id_data
    if posebone.name.find("_L") != -1:
        name = posebone.name.replace("_L", "_R")
    elif posebone.name.find("_R") != -1:
        name = posebone.name.replace("_R", "_L")
    else:
        return

    select_posebone(name)


def clean(fcurve):
    done = False
    points = fcurve.keyframe_points
    while not done:
        for n in range(len(points)):
            if n == len(points) - 1:
                done = True
                break

            if n > 0 and n < len(points) - 1:
                if points[n - 1].co[1] == points[n].co[1] and points[n + 1].co[1] == points[n].co[1]:
                    points.remove(points[n])
                    break


def clean_selected_objects_fcurves():

    ob = bpy.context.active_object

    dict = {}
    for n in ob.pose.bones:
        if n.bone.select:
            dict[n.name] = []

    for n in ob.animation_data.action.fcurves:
        for i in dict.keys():
            if n.data_path.find(i) != -1:
                clean(n)

    refresh()


def func_key_poses(context):

    ob = context.active_object

    dict = {}
    for n in ob.pose.bones:
        if n.bone.select:
            dict[n.name] = []

    fcurves = []

    for n in ob.animation_data.action.fcurves:
        for i in dict.keys():
            if n.data_path.find(i) != -1:
                fcurves.append(n)

    frames = []
    for n in fcurves:
        for i in n.keyframe_points:
            frame = int(i.co[0])
            if frame not in frames:
                frames.append(frame)

    # frames = uniqifylist(frames)

    # for n in ob.pose.bones:
    #     if n.bone.select:
    for i in frames:
        context.scene.frame_set(i)
        bpy.ops.anim.keyframe_insert()

    refresh()


class key_poses(Operator):

    """Key all bones in active keying set for each frame number that has a key"""

    bl_idname = "object.key_poses"
    bl_label = "key poses"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        func_key_poses(context)
        return {'FINISHED'}


class clean_curves(Operator):

    """Remove all redundant keyframes (flat parts in curves) of selected bones"""

    bl_idname = "object.clean_curves"
    bl_label = "Clean curves"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        clean_selected_objects_fcurves()
        return {'FINISHED'}


def func_deselect_all_bones(ob):
    for n in ob.data.bones:
        n.select = False


class remove_flat_curves(Operator):

    """Remove all flat fcurves (curves where all keys have same values)"""

    bl_idname = "object.remove_flat_curves"
    bl_label = "Remove flat curves"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.func_remove_flat_curves(context)
        refresh()
        return {'FINISHED'}

    def func_remove_flat_curves(self, context):
        ob = context.active_object

        bone_dict = {n.name: [] for n in ob.pose.bones if n.bone.select}

        curves_to_remove = []

        for n in ob.animation_data.action.fcurves:
            for i in bone_dict.keys():
                if n.data_path.find(i) != -1:
                    points = n.keyframe_points
                    previous = points[0].co[1]
                    remove = True
                    for i in points:
                        value = i.co[1]
                        if value != previous:
                            remove = False
                            break
                        previous = i.co[1]

                    if remove:
                        curves_to_remove.append(n)

        for n in curves_to_remove:
            try:
                ob.animation_data.action.fcurves.remove(n)
            except:
                print("curve %s not found" % n.data_path)


# Boomsmash (playblast) =======================================================

def blast(context):

    bpy.context.scene.render.file_format = 'AVI_JPEG'
    bpy.context.scene.render.use_stamp = True
    bpy.context.scene.render.use_stamp_frame = True
    only_render_before = bpy.context.area.active_space.show_only_render
    bpy.context.area.active_space.show_only_render = True

    bpy.ops.render.opengl(animation=True)
    bpy.ops.render.play_rendered_anim()

    bpy.context.area.active_space.show_only_render = only_render_before


class Playblast(Operator):

    """Make Playblast"""

    bl_idname = "play.blast"
    bl_label = "Playblast"

    def execute(self, context):
        blast(context)
        return {'FINISHED'}


class delete_current_frame(Operator):

    """Delete loc/rot/scale keys for selected bones"""

    bl_idname = "object.delete_current_frame"
    bl_label = "Delete keyframe"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        ob = context.active_object
        for n in ob.pose.bones:
            if n.bone.select:
                n.keyframe_delete('location')
                n.keyframe_delete('rotation_quaternion')
                n.keyframe_delete('rotation_euler')
                n.keyframe_delete('scale')
        f = context.scene.frame_current
        context.scene.frame_set(f)
        return {'FINISHED'}


S = 1 << 1
R = 1 << 2
T = 1 << 3


def add_to_ks(flags=S | R | T, array_index=-1):
    ob = bpy.context.active_object
    ks = bpy.context.scene.keying_sets.active

    for n in ob.pose.bones:
        if n.bone.select:
            path = n.path_from_id()

            if flags & S:
                line = path + ".scale"
                ks.paths.add(ob, line, array_index)
                if array_index == -1:
                    p = ks.paths[len(ks.paths) - 1]
                    p.use_entire_array = True

            if flags & R:
                if n.rotation_mode == 'QUATERNION':
                    line = path + ".rotation_quaternion"
                else:
                    line = path + ".rotation_euler"
                ks.paths.add(ob, line, array_index)
                if array_index == -1:
                    p = ks.paths[len(ks.paths) - 1]
                    p.use_entire_array = True

            if flags & T:
                line = path + ".location"
                ks.paths.add(ob, line, array_index)
                if array_index == -1:
                    p = ks.paths[len(ks.paths) - 1]
                    p.use_entire_array = True

            p = ks.paths[len(ks.paths) - 1]
            # p.insertkey_visual =True
            # p.insertkey_xyz_to_rgb = True
            p.bl_options = 'INSERTKEY_VISUAL'


class add_pos_to_keying_set(Operator):

    """Adds all selected bone-locations to active keying set"""

    bl_idname = "object.add_pos_to_keying_set"
    bl_label = "Loc to Keying-set"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        add_to_ks(T)
        return {'FINISHED'}


class add_rot_to_keying_set(Operator):

    """Adds all selected bone-rotations to active keying set"""

    bl_idname = "object.add_rot_to_keying_set"
    bl_label = "Rot to Keying-set"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        add_to_ks(R)
        return {'FINISHED'}


class add_scl_to_keying_set(Operator):

    """Adds all selected bone-scales to active keying set"""

    bl_idname = "object.add_scl_to_keying_set"
    bl_label = "Scl to Keying-set"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        add_to_ks(S)
        return {'FINISHED'}


class add_SRT_to_keying_set(Operator):

    """Adds all selected bone transforms to active keying set"""

    bl_idname = "object.add_srt_to_keying_set"
    bl_label = "SRT to Keying-set"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        add_to_ks(S | R | T)
        return {'FINISHED'}


class jump_first_frame(Operator):

    """"""

    bl_idname = "scene.jump_first_frame"
    bl_label = "Jump to first frame"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        context.scene.frame_set(context.scene.frame_start)
        return {'FINISHED'}


class jump_last_frame(Operator):

    """"""

    bl_idname = "scene.jump_last_frame"
    bl_label = "Jump to last frame"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        context.scene.frame_set(context.scene.frame_end)
        return {'FINISHED'}


# Key Bones ===================================================================

class bone_key_loc(Operator):

    """Insert location key for all selected bones"""

    bl_idname = "object.bone_key_loc"
    bl_label = "Key Loc"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        ob = context.active_object
        for n in ob.pose.bones:
            if n.bone.select:
                n.keyframe_insert('location')
        refresh()
        return {'FINISHED'}


class bone_key_rot(Operator):

    """Insert rotation key for all selected bones"""

    bl_idname = "object.bone_key_rot"
    bl_label = "Key Rot"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        ob = context.active_object
        for n in ob.pose.bones:
            if n.bone.select:
                if n.rotation_mode == 'QUATERNION':
                    n.keyframe_insert('rotation_quaternion')
                else:
                    n.keyframe_insert('rotation_euler')
        refresh()
        return {'FINISHED'}


class bone_key_scl(Operator):

    """Insert scale key for all selected bones"""

    bl_idname = "object.bone_key_scl"
    bl_label = "Key Scl"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        ob = context.active_object
        for n in ob.pose.bones:
            if n.bone.select:
                n.keyframe_insert('scale')
        refresh()
        return {'FINISHED'}


class select_opposite_bone(Operator):

    """Select opposite bone"""

    bl_idname = "object.select_opposite_bone"
    bl_label = "Select opposite bone"

    def execute(self, context):
        select_opposite()
        return {'FINISHED'}


class ivo_calc_motion_paths(Operator):

    """Motion path"""

    bl_idname = "object.ivo_calc_motion_paths"
    bl_label = "Motion paths"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        ob = context.active_object
        bpy.ops.pose.paths_clear()
        if context.scene.use_preview_range:
            ob.pose.animation_visualisation.motion_path.frame_start = context.scene.frame_preview_start
            ob.pose.animation_visualisation.motion_path.frame_end = context.scene.frame_preview_end
        else:
            ob.pose.animation_visualisation.motion_path.frame_start = context.scene.frame_start
            ob.pose.animation_visualisation.motion_path.frame_end = context.scene.frame_end
        ob.pose.animation_visualisation.motion_path.bake_location = 'HEADS'
        ob.pose.animation_visualisation.motion_path.show_keyframe_numbers = True
        ob.pose.animation_visualisation.motion_path.show_keyframe_action_all = True
        ob.pose.animation_visualisation.motion_path.show_keyframe_highlight = True
        bpy.ops.pose.paths_calculate()
        context.scene.frame_current = context.scene.frame_current
        return {'FINISHED'}


class distance_between_bones(Operator):

    """Prints distance between two selected bones"""

    bl_idname = "object.distance_between_bones"
    bl_label = "Distance"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        bone1 = None
        bone2 = None
        for n in ob.pose.bones:
            if bone1 is None:
                if n.bone.select:
                    bone1 = n
            elif bone2 is None:
                if n.bone.select:
                    bone2 = n
            if bone2 is not None:
                break

        if bone2 is not None:
            vec1 = bone1.matrix.translation_part()
            vec2 = bone2.matrix.translation_part()

            print((vec1 - vec2).length)

        return {'FINISHED'}


# Cycle Layers ================================================================

def func_cycle_armature_layer(ob, increment=1):
    layer = ob.data.layers

    index = -1
    for n in range(len(layer)):
        if layer[n]:
            index = n

    if index + increment < len(layer) and index + increment > -1:
        index += increment
    layer = [False for n in range(len(layer))]
    layer[index] = True
    print(layer)
    ob.data.layers = layer


class next_armature_layer(Operator):

    """"""

    bl_idname = "object.next_armature_layer"
    bl_label = "next_armature_layer"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        props = self.properties
        ob = context.active_object
        func_cycle_armature_layer(ob, 1)
        return {'FINISHED'}


class prev_armature_layer(Operator):

    """"""

    bl_idname = "object.prev_armature_layer"
    bl_label = "prev_armature_layer"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        props = self.properties
        ob = context.active_object
        func_cycle_armature_layer(ob, -1)
        return {'FINISHED'}


# Bone Snapping ===============================================================

def snap_bone_to_position(ob, posebone, location):

    bone = posebone.parent

    scl = mathutils.Matrix.Scale(1, 4)
    rot = bone.rotation_quaternion.to_matrix().resize4x4()
    pos = mathutils.Matrix.Translation(bone.location)

    inmat = mathutils.Matrix.Translation(location)
    pc_trans = scl * rot * pos
    inv_trans = pc_trans.invert()
    pc_posemat = bone.matrix.copy() * inv_trans
    inv_posemat = pc_posemat.copy().invert()
    outmat = inv_posemat * inmat

    bone.location = outmat.translation_part()

#  In:
#    posebone: the one that should be snapped/transformed
#    target: can bei either a posebone or a matrix in armature space


def snap_posebone_to_posebone(posebone, target, loc=True, rot=True):

    if posebone.parent is not None:
        parent_inverse = posebone.parent.matrix.copy()
        parent_inverse.invert()
        parent_local_inverse = posebone.parent.bone.matrix_local.copy()
        parent_local_inverse.invert()
        matrix_local = posebone.bone.matrix_local.copy()

    else:
        parent_inverse = parent_local_inverse = matrix_local = mathutils.Matrix()
    # tmp3 = posebone.parent.bone.matrix_local.copy()
    # tmp3.invert()

    # parent_offset = tmp3 * posebone.bone.matrix_local.copy()
    parent_offset = parent_local_inverse * posebone.bone.matrix_local.copy()
    # tmp4 = parent_offset.copy()
    # tmp4.invert()
    parent_offset.invert()
    # m = tmp4 * parent_inverse #  we have the world center now ...
    m = parent_offset * parent_inverse  # we have the world center now ...

    # ... and simply mul by target world matrix
    if isinstance(target, mathutils.Matrix):
        m *= target
    elif isinstance(target, bpy.types.PoseBone):
        m *= target.matrix

    # output
    if loc:
        posebone.location = m.to_translation()
    if rot:
        if posebone.rotation_mode == 'QUATERNION':
            posebone.rotation_quaternion = m.to_quaternion()
        else:
            posebone.rotation_euler = m.to_euler(posebone.rotation_mode)


def snap_bone_to_bone(ob, posebone, destbone):

    bone = posebone
    scl = mathutils.Matrix.Scale(1, 4)
    rot = bone.rotation_quaternion.to_matrix().resize4x4()
    pos = mathutils.Matrix.Translation(bone.location)

    inmat = destbone.matrix
    pc_trans = scl * rot * pos
    inv_trans = pc_trans.invert()
    pc_posemat = bone.matrix.copy() * inv_trans
    inv_posemat = pc_posemat.copy().invert()
    outmat = inv_posemat * inmat

    bone.location = outmat.translation_part()
    if bone.rotation_mode == 'QUATERNION':
        bone.rotation_quaternion = outmat.rotation_part().to_quat()
    else:
        bone.rotation_euler = outmat.rotation_part().to_euler()


def snap_bone_to_matrix(ob, posebone, mat):

    bone = posebone
    scl = mathutils.Matrix.Scale(1, 4)
    rot = bone.rotation_quaternion.to_matrix().resize4x4()
    pos = mathutils.Matrix.Translation(bone.location)

    inmat = mat
    pc_trans = scl * rot * pos
    inv_trans = pc_trans.invert()
    pc_posemat = bone.matrix.copy() * inv_trans
    inv_posemat = pc_posemat.copy().invert()
    outmat = inv_posemat * inmat

    bone.location = outmat.translation_part()
    if bone.rotation_mode == 'QUATERNION':
        bone.rotation_quaternion = outmat.rotation_part().to_quat()
    else:
        bone.rotation_euler = outmat.rotation_part().to_euler()


def bone_match_rotation(ob, bone, target_matrix):

    has_parent = None
    rotation_mode = bone.rotation_mode
    bone_ = ob.data.bones[bone.name]
    if bone.parent is None:
        has_parent = False
        mat = bone_.matrix.copy().resize4x4()  # * tobone.matrix_local
    else:
        mat = bone.parent.matrix * bone_.matrix.copy().resize4x4()  # * tobone.matrix_local
        has_parent = True
    offs = mat.copy()
    offs[3][0] = bone_.head[0]
    offs[3][1] = bone_.head[1]
    offs[3][2] = bone_.head[2]

    if has_parent:
        offs[3][1] += bone_.parent.length

    m2 = offs.copy().invert() * target_matrix

    if bone.rotation_mode == 'QUATERNION':
        bone.rotation_quaternion = m2.rotation_part().to_quat()
        return m2.rotation_part()
    else:
        bone.rotation_euler = m2.rotation_part().to_euler(rotation_mode)
        return m2.rotation_part()


class bone_snap_rotation(Operator):

    """Match rotation betwween first and second bone or object"""

    bl_idname = "object.bone_snap_rotation"
    bl_label = "bone_snap_rotation"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        target = context.active_pose_bone
        source = None

        # find amount of selected objects
        num = 0
        for n in bpy.context.scene.objects:
            if n.select:
                num += 1

        # find source object
        if num > 1:
            for n in bpy.context.scene.objects:
                if n.select and n != ob:
                    source = n
                    break
            if source is None:
                print("Mist ... source == None")

        if num == 1 and ob.type == 'ARMATURE':  # only one armature is selected
            for n in ob.pose.bones:
                if n.bone.select and n != target:
                    # bone_match_rotation(ob, n, target.matrix)
                    snap_posebone_to_posebone(n, target, loc=False, rot=True)

        elif num > 1:  # two objects are selected
            if ob.type == source.type == 'ARMATURE':  # two armatures are selected
                # find source posebone
                src_posebone = None
                for n in source.pose.bones:
                    if n.bone.select:
                        src_posebone = n
                        break
                if src_posebone is not None:
                    bone_match_rotation(source, src_posebone, target.matrix)
                else:
                    print("ERROR")

        return {'FINISHED'}


class bone_snap_location(Operator):

    """Match rotation betwween first and second bone or object"""

    bl_idname = "object.bone_snap_location"
    bl_label = "bone_snap_location"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        target = context.active_pose_bone
        source = None

        # find amount of selected objects
        num = 0
        for n in bpy.context.scene.objects:
            if n.select:
                num += 1

        # find source object
        if num > 1:
            for n in bpy.context.scene.objects:
                if n.select and n != ob:
                    source = n
                    break
            if source is None:
                print("Mist ... source == None")

        if num == 1 and ob.type == 'ARMATURE':  # only one armature is selected
            for n in ob.pose.bones:
                if n.bone.select and n != target:
                    # bone_match_rotation(ob, n, target.matrix)
                    snap_posebone_to_posebone(n, target, loc=True, rot=False)

        elif num > 1:  # two objects are selected
            if ob.type == source.type == 'ARMATURE':  # two armatures are selected

                # find source posebone
                src_posebone = None
                for n in source.pose.bones:
                    if n.bone.select:
                        src_posebone = n
                        break
                if src_posebone is not None:
                    bone_match_rotation(source, src_posebone, target.matrix)
                else:
                    print("ERROR")

        return {'FINISHED'}


class bone_snap_locrot(Operator):

    """Match rotation betwween first and second bone or object"""

    bl_idname = "object.bone_snap_locrot"
    bl_label = "bone_snap_locrot"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        target = context.active_pose_bone
        source = None

        # find amount of selected objects
        num = 0
        for n in bpy.context.scene.objects:
            if n.select:
                num += 1

        # find source object
        if num > 1:
            for n in bpy.context.scene.objects:
                if n.select and n != ob:
                    source = n
                    break
            if source is None:
                print("Mist ... source == None")

        if num == 1 and ob.type == 'ARMATURE':  # only one armature is selected
            for n in ob.pose.bones:
                if n.bone.select and n != target:
                    # bone_match_rotation(ob, n, target.matrix)
                    snap_posebone_to_posebone(n, target, loc=True, rot=True)

        elif num > 1:  # two objects are selected
            if ob.type == source.type == 'ARMATURE':  # two armatures are selected

                # find source posebone
                src_posebone = None
                for n in source.pose.bones:
                    if n.bone.select:
                        src_posebone = n
                        break
                if src_posebone is not None:
                    bone_match_rotation(source, src_posebone, target.matrix)
                else:
                    print("ERROR")

        return {'FINISHED'}


# Baking ======================================================================

def func_bake(loc=True, rot=True):

    scene = bpy.context.scene

    if scene.use_preview_range:
        startframe = bpy.context.scene.frame_preview_start
        endframe = bpy.context.scene.frame_preview_end
    else:
        startframe = bpy.context.scene.frame_start
        endframe = bpy.context.scene.frame_end

    ob = bpy.context.active_object
    scene = bpy.context.scene

    for n in range(startframe, endframe):

        scene.frame_current = n
        scene.frame_set(n)

        bpy.ops.pose.visual_transform_apply()
        for i in ob.pose.bones:
            if i.bone.select:

                if rot:
                    if i.rotation_mode == 'QUATERNION':
                        i.keyframe_insert('rotation_quaternion')

                    else:
                        i.keyframe_insert('rotation_euler')
                if loc:
                    i.keyframe_insert('location')


class bone_bake_rotations(Operator):

    """Bake rotation for selected bones"""

    bl_idname = "object.bone_bake_rotations"
    bl_label = "bone_bake_rotations"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        func_bake(loc=False, rot=True)
        return {'FINISHED'}


class bone_bake_locations(Operator):

    """Bake rotation for selected bones"""

    bl_idname = "object.bone_bake_locations"
    bl_label = "bone_bake_locations"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        func_bake(loc=True, rot=False)
        return {'FINISHED'}


class bone_bake_locrot(Operator):

    """Bake rotation for selected bones"""

    bl_idname = "object.bone_bake_locrot"
    bl_label = "bone_bake_locrot"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        func_bake(loc=True, rot=True)
        return {'FINISHED'}


# Toggle ======================================================================

class posebone_toggle_constraints(Operator):

    """Toggles constraints of active bone"""

    bl_idname = "object.posebone_toggle_constraints"
    bl_label = "Toggle constraints"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # ob = context.active_object

        # for n in ob.pose.bones:
        #   if n.bone.select:
        for i in context.active_pose_bone.constraints:
            i.mute = not i.mute

        return {'FINISHED'}


class xraytoggle(Operator):

    """"""

    bl_idname = "object.xraytoggle"
    bl_label = "Ivo X-Ray toggle"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        ob.show_x_ray = not ob.show_x_ray
        return {'FINISHED'}


class draw_axis_toggle(Operator):

    """"""

    bl_idname = "armature.draw_axis_toggle"
    bl_label = "Show axes"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        ob.data.show_axes = not ob.data.show_axes
        return {'FINISHED'}


class toggle_geo_solo(Operator):

    """Toggle Geometry only display"""

    bl_idname = "scene.toggle_geo_solo"
    bl_label = "Geometry only"

    def execute(self, context):
        context.area.spaces.active.show_only_render = not context.area.spaces.active.show_only_render
        return {'FINISHED'}


# Reset Transforms ============================================================

class ivo_reset_transforms(Operator):

    """Reset current pose bone"""

    bl_idname = "object.ivo_reset_transforms"
    bl_label = "Reset transforms"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        try:
            bpy.ops.pose.rot_clear()
            bpy.ops.pose.loc_clear()
            bpy.ops.pose.scale_clear()
        except:
            bpy.ops.object.rotation_clear()
            bpy.ops.object.scale_clear()
            bpy.ops.object.location_clear()

        return {'FINISHED'}


class ivo_reset_all_transforms(Operator):

    """Reset all pose bones"""

    bl_idname = "object.ivo_reset_all_transforms"
    bl_label = "Reset all transforms"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = bpy.context.active_object

        for n in ob.pose.bones:
            n.matrix_basis.identity()

        bpy.context.scene.frame_current = bpy.context.scene.frame_current
        return {'FINISHED'}


class ivo_armature_show_all_layers(Operator):

    """"""

    bl_idname = "object.ivo_armature_show_all_layers"
    bl_label = "Show all am Layers"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        for n in range(len(ob.data.layers)):
            ob.data.layers[n] = True

        return {'FINISHED'}


class to_start_frame(Operator):

    """Tooltip"""

    bl_idname = "ivo.to_start_frame"
    bl_label = "To start frame"

    def execute(self, context):
        scene = bpy.context.scene
        if scene.use_preview_range:
            scene.frame_current = scene.frame_preview_start
        else:
            scene.frame_current = scene.frame_start
        return {'FINISHED'}


class to_end_frame(Operator):

    """Tooltip"""

    bl_idname = "ivo.to_end_frame"
    bl_label = "To end frame"

    def execute(self, context):
        scene = bpy.context.scene
        if scene.use_preview_range:
            scene.frame_current = scene.frame_preview_end
        else:
            scene.frame_current = scene.frame_end
        return {'FINISHED'}


class VIEW3D_PT_tools_ivoanim(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rig'
    bl_context = "posemode"
    bl_label = "Ivo animation toolbox"

    def draw(self, context):
        layout = self.layout

        ad = context.active_object.animation_data
        scn = context.scene
        am = context.active_object.data
        interpolation = context.user_preferences.edit.keyframe_new_interpolation_type

        col = layout.column(align=True)

        row = layout.row(align=True)
        row.operator("object.bone_key_loc")
        row.operator("object.bone_key_rot")
        row.operator("object.bone_key_scl")

        col = layout.column(align=True)
        col.operator("object.delete_current_frame")

        col = layout.column(align=True)
        col.operator("scene.toggle_geo_solo", text="Show only geometry")

        col = layout.column(align=True)
        col.operator("play.blast")

        col = layout.column(align=True)
        col.operator("object.ivo_reset_transforms")

        col = layout.column(align=True)
        # col.prop(interpolation, "Interpolation")
        col.operator("object.clean_curves")
        col.operator("object.key_poses")
        col.operator("object.remove_flat_curves")

        col = layout.column(align=True)
        col.operator("object.bone_bake_locations", text="Bake locations")
        col.operator("object.bone_bake_rotations", text="Bake rotations")
        col.operator("object.bone_bake_locrot", text="Bake loc+rot")

        col = layout.column(align=True)
        col.operator("object.bone_snap_location", text="Snap location")
        col.operator("object.bone_snap_rotation", text="Snap rotation")
        col.operator("object.bone_snap_locrot", text="Snap loc+rot")

        # Commented this out because it makes blender freeze sometimes
        # row = layout.row(align=True)
        # row.operator("object.ivo_calc_motion_paths", text="Calculate Paths")
        # row.operator("pose.paths_clear", text="Clear Paths")

        try:
            col = layout.column(align=True)
            col.prop(ad, "action", slider=True)
        except:
            pass

        col = layout.column(align=True)
        # col.prop(scn, "active_keying_set")
        col.prop_search(scn.keying_sets_all, "active", scn, "keying_sets_all", text="Keying set: ")

        col = layout.column(align=True)
        col.prop(context.user_preferences.edit, "keyframe_new_interpolation_type", text='Keys')

        col = layout.column(align=True)
        col.operator("object.add_pos_to_keying_set")
        col.operator("object.add_rot_to_keying_set")
        col.operator("object.add_scl_to_keying_set")
        col.operator("object.add_srt_to_keying_set")

        col = layout.column(align=True)
        col.prop(am, "layers", text="Armature layers:")
        row = layout.row(align=True)
        row.operator("object.prev_armature_layer", text="prev")
        row.operator("object.next_armature_layer", text="next")

        col = layout.column(align=True)
        col.operator("object.ivo_armature_show_all_layers")

        # col.operator("object.distance_between_bones")
        # col.operator("object.posebone_toggle_constraints")

        col.operator("object.select_opposite_bone")
        col.operator("object.deselect_bones")

        col = layout.column(align=True)
        # col.operator("object.wiretoggle", text="Wireframe on shaded")
        col.operator("object.xraytoggle", text="X-Ray")
        col.operator("object.ivo_reset_all_transforms")

        # st = context.space_data
        # layout.template_ID(st, "action", new="action.new")


classes = (
    deselect_all_bones,
    key_poses,
    clean_curves,
    remove_flat_curves,
    Playblast,
    delete_current_frame,
    add_pos_to_keying_set,
    add_rot_to_keying_set,
    add_scl_to_keying_set,
    add_SRT_to_keying_set,
    jump_first_frame,
    jump_last_frame,
    bone_key_loc,
    bone_key_rot,
    bone_key_scl,
    select_opposite_bone,
    ivo_calc_motion_paths,
    distance_between_bones,
    next_armature_layer,
    prev_armature_layer,
    bone_snap_rotation,
    bone_snap_location,
    bone_snap_locrot,
    bone_bake_rotations,
    bone_bake_locations,
    bone_bake_locrot,
    posebone_toggle_constraints,
    xraytoggle,
    draw_axis_toggle,
    toggle_geo_solo,
    ivo_reset_transforms,
    ivo_reset_all_transforms,
    ivo_armature_show_all_layers,
    to_start_frame,
    to_end_frame,
    VIEW3D_PT_tools_ivoanim
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
