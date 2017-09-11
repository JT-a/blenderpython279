#____________________________________________________________________________|
#  Thanks to Frankie Hobbins, Joel Daniels, Julien Duroure,
# Hjalti Hjalmarsson, Bassam Kurdali, Luciano Munoz, Cristian Hasbun,
# and anyone that I left out!
#
# Latest update: Rethinking the amount of tools and interface.
# Removed tools that are better left to hotkeys.
# Will add preferences of hotkeys later.
#     "support": "TESTING",

bl_info = {
    "name": "Animator's Toolbox",
    "description": "A set of tools specifically for animators.",
    "author": "Brandon Ayers (thedaemon)",
    "version": (0, 5, 2),
    "blender": (2, 78, 0),
    "location": "View3D > Toolbar > Animation > Animator's Toolbox",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/thedaemon/Blender-Scripts",
    "tracker_url": "https://github.com/thedaemon/Blender-Scripts/issues",
    "category": "Animation"
}

import bpy
from bpy.props import BoolProperty, IntProperty
from bpy.types import Operator, PropertyGroup, Panel

KEYMAPS = list()


# FEATURE: Jump forward/backward every N frames. Currently hardcoded variable.
# the frame jump amount needs to be in preferences along with hotkey selector (viewer?)
class AnimatorsToolboxFrameJump(Operator):
    """Jump a number of frames forward/backwards"""
    bl_idname = "screen.animatorstools_frame_jump"
    bl_label = "Jump Frames"
    forward = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        scene = context.scene
        framedelta = 4
        if self.forward:
            scene.frame_current = scene.frame_current + framedelta
        else:
            scene.frame_current = scene.frame_current - framedelta
        return {"FINISHED"}


# FEATURE: A toggle to keep the animator from selecting something other
# than the Armature.
class ToggleSelectability(Operator):
    """
    Turns off selection for all objects
    leaving only Armatures selectable
    """
    bl_idname = "bone.toggleselectability"
    bl_label = "Armature Selection Only"

    def execute(self, context):
        do_i_hide_select = not bpy.context.active_object.hide_select
        if bpy.context.selected_objects == []:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    ob.hide_select = True
            else:
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        ob.hide_select = do_i_hide_select
        else:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        do_i_hide_select2 = not ob.hide_select
                        for ob in bpy.context.scene.objects:
                            ob.hide_select = do_i_hide_select2
                        break
                bpy.context.object.hide_select = False
            else:
                for ob in bpy.context.selected_objects:
                    ob.hide_select = not ob.hide_select
        return{'FINISHED'}


# Useless because blender already has this freaking command but I programmed
# it anyways. I may use it for specific axis template.
class ClearAllTransforms(Operator):
    """Clears all transforms on the bone I hope"""
    bl_idname = "pose.clearall"
    bl_label = "Clear Transforms"

    def execute(self, context):
        for object in bpy.data.objects:
            if object.type == 'ARMATURE':
                bpy.ops.pose.rot_clear()
                bpy.ops.pose.loc_clear()
                bpy.ops.pose.scale_clear()
        return{'FINISHED'}


# FEATURE: A toggle for OpenSubdiv on all objects in scene with a Subdivision
# Surface Modifier.
class ToggleOpensubdiv(Operator):
    """
    Toggles OpenSubdiv for all Objects for
    improved animation playback speed
    """
    bl_idname = "mesh.opensubdiv"
    bl_label = "Mesh OpenSubdiv"

    def execute(self, context):
        for mm in (m for o in bpy.context.scene.objects
                   for m in o.modifiers if m.type == 'SUBSURF'):
            if mm.use_opensubdiv is True:
                mm.use_opensubdiv = False
            else:
                if mm.use_opensubdiv is False:
                    mm.use_opensubdiv = True
        return{'FINISHED'}


# Feature: Turns OpenSubdiv on for all meshes with Subdivision Surface
# Modifiers for improved viewport performance.
class OpensubdivOn(Operator):
    bl_idname = "opensubdiv.on"
    bl_label = "OpenSubdiv On"

    def execute(self, context):
        for mm in (m for o in bpy.context.scene.objects
                   for m in o.modifiers if m.type == 'SUBSURF'):
            mm.use_opensubdiv = True
        return{'FINISHED'}


# Feature: Turns OpenSubdiv on for all meshes with Subdivision Surface
# Modifiers for improved viewport performance.
class OpensubdivOff(Operator):
    bl_idname = "opensubdiv.off"
    bl_label = "OpenSubdiv Off"

    def execute(self, context):
        for mm in (m for o in bpy.context.scene.objects
                   for m in o.modifiers if m.type == 'SUBSURF'):
            mm.use_opensubdiv = False
        return{'FINISHED'}


# FEATURE: Simple X-Ray toggle for Armature
class ToggleXray(Operator):
    """Toggles X-Ray mode for bones"""
    bl_idname = "bone.togglexray"
    bl_label = "Armature X-Ray"

    def execute(self, context):
        for object in bpy.data.objects:
            if object.type == 'ARMATURE':
                object.show_x_ray = not object.show_x_ray
        return{'FINISHED'}


# FEATURE: Simple Auto-IK toggle for Armature
# context.active_object.data, "use_auto_ik", text="Auto IK")
class ToggleAutoIK(Operator):
    """Toggles Auto IK mode for bones"""
    bl_idname = "bone.toggleautoik"
    bl_label = "Armature Auto IK"

    def execute(self, context):
        for object in bpy.data.active_object:
            if object.type == 'ARMATURE':
                object.use_auto_ik = not object.use_auto_ik
        return{'FINISHED'}


class QuickMotionPath(Operator):
    """Create motion path by preview range"""
    bl_label = "Calculate"
    bl_idname = "cenda.motion_pats"

    def execute(self, context):
        if(bpy.context.scene.use_preview_range):
            startFrame = bpy.context.scene.frame_preview_start
            endFrame = bpy.context.scene.frame_preview_end
        else:
            startFrame = bpy.context.scene.frame_start
            endFrame = bpy.context.scene.frame_end
        bpy.ops.pose.paths_calculate(start_frame=startFrame, end_frame=endFrame, bake_location='TAILS')
        return{'FINISHED'}


# UI --

class animatorstoolboxData(PropertyGroup):
    """
    UI property group for the add-on  WORK IN PROGRESS
    Options to adjust how the panel is displayed.
    bpy > types > WindowManager > animatorstoolboxDataUI
    bpy > context > window_manager > animatorstoolboxDataUI
    """
    bl_idname = 'animatorstoolboxDataUI'
    displayMode = BoolProperty(
        name='Display Mode', description="Use"
        "this to hide many of the options below that"
        "are generally needed while rigging."
        "(Useful for animating.)",
        default=False)
    deformOptions = BoolProperty(
        name='Deform Options',
        description="Display the deform options for this bone.",
        default=False)
    breakdowner_percentage = IntProperty(
        name='Breakdowner Percentage',
        description=' a percentage for the Breakdowner Button.',
        default=50,
        min=0,
        max=100)


def draw_animatorstoolbox_panel(context, layout):
    scene = context.scene
    screen = context.screen
    render = scene.render
    cscene = scene.cycles
    object = context.object
    toolsettings = context.tool_settings
    userpref = context.user_preferences
    edit = userpref.edit
    #
    col = layout.column(align=True)
    row = col.row(align=True)
    box = row.box()
    box.operator("pose.transforms_clear", text="Reset All")
    
#    box.operator("show_x_ray", text="X-Ray")
    box.operator("bone.toggleselectability", text="Select Armature Only")

    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("pose.copy", text="Copy")
    row.operator("pose.paste", text="Paste").flipped = False
    row.operator("pose.paste", text="Flip").flipped = True

    col = layout.column(align=True)
    row = col.row(align=True)
    row.prop(toolsettings, "use_keyframe_insert_auto", text="", toggle=True)
    if toolsettings.use_keyframe_insert_auto:
        row.prop(toolsettings, "use_keyframe_insert_keyingset",
                 text="", toggle=True)
        if screen.is_animation_playing:
            subsub = row.row()
            subsub.prop(toolsettings, "use_record_with_nla", toggle=True)
    row.prop_search(scene.keying_sets_all, "active", scene, "keying_sets_all", text="")

    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("pose.relax", text="Relax")
    row.operator("pose.breakdown", text="Tween")
    row.operator("pose.push", text="Push")
    # row.prop(scene, 'breakdowner_percentage', slider=True )

    #--Motion Path
    pchan = context.active_pose_bone
    mpath = pchan.motion_path if pchan else None
    col = layout.column(align=True)
    col.label(text="Paths Preview Range:")
    if mpath:
        row = col.row(align=True)
        row.operator("pose.paths_update", text="Update")
        row.operator("pose.paths_clear", text="", icon='X')
    else:
        # col.operator("pose.paths_calculate", text="Calculate")
        col.operator("cenda.motion_pats", icon='ANIM_DATA')
    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("opensubdiv.on", text="OpenSubdiv")
    row.operator("opensubdiv.off", text="Off")
    col.separator()

    #--Simplify
    # col = layout.column(align=True)
    # col.label(text="Simplify:")
    col = layout.column(align=True)
    row = col.row(align=True)
    row.prop(render, "use_simplify", text="Simplify")
    row = col.row(align=True)
    row.prop(render, "simplify_subdivision", text="Subdivision")

    #--New Key Type
    col.separator()
    col = layout.column(align=True)
    row = col.row()
    row.prop(edit, "keyframe_new_interpolation_type", text="", icon_only=False)
    row = col.row()
    row.prop(edit, "keyframe_new_handle_type", text="", icon_only=False)
    row = col.row()
    row.prop(toolsettings, "keyframe_type", text="", icon_only=False)


class AnimatorsToolBox(Panel):
    """Creates a custom Animator Panel in the 3D View"""
    bl_label = "Animator's Toolbox"
    bl_idname = "ANIM_TOOLBOX"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Animate"

    #--Header
    def draw_header(self, context):
        layout = self.layout
        # animatorstoolboxDataUIProps = context.window_manager.animatorstoolboxDataUI
        # layout.prop('animatorstoolboxDataUI', "displayMode", text="")
        DoButton = self.layout
        DoButton.operator('bs.doboom', text='', icon='RENDER_ANIMATION')

    #--Draw Toolboxes
    def draw(self, context):
        layout = self.layout
        draw_animatorstoolbox_panel(context, layout)


classes = (
    AnimatorsToolboxFrameJump,
    ToggleSelectability,
    ClearAllTransforms,
    ToggleOpensubdiv,
    OpensubdivOn,
    OpensubdivOff,
    ToggleXray,
    ToggleAutoIK,
    QuickMotionPath,
    animatorstoolboxData,
    AnimatorsToolBox
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    #---KeyMaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name="Frames")
    kmi = km.keymap_items.new(
        "screen.animatorstools_frame_jump",
        "RIGHT_ARROW", "PRESS", shift=True)
    kmi.properties.forward = True
    KEYMAPS.append((km, kmi))
    kmi = km.keymap_items.new(
        "screen.animatorstools_frame_jump",
        "LEFT_ARROW", "PRESS", shift=True)
    kmi.properties.forward = False
    KEYMAPS.append((km, kmi))
    #---New Preferences Tab Apply after Blender Restart FIX
    #--update_panel(None, bpy.context)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
    #---KeyMaps
    for km, kmi in KEYMAPS:
        km.keymap_items.remove(kmi)
    KEYMAPS.clear()


if __name__ == "__main__":
    register()
