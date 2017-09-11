import bpy
import math
import array
import sys
import os

import mathutils

#import mathutils
from mathutils import Vector
from mathutils import Matrix
from mathutils import Color

from math import radians

from bpy.types import OperatorStrokeElement

from bpy.props import FloatProperty

#
global _VC_ChannelName
_VC_ChannelName = "VAO"

bpy.types.Scene.archiuv_vao_planarthresshold = bpy.props.FloatProperty(name= "VAO Angle Limit" , description="Faces with a lower rotation are whitened", default = 0)

bpy.types.Scene.archiuv_vao_horizontalsurfacescan = bpy.props.BoolProperty("VAO Horizontal Scan", description="Scan for horizontal faces?", default = False)

# get object rotation matrix
def get_mat_objectrot(object, axisOrder = 'XYZ'):

    mat_rot = mathutils.Matrix.Identity(4)
    for i,char in enumerate(axisOrder):
        mat_angle = mathutils.Matrix.Rotation(object.rotation_euler[i] ,4,char)
        mat_rot = mat_rot * mat_angle.inverted()
    
    return mat_rot

# get object scale matrix
def get_mat_objectscale(object, axisOrder = 'XYZ' ):

    mat_scale = mathutils.Matrix.Identity(4)
    
    for i,char in enumerate(axisOrder):
        
        direction = Vector((0,0,1))
        if (char == 'X'):
            direction = Vector((1,0,0))

        if (char == 'Y'):
            direction = Vector((0,1,0))

        if (char == 'Z'):
            direction = Vector((0,0,1))
            
        mat_sc = mathutils.Matrix.Scale(object.scale[i] ,4,direction)
        
        mat_scale = mat_scale * mat_sc   
    return mat_scale

# because python does not know Clamp
def Clamp(val, clampMin, clampMax):
    return max(min(val, clampMax), clampMin)

##############
# VAO
##############

# check if this object has a VAO channel, if not create one
def CheckAndCreateEmptyVAOMap(object):
    mesh = object.data
    # this is quiete safe
    try:
        mesh.vertex_colors[_VC_ChannelName]
    except:
        print("VAO Channel does not exist, creating a new one")
#        bpy.ops.mesh.vertex_color_add() # only uses selected mesh
        mesh.vertex_colors.new(_VC_ChannelName)
#       mesh.vertex_colors.active.name = _VC_ChannelName   

def CreateVAOMap(object, mode ,parameter = 'BOT'):


    # settings    Scene.archiuv_vao_horizontalsurfacescan

    bNormalsCheck = bpy.context.scene.archiuv_vao_horizontalsurfacescan
    mesh = object.data
    
    # get object Z dimension
    objectHeight = object.dimensions.z
    if objectHeight == 0:
        objectHeight = 1
    print(objectHeight)
    
    # get correct VC channel, this is quiete safe
    try:
        mesh.vertex_colors[_VC_ChannelName]
    except:
        print("VAO Channel does not exist, creating a new one")
#        bpy.ops.mesh.vertex_color_add() # only uses selected mesh
        mesh.vertex_colors.new(_VC_ChannelName)
#       mesh.vertex_colors.active.name = _VC_ChannelName
    vCol = mesh.vertex_colors[_VC_ChannelName].data
    
    # MODES: CURSOR_3D , LOCAL, WORLD
    
    mat_rot = get_mat_objectrot(object, 'XYZ')
    mat_scale = get_mat_objectscale(object)
    mat_transform =  mat_scale * mat_rot
    
    # points used to calculate shade, defaults to first vertex position
    topPoint = mesh.vertices[0].co * mat_transform + object.location
    botPoint = mesh.vertices[0].co * mat_transform + object.location


    # find highest and lowest points
    for vertex in mesh.vertices:
        vert = vertex.co * mat_transform
        if(vert.z + object.location.z > topPoint.z):
            topPoint = vert + object.location
        if(vert.z + object.location.z < botPoint.z):
            botPoint = vert + object.location
     
    if(mode == 'LOCAL'):
        print("Current mode is %s" %(mode))
           # botpoint and toppoint are already set, no problems

    
    if(mode == 'CURSOR_3D'):
        print("Current mode is %s, parameter is %s" %(mode,parameter))
#        parameter = 'BOT' # bot,top,auto
        
        cursorLocation = bpy.context.scene.cursor_location
        if(parameter == 'BOT'):
            botPoint = cursorLocation
        if( parameter == 'TOP'):
            topPoint = cursorLocation

    print("toppoint: %s,  botpoint: %s" %(topPoint, botPoint)) 
    
    for face in mesh.polygons:
        faceID = face.index
        normal = face.normal * mat_rot
        col_normalMod = 0
        if(bNormalsCheck):
            # do normals check
            print(bNormalsCheck)
            # todo: come up with a blending mode
            if(normal.z >= .9):
                col_normalMod = 1
        
#        print ("Face: %s" %(faceID))
        for vertloopID, v_idx in enumerate(mesh.polygons[faceID].loop_indices):

            vertIDInLoop = mesh.loops[v_idx].vertex_index
            vertCol = vCol[v_idx]
            vertexCoords = mesh.vertices[vertIDInLoop].co * mat_transform
            
            # the forumale
            #
            # (Zp - Zb)
            #----------- = height relative to top and bot, MAKE SURE no 0 divisions
            # (Zt - Zb )
            
            #numerator:
            enumerator = (vertexCoords.z + object.location.z) - botPoint.z
            #denominator:
            denominator = (topPoint.z - botPoint.z)
            
            if(denominator == 0 ):
                print("WARNING: There is no height difference")
                denominator = 1
            
            heightFraction = ( enumerator / denominator )
            
            heightFraction = Clamp (heightFraction, 0 , 1)
            if(heightFraction <0 ):
                heightFraction = 0
            
            print("Heightfraction: %s" %(heightFraction))
            print("Normalmod: %s" %(col_normalMod))

            newColor = heightFraction+col_normalMod  
            print("Heightfraction: %s" %(heightFraction))
            print("Normalmod: %s" %(col_normalMod))
            print("NewColor: %s" %(newColor))
            vertCol.color = Color((newColor,newColor,newColor))   
    
 
class ArchiUV_VAOButton(bpy.types.Operator):
    bl_idname = "archiuv_vao_addmap.button"
    bl_label = "Apply Empty"
    bl_description = "Adds a white VAO layer to any object that has no VAO yet. This prevents them from flickering."
    
    
    def execute(self, context):
        for obj in bpy.context.selected_editable_objects:
            if (obj.type == 'MESH'):
                CheckAndCreateEmptyVAOMap( obj )
        return {'FINISHED'}


class ArchiUV_VAOButton(bpy.types.Operator):
    bl_idname = "archiuv_vao_local.button"
    bl_label = "VAO LOCAL"
    
    def execute(self,context):
        print("LOCAL")
        for obj in bpy.context.selected_editable_objects:
            CreateVAOMap(obj,'LOCAL')
        return {'FINISHED'}
    
class ArchiUV_VAOButton(bpy.types.Operator):
    bl_idname = "archiuv_vao_cursor.button"
    bl_label = "VAO CURSOR"
    topbot = bpy.props.StringProperty()
    
    def execute(self,context):
        for obj in bpy.context.selected_editable_objects:
            CreateVAOMap(obj,'CURSOR_3D' , self.topbot)
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__);
    bpy.types.Scene.archiuv_vao_planarthresshold = bpy.props.FloatProperty(name= "VAO Angle Limit" , description="Faces with a lower rotation are whitened", default = 0)
    bpy.types.Scene.archiuv_vao_horizontalsurfacescan = bpy.props.BoolProperty("VAO Horizontal Scan", description="Scan for horizontal faces?", default = False)


def unregister():
    bpy.utils.unregister_module(__name__);


if __name__ == "__main__":
    register()