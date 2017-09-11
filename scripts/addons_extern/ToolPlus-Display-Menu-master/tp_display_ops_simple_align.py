# AlingTools.py (c) 2009, 2010 Gabriel Beaudin (gabhead)
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

#bl_info = {
#    "author": "Gabriel Beaudin (gabhead)",
#    "version": (0,1),
#    "blender": (2, 71, 0),
#    "description": "Align Selected Objects to Active Object",
#    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"Scripts/3D interaction/Align_Tools",
#    "tracker_url": "https://developer.blender.org/T22389",


import bpy

# Align all
def main(context):
    for i in bpy.context.selected_objects:
        i.location = bpy.context.active_object.location
        i.rotation_euler = bpy.context.active_object.rotation_euler

# Align Location
def LocAll(context):
    for i in bpy.context.selected_objects:
        i.location = bpy.context.active_object.location

def LocX(context):
    for i in bpy.context.selected_objects:
        i.location.x = bpy.context.active_object.location.x

def LocY(context):
    for i in bpy.context.selected_objects:
        i.location.y = bpy.context.active_object.location.y

def LocZ(context):
    for i in bpy.context.selected_objects:
        i.location.z = bpy.context.active_object.location.z

# Align Rotation
def RotAll(context):
    for i in bpy.context.selected_objects:
        i.rotation_euler = bpy.context.active_object.rotation_euler

def RotX(context):
    for i in bpy.context.selected_objects:
        i.rotation_euler.x = bpy.context.active_object.rotation_euler.x

def RotY(context):
    for i in bpy.context.selected_objects:
        i.rotation_euler.y = bpy.context.active_object.rotation_euler.y

def RotZ(context):
    for i in bpy.context.selected_objects:
        i.rotation_euler.z = bpy.context.active_object.rotation_euler.z

# Align Scale
def ScaleAll(context):
    for i in bpy.context.selected_objects:
        i.scale = bpy.context.active_object.scale

def ScaleX(context):
    for i in bpy.context.selected_objects:
        i.scale.x = bpy.context.active_object.scale.x

def ScaleY(context):
    for i in bpy.context.selected_objects:
        i.scale.y = bpy.context.active_object.scale.y

def ScaleZ(context):
    for i in bpy.context.selected_objects:
        i.scale.z = bpy.context.active_object.scale.z
        


class TP_Display_Align_All(bpy.types.Operator):
    """Align Selected To Active"""
    bl_idname = "tp_display.align"
    bl_label = "Align Selected To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


class TP_Display_Align_Location_All(bpy.types.Operator):
    """Align Selected Location To Active"""
    bl_idname = "tp_display.align_location_all"
    bl_label = "Align Selected Location To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        LocAll(context)
        return {'FINISHED'}


class TP_Display_Align_Location_X(bpy.types.Operator):
    """Align Selected Location X To Active"""
    bl_idname = "tp_display.align_location_x"
    bl_label = "Align Selected Location X To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        LocX(context)
        return {'FINISHED'}


class TP_Display_Align_Location_Y(bpy.types.Operator):
    """Align Selected Location Y To Active"""
    bl_idname = "tp_display.align_location_y"
    bl_label = "Align Selected Location Y To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        LocY(context)
        return {'FINISHED'}


class TP_Display_Align_Location_Z(bpy.types.Operator):
    """Align Selected Location Z To Active"""
    bl_idname = "tp_display.align_location_z"
    bl_label = "Align Selected Location Z To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        LocZ(context)
        return {'FINISHED'}


class TP_Display_Align_Rotation_All(bpy.types.Operator):
    """Align Selected Rotation To Active"""
    bl_idname = "tp_display.align_rotation_all"
    bl_label = "Align Selected Rotation To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        RotAll(context)
        return {'FINISHED'}


class TP_Display_Align_Rotation_X(bpy.types.Operator):
    """Align Selected Rotation X To Active"""
    bl_idname = "tp_display.align_rotation_x"
    bl_label = "Align Selected Rotation X To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        RotX(context)
        return {'FINISHED'}


class TP_Display_Align_Rotation_Y(bpy.types.Operator):
    """Align Selected Rotation Y To Active"""
    bl_idname = "tp_display.align_rotation_y"
    bl_label = "Align Selected Rotation Y To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        RotY(context)
        return {'FINISHED'}


class TP_Display_Align_Rotation_Z(bpy.types.Operator):
    """Align Selected Rotation Z To Active"""
    bl_idname = "tp_display.align_rotation_z"
    bl_label = "Align Selected Rotation Z To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        RotZ(context)
        return {'FINISHED'}


class TP_Display_Align_Scale_All(bpy.types.Operator):
    """Align Selected Scale To Active"""
    bl_idname = "tp_display.align_scale_all"
    bl_label = "Align Selected Scale To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ScaleAll(context)
        return {'FINISHED'}


class TP_Display_Align_Scale_X(bpy.types.Operator):
    """Align Selected Scale X To Active"""
    bl_idname = "tp_display.align_scale_x"
    bl_label = "Align Selected Scale X To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ScaleX(context)
        return {'FINISHED'}


class TP_Display_Align_Scale_Y(bpy.types.Operator):
    """Align Selected Scale Y To Active"""
    bl_idname = "tp_display.align_scale_y"
    bl_label = "Align Selected Scale Y To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ScaleY(context)
        return {'FINISHED'}


class TP_Display_Align_Scale_Z(bpy.types.Operator):
    """Align Selected Scale Z To Active"""
    bl_idname = "tp_display.align_scale_z"
    bl_label = "Align Selected Scale Z To Active"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ScaleZ(context)
        return {'FINISHED'}


## registring
def register():
    bpy.utils.register_module(__name__)

    pass

def unregister():
    bpy.utils.unregister_module(__name__)

    pass

if __name__ == "__main__":
    register()

