import bpy
from bpy import*
from bpy.props import *
#from . icons.icons import load_icons



class View3D_TP_Tileable_Copy_Panel(bpy.types.Panel):
    """"""
    bl_label = "Copy"
    bl_idname = "OBJECT_TP_Copy_Pattern"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' 
    bl_category = "T+"
    bl_context = "objectmode"
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
                    
            box = layout.box().column(1)

            row = box.row(1)          
            row.label(text="Copy", icon = "MOD_ARRAY")      

            box.separator()
            
            row = box.row(1) 
            row.operator("tp_ops.copy_to_selected_faces", text="Copy to Faces",icon="UV_FACESEL") 
            
            box.separator()  
             
            row = box.row(1)            
            row.operator("curve_mft.radialclone", text="", icon="FILE_REFRESH")
            row.operator("curve_mft.radialclone_panel", text="Radial Z-Axis Clone", icon="BLANK1")
 
            row = box.row(1) 
            row.prop(context.scene, "radialClonesAngle", text="")
            row.prop(context.scene, "clonez", text="")
          
            box.separator() 
            box.separator() 

            row = box.row(1)  
            row.operator("tp_ops.copy_to_cursor", text="", icon="NEXT_KEYFRAME")                     
            row.operator("tp_ops.copy_to_cursor_panel", text="Copy to Cursor", icon="BLANK1")                     
            
            row = box.row(1)  
            row.prop(context.scene, "ctc_total", text="How many?")
                        
            box.separator()                    
            box.separator()                    
  
            row = box.row(1) 
            row.operator("object.make_links_data",text="link", icon="LINKED").type='OBDATA'
            row.operator("tp_ops.make_single",text="unlink", icon="UNLINKED")
            row.operator("object.join", icon = "AUTOMERGE_ON")                   
           
            box.separator()   
