import bpy, mathutils, math, re
from mathutils.geometry import intersect_line_plane
from mathutils import Vector
from math import radians
from bpy import*



### BoundingBox Main
class TP_Header_BBox (bpy.types.Operator):
    """create a bound boxes for selected object"""      
    bl_idname = "tp_header.bounding_box_main"
    bl_label = "BBox"
    bl_options = {'REGISTER', 'UNDO'}

                                 
    bbox_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)            
    bbox_wire = bpy.props.BoolProperty(name="Wire only", description="Delete Face", default= False) 
    bbox_origin = bpy.props.BoolProperty(name="Origin Center",  description="Origin to BBox-Center", default=False)  
    bbox_renderoff = bpy.props.BoolProperty(name="Render off",  description="Hide from Render", default=False)
    bbox_freeze = bpy.props.BoolProperty(name="Freeze Selection",  description="Hide from Selection", default=False)            
    bbox_apply = bpy.props.BoolProperty(name="Apply Scale & Rotation",  description="Apply Scale & Rotation", default=False)  
    bbox_clear = bpy.props.BoolProperty(name="Clear Scale & Rotation",  description="Clear Scale & Rotation", default=False)  

    
    def execute(self, context): 
        if bpy.context.selected_objects: 
            if context.space_data.local_view is not None:
                bpy.ops.view3d.localview()
                bpy.ops.tp_header.bounding_box_wire()  
                bpy.ops.object.select_pattern(pattern="_bbox_wire*", case_sensitive=False, extend=False)
                #bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
            else:            
                bpy.ops.tp_header.bounding_box_wire()  
                bpy.ops.object.select_pattern(pattern="_bbox_wire*", case_sensitive=False, extend=False)  
                #bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

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


            for i in range(self.bbox_freeze):
                bpy.context.object.hide_select = True
            
            for i in range(self.bbox_renderoff):
                bpy.context.object.hide_render = True

            for i in range(self.bbox_clear):
                bpy.ops.object.rotation_clear()
                bpy.ops.object.scale_clear()

            for i in range(self.bbox_apply):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            bpy.ops.view3d.rec_normals()

        bpy.ops.object.select_all(action='DESELECT')         
        return {'FINISHED'}                        

    def invoke(self, context, event):
        self.bbox_subdiv            
        self.bbox_wire
        self.bbox_origin
        self.bbox_renderoff
        self.bbox_freeze          
        self.bbox_apply
        self.bbox_clear 
        return context.window_manager.invoke_props_dialog(self, width = 300) 



### BoundingBox Source 
### snippet from nikitron (http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Object/Nikitron_tools)
class TP_Header_BBox_Wire (bpy.types.Operator):
    """Make bound boxes for selected objects"""      
    bl_idname = "tp_header.bounding_box_wire"
    bl_label = "Bounding Box Wire"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        i = 0
        for a in objects:
            self.make_it(i, a)
            i += 1                 
        return {'FINISHED'}

    def make_it(self, i, obj):
        box = bpy.context.selected_objects[i].bound_box
        mw = bpy.context.selected_objects[i].matrix_world
        name = ('_bbox_wire') 
        me = bpy.data.meshes.new(name) 
        ob = bpy.data.objects.new(name, me)
        
        ob.location = mw.translation
        ob.scale = mw.to_scale()
        ob.rotation_euler = mw.to_euler()
        ob.show_name = False
        bpy.context.scene.objects.link(ob)
        loc = []
        for ver in box:
            loc.append(mathutils.Vector((ver[0],ver[1],ver[2])))
        me.from_pydata((loc), [], ((0,1,2,3),(0,1,5,4),(4,5,6,7), (6,7,3,2),(0,3,7,4),(1,2,6,5)))
        me.update(calc_edges=True)
        return

    















