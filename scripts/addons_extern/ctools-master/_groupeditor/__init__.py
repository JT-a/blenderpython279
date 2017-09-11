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
    'name': 'Group Editor',
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
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty


translation_dict = {
    'ja_JP': {
        ('*', 'String'): '文字列',
    }
}


class AddonPreferencesGroupEditor(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__


class EditInstance(bpy.types.Operator):
    bl_idname = 'group.edit_instance'
    bl_label = 'Edit Instance'
    bl_options = {'REGISTER', 'UNDO'}

    def enter(self, context):
        """
        :type context: bpy.types.Context
        """

        # 確認
        scene = context.scene
        actob = context.active_object
        if actob.dupli_type == 'GROUP':
            group = actob.dupli_group
        else:
            group = None
        if not group:
            return False

        # IDPropertyへGroupのオフセット、レイヤー、シーンをバックアップ
        group['dupli_offset'] = list(group.dupli_offset)
        for ob in group.objects:
            ob['layers'] = list(ob.layers)
            scenes = [item for item in bpy.data.user_map([ob])
                      if isinstance(item, bpy.types.Scene)]
            ob['scenes'] = [scn.name for scn in scenes]

        # emptyを追加してグループのオブジェクトを全部子にする
        offset = group.dupli_offset
        bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False,
                                 location=offset, rotation=(0, 0, 0))
        empty_extracted_group = context.active_object
        empty_extracted_group.layers = actob.layers
        for ob in group.objects:
            ob.select = True
        # FIXME: parent階層
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        empty_extracted_group.matrix_world = actob.matrix_world
        actob.dupli_group = None

        group.dupli_offset = empty_extracted_group.matrix_world.to_translation()

        # groupを利用しているオブジェクトに対して修正を行う
        for ob in context.selected_objects:
            ob.select = False
        for ob in list(group.users_dupli_group):
            if ob == actob:
                continue
            ob.dupli_group = None
            bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False,
                                     location=(0, 0, 0), rotation=(0, 0, 0))
            empty = context.active_object
            empty.layers = ob.layers
            empty.dupli_type = 'GROUP'
            empty.dupli_group = group
            empty.hide_select = True

            empty.matrix_world = ob.matrix_world * actob.matrix_world.to_3x3().inverted().to_4x4()
            empty.select = True
            ob.select = True
            scene.objects.active = ob
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
            ob.select = False
            empty.select = False

        for ob in group.objects:
            ob.select = True

        # FIXME groupの元あった場所に追加

    def exit(self, context):
        """
        :type context: bpy.types.Context
        """
        pass

    def modal(self, context, event):
        """
        :type context: bpy.types.Context
        :type event: bpy.types.Event
        :rtype: set
        """
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        """
        :type context: bpy.types.Context
        :type event: bpy.types.Event
        :rtype: set
        """
        self.enter(context)
        return {'FINISHED'}

        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}


classes = [
    AddonPreferencesGroupEditor,
    EditInstance,
]


@AddonPreferencesGroupEditor.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.translations.register(__name__, translation_dict)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = AddonPreferencesGroupEditor.get_keymap('Mesh')
        # kmi = km.keymap_items.new('mesh.intersect_cutoff', 'B', 'PRESS',
        #                           shift=True, ctrl=True, alt=True, oskey=True)


@AddonPreferencesGroupEditor.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)


if __name__ == '__main__':
    register()
