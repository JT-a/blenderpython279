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
# by meta-androcto, parts based on work by Erich Toven #

bl_info = {
    "name": "Info Menus",
    "author": "Meta Androcto, ",
    "version": (0, 2),
    "blender": (2, 75, 0),
    "location": "Info Header: File, Render, Window, Help",
    "description": "Custom menu items.",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6"\
        "/Py/Scripts",
    "tracker_url": "",
    "category": "Addon Factory"}


if "bpy" in locals():
    import importlib
    importlib.reload(INFO_MT_file_external_data)
    importlib.reload(INFO_MT_file)
    importlib.reload(INFO_MT_help)
    importlib.reload(INFO_MT_window)

else:
    from . import INFO_MT_file
    from . import INFO_MT_file_external_data
    from . import INFO_MT_help
    from . import INFO_MT_window

import bpy

def register():
    bpy.utils.register_module(__name__)
    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.INFO_MT_file.append(INFO_MT_file.menu)
    bpy.types.INFO_MT_file_external_data.append(INFO_MT_file_external_data.menu)
    bpy.types.INFO_MT_help.append(INFO_MT_help.menu)
    bpy.types.INFO_MT_help.append(INFO_MT_help.menu_func)
    bpy.types.INFO_MT_window.append(INFO_MT_window.menu)


def unregister():
	bpy.utils.unregister_module(__name__)
    # Remove "Extras" menu from the "Add Mesh" menu.
	bpy.types.INFO_MT_file.remove(INFO_MT_file.menu)
	bpy.types.INFO_MT_file_external_data.remove(INFO_MT_file_external_data.menu)
	bpy.types.INFO_MT_help.remove(INFO_MT_help.menu)
	bpy.types.INFO_MT_help.remove(INFO_MT_help.menu_func)
	bpy.types.INFO_MT_window.remove(INFO_MT_window.menu)

if __name__ == "__main__":
    register()
