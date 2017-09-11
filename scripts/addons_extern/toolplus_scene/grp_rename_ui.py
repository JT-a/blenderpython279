import bpy, os, re
from bpy import*
from bpy.props import* 
import bpy.utils.previews





def draw_rename_panel_layout(self, context, layout):

        #icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)
 
 
        box = layout.box().column(1)    
       
        row = box.row(1) 
        row.prop(context.scene,'rno_bool_keepOrder',text='')         
        row.enabled = False
        row.operator("object.rno_keep_selection_order", "Respect Selection")


        box = layout.box().column(1)                     

        row = box.row(1) 
        row.prop(context.scene,"rno_str_new_name", "Name",)
        
        box.separator() 
                
        row = box.row(1) 
        row.prop(context.scene,"rno_bool_numbered")
        row.prop(context.scene,"rno_str_numFrom")
        
        box.separator() 
                
        row = box.column(1)
        row.operator("object.rno_setname", "Set new Name", icon ="FONT_DATA")
        row.operator("object.copynametodata", "Copy to Data Name", icon ="OOPS")        
         
        box = layout.box().column(1)                     

        row = box.column(1) 
        row.prop(context.scene, "rno_str_old_string")
        row.prop(context.scene, "rno_str_new_string")
        
        box.separator()
        
        row = box.row(1)         
        row.operator("object.rno_replace_in_name", "Replace Old String Name")

        box = layout.box().column(1)                     

        row = box.row(1) 
        row.prop(context.scene,'rno_bool_keepIndex',text='keep object Index')
       
        row = box.column(1)
        row.prop(context.scene, "rno_str_prefix")
        row.prop(context.scene, "rno_str_subfix")     
        
        box.separator()      
        
        row = box.row(1)        
        row.operator("object.rno_add_subfix_prefix", "Add Subfix / Prefix")

        ###    
        box.separator()                             


        Display_History = context.user_preferences.addons[__package__].preferences.tab_history 
        if Display_History == 'on':
            
            box = layout.box().column(1)  

            row = box.row(1)        
            row.operator("view3d.ruler", text="Ruler")   
             
            row.operator("ed.undo_history", text="History")
            row.operator("ed.undo", text="", icon="LOOP_BACK")
            row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
           
            box.separator() 



class VIEW3D_TP_Rename_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Options"
    bl_idname = "VIEW3D_TP_Rename_Panel_TOOLS"
    bl_label = "ReNamer"
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
        return (context.object is not None and isModelingMode and context.mode == 'OBJECT')


    def draw(self, context):
        layout = self.layout.column_flow(1)    
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_rename_panel_layout(self, context, layout) 



class VIEW3D_TP_Rename_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Rename_Panel_UI"
    bl_label = "ReNamer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'objectmode'
    bl_options = {'DEFAULT_CLOSED'}


    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)


    def draw(self, context):
        layout = self.layout.column_flow(1)    
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_rename_panel_layout(self, context, layout) 




