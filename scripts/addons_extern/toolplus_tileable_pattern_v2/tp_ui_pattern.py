import bpy
from bpy import*
from bpy.props import *
#from . icons.icons import load_icons



class View3D_TP_Tileable_Pattern_Panel(bpy.types.Panel):
    """"""
    bl_label = "Editing"
    bl_idname = "OBJECT_TP_Tileable_Pattern"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' 
    bl_category = "T+"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (isModelingMode)


    def draw(self, context):
        layout = self.layout.column_flow(1)
        layout.operator_context = 'INVOKE_DEFAULT'

        #icons = load_icons()
        #CST = icons.get("CST")
        #row.label("Animation Render", icon_value=CST.icon_id)
        
        if len(context.selected_objects) == 0:

            box = layout.box().column(1)

            row = box.row(1)          
            row.label(text="Nothing selected", icon = "INFO")      

            box.separator()   

        else:                    

            if context.mode == 'OBJECT':



                obj = context.active_object
                if obj:
                    obj_type = obj.type
                    
                    
                    if obj.type not in {'CAMERA', 'LAMP'}:   
                        
                        box = layout.box().column(1)

                        row = box.row(1)          
                        row.label(text="Relation", icon = "CONSTRAINT_DATA")      

                        box.separator()                                     
              
                        row = box.row(1) 
                        row.operator("object.make_links_data",text="link", icon="LINKED").type='OBDATA'
                        row.operator("tp_ops.make_single",text="unlink", icon="UNLINKED")
                        row.operator("object.join", icon = "AUTOMERGE_ON")                 

                        box.separator()   

                        row = box.row(1)                
                        if context.mode == 'OBJECT':
                            row.operator_menu_enum("object.origin_set", "type","Origin", icon="LAYER_ACTIVE")
                        else:
                            row.operator("tp_ops.origin_obm","Object", icon = "LAYER_ACTIVE")
                            row.operator("tp_ops.origin_edm","Edit", icon = "LAYER_ACTIVE")


                        if obj.type in {'MESH'}: 
                                row.operator("bbox.ops_back","BBox", icon ="LAYER_ACTIVE")
                            
                        box.separator()   



                box = layout.box().column(1)

                row = box.row(1)          
                row.label(text="Optimize", icon = "MODIFIER")      

                box.separator()
                
                row = box.row(1) 
                row.operator("object.hide_view_clear","Show", icon = "RESTRICT_VIEW_OFF")
                row.operator("object.hide_view_set","Hide", icon = "RESTRICT_VIEW_ON").unselected=False           
                
                row = box.row(1) 
                row.operator("tp_ops.tileable_unfreeze", "Unfreeze", icon = "RESTRICT_SELECT_OFF")                
                row.operator("tp_ops.tileable_freeze", "Freeze",icon = "RESTRICT_SELECT_ON")    

                box.separator()


                obj = context.active_object
                if obj:
                    obj_type = obj.type
                    
                    
                    if obj.type in {'CAMERA'}:    
                        
                        box = layout.box().column(1)

                        row = box.row(1)          
                        row.label(text="Camera", icon = "CAMERA_DATA")     

                        box.separator()
                        
                        row = box.row(1)
                        row.operator("view3d.viewnumpad","Jump to View", icon = "RENDER_REGION").type='CAMERA' 
                        
                        if bpy.context.space_data.lock_camera == False:
                            row.prop(context.space_data, "lock_camera", text="", icon = "UNLOCKED")                         
                        else:
                            row.prop(context.space_data, "lock_camera", text="", icon = "LOCKED")  

                        box.separator()
                        
                        row = box.column_flow(2)       
                        row.prop(context.object.data, "show_guide", text="Composition guides")           
                        row.prop(context.object.data, "show_limits", text="Limits")
                        row.prop(context.object.data, "show_mist", text="Mist")
                        row.prop(context.object.data, "show_sensor", text="Sensor")
                        row.prop(context.object.data, "show_name", text="Name")      
                        row.prop(context.object.data, "show_passepartout", text="Passepartout")                          
                        row.prop(context.object.data, "passepartout_alpha", text="Alpha", slider=True)

                        ###    
                        box.separator()     


                    if obj_type in {'LAMP'}:    

                        lamp = context.object.data
                        if lamp.type in {'POINT', 'SUN', 'SPOT', 'HEMI', 'AREA'}:                          
                          
                            box = layout.box().column(1) 
                                              
                            row = box.row(1)
                            row.prop(lamp, "type", expand=True)

                            row = box.row(1)
                            row.prop(lamp, "color", text="")
                            row.prop(lamp, "energy")

                            if lamp.type in {'POINT', 'SPOT'}:

                                row = box.row(1)
                                row.prop(lamp, "falloff_type", text="")
                                row.prop(lamp, "distance")

                                if lamp.falloff_type == 'LINEAR_QUADRATIC_WEIGHTED':                   
                                    row = box.row(1)
                                    row.prop(context.object.data, "linear_attenuation", slider=True, text="Linear")
                                    row.prop(context.object.data, "quadratic_attenuation", slider=True, text="Quadratic")

                                row = box.row(1)
                                row.prop(lamp, "use_sphere")

                            if lamp.type == 'AREA':
                                row = box.row(1)
                                row.prop(lamp, "distance")
                                row.prop(lamp, "gamma")                   

                            ###    
                            box.separator()  
                          
                    
                    
                    if obj_type in {'MESH'}:                 

                        row = box.row(1) 
                        row.operator("object.shade_smooth", text="Smooth", icon="SOLID")
                        row.operator("object.shade_flat", text="Flat", icon="MESH_CIRCLE")                    
                                                          
                        row = box.row(1)               
                        row.operator("tp_ops.purge_unused_data","Purge", icon = "X")    
                        row.operator("tp_ops.recalculate_normals","Rec.Normal", icon = "SNAP_NORMAL")     
                        
                        box.separator()

                        box = layout.box().column(1)
                        
                        row = box.row(1)                                                       
                        row.operator("object.convert",text="Convert > Curve", icon="CURVE_DATA").target='CURVE' 
                   
                    
                    if obj_type in {'CURVE'}:

                        row = box.row(1) 
                        row.operator("object.shade_smooth", text="Smooth", icon="SOLID")
                        row.operator("object.shade_flat", text="Flat", icon="MESH_CIRCLE")                    
                                                          
                        row = box.row(1)               
                        row.operator("tp_ops.purge_unused_data","Purge", icon = "X")                     
                        row.operator("object.join", icon = "AUTOMERGE_ON")       
                        
                        box.separator()

                        box = layout.box()
                        row = box.row(1)
                        sub = row.row(1)
                        sub.scale_x = 0.25           
                        sub.prop(context.object.data, "dimensions", expand=True)
                         
                        box = layout.box().column(1)

                        row = box.row(1)
                        row.alignment = 'CENTER' 
                        row.label("Bevel Curve") 
                         
                        row = box.row(1)        
                        row.prop(context.object.data, "fill_mode", text="")           
                        row.prop(context.object.data, "use_fill_deform")

                        box = layout.box().column(1)
                         
                        row = box.row(1)
                        row.prop(context.object.data, "bevel_depth", text="Bevel Depth")
                         
                        row = box.row(1)
                        row.prop(context.object.data, "resolution_u", text="Rings")          
                        row.prop(context.object.data, "bevel_resolution", text="Loops")

                        row = box.row(1)
                        row.prop(context.object.data, "offset")
                        row.prop(context.object.data, "extrude","Height")                  

                        box = layout.box().column(1)
                        

                    if obj_type in {'CURVE', 'SURFACE', 'META', 'FONT'}:
                        
                        row = box.row(1)                                     
                        row.operator("object.convert",text="Convert > Mesh ", icon = "OUTLINER_DATA_MESH").target="MESH"                    
                    
                       
                    box.separator()

                    box = layout.box().column(1)

                    row = box.row(1)
                    row.prop(context.object, "show_x_ray", text="X-Ray", icon ="META_CUBE") 
                    row.prop(context.object, "draw_type", text="")           
                    
                    row = box.row(1)            
                    row.operator("tp_ops.wire_all", text="Wire all", icon='WIRE')
                    
                    active_wire = bpy.context.object.show_wire 
                    if active_wire == True:
                        row.operator("tp_ops.wire_off", "Wire Select", icon = 'MESH_PLANE')              
                    else:                       
                        row.operator("tp_ops.wire_on", "Wire Select", icon = 'MESH_GRID')    

                    box.separator()

                                        
                    if obj_type in {'CURVE'}:
                        
                        box = layout.box().column(1)

                        row = box.row(1)          
                        row.label(text="Join", icon = "MOD_MESHDEFORM")      

                        box.separator() 
     
                        row = box.row(1) 
                        row.operator("tp_ops.join_curves",text = "merge curve instances", icon = "FULLSCREEN_EXIT")   

                 



            if context.mode == 'EDIT_MESH':            

                box = layout.box().column(1)

                row = box.row(1)  
                row.operator("mesh.reveal","Show", icon = "RESTRICT_VIEW_OFF")
                row.operator("mesh.hide","Hide", icon = "RESTRICT_VIEW_ON").unselected=False

                box.separator()

                row = box.row(1)
                row.operator("mesh.faces_shade_smooth", text="Smooth", icon="SMOOTH")
                row.operator("mesh.faces_shade_flat", text="Flat", icon="MESH_CIRCLE") 

                row = box.row(1)
                row.operator("mesh.normals_make_consistent",text="Recalculate", icon='SNAP_NORMAL')
                row.operator("mesh.flip_normals", text="Flip", icon = "FILE_REFRESH")   
                
                box.separator()

                row = box.row(1)
                row.prop(context.object, "show_x_ray", text="X-Ray", icon ="META_CUBE") 
                row.prop(context.object, "draw_type", text="")             
              
                box.separator()

                row = box.row(1)
                row.operator("mesh.remove_doubles", "Rem. Doubles")
                row.operator_menu_enum("mesh.merge", "type")
                
                box.separator()
                
                row = box.row(1)
                row.operator("mesh.delete_loose")
                row.operator("mesh.fill_holes")

                box.separator()
                
                row = box.row(1)
                row.operator("mesh.subdivide")
                row.operator("mesh.unsubdivide", text="(Un-)Subdivide")

                box.separator()

     
            if context.mode == 'EDIT_CURVE':   
      
                 box = layout.box().column(1)
                 
                 row = box.column(1)  
                 row.operator("curve.spline_type_set", "Set Spline Type", icon="IPO_BEZIER")           
                 row.operator("curve.switch_direction", text="Switch Direction", icon = "ARROW_LEFTRIGHT")                   
                 row.operator("curve.cyclic_toggle","Open / Close Curve", icon="MOD_CURVE")  
                          
                 box = layout.box().column(1)

                 row = box.row(1)
                 row.alignment = 'CENTER'  
                 row.label("Handles") 
                
                 row = box.row(1)   
                 row.operator("curve.handle_type_set", text="Auto").type = 'AUTOMATIC'
                 row.operator("curve.handle_type_set", text="Vector").type = 'VECTOR'
                 
                 row = box.row(1)   
                 row.operator("curve.handle_type_set", text="Align").type = 'ALIGNED'
                 row.operator("curve.handle_type_set", text="Free").type = 'FREE_ALIGN'
                 
                 box.separator() 

                 box = layout.box().column(1)

                 row = box.row(1)
                 row.alignment = 'CENTER' 
                 row.label("Subdivide")   
                 
                 row = box.row(1) 
                 row.operator("curve.subdivide", text="1").number_cuts=1        
                 row.operator("curve.subdivide", text="2").number_cuts=2
                 row.operator("curve.subdivide", text="3").number_cuts=3
                 row.operator("curve.subdivide", text="4").number_cuts=4
                 row.operator("curve.subdivide", text="5").number_cuts=5        
                 row.operator("curve.subdivide", text="6").number_cuts=6  
                 
                 box.separator() 
                
                 box = layout.box().column(1)

                 row = box.row(1)  
                 row.operator("curve.extrude_move", text="Extrude")
                 row.operator("curve.make_segment",  text="Weld") 

                 row = box.row(1)             
                 row.operator("curve.split",  text="Split")          
                 row.operator("curve.bezier_spline_divide", text='Divide') 
                          
                 row = box.row(1)             
                 row.operator("curve.separate",  text="Separate")         
                 row.operator("curve.bezier_points_fillet", text='Fillet') 
             
                 row = box.row(1)
                 row.operator("transform.vertex_random") 
                 row.operator("object._curve_outline",  text="Outline")             

                 row = box.row(1)
                 row.operator("curve.trim_tool", text="Trim")
                 row.operator("curve.extend_tool", text="Extend")

                 row = box.row(1) 
                 row.operator("transform.tilt", text="Tilt")                                     
                 row.operator("curve.radius_set", "Radius")                 

                 box.separator()  

                 row = box.row(1) 
                 row.operator("curve.smooth", icon ="SMOOTHCURVE")  

                 ###
                 box.separator() 
             
                 box = layout.box()
                 row = box.row(1)
                 sub = row.row(1)
                 sub.scale_x = 0.25           
                 sub.prop(context.object.data, "dimensions", expand=True)
                 
                 box = layout.box().column(1)

                 row = box.row(1)
                 row.alignment = 'CENTER' 
                 row.label("Bevel Curve") 
                 
                 row = box.row(1)        
                 row.prop(context.object.data, "fill_mode", text="")           
                 row.prop(context.object.data, "use_fill_deform")

                 box = layout.box().column(1)
                 
                 row = box.row(1)
                 row.operator("tp_ops.wire_all", text="", icon='WIRE')
                 row.prop(context.object.data, "bevel_depth", text="Bevel Depth")
                 
                 row = box.row(1)
                 row.prop(context.object.data, "resolution_u", text="Rings")          
                 row.prop(context.object.data, "bevel_resolution", text="Loops")

                 row = box.row(1)
                 row.prop(context.object.data, "offset")
                 row.prop(context.object.data, "extrude","Height")


