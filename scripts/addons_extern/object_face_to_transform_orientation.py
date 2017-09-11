# <pep8-80 compliant>

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
import mathutils
from math import radians
from bpy.props import *


__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "0.2"
__date__ = "17 May 2015"

bl_info = {
    "name": "Face to Transform Orientation",
    "author": "Nutti",
    "version": (0, 2),
    "blender": (2, 7, 0),
    "location": "Object > Face object to Transform Orientation",
    "description": "Face object to transform orientation",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


def SetOrientationCallback(scene, context):

    items = []

    for key in bpy.data.screens['Default'].scene.orientations.keys():
        items.append((key, key, ""))

    return items


# face to
class FTTO(bpy.types.Operator):
    """ """

    bl_idname = "object_transform.face_to_transform_orientation"
    bl_label = "Face To Transform Orientation"
    bl_description = "Face to transform orientation"
    bl_options = {'REGISTER', 'UNDO'}

    orientation = EnumProperty(
        name="Transform Orientation",
        description="Transform orientation",
        items=SetOrientationCallback)

    offset_euler_x = FloatProperty(
        name="Rotate X",
        description="Rotate X ...",
        default=0.0,
        min=-360.0,
        max=360.0)

    offset_euler_y = FloatProperty(
        name="Rotate Y",
        description="Rotate Y ...",
        default=0.0,
        min=-360.0,
        max=360.0)

    offset_euler_z = FloatProperty(
        name="Rotate Z",
        description="Rotate Z ...",
        default=0.0,
        min=-360.0,
        max=360.0)

    base_euler = None
    prev_orientation = None

    def __init__(self):
        self.face_to(self.orientation)

    def face_to(self, orientation):
        # get base orientation
        scene = bpy.data.screens['Default'].scene
        if len(scene.orientations) == 0:
            self.report({'WARNING'}, "Make Transform Orientation at first.")
            return 1
        mat = scene.orientations[orientation].matrix
        base_quota = mat.to_quaternion()

        # set orientation to object
        active_objs = bpy.context.selected_objects
        for o in active_objs:
            mode = o.rotation_mode
            o.rotation_mode = 'QUATERNION'
            o.rotation_quaternion = base_quota.copy()
            o.rotation_mode = mode

        # set initial value
        self.offset_euler_x = 0.0
        self.offset_euler_y = 0.0
        self.offset_euler_z = 0.0
        self.base_euler = base_quota.to_euler()

        self.prev_orientation = orientation

    def execute(self, context):

        if self.prev_orientation != self.orientation:
            ret = self.face_to(self.orientation)
            if ret != 0:
                return {'CANCELLED'}

        # set orientation to object
        new_euler = self.base_euler.copy()
        new_euler.x += radians(self.offset_euler_x)
        new_euler.y += radians(self.offset_euler_y)
        new_euler.z += radians(self.offset_euler_z)
        active_objs = bpy.context.selected_objects
        for o in active_objs:
            mode = o.rotation_mode
            o.rotation_mode = 'QUATERNION'
            o.rotation_quaternion = new_euler.to_quaternion()
            o.rotation_mode = mode

        return {'FINISHED'}


# registration
def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(FTTO.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_transform_object.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_transform_object.remove(menu_func)


if __name__ == "__main__":
    register()
