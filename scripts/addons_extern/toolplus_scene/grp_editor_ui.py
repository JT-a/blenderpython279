import bpy, os
from bpy import*
from bpy.props import* 
import bpy.utils.previews




def draw_groupeditor_panel_layout(self, context, layout):

        #icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)

        box = layout.box().column(1)
        
        row = box.row(1)              
        row.alignment = 'CENTER'
        row.label("ObjectGroups", icon='GROUP')     
        
        box.separator()                                       
        
        row = box.row()   
        row.prop(context.scene, "hk_group_name_txt")
        row.operator("scene.hk_rename_group_list", text="", icon="OUTLINER_DATA_FONT")  
                        
        box.separator() 
         
        row = box.row()
        row.template_list( "SCENE_PT_HK_GroupEditor_ItemList", "", context.scene, "hk_group_list", context.scene, "hk_group_list_index",rows=3)  # Group List
        
        col = row.column(1)
        col.operator("scene.hk_create_new_group_list", text="", icon="GROUP")
        col.operator("scene.hk_select_group_list", text="", icon="RESTRICT_SELECT_OFF")
        col.operator("scene.hk_deselect_group_list", text="", icon="RESTRICT_SELECT_ON")
        col.operator("scene.hk_unlink_selected_group", text="", icon="UNLINKED")

        box.separator() 
                        
        row = box.row()        
        row.operator("scene.hk_refresh_group_list", text="Refresh Group List", icon="FILE_REFRESH")
        row.operator("scene.hk_remove_selected_group", text="", icon="CANCEL")

        box.separator() 

        row = box.row()        
        row.template_list( "SCENE_PT_HK_GroupEditor_ItemList", "", context.scene, "hk_group_object_list", context.scene, "hk_group_object_list_index", rows=3 )  # Group Object List
        
        col = row.column(1)
        col.operator("scene.hk_add_object_group_list", text="", icon="ZOOMIN")
        col.operator("scene.hk_remove_object_group_list", text="", icon="ZOOMOUT")        
        col.operator("scene.hk_select_object_group_list", text="", icon="RESTRICT_SELECT_OFF")        
        col.operator("scene.hk_unlink_object_group_list", text="", icon="UNLINKED")

        box.separator() 
        
        row = box.row()
        row.operator("scene.hk_get_group_contents_list", text="Get Group Content", icon="STYLUS_PRESSURE")        
        row.operator("purge.unused_group_data", text="", icon="COLOR_RED")

        box.separator()    


        

class Purge_Groups(bpy.types.Operator):
    '''purge all unused orphaned groups data'''
    bl_idname="purge.unused_group_data"
    bl_label="Purge Groups"
    bl_options = {"REGISTER", 'UNDO'}    

    def execute(self, context):

        target_coll = eval("bpy.data.groups")

        for item in target_coll:
            if item.users == 0:
                target_coll.remove(item)
        
        print(self)
        self.report({'INFO'}, "purge all unused orphaned groups data")            
        return {'FINISHED'}




class VIEW3D_TP_Groups_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Relations"
    bl_idname = "VIEW3D_TP_Groups_Panel_TOOLS"
    bl_label = "GroupEditor"
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
        return (isModelingMode and context.mode == 'OBJECT')
   
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_groupeditor_panel_layout(self, context, layout) 




class VIEW3D_TP_Groups_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Groups_Panel_UI"
    bl_label = "GroupEditor"
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
        return (isModelingMode and context.mode == 'OBJECT')
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_groupeditor_panel_layout(self, context, layout) 




