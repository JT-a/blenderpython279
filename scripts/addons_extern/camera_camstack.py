"""
    CamStack is used to create a hierarchy of cameras for the express purpose of creating handheld camera motion.

    New: Create a new stack at scene origin based on parameters given in the CamStack panel.
    Generate: Create a stack based on selected camera(s) and their data. Safe to use with existing animation.
    Split (for use with an existing stack): Make current camera single-user and
    link all child cameras to the split camera.

    Normal animation goes on camera objects. _main is the standard layout pass for
    basic moves and composition. _handheld1 is the first layer of lower-frequency
    handheld motion. _handheld2 is the second layer. _shake1 is the first layer of
    high-frequency shake (vibrations, turbulence, etc.). _shake2 is the second layer.
    Second layers are not always necessary, but provide an easy way to add animation
    non-destructively. Look through each camera to see its effect on the shot.

    Focal length and focus are on the camera data. When linked, all changes
    in this data will propagate to the other cameras. Split cameras to enable
    further tweaking of these parameters.

    _global_move_control is used to reposition or scale the stack to fit a scene
    after animation has been made. For example, the animator spends a week on
    a shot, then set dressing or the plate change the scene.
    Transform _global_move_control to reposition the cameras
    while maintaining camera animation.

    Based on my original Maya script here: https://github.com/Italic-/maya-scripts/blob/master/py/cameraStack.py

    This script is licensed under the Apache 2.0 license.
    See details of this license here:
    https://www.apache.org/licenses/LICENSE-2.0

"""

bl_info = {
    'name': 'CamStack',
    'description': 'Create camera hierarchy (stack) for handheld camera motion.',
    'author': 'italic',
    'category': 'Camera',
    'location': '3D View -> Tools (region) -> Tools (tab) -> CamStack',
    'version': (1, 0, 0),
    'blender': (2, 76, 0),
    'tracker_url': 'https://github.com/meta-androcto/blenderpython/issues'
}

import bpy
import logging

from bpy.types import PropertyGroup, Panel, Operator
from bpy.props import StringProperty, FloatProperty, PointerProperty

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
log = logging.getLogger(__name__)


def subCam(context, main_cam, cam_name):
    """Create child cameras linked to main camera."""
    log = logging.getLogger(__name__ + ".subCamLogger")
    log.setLevel('INFO')
    log.info("%s | '%s'", main_cam.name, main_cam.type)

    bpy.ops.object.select_all(action='DESELECT')
    main_cam.select = True
    context.scene.objects.active = main_cam
    log.debug("Active object: '%s'", context.scene.objects.active.name)

    # Handheld1 - Set properties, locks and axes
    bpy.ops.object.duplicate(linked=True)
    handheld1 = context.object
    handheld1.animation_data_clear()
    handheld1.name = cam_name + "_handheld1"
    handheld1.parent = main_cam
    handheld1.rotation_mode = 'XYZ'
    handheld1.lock_rotation[0:3] = (False, False, True)
    handheld1.location = (0, 0, 0)
    handheld1.rotation_euler = (0, 0, 0)
    handheld1.scale = (0.9, 0.9, 0.9)
    log.debug("Handheld1: '%s', Parent: '%s'", handheld1.name, handheld1.parent.name)
    log.info("%s | '%s'", handheld1.name, handheld1.type)

    # Handheld2
    bpy.ops.object.duplicate(linked=True)
    handheld2 = context.object
    handheld1.animation_data_clear()
    handheld2.name = cam_name + "_handheld2"
    handheld2.parent = handheld1
    handheld2.location = (0, 0, 0)
    handheld2.rotation_euler = (0, 0, 0)
    handheld2.scale = (0.9, 0.9, 0.9)
    log.debug("Handheld2: '%s', Parent: '%s'", handheld2.name, handheld2.parent.name)
    log.info("%s | '%s'", handheld2.name, handheld2.type)

    # Shake1
    bpy.ops.object.duplicate(linked=True)
    shake1 = context.object
    handheld1.animation_data_clear()
    shake1.name = cam_name + "_shake1"
    shake1.parent = handheld2
    shake1.location = (0, 0, 0)
    shake1.rotation_euler = (0, 0, 0)
    shake1.scale = (0.9, 0.9, 0.9)
    log.debug("Shake1: '%s', Parent: '%s'", shake1.name, shake1.parent.name)
    log.info("%s | '%s'", shake1.name, shake1.type)

    # Shake2
    bpy.ops.object.duplicate(linked=True)
    shake2 = context.object
    handheld1.animation_data_clear()
    shake2.name = cam_name + "_shake2"
    shake2.parent = shake1
    shake2.location = (0, 0, 0)
    shake2.rotation_euler = (0, 0, 0)
    shake2.scale = (0.9, 0.9, 0.9)
    log.debug("Shake2: '%s', Parent: '%s'", shake2.name, shake2.parent.name)
    log.info("%s | '%s'", shake2.name, shake2.type)

    log.debug("Finished subcams.")


class VIEW3D_OT_camstack_new(Operator):
    """Create a new camera stack from parameters in CamStack panel."""

    bl_idname = 'camstack.new'
    bl_label = 'New'
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        csp = context.camstack_props
        layout = self.layout
        col = layout.column()
        col.prop(csp, 'cam_name')
        col.prop(csp, 'focal_len')

    def execute(self, context):
        log = logging.getLogger(__name__ + ".newLogger")
        log.setLevel('INFO')
        log.info("Creating new stack from given parameters.\n")

        sc = context.scene
        csp = sc.camstack_props
        cam_name = csp.cam_name
        focal_len = csp.focal_len

        log.debug(
            "\nName: %s \nFocal Length: %s \nExpected names: [%s %s %s %s %s %s]\n",
            cam_name, focal_len,
            cam_name + "_cam_move_all",
            cam_name + "_main",
            cam_name + "_handheld1",
            cam_name + "_handheld2",
            cam_name + "_shake1",
            cam_name + "_shake2"
        )

        if cam_name == "":
            log.error("Camera name required.")
            self.report({'ERROR'}, "Camera name required")
            return {'CANCELLED'}
        else:
            pass

        # Global move control
        bpy.ops.curve.primitive_nurbs_circle_add(
            radius=1.0,
            view_align=False,
            enter_editmode=False,
            location=(0.0, 0.0, 0.0),
            rotation=(0.0, 0.0, 0.0),  # Radians
        )
        global_move = context.object
        global_move.data.use_path = False
        global_move.name = cam_name + "_cam_move_all"
        log.debug("Global move control: '%s' | '%s'", global_move.name, global_move.type)

        # Master camera
        bpy.ops.object.camera_add(
            view_align=False,
            location=(0.0, 0.0, 0.0),
            rotation=(1.5707964, 0.0, 0.0),  # Radians
        )
        main_cam = context.object
        main_cam.data.name = cam_name
        main_cam.data.lens = focal_len
        main_cam.name = cam_name + "_main"
        main_cam.parent = global_move
        log.debug("Master camera: '%s' | '%s'", main_cam.name, main_cam.type)

        subCam(context, main_cam, cam_name)

        bpy.ops.object.select_all(action='DESELECT')
        main_cam.select = True
        context.scene.objects.active = main_cam
        context.scene.update()

        log.info("Complete\n")

        return {'FINISHED'}


class VIEW3D_OT_camstack_generator(Operator):
    """Generate a stack based on the selected camera(s)."""

    bl_idname = 'camstack.gen'
    bl_label = 'Generate'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene.objects.active)

    def execute(self, context):
        log = logging.getLogger(__name__ + ".genLogger")
        log.setLevel('INFO')

        sel = context.selected_objects

        cam_list = []

        for item in sel:
            if item.type == 'CAMERA':
                cam_list.append(item)
            else:
                continue

        if cam_list != []:
            log.debug("List: %s", str(cam_list))

            for item in cam_list:
                log.info("Generating stack from existing camera(s).")

                main_cam = item
                cam_name = item.name

                log.debug(
                    "\nName: %s \nFocal Length: %s \nExpected names: [%s %s %s %s %s %s]\n",
                    cam_name, item.data.lens,
                    cam_name + "_cam_move_all",
                    cam_name + "_main",
                    cam_name + "_handheld1",
                    cam_name + "_handheld2",
                    cam_name + "_shake1",
                    cam_name + "_shake2"
                )

                bpy.ops.curve.primitive_nurbs_circle_add(
                    radius=1.0,
                    view_align=False,
                    enter_editmode=False,
                    location=(0.0, 0.0, 0.0),
                    rotation=(0.0, 0.0, 0.0),  # Radians
                )
                global_move = context.object
                global_move.data.use_path = False
                global_move.name = cam_name + "_cam_move_all"
                log.debug("Global move control: '%s' | '%s'", global_move.name, global_move.type)

                item.parent = global_move
                item.data.name = cam_name
                item.name = cam_name + "_main"
                log.debug("Master camera: '%s' | '%s'", main_cam.name, main_cam.type)

                subCam(context, main_cam, cam_name)

        else:
            log.error("Select a camera.")
            self.report({'ERROR'}, "Select a camera")
            return {'CANCELLED'}

        context.scene.update()

        log.info("Complete\n")

        return {'FINISHED'}


class VIEW3D_OT_camstack_split(Operator):
    """Make current camera data single user; further children use new camera data."""

    bl_idname = 'camstack.split'
    bl_label = "Split"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene.objects.active and context.scene.objects.active.type == 'CAMERA')

    def execute(self, context):
        log = logging.getLogger(__name__ + ".splitLogger")
        log.setLevel('INFO')
        log.info("Splitting camera datablock.")

        current_cam = context.scene.objects.active
        log.debug("%s | %s | %s", current_cam.type, current_cam.name, current_cam)

        # Make selected camera data single user
        bpy.ops.object.make_single_user(
            type='SELECTED_OBJECTS',
            object=False,
            obdata=True,
            animation=False
        )
        current_cam.data.name = current_cam.name

        # Change all child cameras to new copy
        bpy.ops.object.select_all(action='DESELECT')
        context.scene.objects.active = current_cam
        bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
        current_cam.select = True
        context.scene.objects.active = current_cam
        bpy.ops.object.make_links_data(type='OBDATA')
        log.debug("Cameras: %s \nUsing new data: %s", context.selected_objects, current_cam.data.name)

        context.scene.update()

        log.info("Complete\n")

        return {'FINISHED'}


class VIEW3D_PT_camstack(Panel):
    bl_label = 'CamStack'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        csp = context.scene.camstack_props

        layout = self.layout
        layout.prop(csp, "cam_name")
        layout.prop(csp, "focal_len")
        row = layout.row()
        row.operator('camstack.new')
        row.operator('camstack.gen')
        row.operator('camstack.split')


class CamStack_prop_group(PropertyGroup):
    cam_name = StringProperty(
        name="Name",
        description="Name prefix to give camera stack",
        default="shot",
        maxlen=0
    )

    focal_len = FloatProperty(
        name='Focal Length',
        description='Focal length for each camera',
        default=35.0,
        min=0.01,
        precision=2
    )


def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.camstack_props = PointerProperty(
        type=CamStack_prop_group, name='CamStack Properties', description='')


def unregister():
    bpy.utils.unregister_module(__name__)

    del bpy.types.Scene.camstack_props


if __name__ == '__main__':
    register()
