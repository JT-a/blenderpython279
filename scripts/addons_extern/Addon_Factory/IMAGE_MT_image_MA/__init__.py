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
    "name": "Image Menu's",
    "author": "Meta Androcto",
    "version": (0, 2),
    "blender": (2, 75, 0),
    "location": "Image Related",
    "description": "Tools for managing Images",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6"\
        "/Py/Scripts",
    "tracker_url": "",
    "category": "Addon Factory"}


if "bpy" in locals():
    import importlib
    importlib.reload(IMAGE_MT_image)
    importlib.reload(IMAGE_MT_select)
    importlib.reload(IMAGE_MT_uvs)
    importlib.reload(IMAGE_MT_view)

else:
    from . import IMAGE_MT_image
    from . import IMAGE_MT_select
    from . import IMAGE_MT_uvs
    from . import IMAGE_MT_view

import bpy

def register():
    bpy.utils.register_module(__name__)
    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.IMAGE_MT_image.append(IMAGE_MT_image.menu)
    bpy.types.IMAGE_MT_select.append(IMAGE_MT_select.menu)
    bpy.types.IMAGE_MT_uvs.append(IMAGE_MT_uvs.menu)
    bpy.types.IMAGE_MT_view.append(IMAGE_MT_view.menu)


def unregister():

    # Remove "Extras" menu from the "Add Mesh" menu.
	bpy.types.IMAGE_MT_image.remove(IMAGE_MT_image.menu)
	bpy.types.IMAGE_MT_select.remove(IMAGE_MT_select.menu)
	bpy.types.IMAGE_MT_uvs.remove(IMAGE_MT_uvs.menu)
	bpy.types.IMAGE_MT_view.remove(IMAGE_MT_view.menu)
	bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
