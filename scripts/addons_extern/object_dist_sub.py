#
# dist_sub.py
#
# This script automatically sets subdivision levels for
# objects with a Subdivision modifier, based on their distance
# from the camera. 
#
bl_info = { "name": "Distance-based Subdivision", 
            "description": "Sets subdivision levels on objects based on distance from the camera",
            "version": (0, 1),
            "blender": (2, 76, 0),
            "category": "Object",
            "author": "Dale Cieslak"}

import bpy
from math import *
from bpy.props import *

# Store properties in the active scene
#
bpy.types.Scene.NearDist = FloatProperty(
    name = "Near distance", 
    description = "nearest distance to set SubD level",
    default = 0.0)
 
bpy.types.Scene.FarDist = FloatProperty(
    name = "Far distance", 
    description = "farthest distance to set SubD level",
    default = 10000.0)
 
bpy.types.Scene.MaxSubd = IntProperty(
    name = "Max. SubD level",
    description = "maximum subd level for closest object",
    default = 4)
    
bpy.types.Scene.MinSubd = IntProperty(
    name = "Min. SubD level",
    description = "minimum subd level for farthest object",
    default = 0)
    
bpy.types.Scene.AllObjects = BoolProperty(
    name="Affect All Objects",
    default = True)

bpy.types.Scene.VisualLevels = BoolProperty(
    name="Set Visual Levels",
    default = False)
    
# Set up panel layout
class ToolPropsPanel(bpy.types.Panel):

    bl_label = "Distance-based SubD"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def draw(self, context):
        scene = context.scene
       
        self.layout.prop(scene, 'NearDist')
        self.layout.operator('set.neardist')
        self.layout.operator('set.neardistsel')
        self.layout.operator('set.neardistcam')
        self.layout.separator()
        self.layout.prop(scene, 'FarDist')
        self.layout.operator('set.fardist')
        self.layout.operator('set.fardistsel')
        self.layout.operator('set.fardistcam')
        self.layout.separator()
        self.layout.prop(scene, 'MaxSubd')
        self.layout.prop(scene, 'MinSubd')
        self.layout.separator()
        self.layout.prop(scene, 'AllObjects')
        self.layout.prop(scene, 'VisualLevels')
        self.layout.operator('execute.subdset')
    

class OBJECT_OT_ExecuteButton(bpy.types.Operator):
    bl_idname = "execute.subdset"
    bl_label = "Set SubD Levels"

    def execute(self, context):
        scene = context.scene
        cam_obj = bpy.data.objects[context.scene.camera.name]

        clip = scene.FarDist - scene.NearDist

        maxLevel = scene.MaxSubd - scene.MinSubd
        offset = scene.MinSubd
        
        for ob in scene.objects:
            if len(ob.modifiers) > 0:
                for m in ob.modifiers:
                    if ob.select == True or scene.AllObjects == True:
                        if m.type == 'SUBSURF':
                            dist = measure(ob.location, cam_obj.location) - scene.NearDist
                            if dist < 0:
                                subdLevel = scene.MaxSubd
                            elif dist > clip:
                                subdLevel = scene.MinSubd
                            else:
                                subdLevel = int((1.0-(dist/clip)) * maxLevel + 0.5) + offset
                            
                            if scene.VisualLevels:
                                m.levels = subdLevel
                            m.render_levels = subdLevel

        return{'FINISHED'}

class OBJECT_OT_SetNearDistButton(bpy.types.Operator):
    bl_idname = "set.neardist"
    bl_label = "Nearest Object"
 
    def execute(self, context):
        cam_obj = bpy.data.objects[context.scene.camera.name]

        scene = context.scene
        nearVal = 10000.0
        for ob in scene.objects:
            if not ob == cam_obj:
                dist = measure(ob.location, cam_obj.location)
                if dist < nearVal:
                    nearVal = dist

        scene['NearDist'] = nearVal
        return{'FINISHED'} 

class OBJECT_OT_SetNearDistSelButton(bpy.types.Operator):
    bl_idname = "set.neardistsel"
    bl_label = "Nearest Selected"
 
    def execute(self, context):
        cam_obj = bpy.data.objects[context.scene.camera.name]

        scene = context.scene
        nearVal = 10000.0
        for ob in scene.objects:
            if ob.select == True:
                dist = measure(ob.location, cam_obj.location)
                if dist < nearVal:
                    nearVal = dist

        scene['NearDist'] = nearVal
        return{'FINISHED'} 

class OBJECT_OT_SetNearDistCamButton(bpy.types.Operator):
    bl_idname = "set.neardistcam"
    bl_label = "Camera Clip Start"
 
    def execute(self, context):
        cam = bpy.data.cameras[context.scene.camera.name]
    
        scene = context.scene
        scene['NearDist'] = cam.clip_start
        return{'FINISHED'} 

class OBJECT_OT_SetFarDistButton(bpy.types.Operator):
    bl_idname = "set.fardist"
    bl_label = "Farthest Object"
 
    def execute(self, context):
        cam_obj = bpy.data.objects[context.scene.camera.name]

        scene = context.scene
        farVal = 0.0
        for ob in scene.objects:
            if not ob == cam_obj:
                dist = measure(ob.location, cam_obj.location)
                if dist > farVal:
                    farVal = dist

        scene['FarDist'] = farVal
        return{'FINISHED'}    


class OBJECT_OT_SetFarDistSelButton(bpy.types.Operator):
    bl_idname = "set.fardistsel"
    bl_label = "Farthest Selected"
 
    def execute(self, context):
        cam_obj = bpy.data.objects[context.scene.camera.name]

        scene = context.scene
        farVal = 0.0
        for ob in scene.objects:
            if ob.select == True:
                dist = measure(ob.location, cam_obj.location)
                if dist > farVal:
                    farVal = dist

        scene['FarDist'] = farVal
        return{'FINISHED'}    

class OBJECT_OT_SetFarDistCamButton(bpy.types.Operator):
    bl_idname = "set.fardistcam"
    bl_label = "Camera Clip End"
 
    def execute(self, context):
        cam = bpy.data.cameras[context.scene.camera.name]

        scene = context.scene
        scene['FarDist'] = cam.clip_end
        return{'FINISHED'} 

# calculate distance between two points
def measure (first, second):
    locx = second[0] - first[0]
    locy = second[1] - first[1]
    locz = second[2] - first[2]
    distance = sqrt((locx)**2 + (locy)**2 + (locz)**2) 
    return distance

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

