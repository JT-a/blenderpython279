import bpy, mathutils, math, re
from mathutils.geometry import intersect_line_plane
from mathutils import Vector
from math import radians
from bpy import*


class VIEW3D_TP_BBox_for_Panel(bpy.types.Operator):
    """create bounding boxes for selected objects"""      
    bl_idname = "tp_ops.bbox_for_panel"
    bl_label = "BBox"
    bl_options = {'REGISTER', 'UNDO'}
                                 
    bpy.types.Scene.bbox_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)            
    bpy.types.Scene.bbox_wire = bpy.props.BoolProperty(name="Wire only", description="Delete Face", default= False) 
    bpy.types.Scene.bbox_shade = bpy.props.BoolProperty(name="Shade off",  description="Shade off", default=False)  
    bpy.types.Scene.bbox_smooth = bpy.props.BoolProperty(name="Smooth",  description="Smooth", default=False)  
    bpy.types.Scene.bbox_origin = bpy.props.BoolProperty(name="Origin Center",  description="Origin to BBox-Center", default=False)  
    bpy.types.Scene.bbox_renderoff = bpy.props.BoolProperty(name="Restrict Render",  description="Restrict Render", default=False)
    bpy.types.Scene.bbox_freeze = bpy.props.BoolProperty(name="Restrict Selection",  description="Restrict Selection", default=False)            
    bpy.types.Scene.bbox_apply = bpy.props.BoolProperty(name="Apply Scale/Rotation",  description="Apply Scale / Rotation", default=False)  
    bpy.types.Scene.bbox_clear = bpy.props.BoolProperty(name="Clear Scale/Rotation",  description="Clear Scale / Rotation", default=False)  

    
    def execute(self, context): 
        if bpy.context.selected_objects: 
            if context.space_data.local_view is not None:  
                bpy.ops.view3d.localview()
                
                if context.scene.bbox_wire:
                    bpy.ops.tp_ops.bounding_box_wire()
                    bpy.ops.object.select_pattern(pattern="_bwire*", case_sensitive=False, extend=False)
                else:   
                    bpy.ops.tp_ops.bounding_box_source()  
                    bpy.ops.object.select_pattern(pattern="_bbox*", case_sensitive=False, extend=False)            
            else:            
 
                if context.scene.bbox_wire:
                    bpy.ops.tp_ops.bounding_box_wire()
                    bpy.ops.object.select_pattern(pattern="_bwire*", case_sensitive=False, extend=False)  
                else:   
                    bpy.ops.tp_ops.bounding_box_source()  
                    bpy.ops.object.select_pattern(pattern="_bbox*", case_sensitive=False, extend=False)

        else:
            bpy.ops.mesh.primitive_cube_add()            
            bpy.context.object.name = "_bbox"


        for obj in bpy.context.selected_objects:
                         
            bpy.context.scene.objects.active = obj                                                        
            bpy.ops.object.editmode_toggle()  
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent()                       
        

            for i in range(context.scene.bbox_subdiv):
                bpy.ops.mesh.subdivide(number_cuts=1)

            for i in range(context.scene.bbox_wire):
                bpy.ops.mesh.delete(type='ONLY_FACE')
           

            bpy.ops.object.editmode_toggle()

            for i in range(context.scene.bbox_origin):
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')                              

           
            # FURTHER TOOLS

            for i in range(context.scene.bbox_shade): 
                bpy.context.object.draw_type = 'WIRE'

            for i in range(context.scene.bbox_smooth):
                bpy.ops.object.shade_smooth()

            for i in range(context.scene.bbox_freeze):
                bpy.context.object.hide_select = True
            
            for i in range(context.scene.bbox_renderoff):
                bpy.context.object.hide_render = True

            for i in range(context.scene.bbox_clear):
                bpy.ops.object.rotation_clear()
                bpy.ops.object.scale_clear()

            for i in range(context.scene.bbox_apply):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            bpy.ops.tp_ops.rec_normals()

        bpy.ops.object.select_all(action='DESELECT')         
        return {'FINISHED'}                        





class VIEW3D_TP_BBox_for_Menu(bpy.types.Operator):
    """create bounding boxes for selected objects"""      
    bl_idname = "tp_ops.bbox_for_menu"
    bl_label = "BBox"
    bl_options = {'REGISTER', 'UNDO'}
                                 
    bbox_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)            
    bbox_wire = bpy.props.BoolProperty(name="Wire only", description="Delete only Face", default= False) 
    bbox_shade = bpy.props.BoolProperty(name="Shade off",  description="Shade off", default=False)  
    bbox_smooth = bpy.props.BoolProperty(name="Smooth",  description="Smooth", default=False)   
    bbox_origin = bpy.props.BoolProperty(name="Origin > Center",  description="Origin to Center", default=False)  

    bbox_renderoff = bpy.props.BoolProperty(name="Restrict Render",  description="Restrict Render", default=False)
    bbox_freeze = bpy.props.BoolProperty(name="Restrict Selection",  description="Restrict Selection", default=False)            
    bbox_apply = bpy.props.BoolProperty(name="Apply Scale/Rotation",  description="Apply Scale/Rotation", default=False)  
    bbox_clear = bpy.props.BoolProperty(name="Clear Scale/Rotation",  description="Clear Scale/Rotation", default=False)  

    
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


            # FURTHER TOOLS

            for i in range(self.bbox_shade): 
                bpy.context.object.draw_type = 'WIRE'

            for i in range(self.bbox_smooth):
                bpy.ops.object.shade_smooth()

            for i in range(self.bbox_freeze):
                bpy.context.object.hide_select = True
            
            for i in range(self.bbox_renderoff):
                bpy.context.object.hide_render = True

            for i in range(self.bbox_clear):
                bpy.ops.object.rotation_clear()
                bpy.ops.object.scale_clear()

            for i in range(self.bbox_apply):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


            bpy.ops.tp_ops.rec_normals()

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



class VIEW3D_TP_BBox_Source_Wire(bpy.types.Operator):
    """Make bound boxes for selected objects"""      
    bl_idname = "tp_ops.bounding_box_wire"
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
        name = ('_bwire') #(bpy.context.selected_objects[i].name + '_bwire') 
        me = bpy.data.meshes.new(name) #bpy.data.meshes.new(name + '_bbox')
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




class VIEW3D_TP_BBox_Source(bpy.types.Operator):
    """Make bound boxes for selected objects"""      
    bl_idname = "tp_ops.bounding_box_source"
    bl_label = "Bounding Box"
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
        name = ('_bbox') #(bpy.context.selected_objects[i].name + '_bbox') 
        me = bpy.data.meshes.new(name) #bpy.data.meshes.new(name +  '_bbox')
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




def register():
    bpy.utils.register_module(__name__)
     
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()





















