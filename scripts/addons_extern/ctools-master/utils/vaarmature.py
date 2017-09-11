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


"""
NOTE:

context.active_bone: EditBone or Bone
context.active_pose_bone: PoseBone

EditBone:
    <Armature Space>
    matrix: 4x4。scale成分は含まない。

Bone:
    <Bone Space>  親Bone基準の座標系。scale成分は含まず、親tailが原点。
    matrix: 3x3行列。
        (source: Bone.bone_mat  # rotation derived from head/tail/roll)
    head: (source: Bone.head)
    tail: (source: Bone.tail)

    <Armature Space>
    matrix_local: 4x4行列。scale成分は含まない。EditBone.matrixと同じ。
         (source: Bone.arm_mat  # matrix: (bonemat(b)+head(b))*arm_mat(b-1), rest pos)
    head_local: (source: Bone.arm_head)
    tail_local: (source: Bone.arm_head)

PoseBone:
    <Object Space>
    matrix: ドライバやConstraintを適用済み。
        (souce: bPoseChannel.pose_mat
         # constraints accumulate here. in the end, pose_mat = bone->arm_mat * chan_mat
           this matrix is object space)
         ※ 実際の計算式はこうだが、コメが間違ってる？ pose_mat = chan_mat * bone->arm_mat
    matrix_channel:
        ドライバやConstraintを適用済み。読み込み専用。
        PoseBone.matrix = PoseBone.matrix_channel * Bone.matrix_local という関係
        (source: bPoseChannel.chan_mat
         # matrix result of loc/quat/size, and where we put deform in, see next line)

    <Pose Bone Space> (仮の名称)
    matrix_basis:
        location/scale/rotationのみ適用したもの。Constraint等は含まない
"""


import math

import bpy
#from bpy.props import *
#import mathutils as Math
from mathutils import Matrix, Euler, Vector, Quaternion

from . import vamath as vam


# custom_properties_add()とcustom_properties_remove()で使用
_custom_properties = []


def custom_properties_add(targets=(bpy.types.Bone, bpy.types.EditBone,
                                   bpy.types.PoseBone),
                          stack=_custom_properties):
    """カスタムプロパティの追加。custom_properties_remove()と対の関係。
    EditBone, Bone, PoseBone:
        'is_visible'
    PoseBone:
        'select', 'select_head', 'select_tail', 'hide', 'layers', 'use_connect'
    """
    backup = {bpy_type: {} for bpy_type in targets}

    # 'is_visible'
    attr = 'is_visible'
    for bpy_type in (bpy.types.Bone, bpy.types.EditBone, bpy.types.PoseBone):
        if bpy_type not in targets:
            continue
        d = backup[bpy_type]
        if hasattr(bpy_type, attr):
            d[attr] = getattr(bpy_type, attr)
        else:
            d[attr] = None
        def fget(self):
            if isinstance(self, bpy.types.PoseBone):
                arm = self.id_data.data  # id_dada: Object
            else:
                arm = self.id_data  # id_data: Armature
            return (not self.hide and
                    any([a and b for a, b in zip(arm.layers, self.layers)]))
        setattr(bpy_type, attr, property(fget))

    # PoseBone
    # PoseBone.boneの属性を直接参照出来るようにする
    if bpy.types.PoseBone in targets:
        d = backup[bpy.types.PoseBone]
        for attr in ('select', 'select_head', 'select_tail', 'hide', 'layers',
                     'use_connect'):
            if hasattr(bpy.types.PoseBone, attr):
                d[attr] = getattr(bpy.types.PoseBone, attr)
            else:
                d[attr] = None
            def fget(self, attr=attr):
                return getattr(self.bone, attr)
            def fset(self, value, attr=attr):
                return setattr(self.bone, attr, value)
            setattr(bpy.types.PoseBone, attr, property(fget, fset))

    stack.append(backup)


def custom_properties_remove(stack=_custom_properties):
    """custom_properties_add()で追加したものを元に戻す"""
    if not stack:
        return False
    backup = stack.pop()
    for bpy_type, props in backup.items():
        for attr, prop in props.items():
            if prop is None:
                if hasattr(bpy_type, attr):
                    delattr(bpy_type, attr)
            else:
                setattr(bpy_type, attr, prop)
    return True


class CustomProperty:
    """with文で使う
    with CustomProperty():
        pass
    """
    properties = []  # 既存のプロパティ

    def __init__(self, targets=(bpy.types.Bone, bpy.types.EditBone,
                                bpy.types.PoseBone)):
        self.targets = targets

    def __enter__(self):
        custom_properties_add(self.targets, self.properties)

    def __exit__(self, exc_type, exc_value, traceback):
        custom_properties_remove(self.properties)


def bone_is_visible(ob, bone):
    """layer,hideによりBoneが表示中か判定する。
    :param ob: Armature Object
    :type ob: bpy.types.Object
    :param bone: Bone
    :type bone: bpy.types.Bone | bpy.types.EditBone | bpy.types.PoseBone
    :return: visible or not
    :rtype: bool
    """
    if isinstance(bone, bpy.types.PoseBone):
        bone = bone.bone
    if bone.hide:
        return False
    return any([a and b for a, b in zip(ob.data.layers, bone.layers)])


def get_visible_bones(ob, mode=None):
    """Return list of visible bones.
    :param ob: Armature Object
    :type ob: bpy.types.Object
    :param mode: 'OBJECT', 'EDIT', 'POSE'
    :type mode: str
    :return: visible bones
    :rtype: list[bpy.types.Bone | bpy.types.EditBone | bpy.types.PoseBone]
    """
    if ob.type != 'ARMATURE':
        return None
    if not mode:
        mode = ob.mode
    if mode == 'OBJECT':
        bones = [b for b in ob.data.bones if bone_is_visible(ob, b)]
    elif mode == 'EDIT':
        bones = [eb for eb in ob.data.edit_bones if bone_is_visible(ob, eb)]
    else:  # 'POSE'
        bones = [pb for pb in ob.pose.bones if bone_is_visible(ob, pb)]
    return bones


def get_selected_bones(ob, mode=None):
    """Return list of visible and selected bones.
    :param ob: Armature Object
    :type ob: bpy.types.Object
    :param mode: 'OBJECT', 'EDIT', 'POSE'
    :type mode: str
    :return: visible and selected bones
    :rtype: list[Bone | EditBone | PoseBone]
    """
    if ob.type != 'ARMATURE':
        return None
    if not mode:
        mode = ob.mode
    bones = get_visible_bones(ob, mode)
    if mode == 'POSE':
        return [b for b in bones if b.bone.select]
    else:
        return [b for b in bones if b.select]


def mat3_to_vec_roll(mat):
    """blenkernel/intern/armature.c: mat3_to_vec_rollより"""
    mat = mat.to_3x3()

    vec = mat.col[1].copy()

    vecmat = vec_roll_to_mat3(mat.col[1], 0.0)
    rollmat = vecmat.inverted() * mat
    roll = math.atan2(rollmat.col[2][0], rollmat.col[2][2])

    return vec, roll


def vec_roll_to_mat3(vec, roll):
    """blenkernel/intern/armature.c: vec_roll_to_mat3より"""
    THETA_THRESHOLD_NEGY = 1.0e-9
    THETA_THRESHOLD_NEGY_CLOSE = 1.0e-5

    nor = vec.normalized()

    bMatrix = Matrix.Identity(3)

    theta = 1.0 + nor[1]

    if (theta > THETA_THRESHOLD_NEGY_CLOSE or
            ((nor[0] or nor[2]) and theta > THETA_THRESHOLD_NEGY)):
        bMatrix.col[0][1] = -nor[0]
        bMatrix.col[1][0] = nor[0]
        bMatrix.col[1][1] = nor[1]
        bMatrix.col[1][2] = nor[2]
        bMatrix.col[2][1] = -nor[2]
        if theta > THETA_THRESHOLD_NEGY_CLOSE:
            bMatrix.col[0][0] = 1 - nor[0] * nor[0] / theta
            bMatrix.col[2][2] = 1 - nor[2] * nor[2] / theta
            bMatrix.col[2][0] = bMatrix.col[0][2] = -nor[0] * nor[2] / theta
        else:
            theta = nor[0] * nor[0] + nor[2] * nor[2]
            bMatrix.col[0][0] = (nor[0] + nor[2]) * (nor[0] - nor[2]) / -theta
            bMatrix.col[2][2] = -bMatrix.col[0][0]
            bMatrix.col[2][0] = bMatrix.col[0][2] = \
                2.0 * nor[0] * nor[2] / theta
    else:
        bMatrix.col[0][0] = bMatrix.col[1][1] = -1.0

    rMatrix = Quaternion(nor, roll).to_matrix()
    return rMatrix * bMatrix
