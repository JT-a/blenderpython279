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
    "name": "Bar Add-on",
    "version": (0, 1),
    "description": "Addon group test",
    "category": "3D View",
}


if "bpy" in locals():
    BarAddonPreferences.reload_submodules()
else:
    from ... import addongroup

import bpy


class BarAddonPreferences(addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__


classes = [
    BarAddonPreferences,
]


@BarAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


@BarAddonPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
