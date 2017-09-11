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
#
# ***** END GPL LICENCE BLOCK *****


import bpy
from bpy import *


###########  Menu  #######################

class WKST_Transform_Menu(bpy.types.Menu):
    """Transform Menu"""
    bl_label = "Transform Menu"
    bl_idname = "wkst.transform_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("transform.translate", text="Translate", icon="MAN_TRANS")
        layout.operator("transform.rotate", text="Rotate", icon="MAN_ROT")
        layout.operator("transform.resize", text="Resize", icon="MAN_SCALE")

        if context.mode == 'OBJECT':

            layout.separator()

            layout.menu("VIEW3D_MT_object_clear")
            layout.menu("VIEW3D_MT_object_apply")

         ###space###
        if context.mode == 'EDIT_MESH':

            layout.separator()

            layout.operator("transform.tosphere", "to Sphere")
            layout.operator("transform.push_pull", text="Push/Pull")
            layout.operator("transform.shrink_fatten", text="Shrink Fatten")
            layout.operator('mesh.rot_con', 'Face-Rotation')

            layout.separator()

            layout.operator("transform.shear", text="Shear")
            layout.operator("transform.bend", text="Bend")
            layout.operator("transform.vertex_warp", text="Warp")
            layout.operator("transform.vertex_random", text="Randomize")

            layout.separator()

            layout.operator("transform.translate", text="Move Texture Space").texture_space = True
            layout.operator("transform.resize", text="Scale Texture Space").texture_space = True


########### Freeze Transformation ###########

class Set_Freezetransform(bpy.types.Operator):
    """set transform values to zero"""
    bl_idname = "freeze_transform.selected"
    bl_label = "Freeze Transform"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        str = context.active_object.type
        if str.startswith('EMPTY') or str.startswith('SPEAKER') or str.startswith('CAMERA')or str.startswith('LAMP')or str.startswith('FONT'):
            # Location
            context.active_object.delta_location += context.active_object.location
            context.active_object.location = [0, 0, 0]

            # Rotation

            rotX = bpy.context.active_object.rotation_euler.x
            rotDeltaX = bpy.context.active_object.delta_rotation_euler.x
            bpy.context.active_object.delta_rotation_euler.x = rotX + rotDeltaX

            rotY = bpy.context.active_object.rotation_euler.y
            rotDeltaY = bpy.context.active_object.delta_rotation_euler.y
            bpy.context.active_object.delta_rotation_euler.y = rotDeltaY + rotY

            rotZ = bpy.context.active_object.rotation_euler.z
            rotDeltaZ = bpy.context.active_object.delta_rotation_euler.z
            bpy.context.active_object.delta_rotation_euler.z = rotDeltaZ + rotZ

            rquatW = context.active_object.rotation_quaternion.w
            rquatX = context.active_object.rotation_quaternion.x
            rquatY = context.active_object.rotation_quaternion.y
            rquatZ = context.active_object.rotation_quaternion.z

            drquatW = context.active_object.delta_rotation_quaternion.w
            drquatX = context.active_object.delta_rotation_quaternion.x
            drquatY = context.active_object.delta_rotation_quaternion.y
            drquatZ = context.active_object.delta_rotation_quaternion.z

            context.active_object.delta_rotation_quaternion.w = 1.0
            context.active_object.delta_rotation_quaternion.x = rquatX + drquatX
            context.active_object.delta_rotation_quaternion.y = rquatY + drquatY
            context.active_object.delta_rotation_quaternion.z = rquatZ + drquatZ

            context.active_object.rotation_quaternion.w = 1.0
            context.active_object.rotation_quaternion.x = 0.0
            context.active_object.rotation_quaternion.y = 0.0
            context.active_object.rotation_quaternion.z = 0.0

            bpy.context.active_object.rotation_euler.x = 0
            bpy.context.active_object.rotation_euler.y = 0
            bpy.context.active_object.rotation_euler.z = 0

            # Scale
            context.active_object.delta_scale.x += (context.active_object.scale.x - 1) * context.active_object.delta_scale.x
            context.active_object.delta_scale.y += (context.active_object.scale.y - 1) * context.active_object.delta_scale.y
            context.active_object.delta_scale.z += (context.active_object.scale.z - 1) * context.active_object.delta_scale.z
            context.active_object.scale = [1, 1, 1]

            return {'FINISHED'}
        else:
            context.active_object.delta_location += context.active_object.location
            context.active_object.location = [0, 0, 0]
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            return {'FINISHED'}


######  Transform Orientation  ##################################################################

class spaceGlobal(bpy.types.Operator):
    """Transform Orientation Global"""
    bl_idname = "space.global"
    bl_label = "Transform Orientation Global"
    bl_options = {'REGISTER'}

    def execute(self, context):

        bpy.context.space_data.transform_orientation = 'GLOBAL'
        return {'FINISHED'}

bpy.utils.register_class(spaceGlobal)


class spaceLOCAL(bpy.types.Operator):
    """Transform Orientation LOCAL"""
    bl_idname = "space.local"
    bl_label = "Transform Orientation LOCAL"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'LOCAL'
        return {'FINISHED'}

bpy.utils.register_class(spaceLOCAL)


class spaceNORMAL(bpy.types.Operator):
    """Transform Orientation NORMAL"""
    bl_idname = "space.normal"
    bl_label = "Transform Orientation NORMAL"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'NORMAL'
        return {'FINISHED'}

bpy.utils.register_class(spaceNORMAL)


class spaceGIMBAL(bpy.types.Operator):
    """Transform Orientation GIMBAL"""
    bl_idname = "space.gimbal"
    bl_label = "Transform Orientation GIMBAL"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'GIMBAL'
        return {'FINISHED'}

bpy.utils.register_class(spaceGIMBAL)


class spaceVIEW(bpy.types.Operator):
    """Transform Orientation VIEW"""
    bl_idname = "space.view"
    bl_label = "Transform Orientation VIEW"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'VIEW'
        return {'FINISHED'}

bpy.utils.register_class(spaceVIEW)


######  Snap Target  ##################################################################

class snapACTIVE(bpy.types.Operator):
    """Snap Target ACTIVE"""
    bl_idname = "snap.active"
    bl_label = "Snap Target ACTIVE"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        return {'FINISHED'}

bpy.utils.register_class(snapACTIVE)


class snapMEDIAN(bpy.types.Operator):
    """Snap Target MEDIAN"""
    bl_idname = "snap.median"
    bl_label = "Snap Target MEDIAN"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'MEDIAN'
        return {'FINISHED'}

bpy.utils.register_class(snapMEDIAN)


class snapCENTER(bpy.types.Operator):
    """Snap Target CENTER"""
    bl_idname = "snap.center"
    bl_label = "Snap Target CENTER"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'CENTER'
        return {'FINISHED'}

bpy.utils.register_class(snapCENTER)


class snapCLOSEST(bpy.types.Operator):
    """Snap Target CLOSEST"""
    bl_idname = "snap.closest"
    bl_label = "Snap Target CLOSEST"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        return {'FINISHED'}

bpy.utils.register_class(snapCLOSEST)


######  Snap Element  ##################################################################

class snaepVOLUME(bpy.types.Operator):
    """Snap Element VOLUME"""
    bl_idname = "snape.volume"
    bl_label = "Snap Element VOLUME"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VOLUME'
        return {'FINISHED'}

bpy.utils.register_class(snaepVOLUME)


class snaepFACE(bpy.types.Operator):
    """Snap Element FACE"""
    bl_idname = "snape.face"
    bl_label = "Snap Element FACE"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'FACE'
        return {'FINISHED'}

bpy.utils.register_class(snaepFACE)


class snaepEDGE(bpy.types.Operator):
    """Snap Element EDGE"""
    bl_idname = "snape.edge"
    bl_label = "Snap Element EDGE"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'EDGE'
        return {'FINISHED'}

bpy.utils.register_class(snaepEDGE)


class snaepVERTEX(bpy.types.Operator):
    """Snap Element VERTEX"""
    bl_idname = "snape.vertex"
    bl_label = "Snap Element VERTEX"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        return {'FINISHED'}

bpy.utils.register_class(snaepVERTEX)


class snaepINCREMENT(bpy.types.Operator):
    """Snap Element INCREMENT"""
    bl_idname = "snape.increment"
    bl_label = "Snap Element INCREMENT"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'INCREMENT'
        return {'FINISHED'}

bpy.utils.register_class(snaepINCREMENT)


# Menus Proportional  #######-------------------------------------------------------

class ProportionalMenu(bpy.types.Menu):
    """Proportional Menu"""
    bl_label = "Proportional Menu"
    bl_idname = "proportionalmenu"

    def draw(self, context):
        layout = self.layout
        view = context.space_data
        obj = context.active_object
        toolsettings = context.tool_settings

        layout.prop(toolsettings, "use_proportional_edit_objects", text="on/off", icon_only=True)

        if toolsettings.use_proportional_edit_objects:
            layout.prop(toolsettings, "proportional_edit_falloff", icon_only=True)

        layout.prop(toolsettings, "proportional_edit", icon_only=True)

bpy.utils.register_class(ProportionalMenu)


# Menus Apply / Clear  #######-------------------------------------------------------


class VIEW3D_ApplyandClear(bpy.types.Menu):
    """Apply & Clear Setup"""
    bl_label = "Apply & Clear Setup"
    bl_idname = "wkst.applyclear_transform"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mesh = context.active_object.data

        layout.label("Apply Transform", icon="FILE_TICK")

        props = layout.operator("object.transform_apply", text=" Move", icon="RIGHTARROW_THIN")
        props.location = True
        props.rotation = False
        props.scale = False

        props = layout.operator("object.transform_apply", text=" Rotation", icon="RIGHTARROW_THIN")
        props.location = False
        props.rotation = True
        props.scale = False

        props = layout.operator("object.transform_apply", text=" Scale", icon="RIGHTARROW_THIN")
        props.location = False
        props.rotation = False
        props.scale = True

        layout.separator()

        layout.operator("object.visual_transform_apply", text="Visual Transform")
        layout.operator("object.duplicates_make_real", text="Real Duplicate")

        layout.separator()

        layout.label("Clear Transform", icon="X")

        layout.operator("object.location_clear", text=" Move")
        layout.operator("object.rotation_clear", text=" Rotation")
        layout.operator("object.scale_clear", text=" Scale")

        layout.separator()

        layout.operator("object.location_clear", text="Origin", icon="LAYER_ACTIVE")

bpy.utils.register_class(VIEW3D_ApplyandClear)


class VIEW3D_PoseApplyClear(bpy.types.Menu):
    """Apply & Clear"""
    bl_label = "Apply & Clear"
    bl_idname = "wkst.applyclearpose"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Apply Pose", icon="PMARKER")

        layout.operator("pose.armature_apply", text="Pose as Rest Pose")

        layout.operator("pose.visual_transform_apply", text="Visual as Pose")

        layout.separator()

        layout.label(text="Clear Pose", icon="PANEL_CLOSE")

        layout.operator("pose.loc_clear", text="Location")
        layout.operator("pose.rot_clear", text="Rotation")
        layout.operator("pose.scale_clear", text="Scale")
        layout.operator("pose.transforms_clear", text="Clear All Pose")

        layout.separator()

        layout.operator("pose.user_transforms_clear", text="Reset unkeyed")

bpy.utils.register_class(VIEW3D_PoseApplyClear)


######------------################################################################################################################
######  Registry  ################################################################################################################

def abs(val):
    if val > 0:
        return val
    return -val


def register():

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
