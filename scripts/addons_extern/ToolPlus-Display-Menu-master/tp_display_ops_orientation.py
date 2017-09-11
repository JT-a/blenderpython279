import bpy
from bpy import *



class TP_Display_Space_Global(bpy.types.Operator):
    """Transform Orientation Global"""
    bl_idname = "tp_display.orient_global"
    bl_label = "Transform Orientation Global"
    bl_options = {'REGISTER'}

    def execute(self, context):

        bpy.context.space_data.transform_orientation = 'GLOBAL'
        return {'FINISHED'}
      

class TP_Display_Space_LOCAL(bpy.types.Operator):
    """Transform Orientation LOCAL"""
    bl_idname = "tp_display.orient_local"
    bl_label = "Transform Orientation LOCAL"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'LOCAL'
        return {'FINISHED'}


class TP_Display_Space_NORMAL(bpy.types.Operator):
    """Transform Orientation NORMAL"""
    bl_idname = "tp_display.orient_normal"
    bl_label = "Transform Orientation NORMAL"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'NORMAL'
        return {'FINISHED'}


class TP_Display_Space_GIMBAL(bpy.types.Operator):
    """Transform Orientation GIMBAL"""
    bl_idname = "tp_display.orient_gimbal"
    bl_label = "Transform Orientation GIMBAL"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'GIMBAL'
        return {'FINISHED'}


class TP_Display_Space_VIEW(bpy.types.Operator):
    """Transform Orientation VIEW"""
    bl_idname = "tp_display.orient_view"
    bl_label = "Transform Orientation VIEW"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.transform_orientation = 'VIEW'
        return {'FINISHED'}




class TP_Display_Orientation_Menu(bpy.types.Menu):
    bl_label = "Orientation"
    bl_idname = "tp_display.menu_orient"
    
    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
         
        layout.operator("tp_display.orient_global", text="Global")       
        layout.operator("tp_display.orient_local", text="Local")       
        layout.operator("tp_display.orient_normal", text="Normal")       
        layout.operator("tp_display.orient_gimbal", text="Gimbal")       
        layout.operator("tp_display.orient_view", text="View")       

            
bpy.utils.register_class(TP_Display_Orientation_Menu)

        
                       
def register():
    
    bpy.utils.register_module(__name__)        
    
    
def unregister():
    
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register() 	



