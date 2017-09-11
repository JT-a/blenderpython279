bl_info = {
    "name": "Auto Refresha",
    "author": "RossenX",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "UV/Image > Side Panel",
    "description": "Refreshes Image when you hover your mouse over Blender, Click Start to start, Left/Right Click inside Blender to Stop",
    "warning": "",
    "wiki_url": "",
    "category": "UV",
    }


import bpy

class HelloWorld(bpy.types.Panel):
    """Creates a Panel in the Image Editor properties region"""
    bl_label = "Auto Refresha"
    bl_idname = "OBJECT_PT_AutoRefresha"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.startrefresh", text="Start")
   
class OBJECT_OT_startrefresh(bpy.types.Operator):
    bl_label = "Auto Refresh"
    bl_idname = "object.startrefresh"
    bl_description = "Refreshes Image when you hover your mouse over Blender, Click Start to start, Left/Right Click inside Blender to Stop"
    
    def modal(self, context, event):
        bpy.ops.image.reload()
        if event.type in {'RIGHTMOUSE', 'ESC','LEFTMOUSE', 'MIDDLEMOUSE'}:
            return {'FINISHED'}
        return {'RUNNING_MODAL'}
    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
