import bpy
from bpy import*
from bpy.props import *
#from . icons.icons import load_icons


class View3D_TP_Tileable_Camera_Panel(bpy.types.Panel):
    bl_label = "Camera"
    bl_idname = "View3D_TP_Tileable_Camera_Panel"
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
        row.label(text="Camera", icon = "CAMERA_DATA")     

        box.separator()        

        row = box.column(1)                    
        row.operator("tp_ops.tileable_camera", text="add camera & sun light")
       
        box.separator()
        
        row = box.row(1)
        row.operator("view3d.viewnumpad","Camera View", icon = "RENDER_REGION").type='CAMERA' 
        
        if bpy.context.space_data.lock_camera == False:
            row.prop(context.space_data, "lock_camera", text="", icon = "UNLOCKED")                         
        else:
            row.prop(context.space_data, "lock_camera", text="", icon = "LOCKED")                         

        box.separator() 


        box.separator()

        obj = context.active_object
        if obj:
            obj_type = obj.type
            
            
            if obj.type in {'CAMERA'}:    
                
                box = layout.box().column(1) 

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

 
            else:
                row = box.column(1)
                row.label("no camera selected", icon = "INFO") 

