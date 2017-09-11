import bpy
import bmesh
from mathutils import Vector   
 


def tp_desc_curve_insert(object):
    #initial set
    if object == "Torus.png":
        bpy.ops.mesh.primitive_torus_add()

    elif object == "Icosphere.png":
        bpy.ops.mesh.primitive_ico_sphere_add()

    elif object == "Cone.png":
        bpy.ops.mesh.primitive_cone_add()




def tp_insert_curve_geometry(self, context):
    wm = context.window_manager
    object = wm.TP_Tileable_Curve_Previews
    obj_list = []    
    second_obj = ""
    
    if bpy.context.mode == 'OBJECT':
        
        tp_desc_curve_insert(object)###objectlist
        
    elif bpy.context.mode == 'EDIT':        
        bpy.ops.object.mode_set(mode='OBJECT')  
        ref_obj = bpy.context.active_object

        if len(context.selected_objects) == 2:
            obj1, obj2 = context.selected_objects
            second_obj = obj1 if obj2 == ref_obj else obj2
        
            bpy.data.objects[second_obj.name].select=False

        bpy.ops.object.duplicate_move()
        bpy.context.active_object.name = "Dummy"
        obj = context.active_object
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
            bpy.context.scene.cursor_location = loc_world_space
            
            tp_desc_curve_insert(object)###objectlist         
     
            bpy.ops.transform.rotate(value=angle, axis=axis)
            obj_list.append(context.object.name)
     
        bm.to_mesh(obj.data)
     
        bm.free()
        
        bpy.context.scene.cursor_location = copy_cursor
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = bpy.data.objects["Dummy"]         
        bpy.data.objects["Dummy"].select = True
        bpy.ops.object.delete(use_global=False)
        
        bpy.context.scene.objects.active = bpy.data.objects[obj_list[0]]
        
        for obj in obj_list:
            bpy.data.objects[obj].select=True
            bpy.ops.make.link()  # custom link called from operators module
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = bpy.data.objects[ref_obj.name]

        if second_obj:
            bpy.data.objects[second_obj.name].select=True   

        bpy.data.objects[ref_obj.name].select=True
     
        bpy.ops.object.mode_set(mode='EDIT')
        del(obj_list[:])
 
