import bpy
from bpy import *
from bpy.props import *
from .icons.icons import load_icons

EDIT = ["EDIT_MESH","EDIT_CURVE", "EDIT_SURFACE", "EDIT_LATTICE", "EDIT_METABALL", "EDIT_TEXT", "EDIT_ARMATURE", "POSE"]
GEOM = ['POSE', 'LAMP', 'CAMERA', 'EMPTY', 'SPEAKER']

class VIEW3D_TP_BBOX_MESHES_TOOLS(bpy.types.Panel):
    bl_category = "T+"
    bl_idname = "VIEW3D_TP_BBOX_MESHES_TOOLS"
    bl_label = "Bounding"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        obj = context.active_object     
        if obj:
            obj_type = obj.type                                                                
            if obj_type not in GEOM:
                return isModelingMode and context.mode not in EDIT
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_bounding_panel_layout(context, layout) 



class VIEW3D_TP_BBOX_MESHES_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_BBOX_MESHES_UI"
    bl_label = "Bounding"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        obj = context.active_object     
        if obj:
            obj_type = obj.type                                                                
            if obj_type not in GEOM:
                return isModelingMode and context.mode not in EDIT

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_bounding_panel_layout(context, layout) 






def draw_bounding_panel_layout(context, layout):
    tp_props = context.window_manager.bbox_window
    
    icons = load_icons()     
    
    layout.operator_context = 'INVOKE_REGION_WIN'
    
    icons = load_icons()
   

    col = layout.column(1)                                                
    box = col.box().column(1)

    row = box.row(1) 
    button_bbox = icons.get("icon_bbox") 
    row.operator("tp_ops.bbox_for_menu", text="", icon_value=button_bbox.icon_id)  
    row.operator("tp_ops.bbox_for_panel",text="Bounding Box")  
   
    box.separator() 
    
    row = box.row(1)

    if tp_props.display_bbox_set: 
        row.prop(tp_props, "display_bbox_set", text="", icon="SCRIPTPLUGINS") 
    else:                  
        row.prop(tp_props, "display_bbox_set", text="", icon="SCRIPTWIN")  

    row.prop(context.scene, "bbox_subdiv", text="Subdivide")   

    if tp_props.display_bbox_set: 

        box = col.box().column(1)

        row = box.row(1)
        row.prop(context.scene, "bbox_wire", text="Wire only") 
        row.prop(context.scene, "bbox_shade", text="Shade off")
        
        row = box.row(1)
        row.prop(context.scene, "bbox_origin", text="C-Origin")
        row.prop(context.scene, "bbox_smooth", text="Smooth")

        row = box.row(1)
        row.prop(context.scene, "bbox_renderoff", text="Render off")
        row.prop(context.scene, "bbox_freeze", text="Freeze")
        
    box.separator()


    box = col.box().column(1)
   
    row = box.row(1)
    button_bcyl = icons.get("icon_bcyl") 
    row.operator("tp_ops.bcylinder_for_menu",text="", icon_value=button_bcyl.icon_id)
    row.operator("tp_ops.bcylinder_for_panel",text="Bounding Cylinder")
    
    box.separator() 

    row = box.row(1)
    
    if tp_props.display_bcyl_set: 
        row.prop(tp_props, "display_bcyl_set", text="", icon="SCRIPTPLUGINS")  
    else:                  
        row.prop(tp_props, "display_bcyl_set", text="", icon="SCRIPTWIN")  

    row.prop(context.scene, "tp_cyl", text="")
     
    if tp_props.display_bcyl_set: 

        box = col.box().column(1)

        row = box.row(1)
        row.prop(context.scene, "bcyl_wire", text="Wire only")  
        row.prop(context.scene, "bcyl_shade", text="Shade off")
                           
        row = box.row(1)
        row.prop(context.scene, "bcyl_origin", text="C-Origin")
        row.prop(context.scene, "bcyl_smooth", text="Smooth")


    box.separator() 


    display_select = context.user_preferences.addons[__package__].preferences.tab_display_select
    if display_select == 'on': 

                                                       
        box = col.box().column(1)
        
        row = box.row(1)
        row.prop(context.scene, "tp_sel", text="")                          
        row.operator("tp_ops.bbox_select_box", text="Select", icon="RESTRICT_SELECT_OFF")          

        box.separator()



    display_apply = context.user_preferences.addons[__package__].preferences.tab_display_apply
    if display_apply == 'on': 

        box = col.box().column(1)
        
        row = box.row(1)                 
        row.label("Transform")

        sub = row.row(1)
        sub.scale_x = 0.3 
        sub.operator("object.transforms_to_deltas", text=" ", icon ="NDOF_DOM").mode='ALL'          
        
        button_move = icons.get("icon_apply_move") 
        sub.operator("object.transform_apply", text=" ", icon_value=button_move.icon_id).location=True

        button_rota = icons.get("icon_apply_rota") 
        sub.operator("object.transform_apply", text=" ", icon_value=button_rota.icon_id).rotation=True                

        button_scale = icons.get("icon_apply_scale") 
        sub.operator("object.transform_apply", text=" ", icon_value=button_scale.icon_id).scale=True  
       
        box.separator()



    display_history = context.user_preferences.addons[__package__].preferences.tab_display_history 
    if display_history == 'on':
        
        box = col.box().column(1)

        row = box.row(1)        
        row.operator("view3d.ruler", text="Ruler")   
         
        row.operator("ed.undo_history", text="History")
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
       
        box.separator()               
        