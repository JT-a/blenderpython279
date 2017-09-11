import bpy
from bpy import *


class TP_Align_X_Axis(bpy.types.Operator):
    """align selected face > x"""
    bl_label = "Align X Axis"
    bl_idname = "tp_display.align_x_axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"} 


class TP_Align_Y_Axis(bpy.types.Operator):
    """align selected face to Y axis"""
    bl_label = "Align Y Axis"
    bl_idname = "tp_display.align_y_axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.transform.resize(value=(1, 0, 1), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}



class TP_Align_Z_Axis(bpy.types.Operator):
    """align selected face to Z axis"""
    bl_label = "Align Z Axis"
    bl_idname = "tp_display.align_z_axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"} 
                      


def register():
    
    bpy.utils.register_module(__name__)        
    
    
def unregister():
    
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register() 	



