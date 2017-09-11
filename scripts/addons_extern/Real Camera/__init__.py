# Addon Info
bl_info = {
    "name": "Real Camera",
    "description": "Physical Camera Controls",
    "author": "Wolf",
    "version": (2, 1),
    "blender": (2, 78, 0),
    "location": "Properties > Camera",
    "wiki_url": "http://www.3d-wolf.com/camera.html",
    "tracker_url": "http://www.3d-wolf.com/camera.html",
    "support": "COMMUNITY",
    "category": "Render"
    }


# Import
import bpy
import os
import mathutils
import bmesh
import math
from bpy.props import *
from mathutils import Vector
from . import addon_updater_ops


#Panel###############################################################
class RealCameraPanel(bpy.types.Panel):

    # Create a Panel in the Camera Properties
    bl_category = "Real Camera"
    bl_label = "Real Camera"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return context.camera and context.scene.render.engine == 'CYCLES'

    def draw_header(self, context):
        settings = context.scene.camera_settings
        layout = self.layout
        layout.prop(settings, 'enabled', text='')
        
    def draw(self, context):
        addon_updater_ops.check_for_update_background(context)
        settings = context.scene.camera_settings
        layout = self.layout
        layout.enabled = settings.enabled

        row = layout.row()
        row.prop(settings, 'ae')
        if settings.ae:
            row = layout.row()
            row.prop(settings, 'ev')
            row = layout.row()
            row.scale_y = 1.5
            row.operator("wm.url_open", text="Chart", icon='IMAGEFILE').url = "https://drive.google.com/open?id=1p0YmKZp-6n1nqBO5xNmbhCAMoZOTHi_83Zx5B4uubmo"
        else:
            split = layout.split()
            col = split.column(align=True)
            col.prop(settings, 'aperture')
            row = col.row(align=True)
            row.prop(settings, 'shutter_speed')
            col.prop(settings, 'iso')

        row = layout.row()
        row.prop(settings, 'af')
        sub = row.row(align=True)
        sub.active = settings.af
        if settings.af:
            sub.prop(settings, 'af_bake', icon='PLAY', text="Bake")
            sub.prop(settings, 'af_step', text="Step")
        split = layout.split()
        col = split.column(align=True)
        col.prop(settings, 'zoom')
        if not settings.af:
            col.prop(settings, 'focus_point')

        # EV
        if not settings.ae:
            ev = update_exposure_value(self, context)
            ev = str(ev)
            row = col.row(align=True)
            row.alignment = 'CENTER'
            row.label("Exposure Value: " + ev, icon='LAMP_SUN')

        addon_updater_ops.update_notice_box_ui(self, context)


#Update##############################################################

# Update Toggle
def toggle_update(self, context):
    settings = context.scene.camera_settings

    if settings.enabled:
        # Change Name
        name = "Real Camera"
        bpy.context.object.data.name = name
        bpy.context.object.name = name

        # Check if the scene is an Animation
        auto_shutter(self, context)

        # Set Limits
        bpy.data.cameras[name].show_limits = True
        # Set Metric System
        bpy.context.scene.unit_settings.system = 'METRIC'
        # Change Aperture to FSTOP
        bpy.data.cameras[name].cycles.aperture_type = 'FSTOP'
        # Initial Values Issue
        update_aperture(self, context)
        update_shutter_speed(self, context)
        update_iso(self, context)
        update_zoom(self, context)
        update_focus_point(self, context)

    else:
        # Change Name
        name = "Camera"
        bpy.context.object.data.name = name
        bpy.context.object.name = name

        # Reset Limits
        bpy.data.cameras[name].show_limits = False
        # Change Aperture to RADIUS
        bpy.data.cameras[name].cycles.aperture_type = 'RADIUS'
        # Reset AutoFocus
        bpy.context.scene.camera_settings.af = False
        # Reset Motion Blur
        bpy.context.scene.render.use_motion_blur = False

# Update Auto Focus
def update_af(self, context):
    af = context.scene.camera_settings.af
    
    if af:
        o = bpy.data.objects["Real Camera"]

        # Ray Cast
        ray = bpy.context.scene.ray_cast(o.location, o.matrix_world.to_quaternion() * Vector((0.0, 0.0, -1.0)) )
        distance = (ray[1]-o.location).magnitude
        bpy.data.cameras["Real Camera"].dof_distance = distance

    else:
        # Reset DOF
        bpy.context.object.data.dof_distance = bpy.context.scene.camera_settings.focus_point

# Update AF Bake
def update_af_bake(self, context):
    scene = bpy.context.scene
    bake = scene.camera_settings.af_bake
    # Number of Frames
    start = scene.frame_start
    end = scene.frame_end
    frames = end-start+1
    steps = scene.camera_settings.af_step
    n = int(float(frames/steps))
    # Get current frame and Current Frame = Start
    current_frame = scene.frame_current
    scene.frame_current = start
    cam = bpy.data.cameras["Real Camera"]

    if bake:
        # Every Step frames, place a Keyframe
        for i in range(n+1):
            update_af(self, context)
            cam.keyframe_insert('dof_distance')
            scene.frame_set(scene.frame_current+steps)

    else:
        # Delete all the Keyframes
        fcurv = cam.animation_data.action.fcurves
        for c in fcurv:
            if c.data_path.startswith("dof_distance"):
                fcurv.remove(c)

    # Current Frame
    scene.frame_current = current_frame

# Update EV for the write
def update_exposure_value(self, context):
    settings = bpy.context.scene.camera_settings
    A = settings.aperture
    S = settings.shutter_speed
    I = settings.iso
    EV = math.log((100*(A*A)/(I*S)), 2)
    EV = round(EV, 2)
    return EV

# Update EV
def update_ev(self, context):
    ae = context.scene.camera_settings.ae
    settings = bpy.context.scene.camera_settings
    if not ae:
        A = settings.aperture
        S = settings.shutter_speed
        I = settings.iso
        EV = math.log((100*(A*A)/(I*S)), 2)
        EV = round(EV, 2)
    else:
        EV = settings.ev
    # Filmic
    filmic = -0.68*EV+5.95
    bpy.context.scene.view_settings.exposure = filmic
    
# Update Aperture
def update_aperture(self, context):
    bpy.context.object.data.cycles.aperture_fstop = bpy.context.scene.camera_settings.aperture
    update_ev(self, context)
# Update Shutter Speed
def update_shutter_speed(self, context):
    scene = bpy.context.scene
    fps = scene.render.fps
    value = scene.camera_settings.shutter_speed
    motion = fps*value
    scene.render.motion_blur_shutter = motion
    update_ev(self, context)
# Update ISO
def update_iso(self, context):
    update_ev(self, context)
# Update Zoom
def update_zoom(self, context):
    bpy.context.object.data.lens = bpy.context.scene.camera_settings.zoom
# Update Focus Point
def update_focus_point(self, context):
    bpy.context.object.data.dof_distance = bpy.context.scene.camera_settings.focus_point

# Time Label in the Timeline
def time_info(self, context):
    layout = self.layout
    scene = context.scene
    row = layout.row(align=True)

    # Check for preview range
    frame_start = scene.frame_preview_start if scene.use_preview_range else scene.frame_start
    frame_end = scene.frame_preview_end if scene.use_preview_range else scene.frame_end

    cur_frame = bpy.utils.smpte_from_frame(scene.frame_current - frame_start)
    fin_frame = bpy.utils.smpte_from_frame(frame_end - frame_start)
    cur_frame = str(cur_frame)
    fin_frame = str(fin_frame)
    cur_frame = cur_frame[3:]
    fin_frame = fin_frame[3:]

    row.label(text=cur_frame + " / " + fin_frame)

# Auto Shutter Speed Activator
def auto_shutter(self, context):
    ob_list = [obj for obj in bpy.context.scene.objects]
    keyframes = []
    for obj in ob_list:
        anim = obj.animation_data
        if anim is not None and anim.action is not None:
            for fcu in anim.action.fcurves:
                for keyframe in fcu.keyframe_points:
                    x, y = keyframe.co
                    if x not in keyframes:
                        keyframes.append((math.ceil(x)))
    keys = len(keyframes)
    if keys>=2:
        bpy.context.scene.render.use_motion_blur = True
    else:
        bpy.context.scene.render.use_motion_blur = False

#Settings############################################################

class CameraSettings(bpy.types.PropertyGroup):
    
    # Toggle
    enabled = bpy.props.BoolProperty(
        name = "Enabled",
        description = "Enable Real Camera",
        default = False,
        update = toggle_update
    )
    
    # Exposure Triangle
    aperture = bpy.props.FloatProperty(
        name = "Aperture",
        description = "Depth of Field",
        min = 0.5,
        max = 128,
        step = 10,
        precision = 1,
        default = 5.6,
        update = update_aperture
    )

    shutter_speed = bpy.props.FloatProperty(
        name = "Shutter Speed",
        description = "Motion Blur",
        min = 0.000001,
        max = float('inf'),
        step = 0.1,
        precision = 3,
        default = 0.05,
        update = update_shutter_speed
    )

    iso = bpy.props.IntProperty(
        name = "ISO",
        description = "Exposure",
        min = 1,
        max = 102400,
        default = 100,
        update = update_iso
    )

    ae = bpy.props.BoolProperty(
        name = "Auto Exposure",
        description = "Enable Auto Exposure",
        default = False,
        update = update_ev
    )

    ev = bpy.props.FloatProperty(
        name = "EV",
        description = "Exposure Value: look at the Chart",
        min = -100,
        max = 100,
        step = 1,
        precision = 2,
        default = 15,
        update = update_ev
    )

    # Mechanics
    af = bpy.props.BoolProperty(
        name = "Autofocus",
        description = "Enable Autofocus",
        default = False,
        update = update_af
    )

    af_bake = bpy.props.BoolProperty(
        name = "Autofocus Baking",
        description = "Bake Autofocus for the entire Animation",
        default = False,
        update = update_af_bake
    )

    af_step = bpy.props.IntProperty(
        name = "Step",
        description = "Every Step frames insert a keyframe",
        min = 1,
        max = 10000,
        default = 30
    )

    focus_point = bpy.props.FloatProperty(
        name = "Focus Point",
        description = "Focus Point for the DOF",
        min = 0,
        max = float('inf'),
        step = 1,
        precision = 2,
        default = 1,
        unit = 'LENGTH',
        update = update_focus_point
    )

    zoom = bpy.props.FloatProperty(
        name = "Focal Length",
        description = "Zoom",
        min = 1,
        max = float('inf'),
        step = 1,
        precision = 2,
        default = 35,
        update = update_zoom
    )


############################################################################################################

# Preferences
class RealCameraPreferences(bpy.types.AddonPreferences):

    bl_idname = __package__

    # addon updater preferences from `__init__`, be sure to copy all of them
    auto_check_update = bpy.props.BoolProperty(
    name = "Auto-check for Update",
    description = "If enabled, auto-check for updates using an interval",
    default = True,
    )
    updater_intrval_months = bpy.props.IntProperty(
    name='Months',
    description = "Number of months between checking for updates",
    default=0,
    min=0
    )
    updater_intrval_days = bpy.props.IntProperty(
    name='Days',
    description = "Number of days between checking for updates",
    default=1,
    min=0,
    )
    updater_intrval_hours = bpy.props.IntProperty(
    name='Hours',
    description = "Number of hours between checking for updates",
    default=0,
    min=0,
    max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
    name='Minutes',
    description = "Number of minutes between checking for updates",
    default=0,
    min=0,
    max=59
    )

    def draw(self, context):
        layout = self.layout
        addon_updater_ops.update_settings_ui(self, context)

# Register
def register():
    
    addon_updater_ops.register(bl_info)
    bpy.utils.register_class(RealCameraPreferences)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.camera_settings = bpy.props.PointerProperty(type=CameraSettings)
    bpy.types.TIME_HT_header.append(time_info)

# Unregister
def unregister():

    bpy.utils.unregister_class(RealCameraPreferences)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.camera_settings
    bpy.types.TIME_HT_header.remove(time_info)


if __name__ == "__main__":
    register()
