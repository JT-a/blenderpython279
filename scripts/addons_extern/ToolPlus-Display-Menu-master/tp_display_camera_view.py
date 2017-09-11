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
    "name": "TP Display Camera View",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }



import bpy
from bpy import *



class TP_Display_Camera_View_Menu(bpy.types.Menu):
    """Align Camera & View"""   
    bl_label = "View & Camera [ALT+1]"
    bl_idname = "tp_display.camera_view_menu"

    def draw(self, context):
        from math import pi
        layout = self.layout
        view = context.space_data

        layout.operator_context = 'INVOKE_REGION_WIN'                
       
        layout.menu("tp_display.3d_navigation_menu", icon = "MANIPUL")
        layout.menu("tp_display.view_menu", icon = "VIEWZOOM")  

        layout.separator()

        layout.operator("object.camera_add")                

        layout.separator()

        layout.operator("view3d.zoom_camera_1_to_1", text="CamZoom 1:1")          
        layout.operator("view3d.viewnumpad", text="Active Camera").type = 'CAMERA'
        layout.operator("view3d.camera_to_view", text="Active Cam to View")
        layout.operator("view3d.object_as_camera", text="Active Object as Cam")
        
        layout.operator("view3d.camera_to_view_selected", text="Active Cam to Selected") 

        layout.separator()
        
        layout.menu("VIEW3D_MT_object_showhide", icon = "RESTRICT_VIEW_OFF")
        layout.operator("view3d.layers", text="Show All Layers").nr = 0          

        layout.separator()

        layout.operator("tp_display.look_at_it", text="Look at Obj", icon = "FRAME_NEXT")
        layout.operator("tp_display.look_at_cursor", text="Look at Cursor")                
        layout.menu("tp_display.look_at_menu", text="Look at Menu")                

        layout.separator()            
        
        layout.menu("tp_display.border_menu", icon = "RENDER_REGION")
 
        layout.separator()

        layout.menu("tp_display.lock_menu")

        layout.separator()        
        
        layout.menu("tp_display.animation_player", text="Animation Player", icon = "PLAY")

        layout.separator()      
        
        layout.operator("view3d.fly", icon = "NDOF_FLY")
        layout.operator("view3d.walk", icon = "NDOF_TRANS")             

               

class TP_Display_Lock_Menu(bpy.types.Menu):
    bl_label = "Lock View"
    bl_idname = "tp_display.lock_menu"    

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'  
        view = context.space_data

        layout.prop(context.space_data, "lock_camera")        
        layout.operator("view3d.view_lock_to_active")
        layout.operator("view3d.view_lock_clear") 

        layout.separator()
        
        layout.label(text="View to Object:")        
        layout.prop(view, "lock_object", text="")
           

bpy.utils.register_class(TP_Display_Lock_Menu)   



class TP_Display_View_Menu(bpy.types.Menu):
    bl_label = "View Menu"
    bl_idname = "tp_display.view_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
     
        layout.operator("view3d.view_all", icon = "VIEWZOOM") 
        layout.operator("view3d.view_center_cursor", text = "View to Cursor")
        layout.operator("view3d.view_selected", text = "View to Selected")
        layout.operator("view3d.zoom_border", text="Zoom with Border", icon = "BORDERMOVE")        

        layout.separator()
                    
        layout.operator("view3d.localview", text="View Global/Local")
        layout.operator("view3d.view_persportho", text="View Persp/Ortho")        


bpy.utils.register_class(TP_Display_View_Menu)   



class TP_Display_Border_Menu(bpy.types.Menu):
    bl_label = "Border..."
    bl_idname = "tp_display.border_menu"
    
    def draw(self, context):
        layout = self.layout        
        view = context.space_data 
               
        layout.prop(view, "use_render_border", text = "Render Border")
        layout.operator("view3d.render_border", text="Draw Render Border...")        
        layout.operator("view3d.clip_border", text="Draw Clipping Border...")

bpy.utils.register_class(TP_Display_Border_Menu)



class TP_Display_Animation_Player(bpy.types.Menu):
    bl_label = "Animation Player"
    bl_idname = "tp_display.animation_player"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        toolsettings = context.tool_settings
        screen = context.screen

        layout.operator("screen.frame_jump", text="Jump REW", icon='REW').end = False
        layout.operator("screen.keyframe_jump", text="Previous FR", icon='PREV_KEYFRAME').next = False
        layout.operator("screen.animation_play", text="Reverse", icon='PLAY_REVERSE').reverse = True
        
        layout.operator("screen.animation_play", text="PLAY", icon='PLAY')
        
        layout.operator("screen.animation_play", text="Stop", icon='PAUSE')
        
        layout.operator("screen.keyframe_jump", text="Next FR", icon='NEXT_KEYFRAME').next = True
        layout.operator("screen.frame_jump", text="Jump FF", icon='FF').end = True    

bpy.utils.register_class(TP_Display_Animation_Player)



def register():

    bpy.utils.register_class(TP_Display_Camera_View_Menu)      
               
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'ONE', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.camera_view_menu"      


def unregister():
  
    bpy.utils.unregister_class(TP_Display_Camera_View_Menu)

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
    bpy.ops.wm.call_menu(name=TP_Display_Camera_View_Menu.bl_idname)        








