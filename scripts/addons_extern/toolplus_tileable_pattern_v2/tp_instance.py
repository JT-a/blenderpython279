import bpy, bmesh
from bpy import*
from bpy.props import *



class TP_Reference_Grid(bpy.types.Operator):
    """adds a wire square object"""
    bl_idname = "tp_ops.reference_grid"
    bl_label = "RefzGrid"
    bl_options = {'REGISTER', 'UNDO'}  

    div_ref = bpy.props.BoolProperty(name="Divide",  description="only 9/25 reference grid", default=True) 

    def draw(self, context):
        layout = self.layout.column(1)
        
        box = layout.box().column(1)
        
        row = box.row(1)
        
        if self.div_ref == True:        
            row.prop(self, "div_ref","9 -> 25 Grid", icon ="FILE_REFRESH")
        else:
            row.prop(self, "div_ref","25 -> 9 Grid", icon ="FILE_REFRESH")

 
    def execute(self, context):  

        bpy.ops.view3d.snap_cursor_to_center()

        bpy.ops.mesh.primitive_plane_add(radius=5)

        if self.div_ref == True:
            bpy.context.object.scale[0] = 3.468
            bpy.context.object.scale[1] = 3.468
            bpy.context.object.scale[2] = 3.468           
        else:
            bpy.context.object.scale[0] = 5.7799995
            bpy.context.object.scale[1] = 5.7799995
            bpy.context.object.scale[2] = 5.7799995 
       
        bpy.ops.view3d.snap_selected_to_cursor()

        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.select_mode(type='FACE')
        
        if self.div_ref == True:
            bpy.ops.mesh.subdivide(number_cuts=2)
            bpy.context.object.name = "Ref_9_Grid"
            bpy.context.object.data.name = "Ref_9_Grid"  

        else:           
            bpy.ops.mesh.subdivide(number_cuts=4)            
            bpy.context.object.name = "Ref_25_Grid"
            bpy.context.object.data.name = "Ref_25_Grid"  
            
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.mesh.remove_doubles()         
        bpy.ops.object.editmode_toggle()

        bpy.data.objects["Ref_9_Grid"].hide_select = True
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 150) 




class TP_Tileable_Planes(bpy.types.Operator):
    """adds a wire square object with instances [add your geomtry to Instance Fill]"""
    bl_idname = "tp_ops.instances_fields"
    bl_label = "Add Planes"
    bl_options = {'REGISTER', 'UNDO'}  

    div_nine = bpy.props.BoolProperty(name="Divide",  description="Instances 9/25 for pattern creation", default=True) 


    def draw(self, context):
        layout = self.layout.column(1)
        
        row = layout.row(1)
        if self.div_nine == True:        
            row.prop(self, "div_nine","9 -> 25 Grid", icon ="FILE_REFRESH")
        else:
            row.prop(self, "div_nine","25 -> 9 Grid", icon ="FILE_REFRESH")

 
    def execute(self, context):
        print(self)
        self.report({'INFO'}, "added linked wire squares")    

        bpy.ops.view3d.snap_cursor_to_center()

        bpy.ops.mesh.primitive_plane_add(radius=5)

        if self.div_nine == True:
            bpy.context.object.scale[0] = 3.468
            bpy.context.object.scale[1] = 3.468
            bpy.context.object.scale[2] = 3.468           
        else:
            bpy.context.object.scale[0] = 5.7799995
            bpy.context.object.scale[1] = 5.7799995
            bpy.context.object.scale[2] = 5.7799995 

        bpy.context.object.name = "Instance_Planes"
        bpy.context.object.data.name = "Instance_Planes"        
 
        bpy.ops.view3d.snap_selected_to_cursor()

        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.select_mode(type='FACE')
        
        if self.div_nine == True:
            bpy.ops.mesh.subdivide(number_cuts=2)

        else:           
            bpy.ops.mesh.subdivide(number_cuts=4)            

        bpy.ops.mesh.inset(thickness=0, use_individual=True)
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type='FACE')    

        bpy.ops.mesh.select_all(action='SELECT')       
        bpy.ops.mesh.normals_make_consistent()  

        bpy.ops.mesh.separate(type='LOOSE')        

        bpy.ops.object.editmode_toggle() 

        bpy.ops.object.select_all(action='DESELECT') 

        if self.div_nine == True:
            bpy.context.scene.objects.active = bpy.data.objects["Instance_Planes.007"] 
            bpy.ops.object.select_pattern(pattern="Instance_Planes.007") 

        else:          
            bpy.context.scene.objects.active = bpy.data.objects["Instance_Planes.016"] 
            bpy.ops.object.select_pattern(pattern="Instance_Planes.016") 

        bpy.context.object.name = "Instance_Fill"
        bpy.context.object.data.name = "Instance_Fill"       
      
        bpy.context.scene.objects.active = bpy.data.objects["Instance_Fill"] 
        bpy.ops.object.select_pattern(pattern="Instance_Fill")        
 
        bpy.ops.object.select_all(action='DESELECT') 
        
        bpy.ops.object.select_pattern(pattern="Instance*", extend=True)
        
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        bpy.ops.object.make_links_data(type='OBDATA')
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT') 
        bpy.ops.mesh.delete(type='ONLY_FACE')

        bpy.ops.object.editmode_toggle()        
           
        bpy.ops.object.select_all(action='DESELECT')  
        
        bpy.ops.object.select_pattern(pattern="Instance_Fill", case_sensitive=False, extend=False)
        bpy.context.scene.objects.active = bpy.data.objects["Instance_Fill"] 

        # add plane to the middle instance field
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.mesh.primitive_plane_add()


        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 150) 
    
    

class TP_Tileable_Curves(bpy.types.Operator):
    """adds a wire square object with instances [add your geomtry to Instance Fill]"""
    bl_idname = "tp_ops.instances_curves"
    bl_label = "Add Curves"
    bl_options = {'REGISTER', 'UNDO'}  

    div_nine = bpy.props.BoolProperty(name="Divide",  description="Instances 9/25 for pattern creation", default=True) 

    def draw(self, context):
        layout = self.layout.column(1)
        
        row = layout.row(1)
        if self.div_nine == True:        
            row.prop(self, "div_nine","9 -> 25 Grid", icon ="FILE_REFRESH")
        else:
            row.prop(self, "div_nine","25 -> 9 Grid", icon ="FILE_REFRESH")

 
    def execute(self, context):
        print(self)
        self.report({'INFO'}, "added linked wire squares")    

        bpy.ops.view3d.snap_cursor_to_center()

        bpy.ops.mesh.primitive_plane_add(radius=5)

        if self.div_nine == True:
            bpy.context.object.scale[0] = 3.468
            bpy.context.object.scale[1] = 3.468
            bpy.context.object.scale[2] = 3.468           
        else:
            bpy.context.object.scale[0] = 5.7799995
            bpy.context.object.scale[1] = 5.7799995
            bpy.context.object.scale[2] = 5.7799995 

        bpy.context.object.name = "Instance_Planes"
        bpy.context.object.data.name = "Instance_Planes"        
 
        bpy.ops.view3d.snap_selected_to_cursor()

        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.select_mode(type='FACE')
        
        if self.div_nine == True:
            bpy.ops.mesh.subdivide(number_cuts=2)

        else:           
            bpy.ops.mesh.subdivide(number_cuts=4)            

        bpy.ops.mesh.inset(thickness=0, use_individual=True)
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type='FACE')    

        bpy.ops.mesh.select_all(action='SELECT')       
        bpy.ops.mesh.normals_make_consistent()  

        bpy.ops.mesh.separate(type='LOOSE')        

        bpy.ops.object.editmode_toggle() 

        bpy.ops.object.select_all(action='DESELECT') 

        if self.div_nine == True:
            bpy.context.scene.objects.active = bpy.data.objects["Instance_Planes.007"] 
            bpy.ops.object.select_pattern(pattern="Instance_Planes.007") 

        else:          
            bpy.context.scene.objects.active = bpy.data.objects["Instance_Planes.016"] 
            bpy.ops.object.select_pattern(pattern="Instance_Planes.016") 

        bpy.context.object.name = "Instance_Fill"
        bpy.context.object.data.name = "Instance_Fill"       
      
        bpy.context.scene.objects.active = bpy.data.objects["Instance_Fill"] 
        bpy.ops.object.select_pattern(pattern="Instance_Fill")        
 
        bpy.ops.object.select_all(action='DESELECT') 
        
        bpy.ops.object.select_pattern(pattern="Instance*", extend=True)
        
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
 
        bpy.ops.object.make_links_data(type='OBDATA')
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT') 
        bpy.ops.mesh.delete(type='ONLY_FACE')

        bpy.ops.object.editmode_toggle()        

        bpy.ops.object.select_all(action='SELECT')       
        bpy.ops.curve.convert_bezier()
        
        bpy.ops.object.make_links_data(type='OBDATA')
        
        bpy.ops.object.select_all(action='DESELECT')  
        
        bpy.ops.object.select_pattern(pattern="Instance_Fill", case_sensitive=False, extend=False)
        bpy.context.scene.objects.active = bpy.data.objects["Instance_Fill"] 

        # add circle to the middle instance field
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.curve.primitive_bezier_circle_add(radius=1)
        bpy.ops.curve.handle_type_set(type='VECTOR')
        bpy.context.object.data.dimensions = '2D'

        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 150) 
    
    

class TP_Tileable_Join(bpy.types.Operator):
    """press join instances when you finished the pattern"""
    bl_idname = "tp_ops.tileable_join"
    bl_label = "Join Instances"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')         

        bpy.ops.object.select_pattern(pattern="Instance*", case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = bpy.data.objects["Instance_Fill"] 
        bpy.ops.object.join()                        

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(type='VERT')  
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent()    
        bpy.ops.object.editmode_toggle() 

        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        return {'FINISHED'}



class TP_Tileable_Normals(bpy.types.Operator):
    """Recalculate Normals for all selected objects in objectmode"""
    bl_idname = "tp_ops.recalculate_normals"
    bl_label = "Recalculate Normals"     

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Recalculate Normals")                   
        
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj 
                
            if obj:
                obj_type = obj.type

                if obj_type in {'MESH'}:                 
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.normals_make_consistent()
                    bpy.ops.object.editmode_toggle()            

        return {'FINISHED'}       


    
class TP_Tileable_Purge_Mesh(bpy.types.Operator):
    '''purge all unused data meshes or curves'''
    bl_idname="tp_ops.purge_unused_data"
    bl_label="Purge Mesh"
    bl_options = {"REGISTER", 'UNDO'}    

    def execute(self, context):
        
        obj = context.active_object
        if obj:
            obj_type = obj.type
            
            if obj_type in {'MESH'}:
                print(self)
                self.report({'INFO'}, "purged meshes")                   

                target_coll = eval("bpy.data.meshes")                
            
            if obj_type in {'CURVE'}:
                print(self)
                self.report({'INFO'}, "purged curves")  
                
                target_coll = eval("bpy.data.curves")

        for item in target_coll:
            if item.users == 0:
                target_coll.remove(item)

        return {'FINISHED'}



class TP_Tileable_Remove_Doubles(bpy.types.Operator):
    """Removes doubles on selected objects."""
    bl_idname = "tp_ops.tileable_remove_double"
    bl_label = "Remove Doubles off Selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')        
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}



class TP_Tileable_Freeze(bpy.types.Operator):
    """Freeze from Selection"""
    bl_idname = "tp_ops.tileable_freeze"
    bl_label = "Freeze from Selection"
    
    def execute(self, context):       
        bpy.context.object.hide_select = True
        return {'FINISHED'}   



#snippet from vismaya
def get_AllObjectsInScene():   
    return bpy.data.objects

def get_dehideSelectObjects(object_list):
    hidedObjs = []
    for i in object_list:
        if i.hide_select == True:
            i.hide_select = False
            hidedObjs.append(i)
    return hidedObjs

def get_highlightObjects(selection_list):
    
   for i in selection_list:
        bpy.data.objects[i.name].select = True         



class TP_Tileable_Unfreeze(bpy.types.Operator):
    bl_idname = "tp_ops.tileable_unfreeze"
    bl_label = "Unfreeze All"
    bl_description = "Enables all freezed"
   
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        selection = get_AllObjectsInScene()
        n = len(selection)

        if n > 0:
            freezed_array = get_dehideSelectObjects(selection)
            get_highlightObjects(freezed_array)
            self.report({'INFO'}, "%d Object%s released." % (n, "s"[n==1:]))
        else:
            self.report({'INFO'}, 'Nothing selected.')
        
        return{'FINISHED'} 
    




import bmesh
from bpy import*
from bpy.props import*


class TP_Tileable_Cutout_Cube(bpy.types.Operator):
    """"""
    bl_idname = "tp_ops.cutout_cube"
    bl_label = "Cutout Cube"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        verts = [(-34.68000030517578, -34.68000030517578, 50.0), (34.68000030517578, -34.68000030517578, 50.0), (-34.68000030517578, 34.68000030517578, 50.0), (34.68000030517578, 34.68000030517578, 50.0), (-5.779999732971191, -5.779999256134033, 50.0), (-5.78000020980835, 5.78000020980835, 50.0), (5.779999732971191, -5.779999256134033, 50.0), (5.779999256134033, 5.78000020980835, 50.0), (-34.68000030517578, -34.68000030517578, -50.0), (34.68000030517578, -34.68000030517578, -50.0), (-34.68000030517578, 34.68000030517578, -50.0), (34.68000030517578, 34.68000030517578, -50.0), (-5.779999732971191, -5.779999256134033, -50.0), (-5.78000020980835, 5.78000020980835, -50.0), (5.779999732971191, -5.779999256134033, -50.0), (5.779999256134033, 5.78000020980835, -50.0)]
        faces = [(6, 14, 12, 4), (4, 12, 13, 5), (2, 3, 11, 10), (0, 2, 10, 8), (7, 5, 13, 15), (6, 7, 15, 14), (1, 9, 11, 3), (0, 8, 9, 1), (6, 4, 0, 1), (7, 6, 1, 3), (7, 3, 2, 5), (5, 2, 0, 4), (14, 9, 8, 12), (15, 11, 9, 14), (15, 13, 10, 11), (13, 12, 8, 10)]

        mesh_data = bpy.data.meshes.new("cube_mesh_data")  
        mesh_data.from_pydata(verts, [], faces)  
        mesh_data.update()

        obj = bpy.data.objects.new("Cutout", mesh_data)  

        scene = bpy.context.scene    
        scene.objects.link(obj)    
        obj.select = True  
        #bpy.data.objects["Cutout"].hide = True
        #bpy.data.objects["Cutout"].hide_render = True    
        return {'FINISHED'}
    



class TP_Tileable_Cutout(bpy.types.Operator):
    """extruded and overlapped mesh cutout of the middle field"""
    bl_idname = "tp_ops.tileable_cutout"
    bl_label = "Cutout"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "cutout middle field")     

        bpy.ops.tp_ops.cutout_cube()        

        bpy.ops.tp_ops.tileable_boolean()
        bpy.ops.tp_ops.instances_remove()

        bpy.ops.object.select_pattern(pattern="Instance_Fill", case_sensitive=False, extend=False)
        bpy.context.scene.objects.active = bpy.data.objects["Instance_Fill"] 
        
        return {'FINISHED'}



class TP_Tileable_CutOut_Boolean(bpy.types.Operator):
    """cutout the tilable middle plane"""
    bl_idname = "tp_ops.tileable_boolean"
    bl_label = "BOOLEAN"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        
        bpy.context.scene.objects.active = bpy.data.objects["Instance_Fill"] 
        bpy.ops.object.select_pattern(pattern="Instance_Fill")   

        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Cutout"]
        bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}



class TP_Tileable_Remove_double(bpy.types.Operator):
    """delete cutout object"""
    bl_idname = "tp_ops.instances_remove"
    bl_label = "Delete Cutout Object"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):

        #bpy.data.objects["Cutout"].hide = False

        bpy.ops.object.select_pattern(pattern="Cutout", case_sensitive=False, extend=False)   
        bpy.context.scene.objects.active = bpy.data.objects["Cutout"]   
        
        bpy.ops.object.delete(use_global=False)

        return {'FINISHED'}



class TP_Tileable_Make_Single(bpy.types.Operator):
    """Make Single User for all Linked (Object Data)"""
    bl_idname = "tp_ops.make_single"
    bl_label = "Make Single"

    def execute(self, context):
        bpy.ops.object.select_linked(type='OBDATA')
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)
        return {'FINISHED'}




class Wire_All(bpy.types.Operator):
    """Wire on All Objects"""
    bl_idname = "tp_ops.wire_all"
    bl_label = "Wire on All Objects"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        for obj in bpy.data.objects:
            if obj.show_wire:
                obj.show_all_edges = False
                obj.show_wire = False            
            else:
                obj.show_all_edges = True
                obj.show_wire = True
                             
        return {'FINISHED'} 

class Wire_On(bpy.types.Operator):
    '''Wire on'''
    bl_idname = "tp_ops.wire_on"
    bl_label = "Wire on"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        selection = bpy.context.selected_objects  
         
        if not(selection): 
            for obj in bpy.data.objects:
                obj.show_wire = True
                obj.show_all_edges = True
                
        else:
            for obj in selection:
                obj.show_wire = True
                obj.show_all_edges = True 
        return {'FINISHED'}


class Wire_Off(bpy.types.Operator):
    '''Wire off'''
    bl_idname = "tp_ops.wire_off"
    bl_label = "Wire off"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        selection = bpy.context.selected_objects  
        
        if not(selection): 
            for obj in bpy.data.objects:
                obj.show_wire = False
                obj.show_all_edges = False
                
        else:
            for obj in selection:
                obj.show_wire = False
                obj.show_all_edges = False   

        return {'FINISHED'}
    

class ConvertBezier(bpy.types.Operator):
    """Convert to Curve with Bezièr Spline Typ"""
    bl_idname = "curve.convert_bezier"
    bl_label = "Convert to Curve with Bezièr Spline Typ"

    def execute(self, context):
        bpy.ops.object.convert(target='CURVE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.spline_type_set(type='BEZIER')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class Join_Curves(bpy.types.Operator):
    """join curves instances and convert to mesh"""
    bl_idname = "tp_ops.join_curves"
    bl_label = "Join Curves"

    def execute(self, context):        
        bpy.ops.object.select_all(action='DESELECT')         

        bpy.ops.object.select_pattern(pattern="Instance*", case_sensitive=False, extend=True)
        bpy.context.scene.objects.active = bpy.data.objects["Instance_Fill"]  
        bpy.ops.object.join()
        bpy.ops.object.convert(target='MESH')
        return {'FINISHED'}



        
class Display_Modifiers_On(bpy.types.Operator):
    '''Display modifiers in viewport'''
    bl_idname = "tp_ops.modifiers_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_objects 
        
        if not(selection):    
            for obj in bpy.data.objects:        
                for mod in obj.modifiers:
                    mod.show_viewport = True
        else:
            for obj in selection:        
                for mod in obj.modifiers:
                    mod.show_viewport = True

        return {'FINISHED'}
    

class Display_Modifiers_Off(bpy.types.Operator):
    '''Hide modifiers in viewport'''
    bl_idname = "tp_ops.modifiers_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_objects 
        
        if not(selection):    
            for obj in bpy.data.objects:        
                for mod in obj.modifiers:
                    mod.show_viewport = False
        else:
            for obj in selection:        
                for mod in obj.modifiers:
                    mod.show_viewport = False

        return {'FINISHED'}



def register():

    bpy.utils.register_class(TP_Reference_Grid)
    bpy.utils.register_class(TP_Tileable_Planes)
    bpy.utils.register_class(TP_Tileable_Curves)
    bpy.utils.register_class(TP_Tileable_Join)
    bpy.utils.register_class(TP_Tileable_Normals)
    bpy.utils.register_class(TP_Tileable_Purge_Mesh)
    bpy.utils.register_class(TP_Tileable_Remove_Doubles)
    bpy.utils.register_class(TP_Tileable_Freeze)
    bpy.utils.register_class(TP_Tileable_Unfreeze)
    bpy.utils.register_class(TP_Tileable_Cutout_Cube)
    bpy.utils.register_class(TP_Tileable_Cutout)
    bpy.utils.register_class(TP_Tileable_CutOut_Boolean)
    bpy.utils.register_class(TP_Tileable_Remove_double)
    bpy.utils.register_class(TP_Tileable_Make_Single)
    bpy.utils.register_class(Wire_All)
    bpy.utils.register_class(Wire_On)
    bpy.utils.register_class(Wire_Off)
    bpy.utils.register_class(ConvertBezier)
    bpy.utils.register_class(Join_Curves)
    bpy.utils.register_class(Display_Modifiers_On)
    bpy.utils.register_class(Display_Modifiers_Off)



def unregister():

    bpy.utils.unregister_class(TP_Reference_Grid)
    bpy.utils.unregister_class(TP_Tileable_Planes)
    bpy.utils.unregister_class(TP_Tileable_Curves)
    bpy.utils.unregister_class(TP_Tileable_Join)
    bpy.utils.unregister_class(TP_Tileable_Normals)
    bpy.utils.unregister_class(TP_Tileable_Purge_Mesh)
    bpy.utils.unregister_class(TP_Tileable_Remove_Doubles)
    bpy.utils.unregister_class(TP_Tileable_Freeze)
    bpy.utils.unregister_class(TP_Tileable_Unfreeze)
    bpy.utils.unregister_class(TP_Tileable_Cutout_Cube)
    bpy.utils.unregister_class(TP_Tileable_Cutout)
    bpy.utils.unregister_class(TP_Tileable_CutOut_Boolean)
    bpy.utils.unregister_class(TP_Tileable_Remove_double)
    bpy.utils.unregister_class(TP_Tileable_Make_Single)
    bpy.utils.unregister_class(Wire_All)
    bpy.utils.unregister_class(Wire_On)
    bpy.utils.unregister_class(Wire_Off)
    bpy.utils.unregister_class(ConvertBezier)
    bpy.utils.unregister_class(Join_Curves)
    bpy.utils.unregister_class(Display_Modifiers_On)
    bpy.utils.unregister_class(Display_Modifiers_Off)

if __name__ == "__main__":
    register()
