'''
AmasawaTools

Copyright (c) 2016 Amasawa Rasen

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
'''
import bpy
from mathutils import Vector
import math 
import bmesh
import numpy as np
import random
import copy
from math import radians
import bmesh
from bpy.types import WindowManager
from freestyle.types import Operators
from freestyle.predicates import *
import parameter_editor
from bpy.props import *

bl_info = {
    "name": "AmasawaTools",
    "description": "",
    "author": "AmasawaRasen",
    "version": (1, 5, 5),
    "blender": (2, 7, 8),
    "location": "View3D > Toolbar",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}
    
#パスを作る関数
def make_Path(verts):
    bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False))
    for i,point in enumerate(bpy.context.scene.objects.active.data.splines[0].points):
        point.co = verts[i]
        
#NURBS円を作る関数
def make_circle(verts):
    bpy.ops.curve.primitive_nurbs_circle_add(radius=0.1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False))
    for i,point in enumerate(bpy.context.scene.objects.active.data.splines[0].points):
        point.co = verts[i]

#カーブをアーマチュアやアーマチュア付メッシュに変換
def curveConvert(curveobjs,meshFlag=False,fullFlag=False,boneName='nashi',
    ystretch=False,radiusFlag=False,hideSelect=False,amaOnly=False):
    #何かの子になってと動作がおかしいので親を外す
    for c in curveobjs:
        c.parent = None
    #元のカーブを消さないようにコピーしておく
    copyCurveObjList = []
    bpy.ops.object.select_all(action='DESELECT')
    for c in curveobjs:
        bpy.context.scene.objects.active = c
        bpy.ops.object.select_pattern(pattern=c.name, case_sensitive=False, extend=True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
     TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False),
      "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED',
       "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False,
        "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False,
         "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False,
          "remove_on_cancel":False, "release_confirm":False})
    copyCurveObjList = bpy.context.selected_objects
    for c in curveobjs:
        c.layers[18] = True
    #スプラインを別オブジェクトに分離
    newObjList = []
    for c in copyCurveObjList:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = c
        bpy.ops.object.select_pattern(pattern=c.name, case_sensitive=False, extend=False)
        range1 = range(len(c.data.splines)-1)
        for i in range1:
            bpy.ops.object.editmode_toggle()
            bpy.ops.curve.select_all(action = 'DESELECT')
            if bpy.data.objects[c.name].data.splines[0].type == 'POLY' or\
                bpy.data.objects[c.name].data.splines[0].type == 'NURBS':
                bpy.data.objects[c.name].data.splines[0].points[0].select = True
            else:
                bpy.data.objects[c.name].data.splines[0].bezier_points[0].select_control_point = True
            bpy.ops.curve.select_linked()
            bpy.ops.curve.separate()
            bpy.ops.object.editmode_toggle()
        newObjList.extend(bpy.context.selected_objects)
    #オリジナルを保持したままメッシュ変換
    newMeshObjList = []
    activeAmaList = []
    for newobj in newObjList:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = newobj
        bpy.ops.object.select_pattern(pattern=newobj.name, case_sensitive=False, extend=False)
        bpy.ops.object.convert(target='MESH', keep_original=True)
        newMeshObjList.append(bpy.context.scene.objects.active)
        newMeshObj = bpy.context.scene.objects.active
        #オリジナルのテーパー、ベベル、深度、押し出しを外して線にする
        newobj.data.taper_object = None
        newobj.data.bevel_object = None
        newobj.data.bevel_depth = 0
        newobj.data.extrude = 0

        #Fullモードでは変換した辺を利用してアーマチュアを作る
        if fullFlag:
            #辺に変換
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = newobj
            bpy.ops.object.select_pattern(pattern=newobj.name, case_sensitive=False, extend=False)
            bpy.ops.object.convert(target='MESH', keep_original=True)
            baseMesh = bpy.context.scene.objects.active
            #基準辺からアーマチュアを作る
            bpy.ops.object.armature_add(radius=1, view_align=False, enter_editmode=False,
            location=(0, 0, 0),
            layers=bpy.context.scene.layers)
            activeAma = bpy.context.scene.objects.active
            activeAma.name = boneName
            activeAma.location = newobj.location
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.delete()
            bpy.ops.armature.bone_primitive_add()
            
            
            activeAma.data.edit_bones[0].head = [baseMesh.data.vertices[0].co[0],
                                                 baseMesh.data.vertices[0].co[1],
                                                 baseMesh.data.vertices[0].co[2]]
                                                    
            activeAma.data.edit_bones[0].name = newMeshObj.name + boneName
            if len(baseMesh.data.vertices) >= 3:
                for i,newPoint in enumerate(baseMesh.data.vertices[1:-1]):
                    rootBoneName = activeAma.data.edit_bones[0].name
                    newBone = activeAma.data.edit_bones.new(rootBoneName)
                    newBone.parent = activeAma.data.edit_bones[i]
                    newBone.use_connect = True
                    newBone.head = [newPoint.co[0],
                                    newPoint.co[1],
                                    newPoint.co[2]]
            else:
                newBone = activeAma.data.edit_bones[0]
                    
            lastBone = newBone
            lastBone.tail = [baseMesh.data.vertices[-1].co[0],
                            baseMesh.data.vertices[-1].co[1],
                            baseMesh.data.vertices[-1].co[2]]
            #基準辺の削除
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = baseMesh
            bpy.ops.object.select_pattern(pattern=baseMesh.name, case_sensitive=False, extend=False)
            bpy.ops.object.delete(use_global=False)
            
        else:
            #Fullモード以外ではスプラインからアーマチュアを作る
            #Fullじゃない場合は多角形に変換
            newobj.data.splines[0].type = 'POLY'
            #アーマチュアを作成
            bpy.ops.object.armature_add(radius=1, view_align=False, enter_editmode=False,
            location=(0, 0, 0),
            layers=bpy.context.scene.layers)
            activeAma = bpy.context.scene.objects.active
            activeAma.name = boneName
            activeAma.location = newobj.location
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.delete()
            bpy.ops.armature.bone_primitive_add()
            newSpline = newobj.data.splines[0]
            if newSpline.type == 'POLY' or newSpline.type == 'NURBS':
                activeAma.data.edit_bones[0].head = [newSpline.points[0].co[0],
                                                        newSpline.points[0].co[1],
                                                        newSpline.points[0].co[2]]
            else:
                activeAma.data.edit_bones[0].head = [newSpline.bezier_points[0].co[0],
                                                        newSpline.bezier_points[0].co[1],
                                                        newSpline.bezier_points[0].co[2]]
            activeAma.data.edit_bones[0].name = newMeshObj.name + boneName
            if newSpline.type == 'POLY' or newSpline.type == 'NURBS':
                if len(newSpline.points) >= 3:
                    for i,newPoint in enumerate(newSpline.points[1:-1]):
                        rootBoneName = activeAma.data.edit_bones[0].name
                        newBone = activeAma.data.edit_bones.new(rootBoneName)
                        newBone.parent = activeAma.data.edit_bones[i]
                        newBone.use_connect = True
                        newBone.head = [newPoint.co[0],
                                        newPoint.co[1],
                                        newPoint.co[2]]
                else:
                    newBone = activeAma.data.edit_bones[0]
            else:
                if len(newSpline.bezier_points) >= 3:
                    for i,newPoint in enumerate(newSpline.bezier_points[1:-1]):
                        rootBoneName = activeAma.data.edit_bones[0].name
                        newBone = activeAma.data.edit_bones.new(rootBoneName)
                        newBone.parent = activeAma.data.edit_bones[i]
                        newBone.use_connect = True
                        newBone.head = [newPoint.co[0],
                                        newPoint.co[1],
                                        newPoint.co[2]]
                else:
                    newBone = activeAma.data.edit_bones[0]
            lastBone = newBone
            if newSpline.type == 'POLY' or newSpline.type == 'NURBS':
                lastBone.tail = [newSpline.points[-1].co[0],
                                newSpline.points[-1].co[1],
                                newSpline.points[-1].co[2]]
            else:
                lastBone.tail = [newSpline.bezier_points[-1].co[0],
                                newSpline.bezier_points[-1].co[1],
                                newSpline.bezier_points[-1].co[2]]
            bpy.ops.object.editmode_toggle()
        activeAma.data.draw_type = "STICK"
        #アーマチュアにスプラインIKをセット
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = activeAma
        bpy.ops.object.select_pattern(pattern=activeAma.name, case_sensitive=False, extend=False)
        bpy.ops.object.posemode_toggle()
        if len(activeAma.pose.bones) >= 1:
            spIK = activeAma.pose.bones[-1].constraints.new("SPLINE_IK")
            spIK.target = newobj
            spIK.chain_count = len(activeAma.data.bones)
            spIK.use_chain_offset = False
            spIK.use_y_stretch = ystretch
            spIK.use_curve_radius = radiusFlag
            if radiusFlag:
                spIK.use_curve_radius = True
            else:
                spIK.use_curve_radius = False
            activeAma.pose.bones[-1]["spIKName"] = newobj.name
            
        bpy.ops.object.posemode_toggle()
        newobj.data.resolution_u = 64
        #重複した頂点を削除
        meshobj = newMeshObj
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=meshobj.name, case_sensitive=False, extend=False)
        bpy.context.scene.objects.active = meshobj
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.object.editmode_toggle()
        #自動のウェイトでアーマチュアを設定
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=meshobj.name, case_sensitive=False, extend=False)
        bpy.ops.object.select_pattern(pattern=activeAma.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = activeAma
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        #シェイプキーを２つ追加し、一つをBasis、一つをKey1にする
        curve = newobj
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = curve
        bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
        bpy.ops.object.shape_key_add(from_mix=False)
        bpy.ops.object.shape_key_add(from_mix=False)
        curve.data.shape_keys.key_blocks[1].value = 1
        bpy.context.object.active_shape_key_index = 1
        #Curveをレントゲンにして透けて見えるように
        curve.show_x_ray = True
        activeAmaList.append(activeAma)
    #アーマチュアとメッシュを合成
    pmesh = newMeshObjList[-1]
    bpy.ops.object.select_all(action='DESELECT')
    for mesh in newMeshObjList:
        bpy.context.scene.objects.active = mesh
        bpy.ops.object.select_pattern(pattern=mesh.name, case_sensitive=False, extend=True)
    bpy.context.scene.objects.active = pmesh
    bpy.ops.object.select_pattern(pattern=pmesh.name, case_sensitive=False, extend=True)
    bpy.ops.object.join()
    #Curveの親用のEmptyを作る
    bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=curveobjs[0].location)
    emptyobj = bpy.context.scene.objects.active
    emptyobj.name = boneName + "Emp"
    #アーマチュアの親オブジェクトを作る
    bpy.ops.object.armature_add(location=curveobjs[0].location,enter_editmode=False)
    pama = bpy.context.scene.objects.active
    pama.data.bones[0].use_deform = False
    #Curveの親を設定
    for c in newObjList:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=c.name, case_sensitive=False, extend=False)
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = emptyobj
        bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
    #アーマチュアを合成
    bpy.ops.object.select_all(action='DESELECT')
    for ama in activeAmaList:
        bpy.ops.object.select_pattern(pattern=ama.name, case_sensitive=False, extend=True)
    bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=True)
    bpy.context.scene.objects.active = pama
    pama.data.draw_type = "STICK"
    bpy.ops.object.join()
    pama = bpy.context.scene.objects.active
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=False)
    bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
    bpy.context.scene.objects.active = emptyobj
    bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
    pama.name = boneName
    #親エンプティの回転を元のCurveと同じにする
    emptyobj.rotation_euler = curveobjs[0].rotation_euler
    #アーマチュアのデータを随時更新に変更
    pama.use_extra_recalc_data = True
    #このアーマチュアの名前のボーングループをセット
    boneGroups = pama.pose.bone_groups.new(boneName)
    for bone in pama.pose.bones:
        bone.bone_group = boneGroups
    layers=(False, False,
         False, False, False, False, False, False,
         False, False, False, False, False, False,
         False, False, False, False, False, False,
         False, False, False, True, False, False,
         False, False, False, False, False, False)
    for i,bone in enumerate(pama.data.bones):
        if i != 0:
            bone.layers = layers
    #アーマチュアのみの場合はメッシュを消す
    if amaOnly:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = pmesh
        bpy.ops.object.select_pattern(pattern=pmesh.name, case_sensitive=False, extend=False)
        bpy.ops.object.delete(use_global=False)

    else:
        #メッシュオブジェクトにアーマチュアを設定
        pmesh.modifiers[-1].object = pama
        pmesh.hide_select = hideSelect
    #選択をEmptyに
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = emptyobj
    bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=False)
    
        
#Bevel用のカーブを作成する
#verts : 頂点配列
#loopFlag : ループするかしないか
#order_uValue : 次数
#resulution_uValue : 解像度
#splineType : NURBS・ベジエ・多角形などのスプラインのタイプ
def make_bevelCurve(verts, loopFlag, order_uValue, resolution_uValue,splineType='NURBS'):
    bpy.ops.curve.primitive_nurbs_circle_add(radius=0.1, view_align=False,
    enter_editmode=False, location=(0, 0, 0), layers=(False, False, False,
    False, False, False, False, False, False, False, False, False, False,
    False, False, False, False, False, True, False))
    curve = bpy.context.scene.objects.active
    #頂点をすべて消す
    curve.data.splines.clear()
    newSpline = curve.data.splines.new(type='NURBS')
    #頂点を追加していく
    newSpline.points.add(len(verts)-1)
    for vert,newPoint in zip(verts,newSpline.points):
        newPoint.co = vert
    #ループにする
    newSpline.use_cyclic_u = loopFlag
    #次数を2にする
    newSpline.order_u = order_uValue
    #解像度を1にする
    newSpline.resolution_u = resolution_uValue
    newSpline.use_endpoint_u = True
    #スプラインのタイプを設定
    newSpline.type = splineType

#オペレータークラス
#オブジェクトの辺をアニメ風の髪に変換
#カーブの再変換もできる
class AnimeHairOperator(bpy.types.Operator):
    bl_idname = "object.animehair"
    bl_label = "AnimeHair"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "メッシュの辺をアニメ風の髪の毛に変換"

    my_int_bevelType = bpy.props.IntProperty(name="BevelType",min=0,max=14)
    my_int_taparType = bpy.props.IntProperty(name="TaperType",min=0,max=7)
    my_float_x = bpy.props.FloatProperty(name="X",default=1.0,min=0.0)
    my_float_y = bpy.props.FloatProperty(name="Y",default=1.0,min=0.0)
    my_float_weight = bpy.props.FloatProperty(name="SoftBody Goal",default=0.3,min=0.0,max=1.0)
    my_float_mass = bpy.props.FloatProperty(name="SoftBody Mass",default=0.3,min=0.0,)
    my_float_goal_friction = bpy.props.FloatProperty(name="SoftBody Friction",default=5.0,min=0.0)
    my_beziers_auto = bpy.props.BoolProperty(name="Beziers Auto",default=False)
    
    my_simple_flag = bpy.props.BoolProperty(name="simplify Curve")
    my_simple_err = bpy.props.FloatProperty(name="Simple_err",default=0.015,description="値を上げるほどカーブがシンプルになる",min=0.0,step=1)
    my_digout = bpy.props.IntProperty(default=0,name="digout",min=0) #次数
    my_reso = bpy.props.IntProperty(default=3,name="resolusion",min=0) #カーブの解像度

    def execute(self, context):
        #選択オブジェクトを保存
        active = bpy.context.scene.objects.active
        #選択オブジェクトのタイプを保存
        actype = active.type
        #選択オブジェクトがガーブ＆メッシュ以外だったらReturn
        if not (actype=='MESH' or actype=='CURVE'):
            return {'FINISHED'}
        #選択オブジェクトのメッシュがメッシュだったらカーブに変換
        if actype == 'MESH':
        	#カーブに変換
        	bpy.ops.object.convert(target='CURVE')
        
        #NurbsかBeziersに変換
        bpy.ops.object.editmode_toggle()
        
        if self.my_beziers_auto:
            for s in active.data.splines:
                s.type = 'BEZIER'
            for s in active.data.splines:
                for p in s.bezier_points:
                    p.handle_left_type = 'AUTO'
                    p.handle_right_type = 'AUTO'
        else:
            bpy.ops.curve.spline_type_set(type='NURBS') 
        bpy.ops.object.editmode_toggle()

        
        #指定された場合カーブをシンプル化
        if self.my_simple_flag:
            pre_curve = bpy.context.active_object
            bpy.ops.curve.simplify(output='INPUT', error=self.my_simple_err,
             degreeOut=self.my_digout, keepShort=True)
            #シンプルカーブの設定を変更
            simp_Curve = bpy.context.scene.objects.active
            simp_Curve.data.dimensions = '3D'
            simp_Curve.data.resolution_u = self.my_reso
            #元のカーブを削除
            bpy.ops.object.select_pattern(pattern=pre_curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.delete()
            bpy.ops.object.select_pattern(pattern=simp_Curve.name, case_sensitive=False, extend=False)
            
        #終点とスムーズを設定
        for spline in bpy.context.scene.objects.active.data.splines:
            spline.use_endpoint_u = True #終点を設定
            spline.use_smooth = True #スムーズを設定
            
        #元々設定されているベベルとテーパーを削除
        taperobj = bpy.context.scene.objects.active.data.taper_object
        bevelobj = bpy.context.scene.objects.active.data.bevel_object
        for scene in bpy.data.scenes:
            for obj in scene.objects:
                if obj == taperobj:
                    scene.objects.unlink(taperobj)
                if obj == bevelobj:
                    scene.objects.unlink(bevelobj)
        if taperobj != None:
            bpy.data.objects.remove(taperobj)
        if bevelobj != None:
            bpy.data.objects.remove(bevelobj)
    
        #テイパーを設定
        target = bpy.context.scene.objects.active
        if self.my_int_taparType == 0:
            for spline in bpy.context.active_object.data.splines:
                if spline.type == 'BEZIER':
                    spline.bezier_points[-1].radius = 0.0
                else:
                    spline.points[-1].radius = 0.0
        elif self.my_int_taparType == 1:
            for spline in bpy.context.active_object.data.splines:
                for point in spline.points:
                    point.radius = 1.0
        elif self.my_int_taparType == 2:
            verts = [(-2.0, 1.29005, 0.0, 1.0), (-1.0, 0.97704, 0.0, 1.0), (0.0, 0.67615, 0.0, 1.0), (1.0, 0.33936, 0.0, 1.0), (2.0, 0.0, 0.0, 1.0)]
            make_Path(verts)
        elif self.my_int_taparType == 3:
            verts = [(-2.0, 0.82815, 0.0, 1.0), (-1.0, 1.08073, 0.0, 1.0), (0.0, 1.12222, 0.0, 1.0), (1.0, 0.14653, 0.0, 1.0), (2.0, 0.0, 0.0, 1.0)]
            make_Path(verts)
        elif self.my_int_taparType == 4:
            verts = [(-2.0, 1.74503, 0.0, 1.0), (-1.0, 1.74503, 0.0, 1.0), (0.0, 1.74503, 0.0, 1.0), (1.0, 1.74503, 0.0, 1.0), (2.0, 0.0, 0.0, 1.0)]
            make_Path(verts)
        elif self.my_int_taparType == 5:
            verts = [(-2.0, 0.0, 0.0, 1.0), (-1.0, 1.517, 0.0, 1.0), (0.0, 1.9242, 0.0, 1.0), (1.0, 1.81018, 0.0, 1.0), (2.0, 0.0, 0.0, 1.0)]
            make_Path(verts)
        elif self.my_int_taparType == 6:
            verts = [(-2.0, 1.6929, 0.0, 1.0), (-1.0, 0.79381, 0.0, 1.0), (0.0, 0.3801, 0.0, 1.0), (1.0, 0.12926, 0.0, 1.0), (2.0, 0.0, 0.0, 1.0)]
            make_Path(verts)
        elif self.my_int_taparType == 7:
            verts = [(-2.0, 1.17495, 0.0, 1.0), (-1.0, 1.27268, 0.0, 1.0), (0.0, 0.9632, 0.0, 1.0), (1.0, -1.26827, 0.0, 1.0), (2.0, 0.0, 0.0, 1.0)]
            make_Path(verts)
        else:
            print("errer 01")
        target.data.taper_object = bpy.context.scene.objects.active
        bpy.context.scene.objects.active = target
        
        #ベベルを設定
        target = bpy.context.scene.objects.active
        if self.my_int_bevelType == 0:
            verts = [(0.0, -0.1, 0.0, 1.0), (-0.1, -0.1, 0.0, 0.354), (-0.1, 0.0, 0.0, 1.0), (-0.1, 0.1, 0.0, 0.354), (0.0, 0.1, 0.0, 1.0), (0.1, 0.1, 0.0, 0.354), (0.1, 0.0, 0.0, 1.0), (0.1, -0.1, 0.0, 0.354)]
            make_bevelCurve(verts,True,4,3)
        elif self.my_int_bevelType == 1:
            verts = [(0.0, -0.1, 0.0, 1.0), (-0.01341, -0.01341, 0.0, 0.354), (-0.1, 0.0, 0.0, 1.0), (-0.01341, 0.01341, 0.0, 0.354), (0.0, 0.1, 0.0, 1.0), (0.01341, 0.01341, 0.0, 0.354), (0.1, 0.0, 0.0, 1.0), (0.01341, -0.01341, 0.0, 0.354)]
            make_bevelCurve(verts,True,4,3)
        elif self.my_int_bevelType == 2:
            verts = [(0.0, -0.05443, 0.0, 1.0), (-0.10876, -0.05093, 0.0, 0.354), (-0.15258, 0.05083, 0.0, 1.0), (-0.04917, 0.01237, 0.0, 0.354), (0.0, 0.08072, 0.0, 1.0), (0.04216, 0.00711, 0.0, 0.354), (0.17186, 0.05083, 0.0, 1.0), (0.10351, -0.04917, 0.0, 0.354)]
            make_bevelCurve(verts,True,4,3)
        elif self.my_int_bevelType == 3:
            verts = [(0.0, -0.1, 0.0, 1.0), (-0.1, -0.1, 0.0, 0.354), (-0.15173, -0.07836, 0.0, 1.0), (-0.11293, 0.07718, 0.0, 0.354), (0.0, 0.1, 0.0, 1.0), (0.12282, 0.0749, 0.0, 0.354), (0.1601, -0.07608, 0.0, 1.0), (0.1, -0.1, 0.0, 0.354)]
            make_bevelCurve(verts,True,4,3)
        elif self.my_int_bevelType == 4:
            verts = [(0.0, -0.1, 0.0, 1.0), (-0.1, -0.1, 0.0, 0.354), (-0.15173, -0.07836, 0.0, 1.0), (-0.02207, -0.02882, 0.0, 0.354), (0.0, 0.1, 0.0, 1.0), (0.03385, -0.02542, 0.0, 0.354), (0.1601, -0.07608, 0.0, 1.0), (0.1, -0.1, 0.0, 0.354)]
            make_bevelCurve(verts,True,4,3)
        elif self.my_int_bevelType == 5:
            verts = [(0.0,-0.10737,0.0,1.0),(-0.02482,-0.05971,0.0,1.0),(-0.07637,-0.07637,0.0,1.0)\
            ,(-0.05971,-0.02482,0.0,1.0),(-0.10737,0.0,0.0,1.0),(-0.05971,0.02482,0.0,1.0)\
            ,(-0.07637,0.07637,0.0,1.0),(-0.02482,0.05971,0.0,1.0),(0.0,0.10737,0.0,1.0)\
            ,(0.02482,0.05971,0.0,1.0),(0.07637,0.07637,0.0,1.0),(0.05971,0.02482,0.0,1.0)\
            ,(0.10737,0.0,0.0,1.0),(0.05971,-0.02482,0.0,1.0),(0.07637,-0.07637,0.0,1.0)\
            ,(0.02482,-0.05971,0.0,1.0)]
            make_bevelCurve(verts,True,2,1)
        elif self.my_int_bevelType == 6:
            verts = [(-0.10737,0.0,0.0,1.0),(-0.05971,0.02482,0.0,1.0)\
            ,(-0.07637,0.07637,0.0,1.0),(-0.02482,0.05971,0.0,1.0),(0.0,0.10737,0.0,1.0)\
            ,(0.02482,0.05971,0.0,1.0),(0.07637,0.07637,0.0,1.0),(0.05971,0.02482,0.0,1.0)\
            ,(0.10737,0.0,0.0,1.0)]
            make_bevelCurve(verts,False,2,1,'POLY')
        elif self.my_int_bevelType == 7:
            verts = [(-0.21377,-0.01224,0.0,1.0),(-0.21369,0.01544,0.0,1.0),(-0.05366,0.01465,0.0,1.0),\
            (0.0,0.08072,0.0,1.0),(0.04366,0.01472,0.0,1.0),(0.23172,0.01658,0.0,1.0),\
            (0.23112,-0.00807,0.0,1.0)]
            make_bevelCurve(verts,False,4,3)
        elif self.my_int_bevelType == 8:
            verts = [(-0.21369,-0.00024,0.0,1.0),(0.0,0.06504,0.0,1.0),\
            (0.23172,0.0009,0.0,1.0)]
            make_bevelCurve(verts,False,3,3)
        elif self.my_int_bevelType == 9:
            verts = [(-0.21369,-0.00024,0.0,1.0),(0.0,-0.06517,0.0,1.0),\
            (0.23172,0.0009,0.0,1.0)]
            make_bevelCurve(verts,False,3,3)
        elif self.my_int_bevelType == 10:
            verts = [(-0.21369,-0.00024,0.0,1.0),(0.23172,0.0009,0.0,1.0)]
            make_bevelCurve(verts,False,2,2)
        elif self.my_int_bevelType == 11:
            verts = [(0.0,-0.00981,0.0,1.0),(-0.160276,-0.012221,0.0,1.0),(-0.179911,-0.052557,0.0,1.0),
            (-0.208451,0.0,0.0,1.0),(-0.17869,0.051167,0.0,1.0),(-0.159358,0.00654,0.0,1.0),
            (0.0,-0.00414,0.0,1.0),(0.169297,0.008569,0.0,1.0),(0.186631,0.039629,0.0,1.0),
            (0.215239,0.0,0.0,1.0),(0.186103,-0.035806,0.0,1.0),(0.151654,-0.014581,0.0,1.0)]
            make_bevelCurve(verts,True,6,2)
        elif self.my_int_bevelType == 12:
            verts = [(-0.179911,-0.029543,0.0,1.0),
            (-0.208451,0.0,0.0,1.0),(-0.17869,0.051167,0.0,1.0),(-0.159358,0.00654,0.0,1.0),
            (0.0,-0.00414,0.0,1.0),(0.169297,0.008569,0.0,1.0),(0.186631,0.039629,0.0,1.0),
            (0.215239,0.0,0.0,1.0),(0.186103,-0.035806,0.0,1.0)]
            make_bevelCurve(verts,False,6,2)
        elif self.my_int_bevelType == 13:
            verts = [(-0.21369,0.0,0.0,1.0),(-0.185852,0.016927,0.0,1.0),(-0.158014,0.0,0.0,1.0),
            (-0.130176,0.017069,0.0,1.0),(-0.102337,0.0,0.0,1.0),(-0.074499,0.017212,0.0,1.0),
            (-0.046661,0.0,0.0,1.0),(-0.018823,0.017354,0.0,1.0),(0.009015,0.0,0.0,1.0),
            (0.036853,0.017497,0.0,1.0),(0.064691,0.0,0.0,1.0),(0.092529,0.017639,0.0,1.0),
            (0.120367,0.0,0.0,1.0),(0.148206,0.017782,0.0,1.0),(0.176044,0.0,0.0,1.0),
            (0.203882,0.017924,0.0,1.0),(0.23172,0.0,0.0,1.0)]
            make_bevelCurve(verts,False,2,1,'POLY')
        elif self.my_int_bevelType == 14:
            verts = [(-0.1,0,0,1),(0.1,0,0,1)]
            make_bevelCurve(verts,False,2,1,'POLY')
        else:
            print("errer 02")
        bpy.context.object.scale[0] = self.my_float_x
        bpy.context.object.scale[1] = self.my_float_y
        target.data.bevel_object = bpy.context.scene.objects.active
        bpy.context.scene.objects.active = target
        
        #UVを設定
        bpy.context.object.data.use_uv_as_generated = True
        bpy.context.object.data.use_fill_caps = False

        #選択オブジェクトの名前を取得
        objname = bpy.context.scene.objects.active.data.name
        
        #元々がメッシュだったらゴールウェイトを設定
        if actype == 'MESH':
            #すべてのpointsのゴールウェイトに0を設定
            for spline in bpy.data.curves[objname].splines:
                if self.my_beziers_auto:
                    for p in spline.bezier_points:
                        p.weight_softbody = 0
                else:
    	            for point in spline.points:
    	                point.weight_softbody = self.my_float_weight
	    #根本とその次のゴールウェイトに1を設定
        for spline in bpy.data.curves[objname].splines:
            if spline.type=='BEZIER':
                spline.bezier_points[0].weight_softbody = 1
                spline.bezier_points[1].weight_softbody = 1
                print("softweight",spline.bezier_points[0].weight_softbody)
            else:
               spline.points[0].weight_softbody = 1
               spline.points[1].weight_softbody = 1
            
        #ソフトボディを設定
        bpy.ops.object.modifier_add(type='SOFT_BODY')
        bpy.context.scene.objects.active.soft_body.mass = self.my_float_mass
        bpy.context.scene.objects.active.soft_body.goal_friction = self.my_float_goal_friction
        bpy.context.scene.objects.active.soft_body.goal_default = 1.0
        softbody = bpy.context.scene.objects.active.modifiers[0]
        for m in bpy.context.scene.objects.active.modifiers:
        	if m.type == 'SOFT_BODY':
        		softbody = m
        softbody.point_cache.frame_step = 1
        
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
#カーブの全制御点の半径の値をソフトボディウェイトにコピー
class Radius2weight(bpy.types.Operator):
    bl_idname = "object.radiustoweight"
    bl_label = "Radius -> SoftBody_Weight"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "カーブの全制御点の半径の値をソフトボディウェイトにコピー"

    my_float_max_radius = bpy.props.FloatProperty(name="Threshold",default=1.0,min=0.0)

    def execute(self, context):
        active = bpy.context.scene.objects.active
        for spline in active.data.splines:
            if spline.type == 'POLY' or spline.type == 'NURBS':
                for point in spline.points:
                    #しきい値以下だったらコピー
                    if self.my_float_max_radius >= point.radius:
                        point.weight_softbody = point.radius
            else:
                for p in spline.bezier_points:
                    if self.my_float_max_radius >= p.radius:
                        p.weight_softbody = p.radius
        return {'FINISHED'}

#Curveをアーマチュア付きメッシュに変換
class Hair2MeshOperator(bpy.types.Operator):
    bl_idname = "object.hair2mesh"
    bl_label = "Hair -> Mesh"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "Curveをアーマチュア付きメッシュに変換"

    my_boneName = bpy.props.StringProperty(name="BoneName",default="Untitled")
    my_ystretch = bpy.props.BoolProperty(name="Y stretch")
    my_radius = bpy.props.BoolProperty(name="Radius",default = False)
    my_hide_select = bpy.props.BoolProperty(name="hide select", default=False)
    my_fullMode = bpy.props.BoolProperty(name="Full Mode", default=True)
    my_amaOnly = bpy.props.BoolProperty(name="Amarture Only", default=False)

    def execute(self, context):
        actives = bpy.context.selected_objects
        curveConvert(actives,meshFlag=True, fullFlag=self.my_fullMode, boneName=self.my_boneName,
            ystretch=self.my_ystretch, radiusFlag=self.my_radius,
            hideSelect=self.my_hide_select, amaOnly=self.my_amaOnly)
        return {'FINISHED'}
        
        active = bpy.context.scene.objects.active
        curveList = []
        amaList = []
        meshList = []
        defaultrot = active.rotation_euler
        for i,spline in enumerate(active.data.splines):
            #スプラインの頂点が一つしか無かったら処理を中止して次に行く
            if len(spline.points) <= 1:
                continue
            #スプライン一つ一つにカーブオブジェクトを作る
            pos = active.location
            bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False,
                enter_editmode=False, location=pos)
            #Curveの設定からコピーできるものをコピーする
            curve = bpy.context.scene.objects.active
            oldCurve = active
            #splineを全て消し、既存のものからコピーする
            curve.data.splines.clear()
            newSpline = curve.data.splines.new(type='NURBS')
            newSpline.points.add(len(spline.points)-1)
            for point,newPoint in zip(spline.points,newSpline.points):
                newPoint.co = point.co
                newPoint.radius = point.radius
                newPoint.tilt = point.tilt
                newPoint.weight_softbody = point.weight_softbody
            newSpline.use_smooth = spline.use_smooth
            newSpline.use_endpoint_u = spline.use_endpoint_u
            newSpline.use_bezier_u = spline.use_bezier_u
            newSpline.id_data.bevel_object = spline.id_data.bevel_object
            newSpline.id_data.taper_object = spline.id_data.taper_object
            newSpline.id_data.use_fill_caps = False
            newSpline.id_data.resolution_u = spline.id_data.resolution_u
            newSpline.id_data.render_resolution_u = spline.id_data.render_resolution_u
            newSpline.order_u = spline.order_u
            newSpline.resolution_u = spline.resolution_u
            curve.data.twist_mode = oldCurve.data.twist_mode
            curve.data.use_auto_texspace = oldCurve.data.use_auto_texspace
            curve.data.use_uv_as_generated = oldCurve.data.use_uv_as_generated
            if newSpline.id_data.bevel_object == None:
                newSpline.id_data.bevel_depth = spline.id_data.bevel_depth
                newSpline.id_data.bevel_resolution = spline.id_data.bevel_resolution
                curve.data.fill_mode = oldCurve.data.fill_mode
                curve.data.offset = oldCurve.data.offset
                curve.data.extrude = oldCurve.data.extrude
                curve.data.bevel_depth = oldCurve.data.bevel_depth
                curve.data.bevel_resolution = oldCurve.data.bevel_resolution
            #ソフトボディを設定
            if oldCurve.soft_body != None:
        	    bpy.ops.object.modifier_add(type='SOFT_BODY')
        	    curve.soft_body.mass = oldCurve.soft_body.mass
        	    curve.soft_body.goal_friction = oldCurve.soft_body.goal_friction 
        	    curve.soft_body.friction = oldCurve.soft_body.friction
        	    curve.soft_body.speed = oldCurve.soft_body.speed
        	    curve.soft_body.goal_default = oldCurve.soft_body.goal_default
        	    curve.soft_body.goal_max = oldCurve.soft_body.goal_max
        	    curve.soft_body.goal_min = oldCurve.soft_body.goal_min
        	    curve.soft_body.goal_spring = oldCurve.soft_body.goal_spring
            #アーマチュアを作る
            bpy.ops.object.armature_add(location=pos,enter_editmode=False)
            activeAma = bpy.context.scene.objects.active
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.delete()
            bpy.ops.armature.bone_primitive_add()
            activeAma.data.edit_bones[0].head = [newSpline.points[0].co[0],
                                                    newSpline.points[0].co[1],
                                                    newSpline.points[0].co[2]]
            activeAma.data.edit_bones[0].name = self.my_boneName + str(i)
            if len(newSpline.points) >= 3:
                for i,newPoint in enumerate(newSpline.points[1:-1]):
                    rootBoneName = activeAma.data.edit_bones[0].name
                    newBone = activeAma.data.edit_bones.new(rootBoneName)
                    newBone.parent = activeAma.data.edit_bones[i]
                    newBone.use_connect = True
                    newBone.head = [newPoint.co[0],
                                    newPoint.co[1],
                                    newPoint.co[2]]
            else:
                newBone = activeAma.data.edit_bones[0]
            lastBone = newBone
            lastBone.tail = [newSpline.points[-1].co[0],
                            newSpline.points[-1].co[1],
                            newSpline.points[-1].co[2]]
            activeAma.data.draw_type = "STICK"
            #ボーンのセグメントを設定（設定しない方が綺麗に動くので終了）
            #for bone in activeAma.data.edit_bones:
            #    bone.bbone_segments = newSpline.order_u
            #カーブを実体化する
            #物理に使うので元のカーブは残す
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.convert(target='MESH', keep_original=True)
            meshobj = bpy.context.scene.objects.active
            #マテリアルをコピーする
            if len(oldCurve.data.materials) >= 1:
                material = oldCurve.data.materials[spline.material_index]
                meshobj.data.materials.append(material) 
            #元のカーブは多角形にしてBevelやテイパーやメッシュを外してを設定して、物理として使う
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bebelObj = curve.data.bevel_object
            curve.data.bevel_object = None
            curve.data.taper_object = None
            curve.data.bevel_depth = 0
            curve.data.bevel_resolution = 0
            curve.data.extrude = 0
            newSpline.type = 'POLY'
            #アーマチュアにスプラインIKをセット
            if len(activeAma.pose.bones) >= 1:
                spIK = activeAma.pose.bones[-1].constraints.new("SPLINE_IK")
                spIK.target = curve
                spIK.chain_count = len(activeAma.data.bones)
                spIK.use_chain_offset = False
                spIK.use_y_stretch = self.my_ystretch
                if self.my_radius:
                    spIK.use_curve_radius = True
                else:
                    spIK.use_curve_radius = False
            activeAma.pose.bones[-1]["spIKName"] = curve.name
            curve.data.resolution_u = 64
            #重複した頂点を削除
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=meshobj.name, case_sensitive=False, extend=False)
            bpy.context.scene.objects.active = meshobj
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.mesh.remove_doubles(threshold=0.0001)
            bpy.ops.object.editmode_toggle()
            #自動のウェイトでアーマチュアを設定
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=meshobj.name, case_sensitive=False, extend=False)
            bpy.ops.object.select_pattern(pattern=activeAma.name, case_sensitive=False, extend=True)
            bpy.context.scene.objects.active = activeAma
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
            #シェイプキーを２つ追加し、一つをBasis、一つをKey1にする
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.shape_key_add(from_mix=False)
            bpy.ops.object.shape_key_add(from_mix=False)
            curve.data.shape_keys.key_blocks[1].value = 1
            bpy.context.object.active_shape_key_index = 1
            #Curveをレントゲンにして透けて見えるように
            curve.show_x_ray = True
            #Curveとアーマチュアとメッシュは後でまとめるのでリストにする
            curveList.append(curve)
            amaList.append(activeAma)
            meshList.append(meshobj)
        #Curveの親用のEmptyを作る
        bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=active.location)
        emptyobj = bpy.context.scene.objects.active
        emptyobj.name = self.my_boneName + "Emp"
        #アーマチュアの親オブジェクトを作る
        bpy.ops.object.armature_add(location=active.location,enter_editmode=False)
        pama = bpy.context.scene.objects.active
        pama.data.bones[0].use_deform = False
        #Curveの親を設定
        for c in curveList:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=c.name, case_sensitive=False, extend=False)
            bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
            bpy.context.scene.objects.active = emptyobj
            bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
        #アーマチュアを合成
        bpy.ops.object.select_all(action='DESELECT')
        for ama in amaList:
            bpy.ops.object.select_pattern(pattern=ama.name, case_sensitive=False, extend=True)
        bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = pama
        pama.data.draw_type = "STICK"
        bpy.ops.object.join()
        pama = bpy.context.scene.objects.active
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=False)
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = emptyobj
        bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
        pama.name = self.my_boneName
        #メッシュを合成
        bpy.ops.object.select_all(action='DESELECT')
        for m in meshList:
            bpy.ops.object.select_pattern(pattern=m.name, case_sensitive=False, extend=True)
        if len(meshList) >= 1:
            bpy.context.scene.objects.active = meshList[0]
            bpy.ops.object.join()
            activeMesh = bpy.context.scene.objects.active
            activeMesh.modifiers["Armature"].object = pama
            #メッシュを選択不可能オブジェクトにする
            activeMesh.hide_select = self.my_hide_select
        #親エンプティの回転を元のCurveと同じにする
        emptyobj.rotation_euler = defaultrot
        #アーマチュアのデータを随時更新に変更
        pama.use_extra_recalc_data = True
        #このアーマチュアの名前のボーングループをセット
        boneGroups = pama.pose.bone_groups.new(self.my_boneName)
        for bone in pama.pose.bones:
            bone.bone_group = boneGroups
        layers=(False, False,
             False, False, False, False, False, False,
             False, False, False, False, False, False,
             False, False, False, False, False, False,
             False, False, False, True, False, False,
             False, False, False, False, False, False)
        for i,bone in enumerate(pama.data.bones):
            if i != 0:
                bone.layers = layers
        #選択をEmptyに
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=False)
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

#Curveをアーマチュアに変換
class Curve2AmaOperator(bpy.types.Operator):
    bl_idname = "object.curve2ama"
    bl_label = "Curve -> Ama"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "Curveをアーマチュアに変換"

    my_boneName = bpy.props.StringProperty(name="BoneName",default="Untitled")
    my_ystretch = bpy.props.BoolProperty(name="Y stretch")
    my_radius = bpy.props.BoolProperty(name="Radius",default = False)

    def execute(self, context):
        active = bpy.context.scene.objects.active
        curveList = []
        amaList = []
        #meshList = []
        for i,spline in enumerate(active.data.splines):
            #スプラインの頂点が一つしか無かったら処理を中止して次に行く
            if len(spline.points) <= 1:
                continue
            #スプライン一つ一つにカーブオブジェクトを作る
            pos = active.location
            defaultrot = active.rotation_euler
            bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False,
                enter_editmode=False, location=pos)
            #Curveの設定からコピーできるものをコピーする
            curve = bpy.context.scene.objects.active
            oldCurve = active
            #splineを全て消し、既存のものからコピーする
            curve.data.splines.clear()
            newSpline = curve.data.splines.new(type='NURBS')
            newSpline.points.add(len(spline.points)-1)
            for point,newPoint in zip(spline.points,newSpline.points):
                newPoint.co = point.co
                newPoint.radius = point.radius
                newPoint.tilt = point.tilt
                newPoint.weight_softbody = point.weight_softbody
            newSpline.use_smooth = spline.use_smooth
            newSpline.use_endpoint_u = spline.use_endpoint_u
            newSpline.use_bezier_u = spline.use_bezier_u
            newSpline.id_data.bevel_object = spline.id_data.bevel_object
            newSpline.id_data.taper_object = spline.id_data.taper_object
            newSpline.id_data.use_fill_caps = False
            newSpline.id_data.resolution_u = spline.id_data.resolution_u
            newSpline.id_data.render_resolution_u = spline.id_data.render_resolution_u
            newSpline.order_u = spline.order_u
            newSpline.resolution_u = spline.resolution_u
            curve.data.twist_mode = oldCurve.data.twist_mode
            if newSpline.id_data.bevel_object == None:
                newSpline.id_data.bevel_depth = spline.id_data.bevel_depth
                newSpline.id_data.bevel_resolution = spline.id_data.bevel_resolution
            #ソフトボディを設定
            if oldCurve.soft_body != None:
                bpy.ops.object.modifier_add(type='SOFT_BODY')
                curve.soft_body.mass = oldCurve.soft_body.mass
                curve.soft_body.goal_friction = oldCurve.soft_body.goal_friction
                curve.soft_body.friction = oldCurve.soft_body.friction
                curve.soft_body.speed = oldCurve.soft_body.speed
                curve.soft_body.goal_default = oldCurve.soft_body.goal_default
                curve.soft_body.goal_max = oldCurve.soft_body.goal_max
                curve.soft_body.goal_min = oldCurve.soft_body.goal_min
                curve.soft_body.goal_spring = oldCurve.soft_body.goal_spring
            #アーマチュアを作る
            bpy.ops.object.armature_add(location=pos,enter_editmode=False)
            activeAma = bpy.context.scene.objects.active
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.delete()
            bpy.ops.armature.bone_primitive_add()
            activeAma.data.edit_bones[0].head = [newSpline.points[0].co[0],
                                                    newSpline.points[0].co[1],
                                                    newSpline.points[0].co[2]]
            activeAma.data.edit_bones[0].name = self.my_boneName + str(i)
            if len(newSpline.points) >= 3:
                for i,newPoint in enumerate(newSpline.points[1:-1]):
                    rootBoneName = activeAma.data.edit_bones[0].name
                    newBone = activeAma.data.edit_bones.new(rootBoneName)
                    newBone.parent = activeAma.data.edit_bones[i]
                    newBone.use_connect = True
                    newBone.head = [newPoint.co[0],
                                    newPoint.co[1],
                                    newPoint.co[2]]
            else:
                newBone = activeAma.data.edit_bones[0]
            lastBone = newBone
            lastBone.tail = [newSpline.points[-1].co[0],
                            newSpline.points[-1].co[1],
                            newSpline.points[-1].co[2]]
            activeAma.data.draw_type = "STICK"
            #元のカーブは多角形にしてBevelやテイパーやメッシュを外してを設定して、物理として使う
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bebelObj = curve.data.bevel_object
            curve.data.bevel_object = None
            curve.data.taper_object = None
            curve.data.bevel_depth = 0
            curve.data.bevel_resolution = 0
            newSpline.type = 'POLY'
            #アーマチュアにスプラインIKをセット
            if len(activeAma.pose.bones) >= 1:
                spIK = activeAma.pose.bones[-1].constraints.new("SPLINE_IK")
                spIK.target = curve
                spIK.chain_count = len(activeAma.data.bones)
                spIK.use_chain_offset = False
                spIK.use_y_stretch = self.my_ystretch
                if self.my_radius:
                    spIK.use_curve_radius = True
                else:
                    spIK.use_curve_radius = False
                activeAma.pose.bones[-1]["spIKName"] = curve.name
            curve.data.resolution_u = 64
            #シェイプキーを２つ追加し、一つをBasis、一つをKey1にする
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.shape_key_add(from_mix=False)
            bpy.ops.object.shape_key_add(from_mix=False)
            curve.data.shape_keys.key_blocks[1].value = 1
            bpy.context.object.active_shape_key_index = 1
            #Curveをレントゲンにして透けて見えるように
            curve.show_x_ray = True
            #Curveとアーマチュアとメッシュは後でまとめるのでリストにする
            curveList.append(curve)
            amaList.append(activeAma)
        #Curveの親用のEmptyを作る
        bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=active.location)
        emptyobj = bpy.context.scene.objects.active
        emptyobj.name = self.my_boneName + "Emp"
        #アーマチュアの親オブジェクトを作る
        bpy.ops.object.armature_add(location=active.location,enter_editmode=False)
        pama = bpy.context.scene.objects.active
        pama.data.bones[0].use_deform = False
        #Curveの親を設定
        for c in curveList:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=c.name, case_sensitive=False, extend=False)
            bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
            bpy.context.scene.objects.active = emptyobj
            bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
        #アーマチュアを合成
        bpy.ops.object.select_all(action='DESELECT')
        for ama in amaList:
            bpy.ops.object.select_pattern(pattern=ama.name, case_sensitive=False, extend=True)
        bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = pama
        pama.data.draw_type = "STICK"
        bpy.ops.object.join()
        pama = bpy.context.scene.objects.active
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=False)
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = emptyobj
        bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
        pama.name = self.my_boneName
        #親エンプティの回転を元のCurveと同じにする
        emptyobj.rotation_euler = defaultrot
        #アーマチュアのデータを随時更新に変更
        pama.use_extra_recalc_data = True
        #このアーマチュアの名前のボーングループをセット
        boneGroups = pama.pose.bone_groups.new(self.my_boneName)
        for bone in pama.pose.bones:
            bone.bone_group = boneGroups
        layers=(False, False,
             False, False, False, False, False, False,
             False, False, False, False, False, False,
             False, False, False, False, False, False,
             False, False, False, True, False, False,
             False, False, False, False, False, False)
        for i,bone in enumerate(pama.data.bones):
            if i != 0:
                bone.layers = layers
        #選択をEmptyに
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=False)
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

#Curveを正確なアーマチュア付きメッシュに変換
class Hair2MeshFullOperator(bpy.types.Operator):
    bl_idname = "object.hair2meshfull"
    bl_label = "Hair -> Mesh_Full"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "Curveを正確なアーマチュア付きメッシュに変換"

    my_boneName = bpy.props.StringProperty(name="BoneName",default="Untitled")
    my_ystretch = bpy.props.BoolProperty(name="Y stretch")
    my_radius = bpy.props.BoolProperty(name="Radius",default = False)
    my_hide_select = bpy.props.BoolProperty(name="hide select", default=False)

    def execute(self, context):
        active = bpy.context.scene.objects.active
        curveList = []
        amaList = []
        meshList = []
        for i,spline in enumerate(active.data.splines):
            #スプラインの頂点が一つしか無かったら処理を中止して次に行く
            if len(spline.points) <= 1:
                continue
            #スプライン一つ一つにカーブオブジェクトを作る
            pos = active.location
            defaultrot = active.rotation_euler
            bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False,
                enter_editmode=False, location=pos)
            #Curveの設定からコピーできるものをコピーする
            curve = bpy.context.scene.objects.active
            oldCurve = active
            #splineを全て消し、既存のものからコピーする
            curve.data.splines.clear()
            newSpline = curve.data.splines.new(type='NURBS')
            newSpline.points.add(len(spline.points)-1)
            for point,newPoint in zip(spline.points,newSpline.points):
                newPoint.co = point.co
                newPoint.radius = point.radius
                newPoint.tilt = point.tilt
                newPoint.weight_softbody = point.weight_softbody
            newSpline.use_smooth = spline.use_smooth
            newSpline.use_endpoint_u = spline.use_endpoint_u
            newSpline.use_bezier_u = spline.use_bezier_u
            newSpline.id_data.bevel_object = spline.id_data.bevel_object
            newSpline.id_data.taper_object = spline.id_data.taper_object
            newSpline.id_data.use_fill_caps = False
            newSpline.id_data.resolution_u = spline.id_data.resolution_u
            newSpline.id_data.render_resolution_u = spline.id_data.render_resolution_u
            newSpline.order_u = spline.order_u
            newSpline.resolution_u = spline.resolution_u
            curve.data.twist_mode = oldCurve.data.twist_mode
            curve.data.use_auto_texspace = oldCurve.data.use_auto_texspace
            curve.data.use_uv_as_generated = oldCurve.data.use_uv_as_generated
            if newSpline.id_data.bevel_object == None:
                newSpline.id_data.bevel_depth = spline.id_data.bevel_depth
                newSpline.id_data.bevel_resolution = spline.id_data.bevel_resolution
                curve.data.fill_mode = oldCurve.data.fill_mode
                curve.data.offset = oldCurve.data.offset
                curve.data.extrude = oldCurve.data.extrude
                curve.data.bevel_depth = oldCurve.data.bevel_depth
                curve.data.bevel_resolution = oldCurve.data.bevel_resolution
            #ソフトボディを設定
            if oldCurve.soft_body != None:
                bpy.ops.object.modifier_add(type='SOFT_BODY')
                curve.soft_body.mass = oldCurve.soft_body.mass
                curve.soft_body.goal_friction = oldCurve.soft_body.goal_friction
                curve.soft_body.friction = oldCurve.soft_body.friction
                curve.soft_body.speed = oldCurve.soft_body.speed
                curve.soft_body.goal_default = oldCurve.soft_body.goal_default
                curve.soft_body.goal_max = oldCurve.soft_body.goal_max
                curve.soft_body.goal_min = oldCurve.soft_body.goal_min
                curve.soft_body.goal_spring = oldCurve.soft_body.goal_spring
            #アーマチュア制作用の基準カーブを作る
            bpy.context.scene.objects.active = curve
            bpy.ops.object.duplicate()
            stdCurve = bpy.context.scene.objects.active
            stdCurve.name = "stdCurve"
            stdCurve.data.bevel_depth = 0
            stdCurve.data.extrude = 0
            stdCurve.data.bevel_object = None
            bpy.ops.object.convert(target='MESH', keep_original=False)
            stdCurveObj = bpy.context.scene.objects.active
            #アーマチュアを作る
            bpy.ops.object.armature_add(location=pos,enter_editmode=False)
            activeAma = bpy.context.scene.objects.active
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.delete()
            bpy.ops.armature.bone_primitive_add()
            activeAma.data.edit_bones[0].head = [stdCurveObj.data.vertices[0].co[0],
                                                    stdCurveObj.data.vertices[0].co[1],
                                                    stdCurveObj.data.vertices[0].co[2]]
            activeAma.data.edit_bones[0].name = self.my_boneName + str(i)
            if len(stdCurveObj.data.vertices) >= 3:
                for i,newPoint in enumerate(stdCurveObj.data.vertices[1:-1]):
                    rootBoneName = activeAma.data.edit_bones[0].name
                    newBone = activeAma.data.edit_bones.new(rootBoneName)
                    newBone.parent = activeAma.data.edit_bones[i]
                    newBone.use_connect = True
                    newBone.head = [newPoint.co[0],
                                    newPoint.co[1],
                                    newPoint.co[2]]
            else:
                newBone = activeAma.data.edit_bones[0]
            lastBone = newBone
            lastBone.tail = [stdCurveObj.data.vertices[-1].co[0],
                            stdCurveObj.data.vertices[-1].co[1],
                            stdCurveObj.data.vertices[-1].co[2]]
            activeAma.data.draw_type = "STICK"
            #カーブを実体化する
            #物理に使うので元のカーブは残す
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.convert(target='MESH', keep_original=True)
            meshobj = bpy.context.scene.objects.active
            #マテリアルをコピーする
            if len(oldCurve.data.materials) >= 1:
                material = oldCurve.data.materials[spline.material_index]
                meshobj.data.materials.append(material)
            #元のカーブは多角形にしてBevelやテイパーやメッシュを外してを設定して、物理として使う
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bebelObj = curve.data.bevel_object
            curve.data.bevel_object = None
            curve.data.taper_object = None
            curve.data.bevel_depth = 0
            curve.data.bevel_resolution = 0
            #newSpline.type = curve.data.spline[0].type
            #アーマチュアにスプラインIKをセット
            if len(activeAma.pose.bones) >= 1:
                spIK = activeAma.pose.bones[-1].constraints.new("SPLINE_IK")
                spIK.target = curve
                spIK.chain_count = len(activeAma.data.bones)
                spIK.use_chain_offset = False
                spIK.use_y_stretch = self.my_ystretch
                if self.my_radius:
                    spIK.use_curve_radius = True
                else:
                    spIK.use_curve_radius = False
                activeAma.pose.bones[-1]["spIKName"] = curve.name
            curve.data.resolution_u = 64
            #重複した頂点を削除
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=meshobj.name, case_sensitive=False, extend=False)
            bpy.context.scene.objects.active = meshobj
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.mesh.remove_doubles(threshold=0.0001)
            bpy.ops.object.editmode_toggle()
            #自動のウェイトでアーマチュアを設定
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=meshobj.name, case_sensitive=False, extend=False)
            bpy.ops.object.select_pattern(pattern=activeAma.name, case_sensitive=False, extend=True)
            bpy.context.scene.objects.active = activeAma
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
            #シェイプキーを２つ追加し、一つをBasis、一つをKey1にする
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.shape_key_add(from_mix=False)
            bpy.ops.object.shape_key_add(from_mix=False)
            curve.data.shape_keys.key_blocks[1].value = 1
            bpy.context.object.active_shape_key_index = 1
            #Curveをレントゲンにして透けて見えるように
            curve.show_x_ray = True
            #Curveとアーマチュアとメッシュは後でまとめるのでリストにする
            curveList.append(curve)
            amaList.append(activeAma)
            meshList.append(meshobj)
            #基準カーブ消去
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = stdCurveObj
            bpy.ops.object.select_pattern(pattern=stdCurveObj.name, case_sensitive=False, extend=False)
            bpy.ops.object.delete(use_global=False)
        #Curveの親用のEmptyを作る
        bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=active.location)
        emptyobj = bpy.context.scene.objects.active
        emptyobj.name = self.my_boneName + "Emp"
        #アーマチュアの親オブジェクトを作る
        bpy.ops.object.armature_add(location=active.location,enter_editmode=False)
        pama = bpy.context.scene.objects.active
        pama.data.bones[0].use_deform = False
        #Curveの親を設定
        for c in curveList:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=c.name, case_sensitive=False, extend=False)
            bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
            bpy.context.scene.objects.active = emptyobj
            bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
        #アーマチュアを合成
        bpy.ops.object.select_all(action='DESELECT')
        for ama in amaList:
            bpy.ops.object.select_pattern(pattern=ama.name, case_sensitive=False, extend=True)
        bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = pama
        pama.data.draw_type = "STICK"
        bpy.ops.object.join()
        pama = bpy.context.scene.objects.active
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=False)
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = emptyobj
        bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
        pama.name = self.my_boneName
        #メッシュを合成
        bpy.ops.object.select_all(action='DESELECT')
        for m in meshList:
            bpy.ops.object.select_pattern(pattern=m.name, case_sensitive=False, extend=True)
        if len(meshList) >= 1:
            bpy.context.scene.objects.active = meshList[0]
            bpy.ops.object.join()
            activeMesh = bpy.context.scene.objects.active
            activeMesh.modifiers["Armature"].object = pama
            #メッシュを選択不可能オブジェクトにする
            activeMesh.hide_select = self.my_hide_select
        #親エンプティの回転を元のCurveと同じにする
        emptyobj.rotation_euler = defaultrot
        #アーマチュアのデータを随時更新に変更
        pama.use_extra_recalc_data = True
        #このアーマチュアの名前のボーングループをセット
        boneGroups = pama.pose.bone_groups.new(self.my_boneName)
        for bone in pama.pose.bones:
            bone.bone_group = boneGroups
        layers=(False, False,
             False, False, False, False, False, False,
             False, False, False, False, False, False,
             False, False, False, False, False, False,
             False, False, False, True, False, False,
             False, False, False, False, False, False)
        for i,bone in enumerate(pama.data.bones):
            if i != 0:
                bone.layers = layers
                
        #選択をEmptyに
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=False)
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

#Curveを正確なアーマチュアに変換
class Curve2AmaFullOperator(bpy.types.Operator):
    bl_idname = "object.curve2amafull"
    bl_label = "Curve -> Ama_Full"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "Curveを正確なアーマチュアに変換"

    my_boneName = bpy.props.StringProperty(name="BoneName",default="Untitled")
    my_ystretch = bpy.props.BoolProperty(name="Y stretch")
    my_radius = bpy.props.BoolProperty(name="Radius",default = False)

    def execute(self, context):
        active = bpy.context.scene.objects.active
        curveList = []
        amaList = []
        #meshList = []
        for i,spline in enumerate(active.data.splines):
            #スプラインの頂点が一つしか無かったら処理を中止して次に行く
            if len(spline.points) <= 1:
                continue
            #スプライン一つ一つにカーブオブジェクトを作る
            pos = active.location
            defaultrot = active.rotation_euler
            bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False,
                enter_editmode=False, location=pos)
            #Curveの設定からコピーできるものをコピーする
            curve = bpy.context.scene.objects.active
            oldCurve = active
            #splineを全て消し、既存のものからコピーする
            curve.data.splines.clear()
            newSpline = curve.data.splines.new(type='NURBS')
            newSpline.points.add(len(spline.points)-1)
            for point,newPoint in zip(spline.points,newSpline.points):
                newPoint.co = point.co
                newPoint.radius = point.radius
                newPoint.tilt = point.tilt
                newPoint.weight_softbody = point.weight_softbody
            newSpline.use_smooth = spline.use_smooth
            newSpline.use_endpoint_u = spline.use_endpoint_u
            newSpline.use_bezier_u = spline.use_bezier_u
            newSpline.id_data.bevel_object = spline.id_data.bevel_object
            newSpline.id_data.taper_object = spline.id_data.taper_object
            newSpline.id_data.use_fill_caps = False
            newSpline.id_data.resolution_u = spline.id_data.resolution_u
            newSpline.id_data.render_resolution_u = spline.id_data.render_resolution_u
            newSpline.order_u = spline.order_u
            newSpline.resolution_u = spline.resolution_u
            curve.data.twist_mode = oldCurve.data.twist_mode
            if newSpline.id_data.bevel_object == None:
                newSpline.id_data.bevel_depth = spline.id_data.bevel_depth
                newSpline.id_data.bevel_resolution = spline.id_data.bevel_resolution
            #ソフトボディを設定
            if oldCurve.soft_body != None:
                bpy.ops.object.modifier_add(type='SOFT_BODY')
                curve.soft_body.mass = oldCurve.soft_body.mass
                curve.soft_body.goal_friction = oldCurve.soft_body.goal_friction
                curve.soft_body.friction = oldCurve.soft_body.friction
                curve.soft_body.speed = oldCurve.soft_body.speed
                curve.soft_body.goal_default = oldCurve.soft_body.goal_default
                curve.soft_body.goal_max = oldCurve.soft_body.goal_max
                curve.soft_body.goal_min = oldCurve.soft_body.goal_min
                curve.soft_body.goal_spring = oldCurve.soft_body.goal_spring
            #アーマチュア制作用の基準カーブを作る
            bpy.context.scene.objects.active = curve
            bpy.ops.object.duplicate()
            stdCurve = bpy.context.scene.objects.active
            stdCurve.name = "stdCurve"
            stdCurve.data.bevel_depth = 0
            stdCurve.data.extrude = 0
            stdCurve.data.bevel_object = None
            bpy.ops.object.convert(target='MESH', keep_original=False)
            stdCurveObj = bpy.context.scene.objects.active
            #アーマチュアを作る
            bpy.ops.object.armature_add(location=pos,enter_editmode=False)
            activeAma = bpy.context.scene.objects.active
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.delete()
            bpy.ops.armature.bone_primitive_add()
            
            activeAma.data.edit_bones[0].head = [stdCurveObj.data.vertices[0].co[0],
                                                    stdCurveObj.data.vertices[0].co[1],
                                                    stdCurveObj.data.vertices[0].co[2]]
            activeAma.data.edit_bones[0].name = self.my_boneName + str(i)
            if len(stdCurveObj.data.vertices) >= 3:
                for i,newPoint in enumerate(stdCurveObj.data.vertices[1:-1]):
                    rootBoneName = activeAma.data.edit_bones[0].name
                    newBone = activeAma.data.edit_bones.new(rootBoneName)
                    newBone.parent = activeAma.data.edit_bones[i]
                    newBone.use_connect = True
                    newBone.head = [newPoint.co[0],
                                    newPoint.co[1],
                                    newPoint.co[2]]
            else:
                newBone = activeAma.data.edit_bones[0]
            lastBone = newBone
            lastBone.tail = [stdCurveObj.data.vertices[-1].co[0],
                            stdCurveObj.data.vertices[-1].co[1],
                            stdCurveObj.data.vertices[-1].co[2]]
            activeAma.data.draw_type = "STICK"
            #元のカーブは多角形にしてBevelやテイパーやメッシュを外してを設定して、物理として使う
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bebelObj = curve.data.bevel_object
            curve.data.bevel_object = None
            curve.data.taper_object = None
            curve.data.bevel_depth = 0
            curve.data.bevel_resolution = 0
            #newSpline.type = curve.data.spline[0].type
            #アーマチュアにスプラインIKをセット
            if len(activeAma.pose.bones) >= 1:
                spIK = activeAma.pose.bones[-1].constraints.new("SPLINE_IK")
                spIK.target = curve
                spIK.chain_count = len(activeAma.data.bones)
                spIK.use_chain_offset = False
                spIK.use_y_stretch = self.my_ystretch
                if self.my_radius:
                    spIK.use_curve_radius = True
                else:
                    spIK.use_curve_radius = False
                activeAma.pose.bones[-1]["spIKName"] = curve.name
            curve.data.resolution_u = 64
            #シェイプキーを２つ追加し、一つをBasis、一つをKey1にする
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.shape_key_add(from_mix=False)
            bpy.ops.object.shape_key_add(from_mix=False)
            curve.data.shape_keys.key_blocks[1].value = 1
            bpy.context.object.active_shape_key_index = 1
            #Curveをレントゲンにして透けて見えるように
            curve.show_x_ray = True
            #Curveとアーマチュアとメッシュは後でまとめるのでリストにする
            curveList.append(curve)
            amaList.append(activeAma)
            #基準カーブ消去
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = stdCurveObj
            bpy.ops.object.select_pattern(pattern=stdCurveObj.name, case_sensitive=False, extend=False)
            bpy.ops.object.delete(use_global=False)
        #Curveの親用のEmptyを作る
        bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=active.location)
        emptyobj = bpy.context.scene.objects.active
        emptyobj.name = self.my_boneName + "Emp"
        #アーマチュアの親オブジェクトを作る
        bpy.ops.object.armature_add(location=active.location,enter_editmode=False)
        pama = bpy.context.scene.objects.active
        pama.data.bones[0].use_deform = False
        #Curveの親を設定
        for c in curveList:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=c.name, case_sensitive=False, extend=False)
            bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
            bpy.context.scene.objects.active = emptyobj
            bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
        #アーマチュアを合成
        bpy.ops.object.select_all(action='DESELECT')
        for ama in amaList:
            bpy.ops.object.select_pattern(pattern=ama.name, case_sensitive=False, extend=True)
        bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = pama
        pama.data.draw_type = "STICK"
        bpy.ops.object.join()
        pama = bpy.context.scene.objects.active
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=pama.name, case_sensitive=False, extend=False)
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = emptyobj
        bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
        pama.name = self.my_boneName
        #親エンプティの回転を元のCurveと同じにする
        emptyobj.rotation_euler = defaultrot
        #アーマチュアのデータを随時更新に変更
        pama.use_extra_recalc_data = True
        #このアーマチュアの名前のボーングループをセット
        boneGroups = pama.pose.bone_groups.new(self.my_boneName)
        for bone in pama.pose.bones:
            bone.bone_group = boneGroups
        layers=(False, False,
             False, False, False, False, False, False,
             False, False, False, False, False, False,
             False, False, False, False, False, False,
             False, False, False, True, False, False,
             False, False, False, False, False, False)
        for i,bone in enumerate(pama.data.bones):
            if i != 0:
                bone.layers = layers
        #選択をEmptyに
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=emptyobj.name, case_sensitive=False, extend=False)
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

#全てのボーンのスプラインIKのミュートを外す
class ViewSpIKOperator(bpy.types.Operator):
	bl_idname = "object.viewspik"
	bl_label = "ViewSPIK"
	bl_options = {'REGISTER','UNDO'}
	bl_description = "全てのボーンに付いているスプラインIKからミュートを外す"
	def execute(self, context):
		ama = bpy.context.scene.objects.active
		for bone in ama.pose.bones:
		    if len(bone.constraints) >= 1:
		        for con in bone.constraints:
		            if con.type == "SPLINE_IK":
		                con.mute = False
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.editmode_toggle()
		return {'FINISHED'}

#全てのボーンのスプラインIKをミュート
class HiddenSpIKOperator(bpy.types.Operator):
	bl_idname = "object.hiddenspik"
	bl_label = "MuteSPIK"
	bl_options = {'REGISTER','UNDO'}
	bl_description = "全てのボーンに付いているスプラインIKをミュート"
	def execute(self, context):
		ama = bpy.context.scene.objects.active
		for bone in ama.pose.bones:
		    if len(bone.constraints) >= 1:
		        for con in bone.constraints:
		            if con.type == "SPLINE_IK":
		                con.mute = True
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.editmode_toggle()
		return {'FINISHED'}

#すべてのボーンのコンストレントのミュートを外す
class ViewBoneConstOperator(bpy.types.Operator):
    bl_idname = "object.viewboneconst"
    bl_label = "ViewSPIK"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "全てのボーンコンストレイントに付いているミュートを外す"
    def execute(self, context):
        ama = bpy.context.scene.objects.active
        for bone in ama.pose.bones:
            if len(bone.constraints) >= 1:
                for con in bone.constraints:
                    con.mute = False
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
#すべてのボーンのコンストレントのミュートをミュート
class HiddenBoneConstOperator(bpy.types.Operator):
    bl_idname = "object.hidenboneconst"
    bl_label = "ViewSPIK"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "全てのボーンコンストレイントをミュート"
    def execute(self, context):
        ama = bpy.context.scene.objects.active
        for bone in ama.pose.bones:
            if len(bone.constraints) >= 1:
                for con in bone.constraints:
                    con.mute = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'} 
       
#おっぱい作成機能
class MakePIOperator(bpy.types.Operator):
    bl_idname = "object.make_pi"
    bl_label = "Make PI"
    #bl_options = {'REGISTER','UNDO'}
    bl_description = "選択中の頂点を膨らませる"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_float_emp_normal_value = bpy.props.FloatProperty(name="normal Value",default=0.0,step=0.01)
    my_float_normal_mix = bpy.props.FloatProperty(name="mix Value",default=1.0,max=1.0,min=0.0,step=0.01)
    my_float_normal_disp = bpy.props.FloatProperty(name="Disp Value",default=0.0,max=1.0,min=0.0,step=0.01)
    
    def execute(self, context):
        emp_normal_value = self.my_float_emp_normal_value
        normal_mix = self.my_float_normal_mix
        normal_disp = self.my_float_normal_disp
        
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        obj.data.use_auto_smooth = True
        
        #select vertex list
        sel_verts = [v for v in bm.verts if v.select]
        
        # average normal and vector
        ave_normal = [0,0,0]
        ave_co = [0,0,0]
        for v in sel_verts :
            normal_local = v.normal.to_4d()
            normal_local.w = 0
            world_n = (obj.matrix_world * normal_local).to_3d()
            ave_normal[0] += world_n[0]
            ave_normal[1] += world_n[1]
            ave_normal[2] += world_n[2]
            
            world_v = obj.matrix_world * v.co
            ave_co[0] += world_v[0]
            ave_co[1] += world_v[1]
            ave_co[2] += world_v[2]
            
        for i,a in enumerate(ave_normal):
            ave_normal[i] /= len(sel_verts)
        for i,a in enumerate(ave_co):
            ave_co[i] /= len(sel_verts)
        
        #make average empty
        a = np.array(ave_co)# ベクトルaの生成
        b = np.array(ave_normal)# ベクトルbの生成
        c = np.array(obj.location)
        an_co = a +(b * emp_normal_value) # ベクトルa,b,cの和
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=an_co, layers=obj.layers)
        empty_obj = bpy.context.active_object
        
        #make vertex group
        bpy.context.scene.objects.active = obj
        bpy.ops.object.vertex_group_add()
        vg = bpy.context.active_object.vertex_groups[-1]
        vg.name = "PI"
        bpy.ops.object.editmode_toggle()
        bpy.context.scene.tool_settings.vertex_group_weight = 1.0
        bpy.ops.object.vertex_group_assign()
        
        #make NormalEdit
        bpy.context.scene.objects.active = obj
        bpy.ops.object.modifier_add(type='NORMAL_EDIT')
        normal_edit = obj.modifiers[-1]
        normal_edit.mix_factor = normal_mix
        normal_edit.target = empty_obj
        normal_edit.vertex_group = vg.name
        
        #make disp
        if normal_disp > 0.0:
            bpy.ops.object.modifier_add(type='DISPLACE')
            disp = obj.modifiers[-1]
            bpy.context.object.modifiers[disp.name].direction = 'CUSTOM_NORMAL'
            bpy.context.object.modifiers[disp.name].vertex_group = vg.name
            bpy.context.object.modifiers[disp.name].strength = normal_disp
            bpy.ops.object.modifier_move_up(modifier=disp.name)
            
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        
#グリースペンシルをラインに変換
class Gp2LineOperator(bpy.types.Operator):
    bl_idname = "object.gp2line"
    bl_label = "greasePencil -> Line"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "選択中のグリースペンシルをカーブを使ったラインに変換(要:Simplify curvesアドオン)"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    #設定
    my_thick = bpy.props.FloatProperty(name="line thick",default=0.02,min=0.00)
    my_irinuki = bpy.props.BoolProperty(default=True,name="IritoNuki")
    my_loop = bpy.props.BoolProperty(default=False,name="loop")
    my_strokeLink = bpy.props.BoolProperty(default=False,name="Stroke Link")
    my_pivot_center = bpy.props.BoolProperty(default=False,name="Pivot Center")
    my_simple_err = bpy.props.FloatProperty(name="Simple_err",default=0.015,description="値を上げるほどカーブがシンプルになる",min=0.0,step=1)
    my_digout = bpy.props.IntProperty(default=0,name="digout",min=0) #次数
    my_reso = bpy.props.IntProperty(default=3,name="resolusion",min=0) #カーブの解像度
    
    def execute(self, context):
        active_obj = bpy.context.scene.objects.active

        #グリースペンシルの頂点位置を取得
        #選択されたグリースペンシルがシーンかオブジェクトかを判断
        gp_source = bpy.context.scene.tool_settings.grease_pencil_source
        if gp_source == "SCENE":
            active_gp = bpy.context.scene.grease_pencil.layers.active
        else:
            active_gp = bpy.context.object.grease_pencil.layers.active
        if active_gp.active_frame != None:
            #空のカーブを作成
            bpy.ops.curve.primitive_nurbs_path_add()
            curve = bpy.context.active_object
            bpy.ops.object.location_clear()
            #頂点をすべて消す
            curve.data.splines.clear()
            bpy.context.scene.objects.active = active_obj
            #空のカーブにStrokeの位置を入れる    
            for i, stroke in enumerate(active_gp.active_frame.strokes):
                #新しいスプラインを追加
                if self.my_simple_err > 0.0:
                    newSpline = curve.data.splines.new(type='NURBS')
                else:
                    newSpline = curve.data.splines.new(type='POLY')
                newSpline.points.add(len(stroke.points)-1)
                for sPoint,newPoint in zip(stroke.points,newSpline.points):
                    newPoint.co = [sPoint.co[0],sPoint.co[1],sPoint.co[2],1.0]
            #カーブの各スプラインを接続する
            if self.my_strokeLink:
                #空のカーブを作成
                bpy.ops.curve.primitive_nurbs_path_add()
                curve3 = bpy.context.active_object
                bpy.ops.object.location_clear()
                #頂点をすべて消す
                curve3.data.splines.clear()
                #スプラインを一つ作る
                curvetype = curve.data.splines[0].type
                newSpline3 = curve3.data.splines.new(type=curvetype)
                #全頂点数を数える
                spline_len = 0
                for spline in curve.data.splines:
                    spline_len += len(spline.points)
                for i,c2spline in enumerate(curve.data.splines):
                    for j,c2point in enumerate(c2spline.points):
                        #最初の1個だけはaddせずもう出来ているものにコピー
                        if i==0 and j==0:
                            newSpline3.points[0].co = c2point.co
                        else:
                            newSpline3.points.add(1)
                            newSpline3.points[-1].co = c2point.co
                #本のカーブを消して3を入れる
                bpy.context.scene.objects.active = curve
                bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
                bpy.ops.object.delete()
                curve = curve3
            #原点を中心に移動
            bpy.context.scene.objects.active = curve
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            if self.my_pivot_center == False:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            curve2 = curve
            if self.my_simple_err > 0.0:
                #Curvesをシンプル化
                bpy.context.scene.objects.active = curve
                bpy.ops.curve.simplify(output='NURBS', error=self.my_simple_err, degreeOut=self.my_digout, keepShort=True)
                curve2 = bpy.context.scene.objects.active
                #元のカーブを削除
                bpy.context.scene.objects.active = curve
                bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
                bpy.ops.object.delete()
                if self.my_strokeLink:
                    bpy.context.scene.objects.active = curve3
                    bpy.ops.object.select_pattern(pattern=curve3.name, case_sensitive=False, extend=False)
                    bpy.ops.object.delete()
            #カーブの設定を変更
            curve2.data.dimensions = '3D'
            curve2.data.fill_mode = 'FULL'
            curve2.data.bevel_depth = self.my_thick
            for spline in curve2.data.splines:
                spline.use_endpoint_u = True
                #ループ設定
                if self.my_loop:
                    spline.use_cyclic_u = True
            curve2.data.resolution_u = self.my_reso
            curve2.data.bevel_resolution = 1
            #irinuki
            if self.my_irinuki:
                for spline in curve2.data.splines:
                    if len(spline.points) > 2:
                        spline.points[0].radius = 0.0
                        spline.points[-1].radius = 0.0
            bpy.context.scene.objects.active = curve2
            bpy.ops.object.select_pattern(pattern=curve2.name, case_sensitive=False, extend=False)
            
            return {'FINISHED'} 
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
      
#グリースペンシルをメッシュに変換
class Gp2MeshOperator(bpy.types.Operator):
    bl_idname = "object.gp2mesh"
    bl_label = "greasePencil -> Mesh"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "選択中のグリースペンシルをメッシュに変換(要:Simplify curvesアドオン)"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    #設定
    my_addface = bpy.props.BoolProperty(default=True,description="面を貼る",name="Add Face")
    my_loop = bpy.props.BoolProperty(default=True,description="ループ",name="Loop")
    my_strokeLink = bpy.props.BoolProperty(default=False,description="すべての辺を繋いだメッシュにするか",name="Stroke Link")
    my_simple_err = bpy.props.FloatProperty(name="Simple_err",default=0.015,description="値を上げるほどカーブがシンプルになる",min=0.0,step=1)
    my_removedoubles = bpy.props.FloatProperty(name="remove doubles",default=0.0,description="値の距離以下の頂点は結合(0で無効)",min=0.0,step=1)
    my_digout = bpy.props.IntProperty(default=0,name="digout",min=0) #次数
    my_reso = bpy.props.IntProperty(default=3,name="resolusion",min=0) #カーブの解像度
    my_thickness = bpy.props.FloatProperty(name="thicknss",default=0.0,description="厚み付け",step=1)
    my_solioffset = bpy.props.FloatProperty(name="Soli Offset",default=0.0,description="厚み付けのオフセット",min=-1.0,max=1.0,step=1)
    my_isskin = bpy.props.BoolProperty(default=False,description="スキンモディファイアを設定",name="Add Skin")
    my_skinvalueX = bpy.props.FloatProperty(name="skin X",default=0.25,description="",min=0.0,step=1)
    my_skinvalueY = bpy.props.FloatProperty(name="skin Y",default=0.25,description="",min=0.0,step=1)
    
    def execute(self, context):
        #グリースペンシルをカーブに変換
        bpy.ops.object.gp2line(my_thick=0.0,my_irinuki=False,my_loop=self.my_loop,my_simple_err=self.my_simple_err,my_digout=self.my_digout,my_reso=self.my_reso,my_strokeLink=self.my_strokeLink)
        #メッシュに変換
        curve = bpy.context.scene.objects.active
        bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
        bpy.ops.object.convert(target='MESH')
        obj = bpy.context.scene.objects.active
        #頂点を結合
        if self.my_removedoubles > 0.0:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles(threshold=self.my_removedoubles,\
             use_unselected=False)
            bpy.ops.object.editmode_toggle()
        if self.my_addface:
            #編集モードに移行
            bpy.ops.object.editmode_toggle()
            #メッシュごとに全選択しメッシュを貼る
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()
        #厚み付け
        if self.my_thickness != 0.0:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.select_pattern(pattern=obj.name, case_sensitive=False, extend=False)
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            obj.modifiers[-1].thickness = self.my_thickness
            obj.modifiers[-1].offset = self.my_solioffset
        #スキンモディファイアを設定
        if self.my_isskin:
            bpy.ops.object.modifier_add(type='SKIN')
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.skin_resize(value=(self.my_skinvalueX, self.my_skinvalueY, 0.25),\
             constraint_axis=(False, False, False), constraint_orientation='LOCAL',\
             mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            bpy.ops.object.skin_root_mark()
            bpy.ops.object.editmode_toggle()

        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        
#グリースペンシルを髪の毛に変換
class Gp2AnimehairOperator(bpy.types.Operator):
    bl_idname = "object.gp2animehair"
    bl_label = "greasePencil -> AnimeHair"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "選択中のグリースペンシルを髪の毛に変換(要:Simplify curvesアドオン)"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    #グリースペンシル用の設定
    my_irinuki_2 = bpy.props.BoolProperty(default=False,name="IritoNuki")
    my_simple_err_2 = bpy.props.FloatProperty(name="Simple_err",default=0.015,description="値を上げるほどカーブがシンプルになる",min=0.0,step=1)
    my_digout_2 = bpy.props.IntProperty(default=0,name="digout",min=0) #次数
    my_reso_2 = bpy.props.IntProperty(default=3,name="resolusion",min=0) #カーブの解像度
    #アニメヘアー用の設定
    my_int_bevelType_2 = bpy.props.IntProperty(name="BevelType",min=0,max=14)
    my_int_taparType_2 = bpy.props.IntProperty(name="TaperType",min=0,max=7)
    my_float_x_2 = bpy.props.FloatProperty(name="X",default=1.0,min=0.0)
    my_float_y_2 = bpy.props.FloatProperty(name="Y",default=1.0,min=0.0)
    my_float_weight_2 = bpy.props.FloatProperty(name="SoftBody Goal",default=0.3,min=0.0,max=1.0)
    my_float_mass_2 = bpy.props.FloatProperty(name="SoftBody Mass",default=0.3,min=0.0,)
    my_float_goal_friction_2 = bpy.props.FloatProperty(name="SoftBody Friction",default=5.0,min=0.0)
    
    my_beziers_auto = bpy.props.BoolProperty(name="Beziers Auto",default=False)
    my_simple_flag = bpy.props.BoolProperty(name="simplify Curve")
    my_simple_err = bpy.props.FloatProperty(name="Simple_err",default=0.015,description="値を上げるほどカーブがシンプルになる",min=0.0,step=1)
    my_digout = bpy.props.IntProperty(default=0,name="digout",min=0) #次数
    my_reso = bpy.props.IntProperty(default=3,name="resolusion",min=0) #カーブの解像度
    
    
    def execute(self, context):
        bpy.ops.object.gp2line(my_irinuki=self.my_irinuki_2, my_simple_err=self.my_simple_err_2, my_digout=self.my_digout_2, my_reso=self.my_reso_2)
        bpy.ops.object.animehair(my_int_bevelType=self.my_int_bevelType_2, my_int_taparType=self.my_int_taparType_2,\
         my_float_x=self.my_float_x_2, my_float_y=self.my_float_y_2, my_float_weight=self.my_float_weight_2, my_float_mass=self.my_float_mass_2, my_float_goal_friction=self.my_float_goal_friction_2,\
         my_simple_flag=self.my_simple_flag, my_simple_err=self.my_simple_err, my_digout=self.my_digout, my_reso=self.my_reso,
         my_beziers_auto = self.my_beziers_auto)
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        
#カーブをグリースペンシルに変換
class Curve2GPOperator(bpy.types.Operator):
    bl_idname = "object.curve2gp"
    bl_label = "curve -> greasePencil"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "カーブをグリースペンシルに変換"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_loop = bpy.props.BoolProperty(default=False,name="loop")
    my_line_width = bpy.props.IntProperty(name="Line Width",default=3,description="",min=0,step=1)
    my_edgeStroke = bpy.props.BoolProperty(default=False,name="Edge Stroke")
    
    def execute(self, context):
        #カーブをメッシュに変換
        active_obj = bpy.context.scene.objects.active
        if active_obj.type != 'CURVE':
            return {'FINISHED'}
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
        TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False),
        "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED',
        "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False,
        "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False,
        "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False,
        "remove_on_cancel":False, "release_confirm":False})
        dup_obj = bpy.context.scene.objects.active
        dup_obj.data.bevel_depth = 0.0
        dup_obj.data.bevel_object = None
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        dupObjList = bpy.context.selected_objects
        #メッシュをグリースペンシルに変換
        scene = bpy.context.scene
        if scene.grease_pencil == None:
            bpy.ops.gpencil.data_add()
        layer = scene.grease_pencil.layers.new("Curve", set_active=True)
        frame = layer.frames.new(scene.frame_current)
        if len(bpy.context.scene.grease_pencil.palettes) <= 0:
            bpy.ops.gpencil.palette_add()
        if len(bpy.context.scene.grease_pencil.palettes.active.colors) <= 0:
            bpy.ops.gpencil.palettecolor_add()
        gpColor = bpy.context.scene.grease_pencil.palettes.active.colors.active
        if self.my_edgeStroke != True:
            for d in dupObjList:
                stroke = frame.strokes.new()
                stroke.draw_mode = '3DSPACE'
                stroke.line_width = self.my_line_width
                stroke.colorname = gpColor.name
                stroke.points.add(len(d.data.vertices))
                for i,v in enumerate(d.data.vertices):
                    stroke.points[i].co = d.matrix_world * Vector(v.co)
                    stroke.points[i].strength = 1
                    stroke.points[i].pressure = 1
                if self.my_loop:
                    stroke.points.add(1)
                    stroke.points[-1].co = d.matrix_world * Vector(d.data.vertices[0].co)
                    stroke.points[-1].strength = 1
                    stroke.points[-1].pressure = 1
        else:
            for d in dupObjList:
                mesh = d.data
                for edge in mesh.edges:
                    stroke = frame.strokes.new()
                    stroke.draw_mode = '3DSPACE'
                    stroke.line_width = self.my_line_width
                    stroke.colorname = gpColor.name
                    stroke.points.add(2)
                    stroke.points[0].co = d.matrix_world * Vector(mesh.vertices[edge.vertices[0]].co)
                    stroke.points[0].strength = 1
                    stroke.points[0].pressure = 1
                    stroke.points[1].co = d.matrix_world * Vector(mesh.vertices[edge.vertices[1]].co)
                    stroke.points[1].strength = 1
                    stroke.points[1].pressure = 1
                if self.my_loop:
                    stroke = frame.strokes.new()
                    stroke.draw_mode = '3DSPACE'
                    stroke.line_width = self.my_line_width
                    stroke.colorname = gpColor.name
                    stroke.points.add(2)
                    stroke.points[0].co = d.matrix_world * Vector(mesh.vertices[-1].co)
                    stroke.points[0].strength = 1
                    stroke.points[0].pressure = 1
                    stroke.points[1].co = d.matrix_world * Vector(mesh.vertices[0].co)
                    stroke.points[1].strength = 1
                    stroke.points[1].pressure = 1
        #いらない変換後のカーブは消去
        #(いっぺんに消すとフリーズするのでレイヤーを移動させてハイド)
        bpy.ops.object.select_all(action='DESELECT')
        for d in dupObjList:
            bpy.context.scene.objects.active = d
            bpy.ops.object.select_pattern(pattern=d.name, case_sensitive=True, extend=True)
            bpy.ops.object.move_to_layer(layers=(False, False, False, False, False,
             False, False, False, False, False, False, False, False, False,
             False, False, False, False, False, True))
            bpy.context.object.hide_render = True
#            bpy.ops.object.unlink_data()
#            bpy.data.objects.is_updated = True
#            bpy.data.objects.remove(d,True)
        #bpy.ops.object.join()
#        bpy.ops.object.delete()
        bpy.context.scene.objects.active = active_obj
        bpy.ops.object.select_pattern(pattern=active_obj.name, case_sensitive=False, extend=False)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
def menu_draw( self, context ): 
    self.layout.operator_context = 'INVOKE_REGION_WIN' 
    self.layout.operator( MakePIOperator.bl_idname, "make PI" ) 

#指定された角度以上に曲がっている辺にラインを描画
class Crease2LineOperator(bpy.types.Operator):
    bl_idname = "object.crease2line"
    bl_label = "Crease -> Line"
    bl_options = {'REGISTER','UNDO'}
    bl_description = "指定された角度以上の折り目をラインに変換(要:Simplify curvesアドオン)"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    #my_defaultFlag = bpy.props.BoolProperty(default=False,name="Default Select edge",description="デフォルトで選択されている辺を使う")
    my_defaultFlag = False
    my_irinuki = bpy.props.BoolProperty(default=True,name="IritoNuki")
    my_sharp = bpy.props.FloatProperty(name="angle",default=60.0,description="折り目角度",min=0.0,max=180.0)
    my_simple_err = bpy.props.FloatProperty(name="Simple_err",default=0.0,description="値を上げるほどカーブがシンプルに(0で無効)",min=0.0,step=1)
    my_digout = bpy.props.IntProperty(default=0,name="digout",min=0) #次数
    my_thick=bpy.props.FloatProperty(name="line thick",default=0.005,min=0.00)
    my_reso = bpy.props.IntProperty(default=3,name="resolusion",min=0) #カーブの解像度
    my_toGP = bpy.props.BoolProperty(default=False,name="Conversion to GP")
    my_loopGP = bpy.props.BoolProperty(default=False,name="GP Loop")
    my_lineWidth = bpy.props.IntProperty(default=3,name="GP Line Width",min=0) 
    
    def execute(self, context):
        active = bpy.context.scene.objects.active
        #オブジェクトを複数選択していた場合は
        #コピーしてブーリアン
        booleanFlag = False
        if len(bpy.context.selected_objects) >= 2:
            objs = bpy.context.selected_objects
            bpy.ops.object.select_all(action='TOGGLE')
            bpy.context.scene.objects.active = active
            bpy.ops.object.select_pattern(pattern=active.name, case_sensitive=False, extend=False)
            bpy.ops.object.duplicate()
            dup_active = bpy.context.scene.objects.active
            for o in objs:
                if o == active:
                    continue
                bpy.ops.object.modifier_add(type='BOOLEAN')
                dup_active.modifiers[-1].operation = 'UNION'
                dup_active.modifiers[-1].object = o
                bpy.ops.object.convert(target='MESH')
            booleanFlag = True
        #編集モードに以降
        bpy.ops.object.editmode_toggle()
        #デフォルトで選択されている辺を使うか使わないか
        if self.my_defaultFlag == False:
            #クリースを選択
            bpy.ops.mesh.select_all(action='DESELECT')
            sharp = radians(self.my_sharp)
            bpy.ops.mesh.edges_select_sharp(sharpness=sharp)
            
        #何も選択していない場合はエラーなので終わり
        try:
            bpy.ops.mesh.separate(type='SELECTED')
        except:
            bpy.ops.object.editmode_toggle()
            return {'FINISHED'}
        
        #選択した辺を複製
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False),\
         "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1,\
          "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False,\
           "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

        
        #面を選択している場合は除去
        bpy.ops.mesh.delete(type='ONLY_FACE')
        
        #Objectモードへ移行
        bpy.ops.object.editmode_toggle()
        #辺をカーブに変換
        curve = bpy.context.selected_objects[0]
        bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
        bpy.context.scene.objects.active = curve
        bpy.ops.object.convert(target='CURVE')

        if self.my_simple_err > 0.0:
            #Curvesをシンプル化
            bpy.context.scene.objects.active = curve
            bpy.ops.curve.simplify(output='NURBS', error=self.my_simple_err, degreeOut=self.my_digout, keepShort=True)
            #元のカーブを削除
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.delete()
        curve2 = bpy.context.scene.objects.active

        #シンプルカーブの設定を変更
        curve2.data.dimensions = '3D'
        curve2.data.fill_mode = 'FULL'
        curve2.data.bevel_depth = self.my_thick
        for spline in curve2.data.splines:
            spline.use_endpoint_u = True
        curve2.data.resolution_u = self.my_reso
        curve2.data.bevel_resolution = 1
        #irinuki
        if self.my_irinuki:
            for spline in curve2.data.splines:
                if len(spline.points) > 2:
                    spline.points[0].radius = 0.0
                    spline.points[-1].radius = 0.0
        #原点を中心に移動
        bpy.context.scene.objects.active = curve2
        bpy.ops.object.select_pattern(pattern=curve2.name, case_sensitive=False, extend=False)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        
        #コピーしていたものを消す
        if booleanFlag:
            bpy.context.scene.objects.active = dup_active
            bpy.ops.object.select_pattern(pattern=dup_active.name, case_sensitive=False, extend=False)
            bpy.ops.object.delete(use_global=False)
        
        bpy.context.scene.objects.active = curve2
        bpy.ops.object.select_pattern(pattern=curve2.name, case_sensitive=False, extend=False)
        
        #グリースペンシルに変換
        if self.my_toGP:
            bpy.ops.object.curve2gp(my_line_width = self.my_lineWidth,my_loop = self.my_loopGP)
            bpy.ops.object.delete(use_global=False)
            bpy.context.scene.objects.active = active
            bpy.ops.object.select_pattern(pattern=active.name, case_sensitive=False, extend=False)
            
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#カメラティスを設定
class SetCamelattice(bpy.types.Operator):
    bl_idname = "object.setcamelattice"
    bl_label = "set Camelattice"
    bl_description = "カメラの面にラティスを設定"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_depth = bpy.props.FloatProperty(name="depth",default=1.0,description="ラティスとカメラの距離",min=0.0,\
        subtype='DISTANCE',unit='LENGTH')
    my_latu = bpy.props.IntProperty(name="Lattice_u",default=2,description="ラティスの縦",min=2)
    my_latv = bpy.props.IntProperty(name="Lattice_v",default=2,description="ラティスの横",min=2)
    my_latw = bpy.props.IntProperty(name="Lattice_v",default=1,description="ラティスの奥ゆき",min=1)
    my_setLattice = bpy.props.BoolProperty(name="set Lattice",default=False,\
        description="選択したオブジェクトにラティスを設定")
    my_setLatticeAll = bpy.props.BoolProperty(name="set Lattice All",default=False,\
        description="表示されている全てのメッシュオブジェクトにラティスを設定")
    
    def execute(self, context):
        #選択オブジェクトはラティスを設定するときに使う
        selectObjList = bpy.context.selected_objects
        #ラティスを作る
        bpy.ops.object.add(type='LATTICE', view_align=False, enter_editmode=False, location=(0, 0, 0),\
         layers=bpy.data.scenes['Scene'].layers)
        lat = bpy.context.active_object
        #ラティスの大きさの調整
        lat.data.points_u = self.my_latu
        lat.data.points_v = self.my_latv
        lat.data.points_w = self.my_latw
        lat.data.interpolation_type_u = 'KEY_BSPLINE'
        lat.data.interpolation_type_v = 'KEY_BSPLINE'
        lat.data.interpolation_type_w = 'KEY_BSPLINE'
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize( value=(0.5,0.5,0.5))
        bpy.ops.object.editmode_toggle()
        #ラティスをカメラの子にして位置・回転を合わせる
        lat.location = (0,0,-self.my_depth)
        camera = bpy.context.scene.camera
        lat.parent = camera
        lat.lock_rotation[0] = True
        lat.lock_rotation[1] = True
        lat.lock_rotation[2] = True
        lat.lock_location[0] = True
        lat.lock_location[1] = True 
        bpy.ops.object.shape_key_add(from_mix=False)
        bpy.ops.object.shape_key_add(from_mix=False)
        lat.data.shape_keys.key_blocks[1].value = 1.0
        #X,Y拡縮にドライバを設定
        driver = lat.driver_add('scale',1).driver
        driver.type = 'SCRIPTED'
        self.setdrivevalue( driver, lat) 
        driver.expression ="-depth*tan(camAngle/2)*bpy.context.scene.render.resolution_y * bpy.context.scene.render.pixel_aspect_y/(bpy.context.scene.render.resolution_x * bpy.context.scene.render.pixel_aspect_x)*2"
        driver = lat.driver_add('scale',0).driver
        driver.type= 'SCRIPTED'
        self.setdrivevalue( driver, lat)
        driver.expression ="-depth*tan(camAngle/2)*2"
        
        #オブジェクトを選択していた場合ラティスを設定
        objlistlotadd = [0,0,0]
        if len(selectObjList) > 0 and self.my_setLattice:
            for obj in selectObjList:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = obj
                bpy.ops.object.select_pattern(pattern=obj.name, case_sensitive=False, extend=False)
                bpy.ops.object.modifier_add(type='LATTICE')
                obj.modifiers[-1].object = lat
        #表示されている全てのメッシュオブジェクトにラティスを設定
        elif self.my_setLatticeAll:
            viewObjList = []
            viewLayers = bpy.context.scene.layers
            for o in bpy.context.scene.objects:
                if (o.type == 'MESH' or o.type == 'CURVE') and o.hide == False and o.hide_render == False:
                    for i,l in enumerate(viewLayers):
                        if l == True and o.layers[i] == True:
                            bpy.ops.object.select_all(action='DESELECT')
                            bpy.context.scene.objects.active = o
                            bpy.ops.object.select_pattern(pattern=o.name, case_sensitive=False, extend=False)
                            bpy.ops.object.modifier_add(type='LATTICE')
                            o.modifiers[-1].object = lat
        bpy.context.scene.objects.active = lat
        bpy.ops.object.select_pattern(pattern=lat.name, case_sensitive=False, extend=False)
        return {'FINISHED'}
    
    def setdrivevalue(self, driver, lattice):
        angle = driver.variables.new()
        angle.name = 'camAngle'
        angle.type = 'SINGLE_PROP'
        angle.targets[0].id = lattice.parent
        angle.targets[0].data_path="data.angle"
        dep = driver.variables.new()
        dep.name = 'depth'
        dep.type = 'TRANSFORMS'
        dep.targets[0].id = lattice
        dep.targets[0].data_path = 'location'
        dep.targets[0].transform_type = 'LOC_Z'
        dep.targets[0].transform_space = 'LOCAL_SPACE'
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#オブジェクトが設定されていない全てのラティスを削除
class DelNonelattice(bpy.types.Operator):
    bl_idname = "object.delnonelattice"
    bl_label = "del None Lattice"
    bl_description = "オブジェクトが設定されていない全てのラティスを削除"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def execute(self, context):
        for o in bpy.context.scene.objects:
            for m in o.modifiers:
                if m.type == 'LATTICE' :
                    if m.object == None:
                        o.modifiers.remove(m)
        return {'FINISHED'}

#ランダム値が乗算された配列複製
class RandArray(bpy.types.Operator):
    bl_idname = "object.randarray"
    bl_label = "Rand Array"
    bl_description = "選択オブジェクトをランダムやグリースペンシルを使って配列複製"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_count = bpy.props.IntProperty(name="count",default=2,description="数",min=1)
    my_objlink = bpy.props.BoolProperty(name="Object Link",default=True)

    my_offset = bpy.props.FloatVectorProperty(name="offset Lot",default=[0,0,0])
    my_offsetrot = bpy.props.FloatVectorProperty(name="offset rot",default=[0,0,0])
    my_offsetsca = bpy.props.FloatVectorProperty(name="offset Scale",default=[0,0,0])
    
    my_randSeed = bpy.props.IntProperty(default=1,name="Random Seed"\
        ,description="ランダムシード")
    my_rand = bpy.props.FloatVectorProperty(name="rand Lot",default=[0,0,0])
    my_randrot = bpy.props.FloatVectorProperty(name="rand rot",default=[0,0,0])
    my_scale_even = bpy.props.BoolProperty(name="Scale Even",default=False)
    my_randsca = bpy.props.FloatVectorProperty(name="rand Scale",default=[0,0,0])
    
    my_useGP = bpy.props.BoolProperty(name="use GP",default=False)
    my_onGP = bpy.props.BoolProperty(name="on GP",default=True)
    my_simple_err = bpy.props.FloatProperty(name="Simple_err",default=0.02,\
        description="値を上げるほどカーブがシンプルに(0で無効)",min=0.0,step=1)
    my_digout = bpy.props.IntProperty(default=3,name="digout",min=0\
        ,description="カーブ度合い")
    my_reso = bpy.props.IntProperty(default=1,name="resolusion",min=0\
        ,description="解像度")
    
    my_camera_track = bpy.props.BoolProperty(name="Camera Track",default=False)
    
    
    def execute(self, context):
        fobj = bpy.context.active_object
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.scene.objects.active = fobj
        bpy.ops.object.select_pattern(pattern=fobj.name, case_sensitive=False, extend=False)
        curveobj = None
        #選択されたオブジェクトをコピー
        if self.my_useGP:
            #カーブを作る
            bpy.ops.object.gp2line(my_irinuki=False, my_simple_err=self.my_simple_err,\
             my_digout=self.my_digout, my_reso=self.my_reso, my_thick=0)
            #カーブをメッシュに変換
            curve = bpy.context.scene.objects.active
            bpy.ops.object.select_pattern(pattern=curve.name, case_sensitive=False, extend=False)
            bpy.ops.object.convert(target='MESH',keep_original=False)
            curveobj = bpy.context.scene.objects.active
            #グリースペンシルを使用するかしないか
            if self.my_onGP:
                fobjLoc = copy.copy(fobj.location)
                fobj.location = [0,0,0]
                fobj.parent = curveobj
                curLoc = bpy.context.scene.cursor_location.copy()
                bpy.context.scene.cursor_location = fobjLoc
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                fobj.location = fobjLoc
                bpy.context.scene.cursor_location = curLoc
                
            else:
                curveobj.location = [0,0,0]
                curveobj.rotation_euler = [0,0,0]
                curveobj.scale = [1,1,1]
                foblot = copy.copy(fobj.location)
                fobj.parent = curveobj
                fobj.location = [0,0,0]
                curveobj.location = foblot
            #複製　頂点にチェック
            curveobj.dupli_type = "VERTS"
            
        else:
            #グリースペンシルを使用しない場合
            objList = []
            for c in range(self.my_count):
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":self.my_objlink, "mode":'TRANSLATION'},\
                 TRANSFORM_OT_translate={"value":(0,0,0),\
                  "constraint_axis":(False, False, False), "constraint_orientation":'LOCAL',\
                  "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH',\
                  "proportional_size":1, "snap":False, "snap_target":'CLOSEST',\
                  "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),\
                  "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False,\
                  "release_confirm":False})
                active = bpy.context.active_object
                active.location = [0,0,0]
                active.rotation_euler = [0,0,0]
                active.scale = [1,1,1]
                active.parent = fobj
                objList.append(active)
            
            #選択されたオブジェクトの位置・回転・拡縮
            for i,o in enumerate(objList):
                i += 1
                o.location = [self.my_offset[0] * i,\
                              self.my_offset[1] * i,\
                              self.my_offset[2] * i]
                o.rotation_euler = [self.my_offsetrot[0] * i,\
                                    self.my_offsetrot[1] * i,\
                                    self.my_offsetrot[2] * i]
                o.scale = [o.scale[0] + self.my_offsetsca[0] * i,\
                           o.scale[1] + self.my_offsetsca[1] * i,\
                           o.scale[2] + self.my_offsetsca[2] * i]
                           
            #オブジェクトトランスフォームのランダム化
            loc = self.my_rand
            rot = self.my_randrot
            scale = self.my_randsca
            random.seed(self.my_randSeed)
            def rand_vec(vec_range):
                return Vector(random.uniform(-val, val) for val in vec_range)
            for obj in objList:
                obj.location += rand_vec(loc)
                rotvec = rand_vec(rot)
                obj.rotation_euler[0] += rotvec[0]
                obj.rotation_euler[1] += rotvec[1]
                obj.rotation_euler[2] += rotvec[2]
                if self.my_scale_even:
                    scavec = rand_vec(scale)
                    obj.scale[0] += scavec[0]
                    obj.scale[1] += scavec[0]
                    obj.scale[2] += scavec[0]
                else:
                    obj.scale += rand_vec(scale)
                    
        #オブジェクトがカメラの方向を向く機能
        if self.my_camera_track == True:
            if self.my_useGP == True:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = curveobj
                bpy.ops.object.select_pattern(pattern=curveobj.name,\
                 case_sensitive=False, extend=False)
                bpy.ops.object.duplicates_make_real()
                objList = bpy.context.selected_objects
                activeLine = objList.pop()
                bpy.context.scene.objects.active = activeLine
                bpy.ops.object.select_pattern(pattern=activeLine.name,\
                 case_sensitive=False, extend=False)
                bpy.ops.object.delete(use_global=False)
            for o in objList:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = o
                bpy.ops.object.select_pattern(pattern=o.name,\
                 case_sensitive=False, extend=False)
                bpy.ops.object.constraint_add(type='TRACK_TO')
                o.constraints[-1].target = bpy.context.scene.camera
                
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = fobj
        bpy.ops.object.select_pattern(pattern=fobj.name, case_sensitive=False, extend=False)
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#ビル群を作る
class MakeBuildings(bpy.types.Operator):
    bl_idname = "object.makebuildings"
    bl_label = "Make buildings"
    bl_description = "ビル群を作る"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    tex_items = [('CLOUDS','CLOUDS','',1), ('DISTORTED_NOISE','DISTORTED_NOISE','',2),
                ('STUCCI','STUCCI','',3)]
    tex_noisetype_items = [('SOFT_NOISE','SOFT_NOISE','',1),('HARD_NOISE','HARD_NOISE','',2)]
    
    my_subdiv = bpy.props.IntProperty(name="subdivision",default=30,description="分割数",min=1)
    my_texType = bpy.props.EnumProperty(items=tex_items,name="Tex Type",default='CLOUDS')
    my_texNoiseType = bpy.props.EnumProperty(items=tex_noisetype_items,name="Noise Type",default='HARD_NOISE')
    my_useCellNoise = bpy.props.BoolProperty(default=False,name="use Cell Noise")
    my_cloudSize = bpy.props.FloatProperty(name="Tex Size",default=1,min=0)
    my_cloudDepth = bpy.props.IntProperty(name="Tex Depth",default=4,min=0)
    my_texDistortion = bpy.props.FloatProperty(name="Tex Distortion",default=1,min=0)
    my_texTurbulence = bpy.props.FloatProperty(name="Tex Turbulence",default=5,min=0)
    my_dispStrength = bpy.props.FloatProperty(name="Disp Strength",default=6.0)
    my_angleLimit = bpy.props.FloatProperty(name="Angle Limit",default=1,min=0,max=3.14)
    my_use_dissolve_boundaries = bpy.props.BoolProperty(name="All Boundaries",default=True)
    my_step = bpy.props.IntProperty(name="Step",default=10,min=0)
    my_step_hight = bpy.props.FloatProperty(name="Step Hight",default=0.3)
    my_step_hight_rand = bpy.props.FloatProperty(name="Step Hight rand",default=0.0,min=0)
    my_stepSelectPercent = bpy.props.IntProperty(name="Step Select Percent",default=50,min=0,max=100)
    my_stepSelectSeed = bpy.props.IntProperty(name="Step Select Seed",default=1,min=1)
    my_polysaku = bpy.props.BoolProperty(default=True,name="Decimate")
    my_useselect = bpy.props.BoolProperty(default=False,name="use Select")
    my_useVertexG = bpy.props.BoolProperty(default=False,name="use Active Vertex Groups")
    my_useVertNum = bpy.props.IntProperty(name="use Vertex Number",default=2,min=2,
                    description="この数以上の頂点のある面は押し上げない")
    my_useToSphere = bpy.props.FloatProperty(name="use To Sphere",default=0,min=0,max=1)
    my_useSmooth = bpy.props.FloatProperty(name="use Smooth",default=0,min=0)
    my_setRoofTopSize = bpy.props.FloatProperty(name="set Roof Top Size",default=0.003,min=0,step=0.1)
    my_setRoofTopMate = bpy.props.BoolProperty(default=True,name="set Roof Top Material")
    my_delUnder = bpy.props.BoolProperty(default=True,name="Del Under")
   
    
    
    def execute(self, context):
        if self.my_useselect == False:
            bpy.ops.mesh.primitive_grid_add(radius=1, view_align=False,\
            enter_editmode=False, location=(0, 0, 0), layers=bpy.context.scene.layers,\
            x_subdivisions = self.my_subdiv, y_subdivisions=self.my_subdiv)
        
        #ディスプレイス
        act_obj = bpy.context.active_object
        act_obj.show_wire = True
        act_obj.show_all_edges = True
        bpy.ops.object.modifier_add(type='DISPLACE')
        
        if self.my_useselect and self.my_useVertexG:
            if act_obj.vertex_groups.active != None:
                actVGname = act_obj.vertex_groups.active.name
                act_obj.modifiers[-1].vertex_group = actVGname
                act_obj.modifiers[-1].mid_level = 0
        
        bpy.ops.texture.new()
        tex = bpy.data.textures[-1]
        disp = act_obj.modifiers[-1]
        tex.type = self.my_texType
        disp.strength = self.my_dispStrength
        if self.my_texType == 'CLOUDS':
            bpy.data.textures[tex.name].noise_type = self.my_texNoiseType
            bpy.data.textures[tex.name].noise_scale = self.my_cloudSize
            bpy.data.textures[tex.name].noise_depth = self.my_cloudDepth
            if self.my_useCellNoise:
                bpy.data.textures[tex.name].noise_basis = 'CELL_NOISE'
        elif self.my_texType == 'DISTORTED_NOISE':
            bpy.data.textures[tex.name].distortion = self.my_texDistortion
            bpy.data.textures[tex.name].noise_scale = self.my_cloudSize
            if self.my_useCellNoise:
                bpy.data.textures[tex.name].noise_basis = 'CELL_NOISE'
        elif self.my_texType == 'STUCCI':
            bpy.data.textures[tex.name].noise_type = self.my_texNoiseType
            bpy.data.textures[tex.name].noise_scale = self.my_cloudSize
            bpy.data.textures[tex.name].turbulence = self.my_texTurbulence
            if self.my_useCellNoise:
                bpy.data.textures[tex.name].noise_basis = 'CELL_NOISE'
                
        disp.texture = tex
        
        #ポリゴン数削減
        bpy.ops.object.modifier_add(type='DECIMATE')
        decimate = act_obj.modifiers[-1]
        decimate.decimate_type = 'DISSOLVE'
        decimate.angle_limit = self.my_angleLimit
        decimate.use_dissolve_boundaries= self.my_use_dissolve_boundaries
        
        #モディファイアの適用
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=disp.name)
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=decimate.name)
        
        #平面化
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True),\
         constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED',\
         proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        bpy.ops.object.editmode_toggle()
        
        #ランダム選択->引き伸ばし
        if self.my_useVertNum >= 3:
            bpy.ops.mesh.select_face_by_sides(number=self.my_useVertNum, type='LESS',
            extend=False)
        else:
            bpy.ops.mesh.select_all(action="SELECT")
        #球形に変形
        if self.my_useToSphere > 0:
            bpy.ops.transform.tosphere(value=self.my_useToSphere, mirror=False, proportional='DISABLED',
            proportional_edit_falloff='SMOOTH', proportional_size=1)
        #スムーズをかける
        if self.my_useSmooth > 0:
            bpy.ops.mesh.vertices_smooth(factor=self.my_useSmooth, repeat=3)

        for i in range(self.my_step):
            bpy.ops.mesh.select_random(percent=self.my_stepSelectPercent,
             seed=self.my_stepSelectSeed, action='DESELECT')
            random.seed()
            rand = 1+random.uniform(-self.my_step_hight_rand,self.my_step_hight_rand)
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False},
             TRANSFORM_OT_translate={"value":(0.0, 0.0, self.my_step_hight*rand),
             "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL',
             "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH',
             "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0),
             "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False,
             "remove_on_cancel":False, "release_confirm":False})
        
        #一番下の面を削除
        if self.my_delUnder:
            bpy.ops.mesh.select_all(action='DESELECT')
            bm = bmesh.from_edit_mesh(bpy.context.object.data)
            for f in bm.faces:
                if  0.95 < f.normal.z and f.normal.z < 1.05:
                    if f.calc_center_median().z <= 0.01:
                        f.select = True
            bpy.ops.mesh.delete(type='FACE')
        #マテリアルを設定
        if self.my_setRoofTopMate:
            bpy.ops.object.material_slot_add()
            bpy.ops.object.material_slot_add()
            bpy.ops.mesh.select_all(action='DESELECT')
            bm = bmesh.from_edit_mesh(bpy.context.object.data)
            for f in bm.faces:
                if  0.95 < f.normal.z and f.normal.z < 1.05:
                    f.select = True
            bpy.ops.object.material_slot_assign()
        #屋上を作る
        if self.my_setRoofTopSize > 0:
            bpy.ops.mesh.select_all(action='DESELECT')
            bm = bmesh.from_edit_mesh(bpy.context.object.data)
            for f in bm.faces:
                if  0.95 < f.normal.z and f.normal.z < 1.05:
                    f.select = True
            bpy.ops.mesh.select_axis(mode='POSITIVE', axis='Z_AXIS', threshold=0.0001)
            bpy.ops.mesh.inset(thickness=self.my_setRoofTopSize)
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False},
                TRANSFORM_OT_translate={"value":(0, -0, -0.0115835),
                "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL',
                "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH',
                "proportional_size":1, "snap":False, "snap_target":'CLOSEST',
                "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False,
                "release_confirm":False})

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        
        #ポリゴン数削減して平面を一つに
        if self.my_polysaku :
            bpy.ops.object.modifier_add(type='DECIMATE')
            act_obj.modifiers[-1].decimate_type = 'DISSOLVE'
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=act_obj.modifiers[-1].name)
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#三面図用のカーブを作る
class MakeMakeThreeViews(bpy.types.Operator):
    bl_idname = "object.makethreeviews"
    bl_label = "Make Three Views"
    bl_description = "三面図用のカーブを作る"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    
    def execute(self, context):
        curlot = context.scene.cursor_location
        bpy.ops.curve.primitive_bezier_circle_add(radius=1, view_align=False,
         enter_editmode=False, location=(0, 0, 0), layers=bpy.context.scene.layers)
        active = bpy.context.active_object
        active.location = curlot
        active.location.z += 2.0
        active.data.dimensions = '2D'
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        active.modifiers[-1].thickness = 4
        
        bpy.ops.curve.primitive_bezier_circle_add(radius=1, view_align=False,
         enter_editmode=False, location=(0, 0, 0), layers=bpy.context.scene.layers)
        active = bpy.context.active_object
        active.location = curlot
        active.location.x += 2.0
        active.rotation_euler.y = 1.570796
        active.data.dimensions = '2D'
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        active.modifiers[-1].thickness = 4
        
        bpy.ops.curve.primitive_bezier_circle_add(radius=1, view_align=False,
         enter_editmode=False, location=(0, 0, 0), layers=bpy.context.scene.layers)
        active = bpy.context.active_object
        active.location = curlot
        active.location.y += -2.0
        active.rotation_euler.x = 1.570796
        active.data.dimensions = '2D'
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        active.modifiers[-1].thickness = 4      

        return {'FINISHED'}
    
#カーブをツイストさせる
class CurveTwist(bpy.types.Operator):
    bl_idname = "object.curvetwist"
    bl_label = "CurveTwist"
    bl_description = "カーブをツイストさせる"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_easeNo = bpy.props.IntProperty(name="Ease No",default=1,max=22,min=1)
    my_wave = bpy.props.FloatProperty(name="wave",default=2,max=10,min=-10)
    my_curveValue = bpy.props.FloatProperty(name="curveValue",default=2,max=4,min=-4)
    
    def execute(self, context):
        #カーブ一本一本ごとに処理を行う
        splines = bpy.context.scene.objects.active.data.splines
        for s in splines:
            #どの頂点が選択されているかを確かめる
            select_p = []
            if s.type == "BEZIER":
                for p in s.bezier_points:
                    if p.select_control_point == True:
                        select_p.append(p)
            else:
                for p in s.points:
                    if p.select == True:
                        select_p.append(p)
            for i,sp in enumerate(select_p):
                #数値に合わせて頂点に回転を設定
                #kaiten = (((1/(i+1))**self.my_curveValue))*self.my_multiply
                ease_no = self.my_easeNo
                if ease_no== 20 or ease_no== 22:
                    ease_no = 1
                kaiten = getEasing(i,0,self.my_curveValue,self.my_wave,ease_no=ease_no)
                sp.tilt = kaiten
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#イージング処理
#t:時間 b:開始の値 c:開始と終了の値の差分 d:合計時間
def getEasing(t,b,c,d,ease_type="",ease_no=0):
    if ease_type == "Linear" or ease_no==1:
        return c*t/d + b
    elif ease_type == "Quadratic_in" or ease_no==2:
        t /= d
        return c*t*t + b
    elif ease_type == "Quadratic_out" or ease_no==3:
        t /= d
        return -c*t*(t-2.0) + b
    elif ease_type == "Quadratic_in_out" or ease_no==4:
        t /= d/2.0
        if t < 1:
            return c/2.0*t*t + b
        t = t - 1
        return -c/2.0 * (t*(t-2) - 1) + b
    
    elif ease_type == "Cubic_in" or ease_no==5:
        t /= d
        return c*t*t*t + b
    elif ease_type == "Cubic_out" or ease_no==6:
        t /= d
        t = t - 1
        return c*(t*t*t + 1) + b
    elif ease_type == "Cubic_in_out" or ease_no==7:
        t /= d/2.0
        if t < 1:
            return c/2.0*t*t*t + b
        t = t - 2
        return c/2.0 * (t*t*t + 2) + b
    
    elif ease_type == "Quartic_in" or ease_no==8:
        t /= d
        return c*t*t*t*t + b
    elif ease_type == "Quartic_out" or ease_no==9:
        t /= d
        t = t - 1
        return -c*(t*t*t*t - 1) + b
    elif ease_type == "Quartic_in_out" or ease_no==10:
        t /= d/2.0
        if t < 1:
            return c/2.0*t*t*t*t + b
        t = t - 2
        return -c/2.0 * (t*t*t*t - 2) + b
    
    elif ease_type == "Quintic_in" or ease_no==11:
        t /= d
        return c*t*t*t*t*t + b
    elif ease_type == "Quintic_out" or ease_no==12:
        t /= d
        t = t - 1
        return c*(t*t*t*t*t + 1) + b
    elif ease_type == "Quintic_in_out" or ease_no==13:
        t /= d/2.0
        if t < 1:
            return c/2.0*t*t*t*t*t + b
        t = t - 2
        return c/2.0 * (t*t*t*t*t + 2) + b
    
    elif ease_type == "Sinusoidal_in" or ease_no==14:
        return -c * math.cos(t/d * (math.pi/2.0)) + c + b
    elif ease_type == "Sinusoidal_out" or ease_no==15:
        return c * math.sin(t/d * (math.pi/2.0)) + b
    elif ease_type == "Sinusoidal_in_out" or ease_no==16:
        return -c/2.0 * (math.cos(math.pi*t/d) - 1) + b
    
    elif ease_type == "Exponential_in" or ease_no==17:
        return c * 2**(10*(t/d - 1)) + b
    elif ease_type == "Exponential_out" or ease_no==18:
        return c * (-(2.0**(-10.0 * t/d)) + 1) + b
    elif ease_type == "Exponential_in_out" or ease_no==19:
        t /= d/2.0
        if t < 1:
            return c/2.0 * 2.0**(10.0 * (t-1)) + b
        t = t - 1
        return c/2.0 * (-(2**(-10*t)) + 2 ) + b
    
    elif ease_type == "Circular_in" or ease_no==20:
        t /= d
        return -c * (math.sqrt(1 - t*t) - 1) + b
    elif ease_type == "Circular_out" or ease_no==21:
        t /= d
        t = t - 1
        return c * math.sqrt(1 - t*t) + b
    elif ease_type == "Circular_in_out" or ease_no==22:
        t /= d/2.0
        if t < 1:
            return -c/2.0 * (math.sqrt(1 - t*t) - 1)
        t = t - 2	
        return c/2.0 * (math.sqrt(1 - t*t) + 1) + b
    
    else:
        return c*t/d + b
    
    #該当なしの時はリニア
    return c*t/d + b
#選択中のカーブの傾きをリセット
class CurveTwistReset(bpy.types.Operator):
    bl_idname = "object.curvetwistreset"
    bl_label = "CurveTwistReset"
    bl_description = "カーブの傾きをリセットする"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def execute(self, context):
        #カーブ一本一本ごとに処理を行う
        splines = bpy.context.scene.objects.active.data.splines
        for s in splines:
            #どの頂点が選択されているかを確かめる
            select_p = []
            if s.type == "BEZIER":
                for p in s.bezier_points:
                    if p.select_control_point == True:
                        select_p.append(p)
            else:
                for p in s.points:
                    if p.select == True:
                        select_p.append(p)
            for i,sp in enumerate(select_p):
                #回転をリセット
                sp.tilt = 0
        return {'FINISHED'}

#選択中のカーブの半径を設定
class SetCurveRadius(bpy.types.Operator):
    bl_idname = "object.setcurveradius"
    bl_label = "SetCurveRadius"
    bl_description = "選択中のカーブの半径を設定"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_wave = bpy.props.FloatProperty(name="wave",default=2,max=10,min=-10)
    my_curveValue = bpy.props.FloatProperty(name="curveValue",default=2,max=4,min=-4)
    
    def execute(self, context):
        #カーブ一本一本ごとに処理を行う
        splines = bpy.context.scene.objects.active.data.splines
        for s in splines:
            #どの頂点が選択されているかを確かめる
            select_p = []
            if s.type == "BEZIER":
                for p in s.bezier_points:
                    if p.select_control_point == True:
                        select_p.append(p)
            else:
                for p in s.points:
                    if p.select == True:
                        select_p.append(p)
            for i,sp in enumerate(select_p):
                #数値に合わせて頂点に半径を設定
                hankei = (((1/(i+1))**self.my_curveValue))*self.my_wave
                sp.radius = hankei
            if len(select_p) > 0:
                select_p[-1].radius = 0
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
#選択中のカーブの次数を設定
class SetCurveOrderU(bpy.types.Operator):
    bl_idname = "object.setcurveorderu"
    bl_label = "SetCurveOrderU"
    bl_description = "選択中のカーブの次数を設定"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_orderu = bpy.props.IntProperty(name="multiply",default=3,max=64,min=-0)
    
    def execute(self, context):
        #カーブ一本一本ごとに処理を行う
        splines = bpy.context.scene.objects.active.data.splines
        for s in splines:
            #どの頂点が選択されているかを確かめる
            if s.type == "BEZIER":
                for p in s.bezier_points:
                    if p.select_control_point == True:
                        s.order_u = self.my_orderu
            else:
                for p in s.points:
                    if p.select == True:
                        s.order_u = self.my_orderu
                
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#選択中のカーブの解像度を設定
class SetCurveResolutionU(bpy.types.Operator):
    bl_idname = "object.setcurveresolutionu"
    bl_label = "SetCurveResolutionU"
    bl_description = "選択中のカーブの解像度を設定"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_resolution_u = bpy.props.IntProperty(name="multiply",default=3,max=64,min=-0)
    
    def execute(self, context):
        #カーブ一本一本ごとに処理を行う
        splines = bpy.context.scene.objects.active.data.splines
        for s in splines:
            #どの頂点が選択されているかを確かめる
            if s.type == "BEZIER":
                for p in s.bezier_points:
                    if p.select_control_point == True:
                        s.resolution_u = self.my_resolution_u
            else:
                for p in s.points:
                    if p.select == True:
                        s.resolution_u = self.my_resolution_u
                
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

#FreeStyleだけを描画する処理
class OnlyFreeStylePhoto(bpy.types.Operator):
    bl_idname = "object.onlyfreestylephoto"
    bl_label = "OnlyFreestyle Photo"
    bl_description = "Freestyleだけをレンダリング"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_onlySelect = bpy.props.BoolProperty(default=False,name="Only Select")
    my_makeGP = bpy.props.BoolProperty(default=False,name="Make GreasePencil")
    my_line_width = bpy.props.FloatProperty(default=3.0,name="Line Width")
    
    def execute(self, context):
        
        #FreestyleをONにする
        pre_use_freestyle = bpy.context.scene.render.use_freestyle
        bpy.context.scene.render.use_freestyle = True
        pre_layer_use_freestyle = bpy.context.scene.render.layers.active.use_freestyle
        bpy.context.scene.render.layers.active.use_freestyle = True
        #レンダリング設定を保存して外す
        pre_use_zmask = bpy.context.scene.render.layers.active.use_zmask
        bpy.context.scene.render.layers.active.use_zmask =False
        pre_invert_zmask = bpy.context.scene.render.layers.active.invert_zmask
        bpy.context.scene.render.layers.active.invert_zmask = False
        pre_use_all_z = bpy.context.scene.render.layers.active.use_all_z
        bpy.context.scene.render.layers.active.use_all_z = False
        pre_use_solid = bpy.context.scene.render.layers.active.use_solid
        bpy.context.scene.render.layers.active.use_solid = False
        pre_use_halo = bpy.context.scene.render.layers.active.use_halo
        bpy.context.scene.render.layers.active.use_halo = False
        pre_use_ztransp = bpy.context.scene.render.layers.active.use_ztransp
        bpy.context.scene.render.layers.active.use_ztransp = False
        pre_use_sky = bpy.context.scene.render.layers.active.use_sky
        bpy.context.scene.render.layers.active.use_sky = False
        pre_use_edge_enhance = bpy.context.scene.render.layers.active.use_edge_enhance
        bpy.context.scene.render.layers.active.use_edge_enhance = False
        pre_use_strand = bpy.context.scene.render.layers.active.use_strand
        bpy.context.scene.render.layers.active.use_strand = False
        pre_use_ao = bpy.context.scene.render.layers.active.use_ao
        bpy.context.scene.render.layers.active.use_ao = False
        
        #選択中のオブジェクトだけをレンダリングするようにgroupを設定＆変更
        if self.my_onlySelect:
            selobjs = bpy.context.selected_objects
            linegroup = bpy.data.groups.new("OnlyFreeStyleGroup")
            for o in selobjs:
                linegroup.objects.link(o)
            linesets = bpy.context.scene.render.layers.active.freestyle_settings.linesets
            pre_groupList =[]
            if len(linesets) <= 0:
                bpy.ops.scene.freestyle_lineset_add()
            for l in linesets:
                if l.show_render == True:
                    pre_groupList.append([l.select_by_group, l.group, l.group_negation])
                    l.select_by_group = True
                    l.group = linegroup
                    l.group_negation = 'INCLUSIVE'
        
        #Freestyleをグリースペンシルに変換する
        def post_lineset_makegp(scene, layer, lineset):
            #freeStyleの3D上での位置はこうして見つける
#            for i in range(Operators().get_strokes_size()):
#                for j in Operators().get_stroke_from_index(i):
#                    print(j.point_3d.x)
            scene = bpy.context.scene
            gp = None
            if scene.tool_settings.grease_pencil_source == "SCENE":
                if scene.grease_pencil == None:
                    bpy.ops.gpencil.data_add()
                gp = scene.grease_pencil
            else:
                if scene.objects.active.grease_pencil == None:
                    bpy.ops.gpencil.data_add()
                gp = scene.objects.active.grease_pencil
            layer = None
            if gp.layers.active != None:
                layer = gp.layers.active
            else:
                layer = gp.layers.new("FreeStyle", set_active=True)
            frame = None
            for f in layer.frames:
                if f.frame_number == scene.frame_current:
                    frame = f
                    frame.clear()
                    break
            else:
                frame = layer.frames.new(scene.frame_current)
            if len(gp.palettes) <= 0:
                bpy.ops.gpencil.palette_add()
            if len(gp.palettes.active.colors) <= 0:
                bpy.ops.gpencil.palettecolor_add()
            gpColor = gp.palettes.active.colors.active
            mat = bpy.context.scene.camera.matrix_local.copy()
            for i in range(Operators().get_strokes_size()):
                try:
                    stroke = frame.strokes.new()
                    stroke.draw_mode = '3DSPACE'
                    stroke.line_width = self.my_line_width
                    stroke.colorname = gpColor.name
                    stroke.points.add(len(Operators().get_stroke_from_index(i)))
                except:
                    print("makeGP stroke ERROR")
                finally:
                    for i,v in enumerate(Operators().get_stroke_from_index(i)):
                        try:
                            stroke.points[i].co = mat * v.point_3d
                            stroke.points[i].strength = 1
                            stroke.points[i].pressure = 1
                        except:
                            print("makeGP points ERROR")
        if self.my_makeGP:
            #グリースペンシルを設定する
            if bpy.context.scene.tool_settings.grease_pencil_source == 'SCENE':
                if bpy.context.scene.grease_pencil == None:
                    bpy.ops.gpencil.data_add()
                if len(bpy.context.scene.grease_pencil.palettes) <= 0:
                    bpy.ops.gpencil.palette_add()
                if len(bpy.context.scene.grease_pencil.palettes.active.colors) <= 0:
                    bpy.ops.gpencil.palettecolor_add()
            else:
                if bpy.context.scene.objects.active.grease_pencil == None:
                    bpy.ops.gpencil.data_add()
                if len(bpy.context.scene.objects.active.grease_pencil.palettes) <= 0:
                    bpy.ops.gpencil.palette_add()
                if len(bpy.context.scene.objects.active.grease_pencil.palettes.active.colors) <= 0:
                    bpy.ops.gpencil.palettecolor_add()
            #FreeStyle描画後の処理を設定
            parameter_editor.callbacks_lineset_post.append(post_lineset_makegp)
        
        #レンダリング後の処理をセット
        def post_render(scene):
            #FreeStyleの設定を元に戻す(後でfreeStyleのPostに移す)
            bpy.context.scene.render.use_freestyle = pre_use_freestyle
            bpy.context.scene.render.layers.active.use_freestyle = pre_layer_use_freestyle
            bpy.context.scene.render.layers.active.use_zmask = pre_use_zmask
            bpy.context.scene.render.layers.active.invert_zmask = pre_invert_zmask
            bpy.context.scene.render.layers.active.use_all_z = pre_use_all_z
            bpy.context.scene.render.layers.active.use_solid = pre_use_solid
            bpy.context.scene.render.layers.active.use_halo = pre_use_halo
            bpy.context.scene.render.layers.active.use_ztransp = pre_use_ztransp
            bpy.context.scene.render.layers.active.use_sky = pre_use_sky
            bpy.context.scene.render.layers.active.use_edge_enhance = pre_use_edge_enhance
            bpy.context.scene.render.layers.active.use_strand = pre_use_strand
            bpy.context.scene.render.layers.active.use_ao = pre_use_ao
            #選択中のオブジェクトだけをレンダリングするようにgroupを元に戻す
            if self.my_onlySelect:
                for l in linesets:
                    for g in pre_groupList:
                        l.group = g[1]
                        l.select_by_group = g[0]
                        l.group_negation = g[2]
                for o in selobjs:
                    bpy.data.groups[linegroup.name].objects.unlink(o)
                    
            #Freestyleをグリースペンシルに変換するための設定を外す
            if self.my_makeGP:
                parameter_editor.callbacks_lineset_post.remove(post_lineset_makegp)
                
            #処理自体を消去
            bpy.app.handlers.render_post.remove(post_render)
            
        #レンダー後の処理を設定
        bpy.app.handlers.render_post.append(post_render)
        
        #レンダリング
        if self.my_makeGP:
            bpy.ops.render.render()
        else:
            bpy.ops.render.render("INVOKE_DEFAULT")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self) 
    
#選択中のグリースペンシルの密度が高い場所の線の太さを変える
class GpReduceHighDensityParts(bpy.types.Operator):
    bl_idname = "object.gpreducehighdensityparts"
    bl_label = "Reduce high density parts"
    bl_description = "!!!実験中選択中のグリースペンシルの密度が高い場所の線の太さを変える"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_range = bpy.props.FloatProperty(default=0.1,name="Line Width")
    my_lenpoint = bpy.props.IntProperty(default=5,name="Len Point",min=0)
    my_pressure = bpy.props.FloatProperty(default=0.5,name="pressure")
    my_strength = bpy.props.FloatProperty(default=0.5,name="strength")
    
    
    def execute(self, context):
        #グリースペンシルを取得
        gp = None
        if bpy.context.scene.tool_settings.grease_pencil_source == 'SCENE':
            gp = bpy.context.scene.grease_pencil
        else:
            gp = bpy.context.scene.objects.active.grease_pencil
        #グリースペンシルの位置を取得
        gplayer = gp.layers.active
        scene = bpy.context.scene
        if gplayer.active_frame != None:
            #ポイントとカメラとの相対角度のリスト[ポイント,相対角度]
            pointList = []
            cam = bpy.context.scene.camera
            frame = gplayer.active_frame
            for s in frame.strokes:
                for p in s.points:
                    #相対角度を割り出す
                    #ワールド空間からローカル空間に位置を変換
                    local_co = cam.matrix_local * p.co
                    angle = math.degrees(math.atan2(local_co.z,-local_co.y))
                    print(p.co,local_co,angle)
                    pass
                
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#グリースペンシルに入りと抜きを入れる
class GpIritonuki(bpy.types.Operator):
    bl_idname = "object.gpiritonuki"
    bl_label = "GP Iritonuki"
    bl_description = "グリースペンシルに入りと抜きを入れる"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_isselect = bpy.props.BoolProperty(default=False,name="Is Select")
    my_pressure = bpy.props.BoolProperty(default=True,name="Pressure")
    my_strength = bpy.props.BoolProperty(default=True,name="Strength")
    
    my_value1 = bpy.props.FloatProperty(default=0.5,name="value1",min=0.0,max=1.0)
    my_value2 = bpy.props.FloatProperty(default=0.0,name="value2",min=-1.0,max=1.0)
    
    def execute(self, context):
        #グリースペンシルを取得
        gp = None
        if bpy.context.scene.tool_settings.grease_pencil_source == 'SCENE':
            gp = bpy.context.scene.grease_pencil
        else:
            gp = bpy.context.scene.objects.active.grease_pencil
        #グリースペンシルの位置を取得
        gplayer = gp.layers.active
        scene = bpy.context.scene
        if gplayer.active_frame != None:
            #平面化した頂点のリスト(平面前のポイント, 平面化済みの座標)
            point2dList = []
            frame = gplayer.active_frame
            for s in frame.strokes:
                pointlen = len(s.points)
                if pointlen <= 1:
                    continue
                harf = (pointlen-1)/2
                one = 1/(pointlen-1)
                #入りと抜きの度合いを決定する
                for i,p in enumerate(s.points):
                    #数値に合わせて頂点に半径を設定
                    x = one * i
                    if x <= self.my_value1:
                        hankei = x + self.my_value2
                    else:
                        hankei = 1-x + self.my_value2
                    def strAndPre(hankei_):return hankei_*2
                    if self.my_isselect:
                        if self.my_strength and p.select: p.strength = strAndPre(hankei)
                        if self.my_pressure and p.select: p.pressure = strAndPre(hankei)
                    else:
                        if self.my_strength: p.strength = strAndPre(hankei)
                        if self.my_pressure: p.pressure = strAndPre(hankei)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#グリースペンシルを細分化
class GpSubdivide(bpy.types.Operator):
    bl_idname = "object.gpsubdivide"
    bl_label = "GP Subdivide"
    bl_description = "グリースペンシルを細分化"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_subdivide = bpy.props.IntProperty(default=2,min=1,max=10,name="subdivide")
    
    def execute(self, context):
        #グリースペンシルを取得
        gp = None
        if bpy.context.scene.tool_settings.grease_pencil_source == 'SCENE':
            gp = bpy.context.scene.grease_pencil
        else:
            gp = bpy.context.scene.objects.active.grease_pencil
        #グリースペンシルの位置を取得
        gplayer = gp.layers.active
        scene = bpy.context.scene
        gpColor = gp.palettes.active.colors.active
        if gplayer.active_frame != None:
            for j in range(self.my_subdivide):
                #変換後のストロークを保存するリスト
                post_sList = []
                frame = gplayer.active_frame
                post_width = 1
                for s in frame.strokes:
                    post_s = []
                    post_width = s.line_width
                    for i,p in enumerate(s.points):
                        #最初と最後だった場合は処理しないでそのまま入れる
                        if p == s.points[0]:
                            post_s.append([p.co,p.strength,p.pressure])
                            continue
                        #1個前のポイントとこのポイントとの間のポイントを追加していく
                        post_co = ((p.co - s.points[i-1].co)/2)+s.points[i-1].co
                        post_str = (p.strength+s.points[i-1].strength)/2
                        post_press = (p.pressure+s.points[i-1].pressure)/2
                        post_s.append([post_co,post_str,post_press])
                        #このポイントを追加する
                        post_s.append([p.co,p.strength,p.pressure])
                    #ポイントが最初と最後の2つだけだった時はそれを割った値を出す
                    if len(post_s) == 2:
                        ins_co = ((post_s[1][0] - post_s[0][0])/2)+post_s[0][0]
                        ins_str = (post_s[1][1]+post_s[0][1])/2
                        ins_press = (post_s[1][2]+post_s[0][2])/2
                        post_s.insert(1,[ins_co,ins_str,ins_press])
                    #新しいストロークをリストに入れる
                    post_sList.append(post_s)
                #全てのストロークを消し
                #post_sListを元に新しいストロークを作る
                for i in range(len(frame.strokes)):
                    frame.strokes.remove(frame.strokes[0])
                for pos in post_sList:
                    st = frame.strokes.new(gpColor.name)
                    st.draw_mode = '3DSPACE'
                    st.line_width = post_width
                    st.points.add(count=len(pos))
                    for i,po in enumerate(pos):
                        st.points[i].co = po[0]
                        st.points[i].strength = po[1]
                        st.points[i].pressure = po[2]
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#グリースペンシルポイントの色の濃さを設定
class GpStrength(bpy.types.Operator):
    bl_idname = "object.gpstrength"
    bl_label = "GP Strength"
    bl_description = "グリースペンシルポイントの色の濃さを設定"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_isSelect = bpy.props.BoolProperty(default=False,name="Is Select")
    my_strength = bpy.props.FloatProperty(default=0.5,min=0.0,max=1.0,name="Strength")
    
    def execute(self, context):
        
        #グリースペンシルを取得
        gp = None
        if bpy.context.scene.tool_settings.grease_pencil_source == 'SCENE':
            gp = bpy.context.scene.grease_pencil
        else:
            gp = bpy.context.scene.objects.active.grease_pencil
        gplayer = gp.layers.active
        scene = bpy.context.scene
        gpColor = gp.palettes.active.colors.active
        if gplayer.active_frame != None:
            frame = gplayer.active_frame
            for s in frame.strokes:
                for p in s.points:
                    if self.my_isSelect:
                        if p.select:
                            p.strength = self.my_strength
                    else:
                        p.strength = self.my_strength
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#グリースペンシルをクリーンアップ
class GPCleanUp(bpy.types.Operator):
    bl_idname = "object.gpcleanup"
    bl_label = "GP Clean Up"
    bl_description = "指定の頂点数か長さ以下のストロークを削除"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_isSelect = bpy.props.BoolProperty(default=False,name="Is Select")
    my_strnum = bpy.props.IntProperty(default=5,min=0,name="Stroke Number")
    my_strlength = bpy.props.FloatProperty(default=0.01,min=0.0,name="Stroke length",unit="LENGTH")
    
    def execute(self, context):
        #グリースペンシルを取得
        gp = None
        if bpy.context.scene.tool_settings.grease_pencil_source == 'SCENE':
            gp = bpy.context.scene.grease_pencil
        else:
            gp = bpy.context.scene.objects.active.grease_pencil
        gplayer = gp.layers.active
        if gplayer.active_frame != None:
            frame = gplayer.active_frame
            removeList = []
            for s in frame.strokes:
                if self.my_isSelect:
                    if s.select:
                        #指定の個数以下なら削除
                        if len(s.points) <= self.my_strnum:
                            removeList.append(s)
                        #指定の長さ以下なら削除
                        length = 0
                        for i,p in enumerate(s.points):
                            if p == s.points[0]:
                                continue
                            length += abs((p.co - s.points[i-1].co).length)
                        if self.my_strlength >= length:
                            if s not in removeList:
                                removeList.append(s)
                else:
                    #指定の個数以下なら削除
                    if len(s.points) <= self.my_strnum:
                        removeList.append(s)
                    #指定の長さ以下なら削除
                    length = 0
                    for i,p in enumerate(s.points):
                        if p == s.points[0]:
                            continue
                        length += abs((p.co - s.points[i-1].co).length)
                    if self.my_strlength >= length:
                        if s not in removeList:
                            removeList.append(s)
            print(removeList)
            #削除リストのストロークを削除
            for i in range(len(removeList)):
                frame.strokes.remove(removeList[i])
                        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self) 
    
#グリースペンシルポイントに同じストロークで同じ位置の頂点があった場合融解する
class GpSamePointDissolve(bpy.types.Operator):
    bl_idname = "object.gpsamepointdissolve"
    bl_label = "GP Disolve+[実験中]"
    bl_description = "グリースペンシルポイントに同じストロークで同じ位置の頂点があった場合融解"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_isSelect = bpy.props.BoolProperty(default=False,name="Is Select")
    my_range = bpy.props.FloatProperty(default=0.0001,min=0.0,name="renge",unit="LENGTH")
    
    def execute(self, context):
        
        #グリースペンシルを取得
        gp = None
        if bpy.context.scene.tool_settings.grease_pencil_source == 'SCENE':
            gp = bpy.context.scene.grease_pencil
        else:
            gp = bpy.context.scene.objects.active.grease_pencil
        gplayer = gp.layers.active
        scene = bpy.context.scene
        gpColor = gp.palettes.active.colors.active
        if gplayer.active_frame != None:
            frame = gplayer.active_frame
            pdisList = []
            for s in frame.strokes:
                plen = len(s.points)
                for i,p in enumerate(s.points):
                    if self.my_isSelect:
                        if p.select:
                            #最初と最後のポイントだったら終了
                            if i >= (plen - 2) or i <= 0:
                                continue
                            #次のポイントが選択されていなかったら終了
                            if s.points[i+1].select == False:
                                continue
                            #一つ後のポイントと位置が同じだったら融合リストに入れる
                            if (abs((p.co - s.points[i+1].co).length) <= self.my_range):
                                pdisList.append(p)
                    else:
                        #最初と最後のポイントだったら終了
#                        if i >= (plen - 1) or i <= 0:
                        if p == s.points[0] or p == s.points[-1]:
                            continue
                        #一つ後のポイントと位置が同じだったら融合リストに入れる
                        length = (p.co - s.points[i+1].co).length
                        print(length)
                        if (length <= self.my_range):
                            pdisList.append(p)
            #融合リストのものを融合していく
            bpy.ops.object.mode_set(mode='GPENCIL_EDIT', toggle=False)
            bpy.ops.gpencil.select_all(action='DESELECT')
            for p in pdisList:
                p.select = True
            bpy.ops.gpencil.delete(type='POINTS')
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#別のストロークに同じ位置の頂点があったらストロークを繋げる
class GpConnect(bpy.types.Operator):
    bl_idname = "object.gpconnect"
    bl_label = "GP Connect[実験中]"
    bl_description = "別のストロークに同じ位置の頂点があったらストロークを繋げる"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_isSelect = bpy.props.BoolProperty(default=False,name="Is Select")
    my_range = bpy.props.FloatProperty(default=0.001,min=0.0,name="renge",unit="LENGTH")
    
    def execute(self, context):
        
        #グリースペンシルを取得
        gp = None
        if bpy.context.scene.tool_settings.grease_pencil_source == 'SCENE':
            gp = bpy.context.scene.grease_pencil
        else:
            gp = bpy.context.scene.objects.active.grease_pencil
        gplayer = gp.layers.active
        scene = bpy.context.scene
        gpColor = gp.palettes.active.colors.active
        if gplayer.active_frame != None:
            frame = gplayer.active_frame
            conneList = []
            for s1 in frame.strokes:
                plen = len(s1.points)
                for i,p1 in enumerate(s1.points):
                    #最初と最後のポイントだったら終了
                    if i >= (plen - 1) or i <= 0:
                        continue
                    for s2 in frame.strokes:
                        #同一ストロークだったら次へ
                        if s1 == s2 : continue
                        plen2 = len(s2.points)
                        for j,p2 in enumerate(s2.points):
                            if j >= (plen - 1) or j <= 0:
                                continue
                            if self.my_isSelect:
                                if p1.select and p2.select:
                                    #2つのポイントの距離がしきい値以下だったら2つとも記録
                                    if (abs((p1.co - p2.co).length) <= self.my_range):
                                        conneList.append([p1,p2])
                            else:
                                #2つのポイントの距離がしきい値以下だったら2つとも記録
                                if (abs((p1.co - p2.co).length) <= self.my_range):
                                    conneList.append([p1,p2])
            #リストのものを統合していく
            bpy.ops.object.mode_set(mode='GPENCIL_EDIT', toggle=False)
            bpy.ops.gpencil.select_all(action='DESELECT')
            for c in conneList:
                bpy.ops.gpencil.select_all(action='DESELECT')
                c[0].select = True
                c[1].select = True
                bpy.ops.gpencil.stroke_join(type='JOIN', leave_gaps=True)
                
                
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#グリースペンシルが設定してあるフレームのみレンダリング
class GpFrameRender(bpy.types.Operator):
    bl_idname = "object.gpframerender"
    bl_label = "GP Frame Render"
    bl_description = "グリースペンシルが設定してあるフレームのみレンダリング"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_opengl = bpy.props.BoolProperty(default=True,name="Open GL")
    
    def execute(self, context):
        scene = bpy.context.scene
        gp = None
        if scene.tool_settings.grease_pencil_source == "SCENE":
            gp = scene.grease_pencil
        else:
            gp = scene.objects.active.grease_pencil
        gp_frame = []
        for f in gp.layers.active.frames:
            gp_frame.append(f.frame_number)
        
        scn = bpy.context.scene

        old_output_path = scn.render.filepath
        import os
        output_path = os.path.abspath(old_output_path)
        
        # 4桁のフレーム数を返す
        def formatNumbers(number, length):
            return '%0*d' % (length, number)
        
        # レンダリングするフレームを決める
        oldrendflame = 0
        try:
            for f in range(scn.frame_start,scn.frame_end):
                #最初とフレームとグリースペンシルがあるフレームだけレンダリング
                rendflame = False
                for gpf in gp_frame:
                    if f == gpf:
                        rendflame = True
                if f == scn.frame_start:
                    rendflame = True
                if rendflame == False:
                    oldfilepath = os.path.join(output_path,
                        formatNumbers(oldrendflame, 4) + ".png",)
                    newfilepath = os.path.join(output_path,
                        formatNumbers(f, 4) + ".png",)
                    import shutil
                    shutil.copyfile(oldfilepath, newfilepath)
                    continue
                # フレームをセット
                scn.frame_set(f)
                # ファイルパスをセット
                scn.render.filepath = os.path.join(
                        output_path,
                        formatNumbers(f, 4) + ".png",)
                if self.my_opengl:
                    # OpenGLをレンダ
                    bpy.ops.render.opengl(write_still=True)
                else:
                    bpy.ops.render.render(write_still = True)
                oldrendflame = f
        except:
            # reset internal filepath
            bpy.context.scene.render.filepath = old_output_path
            print("ERROR")
            
        # reset internal filepath
        bpy.context.scene.render.filepath = old_output_path
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self) 
    
#全てのフレームのグリースペンシルを編集
class GPAllFrameEdit(bpy.types.Operator):
    bl_idname = "object.gpallframeedit"
    bl_label = "GP All Frame Edit"
    bl_description = "全てのフレームのグリースペンシルを編集"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_iritonuki = bpy.props.BoolProperty(default=False,name="Iritonuki")
    my_pressure = bpy.props.BoolProperty(default=True,name="Pressure")
    my_strngth = bpy.props.BoolProperty(default=True,name="Strength")
    my_value1 = bpy.props.FloatProperty(default=0.5,min=0.0,max=1.0,name="Value1")
    my_value2 = bpy.props.FloatProperty(default=0.0,min=-1.0,max=1.0,name="Value2")
    
    my_iritonuki = bpy.props.BoolProperty(default=False,name="Iritonuki")
    
    my_issubdivide = bpy.props.BoolProperty(default=False,name="Subdivide")
    my_subdiv = bpy.props.IntProperty(name="subdivide",default=2,min=1)
    
    my_cleanUp = bpy.props.BoolProperty(default=False,name="CleanUp")
    my_strNo = bpy.props.IntProperty(default=5,min=0,name="Stroke Number")
    my_strlength = bpy.props.FloatProperty(default=0.01,min=0.0,name="Stroke length",unit="LENGTH")
    
    my_isstrength = bpy.props.BoolProperty(default=False,name="Strength")
    my_strength = bpy.props.FloatProperty(default=1.0,min=0.0,max=1.0,name="Strength")
    
    def execute(self, context):
        scene = bpy.context.scene
        gp = None
        if scene.tool_settings.grease_pencil_source == "SCENE":
            gp = scene.grease_pencil
        else:
            gp = scene.objects.active.grease_pencil
        gp_frame = []
        for f in gp.layers.active.frames:
            gp_frame.append(f.frame_number)
            
        scn = bpy.context.scene
        oldFrame = scn.frame_current
        scn.frame_set(scn.frame_start)
        for f in gp_frame:
            #フレーム更新
            scn.frame_set(f)
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            
            if self.my_cleanUp:
                bpy.ops.object.gpcleanup(my_strnum = self.my_strNo,
                 my_strlength = self.my_strlength)
                
            if self.my_iritonuki:
                bpy.ops.object.gpiritonuki(my_value1=self.my_value1,my_value2=self.my_value2,
                    my_strength=self.my_strngth,my_pressure=self.my_pressure)
                
            if self.my_issubdivide:
                bpy.ops.object.gpsubdivide(my_subdivide = self.my_subdiv)
            
        scn.frame_set(oldFrame)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
#FreeStyleをグリースペンシルに変換する処理のアニメ版
class OnlyFreeStyleAnime(bpy.types.Operator):
    bl_idname = "object.onlyfreestyleanime"
    bl_label = "FreeStyle2GP Anime"
    bl_description = "FreeStyleを使用してグリースペンシルアニメを作る"
    bl_options = {'REGISTER','UNDO'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    my_frameStep = bpy.props.IntProperty(default=3,min=1,name="Frame Step")
    my_isSelect = bpy.props.BoolProperty(default=False,name="Is select")
    my_lineWidth = bpy.props.FloatProperty(default=3.0,min=0.0,name="Line Width")
    
    def execute(self, context):
        #現在フレームを記録
        scn = bpy.context.scene
        old_frame = scn.frame_current
        #第一フレームに移動
        scn.frame_set(scn.frame_start)
        #最終フレームより先に行ってたら現在フレームに変更して終了
        #最終フレームより先に行ってなかったらレンダリングを繰り返す
        while scn.frame_current < scn.frame_end:
            #レンダリング
            bpy.ops.object.onlyfreestylephoto(my_line_width = self.my_lineWidth,
                my_makeGP = True, my_onlySelect=self.my_isSelect)
            #フレームステップ分飛ばす
            scn.frame_set(scn.frame_current + self.my_frameStep)
            #フレーム更新
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            
        scn.frame_set(old_frame)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
##    Store properties in the active scene
#def initSceneProperties(scn):
#    
#    bpy.types.Scene.OnlySelect = BoolProperty(
#    name = "Only Selected one", 
#    description = "選択されているものだけをFreeStyleで描画")
#    scn['OnlySelect'] = False
#    
#    bpy.types.Scene.ConvGP = BoolProperty(
#    name = "Convert to grease pencil", 
#    description = "FreeStyleをグリースペンシルに変換")
#    scn['ConvGP'] = False
#    
#    return
#initSceneProperties(bpy.context.scene) #ここでちゃんと登録
        
#FreeStyleレンダリングの後処理
def post_lineset(scene, layer, lineset):
    pass
    #print('post_lineset')
    #print('size',Operators().get_strokes_size())
    #freeStyleの3D上での位置はこうして見つける
    #print('index',Operators().get_stroke_from_index(0)[1].point_3d)
    
#Menu in tools region
class AnimeHairPanel(bpy.types.Panel):
    bl_label = "Amasawa Tools"
    bl_space_type = "VIEW_3D"
    bl_context = "objectmode"
    bl_region_type = "UI"
    bl_category = "Custom"
    
    def draw(self, context):
        hairCol = self.layout.column(align=True)
        hairCol.label(text="Create:")
        hairCol.operator("object.animehair")
        hairCol.operator("object.radiustoweight")
        hairCol.operator("object.crease2line")

        col = self.layout.column(align=True)
        col.label(text="Convert:")
        col.operator("object.hair2mesh")
#        col.operator("object.curve2ama")
#        col.operator("object.hair2meshfull")
#        col.operator("object.curve2amafull")
        
        col = self.layout.column(align=True)
        col.label(text="GreasePencil:")
        col.operator("object.gp2line")
        col.operator("object.gp2mesh")
        col.operator("object.gp2animehair")
        col.operator("object.curve2gp")
        
        col4 = self.layout.column(align=True)
        col4.label(text="GreasePencilEdit:")
        #col4.operator("object.gpreducehighdensityparts")
        col4.operator("object.gpiritonuki")
        col4.operator("object.gpsubdivide")
        col4.operator("object.gpstrength")
        col4.operator("object.gpcleanup")
        col4.operator("object.gpallframeedit")
#        col4.operator("object.gpsamepointdissolve")
#        col4.operator("object.gpconnect")
        
        col2 = self.layout.column(align=True)
        col2.label(text="Render:")
        col2.operator("object.onlyfreestylephoto")
        col2.operator("object.onlyfreestyleanime")
        col2.operator("object.gpframerender")
#        col2.operator("object.onlyfreestyleanime")
#        layout = self.layout
#        scn = context.scene
#        col5 = self.layout.column(align=True)
#        col5.prop(scn, 'OnlySelect',toggle=True)
#        col2.prop(scn, 'ConvGP',toggle=True)

        
        col3 = self.layout.column(align=True)
        if context.space_data.type == 'VIEW_3D':
            propname = "gpencil_stroke_placement_view3d"
        elif context.space_data.type == 'SEQUENCE_EDITOR':
            propname = "gpencil_stroke_placement_sequencer_preview"
        elif context.space_data.type == 'IMAGE_EDITOR':
            propname = "gpencil_stroke_placement_image_editor"
        else:
            propname = "gpencil_stroke_placement_view2d"
        ts = context.tool_settings
        col3.label(text="Stroke Placement:")
        row = col3.row(align=True)
        row.prop_enum(ts, propname, 'VIEW')
        row.prop_enum(ts, propname, 'CURSOR')
        if context.space_data.type == 'VIEW_3D':
            row = col3.row(align=True)
            row.prop_enum(ts, propname, 'SURFACE')
            row.prop_enum(ts, propname, 'STROKE')
            row = col3.row(align=False)
            row.active = getattr(ts, propname) in {'SURFACE', 'STROKE'}
            row.prop(ts, "use_gpencil_stroke_endpoints")

        col3.label(text="all of Spline IK:")
        row = col3.row(align=True)
        row.operator("object.viewspik",text="View")
        row.operator("object.hiddenspik",text="Mute")
        col3.label(text="all of Bone constraints:")
        row = col3.row(align=True)
        row.operator("object.viewboneconst",text="View")
        row.operator("object.hidenboneconst",text="Mute")
        
        latcol = self.layout.column(align=True)
        latcol.label(text="Object:")
        
        latrow = latcol.row(align=True)
        latrow.operator("object.setcamelattice",text="Set Camelattice")
        latrow.operator("object.delnonelattice",text="Del None Lattice")
        
        latcol.operator("object.randarray")
        latcol.operator("object.makebuildings")
        latcol.operator("object.makethreeviews")
        
class AnimeHairCurveEditPanel(bpy.types.Panel):
    bl_label = "Amasawa Tools"
    bl_space_type = "VIEW_3D"
    bl_context = "curve_edit"
    bl_region_type = "UI"
    bl_category = "Custom"
    
    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("object.curvetwist")
        col.operator("object.curvetwistreset")
        col = self.layout.column(align=True)
        col.operator("object.setcurveradius")
        col = self.layout.column(align=True)
        col.operator("object.setcurveorderu")
        col.operator("object.setcurveresolutionu")
        
def register():# 登録
    bpy.utils.register_class(AnimeHairOperator)
    bpy.utils.register_class(Radius2weight)

    bpy.utils.register_class(Hair2MeshOperator)
    bpy.utils.register_class(Curve2AmaOperator)
    bpy.utils.register_class(Hair2MeshFullOperator)
    bpy.utils.register_class(Curve2AmaFullOperator)

    bpy.utils.register_class(AnimeHairPanel)
    bpy.utils.register_class(ViewSpIKOperator)
    bpy.utils.register_class(HiddenSpIKOperator)

    bpy.utils.register_class(ViewBoneConstOperator)
    bpy.utils.register_class(HiddenBoneConstOperator)
    
    bpy.utils.register_class( MakePIOperator )
    bpy.utils.register_class( Gp2LineOperator )
    bpy.utils.register_class( Gp2AnimehairOperator )
    bpy.utils.register_class( Crease2LineOperator )
    bpy.utils.register_class( Gp2MeshOperator )
    bpy.utils.register_class( Curve2GPOperator )
    
    bpy.utils.register_class(SetCamelattice)
    bpy.utils.register_class(DelNonelattice)
    
    bpy.utils.register_class(RandArray)
    bpy.utils.register_class(MakeBuildings)
    bpy.utils.register_class(MakeMakeThreeViews)
    
    bpy.utils.register_class(AnimeHairCurveEditPanel)
    bpy.utils.register_class(CurveTwist)
    bpy.utils.register_class(CurveTwistReset)
    bpy.utils.register_class(SetCurveRadius)
    bpy.utils.register_class(SetCurveOrderU)
    bpy.utils.register_class(SetCurveResolutionU)
    
    bpy.utils.register_class(OnlyFreeStylePhoto)
    bpy.utils.register_class(OnlyFreeStyleAnime)
    
    bpy.utils.register_class(GpReduceHighDensityParts)
    
    bpy.utils.register_class(GpFrameRender)
    bpy.utils.register_class(GpIritonuki)
    bpy.utils.register_class(GpSubdivide)
    bpy.utils.register_class(GpStrength)
    bpy.utils.register_class(GpSamePointDissolve)
    bpy.utils.register_class(GpConnect)
    bpy.utils.register_class(GPCleanUp)
    bpy.utils.register_class(GPAllFrameEdit)
    
    bpy.types.VIEW3D_MT_edit_mesh_specials.append( menu_draw )
    
    
    
def unregister():# 解除
    bpy.utils.unregister_class(AnimeHairOperator)
    bpy.utils.unregister_class(Radius2weight)

    bpy.utils.unregister_class(Hair2MeshOperator)
    bpy.utils.unregister_class(Curve2AmaOperator)
    bpy.utils.unregister_class(Hair2MeshFullOperator)
    bpy.utils.unregister_class(Curve2AmaFullOperator)

    bpy.utils.unregister_class(AnimeHairPanel)
    bpy.utils.unregister_class(ViewSpIKOperator)
    bpy.utils.unregister_class(HiddenSpIKOperator)

    bpy.utils.unregister_class(ViewBoneConstOperator)
    bpy.utils.unregister_class(HiddenBoneConstOperator)
    
    bpy.utils.unregister_class( MakePIOperator )
    bpy.utils.unregister_class( Gp2LineOperator )
    bpy.utils.unregister_class( Gp2AnimehairOperator )
    bpy.utils.unregister_class( Crease2LineOperator )
    bpy.utils.unregister_class( Gp2MeshOperator )
    bpy.utils.unregister_class( Curve2GPOperator )
    
    bpy.utils.unregister_class( SetCamelattice)
    bpy.utils.unregister_class( DelNonelattice)
    
    bpy.utils.unregister_class( RandArray )
    bpy.utils.unregister_class(MakeBuildings)
    bpy.utils.unregister_class(MakeMakeThreeViews)
    
    bpy.utils.unregister_class(AnimeHairCurveEditPanel)
    bpy.utils.unregister_class(CurveTwist)
    bpy.utils.unregister_class(CurveTwistReset)
    bpy.utils.unregister_class(SetCurveRadius)
    bpy.utils.unregister_class(SetCurveOrderU)
    bpy.utils.unregister_class(SetCurveResolutionU)
    
    bpy.utils.unregister_class(OnlyFreeStylePhoto)
    bpy.utils.unregister_class(OnlyFreeStyleAnime)
    
    bpy.utils.unregister_class(GpReduceHighDensityParts)
    
    bpy.utils.unregister_class(GpFrameRender)
    bpy.utils.unregister_class(GpIritonuki)
    bpy.utils.unregister_class(GpSubdivide)
    bpy.utils.unregister_class(GpStrength)
    bpy.utils.unregister_class(GpSamePointDissolve)
    bpy.utils.unregister_class(GpConnect)
    bpy.utils.unregister_class(GPCleanUp)
    bpy.utils.unregister_class(GPAllFrameEdit)
    
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove( menu_draw )
  
#入力
#bpy.ops.object.animehair('INVOKE_DEFAULT')

if __name__ == "__main__":
    register()