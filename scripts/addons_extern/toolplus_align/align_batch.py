__status__ = "toolplus custom version"
__author__ = "mkbreuer"
__version__ = "1.0"
__date__ = "2016"


import bpy, mathutils, math, re
from mathutils.geometry import intersect_line_plane
from mathutils import Vector
from math import radians
from bpy import*


#Align
def axe_select(self, context):
    axes = ['X','Y','Z']
    return [tuple(3 * [axe]) for axe in axes]

#Align
def project_select(self, context):
    projects = ['XY','XZ','YZ','XYZ']
    return [tuple(3 * [proj]) for proj in projects]



def draw_normal_tools(context, layout):

    Display_Normals = context.user_preferences.addons[__package__].preferences.tab_normals_menu
    if Display_Normals == 'on':
                 
        box = layout.box().column(1) 
        
        row = box.column(1) 
        row.label("Normals Transform", icon="ROTACTIVE")

        box.separator() 

        row = box.row(1)                
        row.menu("tp_ops.translate_normal_menu", text="Move")
        row.menu("tp_ops.rotate_normal_menu", text="Rotate")
        row.menu("tp_ops.resize_normal_menu", text="Scale")           

        box.separator() 



class View3D_TP_Align_Menu(bpy.types.Operator):
    """TP Align :)"""
    bl_label = "TP Align :)"
    bl_idname = "tp_batch.align_menu"               
    bl_options = {'REGISTER', 'UNDO'}          
    
    bpy.types.Scene.AxesProperty = bpy.props.EnumProperty(items=axe_select)
    bpy.types.Scene.ProjectsProperty = bpy.props.EnumProperty(items=project_select)

    def draw(self, context):
        tpw = context.window_manager.tp_collapse_menu_align
        lt = context.window_manager.looptools
        
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        
        if context.mode == 'OBJECT':

            box = layout.box().column(1)  
            
            row = box.row(1)
            row.alignment = "CENTER"            
            row.label("Align all Selected to Active")  
             
            box.separator() 
                        
            row = box.row(1)
            row.operator("object.align_location_all",text=" ", icon='MAN_TRANS')  
            row.operator("object.align_location_x",text="X")
            row.operator("object.align_location_y",text="Y")
            row.operator("object.align_location_z",text="Z")
        
            sub = row.row(1)
            sub.scale_x = 2.0    
            sub.operator("object.location_clear", text="", icon="X")
          
            props = row.operator("object.transform_apply", text="",icon="FILE_TICK")
            props.location= True
            props.rotation= False
            props.scale= False
                         
            row = box.row(1)
            row.operator("object.align_rotation_all",text=" ", icon='MAN_ROT') 
            row.operator("object.align_rotation_x",text="X")
            row.operator("object.align_rotation_y",text="Y")
            row.operator("object.align_rotation_z",text="Z")
            
            sub = row.row(1)
            sub.scale_x = 2.0           
            sub.operator("object.rotation_clear", text="", icon="X")
            props = row.operator("object.transform_apply", text="",icon="FILE_TICK")
            props.location= False
            props.rotation= True
            props.scale= False           

            row = box.row(1)
            row.operator("object.align_objects_scale_all",text=" ", icon='MAN_SCALE')  
            row.operator("object.align_objects_scale_x",text="X")
            row.operator("object.align_objects_scale_y",text="Y")
            row.operator("object.align_objects_scale_z",text="Z")
            
            sub = row.row(1)
            sub.scale_x = 2.0           
            sub.operator("object.scale_clear", text="", icon="X")
            
            props = row.operator("object.transform_apply", text="",icon="FILE_TICK")
            props.location= False
            props.rotation= False
            props.scale= True  
          
            box.separator()        
           
            row = box.row(1)         
            row.operator("object.distribute_osc", text="distribute between origins", icon="ALIGN")   

            box.separator()  

            Display_Normals = context.user_preferences.addons[__package__].preferences.tab_normals_menu
            if Display_Normals == 'on':

                box = layout.box().column(1) 
                          
                row = box.row(1)  
                row.label("Normals [ZZ]") 
                
                row = box.row(1)              
                row.menu("tp_ops.translate_normal_menu", text="Move")
                row.menu("tp_ops.rotate_normal_menu", text="Rotate")
                row.menu("tp_ops.resize_normal_menu", text="Scale")           

                box.separator() 
            
            box = layout.box().column(1) 
                      
            row = box.row(1)  
            row.label("Mirror", icon='ARROW_LEFTRIGHT') 

            row = box.row(1)                             
            row.operator("tp_ops.mirror1",text="X-Axis")
            row.operator("tp_ops.mirror2",text="Y-Axis")
            row.operator("tp_ops.mirror3",text="Z-Axis")      

            box.separator()  
    
            box = layout.box().column(1) 
                      
            row = box.row(1)         
            row.label("Align with Local Y-Axis") 
            
            row = box.row(1) 
            row.operator("lookat.it", text="Look @ Obj ")
            row.operator("lookat.cursor", text="Look @ Cursor")   

            box.separator()  

            box = layout.box().column(1)           

            row = box.row(1)
            row.operator("object.align_by_faces", text="Active Face to Active Face", icon="SNAP_SURFACE") 
            row = box.row(1)
            row.operator("object.drop_on_active", text="Drop down to Active", icon="NLA_PUSHDOWN")        

            box.separator()      
                               
            box = layout.box().column(1)  
            
            row = box.row(1)
            row.operator("object.align_tools", "Advance Align Tools", icon="ROTATE") 

            box.separator()      
                               

        if context.mode == 'EDIT_MESH':

            box = layout.box().row()
            
            row = box.column(1) 
            row.label("Align") 
            row.label("to") 
            row.label("Axis") 

            row = box.column(1)
            row.operator("tp_ops.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
            row.operator("tp_ops.face_align_yz", "Zy", icon='TRIA_UP_BAR')           
            row.operator("tp_ops.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

            row = box.column(1)
            row.operator("tp_ops.face_align_x", "X", icon='TRIA_RIGHT')
            row.operator("tp_ops.face_align_y", "Y", icon='TRIA_UP')           
            row.operator("tp_ops.face_align_z", "Z", icon='SPACE3')

            row.separator()          

            row = layout.box().column(1)                  
            row.operator("tp_ops.align_to_normal", "Align to active Normal", icon ="SNAP_NORMAL")    

            box.separator() 

            box = layout.box().column(1)   
                         
            row = box.column(1)                                                         
            row.operator("mesh.vertex_align",text="Straighten Line", icon ="ALIGN") 
            row.operator("mesh.vertex_distribute",text="Distribute Vertices", icon ="PARTICLE_POINT")                                        
      
            box.separator() 
            
            box = layout.box().column(1)              
            
            row = box.row(1)  
            # space - first line
            split = row.split(percentage=0.15, align=True)
            if lt.display_space:
                split.prop(lt, "display_space", text="", icon='TRIA_DOWN')
            else:
                split.prop(lt, "display_space", text="", icon='TRIA_RIGHT')
            
            split.operator("mesh.looptools_space", text="LT Space", icon='BLANK1')
            # space - settings
            if lt.display_space:
                box = layout.box().column(1)              
                
                row = box.column(1) 
                row.prop(lt, "space_interpolation")
                row.prop(lt, "space_input")

                box.separator()

                col_move = box.column(align=True)
                row = col_move.row(align=True)
                if lt.space_lock_x:
                    row.prop(lt, "space_lock_x", text = "X", icon='LOCKED')
                else:
                    row.prop(lt, "space_lock_x", text = "X", icon='UNLOCKED')
                if lt.space_lock_y:
                    row.prop(lt, "space_lock_y", text = "Y", icon='LOCKED')
                else:
                    row.prop(lt, "space_lock_y", text = "Y", icon='UNLOCKED')
                if lt.space_lock_z:
                    row.prop(lt, "space_lock_z", text = "Z", icon='LOCKED')
                else:
                    row.prop(lt, "space_lock_z", text = "Z", icon='UNLOCKED')
                col_move.prop(lt, "space_influence")

                box.separator() 
                box = layout.box().column(1)   


            row = box.row(1)  
            # curve - first line
            split = row.split(percentage=0.15, align=True)
            if lt.display_curve:
                split.prop(lt, "display_curve", text="", icon='TRIA_DOWN')
            else:
                split.prop(lt, "display_curve", text="", icon='TRIA_RIGHT')
            split.operator("mesh.looptools_curve", text="LT Curve", icon='BLANK1')
            # curve - settings
            if lt.display_curve:
                box = layout.box().column(1)              
                
                row = box.column(1) 
                row.prop(lt, "curve_interpolation")
                row.prop(lt, "curve_restriction")
                row.prop(lt, "curve_boundaries")
                row.prop(lt, "curve_regular")
                
                box.separator()

                col_move = box.column(align=True)
                row = col_move.row(align=True)
                if lt.curve_lock_x:
                    row.prop(lt, "curve_lock_x", text = "X", icon='LOCKED')
                else:
                    row.prop(lt, "curve_lock_x", text = "X", icon='UNLOCKED')
                if lt.curve_lock_y:
                    row.prop(lt, "curve_lock_y", text = "Y", icon='LOCKED')
                else:
                    row.prop(lt, "curve_lock_y", text = "Y", icon='UNLOCKED')
                if lt.curve_lock_z:
                    row.prop(lt, "curve_lock_z", text = "Z", icon='LOCKED')
                else:
                    row.prop(lt, "curve_lock_z", text = "Z", icon='UNLOCKED')
                col_move.prop(lt, "curve_influence")

                box.separator() 
                box = layout.box().column(1)    


            row = box.row(1)  
            # circle - first line
            split = row.split(percentage=0.15, align=True)
            if lt.display_circle:
                split.prop(lt, "display_circle", text="", icon='TRIA_DOWN')
            else:
                split.prop(lt, "display_circle", text="", icon='TRIA_RIGHT')
            split.operator("mesh.looptools_circle", text="LT Circle", icon='BLANK1')
            # circle - settings
            if lt.display_circle:
                box = layout.box().column(1)              
                
                row = box.column(1) 
                row.prop(lt, "circle_fit")
                
                row.separator()

                row.prop(lt, "circle_flatten")
                
                row = box.row(align=True)
                row.prop(lt, "circle_custom_radius")
                
                row_right = row.row(align=True)
                row_right.active = lt.circle_custom_radius
                row_right.prop(lt, "circle_radius", text="")                
                box.prop(lt, "circle_regular")
                
                box.separator()

                col_move = box.column(align=True)
                row = col_move.row(align=True)
                if lt.circle_lock_x:
                    row.prop(lt, "circle_lock_x", text = "X", icon='LOCKED')
                else:
                    row.prop(lt, "circle_lock_x", text = "X", icon='UNLOCKED')
                if lt.circle_lock_y:
                    row.prop(lt, "circle_lock_y", text = "Y", icon='LOCKED')
                else:
                    row.prop(lt, "circle_lock_y", text = "Y", icon='UNLOCKED')
                if lt.circle_lock_z:
                    row.prop(lt, "circle_lock_z", text = "Z", icon='LOCKED')
                else:
                    row.prop(lt, "circle_lock_z", text = "Z", icon='UNLOCKED')
                col_move.prop(lt, "circle_influence")

            
            box.separator() 

            box = layout.box().column(1)              
            
            row = box.column(1) 
            row.operator("mesh.rot_con", "Rotate selected Face", icon ="LOCKVIEW_ON")   
            
            box.separator() 
                                            
            Display_Normals = context.user_preferences.addons[__package__].preferences.tab_normals_menu
            if Display_Normals == 'on':
                         
                box = layout.box().column(1) 
                
                row = box.column(1) 
                row.label("Normals Transform", icon="ROTACTIVE")

                box.separator() 

                row = box.row(1)                
                row.menu("tp_ops.translate_normal_menu", text="Move")
                row.menu("tp_ops.rotate_normal_menu", text="Rotate")
                row.menu("tp_ops.resize_normal_menu", text="Scale")           

                box.separator() 

            box = layout.box().column(1)   
                         
            row = box.column(1)             
            row.label("Mirror", icon="ARROW_LEFTRIGHT")
                            
            row = box.row(1) 
            row.operator("tp_ops.mirror1",text="X-Axis")
            row.operator("tp_ops.mirror2",text="Y-Axis")
            row.operator("tp_ops.mirror3",text="Z-Axis")      

            box.separator() 

            row = box.column(1)          
            row.operator("tp_ops.mirror_over_edge", "Mirror over selected Edge", icon='IPO_LINEAR')    

            box.separator() 
  
            box = layout.box().column(1) 
                      
            row = box.row(1)         
            row.label("Align Edge to Edge") 
            
            row = box.row(1) 
            row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
            align_op = row.operator("mesh.align_operator", text = 'Align Edge').type_op = 0

            box.separator()      
 
            row = box.row(1) 
            if tpw.display_align_help:
                row.prop(tpw, "display_align_help", text="", icon='INFO')
            else:
                row.prop(tpw, "display_align_help", text="", icon='INFO')

            row.prop(bpy.context.window_manager.paul_manager, 'align_dist_z', text = 'Superpose')
            row.prop(bpy.context.window_manager.paul_manager, 'align_lock_z', text = 'lock Z')

            if tpw.display_align_help:

                box.separator() 
                              
                row = box.column(1)         
                row.label("This Tool need stored edge in the target:")         
                row.label("1. go into the editmode of the target") 
                row.label("2. select one edge as active") 
                row.label("3. and press Store Edge") 
               
                row.separator()            
                
                row.label("Now go into editmode of the object you want to align") 
                row.label("1. select all mesh that needs to be align") 
                row.label("2. select on edge as active") 
                row.label("3. and press Align Edge")
                
                row.separator()            
                
                row.label("Superpose: edge jump to edge")                  
                row.label("lock Z: preserve the z axis")                  

            ### 
            box.separator()     
                  

        if context.mode == 'EDIT_LATTICE':

             box = layout.box().row()
             row = box.column(1) 
             row.label("Align") 
             row.label("to") 
             row.label("Axis") 

             row = box.column(1)
             row.operator("tp_ops.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
             row.operator("tp_ops.face_align_yz", "Zy", icon='TRIA_UP_BAR')           
             row.operator("tp_ops.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

             row = box.column(1)
             row.operator("tp_ops.face_align_x", "X", icon='TRIA_RIGHT')
             row.operator("tp_ops.face_align_y", "Y", icon='TRIA_UP')           
             row.operator("tp_ops.face_align_z", "Z", icon='SPACE3')

             box = layout.box().column(1)   

             row = box.row(1) 
             row.operator("lattice.flip", text="FlipX").axis = "U"
             row.operator("lattice.flip", text="FlipY").axis = "V"
             row.operator("lattice.flip", text="FlipZ").axis = "W"

             box.separator()  
             
             row = box.row(1)         
             row.operator("tp_ops.mirror1",text="MX", icon='ARROW_LEFTRIGHT')
             row.operator("tp_ops.mirror2",text="MY", icon='ARROW_LEFTRIGHT')
             row.operator("tp_ops.mirror3",text="MZ", icon='ARROW_LEFTRIGHT')            

             ###         
             box.separator()

             draw_normal_tools(context, layout)    
             
             

        if context.mode == 'EDIT_CURVE' or context.mode == 'EDIT_SURFACE':

             box = layout.box().row()
             row = box.column(1) 
             row.label("Align") 
             row.label("to") 
             row.label("Axis") 

             row = box.column(1)
             row.operator("tp_ops.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
             row.operator("tp_ops.face_align_yz", "Zy", icon='TRIA_UP_BAR')           
             row.operator("tp_ops.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

             row = box.column(1)
             row.operator("tp_ops.face_align_x", "X", icon='TRIA_RIGHT')
             row.operator("tp_ops.face_align_y", "Y", icon='TRIA_UP')           
             row.operator("tp_ops.face_align_z", "Z", icon='SPACE3')

             box.separator()  
           
             box = layout.box().column(1)               
            
             row = box.row(1)         
             row.operator("tp_ops.mirror1",text="MX", icon='ARROW_LEFTRIGHT')
             row.operator("tp_ops.mirror2",text="MY", icon='ARROW_LEFTRIGHT')
             row.operator("tp_ops.mirror3",text="MZ", icon='ARROW_LEFTRIGHT')            

             ###         
             box.separator()

             draw_normal_tools(context, layout)    



        if context.mode == 'EDIT_ARMATURE':    

             box = layout.box().row()
             row = box.column(1) 
             row.label("Align") 
             row.label("to") 
             row.label("Axis") 

             row = box.column(1)
             row.operator("tp_ops.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
             row.operator("tp_ops.face_align_yz", "Zy", icon='TRIA_UP_BAR')           
             row.operator("tp_ops.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

             row = box.column(1)
             row.operator("tp_ops.face_align_x", "X", icon='TRIA_RIGHT')
             row.operator("tp_ops.face_align_y", "Y", icon='TRIA_UP')           
             row.operator("tp_ops.face_align_z", "Z", icon='SPACE3')

             ###         
             box.separator()
            
             draw_normal_tools(context, layout)      
                    

        Display_History = context.user_preferences.addons[__package__].preferences.tab_history_menu
        if Display_History == 'on':

            box = layout.box().column(1)  
           
            row = box.row(1)
            row.scale_y = 0.85        
            row.operator("ed.undo", text=" ", icon="LOOP_BACK")
            row.operator("ed.redo", text=" ", icon="LOOP_FORWARDS") 
           
            box.separator()   
        

    def execute(self, context):
   
        return {'FINISHED'}

    def check(self, context):
        return True

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=300)





def register():

    bpy.utils.register_module(__name__)

def unregister():

    bpy.utils.unregister_module(__name__) 


if __name__ == "__main__":
    register()

   