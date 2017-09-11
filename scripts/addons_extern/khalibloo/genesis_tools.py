# <pep8 compliant>
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
import bmesh
import math
from .utils import *


#============================================================================
# DEFINE FUNCTIONS
#============================================================================

rigifyRig = None
genesisRig = None


def copyMeshPos(metarig, genesis, targetBone, headOrTail, vgroupName):
    vgroupIndex = genesis.vertex_groups[vgroupName].index
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = genesis
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.context.active_object.vertex_groups.active_index = vgroupIndex
    bpy.ops.object.vertex_group_select()
    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')

    if headOrTail == "head":
        bpy.context.active_object.data.edit_bones[targetBone].select_head = True
    if headOrTail == "tail":
        bpy.context.active_object.data.edit_bones[targetBone].select_tail = True

    bpy.ops.view3d.snap_selected_to_cursor()
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def copyBonePos(metarig, genesisRig, targetBone, headOrTail, sourceBone):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = genesisRig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')

    if headOrTail == "head":
        bpy.context.active_object.data.edit_bones[sourceBone].select_head = True
    if headOrTail == "tail":
        bpy.context.active_object.data.edit_bones[sourceBone].select_tail = True

    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')

    if headOrTail == "head":
        bpy.context.active_object.data.edit_bones[targetBone].select_head = True
    if headOrTail == "tail":
        bpy.context.active_object.data.edit_bones[targetBone].select_tail = True

    bpy.ops.view3d.snap_selected_to_cursor()
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def metarigPrep(metarig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.active_object.data.use_mirror_x = True
    bpy.context.active_object.data.edit_bones["neck"].use_connect = True
    bpy.ops.object.mode_set(mode='OBJECT')

def metarigFinishingTouches(metarig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["heel.02.L"].head[2] = 0
    bpy.context.active_object.data.edit_bones["heel.02.R"].head[2] = 0
    bpy.context.active_object.data.edit_bones["heel.02.L"].tail[2] = 0
    bpy.context.active_object.data.edit_bones["heel.02.R"].tail[2] = 0
    bpy.context.active_object.data.edit_bones["heel.02.L"].tail[1] = bpy.context.active_object.data.edit_bones["heel.02.L"].head[1]
    bpy.context.active_object.data.edit_bones["heel.02.R"].tail[1] = bpy.context.active_object.data.edit_bones["heel.02.R"].head[1]
    bpy.context.active_object.data.edit_bones["heel.L"].tail[2] = 0
    bpy.context.active_object.data.edit_bones["heel.R"].tail[2] = 0
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def createFaceRig(g3):
    #we need to know if it's a g3 because of its unique skeleton
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.armature_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
    faceRig = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')

    #add tongue bones
    #the default bone is the tongue's base
    bpy.context.space_data.cursor_location[0] = 0
    bpy.ops.armature.bone_primitive_add()
    bpy.context.space_data.cursor_location[0] = 1
    bpy.ops.armature.bone_primitive_add()
    bpy.context.space_data.cursor_location[0] = 2
    bpy.ops.armature.bone_primitive_add()
    if(g3 == False):
        bpy.context.space_data.cursor_location[0] = 3
        bpy.ops.armature.bone_primitive_add()
        bpy.context.space_data.cursor_location[0] = 4
        bpy.ops.armature.bone_primitive_add()
        bpy.context.space_data.cursor_location[0] = 5
        bpy.ops.armature.bone_primitive_add()
    #add eye bones
    bpy.context.space_data.cursor_location[0] = 6
    bpy.ops.armature.bone_primitive_add()
    bpy.context.space_data.cursor_location[0] = 7
    bpy.ops.armature.bone_primitive_add()
    bpy.context.space_data.cursor_location[0] = 8
    bpy.ops.armature.bone_primitive_add()
    bpy.context.space_data.cursor_location[0] = 9
    bpy.ops.armature.bone_primitive_add()
    bpy.context.space_data.cursor_location[0] = 10
    bpy.ops.armature.bone_primitive_add()
    bpy.context.space_data.cursor_location[0] = 11

    #names
    i = 0
    if(g3 == False):
        faceRig.data.edit_bones[i].name = "DEF-tonguebase"
        i += 1
    faceRig.data.edit_bones[i].name = "DEF-tongue.01"
    i += 1
    faceRig.data.edit_bones[i].name = "DEF-tongue.02"
    i += 1
    faceRig.data.edit_bones[i].name = "DEF-tongue.03"
    i += 1
    faceRig.data.edit_bones[i].name = "DEF-tongue.04"
    i += 1
    if(g3 == False):
        faceRig.data.edit_bones[i].name = "DEF-tongue.05"
        i += 1
        faceRig.data.edit_bones[i].name = "DEF-tonguetip"
        i += 1
    faceRig.data.edit_bones[i].name = "DEF-eye.L"
    i += 1
    faceRig.data.edit_bones[i].name = "DEF-eye.R"
    i += 1
    faceRig.data.edit_bones[i].name = "IK-eye.L"
    i += 1
    faceRig.data.edit_bones[i].name = "IK-eye.R"
    i += 1
    faceRig.data.edit_bones[i].name = "IK-eyes_lookat"

    #disable deform
    faceRig.data.edit_bones["IK-eye.L"].use_deform = False
    faceRig.data.edit_bones["IK-eye.R"].use_deform = False
    faceRig.data.edit_bones["IK-eyes_lookat"].use_deform = False

    #constraints
    bpy.ops.object.mode_set(mode='POSE')

    faceRig.data.bones.active = faceRig.data.bones["DEF-eye.L"]
    bpy.ops.pose.constraint_add(type='IK')
    faceRig.pose.bones["DEF-eye.L"].constraints[-1].target = faceRig
    faceRig.pose.bones["DEF-eye.L"].constraints[-1].subtarget = "IK-eye.L"
    faceRig.pose.bones["DEF-eye.L"].constraints[-1].chain_count = 1

    faceRig.data.bones.active = faceRig.data.bones["DEF-eye.R"]
    bpy.ops.pose.constraint_add(type='IK')
    faceRig.pose.bones["DEF-eye.R"].constraints[-1].target = faceRig
    faceRig.pose.bones["DEF-eye.R"].constraints[-1].subtarget = "IK-eye.R"
    faceRig.pose.bones["DEF-eye.R"].constraints[-1].chain_count = 1

    bpy.ops.object.mode_set(mode='OBJECT')

    return faceRig

def faceRigSetParents(faceRig, g3):
    #we need to know if it's a g3 because of its unique skeleton
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = faceRig
    bpy.ops.object.mode_set(mode='EDIT')

    #faceRig.data.edit_bones["DEF-tongue.01"].parent = faceRig.data.edit_bones["DEF-head"]
    #faceRig.data.edit_bones["DEF-tongue.01"].use_connect = False

    faceRig.data.edit_bones["DEF-tongue.02"].parent = faceRig.data.edit_bones["DEF-tongue.01"]
    faceRig.data.edit_bones["DEF-tongue.02"].use_connect = True

    faceRig.data.edit_bones["DEF-tongue.03"].parent = faceRig.data.edit_bones["DEF-tongue.02"]
    faceRig.data.edit_bones["DEF-tongue.03"].use_connect = True

    faceRig.data.edit_bones["DEF-tongue.04"].parent = faceRig.data.edit_bones["DEF-tongue.03"]
    faceRig.data.edit_bones["DEF-tongue.04"].use_connect = True

    if(g3 == False):
        faceRig.data.edit_bones["DEF-tongue.01"].parent = faceRig.data.edit_bones["DEF-tonguebase"]
        faceRig.data.edit_bones["DEF-tongue.01"].use_connect = True

        faceRig.data.edit_bones["DEF-tongue.05"].parent = faceRig.data.edit_bones["DEF-tongue.04"]
        faceRig.data.edit_bones["DEF-tongue.05"].use_connect = True

        faceRig.data.edit_bones["DEF-tonguetip"].parent = faceRig.data.edit_bones["DEF-tongue.05"]
        faceRig.data.edit_bones["DEF-tonguetip"].use_connect = True

    faceRig.data.edit_bones["IK-eye.L"].parent = faceRig.data.edit_bones["IK-eyes_lookat"]
    faceRig.data.edit_bones["IK-eye.R"].parent = faceRig.data.edit_bones["IK-eyes_lookat"]

def faceRigFinishingTouches(faceRig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = faceRig
    bpy.ops.object.mode_set(mode='EDIT')

    #Left Eye IK bone
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["DEF-eye.L"].select_tail = True
    bpy.ops.view3d.snap_cursor_to_selected()

    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["IK-eye.L"].select_head = True
    cursorY = bpy.context.space_data.cursor_location[1]
    bpy.context.space_data.cursor_location[1] = cursorY - 0.5
    bpy.ops.view3d.snap_selected_to_cursor()
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["IK-eye.L"].select_tail = True
    cursorY = bpy.context.space_data.cursor_location[1]
    bpy.context.space_data.cursor_location[1] = cursorY - 0.05
    bpy.ops.view3d.snap_selected_to_cursor()

    #Right Eye IK bone
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["DEF-eye.R"].select_tail = True
    bpy.ops.view3d.snap_cursor_to_selected()

    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["IK-eye.R"].select_head = True
    cursorY = bpy.context.space_data.cursor_location[1]
    bpy.context.space_data.cursor_location[1] = cursorY - 0.5
    bpy.ops.view3d.snap_selected_to_cursor()
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["IK-eye.R"].select_tail = True
    cursorY = bpy.context.space_data.cursor_location[1]
    bpy.context.space_data.cursor_location[1] = cursorY - 0.05
    bpy.ops.view3d.snap_selected_to_cursor()


    #Eyes Look-at Bone
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["DEF-eye.L"].select_tail = True
    bpy.context.active_object.data.edit_bones["DEF-eye.R"].select_tail = True
    bpy.ops.view3d.snap_cursor_to_selected()

    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["IK-eyes_lookat"].select_head = True
    cursorY = bpy.context.space_data.cursor_location[1]
    bpy.context.space_data.cursor_location[1] = cursorY - 0.5
    bpy.ops.view3d.snap_selected_to_cursor()

    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["IK-eyes_lookat"].select_tail = True
    cursorY = bpy.context.space_data.cursor_location[1]
    bpy.context.space_data.cursor_location[1] = cursorY - 0.1
    bpy.ops.view3d.snap_selected_to_cursor()

    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.calculate_roll(type='POS_X')

def setGenesisRolls(metarig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["head"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["neck"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["chest"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["spine"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["hips"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["thigh.L"].roll = -0.050401
    bpy.context.active_object.data.edit_bones["shin.L"].roll = -0.015987
    bpy.context.active_object.data.edit_bones["foot.L"].roll = -1.212506
    bpy.context.active_object.data.edit_bones["toe.L"].roll = 1.431089
    bpy.context.active_object.data.edit_bones["heel.L"].roll = 0.0939
    bpy.context.active_object.data.edit_bones["heel.02.L"].roll = 0.0000
    bpy.context.active_object.data.edit_bones["shoulder.L"].roll = -0.006807
    bpy.context.active_object.data.edit_bones["upper_arm.L"].roll = 0.037177
    bpy.context.active_object.data.edit_bones["forearm.L"].roll = 1.635199
    bpy.context.active_object.data.edit_bones["hand.L"].roll = -0.001864
    bpy.context.active_object.data.edit_bones["thumb.01.L"].roll = 3.296754
    bpy.context.active_object.data.edit_bones["thumb.02.L"].roll = 1.938887
    bpy.context.active_object.data.edit_bones["thumb.03.L"].roll = 2.002941
    bpy.context.active_object.data.edit_bones["palm.01.L"].roll = -0.406613
    bpy.context.active_object.data.edit_bones["f_index.01.L"].roll = 0.492358
    bpy.context.active_object.data.edit_bones["f_index.02.L"].roll = 1.188135
    bpy.context.active_object.data.edit_bones["f_index.03.L"].roll = 1.618493
    bpy.context.active_object.data.edit_bones["palm.02.L"].roll = -0.170279
    bpy.context.active_object.data.edit_bones["f_middle.01.L"].roll = 0.26428
    bpy.context.active_object.data.edit_bones["f_middle.02.L"].roll = 1.144632
    bpy.context.active_object.data.edit_bones["f_middle.03.L"].roll = 1.603266
    bpy.context.active_object.data.edit_bones["palm.03.L"].roll = -0.054727
    bpy.context.active_object.data.edit_bones["f_ring.01.L"].roll = 0.244636
    bpy.context.active_object.data.edit_bones["f_ring.02.L"].roll = 0.781639
    bpy.context.active_object.data.edit_bones["f_ring.03.L"].roll = 1.198028
    bpy.context.active_object.data.edit_bones["palm.04.L"].roll = 0.19465
    bpy.context.active_object.data.edit_bones["f_pinky.01.L"].roll = 0.185069
    bpy.context.active_object.data.edit_bones["f_pinky.02.L"].roll = 0.826136
    bpy.context.active_object.data.edit_bones["f_pinky.03.L"].roll = 0.997271
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def setGenesis2FemaleRolls(metarig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["head"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["neck"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["chest"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["spine"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["hips"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["thigh.L"].roll = -0.050401
    bpy.context.active_object.data.edit_bones["shin.L"].roll = -0.015987
    bpy.context.active_object.data.edit_bones["foot.L"].roll = 1.789502 #1.944836
    bpy.context.active_object.data.edit_bones["toe.L"].roll = 1.789502
    bpy.context.active_object.data.edit_bones["heel.L"].roll = 0.0939
    bpy.context.active_object.data.edit_bones["heel.02.L"].roll = 0.0000
    bpy.context.active_object.data.edit_bones["shoulder.L"].roll = -0.006807
    bpy.context.active_object.data.edit_bones["upper_arm.L"].roll = 0.037177
    bpy.context.active_object.data.edit_bones["forearm.L"].roll = 1.635199
    bpy.context.active_object.data.edit_bones["hand.L"].roll = -0.394818
    bpy.context.active_object.data.edit_bones["thumb.01.L"].roll = 3.296754
    bpy.context.active_object.data.edit_bones["thumb.02.L"].roll = 1.938887
    bpy.context.active_object.data.edit_bones["thumb.03.L"].roll = 2.002941
    bpy.context.active_object.data.edit_bones["palm.01.L"].roll = -0.152829
    bpy.context.active_object.data.edit_bones["f_index.01.L"].roll = -0.089205
    bpy.context.active_object.data.edit_bones["f_index.02.L"].roll = 0.446884
    bpy.context.active_object.data.edit_bones["f_index.03.L"].roll = 0.419287
    bpy.context.active_object.data.edit_bones["palm.02.L"].roll = -0.230173
    bpy.context.active_object.data.edit_bones["f_middle.01.L"].roll = -0.134652
    bpy.context.active_object.data.edit_bones["f_middle.02.L"].roll = 0.169072
    bpy.context.active_object.data.edit_bones["f_middle.03.L"].roll = 0.037349
    bpy.context.active_object.data.edit_bones["palm.03.L"].roll = -0.232888
    bpy.context.active_object.data.edit_bones["f_ring.01.L"].roll = -0.05762
    bpy.context.active_object.data.edit_bones["f_ring.02.L"].roll = 0.096312
    bpy.context.active_object.data.edit_bones["f_ring.03.L"].roll = 0.185756
    bpy.context.active_object.data.edit_bones["palm.04.L"].roll = -0.082646
    bpy.context.active_object.data.edit_bones["f_pinky.01.L"].roll = -0.235231
    bpy.context.active_object.data.edit_bones["f_pinky.02.L"].roll = 0.008269
    bpy.context.active_object.data.edit_bones["f_pinky.03.L"].roll = 0.182735
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def setGenesis2MaleRolls(metarig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["head"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["neck"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["chest"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["spine"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["hips"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["thigh.L"].roll = -0.050401
    bpy.context.active_object.data.edit_bones["shin.L"].roll = -0.015987
    bpy.context.active_object.data.edit_bones["foot.L"].roll = 1.658602
    bpy.context.active_object.data.edit_bones["toe.L"].roll = 1.658602 #2.005925
    bpy.context.active_object.data.edit_bones["heel.L"].roll = 0.0939
    bpy.context.active_object.data.edit_bones["heel.02.L"].roll = 0.0000
    bpy.context.active_object.data.edit_bones["shoulder.L"].roll = -0.006807
    bpy.context.active_object.data.edit_bones["upper_arm.L"].roll = 0.037177
    bpy.context.active_object.data.edit_bones["forearm.L"].roll = 1.635199
    bpy.context.active_object.data.edit_bones["hand.L"].roll = -0.394818
    bpy.context.active_object.data.edit_bones["thumb.01.L"].roll = 3.296754
    bpy.context.active_object.data.edit_bones["thumb.02.L"].roll = 1.938887
    bpy.context.active_object.data.edit_bones["thumb.03.L"].roll = 2.002941
    bpy.context.active_object.data.edit_bones["palm.01.L"].roll = -0.152829
    bpy.context.active_object.data.edit_bones["f_index.01.L"].roll = -0.089205
    bpy.context.active_object.data.edit_bones["f_index.02.L"].roll = 0.446884
    bpy.context.active_object.data.edit_bones["f_index.03.L"].roll = 0.419287
    bpy.context.active_object.data.edit_bones["palm.02.L"].roll = -0.230173
    bpy.context.active_object.data.edit_bones["f_middle.01.L"].roll = -0.134652
    bpy.context.active_object.data.edit_bones["f_middle.02.L"].roll = 0.169072
    bpy.context.active_object.data.edit_bones["f_middle.03.L"].roll = 0.037349
    bpy.context.active_object.data.edit_bones["palm.03.L"].roll = -0.232888
    bpy.context.active_object.data.edit_bones["f_ring.01.L"].roll = -0.05762
    bpy.context.active_object.data.edit_bones["f_ring.02.L"].roll = 0.096312
    bpy.context.active_object.data.edit_bones["f_ring.03.L"].roll = 0.185756
    bpy.context.active_object.data.edit_bones["palm.04.L"].roll = -0.082646
    bpy.context.active_object.data.edit_bones["f_pinky.01.L"].roll = -0.235231
    bpy.context.active_object.data.edit_bones["f_pinky.02.L"].roll = 0.008269
    bpy.context.active_object.data.edit_bones["f_pinky.03.L"].roll = 0.182735
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def setGenesis3FemaleRolls(metarig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["head"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["neck"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["chest"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["spine"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["hips"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["thigh.L"].roll = -0.050401
    bpy.context.active_object.data.edit_bones["shin.L"].roll = -0.015987
    bpy.context.active_object.data.edit_bones["foot.L"].roll = -1.210693
    bpy.context.active_object.data.edit_bones["toe.L"].roll = 1.538201
    bpy.context.active_object.data.edit_bones["heel.L"].roll = -0.0061
    bpy.context.active_object.data.edit_bones["heel.02.L"].roll = 0.0000
    bpy.context.active_object.data.edit_bones["shoulder.L"].roll = -0.006807
    bpy.context.active_object.data.edit_bones["upper_arm.L"].roll = 0.037177
    bpy.context.active_object.data.edit_bones["forearm.L"].roll = 1.635199
    bpy.context.active_object.data.edit_bones["hand.L"].roll = -0.009100
    bpy.context.active_object.data.edit_bones["thumb.01.L"].roll = 1.396754
    bpy.context.active_object.data.edit_bones["thumb.02.L"].roll = 1.538887
    bpy.context.active_object.data.edit_bones["thumb.03.L"].roll = 1.702941
    bpy.context.active_object.data.edit_bones["palm.01.L"].roll = 0.059231
    bpy.context.active_object.data.edit_bones["f_index.01.L"].roll = 0.107271
    bpy.context.active_object.data.edit_bones["f_index.02.L"].roll = 0.119477
    bpy.context.active_object.data.edit_bones["f_index.03.L"].roll = 0.044151
    bpy.context.active_object.data.edit_bones["palm.02.L"].roll = 0.025885
    bpy.context.active_object.data.edit_bones["f_middle.01.L"].roll = 0.045638
    bpy.context.active_object.data.edit_bones["f_middle.02.L"].roll = 0.167271
    bpy.context.active_object.data.edit_bones["f_middle.03.L"].roll = 0.029049
    bpy.context.active_object.data.edit_bones["palm.03.L"].roll = 0.038919
    bpy.context.active_object.data.edit_bones["f_ring.01.L"].roll = 0.078443
    bpy.context.active_object.data.edit_bones["f_ring.02.L"].roll = 0.090552
    bpy.context.active_object.data.edit_bones["f_ring.03.L"].roll = 0.03262
    bpy.context.active_object.data.edit_bones["palm.04.L"].roll = 0.110783
    bpy.context.active_object.data.edit_bones["f_pinky.01.L"].roll = 0.065368
    bpy.context.active_object.data.edit_bones["f_pinky.02.L"].roll = 0.061447
    bpy.context.active_object.data.edit_bones["f_pinky.03.L"].roll = -0.007734
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def setGenesis3MaleRolls(metarig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = metarig
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.context.active_object.data.edit_bones["head"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["neck"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["chest"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["spine"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["hips"].roll = 3.141593
    bpy.context.active_object.data.edit_bones["thigh.L"].roll = -0.050401
    bpy.context.active_object.data.edit_bones["shin.L"].roll = -0.015987
    bpy.context.active_object.data.edit_bones["foot.L"].roll = -1.210693
    bpy.context.active_object.data.edit_bones["toe.L"].roll = 1.538201
    bpy.context.active_object.data.edit_bones["heel.L"].roll = -0.0061
    bpy.context.active_object.data.edit_bones["heel.02.L"].roll = 0.0000
    bpy.context.active_object.data.edit_bones["shoulder.L"].roll = -0.006807
    bpy.context.active_object.data.edit_bones["upper_arm.L"].roll = 0.037177
    bpy.context.active_object.data.edit_bones["forearm.L"].roll = 1.635199
    bpy.context.active_object.data.edit_bones["hand.L"].roll = -0.009100
    bpy.context.active_object.data.edit_bones["thumb.01.L"].roll = 1.396754
    bpy.context.active_object.data.edit_bones["thumb.02.L"].roll = 1.538887
    bpy.context.active_object.data.edit_bones["thumb.03.L"].roll = 1.702941
    bpy.context.active_object.data.edit_bones["palm.01.L"].roll = 0.059231
    bpy.context.active_object.data.edit_bones["f_index.01.L"].roll = 0.107271
    bpy.context.active_object.data.edit_bones["f_index.02.L"].roll = 0.119477
    bpy.context.active_object.data.edit_bones["f_index.03.L"].roll = 0.044151
    bpy.context.active_object.data.edit_bones["palm.02.L"].roll = 0.025885
    bpy.context.active_object.data.edit_bones["f_middle.01.L"].roll = 0.045638
    bpy.context.active_object.data.edit_bones["f_middle.02.L"].roll = 0.167271
    bpy.context.active_object.data.edit_bones["f_middle.03.L"].roll = 0.029049
    bpy.context.active_object.data.edit_bones["palm.03.L"].roll = 0.038919
    bpy.context.active_object.data.edit_bones["f_ring.01.L"].roll = 0.078443
    bpy.context.active_object.data.edit_bones["f_ring.02.L"].roll = 0.090552
    bpy.context.active_object.data.edit_bones["f_ring.03.L"].roll = 0.03262
    bpy.context.active_object.data.edit_bones["palm.04.L"].roll = 0.110783
    bpy.context.active_object.data.edit_bones["f_pinky.01.L"].roll = 0.065368
    bpy.context.active_object.data.edit_bones["f_pinky.02.L"].roll = 0.061447
    bpy.context.active_object.data.edit_bones["f_pinky.03.L"].roll = -0.007734
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def joinFaceRig(faceRig, rigifyRig, g3):
    #we need to know if it's g3
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    faceRig.select = True
    rigifyRig.select = True
    bpy.context.scene.objects.active = rigifyRig
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode='EDIT')
    rigifyRig.data.edit_bones["DEF-eye.L"].parent = rigifyRig.data.edit_bones["DEF-head"]
    rigifyRig.data.edit_bones["DEF-eye.R"].parent = rigifyRig.data.edit_bones["DEF-head"]
    rigifyRig.data.edit_bones["IK-eyes_lookat"].parent = rigifyRig.data.edit_bones["DEF-head"]
    if(g3 == False):
        rigifyRig.data.edit_bones["DEF-tonguebase"].parent = rigifyRig.data.edit_bones["DEF-head"]
    else:
        rigifyRig.data.edit_bones["DEF-tongue.01"].parent = rigifyRig.data.edit_bones["DEF-head"]

    rigifyRig.data.edit_bones["DEF-eye.L"].layers = [False] * 23 + [True] + [False] * 8
    rigifyRig.data.edit_bones["DEF-eye.R"].layers = [False] * 23 + [True] + [False] * 8
    rigifyRig.data.edit_bones["IK-eye.L"].layers = [False] * 23 + [True] + [False] * 8
    rigifyRig.data.edit_bones["IK-eye.R"].layers = [False] * 23 + [True] + [False] * 8

    rigifyRig.data.edit_bones["IK-eyes_lookat"].layers = [False] * 22 + [True] + [False] * 9
    rigifyRig.data.edit_bones["DEF-tongue.01"].layers = [False] * 23 + [True] + [False] * 8
    rigifyRig.data.edit_bones["DEF-tongue.02"].layers = [False] * 23 + [True] + [False] * 8
    rigifyRig.data.edit_bones["DEF-tongue.03"].layers = [False] * 23 + [True] + [False] * 8
    rigifyRig.data.edit_bones["DEF-tongue.04"].layers = [False] * 23 + [True] + [False] * 8
    if(g3 == False):
        rigifyRig.data.edit_bones["DEF-tonguebase"].layers = [False] * 23 + [True] + [False] * 8
        rigifyRig.data.edit_bones["DEF-tongue.05"].layers = [False] * 23 + [True] + [False] * 8
        rigifyRig.data.edit_bones["DEF-tonguetip"].layers = [False] * 23 + [True] + [False] * 8


    bpy.context.object.data.layers[22] = True
    bpy.context.object.show_x_ray = True
    bpy.ops.object.mode_set(mode='OBJECT')

def parentWGTs():
    bpy.ops.object.mode_set(mode='OBJECT')
    objNameList = bpy.data.objects.keys()
    wgtList = []
    for name in objNameList:
        obj = bpy.data.objects[name]
        if (name.startswith("WGT-")):
            wgtList.append(obj)

    if (len(wgtList) > 0):
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        wgtParent = bpy.context.active_object
        wgtParent.name = "WGTs"
        for obj in wgtList:
            obj.parent = wgtParent



#-------------------------------------------------------------

def mixVgroups(obj, vgroupA, vgroupB):
    if ((vgroupA in obj.vertex_groups.keys()) and (vgroupB in obj.vertex_groups.keys())):
        backupName = vgroupA + "_copy"
        if (backupName not in obj.vertex_groups.keys()):
            #Create backup
            bpy.ops.object.vertex_group_set_active(group=vgroupA)
            bpy.ops.object.vertex_group_copy()

        bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_MIX')
        #to determine the name of the modifier just created
        length = len(obj.modifiers.keys())
        index = length - 1
        mod_name = obj.modifiers[index].name

        obj.modifiers[mod_name].vertex_group_a = vgroupA
        obj.modifiers[mod_name].vertex_group_b = vgroupB
        obj.modifiers[mod_name].mix_mode = 'ADD'
        obj.modifiers[mod_name].mix_set = 'OR'
        bpy.ops.object.modifier_apply(modifier=mod_name)

def renameVgroups(obj, oldname, newname):
    if (oldname in obj.vertex_groups.keys()):
        obj.vertex_groups[oldname].name = newname

def setupArmatureModifier(obj, rigifyRig):
    if (len(obj.modifiers.keys()) > 0):
        for modifierName in obj.modifiers.keys():
            if (obj.modifiers[modifierName].type == 'ARMATURE'):
                obj.modifiers["Armature"].use_deform_preserve_volume = True
                if (rigifyRig.name in bpy.context.scene.objects.keys()):
                    obj.modifiers["Armature"].object = rigifyRig



#------------------------------------------------------------------

def checkForMatName(obj, checkName):
    objMatList = obj.material_slots.keys()
    for key in objMatList:
        if (key == checkName):
            #normally, this checkpoint should be useless.
            #the next checkpoint should handle this possibility by itself.
            #I think it's a bug or sth...
            return key
        if (key.startswith(checkName)):
            if (isNameExtension(key, checkName)):
                return key
    return None

def setupSpecTex(mat, name):
    mat.texture_slots[0].texture.name = name+"-COL"
    texName = name+"-SPEC"
    matList = bpy.context.active_object.material_slots.keys()
    index = matList.index(name)
    bpy.context.object.active_material_index = index
    texCount = len(mat.texture_slots.keys())
    #bpy.context.object.active_material.active_texture_index = texCount
    tex = bpy.data.textures.new(texName, 'IMAGE')
    mat.texture_slots.add()
    mat.texture_slots[texCount].texture = tex
    image = mat.texture_slots[texCount-1].texture.image
    mat.texture_slots[texCount].texture.type = 'IMAGE'
    mat.texture_slots[texCount].texture.image = image
    mat.texture_slots[texCount].texture_coords = 'UV'
    mat.texture_slots[texCount].use_map_color_diffuse = False
    mat.texture_slots[texCount].use_map_specular = True
    mat.texture_slots[texCount].use_rgb_to_intensity = True

def setupBumpTex(mat, name):
    mat.texture_slots[0].texture.name = name+"-COL"
    texName = name+"-BUMP"
    matList = bpy.context.active_object.material_slots.keys()
    index = matList.index(name)
    bpy.context.object.active_material_index = index
    texCount = len(mat.texture_slots.keys())
    #bpy.context.object.active_material.active_texture_index = texCount
    tex = bpy.data.textures.new(texName, 'IMAGE')
    mat.texture_slots.add()
    mat.texture_slots[texCount].texture = tex
    image = mat.texture_slots[texCount-1].texture.image
    mat.texture_slots[texCount].texture.type = 'IMAGE'
    mat.texture_slots[texCount].texture.image = image
    mat.texture_slots[texCount].texture_coords = 'UV'
    mat.texture_slots[texCount].use_map_color_diffuse = False
    mat.texture_slots[texCount].use_map_normal = True
    mat.texture_slots[texCount].normal_factor = 0.05
    mat.texture_slots[texCount].use_rgb_to_intensity = True

def genMatMergeList(obj, originalMatList):
    matList = obj.material_slots.keys()
    originalMatListLength = len(originalMatList)
    for m in range(0, originalMatListLength-1):
        n = len(obj.material_slots[m].material.texture_slots.keys())
        if (n == 0):
            index = matList.index(originalMatList[m])
            del matList[index]
        elif (obj.material_slots[m].material.texture_slots[0].texture.type != 'IMAGE'):
            index = matList.index(originalMatList[m])
            del matList[index]
    return matList

def mergeMats(obj, originalMatList):
    matList = genMatMergeList(obj, originalMatList)
    terminationList = []
    checkList = []
    for mainMat in matList:
        if (mainMat not in checkList):
            originalIndex = originalMatList.index(mainMat)
            image = obj.material_slots[mainMat].material.texture_slots[0].texture.image
            for childMat in matList:
                if (childMat not in checkList):
                    if (childMat != mainMat):
                        childIndex = originalMatList.index(childMat)
                        if (obj.material_slots[childMat].material.texture_slots[0].texture.image == image):
                            extractMat(obj, originalIndex, childIndex)
                            checkList.append(childMat)
                            terminationList.append(childMat)
        checkList.append(mainMat)

    delMaterial(obj, terminationList, originalMatList)

def extractMat(obj, mainMatIndex, childMatIndex):
    #bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.context.scene.objects.active = obj
    obj.active_material_index = childMatIndex
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.material_slot_select()
    obj.active_material_index = mainMatIndex
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def delMaterial(obj, terminationList, originalMatList):
    bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.context.scene.objects.active = obj
    for m in terminationList:
        index = originalMatList.index(m)
        obj.active_material_index = index
        del originalMatList[index]
        bpy.ops.object.material_slot_remove()

def texturesOff(obj):
    matCount = len(obj.material_slots.keys())
    if (matCount > 0):
        for matSlot in obj.material_slots:
            matSlot.material.use_textures = [False] * 18

def texturesOn(obj):
    matCount = len(obj.material_slots.keys())
    if (matCount > 0):
        for matSlot in obj.material_slots:
            matSlot.material.use_textures = [True] * 18

def materialsRemove(obj):
    matCount = len(obj.material_slots.keys())
    if (matCount > 0):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = obj
        for i in range(0, matCount):
            bpy.ops.object.material_slot_remove()


#============================================================================
# DEFINE OPERATORS
#============================================================================


class GenesisRigifySetup(bpy.types.Operator):
    """Generate and setup a rigify rig for the active Genesis figure"""
    bl_idname = "object.khalibloo_genesis_rigify_setup"
    bl_label = "Rigify"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'MESH'))

    def execute(self, context):
        genesis = bpy.context.active_object
        global rigifyRig
        global genesisRig

        if (genesis.find_armature() is not None):
            if (len(genesis.data.vertices.items()) == 19296):
                genesisRig = bpy.context.active_object.find_armature()

                genesisRig.hide = False
                bpy.context.scene.layers[findLayer(genesisRig)] = True


                #VERTEX GROUPS RAW DATA
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(bpy.data.meshes[genesis.data.name])

                head_tail = [3189, 3230]
                chest_head = [181, 182, 183, 184, 189, 190, 192, 3956, 3957, 4111, 4170, 4501,
                              4503, 4514, 4675, 4738, 4744, 4770, 4773, 4782, 4783, 4784,
                                4785, 4794, 4801, 4830, 4989, 4997, 4998, 4999, 5001, 5003,
                                5005, 5006, 5008, 5009, 5010, 5011, 5013, 5014, 5015, 5028,
                                6425, 6426, 6427, 6428, 6482, 6485, 6494, 6495, 6506, 6516,
                                6517, 6518, 6519, 9617, 9618, 9619, 9620, 9625, 9626, 9628,
                                13267, 13268, 13421, 13474, 13783, 13785, 13796, 13950, 14011,
                                14017, 14043, 14046, 14055, 14056, 14057, 14058, 14067, 14074,
                                14103, 14249, 14257, 14258, 14259, 14261, 14263, 14265, 14266,
                                14268, 14269, 14270, 14271, 14273, 14274, 14285, 15648, 15649,
                                15650, 15651, 15705, 15708, 15717, 15718, 15729, 15739, 15740,
                                15741, 15742]
                spine_head = [3943, 4834, 4870, 4973, 4986, 5063, 5068, 5074, 5075, 5076, 5077,
                              5078, 5079, 5080, 5081, 5082, 5083, 5084, 5085, 5086, 5087, 5088,
                              5089, 5090, 5100, 5108, 5109, 5110, 5111, 5112, 5113, 5114, 5115,
                              5116, 5117, 5118, 5119, 5120, 5121, 5122, 5123, 5124, 6522, 6523,
                              6524, 6525, 13254, 14107, 14140, 14233, 14246, 14318, 14323, 14329,
                              14330, 14331, 14332, 14333, 14334, 14335, 14336, 14337, 14338, 14339,
                              14340, 14341, 14342, 14343, 14344, 14354, 14359, 14360, 14361, 14362,
                              14363, 14364, 14365, 14366, 14367, 14368, 14369, 14370, 14371, 14372,
                              14373, 14374, 15745, 15746, 15747, 15748]
                hips_head = [166, 454, 483, 484, 485, 486, 487, 488, 489, 491, 492, 502, 507, 510,
                            511, 539, 542, 608, 609, 610, 611, 612, 613, 3780, 3781, 3837, 3920,
                            3923, 3932, 3933, 4365, 6466, 6467, 6472, 6473, 9272, 9277, 9602, 9890,
                            9919, 9920, 9921, 9922, 9923, 9924, 9925, 9927, 9928, 9938, 9943, 9946,
                            9947, 9975, 9978, 10044, 10045, 10046, 10047, 10048, 10049, 13091, 13092,
                            13148, 13231, 13234, 13243, 13244, 13659, 15689, 15690, 15695, 15696,
                            18426, 18431]
                toe_tail_L = [1288]
                heel_tail_L = [6575, 6586]
                heel02_head_L = [289]
                heel02_tail_L = [1410, 1451]
                hand_tail_L = [1561, 1742, 1779, 1781, 1783, 5140, 6400, 6643, 6644]
                thumbtip_L = [1602, 1603]
                indextip_L = [5778, 5850]
                midtip_L = [5926, 5998]
                ringtip_L = [6074, 6146]
                pinkytip_L = [6222, 6294]
                indexcarp_L = [1646, 1686, 1689, 1690, 1830, 1841, 1852, 1874, 6642]
                midcarp_L = [1584, 1670, 1751, 1796, 1798, 1801, 1809, 1873, 1874, 1875]
                ringcarp_L = [1648, 1666, 1693, 1695, 1696, 1697, 1767, 1768, 1788, 1791, 1801, 6404]
                pinkycarp_L = [1668, 1692, 1693, 1713, 1791, 1794]
                #face rig
                eye_head_L = [3385, 3386, 3389, 3391, 3393, 3395, 3397, 3399, 3401, 3403, 3405, 3407,
                              3409, 3411, 3413, 3415]
                eye_head_R = [12700, 12701, 12704, 12706, 12708, 12710, 12712, 12714, 12716, 12718,
                              12720, 12722, 12724, 12726, 12728, 12730]
                eye_tail_L = [3516]
                eye_tail_R = [12831]
                tonguetip_tail = [7342]

                createVgroup(genesis, bm, "metarig_head_tail", head_tail)
                createVgroup(genesis, bm, "metarig_chest_head", chest_head)
                createVgroup(genesis, bm, "metarig_spine_head", spine_head)
                createVgroup(genesis, bm, "metarig_hips_head", hips_head)
                createVgroup(genesis, bm, "metarig_toe_tail.L", toe_tail_L)
                createVgroup(genesis, bm, "metarig_heel_tail.L", heel_tail_L)
                createVgroup(genesis, bm, "metarig_heel02_head.L", heel02_head_L)
                createVgroup(genesis, bm, "metarig_heel02_tail.L", heel02_tail_L)
                createVgroup(genesis, bm, "metarig_hand_tail.L", hand_tail_L)
                createVgroup(genesis, bm, "metarig_thumbtip.L", thumbtip_L)
                createVgroup(genesis, bm, "metarig_indextip.L", indextip_L)
                createVgroup(genesis, bm, "metarig_midtip.L", midtip_L)
                createVgroup(genesis, bm, "metarig_ringtip.L", ringtip_L)
                createVgroup(genesis, bm, "metarig_pinkytip.L", pinkytip_L)
                createVgroup(genesis, bm, "metarig_indexcarp.L", indexcarp_L)
                createVgroup(genesis, bm, "metarig_midcarp.L", midcarp_L)
                createVgroup(genesis, bm, "metarig_ringcarp.L", ringcarp_L)
                createVgroup(genesis, bm, "metarig_pinkycarp.L", pinkycarp_L)
                #face rig
                createVgroup(genesis, bm, "metarig_eye_head.L", eye_head_L)
                createVgroup(genesis, bm, "metarig_eye_head.R", eye_head_R)
                createVgroup(genesis, bm, "metarig_eye_tail.L", eye_tail_L)
                createVgroup(genesis, bm, "metarig_eye_tail.R", eye_tail_R)
                createVgroup(genesis, bm, "metarig_tonguetip_tail", tonguetip_tail)

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.view3d.snap_cursor_to_center()
                try:
                    bpy.ops.object.armature_human_metarig_add()
                except AttributeError:
                    self.report({'ERROR'}, "Missing Addon: 'Rigify'")
                    return {'CANCELLED'}
                except:
                    self.report({'ERROR'}, "Rigify: Broken... Something's wrong with Rigify. Please report this")
                    return {'CANCELLED'}
                metarig = bpy.context.active_object

                metarigPrep(metarig)

                copyMeshPos(metarig, genesis, "head", "tail", "metarig_head_tail")
                copyMeshPos(metarig, genesis, "chest", "head", "metarig_chest_head")
                copyMeshPos(metarig, genesis, "spine", "head", "metarig_spine_head")
                copyMeshPos(metarig, genesis, "hips", "head", "metarig_hips_head")
                copyMeshPos(metarig, genesis, "toe.L", "tail", "metarig_toe_tail.L")
                copyMeshPos(metarig, genesis, "heel.L", "tail", "metarig_heel_tail.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "head", "metarig_heel02_head.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "tail", "metarig_heel02_tail.L")
                copyMeshPos(metarig, genesis, "hand.L", "tail", "metarig_hand_tail.L")
                copyMeshPos(metarig, genesis, "thumb.03.L", "tail", "metarig_thumbtip.L")
                copyMeshPos(metarig, genesis, "f_index.03.L", "tail", "metarig_indextip.L")
                copyMeshPos(metarig, genesis, "f_middle.03.L", "tail", "metarig_midtip.L")
                copyMeshPos(metarig, genesis, "f_ring.03.L", "tail", "metarig_ringtip.L")
                copyMeshPos(metarig, genesis, "f_pinky.03.L", "tail", "metarig_pinkytip.L")
                copyMeshPos(metarig, genesis, "palm.01.L", "head", "metarig_indexcarp.L")
                copyMeshPos(metarig, genesis, "palm.02.L", "head", "metarig_midcarp.L")
                copyMeshPos(metarig, genesis, "palm.03.L", "head", "metarig_ringcarp.L")
                copyMeshPos(metarig, genesis, "palm.04.L", "head", "metarig_pinkycarp.L")

                copyBonePos(metarig, genesisRig, "neck", "head", "neck")
                copyBonePos(metarig, genesisRig, "neck", "tail", "neck")
                copyBonePos(metarig, genesisRig, "thigh.L", "head", "lThigh")
                copyBonePos(metarig, genesisRig, "shin.L", "head", "lShin")
                copyBonePos(metarig, genesisRig, "shin.L", "tail", "lShin")
                #copyBonePos(metarig, genesisRig, "foot.L", "head", "lFoot")
                copyBonePos(metarig, genesisRig, "toe.L", "head", "lToe")
                copyBonePos(metarig, genesisRig, "shoulder.L", "head", "lCollar")
                copyBonePos(metarig, genesisRig, "shoulder.L", "tail", "lCollar")
                copyBonePos(metarig, genesisRig, "upper_arm.L", "head", "lShldr")
                copyBonePos(metarig, genesisRig, "forearm.L", "head", "lForeArm")
                copyBonePos(metarig, genesisRig, "forearm.L", "tail", "lForeArm")
                copyBonePos(metarig, genesisRig, "thumb.01.L", "head", "lThumb1")
                copyBonePos(metarig, genesisRig, "thumb.02.L", "head", "lThumb2")
                copyBonePos(metarig, genesisRig, "thumb.03.L", "head", "lThumb3")
                copyBonePos(metarig, genesisRig, "f_index.01.L", "head", "lIndex1")
                copyBonePos(metarig, genesisRig, "f_index.02.L", "head", "lIndex2")
                copyBonePos(metarig, genesisRig, "f_index.03.L", "head", "lIndex3")
                copyBonePos(metarig, genesisRig, "f_middle.01.L", "head", "lMid1")
                copyBonePos(metarig, genesisRig, "f_middle.02.L", "head", "lMid2")
                copyBonePos(metarig, genesisRig, "f_middle.03.L", "head", "lMid3")
                copyBonePos(metarig, genesisRig, "f_ring.01.L", "head", "lRing1")
                copyBonePos(metarig, genesisRig, "f_ring.02.L", "head", "lRing2")
                copyBonePos(metarig, genesisRig, "f_ring.03.L", "head", "lRing3")
                copyBonePos(metarig, genesisRig, "f_pinky.01.L", "head", "lPinky1")
                copyBonePos(metarig, genesisRig, "f_pinky.02.L", "head", "lPinky2")
                copyBonePos(metarig, genesisRig, "f_pinky.03.L", "head", "lPinky3")

                metarigFinishingTouches(metarig)
                setGenesisRolls(metarig)

                delVgroup(genesis, "metarig_head_tail")
                delVgroup(genesis, "metarig_chest_head")
                delVgroup(genesis, "metarig_spine_head")
                delVgroup(genesis, "metarig_hips_head")
                delVgroup(genesis, "metarig_toe_tail.L")
                delVgroup(genesis, "metarig_heel_tail.L")
                delVgroup(genesis, "metarig_heel02_head.L")
                delVgroup(genesis, "metarig_heel02_tail.L")
                delVgroup(genesis, "metarig_hand_tail.L")
                delVgroup(genesis, "metarig_thumbtip.L")
                delVgroup(genesis, "metarig_indextip.L")
                delVgroup(genesis, "metarig_midtip.L")
                delVgroup(genesis, "metarig_ringtip.L")
                delVgroup(genesis, "metarig_pinkytip.L")
                delVgroup(genesis, "metarig_indexcarp.L")
                delVgroup(genesis, "metarig_midcarp.L")
                delVgroup(genesis, "metarig_ringcarp.L")
                delVgroup(genesis, "metarig_pinkycarp.L")

                #face rig
                faceRig = createFaceRig(False)
                #print(faceRig.name)
                faceRigSetParents(faceRig, False)
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "tail", "metarig_eye_tail.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "tail", "metarig_eye_tail.R")
                copyMeshPos(faceRig, genesis, "DEF-tonguetip", "tail", "metarig_tonguetip_tail")

                copyBonePos(faceRig, genesisRig, "DEF-tonguebase", "head", "tongueBase")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.01", "head", "tongue01")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.02", "head", "tongue02")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.03", "head", "tongue03")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.04", "head", "tongue04")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.05", "head", "tongue05")
                copyBonePos(faceRig, genesisRig, "DEF-tonguetip", "head", "tongueTip")
                faceRigFinishingTouches(faceRig)

                delVgroup(genesis, "metarig_eye_head.L")
                delVgroup(genesis, "metarig_eye_head.R")
                delVgroup(genesis, "metarig_eye_tail.L")
                delVgroup(genesis, "metarig_eye_tail.R")
                delVgroup(genesis, "metarig_tonguetip_tail")

                bpy.ops.view3d.snap_cursor_to_center()
                bpy.context.scene.objects.active = metarig
                bpy.ops.pose.rigify_generate()
                rigifyRig = bpy.context.active_object
                rigifyRig.name = genesis.name + "-rig"
                #fix neck issue
                bpy.ops.object.khalibloo_rigify_neck_fix()
                parentWGTs()

                joinFaceRig(faceRig, rigifyRig, False)
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = genesis
                genesis.select = True
        return {'FINISHED'}

class Genesis2FemaleRigifySetup(bpy.types.Operator):
    """Generate and setup a rigify rig for the active Genesis 2 Female figure"""
    bl_idname = "object.khalibloo_genesis2female_rigify_setup"
    bl_label = "Rigify"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'MESH'))

    def execute(self, context):
        genesis = bpy.context.active_object
        global rigifyRig
        global genesisRig

        if (genesis.find_armature() is not None):
            if (len(genesis.data.vertices.items()) == 21556):
                genesisRig = bpy.context.active_object.find_armature()

                genesisRig.hide = False
                bpy.context.scene.layers[findLayer(genesisRig)] = True


                #VERTEX GROUPS RAW DATA
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(bpy.data.meshes[genesis.data.name])

                head_tail = [2054, 2087]
                chest_head = [10671, 21322]
                spine_head = [2926, 13724]
                hips_head = [7848, 18528]
                toe_tail_L = [789]
                heel_tail_L = [4128, 4133]
                heel02_head_L = [9337]
                heel02_tail_L = [8623]
                hand_tail_L = [1076, 2957, 3988, 4176, 9423, 9445, 9446]
                thumbtip_L = [964, 965]
                indextip_L = [3380, 3452]
                midtip_L = [3528, 3600]
                ringtip_L = [3676, 3748]
                pinkytip_L = [3824, 3896]
                indexcarp_L = [9404, 9409, 9692]
                midcarp_L = [1085, 9430, 9437]
                ringcarp_L = [1083, 9459, 9465]
                pinkycarp_L = [1008, 9484, 9515]
                #face rig
                eye_head_L = [2191, 2192, 2195, 2197, 8267, 8268, 8271, 8273, 8301, 8323, 8325, 8327, 8357, 8359, 8361, 8382]
                eye_head_R = [13023, 13024, 13027, 13029, 18938, 18939, 18942, 18944, 18972, 18994, 18996, 18998, 19028,
                              19030, 19032, 19053]
                eye_tail_L = [8313]
                eye_tail_R = [18984]
                tonguetip_tail = [4863]

                createVgroup(genesis, bm, "metarig_head_tail", head_tail)
                createVgroup(genesis, bm, "metarig_chest_head", chest_head)
                createVgroup(genesis, bm, "metarig_spine_head", spine_head)
                createVgroup(genesis, bm, "metarig_hips_head", hips_head)
                createVgroup(genesis, bm, "metarig_toe_tail.L", toe_tail_L)
                createVgroup(genesis, bm, "metarig_heel_tail.L", heel_tail_L)
                createVgroup(genesis, bm, "metarig_heel02_head.L", heel02_head_L)
                createVgroup(genesis, bm, "metarig_heel02_tail.L", heel02_tail_L)
                createVgroup(genesis, bm, "metarig_hand_tail.L", hand_tail_L)
                createVgroup(genesis, bm, "metarig_thumbtip.L", thumbtip_L)
                createVgroup(genesis, bm, "metarig_indextip.L", indextip_L)
                createVgroup(genesis, bm, "metarig_midtip.L", midtip_L)
                createVgroup(genesis, bm, "metarig_ringtip.L", ringtip_L)
                createVgroup(genesis, bm, "metarig_pinkytip.L", pinkytip_L)
                createVgroup(genesis, bm, "metarig_indexcarp.L", indexcarp_L)
                createVgroup(genesis, bm, "metarig_midcarp.L", midcarp_L)
                createVgroup(genesis, bm, "metarig_ringcarp.L", ringcarp_L)
                createVgroup(genesis, bm, "metarig_pinkycarp.L", pinkycarp_L)
                #face rig
                createVgroup(genesis, bm, "metarig_eye_head.L", eye_head_L)
                createVgroup(genesis, bm, "metarig_eye_head.R", eye_head_R)
                createVgroup(genesis, bm, "metarig_eye_tail.L", eye_tail_L)
                createVgroup(genesis, bm, "metarig_eye_tail.R", eye_tail_R)
                createVgroup(genesis, bm, "metarig_tonguetip_tail", tonguetip_tail)

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.view3d.snap_cursor_to_center()
                try:
                    bpy.ops.object.armature_human_metarig_add()
                except AttributeError:
                    self.report({'ERROR'}, "Missing Addon: 'Rigify'")
                    return {'CANCELLED'}
                except:
                    self.report({'ERROR'}, "Rigify: Broken... Something's wrong with Rigify. Please report this")
                    return {'CANCELLED'}
                metarig = bpy.context.active_object

                metarigPrep(metarig)

                copyMeshPos(metarig, genesis, "head", "tail", "metarig_head_tail")
                copyMeshPos(metarig, genesis, "chest", "head", "metarig_chest_head")
                copyMeshPos(metarig, genesis, "spine", "head", "metarig_spine_head")
                copyMeshPos(metarig, genesis, "hips", "head", "metarig_hips_head")
                copyMeshPos(metarig, genesis, "toe.L", "tail", "metarig_toe_tail.L")
                copyMeshPos(metarig, genesis, "heel.L", "tail", "metarig_heel_tail.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "head", "metarig_heel02_head.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "tail", "metarig_heel02_tail.L")
                copyMeshPos(metarig, genesis, "hand.L", "tail", "metarig_hand_tail.L")
                copyMeshPos(metarig, genesis, "thumb.03.L", "tail", "metarig_thumbtip.L")
                copyMeshPos(metarig, genesis, "f_index.03.L", "tail", "metarig_indextip.L")
                copyMeshPos(metarig, genesis, "f_middle.03.L", "tail", "metarig_midtip.L")
                copyMeshPos(metarig, genesis, "f_ring.03.L", "tail", "metarig_ringtip.L")
                copyMeshPos(metarig, genesis, "f_pinky.03.L", "tail", "metarig_pinkytip.L")
                copyMeshPos(metarig, genesis, "palm.01.L", "head", "metarig_indexcarp.L")
                copyMeshPos(metarig, genesis, "palm.02.L", "head", "metarig_midcarp.L")
                copyMeshPos(metarig, genesis, "palm.03.L", "head", "metarig_ringcarp.L")
                copyMeshPos(metarig, genesis, "palm.04.L", "head", "metarig_pinkycarp.L")

                copyBonePos(metarig, genesisRig, "neck", "head", "neck")
                copyBonePos(metarig, genesisRig, "neck", "tail", "neck")
                copyBonePos(metarig, genesisRig, "thigh.L", "head", "lThigh")
                copyBonePos(metarig, genesisRig, "shin.L", "head", "lShin")
                copyBonePos(metarig, genesisRig, "shin.L", "tail", "lShin")
                #copyBonePos(metarig, genesisRig, "foot.L", "head", "lFoot")
                copyBonePos(metarig, genesisRig, "toe.L", "head", "lToe")
                copyBonePos(metarig, genesisRig, "shoulder.L", "head", "lCollar")
                copyBonePos(metarig, genesisRig, "shoulder.L", "tail", "lCollar")
                copyBonePos(metarig, genesisRig, "upper_arm.L", "head", "lShldr")
                copyBonePos(metarig, genesisRig, "forearm.L", "head", "lForeArm")
                copyBonePos(metarig, genesisRig, "forearm.L", "tail", "lForeArm")
                copyBonePos(metarig, genesisRig, "thumb.01.L", "head", "lThumb1")
                copyBonePos(metarig, genesisRig, "thumb.02.L", "head", "lThumb2")
                copyBonePos(metarig, genesisRig, "thumb.03.L", "head", "lThumb3")
                copyBonePos(metarig, genesisRig, "f_index.01.L", "head", "lIndex1")
                copyBonePos(metarig, genesisRig, "f_index.02.L", "head", "lIndex2")
                copyBonePos(metarig, genesisRig, "f_index.03.L", "head", "lIndex3")
                copyBonePos(metarig, genesisRig, "f_middle.01.L", "head", "lMid1")
                copyBonePos(metarig, genesisRig, "f_middle.02.L", "head", "lMid2")
                copyBonePos(metarig, genesisRig, "f_middle.03.L", "head", "lMid3")
                copyBonePos(metarig, genesisRig, "f_ring.01.L", "head", "lRing1")
                copyBonePos(metarig, genesisRig, "f_ring.02.L", "head", "lRing2")
                copyBonePos(metarig, genesisRig, "f_ring.03.L", "head", "lRing3")
                copyBonePos(metarig, genesisRig, "f_pinky.01.L", "head", "lPinky1")
                copyBonePos(metarig, genesisRig, "f_pinky.02.L", "head", "lPinky2")
                copyBonePos(metarig, genesisRig, "f_pinky.03.L", "head", "lPinky3")
                metarigFinishingTouches(metarig)
                setGenesis2FemaleRolls(metarig)

                delVgroup(genesis, "metarig_head_tail")
                delVgroup(genesis, "metarig_chest_head")
                delVgroup(genesis, "metarig_spine_head")
                delVgroup(genesis, "metarig_hips_head")
                delVgroup(genesis, "metarig_toe_tail.L")
                delVgroup(genesis, "metarig_heel_tail.L")
                delVgroup(genesis, "metarig_heel02_head.L")
                delVgroup(genesis, "metarig_heel02_tail.L")
                delVgroup(genesis, "metarig_hand_tail.L")
                delVgroup(genesis, "metarig_thumbtip.L")
                delVgroup(genesis, "metarig_indextip.L")
                delVgroup(genesis, "metarig_midtip.L")
                delVgroup(genesis, "metarig_ringtip.L")
                delVgroup(genesis, "metarig_pinkytip.L")
                delVgroup(genesis, "metarig_indexcarp.L")
                delVgroup(genesis, "metarig_midcarp.L")
                delVgroup(genesis, "metarig_ringcarp.L")
                delVgroup(genesis, "metarig_pinkycarp.L")

                #face rig
                faceRig = createFaceRig(False)
                #print(faceRig.name)
                faceRigSetParents(faceRig, False)
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "tail", "metarig_eye_tail.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "tail", "metarig_eye_tail.R")
                copyMeshPos(faceRig, genesis, "DEF-tonguetip", "tail", "metarig_tonguetip_tail")

                copyBonePos(faceRig, genesisRig, "DEF-tonguebase", "head", "tongueBase")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.01", "head", "tongue01")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.02", "head", "tongue02")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.03", "head", "tongue03")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.04", "head", "tongue04")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.05", "head", "tongue05")
                copyBonePos(faceRig, genesisRig, "DEF-tonguetip", "head", "tongueTip")
                faceRigFinishingTouches(faceRig)

                delVgroup(genesis, "metarig_eye_head.L")
                delVgroup(genesis, "metarig_eye_head.R")
                delVgroup(genesis, "metarig_eye_tail.L")
                delVgroup(genesis, "metarig_eye_tail.R")
                delVgroup(genesis, "metarig_tonguetip_tail")

                bpy.ops.view3d.snap_cursor_to_center()
                bpy.context.scene.objects.active = metarig
                bpy.ops.pose.rigify_generate()
                rigifyRig = bpy.context.active_object
                rigifyRig.name = genesis.name + "-rig"
                #fix neck issue
                bpy.ops.object.khalibloo_rigify_neck_fix()
                parentWGTs()

                joinFaceRig(faceRig, rigifyRig, False)
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = genesis
                genesis.select = True
        return {'FINISHED'}

class Genesis2MaleRigifySetup(bpy.types.Operator):
    """Generate and setup a rigify rig for the active Genesis 2 Male figure"""
    bl_idname = "object.khalibloo_genesis2male_rigify_setup"
    bl_label = "Rigify"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'MESH'))

    def execute(self, context):
        genesis = bpy.context.active_object
        global rigifyRig
        global genesisRig

        if (genesis.find_armature() is not None):
            if (len(genesis.data.vertices.items()) == 21556):
                genesisRig = bpy.context.active_object.find_armature()

                genesisRig.hide = False
                bpy.context.scene.layers[findLayer(genesisRig)] = True


                #VERTEX GROUPS RAW DATA
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(bpy.data.meshes[genesis.data.name])

                head_tail = [2054, 2087]
                chest_head = [10459, 21116]
                spine_head = [2926, 13724]
                hips_head = [7872, 18552]
                toe_tail_L = [789]
                heel_tail_L = [4128, 4133]
                heel02_head_L = [9334]
                heel02_tail_L = [867, 8623]
                hand_tail_L = [1076, 2957, 3988, 4176, 9423, 9445, 9446]
                thumbtip_L = [964, 965]
                indextip_L = [3380, 3452]
                midtip_L = [3528, 3600]
                ringtip_L = [3676, 3748]
                pinkytip_L = [3824, 3896]
                indexcarp_L = [9404, 9409, 9692]
                midcarp_L = [1085, 9430, 9437]
                ringcarp_L = [1083, 9459, 9465]
                pinkycarp_L = [1008, 9484, 9515]
                #face rig
                eye_head_L = [2191, 2192, 2195, 2197, 8267, 8268, 8271, 8273, 8301, 8323, 8325, 8327, 8357, 8359, 8361, 8382]
                eye_head_R = [13023, 13024, 13027, 13029, 18938, 18939, 18942, 18944, 18972, 18994, 18996, 18998, 19028,
                              19030, 19032, 19053]
                eye_tail_L = [8313]
                eye_tail_R = [18984]
                tonguetip_tail = [4863]

                createVgroup(genesis, bm, "metarig_head_tail", head_tail)
                createVgroup(genesis, bm, "metarig_chest_head", chest_head)
                createVgroup(genesis, bm, "metarig_spine_head", spine_head)
                createVgroup(genesis, bm, "metarig_hips_head", hips_head)
                createVgroup(genesis, bm, "metarig_toe_tail.L", toe_tail_L)
                createVgroup(genesis, bm, "metarig_heel_tail.L", heel_tail_L)
                createVgroup(genesis, bm, "metarig_heel02_head.L", heel02_head_L)
                createVgroup(genesis, bm, "metarig_heel02_tail.L", heel02_tail_L)
                createVgroup(genesis, bm, "metarig_hand_tail.L", hand_tail_L)
                createVgroup(genesis, bm, "metarig_thumbtip.L", thumbtip_L)
                createVgroup(genesis, bm, "metarig_indextip.L", indextip_L)
                createVgroup(genesis, bm, "metarig_midtip.L", midtip_L)
                createVgroup(genesis, bm, "metarig_ringtip.L", ringtip_L)
                createVgroup(genesis, bm, "metarig_pinkytip.L", pinkytip_L)
                createVgroup(genesis, bm, "metarig_indexcarp.L", indexcarp_L)
                createVgroup(genesis, bm, "metarig_midcarp.L", midcarp_L)
                createVgroup(genesis, bm, "metarig_ringcarp.L", ringcarp_L)
                createVgroup(genesis, bm, "metarig_pinkycarp.L", pinkycarp_L)
                #face rig
                createVgroup(genesis, bm, "metarig_eye_head.L", eye_head_L)
                createVgroup(genesis, bm, "metarig_eye_head.R", eye_head_R)
                createVgroup(genesis, bm, "metarig_eye_tail.L", eye_tail_L)
                createVgroup(genesis, bm, "metarig_eye_tail.R", eye_tail_R)
                createVgroup(genesis, bm, "metarig_tonguetip_tail", tonguetip_tail)

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.view3d.snap_cursor_to_center()
                try:
                    bpy.ops.object.armature_human_metarig_add()
                except AttributeError:
                    self.report({'ERROR'}, "Missing Addon: 'Rigify'")
                    return {'CANCELLED'}
                except:
                    self.report({'ERROR'}, "Rigify: Broken... Something's wrong with Rigify. Please report this")
                    return {'CANCELLED'}
                metarig = bpy.context.active_object

                metarigPrep(metarig)

                copyMeshPos(metarig, genesis, "head", "tail", "metarig_head_tail")
                copyMeshPos(metarig, genesis, "chest", "head", "metarig_chest_head")
                copyMeshPos(metarig, genesis, "spine", "head", "metarig_spine_head")
                copyMeshPos(metarig, genesis, "hips", "head", "metarig_hips_head")
                copyMeshPos(metarig, genesis, "toe.L", "tail", "metarig_toe_tail.L")
                copyMeshPos(metarig, genesis, "heel.L", "tail", "metarig_heel_tail.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "head", "metarig_heel02_head.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "tail", "metarig_heel02_tail.L")
                copyMeshPos(metarig, genesis, "hand.L", "tail", "metarig_hand_tail.L")
                copyMeshPos(metarig, genesis, "thumb.03.L", "tail", "metarig_thumbtip.L")
                copyMeshPos(metarig, genesis, "f_index.03.L", "tail", "metarig_indextip.L")
                copyMeshPos(metarig, genesis, "f_middle.03.L", "tail", "metarig_midtip.L")
                copyMeshPos(metarig, genesis, "f_ring.03.L", "tail", "metarig_ringtip.L")
                copyMeshPos(metarig, genesis, "f_pinky.03.L", "tail", "metarig_pinkytip.L")
                copyMeshPos(metarig, genesis, "palm.01.L", "head", "metarig_indexcarp.L")
                copyMeshPos(metarig, genesis, "palm.02.L", "head", "metarig_midcarp.L")
                copyMeshPos(metarig, genesis, "palm.03.L", "head", "metarig_ringcarp.L")
                copyMeshPos(metarig, genesis, "palm.04.L", "head", "metarig_pinkycarp.L")

                copyBonePos(metarig, genesisRig, "neck", "head", "neck")
                copyBonePos(metarig, genesisRig, "neck", "tail", "neck")
                copyBonePos(metarig, genesisRig, "thigh.L", "head", "lThigh")
                copyBonePos(metarig, genesisRig, "shin.L", "head", "lShin")
                copyBonePos(metarig, genesisRig, "shin.L", "tail", "lShin")
                #copyBonePos(metarig, genesisRig, "foot.L", "head", "lFoot")
                copyBonePos(metarig, genesisRig, "toe.L", "head", "lToe")
                copyBonePos(metarig, genesisRig, "shoulder.L", "head", "lCollar")
                copyBonePos(metarig, genesisRig, "shoulder.L", "tail", "lCollar")
                copyBonePos(metarig, genesisRig, "upper_arm.L", "head", "lShldr")
                copyBonePos(metarig, genesisRig, "forearm.L", "head", "lForeArm")
                copyBonePos(metarig, genesisRig, "forearm.L", "tail", "lForeArm")
                copyBonePos(metarig, genesisRig, "thumb.01.L", "head", "lThumb1")
                copyBonePos(metarig, genesisRig, "thumb.02.L", "head", "lThumb2")
                copyBonePos(metarig, genesisRig, "thumb.03.L", "head", "lThumb3")
                copyBonePos(metarig, genesisRig, "f_index.01.L", "head", "lIndex1")
                copyBonePos(metarig, genesisRig, "f_index.02.L", "head", "lIndex2")
                copyBonePos(metarig, genesisRig, "f_index.03.L", "head", "lIndex3")
                copyBonePos(metarig, genesisRig, "f_middle.01.L", "head", "lMid1")
                copyBonePos(metarig, genesisRig, "f_middle.02.L", "head", "lMid2")
                copyBonePos(metarig, genesisRig, "f_middle.03.L", "head", "lMid3")
                copyBonePos(metarig, genesisRig, "f_ring.01.L", "head", "lRing1")
                copyBonePos(metarig, genesisRig, "f_ring.02.L", "head", "lRing2")
                copyBonePos(metarig, genesisRig, "f_ring.03.L", "head", "lRing3")
                copyBonePos(metarig, genesisRig, "f_pinky.01.L", "head", "lPinky1")
                copyBonePos(metarig, genesisRig, "f_pinky.02.L", "head", "lPinky2")
                copyBonePos(metarig, genesisRig, "f_pinky.03.L", "head", "lPinky3")
                metarigFinishingTouches(metarig)
                setGenesis2MaleRolls(metarig)

                delVgroup(genesis, "metarig_head_tail")
                delVgroup(genesis, "metarig_chest_head")
                delVgroup(genesis, "metarig_spine_head")
                delVgroup(genesis, "metarig_hips_head")
                delVgroup(genesis, "metarig_toe_tail.L")
                delVgroup(genesis, "metarig_heel_tail.L")
                delVgroup(genesis, "metarig_heel02_head.L")
                delVgroup(genesis, "metarig_heel02_tail.L")
                delVgroup(genesis, "metarig_hand_tail.L")
                delVgroup(genesis, "metarig_thumbtip.L")
                delVgroup(genesis, "metarig_indextip.L")
                delVgroup(genesis, "metarig_midtip.L")
                delVgroup(genesis, "metarig_ringtip.L")
                delVgroup(genesis, "metarig_pinkytip.L")
                delVgroup(genesis, "metarig_indexcarp.L")
                delVgroup(genesis, "metarig_midcarp.L")
                delVgroup(genesis, "metarig_ringcarp.L")
                delVgroup(genesis, "metarig_pinkycarp.L")

                #face rig
                faceRig = createFaceRig(False)
                #print(faceRig.name)
                faceRigSetParents(faceRig, False)
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "tail", "metarig_eye_tail.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "tail", "metarig_eye_tail.R")
                copyMeshPos(faceRig, genesis, "DEF-tonguetip", "tail", "metarig_tonguetip_tail")

                copyBonePos(faceRig, genesisRig, "DEF-tonguebase", "head", "tongueBase")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.01", "head", "tongue01")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.02", "head", "tongue02")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.03", "head", "tongue03")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.04", "head", "tongue04")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.05", "head", "tongue05")
                copyBonePos(faceRig, genesisRig, "DEF-tonguetip", "head", "tongueTip")
                faceRigFinishingTouches(faceRig)

                delVgroup(genesis, "metarig_eye_head.L")
                delVgroup(genesis, "metarig_eye_head.R")
                delVgroup(genesis, "metarig_eye_tail.L")
                delVgroup(genesis, "metarig_eye_tail.R")
                delVgroup(genesis, "metarig_tonguetip_tail")

                bpy.ops.view3d.snap_cursor_to_center()

                bpy.ops.view3d.snap_cursor_to_center()
                bpy.context.scene.objects.active = metarig
                bpy.ops.pose.rigify_generate()
                rigifyRig = bpy.context.active_object
                rigifyRig.name = genesis.name + "-rig"
                #fix neck issue
                bpy.ops.object.khalibloo_rigify_neck_fix()
                parentWGTs()

                joinFaceRig(faceRig, rigifyRig, False)
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = genesis
                genesis.select = True
        return {'FINISHED'}

class Genesis3FemaleRigifySetup(bpy.types.Operator):
    """Generate and setup a rigify rig for the active Genesis 3 Female figure"""
    bl_idname = "object.khalibloo_genesis3female_rigify_setup"
    bl_label = "Rigify"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'MESH'))

    def execute(self, context):
        genesis = bpy.context.active_object
        global rigifyRig
        global genesisRig

        if (genesis.find_armature() is not None):
            if (len(genesis.data.vertices.items()) == 17418):
                genesisRig = bpy.context.active_object.find_armature()

                genesisRig.hide = False
                bpy.context.scene.layers[findLayer(genesisRig)] = True

                #VERTEX GROUPS RAW DATA
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(bpy.data.meshes[genesis.data.name])

                hips_head = [1713, 8611]
                head_tail = [79, 3958]
                toe_tail_L = [5043, 5046]
                heel_tail_L = [4745, 4758]
                heel02_head_L = [4090, 4091]
                heel02_tail_L = [3983, 4734]
                hand_tail_L = [4369, 4388, 4389, 6589]
                thumbtip_L = [5323, 5327]
                indextip_L = [5336, 5338]
                midtip_L = [5316, 5320]
                ringtip_L = [5306, 5310]
                pinkytip_L = [5300, 5302]
                #face rig
                eye_head_L = [16648, 16649, 16651, 16655, 16657, 16658, 16659, 16660, 16674, 16675, 16677, 16681, 16683, 16684, 16685, 16686, 16698, 16699, 16706, 16708, 16712, 16714, 16715, 16716, 16725, 16727, 16731, 16733, 16734, 16735, 16744, 16745]
                eye_tail_L = [16704]
                eye_head_R = [16810, 16811, 16813, 16817, 16819, 16820, 16821, 16822, 16836, 16837, 16839, 16843, 16845, 16846, 16847, 16848, 16860, 16861, 16868, 16870, 16874, 16876, 16877, 16878, 16887, 16889, 16893, 16895, 16896, 16897, 16906, 16907]
                eye_tail_R = [16866]

                createVgroup(genesis, bm, "metarig_hips_head", hips_head)
                createVgroup(genesis, bm, "metarig_head_tail", head_tail)
                createVgroup(genesis, bm, "metarig_toe_tail.L", toe_tail_L)
                createVgroup(genesis, bm, "metarig_heel_tail.L", heel_tail_L)
                createVgroup(genesis, bm, "metarig_heel02_head.L", heel02_head_L)
                createVgroup(genesis, bm, "metarig_heel02_tail.L", heel02_tail_L)
                createVgroup(genesis, bm, "metarig_hand_tail.L", hand_tail_L)
                createVgroup(genesis, bm, "metarig_thumbtip.L", thumbtip_L)
                createVgroup(genesis, bm, "metarig_indextip.L", indextip_L)
                createVgroup(genesis, bm, "metarig_midtip.L", midtip_L)
                createVgroup(genesis, bm, "metarig_ringtip.L", ringtip_L)
                createVgroup(genesis, bm, "metarig_pinkytip.L", pinkytip_L)
                #face rig
                createVgroup(genesis, bm, "metarig_eye_head.L", eye_head_L)
                createVgroup(genesis, bm, "metarig_eye_tail.L", eye_tail_L)
                createVgroup(genesis, bm, "metarig_eye_head.R", eye_head_R)
                createVgroup(genesis, bm, "metarig_eye_tail.R", eye_tail_R)

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.view3d.snap_cursor_to_center()
                try:
                    bpy.ops.object.armature_human_metarig_add()
                except AttributeError:
                    self.report({'ERROR'}, "Missing Addon: 'Rigify'")
                    return {'CANCELLED'}
                except:
                    self.report({'ERROR'}, "Rigify: Broken... Something's wrong with Rigify. Please report this")
                    return {'CANCELLED'}
                metarig = bpy.context.active_object

                metarigPrep(metarig)

                copyMeshPos(metarig, genesis, "head", "tail", "metarig_head_tail")
                copyMeshPos(metarig, genesis, "hips", "head", "metarig_hips_head")
                copyMeshPos(metarig, genesis, "toe.L", "tail", "metarig_toe_tail.L")
                copyMeshPos(metarig, genesis, "heel.L", "tail", "metarig_heel_tail.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "head", "metarig_heel02_head.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "tail", "metarig_heel02_tail.L")
                copyMeshPos(metarig, genesis, "hand.L", "tail", "metarig_hand_tail.L")
                copyMeshPos(metarig, genesis, "thumb.03.L", "tail", "metarig_thumbtip.L")
                copyMeshPos(metarig, genesis, "f_index.03.L", "tail", "metarig_indextip.L")
                copyMeshPos(metarig, genesis, "f_middle.03.L", "tail", "metarig_midtip.L")
                copyMeshPos(metarig, genesis, "f_ring.03.L", "tail", "metarig_ringtip.L")
                copyMeshPos(metarig, genesis, "f_pinky.03.L", "tail", "metarig_pinkytip.L")

                copyBonePos(metarig, genesisRig, "spine", "head", "abdomenLower")
                copyBonePos(metarig, genesisRig, "spine", "tail", "abdomenUpper")
                copyBonePos(metarig, genesisRig, "neck", "head", "neckLower")
                copyBonePos(metarig, genesisRig, "neck", "tail", "neckUpper")
                copyBonePos(metarig, genesisRig, "thigh.L", "head", "lThighBend")
                copyBonePos(metarig, genesisRig, "shin.L", "head", "lShin")
                copyBonePos(metarig, genesisRig, "shin.L", "tail", "lFoot")
                copyBonePos(metarig, genesisRig, "toe.L", "head", "lToe")
                copyBonePos(metarig, genesisRig, "shoulder.L", "head", "lCollar")
                copyBonePos(metarig, genesisRig, "shoulder.L", "tail", "lShldrBend")
                copyBonePos(metarig, genesisRig, "upper_arm.L", "head", "lShldrBend")
                copyBonePos(metarig, genesisRig, "forearm.L", "head", "lForearmBend")
                copyBonePos(metarig, genesisRig, "forearm.L", "tail", "lHand")
                copyBonePos(metarig, genesisRig, "palm.01.L", "head", "lCarpal1")
                copyBonePos(metarig, genesisRig, "palm.02.L", "head", "lCarpal2")
                copyBonePos(metarig, genesisRig, "palm.03.L", "head", "lCarpal3")
                copyBonePos(metarig, genesisRig, "palm.04.L", "head", "lCarpal4")
                copyBonePos(metarig, genesisRig, "thumb.01.L", "head", "lThumb1")
                copyBonePos(metarig, genesisRig, "thumb.02.L", "head", "lThumb2")
                copyBonePos(metarig, genesisRig, "thumb.03.L", "head", "lThumb3")
                copyBonePos(metarig, genesisRig, "f_index.01.L", "head", "lIndex1")
                copyBonePos(metarig, genesisRig, "f_index.02.L", "head", "lIndex2")
                copyBonePos(metarig, genesisRig, "f_index.03.L", "head", "lIndex3")
                copyBonePos(metarig, genesisRig, "f_middle.01.L", "head", "lMid1")
                copyBonePos(metarig, genesisRig, "f_middle.02.L", "head", "lMid2")
                copyBonePos(metarig, genesisRig, "f_middle.03.L", "head", "lMid3")
                copyBonePos(metarig, genesisRig, "f_ring.01.L", "head", "lRing1")
                copyBonePos(metarig, genesisRig, "f_ring.02.L", "head", "lRing2")
                copyBonePos(metarig, genesisRig, "f_ring.03.L", "head", "lRing3")
                copyBonePos(metarig, genesisRig, "f_pinky.01.L", "head", "lPinky1")
                copyBonePos(metarig, genesisRig, "f_pinky.02.L", "head", "lPinky2")
                copyBonePos(metarig, genesisRig, "f_pinky.03.L", "head", "lPinky3")
                metarigFinishingTouches(metarig)
                setGenesis3FemaleRolls(metarig)

                delVgroup(genesis, "metarig_head_tail")
                delVgroup(genesis, "metarig_hips_head")
                delVgroup(genesis, "metarig_toe_tail.L")
                delVgroup(genesis, "metarig_heel_tail.L")
                delVgroup(genesis, "metarig_heel02_head.L")
                delVgroup(genesis, "metarig_heel02_tail.L")
                delVgroup(genesis, "metarig_hand_tail.L")
                delVgroup(genesis, "metarig_thumbtip.L")
                delVgroup(genesis, "metarig_indextip.L")
                delVgroup(genesis, "metarig_midtip.L")
                delVgroup(genesis, "metarig_ringtip.L")
                delVgroup(genesis, "metarig_pinkytip.L")

                #face rig
                faceRig = createFaceRig(True)
                #print(faceRig.name)
                faceRigSetParents(faceRig, True)
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "tail", "metarig_eye_tail.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "tail", "metarig_eye_tail.R")

                copyBonePos(faceRig, genesisRig, "DEF-tongue.01", "head", "tongue01")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.02", "head", "tongue02")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.03", "head", "tongue03")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.04", "head", "tongue04")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.04", "tail", "tongue04")
                faceRigFinishingTouches(faceRig)

                delVgroup(genesis, "metarig_eye_head.L")
                delVgroup(genesis, "metarig_eye_head.R")
                delVgroup(genesis, "metarig_eye_tail.L")
                delVgroup(genesis, "metarig_eye_tail.R")

                bpy.ops.view3d.snap_cursor_to_center()
                bpy.context.scene.objects.active = metarig
                bpy.ops.pose.rigify_generate()
                rigifyRig = bpy.context.active_object
                rigifyRig.name = genesis.name + "-rig"
                #fix neck issue
                bpy.ops.object.khalibloo_rigify_neck_fix()
                parentWGTs()

                joinFaceRig(faceRig, rigifyRig, True)
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = genesis
                genesis.select = True
        return {'FINISHED'}

class Genesis3MaleRigifySetup(bpy.types.Operator):
    """Generate and setup a rigify rig for the active Genesis 3 Male figure"""
    bl_idname = "object.khalibloo_genesis3male_rigify_setup"
    bl_label = "Rigify"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'MESH'))

    def execute(self, context):
        genesis = bpy.context.active_object
        global rigifyRig
        global genesisRig

        if (genesis.find_armature() is not None):
            if (len(genesis.data.vertices.items()) == 17246):
                genesisRig = bpy.context.active_object.find_armature()

                genesisRig.hide = False
                bpy.context.scene.layers[findLayer(genesisRig)] = True

                #VERTEX GROUPS RAW DATA
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(bpy.data.meshes[genesis.data.name])

                hips_head = [3363, 9918]
                head_tail = [78, 3733]
                toe_tail_L = [4826]
                heel_tail_L = [4465]
                heel02_tail_L = [3756, 3757]
                heel02_head_L = [3865, 3866]
                hand_tail_L = [4140, 5613, 5615, 5623]
                thumbtip_L = [5043, 5047]
                indextip_L = [5056, 5058]
                midtip_L = [5036, 5040]
                ringtip_L = [5026, 5030]
                pinkytip_L = [5020, 5022]
                eye_tail_L = [16049]
                eye_head_L = [15993, 15994, 15996, 16000, 16002, 16003, 16004, 16005, 16019, 16020, 16022, 16026, 16028, 16029, 16030, 16031, 16043, 16044, 16051, 16053, 16057, 16059, 16060, 16061, 16070, 16072, 16076, 16078, 16079, 16080, 16089, 16090]
                eye_tail_R = [16211]
                eye_head_R = [16155, 16156, 16158, 16162, 16164, 16165, 16166, 16167, 16181, 16182, 16184, 16188, 16190, 16191, 16192, 16193, 16205, 16206, 16213, 16215, 16219, 16221, 16222, 16223, 16232, 16234, 16238, 16240, 16241, 16242, 16251, 16252]

                createVgroup(genesis, bm, "metarig_hips_head", hips_head)
                createVgroup(genesis, bm, "metarig_head_tail", head_tail)
                createVgroup(genesis, bm, "metarig_toe_tail.L", toe_tail_L)
                createVgroup(genesis, bm, "metarig_heel_tail.L", heel_tail_L)
                createVgroup(genesis, bm, "metarig_heel02_head.L", heel02_head_L)
                createVgroup(genesis, bm, "metarig_heel02_tail.L", heel02_tail_L)
                createVgroup(genesis, bm, "metarig_hand_tail.L", hand_tail_L)
                createVgroup(genesis, bm, "metarig_thumbtip.L", thumbtip_L)
                createVgroup(genesis, bm, "metarig_indextip.L", indextip_L)
                createVgroup(genesis, bm, "metarig_midtip.L", midtip_L)
                createVgroup(genesis, bm, "metarig_ringtip.L", ringtip_L)
                createVgroup(genesis, bm, "metarig_pinkytip.L", pinkytip_L)
                #face rig
                createVgroup(genesis, bm, "metarig_eye_head.L", eye_head_L)
                createVgroup(genesis, bm, "metarig_eye_tail.L", eye_tail_L)
                createVgroup(genesis, bm, "metarig_eye_head.R", eye_head_R)
                createVgroup(genesis, bm, "metarig_eye_tail.R", eye_tail_R)

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.view3d.snap_cursor_to_center()
                try:
                    bpy.ops.object.armature_human_metarig_add()
                except AttributeError:
                    self.report({'ERROR'}, "Missing Addon: 'Rigify'")
                    return {'CANCELLED'}
                except:
                    self.report({'ERROR'}, "Rigify: Broken... Something's wrong with Rigify. Please report this")
                    return {'CANCELLED'}
                metarig = bpy.context.active_object

                metarigPrep(metarig)

                copyMeshPos(metarig, genesis, "head", "tail", "metarig_head_tail")
                copyMeshPos(metarig, genesis, "hips", "head", "metarig_hips_head")
                copyMeshPos(metarig, genesis, "toe.L", "tail", "metarig_toe_tail.L")
                copyMeshPos(metarig, genesis, "heel.L", "tail", "metarig_heel_tail.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "head", "metarig_heel02_head.L")
                copyMeshPos(metarig, genesis, "heel.02.L", "tail", "metarig_heel02_tail.L")
                copyMeshPos(metarig, genesis, "hand.L", "tail", "metarig_hand_tail.L")
                copyMeshPos(metarig, genesis, "thumb.03.L", "tail", "metarig_thumbtip.L")
                copyMeshPos(metarig, genesis, "f_index.03.L", "tail", "metarig_indextip.L")
                copyMeshPos(metarig, genesis, "f_middle.03.L", "tail", "metarig_midtip.L")
                copyMeshPos(metarig, genesis, "f_ring.03.L", "tail", "metarig_ringtip.L")
                copyMeshPos(metarig, genesis, "f_pinky.03.L", "tail", "metarig_pinkytip.L")

                copyBonePos(metarig, genesisRig, "spine", "head", "abdomenLower")
                copyBonePos(metarig, genesisRig, "spine", "tail", "abdomenUpper")
                copyBonePos(metarig, genesisRig, "neck", "head", "neckLower")
                copyBonePos(metarig, genesisRig, "neck", "tail", "neckUpper")
                copyBonePos(metarig, genesisRig, "thigh.L", "head", "lThighBend")
                copyBonePos(metarig, genesisRig, "shin.L", "head", "lShin")
                copyBonePos(metarig, genesisRig, "shin.L", "tail", "lFoot")
                copyBonePos(metarig, genesisRig, "toe.L", "head", "lToe")
                copyBonePos(metarig, genesisRig, "shoulder.L", "head", "lCollar")
                copyBonePos(metarig, genesisRig, "shoulder.L", "tail", "lShldrBend")
                copyBonePos(metarig, genesisRig, "upper_arm.L", "head", "lShldrBend")
                copyBonePos(metarig, genesisRig, "forearm.L", "head", "lForearmBend")
                copyBonePos(metarig, genesisRig, "forearm.L", "tail", "lHand")
                copyBonePos(metarig, genesisRig, "palm.01.L", "head", "lCarpal1")
                copyBonePos(metarig, genesisRig, "palm.02.L", "head", "lCarpal2")
                copyBonePos(metarig, genesisRig, "palm.03.L", "head", "lCarpal3")
                copyBonePos(metarig, genesisRig, "palm.04.L", "head", "lCarpal4")
                copyBonePos(metarig, genesisRig, "thumb.01.L", "head", "lThumb1")
                copyBonePos(metarig, genesisRig, "thumb.02.L", "head", "lThumb2")
                copyBonePos(metarig, genesisRig, "thumb.03.L", "head", "lThumb3")
                copyBonePos(metarig, genesisRig, "f_index.01.L", "head", "lIndex1")
                copyBonePos(metarig, genesisRig, "f_index.02.L", "head", "lIndex2")
                copyBonePos(metarig, genesisRig, "f_index.03.L", "head", "lIndex3")
                copyBonePos(metarig, genesisRig, "f_middle.01.L", "head", "lMid1")
                copyBonePos(metarig, genesisRig, "f_middle.02.L", "head", "lMid2")
                copyBonePos(metarig, genesisRig, "f_middle.03.L", "head", "lMid3")
                copyBonePos(metarig, genesisRig, "f_ring.01.L", "head", "lRing1")
                copyBonePos(metarig, genesisRig, "f_ring.02.L", "head", "lRing2")
                copyBonePos(metarig, genesisRig, "f_ring.03.L", "head", "lRing3")
                copyBonePos(metarig, genesisRig, "f_pinky.01.L", "head", "lPinky1")
                copyBonePos(metarig, genesisRig, "f_pinky.02.L", "head", "lPinky2")
                copyBonePos(metarig, genesisRig, "f_pinky.03.L", "head", "lPinky3")
                metarigFinishingTouches(metarig)
                setGenesis3MaleRolls(metarig)

                delVgroup(genesis, "metarig_head_tail")
                delVgroup(genesis, "metarig_hips_head")
                delVgroup(genesis, "metarig_toe_tail.L")
                delVgroup(genesis, "metarig_heel_tail.L")
                delVgroup(genesis, "metarig_heel02_head.L")
                delVgroup(genesis, "metarig_heel02_tail.L")
                delVgroup(genesis, "metarig_hand_tail.L")
                delVgroup(genesis, "metarig_thumbtip.L")
                delVgroup(genesis, "metarig_indextip.L")
                delVgroup(genesis, "metarig_midtip.L")
                delVgroup(genesis, "metarig_ringtip.L")
                delVgroup(genesis, "metarig_pinkytip.L")

                #face rig
                faceRig = createFaceRig(True)
                #print(faceRig.name)
                faceRigSetParents(faceRig, True)
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "DEF-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "DEF-eye.R", "tail", "metarig_eye_tail.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "head", "metarig_eye_head.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "head", "metarig_eye_head.R")
                copyMeshPos(faceRig, genesis, "IK-eye.L", "tail", "metarig_eye_tail.L")
                copyMeshPos(faceRig, genesis, "IK-eye.R", "tail", "metarig_eye_tail.R")

                copyBonePos(faceRig, genesisRig, "DEF-tongue.01", "head", "tongue01")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.02", "head", "tongue02")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.03", "head", "tongue03")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.04", "head", "tongue04")
                copyBonePos(faceRig, genesisRig, "DEF-tongue.04", "tail", "tongue04")
                faceRigFinishingTouches(faceRig)

                delVgroup(genesis, "metarig_eye_head.L")
                delVgroup(genesis, "metarig_eye_head.R")
                delVgroup(genesis, "metarig_eye_tail.L")
                delVgroup(genesis, "metarig_eye_tail.R")

                bpy.ops.view3d.snap_cursor_to_center()
                bpy.context.scene.objects.active = metarig
                bpy.ops.pose.rigify_generate()
                rigifyRig = bpy.context.active_object
                rigifyRig.name = genesis.name + "-rig"
                #fix neck issue
                bpy.ops.object.khalibloo_rigify_neck_fix()
                parentWGTs()

                joinFaceRig(faceRig, rigifyRig, True)
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = genesis
                genesis.select = True
        return {'FINISHED'}

class GenesisRigifyVgroups(bpy.types.Operator):
    """Mixes and renames the deformation vertex groups of a Genesis figure and/or selected Genesis item(s) to conform with Rigify. Backups are made before mixing, so no vertex groups are lost."""
    bl_idname = "object.khalibloo_genesis_rigify_vgroups"
    bl_label = "Rigify Vertex Groups"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'MESH'))

    def execute(self, context):
        selectionList = bpy.context.selected_objects
        objBackup = bpy.context.active_object
        global rigifyRig


        for obj in selectionList:
            bpy.context.scene.objects.active = bpy.data.objects[obj.name]
            if (len(obj.vertex_groups.keys())>0):
                mixVgroups(obj, "lThighBend", "lThighTwist")
                mixVgroups(obj, "lToe", "lBigToe")
                mixVgroups(obj, "lToe", "lSmallToe1")
                mixVgroups(obj, "lToe", "lSmallToe2")
                mixVgroups(obj, "lToe", "lSmallToe3")
                mixVgroups(obj, "lToe", "lSmallToe4")
                mixVgroups(obj, "lToe", "lBigToe_2")
                mixVgroups(obj, "lToe", "lSmallToe1_2")
                mixVgroups(obj, "lToe", "lSmallToe2_2")
                mixVgroups(obj, "lToe", "lSmallToe3_2")
                mixVgroups(obj, "lToe", "lSmallToe4_2")
                mixVgroups(obj, "lFoot", "lHeel")
                mixVgroups(obj, "lFoot", "lMetatarsals")

                mixVgroups(obj, "rThighBend", "rThighTwist")
                mixVgroups(obj, "rToe", "rBigToe")
                mixVgroups(obj, "rToe", "rSmallToe1")
                mixVgroups(obj, "rToe", "rSmallToe2")
                mixVgroups(obj, "rToe", "rSmallToe3")
                mixVgroups(obj, "rToe", "rSmallToe4")
                mixVgroups(obj, "rToe", "rBigToe_2")
                mixVgroups(obj, "rToe", "rSmallToe1_2")
                mixVgroups(obj, "rToe", "rSmallToe2_2")
                mixVgroups(obj, "rToe", "rSmallToe3_2")
                mixVgroups(obj, "rToe", "rSmallToe4_2")
                mixVgroups(obj, "rFoot", "rHeel")
                mixVgroups(obj, "rFoot", "rMetatarsals")

                mixVgroups(obj, "lShldrBend", "lShldrTwist")
                mixVgroups(obj, "lForearmBend", "lForearmTwist")
                mixVgroups(obj, "rShldrBend", "rShldrTwist")
                mixVgroups(obj, "rForearmBend", "rForearmTwist")

                #mixVgroups(obj, "head", "tongueBase")
                #mixVgroups(obj, "head", "tongue01")
                #mixVgroups(obj, "head", "tongue02")
                #mixVgroups(obj, "head", "tongue03")
                #mixVgroups(obj, "head", "tongue04")
                #mixVgroups(obj, "head", "tongue05")
                #mixVgroups(obj, "head", "tongueTip")
                mixVgroups(obj, "head", "lowerJaw")
                mixVgroups(obj, "head", "upperJaw")
                mixVgroups(obj, "head", "CenterBrow")
                mixVgroups(obj, "head", "lBrowOuter")
                mixVgroups(obj, "head", "lBrowMid")
                mixVgroups(obj, "head", "lBrowInner")
                mixVgroups(obj, "head", "MidNoseBridge")
                mixVgroups(obj, "head", "lEyelidInner")
                mixVgroups(obj, "head", "lEyelidUpperInner")
                mixVgroups(obj, "head", "lEyelidUpper")
                mixVgroups(obj, "head", "lEyelidUpperOuter")
                mixVgroups(obj, "head", "lEyelidOuter")
                mixVgroups(obj, "head", "lEyelidLowerOuter")
                mixVgroups(obj, "head", "lEyelidLower")
                mixVgroups(obj, "head", "lEyelidLowerInner")
                mixVgroups(obj, "head", "lSquintInner")
                mixVgroups(obj, "head", "lSquintOuter")
                mixVgroups(obj, "head", "lCheekUpper")
                mixVgroups(obj, "head", "lCheekLower")
                mixVgroups(obj, "head", "Nose")
                mixVgroups(obj, "head", "lNostril")
                mixVgroups(obj, "head", "lLipBelowNose")
                mixVgroups(obj, "head", "lLipUpperOuter")
                mixVgroups(obj, "head", "lLipUpperInner")
                mixVgroups(obj, "head", "LipUpperMiddle")
                mixVgroups(obj, "head", "lLipNasolabialCrease")
                mixVgroups(obj, "head", "lNasolabialUpper")
                mixVgroups(obj, "head", "lNasolabialMiddle")
                mixVgroups(obj, "head", "lNasolabialLower")
                mixVgroups(obj, "head", "lNasolabialMouthCorner")
                mixVgroups(obj, "head", "lLipCorner")
                mixVgroups(obj, "head", "lLipLowerOuter")
                mixVgroups(obj, "head", "LipLowerMiddle")
                mixVgroups(obj, "head", "lLipLowerInner")
                mixVgroups(obj, "head", "LipBelow")
                mixVgroups(obj, "head", "Chin")
                mixVgroups(obj, "head", "BelowJaw")
                mixVgroups(obj, "head", "lJawClench")
                mixVgroups(obj, "head", "lowerTeeth")
                mixVgroups(obj, "head", "upperTeeth")
                mixVgroups(obj, "head", "lowerFaceRig")
                mixVgroups(obj, "head", "upperFaceRig")
                mixVgroups(obj, "head", "lowerJaw")
                mixVgroups(obj, "head", "lEar")

                mixVgroups(obj, "head", "rBrowOuter")
                mixVgroups(obj, "head", "rBrowMid")
                mixVgroups(obj, "head", "rBrowInner")
                mixVgroups(obj, "head", "rEyelidInner")
                mixVgroups(obj, "head", "rEyelidUpperInner")
                mixVgroups(obj, "head", "rEyelidUpper")
                mixVgroups(obj, "head", "rEyelidUpperOuter")
                mixVgroups(obj, "head", "rEyelidOuter")
                mixVgroups(obj, "head", "rEyelidLowerOuter")
                mixVgroups(obj, "head", "rEyelidLower")
                mixVgroups(obj, "head", "rEyelidLowerInner")
                mixVgroups(obj, "head", "rSquintInner")
                mixVgroups(obj, "head", "rSquintOuter")
                mixVgroups(obj, "head", "rCheekUpper")
                mixVgroups(obj, "head", "rCheekLower")
                mixVgroups(obj, "head", "rNostril")
                mixVgroups(obj, "head", "rLipBelowNose")
                mixVgroups(obj, "head", "rLipUpperOuter")
                mixVgroups(obj, "head", "rLipUpperInner")
                mixVgroups(obj, "head", "rLipNasolabialCrease")
                mixVgroups(obj, "head", "rNasolabialUpper")
                mixVgroups(obj, "head", "rNasolabialMiddle")
                mixVgroups(obj, "head", "rNasolabialLower")
                mixVgroups(obj, "head", "rNasolabialMouthCorner")
                mixVgroups(obj, "head", "rLipCorner")
                mixVgroups(obj, "head", "rLipLowerOuter")
                mixVgroups(obj, "head", "rLipLowerInner")
                mixVgroups(obj, "head", "rJawClench")
                mixVgroups(obj, "head", "rEar")

                mixVgroups(obj, "neckLower", "neckUpper")
                mixVgroups(obj, "chest", "lPectoral")
                mixVgroups(obj, "chest", "rPectoral")
                mixVgroups(obj, "chestLower", "chestUpper") #g3
                mixVgroups(obj, "chestLower", "lPectoral") #g3
                mixVgroups(obj, "chestLower", "rPectoral") #g3
                mixVgroups(obj, "abdomenLower", "abdomenUpper")

                renameVgroups(obj, "head", "DEF-head")
                renameVgroups(obj, "neck", "DEF-neck")
                renameVgroups(obj, "neckLower", "DEF-neck") #g3
                renameVgroups(obj, "chest", "DEF-chest")
                renameVgroups(obj, "chestLower", "DEF-chest") #g3
                renameVgroups(obj, "abdomen2", "DEF-spine")
                renameVgroups(obj, "abdomenLower", "DEF-spine") #g3
                renameVgroups(obj, "pelvis", "DEF-hips")
                renameVgroups(obj, "tongueBase", "DEF-tonguebase")
                renameVgroups(obj, "tongue01", "DEF-tongue.01")
                renameVgroups(obj, "tongue02", "DEF-tongue.02")
                renameVgroups(obj, "tongue03", "DEF-tongue.03")
                renameVgroups(obj, "tongue04", "DEF-tongue.04")
                renameVgroups(obj, "tongue05", "DEF-tongue.05")
                renameVgroups(obj, "tongueTip", "DEF-tonguetip")

                #LEFT
                renameVgroups(obj, "lEye", "DEF-eye.L")
                renameVgroups(obj, "lThigh", "DEF-thigh.01.L")
                renameVgroups(obj, "lThighBend", "DEF-thigh.01.L") #g3
                renameVgroups(obj, "lShin", "DEF-shin.01.L")
                renameVgroups(obj, "lFoot", "DEF-foot.L")
                renameVgroups(obj, "lToe", "DEF-toe.L")
                renameVgroups(obj, "lCollar", "DEF-shoulder.L")
                renameVgroups(obj, "lShldr", "DEF-upper_arm.01.L")
                renameVgroups(obj, "lShldrBend", "DEF-upper_arm.01.L") #g3
                renameVgroups(obj, "lForeArm", "DEF-forearm.01.L")
                renameVgroups(obj, "lForearmBend", "DEF-forearm.01.L") #g3
                renameVgroups(obj, "lHand", "DEF-hand.L")
                if("lCarpal3" in obj.vertex_groups.keys() or "lCarpal4" in obj.vertex_groups.keys()):
                    #it's a g3
                    renameVgroups(obj, "lCarpal1", "DEF-palm.01.L")
                    renameVgroups(obj, "lCarpal2", "DEF-palm.02.L")
                    renameVgroups(obj, "lCarpal3", "DEF-palm.03.L")
                    renameVgroups(obj, "lCarpal4", "DEF-palm.04.L")
                else:
                    renameVgroups(obj, "lCarpal1", "DEF-palm.01.L")
                    renameVgroups(obj, "lCarpal2", "DEF-palm.04.L")
                renameVgroups(obj, "lThumb1", "DEF-thumb.01.L.02")
                renameVgroups(obj, "lThumb2", "DEF-thumb.02.L")
                renameVgroups(obj, "lThumb3", "DEF-thumb.03.L")
                renameVgroups(obj, "lIndex1", "DEF-f_index.01.L.01")
                renameVgroups(obj, "lIndex2", "DEF-f_index.02.L")
                renameVgroups(obj, "lIndex3", "DEF-f_index.03.L")
                renameVgroups(obj, "lMid1", "DEF-f_middle.01.L.01")
                renameVgroups(obj, "lMid2", "DEF-f_middle.02.L")
                renameVgroups(obj, "lMid3", "DEF-f_middle.03.L")
                renameVgroups(obj, "lRing1", "DEF-f_ring.01.L.01")
                renameVgroups(obj, "lRing2", "DEF-f_ring.02.L")
                renameVgroups(obj, "lRing3", "DEF-f_ring.03.L")
                renameVgroups(obj, "lPinky1", "DEF-f_pinky.01.L.01")
                renameVgroups(obj, "lPinky2", "DEF-f_pinky.02.L")
                renameVgroups(obj, "lPinky3", "DEF-f_pinky.03.L")

                #RIGHT
                renameVgroups(obj, "rEye", "DEF-eye.R")
                renameVgroups(obj, "rThigh", "DEF-thigh.01.R")
                renameVgroups(obj, "rThighBend", "DEF-thigh.01.R") #g3
                renameVgroups(obj, "rShin", "DEF-shin.01.R")
                renameVgroups(obj, "rFoot", "DEF-foot.R")
                renameVgroups(obj, "rToe", "DEF-toe.R")
                renameVgroups(obj, "rCollar", "DEF-shoulder.R")
                renameVgroups(obj, "rShldr", "DEF-upper_arm.01.R")
                renameVgroups(obj, "rShldrBend", "DEF-upper_arm.01.R") #g3
                renameVgroups(obj, "rForeArm", "DEF-forearm.01.R")
                renameVgroups(obj, "rForearmBend", "DEF-forearm.01.R") #g3
                renameVgroups(obj, "rHand", "DEF-hand.R")
                if("rCarpal3" in obj.vertex_groups.keys() or "rCarpal4" in obj.vertex_groups.keys()):
                    #it's a g3
                    renameVgroups(obj, "rCarpal1", "DEF-palm.01.R")
                    renameVgroups(obj, "rCarpal2", "DEF-palm.02.R")
                    renameVgroups(obj, "rCarpal3", "DEF-palm.03.R")
                    renameVgroups(obj, "rCarpal4", "DEF-palm.04.R")
                else:
                    renameVgroups(obj, "rCarpal1", "DEF-palm.01.R")
                    renameVgroups(obj, "rCarpal2", "DEF-palm.04.R")
                renameVgroups(obj, "rThumb1", "DEF-thumb.01.R.02")
                renameVgroups(obj, "rThumb2", "DEF-thumb.02.R")
                renameVgroups(obj, "rThumb3", "DEF-thumb.03.R")
                renameVgroups(obj, "rIndex1", "DEF-f_index.01.R.01")
                renameVgroups(obj, "rIndex2", "DEF-f_index.02.R")
                renameVgroups(obj, "rIndex3", "DEF-f_index.03.R")
                renameVgroups(obj, "rMid1", "DEF-f_middle.01.R.01")
                renameVgroups(obj, "rMid2", "DEF-f_middle.02.R")
                renameVgroups(obj, "rMid3", "DEF-f_middle.03.R")
                renameVgroups(obj, "rRing1", "DEF-f_ring.01.R.01")
                renameVgroups(obj, "rRing2", "DEF-f_ring.02.R")
                renameVgroups(obj, "rRing3", "DEF-f_ring.03.R")
                renameVgroups(obj, "rPinky1", "DEF-f_pinky.01.R.01")
                renameVgroups(obj, "rPinky2", "DEF-f_pinky.02.R")
                renameVgroups(obj, "rPinky3", "DEF-f_pinky.03.R")

                #apply parent's transforms
                if (obj.parent):
                    obj.parent.hide = False
                    bpy.context.scene.layers[findLayer(obj.parent)] = True
                    bpy.context.scene.objects.active = obj.parent
                    obj.parent.select = True
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

                if (rigifyRig is not None):
                    obj.parent = rigifyRig
                    setupArmatureModifier(obj, rigifyRig)

        bpy.ops.object.select_all(action='DESELECT')
        objBackup.select = True
        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class GenesisUnrigifyVgroups(bpy.types.Operator):
    """Renames the vertex groups of a rigified Genesis figure and/or selected Genesis item(s) to their original names"""
    bl_idname = "object.khalibloo_genesis_unrigify_vgroups"
    bl_label = "Unrigify Vertex Groups"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'MESH'))

    def execute(self, context):
        selectionList = bpy.context.selected_objects
        objBackup = bpy.context.active_object
        global genesisRig


        for obj in selectionList:
            bpy.context.scene.objects.active = bpy.data.objects[obj.name]
            if (len(obj.vertex_groups.keys())>0):

                renameVgroups(obj, "DEF-head", "head")
                renameVgroups(obj, "DEF-neck", "neck")
                renameVgroups(obj, "DEF-chest", "chest")
                renameVgroups(obj, "DEF-spine", "abdomen2")
                renameVgroups(obj, "DEF-hips", "pelvis")
                renameVgroups(obj, "DEF-tonguebase", "tongueBase")
                renameVgroups(obj, "DEF-tongue.01", "tongue01")
                renameVgroups(obj, "DEF-tongue.02", "tongue02")
                renameVgroups(obj, "DEF-tongue.03", "tongue03")
                renameVgroups(obj, "DEF-tongue.04", "tongue04")
                renameVgroups(obj, "DEF-tongue.05", "tongue05")
                renameVgroups(obj, "DEF-tonguetip", "tongueTip")
                #LEFT
                renameVgroups(obj, "DEF-eye.L", "lEye")
                renameVgroups(obj, "DEF-thigh.01.L", "lThigh")
                renameVgroups(obj, "DEF-shin.01.L", "lShin")
                renameVgroups(obj, "DEF-foot.L", "lFoot")
                renameVgroups(obj, "DEF-toe.L", "lToe")
                renameVgroups(obj, "DEF-shoulder.L", "lCollar")
                renameVgroups(obj, "DEF-upper_arm.01.L", "lShldr")
                renameVgroups(obj, "DEF-forearm.01.L", "lForeArm")
                renameVgroups(obj, "DEF-hand.L", "lHand")
                renameVgroups(obj, "DEF-palm.04.L", "lCarpal2")
                renameVgroups(obj, "DEF-palm.01.L", "lCarpal1")
                renameVgroups(obj, "DEF-thumb.01.L.02", "lThumb1")
                renameVgroups(obj, "DEF-thumb.02.L", "lThumb2")
                renameVgroups(obj, "DEF-thumb.03.L", "lThumb3")
                renameVgroups(obj, "DEF-f_index.01.L.01", "lIndex1")
                renameVgroups(obj, "DEF-f_index.02.L", "lIndex2")
                renameVgroups(obj, "DEF-f_index.03.L", "lIndex3")
                renameVgroups(obj, "DEF-f_middle.01.L.01", "lMid1")
                renameVgroups(obj, "DEF-f_middle.02.L", "lMid2")
                renameVgroups(obj, "DEF-f_middle.03.L", "lMid3")
                renameVgroups(obj, "DEF-f_ring.01.L.01", "lRing1")
                renameVgroups(obj, "DEF-f_ring.02.L", "lRing2")
                renameVgroups(obj, "DEF-f_ring.03.L", "lRing3")
                renameVgroups(obj, "DEF-f_pinky.01.L.01", "lPinky1")
                renameVgroups(obj, "DEF-f_pinky.02.L", "lPinky2")
                renameVgroups(obj, "DEF-f_pinky.03.L", "lPinky3")

                #RIGHT
                renameVgroups(obj, "DEF-eye.R", "rEye")
                renameVgroups(obj, "DEF-thigh.01.R", "rThigh")
                renameVgroups(obj, "DEF-shin.01.R", "rShin")
                renameVgroups(obj, "DEF-foot.R", "rFoot")
                renameVgroups(obj, "DEF-toe.R", "rToe")
                renameVgroups(obj, "DEF-shoulder.R", "rCollar")
                renameVgroups(obj, "DEF-upper_arm.01.R", "rShldr")
                renameVgroups(obj, "DEF-forearm.01.R", "rForeArm")
                renameVgroups(obj, "DEF-hand.R", "rHand")
                renameVgroups(obj, "DEF-palm.04.R", "rCarpal2")
                renameVgroups(obj, "DEF-palm.01.R", "rCarpal1")
                renameVgroups(obj, "DEF-thumb.01.R.02", "rThumb1")
                renameVgroups(obj, "DEF-thumb.02.R", "rThumb2")
                renameVgroups(obj, "DEF-thumb.03.R", "rThumb3")
                renameVgroups(obj, "DEF-f_index.01.R.01", "rIndex1")
                renameVgroups(obj, "DEF-f_index.02.R", "rIndex2")
                renameVgroups(obj, "DEF-f_index.03.R", "rIndex3")
                renameVgroups(obj, "DEF-f_middle.01.R.01", "rMid1")
                renameVgroups(obj, "DEF-f_middle.02.R", "rMid2")
                renameVgroups(obj, "DEF-f_middle.03.R", "rMid3")
                renameVgroups(obj, "DEF-f_ring.01.R.01", "rRing1")
                renameVgroups(obj, "DEF-f_ring.02.R", "rRing2")
                renameVgroups(obj, "DEF-f_ring.03.R", "rRing3")
                renameVgroups(obj, "DEF-f_pinky.01.R.01", "rPinky1")
                renameVgroups(obj, "DEF-f_pinky.02.R", "rPinky2")
                renameVgroups(obj, "DEF-f_pinky.03.R", "rPinky3")

                #apply parent's transforms
                bpy.context.scene.objects.active = obj.parent
                obj.parent.select = True
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

                if (genesisRig is not None):
                    obj.parent = genesisRig
                    setupArmatureModifier(obj, genesisRig)


        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class GenesisMaterialSetup(bpy.types.Operator):
    """Fixes the necessary settings on each of the materials and textures of the active Genesis figure.
    Note:for this to work, the materials must be using their default names."""
    bl_idname = "object.khalibloo_genesis_material_setup"
    bl_label = "Setup Materials"


    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (len(context.active_object.material_slots.keys()) != 0) and (bpy.context.scene.render.engine == 'BLENDER_RENDER'))

    def execute(self, context):
        obj = bpy.context.active_object
        originalMatList = obj.material_slots.keys()
        affect_textures = bpy.context.scene.khalibloo_affect_textures
        merge_mats = bpy.context.scene.khalibloo_merge_mats


        if (merge_mats):
            mergeMats(obj, originalMatList)


        #daz_3_SkinFoot
        guessName = "daz_3_SkinFoot"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Feet"
            check = checkForMatName(obj, guessName)
            if (check is None):
                guessName = "Limbs"
                check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Feet"
            if (merge_mats):
                name = "Limbs"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_6_Eyelash
        guessName = "daz_6_Eyelash"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Eyelashes"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Eyelashes"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            if (mat.texture_slots[0] is not None):
                mat.texture_slots[0].use_rgb_to_intensity = True
            check = None


        #daz_5_Sclera
        guessName = "daz_5_Sclera"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Sclera"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Sclera"
            if (merge_mats):
                name = "Irises"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            check = None


        #daz_5_Pupil
        guessName = "daz_5_Pupil"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Pupils"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Pupils"
            if (merge_mats):
                name = "Irises"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            check = None


        #daz_5_Iris
        guessName = "daz_5_Iris"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Irises"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            #print(mat.name)
            name = "Irises"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupBumpTex(mat, name)
            check = None

        #daz_5_Cornea if it's a Genesis 2 figure
        guessName = "Cornea"
        check = checkForMatName(obj, guessName)
        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Cornea"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_shader = 'WARDISO'
            mat.specular_intensity = 1
            mat.specular_slope = 0.05
            mat.use_transparency = True
            mat.alpha = 0
            mat.specular_alpha = 0
            check = None

        if (len(obj.data.vertices.items()) == 19296):
            #daz_5_Cornea ONLY if it's a Genesis figure
            guessName = "daz_5_Cornea"
            check = checkForMatName(obj, guessName)
            if (check is None):
                guessName = "Cornea"
                check = checkForMatName(obj, guessName)

            if (check is not None):
                mat = obj.material_slots[check].material
                name = "Cornea"
                mat.name = name
                mat.diffuse_intensity = 1
                mat.use_transparent_shadows = True
                mat.specular_shader = 'WARDISO'
                mat.specular_intensity = 1
                mat.specular_slope = 0.05
                mat.use_transparency = True
                mat.alpha = 0
                check = None


        #EyeReflection
        guessName = "EyeReflection"
        check = checkForMatName(obj, guessName)
        if (check is not None):
            mat = obj.material_slots[check].material
            name = "EyeReflection"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_shader = 'WARDISO'
            mat.specular_intensity = 1
            mat.specular_slope = 0.05
            mat.use_transparency = True
            mat.alpha = 0
            check = None


        #daz_4_Tongue
        guessName = "daz_4_Tongue"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Tongue"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Tongue"
            if (merge_mats):
                name = "InnerMouth"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 1
            mat.specular_hardness = 500
            if affect_textures:
                setupBumpTex(mat, name)
            check = None


        #daz_4_Teeth
        guessName = "daz_4_Teeth"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Teeth"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Teeth"
            if (merge_mats):
                name = "InnerMouth"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 1
            mat.specular_hardness = 500
            if affect_textures:
                setupBumpTex(mat, name)
            check = None


        #daz_4_InnerMouth
        guessName = "daz_4_InnerMouth"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "InnerMouth"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "InnerMouth"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 1
            mat.specular_hardness = 500
            if affect_textures:
                setupBumpTex(mat, name)
            check = None


        #daz_4_Gums
        guessName = "daz_4_Gums"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Gums"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Gums"
            if (merge_mats):
                name = "InnerMouth"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 1
            mat.specular_hardness = 500
            if affect_textures:
                setupBumpTex(mat, name)
            check = None


        #daz_3_SkinArm
        guessName = "daz_3_SkinArm"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Shoulders"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Shoulders"
            if (merge_mats):
                name = "Limbs"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_2_SkinTorso
        guessName = "daz_2_SkinTorso"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Torso"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Torso"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_2_Nipple
        guessName = "daz_2_Nipple"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Nipples"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Nipples"
            if (merge_mats):
                name = "Torso"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_2_SkinNeck
        guessName = "daz_2_SkinNeck"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Neck"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Neck"
            if (merge_mats):
                name = "Torso"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_3_SkinForearm
        guessName = "daz_3_SkinForearm"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Forearms"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Forearms"
            if (merge_mats):
                name = "Limbs"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_3_SkinLeg
        guessName = "daz_3_SkinLeg"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Legs"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Legs"
            if (merge_mats):
                name = "Limbs"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_2_SkinHip
        guessName = "daz_2_SkinHip"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Hips"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Hips"
            if (merge_mats):
                name = "Torso"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_2_SkinHead
        guessName = "daz_2_SkinHead"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Head"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Head"
            if (merge_mats):
                name = "Torso"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_3_SkinHand
        guessName = "daz_3_SkinHand"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Hands"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Hands"
            if (merge_mats):
                name = "Limbs"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_7_Tear
        guessName = "daz_7_Tear"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Tears"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Tears"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_shader = 'WARDISO'
            mat.specular_intensity = 1
            mat.specular_slope = 0.05
            mat.use_transparency = True
            mat.alpha = 0
            check = None


        #daz_1_Nostril
        guessName = "daz_1_Nostril"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Nostrils"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Nostrils"
            if (merge_mats):
                name = "Face"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_1_Lip
        guessName = "daz_1_Lip"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Lips"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Lips"
            if (merge_mats):
                name = "Face"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0.6
            mat.specular_hardness = 400
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_5_Lacrimal
        guessName = "daz_5_Lacrimal"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Lacrimals"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Lacrimals"
            if (merge_mats):
                name = "Irises"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            check = None


        #daz_1_SkinFace
        guessName = "daz_1_SkinFace"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Face"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Face"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #Ears
        guessName = "Ears"
        check = checkForMatName(obj, guessName)
        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Ears"
            if (merge_mats):
                name = "Torso"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None


        #daz_3_Fingernail
        guessName = "daz_3_Fingernail"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Fingernails"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Fingernails"
            if (merge_mats):
                name = "Limbs"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None



        #daz_3_Toenail
        guessName = "daz_3_Toenail"
        check = checkForMatName(obj, guessName)
        if (check is None):
            guessName = "Toenails"
            check = checkForMatName(obj, guessName)

        if (check is not None):
            mat = obj.material_slots[check].material
            name = "Toenails"
            if (merge_mats):
                name = "Limbs"
            mat.name = name
            mat.diffuse_intensity = 1
            mat.use_transparent_shadows = True
            mat.specular_intensity = 0
            if affect_textures:
                setupSpecTex(mat, name)
                setupBumpTex(mat, name)
            check = None

        return {'FINISHED'}

class RigifyNeckFix(bpy.types.Operator):
    """Fixes a rare condition where the rigify rig's neck bone is a lot larger than it should be"""
    bl_idname = "object.khalibloo_rigify_neck_fix"
    bl_label = "Rigify Neck Fix"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'ARMATURE'))



    def execute(self, context):
        rig = context.active_object
        neck = rig.pose.bones["neck"].custom_shape
        context.scene.layers[findLayer(neck)] = True
        neck.hide = False
        bpy.ops.object.select_all(action='DESELECT')
        context.scene.objects.active = neck
        neck.select = True
        context.space_data.pivot_point = 'MEDIAN_POINT'
        context.object.scale[0] = 0.390
        context.object.scale[1] = 0.390
        context.object.scale[2] = 0.390
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        pivot = context.space_data.pivot_point
        context.space_data.pivot_point = 'CURSOR'
        bpy.ops.transform.resize(value=(0.2442, 0.2442, 0.2442), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        context.scene.objects.active = rig
        context.space_data.pivot_point = pivot

        return{'FINISHED'}

class GenesisImportMorphs(bpy.types.Operator):
    """Imports all Genesis morphs(.obj) in the path specified as shape keys of the active Genesis figure"""
    bl_idname = "object.khalibloo_import_genesis_morphs"
    bl_label = "Import Morphs"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None) and (context.active_object.type == 'MESH'))


    def execute(self, context):
        import os
        obj = bpy.context.active_object
        morph_dir = bpy.context.scene.khalibloo_genesis_morph_dir

        for filename in os.listdir(morph_dir):
            filepath = morph_dir + filename
            name, extension = os.path.splitext(filepath)
            if (extension == ".obj"):
                try:
                    bpy.ops.import_scene.obj(filepath=filepath, filter_glob="*.obj;*.mtl",
                                use_edges=True, use_smooth_groups=True,
                                use_split_objects=False, use_split_groups=False,
                                use_groups_as_vgroups=False, use_image_search=False,
                                split_mode='OFF', global_clamp_size=0,
                                axis_forward='-Y', axis_up='Z')
                except AttributeError:
                    self.report({'ERROR'}, "Missing Addon: 'Import-Export: Wavefront OBJ format'")
                    return {'CANCELLED'}
                except RuntimeError:
                    self.report({'WARNING'}, "Ensure that only the relevant OBJ files are in the folder!")
                    return {'CANCELLED'}
            bpy.ops.object.khalibloo_apply_rotation()
            bpy.ops.object.khalibloo_apply_scale()
            bpy.ops.object.join_shapes()
            bpy.ops.object.delete()
        obj.select = True
        return {'FINISHED'}
