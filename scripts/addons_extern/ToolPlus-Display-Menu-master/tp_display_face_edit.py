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
    "name": "TP Display Face Edit",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy, re
from bpy import *


class VIEW3D_TP_Display_Face_one_edm(bpy.types.Menu):
    bl_label = "Face Edit [CTRL+F]"
    bl_idname = "tp_display.face_one_edm"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH'))

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        scene = context.scene
        
        layout.operator("mesh.edge_face_add", icon = "MOD_TRIANGULATE")
        layout.operator("mesh.subdivide")
        layout.operator("mesh.unsubdivide")               

        layout.separator()        

        layout.operator("mesh.intersect")
        layout.operator("mesh.intersect_boolean")

        layout.separator()        
        
        layout.operator("mesh.fill", icon = "MOD_MESHDEFORM")
        layout.operator("mesh.fill_grid")        
        layout.operator("mesh.beautify_fill")     

        layout.separator()
        
        layout.menu("VIEW3D_MT_edit_mesh_extrude", icon = "MOD_BOOLEAN")
        layout.operator("mesh.poke",  text="Poke Inset")                
        layout.operator("mesh.inset",  text="Face Inset")
      
        layout.separator()
      
        layout.operator("mesh.face_split_by_edges")        
      
        layout.separator()
                      
        layout.operator("mesh.bevel", icon = "MOD_BEVEL").vertex_only = False
        layout.operator("mesh.solidify")
        layout.operator("mesh.wireframe")        
        
        layout.separator()	

        layout.operator("mesh.face_make_planar", "Planar Faces", icon="MOD_DISPLACE") 

        layout.separator()

        layout.operator("mesh.quads_convert_to_tris", icon="OUTLINER_DATA_MESH")
        layout.operator("mesh.tris_convert_to_quads", icon="OUTLINER_DATA_LATTICE") 
        
            


def register():

    bpy.utils.register_class(VIEW3D_TP_Display_Face_one_edm)    

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.face_one_edm"      


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Display_Face_one_edm) 

    bpy.utils.unregister_module(__name__)         

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
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_Face_one_edm.bl_idname)
         







