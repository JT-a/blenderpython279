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
    "name": "TP Display Edge Visual",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy
from bpy import *


class VIEW3D_TP_Display_Edge_two_edm(bpy.types.Menu):
    bl_label = "Edge Visual [SHIFT+E]"
    bl_idname = "tp_display.edge_two_edm" 
    
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH'))    

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        mesh = context.active_object.data
        scene = context.scene		
	
        with_freestyle = bpy.app.build_options.freestyle

        layout.operator("mesh.mark_seam", icon = "UV_EDGESEL").clear = False
        layout.operator("mesh.mark_seam", text="Clear Seam").clear = True

        layout.separator()

        layout.operator("mesh.mark_sharp", icon = "SNAP_EDGE").clear = False
        layout.operator("mesh.mark_sharp", text="Clear Sharp").clear = True

        layout.separator()

        layout.operator("transform.edge_crease", icon="IPO_CIRC")
        layout.operator("transform.edge_bevelweight")

        layout.separator()

        if with_freestyle and not scene.render.use_shading_nodes:
            layout.operator("mesh.mark_freestyle_edge", icon="IPO_SINE").clear = False
            layout.operator("mesh.mark_freestyle_edge", text="Clear Freestyle Edge").clear = True

        layout.separator()            

        layout.prop(mesh, "show_extra_edge_length", text="Edge Length Info", icon="INFO")
        layout.prop(mesh, "show_extra_edge_angle", text="Edge Angle Info", icon="INFO")
		


def register():

    bpy.utils.register_class(VIEW3D_TP_Display_Edge_two_edm)   
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'E', 'PRESS', shift=True)
        kmi.properties.name = "tp_display.edge_two_edm"      


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Display_Edge_two_edm)

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
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_Edge_two_edm.bl_idname)






