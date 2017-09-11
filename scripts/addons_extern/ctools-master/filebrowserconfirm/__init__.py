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
    'name': 'File Browser Confirm',
    'author': 'chromoly',
    'version': (0, 1, 3),
    'blender': (2, 78, 0),
    'location': 'File Browser',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'User Interface',
}

import importlib
import os
import re

import bpy

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(structures)
    importlib.reload(utils)
    importlib.reload(wrapoperator)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import structures
    from ..utils import utils
    from ..utils import wrapoperator

translation_dict = {
    'ja_JP': {
        ('Operator', 'Overwrite'): '上書き保存',
        ('*', 'Overwrite existing file'): '上書き保存',
        ('*', 'separator: ","\ne.g. "image.save_as, wm.save_as_mainfile"'):
            'オペレーターを "," で区切って記述します\n'
            '例: "image.save_as, wm.save_as_mainfile"',
    }
}


class SaveConfirmPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    use_save_as_mainfile = bpy.props.BoolProperty(
        name='Save As Main File',
        description='bpy.ops.wm.save_as_mainfile()',
        default=True,
    )
    use_save_as_image = bpy.props.BoolProperty(
        name='Save as Image',
        description='bpy.ops.image.save_as()',
        default=True,
    )
    extra_operators = bpy.props.StringProperty(
        name='Extra',
        description='separator: ","\n'
                    'e.g. "image.save_as, wm.save_as_mainfile"',
        default='',
    )

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        column.prop(self, 'use_save_as_mainfile')
        column.prop(self, 'use_save_as_image')
        sp = column.split(0.15)
        col = sp.column()
        text = bpy.app.translations.pgettext_iface('Extra') + ':'
        col.label(text)
        col = sp.column()
        col.prop(self, 'extra_operators', text='')

        self.layout.separator()
        super().draw(context)


attributes = wrapoperator.convert_operator_attributes('file.execute')
execute_internal = attributes['execute']


def execute(self, context):
    prefs = SaveConfirmPreferences.get_instance()
    space_file = context.space_data
    op = space_file.active_operator  # 値はspace_file.operatorと同じ

    bl_idnames = []
    text = re.sub('\s*,\s*', ',', prefs.extra_operators).strip(' ')
    for name in text.split(','):
        bl_idnames.append(utils.bl_idname(name))
    if prefs.use_save_as_mainfile:
        bl_idnames.append('WM_OT_save_as_mainfile')
    if prefs.use_save_as_image:
        bl_idnames.append('IMAGE_OT_save_as')

    if op and op.bl_idname in bl_idnames:
        if 0:
            # 起動直後にディレクトに変更を加えず保存する場合は
            # op.filepathがファイル名のみでディレクトリ情報を含んでいない
            path = op.filepath
            if path.startswith('//') and bpy.data.filepath:
                blend_dir = os.path.dirname(bpy.data.filepath)
                path = os.path.normpath(os.path.join(blend_dir, path[2:]))
        else:
            path = os.path.join(space_file.params.directory,
                                space_file.params.filename)
        if os.path.exists(path):
            kwargs = {}
            if self.properties.is_property_set('need_active'):
                kwargs['need_active'] = self.need_active
            return bpy.ops.file.execute_confirm('INVOKE_DEFAULT', **kwargs)

    return execute_internal(self, context)

attributes['execute'] = execute
FILE_OT_execute = type('FILE_OT_execute', (bpy.types.Operator,), attributes)


class FILE_OT_execute_confirm(bpy.types.Operator):
    bl_idname = 'file.execute_confirm'
    bl_label = 'Overwrite'
    bl_description = 'Overwrite existing file'
    bl_options = {'REGISTER', 'INTERNAL'}

    need_active = attributes['need_active']

    def execute(self, context):
        return execute_internal(self, context)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


classes = [
    SaveConfirmPreferences,
    FILE_OT_execute,
    FILE_OT_execute_confirm,
]


@SaveConfirmPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.translations.register(__name__, translation_dict)


@SaveConfirmPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
    bpy.app.translations.unregister(__name__)


if __name__ == '__main__':
    register()
