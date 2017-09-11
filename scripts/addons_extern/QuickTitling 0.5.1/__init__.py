#QuickTitling 0.5
#
#
#Todo:
#   Future todo if possible:
#       Overlays in the sequencer viewer to show information about objects (selected object, animations, layers)
#       selecting objects in the sequencer viewer
#       moving objects in the sequencer viewer (drag/drop)
#
#
#Version History:
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
#   0.50
#       Implemented adding multiple objects of 4 basic types: image, box, circle, and text
#       Implemented presets
#       Implemented saving/loading presets
#       Reworked interface
#       Added animation abilities and presets
#       Implemented new way of handling materials
#       Implemented saving preset preview images


import bpy
import math
import os
from math import pi
from bpy.app.handlers import persistent
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy_extras.image_utils import load_image

bl_info = {
    "name": "VSE Quick Titling",
    "description": "Enables easy creation of simple title scenes in the VSE",
    "author": "Hudson Barkley (Snu)",
    "version": (0, 5, 1),
    "blender": (2, 78, 0),
    "location": "Sequencer Panels",
    "wiki_url": "none yet",
    "category": "Sequencer"
}

animations = [
    {
        'name':'Fade In And Out',
        'variable':'Alpha',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':0,
        'out_amount':0
    },
    {
        'name':'X Slide From Right',
        'variable':'X Slide',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':2,
        'out_amount':2
    },
    {
        'name':'X Slide From Left',
        'variable':'X Slide',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':-2,
        'out_amount':-2
    },
    {
        'name':'Y Slide Up And Down',
        'variable':'Y Slide',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':-1,
        'out_amount':-1
    },
    {
        'name':'Y Slide Down And Up',
        'variable':'Y Slide',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':1,
        'out_amount':1
    },
    {
        'name':'Z Slide Forward And Back',
        'variable':'Z Slide',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':-2,
        'out_amount':-2
    },
    {
        'name':'Z Slide Back And Forward',
        'variable':'Z Slide',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':2,
        'out_amount':2
    },
    {
        'name':'X Tilt Forward And Back',
        'variable':'X Rotate',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':-90,
        'out_amount':-90
    },
    {
        'name':'X Tilt Backward And Forward',
        'variable':'X Rotate',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':90,
        'out_amount':90
    },
    {
        'name':'Y Turn Forward And Back',
        'variable':'Y Rotate',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':-90,
        'out_amount':-90
    },
    {
        'name':'Y Turn Backward And Forward',
        'variable':'Y Rotate',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':90,
        'out_amount':90
    },
    {
        'name':'Z Spin Forward And Back',
        'variable':'Z Rotate',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':90,
        'out_amount':90
    },
    {
        'name':'Z Spin Backward And Forward',
        'variable':'Z Rotate',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':-90,
        'out_amount':-90
    },
    {
        'name':'Width Grow And Shrink',
        'variable':'Width',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':0,
        'out_amount':0
    },
    {
        'name':'Height Grow And Shrink',
        'variable':'Height',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':0,
        'out_amount':0
    },
    {
        'name':'Depth Grow And Shrink',
        'variable':'Depth',
        'animate_in':True,
        'animate_out':True,
        'in_length':15,
        'out_length':15,
        'in_offset':0,
        'out_offset':0,
        'in_amount':0,
        'out_amount':0
    }
]

def to_bool(value):
    '''Function to convert various Non-Boolean true/false values to Boolean.
    Inputs that return True are:
        'Yes', 'yes', 'True', 'True', 'T', 't', '1', 1, 'Down', 'down'
    Any other value returns a False.
    '''
    return str(value).lower() in ('yes', 'true', 't', '1', 'down')

def get_current_object(quicktitle_preset=False):
    #Get the current quicktitle preset object
    if not quicktitle_preset:
        quicktitle_preset = current_quicktitle()
    if not quicktitle_preset:
        return False
    else:
        current_object_index = quicktitle_preset.selected_object
        current_object = quicktitle_preset.objects[current_object_index]
        return current_object

def find_titling_scene():
    #If the active sequence is a title scene, return that scene, otherwise return the current scene
    selected = titling_scene_selected()
    if selected:
        return selected.scene
    else:
        return bpy.context.scene

def titling_scene_selected():
    #determines if a titling scene is selected
    sequence_editor = bpy.context.scene.sequence_editor
    if hasattr(sequence_editor, 'active_strip'):
        #there is an active strip
        active_sequence = sequence_editor.active_strip
        if active_sequence:
            if active_sequence.type == 'SCENE':
                #this is a scene strip
                if 'QuickTitle:' in active_sequence.name:
                    #strip is named properly
                    scene = active_sequence.scene
                    if len(scene.quicktitles) > 0:
                        #scene has a quicktitle preset
                        return active_sequence
    return False

def current_quicktitle(sequence=None):
    #Function to return the current QuickTitle preset depending on what is selected in the sequencer
    if not sequence:
        sequence = titling_scene_selected()
    if sequence:
        scene = sequence.scene
    else:
        scene = find_titling_scene()
    if len(scene.quicktitles) > 0:
        return scene.quicktitles[0]
    else:
        return False

def copy_title_preset(old_title, title):
    #Function to copy one QuickTitle preset to another
    title.name = old_title.name
    title.description = old_title.description
    title.z_scale = old_title.z_scale
    title.shadowsize = old_title.shadowsize
    title.shadowamount = old_title.shadowamount
    title.shadowsoft = old_title.shadowsoft
    title.shadowx = old_title.shadowx
    title.shadowy = old_title.shadowy
    title.length = old_title.length
    title.qualityshadows = old_title.qualityshadows
    title.objects.clear()
    for oldobject in old_title.objects:
        newobject = title.objects.add()
        newobject.name = oldobject.name
        newobject.type = oldobject.type
        newobject.x = oldobject.x
        newobject.y = oldobject.y
        newobject.z = oldobject.z
        newobject.rot_x = oldobject.rot_x
        newobject.rot_y = oldobject.rot_y
        newobject.rot_z = oldobject.rot_z
        newobject.scale = oldobject.scale
        newobject.width = oldobject.width
        newobject.height = oldobject.height
        newobject.shear = oldobject.shear
        newobject.set_material = oldobject.set_material
        newobject.cast_shadows = oldobject.cast_shadows
        newobject.material = oldobject.material
        newobject.use_shadeless = oldobject.use_shadeless
        newobject.use_transparency = oldobject.use_transparency
        newobject.alpha = oldobject.alpha
        newobject.diffuse_color = oldobject.diffuse_color
        newobject.specular_intensity = oldobject.specular_intensity
        newobject.specular_hardness = oldobject.specular_hardness
        newobject.specular_color = oldobject.specular_color
        newobject.extrude = oldobject.extrude
        newobject.bevel = oldobject.bevel
        newobject.bevel_resolution = oldobject.bevel_resolution
        newobject.text = oldobject.text
        newobject.font = oldobject.font
        newobject.word_wrap = oldobject.word_wrap
        newobject.wrap_width = oldobject.wrap_width
        newobject.align = oldobject.align
        newobject.texture = oldobject.texture
        newobject.alpha_texture = oldobject.alpha_texture
        newobject.animations.clear()
        for oldanimation in oldobject.animations:
            newanimation = newobject.animations.add()
            newanimation.variable = oldanimation.variable
            newanimation.animate_in = oldanimation.animate_in
            newanimation.animate_out = oldanimation.animate_out
            newanimation.in_length = oldanimation.in_length
            newanimation.out_length = oldanimation.out_length
            newanimation.in_offset = oldanimation.in_offset
            newanimation.out_offset = oldanimation.out_offset
            newanimation.in_amount = oldanimation.in_amount
            newanimation.out_amount = oldanimation.out_amount

def quicktitle_autoupdate(self=None, context=None):
    #Auto update function called when changing settings
    #will update a selected title if autoupdate is enabled, should only update objects that are needed
    if bpy.context.scene.quicktitler.autoupdate:
        #Determine if a titler sequence is selected
        quicktitle = titling_scene_selected()
        if quicktitle:
            if len(quicktitle.scene.quicktitles) > 0:
                preset = quicktitle.scene.quicktitles[0]
                quicktitle_update(quicktitle, preset)

def quicktitle_autoupdate_all(self=None, context=None):
    #Auto update function
    #will update a selected title if autoupdate is enabled, will update all objects in the scene
    if bpy.context.scene.quicktitler.autoupdate:
        #Determine if a titler sequence is selected
        quicktitle = titling_scene_selected()
        if quicktitle:
            if len(quicktitle.scene.quicktitles) > 0:
                preset = quicktitle.scene.quicktitles[0]
                quicktitle_update(quicktitle, preset, all=True)

def isimageloaded(filepath):
    #Function to check if an image is already loaded
    for image in bpy.data.images:
        if image.filepath == filepath:
            return image
    return False

def istexture(image):
    #Function to check if a texture with a specific image exists
    for texture in bpy.data.textures:
        if hasattr(texture, 'image'):
            if texture.image == image:
                return texture
    return False

def istype(object, type):
    #Function to test if an object is the correct blender type for what the script thinks it is
    if type == 'TEXT' and object.type == 'FONT':
        return True
    if (type == 'BOX' and object.type == 'CURVE') or (type == 'CIRCLE' and object.type == 'CURVE'):
        return True
    if type == 'IMAGE' and object.type == 'MESH':
        return True
    return False

def quicktitle_create(quicktitle=False):
    #Function to create QuickTitle scenes and sequences
    scene = bpy.context.scene
    if not quicktitle:
        quicktitle = scene.quicktitles[0]
    
    #Basic scene setup
    bpy.ops.scene.new(type='EMPTY')
    title_scene = bpy.context.scene
    title_scene.frame_end = quicktitle.length
    title_scene.layers = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    title_scene.render.engine = 'BLENDER_RENDER'
    title_scene.render.alpha_mode = 'TRANSPARENT'
    title_scene.render.image_settings.file_format = 'PNG'
    title_scene.render.image_settings.color_mode = 'RGBA'
    title_scene.quicktitles.clear()
    title_scene.quicktitles.add()
    copy_title_preset(quicktitle, title_scene.quicktitles[0])
    quicktitle_preset = title_scene.quicktitles[0]
    if quicktitle.name:
        name = "QuickTitle: "+quicktitle.name
    else:
        name = "QuickTitle: "+quicktitle.text
    title_scene.name = name
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    lampcenter = bpy.context.scene.objects.active

    #Camera setup
    bpy.ops.object.camera_add()
    camera = bpy.context.scene.objects.active
    title_scene.camera = camera
    camera.location = ((0, 0, 2.17))
    camera.name = "QuickTitlerCamera"
    
    #Basic lamps setup
    lampEnergy = 0.5
    bpy.ops.object.lamp_add(location=(-1.1, -.6, .5))
    lamp1 = bpy.context.scene.objects.active
    lamp1.data.energy = lampEnergy
    lamp1.data.shadow_method = 'NOSHADOW'
    lamp1.parent = lampcenter
    bpy.ops.object.lamp_add(location=(1.1, -.6, .5))
    lamp2 = bpy.context.scene.objects.active
    lamp2.data.energy = lampEnergy
    lamp2.data.shadow_method = 'NOSHADOW'
    lamp2.parent = lampcenter
    bpy.ops.object.lamp_add(location=(-1.1, .6, .5))
    lamp3 = bpy.context.scene.objects.active
    lamp3.data.energy = lampEnergy
    lamp3.data.shadow_method = 'NOSHADOW'
    lamp3.parent = lampcenter
    bpy.ops.object.lamp_add(location=(1.1, .6, .5))
    lamp4 = bpy.context.scene.objects.active
    lamp4.data.energy = lampEnergy
    lamp4.data.shadow_method = 'NOSHADOW'
    lamp4.parent = lampcenter
    
    #Shadow lamp setup
    bpy.ops.object.lamp_add(type= 'SPOT', location=(0, 0, 1))
    shadowLamp = bpy.context.scene.objects.active
    basename = 'QuickTitlerLamp'
    if basename in bpy.data.objects:
        name = 'QuickTitlerLamp.001'
        index = 1
        while name in bpy.data.objects:
            index = index+1
            name = basename+str(index).zfill(3)
    else:
        name = basename
    shadowLamp.name = name
    quicktitle_preset.shadowlamp_internal_name = shadowLamp.name
    shadowLamp.parent = lampcenter
    shadowLamp.data.use_only_shadow = True
    shadowLamp.data.use_specular = False
    shadowLamp.data.distance = 3
    shadowLamp.data.shadow_ray_samples = 4
    shadowLamp.data.shadow_soft_size = 0
    shadowLamp.data.falloff_type = 'CONSTANT'
    shadowLamp.data.shadow_method = 'BUFFER_SHADOW'
    shadowLamp.data.shadow_buffer_type = 'REGULAR'
    shadowLamp.data.shadow_buffer_soft = 10
    shadowLamp.data.shadow_buffer_bias = 0.1
    shadowLamp.data.shadow_buffer_size = 4096
    shadowLamp.data.shadow_buffer_samples = 4
    shadowLamp.data.shadow_sample_buffers = 'BUFFERS_4'
    shadowLamp.data.shadow_buffer_clip_end = 4
    shadowLamp.data.use_auto_clip_start = True
    shadowLamp.data.use_auto_clip_end = True
    shadowLamp.data.spot_size = 2.6
    shadowLamp.data.use_square = True
    
    #Add scene to sequencer
    bpy.context.screen.scene = scene
    bpy.ops.sequencer.scene_strip_add(frame_start=scene.frame_current, scene=title_scene.name)
    sequence = bpy.context.scene.sequence_editor.active_strip
    sequence.name = name
    sequence.blend_type = 'ALPHA_OVER'
    scene = title_scene

def quicktitle_update(sequence, quicktitle, all=False):
    #Function to update a QuickTitle sequence
    scene = sequence.scene
    oldscene = bpy.context.screen.scene
    bpy.context.screen.scene = scene
    scenename = "QuickTitle: "+quicktitle.name
    if all:
        update_all = True
    else:
        update_all = False
    
    #Update scene length, if changed, update all objects
    if scene.frame_end != quicktitle.length:
        scene.frame_end = quicktitle.length
        update_all = True
    
    #attempt to find and update the shadow lamp
    if quicktitle.shadowlamp_internal_name in scene.objects:
        shadowLamp = scene.objects[quicktitle.shadowlamp_internal_name]
        softshadow = quicktitle.shadowsoft * 10
        shadowLamp.data.shadow_buffer_soft = softshadow
        if softshadow >= 20:
            shadowLamp.data.shadow_buffer_samples = 8
            shadowLamp.data.shadow_ray_samples = 8
        elif softshadow >= 10:
            shadowLamp.data.shadow_buffer_samples = 6
            shadowLamp.data.shadow_ray_samples = 6
        elif softshadow > 0:
            shadowLamp.data.shadow_buffer_samples = 4
            shadowLamp.data.shadow_ray_samples = 4
        else:
            shadowLamp.data.shadow_buffer_samples = 1
            shadowLamp.data.shadow_ray_samples = 1
        shadowLamp.data.energy = quicktitle.shadowamount
        shadowLamp.data.shadow_soft_size = quicktitle.shadowsoft
        shadowLamp.location = (-quicktitle.shadowx, quicktitle.shadowy, quicktitle.shadowsize)
        if quicktitle.shadowamount > 0:
            if quicktitle.qualityshadows:
                shadowLamp.data.shadow_method = 'RAY_SHADOW'
            else:
                shadowLamp.data.shadow_method = 'BUFFER_SHADOW'
        else:
            shadowLamp.data.shadow_method = 'NOSHADOW'
    else:
        shadowLamp = None
        print('Selected Title Scene Is Incomplete: Missing Shadow Lamp')

    #update individual scene objects
    total_object_layers = len(quicktitle.objects)
    for object_layer, object_preset in enumerate(quicktitle.objects):
        if object_layer == quicktitle.selected_object:
            selected_object = True
        else:
            selected_object = False
        
        #get or create object name used for internal naming
        if object_preset.name:
            name = object_preset.type+':'+object_preset.name
        else:
            name = object_preset.type
        
        #determine if object needs to be created
        if object_preset.internal_name not in scene.objects:
            #object is not found or doesnt exist
            object = False
        else:
            #object exists
            object = scene.objects[object_preset.internal_name]
            if not istype(object, object_preset.type):
                #object exists but its not the correct type, need to recreate object
                object = False
            else:
                if object_preset.type == 'IMAGE':
                    if len(object.data.vertices) != 4:
                        object = False
                if object_preset.type == 'BOX' or object_preset.type == 'CIRCLE':
                    if len(object.data.splines[0].points) != 4:
                        object = False
        if not object:
            #create object
            scene.cursor_location = (0.0, 0.0, 0.0)
            
            if object_preset.type == 'IMAGE':
                #create image
                mesh = bpy.data.meshes.new(name=name)
                verts = [(-1, 1, 0.0),(1, 1, 0.0), (1, -1, 0.0),(-1, -1, 0.0)]
                faces = [(3, 2, 1, 0)]
                mesh.from_pydata(verts, [], faces)
                uvmap = mesh.uv_textures.new()
                object = bpy.data.objects.new(name=name, object_data=mesh)
                scene.objects.link(object)
                
            elif object_preset.type == 'CIRCLE':
                #create circle
                curve = bpy.data.curves.new(name=name, type='CURVE')
                curve.dimensions = '2D'
                curve.resolution_u = 24
                curve.twist_mode = 'MINIMUM'
                spline = curve.splines.new('NURBS')
                spline.points.add(3)
                w = 0.354
                spline.points[0].co = (-1,1,0,w)
                spline.points[1].co = (1,1,0,w)
                spline.points[2].co = (1,-1,0,w)
                spline.points[3].co = (-1,-1,0,w)
                spline.use_cyclic_u = True
                spline.resolution_u = 24
                spline.order_u = 4
                object = bpy.data.objects.new(name=name, object_data=curve)
                scene.objects.link(object)
                
            elif object_preset.type == 'BOX':
                #create box
                curve = bpy.data.curves.new(name=name, type='CURVE')
                curve.dimensions = '2D'
                curve.resolution_u = 1
                curve.twist_mode = 'MINIMUM'
                spline = curve.splines.new('NURBS')
                spline.points.add(3)
                w = 1
                spline.points[0].co = (-1,1,0,w)
                spline.points[1].co = (1,1,0,w)
                spline.points[2].co = (1,-1,0,w)
                spline.points[3].co = (-1,-1,0,w)
                spline.use_cyclic_u = True
                spline.resolution_u = 1
                spline.order_u = 2
                object = bpy.data.objects.new(name=name, object_data=curve)
                scene.objects.link(object)
                
            else:
                #create text
                text = bpy.data.curves.new(name=name, type='FONT')
                text.size = 0.1
                object = bpy.data.objects.new(name=name, object_data=text)
                scene.objects.link(object)
            
            object_preset.internal_name = object.name
            created_object = True
        
        else:
            created_object = False
        
        #General object settings
        offset_multiplier = 0.462
        z_index = object_layer
        z_scale = quicktitle.z_scale / 10.0
        scale_multiplier = (z_scale * (z_index * offset_multiplier)) + 1
        pos_multiplier = 1 + (z_scale* (z_index * offset_multiplier))
        z_offset = z_index * z_scale
        object.location = (pos_multiplier * object_preset.x, pos_multiplier * object_preset.y, object_preset.z - z_offset)
        object.scale = (scale_multiplier * object_preset.scale * object_preset.width, scale_multiplier * object_preset.scale * object_preset.height, object_preset.scale)
        
        #detailed settings need to be updated for this object
        if selected_object or created_object or update_all:
            object.rotation_euler = (object_preset.rot_x/180.0*pi, object_preset.rot_y/180.0*pi, -object_preset.rot_z/180.0*pi)
        
            #Material settings
            if object_preset.set_material:
                #material is set manually
                if object_preset.material == 'No Preset':
                    #material is unset, disable manual setting
                    object_preset.set_material = False
                    
                else:
                    if object_preset.material in bpy.data.materials:
                        #material exists
                        material = bpy.data.materials[object_preset.material]
                        
                    else:
                        #material doesnt exist, create it
                        material = bpy.data.materials.new(object_preset.material)
                        
            if not object_preset.set_material:
                #material is determined automatically
                if object.active_material:
                    #object has a material set, check if its valid
                    material = object.active_material
                    if material.users > 1:
                        #this material is being used by multiple objects, create a new one instead
                        material = bpy.data.materials.new(object_preset.material)
                        object.active_material = material
                        
                    object_preset.material = material.name
                    
                else:
                    #object doesnt have a material, create one
                    material = bpy.data.materials.new('QuickTitler '+object_preset.type+' Material')
                    object_preset.material = material.name

            #set up material
            material.diffuse_intensity = 1
            material.diffuse_color = object_preset.diffuse_color
            material.specular_intensity = object_preset.specular_intensity
            material.specular_hardness = object_preset.specular_hardness
            material.specular_color = object_preset.specular_color
            material.use_shadeless = object_preset.use_shadeless
            material.use_transparency = object_preset.use_transparency
            material.alpha = object_preset.alpha
            material.specular_alpha = 0
            
            if object_preset.cast_shadows:
                material.use_cast_shadows = True
                material.use_cast_buffer_shadows = True
                
            else:
                material.use_cast_shadows = False
                material.use_cast_buffer_shadows = False
        
            #settings for different object types
            if object_preset.type == 'IMAGE':
                #set up image type
                video = False
                shear = object_preset.shear
                if object_preset.texture:
                    #look for image, load if needed
                    path = os.path.abspath(bpy.path.abspath(object_preset.texture))
                    image = isimageloaded(path)
                    extension = os.path.splitext(path)[1].lower()
                    if extension in bpy.path.extensions_movie:
                        #The file is a known video file type, load it
                        video = True
                    if not image and os.path.isfile(path):
                        if extension in bpy.path.extensions_image or video:
                            #The file is a known file type, load it
                            image = load_image(path)
                            image.update()
                    if image:
                        #look for texture, create if needed
                        texture = istexture(image)
                        if not texture:
                            texture = bpy.data.textures.new(name=image.name, type='IMAGE')
                            texture.image = image
                            texture.extension = 'EXTEND'
                        
                        #set texture
                        if not material.texture_slots[0]:
                            material.texture_slots.add()
                        
                        #material.texture_slots[0].texture_coords = 'ORCO'
                        material.texture_slots.update()
                        material.texture_slots[0].texture = texture
                        material.texture_slots[0].blend_type = 'MULTIPLY'
                        material.texture_slots[0].use_map_alpha = True
                        if video:
                            texture.image_user.use_cyclic = True
                            texture.image_user.use_auto_refresh = True
                            texture.image_user.frame_duration = image.frame_duration
                        #set plane size based on image aspect ratio
                        ix = 1
                        iy = (image.size[1] / image.size[0])
                        object.data.vertices[0].co = (-ix+shear, iy, 0)
                        object.data.vertices[1].co = (ix+shear, iy, 0)
                        object.data.vertices[2].co = (ix-shear, -iy, 0)
                        object.data.vertices[3].co = (-ix-shear, -iy, 0)
                else:
                    #image texture is not set or has been unset, remove it from material if needed and set plane back to original dimensions
                    object.data.vertices[0].co = (-1+shear, 1, 0)
                    object.data.vertices[1].co = (1+shear, 1, 0)
                    object.data.vertices[2].co = (1-shear, -1, 0)
                    object.data.vertices[3].co = (-1-shear, -1, 0)
                    material.texture_slots.clear(0)

                if object_preset.alpha_texture:
                    video = False
                    #look for alpha image, load if needed
                    path = os.path.abspath(bpy.path.abspath(object_preset.alpha_texture))
                    image = isimageloaded(path)
                    extension = os.path.splitext(path)[1].lower()
                    if not image and os.path.isfile(path):
                        if extension in bpy.path.extensions_movie:
                            #The file is a known video file type, load it
                            video = True
                    if not image and os.path.isfile(path):
                        if extension in bpy.path.extensions_image or video:
                            #The file is a known file type, load it
                            image = load_image(path)
                            image.update()
                    if image:
                        #look for texture, create if needed
                        texture = istexture(image)
                        if not texture:
                            texture = bpy.data.textures.new(name=image.name, type='IMAGE')
                            texture.extension = 'EXTEND'
                            texture.image = image
                        #set texture
                        if not material.texture_slots[0]:
                            material.texture_slots.add()
                        if not material.texture_slots[1]:
                            material.texture_slots.add()
                        #material.texture_slots[1].texture_coords = 'ORCO'
                        material.texture_slots[1].texture = texture
                        material.texture_slots[1].use_map_color_diffuse = False
                        material.texture_slots[1].use_map_alpha = True
                        material.texture_slots[1].use_rgb_to_intensity = True
                        material.texture_slots[1].alpha_factor = -1
                        material.texture_slots[1].blend_type = 'SUBTRACT'
                        material.texture_slots.update()
                        if video:
                            texture.image_user.use_cyclic = True
                            texture.image_user.use_auto_refresh = True
                            texture.image_user.frame_duration = image.frame_duration
                else:
                    #image texture is not set or has been unset, remove it from material if needed and set plane back to original dimensions
                    material.texture_slots.clear(1)
                
            if object_preset.type == 'CIRCLE' or object_preset.type == 'BOX' or object_preset.type == 'TEXT':
                #set up the circle, box and text settings
                object.data.extrude = object_preset.extrude/10.0
                object.data.bevel_depth = object_preset.bevel/10.0
                object.data.bevel_resolution = object_preset.bevel_resolution
            
            if object_preset.type == 'CIRCLE' or object_preset.type == 'BOX':
                #set up the circle and box settings
                object.data.splines[0].points[0].co[0] = -1 + object_preset.shear
                object.data.splines[0].points[1].co[0] = 1 + object_preset.shear
                object.data.splines[0].points[2].co[0] = 1 - object_preset.shear
                object.data.splines[0].points[3].co[0] = -1 - object_preset.shear

            if object_preset.type == 'TEXT':
                #set up the text settings
                object.data.body = object_preset.text
                object.data.align_x = object_preset.align
                object.data.shear = object_preset.shear
                if object_preset.font in bpy.data.fonts:
                    object.data.font = bpy.data.fonts[object_preset.font]
                if object_preset.word_wrap:
                    #box_size = (1.0/object.scale[0])*2
                    box_size = 1.94
                    object.data.text_boxes[0].width = box_size * object_preset.wrap_width
                    object.data.text_boxes[0].x = -(box_size/2) * object_preset.wrap_width
                else:
                    object.data.text_boxes[0].width = 0
                    object.data.text_boxes[0].x = 0
            object.active_material = material

            #look for and clear animations that are no longer set
            if object.animation_data:
                if object.animation_data.action:
                    if object.animation_data.action.fcurves:
                        fcurves = object.animation_data.action.fcurves
                        animation_types = []
                        for animation in object_preset.animations:
                            animation_types.append(animation.variable)
                        for curve in fcurves:
                            if curve.data_path == 'active_material.alpha':
                                if 'Alpha' not in animation_types:
                                    fcurves.remove(curve)
                            elif curve.data_path == 'location':
                                if curve.array_index == 0:
                                    if 'X Slide' not in animation_types:
                                        fcurves.remove(curve)
                                elif curve.array_index == 1:
                                    if 'Y Slide' not in animation_types:
                                        fcurves.remove(curve)
                                elif curve.array_index == 2:
                                    if 'Z Slide' not in animation_types:
                                        fcurves.remove(curve)
                            elif curve.data_path == 'rotation_euler':
                                if curve.array_index == 0:
                                    if 'X Rotate' not in animation_types:
                                        fcurves.remove(curve)
                                elif curve.array_index == 1:
                                    if 'Y Rotate' not in animation_types:
                                        fcurves.remove(curve)
                                elif curve.array_index == 2:
                                    if 'Z Rotate' not in animation_types:
                                        fcurves.remove(curve)
                            elif curve.data_path == 'scale':
                                if curve.array_index == 0:
                                    if 'Width' not in animation_types:
                                        fcurves.remove(curve)
                                elif curve.array_index == 1:
                                    if 'Height' not in animation_types:
                                        fcurves.remove(curve)
                                elif curve.array_index == 2:
                                    if 'Depth' not in animation_types:
                                        fcurves.remove(curve)
            
            #if animations are on this object, update them
            if len(object_preset.animations) > 0:
                if not object.animation_data:
                    animation = object.animation_data_create()
                else:
                    animation = object.animation_data
                if not animation.action:
                    action = bpy.data.actions.new(object.name)
                    animation.action = action
                else:
                    action = animation.action
                start_frame = scene.frame_start
                end_frame = scene.frame_end
                fcurves = action.fcurves
                for animation_preset in object_preset.animations:
                    in_amount = animation_preset.in_amount
                    out_amount = animation_preset.out_amount
                    variable = animation_preset.variable
                    fcurve, value = get_fcurve(fcurves, variable, material=material, object=object)
                    offsetvalue = value
                    scalevalue = 1
                    if 'Rotate' in variable:
                        in_amount = in_amount / 180 * pi
                        out_amount = out_amount / 180 * pi
                    if 'Slide' in variable:
                        scalevalue = 1+(z_offset*.457)
                        offsetvalue = offsetvalue / pos_multiplier
                    if variable == 'Alpha' or variable == 'Width' or variable == 'Height' or variable == 'Depth':
                        offsetvalue = 0
                        material.use_transparency = True
                    if fcurve:
                        points = []
                        if animation_preset.animate_in:
                            points.append((start_frame+animation_preset.in_offset, (offsetvalue+in_amount)*scalevalue))
                            points.append((start_frame+animation_preset.in_offset+animation_preset.in_length, value))
                        else:
                            points.append((start_frame, value))
                        if animation_preset.animate_out:
                            points.append((end_frame+animation_preset.out_offset-animation_preset.out_length, value))
                            points.append((end_frame+animation_preset.out_offset, (offsetvalue+out_amount)*scalevalue))
                        else:
                            points.append((end_frame, value))
                        clear_keyframes(fcurve)
                        for index, point in enumerate(points):
                            fcurve.keyframe_points.add()
                            fcurve.keyframe_points[index].co = point
                        fcurve.update()

        if selected_object and object_preset.set_material:
            #search for other objects using same material name and update their settings to match the selected object
            for other_object in quicktitle.objects:
                if other_object.material == object_preset.material:
                    other_object.cast_shadows = object_preset.cast_shadows
                    other_object.use_shadeless = object_preset.use_shadeless
                    other_object.use_transparency = object_preset.use_transparency
                    other_object.alpha = object_preset.alpha
                    other_object.diffuse_color = object_preset.diffuse_color
                    other_object.specular_intensity = object_preset.specular_intensity
                    other_object.specular_hardness = object_preset.specular_hardness
                    other_object.specular_color = object_preset.specular_color
                    other_object.texture = object_preset.texture
                    other_object.alpha_texture = object_preset.alpha_texture

    #update scene and sequence
    scene.name = scenename
    sequence.name = scenename
    bpy.context.screen.scene = oldscene
    scene.update()
    bpy.ops.sequencer.reload(adjust_length=True)
    bpy.ops.sequencer.refresh_all()

def get_fcurve(fcurves, variable, material=None, object=None):
    #find and return an fcurve matching the given internal script variable name
    fcurve = None
    value = None
    if variable == 'Alpha':
        data_path = 'active_material.alpha'
        if material:
            value = material.alpha
        fcurve = fcurves.find(data_path)
        if not fcurve:
            fcurve = fcurves.new(data_path)
    elif variable == 'X Slide':
        data_path = 'location'
        if object:
            value = object.location[0]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 0:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 0)
    elif variable == 'Y Slide':
        data_path = 'location'
        if object:
            value = object.location[1]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 1:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 1)
    elif variable == 'Z Slide':
        data_path = 'location'
        if object:
            value = object.location[2]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 2:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 2)
    elif variable == 'X Rotate':
        data_path = 'rotation_euler'
        if object:
            value = object.rotation_euler[0]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 0:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 0)
    elif variable == 'Y Rotate':
        data_path = 'rotation_euler'
        if object:
            value = object.rotation_euler[1]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 1:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 1)
    elif variable == 'Z Rotate':
        data_path = 'rotation_euler'
        if object:
            value = object.rotation_euler[2]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 2:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 2)
    elif variable == 'Width':
        data_path = 'scale'
        if object:
            value = object.scale[0]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 0:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 0)
    elif variable == 'Height':
        data_path = 'scale'
        if object:
            value = object.scale[1]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 1:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 1)
    elif variable == 'Depth':
        data_path = 'scale'
        if object:
            value = object.scale[2]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 2:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index = 2)
    return (fcurve, value)

def clear_keyframes(fcurve):
    #Removes all points on a curve
    index = len(fcurve.keyframe_points) - 1
    while index >= 0:
        fcurve.keyframe_points.remove(fcurve.keyframe_points[index], fast=True)
        index = index-1

def quicktitle_object_icon(type):
    #returns an icon name for a given internal object type
    if type == "TEXT":
        return "FONT_DATA"
    elif type == "BOX":
        return "MESH_PLANE"
    elif type == "CIRCLE":
        return "MESH_CIRCLE"
    elif type == "IMAGE":
        return "IMAGE_DATA"
    else:
        return "DOT"

def quicktitle_animation_icon(type):
    #returns an icon name for a given internal animation type
    if type == "Alpha":
        return "IMAGE_RGB_ALPHA"
    elif type == "X Slide":
        return "MAN_TRANS"
    elif type == "Y Slide":
        return "MAN_TRANS"
    elif type == "Z Slide":
        return "MAN_TRANS"
    elif type == "X Rotate":
        return "MAN_ROT"
    elif type == "Y Rotate":
        return "MAN_ROT"
    elif type == "Z Rotate":
        return "MAN_ROT"
    elif type == "Width":
        return "MAN_SCALE"
    elif type == "Height":
        return "MAN_SCALE"
    elif type == "Depth":
        return "MAN_SCALE"
    else:
        return "DOT"

class QuickTitleAnimation(bpy.types.PropertyGroup):
    #animation object stored in quicktitle objects
    variable=bpy.props.StringProperty(
        name = "Animation Variable Name",
        default = 'Alpha')
    animate_in=bpy.props.BoolProperty(
        name = "Animate Variable In",
        default = True,
        description = "This will determine if this animation will change this variable from the beginning of the title.",
        update = quicktitle_autoupdate)
    animate_out=bpy.props.BoolProperty(
        name = "Animate Variable Out",
        default = True,
        description = "This will determine if this animation will change this variable at the end of the title.",
        update = quicktitle_autoupdate)
    in_length=bpy.props.IntProperty(
        name = "Length Of In Animation",
        default = 15,
        min = 0,
        description = "Length in frames of the animation applied to the beginning of the title.",
        update = quicktitle_autoupdate)
    out_length=bpy.props.IntProperty(
        name = "Length Of Out Animation",
        default = 15,
        min = 0,
        description = "Length in frames of the animation applied to the ending of the title.",
        update = quicktitle_autoupdate)
    in_offset=bpy.props.IntProperty(
        name = "Frame Offset Of In Animation",
        default = 0,
        description = "Distance in frames the animation will be offset from the beginning of the title.  Positive values result in a delayed animation, negative values result in an animation beginning before the start of the title.",
        update = quicktitle_autoupdate)
    out_offset=bpy.props.IntProperty(
        name = "Frame Offset Of Out Animation",
        default = 0,
        description = "Distance in frames the animation will be offset from the end of the title.  Positive values result in a delayed animation, negative values result in an animation beginning before the start of the title.",
        update = quicktitle_autoupdate)
    in_amount=bpy.props.FloatProperty(
        name = "Amount Of In Animation",
        default = 1,
        description = "Beginning value of the starting animation.  This is a float with any value allowed, but depending on the variable being animated, some values will not make sense.",
        update = quicktitle_autoupdate)
    out_amount=bpy.props.FloatProperty(
        name = "Amount Of Out Animation",
        default = 1,
        description = "Ending value of the end animation.  This is a float with any value allowed, but depending on the variable being animated, some values will not make sense.",
        update = quicktitle_autoupdate)

class QuickTitleObject(bpy.types.PropertyGroup):
    #Preset for objects stored in a title scene
    
    #Basic variables for all object types:
    name=bpy.props.StringProperty(
        name = "Object Name",
        description = "Name to identify this object.")
    internal_name=bpy.props.StringProperty(
        name = "Blender Name",
        description = "Reference name to this object used by Blender.")
    type=bpy.props.EnumProperty(
        name = "Object Type",
        items = [('TEXT', 'Text', '', 1),('IMAGE', 'Image', '', 2),('BOX', 'Box', '', 3),('CIRCLE', 'Circle', '', 4)],
        description = "Type of object")
    x=bpy.props.FloatProperty(
        name = "Object X Location",
        default = 0,
        description = "Horizontal location of this object.  0 is centered, 1 is the right side of screen, -1 is the left side of screen.",
        update = quicktitle_autoupdate)
    y=bpy.props.FloatProperty(
        name = "Object Y Location",
        default = 0,
        description = "Vertical location of this object.  0 is centered, top and bottom vary depending on the aspect ratio of the screen, 0.56 will usually be at the top, -0.56 at the bottom.",
        update = quicktitle_autoupdate)
    z=bpy.props.FloatProperty(
        name = "Object Z Position",
        default = 0,
        description = "Offset for 3d positioning of this object.  This value will affect the position and size of this object, as well as position above or below other objects.",
        update = quicktitle_autoupdate)
    rot_x=bpy.props.FloatProperty(
        name = 'X Rotation',
        default = 0,
        description = 'Object rotation around the X axis (forward and back tilting).',
        update = quicktitle_autoupdate)
    rot_y=bpy.props.FloatProperty(
        name = 'Y Rotation',
        default = 0,
        description = 'Object rotation around the Y axis (left and right wobble).',
        update = quicktitle_autoupdate)
    rot_z=bpy.props.FloatProperty(
        name = 'Z Rotation',
        default = 0,
        description = 'Object rotation around the Z axis (spin).',
        update = quicktitle_autoupdate)
    scale=bpy.props.FloatProperty(
        name = "Overall Object Scale",
        default = 1,
        min = 0,
        description = "Overall scaling of this object.  1 is the original size, 0.5 is half size, 2 is double size.",
        update = quicktitle_autoupdate)
    width=bpy.props.FloatProperty(
        name = "Object Width Multiplier",
        default = 1,
        min = 0,
        description = "Multiplies the size of the object on the width axis.  1 is original size, 0.5 is half size, 2 is double size.",
        update = quicktitle_autoupdate)
    height=bpy.props.FloatProperty(
        name = "Object Height Multiplier",
        default = 1,
        min = 0,
        description = "Multiplies the size of the object on the height axis.  1 is the original size, 0.5 is half size, 2 is double size.",
        update = quicktitle_autoupdate)
    shear=bpy.props.FloatProperty(
        name = "Shearing",
        default = 0,
        min = -1,
        max = 1,
        description = "Creates an italic effect by shearing the object.  0 is no shearing, 1 is full forward lean, -1 is full backward lean.",
        update = quicktitle_autoupdate)
    set_material=bpy.props.BoolProperty(
        name = "Set Material",
        default = False,
        description = "When unchecked, this object will use a default material, when checked, you may set the material manually.",
        update = quicktitle_autoupdate)
    material=bpy.props.StringProperty(
        name = "Object Material",
        default = "No Preset",
        update = quicktitle_autoupdate)
    internal_material=bpy.props.StringProperty(
        name = "Internal Object Material Name",
        default = "No Preset")
    cast_shadows=bpy.props.BoolProperty(
        name = "Cast Shadows",
        default = True,
        description = "Allow this object to cast shadows on objects behind it.",
        update = quicktitle_autoupdate)
    use_shadeless=bpy.props.BoolProperty(
        name = "Shadeless",
        default = False,
        description = "Give this material a solid color with no shading or specularity.",
        update = quicktitle_autoupdate)
    use_transparency=bpy.props.BoolProperty(
        name = "Transparency",
        default = False,
        description = "Enables transparency on this object.",
        update = quicktitle_autoupdate)
    alpha=bpy.props.FloatProperty(
        name = "Opacity",
        default = 1,
        min = 0,
        max = 1,
        description = "Opacity controls the transparency of this object.  1 is fully visible, 0.5 is half transparent, 0 is invisible.",
        update = quicktitle_autoupdate)
    diffuse_color=bpy.props.FloatVectorProperty(
        name = "Color Of The Material",
        size = 3,
        default = (1, 1, 1),
        min = 0,
        max = 1,
        subtype = 'COLOR',
        description = "Basic color of this object.",
        update = quicktitle_autoupdate)
    specular_intensity=bpy.props.FloatProperty(
        name = "Material Specularity",
        default = 0.5,
        min = 0,
        max = 1,
        description = "Controls the specularity, or shininess of this material.",
        update = quicktitle_autoupdate)
    specular_hardness=bpy.props.IntProperty(
        name = "Specular Hardness",
        default = 50,
        min = 1,
        max = 511,
        description = "Controls the sharpness of the specularity of this material.",
        update = quicktitle_autoupdate)
    specular_color=bpy.props.FloatVectorProperty(
        name = "Color Of The Specularity",
        size = 3,
        default = (1, 1, 1),
        min = 0,
        max = 1,
        subtype = 'COLOR',
        description = "Specular color of this object.",
        update = quicktitle_autoupdate)
    animations=bpy.props.CollectionProperty(
        type=QuickTitleAnimation)
    selected_animation=bpy.props.IntProperty(
        name = 'Selected Animation')
    
    #Variables specific to the Box and Text types:
    extrude=bpy.props.FloatProperty(
        name = "Extrude Amount",
        default = 0,
        min = 0,
        description = "Amount of 3d extrusion to apply to this object.",
        update = quicktitle_autoupdate)
    bevel=bpy.props.FloatProperty(
        name = "Bevel Size",
        default = 0,
        min = 0,
        description = "Size of the added beveled edge.",
        update = quicktitle_autoupdate)
    bevel_resolution=bpy.props.IntProperty(
        name = "Bevel Resolution",
        default = 0,
        min = 0,
        description = "Number of subdivisions on the beveled edge.",
        update = quicktitle_autoupdate)
    
    #Variables specific to the Text type:
    text=bpy.props.StringProperty(
        name = "Text",
        default = "None",
        update = quicktitle_autoupdate)
    font=bpy.props.StringProperty(
        name = "Font",
        default = "Bfont",
        description = "Selected font for this text object",
        update = quicktitle_autoupdate)
    word_wrap=bpy.props.BoolProperty(
        name = "Word Wrapping",
        default = True,
        description = "Enables word-wrapping on text objects to limit the text line width.",
        update = quicktitle_autoupdate)
    wrap_width=bpy.props.FloatProperty(
        name = "Word Wrap Width",
        default = .9,
        min = .01,
        description = "If word-wrap is enabled, this will determine the width of the text box.  The actual size varies based on object scale.  At a scale of 1, 1 is the full width of the screen, 0.5 is half width, 0.01 will result in one word per line.",
        update = quicktitle_autoupdate)
    align=bpy.props.EnumProperty(
        name = "Text Alignment",
        items = [('LEFT', 'Left', '', 1), ('CENTER', 'Center', '', 2), ('RIGHT', 'Right', '', 3), ('JUSTIFY', 'Justify', '', 4), ('FLUSH', 'Flush', '', 5)],
        default = 'CENTER',
        description = "Determines the position of the text within the wrapping box.",
        update = quicktitle_autoupdate)
    
    #Variables specific to the Image type:
    texture=bpy.props.StringProperty(
        name = "Image Texture",
        default = "",
        description = "File path to the image or video texture.",
        subtype = 'FILE_PATH',
        update = quicktitle_autoupdate)
    alpha_texture=bpy.props.StringProperty(
        name = "Alpha Transparent Texture",
        default = "",
        description = "File path to the image used for transparency.",
        subtype = 'FILE_PATH',
        update = quicktitle_autoupdate)

class QuickTitle(bpy.types.PropertyGroup):
    #preset for a QuickTitle scene
    name=bpy.props.StringProperty(
        name = "Preset Name",
        default = "Default",
        description = "Name to identify this preset.",
        update = quicktitle_autoupdate)
    description=bpy.props.StringProperty(
        name = "Description",
        default = "",
        description = "Use this text area to describe the preset in detail.")
    z_scale=bpy.props.FloatProperty(
        name = "Z Depth Scale",
        default = 1,
        min = 0,
        description = "Determines the depth distance between objects in the title.  This affects the size of the shadows as well.  A value of 0 will place all objects on the same level, 1 is default.",
        update = quicktitle_autoupdate_all)
    objects=bpy.props.CollectionProperty(
        type=QuickTitleObject)
    selected_object=bpy.props.IntProperty(
        name = "Selected Object",
        default = 0,
        min = 0)
    enable_shadows=bpy.props.BoolProperty(
        name = "Shadows",
        default = True,
        description = "Enables shadows in this title.",
        update = quicktitle_autoupdate)
    shadowlamp_internal_name=bpy.props.StringProperty(
        name = "Internal Name For The Shadow Lamp",
        default = '')
    shadowsize=bpy.props.FloatProperty(
        name = "Shadow Distance",
        default = 1,
        min = 0,
        description = "Distance of the shadow casting lamp, determines the overall size of the shadows.",
        update = quicktitle_autoupdate)
    shadowamount=bpy.props.FloatProperty(
        name = "Shadow Amount",
        default = .5,
        min = 0,
        description = "Overall opacity of the shadow.  0 is no shadows, 1 is full shadows.",
        update = quicktitle_autoupdate)
    shadowsoft=bpy.props.FloatProperty(
        name = "Shadow Softness",
        default = 1,
        min = 0,
        description = "The amount of blur applied to the shadow.  A value of 0 results in fully sharp shadows.",
        update = quicktitle_autoupdate)
    shadowx=bpy.props.FloatProperty(
        name = "Shadow Lamp X Position",
        default = 0,
        description = "Horizontal position of the shadow casting lamp.  -1 is the left side of the screen, 0 is centered, and 1 is the right side of the screen.",
        update = quicktitle_autoupdate)
    shadowy=bpy.props.FloatProperty(
        name = "Shadow Lamp Y Position",
        default = 0,
        description = "Vertical position of the shadow casting lamp.  Values depend on the image aspect ratio, 0.56 will usually be around the top of the screen, 0 at the center, and -0.56 around the bottom.",
        update = quicktitle_autoupdate)
    length=bpy.props.IntProperty(
        name = "Scene Length",
        default = 300,
        description = "Length of the title preset in frames.  Change this value to automatically adjust animations and scene length.",
        update = quicktitle_autoupdate)
    qualityshadows=bpy.props.BoolProperty(
        name = "High Quality Shadows",
        default = False,
        description = "This will switch shadows to ray tracing mode, making them more accurate and smooth, but greatly increasing render times.",
        update = quicktitle_autoupdate)

class QuickTitleObjectListItem(bpy.types.UIList):
    #Draw an object in the object list in the QuickTitler panel
    
    def draw_filter(self, context, layout):
        #prevent filter options from being visible
        pass

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(percentage=0.9)
        split.label(item.name, icon=quicktitle_object_icon(item.type))
        split.operator('quicktitler.delete_object', icon="X", text="").index = index

class QuickTitleAnimationListItem(bpy.types.UIList):
    #Draw an animation in the animation list

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(percentage=0.9)
        split.label(item.variable, icon=quicktitle_animation_icon(item.variable))
        split.operator('quicktitler.delete_animation', icon="X", text="").index = index

class QuickTitlingPanel(bpy.types.Panel):
    #Panel for QuickTitling settings and operators
    bl_label = "Quick Titling"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    
    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, contex):
        scene = bpy.context.scene
        layout = self.layout

        quicktitle_sequence = titling_scene_selected()
        quicktitle_preset = current_quicktitle(quicktitle_sequence)
        if not quicktitle_preset:
            #No presets found, show create preset button
            row = layout.row()
            row.operator('quicktitler.preset_manipulate', text="New Title Preset").operation = "Add"
            row.operator('quicktitler.preset_import', text='Import')
        else:
            if quicktitle_sequence:
                #A valid quicktitle is selected, enter edit mode
                row = layout.row()
                row.operator('quicktitler.create', text='Update Title').action = 'update_all'
                row.operator('quicktitler.replace_image', text='Render To Image')
                
                row = layout.row()
                row.prop(bpy.context.scene.quicktitler, 'autoupdate')
                
                outline = layout.box()
                
                row = outline.row()
                split = row.split(percentage=0.8)
                split.prop(quicktitle_preset, 'name', text="Editing")
                split.operator('quicktitler.preset_export', text='Export')
                
                row = outline.row()
                row.operator('quicktitler.copy_back', text="Copy Preset Back To Scene")
            else:
                #No quicktitle is selected, show preset editor
                row = layout.row()
                row.operator('quicktitler.create', text='Create New Title').action = 'create'
                
                row = layout.row()
                row.prop(bpy.context.scene.quicktitler, 'autoupdate')
                
                outline = layout.box()
                
                row = outline.row()
                split = row.split(percentage=0.66, align=True)
                split.label('Select Preset:')
                split.operator('quicktitler.preset_manipulate', text='New').operation = 'Add'
                split.operator('quicktitler.preset_import', text='Import')
                
                row = outline.row()
                split = row.split(percentage=0.66, align=True)
                split.menu('quicktitler.preset_menu', text=quicktitle_preset.name)
                split.operator('quicktitler.preset_manipulate', text='Copy').operation = 'Copy'
                #split.operator('quicktitler.preset_manipulate', text='Delete').operation = 'Delete'
                split.operator('quicktitler.preset_export', text='Export')
                
            row = layout.row()
            row.prop(quicktitle_preset, 'name')

            row = layout.row()
            row.prop(quicktitle_preset, 'description')
            
            row = layout.row()
            row.prop(quicktitle_preset, 'length')
            row.prop(quicktitle_preset, 'z_scale')
            
            row = layout.row()
            row.label("Objects:")
            preset_objects = quicktitle_preset.objects
            current_object_index = quicktitle_preset.selected_object
            if len(preset_objects) >= current_object_index+1:
                current_object = preset_objects[current_object_index]
            else:
                current_object = False
            
            row = layout.row()
            row.template_list("QuickTitleObjectListItem", "", quicktitle_preset, 'objects', quicktitle_preset, 'selected_object', rows=2)
            col = row.column(align=True)
            col.operator("quicktitler.object_up", text="", icon="TRIA_UP").index = quicktitle_preset.selected_object
            col.operator("quicktitler.object_down", text="", icon="TRIA_DOWN").index = quicktitle_preset.selected_object
            
            row = layout.row(align=True)
            row.label("Add:")
            row.operator('quicktitler.add_object', text='Text', icon=quicktitle_object_icon('TEXT')).type = 'TEXT'
            row.operator('quicktitler.add_object', text='Image', icon=quicktitle_object_icon('IMAGE')).type = 'IMAGE'
            row.operator('quicktitler.add_object', text='Box', icon=quicktitle_object_icon('BOX')).type = 'BOX'
            row.operator('quicktitler.add_object', text='Circle', icon=quicktitle_object_icon('CIRCLE')).type = 'CIRCLE'
            
            if current_object:
                #Object settings
                outline = layout.box()
                
                row = outline.row()
                row.prop(current_object, 'name', text='Object Name', icon=quicktitle_object_icon(current_object.type))

                if current_object.type == 'TEXT':
                    subarea = outline.box()
                    
                    row = subarea.row()
                    row.prop(current_object, 'text')
                    
                    row = subarea.row()
                    split = row.split(percentage=0.9, align=True)
                    split.menu('quicktitler.fonts_menu', text=current_object.font)
                    split.operator('quicktitler.load_font', text='+')
                    
                    row = subarea.row()
                    row.prop(current_object, 'word_wrap', text='Wrapping')
                    row.prop(current_object, 'wrap_width', text='Width')
                    
                    row = subarea.row()
                    row.prop(current_object, 'align', expand=True)

                row = outline.row(align=True)
                split = row.split(percentage=.15, align=True)
                split.label('Pos:')
                split.prop(current_object, 'x', text='X')
                split.prop(current_object, 'y', text='Y')
                split.prop(current_object, 'z', text='Z')
                
                row = outline.row(align=True)
                split = row.split(percentage=.15, align=True)
                split.label('Rot:')
                split.prop(current_object, 'rot_x', text='X')
                split.prop(current_object, 'rot_y', text='Y')
                split.prop(current_object, 'rot_z', text='Z')
                
                row = outline.row()
                row.prop(current_object, 'shear', text='Shearing')
                row.prop(current_object, 'scale', text='Scale')
                
                row = outline.row(align=True)
                row.prop(current_object, 'width', text='Width')
                row.prop(current_object, 'height', text='Height')

                if current_object.type == 'TEXT' or current_object.type == 'BOX' or current_object.type == 'CIRCLE':
                    subarea = outline.box()
                    
                    row = subarea.row()
                    row.label('Thickness', icon="MESH_CUBE")
                    row.prop(current_object, 'extrude', text='Amount')
                    
                    row = subarea.row(align=True)
                    row.prop(current_object, 'bevel', text='Bevel')
                    row.prop(current_object, 'bevel_resolution', text='Resolution')

                subarea = outline.box()
                
                row = subarea.row()
                row.label(text='Material:', icon="MATERIAL_DATA")
                row.prop(current_object, 'set_material', text='Set Material')
                
                if current_object.set_material:
                    row = subarea.row()
                    row.menu('quicktitler.materials_menu', text=current_object.material)
                    
                row = subarea.row()
                split = row.split(percentage=.85)
                subsplit = split.split()
                subsplit.prop(current_object, 'use_shadeless', text='Use No Shading')
                subsplit.prop(current_object, 'cast_shadows', text='Cast Shadows')
                split.prop(current_object, 'diffuse_color', text='')
                
                row = subarea.row()
                split = row.split(percentage=.85, align=True)
                subsplit = split.split(align=True)
                subsplit.prop(current_object, 'specular_intensity', text="Specular")
                subsplit.prop(current_object, 'specular_hardness', text="Hardness")
                split.prop(current_object, 'specular_color', text="")
                
                row = subarea.row()
                row.prop(current_object, 'use_transparency', text='Transparency')
                row.prop(current_object, 'alpha', text='Alpha')
                
                if current_object.type == 'IMAGE':
                    row = subarea.row()
                    row.prop(current_object, 'texture', text='Texture', icon="IMAGE_RGB")
                    
                    row = subarea.row()
                    row.prop(current_object, 'alpha_texture', text='Alpha Texture', icon="IMAGE_ALPHA")
                
                subarea = outline.box()
                
                row = subarea.row()
                row.menu('quicktitler.animations_menu', text='Add Animation', icon="ANIM_DATA")
                
                if current_object.animations:
                    row = subarea.row()
                    row.operator('quicktitler.apply_animations', text='Apply To All Objects')
                    
                    row = subarea.row()
                    row.template_list("QuickTitleAnimationListItem", "", current_object, 'animations', current_object, 'selected_animation', rows=2)
                    
                    if current_object.selected_animation < len(current_object.animations):
                        animation = current_object.animations[current_object.selected_animation]
                        
                        row = subarea.row()
                        row.prop(animation, 'animate_in', text='Animate In')
                        row.prop(animation, 'animate_out', text='Animate Out')
                        
                        row = subarea.row()
                        row.prop(animation, 'in_length', text='In Length')
                        row.prop(animation, 'out_length', text='Out Length')
                        
                        row = subarea.row()
                        row.prop(animation, 'in_offset', text='In Frame Offset')
                        row.prop(animation, 'out_offset', text='Out Frame Offset')
                        
                        row = subarea.row()
                        row.prop(animation, 'in_amount', text='In Amount')
                        row.prop(animation, 'out_amount', text='Out Amount')
            
            #Shadow section
            outline = layout.box()
            
            row = outline.row()
            split = row.split(percentage=.1)
            split.prop(quicktitle_preset, 'enable_shadows', icon="TRIA_DOWN" if quicktitle_preset.enable_shadows else "TRIA_RIGHT", icon_only=True, emboss=True)
            split.label('Title Shadows', icon="LAMP_SPOT")
            
            if quicktitle_preset.enable_shadows:
                row = outline.row()
                row.prop(quicktitle_preset, 'shadowamount')
                
                row = outline.row()
                row.prop(quicktitle_preset, 'shadowsize', text='Distance')
                row.prop(quicktitle_preset, 'shadowsoft', text='Soft')
                
                row = outline.row(align=True)
                row.prop(quicktitle_preset, 'shadowx', text='X Offset')
                row.prop(quicktitle_preset, 'shadowy', text='Y Offset')
                
                row = outline.row()
                row.prop(quicktitle_preset, 'qualityshadows')

class QuickTitlingCopyBack(bpy.types.Operator):
    #Operator to copy the preset from a selected QuickTitle back to the main scene
    bl_idname = 'quicktitler.copy_back'
    bl_label = 'Copy Title Preset Back To Scene'
    bl_description = 'Copies the preset from a selected title strip back to the main scene, replacing settings on any preset with the same name.'
    
    def execute(self, context):
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            scene = quicktitle_sequence.scene
            quicktitle = scene.quicktitles[0]
            parent_scene = bpy.context.scene
            found_preset = False
            for preset in parent_scene.quicktitles:
                if preset.name == quicktitle.name:
                    found_preset = True
                    copy_title_preset(quicktitle, preset)
            if not found_preset:
                preset = parent_scene.quicktitles.add()
                copy_title_preset(quicktitle, preset)
        return {'FINISHED'}

class QuickTitlingReplaceWithImage(bpy.types.Operator, ExportHelper):
    #operator that renders out the middle frame of a title scene to an image, then mutes the original sequence and loads that image in
    bl_idname = 'quicktitler.replace_image'
    bl_label = 'Replace With Image'
    bl_description = 'Renders out an image of the quicktitle scene, and places it on the timeline while muting the original.'
    
    filepath = bpy.props.StringProperty()
    filename_ext = ".png"
    filter_glob = bpy.props.StringProperty(default="*.png", options={'HIDDEN'})
    check_extension = True
    
    def invoke(self, context, event):
        #set the default filename
        quicktitle = current_quicktitle()
        if quicktitle:
            self.filepath = quicktitle.name
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        #after the file browser is closed, save the image
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            if self.filepath.endswith('.png'):
                imagepath = self.filepath
            else:
                imagepath = self.filepath+'.png'
            scene = quicktitle_sequence.scene
            scene.render.filepath = imagepath
            oldscene = bpy.context.scene
            scene.frame_current = scene.frame_end / 2
            bpy.context.screen.scene = scene
            bpy.ops.render.render(write_still=True)
            bpy.context.screen.scene = oldscene
            self.report({'INFO'}, "Rendered QuickTitle as: "+imagepath)
            
            #load the image into the sequencer
            start_frame = quicktitle_sequence.frame_final_start
            end_frame = quicktitle_sequence.frame_final_start + quicktitle_sequence.frame_final_duration - 1
            quicktitle_sequence.mute = True
            path, file = os.path.split(imagepath)
            bpy.ops.sequencer.image_strip_add(directory=path, files=[{'name':file}], frame_start=start_frame, frame_end=end_frame)
            bpy.context.scene.sequence_editor.active_strip.blend_type = 'ALPHA_OVER'
        return {'FINISHED'}

class QuickTitlingObjectMoveUp(bpy.types.Operator):
    #Operator to move a specific object up in the list of objects, object index must be specified
    bl_idname = 'quicktitler.object_up'
    bl_label = 'Move Up'
    bl_description = 'Moves an object up in the current QuickTitling preset.'
    
    index = bpy.props.IntProperty()
    
    def execute(self, context):
        scene = find_titling_scene()
        quicktitle = scene.quicktitles[0]
        objects = quicktitle.objects
        if self.index > 0:
            objects.move(self.index, self.index - 1)
            if quicktitle.selected_object == self.index:
                quicktitle.selected_object = self.index - 1
            elif quicktitle.selected_object == self.index - 1:
                quicktitle.selected_object = self.index
        quicktitle_autoupdate_all()
        return {'FINISHED'}

class QuickTitlingObjectMoveDown(bpy.types.Operator):
    #Operator to move a specific object down in the list of objects, object index must be specified
    bl_idname = 'quicktitler.object_down'
    bl_label = 'Move Down'
    bl_description = 'Moves an object down in the current QuickTitling preset.'
    
    index = bpy.props.IntProperty()
    
    def execute(self, context):
        scene = find_titling_scene()
        quicktitle = scene.quicktitles[0]
        objects = quicktitle.objects
        if self.index+1 < len(objects):
            objects.move(self.index, self.index + 1)
            if quicktitle.selected_object == self.index:
                quicktitle.selected_object = self.index + 1
            elif quicktitle.selected_object == self.index + 1:
                quicktitle.selected_object = self.index
        quicktitle_autoupdate_all()
        return {'FINISHED'}

class QuickTitlingObjectAdd(bpy.types.Operator):
    #Operator to add an object in the current QuickTitler preset, type must be specified
    bl_idname = 'quicktitler.add_object'
    bl_label = 'Add Object'
    bl_description = 'Add an object in the current QuickTitling preset'
    
    type = bpy.props.StringProperty()
    
    def execute(self, context):
        scene = find_titling_scene()
        object = scene.quicktitles[0].objects.add()
        object.type = self.type
        if object.type == 'IMAGE':
            object.specular_intensity = 0
            object.cast_shadows = False
            object.use_shadeless = True
        index = len(scene.quicktitles[0].objects) - 1
        scene.quicktitles[0].objects.move(index, 0)
        scene.quicktitles[0].selected_object = 0
        quicktitle_autoupdate_all()
        return {'FINISHED'}

class QuickTitlingObjectSelect(bpy.types.Operator):
    #Operator to select an object in the current QuickTitler preset, index must be specified
    bl_idname = 'quicktitler.select_object'
    bl_label = 'Select Object'
    bl_description = 'Select an object in the current QuickTitling preset'
    
    index = bpy.props.IntProperty()
    
    def execute(self, context):
        scene = find_titling_scene()
        scene.quicktitles[0].selected_object = self.index
        return {'FINISHED'}

class QuickTitlingObjectDelete(bpy.types.Operator):
    #Operator to delete an object in the current QuickTitler preset, index must be specified
    bl_idname = 'quicktitler.delete_object'
    bl_label = 'Delete Object'
    bl_description = 'Delete an object in the current QuickTitling preset'
    
    index = bpy.props.IntProperty()
    
    def execute(self, context):
        quicktitle_sequence = titling_scene_selected()
        scene = find_titling_scene()
        if quicktitle_sequence:
            objectinfo = scene.quicktitles[0].objects[self.index]
            if objectinfo.internal_name in scene.objects:
                object = scene.objects[objectinfo.internal_name]
                scene.objects.unlink(object)
        scene.quicktitles[0].objects.remove(self.index)
        quicktitle_autoupdate_all()
        return {'FINISHED'}

class QuickTitlingAnimationApply(bpy.types.Operator):
    #Operator to apply the current object's animations to all objects in the QuickTitler preset
    bl_idname = 'quicktitler.apply_animations'
    bl_label = 'Apply Animations'
    bl_description = "Applies the current object's animations to all objects in the current QuickTitler preset"
    
    def execute(self, context):
        scene = find_titling_scene()
        current_object = get_current_object()
        quicktitle = current_quicktitle()
        for object in quicktitle.objects:
            if object != current_object:
                object.animations.clear()
                for animation in current_object.animations:
                    new_animation = object.animations.add()
                    new_animation.variable = animation.variable
                    new_animation.animate_in = animation.animate_in
                    new_animation.animate_out = animation.animate_out
                    new_animation.in_length = animation.in_length
                    new_animation.out_length = animation.out_length
                    new_animation.in_offset = animation.in_offset
                    new_animation.out_offset = animation.out_offset
                    new_animation.in_amount = animation.in_amount
                    new_animation.out_amount = animation.out_amount
        quicktitle_autoupdate_all()
        return {'FINISHED'}

class QuickTitlingAnimationAdd(bpy.types.Operator):
    #Operator to add an animation to the current object in the current QuickTitler preset.  Animation preset index must be specified
    bl_idname = 'quicktitler.add_animation'
    bl_label = 'Add Animation'
    bl_description = 'Add an animation to the current object in the current QuickTitling preset'
    
    index = bpy.props.IntProperty()
    
    def execute(self, context):
        scene = find_titling_scene()
        object = get_current_object()
        animation_preset = animations[self.index]
        animation = False
        for animation_set in object.animations:
            if animation_set.variable == animation_preset['variable']:
                #an animation of this type already exists, overwrite it
                animation = animation_set
        if not animation:
            animation = object.animations.add()
            
        #update all animation variables
        animation.variable = animation_preset['variable']
        animation.animate_in = animation_preset['animate_in']
        animation.animate_out = animation_preset['animate_out']
        animation.in_length = animation_preset['in_length']
        animation.out_length = animation_preset['out_length']
        animation.in_offset = animation_preset['in_offset']
        animation.out_offset = animation_preset['out_offset']
        animation.in_amount = animation_preset['in_amount']
        animation.out_amount = animation_preset['out_amount']
        object.selected_animation = len(object.animations) - 1
        quicktitle_autoupdate()
        return {'FINISHED'}

class QuickTitlingAnimationDelete(bpy.types.Operator):
    #Operator to delete an animation in the current selected object of the current QuickTitler preset.  Animation index must be specified
    bl_idname = 'quicktitler.delete_animation'
    bl_label = 'Delete Animation'
    bl_description = 'Delete an animation from the current object in the current QuickTitling preset'
    
    index = bpy.props.IntProperty()
    
    def execute(self, context):
        quicktitle_sequence = titling_scene_selected()
        scene = find_titling_scene()
        object_preset = get_current_object()
        object_preset.animations.remove(self.index)
        quicktitle_autoupdate()
        return {'FINISHED'}

class QuickTitlingAnimationMenu(bpy.types.Menu):
    #Menu for listing animation types
    bl_idname = 'quicktitler.animations_menu'
    bl_label = 'List of animations'
    
    def draw(self, context):
        layout = self.layout
        for index, animation in enumerate(animations):
            layout.operator('quicktitler.add_animation', text=animation['name'], icon=quicktitle_animation_icon(animation['variable'])).index = index

class QuickTitlingPresetDelete(bpy.types.Operator):
    #Operator to delete a QuickTitler preset.  Preset index must be specified
    bl_idname = 'quicktitler.preset_delete'
    bl_label = 'Delete Presets'
    bl_description = 'Delete A Specific QuickTitling Preset'
    
    index = bpy.props.IntProperty()
    
    def execute(self, context):
        scene = context.scene
        scene.quicktitles.remove(self.index)
        return {'FINISHED'}

class QuickTitlingPresetExport(bpy.types.Operator, ExportHelper):
    #Operator to export the current QuickTitler preset to a file.
    bl_idname = 'quicktitler.preset_export'
    bl_label = 'Export Preset'
    bl_description = 'Exports the current selected QuickTitling preset to a file'
    
    filename_ext = ".xml"
    filter_glob = bpy.props.StringProperty(default="*.xml", options={'HIDDEN'})
    filepath = bpy.props.StringProperty()
    check_extension = True
    
    def invoke(self, context, event):
        #Set up the default filename
        quicktitle = current_quicktitle()
        if quicktitle:
            self.filepath = quicktitle.name
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        #a file has been selected, save to that file
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            #render out a preview image
            if self.filepath.endswith('.xml'):
                imagepath = self.filepath[:-4]
            else:
                imagepath = self.filepath
            if imagepath.endswith('.jpg'):
                imagepath = self.filepath
            else:
                imagepath = imagepath+'.jpg'
            scene = quicktitle_sequence.scene
            scene.render.filepath = imagepath
            old_file_format = scene.render.image_settings.file_format
            old_quality = scene.render.image_settings.quality
            old_resolution_percentage = scene.render.resolution_percentage
            old_color_mode = scene.render.image_settings.color_mode
            scene.render.image_settings.file_format = 'JPEG'
            scene.render.image_settings.quality = 80
            scene.render.resolution_percentage = 50
            scene.render.image_settings.color_mode = 'RGB'
            
            oldscene = bpy.context.scene
            scene.frame_current = scene.frame_end / 2
            bpy.context.screen.scene = scene
            bpy.ops.render.render(write_still=True)
            bpy.context.screen.scene = oldscene
            self.report({'INFO'}, "Rendered QuickTitle Preview As: "+imagepath)
            
            scene.render.image_settings.file_format = old_file_format
            scene.render.image_settings.quality = old_quality
            scene.render.resolution_percentage = old_resolution_percentage
            scene.render.image_settings.color_mode = old_color_mode
            
        preset = current_quicktitle()
        if not preset:
            return {'CANCELED'}
        import xml.etree.cElementTree as ET
        root = ET.Element("preset")
        ET.SubElement(root, 'name', name='Preset Name').text = preset.name
        ET.SubElement(root, 'description', name='Description').text = preset.description
        ET.SubElement(root, 'z_scale', name='Z Depth Scale').text = str(preset.z_scale)
        ET.SubElement(root, 'length', name='Scene Length').text = str(preset.length)
        ET.SubElement(root, 'shadowsize', name='Shadow Distance').text = str(preset.shadowsize)
        ET.SubElement(root, 'shadowamount', name='Shadow Amount').text = str(preset.shadowamount)
        ET.SubElement(root, 'shadowsoft', name='Shadow Softness').text = str(preset.shadowsoft)
        ET.SubElement(root, 'shadowx', name='Shadow Lamp X Position').text = str(preset.shadowx)
        ET.SubElement(root, 'shadowy', name='Shadow Lamp Y Position').text = str(preset.shadowy)
        ET.SubElement(root, 'qualityshadows', name='High Quality Shadows').text = str(preset.qualityshadows)
        for object in preset.objects:
            objects = ET.SubElement(root, 'objects')
            ET.SubElement(objects, 'name', name='Object Name').text = object.name
            ET.SubElement(objects, 'type', name='Object Type').text = object.type
            ET.SubElement(objects, 'x', name='Object X Location').text = str(object.x)
            ET.SubElement(objects, 'y', name='Object Y Location').text = str(object.y)
            ET.SubElement(objects, 'z', name='Object Z Location').text = str(object.z)
            ET.SubElement(objects, 'rot_x', name='Object X Rotation').text = str(object.rot_x)
            ET.SubElement(objects, 'rot_y', name='Object Y Rotation').text = str(object.rot_y)
            ET.SubElement(objects, 'rot_z', name='Object Z Rotation').text = str(object.rot_z)
            ET.SubElement(objects, 'scale', name='Overall Object Scale').text = str(object.scale)
            ET.SubElement(objects, 'width', name='Object Width Multiplier').text = str(object.width)
            ET.SubElement(objects, 'height', name='Object Height Multiplier').text = str(object.height)
            ET.SubElement(objects, 'shear', name='Shearing').text = str(object.shear)
            ET.SubElement(objects, 'cast_shadows', name='Cast Shadows On Other Objects').text = str(object.cast_shadows)
            ET.SubElement(objects, 'set_material', name='Set Material Manually').text = str(object.set_material)
            ET.SubElement(objects, 'material', name='Object Material Name').text = object.material
            ET.SubElement(objects, 'use_shadeless', name='Shadeless Material').text = str(object.use_shadeless)
            ET.SubElement(objects, 'use_transparency', name='Enable Transparency').text = str(object.use_transparency)
            ET.SubElement(objects, 'alpha', name='Object Opacity').text = str(object.alpha)
            diffuse_color = str(round(object.diffuse_color[0] * 255))+', '+str(round(object.diffuse_color[1] * 255))+', '+str(round(object.diffuse_color[2] * 255))
            ET.SubElement(objects, 'diffuse_color', name='Color Of The Material').text = diffuse_color
            ET.SubElement(objects, 'specular_intensity', name='Material Specularity').text = str(object.specular_intensity)
            ET.SubElement(objects, 'specular_hardness', name='Specular Hardness').text = str(object.specular_hardness)
            specular_color = str(round(object.specular_color[0] * 255))+', '+str(round(object.specular_color[1] * 255))+', '+str(round(object.specular_color[2] * 255))
            ET.SubElement(objects, 'specular_color', name='Color Of The Specularity').text = specular_color
            ET.SubElement(objects, 'extrude', name='Extrusion Amount').text = str(object.extrude)
            ET.SubElement(objects, 'bevel', name='Bevel Size').text = str(object.bevel)
            ET.SubElement(objects, 'bevel_resolution', name='Bevel Resolution').text = str(object.bevel_resolution)
            ET.SubElement(objects, 'text', name='Text').text = object.text
            ET.SubElement(objects, 'font', name='Font Name').text = object.font
            ET.SubElement(objects, 'word_wrap', name='Word Wrapping').text = str(object.word_wrap)
            ET.SubElement(objects, 'wrap_width', name='Word Wrap Width').text = str(object.wrap_width)
            ET.SubElement(objects, 'align', name='Text Alignment').text = object.align
            ET.SubElement(objects, 'texture', name='Path To The Image Texture').text = object.texture
            ET.SubElement(objects, 'alpha_texture', name='Path To The Transparent Texture').text = object.alpha_texture
            for animation in object.animations:
                animations = ET.SubElement(objects, 'animations')
                ET.SubElement(animations, 'variable', name='Animation Variable Name').text = animation.variable
                ET.SubElement(animations, 'animate_in', name='Animate Variable In').text = str(animation.animate_in)
                ET.SubElement(animations, 'animate_out', name='Animate Variable Out').text = str(animation.animate_out)
                ET.SubElement(animations, 'in_length', name='Length Of In Animation').text = str(animation.in_length)
                ET.SubElement(animations, 'out_length', name='Length Of Out Animation').text = str(animation.out_length)
                ET.SubElement(animations, 'in_offset', name='Frame Offset Of In Animation').text = str(animation.in_offset)
                ET.SubElement(animations, 'out_offset', name='Frame Offset Of Out Animation').text = str(animation.out_offset)
                ET.SubElement(animations, 'in_amount', name='Amount Of In Animation').text = str(animation.in_amount)
                ET.SubElement(animations, 'out_amount', name='Amount Of Out Animation').text = str(animation.out_amount)
        tree = ET.ElementTree(root)
        if not self.filepath.endswith('.xml'):
            self.filepath = self.filepath + '.xml'
        tree.write(self.filepath)
        self.report({'INFO'}, "Saved file to: "+self.filepath)
        return {'FINISHED'}

class QuickTitlingPresetImport(bpy.types.Operator, ImportHelper):
    #Operator to import a QuickTitler preset from a file
    bl_idname = 'quicktitler.preset_import'
    bl_label = 'Import Preset'
    bl_description = 'Imports a QuickTitling preset from a file'
    
    filename_ext = ".xml"
    filter_glob = bpy.props.StringProperty(default="*.xml", options={'HIDDEN'})
    filepath = bpy.props.StringProperty()
    
    def execute(self, context):
        #the file has been selected, attempt to parse it as a preset
        try:
            import xml.etree.cElementTree as ET
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            scene = context.scene
            preset = scene.quicktitles.add()
            preset.name = root.findtext('name', default=os.path.splitext(bpy.path.basename(self.filepath))[0])
            preset.description = root.findtext('description', default="")
            preset.z_scale = abs(float(root.findtext('z_scale', default="1")))
            preset.length = abs(int(root.findtext('length', default="300")))
            preset.shadowsize = abs(float(root.findtext('shadowsize', default="1")))
            shadowamount = abs(float(root.findtext('shadowamount', default="0.5")))
            if shadowamount > 1:
                preset.shadowamount = 1
            else:
                preset.shadowamount = shadowamount
            preset.shadowsoft = abs(float(root.findtext('shadowsoft', default="1")))
            preset.shadowx = float(root.findtext('shadowx', default="0"))
            preset.shadowy = float(root.findtext('shadowy', default="0"))
            preset.qualityshadows = to_bool(root.findtext('qualityshadows', default="False"))
            objects = root.findall('objects')
            for object in objects:
                newobject = preset.objects.add()
                newobject.name = object.findtext('name', default="")
                type = object.findtext('type', default="TEXT")
                if type in ['IMAGE', 'BOX', 'CIRCLE', 'TEXT']:
                    newobject.type = type
                else:
                    newobject.type = 'BOX'
                newobject.x = float(object.findtext('x', default="0"))
                newobject.y = float(object.findtext('y', default="0"))
                newobject.z = float(object.findtext('z', default="0"))
                newobject.rot_x = float(object.findtext('rot_x', default="0"))
                newobject.rot_y = float(object.findtext('rot_y', default="0"))
                newobject.rot_z = float(object.findtext('rot_z', default="0"))
                scale = abs(float(object.findtext('scale', default="1")))
                if scale > 0:
                    newobject.scale = scale
                else:
                    newobject.scale = 1
                width = abs(float(object.findtext('width', default="1")))
                if width > 0:
                    newobject.width = width
                else:
                    newobject.width = 1
                height = abs(float(object.findtext('height', default="1")))
                if height > 0:
                    newobject.height = height
                else:
                    newobject.height = 1
                shear = float(object.findtext('shear', default="0"))
                if shear < -1:
                    shear = -1
                if shear > 1:
                    shear = 1
                newobject.shear = shear
                newobject.cast_shadows = to_bool(object.findtext('cast_shadows', default="True"))
                newobject.set_material = to_bool(object.findtext('set_material', default="False"))
                newobject.material = object.findtext('material', default="No Preset")
                newobject.use_shadeless = to_bool(object.findtext('use_shadeless', default="False"))
                newobject.use_transparency = to_bool(object.findtext('use_transparency', default="False"))
                alpha = abs(float(object.findtext('alpha', default="1")))
                if alpha > 1:
                    newobject.alpha = 1
                else:
                    newobject.alpha = alpha
                specular_intensity = abs(float(object.findtext('specular_intensity', default="0.5")))
                if specular_intensity > 1:
                    newobject.specular_intensity = 1
                else:
                    newobject.specular_intensity = specular_intensity
                specular_hardness = abs(int(object.findtext('specular_hardness', default="50")))
                if specular_hardness > 511:
                    newobject.specular_hardness = 511
                elif specular_hardness < 1:
                    newobject.specular_hardness = 1
                else:
                    newobject.specular_hardness = specular_hardness
                newobject.extrude = abs(float(object.findtext('extrude', default="0")))
                newobject.bevel = abs(float(object.findtext('bevel', default="0")))
                newobject.bevel_resolution = abs(int(object.findtext('bevel_resolution', default="0")))
                newobject.text = object.findtext('text', default="None")
                newobject.font = object.findtext('font', default="Bfont")
                newobject.word_wrap = to_bool(object.findtext('word_wrap', default="True"))
                wrap_width = abs(float(object.findtext('wrap_width', default="1")))
                if wrap_width > 1:
                    newobject.wrap_width = 1
                elif wrap_width < 0.01:
                    newobject.wrap_width = 0.01
                else:
                    newobject.wrap_width = wrap_width
                align = object.findtext('align', default="CENTER")
                if align in ['LEFT', 'CENTER', 'RIGHT', 'JUSTIFY', 'FLUSH']:
                    newobject.align = align
                else:
                    newobject.align = 'CENTER'
                newobject.texture = object.findtext('texture', default="")
                newobject.alpha_texture = object.findtext('alpha_texture', default="")
                diffuse_color = object.findtext('diffuse_color', default="1, 1, 1").replace(' ', '').split(',')
                if len(diffuse_color) != 3:
                    newobject.diffuse_color = (1,1,1)
                else:
                    newobject.diffuse_color = (int(diffuse_color[0])/255.0, int(diffuse_color[1])/255.0, int(diffuse_color[2])/255.0)
                specular_color = object.findtext('specular_color', default="1, 1, 1").replace(' ', '').split(',')
                if len(specular_color) != 3:
                    newobject.specular_color = (1,1,1)
                else:
                    newobject.specular_color = (int(specular_color[0])/255.0, int(specular_color[1])/255.0, int(specular_color[2])/255.0)
                animations = object.findall('animations')
                for animation in animations:
                    newanimation = newobject.animations.add()
                    newanimation.variable = animation.findtext('variable', default="Alpha")
                    newanimation.animate_in = to_bool(animation.findtext('animate_in', default="True"))
                    newanimation.animate_out = to_bool(animation.findtext('animate_out', default="True"))
                    newanimation.in_length = abs(int(animation.findtext('in_length', default="15")))
                    newanimation.out_length = abs(int(animation.findtext('out_length', default="15")))
                    newanimation.in_offset = int(animation.findtext('in_offset', default="0"))
                    newanimation.out_offset = int(animation.findtext('out_offset', default="0"))
                    newanimation.in_amount = float(animation.findtext('in_amount', default="0"))
                    newanimation.out_amount = float(animation.findtext('out_amount', default="0"))
            return {'FINISHED'}
        except:
            print("Failed to import file, not a valid preset: "+self.filepath)
            self.report({'WARNING'}, "Failed to import file, not a valid preset: "+self.filepath)
            return {'CANCELLED'}

class QuickTitlingPresetManipulate(bpy.types.Operator):
    #Operator to manipulate QuickTitler presets - create, copy, delete.  Value: operation must be set to 'Delete', 'Copy', or 'Add'
    bl_idname = 'quicktitler.preset_manipulate'
    bl_label = 'Manipulate Presets'
    bl_description = 'Add, Copy Or Delete The First QuickTitling Preset'
    
    #What to do - should be set to 'Delete', 'Copy', 'Add'
    operation = bpy.props.StringProperty()
    
    def execute(self, context):
        scene = context.scene
        if self.operation == 'Delete':
            if len(scene.quicktitles) > 0:
                scene.quicktitles.remove(0)
        else:
            title = scene.quicktitles.add()
            if self.operation == 'Copy' and len(scene.quicktitles) > 1:
                #copy current title info to new title
                old_title = current_quicktitle()
                copy_title_preset(old_title, title)
                
            scene.quicktitles.move((len(scene.quicktitles) - 1),0)
            
        return {'FINISHED'}

class QuickTitlingPresetMenu(bpy.types.Menu):
    #Menu to list the QuickTitler Presets in the scene
    bl_idname = 'quicktitler.preset_menu'
    bl_label = 'List of saved presets'
    
    def draw(self, context):
        presets = context.scene.quicktitles
        layout = self.layout
        
        selected_title = titling_scene_selected()
        if selected_title:
            layout.operator('quicktitler.preset_select', text="Scene Preset: "+selected_title.scene.quicktitles[0].name)
        else:
            layout.label('Select A Preset:')
        
        split = layout.split()
        column = split.column()
        for index, preset in enumerate(presets):
            column.operator('quicktitler.preset_select', text=preset.name).preset = preset.name
        column = split.column()
        for index, preset in enumerate(presets):
            column.operator("quicktitler.preset_delete", text="", icon="X").index = index

class QuickTitlingPresetSelect(bpy.types.Operator):
    #Operator to select a QuickTitling preset so it can be displayed.  Preset name must be specified
    bl_idname = 'quicktitler.preset_select'
    bl_label = 'Set Preset'
    bl_description = 'Select A QuickTitling Preset'
    
    #Preset name
    preset = bpy.props.StringProperty()
    
    def execute(self,context):
        if not self.preset:
            return {'FINISHED'}
        scene = context.scene
        istitle = False
        
        #Iterate through titler presets to try and find the inputted one
        for index, preset in enumerate(scene.quicktitles):
            if preset.name == self.preset:
                title = index
                istitle = True
                break
        
        if istitle:
            #found title
            scene.quicktitles.move(title, 0)
            
            titling_sequence = titling_scene_selected()
            #if a title sequence is selected, copy new selected preset to that scene
            if titling_sequence:
                titling_scene = titling_sequence.scene
                if len(titling_scene.quicktitles) == 0:
                    titling_scene.quicktitles.add()
                copy_title_preset(scene.quicktitles[0], titling_scene.quicktitles[0])
        return {'FINISHED'}

class QuickTitlingLoadFont(bpy.types.Operator):
    #Operator to load a new font into Blender and select it
    bl_idname = 'quicktitler.load_font'
    bl_label = 'Load Font'
    bl_description = 'Load A New Font'
    
    #font file to be loaded
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self,context):
        #When the file browser finishes, this is called
        scene = context.scene
        fonts = bpy.data.fonts
        quicktitle = current_quicktitle()
        
        #Try to load font file
        try:
            font = bpy.data.fonts.load(self.filepath)
            current_object = get_current_object()
            if current_object:
                current_object.font = font.name
        except:
            print("Not a valid font file: "+self.filepath)
            self.report({'WARNING'}, "Not a valid font file: "+self.filepath)
            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        #Open a file browser
        context.window_manager.fileselect_add(self)
        
        return{'RUNNING_MODAL'}

class QuickTitlingFontMenu(bpy.types.Menu):
    #Menu for listing and changing QuickTitler fonts
    bl_idname = 'quicktitler.fonts_menu'
    bl_label = 'List of loaded fonts'
    
    def draw(self, context):
        fonts = bpy.data.fonts
        layout = self.layout
        
        #Ensure that the default font is always displayed
        if 'Bfont' not in fonts:
            layout.operator('quicktitler.change_font', text='Bfont').font = 'Bfont'
        
        for font in fonts:
            layout.operator('quicktitler.change_font', text=font.name).font = font.name

class QuickTitlingChangeFont(bpy.types.Operator):
    #Operator for changing the QuickTitler font on the current preset.  The font variable must be specified
    bl_idname = 'quicktitler.change_font'
    bl_label = 'Change Font'
    
    font = bpy.props.StringProperty()
    
    def execute(self, context):
        current_object = get_current_object()
        if current_object:
            current_object.font = self.font
        
        return {'FINISHED'}

class QuickTitlingMaterialMenu(bpy.types.Menu):
    #Menu to list all Materials in blend file, and assign them to QuickTitler objects
    bl_idname = 'quicktitler.materials_menu'
    bl_label = 'List of loaded materials'
    
    def draw(self, context):
        materials = bpy.data.materials
        layout = self.layout
        layout.operator('quicktitler.change_material', text='No Preset').material = 'No Preset'
        for material in materials:
            layout.operator('quicktitler.change_material', text=material.name).material = material.name

class QuickTitlingChangeMaterial(bpy.types.Operator):
    #Operator to assign a material name to the material of the current object.  The material variable must be set
    bl_idname = 'quicktitler.change_material'
    bl_label = 'Change material on the current object'
    
    material = bpy.props.StringProperty()
    
    def execute(self, context):
        current_object = get_current_object()
        if current_object:
            if self.material == 'No Preset':
                current_object.set_material = False
            current_object.material = self.material
        
        return {'FINISHED'}

class QuickTitlingCreate(bpy.types.Operator):
    #Operator to create QuickTitle scenes from the current quicktitle preset.  Can be used to just update titles as well.
    bl_idname = 'quicktitler.create'
    bl_label = 'Create QuickTitling Scene'
    bl_description = 'Creates or updates a titler scene'
    
    #Should be set to 'create', 'update' or 'update-all'
    action = bpy.props.StringProperty()
    
    def execute(self, context):
        quicktitle = current_quicktitle()
        if not quicktitle:
            print('No QuickTitle Preset Found')
            self.report({'WARNING'}, 'No QuickTitle Preset Found')
            return {'CANCELLED'}
        
        title_scene_length = quicktitle.length
        title_scene_name = "QuickTitle: "+quicktitle.name
        if (self.action == 'create'):
            quicktitle_create(quicktitle)
            
        sequence = bpy.context.scene.sequence_editor.active_strip
        
        if self.action == 'update_all':
            update_all = True
        else:
            update_all = False
        
        quicktitle_update(sequence, sequence.scene.quicktitles[0], update_all)

        return {'FINISHED'}

class QuickTitleSettings(bpy.types.PropertyGroup):
    autoupdate = bpy.props.BoolProperty(
        name = "Auto-Update Titles",
        default = True)

def register():
    #Register operators
    bpy.utils.register_module(__name__)

    #Group properties
    bpy.types.Scene.quicktitles = bpy.props.CollectionProperty(type=QuickTitle)
    bpy.types.Scene.quicktitler = bpy.props.PointerProperty(type=QuickTitleSettings)

def unregister():
    #Unregister operators
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
