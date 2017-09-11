import bpy
from bpy import *


class TP_Display_Snap_ACTIVE(bpy.types.Operator):
    """Snap Target ACTIVE"""
    bl_idname = "tp_display.snap_active"
    bl_label = "Snap Target ACTIVE"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        return {'FINISHED'}
    

class TP_Display_Snap_MEDIAN(bpy.types.Operator):
    """Snap Target MEDIAN"""
    bl_idname = "tp_display.snap_median"
    bl_label = "Snap Target MEDIAN"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'MEDIAN'
        return {'FINISHED'}


class TP_Display_Snap_CENTER(bpy.types.Operator):
    """Snap Target CENTER"""
    bl_idname = "tp_display.snap_center"
    bl_label = "Snap Target CENTER"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'CENTER'
        return {'FINISHED'}


class TP_Display_Snap_CLOSEST(bpy.types.Operator):
    """Snap Target CLOSEST"""
    bl_idname = "tp_display.snap_closest"
    bl_label = "Snap Target CLOSEST"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        return {'FINISHED'}



class TP_Display_Snap_Menu(bpy.types.Menu):
    bl_label = "Snap"
    bl_idname = "tp_display.menu_snap"
    
    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
               
        layout.operator("tp_display.snap_active", text="Active")       
        layout.operator("tp_display.snap_median", text="Median")       
        layout.operator("tp_display.snap_center", text="Center")       
        layout.operator("tp_display.snap_closest", text="Closet")       

            
bpy.utils.register_class(TP_Display_Snap_Menu)

                      
def register():
    
    bpy.utils.register_module(__name__)        
    
    
def unregister():
    
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register() 	



