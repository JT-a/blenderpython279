import bpy
from bpy import*
from bpy.props import *




class TP_Tileable_Pattern_Help(bpy.types.Operator):
    bl_idname = 'tp_ops.tileable_help'
    bl_label = ''
    bl_options = {'REGISTER', 'UNDO'}  

    def draw(self, context):
        layout = self.layout
        layout.label("Please respect the order of use:", icon = "TRIA_DOWN") 
        layout.label("1. Add Planes > fill geometry only to the middle one", icon = "LAYER_USED") 
        layout.label("2. Don´t rewrite the cutout and instance objects", icon = "LAYER_USED") 
        layout.label("3. Join Instances > select only the middle square", icon = "LAYER_USED") 
        layout.label("4. Optimize Join > Recalculate Normals, Remove Doubles, etc.", icon = "LAYER_USED") 
        layout.label("5. 2d Cutout > XY > flat and non-overlapping welded geometry", icon = "LAYER_USED") 
        layout.label("6. 3d Cutout > XYZ > extruded overlapping geometry", icon = "LAYER_USED") 
        layout.label("7. Add XY Arrays > clear location and adds two arrays on it", icon = "LAYER_USED") 
        layout.label("8. Camera Setup > use when arrays added", icon = "LAYER_USED") 
        layout.label("9. Have Fun!!! ;)", icon = "LAYER_USED") 
    
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width = 350)
    
    
def register():

    bpy.utils.register_class(TP_Tileable_Pattern_Help)


def unregister():

    bpy.utils.unregister_class(TP_Tileable_Pattern_Help)

if __name__ == "__main__":
    register()

