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

# <pep8 compliant>

import bpy

bl_info = {
    "name": "Copy Custom Properties",
    "author": "scorpion81",
    "version": (1, 0, 5),
    "blender": (2, 7, 3),
    "location": "Object / Armature > Custom Properties Copy > Copy Custom Properties",
    "description": "Copies custom properties from active object to selected objects",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


def testpose(ob):
    return hasattr(ob, "pose") and ob.pose is not None


def testdata(ob):
    return hasattr(ob, "data") and ob.data is not None


def testbone(ob):
    return testdata(ob) and hasattr(ob.data, "bones") and ob.data.bones is not None


def testeditbone(ob):
    return testdata(ob) and hasattr(ob.data, "edit_bones") and ob.data.edit_bones is not None


def set_prop_bones(bones, data):
    i = 0
    if len(data) > 0:
        for bone in enumerate(bones, i):
            if len(data[i]) > 2:
                name = data[i][0]
                value = data[i][1]
                rna = data[i][2]
                set_prop(bone[1], name, value, rna)


def getPropBones(bones):
    ret = []
    for bone in bones:
        ret.append(getProps(bone))

    return ret


def set_prop(ob, name, value, rna):
    # need to build own dict if missing
    if ob is None:
        return
    if '_RNA_UI' not in ob.keys():
        ob['_RNA_UI'] = {}

    ob['_RNA_UI'][name] = rna
    ob[name] = value


def getRNA(ob, name):
    # min max description settings, thanks to batFINGER !
    try:
        rna = ob['_RNA_UI'][name]
        min = rna['min']
        max = rna['max']
        desc = rna['description']

    except KeyError:
        min = 0.0
        max = 1.0
        desc = ""

    return {'min': min, 'max': max, 'description': desc}


def getProps(ob):
    # object custom properties
    if ob is None:
        return tuple()
    names = list(set(ob.keys()) - set(('cycles_visibility', '_RNA_UI')))
    values = [(name, ob[name], getRNA(ob, name)) for name in names]

    return values


class CopyCustomProperties(bpy.types.Operator):
    """Copy Custom Properties from Active to Selected objects"""
    bl_idname = "object.custom_property_copy"
    bl_label = "Copy Custom Properties"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        active = bpy.context.active_object
        selected = bpy.context.selected_objects

        [[set_prop(ob, name, value, rna) for (name, value, rna) in getProps(active)] for ob in selected]
        [[set_prop(ob.data, name, value, rna) for (name, value, rna) in getProps(active.data)] for ob in selected if testdata(ob)]

        # armature bone handling, can only copy as many bone data sets as bones are available in active object, and catch "missing" bones in dest. objects
        [[set_prop_bones(ob.data.bones, data) for (data) in getPropBones(active.data.bones)] for ob in selected if testbone(ob)]
        [[set_prop_bones(ob.data.edit_bones, data) for (data) in getPropBones(active.data.edit_bones)] for ob in selected if testeditbone(ob)]
        [[set_prop_bones(ob.pose.bones, data) for (data) in getPropBones(active.pose.bones)] for ob in selected if testpose(ob)]

        return {'FINISHED'}


class CopyCustomPropertiesBone(bpy.types.Operator):
    """Copy Custom Properties from Active to Selected Bones"""
    bl_idname = "object.custom_property_copy_bone"
    bl_label = "Copy Custom Properties Bone"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        try:
            active_p = bpy.context.active_pose_bone
            selected_p = bpy.context.selected_pose_bones
            [[set_prop(bo, name, value, rna) for (name, value, rna) in getProps(active_p)] for bo in selected_p]
        except Exception:
            pass

        try:
            active_e = bpy.context.active_editable_bone
            selected_e = bpy.context.selected_editable_bones
            [[set_prop(bo, name, value, rna) for (name, value, rna) in getProps(active_e)] for bo in selected_e]
        except Exception:
            pass

        try:
            active = bpy.context.active_bone
            selected = bpy.context.selected_bones
            [[set_prop(bo, name, value, rna) for (name, value, rna) in getProps(active)] for bo in selected]
        except Exception:
            pass

        return {'FINISHED'}


class CopyPanel(bpy.types.Panel):
    """Creates a Custom Property Panel in the Object properties window"""
    bl_label = "Custom Property Active to Selected"
    bl_idname = "OBJECT_PT_customprop"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.custom_property_copy")


class CopyPanelBone(bpy.types.Panel):
    """Creates a Custom Property Panel in the Object properties window"""
    bl_label = "Custom Property Active to Selected Bone"
    bl_idname = "OBJECT_PT_customprop_bone"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "bone"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.custom_property_copy_bone")


def register():
    bpy.utils.register_class(CopyCustomPropertiesBone)
    bpy.utils.register_class(CopyCustomProperties)
    bpy.utils.register_class(CopyPanel)
    bpy.utils.register_class(CopyPanelBone)


def unregister():
    bpy.utils.unregister_class(CopyPanel)
    bpy.utils.unregister_class(CopyPanelBone)
    bpy.utils.unregister_class(CopyCustomProperties)
    bpy.utils.unregister_class(CopyCustomPropertiesBone)


if __name__ == "__main__":
    register()
