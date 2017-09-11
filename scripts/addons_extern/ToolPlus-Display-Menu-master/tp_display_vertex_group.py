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
    "name": "TP Display Vertex Group",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }



import bpy
from bpy import *



class VIEW3D_TP_Display_VertexGroup(bpy.types.Menu):
    """Vertex Group"""
    bl_label = "Vertex Group [<]"
    bl_idname = "tp_display.vertex_group"

    
    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        obj = context.object
        return (obj and obj.type in {'MESH', 'LATTICE'} and (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        ob = context.object
        group = ob.vertex_groups.active

        layout.prop(ob.vertex_groups, "active_index")

        layout.separator()    

        layout.operator("object.vertex_group_select", text="Select Group", icon="RESTRICT_SELECT_OFF")
        layout.operator("object.vertex_group_deselect", text="Deselect Group", icon="RESTRICT_SELECT_ON")    
            
        layout.separator()
            
        layout.operator("object.vertex_group_assign", text="Assign Group", icon="ZOOMIN")
        layout.operator("object.vertex_group_remove_from", text="Remove Group", icon="ZOOMOUT") 
            
        layout.separator()
                      
        layout.operator("object.vertex_group_add",icon='GROUP_VERTEX',text="Add Vertex Group")
        layout.operator("object.vertex_group_remove",icon='GROUP_VERTEX',text="Remove Vertex Group").all=False           

        layout.separator()

        layout.menu("MESH_MT_vertex_group_specials", icon='TRIA_RIGHT', text="Vertex Group Specials")	

        layout.separator()           

        layout.prop(context.tool_settings, "vertex_group_weight", text="Weight")



def register():

    bpy.utils.register_class(VIEW3D_TP_Display_VertexGroup)    
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'GRLESS', 'PRESS')
        kmi.properties.name = "tp_display.vertex_group"      


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Display_VertexGroup)     
    
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
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_VertexGroup.bl_idname)














