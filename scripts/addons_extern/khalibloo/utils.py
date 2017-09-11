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

from bpy_extras.io_utils import ImportHelper, ExportHelper, path_reference_mode
from bpy.props import StringProperty, BoolProperty, EnumProperty


#============================================================================
# DEFINE FUNCTIONS
#============================================================================


def isShapeKeyType(obj):
    if ((obj.type == 'MESH') or (obj.type == 'CURVE') or (obj.type == 'SURFACE')):
        return True
    else:
        return False

def isMaterialType(obj):
    if ((obj.type == 'MESH') or
        (obj.type == 'CURVE') or
        (obj.type == 'SURFACE') or
        (obj.type == 'FONT') or
        (obj.type == 'META')):
        return True
    else:
        return False

def isModifierType(obj):
    if ((obj.type == 'MESH') or
        (obj.type == 'CURVE') or
        (obj.type == 'SURFACE') or
        (obj.type == 'FONT') or
        (obj.type == 'LATTICE')):
        return True
    else:
        return False

def toonify(mat):
    mat.diffuse_shader = 'TOON'
    mat.diffuse_intensity = 1
    mat.diffuse_toon_size = 1.3
    mat.diffuse_toon_smooth = 0.03
    mat.specular_shader = 'TOON'
    mat.specular_toon_size = 0.1
    mat.specular_toon_smooth = 0.03

def copyAllShapeKeys(sourceObject, targetObject):
    shapeKeyIndex = 1
    totalShapeKeyCount = len(sourceObject.data.shape_keys.key_blocks.items())
    while (shapeKeyIndex < totalShapeKeyCount):
        copyShapeKey(shapeKeyIndex, sourceObject, targetObject)
        shapeKeyIndex = shapeKeyIndex + 1

def copyShapeKey(shapeKeyIndex, sourceObject, targetObject):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = sourceObject
    bpy.context.active_object.active_shape_key_index = shapeKeyIndex
    bpy.context.scene.objects.active = targetObject
    bpy.ops.object.shape_key_transfer()

def updateShrinkwrap(context, obj):
    #safety checks
    if (len(obj.modifiers) == 0):
        return 'CANCELLED'

    modeBackup = context.object.mode
    viewShrinkwraps = []
    renderShrinkwraps = []
    disabledShrinkwraps = []
    for mod in obj.modifiers:
        #list all shrinkwrap modifiers
        if (mod.type == 'SHRINKWRAP'):
            if (mod.show_viewport):
                viewShrinkwraps.append(mod)
            elif (mod.show_render):
                renderShrinkwraps.append(mod)
            else:
                disabledShrinkwraps.append(mod)
    #safety check
    if (len(viewShrinkwraps) + len(renderShrinkwraps) + len(disabledShrinkwraps) == 0):
        return 'CANCELLED'
    #choose
    if (len(viewShrinkwraps) > 0):
        modifier = viewShrinkwraps[0]
    elif (len(renderShrinkwraps) > 0):
        modifier = viewShrinkwraps[0]
    elif (len(disabledShrinkwraps) > 0):
        modifier = viewShrinkwraps[0]
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.modifier_copy(modifier = modifier.name)
    bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = modifier.name)
    bpy.ops.object.mode_set(mode = modeBackup)
    return 'FINISHED'

def bindMesh(context, activeObj, selectedObj, file):
    #security data
    context.scene.objects.active = selectedObj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.data.meshes[selectedObj.data.name])
    vCount = str(len(bm.verts))
    eCount = str(len(bm.edges))
    fCount = str(len(bm.faces))
    bpy.ops.object.mode_set(mode='OBJECT')
    file.write(vCount + " " + eCount + " " + fCount + "\n")
    context.scene.objects.active = activeObj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.data.meshes[activeObj.data.name])
    vCount = str(len(bm.verts))
    eCount = str(len(bm.edges))
    fCount = str(len(bm.faces))
    bpy.ops.object.mode_set(mode='OBJECT')
    file.write(vCount + " " + eCount + " " + fCount + "\n")

    context.scene.objects.active = selectedObj
    for vert in activeObj.data.vertices :
            location, normal, faceIndex = selectedObj.closest_point_on_mesh(vert.co)
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(bpy.data.meshes[selectedObj.data.name])
            vertList = []
            bm.faces.ensure_lookup_table()
            for v in bm.faces[faceIndex].verts:
                vertList.append(v.index)
            #center = bm.faces[index].calc_center_bounds()
            center = selectedObj.matrix_world * bm.faces[faceIndex].calc_center_median()
            #print(str(center))
            bpy.ops.object.mode_set(mode='OBJECT')
            delta = (activeObj.matrix_world * vert.co) - center

            output = ""
            for v in vertList:
                output = output + str(v) + " "
            output = str(vert.index) + " " + str(delta.x) + " " + str(delta.y) + " " + str(delta.z) + " " + output + "\n"
            file.write(output)
    file.close()

def updateBoundMesh(context, activeObj, selectedObj, filepath):
    f = open(filepath, 'r', encoding="utf-8")
    f.seek(0, 0) #set cursor to beginning of file
    #check if this file is compatible with the selected models
    line = f.readline()
    data = line.split()
    context.scene.objects.active = selectedObj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.data.meshes[selectedObj.data.name])
    vCount = len(bm.verts)
    eCount = len(bm.edges)
    fCount = len(bm.faces)
    bpy.ops.object.mode_set(mode='OBJECT')
    if ((vCount != int(data[0])) or (eCount != int(data[1])) or (fCount != int(data[2]))):
        raise RuntimeError("Reference object data doesn't match the data in the .txt file")
        #self.report({'ERROR'}, "Reference object data doesn't match the data in the .txt file")
    line = f.readline()
    data = line.split()
    context.scene.objects.active = activeObj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.data.meshes[activeObj.data.name])
    vCount = len(bm.verts)
    eCount = len(bm.edges)
    fCount = len(bm.faces)
    bpy.ops.object.mode_set(mode='OBJECT')
    if ((vCount != int(data[0])) or (eCount != int(data[1])) or (fCount != int(data[2]))):
        raise RuntimeError("Active object data doesn't match the data in the .txt file")
        #self.report({'ERROR'}, "Active object data doesn't match the data in the .txt file")
    #duplicate activeObj
    selectedObj.select = False
    bpy.ops.object.duplicate()
    dupliObj = context.active_object
    #bpy.ops.object.shape_key_remove(all=True)
    selectedObj.select = True
    context.scene.objects.active = selectedObj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(selectedObj.data)
    delta = dupliObj.location #just to initialize as Vector3
    vertCount = len(dupliObj.data.vertices)
    for i in range(0, vertCount) :
        line = f.readline()
        data = line.split()
        vertCount = len(data) - 4
        #data[0] is just there for human readability. it's useless here.
        delta.x = float(data[1])
        delta.y = float(data[2])
        delta.z = float(data[3])
        vertList = []
        bm.verts.ensure_lookup_table()
        for v in range(4, len(data)):
            vertList.append(bm.verts[int(data[v])])
        face = bm.faces.get(vertList) #Returns None if no face found
        if (face == None):
            raise RuntimeError("Faces in Active and Reference meshes do not match")
        center = selectedObj.matrix_world * face.calc_center_median()
        dupliObj.data.vertices[i].co = dupliObj.matrix_world.inverted() * (center + delta)
    f.close()
    bpy.ops.object.mode_set(mode='OBJECT')
    context.scene.objects.active = activeObj
    selectedObj.select = False
    bpy.ops.object.join_shapes()
    context.scene.objects.active = dupliObj
    activeObj.select = False
    bpy.ops.object.delete()
    selectedObj.select = True
    activeObj.select = True
    context.scene.objects.active = activeObj
    activeObj.data.shape_keys.key_blocks[-1].name = "khalibloo_mesh_bind"
    activeObj.data.shape_keys.key_blocks[-1].value = 1.0


#----------------------------------------------------------

def hardenWeights(obj, vgroupName, spread_vgroups):
    vgroupHard = obj.vertex_groups[vgroupName]
    hardList = []
    vertCount = len(obj.data.vertices.items())
    vertCheckList = []
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.data.meshes[obj.data.name])
    bpy.ops.mesh.select_all(action='DESELECT')
    obj.vertex_groups.active_index = vgroupHard.index
    bpy.ops.object.vertex_group_select()
    bpy.context.scene.tool_settings.vertex_group_weight = 1
    for i in range(0, vertCount):
        if (bm.verts[i].select == True):
            hardList.append(i)
    bpy.ops.mesh.hide(unselected = True)
    bpy.ops.mesh.select_all(action='DESELECT')
    for i in range(0, vertCount):
        vert = bm.verts[i]
        if ((vert.index in hardList) and (vert.index not in vertCheckList)):
            vert.select = True
            bpy.ops.mesh.select_linked(limit = False)
            connectedVertList = []
            for i in range(0, vertCount):
                if (bm.verts[i].select == True):
                    connectedVertList.append(i)
            print("connected: " + str(connectedVertList))
            vgroupList = massFindVgroups(obj, connectedVertList)
            for vgroup in vgroupList:
                averageWeight = findAverageWeight(obj, vgroup.name, connectedVertList)
                print ("average = " + str(averageWeight))
                bpy.context.scene.tool_settings.vertex_group_weight = averageWeight
                if (spread_vgroups == False):
                    bpy.ops.mesh.select_all(action='DESELECT')
                    obj.vertex_groups.active_index = vgroup.index
                    bpy.ops.object.vertex_group_select()
                for i in range(0, vertCount):
                    if (bm.verts[i].select == True):
                        if (i not in connectedVertList):
                            bm.verts[i].select = False
                bpy.ops.object.vertex_group_assign()
                #for i in range(0, vertCount):
                    #if (bm.verts[i].select == True):
                        #vertCheckList.append(i)
                bpy.ops.mesh.reveal()
                bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

def findAverageWeight(obj, vgroupName, vertList):
    vgroup = obj.vertex_groups[vgroupName]
    vgroupContent = findVertices(obj, vgroupName)
    weightList = []
    for v in vertList:
        if (v in vgroupContent):
            weight = vgroup.weight(v)
            if (vgroup.weight(v) > 0):
                weightList.append(weight)
        else:
            weightList.append(0)
    averageWeight = sum(weightList) / len(weightList)
    return averageWeight

def massFindVgroups(obj, vertList):
    vgroupList = []
    vgroupCount = len(obj.vertex_groups.keys())
    for i in range(0, vgroupCount):
        vgroup = obj.vertex_groups[i]
        vgroupContent = findVertices(obj, vgroup.name)
        for v in vertList:
            if ((v in vgroupContent) and (vgroup.weight(v) > 0)):
                if (vgroup not in vgroupList):
                    vgroupList.append(vgroup)
    return vgroupList

def findVertices(obj, vgroupName):
    vertList = []
    vgroup = obj.vertex_groups[vgroupName]
    vertCount = len(obj.data.vertices.items())
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.data.meshes[obj.data.name])
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='DESELECT')
    obj.vertex_groups.active_index = vgroup.index
    bpy.ops.object.vertex_group_select()
    for v in range (0, vertCount):
        if (bm.verts[v].select == True):
            vertList.append(v)
    return vertList


def findVgroups(obj, vIndex):
    vgroupList = []
    vgroupCount = len(obj.vertex_groups.keys())
    for i in range(0, vgroupCount):
        vgroup = obj.vertex_groups[i]
        if (vgroup.weight(vIndex) > 0):
            vgroupList.append(vgroup)
    return vgroupList

def createVgroup(obj, bm, vgroupName, vertList):
    bpy.ops.mesh.select_all(action='DESELECT')
    bm.verts.ensure_lookup_table()
    for v in vertList:
        bm.verts[v].select = True
    bpy.ops.object.vertex_group_add()
    obj.vertex_groups.active.name = vgroupName
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action='DESELECT')

def delVgroup(obj, vgroupName):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = obj
    vgroupIndex = obj.vertex_groups[vgroupName].index
    bpy.context.active_object.vertex_groups.active_index = vgroupIndex
    bpy.ops.object.vertex_group_remove()

def findLayer(obj):
    for i in range(0, 20):
        if obj.layers[i]:
            return i

def hideSelect():
    for obj in bpy.context.selected_objects:
        obj.hide_select = True

def unhideSelect():
    for obj in bpy.context.scene.objects:
        obj.hide_select = False

def hideRender():
    for obj in bpy.context.selected_objects:
        obj.hide_render = True

def unhideRender():
    for obj in bpy.context.selected_objects:
        obj.hide_render = False

def moveToJunk(obj):
    obj.layers = [False] * 19 + [True]

#------------------------------------------------------------------

def isNameExtension(refName, checkName):
    numerals = "0123456789"
    lenRefName = len(refName)
    lenCheckName = len(checkName)
    if (lenRefName - lenCheckName == 4):
        if (refName[lenCheckName] == "."):
            if (refName[lenCheckName + 1] in numerals):
                if (refName[lenCheckName + 2] in numerals):
                    if (refName[lenCheckName + 3] in numerals):
                        #print("It's a name extension")
                        return True
    #print("It's not a name extension")
    return False

def assignMatIndices():
    i = 1
    for j in range(0, len(bpy.data.materials)):
        bpy.data.materials[j].pass_index = i
        i += 1

def assignObjIndices(context):
    i = 1
    for obj in context.selected_objects:
        obj.pass_index = i
        i += 1

def setupImportedMaterials(context, obj):
    for matslot in obj.material_slots:
        if (matslot.material is not None):
            mat = matslot.material
            mat.diffuse_intensity = 1.0
            mat.specular_intensity = 0.0
            mat.use_transparent_shadows = True
            for texslot in mat.texture_slots:
                if (texslot is not None):
                    #spec
                    if (texslot.use_map_specular):
                        texslot.use_rgb_to_intensity = True
                    #bump
                    elif (texslot.use_map_normal):
                        texslot.texture.use_normal_map = True

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

def updateImages():
    return bpy.data.images.keys()

#----------------------------------------------------------------------------

def modifiersRealTimeOff(obj, modFilter = 'ALL', modType = 'SUBSURF'):
    modList = obj.modifiers
    if (len(modList) > 0):
        bpy.context.scene.objects.active = obj
        for mod in modList:
            if (modFilter == 'ALL'):
                mod.show_viewport = False
            else: #modFilter is 'SPECIFIC'
                if (mod.type == modType):
                    mod.show_viewport = False

def modifiersRealTimeOn(obj, modFilter = 'ALL', modType = 'SUBSURF'):
    modList = obj.modifiers
    if (len(modList) > 0):
        bpy.context.scene.objects.active = obj
        for mod in modList:
            if (modFilter == 'ALL'):
                mod.show_viewport = True
            else: #modFilter is 'SPECIFIC'
                if (mod.type == modType):
                    mod.show_viewport = True

def modifiersRenderOff(obj, modFilter = 'ALL', modType = 'SUBSURF'):
    modList = obj.modifiers
    if (len(modList) > 0):
        bpy.context.scene.objects.active = obj
        for mod in modList:
            if (modFilter == 'ALL'):
                mod.show_render = False
            else: #modFilter is 'SPECIFIC'
                if (mod.type == modType):
                    mod.show_render = False

def modifiersRenderOn(obj, modFilter = 'ALL', modType = 'SUBSURF'):
    modList = obj.modifiers
    if (len(modList) > 0):
        bpy.context.scene.objects.active = obj
        for mod in modList:
            if (modFilter == 'ALL'):
                mod.show_render = True
            else: #modFilter is 'SPECIFIC'
                if (mod.type == modType):
                    mod.show_render = True

def modifiersEditModeOff(obj, modFilter = 'ALL', modType = 'SUBSURF'):
    modList = obj.modifiers
    if (len(modList) > 0):
        bpy.context.scene.objects.active = obj
        for mod in modList:
            if (modFilter == 'ALL'):
                mod.show_in_edit_mode = False
            else: #modFilter is 'SPECIFIC'
                if (mod.type == modType):
                    mod.show_in_edit_mode = False

def modifiersEditModeOn(obj, modFilter = 'ALL', modType = 'SUBSURF'):
    modList = obj.modifiers
    if (len(modList) > 0):
        bpy.context.scene.objects.active = obj
        for mod in modList:
            if (modFilter == 'ALL'):
                mod.show_in_edit_mode = True
            else: #modFilter is 'SPECIFIC'
                if (mod.type == modType):
                    mod.show_in_edit_mode = True

def modifiersApply(obj, modFilter = 'ALL', modType = 'SUBSURF'):
    modList = obj.modifiers
    if (len(modList) > 0):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.scene.objects.active = obj
        i = 0
        while (i < len(modList)):
            if (modFilter == 'ALL'):
                bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = modList[i].name)
                #del modList[i]
            else: #modFilter is 'SPECIFIC'
                if (modList[i].type == modType):
                    bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = modList[i].name)
                else:
                    i += 1

def modifiersRemove(obj, modFilter = 'ALL', modType = 'SUBSURF'):
    modList = obj.modifiers
    if (len(modList) > 0):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = obj
        for mod in modList:
            if (modFilter == 'ALL'):
                bpy.ops.object.modifier_remove(modifier = mod.name)
            else: #modFilter is 'SPECIFIC'
                if (mod.type == modType):
                    bpy.ops.object.modifier_remove(modifier = mod.name)


#--------------------------------------------------------------------------------

def muteConstraints(obj):
    if (len(obj.constraints) > 0):
        for con in obj.constraints:
            con.mute = True

def unmuteConstraints(obj):
    if (len(obj.constraints) > 0):
        for con in obj.constraints:
            con.mute = False

def removeConstraints(obj):
    bpy.context.scene.objects.active = obj
    if (len(obj.constraints) > 0):
        bpy.ops.object.constraints_clear()


#-----------------------------------------------------------------------------------

def startMultiEdit(context):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    selectionList = context.selected_objects
    copiesList = []
    bpy.ops.object.select_all(action = 'DESELECT')
    for obj in selectionList:
        if (obj.type == 'MESH'):
            context.scene.objects.active = obj
            obj.select = True
            #assign all verts to a vgroup containing object name
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.reveal()
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.object.vertex_group_add()
            obj.vertex_groups[-1].name = "khalibloo_multiedit_" + obj.name
            bpy.ops.object.vertex_group_assign()
            bpy.ops.object.mode_set(mode = 'OBJECT')
            #store vertex indices as vertex groups
            #bpy.ops.object.mode_set(mode = 'EDIT')
            #bpy.ops.mesh.select_all(action = 'DESELECT')
            #bm = bmesh.from_edit_mesh(bpy.data.meshes[obj.data.name])
            #vcount = len(obj.data.vertices)
            #for i in range(0, vcount):
                #bm.verts[i].select = True
                #bpy.ops.object.vertex_group_add()
                #obj.vertex_groups[-1].name = "khalibloo_multiedit_" + obj.name + "_" + str(i)
                #bpy.ops.object.vertex_group_assign()
                #bm.verts[i].select = False
            #bpy.ops.object.mode_set(mode = 'OBJECT')
            #duplicate object
            bpy.ops.object.duplicate()
            copy = context.active_object
            copiesList.append(copy)
            #hide original
            obj.select = False
            copy.select = False
            #label object as original
            obj["khalibloo_multiedit"] = "original"
            #move to junk layer
            obj["khalibloo_multiedit_original_layers"] = obj.layers
            moveToJunk(obj)
            obj.hide = True
        else:
            selectionList.remove(obj)
    beginMultiEdit(selectionList, copiesList)

def beginMultiEdit(selectionList, copiesList):
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.object.add(type = 'MESH')
    multiEditObj = bpy.context.active_object
    for copy in copiesList:
        copy.select = True
    bpy.ops.object.join()
    multiEditObj.name = "khalibloo_multiedit_object"
    multiEditObj["khalibloo_multiedit"] = "multi object"
    bpy.ops.object.khalibloo_modifiers_remove()
    bpy.ops.object.khalibloo_constraints_remove()
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    originalsNameList = []
    for originalObj in selectionList:
        originalsNameList.append(originalObj.name)
    multiEditObj["khalibloo_multiedit_originalsNameList"] = originalsNameList
    bpy.ops.object.mode_set(mode = 'EDIT')

def endMultiEdit(multiEditObj):
    #get a list of the originals
    originalsList = multiEditObj["khalibloo_multiedit_originalsNameList"]
    del multiEditObj["khalibloo_multiedit"]
    del multiEditObj["khalibloo_multiedit_originalsNameList"]
    multiEditObj.name = "khalibloo_multiedit_residue"
    #deselect all objects and select only the multiEditObj, set as active
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.context.scene.objects.active = multiEditObj
    multiEditObj.select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.from_edit_mesh(bpy.data.meshes[multiEditObj.data.name])
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    print ("checkpoint 01")
    for originalObjName in originalsList:
        #select all vgroups starting with khalibloo_multiedit_originalName
        for vgroup in multiEditObj.vertex_groups:
            if vgroup.name.startswith("khalibloo_multiedit_" + originalObjName):
                bpy.ops.object.vertex_group_set_active(group = vgroup.name)
                bpy.ops.object.vertex_group_select()
        #if selection size > 0
        #separate selection from the multiEditObj
        vcount = countSelectedVerts(bm)
        if (vcount > 0):
            bpy.ops.mesh.separate(type = 'SELECTED')
            print ("checkpoint 02")
    #if no vertices remain in multiEditObj
    bpy.ops.object.mode_set(mode = 'OBJECT')
    print(str(len(multiEditObj.data.vertices)))
    if (len(multiEditObj.data.vertices) == 0):
        #mark multiEditObj for deletion
        multiEditObj["khalibloo_multiedit_marked_for_deletion"] = True
    else:
        multiEditObj["khalibloo_multiedit_marked_for_deletion"] = False
    #get list of separated objects
    newObjsList = bpy.context.selected_objects
    newObjsList.remove(multiEditObj)
    for newObj in newObjsList:
        bpy.context.scene.objects.active = newObj
        bpy.ops.object.mode_set(mode = 'EDIT')
        bm = bmesh.from_edit_mesh(bpy.data.meshes[newObj.data.name])
        bpy.ops.mesh.select_all(action = 'DESELECT')
        for vgroup in newObj.vertex_groups:
            #delete empty khalibloo_multiedit vgroups
            #bpy.ops.object.mode_set(mode='EDIT')
            if vgroup.name.startswith("khalibloo_multiedit_"):
                bpy.ops.object.vertex_group_set_active(group = vgroup.name)
                bpy.ops.object.vertex_group_select()
                vcount = countSelectedVerts(bm)
                if (vcount == 0):
                    bpy.ops.object.vertex_group_remove(all = False)
                else:
                    bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        greenlight = False
        for vgroup in newObj.vertex_groups:
            #retrieve original name from remaining vgroup
            if (vgroup.name.startswith("khalibloo_multiedit_")):
                originalName = retrieveMultiEditName(vgroup.name)
                if (originalName is not None and originalName in bpy.data.objects.keys()):
                    originalObj = bpy.data.objects[originalName]
                    greenlight = True
                    break
        #if greenlight == False, skip this iteration
        if (greenlight == False):
            #print warning! the original object has been renamed or deleted
            continue
        originalObj.hide = False
        #if originalObj has shape keys
        if (originalObj.data.shape_keys is not None):
            #if we have matching indices, join as shapes
            if (compareMeshes(bpy.data.meshes[newObj.data.name], bpy.data.meshes[originalObj.data.name])):
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.select_all(action = 'DESELECT')
                originalObj.layers = intsToBools(originalObj["khalibloo_multiedit_original_layers"])
                del originalObj["khalibloo_multiedit_original_layers"]
                bpy.context.scene.objects.active = originalObj
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action = 'DESELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.shape_key_add(from_mix = False)
                originalObj.data.shape_keys.key_blocks[-1].name = "khalibloo_multiedit"
                bpy.context.scene.objects.active = newObj
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action = 'DESELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                for i in range(0, len(originalObj.data.vertices)):
                    bpy.context.scene.objects.active = newObj
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bm = bmesh.from_edit_mesh(bpy.data.meshes[newObj.data.name])
                    bm.verts.ensure_lookup_table()
                    bm.verts[i].select = True
                    bpy.ops.view3d.snap_cursor_to_selected()
                    bm.verts[i].select = False
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.context.scene.objects.active = originalObj
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bm = bmesh.from_edit_mesh(bpy.data.meshes[originalObj.data.name])
                    bm.verts.ensure_lookup_table()
                    bm.verts[i].select = True
                    bpy.ops.view3d.snap_selected_to_cursor()
                    bm.verts[i].select = False
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                #delete new object
                bpy.ops.object.select_all(action = 'DESELECT')
                bpy.context.scene.objects.active = newObj
                newObj.select = True
                bpy.ops.object.delete()
        #if originalObj has no shape keys
        else:
            #if newObj has shape keys, something weird happens here... you gotta fix it
            #TOFIX

            #delete all verts from original
            originalObj.layers = intsToBools(originalObj["khalibloo_multiedit_original_layers"])
            del originalObj["khalibloo_multiedit_original_layers"]
            bpy.context.scene.objects.active = originalObj
            originalObj.select = True
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.reveal()
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.delete(type = 'VERT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            #join new with original
            bpy.ops.object.select_all(action = 'DESELECT')
            newObj.select = True
            originalObj.select = True
            bpy.context.scene.objects.active = originalObj
            bpy.ops.object.join()
        #clear khalibloo_multiedit vgroups and custom properties
        originalObj.select = True
        bpy.context.scene.objects.active = originalObj
        for vgroup in originalObj.vertex_groups:
            if (vgroup.name.startswith("khalibloo_multiedit_")):
                bpy.ops.object.vertex_group_set_active(group = vgroup.name)
                bpy.ops.object.vertex_group_remove()
        del originalObj["khalibloo_multiedit"]
    #if multiEditObj has been marked for deletion, delete it
    if (multiEditObj["khalibloo_multiedit_marked_for_deletion"]):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action = 'DESELECT')
        multiEditObj.select = True
        bpy.context.scene.objects.active = multiEditObj
        bpy.ops.object.delete()
    else:
        #clear khalibloo_multiedit vgroups and custom properties
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action = 'DESELECT')
        bpy.context.scene.objects.active = multiEditObj
        multiEditObj.select = True
        for vgroup in multiEditObj.vertex_groups:
            if (vgroup.name.startswith("khalibloo_multiedit_")):
                bpy.ops.object.vertex_group_set_active(group = vgroup.name)
                bpy.ops.object.vertex_group_remove()
        del multiEditObj["khalibloo_multiedit_marked_for_deletion"]

def intsToBools(intsList):
    boolsList = []
    for i in range(0, len(intsList)):
        if (intsList[i] == 0):
            boolsList.append(False)
        else:
            boolsList.append(True)
    print(str(boolsList))
    return boolsList

def retrieveMultiEditName (name):
    if name.startswith("khalibloo_multiedit_"):
        name = name[20:]
        #name = name[:name.rfind("_")]
        return name
    else:
        return None

def countSelectedVerts(bm):
    vcount = 0
    bm.verts.ensure_lookup_table()
    for vert in bm.verts:
        if (vert.select == True):
            vcount += 1
    return vcount

def compareMeshes(mesh1, mesh2):
    bmesh1 = bmesh.new()
    bmesh1.from_mesh(mesh1)
    bmesh2 = bmesh.new()
    bmesh2.from_mesh(mesh2)
    if (len(bmesh1.verts) != len(bmesh2.verts)):
        return False
    if (len(bmesh1.edges) != len(bmesh2.edges)):
        return False
    if (len(bmesh1.faces) != len(bmesh2.faces)):
        return False
    #for each face, if the same verts make up the face
    for i in range(0, len(bmesh1.faces)):
        bmesh1faceVertsList = []
        bmesh2faceVertsList = []
        bmesh1.faces.ensure_lookup_table()
        for vert in bmesh1.faces[i].verts:
            bmesh1faceVertsList.append(vert.index)
        bmesh2.faces.ensure_lookup_table()
        for vert in bmesh2.faces[i].verts:
            bmesh2faceVertsList.append(vert.index)
        bmesh1faceVertsList.sort()
        bmesh2faceVertsList.sort()
        if (bmesh1faceVertsList != bmesh2faceVertsList):
            return False
    #for each edge, if the same verts make up the edge
    for i in range(0, len(bmesh1.edges)):
        bmesh1edgeVertsList = []
        bmesh2edgeVertsList = []
        bmesh1.edges.ensure_lookup_table()
        for vert in bmesh1.edges[i].verts:
            bmesh1faceVertsList.append(vert.index)
        bmesh2.edges.ensure_lookup_table()
        for vert in bmesh2.edges[i].verts:
            bmesh2faceVertsList.append(vert.index)
        bmesh1edgeVertsList.sort()
        bmesh2edgeVertsList.sort()
        if (bmesh1edgeVertsList != bmesh2edgeVertsList):
            return False
    #if we make it through all the checks, we have a match!
    return True


#============================================================================
# DEFINE OPERATORS
#============================================================================

class NameObjectData (bpy.types.Operator):
    """Names object data for all objects"""
    bl_idname = "object.khalibloo_name_object_data"
    bl_label = "Name Object Data"

    @classmethod
    def poll(cls, context):
        return len(bpy.data.objects) > 0

    def execute(self, context):
        for obj in bpy.data.objects:
            try:
                obj.data.name = obj.name
            except(AttributeError):
                pass
        return{'FINISHED'}

class CopyAllShapeKeys(bpy.types.Operator):
    """Copies all shape keys of selected object(s) to active object"""
    bl_idname = "object.khalibloo_copy_all_shape_keys"
    bl_label = "Copy All Shape Keys"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (len(context.selected_objects) > 1))

    def execute(self, context):
        if (isShapeKeyType(context.active_object)):
            targetObject = bpy.context.active_object
            targetObjectIndex = bpy.context.selected_objects.index(bpy.context.active_object)
            selectionList = bpy.context.selected_objects
            del selectionList[targetObjectIndex]
            selectionSize = len(selectionList)
            currentObjectIndex = 0

            #to avoid problems with active object not having shape keys initially
            bpy.ops.object.shape_key_add(from_mix=False)
            shapeKeysCount = len(targetObject.data.shape_keys.key_blocks)

            #but if it already had a shape key, delete the one just created
            if (shapeKeysCount > 1):
                bpy.ops.object.shape_key_remove()

            while (currentObjectIndex < selectionSize):
                sourceObject = selectionList[currentObjectIndex]
                bpy.ops.object.select_all(action='DESELECT')
                sourceObject.select = True
                bpy.context.active_object.select = True
                copyAllShapeKeys(sourceObject, targetObject)
                currentObjectIndex = currentObjectIndex + 1

        return {'FINISHED'}


class ShrinkwrapUpdate (bpy.types.Operator):
    """Updates geometry to match shrinkwrap modifier data"""
    bl_idname = "object.khalibloo_shrinkwrap_update"
    bl_label = "Update Shrinkwrap"

    @classmethod
    def poll(cls, context):
        return len(context.active_object.modifiers) > 0

    def execute(self, context):
        obj = context.active_object
        result = updateShrinkwrap(context, obj)
        return{result}


class HardenWeights(bpy.types.Operator):
    """Harden the weights of the vertex groups of the selected objects."""
    bl_idname = "object.khalibloo_harden_weights"
    bl_label = "Harden Weights"

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None)

    def execute(self, context):
        spread_vgroups = bpy.context.scene.khalibloo_spread_harden_vgroups
        objBackup = bpy.context.active_object
        for obj in bpy.context.selected_objects:
            hardenWeights(obj, "khalibloo_hard", spread_vgroups)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}


class ReceiveTransparentShadows(bpy.types.Operator):
    """Sets all materials of the selected object(s) to receive transparent shadows"""
    bl_idname = "object.khalibloo_receive_transparent_shadows"
    bl_label = "Receive Transparent"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if (len(obj.material_slots.keys()) > 0):
                for matSlot in obj.material_slots:
                    matSlot.material.use_transparent_shadows = True
        return {'FINISHED'}


class RigifyNeckFix(bpy.types.Operator):
    """Fixes a rare condition where the rigify rig's neck bone is a lot larger than it should be"""
    bl_idname = "object.khalibloo_rigify_neck_fix"
    bl_label = "Rigify Neck Fix"

    @classmethod
    def poll(cls, context):
        return ((context.active_object is not None) and (context.active_object.type == 'ARMATURE'))



    def execute(self, context):
        rig = bpy.context.active_object
        neck = rig.pose.bones["neck"].custom_shape
        bpy.context.scene.layers[findLayer(neck)] = True
        neck.hide = False
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = neck
        neck.select = True
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
        bpy.context.object.scale[0] = 0.390
        bpy.context.object.scale[1] = 0.390
        bpy.context.object.scale[2] = 0.390
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.ops.transform.resize(value=(0.2442, 0.2442, 0.2442), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = rig

        return{'FINISHED'}

class ModifiersRealTimeOn(bpy.types.Operator):
    """Turn on real time display of modifiers of the selected objects"""
    bl_idname = "object.khalibloo_modifiers_realtime_on"
    bl_label = "Real Time Display On"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode
        mod_type = bpy.context.scene.khalibloo_modifier_type

        for obj in bpy.context.selected_objects:
            modifiersRealTimeOn(obj, mod_filter_mode, mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ModifiersRealTimeOff(bpy.types.Operator):
    """Turn off real time display of modifiers of the selected objects"""
    bl_idname = "object.khalibloo_modifiers_realtime_off"
    bl_label = "Real Time Display Off"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode
        mod_type = bpy.context.scene.khalibloo_modifier_type

        for obj in bpy.context.selected_objects:
            modifiersRealTimeOff(obj, mod_filter_mode, mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ModifiersRenderOn(bpy.types.Operator):
    """Turn on modifiers of the selected objects during rendering"""
    bl_idname = "object.khalibloo_modifiers_render_on"
    bl_label = "Render Display On"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode
        mod_type = bpy.context.scene.khalibloo_modifier_type

        for obj in bpy.context.selected_objects:
            modifiersRenderOn(obj, mod_filter_mode, mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ModifiersRenderOff(bpy.types.Operator):
    """Turn off modifiers of the selected objects during rendering"""
    bl_idname = "object.khalibloo_modifiers_render_off"
    bl_label = "Render Display Off"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode
        mod_type = bpy.context.scene.khalibloo_modifier_type

        for obj in bpy.context.selected_objects:
            modifiersRenderOff(obj, mod_filter_mode, mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ModifiersEditModeOn(bpy.types.Operator):
    """Turn on edit mode display of modifiers of the selected objects"""
    bl_idname = "object.khalibloo_modifiers_editmode_on"
    bl_label = "Edit Mode Display On"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode
        mod_type = bpy.context.scene.khalibloo_modifier_type

        for obj in bpy.context.selected_objects:
            modifiersEditModeOn(obj, mod_filter_mode, mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ModifiersEditModeOff(bpy.types.Operator):
    """Turn off edit mode display of modifiers of the selected objects"""
    bl_idname = "object.khalibloo_modifiers_editmode_off"
    bl_label = "Edit Mode Display Off"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode
        mod_type = bpy.context.scene.khalibloo_modifier_type

        for obj in bpy.context.selected_objects:
            modifiersEditModeOff(obj, mod_filter_mode, mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ModifiersApply(bpy.types.Operator):
    """Apply all modifiers of the selected objects in order"""
    bl_idname = "object.khalibloo_modifiers_apply"
    bl_label = "Apply"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode
        mod_type = bpy.context.scene.khalibloo_modifier_type

        for obj in bpy.context.selected_objects:
            modifiersApply(obj, mod_filter_mode, mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ModifiersRemove(bpy.types.Operator):
    """Delete all modifiers of the selected objects"""
    bl_idname = "object.khalibloo_modifiers_remove"
    bl_label = "Delete"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode
        mod_type = bpy.context.scene.khalibloo_modifier_type

        for obj in bpy.context.selected_objects:
            modifiersRemove(obj, mod_filter_mode, mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ConstraintsMute(bpy.types.Operator):
    """Mute all constraints of the selected objects"""
    bl_idname = "object.khalibloo_constraints_mute"
    bl_label = "Mute Constraints"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        objBackup = bpy.context.active_object

        for obj in bpy.context.selected_objects:
            muteConstraints(obj)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ConstraintsUnmute(bpy.types.Operator):
    """Unmute all constraints of the selected objects"""
    bl_idname = "object.khalibloo_constraints_unmute"
    bl_label = "Unmute Constraints"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        objBackup = bpy.context.active_object

        for obj in bpy.context.selected_objects:
            unmuteConstraints(obj)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ConstraintsRemove(bpy.types.Operator):
    """Delete all constraints of the selected objects"""
    bl_idname = "object.khalibloo_constraints_remove"
    bl_label = "Delete Constraints"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        objBackup = bpy.context.active_object

        for obj in bpy.context.selected_objects:
            removeConstraints(obj)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class BoneConstraintsMute(bpy.types.Operator):
    """Mute all constraints of the selected bones"""
    bl_idname = "object.khalibloo_bone_constraints_mute"
    bl_label = "Mute Bone Constraints"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'POSE') and (len(context.selected_pose_bones) > 0))
        #the 2nd parameter would spit an error if we are not in pose mode
        #so, it's importaant to check for pose mode before counting selected pose bones


    def execute(self, context):
        for bone in bpy.context.selected_pose_bones:
            muteConstraints(bone)
        return {'FINISHED'}

class BoneConstraintsUnmute(bpy.types.Operator):
    """Unmute all constraints of the selected bones"""
    bl_idname = "object.khalibloo_bone_constraints_unmute"
    bl_label = "Unmute Bone Constraints"

    @classmethod
    def poll(cls, context):
       return ((context.mode == 'POSE') and (len(context.selected_pose_bones) > 0))
        #the 2nd parameter would spit an error if we are not in pose mode
        #so, it's importaant to check for pose mode before counting selected pose bones


    def execute(self, context):
        for bone in bpy.context.selected_pose_bones:
            unmuteConstraints(bone)
        return {'FINISHED'}

class BoneConstraintsRemove(bpy.types.Operator):
    """Delete all constraints of the selected bones"""
    bl_idname = "object.khalibloo_bone_constraints_remove"
    bl_label = "Delete Bone Constraints"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'POSE') and (len(context.selected_pose_bones) > 0))
        #the 2nd parameter would spit an error if we are not in pose mode
        #so, it's importaant to check for pose mode before counting selected pose bones


    def execute(self, context):
        for bone in bpy.context.selected_pose_bones:
            removeConstraints(bone)
        return {'FINISHED'}

class MetarigGamerigSetup(bpy.types.Operator):
    """Hookup active metarig to selected rigify rig"""
    bl_idname = "object.khalibloo_metarig_gamerig_hookup"
    bl_label = "Hookup Metarig"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) == 2) and (context.selected_objects[0].type == 'ARMATURE') and (context.selected_objects[1].type == 'ARMATURE'))

    def execute(self, context):
        metarig = bpy.context.active_object
        for obj in bpy.context.selected_objects:
            if metarig == obj:
                pass
            else:
                rigifyRig = obj
        prefix = "DEF-"
        if (metarig is not None and metarig.type == 'ARMATURE'):
            bpy.ops.object.mode_set(mode='EDIT')
            #AUTOMATIC EDITS
            for bone in metarig.data.edit_bones:
                bone.name = prefix + bone.name
            #MANUAL EDITS
            metarig.data.edit_bones["DEF-upper_arm.L"].name = "DEF-upper_arm.01.L"
            metarig.data.edit_bones["DEF-upper_arm.R"].name = "DEF-upper_arm.01.R"
            metarig.data.edit_bones["DEF-forearm.L"].name = "DEF-forearm.01.L"
            metarig.data.edit_bones["DEF-forearm.R"].name = "DEF-forearm.01.R"
            metarig.data.edit_bones["DEF-thumb.01.L"].name = "DEF-thumb.01.L.01"
            metarig.data.edit_bones["DEF-thumb.01.R"].name = "DEF-thumb.01.R.01"
            metarig.data.edit_bones["DEF-f_index.01.L"].name = "DEF-f_index.01.L.01"
            metarig.data.edit_bones["DEF-f_index.01.R"].name = "DEF-f_index.01.R.01"
            metarig.data.edit_bones["DEF-f_middle.01.L"].name = "DEF-f_middle.01.L.01"
            metarig.data.edit_bones["DEF-f_middle.01.R"].name = "DEF-f_middle.01.R.01"
            metarig.data.edit_bones["DEF-f_ring.01.L"].name = "DEF-f_ring.01.L.01"
            metarig.data.edit_bones["DEF-f_ring.01.R"].name = "DEF-f_ring.01.R.01"
            metarig.data.edit_bones["DEF-f_pinky.01.L"].name = "DEF-f_pinky.01.L.01"
            metarig.data.edit_bones["DEF-f_pinky.01.R"].name = "DEF-f_pinky.01.R.01"
            metarig.data.edit_bones["DEF-thigh.L"].name = "DEF-thigh.01.L"
            metarig.data.edit_bones["DEF-thigh.R"].name = "DEF-thigh.01.R"
            metarig.data.edit_bones["DEF-shin.L"].name = "DEF-shin.01.L"
            metarig.data.edit_bones["DEF-shin.R"].name = "DEF-shin.01.R"
            #DELETE JUNK BONES
            bpy.ops.armature.select_all(action='DESELECT')
            metarig.data.edit_bones["DEF-heel.L"].select = True
            metarig.data.edit_bones["DEF-heel.R"].select = True
            metarig.data.edit_bones["DEF-heel.02.L"].select = True
            metarig.data.edit_bones["DEF-heel.02.R"].select = True
            metarig.data.edit_bones["DEF-palm.01.L"].select = True
            metarig.data.edit_bones["DEF-palm.01.R"].select = True
            metarig.data.edit_bones["DEF-palm.02.L"].select = True
            metarig.data.edit_bones["DEF-palm.02.R"].select = True
            metarig.data.edit_bones["DEF-palm.03.L"].select = True
            metarig.data.edit_bones["DEF-palm.03.R"].select = True
            metarig.data.edit_bones["DEF-palm.04.L"].select = True
            metarig.data.edit_bones["DEF-palm.04.R"].select = True
            bpy.ops.armature.delete()
            #CONSTRAINTS
            bpy.ops.object.mode_set(mode='POSE')
            for bone in metarig.pose.bones:
                bone.constraints.new(type='COPY_TRANSFORMS')
                bone.constraints[0].target = rigifyRig
                bone.constraints[0].subtarget = bone.name
        return {'FINISHED'}

class TexturesOff(bpy.types.Operator):
    """Disable all textures of all materials of the selected objects"""
    bl_idname = "object.khalibloo_textures_off"
    bl_label = "Disable Textures"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        #objBackup = bpy.context.active_object

        for obj in bpy.context.selected_objects:
            texturesOff(obj)

        #bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class TexturesOn(bpy.types.Operator):
    """Enable all textures of all materials of the selected objects"""
    bl_idname = "object.khalibloo_textures_on"
    bl_label = "Disable Textures"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        #objBackup = bpy.context.active_object

        for obj in bpy.context.selected_objects:
            texturesOn(obj)

        #bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class MaterialsRemove(bpy.types.Operator):
    """Remove all materials from the selected objects"""
    bl_idname = "object.khalibloo_materials_remove"
    bl_label = "Remove Materials"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        objBackup = bpy.context.active_object

        for obj in bpy.context.selected_objects:
            materialsRemove(obj)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class AssignMatIndices(bpy.types.Operator):
    """Assign unique pass indices to all materials"""
    bl_idname = "object.khalibloo_assign_mat_indices"
    bl_label = "Assign Mat Indices"

    @classmethod
    def poll(cls, context):
        return (len(bpy.data.materials) > 0)


    def execute(self, context):
        assignMatIndices()
        return {'FINISHED'}

class ImportedMaterialsSetup(bpy.types.Operator):
    """Setup materials for imported objects"""
    bl_idname = "object.khalibloo_setup_imported_materials"
    bl_label = "Setup Imported Materials"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            if (len(obj.material_slots) > 0):
                setupImportedMaterials(context, obj)
        return {'FINISHED'}

class AssignObjIndices(bpy.types.Operator):
    """Assign unique pass indices to selected objects"""
    bl_idname = "object.khalibloo_assign_obj_indices"
    bl_label = "Assign Object Indices"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        assignObjIndices(context)
        return {'FINISHED'}

class LocationApply(bpy.types.Operator):
    """Apply location transforms of the selected objects"""
    bl_idname = "object.khalibloo_apply_location"
    bl_label = "Apply Location"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object

        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class RotationApply(bpy.types.Operator):
    """Apply rotation transforms of the selected objects"""
    bl_idname = "object.khalibloo_apply_rotation"
    bl_label = "Apply Rotation"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object

        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class ScaleApply(bpy.types.Operator):
    """Apply scale transforms of the selected objects"""
    bl_idname = "object.khalibloo_apply_scale"
    bl_label = "Apply Scale"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object

        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class VisualTransformApply(bpy.types.Operator):
    """Apply visual transforms (constraints, etc) of the selected objects"""
    bl_idname = "object.khalibloo_apply_visual_transform"
    bl_label = "Apply Visual Transform"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object

        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.visual_transform_apply()

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}

class HideSelect(bpy.types.Operator):
    """Make selected objects unselectable"""
    bl_idname = "object.khalibloo_hide_select"
    bl_label = "Hide Select"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        hideSelect()
        return {'FINISHED'}

class UnhideSelect(bpy.types.Operator):
    """Make all objects selectable"""
    bl_idname = "object.khalibloo_unhide_select"
    bl_label = "Unhide Select"

    @classmethod
    def poll(cls, context):
        return (len(context.scene.objects) > 0)


    def execute(self, context):
        unhideSelect()
        return {'FINISHED'}

class HideRender(bpy.types.Operator):
    """Make selected objects invisible in renders"""
    bl_idname = "object.khalibloo_hide_render"
    bl_label = "Hide Render"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        hideRender()
        return {'FINISHED'}

class UnhideRender(bpy.types.Operator):
    """Make selected objects visible in renders"""
    bl_idname = "object.khalibloo_unhide_render"
    bl_label = "Unhide Render"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)


    def execute(self, context):
        unhideRender()
        return {'FINISHED'}

class ModifierAdd(bpy.types.Operator):
    """Add the modifier specified above to the selected objects"""
    bl_idname = "object.khalibloo_add_modifier"
    bl_label = "Add Modifier"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None))


    def execute(self, context):
        objBackup = bpy.context.active_object
        mod_type = bpy.context.scene.khalibloo_modifier_type
        nonMeshModList = ['MESH_CACHE', 'ARRAY', 'BUILD', 'DECIMATE', 'EDGE_SPLIT', 'MIRROR',
                           'REMESH', 'SCREW', 'SOLIDIFY', 'SUBSURF', 'TRIANGULATE',
                           'ARMATURE', 'CAST', 'CURVE', 'HOOK', 'LATTICE', 'MESH_DEFORM',
                           'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH', 'WARP', 'WAVE',
                           'SOFT_BODY']

        for obj in bpy.context.selected_objects:
            if (obj.type == 'MESH'):
                bpy.context.scene.objects.active = obj
                bpy.ops.object.modifier_add(type=mod_type)

            #if it's not a mesh, but is still a modifiable object
            elif (isModifierType(obj)):
                if (mod_type in nonMeshModList):
                    bpy.context.scene.objects.active = obj
                    bpy.ops.object.modifier_add(type=mod_type)

        bpy.context.scene.objects.active = objBackup
        return {'FINISHED'}


class MultiEditStart(bpy.types.Operator):
    """Start editing multiple meshes at once"""
    bl_idname = "object.khalibloo_multiedit_start"
    bl_label = "Start Multi Edit"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 1

    def execute(self, context):
        meshCount = 0
        for obj in context.selected_objects:
            if (obj.type == 'MESH'):
                meshCount += 1
        if (meshCount > 1):
            startMultiEdit(context)
        return {'FINISHED'}

class MultiEditEnd(bpy.types.Operator):
    """End editing multiple meshes, and separate them"""
    bl_idname = "object.khalibloo_multiedit_end"
    bl_label = "End Multi Edit"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0) and (context.active_object is not None) and (context.active_object.type == 'MESH')

    def execute(self, context):
        for obj in context.selected_objects:
            greenlight = False
            if (obj.type == 'MESH'):
                print ("mesh")
                if (obj["khalibloo_multiedit"] == "multi object" and len(obj["khalibloo_multiedit_originalsNameList"]) > 0):
                    i = len(obj.vertex_groups) - 1
                    print("checkpoint 01")
                    if (i >= 1):
                        groups = 0
                        print("checkpoint 02")
                        while ((greenlight == False) and (i > -1) and (groups < 2)):
                            print("checkpoint 03")
                            if (obj.vertex_groups[i].name.startswith("khalibloo_multiedit_")):
                                print("checkpoint 04")
                                groups += 1
                                if (groups > 1):
                                    greenlight = True
                                    print ("Greenlight")
                            i -= 1
                        if (greenlight):
                            endMultiEdit(obj)
        return {'FINISHED'}

class Toonify(bpy.types.Operator):
    """Toonify active object's active material"""
    bl_idname = "object.khalibloo_toonify"
    bl_label = "Toonify"

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0) and (context.active_object is not None) and (isMaterialType(context.active_object) and (context.active_object.active_material is not None))

    def execute(self, context):
        obj = context.active_object
        mat = obj.active_material
        toonify(mat)
        return {'FINISHED'}

class BindMesh(bpy.types.Operator, ExportHelper):
    """Bind mesh"""
    bl_idname = "object.khalibloo_bind_mesh"
    bl_label = "Bind Mesh"

    # ImportHelper mixin class uses this
    filename_ext = ".txt"

    filter_glob = StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            )

    path_mode = path_reference_mode
    check_extension = True

    @classmethod
    def poll(cls, context):
        if ((context.active_object is not None) and (len(context.selected_objects) == 2)) :
            if ((context.selected_objects[0].type == 'MESH') and (context.selected_objects[1].type == 'MESH')) :
                return True
        return False

    def execute(self, context):
        file = open(self.filepath, 'w')
        bpy.ops.object.mode_set(mode='OBJECT')
        activeObj = context.active_object
        for obj in context.selected_objects :
            if obj == activeObj :
                pass
            else :
                selectedObj = obj
        bindMesh(context, activeObj, selectedObj, file)
        context.scene.objects.active = activeObj
        return {'FINISHED'}

class UpdateBoundMesh(bpy.types.Operator, ImportHelper):
    """Update the position of each vertex in the active mesh to match the offsets of the selected mesh"""
    bl_idname = "object.khalibloo_update_bound_mesh"
    bl_label = "Update Bound Mesh"

    # ImportHelper mixin class uses this
    filename_ext = ".txt"

    filter_glob = StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            )

    @classmethod
    def poll(cls, context):
        if ((context.active_object is not None) and (len(context.selected_objects) == 2)) :
            if ((context.selected_objects[0].type == 'MESH') and (context.selected_objects[1].type == 'MESH')) :
                return True
        return False

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        activeObj = context.active_object
        for obj in context.selected_objects :
            if obj == activeObj :
                pass
            else :
                selectedObj = obj
        updateBoundMesh(context, activeObj, selectedObj, self.filepath)
        bpy.ops.object.mode_set(mode='OBJECT')
        context.scene.objects.active = activeObj
        return {'FINISHED'}



#---------------------------------------------------------------------

class FlattenUVx(bpy.types.Operator):
    """Flatten selected UV elements on the X axis"""
    bl_idname = "uv.khalibloo_uv_flatten_x"
    bl_label = "Flatten X"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None) and (context.active_object.type == 'MESH'))


    def execute(self, context):
        bpy.ops.transform.resize(value = (0, 1, 1), constraint_axis = (True, False, False),
                                 constraint_orientation = 'GLOBAL', proportional = 'DISABLED')
        return {'FINISHED'}

class FlattenUVy(bpy.types.Operator):
    """Flatten selected UV elements on the Y axis"""
    bl_idname = "uv.khalibloo_uv_flatten_y"
    bl_label = "Flatten Y"

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 0) and (context.active_object is not None) and (context.active_object.type == 'MESH'))


    def execute(self, context):
        bpy.ops.transform.resize(value = (1, 0, 1), constraint_axis = (False, True, False),
                                 constraint_orientation = 'GLOBAL', proportional = 'DISABLED')
        return {'FINISHED'}


def initialize():
    bpy.types.Scene.khalibloo_genesis_platform_subclass = bpy.props.EnumProperty(items =(
                                         ('FIGURE', 'Figure',''),
                                         ('ITEM', 'Item','')),
                                name = ' ',
                                default = 'FIGURE')

    bpy.types.Scene.khalibloo_genesis2_platform_subclass = bpy.props.EnumProperty(items=(
                                         ('MALE', 'Male',''),
                                         ('FEMALE', 'Female',''),
                                         ('ITEM', 'Item', '')),
                                name = ' ',
                                default = 'MALE')

    bpy.types.Scene.khalibloo_genesis3_platform_subclass = bpy.props.EnumProperty(items=(
                                         ('MALE', 'Male',''),
                                         ('FEMALE', 'Female',''),
                                         ('ITEM', 'Item', '')),
                                name = ' ',
                                default = 'MALE')

    bpy.types.Scene.khalibloo_platform = bpy.props.EnumProperty(items=(
                                         ('GENERAL', 'General', ''),
                                         ('DAZ GENESIS', 'DAZ Genesis', ''),
                                         ('DAZ GENESIS 2', 'DAZ Genesis 2', ''),
                                         ('DAZ GENESIS 3', 'DAZ Genesis 3', '')),
                                name = 'Platform Type',
                                description = 'Choose platform type',
                                default = 'GENERAL')

    bpy.types.Scene.khalibloo_general_platform_subclass = bpy.props.EnumProperty(items=(
                                         ('OBJECT DATA', 'Object Data','', 'OBJECT_DATA', 0),
                                         ('MESH DATA', 'Mesh Data','', 'MESH_DATA', 1),
                                         ('MATERIALS', 'Materials', '', 'MATERIAL', 2),
                                         ('MODIFIERS', 'Modifiers', '', 'MODIFIER', 3),
                                         ('ARMATURES', 'Armatures', '', 'ARMATURE_DATA', 4),
                                         ('CONSTRAINTS', 'Constraints', '', 'CONSTRAINT', 5),
                                         ('CUSTOM_OPS', 'Custom Ops', '', 'ZOOMIN', 6)),
                                name = '',
                                description = 'Type of tools to display',
                                default = 'OBJECT DATA')

    bpy.types.Scene.khalibloo_modifier_type = bpy.props.EnumProperty(items =(
                                         #Modify
                                         ('MESH_CACHE', 'Mesh Cache', '', 'MOD_MESHDEFORM', 0),
                                         ('UV_PROJECT', 'UV Project', '', 'MOD_UVPROJECT', 1),
                                         ('UV_WARP', 'UV Warp', '', 'MOD_UVPROJECT', 2),
                                         ('VERTEX_WEIGHT_EDIT', 'Vertex Weight Edit', '', 'MOD_VERTEX_WEIGHT', 3),
                                         ('VERTEX_WEIGHT_MIX', 'Vertex Weight Mix', '', 'MOD_VERTEX_WEIGHT', 4),
                                         ('VERTEX_WEIGHT_PROXIMITY', 'Vertex Weight Proximity', '', 'MOD_VERTEX_WEIGHT', 5),
                                         #Generate
                                         ('ARRAY', 'Array', '', 'MOD_ARRAY', 6),
                                         ('BEVEL', 'Bevel', '', 'MOD_BEVEL', 7),
                                         ('BOOLEAN', 'Boolean', '', 'MOD_BOOLEAN', 8),
                                         ('BUILD', 'Build', '', 'MOD_BUILD', 9),
                                         ('DECIMATE', 'Decimate', '', 'MOD_DECIM', 10),
                                         ('EDGE_SPLIT', 'Edge Split', '', 'MOD_EDGESPLIT', 11),
                                         ('MASK', 'Mask', '', 'MOD_MASK', 12),
                                         ('MIRROR', 'Mirror', '', 'MOD_MIRROR', 13),
                                         ('MULTIRES', 'Multiresolution', '', 'MOD_MULTIRES', 14),
                                         ('REMESH', 'Remesh', '', 'MOD_REMESH', 15),
                                         ('SCREW', 'Screw', '', 'MOD_SCREW', 16),
                                         ('SKIN', 'Skin', '', 'MOD_SKIN', 17),
                                         ('SOLIDIFY', 'Solidify', '', 'MOD_SOLIDIFY', 18),
                                         ('SUBSURF', 'Subsurface Division', '', 'MOD_SUBSURF', 19),
                                         ('TRIANGULATE', 'Triangulate', '', 'MOD_TRIANGULATE', 20),
                                         ('WIREFRAME', 'Wireframe', '', 'MOD_WIREFRAME', 21),
                                         #Deform
                                         ('ARMATURE', 'Armature', '', 'MOD_ARMATURE', 22),
                                         ('CAST', 'Cast', '', 'MOD_CAST', 23),
                                         ('CURVE', 'Curve', '', 'MOD_CURVE', 24),
                                         ('DISPLACE', 'Displace', '', 'MOD_DISPLACE', 25),
                                         ('HOOK', 'Hook', '', 'HOOK', 26),
                                         ('LAPLACIANDEFORM', 'Laplacian Deform', '', 'MOD_MESHDEFORM', 27),
                                         ('LAPLACIANSMOOTH', 'Laplacian Smooth', '', 'MOD_SMOOTH', 28),
                                         ('LATTICE', 'Lattice', '', 'MOD_LATTICE', 29),
                                         ('MESH_DEFORM', 'Mesh Deform', '', 'MOD_MESHDEFORM', 30),
                                         ('SHRINKWRAP', 'Shrinkwrap', '', 'MOD_SHRINKWRAP', 31),
                                         ('SIMPLE_DEFORM', 'Simple Deform', '', 'MOD_SIMPLEDEFORM', 32),
                                         ('SMOOTH', 'Smooth', '', 'MOD_SMOOTH', 33),
                                         ('WARP', 'Warp', '', 'MOD_WARP', 34),
                                         ('WAVE', 'Wave', '', 'MOD_WAVE', 35),
                                         #Simulate
                                         ('CLOTH', 'Cloth', '', 'MOD_CLOTH', 36),
                                         ('COLLISION', 'Collision', '', 'MOD_PHYSICS', 37),
                                         ('DYNAMIC_PAINT', 'Dynamic Paint', '', 'MOD_DYNAMICPAINT', 38),
                                         ('EXPLODE', 'Explode', '', 'MOD_EXPLODE', 39),
                                         ('FLUID_SIMULATION', 'Fluid Simulation', '', 'MOD_FLUIDSIM', 40),
                                         ('OCEAN', 'Ocean', '', 'MOD_OCEAN', 41),
                                         ('PARTICLE_INSTANCE', 'Particle Instance', '', 'MOD_PARTICLES', 42),
                                         ('PARTICLE_SYSTEM', 'Particle System', '', 'MOD_PARTICLES', 43),
                                         ('SMOKE', 'Smoke', '', 'MOD_SMOKE', 44),
                                         ('SOFT_BODY', 'Soft Body', '', 'MOD_SOFT', 45)),
                                         name = '',
                                         description = 'Select type of modifier to be affected by the buttons below',
                                         default = 'SUBSURF')

    bpy.types.Scene.khalibloo_modifier_filter_mode = bpy.props.EnumProperty(items =(
                                         ('ALL', 'All', 'Actions will affect all types of modifiers of all selected objects'),
                                         ('SPECIFIC', 'Specific', 'Actions will affect a specific type of modifier of all selected objects')),
                                name = ' ',
                                description = 'Choose whether to affect all types of modifiers or just a specific type',
                                default = 'ALL')

    bpy.types.Scene.khalibloo_spread_harden_vgroups = bpy.props.BoolProperty(
    name = "Spread Vertex Groups",
    description = "Whether or not vertex group weights may spread to vertices that are not initially part of the vertex groups",
    default=True)

    bpy.types.Scene.khalibloo_affect_textures = bpy.props.BoolProperty(
    name = "Textures",
    description = "Whether or not the material setup affects textures as well",
    default=True)

    bpy.types.Scene.khalibloo_merge_mats = bpy.props.BoolProperty(
    name = "Merge Materials",
    description = "Merge materials with the same diffuse textures. Warning: This will affect EVERY material slot in the active Genesis figure, not just the default Genesis materials",
    default = False)

    bpy.types.Scene.khalibloo_genesis_morph_dir = bpy.props.StringProperty(
    name = "",
    description = "Folder where your Genesis morphs of choice are located",
    subtype = "DIR_PATH",
    default = "c:/")

    bpy.types.Scene.khalibloo_batchbake_images = bpy.props.EnumProperty(items = (
                                ('Default', 'Default', ''),
                                ('Untitled', 'Untitled', '')),
                                name = "",
                                description = "Image to save as",
                                default = 'Default')

    bpy.types.Scene.khalibloo_batchbake_startframe = bpy.props.IntProperty(
    name = "Start Frame",
    description = "The frame from which to start baking",
    default = 1)

    bpy.types.Scene.khalibloo_batchbake_endframe = bpy.props.IntProperty(
    name = "End Frame",
    description = "The frame on which to end baking",
    default = 250)
