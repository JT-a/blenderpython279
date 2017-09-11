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
    "name": "Display Special Menu",
    "author": "Multiple Authors, mkbreuer",
    "version": (0, 1, 1),
    "blender": (2, 7, 2),
    "location": "View3D",
    "description": "Special Menu (W)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Display"}


import bpy
import re
from bpy import *


###### BoolTool ###################

class BoolToolMenu(bpy.types.Menu):
    """BoolTool"""
    bl_label = "BoolTool"
    bl_idname = "wkst.booltool"

    def draw(self, context):
        layout = self.layout

        layout.operator("btool.boolean_union", text="Union Brush", icon="ROTATECOLLECTION")
        layout.operator("btool.boolean_inters", text="Intersection Brush", icon="ROTATECENTER")
        layout.operator("btool.boolean_diff", text="Difference Brush", icon="ROTACTIVE")

        layout.separator()

        layout.operator("btool.boolean_union_direct", text="Union Brush", icon="ROTATECOLLECTION")
        layout.operator("btool.boolean_inters_direct", text="Intersection Brush", icon="ROTATECENTER")
        layout.operator("btool.boolean_diff_direct", text="Difference Brush", icon="ROTACTIVE")

        layout.separator()

        layout.operator("btool.draw_polybrush", icon="LINE_DATA")


#######  Menus Weights  #################

class VIEW3D_Paint_Weight(bpy.types.Menu):
    """Weights"""
    bl_label = "Weights"
    bl_idname = "wkst.weights"

    def draw(self, context):
        layout = self.layout

        layout.operator("paint.weight_from_bones", text="Assign Automatic From Bones").type = 'AUTOMATIC'
        layout.operator("paint.weight_from_bones", text="Assign From Bone Envelopes").type = 'ENVELOPES'

        layout.separator()

        layout.operator("object.vertex_group_normalize_all", text="Normalize All")
        layout.operator("object.vertex_group_normalize", text="Normalize")
        layout.operator("object.vertex_group_mirror", text="Mirror")
        layout.operator("object.vertex_group_invert", text="Invert")

        layout.separator()

        layout.operator("object.vertex_group_clean", text="Clean")
        layout.operator("object.vertex_group_quantize", text="Quantize")
        layout.operator("object.vertex_group_levels", text="Levels")
        layout.operator("object.vertex_group_blend", text="Blend")

        layout.separator()

        layout.operator("object.vertex_group_transfer_weight", text="Transfer Weights")
        layout.operator("object.vertex_group_limit_total", text="Limit Total")
        layout.operator("object.vertex_group_fix", text="Fix Deforms")

        layout.separator()

        layout.operator("paint.weight_set")


class VIEW3D_WeightBrush(bpy.types.Menu):
    """Weight Brushes"""
    bl_label = "Weight Brushes"
    bl_idname = "wkst.weight"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.menu("wkst_vertex", icon='BRUSH_DATA')
        layout.menu("VIEW3D_MT_brush")

bpy.utils.register_class(VIEW3D_WeightBrush)


#######  Menus Armature  #####################

class VIEW3D_MT_EditArmatureTK(bpy.types.Menu):
    """Armature Tools"""
    bl_label = "Armature Tools"
    bl_idname = "wkst.armature"

    def draw(self, context):
        layout = self.layout

        # Edit Armature

        layout.operator("transform.transform", text="Scale Envelope Distance").mode = 'BONE_SIZE'

        layout.operator("transform.transform", text="Scale B-Bone Width").mode = 'BONE_SIZE'

        layout.separator()

        layout.operator("armature.extrude_move")

        layout.operator("armature.extrude_forked")

        layout.operator("armature.duplicate_move")
        layout.operator("armature.merge")
        layout.operator("armature.fill")
        layout.operator("armature.delete")
        layout.operator("armature.separate")

        layout.separator()

        layout.operator("armature.subdivide", text="Subdivide")
        layout.operator("armature.switch_direction", text="Switch Direction")


class VIEW3D_MT_ArmatureName(bpy.types.Menu):
    """Armature Name"""
    bl_label = "Armature Name"
    bl_idname = "wkst.armature_name"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'EXEC_AREA'

        layout.operator("armature.autoside_names", text="AutoName Left/Right").type = 'XAXIS'
        layout.operator("armature.autoside_names", text="AutoName Front/Back").type = 'YAXIS'
        layout.operator("armature.autoside_names", text="AutoName Top/Bottom").type = 'ZAXIS'
        layout.operator("armature.flip_names")


class VIEW3D_MT_ArmatureCut(bpy.types.Menu):
    """Armature Subdivide"""
    bl_label = "Armature Subdivide"
    bl_idname = "wkst.armature_subdivide"

    def draw(self, context):
        layout = self.layout

        layout.operator("armature.subdivide", text="1 Cut").number_cuts = 1
        layout.operator("armature.subdivide", text="2 Cut").number_cuts = 2
        layout.operator("armature.subdivide", text="3 Cut").number_cuts = 3
        layout.operator("armature.subdivide", text="4 Cut").number_cuts = 4
        layout.operator("armature.subdivide", text="5 Cut").number_cuts = 5
        layout.operator("armature.subdivide", text="6 Cut").number_cuts = 6


#######  Menus Pose  ####################

class VIEW3D_MT_PoseCopy(bpy.types.Menu):
    """Pose Copy"""
    bl_label = "Pose Copy"
    bl_idname = "wkst.pose_copy"

    def draw(self, context):
        layout = self.layout

        layout.operator("pose.copy")
        layout.operator("pose.paste")
        layout.operator("pose.paste", text="Paste X-Flipped Pose").flipped = True

        layout.separator()


class VIEW3D_MT_PoseNames(bpy.types.Menu):
    """Pose Copy Name"""
    bl_label = "Pose Copy Name"
    bl_idname = "wkst.pose_copy_name"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'EXEC_AREA'
        layout.operator("pose.autoside_names", text="AutoName Left/Right").axis = 'XAXIS'
        layout.operator("pose.autoside_names", text="AutoName Front/Back").axis = 'YAXIS'
        layout.operator("pose.autoside_names", text="AutoName Top/Bottom").axis = 'ZAXIS'

        layout.operator("pose.flip_names")


#######  AnimationPlayer  ##################

class VIEW3D_AnimationPlayer(bpy.types.Menu):
    """Animation Player"""
    bl_label = "Animation Player"
    bl_idname = "wkst.player"

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


#######  Lock View  #################

class VIEW3D_LockView(bpy.types.Menu):
    bl_label = "Lock View to..."
    bl_idname = "wkst.lockview"

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        view = context.space_data

        layout.label("To Object:")

        layout.prop(view, "lock_object", text="")

        lock_object = view.lock_object
        if lock_object:
            if lock_object.type == 'ARMATURE':
                layout.prop_search(view, "lock_bone", lock_object.data,
                                   "edit_bones" if lock_object.mode == 'EDIT'
                                   else "bones",
                                   text="")
        else:
            layout.prop(view, "lock_cursor", text="Lock to Cursor")

        layout.prop(view, "lock_camera")


#######  Render Menu  #################

class VIEW3D_RenderView(bpy.types.Menu):
    """Render Menu"""
    bl_label = "Render Menu"
    bl_idname = "wkst.rendermenu"

    @classmethod
    def poll(cls, context):
        # add more special types
        return context.object

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        obj = context.object

        layout.operator("render.render", text="Still", icon='RENDER_STILL')
        layout.operator("render.render", text="Animation", icon='RENDER_ANIMATION').animation = True

        layout.separator()

        layout.operator("render.opengl", text="Still_OpenGL", icon='RENDER_STILL')
        layout.operator("render.opengl", text="Anim_OpenGL", icon='RENDER_ANIMATION').animation = True
        layout.menu("INFO_MT_opengl_render")

        layout.separator()

        layout.operator("render.view_show")

        layout.separator()

        props = layout.operator("object.isolate_type_render")
        props = layout.operator("object.hide_render_clear_all")

        layout.separator()

        if not scene.use_preview_range:
            layout.prop(scene, "frame_start", text="Start Frame")
            layout.prop(scene, "frame_end", text="End Frame")
        else:
            layout.prop(scene, "frame_preview_start", text="Start Frame")
            layout.prop(scene, "frame_preview_end", text="End Frame")

        layout.separator()

        view = context.space_data

        layout.prop(view, "use_render_border")
        layout.operator("view3d.render_border", text="Draw Render Border...")


#######  Render Menu  #####################

class VIEW3D_SpecialExtras(bpy.types.Menu):
    """Type Special"""
    bl_label = "Type Special"
    bl_idname = "wkst.specialextras"

    @classmethod
    def poll(cls, context):
        # add more special types
        return context.object

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        obj = context.object

        # layout.separator()

        if obj.type == 'CAMERA':
            layout.operator_context = 'INVOKE_REGION_WIN'

            if obj.data.type == 'PERSP':
                props = layout.operator("wm.context_modal_mouse", text="Camera Lens Angle")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.lens"
                props.input_scale = 0.1
                if obj.data.lens_unit == 'MILLIMETERS':
                    props.header_text = "Camera Lens Angle: %.1fmm"
                else:
                    props.header_text = "Camera Lens Angle: %.1f\u00B0"

            else:
                props = layout.operator("wm.context_modal_mouse", text="Camera Lens Scale")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.ortho_scale"
                props.input_scale = 0.01
                props.header_text = "Camera Lens Scale: %.3f"

            if not obj.data.dof_object:
                #layout.label(text="Test Has DOF obj");
                props = layout.operator("wm.context_modal_mouse", text="DOF Distance")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.dof_distance"
                props.input_scale = 0.02
                props.header_text = "DOF Distance: %.3f"

            layout.separator()

            view3d = context.space_data.region_3d
            cam = context.scene.camera.data

            if view3d.view_perspective == 'CAMERA':
                layout = self.layout

                layout.operator("view3d.render_border_camera", text="Camera as Render Border", icon="FULLSCREEN_ENTER")

                if cam.show_passepartout:
                    layout.prop(cam, "passepartout_alpha", text="Passepartout")
                else:
                    layout.prop(cam, "show_passepartout")

        if obj.type in {'CURVE', 'FONT'}:
            layout.operator_context = 'INVOKE_REGION_WIN'

            props = layout.operator("wm.context_modal_mouse", text="Extrude Size")
            props.data_path_iter = "selected_editable_objects"
            props.data_path_item = "data.extrude"
            props.input_scale = 0.01
            props.header_text = "Extrude Size: %.3f"

            props = layout.operator("wm.context_modal_mouse", text="Width Size")
            props.data_path_iter = "selected_editable_objects"
            props.data_path_item = "data.offset"
            props.input_scale = 0.01
            props.header_text = "Width Size: %.3f"

        if obj.type == 'EMPTY':
            layout.operator_context = 'INVOKE_REGION_WIN'

            props = layout.operator("wm.context_modal_mouse", text="Empty Draw Size")
            props.data_path_iter = "selected_editable_objects"
            props.data_path_item = "empty_draw_size"
            props.input_scale = 0.01
            props.header_text = "Empty Draw Size: %.3f"

        if obj.type == 'LAMP':
            lamp = obj.data

            layout.operator_context = 'INVOKE_REGION_WIN'

            if scene.render.use_shading_nodes:
                try:
                    value = lamp.node_tree.nodes["Emission"].inputs["Strength"].default_value
                except AttributeError:
                    value = None

                if value is not None:
                    props = layout.operator("wm.context_modal_mouse", text="Strength")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.node_tree.nodes[\"Emission\"].inputs[\"Strength\"].default_value"
                    props.header_text = "Lamp Strength: %.3f"
                    props.input_scale = 0.1
                del value

                if lamp.type == 'AREA':
                    props = layout.operator("wm.context_modal_mouse", text="Size X")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.size"
                    props.header_text = "Lamp Size X: %.3f"

                    if lamp.shape == 'RECTANGLE':
                        props = layout.operator("wm.context_modal_mouse", text="Size Y")
                        props.data_path_iter = "selected_editable_objects"
                        props.data_path_item = "data.size_y"
                        props.header_text = "Lamp Size Y: %.3f"

                elif lamp.type in {'SPOT', 'POINT', 'SUN'}:
                    props = layout.operator("wm.context_modal_mouse", text="Size")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.shadow_soft_size"
                    props.header_text = "Lamp Size: %.3f"
            else:
                props = layout.operator("wm.context_modal_mouse", text="Energy")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.energy"
                props.header_text = "Lamp Energy: %.3f"

                if lamp.type in {'SPOT', 'AREA', 'POINT'}:
                    props = layout.operator("wm.context_modal_mouse", text="Falloff Distance")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.distance"
                    props.input_scale = 0.1
                    props.header_text = "Lamp Falloff Distance: %.1f"

            if lamp.type == 'SPOT':
                layout.separator()
                props = layout.operator("wm.context_modal_mouse", text="Spot Size")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.spot_size"
                props.input_scale = 0.01
                props.header_text = "Spot Size: %.2f"

                props = layout.operator("wm.context_modal_mouse", text="Spot Blend")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.spot_blend"
                props.input_scale = -0.01
                props.header_text = "Spot Blend: %.2f"

                if not scene.render.use_shading_nodes:
                    props = layout.operator("wm.context_modal_mouse", text="Clip Start")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.shadow_buffer_clip_start"
                    props.input_scale = 0.05
                    props.header_text = "Clip Start: %.2f"

                    props = layout.operator("wm.context_modal_mouse", text="Clip End")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.shadow_buffer_clip_end"
                    props.input_scale = 0.05
                    props.header_text = "Clip End: %.2f"


def register():
    bpy.utils.register_class(BoolToolMenu)
    bpy.utils.register_class(VIEW3D_Paint_Weight)
    bpy.utils.register_class(VIEW3D_MT_EditArmatureTK)
    bpy.utils.register_class(VIEW3D_MT_ArmatureName)
    bpy.utils.register_class(VIEW3D_MT_ArmatureCut)
    bpy.utils.register_class(VIEW3D_MT_PoseCopy)
    bpy.utils.register_class(VIEW3D_MT_PoseNames)

    bpy.utils.register_class(VIEW3D_AnimationPlayer)
    bpy.utils.register_class(VIEW3D_LockView)
    bpy.utils.register_class(VIEW3D_RenderView)
    bpy.utils.register_class(VIEW3D_SpecialExtras)

    # bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_class(BoolToolMenu)
    bpy.utils.unregister_class(VIEW3D_Paint_Weight)
    bpy.utils.unregister_class(VIEW3D_MT_EditArmatureTK)
    bpy.utils.unregister_class(VIEW3D_MT_ArmatureName)
    bpy.utils.unregister_class(VIEW3D_MT_ArmatureCut)
    bpy.utils.unregister_class(VIEW3D_MT_PoseCopy)
    bpy.utils.unregister_class(VIEW3D_MT_PoseNames)

    bpy.utils.unregister_class(VIEW3D_AnimationPlayer)
    bpy.utils.unregister_class(VIEW3D_LockView)
    bpy.utils.unregister_class(VIEW3D_RenderView)
    bpy.utils.unregister_class(VIEW3D_SpecialExtras)

    # bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
