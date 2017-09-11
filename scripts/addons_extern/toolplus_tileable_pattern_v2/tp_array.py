import bpy
from bpy import*
from bpy.props import *



class TP_Tileable_Add_Vertices_Offset(bpy.types.Operator):
    """Add single vertices to correct array offset"""
    bl_idname = "tp_ops.add_vertices_offset"
    bl_label = "Offset Vertices"
    bl_options = {'REGISTER', 'UNDO'} 

    bpy.types.Scene.tp_verts_offset = bpy.props.EnumProperty(
        items=[("tp_verts_x"    ,"X Axis"   ,"X Axis"),
               ("tp_verts_y"    ,"Y Axis"   ,"Y Axis"),
               ("tp_verts_xy"   ,"XY Axis"  ,"XY Axis")],
               name = "Offset",
               default = "tp_verts_xy",    
               description = "Add single vertices to correct array offset")
               
               
    def execute(self, context):
        print(self)
        self.report({'INFO'}, "add single vertices to correct array offset")   

        scene = bpy.context.scene 
                
        if scene.tp_verts_offset == "tp_verts_x":
           
            verts_x = [(-17.34, -17.34, 0), (-5.78, -17.34, 0)]

            mesh_data = bpy.data.meshes.new("vertices")  
            mesh_data.from_pydata(verts_x, [], [])  
            mesh_data.update() 
 
        if scene.tp_verts_offset == "tp_verts_y":
            
            verts_y = [(-17.34, -17.34, 0), (-17.34, -5.78, 0)]

            mesh_data = bpy.data.meshes.new("vertices")  
            mesh_data.from_pydata(verts_y, [], [])  
            mesh_data.update()


        if scene.tp_verts_offset == "tp_verts_xy":
           
            verts_xy = [(-17.34, -5.78, 0), (-17.34, -17.34, 0), (-17.34, 5.78, 0)]

            mesh_data = bpy.data.meshes.new("vertices")  
            mesh_data.from_pydata(verts_xy, [], [])  
            mesh_data.update()

        obj = bpy.data.objects.new("offset", mesh_data)  

   
        scene.objects.link(obj)    
        obj.select = True  

        if bpy.context.mode == "EDIT_MESH":
            pass
        else:
            bpy.ops.object.join()
            
        return {'FINISHED'}




class TP_Tileable_Camera(bpy.types.Operator):
    """Camera Render Setup"""
    bl_idname = "tp_ops.tileable_camera"
    bl_label = "Camera Setup"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "added camera for tileable pattern")   
    
        bpy.context.scene.render.resolution_x = 1024
        bpy.context.scene.render.resolution_y = 1024
        
        bpy.context.scene.render.resolution_percentage = 100
        
        #bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(17.34, 17.34, 50), rotation=(0, 0, 0))
        bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, 0, 50), rotation=(0, 0, 0))
        bpy.context.object.data.type = 'ORTHO'
        
        bpy.context.object.data.ortho_scale = 34.68
        
        #bpy.ops.object.lamp_add(type='SUN', radius=1, view_align=False, location=(17.34, 17.34, 40))
        bpy.ops.object.lamp_add(type='SUN', radius=1, view_align=False, location=(0, 0, 40))
        
        bpy.context.object.data.energy = 0.25
       
        bpy.ops.view3d.viewnumpad(type='CAMERA')

        return {'FINISHED'}



class TP_Tileable_Arrays(bpy.types.Operator):
    """set the pattern back to the center and adds two array modifier"""
    bl_idname = "tp_ops.tileable_arrays"
    bl_label = "Add XY Arrays"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "clear location / added 2 array modifier")     

        bpy.context.object.name = "Array_Pattern"   
        
        bpy.context.space_data.cursor_location[0] = -5.7799997
        bpy.context.space_data.cursor_location[1] = -5.7799997
        bpy.context.space_data.cursor_location[2] = 0

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        

             
        #bpy.ops.tp_ops.origin_minus_xy()
        bpy.ops.transform.translate(value=(-11.56, -11.56, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)        

        bpy.ops.object.modifier_add(type='ARRAY')      
        bpy.context.object.modifiers["Array"].name = "Array X Axis"        
        bpy.context.object.modifiers["Array X Axis"].count = 3        

        bpy.ops.object.modifier_add(type='ARRAY')      
        bpy.context.object.modifiers["Array"].name = "Array Y Axis"  
        bpy.context.object.modifiers["Array Y Axis"].count = 3
        bpy.context.object.modifiers["Array Y Axis"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array Y Axis"].relative_offset_displace[1] = 1

        return {'FINISHED'}



class TP_Tileable_Array_Scale(bpy.types.Operator):
    """scale the array to 34.68cm"""
    bl_idname = "tp_ops.tileable_array_scale"
    bl_label = "Add XY Arrays"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "scale the array to 34.68cm")     

        current_x, current_y, current_z =  bpy.context.object.dimensions
        bpy.context.object.dimensions = [34.68, 34.68, current_z]

        return {'FINISHED'}




class TP_Tileable_Origin_XY(bpy.types.Operator):  
    """Origin to -XY Corner"""
    bl_idname = "tp_ops.origin_minus_xy"  
    bl_label = "Origin to -XY Corner"  
    bl_options = {'REGISTER', 'UNDO'}  
  
    def execute(self, context):      
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        o=bpy.context.active_object
        init=0
        for x in o.data.vertices:
             if init==0:
                 a=x.co.x
                 b=x.co.y
                 c=x.co.z

                 init=1
             
             elif x.co.x < a:
                 a=x.co.x
                 
             elif x.co.y < b:
                 b=x.co.y
             
             elif x.co.z < c:
                 c=x.co.z
                 
        for x in o.data.vertices:
             x.co.y-=b
             x.co.z-=c
             x.co.x-=a
             
        o.location.y+=b
        o.location.z+=c 
        o.location.x+=a            
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}



def register():

    bpy.utils.register_class(TP_Tileable_Camera)
    bpy.utils.register_class(TP_Tileable_Origin_XY)
    bpy.utils.register_class(TP_Tileable_Array_Scale)
    bpy.utils.register_class(TP_Tileable_Arrays)
    bpy.utils.register_class(TP_Tileable_Add_Vertices_Offset)

def unregister():

    bpy.utils.unregister_class(TP_Tileable_Camera)
    bpy.utils.unregister_class(TP_Tileable_Origin_XY)
    bpy.utils.unregister_class(TP_Tileable_Array_Scale)
    bpy.utils.unregister_class(TP_Tileable_Arrays)
    bpy.utils.unregister_class(TP_Tileable_Add_Vertices_Offset)

if __name__ == "__main__":
    register()



