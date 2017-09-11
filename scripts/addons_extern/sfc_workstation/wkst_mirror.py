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

# bl_info = {
#    "name": "Workstation Mirror",
#    "author": "mkbreuer",
#    "version": (0, 1, 0),
#    "blender": (2, 76, 0),
#    "location": "View3D > Toolbar > Panel",
#    "warning": "",
#    "description": "Mirror Operator for the Main Panel",
#    "wiki_url": "",
#    "category": ""Workstation",
#}


import bpy
from bpy import*


#######  Mirror Full activ  #########

class FullMIRROR(bpy.types.Operator):
    """Add a x mirror modifier with cage and clipping"""
    bl_idname = "view3d.fullmirror"
    bl_label = "Mirror X"

    def execute(self, context):

        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}

bpy.utils.register_class(FullMIRROR)


class FullMIRRORY(bpy.types.Operator):
    """Add a y mirror modifier with cage and clipping"""
    bl_idname = "view3d.fullmirrory"
    bl_label = "Mirror Y"

    def execute(self, context):

        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_x = False
        bpy.context.object.modifiers["Mirror"].use_y = True
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}

bpy.utils.register_class(FullMIRRORY)


class FullMIRRORZ(bpy.types.Operator):
    """Add a z mirror modifier with cage and clipping"""
    bl_idname = "view3d.fullmirrorz"
    bl_label = "Mirror Z"

    def execute(self, context):

        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_x = False
        bpy.context.object.modifiers["Mirror"].use_z = True
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}


#####  Mirror XYZ Local  ##########

class Mirror4(bpy.types.Operator):
    """mirror over X axis / local"""
    bl_idname = "object.mirror4"
    bl_label = "mirror selected on X axis > local"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(True, False, False), constraint_orientation='LOCAL')

        return {'FINISHED'}


class Mirror5(bpy.types.Operator):
    """mirror over Y axis / local"""
    bl_idname = "object.mirror5"
    bl_label = "mirror selected on Y axis > local"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(False, True, False), constraint_orientation='LOCAL')

        return {'FINISHED'}


class Mirror6(bpy.types.Operator):
    """mirror over Z axis / local"""
    bl_idname = "object.mirror6"
    bl_label = "mirror selected on Z axis > local"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(False, False, True), constraint_orientation='LOCAL')

        return {'FINISHED'}


#####  Mirror XYZ Global  #########

class Mirror1(bpy.types.Operator):
    """mirror over X axis / global"""
    bl_idname = "object.mirror1"
    bl_label = "mirror selected on X axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(True, False, False))

        return {'FINISHED'}


class Mirror2(bpy.types.Operator):
    """mirror over Y axis / global"""
    bl_idname = "object.mirror2"
    bl_label = "mirror selected on Y axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(False, True, False))

        return {'FINISHED'}


class Mirror3(bpy.types.Operator):
    """mirror over Z axis / global"""
    bl_idname = "object.mirror3"
    bl_label = "mirror selected on Z axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(False, False, True))

        return {'FINISHED'}


###### Register #######################

def register():

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
