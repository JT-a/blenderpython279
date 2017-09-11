import bpy
from bpy import *


class TP_Display_Snap_VOLUME(bpy.types.Operator):
    """Snap Element VOLUME"""
    bl_idname = "tp_display.snap_volume"
    bl_label = "Snap Element VOLUME"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VOLUME'
        return {'FINISHED'}


class TP_Display_Snap_FACE(bpy.types.Operator):
    """Snap Element FACE"""
    bl_idname = "tp_display.snap_face"
    bl_label = "Snap Element FACE"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'FACE'
        return {'FINISHED'}


class TP_Display_Snap_EDGE(bpy.types.Operator):
    """Snap Element EDGE"""
    bl_idname = "tp_display.snap_edge"
    bl_label = "Snap Element EDGE"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'EDGE'
        return {'FINISHED'}


class TP_Display_Snap_VERTEX(bpy.types.Operator):
    """Snap Element VERTEX"""
    bl_idname = "tp_display.snap_vertex"
    bl_label = "Snap Element VERTEX"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        return {'FINISHED'} 
    

class TP_Display_Snap_INCREMENT(bpy.types.Operator):
    """Snap Element INCREMENT"""
    bl_idname = "tp_display.snap_increment"
    bl_label = "Snap Element INCREMENT"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'INCREMENT'
        return {'FINISHED'}



class TP_Display_Snap_Element_Menu(bpy.types.Menu):
    bl_label = "Snap Element"
    bl_idname = "tp_display.menu_snap_element"
    
    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
               
        layout.operator("tp_display.snap_volume", text="Volume")       
        layout.operator("tp_display.snap_face", text="Face")       
        layout.operator("tp_display.snap_edge", text="Edge")       
        layout.operator("tp_display.snap_vertex", text="Vertex")       
        layout.operator("tp_display.snap_increment", text="Grid")       

            
bpy.utils.register_class(TP_Display_Snap_Element_Menu)



def register():
    
    bpy.utils.register_module(__name__)        
    
    
def unregister():
    
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register() 	



