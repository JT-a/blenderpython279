# Quicktitling -
#   Can be found in the sequence editor properties panel.
#   This will create and edit simple scenes for title overlays.
#   Create Title Scene - This will create a title scene with the settings
#       shown below.
#   Update Title Scene - If an already created title scene is selected,
#       this will apply the current shown settings to that scene.
#   Auto-Update Title - If editing a title, this will change the scene instantly.
#   The top area displays the current QuickTitling preset and gives the ability
#       to select different presets, with options to Copy the current preset,
#       create a New preset, or Delete the selected preset.  The selected
#       preset can be renamed here as well.
#       When a title scene is selected, the preset of that scene will
#       automatically be loaded here.
#   Scene Length - The length in frames of the title scene.
#   Text - Title text.
#   Text Font - A menu of the currently loaded fonts in the blend file.
#   Press the '+' button to load a new font.
#   The following settings change the material on the text directly, and are
#       Not updated automatically.  Click the Update Scene button to see changes.
#   Text Material - A menu of all materials in the blend file.
#       Press the '+' button to create a new material.
#       Use the color square to easily change the color of the current material.
#   Specular is the amount of specular 'shininess' the material has.
#       Hardness determines the sharpness of the specular.
#       The color square on this row is the color of the specular.
#       X/Y Loc - Determines the center point of the text.
#           X of -1 is the left side of the screen, 0 is center, and 1 is right side.
#           Depending on the aspect ratio of the video, the Y location varies.
#           Y location of 0 is always the center, for a 16:9 ratio image (widescreen),
#           .56 will be the top, and -.56 is the bottom.
#   Size - Scale of the text.
#   Extrude Amount - Amount of extrusion to create a 3D look.
#   Bevel Size - Amount of beveling to apply to the text.
#   Bevel Resolution - Subdivisions of the bevel.
#   Shadow Amount - Determines the opacity of the drop shadow.
#       0 is off, 1 is fully dark.
#   Distance - How far away the shadow plane is from the text object, larger
#       values result in a larger shadow, and more exaggerated offset.
#       This must be set higher than 0 for the shadow to be seen if the text
#       is not extruded or beveled.
#   Soft - The amount of blur applied to the drop shadow.  0 is fully sharp,
#       1 is medium softness, this can be increased as much as desired.
#       Higher values will increase render time if not using high quality shadows.
#   X/Y Offset - X and Y offset for the shadow.  The amount of this offset
#       will vary depending on the location of the text.
#   High Quality Shadows - This will switch shadows to ray tracing mode.
#       Shadows will be more accurate and smooth, but render times will increase.
#
#
# Known Bugs:
#   Updating material settings doesnt auto-update scene.  Unfortunately, this may not be possible to fix
#
# Todo:
#   Ability to add multiple objects
#       Objects are stored in a list
#       Object types:
#           Text
#           Box
#           Image
#       All objects need:
#           x - horizontal location, where 0 is center, 1 is right side of screen, -1 is left
#           y - vertical location
#           z - depth location, used for layering, 0 and up
#           scale - adjusted based on z position so it is always relative
#           width - scale multiplier for width, 1 is default
#           height - scale multiplier for height, 1 is default
#           material - material from internal list
#               alpha - transparency value of material
#               diffuse_color - material color
#               specular - specular amount, where 0 is none, 1 is full
#               hardness - hardness of the specular
#               specular_color - color of specular reflection
#           animations - an array of animations to be applied to each object
#       Box and text objects also need:
#           extrude
#           bevel
#           bevel_resolution
#       Text objects only, also need:
#           text
#           font
#           word_wrap
#           wrap_width
#       Image objects only, also need:
#           texture - image or video
#           alpha_texture - texture/video to control transparency
#           video_offset - frame offset for video textures
#
#       Animations are all presets, and one or more can be applied to each object.
#       Each animation has a value for:
#           length - in frames
#           offset - in frames - needs buttons to set it to start and end of title
#           amount - multiplier for how much the animation changes the value
#       Animation presets, each preset has an 'out' version which will reverse the preset
#           Fade - modulates alpha value from 0 to set value
#           Slide Up - slides object from y location of (y-1) to (y)
#           Slide Down - slides object from y location of (y+1) to (y)
#           Slide Right - slides object from x location of (x-1) to (x)
#           Slide Left - slides object from x location of (x+1) to (x)
#
#   Import/export presets
#   Built-in presets (lower third, center, left/right third)
#   Add common animations for each object (slide in with direction, slide out, fade in, fade out, )
#   Overlays in the sequencer viewer to show information about objects (selected object, animations, bounding boxes, layers)
#   Long way into the future if its possible:
#       moving objects in the sequencer viewer (drag/drop)
#
#
# Version History:
#   0.10
#       First stand-alone version, just separated from VSE Quick Functions, no changes
#   0.20
#       Updated interface - made it look better, and its now easier to tell when a scene is being edited
#       When a title scene is edited, changes now happen in realtime
#       Added word-wrapping
#       The values in the interface are now a bit more sane - bevel is multiplied by 100, X location of 1 is the edge of the screen
#       Added shadow offset option
#       Added specular material options
#       Added ability to use ray traced shadows


import bpy
import math
import os
from bpy.app.handlers import persistent


bl_info = {
    "name": "VSE Quick Titling",
    "description": "Enables easy creation of simple title scenes in the VSE",
    "author": "Hudson Barkley (Snu)",
    "version": (0, 2, 0),
    "blender": (2, 77, 0),
    "location": "Sequencer Panels",
    "wiki_url": "none yet",
    "category": "Sequencer"
}


# If the active sequence is a title scene, return that scene, otherwise return the current scene
def find_titling_scene():
    selected = titling_scene_selected()
    if selected:
        return selected
    else:
        return bpy.context.scene

# determines if a titling scene is selected


def titling_scene_selected():
    sequence_editor = bpy.context.scene.sequence_editor
    if hasattr(sequence_editor, 'active_strip'):
        active_sequence = sequence_editor.active_strip
    else:
        active_sequence = None
    if active_sequence == None:
        # if there is no active sequence, this will prevent an error message
        return False
    elif (('QuickTitle: ' in active_sequence.name) & (active_sequence.type == 'SCENE')):
        # the active sequence is probably a quicktitle scene, return that scene
        return active_sequence.scene
    else:
        # the active sequence exists, but its probably not a quicktitle scene, return the current scene
        return False

# Function to return the current QuickTitle preset depending on what is selected in the sequencer


def current_quicktitle():
    scene = find_titling_scene()
    if len(scene.quicktitles) > 0:
        return scene.quicktitles[0]
    else:
        return False

# Function to copy one QuickTitle preset to another


def copy_title_preset(old_title, title):
    title.name = old_title.name
    title.shadowsize = old_title.shadowsize
    title.shadowamount = old_title.shadowamount
    title.shadowsoft = old_title.shadowsoft
    title.shadowx = old_title.shadowx
    title.shadowy = old_title.shadowy
    title.length = old_title.length
    title.qualityshadows = old_title.qualityshadows
    title.objects.clear()
    for oldobject in old_title.objects:
        newobject = title.objects.new()
        newobject.name = oldobject.name
        newobject.type = oldobject.type
        newobject.x = oldobject.x
        newobject.y = oldobject.y
        newobject.z = oldobject.z
        newobject.scale = oldobject.scale
        newobject.width = oldobject.width
        newobject.height = oldobject.height
        newobject.material = oldobject.material
        newobject.alpha = oldobject.alpha
        newobject.diffuse_color = oldobject.diffuse_color
        newobject.specular = oldobject.specular
        newobject.hardness = oldobject.hardness
        newobject.specular_color = oldobject.specular_color
        newobject.extrude = oldobject.extrude
        newobject.bevel = oldobject.bevel
        newobject.bevel_resolution = oldobject.bevel_resolution
        newobject.text = oldobject.text
        newobject.font = oldobject.font
        newobject.word_wrap = oldobject.word_wrap
        newobject.wrap_width = oldobject.wrap_width
        newobject.texture = oldobject.texture
        newobject.alpha_texture = oldobject.alpha_texture
        newobject.video_offset = oldobject.video_offset
        newobject.animations.clear()
        for oldanimation in oldobject.animations:
            newanimation = newobject.animations.new()
            newanimation.preset = oldanimation.preset
            newanimation.length = oldanimation.length
            newanimation.offset = oldanimation.offset
            newanimation.amount = oldanimation.amount


# Auto update function called when changing settings
def quicktitle_autoupdate(self=None, context=None):
    if bpy.context.scene.quicktitler.autoupdate:
        # Determine if a titler sequence is selected
        try:
            sequence = bpy.context.scene.sequence_editor.active_strip
            if (('QuickTitle: ' in sequence.name) & (sequence.type == 'SCENE')):
                quicktitle = current_quicktitle()
                quicktitle_update(sequence, quicktitle)
        except:
            pass


# Function to update a QuickTitle sequence
def quicktitle_update(sequence, quicktitle):
    # todo
    # attempt to find the objects that need to be updated
    scene = sequence.scene
    text = None
    shadow = None
    shadowLamp = None

    for object in scene.objects:
        if (object.type == 'FONT'):
            text = object
        if ("QuickTitlerShadow" in object.name):
            shadow = object
        if ("QuickTitlerLamp" in object.name):
            shadowLamp = object
    if ((text == None) or (shadow == None) or (shadowLamp == None)):
        print('Selected Title Scene Is Incomplete')
        self.report({'WARNING'}, 'Selected Title Scene Is Incomplete')
        return

    name = "QuickTitle: " + quicktitle.text

    # Scene update
    scene.frame_end = quicktitle.length
    index = bpy.data.materials.find(quicktitle.material)
    if (index >= 0):
        text.data.materials.clear()
        text.data.materials.append(bpy.data.materials[index])
        material = bpy.data.materials[index]
    else:
        material = bpy.data.materials.new('QuickTitler Material')
        quicktitle.material = material.name
    text.data.size = quicktitle.size / 10
    text.data.extrude = quicktitle.extrude / 10
    text.data.bevel_depth = quicktitle.bevel / 100
    text.data.bevel_resolution = quicktitle.bevelres
    text.data.body = quicktitle.text
    text.data.font = bpy.data.fonts[quicktitle.font]
    offsety = text.data.size / 2
    offsetz = text.dimensions[2] / 2
    text.location = (quicktitle.x, quicktitle.y - offsety, 0)
    if quicktitle.wrap:
        box_size = 2
        text.data.text_boxes[0].width = box_size * quicktitle.wrapwidth
        text.data.text_boxes[0].x = -(box_size / 2) * quicktitle.wrapwidth
    else:
        text.data.text_boxes[0].width = 0
        text.data.text_boxes[0].x = 0
    shadow.material_slots[0].material.alpha = quicktitle.shadowamount
    softshadow = quicktitle.shadowsoft * 40
    shadowLamp.data.shadow_buffer_soft = softshadow
    if softshadow >= 40:
        shadowLamp.data.shadow_buffer_samples = 8
        shadowLamp.data.shadow_ray_samples = 8
    elif softshadow >= 20:
        shadowLamp.data.shadow_buffer_samples = 6
        shadowLamp.data.shadow_ray_samples = 6
    elif softshadow > 0:
        shadowLamp.data.shadow_buffer_samples = 4
        shadowLamp.data.shadow_ray_samples = 4
    else:
        shadowLamp.data.shadow_buffer_samples = 1
        shadowLamp.data.shadow_ray_samples = 1

    shadowLamp.data.shadow_soft_size = quicktitle.shadowsoft
    shadowLamp.location = (-quicktitle.shadowx, quicktitle.shadowy + offsety, shadowLamp.location[2])
    if quicktitle.shadowamount > 0:
        if quicktitle.qualityshadows:
            shadowLamp.data.shadow_method = 'RAY_SHADOW'
        else:
            shadowLamp.data.shadow_method = 'BUFFER_SHADOW'
    else:
        shadowLamp.data.shadow_method = 'NOSHADOW'
    shadow.location = (0, 0, -(quicktitle.shadowsize / 8) - offsetz)
    scene.name = name
    sequence.name = name
    scene.quicktitles[0].name = name
    bpy.ops.sequencer.reload(adjust_length=True)
    bpy.ops.sequencer.refresh_all()

# Function to create QuickTitle scenes and sequences


def quicktitle_create(quicktitle):
    # todo
    scene = bpy.context.scene
    name = "QuickTitle: " + quicktitle.text

    # Basic scene setup
    bpy.ops.scene.new(type='EMPTY')
    title_scene = bpy.context.scene
    title_scene.name = name
    title_scene.frame_end = quicktitle.length
    title_scene.layers = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    title_scene.render.engine = 'BLENDER_RENDER'
    title_scene.render.alpha_mode = 'TRANSPARENT'
    title_scene.render.image_settings.file_format = 'PNG'
    title_scene.render.image_settings.color_mode = 'RGBA'
    title_scene.quicktitles.clear()
    title_scene.quicktitles.add()
    copy_title_preset(quicktitle, title_scene.quicktitles[0])
    title_scene.quicktitles[0].name = name

    # Text setup
    bpy.ops.object.text_add()
    text = bpy.context.scene.objects.active
    text.scale[0] = 1
    text.scale[1] = 1
    text.scale[2] = 1
    text.data.align = 'CENTER'
    text.name = "QuickTitlerText"

    # Camera setup
    bpy.ops.object.camera_add()
    camera = bpy.context.scene.objects.active
    title_scene.camera = camera
    camera.location = ((0, 0, 2.16))
    camera.name = "QuickTitlerCamera"

    # Basic lamps setup
    lampEnergy = 0.25
    bpy.ops.object.lamp_add(location=(-.5, -.27, .5))
    lamp1 = bpy.context.scene.objects.active
    lamp1.data.energy = lampEnergy
    lamp1.data.shadow_method = 'NOSHADOW'
    lamp1.parent = text
    bpy.ops.object.lamp_add(location=(.5, -.27, .5))
    lamp2 = bpy.context.scene.objects.active
    lamp2.data.energy = lampEnergy
    lamp2.data.shadow_method = 'NOSHADOW'
    lamp2.parent = text
    bpy.ops.object.lamp_add(location=(-.5, .5, .5))
    lamp3 = bpy.context.scene.objects.active
    lamp3.data.energy = lampEnergy
    lamp3.data.shadow_method = 'NOSHADOW'
    lamp3.parent = text
    bpy.ops.object.lamp_add(location=(.5, .5, .5))
    lamp4 = bpy.context.scene.objects.active
    lamp4.data.energy = lampEnergy
    lamp4.data.shadow_method = 'NOSHADOW'
    lamp4.parent = text

    # Shadow lamp setup
    bpy.ops.object.lamp_add(type='SPOT', location=(0, 0, 1))
    shadowLamp = bpy.context.scene.objects.active
    shadowLamp.name = 'QuickTitlerLamp'
    shadowLamp.parent = text
    shadowLamp.data.use_only_shadow = True
    shadowLamp.data.use_specular = False
    shadowLamp.data.distance = 3
    shadowLamp.data.shadow_ray_samples = 4
    shadowLamp.data.shadow_soft_size = 0
    shadowLamp.data.shadow_method = 'BUFFER_SHADOW'
    shadowLamp.data.shadow_buffer_type = 'REGULAR'
    shadowLamp.data.shadow_buffer_soft = 10
    shadowLamp.data.shadow_buffer_bias = 0.1
    shadowLamp.data.shadow_buffer_size = 4096
    shadowLamp.data.shadow_buffer_samples = 4
    shadowLamp.data.shadow_sample_buffers = 'BUFFERS_4'
    shadowLamp.data.shadow_buffer_clip_end = 4
    shadowLamp.data.spot_size = 2.6
    shadowLamp.data.use_square = True

    # Shadow setup
    bpy.ops.mesh.primitive_plane_add(radius=3)
    shadow = bpy.context.scene.objects.active
    shadow.name = "QuickTitlerShadow"
    shadow.draw_type = 'WIRE'
    shadowMaterial = bpy.data.materials.new('QuickTitlerShadow')
    shadowMaterial.diffuse_color = (0, 0, 0)
    shadowMaterial.diffuse_intensity = 1
    shadowMaterial.specular_intensity = 0
    shadowMaterial.use_transparency = True
    shadowMaterial.use_cast_buffer_shadows = False
    shadowMaterial.shadow_only_type = 'SHADOW_ONLY'
    shadowMaterial.use_only_shadow = True
    shadow.data.materials.append(shadowMaterial)

    # Add scene to sequencer
    bpy.context.screen.scene = scene
    bpy.ops.sequencer.scene_strip_add(frame_start=scene.frame_current, scene=title_scene.name)
    sequence = bpy.context.scene.sequence_editor.active_strip
    sequence.name = name
    sequence.blend_type = 'ALPHA_OVER'
    scene = title_scene


class QuickTitleObject(bpy.types.PropertyGroup):
    # Basic variables for all types:
    name = bpy.props.StringProperty(
        name="Object Name",
        description="Identifier for this object")
    type = bpy.props.EnumProperty(
        name="Object Type",
        items=[('TEXT', 'Text', '', 1), ('BOX', 'Box', '', 2), ('IMAGE', 'Image', '', 3)],
        description="Type of object")
    x = bpy.props.FloatProperty(
        name="Object X Location",
        default=0,
        description="Horizontal location of this object.  0 is centered, 1 is the right side of screen, -1 is the left side of screen.",
        update=quicktitle_autoupdate)
    y = bpy.props.FloatProperty(
        name="Object Y Location",
        default=0,
        description="Vertical location of this object.  0 is centered, top and bottom vary depending on the aspect ratio of the screen.",
        update=quicktitle_autoupdate)
    z = bpy.props.FloatProperty(
        name="Object Z Position",
        default=0,
        description="Determines the layering of the objects.  Objects with higher values will be above objects with lower values.",
        update=quicktitle_autoupdate)
    scale = bpy.props.FloatProperty(
        name="Overall Object Scale",
        default=1,
        min=0,
        description="Overall scaling of this object.  1 is the original size, 0.5 is half size, 2 is double size.",
        update=quicktitle_autoupdate)
    width = bpy.props.FloatProperty(
        name="Object Width Multiplier",
        default=1,
        min=0,
        description="Multiplies the size of the object on the width axis.  1 is original size, 0.5 is half size, 2 is double size.",
        update=quicktitle_autoupdate)
    height = bpy.props.FloatProperty(
        name="Object Height Multiplier",
        default=1,
        min=0,
        description="Multiplies the size of the object on the height axis.  1 is the original size, 0.5 is half size, 2 is double size.",
        update=quicktitle_autoupdate)
    material = bpy.props.StringProperty(
        name="Object Material",
        default="None",
        update=quicktitle_autoupdate)
    alpha = bpy.props.FloatProperty(
        name="Opacity",
        default=1,
        min=0,
        max=1,
        description="Opacity controls the transparency of this object.  1 is fully visible, 0.5 is half transparent, 0 is invisible.",
        update=quicktitle_autoupdate)
    diffuse_color = bpy.props.FloatVectorProperty(
        name="Color Of The Material",
        size=3,
        default=(1, 1, 1)
        min=0,
        max=1,
        subtype='COLOR',
        description="Basic color of this object.",
        update=quicktitle_autoupdate)
    specular = bpy.props.FloatProperty(
        name="Material Specularity",
        default=0.5,
        min=0,
        max=1,
        description="Controls the specularity, or shininess of this material.",
        update=quicktitle_autoupdate)
    hardness = bpy.props.IntProperty(
        name="Specular Hardness",
        default=50,
        min=1,
        max=511,
        description="Controls the sharpness of the specularity of this material.",
        update=quicktitle_autoupdate)
    specular_color = bpy.props.FloatVectorProperty(
        name="Color Of The Specularity",
        size=3,
        default=(1, 1, 1)
        min=0,
        max=1,
        subtype='COLOR',
        description="Specular color of this object.",
        update=quicktitle_autoupdate)
    animations = bpy.props.CollectionProperty(
        type=QuickTitleAnimation,
        update=quicktitle_autoupdate)

    # Variables specific to the Box and Text types:
    extrude = bpy.props.FloatProperty(
        name="Extrude Amount",
        default=0,
        min=0,
        description="Distance of 3d extrusion.",
        update=quicktitle_autoupdate)
    bevel = bpy.props.FloatProperty(
        name="Bevel Size",
        default=0,
        min=0,
        description="Size of the added beveled edge.",
        update=quicktitle_autoupdate)
    bevel_resolution = bpy.props.IntProperty(
        name="Bevel Resolution",
        default=0,
        min=0,
        description="Number of subdivisions on the beveled edge.",
        update=quicktitle_autoupdate)

    # Variables specific to the Text type:
    text = bpy.props.StringProperty(
        name="Text",
        default="None",
        update=quicktitle_autoupdate)
    font = bpy.props.StringProperty(
        name="Font",
        default="Bfont",
        description="Selected font for this text object",
        update=quicktitle_autoupdate)
    word_wrap = bpy.props.BoolProperty(
        name="Word Wrapping",
        default=True,
        update=quicktitle_autoupdate)
    wrap_width = bpy.props.FloatProperty(
        name="Word Wrap Width",
        default=1,
        min=.01,
        max=1,
        update=quicktitle_autoupdate)

    # Variables specific to the Image type:
    texture = bpy.props.StringProperty(
        name="Image Texture",
        default="",
        description="Name of the image or video texture.",
        update=quicktitle_autoupdate)
    alpha_texture = bpy.props.StringProperty(
        name="Alpha Transparent Texture",
        default="",
        description="Name of the image used for transparency.",
        update=quicktitle_autoupdate)
    video_offset = bpy.props.IntProperty(
        name="Video Frame Offset",
        default=0,
        description="Frame offset of the video if a video texture is selected.",
        update=quicktitle_autoupdate)


class QuickTitleAnimation(bpy.types.PropertyGroup):
    preset = bpy.props.StringProperty(
        name="Animation Preset",
        default="None")
    length = bpy.props.IntProperty(
        name="Length Of Animation",
        default=0,
        min=0)
    offset = bpy.props.IntProperty(
        name="Frame Offset Of Animation",
        default=0)
    amount = bpy.props.FloatProperty(
        name="Amount Of Animation",
        default=1,
        min=0,
        max=1)


# Property for a QuickTitling preset
class QuickTitle(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(
        name="Preset Name",
        default="Default")
    objects = bpy.props.CollectionProperty(
        type=QuickTitleObject)
    shadowsize = bpy.props.FloatProperty(
        name="Shadow Distance",
        default=1,
        min=0,
        update=quicktitle_autoupdate)
    shadowamount = bpy.props.FloatProperty(
        name="Shadow Amount",
        default=0,
        max=1,
        min=0,
        update=quicktitle_autoupdate)
    shadowsoft = bpy.props.FloatProperty(
        name="Shadow Softness",
        default=1,
        min=0,
        update=quicktitle_autoupdate)
    shadowx = bpy.props.FloatProperty(
        name="Shadow Lamp X Position",
        default=0,
        update=quicktitle_autoupdate)
    shadowy = bpy.props.FloatProperty(
        name="Shadow Lamp Y Position",
        default=0,
        update=quicktitle_autoupdate)
    length = bpy.props.IntProperty(
        name="Scene Length",
        default=300,
        update=quicktitle_autoupdate)
    qualityshadows = bpy.props.BoolProperty(
        name="High Quality Shadows",
        default=False,
        update=quicktitle_autoupdate)

# Panel for QuickTitling settings and operators


class VSEQFQuickTitlingPanel(bpy.types.Panel):
    # todo
    bl_label = "Quick Titling"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        return True

    def draw(self, contex):
        scene = bpy.context.scene
        layout = self.layout

        quicktitle = current_quicktitle()

        if not quicktitle:
            # No presets found, must create one before doing anything
            # bpy.ops.vseqf.quicktitler_preset_manipulate(operation="Add")  # Doesnt work here, have to do it manually...
            row = layout.row()
            row.operator('vseqf.quicktitler_preset_manipulate', text="New Title Preset").operation = "Add"
        else:
            # Load preset

            # Preset info and modification
            selected_title = titling_scene_selected()

            row = layout.row()
            # Determine if a titler sequence is selected
            updating = False
            try:
                sequence = bpy.context.scene.sequence_editor.active_strip
                if (('QuickTitle: ' in sequence.name) & (sequence.type == 'SCENE')):
                    updating = True
            except:
                pass

            if updating:
                row.label("Editing: " + sequence.name)
                row = layout.row()
                row.operator('vseqf.quicktitling', text='Update Title').action = 'update'
                row.operator('vseqf.quicktitling', text='Create New Title').action = 'create'
            else:
                row.label("No Title Selected")
                row = layout.row()
                row.operator('vseqf.quicktitling', text='Create New Title').action = 'create'
                scene = bpy.context.scene

            row = layout.row()
            row.prop(bpy.context.scene.quicktitler, 'autoupdate')

            outline = layout.box()
            row = outline.row()
            if updating:
                row.label('Replace Title With Preset:')
            else:
                row.label('Select Preset:')
            row = outline.row()
            split = row.split(percentage=0.6, align=True)
            split.menu('vseqf.quicktitler_preset_menu', text=quicktitle.name)
            split.operator('vseqf.quicktitler_preset_manipulate', text='Copy').operation = 'Copy'
            split.operator('vseqf.quicktitler_preset_manipulate', text='New').operation = 'Add'
            if not selected_title:
                split.operator('vseqf.quicktitler_preset_manipulate', text='Delete').operation = 'Delete'
            row = outline.row()
            row.prop(quicktitle, 'name')

            preset = layout.box()
            row = preset.row()
            row.prop(quicktitle, 'length')

            # Font section
            outline = preset.box()
            row = outline.row()
            row.prop(quicktitle, 'text')
            row = outline.row()
            split = row.split()
            split.prop(quicktitle, 'wrap')
            split.prop(quicktitle, 'wrapwidth', text='Width')
            row = outline.row(align=True)
            split = row.split()
            split.label('Text Font:')
            split = row.split(percentage=0.66, align=True)
            split.menu('vseqf.quicktitler_fonts_menu', text=quicktitle.font)
            split.operator('vseqf.quicktitler_load_font', text='+')
            row = outline.row(align=True)
            split = row.split()
            split.label('Material:')
            split = row.split(percentage=0.66, align=True)
            split.menu('vseqf.quicktitler_materials_menu', text=quicktitle.material)
            split.operator('vseqf.quicktitler_new_material', text='+')
            index = bpy.data.materials.find(quicktitle.material)
            if (index >= 0):
                material = bpy.data.materials[index]
                split.prop(material, 'diffuse_color', text='')
                row = outline.row()
                split = row.split(percentage=.9, align=True)
                subsplit = split.split(align=True)
                subsplit.prop(material, 'specular_intensity', text="Specular")
                subsplit.prop(material, 'specular_hardness', text="Hardness")
                split.prop(material, 'specular_color', text="")

            # Position and size section
            outline = preset.box()
            row = outline.row()
            split = row.split(align=True)
            split.prop(quicktitle, 'x', text='X Loc')
            split.prop(quicktitle, 'y', text='Y Loc')
            row = outline.row()
            row.prop(quicktitle, 'size', text='Size')

            # Extrude and bevel section
            outline = preset.box()
            row = outline.row()
            row.prop(quicktitle, 'extrude')
            row = outline.row()
            split = row.split(align=True)
            split.prop(quicktitle, 'bevel')
            split.prop(quicktitle, 'bevelres')

            # Shadow section
            outline = preset.box()
            row = outline.row()
            row.prop(quicktitle, 'shadowamount')
            row = outline.row()
            row.prop(quicktitle, 'shadowsize', text='Distance')
            row.prop(quicktitle, 'shadowsoft', text='Soft')
            row = outline.row(align=True)
            row.prop(quicktitle, 'shadowx', text='X Offset')
            row.prop(quicktitle, 'shadowy', text='Y Offset')
            row = outline.row()
            row.prop(quicktitle, 'qualityshadows')

# Operator to delete QuickTitler presets - create, copy, or delete


class VSEQFQuickTitlingPresetManipulate(bpy.types.Operator):
    bl_idname = 'vseqf.quicktitler_preset_delete'
    bl_label = 'Delete Presets'
    bl_description = 'Delete A Specific QuickTitling Preset'

    index = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        scene.quicktitles.remove(self.index)

        return {'FINISHED'}


# Operator to manipulate QuickTitler presets - create, copy, or delete
class VSEQFQuickTitlingPresetManipulate(bpy.types.Operator):
    bl_idname = 'vseqf.quicktitler_preset_manipulate'
    bl_label = 'Manipulate Presets'
    bl_description = 'Add, Copy or Delete The First QuickTitling Preset'

    # What to do - should be set to 'Delete', 'Copy', or 'Add'
    operation = bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        if self.operation == 'Delete':
            if len(scene.quicktitles) > 0:
                scene.quicktitles.remove(0)
        else:
            title = scene.quicktitles.add()
            if self.operation == 'Copy' and len(scene.quicktitles) > 1:
                # copy current title info to new title
                old_title = current_quicktitle()
                copy_title_preset(old_title, title)

            scene.quicktitles.move((len(scene.quicktitles) - 1), 0)

        return {'FINISHED'}

# Menu to list in alphabetical order the QuickTitler Presets


class VSEQFQuickTitlingPresetMenu(bpy.types.Menu):
    bl_idname = 'vseqf.quicktitler_preset_menu'
    bl_label = 'List of saved presets'

    def draw(self, context):
        presets = context.scene.quicktitles
        layout = self.layout
        title_preset_names = []

        # iterate through presets and dump the names into a list
        for preset in presets:
            title_preset_names.append(preset.name)

        selected_title = titling_scene_selected()
        if selected_title:
            layout.operator('vseqf.quicktitler_preset', text="Scene Preset: " + selected_title.quicktitles[0].name)
        else:
            layout.label('Select A Preset:')

        split = layout.split()
        column = split.column()
        for index, name in enumerate(title_preset_names):
            column.operator('vseqf.quicktitler_preset', text=name).preset = name
        column = split.column()
        for index, name in enumerate(title_preset_names):
            column.operator("vseqf.quicktitler_preset_delete", text="", icon="X").index = index


# Operator to select a QuickTitling preset
class VSEQFQuickTitlingPreset(bpy.types.Operator):
    bl_idname = 'vseqf.quicktitler_preset'
    bl_label = 'Set Preset'
    bl_description = 'Select A QuickTitling Preset'

    # Preset name
    preset = bpy.props.StringProperty()

    def execute(self, context):
        if not self.preset:
            return {'FINISHED'}
        scene = context.scene
        istitle = False

        # Iterate through titler presets to try and find the inputted one
        for index, preset in enumerate(scene.quicktitles):
            if preset.name == self.preset:
                title = index
                istitle = True
                break

        if istitle:
            # found title
            scene.quicktitles.move(title, 0)
            titling_scene = titling_scene_selected()

            # if a title sequence is selected, copy new selected preset to that scene
            if titling_scene:
                if len(titling_scene.quicktitles) == 0:
                    titling_scene.quicktitles.add()
                copy_title_preset(scene.quicktitles[0], titling_scene.quicktitles[0])
        return {'FINISHED'}

# Operator to load a new font into Blender


class VSEQFQuickTitlingLoadFont(bpy.types.Operator):
    bl_idname = 'vseqf.quicktitler_load_font'
    bl_label = 'Load Font'
    bl_description = 'Load A New Font'

    # font file to be loaded
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # When the file browser finishes, this is called
        scene = context.scene
        fonts = bpy.data.fonts
        quicktitle = current_quicktitle()

        # Try to load font file
        try:
            font = bpy.data.fonts.load(self.filepath)
            quicktitle.font = font.name
        except:
            print("Not a valid font file: " + self.filepath)
            self.report({'WARNING'}, "Not a valid font file: " + self.filepath)

        return {'FINISHED'}

    def invoke(self, context, event):
        # Open a file browser
        context.window_manager.fileselect_add(self)

        return{'RUNNING_MODAL'}

# Menu for listing and changing QuickTitler fonts


class VSEQFQuickTitlingFontMenu(bpy.types.Menu):
    bl_idname = 'vseqf.quicktitler_fonts_menu'
    bl_label = 'List of loaded fonts'

    def draw(self, context):
        fonts = bpy.data.fonts
        layout = self.layout
        for font in fonts:
            layout.operator('vseqf.quicktitler_change_font', text=font.name).font = font.name

# Operator for changing the QuickTitler font on the current preset


class VSEQFQuickTitlingChangeFont(bpy.types.Operator):
    # todo
    bl_idname = 'vseqf.quicktitler_change_font'
    bl_label = 'Change Font'
    font = bpy.props.StringProperty()

    def execute(self, context):
        quicktitle = current_quicktitle()
        if quicktitle:
            quicktitle.font = self.font
        return {'FINISHED'}

# Operator for copying or creating a new material to be used in QuickTitler


class VSEQFQuickTitlingNewMaterial(bpy.types.Operator):
    # todo
    bl_idname = 'vseqf.quicktitler_new_material'
    bl_label = 'New Material'
    bl_description = 'Creates A New Material, Duplicates Current If Available'

    def execute(self, context):
        quicktitle = current_quicktitle()
        if quicktitle:
            index = bpy.data.materials.find(quicktitle.material)
            if (index >= 0):
                material = bpy.data.materials[index].copy()
            else:
                material = bpy.data.materials.new('QuickTitler Material')
            quicktitle.material = material.name
        return {'FINISHED'}

# Menu to list all Materials in blend file, and assign them to QuickTitler presets


class VSEQFQuickTitlingMaterialMenu(bpy.types.Menu):
    bl_idname = 'vseqf.quicktitler_materials_menu'
    bl_label = 'List of loaded materials'

    def draw(self, context):
        materials = bpy.data.materials
        layout = self.layout
        for material in materials:
            layout.operator('vseqf.quicktitler_change_material', text=material.name).material = material.name

# Operator to assign a material name to the material of a QuickTitler preset


class VSEQFQuickTitlingChangeMaterial(bpy.types.Operator):
    # todo
    bl_idname = 'vseqf.quicktitler_change_material'
    bl_label = 'Change Material'
    material = bpy.props.StringProperty()

    def execute(self, context):
        quicktitle = current_quicktitle()
        if quicktitle:
            quicktitle.material = self.material
        return {'FINISHED'}

# Operator to create QuickTitle scenes


class VSEQFQuickTitling(bpy.types.Operator):
    bl_idname = 'vseqf.quicktitling'
    bl_label = 'VSEQF Quick Titling'
    bl_description = 'Creates or updates a titler scene'

    # Should be set to 'create' or 'update'
    action = bpy.props.StringProperty()

    def execute(self, context):
        quicktitle = current_quicktitle()
        if not quicktitle:
            print('No QuickTitle Preset Found')
            self.report({'WARNING'}, 'No QuickTitle Preset Found')
            return {'CANCELLED'}

        title_scene_length = quicktitle.length
        title_scene_name = "QuickTitle: " + quicktitle.text
        if (self.action == 'create'):
            quicktitle_create(quicktitle)

        sequence = bpy.context.scene.sequence_editor.active_strip

        quicktitle_update(sequence, quicktitle)

        return {'FINISHED'}


class QuickTitleSettings(bpy.types.PropertyGroup):
    autoupdate = bpy.props.BoolProperty(
        name="Auto-Update Titles",
        default=True)


# Register properties, operators, menus and shortcuts
def register():
    # Register operators
    bpy.utils.register_module(__name__)

    # Group properties
    bpy.types.Scene.quicktitles = bpy.props.CollectionProperty(type=QuickTitle)
    bpy.types.Scene.quicktitler = bpy.props.PointerProperty(type=QuickTitleSettings)


def unregister():
    # Unregister operators
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
