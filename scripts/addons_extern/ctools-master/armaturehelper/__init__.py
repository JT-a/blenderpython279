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
    'name': 'Armature Helper',
    'author': 'chromoly',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'location': 'View3D',
    'description': '',
    'wiki_url': '',
    'category': 'Armature',
}


import importlib
import time

import bpy
from mathutils import Matrix

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import vaprops


translation_dict = {
    'ja_JP': {
        ('*', 'String'): '文字列',
    }
}


class ArmatureHelperPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        layout.separator()
        super().draw(context)


class SelectHierarchy:
    def select_hierarchy(self, context, direction, extend):
        """非表示のレイヤーにあるオブジェクトも選択対象。
        :type context: bpy.types.Context
        :type direction: str
        :type extend: bool
        :rtype: dict
        """
        scene = context.scene
        actob = context.active_object

        selected_objects = context.selected_objects
        if actob and not actob.select and actob.mode != 'OBJECT':
            selected_objects.append(actob)
        selected_objects.sort(key=lambda ob: ob.name)

        objects = []

        if direction == 'PARENT':
            for ob in selected_objects:
                parent = ob.parent
                if parent and not parent.hide:
                    if ob.parent_type == 'BONE':
                        if 'EDIT' in context.active_object.mode:
                            bpy.ops.object.mode_set(mode='EDIT', toggle=True)
                        if parent.mode != 'POSE':
                            scene.objects.active = parent
                            bpy.ops.object.mode_set(mode='POSE')
                        if not extend:
                            for pbone in parent.pose.bones:
                                bone = pbone.bone
                                bone.select = False
                            parent.data.bones.active = None
                        if ob.parent_bone in parent.data.bones:
                            bone = parent.data.bones[ob.parent_bone]
                            if not bone.hide:
                                bone.select = True
                                parent.data.bones.active = bone
                        objects.append(parent)
                    else:
                        objects.append(parent)

        else:
            if context.mode in {'POSE', 'EDIT_ARMATURE'}:
                if actob.mode == 'POSE':
                    bone_names = {b.name for b in context.selected_pose_bones}
                else:
                    bone_names = {b.name for b in
                                  context.selected_editable_bones}
                for ob in actob.children:
                    if not ob.hide and ob.parent_type == 'BONE':
                        if ob.parent_bone in bone_names:
                            objects.append(ob)
                if objects:
                    if not extend:
                        for bone in actob.data.bones:
                            bone.select = False
            else:
                for ob in actob.children:
                    if not ob.hide:
                        objects.append(ob)

        if objects:
            objects.sort(key=lambda ob: (ob.mode == 'POSE', ob.name))
            if not extend:
                for ob in scene.objects:
                    ob.select = False
            for ob in objects:
                ob.select = True
            if 'EDIT' in context.active_object.mode:
                bpy.ops.object.mode_set(mode='EDIT', toggle=True)
            scene.objects.active = objects[0]
            return {'FINISHED'}

        else:
            return {'CANCELLED'}


class OBJECT_OT_select_hierarchy_ex(SelectHierarchy, bpy.types.Operator):
    bl_rna_ = bpy.ops.object.select_hierarchy.get_rna().bl_rna
    props = bl_rna_.properties

    bl_idname = 'object.select_hierarchy_ex'
    bl_label = bl_rna_.name
    bl_description = bl_rna_.description
    bl_options = {'REGISTER', 'UNDO'}

    direction = vaprops.bl_prop_to_py_prop(props['direction'])
    extend = vaprops.bl_prop_to_py_prop(props['extend'])
    bone_hierarchy = bpy.props.BoolProperty(name='Bone Hierarchy')

    del bl_rna_
    del props

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if self.bone_hierarchy:
            return self.select_hierarchy(context, self.direction, self.extend)
        else:
            return bpy.ops.object.select_hierarchy(
                direction=self.direction, extend=self.extend)


class ARMATURE_OT_select_hierarchy_ex(SelectHierarchy, bpy.types.Operator):
    bl_rna_ = bpy.ops.armature.select_hierarchy.get_rna().bl_rna
    props = bl_rna_.properties

    bl_idname = 'armature.select_hierarchy_ex'
    bl_label = bl_rna_.name
    bl_description = bl_rna_.description
    bl_options = {'REGISTER', 'UNDO'}

    direction = vaprops.bl_prop_to_py_prop(props['direction'])
    extend = vaprops.bl_prop_to_py_prop(props['extend'])
    bone_hierarchy = bpy.props.BoolProperty(name='Bone Hierarchy')

    del bl_rna_
    del props

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if self.bone_hierarchy:
            self.select_hierarchy(context, self.direction, self.extend)
            return {'FINISHED'}
        else:
            return bpy.ops.armature.select_hierarchy(
                direction=self.direction, extend=self.extend)


class POSE_OT_select_hierarchy_ex(SelectHierarchy, bpy.types.Operator):
    bl_rna_ = bpy.ops.pose.select_hierarchy.get_rna().bl_rna
    props = bl_rna_.properties

    bl_idname = 'pose.select_hierarchy_ex'
    bl_label = bl_rna_.name
    bl_description = bl_rna_.description
    bl_options = {'REGISTER', 'UNDO'}

    direction = vaprops.bl_prop_to_py_prop(props['direction'])
    extend = vaprops.bl_prop_to_py_prop(props['extend'])
    bone_hierarchy = bpy.props.BoolProperty(
        name='Bone Hierarchy',
        default=True)
    del bl_rna_
    del props

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if self.bone_hierarchy:
            self.select_hierarchy(context, self.direction, self.extend)
            return {'FINISHED'}
        else:
            return bpy.ops.pose.select_hierarchy(
                direction=self.direction, extend=self.extend)


class ARMATURE_OT_hold_child_objects_update(bpy.types.Operator):
    bl_idname = 'armature.hold_child_objects_update'
    bl_label = 'Hold Child Objects'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        if context.mode == 'EDIT_ARMATURE':
            bpy.ops.object.mode_set(False, mode='EDIT', toggle=True)
            bpy.ops.object.mode_set(False, mode='EDIT', toggle=True)
        return {'FINISHED'}


class VIEW3D_PT_armature_hold_child_objects(bpy.types.Panel):
    # bl_idname = 'VIEW3D_PT_armature_helper'
    bl_label = 'Hold Bone Children'
    bl_description = 'Hold bone child objects'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_ARMATURE'

    def draw(self, context):
        layout = self.layout
        # layout.prop(context.scene,
        #             'edit_armature_hold_child_objects_constantly')
        layout.operator('armature.hold_child_objects_update',
                        text='Upddate')

    def draw_header(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, 'edit_armature_hold_child_objects',
                    text='')


data = {'mode': 'OBJECT',
        'objects': [],
        'name': '',
        }


def push(context, use_edit=True):
    arm_ob = context.active_object
    arm = arm_ob.data
    objects = {}
    for ob in arm_ob.children:
        if ob.parent_type == 'BONE' and ob.parent_bone in arm.edit_bones:
            if use_edit:
                bone = arm.edit_bones[ob.parent_bone]
                mat = bone.matrix.copy()
                length = (bone.tail - bone.head).length
            else:
                bone = arm.bones[ob.parent_bone]
                mat = bone.matrix_local.copy()
                length = (bone.tail_local - bone.head_local).length
            objects[ob.name] = [ob.matrix_parent_inverse.copy(),
                                mat, length]
    data['objects'] = objects


def pop():
    if data['name'] not in bpy.data.objects:
        return
    arm_ob = bpy.data.objects[data['name']]
    arm = arm_ob.data
    for ob in arm_ob.children:
        if (ob.name in data['objects'] and ob.parent_type == 'BONE' and
                ob.parent_bone in arm.bones):
            bone = arm.bones[ob.parent_bone]
            pimat, bmat, blength = data['objects'][ob.name]
            tmat = Matrix.Translation((0, blength, 0))
            m = bmat * tmat * pimat
            tmat = Matrix.Translation(
                (0, (bone.tail_local - bone.head_local).length, 0))
            mat = (bone.matrix_local * tmat).inverted() * m
            ob.matrix_parent_inverse = mat
            ob.update_tag()


@bpy.app.handlers.persistent
def scene_update_pre(scene):
    if not scene.edit_armature_hold_child_objects:
        return

    context = bpy.context
    if context.mode == 'EDIT_ARMATURE':
        # ↓名前変更の恐れがあるのでEDIT_ARMATURE中は常に実行する
        data['name'] = context.active_object.name
        if data['mode'] != 'EDIT_ARMATURE':
            push(context)
        # if scene.edit_armature_hold_child_objects_constantly:
        #     pop()
        #     context.active_object.update_from_editmode()

    elif data['mode'] == 'EDIT_ARMATURE' and data['objects']:
        pop()
        data['objects'] = []
        data['name'] = ''
    data['mode'] = context.mode


@bpy.app.handlers.persistent
def save_pre(scene):
    if not scene:
        return
    if not scene.edit_armature_hold_child_objects:
        return

    context = bpy.context
    if context.mode == 'EDIT_ARMATURE':
        if data['objects']:
            bpy.ops.object.mode_set(False, mode='EDIT', toggle=True)
            bpy.ops.object.mode_set(False, mode='EDIT', toggle=True)
            data['name'] = context.active_object.name
            pop()


classes = [
    ArmatureHelperPreferences,

    OBJECT_OT_select_hierarchy_ex,
    ARMATURE_OT_select_hierarchy_ex,
    POSE_OT_select_hierarchy_ex,

    ARMATURE_OT_hold_child_objects_update,
    VIEW3D_PT_armature_hold_child_objects,
]


@ArmatureHelperPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    def update(self, context):
        if self.edit_armature_hold_child_objects:
            if context.mode == 'EDIT_ARMATURE':
                push(context, use_edit=False)
        else:
            if context.mode == 'EDIT_ARMATURE':
                bpy.ops.object.mode_set(False, mode='EDIT', toggle=True)
                bpy.ops.object.mode_set(False, mode='EDIT', toggle=True)
                pop()
            data['objects'] = []

    bpy.types.Scene.edit_armature_hold_child_objects = \
        bpy.props.BoolProperty(
            name='Hold Bone Child Objects',
            description='Hold bone child objects',
            update=update
        )
    # bpy.types.Scene.edit_armature_hold_child_objects_constantly = \
    #     bpy.props.BoolProperty(
    #         name='Apply Constantly',
    #         description='Apply constantly with scene callback'
    #     )

    bpy.app.handlers.scene_update_pre.append(scene_update_pre)
    bpy.app.handlers.save_pre.append(save_pre)

    bpy.app.translations.register(__name__, translation_dict)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km_ob = ArmatureHelperPreferences.get_keymap('Object Mode')
        km_arm = ArmatureHelperPreferences.get_keymap('Armature')
        km_pose = ArmatureHelperPreferences.get_keymap('Pose')
        for i in range(4):
            if i < 2:
                args = ('LEFT_BRACKET', 'PRESS')
                direction = 'PARENT'
            else:
                args = ('RIGHT_BRACKET', 'PRESS')
                direction = 'CHILD'
            if i in (0, 2):
                kwargs = {'ctrl': True}
            else:
                kwargs = {'shift': True, 'ctrl': True}
            for km, t in ((km_ob, OBJECT_OT_select_hierarchy_ex),
                          (km_arm, ARMATURE_OT_select_hierarchy_ex),
                          (km_pose, POSE_OT_select_hierarchy_ex)):
                kmi = km.keymap_items.new(t.bl_idname,
                                          *args, **kwargs)
                kmi.properties.direction = direction
                kmi.properties.extend = False
                kmi.properties.bone_hierarchy = True


@ArmatureHelperPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.edit_armature_hold_child_objects

    # if scene_update_pre in bpy.app.handlers.scene_update_pre:
    bpy.app.handlers.scene_update_pre.remove(scene_update_pre)
    # if save_pre in bpy.app.handlers.save_pre:
    bpy.app.handlers.save_pre.remove(save_pre)

    bpy.app.translations.unregister(__name__)


if __name__ == '__main__':
    register()
