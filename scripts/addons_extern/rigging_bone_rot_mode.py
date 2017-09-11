'''
Bone Rotation Modes

Changes a bone(s) rotation mode based on user input.

Usage:
    After installing the addon, (normal installation), it can be enabled
    under User Prefences -> Addons -> Rigging -> Bone Rotation Mode. Once
    enabled, selecting an armature object and entering pose mode, a new
    panel will appear in the tool shelf called - 'Change Bone's Rotation
    Mode' - that will give you the options to use this tool.

    Options:
        Selected Bones - A check box, when enabled this addon will only
        work on selected bones, otherwise it will work on all bones in
        the current armature object.

        Rotation Mode - The rotation mode you wish to change the bone(s)
        to.

        Change Rotation Mode - Invokes this script and changes the rotation
        mode of the bone(s) and indicated in the above 2 parameters.

1/4/2014:
    First initial alpha release. All the functionality that I desire from
    this addon is there and working. This is only considered an alpha
    release because it's not been tested by anyone other than myself.

1/5/2014:
    Added 'undo' to the script. Now when you change a bone(s) rotation
    it can be undone by CTRL-Z, likewise, CTRL-Y works as well.
'''


import bpy

# debug flag - if True, prints data to console
debug = 0


bl_info = {
    "name": "Bone Rotation Modes",
    "author": "revolt_randy",
    "version": (0, 1, 1),
    "blender": (2, 6, 9),
    "location": "3D View -> Tool Shelf",
    "description": "Converts rotation mode of bones based on user input",
    "warning": "Alpha release. Armature must be in Pose mode for this addon to appear in the tool shelf.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"}


class BoneRotationPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_Bone_Rotation"
    bl_label = "Change Bone's Rotation Mode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Animation"

    @classmethod
    def poll(self, context):
        # check mode
        return (
            context.active_object and
            context.active_object.type == "ARMATURE" and
            context.mode == "POSE"
        )

    def draw(self, context):
        wm = bpy.context.window_manager
        layout = self.layout

        row = layout.row()
        row.prop(wm, "selected_bones")
        row = layout.row()
        row.prop(wm, "rotation_mode")
        row = layout.row()
        row.operator("rotationbones.op")


class ChangeRotationOperator(bpy.types.Operator):
    bl_idname = "rotationbones.op"
    bl_label = "Change Rotation Mode"
    bl_description = "Change the rotation mode of Bones in the current" + \
        " Armature depending on user selected options."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wm = bpy.context.window_manager

        if debug:
            print("\nrotation_mode = ", wm.rotation_mode,
                  "  selected bones =", wm.selected_bones)

        # determine what bones to work on & get listing of bones
        if wm.selected_bones:
            bone_text = context.selected_pose_bones
        else:
            armature_name = context.object.name
            bone_text = bpy.data.armatures[armature_name].bones

        if debug:
            for index in bone_text:
                print(index.name)

        # loop thru the bones, changing the rotation mode of them
        for index in bone_text:
            context.object.pose.bones[index.name].rotation_mode = wm.rotation_mode

        return {"FINISHED"}


bpy.types.WindowManager.selected_bones = bpy.props.BoolProperty(
    name='Selected Bones',
    default=False,
    description='Only change rotation mode of selected bones.')

bpy.types.WindowManager.rotation_mode = bpy.props.EnumProperty(
    name='Rotation Mode',
    description='Rotation mode to set bone to',
    default='QUATERNION',
    items=[
        ("QUATERNION", "Quaternion (WXYZ)", "Quaternion rotation - w,x,y,z"),
        ("XYZ", "XYZ Euler", "X, Y, Z rotation order"),
        ("XZY", "XZY Euler", "X, Z, Y rotation order"),
        ("YXZ", "YXZ Euler", "Y, X, Z rotation order"),
        ("YZX", "YZX Euler", "Y, Z, X rotation order"),
        ("ZXY", "ZXY Euler", "Z, X, Y rotation order"),
        ("ZYX", "ZYX Euler", "Z, Y, X rotation order"),
        ("AXIS_ANGLE", "Axis Angle", "Axis Angle (W+XYZ), " +
         "defines a rotation around some axis defined by 3D-Vector")])


def register():
    bpy.utils.register_class(BoneRotationPanel)
    bpy.utils.register_class(ChangeRotationOperator)


def unregister():
    bpy.utils.unregister_class(BoneRotationPanel)
    bpy.utils.unregister_class(ChangeRotationOperator)


if __name__ == "__main__":
    register()
