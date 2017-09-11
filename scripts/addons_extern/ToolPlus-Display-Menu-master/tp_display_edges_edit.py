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
    "name": "TP Display Edge Edit",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy
from bpy import *


class VIEW3D_TP_Display_Edge_one_edm(bpy.types.Menu):
    bl_label = "Edge Edit [CTRL+E]"
    bl_idname = "tp_display.edge_one_edm" 
    
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH'))    

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
        with_freestyle = bpy.app.build_options.freestyle
        scene = context.scene
        
        layout.operator("mesh.edge_face_add", icon = "MOD_TRIANGULATE")
        layout.operator("mesh.subdivide")
        layout.operator("mesh.unsubdivide")
                             
        layout.separator()

        layout.operator("mesh.bevel", icon = "MOD_EDGESPLIT").vertex_only = False
        layout.operator("mesh.edge_split")
        layout.operator("mesh.bridge_edge_loops")
        
        layout.separator()
        
        layout.operator("transform.edge_slide", icon = "IPO_LINEAR")            

        layout.separator()
        
        layout.operator("mesh.edge_rotate", text="Rotate Edge CW", icon = "FILE_REFRESH").use_ccw = False
        layout.operator("mesh.edge_rotate", text="Rotate Edge CCW").use_ccw = True

        layout.separator()
        
        layout.operator("mesh.loop_multi_select",text="Edge Loop", icon="ZOOMOUT").ring=False          
        layout.operator("mesh.loop_multi_select",text="Edge Ring", icon="COLLAPSEMENU").ring=True
        layout.operator("mesh.select_nth") 

        layout.separator()
        
        layout.operator("mesh.region_to_loop")
        layout.operator("mesh.loop_to_region") 



def register():

    bpy.utils.register_class(VIEW3D_TP_Display_Edge_one_edm)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'E', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.edge_one_edm"      


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Display_Edge_one_edm)  
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['Mesh']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 

if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_Edge_one_edm.bl_idname)














