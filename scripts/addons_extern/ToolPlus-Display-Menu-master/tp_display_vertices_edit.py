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
    "name": "TP Display Vertex Edit",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }



import bpy, re
from bpy import *


class VIEW3D_TP_Display_Vertices_edm(bpy.types.Menu):
    bl_label = "Vertices Edit [CTRL+V]"
    bl_idname = "tp_display.vertices_edm"   


    def draw(self, context):
        settings = context.tool_settings
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'        


        obj = context.object       
        if obj.mode == 'EDIT':

            layout.operator("mesh.fill_holes", icon="MOD_TRIANGULATE") 


            layout.separator()   
            
            layout.operator("mesh.merge", icon="AUTOMERGE_ON")
            layout.operator("mesh.vert_connect", text="Connect Vert")        
            layout.operator("mesh.vert_connect_path", text="Connect Path")  
                   
            layout.separator()                 
        
            layout.operator("mesh.rip_move", icon="FULLSCREEN_ENTER")
            layout.operator("mesh.rip_move_fill")        
            layout.operator("mesh.rip_edge_move") 
                    
            layout.separator()

            layout.operator("mesh.bevel", icon="MOD_BEVEL").vertex_only = True 

            layout.separator() 
            
            layout.operator("transform.vert_slide", text="Vertices Slide", icon="PARTICLE_PATH")     
            layout.operator("mesh.vertices_smooth")
                        
            layout.separator()                     

            layout.operator("mesh.split", icon = "MOD_DISPLACE")
            layout.operator_menu_enum("mesh.separate", "type")

            layout.separator()
            
            layout.operator("mesh.mark_sharp", text="Mark Sharp", icon="SNAP_VERTEX").use_verts = True        
            op = layout.operator("mesh.mark_sharp", text="Clear Sharp")
            op.use_verts = True
            op.clear = True
            
            layout.separator() 
                     
            layout.menu("vert_additionalmenu", icon = "RESTRICT_SELECT_OFF")  
            
            layout.separator()

            layout.menu("VIEW3D_MT_hook", icon = "HOOK")         
            
            layout.separator()

            layout.menu("vgroupmenu", icon = "GROUP_VERTEX")
            layout.menu("MESH_MT_vertex_group_specials", text="Vertex Group Specials")
               


class VertAdditionalMenu(bpy.types.Menu):
    bl_label = "Additional"
    bl_idname = "vert_additionalmenu"
    
    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("mesh.convex_hull")
        layout.operator("mesh.blend_from_shape")
        layout.operator("mesh.shape_propagate_to_all")        
        
bpy.utils.register_class(VertAdditionalMenu) 



def register():
    
    bpy.utils.register_class(VIEW3D_TP_Display_Vertices_edm)         
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'V', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.vertices_edm"      


def unregister():
    
    bpy.utils.unregister_class(VIEW3D_TP_Display_Vertices_edm)    
    
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
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_Vertices_edm.bl_idname)
  
  
  
  












