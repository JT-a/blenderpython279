import bpy
from bpy import *



class TP_Display_Mirror_Global_X_Axis(bpy.types.Operator):
    """Mirror over X axis / global"""                 
    bl_idname = "tp_display.mirror_global_x"          
    bl_label = "mirror X axis"                  
    bl_options = {'REGISTER', 'UNDO'}   
       
    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.transform.mirror(constraint_axis=(True, False, False), constraint_orientation='GLOBAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
       
        return {'FINISHED'}


class TP_Display_Mirror_Global_Y_Axis(bpy.types.Operator):
    """Mirror over Y axis / global"""                
    bl_idname = "tp_display.mirror_global_y"         
    bl_label = "mirror Y axis"                 
    bl_options = {'REGISTER', 'UNDO'}   
        
    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.transform.mirror(constraint_axis=(False, True, False), constraint_orientation='GLOBAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {'FINISHED'}


class TP_Display_Mirror_Global_Z_Axis(bpy.types.Operator):
    """Mirror over Z axis / global"""                 
    bl_idname = "tp_display.mirror_global_z"        
    bl_label = "mirror Z axis"                  
    bl_options = {'REGISTER', 'UNDO'}   
      
    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.transform.mirror(constraint_axis=(False, False, True), constraint_orientation='GLOBAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        return {'FINISHED'}
 

class TP_Display_Mirror_Local_X_Axis(bpy.types.Operator):
    """Mirror over X axis / local"""                 
    bl_idname = "tp_display.mirror_local_x"          
    bl_label = "mirror X axis > local"                  
    bl_options = {'REGISTER', 'UNDO'}   
        
    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(True, False, False), constraint_orientation='LOCAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}


class TP_Display_Mirror_Local_YAxis(bpy.types.Operator):
    """Mirror over Y axis / local"""                
    bl_idname = "tp_display.mirror_local_y"         
    bl_label = "mirror Y axis > local"                 
    bl_options = {'REGISTER', 'UNDO'}   
      
    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(False, True, False), constraint_orientation='LOCAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}
    


class TP_Display_Mirror_Local_Z_Axis(bpy.types.Operator):
    """Mirror over Z axis / local"""                 
    bl_idname = "tp_display.mirror_local_z"        
    bl_label = "mirror Z axis > local"                  
    bl_options = {'REGISTER', 'UNDO'}   
        
    def execute(self, context):

        bpy.ops.transform.mirror(constraint_axis=(False, False, True), constraint_orientation='LOCAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)        
        return {'FINISHED'}
                         


def register():
    
    bpy.utils.register_module(__name__)        
    
    
def unregister():
    
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register() 	



