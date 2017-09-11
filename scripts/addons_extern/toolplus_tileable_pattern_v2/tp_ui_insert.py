import bpy 
#from . icons.icons import load_icons
from bpy.props import*



class View3D_TP_Tileable_Insert_Panel(bpy.types.Panel):
    bl_category = "T+"
    bl_idname = "OBJECT_TP_Tileable_Insert_Panel"
    bl_label = "Insert"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_region_type = 'UI'    
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return isModelingMode
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        
        #icons = load_icons()


        if context.mode == "OBJECT":

            box = layout.box().column(1)  
            
            row = box.row(1)          
            row.label(text="Pattern", icon = "MOD_BUILD")      

            box.separator()
                     
            row = box.column(1) 
            row.operator("tp_ops.reference_grid","Refz Grid", icon = "MOD_LATTICE")
            row.operator("tp_ops.instances_fields","Add Planes", icon = "MESH_GRID")
            row.operator("tp_ops.instances_curves","Add Curves", icon = "SURFACE_NCIRCLE")

            box.separator()


            box = layout.box().column(1)  

            row = box.row(1)        
            row.alignment = 'CENTER' 

            sub = row.row(1)
            sub.scale_x = 0.35
            sub.scale_y = 0.35
            sub.template_icon_view(context.window_manager , "TP_Tileable_Curve_Previews")        

            sub = row.row(1)
            sub.scale_x = 0.35
            sub.scale_y = 0.35
            sub.template_icon_view(context.window_manager , "TP_Tileable_Mesh_Previews")

            box.separator()


            """ Primitives """
        
            box = layout.box().column(1)       
           
            row = box.row(1) 
            row.label(text="Mesh:")

            row = box.row(1) 
            row.operator("mesh.primitive_plane_add",icon='MESH_PLANE',text="")
            row.operator("mesh.primitive_cube_add",icon='MESH_CUBE',text="")
            row.operator("mesh.primitive_circle_add",icon='MESH_CIRCLE',text="")
            row.operator("mesh.primitive_uv_sphere_add",icon='MESH_UVSPHERE',text="")
            row.operator("mesh.primitive_ico_sphere_add",icon='MESH_ICOSPHERE',text="")

            row = box.row(1) 
            row.operator("mesh.primitive_grid_add",icon='MESH_GRID',text="")
            row.operator("mesh.primitive_monkey_add",icon='MESH_MONKEY',text="")
            row.operator("mesh.primitive_cylinder_add",icon='MESH_CYLINDER',text="")
            row.operator("mesh.primitive_torus_add",icon='MESH_TORUS',text="")
            row.operator("mesh.primitive_cone_add",icon='MESH_CONE',text="")

            box.separator()
            
        
            """ Add Curve """

            row = box.row(1) 
            row.label(text="Curve / Nurbs:")
       
            row = box.row(1) 
            row.operator("curve.primitive_bezier_curve_add",icon='CURVE_BEZCURVE',text="")
            row.operator("curve.primitive_bezier_circle_add",icon='CURVE_BEZCIRCLE',text="")
            row.operator("curve.primitive_nurbs_curve_add",icon='CURVE_NCURVE',text="")
            row.operator("curve.primitive_nurbs_circle_add",icon='CURVE_NCIRCLE',text="")
            row.operator("curve.primitive_nurbs_path_add",icon='CURVE_PATH',text="")
            
            box.separator()


            """ Add Surface """    
            
            row = box.row(1) 
            row.label(text="Surface:")    
      
            row = box.row(1) 
            row.operator("surface.primitive_nurbs_surface_circle_add",icon='SURFACE_NCIRCLE',text="")
            row.operator("surface.primitive_nurbs_surface_surface_add",icon='SURFACE_NSURFACE',text="")
            row.operator("surface.primitive_nurbs_surface_cylinder_add",icon='SURFACE_NCYLINDER',text="")
            row.operator("surface.primitive_nurbs_surface_sphere_add",icon='SURFACE_NSPHERE',text="")
            row.operator("surface.primitive_nurbs_surface_torus_add",icon='SURFACE_NTORUS',text="")

            box.separator()


            """ Lamp """
            
            box = layout.box().column(1)       
            
            row = box.row(1) 
            row.label(text="Lamp:")
                         
            row = box.row(1) 
            row.operator("object.lamp_add", text="", icon="LAMP_POINT").type='POINT'
            row.operator("object.lamp_add", text="", icon="LAMP_SUN").type='SUN'
            row.operator("object.lamp_add", text="", icon="LAMP_SPOT").type='SPOT'
            row.operator("object.lamp_add", text="", icon="LAMP_HEMI").type='HEMI'
            row.operator("object.lamp_add", text="", icon="LAMP_AREA").type='AREA'        

            box.separator()
            
            
            """ Helper """
            
            box = layout.box().column(1)       
           
            row = box.row(1) 
            row.label(text="Helper:")               
   
            row = box.row(1) 
            row.operator("object.speaker_add",icon='OUTLINER_OB_SPEAKER',text="")
            row.operator("object.camera_add",icon='OUTLINER_OB_CAMERA',text="")
            row.operator("object.metaball_add", text="", icon="OUTLINER_OB_META")          
            row.operator("object.armature_add",text="", icon="OUTLINER_OB_ARMATURE") 

            row = box.row(1) 
            row.operator("object.text_add", text="", icon ="OUTLINER_OB_FONT")                                   
            row.operator("object.empty_add", text="", icon="OUTLINER_OB_MESH")         
            row.operator("object.add",text="",icon="OUTLINER_OB_LATTICE").type="LATTICE"
            row.operator("object.empty_add", text="", icon="OUTLINER_OB_EMPTY").type="PLAIN_AXES"

            box.separator()


            """ Dropdown """

            box = layout.box().column(1)       

            row = box.row(1) 
            row.menu("INFO_MT_add",text="All", icon="OBJECT_DATAMODE")         
            row.menu("INFO_MT_curve_add",icon='PLUGIN',text="Curve")
                 
            row = box.row(1) 
            row.menu("INFO_MT_surface_add",icon='PLUGIN',text="Surface")
            row.menu("INFO_MT_mesh_add",icon='PLUGIN',text="Mesh")
            

            if len(bpy.data.groups) > 10:
                box = layout.box().column(1)       
                
                row = box.row(1) 
                row.operator_context = 'INVOKE_REGION_WIN'
                row.operator("object.group_instance_add", text="Group Instance...", icon='OUTLINER_OB_EMPTY')
           
            else:
                box = layout.box().column(1)       
               
                row = box.row(1) 
                row.operator_menu_enum("object.group_instance_add", "group", text="Group Instance", icon='OUTLINER_OB_EMPTY')                              
                row.operator("view3d.snap_cursor_to_center", "", icon="OUTLINER_DATA_EMPTY")    


        if context.mode == 'EDIT_MESH': 

            box = layout.box().column(1)       
            row = box.row(1) 
            row.alignment = 'CENTER'               
            sub = row.row(1)
            sub.scale_x = 1.9  
            sub.operator("mesh.primitive_plane_add",icon='MESH_PLANE',text="")
            sub.operator("mesh.primitive_cube_add",icon='MESH_CUBE',text="")
            sub.operator("mesh.primitive_circle_add",icon='MESH_CIRCLE',text="")
            sub.operator("mesh.primitive_uv_sphere_add",icon='MESH_UVSPHERE',text="")
            sub.operator("mesh.primitive_ico_sphere_add",icon='MESH_ICOSPHERE',text="")        
                             
            row = box.row(1)  
            row.alignment = 'CENTER'                        
            sub = row.row(1)
            sub.scale_x = 1.9 
            sub.operator("mesh.primitive_cylinder_add",icon='MESH_CYLINDER',text="")
            sub.operator("mesh.primitive_torus_add",icon='MESH_TORUS',text="")
            sub.operator("mesh.primitive_cone_add",icon='MESH_CONE',text="")
            sub.operator("mesh.primitive_grid_add",icon='MESH_GRID',text="")
            sub.operator("mesh.primitive_monkey_add",icon='MESH_MONKEY',text="") 
             

        if context.mode == 'EDIT_CURVE':         

             box = layout.box() 
             row = box.row(1)         
             row.alignment = 'CENTER'               

             sub = row.row(1)
             sub.scale_x = 1.2      
             sub.operator("curve.primitive_bezier_curve_add",icon='CURVE_BEZCURVE',text="")
             sub.operator("curve.primitive_bezier_circle_add",icon='CURVE_BEZCIRCLE',text="")
             sub.operator("curve.primitive_nurbs_curve_add",icon='CURVE_NCURVE',text="")
             sub.operator("curve.primitive_nurbs_circle_add",icon='CURVE_NCIRCLE',text="")
             sub.operator("curve.primitive_nurbs_path_add",icon='CURVE_PATH',text="")          
             sub.operator("curve.draw", icon='LINE_DATA',text="")             
             

        if context.mode == 'EDIT_SURFACE':
             
            box = layout.box()
            row = box.row(1) 
            row.alignment = 'CENTER'               
            sub = row.row(1)
            sub.scale_x = 1.2   

            sub.operator("surface.primitive_nurbs_surface_curve_add",icon='SURFACE_NCURVE',text="") 
            sub.operator("surface.primitive_nurbs_surface_circle_add",icon='SURFACE_NCIRCLE',text="")
            sub.operator("surface.primitive_nurbs_surface_surface_add",icon='SURFACE_NSURFACE',text="")
            sub.operator("surface.primitive_nurbs_surface_cylinder_add",icon='SURFACE_NCYLINDER',text="")
            sub.operator("surface.primitive_nurbs_surface_sphere_add",icon='SURFACE_NSPHERE',text="")
            sub.operator("surface.primitive_nurbs_surface_torus_add",icon='SURFACE_NTORUS',text="")   


        if context.mode == 'EDIT_METABALL':   
                     
            box = layout.box()        
            row = box.row(1)   
            row.alignment = 'CENTER'               
            sub = row.row(1)
            sub.scale_x = 1.2 
                   
            sub.operator("object.metaball_add",icon='META_BALL',text="").type = "BALL"
            sub.operator("object.metaball_add",icon='META_CAPSULE',text="").type = "CAPSULE"
            sub.operator("object.metaball_add",icon='META_PLANE',text="").type = "PLANE"
            sub.operator("object.metaball_add",icon='META_ELLIPSOID',text="").type = "ELLIPSOID"                
            sub.operator("object.metaball_add",icon='META_CUBE',text="").type = "CUBE"         
             
             
        if context.mode == 'EDIT_ARMATURE': 
                      
            box = layout.box().column(1)
            
            row = box.row(1) 
            row.alignment = 'CENTER'               
             
            row.operator("armature.bone_primitive_add",text="Single Bone",icon="BONE_DATA")         
            
          

