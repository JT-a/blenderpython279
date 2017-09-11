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

from . import _menu_items
from ._menu_items import OperatorArgument, PieMenuItem, PieMenu


CTOOLS_PIEMENU = None

VERSION = 0.4


addon_preferences = None
"""AddonPreferences of ctools.piemenu
:type: bpy.types.AddonPreferences
"""


_addon_preferences = []


def register_menus(*args):
    pass


def unregister_menus(*args):
    pass


def register_addon(addon_preferences):
    """:type addon_preferences: bpy.types.AddonPreferences
    """
    if addon_preferences not in _addon_preferences:
        _addon_preferences.append(addon_preferences)


def unregister_addon(addon_preferences):
    """:type addon_preferences: bpy.types.AddonPreferences
        """
    if addon_preferences in _addon_preferences:
        _addon_preferences.remove(addon_preferences)


def get_menu(idname):
    """:type idname: str
    """
    for addon_prefs in _addon_preferences[::-1]:
        for menu in addon_prefs.menus:
            if menu.active:
                if menu.idname == idname:
                    return menu


def set_addon_preferences(addon_prefs):
    global addon_preferences
    addon_preferences = addon_prefs


def delete_addon_preferences():
    global addon_preferences
    addon_preferences = None


bpy.utils.register_class(OperatorArgument)
bpy.utils.register_class(PieMenuItem)
bpy.utils.register_class(PieMenu)
