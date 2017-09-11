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
    "name": "TP Display Face Visual",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy
from bpy import *


class VIEW3D_TP_Display_Face_two_edm(bpy.types.Menu):
    bl_label = "Face Visual [SHIFT+F]"
    bl_idname = "tp_display.face_two_edm"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH'))
    
    def draw(self, context):
        layout = self.layout
        with_freestyle = bpy.app.build_options.freestyle

        layout.operator_context = 'INVOKE_REGION_WIN'
        mesh = context.active_object.data
        scene = context.scene		
        
        layout.operator("mesh.normals_make_consistent", text="Recalculate", icon="SNAP_NORMAL")
        layout.operator("mesh.normals_make_consistent", text="-> Inside").inside = True        
        layout.operator("mesh.normals_make_consistent", text="-> Outside").inside = False

        layout.separator()

        layout.operator("mesh.flip_normals", icon="SNAP_NORMAL") 
		
        layout.separator()
		
        layout.prop(mesh, "show_normal_vertex", text="Show Vertex Normal", icon='VERTEXSEL')
        layout.prop(mesh, "show_normal_face", text="Show Face Normal", icon='FACESEL')		
        layout.prop(context.scene.tool_settings, "normal_size", text="Normal Size")

        layout.separator()

        layout.operator("mesh.uvs_rotate", icon="UV_FACESEL")
        layout.operator("mesh.uvs_reverse")
        layout.operator("view3d.move_uv", text ="Move UV [ALT+G]", icon="UV_FACESEL")
        layout.operator("uv.copy_uv",icon="PASTEFLIPUP")
        layout.operator("uv.paste_uv", icon="PASTEFLIPDOWN") 
		
        layout.separator()
        layout.operator("mesh.colors_rotate", icon="COLOR")
        layout.operator("mesh.colors_reverse")

        layout.separator()

        if with_freestyle and not scene.render.use_shading_nodes:
            layout.operator("mesh.mark_freestyle_face", icon="IPO_SINE").clear = False
            layout.operator("mesh.mark_freestyle_face", text="Clear Freestyle Face").clear = True
			
        layout.separator()

        layout.prop(mesh, "show_extra_face_area", text="Face Area Info", icon="INFO")
        layout.prop(mesh, "show_extra_face_angle", text="Face Angle Info", icon="INFO")



def register():

    bpy.utils.register_class(VIEW3D_TP_Display_Face_two_edm)    
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', shift=True)
        kmi.properties.name = "tp_display.face_two_edm"      


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Display_Face_two_edm)        
    
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
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_Face_two_edm.bl_idname)
         




