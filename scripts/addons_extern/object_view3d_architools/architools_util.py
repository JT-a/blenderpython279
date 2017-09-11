import bpy
import math
import mathutils

from mathutils import *
from math import *

#global constants

global MAX_HIERARCHYLOOPS
MAX_HIERARCHYLOOPS = 20

bpy.types.Scene.archiutil_copymods_array = bpy.props.BoolProperty(name="Copy Array", description = "Setting for modifier copies", default= True)
bpy.types.Scene.archiutil_copymods_edgesplit = bpy.props.BoolProperty(name="Copy Edge split", description = "Setting for modifier copies", default= True)


def GetObjectGeometricalOrigin(obj):
    mesh = obj.data

    totalpos = Vector((0,0,0))
    for vert in mesh.vertices:
        totalpos = totalpos + vert.co
    numVerts = len(mesh.vertices)

    averagePos = totalpos * ( 1 / numVerts )
    return averagePos

def ApplySharedTransform(obj,bPos, bRot, bScale):
    print('Applying object transform')
    # select all shared meshes, apply correct transforms and adjust other meshes
    select_shared_meshdata()

    # make a transform matrix of the position, rotation and scale
    posMat, rotMat, scaleMat = Matrix.Identity(4),Matrix.Identity(4),Matrix.Identity(4)

    # go into edit mode, scale the verts and set the object transforms to default ( set all objects to default scale rot pos

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')

        
    if( bPos == True ):
        # find object geometrical origin and the offset of the objects origin
        geometryOrigin = GetObjectGeometricalOrigin(obj)
        print("Geometry origin: %s" %(geometryOrigin))
        
        bpy.ops.transform.translate(value=geometryOrigin)

    if(bScale == True ):
        bpy.ops.transform.resize(value=obj.scale)

            
    if(bRot == True):
        bpy.ops.transform.rotate( value=obj.rotation_euler.x, axis=Vector((1,0,0)) )
        bpy.ops.transform.rotate( value=obj.rotation_euler.y, axis=Vector((0,1,0)) )
        bpy.ops.transform.rotate( value=obj.rotation_euler.z, axis=Vector((0,0,1)) )
    

    
    bpy.ops.object.editmode_toggle()

    
    for selectionObj in bpy.context.selected_editable_objects:
        
        
        # rot
        if(bRot == True):   
            selectionObj.rotation_euler = Vector((0,0,0))
        
        # pos
        if( bPos == True ):
            selectionObj.location = Vector((0,0,0))        

        # scale
        if(bScale == True ):
            selectionObj.scale = Vector((1,1,1))
    

def MoveSharedMeshOrigin(obj, argument, val):
    # possible arguments: 'CENTEROFMASS' , 'CURSOR3D' , 'POSITION'
    return {'FINISHED'}

def select_list(objectList):
    print("applying selection")
    for obj in objectList:
        obj.select = True

### select similar meshes
def select_shared_meshdata():
    bpy.ops.object.select_linked()
    
### copies all modifiers and modifier settings from object to object
def copy_modifiers(source, target, modifiertype):

    print("Copying modifiers of type: %s" %(modifiertype))
    ## iterate over all modifiers in source object and compare them to the target's mods
    ## if the source has no modifiers, no actions will be taken

    for sourcemod in source.modifiers:
        if (sourcemod.type == modifiertype):
            # check if the target has an array with the same name
            sourcemod_name = sourcemod.name
            
            try:
                targetarraymod_name = target[sourcemod_name].name
                ## if found and no errors are encountered, this array already exists.
            except:
                ## catch any exception, add new array
                modCount = len(target.modifiers)
                bpy.ops.object.modifier_add(type=modifiertype)
                target.modifiers[modCount].name = sourcemod_name

            ## copy settings ( hope this works )
            target.modifiers[sourcemod_name] = sourcemod

class ArchiUtil_CopyModsButton(bpy.types.Operator):
    bl_idname = "archiutil_copymods.button"
    bl_label = "Copy modifiers"

    def execute(self,context):

        print("Copying mods:")
        # active obj
        active_object = bpy.context.active_object
        print ("Active object is of type: %s"%(active_object.type))
        if( active_object.type == 'MESH'):            
            for obj in bpy.context.selected_editable_objects:
                if ( bpy.context.scene.archiutil_copymods_array == True ):
                    print("Copying array")
                    copy_modifiers(active_object , obj , 'ARRAY')
                if ( bpy.context.scene.archiutil_copymods_edgesplit == True ):
                    print("Copying edge split")
                    copy_modifiers(active_object , obj , 'EDGE_SPLIT')
        return {'FINISHED'}
class ArchiUtil_ApplySharedTransform(bpy.types.Operator):
    bl_idname = "archiutil_applysharedtransform.button"
    bl_label = "Apply transform to all shared meshdata objects"

    def execute(self,context):
        ApplySharedTransform(bpy.context.active_object , True , True, True)
        return {'FINISHED'}
class ArchiUtil_SelectSharedButton(bpy.types.Operator):
    bl_idname = "archiutil_selectshared.button"
    bl_label = "Select Shared"
    selectType = bpy.props.StringProperty(name="selectshared_type")

    def execute(self,context):
       
        print("Selecting similar: %s" %(self.selectType))

        if( self.selectType == 'OBJECTTYPE'):
            # begin logic
            baseObject = bpy.context.active_object
            similarObjects = []
            print("similairty: %s" %(baseObject.type))
            
            # iteratore over all objects
            for obj in bpy.data.objects:
                if(baseObject.type == obj.type):
                    similarObjects.append(obj)
            print("%s mode delivered %s similar object(s)!" %(self.selectType, len(similarObjects)))
            select_list(similarObjects)
            # done
            
        elif( self.selectType == 'MESHDATA'):
            # begin logic
            select_shared_meshdata()
            # done
            
        elif( self.selectType == 'VERTEXCOUNT'):
            # begin logic
            
            baseObject = bpy.context.active_object
            similarObjects = []
            
            # only meshes have vertices:
            desiredObjectType = 'MESH'
            if(baseObject.type == desiredObjectType):
                baseObjVxCount = len(baseObject.data.vertices)
                print("similairty: VertexCount %s" %(baseObjVxCount))
                # go find objects
                for obj in bpy.data.objects:
                    try:
                        objVxCount = len(obj.data.vertices)
                        if( baseObjVxCount == objVxCount):
                            similarObjects.append(obj)
                    except AttributeError: # can only be thrown if one of the objects is not a mesh
                        pass
            print("%s mode delivered %s similar object(s)!" %(self.selectType, len(similarObjects)))            
            #
            select_list(similarObjects)
            # done
            
        elif( self.selectType == 'MATERIAL' ):
            # select all objects that share any material from any slot
            # begin logic
            baseObject = bpy.context.active_object
            similarObjects = []
            print("similairty: Materials")
                # per object
            for obj in bpy.data.objects:      
                try:
                    # rework 1.0: Use active material only
                    # Old 0.0: per mat in baseObject, breaks on sign of first match
                    baseObjMat = baseObject.active_material
                    matchFound = False
                    # per mat in object
                    for objMat in obj.data.materials:
                    
                        # check if baseObj shares a mat
                        if(baseObjMat.name == objMat.name):                                
                            similarObjects.append(obj)
                            # break out of these loops
                            matchFound = True
                            break                          
                except AttributeError:
                    print("Caught an error")
                    pass
                
            print("%s mode delivered %s similar object(s)!" %(self.selectType, len(similarObjects)))
            select_list(similarObjects)
            # end logic
        elif (self.selectType == 'HIERARCHY'):
            print("similairty: Hierarchy")
            # start logic
            parentSteps = 0
            EndLoop = False
            # go to parent
            while EndLoop != True:
                print (bpy.context.active_object)
                bpy.ops.object.select_hierarchy(direction='PARENT', extend = False)
                parentSteps += 1
                if (parentSteps >= 20):
                    EndLoop = True
            for i in range(parentSteps):
                bpy.ops.object.select_hierarchy(direction='CHILD', extend = True)
            #end logic
                
        elif(self.selectType == 'OBJECTNAME'):
            similarObjects = []
            baseObject = bpy.context.active_object
            baseObjectFirstName = (baseObject.name.partition('.'))[0] # get everything before the '.' in the name
            print("similairty: Objectname %s" %(baseObjectFirstName))
            for obj in bpy.data.objects:
                objFirstName = (obj.name.partition('.'))[0] # get everything before the '.'
                if(objFirstName == baseObjectFirstName):
                    similarObjects.append(obj)
            print("%s mode delivered %s similar object(s)!" %(self.selectType, len(similarObjects)))
            select_list(similarObjects)
        else:
            raise ValueError('Unknown selectiontype argument: %s'%(self.selectType))     
        return {'FINISHED'}


class SelectSimilarMenu(bpy.types.Menu):
    """Provides options to selecting similar items"""

    bl_label = "Select similar:"
    bl_idname = "architools_selectsimilar.menu"

    def draw(self, context):
        layout = self.layout
        ## draw options
        layout.operator("archiutil_selectshared.button", "Object Type").selectType = 'OBJECTTYPE'
        layout.operator("archiutil_selectshared.button", "Linked MeshData").selectType = 'MESHDATA'
        layout.operator("archiutil_selectshared.button", "Vertex Count").selectType = 'VERTEXCOUNT'
        layout.operator("archiutil_selectshared.button", "Shared Material").selectType = 'MATERIAL'
        layout.operator("archiutil_selectshared.button", "Hierarchy").selectType = 'HIERARCHY'
        layout.operator("archiutil_selectshared.button", "Object Name").selectType = 'OBJECTNAME'


        #layout.operator("wm.save_as_mainfile")
        

def register():
        bpy.utils.register_module(__name__);
        bpy.types.Scene.archiutil_copymods_array = bpy.props.BoolProperty(name="Copy Array", description = "Setting for modifier copies", default= True)
        bpy.types.Scene.archiutil_copymods_edgesplit = bpy.props.BoolProperty(name="Copy Edge split", description = "Setting for modifier copies", default= True)
if __name__ == "__name__":
    register()
   
