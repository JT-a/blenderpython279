__status__ = "toolplus custom version"
__author__ = "mkbreuer"
__version__ = "1.0"
__date__ = "2016"


import bpy
from bpy import *
from bpy.props import *


class View3D_TP_BoundingBox(bpy.types.Operator):
    """BBox to selected objects / Attention: set origin to geometry"""      
    bl_idname = "tp_ops.bounding_box_simple"
    bl_label = "BBox"
    bl_options = {'REGISTER', 'UNDO'}
                                 
    bbox_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)            
    bbox_wire = bpy.props.BoolProperty(name="Wire only", description="Delete Face", default= False) 

    def execute(self, context): 
        selected = bpy.context.selected_objects

        if context.space_data.local_view is not None:                                
            bpy.ops.view3d.localview() 
        else:
            pass          

        for obj in selected: 

            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            #set cursor to selected
            bpy.ops.view3d.snap_cursor_to_selected() 

            #create a default cube
            bpy.ops.mesh.primitive_cube_add()
            bpy.context.object.name = "BBox" 
                                        
            for i in range(self.bbox_subdiv):                   
                bpy.ops.object.editmode_toggle()                      
                bpy.ops.mesh.select_all(action='SELECT')                                            
                bpy.ops.mesh.subdivide(number_cuts=1)
                bpy.ops.mesh.normals_make_consistent() 
                bpy.ops.object.editmode_toggle()
                 
            for i in range(self.bbox_wire):                
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.delete(type='ONLY_FACE')
                bpy.ops.object.editmode_toggle()                       
                
            #keep it as active object
            bound_box = bpy.context.active_object 
            
            #copy dimensions to it
            bound_box.dimensions = obj.dimensions
            bound_box.location = obj.location
            bound_box.rotation_euler = obj.rotation_euler
            
            bpy.ops.object.select_all(action='DESELECT')

            bpy.data.objects["BBox"].select=True 
   
        return {'FINISHED'}                        

    def invoke(self, context, event):
        self.bbox_subdiv            
        self.bbox_wire
        return context.window_manager.invoke_props_dialog(self, width = 300) 



def register():

    bpy.utils.register_module(__name__)

    
def unregister():

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()



















