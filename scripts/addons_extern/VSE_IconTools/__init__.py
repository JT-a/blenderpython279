#
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
    "name": "VSE IconTools",
    "author": "MKBreuer",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "View3D",
    "description": "IconTools to VSE Header",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sequencer"
}


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'VSE_IconTools-master'))


if "bpy" in locals():
    import imp

    imp.reload(vse_function_to_header)

    print("Reloaded multifiles")


else:

    from . import vse_function_to_header

    print("Imported multifiles")


###################################################


import vse_function_to_header

import bpy


###################################################


def register():

    vse_function_to_header.register()


def unregister():

    vse_function_to_header.unregister()

if __name__ == "__main__":
    register()
