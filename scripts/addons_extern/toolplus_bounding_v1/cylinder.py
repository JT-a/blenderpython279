bl_info = {
"name": "T+ Bounding Cylinder", 
"author": "marvink.k.breuer (MKB)",
"version": (1, 0),
"blender": (2, 78, 0),
"location": "View3D > TAB Tools > Panel Bounding",
"description": "create a bounding cylinder around selected object",
"warning": "",
"wiki_url": "",
"tracker_url": "",
"category": "ToolPlus"}



import bpy
from bpy import *
from bpy.props import *

def cyl_06(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=6)

def cyl_08(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=8)

def cyl_10(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=10)

def cyl_12(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=12)

def cyl_14(context):     
    bpy.ops.mesh.primitive_cylinder_add(vertices=14)

def cyl_16(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16)

def cyl_18(context):     
    bpy.ops.mesh.primitive_cylinder_add(vertices=18)    

def cyl_20(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=20)

def cyl_22(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=22)
    
def cyl_24(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=24)
    
def cyl_26(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=26)

def cyl_28(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=28)

def cyl_30(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=30) 
       
def cyl_32(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=32)
                
def cyl_34(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=34)
      
def cyl_36(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=36)

def cyl_38(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=38)
            
def cyl_40(context):    
    bpy.ops.mesh.primitive_cylinder_add(vertices=40)


      
class VIEW3D_TP_BCylinder_for_Menu(bpy.types.Operator):
    """bounding cylinder with different value of vertices"""
    bl_idname = "tp_ops.bcylinder_for_menu"
    bl_label = "Bounding Cylinder"
    bl_options = {'REGISTER', 'UNDO'}

    tp_cyl = bpy.props.EnumProperty(
        items=[("tp_06"    ,"06"   ,"06"),
               ("tp_08"    ,"08"   ,"08"),
               ("tp_10"    ,"10"   ,"10"),
               ("tp_12"    ,"12"   ,"12"),
               ("tp_14"    ,"14"   ,"14"),
               ("tp_16"    ,"16"   ,"16"),
               ("tp_18"    ,"18"   ,"18"),
               ("tp_20"    ,"20"   ,"20"),
               ("tp_22"    ,"22"   ,"22"),
               ("tp_24"    ,"24"   ,"24"),
               ("tp_26"    ,"26"   ,"26"),
               ("tp_28"    ,"28"   ,"28"),
               ("tp_30"    ,"30"   ,"30"),
               ("tp_32"    ,"32"   ,"32"),
               ("tp_34"    ,"34"   ,"34"),
               ("tp_36"    ,"36"   ,"36"),
               ("tp_38"    ,"38"   ,"38"),
               ("tp_40"    ,"40"   ,"40")],
               name = "Subdiv ",
               default = "tp_08",    
               description = "change vertex value")

    bcyl_smooth = bpy.props.BoolProperty(name="Smooth",  description="Smooth Mesh", default=False)    
    bcyl_wire = bpy.props.BoolProperty(name="Wire only",  description="Only Wire Mesh", default=False)   
    bcyl_shade = bpy.props.BoolProperty(name="Shade off",  description="Mesh Shading off", default=False)   
    bcyl_origin = bpy.props.BoolProperty(name="Origin > Center",  description="Origin > Center", default=True)                                

    def execute(self, context):
        selected = bpy.context.selected_objects
        
        #set cursor to selected
        bpy.ops.view3d.snap_cursor_to_selected()
        
        for obj in selected:
            
            #set origin to bounding box center
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

            #create cylinder with different value of vertices
            
            if self.tp_cyl == "tp_06":
                cyl_06(context)     
                
            if self.tp_cyl == "tp_08":
                cyl_08(context)    

            if self.tp_cyl == "tp_10":
                cyl_10(context)                
            
            if self.tp_cyl == "tp_12":
                cyl_12(context)    

            if self.tp_cyl == "tp_14":
                cyl_14(context)    
                
            if self.tp_cyl == "tp_16":
                cyl_16(context)    

            if self.tp_cyl == "tp_18":
                cyl_18(context)    
                
            if self.tp_cyl == "tp_20":
                cyl_20(context)                    
                
            if self.tp_cyl == "tp_22":
                cyl_22(context)    

            if self.tp_cyl == "tp_24":
                cyl_24(context)                    

            if self.tp_cyl == "tp_26":
                cyl_26(context)    

            if self.tp_cyl == "tp_28":
                cyl_28(context)    

            if self.tp_cyl == "tp_30":
                cyl_30(context)    

            if self.tp_cyl == "tp_32":
                cyl_32(context)  

            if self.tp_cyl == "tp_34":
                cyl_34(context)  
                                                
            if self.tp_cyl == "tp_36":
                cyl_36(context)  

            if self.tp_cyl == "tp_38":
                cyl_38(context)  
            
            if self.tp_cyl == "tp_40":
                cyl_40(context)  

            bpy.context.object.name = "_bcyl"

            #keep it as active object
            bound_cyl = bpy.context.active_object 
            
            #copy dimensions to it
            bound_cyl.dimensions = obj.dimensions
            bound_cyl.location = obj.location
            bound_cyl.rotation_euler = obj.rotation_euler
                 
            for i in range(self.bcyl_origin): 
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

            for i in range(self.bcyl_shade): 
                bpy.context.object.draw_type = 'WIRE'

            for i in range(self.bcyl_smooth):
                bpy.ops.object.shade_smooth()

            for i in range(self.bcyl_wire): 
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.delete(type='ONLY_FACE')
                bpy.ops.object.editmode_toggle()

             
        return {'FINISHED'}

            
    def invoke(self, context, event):             
        self.tp_cyl        
        self.bcyl_smooth 
        self.bcyl_wire           
        self.bcyl_shade
        self.bcyl_origin                
        return context.window_manager.invoke_props_dialog(self, width = 300) 




class VIEW3D_TP_BCylinder_for_Panel(bpy.types.Operator):
    """bounding cylinder with different value of vertices"""
    bl_idname = "tp_ops.bcylinder_for_panel"
    bl_label = "Bounding Cylinder"
    bl_options = {'REGISTER', 'UNDO'}

    bpy.types.Scene.tp_cyl = bpy.props.EnumProperty(
        items=[("tp_06"    ,"05"   ,"05"),
               ("tp_08"    ,"08"   ,"08"),
               ("tp_10"    ,"10"   ,"10"),
               ("tp_12"    ,"12"   ,"12"),
               ("tp_14"    ,"14"   ,"14"),
               ("tp_16"    ,"16"   ,"16"),
               ("tp_18"    ,"18"   ,"18"),
               ("tp_20"    ,"20"   ,"20"),
               ("tp_22"    ,"22"   ,"22"),
               ("tp_24"    ,"24"   ,"24"),
               ("tp_26"    ,"26"   ,"26"),
               ("tp_28"    ,"28"   ,"28"),
               ("tp_30"    ,"30"   ,"30"),
               ("tp_32"    ,"32"   ,"32"),
               ("tp_34"    ,"34"   ,"34"),
               ("tp_36"    ,"36"   ,"36"),
               ("tp_38"    ,"38"   ,"38"),
               ("tp_40"    ,"40"   ,"40")],
               name = "Subdiv",
               default = "tp_08",    
               description = "change vertex value")

    bpy.types.Scene.bcyl_smooth = bpy.props.BoolProperty(name="Smooth",  description="Smooth Mesh", default=False)      
    bpy.types.Scene.bcyl_wire = bpy.props.BoolProperty(name="Wire only",  description="Only Wire Mesh", default=False)   
    bpy.types.Scene.bcyl_shade = bpy.props.BoolProperty(name="Shade off",  description="Mesh Shading on/off", default=False)  
    bpy.types.Scene.bcyl_origin = bpy.props.BoolProperty(name="Origin > Center",  description="Origin > Center", default=True)   
                                                       
    def execute(self, context):
        selected = bpy.context.selected_objects
        
        #set cursor to selected
        bpy.ops.view3d.snap_cursor_to_selected()
        
        for obj in selected:
            
            #set origin to bounding box center
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

            #create cylinder with different value of vertices

            if context.scene.tp_cyl == "tp_06":
                cyl_06(context)     
                
            if context.scene.tp_cyl == "tp_08":
                cyl_08(context)    

            if context.scene.tp_cyl == "tp_10":
                cyl_10(context)                
            
            if context.scene.tp_cyl == "tp_12":
                cyl_12(context)    

            if context.scene.tp_cyl == "tp_14":
                cyl_14(context)    
                
            if context.scene.tp_cyl == "tp_16":
                cyl_16(context)    

            if context.scene.tp_cyl == "tp_18":
                cyl_18(context)    
                
            if context.scene.tp_cyl == "tp_20":
                cyl_20(context)                    
                
            if context.scene.tp_cyl == "tp_22":
                cyl_22(context)    

            if context.scene.tp_cyl == "tp_24":
                cyl_24(context)                    

            if context.scene.tp_cyl == "tp_26":
                cyl_26(context)    

            if context.scene.tp_cyl == "tp_28":
                cyl_28(context)    

            if context.scene.tp_cyl == "tp_30":
                cyl_30(context)    

            if context.scene.tp_cyl == "tp_32":
                cyl_32(context)  

            if context.scene.tp_cyl == "tp_34":
                cyl_34(context)  
                                                
            if context.scene.tp_cyl == "tp_36":
                cyl_36(context)  

            if context.scene.tp_cyl == "tp_38":
                cyl_38(context)  
            
            if context.scene.tp_cyl == "tp_40":
                cyl_40(context)  

            bpy.context.object.name = "_bcyl"    
                                                        
            #keep it as active object
            bound_cyl = bpy.context.active_object 
            
            #copy dimensions to it
            bound_cyl.dimensions = obj.dimensions
            bound_cyl.location = obj.location
            bound_cyl.rotation_euler = obj.rotation_euler


            for i in range(context.scene.bcyl_smooth):
                bpy.ops.object.shade_smooth()
                 
            for i in range(context.scene.bcyl_origin): 
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

            for i in range(context.scene.bcyl_wire): 
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.delete(type='ONLY_FACE')
                bpy.ops.object.editmode_toggle()
                
            for i in range(context.scene.bcyl_shade): 
                bpy.context.object.draw_type = 'WIRE'

                
        return {'FINISHED'}



def register():
    bpy.utils.register_module(__name__) 
    
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()






