'''
Copyright (C) 2015 Pistiwique

Created by Pistiwique

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Viewport info",
    "description": "Display selected info in the viewport",
    "author": "Pistiwique",
    "version": (0, 1, 0),
    "blender": (2, 75, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "Object" }


# load and reload submodules
##################################    

import sys
sys.modules["viewport_info"] = sys.modules[__name__]
    
from . import developer_utils
modules = developer_utils.setup_addon_modules(__path__, __name__)

# properties
##################################

import bpy

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    Enable_Tab_01 = bpy.props.BoolProperty(default=True)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Enable_Tab_01", text="Custom icon info", icon="QUESTION")
        if self.Enable_Tab_01:
            layout.label("This addon use custom icons for the select_triangles and select_ngons operator")
            layout.label("You can change these icons as you wish it.")
            layout.label("You just have to go to the 'icons' folder being in the addon folder.")
            layout.label("Replace icons by those of your choice but it's VERY IMPORTANT to keep the 'triangle' and ngon' name.")
        
        
# register
################################## 

import traceback

from . properties import viewportInfoCollectionGroup
from . settings_panel import *

def register():    
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()
    register_pcoll()
    bpy.types.Scene.vieportInfo = bpy.props.PointerProperty(type = viewportInfoCollectionGroup)
    bpy.types.VIEW3D_PT_view3d_shading.append(displayViewportInfoPanel)
    bpy.app.handlers.load_post.append(DrawVieportInfoProperties)
    bpy.app.handlers.load_post.append(updateTextProperties)
    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    unregister_pcoll()
    bpy.types.VIEW3D_PT_view3d_shading.remove(displayViewportInfoPanel)

    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()
    del bpy.types.Scene.vieportInfo
    bpy.app.handlers.load_post.remove(DrawVieportInfoProperties)
    bpy.app.handlers.load_post.remove(updateTextProperties)

    print("Unregistered {}".format(bl_info["name"]))
