import bpy
from bpy import *


class TP_Display_Origin_Objectmode(bpy.types.Operator):
    """set origin to selected / stay in objectmode"""                 
    bl_idname = "tp_display.origin_obm"          
    bl_label = "origin to selected / in objectmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

class TP_Display_Origin_Editmode(bpy.types.Operator):
    """set origin to selected / stay in editmode"""                 
    bl_idname = "tp_display.origin_edm"          
    bl_label = "origin to selected in editmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class TP_Display_Origin_Bottom(bpy.types.Operator):  
    bl_idname = "tp_display.pivo_to_bottom"  
    bl_label = "Origin To Bottom"  
  
    def execute(self, context):
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        o=bpy.context.active_object
        init=0
        for x in o.data.vertices:
             if init==0:
                 a=x.co.z
                 init=1
             elif x.co.z<a:
                 a=x.co.z
                 
        for x in o.data.vertices:
             x.co.z-=a

        o.location.z+=a 
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

                        

def register():
    
    bpy.utils.register_module(__name__)        
    
    
def unregister():
    
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register() 	



