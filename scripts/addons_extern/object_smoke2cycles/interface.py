# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.69.x+ Smoke2Cycles-Addon
# --------------------------------------------------------------------------
#
# Author:
# HiPhiSch
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
#
import bpy
import mathutils as mu
from . import smoke_export_core as core
from .create_mat import Smoke2CyclesImportMaterialGenerator
import os
from traceback import print_exc

class Smoke2CylcesDomainSettings(bpy.types.PropertyGroup):
    """Smoke2Cycles addon settings on a smoke domain object"""
    cycles_domain_obj = bpy.props.StringProperty(name="Cycles Domain Object") 
    cycles_material = bpy.props.StringProperty(name="Cycles Material")
    texture_filename_base = bpy.props.StringProperty(name="Filename Base",
        description="Filename base for texture export, frame and .exr are attached automatically", subtype='FILE_PATH')    
    
class Smoke2CyclesOperatorSettings(bpy.types.PropertyGroup):
    """Smoke2Cycles addon settings for the operator"""
    current_frame = bpy.props.BoolProperty(name="Current Frame",
        description= "Apply only to current frame", default=True)
    export_texture = bpy.props.BoolProperty(name="Export Texture",
        description="Export the required texture", default=True)
    texture_filename_base = bpy.props.StringProperty(name="Filename Base",
        description="Filename base for texture export, frame and .exr are attached automatically",
        default = "//smoke_export", subtype='FILE_PATH')
    create_material = bpy.props.BoolProperty(name="Create Material",
        description="Create the required cycles material", default=True)
    material_type = bpy.props.EnumProperty(name="Material type",
        description = "Select the cycles material for generation", 
        items=[('FIRE', "Fire", "only fire") ,('SMOKE', "Smoke", "only smoke"), ('SMOKE_FIRE', "Smoke + Fire", "smoke and fire")],
        default='SMOKE_FIRE')        
    create_domain_cube = bpy.props.BoolProperty(name="Create Domain Cube",
        description="Create the required cycles material", default=True)
    domain_cube_layer = bpy.props.IntProperty(name="Cycles Domain Cube Layer",
        description = "layer in which a new cycles domain cube is created", default=2,
        min=1, max=20)
    update_key_frames= bpy.props.BoolProperty(name="Update Key Frames",
        description ="Auto insert required key frames", default=True)
    keep_settings = bpy.props.BoolProperty(name="Keep Material/Cube/Export Path",
        description="Use existing materials / cube rather than creating new ones if possible", default=True) 
    start_frame=bpy.props.IntProperty(name="Start Frame",
        description="Use existing material / cube rather than creating new ones", default=1, min = 1) 
    end_frame=bpy.props.IntProperty(name="End Frame",          
        description ="End frame for export", default=10, min = 1)
 
class OBJECT_OT_smoke2cycles(bpy.types.Operator):
    """Convert smoke/fire into cycles compatible materials"""
    bl_idname = "object.smoke2cycles"
    bl_label = "Smoke2Cycles"
    bl_description = "Convert smoke/fire into cycles compatible materials"
    bl_options = {'UNDO'}
    
    settings_glob = bpy.props.PointerProperty(type=Smoke2CyclesOperatorSettings)
    current_frame = bpy.props.IntProperty()
    end_frame = bpy.props.IntProperty()
    progr = bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        return core.is_smoke_domain(context.object)
    
    def __export_texture(self, resolution, smoke, fire, name, frm):
        """export the texture"""        
        scn = bpy.context.scene
        ims = scn.render.image_settings
        backup = {
            'ff': ims.file_format,
            'ec': ims.exr_codec,
            'cd': ims.color_depth,
            'fp': scn.render.filepath,
            'rp': scn.render.resolution_percentage,
            'rx': scn.render.resolution_x,
            'ry': scn.render.resolution_y
        }
         
        try:
            i1 = bpy.data.images.new("export_image", resolution[0], resolution[1] * resolution[2], True, True)
            try:
                # basic settings
                i1.file_format = 'OPEN_EXR'
                i1.colorspace_settings.name = 'Non-Color'
                i1.alpha_mode = 'STRAIGHT'

                # required for compression
                ims = scn.render.image_settings
                ims.file_format = 'OPEN_EXR'
                ims.exr_codec = 'PIZ'
                ims.color_depth = '32'
                scn.render.resolution_percentage = 100
                scn.render.resolution_x = resolution[0]
                scn.render.resolution_y = resolution[1] * resolution[2]
                scn.render.filepath=bpy.path.abspath(os.path.split(name)[0])
                scn.update()
                
                # store data
                pix_arr = [0.0] * (len(smoke) * 4)				
                pix_arr[::4] = smoke # r
                pix_arr[1::4] = fire # g
                pix_arr[3::4] = [1.0] * len(smoke) # alpha
                
                i1.pixels[:] = pix_arr
                
                # save texture
                name = "%s_%03d.exr" % (os.path.split(name)[1], frm)
                i1.save_render(os.path.join(scn.render.filepath, name))
            finally:
                bpy.data.images.remove(i1)
        finally:
            ims.file_format = backup['ff']
            ims.exr_codec = backup['ec']
            ims.color_depth = backup['cd']
            scn.render.filepath = backup['fp']
            scn.render.resolution_percentage = backup['rp']
            scn.render.resolution_x = backup['rx']
            scn.render.resolution_y = backup['ry']
    
    def cleanup(self, context):
        """cleanup after operation"""
        bpy.context.window_manager.progress_end()
    
    def modal(self, context, event):
        """update the individual frames"""
        # settings
        stg = self.settings_glob
        stl = context.object.smoke2cycles

        # finished?
        if self.current_frame > self.end_frame:
            self.cleanup(context)
            return {'FINISHED'}
        
        # cancelled?
        if event.type == 'ESC':
            self.cleanup(context)
            return {'CANCELLED'}
        
        # progress update
        bpy.context.window_manager.progress_update(self.progr) 
        self.progr += 1
        
        # material, domain, and basename from local object
        c_mat = stl.cycles_material
        c_mat = bpy.data.materials[c_mat] if c_mat in bpy.data.materials else None
        c_dom = stl.cycles_domain_obj
        c_dom = bpy.data.objects[c_dom] if c_dom in bpy.data.objects else None 
        basename = stl.texture_filename_base
        
        # frame to work with
        frm = self.current_frame
        self.current_frame += 1
        
        # Debug
        print("Smoke2Cycles: parsing frame %d" % frm)
        
        try:
            # create export object
            sm_exp = core.SmokeExporter(context.object, frm)
            
            if stg.export_texture:                    
                # export the texture
                self.__export_texture( \
                    sm_exp.resolution, sm_exp.smoke, sm_exp.fire, basename, frm)
                
            # transform domain cube to adapt to domain
            if stg.create_domain_cube: 
                c_dom.matrix_world = sm_exp.adaptive_bbox_wm
            
            # adapt material
            if stg.create_material:
                nodes = c_mat.node_tree.nodes
                if "S2C_IMPORT_SCRIPT" in nodes:
                    n = nodes["S2C_IMPORT_SCRIPT"]
                    
                    if "CurrentFrame" in n.inputs:
                        n.inputs["CurrentFrame"].default_value = frm
                    if "Divisions" in n.inputs:
                        n.inputs["Divisions"].default_value = sm_exp.resolution[2]
                    
                    if (basename != "") and ("TextureFilenameBase" in n.inputs):
                        n.inputs["TextureFilenameBase"].default_value = basename
                
                
                if "S2C_FIRE_TEMP" in nodes:
                    n = nodes["S2C_FIRE_TEMP"]
                    
                    if "LowTemp" in n.inputs:
                        n.inputs["LowTemp"].default_value = sm_exp.flame_temp_span[0]
                    if "HighTemp" in n.inputs:
                        n.inputs["HighTemp"].default_value = sm_exp.flame_temp_span[1]         
                        
            # update the key frames
            if stg.update_key_frames:
                # update domain cube               
                if not c_dom is None:
                    c_dom.keyframe_insert("location", frame=frm, group="s2c_adaptive_domain")
                    c_dom.keyframe_insert("rotation_euler", frame=frm, group="s2c_adaptive_domain")
                    c_dom.keyframe_insert("scale", frame=frm, group="s2c_adaptive_domain")  
                    
                # update material
                if not c_mat is None:
                    nodes = c_mat.node_tree.nodes                                        
                    if "S2C_IMPORT_SCRIPT" in nodes:                        
                        n = nodes["S2C_IMPORT_SCRIPT"]
                        if "CurrentFrame" in n.inputs:
                            n.inputs["CurrentFrame"].keyframe_insert("default_value", frame=frm, group="s2c_mat")
                        if "Divisions" in n.inputs:
                            n.inputs["Divisions"].keyframe_insert("default_value", frame=frm, group="s2c_mat")                                                            
        
        except Exception as e:
            if isinstance(e, core.EUnsuportedPlatform):
                self.report({'WARNING'}, "Platform not yet supported")
            elif isinstance(e, core.ELoadCompressionLibraryFailed):
                self.report({'WARNING'}, "Required compression library could not be found or loaded: {1}".format(e))
            elif isinstance(e, core.ENoDomain):
                self.report({'WARNING'}, "Object is not a smoke domain!")
            elif isinstance(e, core.ENotBaked):
                self.report({'WARNING'}, "Please bake the smoke physics first!")
            else:
                self.report({'WARNING'}, "Unexpected error: {1}".format(e))
            
            self.cleanup(context)
            
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
    
    def execute(self, context):    
        """update local settings and initialize"""
        stg = self.settings_glob
        stl = context.object.smoke2cycles
        
        # determine the required frames
        if stg.current_frame:
            self.current_frame = self.end_frame = context.scene.frame_current
            prog_max = 1
        else:
            self.current_frame = stg.start_frame
            self.end_frame = stg.end_frame
            prog_max = stg.end_frame - stg.start_frame + 1                
        
        # create the required material
        c_mat = stl.cycles_material
        c_mat = bpy.data.materials[c_mat] if c_mat in bpy.data.materials else None
        if ((c_mat is None) or (not stg.keep_settings)) and stg.create_material:
            c_mat = Smoke2CyclesImportMaterialGenerator.generate_material(stg.material_type)
            stl.cycles_material = c_mat.name
        
        # generate cycles domain cube if required
        c_dom = stl.cycles_domain_obj        
        c_dom = bpy.data.objects[c_dom] if c_dom in bpy.data.objects else None
        ao = context.scene.objects.active
        try:
            if ((c_dom is None) or (not stg.keep_settings)) and stg.create_domain_cube:
                # create a default cube as domain
                bpy.ops.mesh.primitive_cube_add(layers= \
                    tuple([i == stg.domain_cube_layer for i in range(1,21)]) )
                c_dom = context.object
                c_dom.name = "CyclesSmokeDom"
                c_dom.matrix_world = mu.Matrix.Identity(4)
                              
                stl.cycles_domain_obj = c_dom.name                    

            if not ((c_mat is None) or (c_dom is None)) :
                if stg.create_material:
                    # assign the correct material
                    if len(c_dom.material_slots) == 0:
                        bpy.ops.object.material_slot_add()
                    c_dom.material_slots[0].material = c_mat    
        finally:
            context.scene.objects.active = ao
                            
                
        # determine the right texture base filename:
        basename = ""
        if not c_dom is None:
            basename = stl.texture_filename_base
        if (not stg.keep_settings) or (basename == ""):
            basename = stg.texture_filename_base
            stl.texture_filename_base = basename

        # progress indicator
        self.progr = 0        
        context.window_manager.progress_begin(0, prog_max * 100) # strange mapping to 0 to 9999                       
        
        context.window_manager.modal_handler_add(self)           
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        # copy the settings for correct redo operations
        sg = context.scene.smoke2cycles
        self.settings_glob.current_frame = sg.current_frame
        self.settings_glob.export_texture = sg.export_texture
        self.settings_glob.texture_filename_base = sg.texture_filename_base
        self.settings_glob.create_material = sg.create_material
        self.settings_glob.material_type = sg.material_type
        self.settings_glob.create_domain_cube = sg.create_domain_cube
        self.settings_glob.domain_cube_layer = sg.domain_cube_layer
        self.settings_glob.update_key_frames = sg.update_key_frames
        self.settings_glob.keep_settings = sg.keep_settings
        self.settings_glob.start_frame = sg.start_frame
        self.settings_glob.end_frame = sg.end_frame

        return self.execute(context)

class VIEW3D_PT_Smoke2Cycles(bpy.types.Panel):
    """Smoke2Cycles - settings panel"""
    bl_idname = "VIEW3D_PT_Smoke2Cycles"
    bl_label = "Smoke2Cycles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = "Physics"
        
    @classmethod
    def poll(cls, context):
        return not context.object is None
    
    def draw(self, context):
        layout = self.layout
        
        if core.is_smoke_domain(context.object):
            s2cp = context.scene.smoke2cycles
            
            box = layout.box()
            cols = box.column()
            
            cols.prop(s2cp, "current_frame")
            if not s2cp.current_frame:
                r_1 = cols.row(align=True)
                r_1.alignment = 'EXPAND'
                r_1.prop(s2cp, "start_frame")
                r_1.prop(s2cp, "end_frame")  
            cols.prop(s2cp, "export_texture")  
            if s2cp.export_texture:
                cols.prop(s2cp, "texture_filename_base")
            cols.prop(s2cp, "create_material")
            if s2cp.create_material:
                cols.prop(s2cp, "material_type")
            cols.prop(s2cp, "create_domain_cube")
            if s2cp.create_domain_cube:
                cols.prop(s2cp, "domain_cube_layer")
            cols.prop(s2cp, "update_key_frames")
            # ----
            cols = layout.box().column()
            cols.label("Keep empty for the first run", icon='INFO')
            cols.prop(s2cp, "keep_settings")
            cols.prop_search(context.object.smoke2cycles, "cycles_domain_obj", bpy.data, "objects")
            cols.prop_search(context.object.smoke2cycles, "cycles_material", bpy.data, "materials")
            cols.prop(context.object.smoke2cycles, "texture_filename_base")
            
            # ----
            layout.operator("OBJECT_OT_smoke2cycles")
        else:
            layout.label(text="Please select a smoke domain", icon='INFO')
        
    
def register():
    bpy.utils.register_class(Smoke2CylcesDomainSettings)
    bpy.utils.register_class(Smoke2CyclesOperatorSettings)
    bpy.utils.register_class(OBJECT_OT_smoke2cycles)
    bpy.utils.register_class(VIEW3D_PT_Smoke2Cycles)

    bpy.types.Object.smoke2cycles = bpy.props.PointerProperty(type=Smoke2CylcesDomainSettings,
        description="Smoke2Cycles domain settings")
    bpy.types.Scene.smoke2cycles = bpy.props.PointerProperty(type=Smoke2CyclesOperatorSettings,
        description="Smoke2Cycles settings")
        
    
    
def unregister():
    del bpy.types.Scene.smoke2cycles
    del bpy.types.Object.smoke2cycles

    bpy.utils.unregister_class(bpy.types.VIEW3D_PT_Smoke2Cycles)
    bpy.utils.unregister_class(bpy.types.OBJECT_OT_smoke2cycles)
    bpy.utils.unregister_class(bpy.types.Smoke2CyclesOperatorSettings)
    bpy.utils.unregister_class(bpy.types.Smoke2CylcesDomainSettings)
    
    
    
if __name__ == "__main__":
    print('-' * 40)
    try:
        unregister()
    except:
        print("WARNING: unregister failed!")
        print_exc()
    register()