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

bl_info = {
    "name": "Display View & Camera Menu",
    "author": "Multiple Authors, mkbreuer",
    "version": (0, 1, 0),
    "blender": (2, 7, 2),
    "location": "View3D",
    "description": "[ALT+ONE] Tools for View & Camera",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Display"}


import bpy
from bpy import *


#######  AnimationPlayer  ###################

class VIEW3D_AnimationPlayer(bpy.types.Menu):
    """Animation Player"""
    bl_label = "Animation Player"
    bl_idname = "wkst.animation_player"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        toolsettings = context.tool_settings
        screen = context.screen

        layout.operator("screen.frame_jump", text="Jump REW", icon='REW').end = False
        layout.operator("screen.keyframe_jump", text="Previous FR", icon='PREV_KEYFRAME').next = False
        layout.operator("screen.animation_play", text="Reverse", icon='PLAY_REVERSE').reverse = True

        layout.operator("screen.animation_play", text="PLAY", icon='PLAY')

        layout.operator("screen.animation_play", text="Stop", icon='PAUSE')

        layout.operator("screen.keyframe_jump", text="Next FR", icon='NEXT_KEYFRAME').next = True
        layout.operator("screen.frame_jump", text="Jump FF", icon='FF').end = True

bpy.utils.register_class(VIEW3D_AnimationPlayer)


#######  3D Navigation  ################

class VIEW3D_3DNaviMenu(bpy.types.Menu):
    """3D Navigation"""
    bl_label = "3D Navigation"
    bl_idname = "wkst.3dnavimenu"

    def draw(self, context):
        layout = self.layout

        layout.menu("navimenu", text="View Rotation", icon="NDOF_TURN")

        layout.separator()

        layout.operator("view3d.viewnumpad", text="Camera").type = 'CAMERA'
        layout.operator("view3d.viewnumpad", text="Top").type = 'TOP'
        layout.operator("view3d.viewnumpad", text="Bottom").type = 'BOTTOM'
        layout.operator("view3d.viewnumpad", text="Front").type = 'FRONT'
        layout.operator("view3d.viewnumpad", text="Back").type = 'BACK'
        layout.operator("view3d.viewnumpad", text="Right").type = 'RIGHT'
        layout.operator("view3d.viewnumpad", text="Left").type = 'LEFT'

        layout.separator()

        layout.menu("VIEW3D_MT_view_align_selected", text="View around Active")

bpy.utils.register_class(VIEW3D_3DNaviMenu)


#######  Render Border  ################

class VIEW3D_BorderMenu(bpy.types.Menu):
    """Border..."""
    bl_label = "Border..."
    bl_idname = "wkst.bordermenu"

    def draw(self, context):
        layout = self.layout
        view = context.space_data

        layout.prop(view, "use_render_border", text="Render Border")
        layout.operator("view3d.render_border", text="Draw Render Border...")
        layout.operator("view3d.clip_border", text="Draw Clipping Border...")

bpy.utils.register_class(VIEW3D_BorderMenu)


#######  Camera View  #####################

class VIEW3D_CameraViewMenu(bpy.types.Menu):
    """Camera View"""
    bl_label = "Camera View"
    bl_idname = "wkst.cameraviewmenu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.camera_add")

        layout.separator()

        layout.operator("view3d.zoom_camera_1_to_1", text="Zoom Camera 1:1")

        layout.separator()

        layout.operator("view3d.viewnumpad", text="Active Camera").type = 'CAMERA'
        layout.operator("view3d.object_as_camera")

        layout.operator("view3d.camera_to_view", text="Align Active Camera to View")
        layout.operator("view3d.camera_to_view_selected", text="Align Active Camera to Selected")

        layout.separator()

        layout.operator("object.build_dolly_rig")
        layout.operator("object.build_crane_rig")

bpy.utils.register_class(VIEW3D_CameraViewMenu)


#######  Navigation  ################

class VIEW3D_NaviMenu(bpy.types.Menu):
    """Navigation"""
    bl_label = "Navigation"
    bl_idname = "wkst.navimenu"

    def draw(self, context):
        from math import pi
        layout = self.layout

        layout.operator_enum("view3d.view_orbit", "type")

        layout.separator()

        layout.operator("view3d.view_roll", text="Roll Left").angle = pi / -12.0
        layout.operator("view3d.view_roll", text="Roll Right").angle = pi / 12.0

        layout.separator()

        layout.operator_enum("view3d.view_pan", "type")

        layout.separator()

        layout.operator("view3d.zoom", text="Zoom In").delta = 1
        layout.operator("view3d.zoom", text="Zoom Out").delta = -1

bpy.utils.register_class(VIEW3D_NaviMenu)


#######  Lock View  #################

class VIEW3D_LockMenu(bpy.types.Menu):
    """Lock View"""
    bl_label = "Lock View"
    bl_idname = "wkst.lockmenu"

    def draw(self, context):
        layout = self.layout
        view = context.space_data

        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("view3d.view_lock_to_active")
        layout.operator("view3d.view_lock_clear")

        layout.separator()

        layout.label(text="View to Object:")
        layout.prop(view, "lock_object", text="")

bpy.utils.register_class(VIEW3D_LockMenu)


######  View & Cam Menu  #################

class VIEW3D_CamViewMenu(bpy.types.Menu):
    """View & Camera"""
    bl_label = "View & Camera"
    bl_idname = "wkst.cam_menu"

    def draw(self, context):
        from math import pi
        layout = self.layout
        view = context.space_data

        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("view3d.view_all", icon="VIEWZOOM")
        layout.operator("view3d.view_center_cursor", text="View to Cursor")
        layout.operator("view3d.view_selected", text="View to Selected")
        layout.operator("view3d.zoom_border", text="Zoom with Border", icon="BORDERMOVE")

        layout.separator()

        layout.operator("view3d.localview", text="View Global/Local")
        layout.operator("view3d.view_persportho", text="View Persp/Ortho")

        layout.separator()
        layout.menu("VIEW3D_MT_object_showhide", icon="RESTRICT_VIEW_OFF")
        layout.operator("view3d.layers", text="Show All Layers").nr = 0

        layout.separator()

        layout.operator("lookat.it", text="Look @ Obj")
        layout.operator("lookat.cursor", text="Look @ Cursor")

        layout.separator()

        layout.menu("bordermenu", icon="RENDER_REGION")
        layout.menu("cameraviewmenu", icon="OUTLINER_DATA_CAMERA")

        layout.separator()

        layout.menu("3dnavimenu", icon="MANIPUL")

        layout.menu("lockmenu")

        layout.separator()

        layout.menu("htk_player", text="Animation Player", icon="TRIA_RIGHT")

        layout.separator()

        layout.operator("view3d.fly", icon="RIGHTARROW_THIN")
        layout.operator("view3d.walk", icon="RIGHTARROW_THIN")


######  Registry  ##############################

def register():

    bpy.utils.register_class(VIEW3D_CamViewMenu)

    # bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_class(VIEW3D_CamViewMenu)

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
