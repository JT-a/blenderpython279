import bpy
from bpy import*
from bpy.props import *
#from . icons.icons import load_icons



class View3D_TP_Tileable_Color_Panel(bpy.types.Panel):
    bl_label = "Color"
    bl_idname = "OBJECT_TP_Color_Pattern"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = "T+"
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.column_flow(1)
        layout.operator_context = 'INVOKE_DEFAULT'

        #icons = load_icons()
        #CST = icons.get("CST")
        #row.label("Animation Render", icon_value=CST.icon_id)
        
        box = layout.box().column(1)   

        row = box.row(1)           
        row.alignment = 'CENTER'
        row.label("Color Managment", icon='SEQ_CHROMA_SCOPE')    

        box.separator()  
        
        row = box.row(1)  
        row.label(text="Display:")

        row = box.row(1)          
        row.prop( context.scene.display_settings, "display_device", text="")     
        
        box.separator()  

        row = box.row(1)                             
        row.label(text="Render...", icon='DISCLOSURE_TRI_RIGHT')

        row = box.column(1)                 
        row.template_colormanaged_view_settings(context.scene, "view_settings")
     
        box.separator()  
       
        row = box.row(1)                 
        row.prop(context.scene.cycles, "filter_type", text="")
        row.prop(context.scene.cycles, "film_transparent")

        row = box.row(1) 
        if context.scene.cycles.filter_type != 'BOX':
            row.prop(context.scene.cycles, "filter_width", text="Width")
        row.label("")                 
       
        box.separator() 

        row = box.row(1)                              
        row.label(text="Sequencer / Color Space...", icon='DISCLOSURE_TRI_RIGHT_VEC')

        row = box.row(1)                   
        row.prop(context.scene.sequencer_colorspace_settings, "name", "")

        box.separator()
        
