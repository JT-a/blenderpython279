# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and / or
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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
"name": "T+ Bounding", 
"author": "marvink.k.breuer (MKB)",
"version": (1, 0),
"blender": (2, 78, 0),
"location": "View3D > TAB Tools > Panel: Bounding / Bound Extrude (Experimental)",
"description": "create bounding box or bounding cylinder on selected objects",
"warning": "",
"wiki_url": "",
"tracker_url": "",
"category": "ToolPlus"}


# LOAD PROPS #
from toolplus_bounding.looptools import (TP_LoopToolsProps)

# LOAD UI #
from toolplus_bounding.panel    import (VIEW3D_TP_BBOX_MESHES_TOOLS)
from toolplus_bounding.panel    import (VIEW3D_TP_BBOX_MESHES_UI)

from toolplus_bounding.fun      import (VIEW3D_TP_Experimental_TOOLS)
from toolplus_bounding.fun      import (VIEW3D_TP_Experimental_UI)

# LOAD ICONS #
from . icons.icons              import load_icons
from . icons.icons              import clear_icons


# LOAD OPERATORS #
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'toolplus_bounding'))
   

if "bpy" in locals():
    import imp
    imp.reload(box) 
    imp.reload(cylinder) 
    imp.reload(extrude) 
    imp.reload(looptools) 
    imp.reload(normals) 
    imp.reload(selection) 

else:
    from . import box         
    from . import cylinder                                          
    from . import extrude                                          
    from . import looptools                                          
    from . import normals                                          
    from . import selection                                          
                                 

# LOAD MODULS #   
import bpy
from bpy import*
from bpy.props import* 
from bpy.types import AddonPreferences, PropertyGroup


# UI REGISTRY #
def update_panel_location(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_BBOX_MESHES_UI)     
        bpy.utils.unregister_class(VIEW3D_TP_BBOX_MESHES_TOOLS)   
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_BBOX_MESHES_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location == 'tools':
        
        VIEW3D_TP_BBOX_MESHES_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category        
        bpy.utils.register_class(VIEW3D_TP_BBOX_MESHES_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location == 'ui':
        bpy.utils.register_class(VIEW3D_TP_BBOX_MESHES_UI)
  
    if context.user_preferences.addons[__name__].preferences.tab_location == 'off':
        pass


def update_panel_location_experimental(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Experimental_UI)     
        bpy.utils.unregister_class(VIEW3D_TP_Experimental_TOOLS)   
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Experimental_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_exp == 'tools':
        
        VIEW3D_TP_Experimental_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_exp        
        bpy.utils.register_class(VIEW3D_TP_Experimental_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_exp == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Experimental_UI)
  
    if context.user_preferences.addons[__name__].preferences.tab_location_exp == 'off':
        pass


# REGISTRY: PANEL TOOLS # 
def update_display_tools(self, context):

    try:
        return True
    except:
        pass

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'on':
        return True

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'off':
        pass    


# ADDON PREFERENCES #
class TP_Panels_Preferences(AddonPreferences):
    bl_idname = __name__
    
    prefs_tabs = EnumProperty(
        items=(('info',       "Info",       "Info"),
               ('location',   "Location",   "Location"),
               ('tools',      "Tools",      "Tools"),
               ('url',        "URLs",       "URLs")),
               default='info')

    #TAB LOACATION #           
    tab_location = EnumProperty(
        name = 'Panel Location',
        description = 'location switch',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'on or off for panel in the shelfs')),
               default='tools', update = update_panel_location)

    tab_location_exp = EnumProperty(
        name = 'Panel Location',
        description = 'location switch',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'on or off for panel in the shelfs')),
               default='off', update = update_panel_location_experimental)


    # UPADTE: TOOLSETS #
    tab_display_apply = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Apply Transform on', 'enable more tools in panel'), ('off', 'Apply Transform off', 'disable more tools in panel')), default='off', update = update_display_tools)

    tab_display_select = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Select on', 'enable more tools in panel'), ('off', 'Select off', 'disable more tools in panel')), default='off', update = update_display_tools)

    tab_display_history = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable more tools in panel'), ('off', 'History off', 'disable more tools in panel')), default='off', update = update_display_tools)


    # UPADTE: PANEL #
    tools_category = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_location)
    tools_category_exp = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_location_experimental)

    def draw(self, context):
        layout = self.layout
        
        # INFO #
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)
       
        if self.prefs_tabs == 'info':
            row = layout.row()
            row.label(text="Welcome to T+ Bounding!")

            row = layout.column()
            row.label(text="This addons allows you to create bounding geometry as box or cylinder")
            row.label(text="You can locate the panel in toolshelf [T] or property shelf [N].")
            row.label(text="Or use only the Operators in the default ADD Mesh Menu [SHIFT+A]")
            row.label(text="Have Fun! ;)")


        # LOACATION #
        if self.prefs_tabs == 'location':
            box = layout.box().column(1)
             
            row = box.row(1)  
            row.label("Location: MainPanel ")
            
            row= box.row(1)
            row.prop(self, 'tab_location', expand=True)

            box.separator()
                                               
            if self.tab_location == 'tools':
                
                row = box.row(1)                                                
                row.prop(self, "tools_category")
         
            box.separator()

            row = box.row(1)  
            row.label("Location: Experimental Panel ")
            
            row= box.row(1)
            row.prop(self, 'tab_location_exp', expand=True)

            box.separator()
                                               
            if self.tab_location_exp == 'tools':
                
                row = box.row(1)                                                
                row.prop(self, "tools_category_exp")
         
            box.separator()



        # TOOLS #
        if self.prefs_tabs == 'tools':

            box = layout.box().column(1)

            row = box.row()
            row.label(text="ToolSet in Panel", icon ="INFO")

            row = box.column_flow(4)
            row.prop(self, 'tab_display_apply', expand=True) 
            row.prop(self, 'tab_display_select', expand=True) 
            row.prop(self, 'tab_display_history', expand=True) 

            box.separator() 
            box.separator()

            row = layout.row()
            row.label(text="! save user settings for permant on/off !", icon ="INFO")

            box.separator() 



        # WEB #
        if self.prefs_tabs == 'url':
            row = layout.row()
            row.operator('wm.url_open', text = 'GitHub', icon = 'SCRIPTWIN').url = "https://github.com/mkbreuer/ToolPlus"
            row.operator('wm.url_open', text = 'Thread', icon = 'BLENDER').url = "https://blenderartists.org/forum/showthread.php?435147-Addon-T-Bounding&p=3221535#post3221535"



# PROPS #
class Dropdown_BBox_Props(bpy.types.PropertyGroup):

    display_bbox_set = bpy.props.BoolProperty(name = "Display Setting", description = "Display Setting", default = False)
    display_bcyl_set = bpy.props.BoolProperty(name = "Display Setting", description = "Display Setting", default = False)



# ADD TO DEFAULT MENU #  
from .icons.icons import load_icons 
def draw_item(self, context):
    icons = load_icons()

    layout = self.layout

    layout.separator()    

    button_bbox = icons.get("icon_bbox") 
    layout.operator("tp_ops.bbox_for_menu", text="Boundig Box", icon_value=button_bbox.icon_id)  

    button_bcyl = icons.get("icon_bcyl") 
    layout.operator("tp_ops.bcylinder_for_menu",text="Boundig Cylinder", icon_value=button_bcyl.icon_id)


# REGISTRY #

import traceback

def register():

    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    update_panel_location(None, bpy.context)
    update_display_tools(None, bpy.context)
    update_panel_location_experimental(None, bpy.context)

    # TO MENU
    bpy.types.INFO_MT_mesh_add.append(draw_item) 
   
    # PROPS
    bpy.types.WindowManager.bbox_window = bpy.props.PointerProperty(type = Dropdown_BBox_Props)    
     
    # LOOPTOOLS
    bpy.types.WindowManager.tp_props_looptools = bpy.props.PointerProperty(type = TP_LoopToolsProps) 


def unregister():

    # PROPS    
    del bpy.types.WindowManager.bbox_window

    # LOOPTOOLS
    del bpy.types.WindowManager.tp_props_looptools

    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()


if __name__ == "__main__":
    register()
        
        










