__status__ = "toolplus custom version"
__author__ = "mkbreuer"
__version__ = "1.0"
__date__ = "2016"

import bpy
import math, bmesh, mathutils,re
from bpy import*
from bpy.props import *
from bpy.types import Operator, AddonPreferences

from mathutils import Vector
from math import radians



class View3D_TP_Objects_To_Selected_Faces(bpy.types.Operator):
    """copy selected source to selected faces of the active target"""
    bl_idname = "tp_ops.copy_to_faces"
    bl_label = "Copy to Faces"
    bl_options = {"REGISTER", 'UNDO'}

    set_plus_z = bpy.props.BoolProperty(name="Top",  description="set origin to top", default = False)       
    set_minus_z = bpy.props.BoolProperty(name="Bottom",  description="set origin to bottom", default = False)       

    dupli = bpy.props.BoolProperty(name="Duplicate unlinked",  description="duplicate unlinked", default = False)       
    dupli_linked = bpy.props.BoolProperty(name="Duplicate linked",  description="duplicate linked", default = True)      

    set_edit_target = bpy.props.BoolProperty(name="Edit Target",  description="jump to target editmode", default = False)   
    set_edit_source = bpy.props.BoolProperty(name="Edit Source",  description="jump to source editmode", default = False)   

    def draw(self, context):
        layout = self.layout.column(1)

        if len(bpy.context.selected_objects) == 2:   
        
            box = layout.box().column(1)
             
            row = box.row(1)        
            row.label("Origin to")                 
            row.prop(self, 'set_plus_z', text="Top")                 
            row.prop(self, 'set_minus_z', text="Bottom")                 
           
            row = box.row(1)        
            row.label("Duplicate as:")              
            row.prop(self, 'dupli_linked', text="Linked") 
            row.prop(self, 'dupli', text="Unlinked")   
            
            row = box.row(1)        
            row.label("Jump to Edit:")                   
            row.prop(self, 'set_edit_source', text="Source")
            row.prop(self, 'set_edit_target', text="Target")

            box.separator()       

        else:
            box = layout.box().column(1)

            row = box.row(1)  
            row.label("need a source and a target", icon ="INFO")  
            
            
    def execute(self, context):
        
        obj = context.active_object
   
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'

        bpy.ops.object.mode_set(mode='OBJECT')

        if len(bpy.context.selected_objects) == 2:

            first_obj = bpy.context.active_object

            obj_a, obj_b = context.selected_objects

            second_obj = obj_a if obj_b == first_obj else obj_b  
                
            ### origin to top
            for i in range(self.set_plus_z):
                
                # active: second
                bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]  #["YourName"]           
                bpy.data.objects[second_obj.name].select=True                
                
                bpy.ops.tp_ops.origin_plus_z()  
               
                # active: first                
                bpy.context.scene.objects.active = bpy.data.objects[first_obj.name] 
                bpy.data.objects[first_obj.name].select = True 

            
            ### origin to bottom
            for i in range(self.set_minus_z):
                
                # active: second
                bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]            
                bpy.data.objects[second_obj.name].select=True                

                bpy.ops.tp_ops.origin_minus_z()  
               
                # active: first                    
                bpy.context.scene.objects.active = bpy.data.objects[first_obj.name] 
                bpy.data.objects[first_obj.name].select = True 

            # active: first   
            bpy.data.objects[second_obj.name].select=False

                        
            if context.mode == 'EDIT_MESH': 

                print(self)
                self.report({'INFO'}, "need a source and a target")  

            else: 
                
                bpy.ops.object.duplicate_move()             
                
                bpy.context.object.name = "Dummy"

                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')    

                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                        
                copy_cursor = bpy.context.scene.cursor_location.copy()     
         
                bm = bmesh.new()
                bm.from_mesh(obj.data)

                selected_faces = [f for f in bm.faces if f.select]
         
                for face in selected_faces:
         
                    face_location = face.calc_center_median()
         
                    loc_world_space = obj.matrix_world * Vector(face_location)
         
                    z = Vector((0,0,1))
         
                    angle = face.normal.angle(z)
         
                    axis = z.cross(face.normal)
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    
                    # active: second
                    bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]                    
                    bpy.data.objects[second_obj.name].select=True
                    
                    for i in range(self.dupli_linked):                                     
                        bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'})

                    for i in range(self.dupli):                    
                        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})             

                    bpy.context.scene.cursor_location = loc_world_space
                    
                    bpy.ops.view3d.snap_selected_to_cursor()
         
                    bpy.ops.transform.rotate(value=angle, axis=axis)

         
                bm.to_mesh(obj.data) 
                bm.free()
         
                bpy.context.scene.cursor_location = copy_cursor
                
                bpy.ops.object.select_all(action='DESELECT')
                
                # active: dummy
                bpy.context.scene.objects.active = bpy.data.objects["Dummy"]         
                bpy.data.objects["Dummy"].select = True

                bpy.ops.object.delete(use_global=False)
                                     
                #bpy.ops.object.select_all(action='DESELECT')
                

                for i in range(self.set_edit_source):
                    
                    # active: second
                    bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]                
                    bpy.data.objects[second_obj.name].select=True
                                        
                    bpy.ops.object.mode_set(mode='EDIT')   

                for i in range(self.set_edit_target):

                    # active: first
                    bpy.context.scene.objects.active = bpy.data.objects[first_obj.name]
                    bpy.data.objects[first_obj.name].select=True                    
                    
                    bpy.ops.object.mode_set(mode='EDIT')        
                    
                    print(self)
                    self.report({'INFO'}, "Editmode")      
 
        else:
            print(self)
            self.report({'INFO'}, "need a source and a target")         
                       
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)




class View3D_TP_Objects_To_Selected_Faces_Panel(bpy.types.Operator):
    """copy selected source to selected faces of the active target"""
    bl_idname = "tp_ops.copy_to_faces_panel"
    bl_label = "Copy to Faces"
    bl_options = {"REGISTER", 'UNDO'}

    bpy.types.Scene.pl_set_plus_z = bpy.props.BoolProperty(name="Top",  description="set origin to top", default = False)       
    bpy.types.Scene.pl_set_minus_z = bpy.props.BoolProperty(name="Bottom",  description="set origin to bottom", default = False)       

    bpy.types.Scene.pl_dupli = bpy.props.BoolProperty(name="Duplicate unlinked",  description="duplicate unlinked", default = False)       
    bpy.types.Scene.pl_dupli_linked = bpy.props.BoolProperty(name="Duplicate linked",  description="duplicate linked", default = True)      

    bpy.types.Scene.pl_set_edit_target = bpy.props.BoolProperty(name="Edit Target",  description="jump to target editmode", default = False)   
    bpy.types.Scene.pl_set_edit_source = bpy.props.BoolProperty(name="Edit Source",  description="jump to source editmode", default = False) 


    def draw(self, context):
        layout = self.layout.column(1)
        scene = context.scene 
                
        if len(bpy.context.selected_objects) == 2:   

            box = layout.box().column(1)
             
            row = box.row(1)        
            row.label("Origin to")                 
            row.prop(scene, 'pl_set_plus_z', text="Top")                 
            row.prop(scene, 'pl_set_minus_z', text="Bottom")                 
           
            row = box.row(1)        
            row.label("Duplicate as:")              
            row.prop(scene, 'pl_dupli_linked', text="Linked") 
            row.prop(scene, 'pl_dupli', text="Unlinked")   
            
            row = box.row(1)        
            row.label("Jump to Edit:")                   
            row.prop(scene, 'pl_set_edit_source', text="Source")
            row.prop(scene, 'pl_set_edit_target', text="Target")

            box.separator()       
              
            row = box.row()
            row.operator('wm.operator_defaults', text="Reset", icon ="BLANK1")

        else:
            box = layout.box().column(1)

            row = box.row(1)  
            row.label("need a source and a target", icon ="INFO")            


    def execute(self, context):
        scene = context.scene        

        obj = context.active_object
   
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'

        bpy.ops.object.mode_set(mode='OBJECT')

        if len(bpy.context.selected_objects) > 1:
   

            first_obj = bpy.context.active_object

            obj_a, obj_b = context.selected_objects

            second_obj = obj_a if obj_b == first_obj else obj_b  
                
            ### origin to top
            for i in range(scene.pl_set_plus_z):
                
                # active: second
                bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]            
                bpy.data.objects[second_obj.name].select=True                
                
                bpy.ops.tp_ops.origin_plus_z()  
               
                # active: first                
                bpy.context.scene.objects.active = bpy.data.objects[first_obj.name] 
                bpy.data.objects[first_obj.name].select = True 

            
            ### origin to bottom
            for i in range(scene.pl_set_minus_z):
                
                # active: second
                bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]            
                bpy.data.objects[second_obj.name].select=True                

                bpy.ops.tp_ops.origin_minus_z()  
               
                # active: first                    
                bpy.context.scene.objects.active = bpy.data.objects[first_obj.name] 
                bpy.data.objects[first_obj.name].select = True 

           
            # active: first   
            bpy.data.objects[second_obj.name].select=False
                        
            if context.mode == 'EDIT_MESH': 

                print(self)
                self.report({'INFO'}, "need a source and a target")  

            else: 
                
                bpy.ops.object.duplicate_move()             
                
                bpy.context.object.name = "Dummy"

                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')    

                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                        
                copy_cursor = bpy.context.scene.cursor_location.copy()     
         
                bm = bmesh.new()
                bm.from_mesh(obj.data)

                selected_faces = [f for f in bm.faces if f.select]
         
                for face in selected_faces:
         
                    face_location = face.calc_center_median()
         
                    loc_world_space = obj.matrix_world * Vector(face_location)
         
                    z = Vector((0,0,1))
         
                    angle = face.normal.angle(z)
         
                    axis = z.cross(face.normal)
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    
                    # active: second
                    bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]                    
                    bpy.data.objects[second_obj.name].select=True
                    
                    for i in range(scene.pl_dupli_linked):                                     
                        bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'})

                   
                    for i in range(scene.pl_dupli):                    
                        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})             

                    bpy.context.scene.cursor_location = loc_world_space
                    
                    bpy.ops.view3d.snap_selected_to_cursor()
         
                    bpy.ops.transform.rotate(value=angle, axis=axis)

         
                bm.to_mesh(obj.data) 
                bm.free()
         
                bpy.context.scene.cursor_location = copy_cursor
                
                bpy.ops.object.select_all(action='DESELECT')
                
                # active: dummy
                bpy.context.scene.objects.active = bpy.data.objects["Dummy"]         
                bpy.data.objects["Dummy"].select = True

                bpy.ops.object.delete(use_global=False)
                                     
                #bpy.ops.object.select_all(action='DESELECT')
                
                for i in range(scene.pl_set_edit_source):
                    
                    # active: second
                    bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]                
                    bpy.data.objects[second_obj.name].select=True
                                        
                    bpy.ops.object.mode_set(mode='EDIT')                     
                    
                    print(self)
                    self.report({'INFO'}, "Editmode")  


                for i in range(scene.pl_set_edit_target):

                    # active: first
                    bpy.context.scene.objects.active = bpy.data.objects[first_obj.name]
                    bpy.data.objects[first_obj.name].select=True                    
                    
                    bpy.ops.object.mode_set(mode='EDIT')        
                    
                    print(self)
                    self.report({'INFO'}, "Editmode")
      
 
        else:
            print(self)
            self.report({'INFO'}, "need a source and a target")         
        
                
        return {"FINISHED"}





class View3D_TP_Origin_Plus_Z(bpy.types.Operator):  
    """place origin to top / +z axis""" 
    bl_idname = "tp_ops.origin_plus_z"  
    bl_label = "Origin to Top / +Z Axis"  
    bl_options = {"REGISTER", 'UNDO'}
  
    def draw(self, context):
        layout = self.layout.column(1)
                
        obj = context.active_object     
        if obj:
            obj_type = obj.type
                                                                  
            if obj_type in {'MESH'}: 
                box = layout.box().column(1)

                row = box.row(1)  
                row.label("done", icon ="INFO")

            else:
                box = layout.box().column(1)

                row = box.row(1)  
                row.label("only for mesh", icon ="INFO")            

    def execute(self, context):

        obj = context.active_object     
        if obj:
            obj_type = obj.type
                                                                  
            if obj_type in {'MESH'}: 
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
                     x.co.z+=a
                                 
                o.location.z-=a                   
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.object.editmode_toggle()        

        else:
            print(self)
            self.report({'INFO'}, "only Mesh")  
        
        return {'FINISHED'}


class View3D_TP_Origin_Minus_Z(bpy.types.Operator):  
    """place origin to bottom / -z axis""" 
    bl_idname = "tp_ops.origin_minus_z"  
    bl_label = "Origin to Bottom / -Z Axis"  
    bl_options = {"REGISTER", 'UNDO'}
      
    def draw(self, context):
        layout = self.layout.column(1)
                
        obj = context.active_object     
        if obj:
            obj_type = obj.type
                                                                  
            if obj_type in {'MESH'}: 
                box = layout.box().column(1)

                row = box.row(1)  
                row.label("done", icon ="INFO")

            else:
                box = layout.box().column(1)

                row = box.row(1)  
                row.label("only for mesh", icon ="INFO")            


    def execute(self, context):
 
        obj = context.active_object     
        if obj:
            obj_type = obj.type
                                                                  
            if obj_type in {'MESH'}: 
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

        else:
            print(self)
            self.report({'INFO'}, "only Mesh")  

        return {'FINISHED'}




def register():

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()







