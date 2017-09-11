import bpy
from bpy import*
from bpy.props import *





class View3D_Batch_MiraTools(bpy.types.Operator):
    """Edit MiraTools"""
    bl_idname = "tp_ops.miratools"
    bl_label = "MiraTools :)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):      
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 250)  
 
    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'     
        layout.operator_context = 'INVOKE_REGION_WIN'  
        
        box = layout.box().column(1)

        row = box.row(1)
        row.label("New Mesh Creation")
            
        box.separator()
        
        row = box.row(1)         
        row.operator("mira.poly_loop", text="Poly Loop", icon="MESH_GRID")
            
        box.separator()

        row = box.row(1)
             
        row.operator("mira.curve_surfaces", text="CurveSurfaces", icon="SURFACE_NCURVE")
        
        box.separator()
        
        row = box.row(1)
        row.prop(context.scene.mi_cur_surfs_settings, "spread_loops_type", text='Points')        
                 
        box = layout.box().column(1) 

        row = box.row(1)
        row.label("Loop Manipulation")
            
        box.separator()        
        
        row = box.row(1)        
        row.operator("mira.curve_stretch", text="CurveStretch", icon="STYLUS_PRESSURE")
        row.prop(context.scene.mi_cur_stretch_settings, "points_number", text='PointsNumber')       
        
        box.separator()
        
        row = box.row(1)     
        row.operator("mira.curve_guide", text="CurveGuide", icon="RNA")
        row.prop(context.scene.mi_curguide_settings, "points_number", text='LoopSpread')

        box.separator() 
        
        row = box.row(1)
        row.prop(context.scene.mi_curguide_settings, "deform_type", text='DeformType')      

        box = layout.box().column(1)  

        row = box.row(1)
        row.label("Mesh Transformation")
            
        box.separator() 
        
        row = box.row(1) 
        row.operator("screen.redo_last", text = "", icon="SETTINGS") 
        row.operator("mira.deformer", text="Deformer")
        row.operator("mira.noise", text="NoiseDeform", icon="RNDCURVE")
       
        box.separator() 
 
        row = box.row(1) 
        row.operator("mira.linear_deformer", text="LinearDeformer", icon="OUTLINER_OB_MESH")
        
        row = box.row(1) 
        row.prop(context.scene.mi_ldeformer_settings, "manual_update", text='ManualUpdate')

        box = layout.box().column(1)         

        row = box.row(1)
        row.label("New Mesh Drawing")
            
        box.separator() 

        row = box.row(1)                       
        row.operator("mira.draw_extrude", text="Draw Extrude", icon="VPAINT_HLT")

        box.separator()
        
        if context.scene.mi_extrude_settings.extrude_step_type == 'Asolute':
            row.prop(context.scene.mi_extrude_settings, "absolute_extrude_step", text='Step')
        else:
            row.prop(context.scene.mi_extrude_settings, "relative_extrude_step", text='Step')
 
        row = box.row(1) 
        row.prop(context.scene.mi_extrude_settings, "extrude_step_type", text='Step') 
            
        box.separator()

        row = box.row(1) 
        if context.scene.mi_settings.surface_snap is False:
            row.prop(context.scene.mi_extrude_settings, "do_symmetry", text='Symmetry')

            if context.scene.mi_extrude_settings.do_symmetry:
                row.prop(context.scene.mi_extrude_settings, "symmetry_axys", text='Axys')


        box = layout.box().column(1)  

        row = box.row(1)
        row.label("Tool Settings")
            
        box.separator() 
       
        row = box.row(1) 
        row.prop(context.scene.mi_settings, "surface_snap", text='Snap', icon="SNAP_SURFACE")     
        row.prop(context.scene.mi_settings, "snap_objects", text='', icon="VISIBLE_IPO_ON")
        row.prop(context.scene.mi_settings, "convert_instances", text='i-Convert', icon="BOIDS")


        box = layout.box().column(1)    
                      
        row = box.row(1)                                
        row.operator("screen.screen_full_area", text = "", icon = "FULLSCREEN_ENTER")  
        row.operator("ed.undo_history", text="History")
        
        sub = row.row(1)         
        sub.scale_x = 5
        sub.operator("ed.undo", text = "", icon="LOOP_BACK")
        sub.operator("ed.redo", text = "", icon="LOOP_FORWARDS") 

        
        




