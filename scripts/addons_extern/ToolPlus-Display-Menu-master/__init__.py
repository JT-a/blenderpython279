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
    "name": "ToolPlus Display Menus",
    "author": " Marvin.K.Breuer",
    "version": (0, 1, 0),
    "blender": (2, 7, 7),
    "location": "View 3D",
    "description": "Different Hotkey Menus",
    "warning": "",
    "wiki_url": "https://github.com/mkbreuer",
    "category": "ToolPlus",
}
        
import bpy, os
from bpy.types import Menu
from . import developer_utils

modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())
import traceback

from bpy.props import (StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)

 


######Preferences######
class TP_Display_MenuPrefs(bpy.types.AddonPreferences):
    """ToolPlus Display Menus"""
    bl_idname = __name__    
    
    #Tabs preferences
    bpy.types.Scene.Enable_Tab_01 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_Tab_02 = bpy.props.BoolProperty(default=False)


    def draw(self, context):
        layout = self.layout
            
        
        row = layout.row()
        #Tab Keymap
        row.prop(context.scene, "Enable_Tab_01", text="Keymap", icon="URL")   
        if context.scene.Enable_Tab_01:
            #Add the keymap in the prefs
            col = layout.column()
            col.label("Changing Keymap: got to Input > Key Binding > insert Shortcut > add your new Shortcut", icon="ERROR")
            col.label("eg.: Disable specific default Delete [X] to use the alternative Delete Menu [X]", icon="ERROR")           

            col = layout.column_flow(2)
            col.label("File Menu [ALT W]")
            col.label("Selection Menu [ALT Q]")
            col.label("Modifier Menu [SHIFT V]")

            col.label("Align Menu [\]")
            col.label("Orientation Menu [ALT \]")
            col.label("Window Menu [CTRL \]")
            col.label("View & Camera Menu [ALT 1]")
            col.label("Shading Menu [ALT 2]")
            col.label("Display Menu [ALT 3]")

            col.label("Vertex Edit Menu [CTRL V]")
            col.label("Edge Edit Menu [CTRL E]")
            col.label("Edge Visual Menu [SHIFT E]")
            col.label("Face Edit Menu [CTRL F]")
            col.label("Face Visual Menu [SHIFT F]")
            col.label("Vertex Group Menu [<]")
            col.label("Curve & Surface Menu [CTRL F]")

            col.label("Sculpt Menu [W]")
            col.label("Texture Paint Menu [W]")
            col.label("Vertex Paint Menu [W]")
            col.label("Weight Paint Menu [W]")

            col.label("Armature Menu [CTRL F]")
            col.label("Pose Menu [CTRL F]")
            
            col.label("Delete Menu [X]")

            
        #Tab Links         
        row.prop(context.scene, "Enable_Tab_02", text="URL's", icon="URL")   
        if context.scene.Enable_Tab_02:

            row = layout.row()
            row.operator("wm.url_open", text="Github").url = "https://github.com/mkbreuer"
            row.operator("wm.url_open", text="Google+").url = "https://plus.google.com/+MarvinKBreuer"



def register():
    
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()    
    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))    

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.file_menu"  

        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'BACK_SLASH', 'PRESS', alt = True)
        kmi.properties.name = "tp_display.menu_orientation"

        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.menu_selection" 

        km = kc.keymaps.new(name='Image Paint')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "tp_display.paint_menu" 

        km = kc.keymaps.new(name='Weight Paint')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "tp_display.paint_menu"         

        km = kc.keymaps.new(name='Vertex Paint')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "tp_display.paint_menu"         

        km = kc.keymaps.new(name='Sculpt')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "tp_display.menu_sculpt"   

        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'BACK_SLASH', 'PRESS')
        kmi.properties.name = "tp_display.menu_align"

        km = kc.keymaps.new(name='Pose')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.special_armature"      

        km = kc.keymaps.new(name='Armature')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.special_armature"   

        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'ONE', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.camera_view_menu"    

        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'V', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.vertices_edm"    

        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'E', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.edge_one_edm"   

        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'E', 'PRESS', shift=True)
        kmi.properties.name = "tp_display.edge_two_edm"  

        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.face_one_edm"   
        
        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', shift=True)
        kmi.properties.name = "tp_display.face_two_edm"           
        
        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'GRLESS', 'PRESS')
        kmi.properties.name = "tp_display.vertex_group"

        km = kc.keymaps.new(name='Curve')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.curve_surface"           
        
        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'X', 'PRESS')
        kmi.properties.name = "tp_display.delete_clear"       

        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'V', 'PRESS', shift=True)
        kmi.properties.name = "tp_display.modifier_menu"   

        km = kc.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'V', 'PRESS', shift=True)
        kmi.properties.name = "tp_display.modifier_menu"   

        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'THREE', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.object_mesh"            

        km = kc.keymaps.new(name='Window')
        kmi = km.keymap_items.new('wm.call_menu', 'BACK_SLASH', 'PRESS', ctrl = True)
        kmi.properties.name = "tp_display.view_extend_menu"   

        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'TWO', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.menu_3d_view" 
        


def unregister():
     
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()    
    print("Unregistered {}".format(bl_info["name"]))

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps['3D View']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 

        km = kc.keymaps['Window']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break  

        km = kc.keymaps['Mesh']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break  

        km = kc.keymaps['Curve']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break  

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

        km = kc.keymaps['Sculpt']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 

        km = kc.keymaps['Armature']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 

        km = kc.keymaps['Pose']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break                                  