bl_info = {
    "name": "Realsize Unwrap",
    "author": "Gertjan Van den BRoek",
    "version": (0, 1),
    "blender": (2, 6, 5),
    "location": "3D View, Toolbox",
    "description": "Creates an new UVmap OR updates an existing UVmap called 'UVMapWorldSize',this set of UV's is scaled to match the world size. The UV square is treated as a 1mx1m square",
    "warning": "Not 100% reliable, but 100% safe for your mesh",
    "wiki_url": "",
    "tracker_url": "",
    "support": 'TESTING',
    "category": "UV"
}

import bpy
import math
import array
import sys

from bpy.props import BoolProperty
from bpy.props import FloatVectorProperty

# Custom properties
bpy.types.Scene.realsize_forceunwrap = BoolProperty(
    name="Force Unwrap", description="Forces the script to unwrap the mesh again", default=True
)
bpy.types.Scene.realsize_materialSize = FloatVectorProperty(
    name="Material Size", description="The world dimensions of a texture (metric)", default=(1.0, 1.0),
    min=0.00001,
    max=1000000000,
    soft_min=0,
    soft_max=10000,
    step=3,
    precision=2,
    options={'SKIP_SAVE'},
    subtype='NONE',
    size=2
)

UVMapName = "UVMapWorldSize"
UVToolsObject = 0
_Debug = True

# Debug

def printIDs(meshObj):
    print('----------ID------------')
    for poly in meshObj.data.polygons:
        print(poly.vertices[0])
        print(poly.vertices[1])
        print(poly.vertices[2])
    print('----------ID------------')
    print('----------UV------------')
    for vertice in meshObj.data.uv_layers.data.vertices:
        print(vertice.index)
    print('----------UV------------')

# length of a Vector2


def VectorMagnitude2(first, last):
        # A² + B² = C²
    X = first[0] - last[0]
    Y = first[1] - last[1]
    returnVal = math.pow(X, 2) + math.pow(Y, 2)
    returnVal = math.sqrt(returnVal)
    if(_Debug):
        print("Vector2 magnitude called! Returning " + "%s" % returnVal)
    return returnVal

# length of a Vector3


def VectorMagnitude3(first, last):
        # A² + B² + C² = D²
    X = first[0] - last[0]
    Y = first[1] - last[1]
    Z = first[2] - last[2]
    returnVal = math.pow(X, 2) + math.pow(Y, 2) + math.pow(Z, 2)
    returnVal = math.sqrt(returnVal)
    if(_Debug):
        print("Vector3 magnitude called! Returning " + "%s" % returnVal)
    return returnVal

# not used, but could be usefull


def TriangleArea(x, y, z):
    sumOfSides = x + y + z
    # angleX represents the angle between side y and side z
    # The value of asine() is in radian
    # The value of angle is calculated from angle/opposite_site ratio
    angleX = math.acos((pow(y, 2) + pow(z, 2) - pow(x, 2)) * 3.14 / (360 * y * z))
    # Height of apex Y from side y
    h = z * math.sin(angleX)
    # area of triangle
    area = (y * h) / 2.0
    if(_Debug):
        print("Area of the triangle is %s" % area)
    return area

# Input: worldPoint1, WorldPoint2 , UVPoint 1, UVPoint2
# Purpose: Calculates the scaling needed to convert the UV length between UV1 and UV2 to the length between WP1 and WP2
# Output: ScaleFactor , ERROR = 0


def getEdgeScale(wPoint1, wPoint2, tPoint1, tPoint2):
    # world length
    wLength = VectorMagnitude3(wPoint1, wPoint2)
    # texcoord length
    tLength = VectorMagnitude2(tPoint1, tPoint2)

    # default scale factor = 0 = error code
    returVal = 0
    if(tLength == 0):  # if the texcoord length = 0 then the 2 points are on top of eachother =  not scaleable.
        print("Warning, texture has 0 edge length, has it been unwrapped properly?")  # prints warning
    else:
        returVal = wLength / tLength
    if(_Debug):
        print(returVal)
    return returVal

# Input: MeshData, FaceData
# Purpose: Calculates the average scalefactor of every edge in a face.
# Output: Face scalefactor, ERROR = 0


def getFaceUVScale(obj, face):

    # polygons can consists out of multiple vertices and not just 3 ( ffs )
    numVerts = len(face.vertices)

    # create containers for each vert, ' Verts ' is a refference to the vertex Id's for the other 2 lists
    Verts = [None] * numVerts
    wCoords = [None] * numVerts  # World Coordinates
    tCoords = [None] * numVerts  # Texture Coordinates

    # needs to be filled
    numEdges = numVerts
    # keep a list of every individual edge scale
    edgeScales = [None] * numVerts

    # fill arrays with data
    ArrayIndex = 0
    for i in face.loop_indices:
                # store the face Index in the faceIndexArray called Verts
        Verts[ArrayIndex] = i
        # store the position data in the wCoords and tCoords
        wCoords[ArrayIndex] = obj.data.uv_layers.data.vertices[face.vertices[ArrayIndex]].co
        tCoords[ArrayIndex] = obj.data.uv_layers[UVMapName].data[Verts[ArrayIndex]].uv

        if(_Debug):  # print debug info
            print(wCoords[ArrayIndex])
            print(tCoords[ArrayIndex])
        ArrayIndex += 1  # manually increase array index for next loop

        # get all edge scales
    for i in range(numVerts):
        thisVertArrayIndex = i
        nextVertArrayIndex = 0
        if(i < numVerts - 1):  # if i is not the end of the array
            nextVertArrayIndex = i + 1
        # get edge scale
        edgeScale = getEdgeScale(wCoords[thisVertArrayIndex], wCoords[nextVertArrayIndex], tCoords[thisVertArrayIndex], tCoords[nextVertArrayIndex])
        #
        if(_Debug):  # print debug info
            print("\t\tEdge scale: %s" % edgeScale)
            # in case I get an error, ignore that edge scale and dont count it. This way it doesnt interfere with other results.
        if(edgeScale == 0):  # error code
            numEdges = numEdges - 1
        else:
            edgeScales[i] = edgeScale

    # get average face,edge scale
    totalScale = 0
    for i in range(numVerts):
        if(edgeScales[i] != None):
            totalScale += edgeScales[i]
    scaleFactor = 1
    if(numEdges < 1):  # error code
        print("ERROR: Not a single edge has a scale. Returning scale factor 0 #ERROR")
    else:
        scaleFactor = totalScale / numEdges
    if(_Debug):
        print("\tFace scalefactor: %s" % scaleFactor)
    return scaleFactor


# Input: Mesh Data
# Purpose: To go over every face and get its individual average scale factor. Then combine it into a single number
# Output: Object's scale factor
def GetObjectUVScaleFactor(obj):

    scaleFactor = 1  # default = 1 = failsafe.
    totalScaleFactor = 0  # Sum of all face scales; divided by calculatedFaceCount in the end to get scalefactor

    faceCount = len(obj.data.polygons)
    originalFaceCount = faceCount  # actual face count
    calculatedFaceCount = faceCount  # face count after excluding badfaces
    # go over every face
    for face in obj.data.polygons:
        faceScale = getFaceUVScale(obj, face)  # attempt to get single face scale factor

        if(faceScale == 0):  # error code
            calculatedFaceCount -= 1  # exclude this face from equasion
        else:
            totalScaleFactor += faceScale  # add this scale to equasion

    if(calculatedFaceCount == 0):  # not a single face was usable
        print("ERROR: Not a single face was useable in calculations, setting scale to 1")
    else:
        scaleFactor = totalScaleFactor / calculatedFaceCount

    return scaleFactor

# Input: None
# Purpose: Iterate over every valid mesh in selection, calculate and apply a realsize UV scale
# Output: None


def DoRealWorldUnwrap():
  # check if an object is selected
    SelectedObjects = bpy.context.selected_objects
    isObjectSelected = False
    if (SelectedObjects != []):
        isObjectSelected = True
    print("Object selected = " + ("%s" % isObjectSelected))

    # if selected, iterate over each selected object
    if (isObjectSelected == True):
        for selectedObj in SelectedObjects:

            # DEBUG
            if(_Debug):
                printIDs(selectedObj)
        # select mesh
            bpy.context.scene.objects.active = selectedObj

        # -> EDIT MODE
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        # select all
            bpy.ops.mesh.select_all(action='SELECT')

        # select or add a RealSize UV map to the object
            alreadyHasCoords = False
            for uvs in selectedObj.data.uv_textures:
                if (uvs.name == UVMapName):
                    alreadyHasCoords = True
                    print("Mesh already has worldsize UV map, skipping creation")
            # check if use has decided to unwrap anyway , set hascoords to false

            if(alreadyHasCoords == False):  # if there are no UV coords yet, add a new on with given scripted name
                bpy.ops.mesh.uv_texture_add()
                bpy.context.active_object.data.uv_textures.active.name = UVMapName
                alreadyHasCoords = True

        # unwrap
            if(bpy.context.scene.realsize_forceunwrap == True):
                alreadyHasCoords = False
                bpy.ops.uv.smart_project(angle_limit=45, island_margin=0, user_area_weight=0)

        # activate image editor
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            scalefactor = GetObjectUVScaleFactor(selectedObj)
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)

            # store which area the user is looking at ( probably VIEW_3D )
            originalActiveArea = bpy.context.area.type
            bpy.context.area.type = 'IMAGE_EDITOR'  # change to Image_Editor
            # coulddo: delete existing texture of mesh.
            bpy.ops.uv.select_all(action='SELECT')

            # scaling the UV
            print("resizing UV scale to " + "%s" % scalefactor)
            bpy.ops.transform.resize(value=(scalefactor, scalefactor, scalefactor), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=False)

       # back to original area type (probably 3D view though )
            bpy.context.area.type = originalActiveArea
       # exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
       # done
    print("Script ended!")


def Do_SetMaterialSize():
    print("Setting Material Size")
    # get selected material
    mat = bpy.context.object.active_material
    if(mat == None):
        print("Object has no materials set, ending!")
        return {'FAILED'}
    # iterate textures
    for texSlot in mat.texture_slots:
        if(texSlot != None):
            # calc scale
            texScale = [0] * 2
            texScale[0] = 1 / bpy.context.scene.realsize_materialSize[0]
            texScale[1] = 1 / bpy.context.scene.realsize_materialSize[1]
            print("\tFound: " + texSlot.name + " scaling to x: %s, y: %s" % (texScale[0], texScale[1]))

            texSlot.texture_coords = 'UV'  # set to UV mapping mode
            texSlot.scale[0] = texScale[0]  # set scale X
            texSlot.scale[1] = texScale[1]  # set scale Y
            texSlot.uv_layer = UVMapName  # set UV to realsize UV
    # done
    print("Script Ended!")


class UVTOOLSPanel(bpy.types.Panel):
    "Creates a Panel in the viewport toolbox"
    bl_label = "UV Tools"
    bl_idname = "object_ot_uvtools.dorealsizeunwrap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        sce = context.scene

        layout.prop(sce, "realsize_forceunwrap")
        layout.operator("real_size.button")

        layout.prop(sce, "realsize_materialSize")
        layout.operator("real_size.set_material_size")
        layout.label("v0.1")


class OBJECT_OT_RealsizeSetMaterialSize(bpy.types.Operator):
    bl_idname = "real_size.set_material_size"
    bl_label = "Set Material Size"
    bl_description = "Sets all textures in the material to a given scale using formule : size = 1 / givenscale"

    def execute(self, context):
        Do_SetMaterialSize()
        return {'FINISHED'}


class OBJECT_OT_RealsizeButton(bpy.types.Operator):
    bl_idname = "real_size.button"
    bl_label = "Scale UV to world size"
    bl_description = "Scales model UVs to world size"

    def execute(self, context):
        DoRealWorldUnwrap()
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)
#    bpy.utils.register_class(UVTOOLSPanel)


def unregister():
    bpy.utils.unregister_module(__name__)
#    bpy.utils.unregister_class(UVTOOLSPanel)


if __name__ == "__main__":
    register()
