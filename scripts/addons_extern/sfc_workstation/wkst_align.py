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
#    "name": "Workstation Mesh Align",
#    "author": "mkbreuer",
#    "version": (0, 1, 0),
#    "blender": (2, 76, 0),
#    "location": "View3D > Toolbar > Panel",
#    "warning": "",
#    "description": "Mesh Align Operator for the Main Panel",
#    "wiki_url": "",
#    "category": ""Workstation",
#}


import bpy
from bpy import*

#######  Menus  ######################


class S_ALIGN_LOC_Menu(bpy.types.Menu):
    """Align Location"""
    bl_label = "Align Location"
    bl_idname = "align.location_menu"

    def draw(self, context):
        layout = self.layout

        layout.label("Align Location", icon='MAN_TRANS')

        layout.separator()

        layout.operator("object.align_location_all", text="All Axis")

        layout.separator()

        layout.operator("object.align_location_x", text="-> X")
        layout.operator("object.align_location_y", text="-> Y")
        layout.operator("object.align_location_z", text="-> Z")

        # layout.separator()

        #layout.operator("object.location_clear", text="Clear", icon="X")
        #props = layout.operator("object.transform_apply", text="Apply",icon="FILE_TICK")
        #props.location= True
        #props.rotation= False
        #props.scale= False


bpy.utils.register_class(S_ALIGN_LOC_Menu)


class S_ALIGN_ROTA_Menu(bpy.types.Menu):
    """Align Rotation"""
    bl_label = "Align Rotation"
    bl_idname = "align.rotation_menu"

    def draw(self, context):
        layout = self.layout

        layout.label("Align Rotation", icon='MAN_ROT')

        layout.separator()

        layout.operator("object.align_rotation_all", text="All Axis")

        layout.separator()

        layout.operator("object.align_rotation_x", text="-> X")
        layout.operator("object.align_rotation_y", text="-> Y")
        layout.operator("object.align_rotation_z", text="-> Z")

        # layout.separator()

        #layout.operator("object.rotation_clear", text="Clear", icon="X")
        #props = layout.operator("object.transform_apply", text="Apply",icon="FILE_TICK")
        #props.location= False
        #props.rotation= True
        #props.scale= False

bpy.utils.register_class(S_ALIGN_ROTA_Menu)


class S_ALIGN_SCALE_Menu(bpy.types.Menu):
    """Align Scale"""
    bl_label = "Align Scale"
    bl_idname = "align.scale_menu"

    def draw(self, context):
        layout = self.layout

        layout.label("Align Scale", icon='MAN_SCALE')

        layout.separator()

        layout.operator("object.align_objects_scale_all", text="All Axis")

        layout.separator()

        layout.operator("object.align_objects_scale_x", text="-> X")
        layout.operator("object.align_objects_scale_y", text="-> Y")
        layout.operator("object.align_objects_scale_z", text="-> Z")

        # layout.separator()

        #layout.operator("object.scale_clear", text="Clear", icon="X")
        #props = layout.operator("object.transform_apply", text="Apply",icon="FILE_TICK")
        #props.location= False
        #props.rotation= False
        #props.scale= True

bpy.utils.register_class(S_ALIGN_SCALE_Menu)


#######  Align Transform  ########

class AlignLocMenu(bpy.types.Menu):
    """Location XYZ-Axis"""
    bl_label = "Location XYZ-Axis"
    bl_idname = "wkst.alignlocmenu"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mesh = context.active_object.data

        layout.operator("object.align_location_x", text="Loc X-Axis")
        layout.operator("object.align_location_y", text="Loc Y-Axis")
        layout.operator("object.align_location_z", text="Loc Z-Axis")

bpy.utils.register_class(AlignLocMenu)


class AlignRotMenu(bpy.types.Menu):
    """Rotation XYZ-Axis"""
    bl_label = "Rotation XYZ-Axis"
    bl_idname = "wkst.alignrotmenu"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mesh = context.active_object.data

        layout.operator("object.align_location_x", text="Loc X-Axis")
        layout.operator("object.align_location_y", text="Loc Y-Axis")
        layout.operator("object.align_location_z", text="Loc Z-Axis")

bpy.utils.register_class(AlignRotMenu)


class AlignScaleMenu(bpy.types.Menu):
    """Scale XYZ-Axis"""
    bl_label = "Scale XYZ-Axis"
    bl_idname = "wkst.alignscalemenu"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mesh = context.active_object.data

        layout.operator("object.align_location_x", text="Loc X-Axis")
        layout.operator("object.align_location_y", text="Loc Y-Axis")
        layout.operator("object.align_location_z", text="Loc Z-Axis")

bpy.utils.register_class(AlignScaleMenu)


##### Mesh Align XY / XZ / YZ  ###

class alignxy(bpy.types.Operator):
    """align selected to XY-axis / depend by pivot"""
    bl_label = "align selected face to XY axis"
    bl_idname = "mesh.face_align_xy"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.resize(value=(0, 0, 1), constraint_axis=(True, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}


class alignxz(bpy.types.Operator):
    """align selected to XZ-axis / depend by pivot"""
    bl_label = "align xz"
    bl_idname = "mesh.face_align_xz"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.resize(value=(0, 1, 0), constraint_axis=(True, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}


class alignyz(bpy.types.Operator):
    """align selected to yz-axis / depend by pivot"""
    bl_label = "align yz"
    bl_idname = "mesh.face_align_yz"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.resize(value=(1, 0, 0), constraint_axis=(False, True, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}


#####  Mesh Align X / Y / Z  ####

class alignx(bpy.types.Operator):
    """align selected to X-axis / depend by pivot"""
    bl_label = "align selected face to X axis"
    bl_idname = "mesh.face_align_x"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}


class aligny(bpy.types.Operator):
    """align selected to Y-axis / depend by pivot"""
    bl_label = "align y"
    bl_idname = "mesh.face_align_y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.resize(value=(1, 0, 1), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}


class alignz(bpy.types.Operator):
    """align selected to Z-axis / depend by pivot"""
    bl_label = "align z"
    bl_idname = "mesh.face_align_z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}


# registering and menu integration
def register():

    bpy.utils.register_module(__name__)


# unregistering and removing menus
def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
