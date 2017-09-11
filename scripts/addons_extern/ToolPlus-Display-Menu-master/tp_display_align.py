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
    "name": "TP Display Align",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "User Interface"
    }



import bpy
from bpy import *


def draw_align_history_A(context, layout):

    layout.label("Align to Axis", icon="ALIGN")

    layout.operator("tp_display.align_x_axis", "X-Axis")
    layout.operator("tp_display.align_y_axis", "Y-Axis")           
    layout.operator("tp_display.align_z_axis", "Z-Axis")        


def draw_align_history_B(context, layout):

    obj = context.active_object    
    layout.operator_context = 'INVOKE_REGION_WIN'
              
    layout.label("Mirror", icon="ARROW_LEFTRIGHT")

    if obj and obj.mode == 'OBJECT':            

        layout.operator("tp_display.mirror_global_x",text="X-Axis")
        layout.operator("tp_display.mirror_global_y",text="Y-Axis")
        layout.operator("tp_display.mirror_global_z",text="Z-Axis") 
         

    if obj and obj.mode == 'EDIT':                 

        layout.operator("tp_display.mirror_local_x",text="X-Axis")
        layout.operator("tp_display.mirror_local_y",text="Y-Axis")
        layout.operator("tp_display.mirror_local_z",text="Z-Axis") 
         

    layout.separator() 
    
    layout.menu("tp_display.proportional_menu", "Proportional Menu", icon = "PROP_ON")
    
    layout.separator() 

    layout.operator("object.editmode_toggle", text="Fast Toggle", icon = "OBJECT_DATAMODE") 
      
     

    
class TP_Display_Menu_Align(bpy.types.Menu):
    bl_label = "Align Menu [\]"
    bl_idname = "tp_display.menu_align"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        obj = context.active_object
        mesh = context.active_object.data
    
        obj = context
        if obj and obj.mode == 'OBJECT':
       
                  
            layout.operator("tp_display.align_location_all",text="Align All Location", icon='MAN_TRANS') 
            layout.menu("tp_display.align_location_axis",text="Axis Location") 

            layout.separator()  
        
            layout.operator("tp_display.align_rotation_all",text="Align All Rotation", icon='MAN_ROT')
            layout.menu("tp_display.align_rotation_axis",text="Axis Rotation")

            layout.separator()  
           
            layout.operator("tp_display.align_scale_all",text="Align All Scale", icon='MAN_SCALE')    
            layout.menu("tp_display.align_scale_axis",text="Axis Scale")    
            
            layout.separator()                                  

            draw_align_history_B(context, layout)
            
                        

        if obj and obj.mode == 'EDIT_MESH':                                                        

            draw_align_history_A(context, layout)        

            layout.separator()                                  
            
            draw_align_history_B(context, layout)


        
        if obj and obj.mode == 'EDIT_CURVE':            

            draw_align_history_A(context, layout)
            
            layout.separator()                                  
            
            draw_align_history_B(context, layout)

 
        
        if obj and obj.mode == 'EDIT_SURFACE':            

            draw_align_history_A(context, layout)

            layout.separator()                                  

            draw_align_history_B(context, layout)



        if obj and obj.mode == 'EDIT_METABALL':            
            
            draw_align_history_A(context, layout)

            layout.separator()

            draw_align_history_B(context, layout)


        
        if obj and obj.mode == 'EDIT_LATTICE':

            layout.operator("lattice.flip", text="Flip X-Axis (U)").axis = "U"
            layout.operator("lattice.flip", text="Flip Y-Axis (V)").axis = "V"
            layout.operator("lattice.flip", text="Flip Z-Axis (W)").axis = "W"

            layout.separator()
            
            layout.operator("lattice.make_regular", text="Make Regular (Distribute)")             
                                   
            layout.separator()                                  
                        
            draw_align_history_A(context, layout)

            layout.separator()

            draw_align_history_B(context, layout)
                     
                           
        
        if obj and obj.mode == 'EDIT_ARMATURE': 

            draw_align_history_A(context, layout)

            layout.separator()

            draw_align_history_B(context, layout)



        if obj and obj.mode == 'POSE': 

            draw_align_history_A(context, layout)

            layout.separator()

            draw_align_history_B(context, layout)



  

class TP_Display_Proportional_Menu(bpy.types.Menu):
    bl_label = "Proportional Menu"
    bl_idname = "tp_display.proportional_menu"
  
    def draw(self, context):
        layout = self.layout
        view = context.space_data
        obj = context.active_object
        toolsettings = context.tool_settings

        layout.prop(toolsettings, "use_proportional_edit_objects", text = "on/off", icon_only=True)
       
        if toolsettings.use_proportional_edit_objects:
            layout.prop(toolsettings, "proportional_edit_falloff", icon_only=True)

        layout.prop(toolsettings, "proportional_edit", icon_only=True)

bpy.utils.register_class(TP_Display_Proportional_Menu) 



class TP_Display_Align_Location_Axis_Menu(bpy.types.Menu):
    bl_label = "Align_Location Axis"
    bl_idname = "tp_display.align_location_axis"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("tp_display.align_location_x", text="X Axis") 
        layout.operator("tp_display.align_location_y", text="Y Axis") 
        layout.operator("tp_display.align_location_z", text="Z Axis") 


bpy.utils.register_class(TP_Display_Align_Location_Axis_Menu)



class TP_Display_Align_Rotation_Axis_Menu(bpy.types.Menu):
    bl_label = "Align Rotation Axis"
    bl_idname = "tp_display.align_rotation_axis"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("tp_display.align_rotion_x", text="X Axis") 
        layout.operator("tp_display.align_rotion_y", text="Y Axis") 
        layout.operator("tp_display.align_rotion_z", text="Z Axis") 


bpy.utils.register_class(TP_Display_Align_Rotation_Axis_Menu)



class TP_Display_Align_Scale_Axis_Menu(bpy.types.Menu):
    bl_label = "Align Scale Axis"
    bl_idname = "tp_display.align_scale_axis"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("tp_display.align_scale_x", text="X Axis") 
        layout.operator("tp_display.align_scale_y", text="Y Axis") 
        layout.operator("tp_display.align_scale_z", text="Z Axis") 

bpy.utils.register_class(TP_Display_Align_Scale_Axis_Menu)



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

    bpy.utils.register_class(TP_Display_Menu_Align)     
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'BACK_SLASH', 'PRESS')
        kmi.properties.name = "tp_display.menu_align"


def unregister():

    bpy.utils.unregister_class(TP_Display_Menu_Align)   
    
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
    bpy.ops.wm.call_menu(name=TP_Display_Menu_Align.bl_idname)
         


        



































