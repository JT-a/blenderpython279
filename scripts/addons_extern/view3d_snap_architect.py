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
    "name": "Snap Architect",
    "author": "MKB",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "ToolPlus"
    }


import bpy
from bpy import*
from bpy.props import *


class Snap_Architect_Menu(bpy.types.Menu):
    """Snap Architect :)"""
    bl_idname = "snap_menu.architect_set"
    bl_label = "Snap Architect :)"

    def draw(self, context):
        layout = self.layout     
        layout.operator_context = 'INVOKE_REGION_WIN'

        if context.active_object.type in {'MESH'}:   
            
            layout.operator("object.carver", icon="MOD_BEVEL")  
            
            layout.separator()
            
            layout.operator("mesh.snap_utilities_line", icon="LINE_DATA")         
            layout.operator("mesh.snap_push_pull", icon = "MOD_SOLIDIFY")  
                    
            layout.operator("mesh.snap_utilities_rotate", icon="NDOF_TURN")  #only full version         
            layout.operator("mesh.snap_utilities_move", icon="NDOF_TRANS")   #only full version                         
                
            layout.separator()

        layout.operator("object.align_tools","Align Tools", icon="ROTATE") 

        layout.separator() 

        layout.operator("object.np_point_distance_014", "Snap Distance", icon="CURVE_NCURVE") 
        
        layout.separator()

        layout.prop(context.scene,"pivot_pro_enabled",text='Pivot Pro',icon='LAYER_ACTIVE')

            
                 
def register():

    bpy.utils.register_class(Snap_Architect_Menu)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'ONE', 'PRESS', alt = True)
        kmi.properties.name = "snap_menu.architect_set"               



def unregister():
  
    bpy.utils.unregister_class(Snap_Architect_Menu)
           
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
    bpy.ops.wm.call_menu(name=Snap_Architect_Menu.bl_idname)
