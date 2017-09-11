# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "TP Display Orientation",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }



import bpy
from bpy import *


def draw_orientation_history_A(context, layout):

    layout.menu("tp_display.menu_orient", "Orientation", icon = "EMPTY_DATA")
    layout.menu("tp_display.menu_pivot", "Pivot", icon = "ROTATE")

    
def draw_orientation_history_B(context, layout):


    layout.menu("tp_display.menu_snap", "Snap Target", icon = "SNAP_ON")
    layout.menu("tp_display.menu_snap_element", "Snap Element", icon = "SNAP_SURFACE")     

    layout.separator() 

    mesh = context.active_object.data
    toolsettings = context.tool_settings
    obj = context.active_object 
    
    snap_tp = toolsettings.use_snap

    if snap_tp == False:
        layout.operator("wm.context_toggle", text="Snap on/off", icon="CHECKBOX_DEHLT").data_path = "tool_settings.use_snap"
    else:
        layout.operator("wm.context_toggle", text="Snap on/off", icon="CHECKBOX_HLT").data_path = "tool_settings.use_snap"      

    if obj and obj.mode == 'OBJECT':
        layout.prop(toolsettings, "use_snap_align_rotation", text="Snap Normal", icon="SNAP_NORMAL")

    if obj and obj.mode == 'EDIT':
        layout.prop(toolsettings, "use_snap_self", text="Snap Self", icon="ORTHO")
        layout.prop(toolsettings, "use_snap_project", text="Snap Projection", icon="RETOPO")


    layout.separator() 
    
    if obj and obj.mode == 'EDIT':
        layout.prop(toolsettings, "use_mesh_automerge", text="Auto-Merge", icon='AUTOMERGE_ON')

        layout.separator() 

    layout.menu("tp_display.cursor_to", icon = "FORCE_FORCE")    
    layout.menu("tp_display.selection_to", icon = "RESTRICT_SELECT_OFF")   

    layout.separator() 
    
    layout.operator("object.editmode_toggle", text="Fast Toggle", icon = "OBJECT_DATAMODE") 
      
     

    
class TP_Display_Menu_Orientation(bpy.types.Menu):
    bl_label = "Orientation [CTRL+\]"
    bl_idname = "tp_display.menu_orientation"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        obj = context.active_object
        mesh = context.active_object.data
    
        obj = context
        if obj and obj.mode == 'OBJECT':

            draw_orientation_history_A(context, layout)

            layout.separator()
                        
            layout.menu("tp_display.origin_setup_menu_obm", icon = "LAYER_ACTIVE")
                        
            layout.separator()
            
            draw_orientation_history_B(context, layout)                        

            
        if obj and obj.mode == 'EDIT_MESH':            

            draw_orientation_history_A(context, layout)

            layout.separator() 
            
            layout.menu("tp_display.origin_setup_menu_edm", icon = "LAYER_ACTIVE")                 
                                    
            layout.separator()                                  

            draw_orientation_history_B(context, layout)        


        
        if obj and obj.mode == 'EDIT_CURVE':            
            
            draw_orientation_history_A(context, layout)
            
            layout.separator()            
            
            layout.menu("tp_display.origin_setup_menu_edm", icon = "LAYER_ACTIVE") 
                        
            layout.separator()                                  
                        
            draw_orientation_history_B(context, layout)

     
        if obj and obj.mode == 'EDIT_SURFACE':            
            
            draw_orientation_history_A(context, layout)
            
            layout.separator()            
            
            layout.menu("tp_display.origin_setup_menu_edm", icon = "LAYER_ACTIVE") 
                                     
            layout.separator()                                  
                        
            draw_orientation_history_B(context, layout)



        if obj and obj.mode == 'EDIT_METABALL':            
            
            draw_orientation_history_A(context, layout)
            
            layout.separator()            
            
            layout.menu("tp_display.origin_setup_menu_edm", icon = "LAYER_ACTIVE") 
                                   
            layout.separator()                                  

            draw_orientation_history_B(context, layout)

      
        if obj and obj.mode == 'EDIT_LATTICE':
            
            draw_orientation_history_A(context, layout)
            
            layout.separator()            
            
            layout.menu("tp_display.origin_setup_menu_edm", icon = "LAYER_ACTIVE")

            layout.separator()                                            
                        
            draw_orientation_history_B(context, layout)

                           
        
        if obj and obj.mode == 'EDIT_ARMATURE': 
            
            draw_orientation_history_A(context, layout)

            layout.separator()                         
            
            layout.menu("tp_display.origin_setup_menu_edm", icon = "LAYER_ACTIVE")
            
            layout.separator()                                  

            draw_orientation_history_B(context, layout)



        if obj and obj.mode == 'POSE': 
            
            arm = context.active_object.data
                                                 
            layout.menu("tp_display.origin_setup_menu_edm", icon = "LAYER_ACTIVE")
                        
            layout.separator()                                  
                        
            draw_orientation_history_B(context, layout)




class TP_Display_Selection_to_Menu(bpy.types.Menu):
    bl_label = "Selection to..."
    bl_idname = "tp_display.selection_to"
    
    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
         
        layout.operator("view3d.snap_selected_to_grid", text="Grid")       
        layout.operator("view3d.snap_selected_to_cursor", text="Cursor").use_offset = False
        layout.operator("view3d.snap_selected_to_cursor","Cursor (offset)").use_offset = True
            
bpy.utils.register_class(TP_Display_Selection_to_Menu)


class TP_Display_Cursor_to_Menu(bpy.types.Menu):
    bl_label = "Cursor to..."
    bl_idname = "tp_display.cursor_to"
    
    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("view3d.snap_cursor_to_grid", text="Grid")
        layout.operator("view3d.snap_cursor_to_center", text="Center")
        layout.operator("view3d.snap_cursor_to_active", text="Active")    
        layout.operator("view3d.snap_cursor_to_selected", text="Selected")
                    
bpy.utils.register_class (TP_Display_Cursor_to_Menu)
  


class TP_Display_Origin_Setup_Menu_OBM(bpy.types.Menu):
    bl_label = "Origin Setup"
    bl_idname = "tp_display.origin_setup_menu_obm"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
                
        layout.operator("object.origin_set", text="Geometry").type = 'ORIGIN_GEOMETRY'
        layout.operator("object.origin_set", text="3D Cursor").type = 'ORIGIN_CURSOR'
        layout.operator("object.origin_set", text="Center of Mass").type = 'ORIGIN_CENTER_OF_MASS'

        layout.separator()   
                 
        layout.operator("object.origin_set", text="Geometry to Origin").type = 'GEOMETRY_ORIGIN'        

        layout.separator()  

        layout.operator("tp_display.pivo_to_bottom", "Boundbox Bottom")          

bpy.utils.register_class(TP_Display_Origin_Setup_Menu_OBM) 


class TP_Display_Origin_Setup_Menu_EDM(bpy.types.Menu):
    bl_label = "Origin Setup Menu"
    bl_idname = "tp_display.origin_setup_menu_edm"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.label("Origin to Selected", icon = "RESTRICT_SELECT_OFF")
            
        layout.operator("tp_display.origin_edm","Editmode")
        layout.operator("tp_display.origin_obm","Objectmode")
                          

bpy.utils.register_class(TP_Display_Origin_Setup_Menu_EDM) 



def register():

    bpy.utils.register_class(TP_Display_Menu_Orientation)     
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'BACK_SLASH', 'PRESS', alt = True)
        kmi.properties.name = "tp_display.menu_orientation"


def unregister():

    bpy.utils.unregister_class(TP_Display_Menu_Orientation)   
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['3D View']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 


if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=TP_Display_Menu_Orientation.bl_idname)
         


        



































