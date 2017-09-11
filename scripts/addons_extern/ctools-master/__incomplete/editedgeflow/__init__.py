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
    'name': 'Edit Edge Flow',
    'author': 'chromoly',
    'version': (0, 1),
    'blender': (2, 78, 0),
    'location': 'View3D',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View',
}


import importlib
import math

import bpy

try:
    importlib.reload(registerinfo)
    importlib.reload(utils)
except NameError:
    from . import registerinfo
    from . import utils


class EditEdgeFlowPreferences(
        utils.AddonPreferences,
        registerinfo.AddonRegisterInfo,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        super().draw(context, self.layout)


class Spline:
    def __init__(self, points):
        n = len(points)
        a = [0.0] * n
        b = [0.0] * n
        c = [0.0] * n
        d = [0.0] * n
        num = len(points) - 1








classes = [
    EditEdgeFlowPreferences,
]


@EditEdgeFlowPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = EditEdgeFlowPreferences.get_keymap('Screen Editing')
        # kmi = km.keymap_items.new('view3d.quadview_move', 'LEFTMOUSE', 'PRESS',
        #                           head=True)


@EditEdgeFlowPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
