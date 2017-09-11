import bpy, mathutils, math, re
from mathutils.geometry import intersect_line_plane
from mathutils import Vector
from math import radians
from bpy import*



class tp_ops_OriginObm(bpy.types.Operator):
    """set origin to selected / stay in objectmode"""                 
    bl_idname = "tp_ops.origin_obm"          
    bl_label = "origin to selected / in objectmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}
    

class tp_ops_OriginEdm(bpy.types.Operator):
    """set origin to selected / stay in editmode"""                 
    bl_idname = "tp_ops.origin_edm"          
    bl_label = "origin to selected in editmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class tp_ops_Origin_Edm_Cursor(bpy.types.Operator):
    """set origin to cursor / stay in editmode"""                 
    bl_idname = "tp_ops.origin_cursor_edm"          
    bl_label = "origin to cursor in editmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class tp_ops_Origin_Obm_Cursor(bpy.types.Operator):
    """set origin to cursor / stay in objectmode"""                 
    bl_idname = "tp_ops.origin_cursor_obm"          
    bl_label = "origin to cursor in objectmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}   



class PlaceOrigin(bpy.types.Operator):
    '''Set Origin'''
    bl_idname = "place.origin"
    bl_label = "Set Origin"
    bl_options = {"REGISTER", 'UNDO'}   

    geoto = bpy.props.BoolProperty(name="Geometry to Origin",  description="Place Origin", default = False)   
    orito = bpy.props.BoolProperty(name="Origin to Geometry",  description="Place Origin", default = False)   
    cursor = bpy.props.BoolProperty(name="Origin to 3D Cursor",  description="Place Origin", default = False)   
    mass = bpy.props.BoolProperty(name="Origin to MassCenter",  description="Place Origin", default = False)   
    mode_obm = bpy.props.BoolProperty(name="Switch Mode",  description="Switch the Mode", default = False)   
    cursor_edm = bpy.props.BoolProperty(name="Set to Cursor",  description="Set to Cursor", default = True)   
    mode = bpy.props.BoolProperty(name="Switch Mode",  description="Switch the Mode", default = False)   

    def draw(self, context):
        layout = self.layout.column(1)
        box = layout.box().column(1)

        row = box.column(1)         
        if context.mode == 'OBJECT':   
            row.prop(self, 'geoto')
            row.prop(self, 'orito')
            row.prop(self, 'cursor')
            row.prop(self, 'mass')
            row.prop(self, 'mode_obm')
        else:             
            row.prop(self, 'cursor_edm')
            row.prop(self, 'mode')

        #row.operator('wm.operator_defaults', text="Reset", icon ="RECOVER_AUTO")    

    def execute(self, context):
        

        if bpy.context.mode == 'OBJECT':
            
            for i in range(self.geoto):
                bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
            
            for i in range(self.orito):               
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            for i in range(self.cursor):
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
            for i in range(self.mass):
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        
            for i in range(self.mode_obm):
                bpy.ops.object.editmode_toggle()

        if bpy.context.mode == 'EDIT_MESH':
            
            for i in range(self.cursor_edm):            
                bpy.ops.view3d.snap_cursor_to_selected()
           
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.editmode_toggle()
            
            for i in range(self.mode):
                bpy.ops.object.editmode_toggle()
        
        return{'FINISHED'}
 
    def invoke(self, context, event):
        self.geoto
        self.orito
        self.cursor
        self.mass
        self.mode_obm
        self.mode
        return context.window_manager.invoke_props_dialog(self, width = 150)    

 



class BBox_Origin_Back(bpy.types.Operator):
    """BBox Origin Set :)"""
    bl_label = "BBox Origin Set :)"
    bl_idname = "bbox.ops_back"               
    bl_options = {'REGISTER', 'UNDO'}  
        
    #####
    Back_Left_Top = bpy.props.BoolProperty(name="Back-Left-Top",  description="Back-Left-Top", default=False)     
    Back_Top = bpy.props.BoolProperty(name="Back-Top",  description="Back-Top", default=False)     
    Back_Right_Top = bpy.props.BoolProperty(name="Back-Right-Top",  description="Back-Right-Top", default=False)     

    Back_Left = bpy.props.BoolProperty(name="Back-Left-Top",  description="Back-Left-Top", default=False)     
    Back = bpy.props.BoolProperty(name="Back-Top",  description="Back-Top", default=False)     
    Back_Right = bpy.props.BoolProperty(name="Back-Right-Top",  description="Back-Right-Top", default=False)  

    Back_Left_Bottom = bpy.props.BoolProperty(name="Back-Left-Bottom",  description="Back-Left-Bottom", default=False)     
    Back_Bottom = bpy.props.BoolProperty(name="Back-Bottom",  description="Back-Bottom", default=False)     
    Back_Right_Bottom = bpy.props.BoolProperty(name="Back-Right-Bottom",  description="Back-Right-Bottom", default=False)  

    #####
    Middle_Left_Top = bpy.props.BoolProperty(name="Middle-Left-Top",  description="Middle-Left-Top", default=False)     
    Top = bpy.props.BoolProperty(name="Top",  description="Top", default=False)     
    Middle_Right_Top = bpy.props.BoolProperty(name="Middle-Right-Top",  description="Middle-Right-Top", default=False)     

    Left = bpy.props.BoolProperty(name="Middle-Left-Top",  description="Middle-Left-Top", default=False)     
    Middle = bpy.props.BoolProperty(name="Middle",  description="Middle", default=False)        
    Right = bpy.props.BoolProperty(name="Middle-Right-Top",  description="Middle-Right-Top", default=False)  

    Middle_Left_Bottom = bpy.props.BoolProperty(name="Middle-Left-Bottom",  description="Middle-Left-Bottom", default=False)     
    Bottom = bpy.props.BoolProperty(name="Middle-Bottom",  description="Middle-Bottom", default=False)     
    Middle_Right_Bottom = bpy.props.BoolProperty(name="Middle-Right-Bottom",  description="Middle-Right-Bottom", default=False)  

    #####
    Front_Left_Top = bpy.props.BoolProperty(name="Front-Left-Top",  description="Front-Left-Top", default=False)     
    Front_Top = bpy.props.BoolProperty(name="Front-Top",  description="Front-Top", default=False)     
    Front_Right_Top = bpy.props.BoolProperty(name="Front-Right-Top",  description="Front-Right-Top", default=False)     

    Front_Left = bpy.props.BoolProperty(name="Front-Left-Top",  description="Front-Left-Top", default=False)     
    Front = bpy.props.BoolProperty(name="Front-Top",  description="Front-Top", default=False)     
    Front_Right = bpy.props.BoolProperty(name="Front-Right-Top",  description="Front-Right-Top", default=False)  

    Front_Left_Bottom = bpy.props.BoolProperty(name="Front-Left-Bottom",  description="Front-Left-Bottom", default=False)     
    Front_Bottom = bpy.props.BoolProperty(name="Front-Bottom",  description="Front-Bottom", default=False)     
    Front_Right_Bottom = bpy.props.BoolProperty(name="Front-Right-Bottom",  description="Front-Right-Bottom", default=False)  


    def draw(self, context):
        layout = self.layout
       
        box = layout.box().column(1)     
        box.scale_x = 0.1


        #####  
        
        row = box.row(1)                                     
        sub1 = row.row(1)

        sub1.alignment ='LEFT'         
        sub1.label(" +Y Axis")

        sub2 = row.row(1)
        sub2.alignment ='CENTER'         
        sub2.label("   xY Axis")

        sub3 = row.row(1)
        sub3.alignment ='RIGHT'         
        sub3.label("--Y Axis")



        #####  
        
        row = box.row(1)                                     
        sub1 = row.row(1)

        sub1.alignment ='LEFT' 
        
        sub1.prop(self, 'Back_Left_Top', text="", icon = "LAYER_ACTIVE")
        sub1.prop(self, 'Back_Top', text="", icon = "LAYER_ACTIVE")
        sub1.prop(self, 'Back_Right_Top', text="", icon = "LAYER_ACTIVE")

        sub2 = row.row(1)
        sub2.alignment ='CENTER' 
        
        sub2.prop(self, 'Middle_Left_Top', text="", icon = "LAYER_ACTIVE")
        sub2.prop(self, 'Top', text="", icon = "LAYER_ACTIVE")
        sub2.prop(self, 'Middle_Right_Top', text="", icon = "LAYER_ACTIVE")

        sub3 = row.row(1)
        sub3.alignment ='RIGHT' 
        
        sub3.prop(self, 'Front_Left_Top', text="", icon = "LAYER_ACTIVE")
        sub3.prop(self, 'Front_Top', text="", icon = "LAYER_ACTIVE")
        sub3.prop(self, 'Front_Right_Top', text="", icon = "LAYER_ACTIVE")
        

        #####

        row = box.row(1) 
         
        sub1 = row.row(1)
        sub1.alignment ='LEFT' 
        
        sub1.prop(self, 'Back_Left', text="", icon = "LAYER_ACTIVE")
        sub1.prop(self, 'Back', text="", icon = "LAYER_ACTIVE")
        sub1.prop(self, 'Back_Right', text="", icon = "LAYER_ACTIVE")

        sub2 = row.row(1)
        sub2.alignment ='CENTER' 

        sub2.prop(self, 'Left', text="", icon = "LAYER_ACTIVE")
        sub2.prop(self, 'Middle', text="", icon = "LAYER_ACTIVE")
        sub2.prop(self, 'Right', text="", icon = "LAYER_ACTIVE")

        sub3 = row.row(1)
        sub3.alignment ='RIGHT' 
        
        sub3.prop(self, 'Front_Left', text="", icon = "LAYER_ACTIVE")
        sub3.prop(self, 'Front', text="", icon = "LAYER_ACTIVE")
        sub3.prop(self, 'Front_Right', text="", icon = "LAYER_ACTIVE")


        #####

        row = box.row(1)
          
        sub1 = row.row(1)
        sub1.alignment ='LEFT' 
        
        sub1.prop(self, 'Back_Left_Bottom', text="", icon = "LAYER_ACTIVE")
        sub1.prop(self, 'Back_Bottom', text="", icon = "LAYER_ACTIVE")
        sub1.prop(self, 'Back_Right_Bottom', text="", icon = "LAYER_ACTIVE")

        sub2 = row.row(1)
        sub2.alignment ='CENTER' 

        sub2.prop(self, 'Middle_Left_Bottom', text="", icon = "LAYER_ACTIVE")
        sub2.prop(self, 'Bottom', text="", icon = "LAYER_ACTIVE")
        sub2.prop(self, 'Middle_Right_Bottom', text="", icon = "LAYER_ACTIVE")    

        sub3 = row.row(1)
        sub3.alignment ='RIGHT' 
        
        sub3.prop(self, 'Front_Left_Bottom', text="", icon = "LAYER_ACTIVE")
        sub3.prop(self, 'Front_Bottom', text="", icon = "LAYER_ACTIVE")
        sub3.prop(self, 'Front_Right_Bottom', text="", icon = "LAYER_ACTIVE")

        #####

        box = layout.box().column(1) 
         
        row = box.row(1)
        row.prop(context.object, "show_bounds", text="Show Bounds", icon='STICKY_UVS_LOC') 

        sub = row.row(1)
        sub.scale_x = 0.5  
        sub.prop(context.object, "draw_bounds_type", text="") 


    def execute(self, context):

        #Top         
        for i in range(self.Back_Left_Top):        
            bpy.ops.object.cubeback_cornertop_minus_xy()
        
        for i in range(self.Back_Top):   
            bpy.ops.object.cubeback_edgetop_minus_y()
        
        for i in range(self.Back_Right_Top):            
            bpy.ops.object.cubeback_cornertop_plus_xy()
             
        #Middle          
        for i in range(self.Back_Left):        
            bpy.ops.object.cubefront_edgemiddle_minus_x()
        
        for i in range(self.Back):            
            bpy.ops.object.cubefront_side_plus_y() 
        
        for i in range(self.Back_Right):            
            bpy.ops.object.cubefront_edgemiddle_plus_x()   
         
        #Bottom       
        for i in range(self.Back_Left_Bottom):        
            bpy.ops.object.cubeback_cornerbottom_minus_xy()
        
        for i in range(self.Back_Bottom):            
            bpy.ops.object.cubefront_edgebottom_plus_y() 
       
        for i in range(self.Back_Right_Bottom):            
            bpy.ops.object.cubeback_cornerbottom_plus_xy()  
                   

        #####

        #Top
        for i in range(self.Middle_Left_Top):
            bpy.ops.object.cubefront_edgetop_minus_x()

        for i in range(self.Top):
            bpy.ops.object.cubefront_side_plus_z()

        for i in range(self.Middle_Right_Top):
            bpy.ops.object.cubefront_edgetop_plus_x()              
         
        #Middle
        for i in range(self.Left):                   
            bpy.ops.object.cubefront_side_minus_x()
        
        for i in range(self.Middle):        
            if context.mode == "EDIT_MESH":
                bpy.ops.mesh.select_all(action='SELECT') 
                bpy.ops.view3d.snap_cursor_to_selected()
                bpy.ops.object.editmode_toggle() 
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
                bpy.ops.object.editmode_toggle()
            else:
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
              
        for i in range(self.Right):                         
            bpy.ops.object.cubefront_side_plus_x()              
    
        #Bottom
        for i in range(self.Middle_Left_Bottom):
            bpy.ops.object.cubefront_edgebottom_minus_x()

        for i in range(self.Bottom):           
            bpy.ops.object.cubefront_side_minus_z()             

        for i in range(self.Middle_Right_Bottom):           
            bpy.ops.object.cubefront_edgebottom_plus_x()  


        #####

        #Top                    
        for i in range(self.Front_Left_Top):
            bpy.ops.object.cubefront_cornertop_minus_xy()

        for i in range(self.Front_Top):
            bpy.ops.object.cubeback_edgetop_plus_y()

        for i in range(self.Front_Right_Top):
            bpy.ops.object.cubefront_cornertop_plus_xy()
                        

        #Middle                      
        for i in range(self.Front_Left):
            bpy.ops.object.cubefront_edgemiddle_minus_y()     

        for i in range(self.Front):
            bpy.ops.object.cubefront_side_minus_y()       

        for i in range(self.Front_Right):
            bpy.ops.object.cubefront_edgemiddle_plus_y()          


        #Bottom
        for i in range(self.Front_Left_Bottom):
            bpy.ops.object.cubefront_cornerbottom_minus_xy()             
       
        for i in range(self.Front_Bottom):
            bpy.ops.object.cubefront_edgebottom_minus_y()

        for i in range(self.Front_Right_Bottom):
            bpy.ops.object.cubefront_cornerbottom_plus_xy()
             
        return {'FINISHED'}

    def check(self, context):
        return True

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=300)




    
##################################
###  Origin to Corners on Top  ###
##################################

class Origin_CubeBack_CornerTop_Minus_XY(bpy.types.Operator):  
    bl_idname = "object.cubeback_cornertop_minus_xy"  
    bl_label = "Origin to -XY Corner / Top of Cubeback"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
                 x.co.y+=b
                 x.co.z+=c
                 x.co.x-=a

            o.location.y-=b 
            o.location.z-=c
            o.location.x+=a          
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
            
        else:
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
                 x.co.y+=b
                 x.co.z+=c
                 x.co.x-=a

            o.location.y-=b 
            o.location.z-=c
            o.location.x+=a          
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
        return {'FINISHED'}


class Origin_CubeBack_CornerTop_Plus_XY(bpy.types.Operator):  
    bl_idname = "object.cubeback_cornertop_plus_xy"  
    bl_label = "Origin to +XY Corner / Top of Cubeback"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':          
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
                 x.co.y+=b
                 x.co.z+=c
                 x.co.x+=a

            o.location.y-=b
            o.location.z-=c
            o.location.x-=a          
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.y+=b
                 x.co.z+=c
                 x.co.x+=a

            o.location.y-=b
            o.location.z-=c
            o.location.x-=a          
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
        return {'FINISHED'}


class Origin_CubeFront_CornerTop_Minus_XY(bpy.types.Operator):  
    bl_idname = "object.cubefront_cornertop_minus_xy"  
    bl_label = "Origin to -XY Corner / Top of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':           
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
                 x.co.z+=c
                 x.co.x-=a
                 
            o.location.y+=b 
            o.location.z-=c  
            o.location.x+=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.z+=c
                 x.co.x-=a
                 
            o.location.y+=b 
            o.location.z-=c  
            o.location.x+=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
        return {'FINISHED'}


class Origin_CubeFront_CornerTop_Plus_XY(bpy.types.Operator):  
    bl_idname = "object.cubefront_cornertop_plus_xy"  
    bl_label = "Origin to +XY Corner / Top of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
                 x.co.z+=c
                 x.co.x+=a
                 
            o.location.y+=b
            o.location.z-=c  
            o.location.x-=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.z+=c
                 x.co.x+=a
                 
            o.location.y+=b
            o.location.z-=c  
            o.location.x-=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
        return {'FINISHED'}

#####################################
###  Origin to Corners on Bottom  ###
#####################################

class Origin_CubeFront_CornerBottom_Minus_XY(bpy.types.Operator):  
    bl_idname = "object.cubefront_cornerbottom_minus_xy"  
    bl_label = "Origin to -XY Corner / Bottom of CubeFront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':           
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
            
        else:
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
            
        return {'FINISHED'}



class Origin_CubeFront_CornerBottom_Plus_XY(bpy.types.Operator):  
    bl_idname = "object.cubefront_cornerbottom_plus_xy"  
    bl_label = "Origin to +XY Corner / Bottom of CubeFront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
                 x.co.x+=a
                 
            o.location.y+=b 
            o.location.z+=c  
            o.location.x-=a              
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
            
        else:
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
                 x.co.x+=a
                 
            o.location.y+=b 
            o.location.z+=c  
            o.location.x-=a              
            bpy.ops.object.mode_set(mode = 'EDIT')
            
        return {'FINISHED'}


class Origin_CubeBack_CornerBottom_Minus_XY(bpy.types.Operator):  
    bl_idname = "object.cubeback_cornerbottom_minus_xy"  
    bl_label = "Origin to -XY Corner / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
                 x.co.y+=b
                 x.co.z-=c
                 x.co.x-=a
                 
            o.location.y-=b 
            o.location.z+=c  
            o.location.x+=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
            
        else:
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
                 x.co.y+=b
                 x.co.z-=c
                 x.co.x-=a
                 
            o.location.y-=b 
            o.location.z+=c  
            o.location.x+=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')            
     
        return {'FINISHED'}


class Origin_CubeBack_CornerBottom_Plus_XY(bpy.types.Operator):  
    bl_idname = "object.cubeback_cornerbottom_plus_xy"  
    bl_label = "Origin to +XY Corner / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
                 x.co.y+=b
                 x.co.z-=c
                 x.co.x+=a
                 
            o.location.y-=b 
            o.location.z+=c  
            o.location.x-=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
            
        else:
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
                 x.co.y+=b
                 x.co.z-=c
                 x.co.x+=a
                 
            o.location.y-=b 
            o.location.z+=c  
            o.location.x-=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')
            
        return {'FINISHED'}




###############################################
###  Origin to the Middle of the Top Edges  ###
###############################################


class Origin_CubeBack_EdgeTop_Minus_Y(bpy.types.Operator):  
    bl_idname = "object.cubeback_edgetop_minus_y"  
    bl_label = "Origin to -Y Edge / Top of Cubeback"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':          
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
                 x.co.y+=b
                 x.co.z+=c 
                             
            o.location.y-=b 
            o.location.z-=c                 
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
            
        else:
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
                 x.co.y+=b
                 x.co.z+=c 
                             
            o.location.y-=b 
            o.location.z-=c                 
            bpy.ops.object.mode_set(mode = 'EDIT')
            
        return {'FINISHED'}



class Origin_CubeBack_EdgeTop_Plus_Y(bpy.types.Operator):  
    bl_idname = "object.cubeback_edgetop_plus_y"  
    bl_label = "Origin to +Y Edge / Top of Cubeback"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
                 x.co.z+=c 
                             
            o.location.y+=b 
            o.location.z-=c                  
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
            
        else:
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
                 x.co.z+=c 
                             
            o.location.y+=b 
            o.location.z-=c                  
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
            
        return {'FINISHED'}



class Origin_CubeFront_EdgeTop_Minus_X(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgetop_minus_x"  
    bl_label = "Origin to -X Edge / Top of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':          
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
                 x.co.x-=a
                 x.co.z+=c 
                             
            o.location.x+=a 
            o.location.z-=c                     
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
            
        else:
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
                 x.co.x-=a
                 x.co.z+=c 
                             
            o.location.x+=a 
            o.location.z-=c                     
            bpy.ops.object.mode_set(mode = 'EDIT')            

            
        return {'FINISHED'}


class Origin_CubeFront_EdgeTop_Plus_X(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgetop_plus_x"  
    bl_label = "Origin to +X Edge / Top of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':          
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
                 x.co.x+=a
                 x.co.z+=c 
                             
            o.location.x-=a 
            o.location.z-=c                   
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
            
        else:
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
                 x.co.x+=a
                 x.co.z+=c 
                             
            o.location.x-=a 
            o.location.z-=c                   
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
        return {'FINISHED'}




##################################################
###  Origin to the Middle of the Bottom Edges  ###
##################################################


class Origin_CubeFront_EdgeBottom_Minus_Y(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgebottom_minus_y"  
    bl_label = "Origin to -Y Edge / Bottom of CubeFront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':          
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
                             
            o.location.y+=b 
            o.location.z+=c              
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                             
            o.location.y+=b 
            o.location.z+=c              
            bpy.ops.object.mode_set(mode = 'EDIT')

            
        return {'FINISHED'}


class Origin_CubeFront_EdgeBottom_Plus_Y(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgebottom_plus_y"  
    bl_label = "Origin to +Y Edge / Bottom of CubeFront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
                 x.co.y+=b
                 x.co.z-=c 
                             
            o.location.y-=b 
            o.location.z+=c           
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.y+=b
                 x.co.z-=c 
                             
            o.location.y-=b 
            o.location.z+=c           
            bpy.ops.object.mode_set(mode = 'EDIT')            

            
        return {'FINISHED'}


class Origin_CubeFront_EdgeBottom_Minus_X(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgebottom_minus_x"  
    bl_label = "Origin to -X Edge / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':           
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
                 x.co.x-=a
                 x.co.z-=c 
                             
            o.location.x+=a 
            o.location.z+=c                    
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.x-=a
                 x.co.z-=c 
                             
            o.location.x+=a 
            o.location.z+=c                    
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
        return {'FINISHED'}


class Origin_CubeFront_EdgeBottom_Plus_X(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgebottom_plus_x"  
    bl_label = "Origin to +X Edge / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
                 x.co.x+=a
                 x.co.z-=c
                             
            o.location.x-=a 
            o.location.z+=c                    
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.x+=a
                 x.co.z-=c
                             
            o.location.x-=a 
            o.location.z+=c                    
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
        return {'FINISHED'}




################################################
###  Origin to the Middle of the Side Edges  ###
################################################


class Origin_CubeFront_EdgeMiddle_Minus_Y(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgemiddle_minus_y"  
    bl_label = "Origin to -Y Edge / Middle of CubeFront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':           
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
                 x.co.x-=a 
                             
            o.location.y+=b 
            o.location.x+=a              
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.x-=a 
                             
            o.location.y+=b 
            o.location.x+=a              
            bpy.ops.object.mode_set(mode = 'EDIT')                        
            
        return {'FINISHED'}


class Origin_CubeFront_EdgeMiddle_Plus_Y(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgemiddle_plus_y"  
    bl_label = "Origin to +Y Edge / Middle of CubeFront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':            
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
                 x.co.x+=a 
                             
            o.location.y+=b 
            o.location.x-=a            
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.x+=a 
                             
            o.location.y+=b 
            o.location.x-=a            
            bpy.ops.object.mode_set(mode = 'EDIT')            

            
        return {'FINISHED'}



class Origin_CubeFront_EdgeMiddle_Minus_X(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgemiddle_minus_x"  
    bl_label = "Origin to -X Edge / Middle of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':           
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
                 x.co.y+=b
                 x.co.x-=a 
                             
            o.location.y-=b 
            o.location.x+=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.y+=b
                 x.co.x-=a 
                             
            o.location.y-=b 
            o.location.x+=a                    
            bpy.ops.object.mode_set(mode = 'EDIT')            

            
        return {'FINISHED'}


class Origin_CubeFront_EdgeMiddle_Plus_X(bpy.types.Operator):  
    bl_idname = "object.cubefront_edgemiddle_plus_x"  
    bl_label = "Origin to +X Edge / Middle of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':          
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
                 x.co.y+=b
                 x.co.x+=a 
                             
            o.location.y-=b 
            o.location.x-=a                  
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
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
                 x.co.y+=b
                 x.co.x+=a 
                             
            o.location.y-=b 
            o.location.x-=a                  
            bpy.ops.object.mode_set(mode = 'EDIT')
    
            
        return {'FINISHED'}



######################################
###  Origin to the Middle of Side  ### 
######################################


class Origin_CubeFront_Side_Minus_Y(bpy.types.Operator):  
    bl_idname = "object.cubefront_side_minus_y"  
    bl_label = "Origin to -Y Edge / Bottom of CubeFront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':          
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.y
                     init=1
                 elif x.co.y<a:
                     a=x.co.y
                     
            for x in o.data.vertices:
                 x.co.y-=a
                             
            o.location.y+=a             
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()
        
        else:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.y
                     init=1
                 elif x.co.y<a:
                     a=x.co.y
                     
            for x in o.data.vertices:
                 x.co.y-=a
                             
            o.location.y+=a             
            bpy.ops.object.mode_set(mode = 'EDIT')            
            
        return {'FINISHED'}



class Origin_CubeFront_Side_Plus_Y(bpy.types.Operator):  
    bl_idname = "object.cubefront_side_plus_y"  
    bl_label = "Origin to +Y Edge / Bottom of CubeFront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':          
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.y
                     init=1
                 elif x.co.y<a:
                     a=x.co.y
                     
            for x in o.data.vertices:
                 x.co.y+=a
                             
            o.location.y-=a             
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.y
                     init=1
                 elif x.co.y<a:
                     a=x.co.y
                     
            for x in o.data.vertices:
                 x.co.y+=a
                             
            o.location.y-=a             
            bpy.ops.object.mode_set(mode = 'EDIT')                        
            
        return {'FINISHED'}


class Origin_CubeFront_Side_Minus_X(bpy.types.Operator):  
    bl_idname = "object.cubefront_side_minus_x"  
    bl_label = "Origin to -X Edge / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':           
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.x
                     init=1
                 elif x.co.x<a:
                     a=x.co.x
                     
            for x in o.data.vertices:
                 x.co.x-=a
                             
            o.location.x+=a                   
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.x
                     init=1
                 elif x.co.x<a:
                     a=x.co.x
                     
            for x in o.data.vertices:
                 x.co.x-=a
                             
            o.location.x+=a                   
            bpy.ops.object.mode_set(mode = 'EDIT')

        return {'FINISHED'}



class Origin_CubeFront_Side_Plus_X(bpy.types.Operator):  
    bl_idname = "object.cubefront_side_plus_x"  
    bl_label = "Origin to +X Edge / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':           
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.x
                     init=1
                 elif x.co.x<a:
                     a=x.co.x
                     
            for x in o.data.vertices:
                 x.co.x+=a
                             
            o.location.x-=a                   
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.x
                     init=1
                 elif x.co.x<a:
                     a=x.co.x
                     
            for x in o.data.vertices:
                 x.co.x+=a
                             
            o.location.x-=a                   
            bpy.ops.object.mode_set(mode = 'EDIT')
            
            
        return {'FINISHED'}


class Origin_CubeFront_Side_Minus_Z(bpy.types.Operator):  
    bl_idname = "object.cubefront_side_minus_z"  
    bl_label = "Origin to -Z Edge / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
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
        
            
        return {'FINISHED'}



class Origin_CubeFront_Side_Plus_Z(bpy.types.Operator):  
    bl_idname = "object.cubefront_side_plus_z"  
    bl_label = "Origin to +Z Edge / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':        
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


            
        
        return {'FINISHED'}









