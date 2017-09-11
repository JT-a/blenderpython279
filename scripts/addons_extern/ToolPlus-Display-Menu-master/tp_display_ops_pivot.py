import bpy
from bpy import *


class TP_Display_Pivot_Box(bpy.types.Operator):
   """Set pivot point to Bounding Box"""
   bl_label = "Set pivot point to Bounding Box"
   bl_idname = "tp_display.pivot_bounding_box"
   bl_options = {'REGISTER', 'UNDO'}
    
   def execute(self, context):
       bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
       return {"FINISHED"} 


class TP_Display_Pivot_Cursor(bpy.types.Operator):
   """Set pivot point to 3D Cursor"""
   bl_label = "Set pivot point to 3D Cursor"
   bl_idname = "tp_display.pivot_3d_cursor"
   bl_options = {'REGISTER', 'UNDO'}
    
   def execute(self, context):
       bpy.context.space_data.pivot_point = 'CURSOR'
       return {"FINISHED"} 



class TP_Display_Pivot_Median(bpy.types.Operator):
    """Set pivot point to Median Point"""
    bl_label = "Set pivot point to Median Point"
    bl_idname = "tp_display.pivot_median"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
        return {"FINISHED"}


class TP_Display_Pivot_Active(bpy.types.Operator):
   """Set pivot point to Active"""
   bl_label = "Set pivot point to Active"
   bl_idname = "tp_display.pivot_active"
   bl_options = {'REGISTER', 'UNDO'}
    
   def execute(self, context):
       bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
       return {"FINISHED"} 


class TP_Display_Pivot_Individual(bpy.types.Operator):
    """Set pivot point to Individual"""
    bl_label = "Set pivot point to Individual Point"
    bl_idname = "tp_display.pivot_individual"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        return {"FINISHED"}
        


class TP_Display_Pivot_Menu(bpy.types.Menu):
    bl_label = "Pivot"
    bl_idname = "tp_display.menu_pivot"
    
    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
         
        layout.operator("tp_display.pivot_bounding_box", text="BoundBox")       
        layout.operator("tp_display.pivot_3d_cursor", text="3d Cursor")       
        layout.operator("tp_display.pivot_median", text="Median")       
        layout.operator("tp_display.pivot_active", text="Active")       
        layout.operator("tp_display.pivot_individual", text="Individual")       

            
bpy.utils.register_class(TP_Display_Pivot_Menu)



                       
def register():
    
    bpy.utils.register_module(__name__)        
    
    
def unregister():
    
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register() 	



