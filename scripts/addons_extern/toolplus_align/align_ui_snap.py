


import bpy
from bpy import *
from bpy.props import *


def draw_align_snap_tools_panel_layout(self, context, layout):

        #icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)
    
        Display_Snap = context.user_preferences.addons[__package__].preferences.tab_snap 
        if Display_Snap == 'on':

            box = layout.box().column(1)           

            row = box.row(1)               
            row.operator("wm.context_toggle", text=" ", icon='MANIPUL').data_path = "space_data.show_manipulator" 
            row.operator("tp_ops.manipulator_all", " ", icon = 'NDOF_DOM')
            row.operator("tp_ops.manipulator_move", " ", icon = 'MAN_TRANS')                    
            row.operator("tp_ops.manipulator_rota", " ", icon = 'MAN_ROT')                    
            row.operator("tp_ops.manipulator_scale", " ", icon = 'MAN_SCALE')              

            row = box.row(1)
            if bpy.context.space_data.transform_orientation == 'GLOBAL':         
                row.operator("tp_ops.space_global", "Global", emboss = False)        
            else:        
                row.operator("tp_ops.space_global", "Global")        

            if bpy.context.space_data.transform_orientation == 'LOCAL':   
                row.operator("tp_ops.space_local", "Local", emboss = False)
            else:
                row.operator("tp_ops.space_local", "Local")

            if bpy.context.space_data.transform_orientation == 'NORMAL':   
                row.operator("tp_ops.space_normal", "Normal", emboss = False)
            else:    
                row.operator("tp_ops.space_normal", "Normal")

            if bpy.context.space_data.transform_orientation == 'GIMBAL':   
                row.operator("tp_ops.space_gimbal", "Gimbal", emboss = False)
            else:    
                row.operator("tp_ops.space_gimbal", "Gimbal")                 

            if bpy.context.space_data.transform_orientation == 'VIEW':   
                row.operator("tp_ops.space_view", "View", emboss = False)
            else:    
                row.operator("tp_ops.space_view", "View")    
            
            box.separator()
            box.separator()
                                       
            row = box.row(1)
            row.prop(context.tool_settings, "use_snap", text=" ")           

            if bpy.context.scene.tool_settings.snap_target == 'CLOSEST':         
                row.operator("tp_ops.snap_closest", "Closest", emboss = False)        
            else:        
                row.operator("tp_ops.snap_closest", "Closest")        

            if bpy.context.scene.tool_settings.snap_target == 'CENTER':
                row.operator("tp_ops.snap_center", "Center", emboss = False)
            else:
                row.operator("tp_ops.snap_center", "Center")

            if bpy.context.scene.tool_settings.snap_target == 'MEDIAN':
                row.operator("tp_ops.snap_median", "Median", emboss = False)
            else:    
                row.operator("tp_ops.snap_median", "Median")

            if bpy.context.scene.tool_settings.snap_target == 'ACTIVE':
                row.operator("tp_ops.snap_active", "Active", emboss = False)
            else:    
                row.operator("tp_ops.snap_active", "Active")


            row = box.row(1)
            
            if bpy.context.scene.tool_settings.snap_element == 'INCREMENT':                                    
                row.operator("tp_ops.snape_increment", " ", icon = "SNAP_INCREMENT", emboss = False)        
            else:
                row.operator("tp_ops.snape_increment", " ", icon = "SNAP_INCREMENT")        

            if bpy.context.scene.tool_settings.snap_element == 'VERTEX':            
                row.operator("tp_ops.snape_vertex", " ", icon = "SNAP_VERTEX", emboss = False)        
            else:
                row.operator("tp_ops.snape_vertex", " ", icon = "SNAP_VERTEX")        

            if bpy.context.scene.tool_settings.snap_element == 'EDGE':
                row.operator("tp_ops.snape_edge", " ", icon = "SNAP_EDGE", emboss = False)        
            else:
                row.operator("tp_ops.snape_edge", " ", icon = "SNAP_EDGE")        

            if bpy.context.scene.tool_settings.snap_element == 'FACE':
                row.operator("tp_ops.snape_face", " ", icon = "SNAP_FACE", emboss = False)
            else:
                row.operator("tp_ops.snape_face", " ", icon = "SNAP_FACE")

            if bpy.context.scene.tool_settings.snap_element == 'VOLUME':
                row.operator("tp_ops.snape_volume", " ", icon = "SNAP_VOLUME", emboss = False) 
            else:
                row.operator("tp_ops.snape_volume", " ", icon = "SNAP_VOLUME") 
            
            box.separator()
            box.separator()
            
            row = box.row(1) 
            row.alignment = 'CENTER' 
            
            if bpy.context.scene.tool_settings.snap_element == 'INCREMENT':          
                row.prop(context.tool_settings, "use_snap_grid_absolute", text="Snap Grid = Absolute", icon="SNAP_GRID")           

            if bpy.context.scene.tool_settings.snap_element in {'VERTEX', 'EDGE'}:  
                row.prop(context.tool_settings, "use_snap_align_rotation", text="Snap Vertex & Edge = Normal", icon="SNAP_NORMAL")           
                        
            if bpy.context.scene.tool_settings.snap_element in {'FACE'}: 
                row.prop(context.tool_settings, "use_snap_project", text="Snap Face = Project", icon="RETOPO")

            if bpy.context.scene.tool_settings.snap_element == 'VOLUME': 
                row.prop(context.tool_settings, "use_snap_peel_object", text="Snap Volume = Peel Object", icon="SNAP_PEEL_OBJECT")

            box.separator()
            

       
        Display_SnapSet = context.user_preferences.addons[__package__].preferences.tab_snapset 
        if Display_SnapSet == 'on':

            box = layout.box().column(1)           

            row = box.row(1)
            row.prop(context.scene, 'tp_snap_type',text=" ", expand =True)     

            row = box.row(1)
            row.operator('tp_ops.snap_set', text = "Execute Snapt Set", icon ="SNAP_SURFACE")     
                                        
            box.separator()
        
       
       
        Display_PropEdit = context.user_preferences.addons[__package__].preferences.tab_propedit 
        if Display_PropEdit == 'on':

            box = layout.box().column(1)           

            row = box.row(1)                   
            row.prop(context.tool_settings , "use_proportional_edit_objects","Proportional Edit", icon_only=True)
            
            sub = row.row(1)
            sub.scale_x = 0.5
            sub.prop(context.tool_settings , "proportional_edit_falloff", icon_only=True) 

            ###
            box.separator()           

        
        
        Display_View = context.user_preferences.addons[__package__].preferences.tab_view
        if Display_View == 'on':


            box = layout.box().column(1)           

            row = box.row(1)  
            row.operator("view3d.localview", text="Global/Local")
            row.operator("view3d.view_persportho", text="Persp/Ortho")             

            row = box.row(1) 
            sub = row.row(1)
            #sub.alignment = 'CENTER'         
            sub.scale_x = 0.25
            sub.operator("view3d.viewnumpad", text="F").type='FRONT'
            sub.operator("view3d.viewnumpad", text="B").type='BACK'
            sub.operator("view3d.viewnumpad", text="L").type='LEFT'
            sub.operator("view3d.viewnumpad", text="R").type='RIGHT'
            sub.operator("view3d.viewnumpad", text="T").type='TOP'
            sub.operator("view3d.viewnumpad", text="B").type='BOTTOM'

            ###
            box.separator()                         





class VIEW3D_TP_Align_Snap_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Align"
    bl_idname = "VIEW3D_TP_Align_Snap_Panel_TOOLS"
    bl_label = "Snap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.operator_context = 'INVOKE_AREA'

        draw_align_snap_tools_panel_layout(self, context, layout) 



class VIEW3D_TP_Align_Snap_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Align_Snap_Panel_UI"
    bl_label = "Snap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.operator_context = 'INVOKE_AREA'

        draw_align_snap_tools_panel_layout(self, context, layout) 

