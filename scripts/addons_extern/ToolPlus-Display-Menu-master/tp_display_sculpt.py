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
    "name": "TP Display Sculpt",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy, re
from bpy import*
from bpy.props import*


class TP_Display_Sculpt_Brush(bpy.types.Menu):
    bl_label = "Sculpt Brushes"
    bl_idname = "tp_display.brush_sculpt"

    def draw(self, context):
        layout = self.layout.column_flow(2)
        layout.operator_context = 'INVOKE_REGION_WIN'        

        layout.operator("paint.brush_select", text='Blob', icon='BRUSH_BLOB').sculpt_tool= 'BLOB'    
        
        layout.operator("paint.brush_select", text="Clay", icon='BRUSH_CLAY').sculpt_tool='CLAY'        
        layout.operator("paint.brush_select", text='Claystrips', icon='BRUSH_CREASE').sculpt_tool= 'CLAY_STRIPS'
        
        layout.operator("paint.brush_select", text="Crease", icon='BRUSH_CREASE').sculpt_tool='CREASE'

        layout.operator("paint.brush_select", text='Brush', icon='BRUSH_SCULPT_DRAW').sculpt_tool='DRAW'
        layout.operator("paint.brush_select", text='Fill/Deepen', icon='BRUSH_FILL').sculpt_tool='FILL'

        layout.operator("paint.brush_select", text='Flatten', icon='BRUSH_FLATTEN').sculpt_tool='FLATTEN'
        layout.operator("paint.brush_select", text='Grab', icon='BRUSH_GRAB').sculpt_tool='GRAB'

        layout.operator("paint.brush_select", text='Inflate/Deflate', icon='BRUSH_INFLATE').sculpt_tool='INFLATE'
        layout.operator("paint.brush_select", text='Layer', icon='BRUSH_LAYER').sculpt_tool= 'LAYER'

        layout.operator("paint.brush_select", text='Mask', icon='BRUSH_MASK').sculpt_tool='MASK'
        layout.operator("paint.brush_select", text='Nudge', icon='BRUSH_NUDGE').sculpt_tool= 'NUDGE'

        layout.operator("paint.brush_select", text='Pinch/Magnify', icon='BRUSH_PINCH').sculpt_tool= 'PINCH'
        layout.operator("paint.brush_select", text='Twist', icon='BRUSH_ROTATE').sculpt_tool= 'ROTATE'

        layout.operator("paint.brush_select", text='Scrape/Peaks', icon='BRUSH_SCRAPE').sculpt_tool= 'SCRAPE'
        layout.operator("paint.brush_select", text='Polish', icon='BRUSH_FLATTEN')

        layout.operator("paint.brush_select", text='Smooth', icon='BRUSH_SMOOTH').sculpt_tool= 'SMOOTH'
        layout.operator("paint.brush_select", text='Snakehook', icon='BRUSH_SNAKE_HOOK').sculpt_tool= 'SNAKE_HOOK'

        layout.operator("paint.brush_select", text='Thumb', icon='BRUSH_THUMB').sculpt_tool= 'THUMB'
 
bpy.utils.register_class(TP_Display_Sculpt_Brush)


class TP_Display_Sculpt_Dyntopo(bpy.types.Menu):
    bl_label = "Dyntopo Set"
    bl_idname = "tp_display.brush_dyntopo"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'        

        layout.prop(context.tool_settings.sculpt, "detail_refine_method", text="") 
        layout.prop(context.tool_settings.sculpt, "detail_type_method", text="")                          

        layout.prop(context.tool_settings.sculpt, "use_smooth_shading", "Smooth", icon="MATSPHERE")
       
bpy.utils.register_class(TP_Display_Sculpt_Dyntopo)


class TP_Display_Sculpt_Mirror(bpy.types.Menu):
    bl_label = "Mirror"
    bl_idname = "tp_display.brush_mirror_sculpt"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN' 
        layout.prop(context.tool_settings.sculpt, "use_symmetry_x", text="X Mirror", toggle=True)
        layout.prop(context.tool_settings.sculpt, "use_symmetry_y", text="Y Mirror", toggle=True)
        layout.prop(context.tool_settings.sculpt, "use_symmetry_z", text="Z Mirror", toggle=True)

bpy.utils.register_class(TP_Display_Sculpt_Mirror)


class TP_Display_Sculpt_Menu(bpy.types.Menu):
    bl_label = "Sculpt [W]"
    bl_idname = "tp_display.menu_sculpt"    

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.menu("tp_display.brush_sculpt", icon='BRUSH_DATA')
        
        layout.separator()             

        if context.sculpt_object.use_dynamic_topology_sculpting:
            layout.operator("sculpt.dynamic_topology_toggle", icon='X', text="Disable Dyntopo")
            if (context.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
                layout.prop(context.tool_settings.sculpt, "constant_detail", text="const.") 
                layout.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')
            else:            
                layout.prop(context.tool_settings.sculpt, "detail_size", text="detail") 
            
            layout.separator() 
            
            layout.operator("sculpt.symmetrize", icon='ARROW_LEFTRIGHT')
            layout.prop(context.tool_settings.sculpt, "symmetrize_direction","")
            layout.operator("sculpt.optimize")
            if (context.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
                layout.operator("sculpt.detail_flood_fill")

            layout.menu("tp_display.brush_dyntopo")
        
        else:
            layout.operator("sculpt.dynamic_topology_toggle", icon='SCULPT_DYNTOPO', text="Enable Dyntopo")


        layout.separator()             

        props = layout.operator("paint.hide_show", text="Box Hide", icon = "BORDER_RECT")
        props.action = 'HIDE'
        props.area = 'INSIDE'
    
        props = layout.operator("paint.hide_show", text="Box Show")
        props.action = 'SHOW'
        props.area = 'INSIDE' 

        layout.separator()
    
        props = layout.operator("paint.mask_flood_fill", text="Fill Mask", icon = "BORDER_RECT")
        props.mode = 'VALUE'
        props.value = 1
           
        props = layout.operator("paint.mask_flood_fill", text="Clear Mask")
        props.mode = 'VALUE'
        props.value = 0
    
        layout.operator("paint.mask_flood_fill", text="Invert Mask").mode='INVERT' 
   
        layout.separator()

        props = layout.operator("paint.hide_show", text="Show All", icon = "RESTRICT_VIEW_OFF")
        props.action = 'SHOW'
        props.area = 'ALL'
    
        props = layout.operator("paint.hide_show", text="Hide Masked", icon = "RESTRICT_VIEW_ON")
        props.area = 'MASKED'
        props.action = 'HIDE'
    
        layout.separator()  

        layout.menu("tp_display.brush_mirror_sculpt", icon='WPAINT_HLT')
        layout.menu("VIEW3D_MT_brush")

        layout.separator()  

        layout.operator("tp_display.wire_all", text="Wire all", icon='WIRE')
        layout.prop(context.object, "show_x_ray", text="X-Ray", icon ="META_CUBE")
        layout.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="GROUP")
        layout.prop(context.space_data, "use_matcap", icon ="MATCAP_01")

        if context.space_data.use_matcap:
            row = layout.column(1)
            row.scale_y = 0.3
            row.scale_x = 0.5
            row.template_icon_view(context.space_data, "matcap_icon") 





class TP_Display_Wire_All(bpy.types.Operator):
    """Wire on All Objects"""
    bl_idname = "tp_display.wire_all"
    bl_label = "Wire on All Objects"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        for obj in bpy.data.objects:
            if obj.show_wire:
                obj.show_all_edges = False
                obj.show_wire = False            
            else:
                obj.show_all_edges = True
                obj.show_wire = True
                             
        return {'FINISHED'} 

bpy.utils.register_class(TP_Display_Wire_All)


def register():

    bpy.utils.register_class(TP_Display_Sculpt_Menu)
      
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Sculpt')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "tp_display.menu_sculpt" 



def unregister():

    bpy.utils.unregister_class(TP_Display_Sculpt_Menu)
              
    if kc:
        km = kc.keymaps['Sculpt']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 
                               
                               
if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=TP_Display_Sculpt_Menu.bl_idname)
  
  
  
   









































