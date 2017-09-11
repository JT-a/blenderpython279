bl_info = {
    "name": "Physical Camera 06-1 Modded for Blender 2.78c",
    "author": "bashi",
    "version": (0, 6),
    "blender": (2, 78, 0),
    "location": "Properties > Camera > Physical Camera",
    "description": "Physical Camera Effects Simulator, modded by DeepPurple72",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Scene"}
 
import bpy
from bpy.types import Panel
from math import *
 
from mathutils import Vector
from bpy_extras import view3d_utils
 
from bl_operators.presets import AddPresetBase
 
from bpy.app.handlers import persistent
 
#Update Call from Properties
@persistent
def update(self, context):
    scene=context.scene
    if bpy.context.scene.camera.data.pc_enable is True:
        #print(self.rna_type.identifier)
         
        if bpy.context.scene.camera.data.pc_use_focus_ext is True:
            focus_ext(scene)
        else:
            focus_null(scene)
        dof(scene)
        set_shift(scene)
        if bpy.context.scene.camera.data.pc_camera_type == 'movie':
            set_movie(scene)
         
        mb_shutter(scene)
        if bpy.context.scene.camera.data.pc_use_exposure is True:
            ex(scene)
        else:
            ex_null(scene)
        set_a(scene)
        if bpy.context.scene.camera.data.pc_use_blade_rot is True:
            sim_blades_rot(scene, 0.12)
        if bpy.context.scene.camera.data.pc_use_resolution is True:
            set_res(scene)
        wb_colman()
        #print(self.prop)
 
 
 
#Update call on Frame change
#dirty hack
@persistent
 
def update_all(scene):
    bpy.context.scene.camera.data.pc_aperture+=0
    bpy.context.scene.camera.data.pc_blades+=0
    bpy.context.scene.camera.data.pc_brot_offset+=0
    #bpy.context.scene.camera.data.pc_camera_type+=0
    bpy.context.scene.camera.data.pc_dof_distance+=0
    bpy.context.scene.camera.data.pc_enable+=0
    bpy.context.scene.camera.data.pc_iso+=0
    bpy.context.scene.camera.data.pc_lens+=0
    bpy.context.scene.camera.data.pc_manual_exposure+=0
    bpy.context.scene.camera.data.pc_nd_filter+=0
    bpy.context.scene.camera.data.pc_resolution_x+=0
    bpy.context.scene.camera.data.pc_shift_x+=0
    bpy.context.scene.camera.data.pc_shift_y+=0
    bpy.context.scene.camera.data.pc_shutter+=0
    bpy.context.scene.camera.data.pc_t_is_sec+=0
    bpy.context.scene.camera.data.pc_use_blade_rot+=0
    bpy.context.scene.camera.data.pc_use_dof+=0
    bpy.context.scene.camera.data.pc_use_exposure+=0
    bpy.context.scene.camera.data.pc_use_focus_empty+=0
    bpy.context.scene.camera.data.pc_use_focus_ext+=0
    bpy.context.scene.camera.data.pc_use_focus_ext_exposure+=0
    bpy.context.scene.camera.data.pc_use_nd_filter+=0
    bpy.context.scene.camera.data.pc_use_resolution+=0
    bpy.context.scene.camera.data.pc_wb_color=bpy.context.scene.camera.data.pc_wb_color
 
"""
def update_all(scene):
    if scene.camera.data.pc_enable is True:
        if bpy.context.scene.camera.data.pc_use_focus_ext is True:
            focus_ext()
        else:
            focus_null()
        dof()
        set_shift()
        if bpy.context.scene.camera.data.pc_camera_type == 'movie':
            set_movie()
         
        mb_shutter()
        if bpy.context.scene.camera.data.pc_use_exposure is True:
            ex()
        else:
            ex_null()
        set_a()
        if bpy.context.scene.camera.data.pc_use_blade_rot is True:
            sim_blades_rot(0.12)
        if bpy.context.scene.camera.data.pc_use_resolution is True:
            set_res()
"""
 
def init_variables():
    #Init Variables
    bpy.types.Camera.pc_enable = bpy.props.BoolProperty(
            default = True,
            description = "Physical Camera",
            update = update)
     
    #Try to find better place for UI Property!
    bpy.types.Camera.pc_show_lens_options = bpy.props.BoolProperty(
            default = False,
            description = "")
    bpy.types.Camera.pc_show_body_options = bpy.props.BoolProperty(
            default = False,
            description = "")
    bpy.types.Camera.pc_use_resolution = bpy.props.BoolProperty(
            default = False,
            description = "Set Image Dimensions to chosen Sensor Size.",
            update = update)
    bpy.types.Camera.pc_use_focus_empty = bpy.props.BoolProperty(
            default = False,
            description = "Use Empty as Focus object",
            update = update)
    bpy.types.Camera.pc_wb_color = bpy.props.FloatVectorProperty(
            default = (1.0, 1.0, 1.0),
            min = 0.0,
            max = 1.0,
            subtype='COLOR',
            description = "Color for White Balance",
            update = update)
 
    bpy.types.Camera.pc_use_focus_ext = bpy.props.BoolProperty(
            default = True,
            description = "Makes Focal Length longer on close range. Sometimes called Lens Breathing.",
            update = update)
 
    bpy.types.Camera.pc_use_focus_ext_exposure = bpy.props.BoolProperty(
            default = True,
            description = "Exposure decrease on Close-Up.",
            update = update)
 
    bpy.types.Camera.pc_use_dof = bpy.props.BoolProperty(
            default = True,
            description = "Depth of Field",
            update = update)
 
    bpy.types.Camera.pc_use_nd_filter = bpy.props.BoolProperty(
            default = False,
            description = "Neutral Density Filter.",
            update = update)
 
    bpy.types.Camera.pc_camera_type = bpy.props.EnumProperty(
            items = [('still','Still','Still Camera'),
            ('movie','Movie','Movie Camera')],
            name = "Camera Type", 
            description='Chose which Camera Type to use.', 
            default = ('still'),
            update = update)
 
    bpy.types.Camera.pc_resolution_x = bpy.props.IntProperty(
            default = 1920,
            min = 1,
            max = 128000,
            soft_min = 640,
            soft_max = 7680,
            description = "ISO of Sensor/Film",
            update = update)
     
    bpy.types.Camera.pc_lens = bpy.props.FloatProperty(
            default = 35,
            min = 7,
            max = 1200,
            soft_min = 1,
            soft_max = 100000,
            description = "Focal Length in mm.",
            update = update)
 
    bpy.types.Camera.pc_shift_x = bpy.props.FloatProperty(
            default = 0.0,
            min = -2.0,
            max = 2.0,
            soft_min = -0.5,
            soft_max = 0.5,
            description = "Lens Shift Horizontal",
            update = update)
 
    bpy.types.Camera.pc_shift_y = bpy.props.FloatProperty(
            default = 0.0,
            min = -2.0,
            max = 2.0,
            soft_min = -0.5,
            soft_max = 0.5,
            description = "Lens Shift Vertical",
            update = update)
 
 
    bpy.types.Camera.pc_nd_filter = bpy.props.FloatProperty(
            default = 0,
            min = -100,
            max = 128000,
            soft_min = -10,
            soft_max = 10,
            description = "Neutral Density Filter. For correcting too high Exposure.",
            update = update)
 
    bpy.types.Camera.pc_dof_distance = bpy.props.FloatProperty(
            default = 1,
            min = 0.001,
            max = 100,
            soft_min = 0.05,
            soft_max = 100000,
            description = "Focus Distance. DOF. Use F Key in 3d View for Click DOF!",
            update = update)
 
    bpy.types.Camera.pc_shutter = bpy.props.IntProperty(
            default = 200,
            min = 1,
            max = 16000,
            soft_min = 1,
            soft_max = 4000,
            description = "Shutter Speed of Physical Camera",
            update = update)
 
    bpy.types.Camera.pc_t_is_sec = bpy.props.BoolProperty(
            default = False,
            description = "Shutter in Seconds.",
            update = update)
 
    bpy.types.Camera.pc_iso = bpy.props.IntProperty(
            default = 200,
            min = 1,
            max = 64000,
            soft_min = 20,
            soft_max = 12800,
            description = "ISO of Sensor/Film",
            update = update)
 
    bpy.types.Camera.pc_aperture = bpy.props.FloatProperty(
            default = 16,
            min = 0.5,
            max = 256,
            soft_min = 1.2,
            soft_max = 32,
            description = "Aperture of Physical Camera",
            update = update)
 
    bpy.types.Camera.pc_blades = bpy.props.IntProperty(
            default = 5,
            min = 0,
            max = 22,
            soft_min = 0,
            soft_max = 22,
            description = "Number of Blades in Aperture",
            update = update)
 
    bpy.types.Camera.pc_use_blade_rot = bpy.props.BoolProperty(
            default = True,
            description = "Enable Aperture - Blades rotation coupling",
            update = update)
             
    bpy.types.Camera.pc_brot_offset = bpy.props.FloatProperty(
            default = 0,
            min = -180,
            max = 180,
            subtype = 'ANGLE',
            description = "Blades rotation offset",
            update = update)
             
    bpy.types.Camera.pc_use_exposure = bpy.props.BoolProperty(
            default = True,
            description = "Disable Exposure coupling",
            update = update)
             
    bpy.types.Camera.pc_manual_exposure = bpy.props.FloatProperty(
            default = 1,
            min = 0,
            max = 10,
            soft_min = 0.0125,
            soft_max = 10,
            description = "Manual Exposure",
            update = update)
 
init_variables()
 
#Init Presets
class CAMERA_PC_movie_formats_add(AddPresetBase, bpy.types.Operator):
    """Add a new Movie Format preset."""
    bl_idname = 'camera.pc_movie_formats'
    bl_label = 'Add Movie Format Preset'
    bl_options = {'REGISTER', 'UNDO'}
    preset_menu = 'CAMERA_PC_movie_formats'
    preset_subdir = 'pc_movie_formats'
 
    preset_defines = [
        "c = bpy.context.scene.camera.data",
        ]
 
    preset_values = [
        "c.sensor_width",
        "c.sensor_height",
        ]
         
class CAMERA_PC_movie_formats(bpy.types.Menu):
    '''Presets for Movie Formats.'''
    bl_label = "Movie Formats"
    bl_idname = "CAMERA_PC_movie_formats"
    preset_subdir = "pc_movie_formats"
    preset_operator = "script.execute_preset"
 
    draw = bpy.types.Menu.draw_preset
 
class CAMERA_PC_still_formats_add(AddPresetBase, bpy.types.Operator):
    """Add a new Still Format preset."""
    bl_idname = 'camera.pc_still_formats'
    bl_label = 'Add Still Format Preset'
    bl_options = {'REGISTER', 'UNDO'}
    preset_menu = 'CAMERA_PC_still_formats'
    preset_subdir = 'pc_still_formats'
 
    preset_defines = [
        "c = bpy.context.scene.camera.data",
        ]
 
    preset_values = [
        "c.sensor_width",
        "c.sensor_height",
        ]
         
class CAMERA_PC_still_formats(bpy.types.Menu):
    '''Presets for Still Formats.'''
    bl_label = "Still Formats"
    bl_idname = "CAMERA_PC_still_formats"
    preset_subdir = "pc_still_formats"
    preset_operator = "script.execute_preset"
 
    draw = bpy.types.Menu.draw_preset
 
#Properties - Camera - UI
class Physical_Camera(bpy.types.Panel):
    bl_label = "Physical Camera"
    bl_idname = "OBJECT_PC"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
         
    def draw(self, context):
        gui(self)
         
#Modal Menu - Work in Progress
"""
class PC_Menu(bpy.types.Menu):
    bl_label = "Physical Camera Menu"
    bl_idname = "OBJECT_PC_menu"
 
    def draw(self, context):
        gui(self)
         
def draw_item(self, context):
    layout = self.layout
    layout.menu(PC_Menu.bl_idname)
"""
#bpy.ops.wm.call_menu(name=PC_Menu.bl_idname)
#/Menu
 
#Compositor
 
class PhysicalCameraComp(bpy.types.Panel):
    bl_label = "Physical Camera"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    #bl_context = "material"
  
    def draw(self, context):
        scene=context.scene
        node_tree=scene.node_tree
        nodes=node_tree.nodes
        active_node=nodes.active
        #outputs = active_node.outputs
         
        #if len(outputs) is not 0:
        #if node_tree.type:
        self.layout.operator("pc.node_defocus", text='Defocus')
        self.layout.operator("pc.node_mblur", text='Motion Blur')       
         
         
class OBJECT_OT_PC_CompAddDefocus(bpy.types.Operator):
    bl_idname = "pc.node_defocus"
    bl_label = "Create Defocus Node with Physical Camera Values"
  
    def execute(self, context):
        scene=context.scene
        node_tree=scene.node_tree
        nodes=node_tree.nodes
         
        if nodes.active and 'R_LAYERS' in nodes.active.type:
            active_node=nodes.active
            outputs = active_node.outputs
            location = active_node.location
 
        c = scene.camera.data
                
        #Add File Output Node 
        bpy.ops.node.add_node(use_transform=True, type="CompositorNodeDefocus")
        d=node_tree.nodes.active
        d.label='PC Defocus'
        d.name='PC Defocus'
         
        #Setup File Output Node
        #d.f_stop=c.pc_aperture
        d.use_zbuffer=True
        d.use_gamma_correction=True
        d.bokeh=comp_bokeh_num_to_str()
        #d.angle=blade_angle(0.12)
         
        #if nodes.active and 'R_LAYERS' in nodes.active.type:
            #Set  Location
        #    d.location[0]=location[0]+300
        #    d.location[1]=location[1]+180
               
        return{'FINISHED'}    
 
class OBJECT_OT_PC_CompAddMBlur(bpy.types.Operator):
    bl_idname = "pc.node_mblur"
    bl_label = "Create Vector Motion Blur Node with Physical Camera Values"
  
    def execute(self, context):
        scene=context.scene
        node_tree=scene.node_tree
        nodes=node_tree.nodes
 
 
        c = scene.camera.data
                
        #Add File Output Node 
        bpy.ops.node.add_node(use_transform=True, type="CompositorNodeVecBlur")
        d=node_tree.nodes.active
        d.label='PC Motion Blur'
        d.name='PC Motion Blur'
         
         
         
        #Setup File Output Node
        d.factor=1 #!!!!
        d.use_curved=True
        #d.use_gamma_correction=True
         
        #Set New File Output Location
        #output.location[0]=location[0]+300
        #output.location[1]=location[1]+180
         
        return{'FINISHED'} 
         
def comp_bokeh_num_to_str():
    scene=bpy.context.scene
    c = scene.camera.data
     
    b=c.pc_blades
     
    if b < 2:
        return 'CIRCLE'       
    elif b == 3:
        return 'TRIANGLE'
    elif b == 4:
        return 'SQUARE'
    elif b == 5:
        return 'PENTAGON'
    elif b == 6:
        return 'HEXAGON'
    elif b == 7:
        return 'HEPTAGON'
    elif b == 8:
        return 'OCTAGON'
    elif b >= 9:
        return 'CIRCLE'
#print(comp_bokeh_num_to_str())    
 
#/COmpositor
 
def gui(self):
    context=bpy.context
    scene=context.scene   
    cycles=scene.cycles
     
    layout = self.layout
    object=context.object
     
    c=context.scene.camera.data
     
    render=scene.render
             
    if object.type in {'CAMERA'}:
        c = context.object.data
        r = layout.row()
        r.prop(c, "pc_enable", text='Enable Physical Camera')
         
        if c.pc_enable is True:            
            #camera=c
            cycles=scene.cycles
 
            focal=c.lens
            
             
            r = layout.row()
            r.label(text='Filter')
             
            b = layout.box()
             
             
            r = b.row()
            r.active = c.pc_use_exposure
            r.prop(c, "pc_use_nd_filter", text='ND-Filter')
            if c.pc_use_nd_filter is True:
                nd=r.prop(c, "pc_nd_filter", text='ND f/stop')
         
            #Lens
             
            r = layout.row()
            r.label(text='Lens'+str('{:10.1f}'.format(c.lens))+'mm')
             
            #lens type
            engine = context.scene.render.engine
            if engine == 'CYCLES':  # or 'LUXRENDER_RENDER'
                r.prop(c, "type", text="")
             
            if engine == 'YAFA_RENDER':
                r.prop(c, "camera_type", text="")
             
            if c.type == 'PANO':
                 
                if engine == 'CYCLES':
                  
                    r = layout.row()
                    r.prop(c.cycles, "panorama_type", text="")
             
            #r= layout.row()
            b = layout.box()
            r = b.row()
             
            if c.type == 'PERSP':
                r.prop(c, "pc_lens", text='Focal Length')
             
            if c.type == 'PANO':
                engine = context.scene.render.engine
                if engine == 'CYCLES':
                    ccam = c.cycles
                    if ccam.panorama_type == 'FISHEYE_EQUIDISTANT':
                        r.prop(c.cycles, "fisheye_fov", text="Field of View")
                    elif ccam.panorama_type == 'FISHEYE_EQUISOLID':
                        #r = layout.row()
                        r.prop(c, "pc_lens", text='Focal Length')
                        r = b.row()
                        r.prop(ccam, "fisheye_fov")
            
            if 'PANO' not in c.type:
                r = b.row()
                #r.label(text='Shift')
                r.prop(c, "pc_shift_y", text='Vertical')
                r.prop(c, "pc_shift_x", text='Horizontal')
             
            r = b.row()
            r.prop(c, "pc_use_dof", text='DOF')
            r.prop(c, "pc_show_lens_options", text='Options')
             
            if c.pc_show_lens_options == True:
                r = b.row()
                r.active = c.pc_use_exposure
                r.prop(c, "pc_use_focus_ext_exposure", text='Focus Distance affect Exposure')
                 
                r = b.row()
                r.prop(c, "pc_use_focus_ext", text='Focus Distance affect Focal Length')
                 
                r = b.row()
                r.prop(c, "pc_use_blade_rot", text='Aperture affect Blades rotation')
             
            #if c.pc_use_dof == True:
            r = b.row()
            if c.pc_show_lens_options == True:
                r.prop(c, "dof_object", text="")
            r.prop(c, "pc_dof_distance", text='Focus Distance in m')
            #r.prop(c, "pc_use_focus_ext", text='')
            #r.prop(c, "pc_use_focus_ext_exposure", text='')
             
            r = b.row()
            r.prop(c, "pc_aperture", text='Aperture in f/stop')
            #r.prop(c, "pc_use_blade_rot", text='')            
             
            if engine == 'CYCLES' or 'VRAY_RENDER':
                if c.pc_show_lens_options == True:
                    r = b.row()
                    r.prop(c, "pc_blades", text='Blades')
                    r.prop(c, "pc_brot_offset", text='')
             
            if engine == 'YAFA_RENDER':
                if c.pc_show_lens_options == True:
                    r = b.row()
                    r.prop(c, "bokeh_type", text='')
                    r.prop(c, "bokeh_bias", text='')
                    r.prop(c, "pc_brot_offset", text='')
            #Back
            r = layout.row()
            r.label(text='Camera Body')
            r.prop(c, "pc_camera_type", text="")
            #r = layout.row()
            b = layout.box()
            r = b.row()
             
            if c.pc_camera_type == 'still':
                r.prop(c, "pc_t_is_sec", text='')
            if c.pc_t_is_sec is False:
                r.prop(c, "pc_shutter", text='Shutter 1/')
            else:
                r.prop(c, "pc_shutter", text='Shutter in S')
             
            r = b.row()
            r.active = c.pc_use_exposure
            r.prop(c, "pc_iso", text='ISO')
 
            r = b.row()
            r.prop(render, "use_motion_blur", text='Motion Blur')
             
            if engine == 'LUXRENDER_RENDER':
                r.prop(c.luxrender_camera, "motion_blur_samples")
                r = b.row()
             
            if engine == 'VRAY_RENDER':
                r.prop(c.vray.CameraPhysical, "subdivs")
                r = b.row()
             
            r.prop(c, "pc_use_exposure", text='Exposure')
             
            if c.pc_use_exposure is False:
                r = b.row()
                r.prop(c, "pc_manual_exposure", text='Manual Exposure')
            else:
                r = b.row()
                r.label(text='Exposure: '+str('{:10.2f}'.format(cycles.film_exposure)))
                #r.label(text='EV: '+str('{:10.2f}'.format(get_ev()+19)))
            #Vray - Not Working
            #else:
            #    bpy.context.object.data.vray.CameraPhysical.exposure=1
             
             
             
             
            r = b.row()
            r.prop(c, "pc_show_body_options", text='Options')
             
             
            if c.pc_show_body_options:            
                r = b.row()
                r.prop(scene.view_settings, 'use_curve_mapping', text='')
                r.prop(c, 'pc_wb_color', text='WB')
                r = b.row()
                r.prop(scene.view_settings, 'gamma', text='gamma')
                r.prop(scene.view_settings, 'look', text='Film')
                #col = r.column()
                #col.template_colormanaged_view_settings(scene, "view_settings")
                 
                if c.pc_camera_type == 'movie': 
                    #Movie Format Presets
                    #layout = self.layout
                    col = b.column_flow(align=True)
                    col.label('Movie Formats:')
                    row = col.row(align=True)
                    row.menu("CAMERA_PC_movie_formats",
                             text=bpy.types.CAMERA_PC_movie_formats.bl_label)
                    row.operator("camera.pc_movie_formats", text="", icon='ZOOMIN')
                    row.operator("camera.pc_movie_formats", text="", icon='ZOOMOUT').remove_active = True
                    #/Presets
                elif c.pc_camera_type == 'still': 
                    #Still Format Presets
                    #layout = self.layout
                    col = b.column_flow(align=True)
                    col.label('Still Formats:')
                    row = col.row(align=True)
                    row.menu("CAMERA_PC_still_formats",
                             text=bpy.types.CAMERA_PC_still_formats.bl_label)
                    row.operator("camera.pc_still_formats", text="", icon='ZOOMIN')
                    row.operator("camera.pc_still_formats", text="", icon='ZOOMOUT').remove_active = True
                    #/Presets
                     
                r = b.row()
                r.prop(c, "sensor_height", text='Sensor height in mm')
                r.prop(c, "sensor_width", text='Sensor width in mm')
                 
                r = b.row()
                r.prop(c, "pc_use_resolution", text='Resolution')
                if c.pc_use_resolution == True:
                    r.prop(c, "pc_resolution_x", text='Resolution horizontal in px')
                 
                 
                #from properties_render import RENDER_PT_dimensions
                rd = context.scene.render
                #args = rd.fps, rd.fps_base, RENDER_PT_dimensions._preset_class.bl_label
                #fps_label_text, show_framerate = RENDER_PT_dimensions._draw_framerate_label(*args)
                 
                custom_framerate = (rd.fps not in {23.98, 24, 25, 29.97, 30, 50, 59.94, 60})
                if custom_framerate is True:
                    show_framerate = True
                else:
                    show_framerate = True
                r = b.row()
                fps=scene.render.fps
                r.menu("RENDER_MT_framerate_presets", text=str(fps)+' fps')
 
                if show_framerate:
                    r.prop(rd, "fps")
                    #r.prop(rd, "fps_base", text="/")
            """
            #Infos
            r = layout.row()
            r.label(text='Informations')
             
            b = layout.box()
             
            r = b.row()
            #ev=get_ev()
            #r.label(text='EV: '+str('{:10.2f}'.format(get_ev()+19)))
            #r = b.row()
            #r.label(text='Exposure: '+str('{:10.2f}'.format(cycles.film_exposure)))
             
            if cycles.film_exposure == 0:
                r.label(text='Exposure too low')
             
            if c.pc_use_focus_ext is True:
                r = b.row()
                r.label(text='Real Focal Length:'+str('{:10.1f}'.format(c.lens)))
             
            r = b.row()
            r.label(text='Hyperfocal:'+str('{:10.2f}'.format(hyperfocal())))
             
            r = b.row()
            r.label(text='Near Point:'+str('{:10.2f}'.format(get_points('near'))))
             
            r = b.row()
            r.label(text='Rear Point:'+str('{:10.2f}'.format(get_points('rear'))))
             
            r = b.row()
            r.label(text='Circe of Confusion:'+str('{:10.2f}'.format(coc())))
            """       
 
def set_res(scene):
    #context=bpy.context
    #scene=context.scene
    c=scene.camera.data
    render=scene.render
     
    neg_x = c.sensor_width
    neg_y = c.sensor_height
     
     
    res = c.pc_resolution_x
     
    render.resolution_x = res
     
    render.resolution_y = res/neg_x*neg_y
 
     
def set_shift(scene):
    #context=bpy.context
    c=scene.camera.data
     
    if c.type == 'PANO':
        c.shift_x = 0.0
        c.shift_y = 0.0
    else:
        c.shift_x = c.pc_shift_x
        c.shift_y = c.pc_shift_y
 
         
def t_sec(scene, t):
    #context=bpy.context
    c=scene.camera.data
     
    if c.pc_t_is_sec is True:
        t=1*t
    else:
        t=1/t
    #print(t)
    return t
 
def dof_object_distance(scene):
    dof_object = scene.camera.data.dof_object
    dloc = dof_object.location
 
    empty = scene.camera
    cloc = empty.matrix_world.to_translation()
 
    distance = sqrt(
    pow( dloc.x - cloc.x, 2 ) +
    pow( dloc.y - cloc.y, 2 ) +
    pow( dloc.z - cloc.z, 2 ) )
 
    return distance 
#print (dof_object_distance())
 
 
#Work in Progress
#def focus_empty():
#    context=bpy.context
#    c=context.scene.camera.data
#    if c.pc_use_focus_empty == True:
#        c.pc_dof_distance = empty_distance()
 
def focus_ext(scene):
    #context=bpy.context
    c=scene.camera.data
    neg_x = c.sensor_width
    neg_y = c.sensor_height
    lens=c.pc_lens
     
    #Angle of View - Work in Progress
    #f = B / (2 × tan(α / 2))
    #Focal length = Image size / (2 × tan(Angle of view / 2))
    negd=neg_diag(scene)
    lens1 = negd / (2 * tan(45 / 2)) #Working - Add Horizontal/Vertical
    #print('Angle2Focal'+str(lens1))
     
    abb = lens / (c.pc_dof_distance*100)
     
    if c.pc_use_focus_ext is True:
        fe=lens * (1+(abb/100))
     
     
        # 
        vf=(fe*2)/(lens*2)
     
    else:
        fe=lens
        vf=1.0
     
    #print(vf)
    #return vf
    #/
     
    c.lens=fe
     
    if c.cycles.fisheye_lens:
        c.cycles.fisheye_lens=fe
     
    return fe, vf
 
     
def focus_null(scene):
    #context=bpy.context
    c=scene.camera.data
        
    c.lens=c.pc_lens
    c.cycles.fisheye_lens=c.pc_lens
     
    #Need here vf too???!!!!
     
 
def dof(scene):
    #context=bpy.context
    c=scene.camera.data
     
    if c.dof_object:
        #print('dof_object')
        c.pc_dof_distance=dof_object_distance()
    else:
        c.dof_distance=c.pc_dof_distance
 
 
def set_movie(scene):
    #context=bpy.context
    c=scene.camera.data
    if c.pc_camera_type == 'movie' and c.pc_t_is_sec == True:
        c.pc_t_is_sec = False
     
def mb_shutter(scene):
    #context=bpy.context
    render=scene.render
    fps=render.fps
    c=scene.camera.data
    shutter=c.pc_shutter
 
  
    #Limit for Movie - Find better Solution!
    if c.pc_camera_type == 'movie':
        #print('is movie camera')
        if shutter <= fps:
            c.pc_shutter = fps
            #print(shutter)
             
    #if is_second is False:
    m_shutter=fps*t_sec(scene, shutter)
    #else:
     
    render.motion_blur_shutter=m_shutter
     
    #Compositor Test
    if scene.node_tree:
        if 'PC Motion Blur' in scene.node_tree.nodes:
            mb=scene.node_tree.nodes['PC Motion Blur']
            mb.factor=m_shutter
 
    #VRay - NOT WORKING!!!
    if hasattr(c, 'vray'):
        v=c.vray
        vc=c.vray.CameraPhysical
    #if v:
        #print('yay')
        vc.shutter_speed=shutter
        vc.use_moblur = render.use_motion_blur
             
     
    #Luxrender - Not Working - if Luxrender not enabled!
    #l=c.luxrender_camera
    if hasattr(c, 'luxrender_camera'):
        l=c.luxrender_camera
        l.usemblur=render.use_motion_blur
         
        #Set Shutter
        l.exposure_mode = 'degrees'
        deg=360/shutter*fps
        l.exposure_degrees_end = radians(deg)
        #print(deg)
     
    return m_shutter
     
def get_ev(scene):    
    #context=bpy.context
    c=scene.camera.data
    a=c.pc_aperture
    t=c.pc_shutter
    iso=c.pc_iso
    is_sec=c.pc_t_is_sec
     
    if c.pc_t_is_sec is True:
        ev=2*log2(a)*-1 - log2(t)*-1 + log2(iso/100)
    else:
        ev=2*log2(a)*-1 - log2(t) + log2(iso/100)
 
    ev+=15.64
    #ev-=3
    ev-=7.5
     
    #Apply ND-Filter
    if c.pc_use_nd_filter == True:
        ev-=c.pc_nd_filter
     
    return ev
     
def ex(scene):
    #context=bpy.context
    c=scene.camera.data
    a=c.pc_aperture
    t=c.pc_shutter
    iso=c.pc_iso
    is_sec=c.pc_t_is_sec
 
    ev=get_ev(scene)
     
    #Focus Extension
    null,vf=focus_ext(scene)
    if c.pc_use_focus_ext_exposure is True:   
        ev/=vf
     
 
     
    # Map [1 to -x][0 - 1] 
    if ev < 1:
        ev=ev
        ev*0-1
        ex=pow(2, ev-1)
    else:
        ex=ev
     
    scene.cycles.film_exposure=ex
    #Mitsuba
    #if c.mitsuba_film:
    #    c.mitsuba_film.exposure=ev    
 
    return ex
 
 
def ev_to_ex(ev):
    if ev < 1:
        ev=ev+1
        ev*0-1
        ex=pow(2, ev-1)
     
    else:
        ex=ev
     
    return ex
 
 
def ex_null(scene):
    #context=bpy.context
    c=scene.camera.data
    scene.cycles.film_exposure=c.pc_manual_exposure
 
    #Mitsuba - Not Working
    #if hasattr(c, 'mitsuba_camera'):
    #    ma=c.mitsuba_camera
    #    ma.mitsuba_film.exposure=c.pc_manual_exposure
 
 
 
def wb_colman():
    #Generate Base to target Multipliers for Color Management View
     
    if bpy.context.scene.view_settings.curve_mapping:
        w_level=bpy.context.scene.view_settings.curve_mapping.white_level
         
        col1=bpy.context.scene.camera.data.pc_wb_color
        col2=(1.0, 1.0, 1.0)
         
        #find lowest
        col1_h=[1.0, 0]
        for id, c1 in enumerate(col1):
            if c1<col1_h[0]:
                col1_h[1]=id
                col1_h[0]=c1
         
        mul=col1_h[0]
         
        r_mul=col2[0]/mul*col1[0]
        g_mul=col2[1]/mul*col1[1]
        b_mul=col2[2]/mul*col1[2]
         
        #Apply Values - Put this somewhere else?
        w_level[0]=r_mul
        w_level[1]=g_mul
        w_level[2]=b_mul
 
def blade_angle(mul):
    context=bpy.context
    scene=context.scene
    c=scene.camera.data
    ap=c.pc_aperture
    of=c.pc_brot_offset
    return ap*mul+of
     
 
def sim_blades_rot(scene, mul):
    context=bpy.context
    scene=context.scene
    c=scene.camera.data
     
    b_ang=blade_angle(mul)
 
    c.cycles.aperture_rotation=b_ang
     
    #Compositor
    if scene.node_tree:
        if 'PC Defocus' in scene.node_tree.nodes:
            de=scene.node_tree.nodes['PC Defocus']
            de.angle=b_ang*0.4
     
    #Yafaray
    if 'bokeh_rotation' in c:
        c.bokeh_rotation=b_ang
 
    if hasattr(c, 'vray'):
    #if c.vray:
        vc=c.vray.CameraPhysical
        vc.blades_rotation=degrees(b_ang)
 
def set_a(scene):
    #context=bpy.context
    c=scene.camera.data
    a=c.pc_aperture
    focal=c.lens
     
    if 'RADIUS' not in c.cycles.aperture_type:
        c.cycles.aperture_type='RADIUS'
     
    if c.pc_use_dof == True:
        a_sr=(focal/a)/2000
         
    else:
        a_sr=0
     
    c.cycles.aperture_size=a_sr
     
    #Compositor
    if scene.node_tree:
        if 'PC Defocus' in scene.node_tree.nodes:
            de=scene.node_tree.nodes['PC Defocus']
            de.f_stop=a
            de.bokeh=comp_bokeh_num_to_str()
             
            if de.use_zbuffer == False:
                de.use_zbuffer == True
     
    #Yafaray
    if 'aperture' in c:
    #   print('yehe')
        c.aperture=a_sr
     
    #VRay
    if hasattr(c, 'vray'):
       v=c.vray
       vc=v.CameraPhysical
       vc.f_number=a
       vc.ISO = c.pc_iso
        
       if c.pc_blades > 0:
           vc.blades_enable = True
           vc.blades_num=c.pc_blades
       elif c.pc_blades == 0:
           vc.blades_enable = False
            
       if c.pc_use_dof == True:
           vc.use_dof = True
    #Mitsuba
    if hasattr(c, 'mitsuba_camera'):
        ma=c.mitsuba_camera
         
        ma.apertureRadius=a_sr
        ma.useDOF=c.pc_use_dof
     
    #Luxrender
    #l=c.luxrender_camera
    if hasattr(c, 'luxrender_camera'):
        l=c.luxrender_camera
        l.use_dof=c.pc_use_dof
        l.autofocus = False
        l.fstop=c.pc_aperture
        l.blades=c.pc_blades
         
        l.sensitivity=c.pc_iso
      
    #Blades
    c.cycles.aperture_blades=c.pc_blades
      
 
 
def neg_diag(scene):
    #context=bpy.context
    c=scene.camera.data
    neg_x = c.sensor_width
    neg_y = c.sensor_height
   
    neg_diag = sqrt((neg_x*neg_x)+(neg_y*neg_y))
 
    return neg_diag
 
def res_diag(scene):
    #context=bpy.context
    r=scene.render
    neg_x = r.resolution_x
    neg_y = r.resolution_y
   
    neg_diag = sqrt((neg_x*neg_x)+(neg_y*neg_y))
 
    return neg_diag    
 
def get_lens_type(scene):
    #context=bpy.context
    c=scene.camera.data
    lens=c.pc_lens
     
    n_diag=neg_diag()
     
    if lens <= n_diag*0.7:#Lookup exact definitions of Wide/Tele!
        print('wide')
    elif lens >= n_diag*1.5:
        print('tele')
    else:
        print('normal')
         
#get_lens_type()
 
def coc():
    c = neg_diag()/1500
    #c = res_diag()/40000
    #print('coc: '+str(c))
    #c=0.03
    return c
 
def hyperfocal(scene):
    #context=bpy.context
    c=scene.camera.data
 
    hyperfocal = ((( c.pc_lens * c.pc_lens ) / ( c.pc_aperture * coc())) + c.pc_lens ) / 10
 
    return hyperfocal/100
 
#Work in Progress 
#Focal Length must be somehow involved
def auto_shift(scene):
    c=scene.camera
    rot=degrees(c.rotation_euler[0])
    c.rotation_euler[0]=1.5707969665527344
    diff=90-rot
    if diff < 0:
        diff*=-1
     
    c.data.shift_y=diff/50
 
    #auto_shift()    
 
def get_points(scene, switch):
    #context=bpy.context
    c=scene.camera.data
     
    h=hyperfocal()
    dof=c.pc_dof_distance
    f=c.pc_lens/100
     
    #print('hyperfocal :'+str(h))
    #print('dof :'+str(dof))
    #print('f :'+str(f))
     
     
    if 'near' in switch:
        #Near Point Info
            #(focus distance*hyperfocaldistance)/(hyperfocaldistance+(focus distance-focal length))
        point = ((dof) * h) / ( h + ( (dof) - f*1 ))   
    elif 'rear' in switch:
        #Rear Point Info
            #(Focus Distance*Hyperfocaldistance)/(Hyperfocaldistance-(Focus Distance-focal length))
        point = ((dof) * h) / ( h - ( (dof) - f*1 )) 
    return point
 
#print('near'+str(get_points('near')))    
#print('rear'+str(get_points('rear')))    
 
# Copied from Templates - Get Mouse Distance
def main(context, event, ray_max=10000.0):
    """Run this function on left mouse, execute the ray cast"""
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y
 
    c=context.scene.camera.data
 
    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    ray_target = ray_origin + (view_vector * ray_max)
 
 
    def visible_objects_and_duplis():
        """Loop over (object, matrix) pairs (mesh only)"""
 
        for obj in context.visible_objects:
            if obj.type == 'MESH':
                yield (obj, obj.matrix_world.copy())
 
            if obj.dupli_type != 'NONE':
                obj.dupli_list_create(scene)
                for dob in obj.dupli_list:
                    obj_dupli = dob.object
                    if obj_dupli.type == 'MESH':
                        yield (obj_dupli, dob.matrix.copy())
 
            obj.dupli_list_clear()
 
    def obj_ray_cast(obj, matrix):
        """Wrapper for ray casting that moves the ray into object space"""
 
        # get the ray relative to the object
        matrix_inv = matrix.inverted()
        ray_origin_obj = matrix_inv * ray_origin
        ray_target_obj = matrix_inv * ray_target

        ray_origin_obj = (ray_origin_obj[0],ray_origin_obj[1],ray_origin_obj[2])
        ray_target_obj = (ray_target_obj[0],ray_target_obj[1],ray_target_obj[2])

        print ( "ray_origin = " + str(ray_origin_obj) )
        print ( "ray_target = " + str(ray_target_obj) )
 
        # cast the ray
        tmp = (obj.ray_cast(ray_origin_obj, ray_target_obj)[0],obj.ray_cast(ray_origin_obj, ray_target_obj)[1],obj.ray_cast(ray_origin_obj, ray_target_obj)[2])
        hit, normal, face_index = (tmp)
 
        if face_index != -1:
            return hit, normal, face_index
        else:
            return None, None, None
 
    # cast rays and find the closest object
    best_length_squared = ray_max * ray_max
    best_obj = None
 
    for obj, matrix in visible_objects_and_duplis():
        if obj.type == 'MESH':
            tmp = (obj_ray_cast(obj, matrix)[0],obj_ray_cast(obj, matrix)[1],obj_ray_cast(obj, matrix)[2])
            hit, normal, face_index = tmp
            if hit is not None:
                hit_world = matrix * hit
                #scene.cursor_location = hit_world
                length_squared = (hit_world[0].xyz - ray_origin).length_squared
                if length_squared < best_length_squared:
                    best_length_squared = length_squared
                    best_obj = obj
 
    # now we have the object under the mouse cursor,
    # we could do lots of stuff but for the example just select.
    if best_obj is not None:
        #best_obj.select = True
        #context.scene.objects.active = best_obj
         
        c.pc_dof_distance = sqrt(best_length_squared) 
 
class ClickDOF(bpy.types.Operator):
    """Modal Click DOF for Physical Camera"""
    bl_idname = "view3d.modal_pc_click_dof"
    bl_label = "Physical Camera Click DOF"
 
    def modal(self, context, event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            # allow navigation
            return {'PASS_THROUGH'}
        elif event.type == 'MOUSEMOVE':
            main(context, event)
            return {'RUNNING_MODAL'}
        elif event.type in {'LEFTMOUSE', 'ESC', 'SPACE'}:
            return {'CANCELLED'}
 
        return {'RUNNING_MODAL'}
 
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}
#/ End Copied from Templates - Get Mouse Distance
         
classes = [
    Physical_Camera,
    #PC_Menu,
    ]
 
def register():
    for c in classes:
        bpy.utils.register_class(c)
     
    #bpy.app.handlers.scene_update_post.append(update_all)
    #bpy.app.handlers.render_post.append(update_all)
    bpy.app.handlers.frame_change_pre.append(update_all)
    #bpy.app.handlers.scene_update_pre.append(update_all)
     
    #Key for Click DOF - (Add on Enable Camera??)
    keyMap = bpy.context.window_manager.keyconfigs.user.keymaps['3D View']
    keyMapItem = keyMap.keymap_items.new('view3d.modal_pc_click_dof', 'F', 'PRESS')
    #keyMapItem.properties.name = "VIEW3D_Physical_Camera_click_DOF"
     
    #Key for Focus
    #keyMap2 = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
    #keyMapItem = keyMap2.keymap_items.new('object.data.pc_lens', 'F', 'PRESS')
     
    #bpy.types.INFO_HT_header.append(draw_item)
    bpy.utils.register_class(ClickDOF)
     
    bpy.utils.register_class(CAMERA_PC_movie_formats_add)
    bpy.utils.register_class(CAMERA_PC_movie_formats)
     
    bpy.utils.register_class(CAMERA_PC_still_formats_add)
    bpy.utils.register_class(CAMERA_PC_still_formats)
     
    #Compositor
    bpy.utils.register_class(PhysicalCameraComp)
    bpy.utils.register_class(OBJECT_OT_PC_CompAddDefocus)
    bpy.utils.register_class(OBJECT_OT_PC_CompAddMBlur)
 
     
     
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
 
    #bpy.app.handlers.scene_update_post.append(update_all)
    #bpy.app.handlers.render_pre.remove(update_all)
    bpy.app.handlers.frame_change_pre.remove(update_all)
    #bpy.app.handlers.scene_update_pre.remove(update_all)
     
    keyMapItems = bpy.context.window_manager.keyconfigs.active.keymaps['3D View'].keymap_items
    for keyMapItem in keyMapItems:
        if keyMapItem.idname == 'wm.call_menu' and keyMapItem.properties.name == "VIEW3D_Physical_Camera_click_DOF":
            keyMapItems.remove(keyMapItem)
            break
     
    bpy.types.INFO_HT_header.remove(draw_item)
    bpy.utils.unregister_class(ClickDOF)
     
    bpy.utils.unregister_class(CAMERA_PC_movie_formats_add)
    bpy.utils.unregister_class(CAMERA_PC_movie_formats)
     
    bpy.utils.unregister_class(CAMERA_PC_still_formats_add)
    bpy.utils.unregister_class(CAMERA_PC_still_formats)
     
    #Compositor
    bpy.utils.unregister_class(PhysicalCameraComp)
    bpy.utils.unregister_class(OBJECT_OT_PC_CompAddDefocus)
    bpy.utils.unregister_class(OBJECT_OT_PC_CompAddMBlur)
     
if __name__ == "__main__":
    register()
#if __name__ == "__main__":
#    unregister()
