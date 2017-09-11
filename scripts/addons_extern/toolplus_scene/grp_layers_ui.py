import bpy, os
from bpy import*
from bpy.props import* 
import bpy.utils.previews



def draw_layers_panel_layout(self, context, layout):

        #icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)
        
        box = layout.box().column(1)   

        row = box.row(1)              
        row.alignment = 'CENTER'
        row.label("Layers", icon='OOPS')     
        
        box.separator()
        
        row = box.row()
        if len(context.selected_objects) == 1:                        
            row.prop(context.active_object, "name", text="", icon = "COPY_ID")          
        row.prop(context.scene, "display_layers_collection")
               
        box.separator()
        
        row = box.row()
        col = row.column()
        col.template_list("layers_collection_UL", "", context.scene, "display_layers_collection", context.scene, "display_layers_collection_index", rows = 4)

        col = row.column()
        sub = col.column(1)
        sub.operator("add_layer_from_collection.btn", icon='ZOOMIN', text="")
        sub.operator("remove_layer_from_collection.btn", icon='ZOOMOUT', text="")
        sub.operator("up_layer_from_collection.btn", icon='TRIA_UP', text="")
        sub.operator("down_layer_from_collection.btn", icon='TRIA_DOWN', text="")        
        sub.operator("clear_display_layers_collection.btn", icon="X", text="")           
        
        box.separator()    

        row =box.row(1)
        row.operator("assign_layer.btn", icon="DISCLOSURE_TRI_RIGHT", text="Assign")
        row.operator("remove_layer.btn", icon="DISCLOSURE_TRI_DOWN", text="Remove")      
        row.operator("select_objects.btn", icon="RESTRICT_SELECT_OFF", text="Select")

        box.separator()   
               
        box = layout.box().column(1)
        
        row =box.row(1)
        row.operator('sjoin.join', "Smart Join", icon="LOCKVIEW_ON")
        row.operator('sjoin.separate', "Separate", icon="LOCKVIEW_OFF")

        row =box.row(1)
        row.operator('sjoin.expand', "Expand", icon="PASTEDOWN")
        row.operator('sjoin.collapse', "Collapse", icon="COPYDOWN")

        row =box.row(1)            
        row.operator('sjoin.join_add', "Add 2 Smart", icon="PASTEFLIPUP")
        row.operator('sjoin.update_rec', "Update", icon="LOAD_FACTORY")          
                              
        ###
        box.separator()
             
        Display_Shade = context.user_preferences.addons[__package__].preferences.tab_move 
        if Display_Shade == 'on':


            box = layout.box().column(1)

            row = box.row(1) 
            row.operator("object.move_to_layer", text="Move to Layer")
            row.prop(context.object, "pass_index")

            box.separator()

            row = box.column(1) 
            row.label(text="Parent:")
            
            row =box.row(1)              
            row.prop(context.object, "parent", text="")

            sub = box.row(1)
            sub.prop(context.object, "parent_type", text="")
            parent = context.object.parent
            
            if parent and context.object.parent_type == 'BONE' and parent.type == 'ARMATURE':
                sub.prop_search(context.object, "parent_bone", parent.data, "bones", text="")
            sub.active = (parent is not None)

            ###
            box.separator()
        
        else:
            pass        
              

        Display_Shade = context.user_preferences.addons[__package__].preferences.tab_shade 
        if Display_Shade == 'on':

            box = layout.box().column(1)
            
            row =box.row(1)
            row.operator("tp_ops.wire_all", text="Wire all", icon='WIRE')
            
            active_wire = bpy.context.object.show_wire 
            if active_wire == True:
                row.operator("tp_ops.wire_off", "Wire Select", icon = 'MESH_PLANE')              
            else:                       
                row.operator("tp_ops.wire_on", "Wire Select", icon = 'MESH_GRID')            
           
            row = box.row(1)
            if context.object.draw_type == 'WIRE':
                row.operator("tp_ops.draw_solid", text="Solid Shade", icon='GHOST_DISABLED')     
            else:
                row.operator("tp_ops.draw_wire", text="Wire Shade", icon='GHOST_ENABLED')        
                        

            row.prop(context.object, "draw_type", text="")

            row = box.row(1)
            row.prop(context.object, "show_bounds", text="ShowBounds", icon='STICKY_UVS_LOC') 
            row.prop(context.object, "draw_bounds_type", text="") 

            box.separator()  

            row = box.row(1)          
            row.prop(context.object, "show_x_ray", text="X-Ray", icon ="META_CUBE")

            obj = context.object
            if obj.type in {'MESH'}:
                row.prop(context.space_data, "show_backface_culling", text="Backface", icon ="OUTLINER_OB_LATTICE")  

            box.separator()  
            
            row = box.row(1) 
            row.operator("animation.silhouette_on", text="Silhouette", icon='RADIOBUT_ON')
            
            row = box.row(1) 
            row.operator("animation.silhouette_half", icon='RADIOBUT_OFF')
            row.operator("animation.silhouette_off", icon='RADIOBUT_OFF')

            row = box.row(1)
            row.operator("antonio_animation.backupfile", icon='SAVE_COPY')

            
            ###
            box.separator() 
            
        else:
            pass
            
                
                
class VIEW3D_TP_Layers_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Tools"
    bl_idname = "VIEW3D_TP_Layers_Panel_TOOLS"
    bl_label = "SmartLayer"
    bl_space_type = 'VIEW_3D'
    bl_context = 'objectmode'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return isModelingMode
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_layers_panel_layout(self, context, layout) 



class VIEW3D_TP_Layers_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Layers_Panel_UI"
    bl_label = "SmartLayer"
    bl_space_type = 'VIEW_3D'
    bl_context = 'objectmode'    
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return isModelingMode 
    
    def draw(self, context):
        layout = self.layout.column_flow(1)          
        layout.operator_context = 'INVOKE_REGION_WIN' 

        draw_layers_panel_layout(self, context, layout) 




