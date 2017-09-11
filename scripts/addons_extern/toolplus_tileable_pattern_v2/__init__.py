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
    "name": "Tileable Pattern v2",
    "author": "mkbreuer",
    "version": (0, 3),
    "blender": (2, 78, 0),
    "location": "View3D > Create > Tileable Pattern",
    "description": "adds a wired square with instances for tileable pattern creation",
    "warning": "",
    "wiki_url": "",
    "category": "ToolPlus",
    }

        
import bpy, os
from bpy.types import Menu

#line for the panels
from toolplus_tileable_pattern_v2.tp_ui_color      import (View3D_TP_Tileable_Color_Panel)
from toolplus_tileable_pattern_v2.tp_ui_copy       import (View3D_TP_Tileable_Copy_Panel)
from toolplus_tileable_pattern_v2.tp_ui_insert     import (View3D_TP_Tileable_Insert_Panel)
from toolplus_tileable_pattern_v2.tp_ui_pattern    import (View3D_TP_Tileable_Pattern_Panel)
from toolplus_tileable_pattern_v2.tp_ui_power2     import (View3D_TP_Tileable_Array_Panel)
from toolplus_tileable_pattern_v2.tp_ui_view       import (View3D_TP_Tileable_Display_Panel)
from toolplus_tileable_pattern_v2.tp_ui_render     import (View3D_TP_Tileable_Render_Panel)

from . preview_utils_mesh import register_TP_Tileable_Mesh_pcoll, unregister_TP_Tileable_Mesh_pcoll
from . preview_utils_curve import register_TP_Tileable_Curve_pcoll, unregister_TP_Tileable_Curve_pcoll
from . tp_insert_mesh import *
from . tp_insert_curve import *
from . icons.icons import clear_icons
from . import developer_utils


modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())
import traceback

#import rna_keymap_ui

from bpy.props import (StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)


#Tool Panel for update category and hide panel
def update_Tileable_Pattern_Panels_Tools(self, context):
    try:
        bpy.utils.unregister_class(View3D_TP_Tileable_Color_Panel)
        bpy.utils.unregister_class(View3D_TP_Tileable_Insert_Panel)
        bpy.utils.unregister_class(View3D_TP_Tileable_Pattern_Panel)
        bpy.utils.unregister_class(View3D_TP_Tileable_Copy_Panel)
        bpy.utils.unregister_class(View3D_TP_Tileable_Display_Panel)
        bpy.utils.unregister_class(View3D_TP_Tileable_Array_Panel)
        bpy.utils.unregister_class(View3D_TP_Tileable_Render_Panel)

    except:
        pass
 
    if context.user_preferences.addons[__name__].preferences.tools_panel:
        
        View3D_TP_Tileable_Color_Panel.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        View3D_TP_Tileable_Insert_Panel.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        View3D_TP_Tileable_Pattern_Panel.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        View3D_TP_Tileable_Copy_Panel.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        View3D_TP_Tileable_Display_Panel.bl_category = context.user_preferences.addons[__name__].preferences.tools_category       
        View3D_TP_Tileable_Array_Panel.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        View3D_TP_Tileable_Render_Panel.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
 
        bpy.utils.register_class(View3D_TP_Tileable_Color_Panel)
        bpy.utils.register_class(View3D_TP_Tileable_Insert_Panel)
        bpy.utils.register_class(View3D_TP_Tileable_Pattern_Panel)
        bpy.utils.register_class(View3D_TP_Tileable_Copy_Panel)
        bpy.utils.register_class(View3D_TP_Tileable_Display_Panel)
        bpy.utils.register_class(View3D_TP_Tileable_Array_Panel)
        bpy.utils.register_class(View3D_TP_Tileable_Render_Panel)
        


######Preferences######
class View3D_TP_Tileable_Pattern_MenuPrefs(bpy.types.AddonPreferences):
    """ToolPlus Tileable Pattern"""
    bl_idname = __name__    
    
    #3DVIEW
    tools_panel = BoolProperty(default=True, update=update_Tileable_Pattern_Panels_Tools)
    tools_category = StringProperty( name="Category", description="Choose a name for the category panel", default="T+", update=update_Tileable_Pattern_Panels_Tools)    


    #Tabs preferences
    bpy.types.Scene.Enable_Tab_01 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_Tab_02 = bpy.props.BoolProperty(default=False)


    def draw(self, context):
        layout = self.layout


        #Tab Keymap
        layout.prop(context.scene, "Enable_Tab_01", text="Panel Preferences", icon="INFO")   
        if context.scene.Enable_Tab_01:
            box = layout.box()

            row = box.row()
            row.label(text="3D View :", icon='MESH_CUBE')

            row = box.row()
            row.prop(self, "tools_panel", text="TP Tileable Pattern Panel")

            if self.tools_panel:
                row.prop(self, "tools_category")

            
        #Tab Links         
        layout.prop(context.scene, "Enable_Tab_02", text="URL's", icon="URL")   
        if context.scene.Enable_Tab_02:
            box = layout.box()

            row = box.column()
            row.operator("wm.url_open", text="Demo Clip (not actualy)", icon ="CLIP").url = "https://www.youtube.com/watch?v=3LQAooBEifc&feature=autoshare"
            row.operator("wm.url_open", text="blenderartists.org", icon ="PLUS").url = "https://blenderartists.org/forum/showthread.php?387104-Addon-Tileable-Pattern"
            row.operator("wm.url_open", text="google+", icon ="PLUS").url = "https://plus.google.com/+MarvinKBreuer"



#Properties Render
class Dropdown_TP_Render_Props(bpy.types.PropertyGroup):
    display_object_color = bpy.props.BoolProperty(name="Open", description="Open", default=False)        


# This allows you to right click on a button and link to the manual / see templates
def tp_tileable_pattern_manual_map():
    url_manual_prefix = "https://www.youtube.com/watch?v=L70J9ZaA1vs"
    url_manual_mapping = (
        ("tp_ops.reference_grid", "DEMO CLIP"),               
        )
    return url_manual_prefix, url_manual_mapping



################################## 

def register():
    
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()    
    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))    
    
    bpy.utils.register_manual_map(tp_tileable_pattern_manual_map)

    register_TP_Tileable_Mesh_pcoll()
    register_TP_Tileable_Curve_pcoll()

    bpy.types.WindowManager.tp_collapse_render_props = bpy.props.PointerProperty(type = Dropdown_TP_Render_Props)

    #tab category change   
    update_Tileable_Pattern_Panels_Tools(None, bpy.context)


def unregister():
     
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()    
    print("Unregistered {}".format(bl_info["name"]))

    bpy.utils.unregister_manual_map(tp_tileable_pattern_manual_map)

    del bpy.types.WindowManager.tp_collapse_render_props

    clear_icons()   

    unregister_TP_Tileable_Mesh_pcoll()
    unregister_TP_Tileable_Curve_pcoll()


if __name__ == "__main__":
    register()    


