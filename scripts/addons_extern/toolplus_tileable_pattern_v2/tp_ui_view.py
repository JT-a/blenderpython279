import bpy
from bpy import*
from bpy.props import *
#from . icons.icons import load_icons


class View3D_TP_Tileable_Display_Panel(bpy.types.Panel):
    """"""
    bl_label = "Display"
    bl_idname = "View3D_TP_Tileable_Display_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' 
    bl_category = "T+"
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):
        layout = self.layout.column_flow(1)
        layout.operator_context = 'INVOKE_DEFAULT'

        #icons = load_icons()
        #CST = icons.get("CST")
        #row.label("Animation Render", icon_value=CST.icon_id)

        box = layout.box().column(1)             

        row = box.row(1)              
        row.alignment = 'CENTER'
        row.label("OpenGL", icon='LAMP_SPOT')  

        box.separator()                

        row = box.row(1)
        row.prop(context.space_data, "show_textured_solid","Enable Textured Solid", icon = "TEXTURE_SHADED")        
          
        row = box.row(1)  
        row.menu("VIEW3D_MT_opengl_lights_presets", text=bpy.types.VIEW3D_MT_opengl_lights_presets.bl_label, icon = "COLLAPSEMENU")
        row.operator("scene.opengl_lights_preset_add", text="", icon='ZOOMIN')
        row.operator("scene.opengl_lights_preset_add", text="", icon='ZOOMOUT').remove_active = True

        box.separator()              
                     
        system = bpy.context.user_preferences.system
        
        def opengl_lamp_buttons(column, lamp):
           
            split = column.split(percentage=0.1)
            split.prop(lamp, "use", text="", icon='OUTLINER_OB_LAMP' if lamp.use else 'LAMP_DATA')
            
            col = split.column()
            col.active = lamp.use
            
            row = col.row()
            row.label(text="Diffuse:")
            row.prop(lamp, "diffuse_color", text="")
            
            row = col.row()
            row.label(text="Specular:")
            row.prop(lamp, "specular_color", text="")
            
            col = split.column()           
            col.active = lamp.use
            col.prop(lamp, "direction", text="")
        
        row = box.row(1) 
        p = context.scene.opengl_lights_properties
        row.prop(p, "edit", "Edit OpenGL Light", icon = "LIGHTPAINT")
        
        if(p.edit):
            box.separator()   
            
            box = layout.box().column(1)  
            
            column = box.column()
            
            split = column.split(percentage=0.1)
            split.label()
            split.label(text="Colors:")
            split.label(text="Direction:")
            
            lamp = system.solid_lights[0]
            opengl_lamp_buttons(column, lamp)
            
            lamp = system.solid_lights[1]
            opengl_lamp_buttons(column, lamp)
            
            lamp = system.solid_lights[2]
            opengl_lamp_buttons(column, lamp)

        ###
        box.separator()  
        
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator_context = 'INVOKE_AREA'
        
        box = layout.box().column(1)             

        row = box.row(1)              
        row.alignment = 'CENTER'
        row.label("3D View", icon='LAMP_DATA')  

        box.separator()                     

        row = box.row(1)
        row.prop(context.space_data, "use_matcap", icon ="MATCAP_06")

        if context.space_data.use_matcap:

            box.separator()    

            row = box.row(1)
            row.scale_y = 0.2
            row.scale_x = 0.5
            row.template_icon_view(context.space_data, "matcap_icon") 

            box.separator()              
             
        row = box.row(1)
        row.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="MATCAP_24")

        if context.space_data.fx_settings.use_ssao:
          
            box.separator()   

            row = box.row(1)
            row.prop(context.space_data.fx_settings.ssao, "color","")
            row.prop(context.space_data.fx_settings.ssao, "factor")
            
            row = box.row(1)
            row.prop(context.space_data.fx_settings.ssao, "distance_max")
            row.prop(context.space_data.fx_settings.ssao, "attenuation")
            row.prop(context.space_data.fx_settings.ssao, "samples")

        ###
        box.separator()   
            
        box = layout.box().column(1)  
 
        row = box.row(1)
        row.prop(context.space_data, "show_only_render", text="Render", icon ="RESTRICT_RENDER_ON")
        row.prop(context.space_data, "show_floor", text="Grid", icon ="GRID")     
        
        row = box.row(1)
        row.prop(context.space_data, "show_world", "World" ,icon ="WORLD")
        
        sub = row.row(1)
        sub.scale_x = 0.335
        sub.prop(context.space_data, "show_axis_x", text="X", toggle=True)
        sub.prop(context.space_data, "show_axis_y", text="Y", toggle=True)
        sub.prop(context.space_data, "show_axis_z", text="Z", toggle=True)

        if context.space_data.show_world:

            box.separator()   

            row = box.row(1)
            row.prop(context.scene.world, "horizon_color", "")
            
            row = box.row(1)
            row.prop(context.scene.world, "exposure")
            row.prop(context.scene.world, "color_range")

        ###
        box.separator()  


