import bpy
from bpy import*
from bpy.props import *
#from . icons.icons import load_icons


class View3D_TP_Tileable_Lights_Panel(bpy.types.Panel):
    bl_label = "Lights"
    bl_idname = "View3D_TP_Tileable_Lights_Panel"
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

        box = layout.box().column(1)

        row = box.row(1)          
        row.label(text="Lights", icon = "LAMP_SUN")     

        box.separator()
        
        row = box.row(1)
        row.alignment = "CENTER"          
        row.operator("object.lamp_add", text="", icon="LAMP_POINT").type='POINT'
        row.operator("object.lamp_add", text="", icon="LAMP_SUN").type='SUN'
        row.operator("object.lamp_add", text="", icon="LAMP_SPOT").type='SPOT'
        row.operator("object.lamp_add", text="", icon="LAMP_HEMI").type='HEMI'
        row.operator("object.lamp_add", text="", icon="LAMP_AREA").type='AREA'   

        box.separator()
        box.separator()

        obj = context.active_object
        if obj:
            obj_type = obj.type
                        
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
      


            else:
                row = box.column(1)
                row.label("no light select!", icon = "INFO") 

