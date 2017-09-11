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
    "name": "TP Display Paint",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy, re
from bpy import *



class TP_Display_Paint_Menu(bpy.types.Menu):
    bl_label = "Paint [W]"
    bl_idname = "tp_display.paint_menu"    

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        ob = context
        if  context.mode == 'PARTICLE':

            # Brush Menu
            #layout.menu("VIEW3D_ParticleBrush", text = "Brushes", icon='BRUSH_DATA') 

            #layout.separator() 

            layout.menu("VIEW3D_Paint_Particle", text = "Hair Particles", icon='PARTICLEMODE')            
           

        if ob.mode == 'PAINT_WEIGHT':

            layout.menu("tp_display.vertex_menu", icon='BRUSH_DATA')
            layout.menu("VIEW3D_MT_brush") 

            layout.separator() 
            
            layout.menu("tp_display.weights_menu", icon='WPAINT_HLT')
                                              
         
        if ob.mode == 'PAINT_VERTEX':

            layout.menu("tp_display.vertex_menu", icon='BRUSH_DATA')
            layout.menu("VIEW3D_MT_brush") 

            layout.separator()                       

            layout.operator("paint.vertex_color_set", text="Set Color ", icon='VPAINT_HLT')
            layout.operator("paint.vertex_color_smooth", text="Smooth Color ")
            layout.operator("mesh.connected_vertex_colors", text="Connected Vertex Colors")
            
            layout.separator()        
    
            layout.operator("paint.vertex_color_dirt", text="Dirt Color ", icon='TPAINT_HLT')

            layout.operator("paint.worn_edges", text="Worn Edges")
                    

        if ob.mode == 'PAINT_TEXTURE':
            
            layout.menu("tp_display.texture_menu", icon='BRUSH_DATA')
            layout.menu("VIEW3D_MT_brush")
            



class TP_Display_Texture_Brush(bpy.types.Menu):
    bl_label = "Texture Brushes"
    bl_idname = "tp_display.texture_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN' 
        
        #layout.operator("paint.brush_select", text='Brush', icon='BRUSH_TEXDRAW').texture_paint_tool= 'BRUSH'               
        layout.operator("paint.brush_select", text='Clone', icon='BRUSH_CLONE').texture_paint_tool= 'CLONE'
        
        layout.operator("paint.brush_select", text='Draw', icon='BRUSH_TEXDRAW').texture_paint_tool= 'DRAW'
        layout.operator("paint.brush_select", text='Fill', icon='BRUSH_TEXFILL').texture_paint_tool= 'FILL'               
        
        layout.operator("paint.brush_select", text='Mask', icon='BRUSH_TEXMASK').texture_paint_tool= 'MASK'
        layout.operator("paint.brush_select", text='Smear', icon='BRUSH_SMEAR').texture_paint_tool= 'SMEAR'
          
        layout.operator("paint.brush_select", text='Soften', icon='BRUSH_SOFTEN').texture_paint_tool= 'SOFTEN'               
        layout.operator("paint.brush_select", text='TexDraw', icon='BRUSH_TEXDRAW').texture_paint_tool= 'TEXDRAW'

bpy.utils.register_class(TP_Display_Texture_Brush)



class TP_Display_Vertex_Brush(bpy.types.Menu):
    bl_label = "Vertex Brushes"
    bl_idname = "tp_display.vertex_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN' 
        
        layout.operator("paint.brush_select", text='Add', icon='BRUSH_ADD').vertex_paint_tool= 'ADD'               
        layout.operator("paint.brush_select", text='Blur', icon='BRUSH_MIX').vertex_paint_tool= 'BLUR'
        
        layout.operator("paint.brush_select", text='Darken', icon='BRUSH_DARKEN').vertex_paint_tool= 'DARKEN'               
        layout.operator("paint.brush_select", text='Lighten', icon='BRUSH_LIGHTEN').vertex_paint_tool= 'LIGHTEN'
          
        layout.operator("paint.brush_select", text='Mix', icon='BRUSH_MIX').vertex_paint_tool= 'MIX'               
        layout.operator("paint.brush_select", text='Multiply', icon='BRUSH_MULTIPLY').vertex_paint_tool= 'MUL'
     
        layout.operator("paint.brush_select", text='Substract', icon='BRUSH_SUBTRACT').vertex_paint_tool= 'SUB'                      

bpy.utils.register_class(TP_Display_Vertex_Brush)



class TP_Display_Paint_Weight(bpy.types.Menu):
    bl_label = "Weights"
    bl_idname = "tp_display.weights_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("paint.weight_from_bones", text="Assign Automatic From Bones").type = 'AUTOMATIC'
        layout.operator("paint.weight_from_bones", text="Assign From Bone Envelopes").type = 'ENVELOPES'

        layout.separator()

        layout.operator("object.vertex_group_normalize_all", text="Normalize All")
        layout.operator("object.vertex_group_normalize", text="Normalize")
        layout.operator("object.vertex_group_mirror", text="Mirror")
        layout.operator("object.vertex_group_invert", text="Invert")

        layout.separator()
        
        layout.operator("object.vertex_group_clean", text="Clean")
        layout.operator("object.vertex_group_quantize", text="Quantize")
        layout.operator("object.vertex_group_levels", text="Levels")
        layout.operator("object.vertex_group_blend", text="Blend")

        layout.separator()
        
        layout.operator("object.vertex_group_transfer_weight", text="Transfer Weights")
        layout.operator("object.vertex_group_limit_total", text="Limit Total")
        layout.operator("object.vertex_group_fix", text="Fix Deforms")

        layout.separator()

        layout.operator("paint.weight_set")
        
bpy.utils.register_class(TP_Display_Paint_Weight)        
        

        
class TP_Display_Weight_Brush(bpy.types.Menu):
    bl_label = "Weight Brushes"
    bl_idname = "tp_display.weight_brushes"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN' 

        layout.menu("tp_display.vertex_menu", icon='BRUSH_DATA')
        layout.menu("VIEW3D_MT_brush") 

bpy.utils.register_class(TP_Display_Weight_Brush)



def register():

    bpy.utils.register_class(TP_Display_Paint_Menu)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Image Paint')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "tp_display.paint_menu" 

        km = kc.keymaps.new(name='Weight Paint')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "tp_display.paint_menu"         

        km = kc.keymaps.new(name='Vertex Paint')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "tp_display.paint_menu"         

def unregister():

    bpy.utils.unregister_class(TP_Display_Paint_Menu)
              
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps['Image Paint']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 

        km = kc.keymaps['Vertex Paint']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 

        km = kc.keymaps['Weight Paint']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 


if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=TP_Display_Paint_Menu.bl_idname)
  
  
  
   









































