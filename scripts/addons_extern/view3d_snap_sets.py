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
    "name": "Snap Sets",
    "author": "MKB",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "ToolPlus"
    }


import bpy
from bpy import*
from bpy.props import *


class VIEW3D_Snap_Sets(bpy.types.Menu):
    """Snap Sets :)"""
    bl_idname = "snap_menu.pivot_snap"
    bl_label = "Snap Sets :)"

    def draw(self, context):
        layout = self.layout     
        layout.operator_context = 'INVOKE_REGION_WIN'
      
        layout.operator("snap_ops.grid")         
        layout.operator("snap_ops.place")         
        layout.operator("snap_ops.retopo")         
        layout.operator("snap_ops.active_vert")         
        layout.operator("snap_ops.closest_vert")         
        layout.operator("snap_ops.active_3d")         
        layout.operator("snap_ops.selected_3d")         



class VIEW3D_Snapset_Grid(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "snap_ops.grid"
    bl_label = "Absolute Grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'

        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'INCREMENT'
        bpy.context.scene.tool_settings.use_snap_grid_absolute = True
        bpy.context.scene.tool_settings.use_snap_align_rotation = False            

        return {'FINISHED'}


class VIEW3D_Snapset_Place(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "snap_ops.place"
    bl_label = "Place Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
        
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'FACE'
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        bpy.context.scene.tool_settings.use_snap_align_rotation = True
        bpy.context.scene.tool_settings.use_snap_project = True
                        
        return {'FINISHED'}


class VIEW3D_Snapset_Retopo(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "snap_ops.retopo"
    bl_label = "Mesh Retopo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
                    
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'FACE'
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False
            
            
        return {'FINISHED'}


class VIEW3D_Snapset_Active_Vert(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "snap_ops.active_vert"
    bl_label = "Active Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'            
        
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False       
 
        return {'FINISHED'}



class VIEW3D_Snapset_Closest_Vert(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "snap_ops.closest_vert"
    bl_label = "Closest Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'            
        
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False       
 
        return {'FINISHED'}



class VIEW3D_Snapset_Active_3d(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "snap_ops.active_3d"
    bl_label = "3d Cursor > Active"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'CURSOR'            

        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False   
        bpy.ops.view3d.snap_cursor_to_active()                    

        return {'FINISHED'}
            


class VIEW3D_Snapset_Selected_3d(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "snap_ops.selected_3d"
    bl_label = "3d Cursor > Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            
    
        bpy.context.space_data.pivot_point = 'CURSOR'  

        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False   

        bpy.ops.view3d.snap_cursor_to_selected()

        return {'FINISHED'}


            
                 
def register():

    bpy.utils.register_class(VIEW3D_Snapset_Grid)
    bpy.utils.register_class(VIEW3D_Snapset_Place)
    bpy.utils.register_class(VIEW3D_Snapset_Retopo)
    bpy.utils.register_class(VIEW3D_Snapset_Active_Vert)
    bpy.utils.register_class(VIEW3D_Snapset_Closest_Vert)
    bpy.utils.register_class(VIEW3D_Snapset_Active_3d)
    bpy.utils.register_class(VIEW3D_Snapset_Selected_3d)


    bpy.utils.register_class(VIEW3D_Snap_Sets)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        
        #Change here the Type of Event for your own shortcut, default ALT+TWO
        kmi = km.keymap_items.new('wm.call_menu', 'TWO', 'PRESS', alt = True) #ctrl = True, shift = True)              

        kmi.properties.name = "snap_menu.pivot_snap" 


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_Snapset_Grid)
    bpy.utils.unregister_class(VIEW3D_Snapset_Place)
    bpy.utils.unregister_class(VIEW3D_Snapset_Retopo)
    bpy.utils.unregister_class(VIEW3D_Snapset_Active_Vert)
    bpy.utils.unregister_class(VIEW3D_Snapset_Closest_Vert)
    bpy.utils.unregister_class(VIEW3D_Snapset_Active_3d)
    bpy.utils.unregister_class(VIEW3D_Snapset_Selected_3d)

    bpy.utils.unregister_class(VIEW3D_Snap_Sets)
           
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
    #bpy.ops.wm.call_menu(name=VIEW3D_Snap_Sets.bl_idname)
