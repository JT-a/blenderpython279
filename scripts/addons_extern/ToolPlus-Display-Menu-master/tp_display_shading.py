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
    "name": "TP Display Shading",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy
from bpy import *


class VIEW3D_TP_Menu_3dview(bpy.types.Menu):
    bl_label = "Shading [ALT+2]"
    bl_idname = "tp_display.menu_3d_view"

    def draw(self, context):
        layout = self.layout
        view = context.space_data		
        obj = context.object
        obj_type = obj.type
        is_geometry = (obj_type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'})
        is_empty_image = (obj_type == 'EMPTY' and obj.empty_draw_type == 'IMAGE')		
        with_freestyle = bpy.app.build_options.freestyle
        layout.operator_context = 'INVOKE_REGION_WIN'
        mesh = context.active_object.data
        scene = context.scene

        gs = scene.game_settings
        mode_string = context.mode
        edit_object = context.edit_object
        obj = context.active_object
        
        toolsettings = context.tool_settings
       
        if obj and obj.mode == 'OBJECT':
            layout.operator("object.shade_flat", icon="MESH_CIRCLE")            
            layout.operator("object.shade_smooth", icon="SOLID")
        
        if obj and obj.mode == 'EDIT':
            layout.operator("mesh.faces_shade_flat", icon="MESH_CIRCLE")               
            layout.operator("mesh.faces_shade_smooth", icon="SOLID")


        layout.separator()
        
        if view.viewport_shade == 'SOLID':
            layout.prop(view, "use_matcap")
            if view.use_matcap:
                layout.template_icon_view(view, "matcap_icon")
       
        layout.separator()
        
        layout.prop(view, "show_backface_culling")
        if obj and obj.mode == 'EDIT' and view.viewport_shade not in {'BOUNDBOX', 'WIREFRAME'}:
            layout.prop(view, "show_occlude_wire")
            
        layout.separator()            

        if view.viewport_shade == 'SOLID':               
            layout.prop(view, "show_textured_solid", text="Texture")
               
        elif view.viewport_shade == 'TEXTURED':
            if scene.render.use_shading_nodes or gs.material_mode != 'GLSL':
                layout.prop(view, "show_textured_shadeless")

        if not scene.render.use_shading_nodes:
            layout.prop(gs, "material_mode", text="")                

        layout.separator()   
                                        
        col = layout.column()
        col.prop(view, "show_only_render")

        col = layout.column()
        display_all = not view.show_only_render
        col.active = display_all
        col.prop(view, "show_outline_selected")
        col.prop(view, "show_all_objects_origin")
        col.prop(view, "show_relationship_lines")

        layout.separator()        

        col = layout.column()
        col.active = display_all
        layout.prop(view, "show_floor", text="Grid Floor")

        layout.prop(view, "show_axis_x", text="X", toggle=True)
        layout.prop(view, "show_axis_y", text="Y", toggle=True)
        layout.prop(view, "show_axis_z", text="Z", toggle=True)

        layout.separator()          

        sub = layout.column(align=True)
        sub.active = (display_all and view.show_floor)
        layout.prop(view, "grid_lines", text="Lines")
        layout.prop(view, "grid_scale", text="Scale")
        subsub = sub.column(align=True)
        subsub.active = scene.unit_settings.system == 'NONE'
        subsub.prop(view, "grid_subdivisions", text="Subdivisions")




def register():

    bpy.utils.register_class(VIEW3D_TP_Menu_3dview)
        
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'TWO', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.menu_3d_view"      


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Menu_3dview)
        
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
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Menu_3dview.bl_idname)
         













