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
    "name": "TP Display Modifier",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }



import bpy, re
from bpy import *
             

class TP_Display_Modifier(bpy.types.Menu):
    bl_label = "Modifier [SHIFT+V]"
    bl_idname = "tp_display.modifier_menu"  
    bl_space_type = 'VIEW_3D'
    
    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
        
        layout.operator_menu_enum("object.modifier_add", "type", icon='MODIFIER')              
        layout.menu("tp_display.modifier_visual", text="Visualisation", icon='RESTRICT_VIEW_OFF')

        layout.separator()

        layout.menu("tp_display.modifier_mirror", text="Mirror Setups", icon='MOD_MIRROR')
        layout.menu("tp_display.modifier_subsurf", text="Subsurf-Levels", icon='MOD_SUBSURF')
        layout.menu("tp_display.modifier_array", text="Array Setups", icon='MOD_ARRAY')

        layout.separator()
   
        obj = context.object      
        if obj.mode == 'OBJECT':
            layout.operator("tp_display.apply_modifier", icon = 'FILE_TICK', text="Apply all Mod.")
               
        if obj.mode == 'EDIT':
            layout.operator("tp_display.apply_modifier", icon = 'FILE_TICK', text="Apply all Mod.")        
        
        layout.operator("tp_display.remove_modifier", icon = 'X', text="Delete all Mod.")

        layout.separator()

        layout.operator("view3d.display_modifiers_expand", icon = 'TRIA_DOWN', text="Expand all Mod.")
        layout.operator("view3d.display_modifiers_collapse", icon = 'TRIA_RIGHT', text="Collapse all Mod.")           




class TP_Display_Modifier_SubSurf(bpy.types.Menu):
    bl_label = "Mirror Subsurf"
    bl_idname = "tp_display.modifier_subsurf"
    
    def draw(self, context):
        layout = self.layout
       
        layout.operator("view3d.modifiers_subsurf_level_0",text="0-Level")
        layout.operator("view3d.modifiers_subsurf_level_1",text="1-Level")
        layout.operator("view3d.modifiers_subsurf_level_2",text="2-Level")
        layout.operator("view3d.modifiers_subsurf_level_3",text="3-Level")
        layout.operator("view3d.modifiers_subsurf_level_4",text="4-Level")
        layout.operator("view3d.modifiers_subsurf_level_5",text="5-Level")
        layout.operator("view3d.modifiers_subsurf_level_6",text="6-Level")

bpy.utils.register_class(TP_Display_Modifier_SubSurf) 



class TP_Display_Modifier_Mirror(bpy.types.Menu):
    bl_label = "Mirror Modifier"
    bl_idname = "tp_display.modifier_mirror"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("tp_display.full_mirror_y", text="X Clip-Mirror")
        layout.operator("tp_display.full_mirror_y", text="Y Clip-Mirror")
        layout.operator("tp_display.full_mirror_z", text="Z Clip-Mirror")


bpy.utils.register_class(TP_Display_Modifier_Mirror) 


class TP_Display_Modifier_Array(bpy.types.Menu):
    bl_label = "Array Modifier"
    bl_idname = "tp_display.modifier_array"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("tp_display.xy_array", "XY Array")
        layout.operator("tp_display.xz_array", "XZ Array")
        layout.operator("tp_display.xyz_array", "XYZ Array")

bpy.utils.register_class(TP_Display_Modifier_Array) 




class TP_Display_Modifier_Visual(bpy.types.Menu):
    bl_label = "Visual Modifier"
    bl_idname = "tp_display.modifier_visual"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("view3d.display_modifiers_viewport_on", "View On", icon = 'RESTRICT_VIEW_OFF')
        layout.operator("view3d.display_modifiers_viewport_off", "View Off", icon = 'VISIBLE_IPO_OFF')         
        
        layout.separator() 
 
        layout.operator("view3d.display_modifiers_edit_on",  "Edit On", icon = 'EDITMODE_HLT')
        layout.operator("view3d.display_modifiers_edit_off", "Edit Off", icon = 'SNAP_VERTEX')       

        layout.separator()
                
        layout.operator("view3d.display_modifiers_cage_on", "Cage On", icon = 'OUTLINER_OB_MESH')
        layout.operator("view3d.display_modifiers_cage_off", "Cage Off", icon = 'OUTLINER_DATA_MESH')  
        
        layout.separator()

        layout.operator("view3d.display_modifiers_render_on", "Render On", icon = 'RENDER_STILL') 
        layout.operator("view3d.display_modifiers_render_off", "Render Off", icon = 'RENDER_STILL') 

bpy.utils.register_class(TP_Display_Modifier_Visual) 



class TP_Display_Modifier_Apply(bpy.types.Operator):
    '''apply modifiers'''
    bl_idname = "tp_display.apply_modifier"
    bl_label = "Apply All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
              
        if context.mode == 'OBJECT':
            for obj in bpy.data.objects:
               for mod in obj.modifiers:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
        else:
            bpy.ops.object.editmode_toggle()
           
            for obj in bpy.data.objects:
               for mod in obj.modifiers:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
           
            bpy.ops.object.editmode_toggle()       

        return {"FINISHED"}

bpy.utils.register_class(TP_Display_Modifier_Apply)


    
class TP_Display_Modifier_Remove(bpy.types.Operator):
    '''remove modifiers'''
    bl_idname = "tp_display.remove_modifier"
    bl_label = "Remove All"
    bl_options = {'REGISTER', 'UNDO'}
            
    def execute(self, context):
                    
        if context.mode == 'OBJECT':
            for obj in bpy.data.objects:
               for mod in obj.modifiers:
                    bpy.ops.object.modifier_remove(modifier=mod.name)
        else:
            bpy.ops.object.editmode_toggle()
           
            for obj in bpy.data.objects:
               for mod in obj.modifiers:
                    bpy.ops.object.modifier_remove(modifier=mod.name)
           
            bpy.ops.object.editmode_toggle()       

        return {"FINISHED"}

bpy.utils.register_class(TP_Display_Modifier_Remove)



class TP_Display_XY_Array(bpy.types.Operator):
    bl_label = 'XY_Array'
    bl_idname = 'tp_display.xy_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].count = 5
        bpy.ops.object.modifier_copy(modifier="Array")
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 1
        
        return {'FINISHED'}

bpy.utils.register_class(TP_Display_XY_Array) 



class TP_Display_XZ_Array(bpy.types.Operator):
    bl_label = 'XZ_Array'
    bl_idname = 'tp_display.xz_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].count = 5
        bpy.ops.object.modifier_copy(modifier="Array")
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 1
        
        return {'FINISHED'}

bpy.utils.register_class(TP_Display_XZ_Array) 



class TP_Display_XYZ_Array(bpy.types.Operator):
    bl_label = 'XYZ_Array'
    bl_idname = 'tp_display.xyz_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].count = 5
        bpy.ops.object.modifier_copy(modifier="Array")
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 1
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 0
        bpy.ops.object.modifier_copy(modifier="Array.001")
        bpy.context.object.modifiers["Array.002"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.002"].relative_offset_displace[1] = 0
        bpy.context.object.modifiers["Array.002"].relative_offset_displace[2] = 1        

        return {'FINISHED'}

bpy.utils.register_class(TP_Display_XYZ_Array) 



class TP_Display_MIRROR_X(bpy.types.Operator):
    """Add a x mirror modifier with cage and clipping"""
    bl_idname = "tp_display.full_mirror_x"
    bl_label = "Mirror X"

    def execute(self, context):
    
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}
    
bpy.utils.register_class(TP_Display_MIRROR_X) 



class TP_Display_MIRROR_Y(bpy.types.Operator):
    """Add a y mirror modifier with cage and clipping"""
    bl_idname = "tp_display.full_mirror_y"
    bl_label = "Mirror Y"

    def execute(self, context):
    
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_x = False
        bpy.context.object.modifiers["Mirror"].use_y = True
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}
    
bpy.utils.register_class(TP_Display_MIRROR_Y) 



class TP_Display_MIRROR_Z(bpy.types.Operator):
    """Add a z mirror modifier with cage and clipping"""
    bl_idname = "tp_display.full_mirror_z"
    bl_label = "Mirror Z"

    def execute(self, context):
    
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_x = False
        bpy.context.object.modifiers["Mirror"].use_z = True        
        bpy.ops.view3d.display_modifiers_cage_on()
        bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'} 
      
bpy.utils.register_class(TP_Display_MIRROR_Z) 



def register():

    bpy.utils.register_class(TP_Display_Modifier)    
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'V', 'PRESS', shift=True)
        kmi.properties.name = "tp_display.modifier_menu"      


def unregister():
  
    bpy.utils.unregister_class(TP_Display_Modifier)    
    
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
    bpy.ops.wm.call_menu(name=TP_Display_Modifier.bl_idname)











