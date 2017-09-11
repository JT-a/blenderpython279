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
    "name": "TP Display Curve & Surface",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy
from bpy import *


class VIEW3D_TP_Display_CurveSurface(bpy.types.Menu):
    bl_label = "Curve & Surface [CTRL+F]"
    bl_idname = "tp_display.curve_surface" 
    
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_CURVE' or 'EDIT_SURFACE'))    

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
        scene = context.scene
        toolsettings = context.tool_settings

        layout.operator("screen.redo_last", text="Settings", icon="SCRIPTWIN")

        layout.separator()

        layout.operator("curve.duplicate_move","Duplicate", icon = "MOD_BOOLEAN")          
        layout.operator("curve.extrude_move","Extrude & Move")
        layout.operator("curve.make_segment", icon = "RIGHTARROW_THIN")

        layout.separator()
        
        layout.menu("tp_curve.subdivide", icon = "IPO_QUINT")

        layout.separator()

        layout.operator("curve.split", icon = "MOD_DISPLACE")                
        layout.operator("curve.separate")             
        
        layout.separator()                
        
        edit_object = context.edit_object

        if edit_object.type == 'CURVE':
            
            layout.operator("transform.tilt", icon = "FILE_REFRESH")
            layout.operator("curve.tilt_clear")

        layout.separator()

        layout.operator_menu_enum("curve.handle_type_set", "type", icon = "IPO_BEZIER")
        layout.operator("curve.normals_make_consistent")
            
        layout.separator()

        layout.operator("curve.switch_direction", icon = "ARROW_LEFTRIGHT")

        layout.operator("curve.spline_weight_set")             
        
        edit_object = context.edit_object
        if edit_object.type == 'CURVE':
        
            layout.operator("curve.radius_set")

        layout.separator()

        layout.operator("curve.cyclic_toggle")               
        
        layout.separator()

        layout.menu("VIEW3D_MT_hook", icon = "HOOK")

        layout.separator()

        layout.menu("VIEW3D_MT_edit_curve_showhide", icon = "VISIBLE_IPO_ON")           



class VIEW3D_TP_Display_CurveSubdivide(bpy.types.Menu):
    bl_label = "Curve Subdivide"
    bl_idname = "tp_curve.subdivide"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("curve.subdivide", text="1 Cut").number_cuts=1        
        layout.operator("curve.subdivide", text="2 Cuts").number_cuts=2
        layout.operator("curve.subdivide", text="3 Cuts").number_cuts=3
        layout.operator("curve.subdivide", text="4 Cuts").number_cuts=4
        layout.operator("curve.subdivide", text="5 Cuts").number_cuts=5        
        layout.operator("curve.subdivide", text="6 Cuts").number_cuts=6 

bpy.utils.register_class(VIEW3D_TP_Display_CurveSubdivide)         


def register():

    bpy.utils.register_class(VIEW3D_TP_Display_CurveSurface)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Curve')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.curve_surface"      
     

def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Display_CurveSurface)
          
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['Curve']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 
           

if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_CurveSurface.bl_idname)










