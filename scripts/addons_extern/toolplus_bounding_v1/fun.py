import bpy
from bpy import *
from bpy.props import *
from .icons.icons import load_icons

EDIT = ["EDIT_CURVE", "EDIT_SURFACE", "EDIT_LATTICE", "EDIT_METABALL", "EDIT_TEXT", "EDIT_ARMATURE", "POSE"]
GEOM = ['POSE', 'LAMP', 'CAMERA', 'EMPTY', 'SPEAKER']

class VIEW3D_TP_Experimental_TOOLS(bpy.types.Panel):
    bl_category = "T+"
    bl_idname = "VIEW3D_TP_Experimental_TOOLS"
    bl_label = "Bound Extrude"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        obj = context.active_object     
        if obj:
            obj_type = obj.type                                                                
            if obj_type not in GEOM:
                return isModelingMode and context.mode not in EDIT
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_experimental_panel_layout(context, layout) 



class VIEW3D_TP_Experimental_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Experimental_UI"
    bl_label = "Bound Extrude"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        obj = context.active_object     
        if obj:
            obj_type = obj.type                                                                
            if obj_type not in GEOM:
                return isModelingMode and context.mode not in EDIT

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_experimental_panel_layout(context, layout) 






def draw_experimental_panel_layout(context, layout):

    
    icons = load_icons()     
    
    layout.operator_context = 'INVOKE_REGION_WIN'
    
    icons = load_icons()
   

    col = layout.column(1)                                                
    box = col.box().column(1)


    if context.mode == 'OBJECT': 
        
        row = box.row(1)           
        row.prop(context.scene, "align_vertices_axis", text="Align Axis", expand=True)
       
        row = box.column(1)  
        row.operator("tp_ops.bbox_align_vertices", text="Create WireMesh", icon ="CLIPUV_DEHLT")                  
        #row.operator("tp_ops.rec_normals", text="Fix Normals", icon="SNAP_NORMAL")             
        
        box.separator()



    if context.mode == "EDIT_MESH":  

        row = box.row(1)
        row.operator("tp_ops.circle_div", text="EvenDiv")
        row.operator("mesh.subdivide",text="< OddDiv").number_cuts=1

        row = box.row(1)                          
        row.operator("tp_ops.mirror_extrude_x","X")               
        row.operator("tp_ops.mirror_extrude_y","Y")               
        row.operator("tp_ops.mirror_extrude_z","Z")               
        row.operator("tp_ops.mirror_extrude_n","N")                

        box = col.box().column(1)
        
        row = box.row(1)            
        row.operator("mesh.flip_normals", text="", icon="FILE_REFRESH")
        row.operator("mesh.normals_make_consistent", text="Fix Normals", icon="SNAP_NORMAL")
        
        box.separator()


    display_history = context.user_preferences.addons[__package__].preferences.tab_display_history 
    if display_history == 'on':
        
        box = col.box().column(1)

        row = box.row(1)        
        row.operator("view3d.ruler", text="Ruler")   
         
        row.operator("ed.undo_history", text="History")
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
       
        box.separator()               
        