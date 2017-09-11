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


import bpy

from CTOOLS_MODULE_NAME.piemenu.menu_items import EnumDrawType, \
    EnumQuickAction, EnumHighlight


CTOOLS_PIEMENU = None

VERSION = CURRENT_VERSION


# AddonPreferences of ctools.piemenu
addon_preferences = None

_registered_addon_preferences = []


def register_addon(addon_prefs):
    """:type addon_prefs: bpy.types.AddonPreferences
    """
    if addon_prefs not in _registered_addon_preferences:
        _registered_addon_preferences.append(addon_prefs)


def unregister_addon(addon_prefs):
    """:type addon_prefs: bpy.types.AddonPreferences
    """
    if addon_prefs in _registered_addon_preferences:
        _registered_addon_preferences.remove(addon_prefs)


def get_menu(idname):
    """:type idname: str
    """
    for addon_prefs in _registered_addon_preferences[::-1]:
        if isinstance(addon_prefs.menus, dict):
            menus = addon_prefs.menus.values()
        else:
            menus = addon_prefs.menus
        for menu in menus:
            if menu.idname == idname:
                return menu


# Helper function
def get_keymap(name, keyconfig="addon"):
    """Return result of KeyMaps.new()
    # ref: addongroup/_keymap.py: 319: def get_keymap(name, keyconfig="addon"):
    :type name: str
    :param keyconfig: "addon" or "user" or "blender" or
                      "default"(same as "blender")
    :type keyconfig: str
    :rtype: bpy.types.KeyMap
    """
    import bpy_extras.keyconfig_utils

    # ref: KeyMap.is_modal
    modal_keymaps = {
        "View3D Gesture Circle", "Gesture Border",
        "Gesture Zoom Border", "Gesture Straight Line",
        "Standard Modal Map", "Knife Tool Modal Map",
        "Transform Modal Map", "Paint Stroke Modal", "View3D Fly Modal",
        "View3D Walk Modal", "View3D Rotate Modal", "View3D Move Modal",
        "View3D Zoom Modal", "View3D Dolly Modal", "Eyedropper Modal Map"}

    keyconfigs = bpy.context.window_manager.keyconfigs
    if keyconfig == "addon":  # "Blender Addon"
        kc = keyconfigs.addon
    elif keyconfig == "user":  # "Blender User"
        kc = keyconfigs.user
    elif keyconfig in {"default", "blender"}:  # "Blender"
        kc = keyconfigs.default
    else:
        raise ValueError()
    if not kc:
        return None

    # if 'INVALID_MODAL_KEYMAP' and name in modal_keymaps:
    #     msg = "not support modal keymap: '{}'".format(name)
    #     raise ValueError(msg)

    def get(ls, name):
        for keymap_name, space_type, region_type, children in ls:
            if keymap_name == name:
                is_modal = keymap_name in modal_keymaps
                return kc.keymaps.new(keymap_name, space_type=space_type,
                                      region_type=region_type,
                                      modal=is_modal)
            elif children:
                km = get(children, name)
                if km:
                    return km

    km = get(bpy_extras.keyconfig_utils.KM_HIERARCHY, name)
    if not km:
        def get_names(ls):
            for keymap_name, space_type, region_type, children in ls:
                yield keymap_name
                yield from get_names(children)

        all_names = list(get_names(
            bpy_extras.keyconfig_utils.KM_HIERARCHY))
        for name in modal_keymaps:
            all_names.remove(name)
        msg = "Keymap '{}' not in builtins\n".format(name)
        msg += "[\n"
        msg += "\n".join(["    '" + name + "'" for name in all_names])
        msg += "\n]\n"
        raise ValueError(msg)
    return km
