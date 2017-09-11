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
 "name": "Animation Joiner",  
 "author": "Francois Grassard (AKA CoyHot)",  
 "version": (1, 0),  
 "blender": (2, 6, 4),  
 "location": "View3D > Animation > Animation Joiner",  
 "description": "Merge animated objects into only one mesh, driven by a PC2 file or shape keys",
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Animation"}  

import bpy
import struct
import math


def get_sampled_frames(start, end, sampling):
    return [math.modf(start + x * sampling) for x in range(int((end - start) / sampling) + 1)]

class AnimaJoiner(bpy.types.Panel):
    bl_label = "Animation Joiner"
    bl_idname = "coyhot.animationJoiner"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Animation"
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, 'animaJoinerExportPC2')
        layout.prop(context.scene, 'animaJoinerPC2ConfPath')
        layout.prop(context.scene, 'animaJoinerAnimByShape')
        layout.prop(context.scene, 'animaJoinerSupportSkinnedObjects')
        layout.prop(context.scene, 'animaJoinerMoveToNextLayer')
        layout.operator("object.animationjoinerexec")

class animationJoinerMainFunc(bpy.types.Operator):
    bl_idname = "object.animationjoinerexec"
    bl_label = "Join selected objects"
    
    def execute(self,context):
        wm = bpy.context.window_manager
        selectedOBJ = bpy.context.selected_objects
        targetScene = bpy.context.scene
        filePathToPC2 = targetScene.animaJoinerPC2ConfPath
        convertToShapeKeys = bpy.context.scene.animaJoinerAnimByShape
        convertToPointCache = bpy.context.scene.animaJoinerExportPC2
        moveToNextLayer = bpy.context.scene.animaJoinerMoveToNextLayer
        supportSkinnedObjects = bpy.context.scene.animaJoinerSupportSkinnedObjects

        startFrame = bpy.context.scene.frame_start
        endFrame = bpy.context.scene.frame_end+1
        wm.progress_begin(startFrame, endFrame)
        sampletimes = get_sampled_frames(startFrame, endFrame, 1.0)
        sampleCount = len(sampletimes)
		
        listTempDatas = []

        headerFormat='<12siiffi'
        file = open(filePathToPC2, "wb")
			
        for i in range(startFrame,endFrame):
            wm.progress_update(i)
            bpy.context.scene.frame_set(i)

            for obj in selectedOBJ:
                obj.select = True
			
			
            if not (supportSkinnedObjects) :
                bpy.ops.object.duplicate(linked=True)
            else :
                bpy.ops.object.duplicate(linked=False)


            nameOfNewShape = "mergedAnimatedObjectShape__"+str(i).zfill(5)
            newTargetData = bpy.data.meshes.new(nameOfNewShape)
            newTargetObj = bpy.data.objects.new(("mergedAnimatedObject__"+str(i).zfill(5)), newTargetData)

            targetScene.objects.link(newTargetObj)
            targetScene.objects.active = newTargetObj
            newTargetObj.select = True

            if (supportSkinnedObjects) :
                bpy.ops.object.convert(target='MESH',keep_original=False)
                selectedTempOBJ = bpy.context.selected_objects
                for obj in selectedTempOBJ:
                    selectedTempData = obj.data
                    if not (selectedTempData.name == nameOfNewShape) :
#                        print (selectedTempData)
                        listTempDatas.append(selectedTempData)

            targetScene.objects.active = newTargetObj
            newTargetObj.select = True

#            bpy.context.scene.objects.active = newTargetObj
            bpy.ops.object.join()

            for obj in listTempDatas:
#                print(obj)
                bpy.data.meshes.remove(obj)
#            if (supportSkinnedObjects) :
#                for item in selectedTempOBJ:
#                    item.data.meshes.remove(item)	

            listTempDatas[:]=[]

            if (i == startFrame) :
                for item in bpy.context.selectable_objects:
                    item.select = False
                destObject = bpy.data.objects["mergedAnimatedObject__"+str(startFrame).zfill(5)]
                destObject.select = True

                if(bpy.context.object.active_shape_key):
                    bpy.context.scene.objects.active = destObject
                    bpy.context.object.active_shape_key_index = 1				
                    bpy.ops.object.shape_key_remove(all=True)

                if (convertToShapeKeys) :
                    bpy.ops.object.shape_key_add(from_mix=False)
                if (convertToPointCache) :
                    newMesh = destObject.data
                    headerStr = struct.pack(headerFormat, b'POINTCACHE2\0',1, len(newMesh.vertices), startFrame, 1.0, sampleCount)
                    file.write(headerStr)
                    objForPC2 = bpy.context.selected_objects[0].data.vertices
                    for v in objForPC2:
                        thisVertex = struct.pack('<fff', float(v.co[0]),float(v.co[1]),float(v.co[2]))
                        file.write(thisVertex)
                for item in bpy.context.selectable_objects:
                    item.select = False
            else :
                for item in bpy.context.selectable_objects:
                    item.select = False
                
                nameOfCurrentShape = "mergedAnimatedObject__"+str(i).zfill(5)
                
                bpy.data.objects[nameOfCurrentShape].select = True
				
                if(bpy.context.object.active_shape_key):
                    bpy.context.scene.objects.active = bpy.data.objects[nameOfCurrentShape]
                    bpy.context.object.active_shape_key_index = 1				
                    bpy.ops.object.shape_key_remove(all=True)

                if (convertToPointCache) :
                    objForPC2 = bpy.context.selected_objects[0].data.vertices
				
                if (convertToShapeKeys) :
                    bpy.context.scene.objects.active = destObject
                    bpy.ops.object.join_shapes()
                if (convertToPointCache) :
                    for v in objForPC2:
                        thisVertex = struct.pack('<fff', float(v.co[0]),float(v.co[1]),float(v.co[2]))
                        file.write(thisVertex)
                bpy.ops.object.delete(use_global=False)
				
                if (convertToShapeKeys) :                
                    destObject.data.shape_keys.key_blocks[nameOfCurrentShape].value = 0.0
                    destObject.data.shape_keys.key_blocks[nameOfCurrentShape].keyframe_insert("value",frame=i-1)

                    destObject.data.shape_keys.key_blocks[nameOfCurrentShape].value = 1.0
                    destObject.data.shape_keys.key_blocks[nameOfCurrentShape].keyframe_insert("value",frame=i)

                    if not i == bpy.context.scene.frame_end:

                        destObject.data.shape_keys.key_blocks[nameOfCurrentShape].value = 0.0
                        destObject.data.shape_keys.key_blocks[nameOfCurrentShape].keyframe_insert("value",frame=i+1)
                
#                    bpy.data.meshes.remove(bpy.data.meshes[nameOfNewShape])

                bpy.data.meshes.remove(bpy.data.meshes[nameOfNewShape])

            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        if (convertToPointCache) :
            file.flush()
            file.close()
        destObject.name = "oneAnimatedObject"
        destObject.data.name = "oneAnimatedObjectData"
        destObject.select = True
			
        if (convertToPointCache) :
            destObject.select = True
            targetScene.objects.active = destObject
            bpy.ops.object.modifier_add(type='MESH_CACHE')
            bpy.context.object.modifiers["Mesh Cache"].cache_format = 'PC2'
            destObject.modifiers["Mesh Cache"].filepath = filePathToPC2
            destObject.modifiers["Mesh Cache"].frame_start = 1.0
			
        if (moveToNextLayer) :
            layers_new = [False] * 20
            layers_new[(destObject.layers[:].index(True) + 1) % 20] = True
            destObject.layers = layers_new
			
        return{'FINISHED'}


def register():
    bpy.utils.register_class(AnimaJoiner)
    bpy.utils.register_class(animationJoinerMainFunc)
    bpy.types.Scene.animaJoinerPC2ConfPath = bpy.props.StringProperty(name = "PC2 File", default = "/tmp/animJoinerPointCache.pc2",description = "Define the path to the generated PC2 file",subtype = 'FILE_PATH')
    bpy.types.Scene.animaJoinerExportPC2 = bpy.props.BoolProperty(name = "Export PC2 file",description = "Export the animation to PC2 PointCache File",default=False)
    bpy.types.Scene.animaJoinerAnimByShape = bpy.props.BoolProperty(name = "Convert animation to shape keys",description = "Recreate the animation by using one shape per frame",default=False)
    bpy.types.Scene.animaJoinerMoveToNextLayer = bpy.props.BoolProperty(name = "Move to the next layer",description = "Move the animated object to the next layer",default=True)
    bpy.types.Scene.animaJoinerSupportSkinnedObjects = bpy.props.BoolProperty(name = "Support objects with modifiers (it could be a bit longer)",description = "Export the animation to PC2 PointCache File",default=False)


def unregister():
    bpy.utils.unregister_class(AnimaJoiner)
    bpy.utils.unregister_class(animationJoinerMainFunc)
    del bpy.types.Scene.animaJoinerPC2ConfPath
    del bpy.types.Scene.animaJoinerExportPC2
    del bpy.types.Scene.animaJoinerAnimByShape
    del bpy.types.Scene.animaJoinerMoveToNextLayer
	
    
if __name__ == "__main__":
    register()