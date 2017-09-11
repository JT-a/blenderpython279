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
    'name': '',
    'author': 'chromoly',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'location': 'View3D',
    'description': '',
    'wiki_url': '',
    'category': '3D View',
}


import importlib

import bpy

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(registerinfo)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import registerinfo


translation_dict = {
    'ja_JP': {
        ('*', 'String'): '文字列',
    }
}


class Preferences(
        addongroup.AddonGroupPreferences,
        registerinfo.AddonRegisterInfo,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        layout.separator()
        super().draw(context)


class Operator(bpy.types.Operator):
    bl_idname = ''
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        return True

    def cancel(self, context):
        pass

    def modal(self, context, event):
        if event.type in {'INBETWEEN_MOUSEMOVE', 'MOUSEMOVE'}:
            return {'PASS_THROUGH'}
        elif event.type.startswith('TIMER'):
            return {'PASS_THROUGH'}
        else:
            return {'RUNNING_MODAL'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return {'FINISHED'}


classes = [
    Preferences,
    Operator,
]


@Preferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.translations.register(__name__, translation_dict)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = Preferences.get_keymap('Mesh')
        # kmi = km.keymap_items.new('foo.bar', 'B', 'PRESS')


@Preferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)


if __name__ == '__main__':
    register()
