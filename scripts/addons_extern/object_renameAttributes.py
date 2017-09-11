########
"""
This code is open source under the MIT license.

It tries to change the name of all attributes of an object
that match an input format, for example if an object is
formatted with the name 'steve', such that it consists of
objects 'steve_arm' or 'steve.eye.L' or 'steve.materialMain'
and so forth.

Currently works for objects, materials (first slot?), groups
>> need to support MESH names (indp of objects)
and textures under the materials

# currenly works for most cases, except for example:
find: stevey
replace with: steve

# the following does work, however:
find: steve
replace with: stevey

# also cannot 'replace' with nothing yet
"""

########
bl_info = {
    "name": "Rename Attributes",
    "category": "Object",
    "version": (1, 0),
    "blender": (2, 70, 0),
    "location": "3D window toolshelf",
    "description": "Help rename several attributes of a common base name",
    "wiki_url": "https://github.com/TheDuckCow/blendNameChange",
    "author": "Patrick W. Crawford, TheDuckCow"
}

import bpy


def matList(objList):
    matList = []
    for obj in objList:
        # ignore non mesh selected objects
        if obj.type != 'MESH':
            continue

        # check that operation has not already been done to material:
        # mat = obj.material_slots

        for mat in obj.material_slots:
            if mat.material.name not in matList:
                matList.append(mat.material)
    return matList


def texList(materials):
    texList = []
    for mat in materials:
        for slot in mat.texture_slots:
            try:
                if slot.texture not in texList:
                    texList.append(slot.texture)
            except:
                continue

    return texList


#######
# get attributes into one list
def listAttributes():
    context = bpy.context

    # add attributes to master list (at the level where x.name can be used)
    # only use data connected to selected objects
    nameList = context.selected_objects
    materials = matList(nameList)
    nameList += materials
    nameList += texList(materials)
    return nameList


#######
# the find/replace function
def nameChange():

    context = bpy.context
    key = context.scene.attChange_find
    replace = context.scene.attChange_replace

    nameList = listAttributes()

    # iteration for object names
    for name in nameList:
        tmp = name.name.split(key)
        if len(name.name.split(replace)) > 1:
            continue
        # print(tmp)
        newName = tmp[0]

        if (len(tmp) != 1):
            for a in tmp[1:]:
                # print(newName)
                newName = newName + replace + a

            # print(newName)
            # assign new name
        name.name = newName

    for group in bpy.data.groups:
        # to be consistent, should only check groups part of current selection...
        if (group.name == key):
            group.name = replace
            # print("group renamed: "+replace)


#######
# function for adding a consistent name structure
def prefixName():
    print("Not yet programmed")

    context = bpy.context
    nameList = listAttributes()
    replace = context.scene.attChange_replace

    for name in nameList:
        tmp = name.name.split(replace)
        if tmp[0] == '':
            continue

        name.name = replace + name.name

    for group in bpy.data.groups:
        # to be consistent, should only check groups part of current selection...
        tmp = group.name.split(replace)
        if (tmp[0] != ''):
            group.name = replace + group.name


#######
# attribute change class
class attchange(bpy.types.Operator):
    """Renames attributes of selected objects with a consistent base name to a new base name"""
    bl_idname = "object.attchange"
    bl_label = "Rename Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        nameChange()
        return {'FINISHED'}

#######
# attribute change class


class attprefix(bpy.types.Operator):
    """Adds a prefix name to attributes of selected objects, from 'replace' field"""
    bl_idname = "object.attprefix"
    bl_label = "Prefix Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefixName()
        return {'FINISHED'}


#######
# panel for these declared tools
class attchange_panel(bpy.types.Panel):
    """renameAttributes"""
    bl_label = "Raname Attributes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"

    def draw(self, context):

        layout = self.layout

        split = layout.split()
        col = split.column(align=True)

        col.label(text="Find this name:")
        col.prop(context.scene, "attChange_find", text="")
        col.label(text="Replace with this name:")
        col.prop(context.scene, "attChange_replace", text="")

        split = layout.split()
        col = split.column(align=True)

        col.operator("object.attchange", text="Rename")
        # the prefix function
        col.operator("object.attprefix", text="Prefix")


#######
# un/registration to run addon
def register():
    bpy.utils.register_class(attchange)
    bpy.utils.register_class(attprefix)
    bpy.utils.register_class(attchange_panel)

    # properties
    bpy.types.Scene.attChange_find = bpy.props.StringProperty(
        name="Starting name key, like 'find'",
        description="This is the name that is searched for within the full name of any attribute, and then replaced with a new name",
        default="startingName")
    bpy.types.Scene.attChange_replace = bpy.props.StringProperty(
        name="Replacing name key, like 'replace'",
        description="Attributes with the starting key substring will have that substring changed to this name",
        default="replaceName")


def unregister():
    bpy.utils.unregister_class(attchange)
    bpy.utils.unregister_class(attchange_panel)
    bpy.utils.unregister_class(attprefix)

    # properties
    del bpy.types.Scene.attChange_find
    del bpy.types.Scene.attChange_replace


if __name__ == "__main__":
    register()
