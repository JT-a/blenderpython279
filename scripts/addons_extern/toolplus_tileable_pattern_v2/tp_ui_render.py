import bpy
from bpy import*
from bpy.props import *
#from . icons.icons import load_icons


class Dropdown_TP_Render_Props(bpy.types.PropertyGroup):

    ### Render
    display_object_color = bpy.props.BoolProperty(name="Open", description="Open", default=False)     


class View3D_TP_Tileable_Render_Panel(bpy.types.Panel):
    """"""
    bl_label = "Render"
    bl_idname = "OBJECT_TP_Tileable_Render"
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
        
        lt = context.window_manager.tp_collapse_render_props
        
        box = layout.box().column(1)

        row = box.row(1)          
        row.label(text="Camera", icon = "CAMERA_DATA")     

        box.separator()        

        row = box.column(1)                    
        row.operator("tp_ops.tileable_camera", text="add camera & sun light")
      
        box.separator()        

        box = layout.box().column(1)   

        #icons = load_icons()
        #CST = icons.get("CST")
        #row.label("Animation Render", icon_value=CST.icon_id)

        row = box.row(1)              
        row.alignment = 'CENTER'
        row.label("Image Rendering", icon='RENDER_STILL')     
        
        box.separator()

        row = box.row(1)               
        row.prop(context.scene, "Render_Setup", text="Render Resolution", expand=True)
        
        row = box.row(1) 
        row.operator("tp_ops.instances_res_apply", text="> apply render resolution")

        box.separator()

        row = box.row(1)               
        row.scale_y = 3
        row.operator("render.render", text="Render#")

        row.operator("render.opengl", text="OpenGL#")

        row = box.row(1)
        row.prop(context.scene.render, "display_mode", text="")                                                                 
        row.menu("INFO_MT_opengl_render", "OpenGl Opt.")              
        
        box.separator()
        box.separator()


        row = box.row(1)
        if lt.display_object_color:                       
             row.prop(lt, "display_object_color", text="Color", icon='SEQ_CHROMA_SCOPE')                             
        else:            
             row.prop(lt, "display_object_color", text="Color", icon='SEQ_CHROMA_SCOPE')

        box.separator()


        # Color Managment
        if lt.display_object_color:

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
            row.label(text="Render...", icon='DISCLOSURE_TRI_RIGHT_VEC')

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
            
    