#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ##### END GPL LICENSE BLOCK #####

#This states the metadata for the plugin
bl_info = {
    "name": "Polysaurus",
    "author": "Takanu Kyriako, w/code from Stanislav Blinov, Yigit Savtur",
    "version": (1,0),
    "blender": (2, 7, 7),
    "api": 39347,
    "location": "3D View > Sculpt Mode > Tools > Poly",
    "description": "Sculpt masking presets and shortcuts, built from the Mask Tools addon.",
    "warning": "Beta",
    "tracker_url": "",
    "category": "Sculpting"
}

# Start importing all the addon files
# The init file just gets things started, no code needs to be placed here.
if "bpy" in locals():
    import imp
    print(">>>>>>>>>>> Reloading Plugin", __name__, "<<<<<<<<<<<<")
    if "properties" in locals():
        imp.reload(properties)
    if "user_interface" in locals():
        imp.reload(user_interface)
    if "mask_menu" in locals():
        imp.reload(mask_menu)
    if "mask_tools_ops" in locals():
        imp.reload(mask_tools_ops)


print(">>>>>>>>>>> Beginning Import", __name__, "<<<<<<<<<<<<")

import bpy
from . import properties
from . import user_interface
from . import mask_menu
from . import mask_tools_ops
from bpy.props import IntProperty, BoolProperty, StringProperty, PointerProperty, CollectionProperty, EnumProperty
from bpy.types import AddonPreferences, PropertyGroup, Menu

print("End of import")

class PolySAddonPreferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        row = layout.column(align=True)
        row.label("Psst.  I hear that if you press \"Alt + M\" while in Sculpt mode, you get a sweet pie menu.")
        row.label("Don't tell anyone I told you this though... <_<")

addon_keymaps = []

def register():
    bpy.utils.register_module(__name__)
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'M', 'PRESS', alt=True)
        kmi.properties.name = "pie.maskstandard"
#        kmi.active = True
        addon_keymaps.append(kmi)


def unregister():
    bpy.utils.unregister_module(__name__)

    wm = bpy.context.window_manager

    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['Sculpt']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu_pie':
                if kmi.properties.name == "pie.maskstandard":
                    km.keymap_items.remove(kmi)

    # clear the list
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
