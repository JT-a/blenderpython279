__status__ = "toolplus custom version"
__author__ = "mkbreuer"
__version__ = "1.0"
__date__ = "2016"



import bpy, re
from bpy import *
             

class VIEW3D_TP_Modifier_Menu(bpy.types.Menu):
    bl_label = "T+ Modifier :)"
    bl_idname = "VIEW3D_TP_Modifier_Menu"  
    bl_space_type = 'VIEW_3D'
    
    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
        
        layout.operator_menu_enum("object.modifier_add", "type", text="New", icon='MODIFIER')            
        layout.menu("tp_menu.modifier_visual", text="Visual", icon='RESTRICT_VIEW_OFF')

        layout.separator()
        
        Display_Menus = context.user_preferences.addons[__package__].preferences.tab_tp_menus 
        if Display_Menus == 'on': 

            layout.menu("tp_menu.modifier_subsurf", text="Subsurf", icon='MOD_SUBSURF')
            layout.menu("tp_menu.modifier_automirror_xyz", text="AutoCut", icon='MOD_MIRROR')
            layout.menu("tp_menu.modifier_mirror", text="MirrorAxis", icon='MOD_MIRROR')
            layout.menu("tp_menu.modifier_array", text="ArrayAxis", icon='MOD_ARRAY')

            layout.separator()
        
        Display_ATM = context.user_preferences.addons[__package__].preferences.tab_automirror_menu 
        if Display_ATM == 'on':   

            layout.operator("tp_batch.automirror", text="AutoMirror", icon = 'MOD_WIREFRAME')  
           
            layout.separator()
            
        Display_ModStack = context.user_preferences.addons[__package__].preferences.tab_modstack_menu 
        if Display_ModStack == 'on':

            layout.operator("tp_batch.modifier_stack", text="Modifier Stack", icon = 'COLLAPSEMENU')  

            layout.separator()

        Display_Apply = context.user_preferences.addons[__package__].preferences.tab_clear_menu 
        if Display_Apply == 'on':
            
            obj = context.object      
            if obj.mode == 'OBJECT':
                layout.operator("tp_ops.apply_mod", icon = 'FILE_TICK', text="Apply all")
                   
            if obj.mode == 'EDIT':
                layout.operator("tp_ops.apply_mod", icon = 'FILE_TICK', text="Apply all")        
            
            layout.operator("tp_ops.remove_mod", icon = 'X', text="Delete all")
        

        Display_Hover = context.user_preferences.addons[__package__].preferences.tab_hover_menu 
        if Display_Hover == 'on':
            
            layout.separator()

            layout.operator("tp_ops.collapse_mod", icon = 'TRIA_RIGHT', text="HoverCollapse")  
            layout.operator("tp_ops.expand_mod", icon = 'TRIA_DOWN', text="HoverExpand")
        
         


class VIEW3D_TP_Display_Modifier_SubSurf(bpy.types.Menu):
    bl_label = "Mirror Subsurf"
    bl_idname = "tp_menu.modifier_subsurf"
    
    def draw(self, context):
        layout = self.layout
       
        layout.operator("tp_ops.subsurf_0")
        layout.operator("tp_ops.subsurf_1")
        layout.operator("tp_ops.subsurf_2")            
        layout.operator("tp_ops.subsurf_3")
        layout.operator("tp_ops.subsurf_4")
        layout.operator("tp_ops.subsurf_5")
        layout.operator("tp_ops.subsurf_6")




class VIEW3D_TP_Display_Modifier_Mirror(bpy.types.Menu):
    bl_label = "Mirror Modifier"
    bl_idname = "tp_menu.modifier_mirror"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("tp_ops.mod_mirror_x", text="X Axis")
        layout.operator("tp_ops.mod_mirror_y", text="Y Axis")
        layout.operator("tp_ops.mod_mirror_z", text="Z Axis")

        layout.separator()

        layout.operator("tp_ops.mod_mirror_xy", text="XY Axis")
        layout.operator("tp_ops.mod_mirror_yz", text="XZ Axis")
        layout.operator("tp_ops.mod_mirror_xz", text="YZ Axis")

        layout.separator()
        
        layout.operator("tp_ops.mod_mirror_xyz", text="XYZ Axis")        




class VIEW3D_TP_Display_Modifier_Array(bpy.types.Menu):
    bl_label = "Array Modifier"
    bl_idname = "tp_menu.modifier_array"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("tp_ops.x_array", "X Array")
        layout.operator("tp_ops.y_array", "Y Array")
        layout.operator("tp_ops.z_array", "Z Array")

        layout.separator()

        layout.operator("tp_ops.xy_array", "XY Array")
        layout.operator("tp_ops.xz_array", "XZ Array")
        layout.operator("tp_ops.yz_array", "YZ Array")

        layout.separator()

        layout.operator("tp_ops.xyz_array", "XYZ Array")




class VIEW3D_TP_Display_Modifier_Automirror(bpy.types.Menu):
    bl_label = "Array Modifier"
    bl_idname = "tp_menu.modifier_automirror"
    
    def draw(self, context):
        layout = self.layout
        
        if context.mode == 'EDIT_MESH':
            layout.operator("tp_ops.mods_negativ_x_cut", "X Cut")
            layout.operator("tp_ops.mods_positiv_x_cut", "X Cut")
            
            layout.separator()
            
            layout.operator("tp_ops.mods_negativ_y_cut", "Y Cut")
            layout.operator("tp_ops.mods_positiv_y_cut", "Y Cut")

            layout.separator()
            
            layout.operator("tp_ops.mods_negativ_z_cut", "Z Cut")
            layout.operator("tp_ops.mods_positiv_z_cut", "Z Cut")

        else:
            layout.operator("tp_ops.mods_negativ_x_cut_obm", "X Cut")
            layout.operator("tp_ops.mods_positiv_x_cut_obm", "X Cut")
            
            layout.separator()
            
            layout.operator("tp_ops.mods_negativ_y_cut_obm", "Y Cut")
            layout.operator("tp_ops.mods_positiv_y_cut_obm", "Y Cut")
            
            layout.separator()
            
            layout.operator("tp_ops.mods_negativ_z_cut_obm", "Z Cut")
            layout.operator("tp_ops.mods_positiv_z_cut_obm", "Z Cut")




class VIEW3D_TP_Display_Modifier_Automirror_XYZ_Cut(bpy.types.Menu):
    bl_label = "Array Modifier"
    bl_idname = "tp_menu.modifier_automirror_xyz"
    
    def draw(self, context):
        layout = self.layout
        
        layout.label("Positiv remove", icon="MOD_WIREFRAME")


        layout.operator("tp_ops.mods_positiv_x_cut_obm", "+X")
        layout.operator("tp_ops.mods_positiv_y_cut_obm", "+Y")
        layout.operator("tp_ops.mods_positiv_z_cut_obm", "+Z")        

        layout.separator()

        layout.operator("tp_ops.mods_positiv_xy_cut_obm", "+XY")
        layout.operator("tp_ops.mods_positiv_xz_cut_obm", "+XZ")
        layout.operator("tp_ops.mods_positiv_yz_cut_obm", "+YZ")
        layout.operator("tp_ops.mods_positiv_xyz_cut_obm", "+XYZ")

        layout.separator()
        
        layout.label("Negative remove", icon="MOD_WIREFRAME")
                
        layout.operator("tp_ops.mods_negativ_x_cut_obm", "-- X")
        layout.operator("tp_ops.mods_negativ_y_cut_obm", "-- Y")    
        layout.operator("tp_ops.mods_negativ_z_cut_obm", "-- Z")

        layout.separator()    

        layout.operator("tp_ops.mods_negativ_xy_cut_obm", "-- XY")
        layout.operator("tp_ops.mods_negativ_xz_cut_obm", "-- XZ")
        layout.operator("tp_ops.mods_negativ_yz_cut_obm", "-- YZ")
        layout.operator("tp_ops.mods_negativ_xyz_cut_obm", "-- XYZ")




class VIEW3D_TP_Display_Modifier_Visual(bpy.types.Menu):
    bl_label = "Visual Modifier"
    bl_idname = "tp_menu.modifier_visual"
    
    def draw(self, context):
        layout = self.layout                         
    
        layout.operator("tp_ops.mods_view","View", icon = 'RESTRICT_VIEW_OFF')                                                                       
        layout.operator("tp_ops.mods_edit","Edit", icon='EDITMODE_HLT')                                                    
        layout.operator("tp_ops.mods_cage","Cage", icon='OUTLINER_OB_MESH')      
        layout.operator("tp_ops.mods_render","Render", icon = 'RESTRICT_RENDER_OFF') 


def register():

    bpy.utils.register_module(__name__)    

def unregister():
  
    bpy.utils.unregister_module(__name__)   


if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Modifier_Menu.bl_idname)
















