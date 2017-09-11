import bpy
from bpy import*
from bpy.props import  *


import mathutils, math, re
from mathutils.geometry import intersect_line_plane
from mathutils import Vector
from math import radians

bpy.types.Scene.align_vertices_axis = bpy.props.EnumProperty(items = [("x", "X", "", 1),("y", "Y", "", 2),("z", "Z", "", 3)], description="Axis")

class VIEW3D_TP_BBox_Align(bpy.types.Operator):
    """ BBox Quad to choosen Axis """
    bl_idname = "tp_ops.bbox_align_vertices"
    bl_label = "Quad Wire to choosen Axis"
    bl_options = {'REGISTER', 'UNDO'}       

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Created Quad Wire")               
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.tp_ops.bbox_extrude()
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.mode_set(mode = 'OBJECT')

        x1,y1,z1 = bpy.context.scene.cursor_location
        bpy.ops.view3d.snap_cursor_to_selected()

        x2,y2,z2 = bpy.context.scene.cursor_location

        bpy.context.scene.cursor_location[0],bpy.context.scene.cursor_location[1],bpy.context.scene.cursor_location[2]  = 0,0,0

        #Vertices coordinate to 0 (local coordinate, so on the origin)
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if bpy.context.scene.align_vertices_axis == 'x':
                    axis = 0
                elif bpy.context.scene.align_vertices_axis == 'y':
                    axis = 1
                elif bpy.context.scene.align_vertices_axis == 'z':
                    axis = 2
                vert.co[axis] = 0
        
        bpy.context.scene.cursor_location = x2,y2,z2

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        bpy.context.scene.cursor_location = x1,y1,z1

        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent()             
        bpy.ops.mesh.delete(type='ONLY_FACE')         
        bpy.ops.mesh.select_mode(type='VERT')                                                     
        bpy.ops.mesh.select_all(action='SELECT') 
        bpy.ops.mesh.remove_doubles(threshold=0.5) 
        
        bpy.context.object.name = "_cylbox"        
        bpy.ops.mesh.select_all(action='SELECT')         
        return {'FINISHED'}   


class VIEW3D_TP_BoundingBox_Extrude(bpy.types.Operator):
    """create a bound boxes for selected object"""      
    bl_idname = "tp_ops.bbox_extrude"
    bl_label = "BBox"
    bl_options = {'REGISTER', 'UNDO'}

                                 
    bbox_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)            
    bbox_wire = bpy.props.BoolProperty(name="Wire only", description="Delete Face", default= False) 
    bbox_origin = bpy.props.BoolProperty(name="Origin Center",  description="Origin to BBox-Center", default=False)  
    
    def execute(self, context): 
        if bpy.context.selected_objects: 
            if context.space_data.local_view is not None:
                bpy.ops.view3d.localview()
                bpy.ops.tp_ops.bounding_box_wire()  
                bpy.ops.object.select_pattern(pattern="_bwire*", case_sensitive=False, extend=False)
            
            else:            
                bpy.ops.tp_ops.bounding_box_wire()  
                bpy.ops.object.select_pattern(pattern="_bwire*", case_sensitive=False, extend=False)  

        else:
            bpy.ops.mesh.primitive_cube_add()            
            bpy.context.object.name = "_bbox"


        for obj in bpy.context.selected_objects:
                         
            bpy.context.scene.objects.active = obj                                                        
            bpy.ops.object.editmode_toggle()  
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent()                       
        

            for i in range(self.bbox_subdiv):
                bpy.ops.mesh.subdivide(number_cuts=1)

            for i in range(self.bbox_wire):
                bpy.ops.mesh.delete(type='ONLY_FACE')
           
            bpy.ops.object.editmode_toggle()

            for i in range(self.bbox_origin):
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')                              

            bpy.ops.tp_ops.rec_normals()

        return {'FINISHED'}                        

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)





class VIEW3D_TP_BBoxCircle_DIV(bpy.types.Operator):
    """BBox Circle SubDiv"""                 
    bl_idname = "tp_ops.circle_div"        
    bl_label = "CylDiv"                  
    bl_options = {'REGISTER', 'UNDO'} 
        
    circle_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)            

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "BBox Circle SubDiv") 
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        for i in range(self.circle_subdiv):
            bpy.ops.mesh.subdivide(number_cuts=0)
              
        bpy.ops.mesh.remove_doubles(threshold=0.5)              
        bpy.ops.mesh.looptools_circle(custom_radius=False, fit='best', flatten=True, influence=100, lock_x=False, lock_y=False, lock_z=False, radius=1, regular=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.view3d.snap_selected_to_cursor()
        bpy.ops.object.editmode_toggle()   
        return {'FINISHED'}    



class VIEW3D_TP_BBox_MirrorExtrudeX(bpy.types.Operator):
    """mirror extrude in x direction"""                 
    bl_idname = "tp_ops.mirror_extrude_x"        
    bl_label = "Mirror Extrude X"                  
    bl_options = {'REGISTER', 'UNDO'}  
        
          
    extrude_x = bpy.props.IntProperty(name="Extrude X", description="How long?", default=0, min=0, soft_max=1000, step=1)                              
    origin = bpy.props.BoolProperty(name="Set Back",  description="set back", default=True)         
    bevel = bpy.props.BoolProperty(name="Bevel 2mm",  description="set bevel", default=False) 
    smooth = bpy.props.BoolProperty(name="Smooth",  description="set smooth", default=False) 
    normals = bpy.props.BoolProperty(name="NormalsFlip",  description="flip normals", default=False) 

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Extrude Cylinder")
        bpy.ops.view3d.snap_cursor_to_selected()                 
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.edge_face_add()       
        bpy.ops.mesh.normals_make_consistent() 
        bpy.ops.mesh.extrude_region()

        for i in range(self.extrude_x):
            bpy.ops.transform.translate(value=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.origin):                        
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.view3d.snap_selected_to_cursor()
            bpy.ops.object.editmode_toggle()

        for i in range(self.bevel):                                   
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)            
            bpy.ops.mesh.select_all(action='INVERT')            
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)

        for i in range(self.smooth):   
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.faces_shade_smooth()

        for i in range(self.normals):   
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()

        return {'FINISHED'} 
    
    def invoke(self, context, event):             
        self.extrude_x        
        self.origin 
        self.bevel           
        self.smooth
        self.normals                
        return context.window_manager.invoke_props_popup(self, event) 


    
class VIEW3D_TP_BBox_MirrorExtrudeY(bpy.types.Operator):
    """mirror extrude in y direction"""                 
    bl_idname = "tp_ops.mirror_extrude_y"        
    bl_label = "Mirror Extrude Y"                  
    bl_options = {'REGISTER', 'UNDO'}  
                             
    extrude_y = bpy.props.IntProperty(name="Extrude Y", description="How long?", default=0, min=0, soft_max=1000, step=1)                        
    origin = bpy.props.BoolProperty(name="Set Back",  description="set back", default=True)         
    bevel = bpy.props.BoolProperty(name="Bevel 2mm",  description="set bevel", default=False) 
    smooth = bpy.props.BoolProperty(name="Smooth",  description="set smooth", default=False) 
    normals = bpy.props.BoolProperty(name="NormalsFlip",  description="flip normals", default=False) 

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Extrude Cylinder")
        bpy.ops.view3d.snap_cursor_to_selected()                 
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.edge_face_add()       
        bpy.ops.mesh.normals_make_consistent() 
        bpy.ops.mesh.extrude_region()

        for i in range(self.extrude_y):
            bpy.ops.transform.translate(value=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.origin):                        
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.view3d.snap_selected_to_cursor()
            bpy.ops.object.editmode_toggle()

        for i in range(self.bevel):                                   
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)            
            bpy.ops.mesh.select_all(action='INVERT')            
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)

        for i in range(self.smooth):   
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.faces_shade_smooth()

        for i in range(self.normals):   
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()

        return {'FINISHED'} 

    def invoke(self, context, event):             
        self.extrude_y      
        self.origin 
        self.bevel           
        self.smooth
        self.normals                
        return context.window_manager.invoke_props_popup(self, event) 


    
class VIEW3D_TP_BBox_MirrorExtrudeZ(bpy.types.Operator):
    """mirror extrude in z direction"""                 
    bl_idname = "tp_ops.mirror_extrude_z"        
    bl_label = "Mirror Extrude Z"                  
    bl_options = {'REGISTER', 'UNDO'}  
        
    extrude_z = bpy.props.IntProperty(name="Extrude Z", description="How long?", default=0, min=0, soft_max=1000, step=1)                
    origin = bpy.props.BoolProperty(name="Set Back",  description="set back", default=True)         
    bevel = bpy.props.BoolProperty(name="Bevel 2mm",  description="set bevel", default=False) 
    smooth = bpy.props.BoolProperty(name="Smooth",  description="set smooth", default=False) 
    normals = bpy.props.BoolProperty(name="NormalsFlip",  description="flip normals", default=False) 

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Extrude Cylinder")
        bpy.ops.view3d.snap_cursor_to_selected()                 
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.edge_face_add()       
        bpy.ops.mesh.normals_make_consistent() 
        bpy.ops.mesh.extrude_region()
        
        for i in range(self.extrude_z):
            bpy.ops.transform.translate(value=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.origin):                        
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.view3d.snap_selected_to_cursor()
            bpy.ops.object.editmode_toggle()

        for i in range(self.bevel):                                   
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)            
            bpy.ops.mesh.select_all(action='INVERT')            
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)

        for i in range(self.smooth):   
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.faces_shade_smooth()

        for i in range(self.normals):   
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()

        return {'FINISHED'} 

    def invoke(self, context, event):             
        self.extrude_z       
        self.origin 
        self.bevel           
        self.smooth
        self.normals                
        return context.window_manager.invoke_props_popup(self, event) 

    


class VIEW3D_TP_BBox_MirrorExtrudeN(bpy.types.Operator):
    """mirror extrude in normal direction"""                 
    bl_idname = "tp_ops.mirror_extrude_n"        
    bl_label = "Mirror Extrude N"                  
    bl_options = {'REGISTER', 'UNDO'}  
        
    extrude_n = bpy.props.IntProperty(name="Extrude Normal", description="How long?", default=0, min=0, soft_max=1000, step=1)                  
    origin = bpy.props.BoolProperty(name="Set Back",  description="set back", default=True)         
    bevel = bpy.props.BoolProperty(name="Bevel 2mm",  description="set bevel", default=False) 
    smooth = bpy.props.BoolProperty(name="Smooth",  description="set smooth", default=False) 
    normals = bpy.props.BoolProperty(name="NormalsFlip",  description="flip normals", default=False) 

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Extrude Cylinder")
        bpy.ops.view3d.snap_cursor_to_selected()                 
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.edge_face_add()       
        bpy.ops.mesh.normals_make_consistent() 
        bpy.ops.mesh.extrude_region()

        for i in range(self.extrude_n):
            bpy.ops.transform.translate(value=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.origin):                        
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.view3d.snap_selected_to_cursor()
            bpy.ops.object.editmode_toggle()

        for i in range(self.bevel):                                   
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)            
            bpy.ops.mesh.select_all(action='INVERT')            
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)

        for i in range(self.smooth):   
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.faces_shade_smooth()

        for i in range(self.normals):   
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()

        return {'FINISHED'} 
    
    def invoke(self, context, event):             
        self.extrude_n        
        self.origin 
        self.bevel           
        self.smooth
        self.normals                
        return context.window_manager.invoke_props_popup(self, event) 



def register():
    bpy.utils.register_module(__name__) 
    
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()























