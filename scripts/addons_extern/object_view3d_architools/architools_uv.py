import bpy
import math
import array
import sys
import os

import mathutils

from mathutils import *
from math import *
from bpy.props import *

_UVMapName = "ArchitectUV"
bpy.types.Object.archiuv_uvrotation = bpy.props.FloatProperty(name="UV Rotation", description = "Determines the rotation of the UV' on an object", default= 0)
bpy.types.Scene.archiuv_operationOrigin = bpy.props.BoolProperty(name="Origin 3D cursor", description ="Use the position of the 3D cursor as a refference to align the texture with", default = True)
def CreateRotationMatrix( Vx, Vy, Vz ):
    mat = Matrix.Identity(4)
    
    Vx.normalize()
    Vy.normalize()
    Vz.normalize()
    
    mat[0].xyz = Vx
    mat[1].xyz = Vy
    mat[2].xyz = Vz
    return mat

def GetActiveMaterialSlotScale( object ):
    mat = object.active_material
    scale = Vector((1,1,1))
    if ( mat != None ):
        slot = mat.active_texture_index
        tex = mat.texture_slots[slot]
        if( tex != None):
            scale = tex.scale        
    return scale
    
# returns face transform matrix
def GetFaceTransform(object, faceid):
    
    currentPoly = object.data.uv_layers.data.polygons[faceid]

    triangleUp = Vector(currentPoly.normal)
    triangleUp.normalize()

    triangleForward = triangleUp.cross(Vector((0,0,1)))
    triangleForward.normalize()
    
    triangleRight = triangleUp.cross(triangleForward)
    triangleRight.normalize()

     # fix names
    if( triangleForward.z == 0 ):
        triangleForward,triangleRight = triangleRight,triangleForward
    
    if( triangleForward.z < 0 ):
        triangleForward.negate()
        
    if( triangleRight.z < 0 ):
        triangleRight.negate()       
         
    triangleRight = triangleForward.cross(triangleUp)
    triangleRight.normalize()  
    
    if( triangleUp.z == 1 ):
        triangleForward = Vector((0,1,0))
        triangleRight = Vector((1,0,0))
    if( triangleUp.z == -1):
        triangleForward = Vector((0,-1,0))
        triangleRight = Vector((-1,0,0))

    # get each vert pos, and calc average to get face pos
    polypos = Vector()
    for vertID in currentPoly.vertices:
        polypos += object.data.vertices[vertID].co
    if( len( currentPoly.vertices ) >0):
        polypos = polypos / len( currentPoly.vertices )

    worldPos = object.location    
#    worldFacePos = worldPos #- polypos / 3
    worldFacePos = polypos
    worldFacePos = worldPos
    
    # align with 3D cursor?
    

    if (bpy.context.scene.archiuv_operationOrigin == True):
        worldFacePos = (-bpy.context.scene.cursor_location + worldFacePos)

      
    print("world face pos: %s" %( worldFacePos))
    uvFacePos = Vector()
    
    if (currentPoly.normal.z >= 0.99 or currentPoly.normal.z <= -0.99): # facing UP or DOWN
        uvFacePos = Vector(( math.modf(worldFacePos.x)[0], math.modf(worldFacePos.y)[0],0)) 
#        uvFacePos = Vector((worldFacePos.x , worldFacePos.y , 0))
    else:
#        uvFacePos = Vector(( math.modf(worldFacePos.x + worldFacePos.z)[0], math.modf(worldFacePos.y + worldFacePos.z)[0],0))  
        uvFacePos = Vector(( math.modf(worldFacePos.x)[0], math.modf(worldFacePos.y)[0],0))          
    translationMatrix = Matrix.Translation(uvFacePos)
#    offSetTransformMatrix = Matrix.Translation(-(-bpy.context.scene.cursor_location + object.location).z)
#    offSetScaleMatrix = 
    #                if(currentPoly.normal.z < 0.99 or currentPoly.normal.z > -0.99):
#                   yOffset =  (-(-bpy.context.scene.cursor_location + object.location).z) * (1+ currentPoly.normal.z)
#    translationMatrix.invert()
    rotationMatrix = CreateRotationMatrix(triangleRight,triangleForward ,triangleUp )

    additionRotMatrix = Matrix.Rotation(radians(object.archiuv_uvrotation),4, 'Z')
    
    transformMatrix =  additionRotMatrix* rotationMatrix * translationMatrix
        
    return transformMatrix
    

def UV_UnwrapFaces(object, faces):
    is_editmode = (object.mode == 'EDIT')
    # get [faces]
    mesh = object.data
    uvs = mesh.uv_layers[_UVMapName].data
    # faces is a list of coplanar faces lists ( every face in a facelist IN faces share normals )
    
    for index, faceList in enumerate(faces): # per facelist
        transform = GetFaceTransform(object, faceList[0])  

        
        for faceID in faceList: # per face
            
            currentPoly = object.data.uv_layers.data.polygons[faceID]
            
            for vertloopID, loop in enumerate(mesh.polygons[faceID].loop_indices):
                v_idx = mesh.loops[loop].vertex_index
                co = mesh.vertices[v_idx].co #+ object.location
                co_uv = transform * co
                yOffset = 0
                
                if(currentPoly.normal.z < 0.99 or currentPoly.normal.z > -0.99):
                    yOffset =  (-(-bpy.context.scene.cursor_location + object.location).z) #* (1+ currentPoly.normal.z)
                   
                uvs[loop].uv[0] = co_uv.x                  
                uvs[loop].uv[1] = co_uv.y + yOffset
                
def InitUVMap(object):
    UvKey = None
    global _UVMapName
    if( object.data.uv_textures != None):
        for UV in object.data.uv_textures:
            if(UV.name == _UVMapName):
                UvKey = _UVMapName
    if( UvKey == None ):
        object.data.uv_textures.new(_UVMapName)


def GetCoplanarFaces(object, c_faces ):
    cp_faces = [[]] # list of faces with the same normals
    cp_normals = [] # list of normals
    
    # relation between cp_faces and cp_normals
        # cp_normals contains normals that relate to face[] in cp_faces
        # example:
                #cp_normals: (0,0,1),(0,1,0)
                #cp_faces:    [1,2], [3,4,5]
                #which means that faces 1 and 2 have normal (0,0,1)
    mesh = object.data
    
    for faceID in c_faces:
#       DebugPrint (faceID)
       face = mesh.polygons[faceID] # list contains a LOT more faces
#       DebugPrint("Iterating over face: %s, norm: %s" %(faceID, face.normal))
       
       # if this normal already exists , get it' ID, if it does not, create a new index
       try:
           cp_normals.index(face.normal)  
#           break
       except ValueError:
           cp_normals.append(face.normal)
#           DebugPrint("Normal not found, adding one to the list")
       
       # the ID of the current normal
       normalID = cp_normals.index(face.normal)
#       DebugPrint("Processinging normalID: %s , normal: %s" %(normalID,cp_normals[normalID] ) )   
           
       if ( len(cp_faces) < normalID+1):
#            DebugPrint("Creating new faces list")
            cp_faces.append([]) # create a new faceList
#       else: DebugPrint("Face list for this normal already exists")
       if(cp_faces[normalID] == None):
#           DebugPrint("Creating new empty array for normal")
           cp_faces[normalID] = [] 
       cp_faces[normalID].append(faceID)
#       DebugPrint(cp_faces)  
    return cp_faces

# puts all loops in a neat list
def GatherFaces(object):
    mesh = object.data
    l_faces = []
    for i, pol in enumerate(mesh.polygons):
        l_faces.append(i)
        
        #for j,loop in enumerate(mesh.polygons[i].loop_indices):
            # check if this face already exists ?
         #   try:
          #      l_faces.index(loop)
           # except ValueError:
                # non existant value
            #    l_faces.append(loop)
    return l_faces

# unwrap the current selection with a given rotational mod
def UnwrapSelection(rotationMod = 0):
    
    for currentObject in bpy.context.selected_editable_objects:
#        DrawConsole()    
        # adjust the rotationmod of the current object
        currentObject.archiuv_uvrotation += rotationMod
        # limit to -360 or 360
        currentObject.archiuv_uvrotation = currentObject.archiuv_uvrotation % 360
    # Create/Find correct UV Channel
        InitUVMap(currentObject)
    # map every face
        l_faces = GatherFaces(currentObject)
#        DebugPrint("Object face count: %s, list face count: %s" %(len(currentObject.data.polygons),len(l_faces)))
        cp_faces = GetCoplanarFaces(currentObject,  l_faces)
    # now that I am certain that the UV map exists
        UV_UnwrapFaces(currentObject, cp_faces)
       

class ArchiUV_UnwrapButton(bpy.types.Operator):
    bl_idname = "archiuv_unwrap.button"
    bl_label = "Unwrap!"
    bl_description = "Unwrap and align with a angle."
    rotationMod = bpy.props.FloatProperty()
    
    def execute(self,context):
        print("Unwrapping...123")
        print("Unwrapping...123")
        
#        ClearConsoleScreen()   
#        unwrapall()
        UnwrapSelection(self.rotationMod)
#        DebugPrint(self.rotationMod)
        return{'FINISHED'}

def register():
        bpy.utils.register_module(__name__);
        bpy.types.Object.archiuv_uvrotation = bpy.props.FloatProperty(name="UV Rotation", description = "Determines the rotation of the UV' on an object", default= 0)
        
if __name__ == "__name__":
    register()
    
# debug
#UnwrapSelection()