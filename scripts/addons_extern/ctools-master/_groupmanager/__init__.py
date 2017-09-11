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
    'name': 'Group Manager',
    'author': 'chromoly',
    'version': (0, 1, 2),
    'blender': (2, 78, 0),
    'location': 'Properties -> Scene, Properties -> Object',
    'category': 'Object'}


import bpy

from ..utils import addongroup


_enum_items_cache = {}


def get_groups(context, list_type):
    seq = []
    # layerとvisibleが重い
    if list_type == 'all':
        seq = bpy.data.groups
    elif list_type == 'scene':
        for group in bpy.data.groups:
            for ob in group.objects:
                if ob.name in context.scene.objects:
                    seq.append(group)
                    break
    elif list_type == 'layer':
        seq = set()
        for ob in context.scene.objects:
            for i in range(20):
                if context.scene.layers[i] and ob.layers[i]:
                    for group in ob.users_group:
                        seq.add(group)
    elif list_type == 'visible':
        seq = set()
        for ob in context.visible_objects:
            for group in ob.users_group:
                seq.add(group)
    elif list_type == 'selected':
        seq = set()
        for ob in context.selected_objects:
            for group in ob.users_group:
                seq.add(group)
    elif list_type == 'active_object':
        actob = bpy.context.scene.objects.active
        if actob:  # and actob.select:
            seq = actob.users_group
    if seq:
        seq = sorted(seq, key=lambda gr: gr.name)
    return seq


def make_group_enum_items(context, groups, tag=False):
    if tag:
        actob = context.active_object
        selobs = context.selected_objects
        items = []
        for i, group in enumerate(groups):
            t = ''
            name = group.name
            obs = [ob for ob in group.objects if ob in selobs]
            if not obs:
                t = ''
            elif len(obs) == 1 and obs[0] == actob:
                t = '  <*Act>'
            elif actob in obs:
                t = '  <*Sel> <*Act>'
            else:
                t = '  <*Sel>'
            name += t
            items.append((group.name, name, '', 'NONE', i))
    else:
        items = [(gr.name, gr.name, '', 'NONE', i)
                 for i, gr in enumerate(groups)]
    return tuple(items)


###############################################################################
# Operator
###############################################################################
class OperatorGroup:
    bl_property = 'group'  # この属性は継承するクラス毎に定義しないといけない

    def get_groups(self, context):
        return []

    def group_enum_items(self, context):
        class_name = self.rna_type.identifier
        items = _enum_items_cache.setdefault(class_name, [])
        cls = getattr(bpy.types, class_name).bl_rna.__class__
        groups = cls.get_groups(self, context)
        items[:] = make_group_enum_items(context, groups)
        return items

    group = bpy.props.EnumProperty(
        name='Group',
        items=group_enum_items,
        options={'SKIP_SAVE'})


class OperatorGroupFilter:
    bl_property = 'group'  # この属性は継承するクラス毎に定義しないといけない

    group_filter = bpy.props.EnumProperty(
        name='Group Filter',
        items=(('all', 'All', 'All objects'),
               ('layer', 'Layer', 'Objects in visible layers'),
               ('visible', 'Visible', 'Visible objects'),
               ('selected', 'Selected', 'Selected objects'),
               ('active_object', 'Active', 'Active object')),
        default='all')

    def group_enum_items(self, context):
        class_name = self.rna_type.identifier
        items = _enum_items_cache.setdefault(class_name, [])
        groups = get_groups(context, self.group_filter)
        items[:] = make_group_enum_items(context, groups)
        return items

    group = bpy.props.EnumProperty(
        name='Group',
        items=group_enum_items,
        options={'SKIP_SAVE'})


class GROUP_OT_objects_link(OperatorGroupFilter, bpy.types.Operator):
    """選択オブジェクトをGroupに追加する。
    groupを指定しなければSearchPopupを呼び出す。
    """
    bl_description = 'Add the objects to an object group'
    bl_idname = 'group.objects_link'
    bl_label = 'Add Selected To Group'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    unlink_others = bpy.props.BoolProperty(
        name='Unlink Other Groups',
        default=False)

    def execute(self, context):
        if self.group not in bpy.data.groups:
            return {'CANCELLED'}
        group = bpy.data.groups[self.group]
        for ob in context.selected_objects:
            if ob.name not in group.objects:
                group.objects.link(ob)
            if self.unlink_others:
                for gr in (gr for gr in ob.users_group if gr != group):
                    gr.objects.unlink(ob)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if self.properties.is_property_set('group'):
            return self.execute(context)
        else:
            context.window_manager.invoke_search_popup(self)
            return {'CANCELLED'}  # 若しくは{'RUNNING_MODAL'}


class GROUP_OT_object_link(OperatorGroupFilter, bpy.types.Operator):
    """Context.objectをGroupに追加する。
    groupを指定しなければSearchPopupを呼び出す。
    GROUP_OT_objects_linkの単一オブジェクト動作版。
    """
    bl_description = 'Add the object to an object group'
    bl_idname = 'group.object_link'
    bl_label = 'Add Object To Group'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    unlink_others = bpy.props.BoolProperty(
        name='Unlink Other Groups',
        default=False)

    def execute(self, context):
        if self.group not in bpy.data.groups:
            return {'CANCELLED'}
        group = bpy.data.groups[self.group]
        ob = context.object
        if ob.name not in group.objects:
            group.objects.link(ob)
        if self.unlink_others:
            for gr in (gr for gr in ob.users_group if gr != group):
                gr.objects.unlink(ob)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if self.properties.is_property_set('group'):
            return self.execute(context)
        else:
            context.window_manager.invoke_search_popup(self)
            return {'CANCELLED'}  # or {'RUNNING_MODAL'}


class GROUP_OT_objects_unlink(OperatorGroupFilter, bpy.types.Operator):
    """選択オブジェクトをGroupから除去する。
    groupを指定しなければSearchPopupを呼び出す。
    """
    bl_description = 'Unlink selected objects. ' + \
                     'Shift + Click to unlink all objects in this group'
    bl_idname = 'group.objects_unlink'
    bl_label = 'Objects Unlink'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    unlink_type = bpy.props.EnumProperty(
        name='Unlink Type',
        items=(('all', 'All', ''),
               ('selected', 'Selected', '')),
        default='selected')

    def execute(self, context):
        if self.group not in bpy.data.groups:
            return {'CANCELLED'}
        group = bpy.data.groups[self.group]
        if self.unlink_type == 'all':
            for ob in group.objects[:]:
                group.objects.unlink(ob)
        else:
            for ob in context.selected_objects:
                if ob.name in group.objects:
                    group.objects.unlink(ob)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.properties.is_property_set('unlink_type'):
            self.unlink_type = 'all' if event.shift else 'selected'
        if self.properties.is_property_set('group'):
            return self.execute(context)
        else:
            context.window_manager.invoke_search_popup(self)
            return {'CANCELLED'}  # or {'RUNNING_MODAL'}


class GROUP_OT_object_unlink(OperatorGroupFilter, bpy.types.Operator):
    """Context.objectをGroupから除去する。active_objectではない点に注意。
    groupを指定しなければSearchPopupを呼び出す。
    GROUP_OT_objects_unlinkの単一オブジェクト動作版。
    """
    bl_description = 'Unlink Context.object. ' + \
                     'Shift + Click to unlink all objects in this group'
    bl_idname = 'group.object_unlink'
    bl_label = 'Object Unlink'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    def execute(self, context):
        if self.group not in bpy.data.groups:
            return {'CANCELLED'}
        group = bpy.data.groups[self.group]
        ob = context.object
        if ob.name in group.objects:
            group.objects.unlink(ob)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if self.properties.is_property_set('group'):
            return self.execute(context)
        else:
            context.window_manager.invoke_search_popup(self)
            return {'CANCELLED'}  # or {'RUNNING_MODAL'}


class GROUP_OT_objects_select(OperatorGroupFilter, bpy.types.Operator):
    bl_description = 'Groupに含まれるObjectを全て選択する'
    bl_idname = 'group.objects_select'
    bl_label = 'Select Objects'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    all = bpy.props.BoolProperty(
        name='All',
        description='search_typeに含まれる全Groupを対象にする。'
                    'この際group属性は無視する')
    deselect = bpy.props.BoolProperty(
        name='Deselect',
        default=False)

    def execute(self, context):
        scn = context.scene
        gm = scn.group_manager
        if self.all:
            groups = get_groups(context, self.group_filter)
        else:
            name = self.group
            if name and name in bpy.data.groups:
                groups = [bpy.data.groups[name]]
            else:
                return {'CANCELLED'}
        for group in groups:
            for ob in group.objects:
                if ob.name in scn.objects:
                    if not gm.select_is_visible or ob.is_visible(scn):
                        if self.deselect:
                            ob.select = False
                        else:
                            ob.select = True
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if self.properties.is_property_set('group') or self.all:
            return self.execute(context)
        else:
            context.window_manager.invoke_search_popup(self)
            return {'CANCELLED'}  # or {'RUNNING_MODAL'}


class GROUP_OT_objects_sync_active(OperatorGroup, bpy.types.Operator):
    bl_description = 'Sync Selected To Active Group ' \
                     '(Shift + Click to call search popup)'
    bl_idname = 'group.objects_sync_active'
    bl_label = 'Sync Selected To Active Group'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    mode = bpy.props.EnumProperty(
        name='Mode',
        items=(('sync', 'Sync', ''),
               ('add', 'Add', ''),
               ('remove', 'Remove', '')),
        default='sync')

    def get_groups(self, context):
        return get_groups(context, 'active_object')

    all = bpy.props.BoolProperty(
        name='All Groups',
        description='active_object.users_groups',
        default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        actob = context.active_object
        actob_groups = [gr for gr in actob.users_group]
        for ob in context.selected_objects:
            if self.all:
                if self.mode == 'remove':
                    for group in actob_groups:
                        if group in ob.users_group:
                            group.objects.unlink(ob)
                elif self.mode == 'sync':
                    for group in ob.users_group:
                        if group not in actob.users_group:
                            group.objects.unlink(ob)
                if self.mode != 'remove':
                    for group in actob.users_group:
                        if group not in ob.users_group:
                            group.objects.link(ob)
            elif self.group:
                group = bpy.data.groups[self.group]
                if self.mode == 'remove':
                    if group in ob.users_group:
                        group.objects.unlink(ob)
                elif self.mode == 'add':
                    if group not in ob.users_group:
                        group.objects.link(ob)
                else:
                    for gr in ob.users_group:
                        if gr != group:
                            gr.objects.unlink(ob)
                    if group not in ob.users_group:
                        group.objects.link(ob)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if ((self.properties.is_property_set('group') or self.all) and
                not event.shift):
            return self.execute(context)
        else:
            self.all = False
            context.window_manager.invoke_search_popup(self)
            return {'CANCELLED'}  # or {'RUNNING_MODAL'}


class GROUP_OT_objects_restrict(OperatorGroup, bpy.types.Operator):
    bl_description = 'Restrict group objects'  # . (Shift + Click: Disable)'
    bl_idname = 'group.objects_restrict'
    bl_label = 'Select Objects'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    def get_groups(self, context):
        return get_groups(context, 'all')

    mode = bpy.props.EnumProperty(
        name='Mode',
        items=(('view', 'Visibility', ''),
               ('select', 'Selection', ''),
               ('render', 'Renderability', '')),
        default='view')
    toggle = bpy.props.BoolProperty(
        name='Toggle',
        default=False)
    enable = bpy.props.BoolProperty(
        name='Enable',
        default=True)

    def execute(self, context):
        name = self.group
        if not name or name not in bpy.data.groups:
            return {'CANCELLED'}
        group = bpy.data.groups[name]
        if self.toggle:
            if self.mode == 'view':
                attr = 'hide'
            elif self.mode == 'select':
                attr = 'hide_select'
            elif self.mode == 'render':
                attr = 'hide_render'
            s = {getattr(ob, attr) for ob in group.objects}
            flag = False if s == {True} else True
            for ob in group.objects:
                setattr(ob, attr, flag)
        else:
            enable = self.enable
            for ob in group.objects:
                if self.mode == 'view':
                    ob.hide = False if enable else True
                elif self.mode == 'select':
                    ob.hide_select = False if enable else True
                elif self.mode == 'render':
                    ob.hide_render = False if enable else True
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.toggle:
            self.enable = not event.shift
        return self.execute(context)


class GROUP_OT_delete(OperatorGroup, bpy.types.Operator):
    bl_description = 'Delete group'
    bl_idname = 'group.delete'
    bl_label = 'Delete Gruop'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    def get_groups(self, context):
        return get_groups(context, 'all')

    def execute(self, context):
        if not self.group or self.group not in bpy.data.groups:
            return {'CANCELLED'}
        group = bpy.data.groups[self.group]
        group.user_clear()
        bpy.data.groups.remove(group)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if self.properties.is_property_set('group'):
            return self.execute(context)
        else:
            context.window_manager.invoke_search_popup(self)
            return {'CANCELLED'}  # or {'RUNNING_MODAL'}


class GROUP_OT_layer(OperatorGroup, bpy.types.Operator):
    bl_description = 'Change Layer. Shift:Extend'
    bl_idname = 'group.layer'
    bl_label = 'Gruop Layer'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'group'

    def get_groups(self, context):
        return get_groups(context, 'all')

    layers = bpy.props.BoolVectorProperty(
        name='Layers',
        subtype='LAYER',
        size=20)
    mode = bpy.props.EnumProperty(
        name='Mode',
        items=(('show', 'Show', ''),
               ('move', 'Move', '')),
        default='show')
    extend = bpy.props.BoolProperty(
        name='Extend',
        description='Shift',
        default=False)

    def execute(self, context):
        if not self.group or self.group not in bpy.data.groups:
            return {'CANCELLED'}
        group = bpy.data.groups[self.group]
        scn = context.scene
        gm = scn.group_manager
        if self.mode == 'show':
            scn.layers = self.layers
        elif self.mode == 'move':
            for ob in group.objects:
                if ob.name in scn.objects:
                    if not gm.select_is_visible or ob.is_visible(scn):
                        ob.layers = self.layers
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.group or self.group not in bpy.data.groups:
            return {'CANCELLED'}
        scn = context.scene
        group = bpy.data.groups[self.group]
        if self.mode == 'show' and event.shift or self.mode == 'move':
            self.extend = True
        if self.extend:
            layers = list(scn.layers)
        else:
            layers = [False for i in range(20)]
        for ob in (ob for ob in group.objects if ob.name in scn.objects):
            for i, b in enumerate(ob.layers):
                layers[i] |= b
        self.layers = layers
        if self.mode == 'show':
            self.extend = event.shift
            return self.execute(context)
        else:

            return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        if self.mode == 'move':
            split = layout.row().split(0.3)
            col = split.column()
            col.label('Layer')
            col = split.column()
            col.prop(self, 'layers', text='')


### Operator - Name ###########################################################
class GM_OT_group_action(bpy.types.Operator):
    """
    グループ毎にパネルを描画する場合、
    layout.context_pointer_set('group', group)を実行しておくこと
    """
    bl_description = 'SelectGroup.' + \
                     ' Shift:ToggleSelect, Ctrl:Rename, Alt:Deselect,' + \
                     ' Shift+Ctrl:Menu'
    bl_idname = 'gm.group_action'
    bl_label = 'GroupAction'
    bl_options = {'REGISTER', 'UNDO'}

    rename = bpy.props.BoolProperty(
        name='Rename',
        default=False)
    name = bpy.props.StringProperty(
        name='Name')

    def execute(self, context):
        if self.rename:
            bpy.data.groups[self.name_bak].name = self.name
        return {'FINISHED'}

    def invoke(self, context, event):
        scn = context.scene
        gm = scn.group_manager
        group = context.group
        if group:
            if event.shift and event.ctrl:
                gm.active_group = group.name
                bpy.ops.wm.call_menu(name='GM_MT_group_operation')
            elif event.shift:  # Toggle Select
                for ob in group.objects:
                    if ob.name in scn.objects:
                        if not gm.select_is_visible or ob.is_visible(scn):
                            ob.select = not ob.select
            elif event.ctrl:  # Rename
                self.rename = True
                self.name = self.name_bak = group.name
                return context.window_manager.invoke_props_popup(self, event)
            elif event.alt:  # Deselect
                for ob in group.objects:
                    if ob.name in scn.objects:
                        if not gm.select_is_visible or ob.is_visible(scn):
                            ob.select = False
            else:  # Select
                actob = scn.objects.active
                if actob and actob.name in scn.objects:
                    if actob.name not in group.objects:
                        if not gm.select_is_visible or actob.is_visible(scn):
                            if 'EDIT' in context.mode:
                                bpy.ops.object.mode_set(mode='OBJECT')
                for ob in scn.objects:
                    if not gm.select_is_visible or ob.is_visible(scn):
                        ob.select = False
                for ob in group.objects:
                    if ob.name in scn.objects:
                        if not gm.select_is_visible or ob.is_visible(scn):
                            ob.select = True
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        if self.rename:
            layout.prop(self, 'name', text='Name')


class GM_OT_object_action(bpy.types.Operator):
    """
    オブジェクト毎にパネルを描画する場合、
    layout.context_pointer_set('object', ob)を実行しておくこと
    """
    bl_description = 'SelectObject.' + \
                     ' Shift:ToggleSelect, Ctrl:Rename, Alt:Deselect' + \
                     ' Shift+Ctrl:Menu'
    bl_idname = 'gm.object_action'
    bl_label = 'ObjectAction'
    bl_options = {'REGISTER', 'UNDO'}

    rename = bpy.props.BoolProperty(
        name='Rename',
        default=False)
    name = bpy.props.StringProperty(
        name='Name')

    def execute(self, context):
        if self.rename:
            bpy.data.objects[self.name_bak].name = self.name
        return {'FINISHED'}

    def invoke(self, context, event):
        scn = context.scene
        gm = scn.group_manager
        group = context.group
        object = context.object
        if object:
            if event.shift and event.ctrl:
                gm.active_group = group.name
                gm.active_object = object.name
                bpy.ops.wm.call_menu(name='GM_MT_object_operation')
            elif event.shift:  # Toggle Select
                if object.name in scn.objects:
                    object.select = not object.select
            elif event.ctrl:  # Rename
                self.rename = True
                self.name = self.name_bak = object.name
                return context.window_manager.invoke_props_popup(self, event)
            elif event.alt:  # Deselect
                if object.name in scn.objects:
                    object.select = False
            else:  # Select
                if object.name in scn.objects:
                    if scn.objects.active != object:
                        if 'EDIT' in context.mode:
                            bpy.ops.object.mode_set(mode='OBJECT')
                    for ob in scn.objects:
                        ob.select = False
                    object.select = True
                    scn.objects.active = object
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        if self.rename:
            layout.prop(self, 'name', text='Name')


### 追加分 ####################################################################
class GM_OT_link_group_objects_to_scene(bpy.types.Operator):
    """GM_MT_group_operationで使う"""
    bl_description = 'groupに所属するobjectをsceneにリンクする'
    bl_idname = 'gm.link_group_objects_to_scene'
    bl_label = 'Link Group Objects to Scene'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in context.group.objects:
            if ob.name not in context.scene.objects:
                context.scene.objects.link(ob)
        return {'FINISHED'}


class GM_OT_unlink_group_objects_to_scene(bpy.types.Operator):
    """GM_MT_group_operationで使う"""
    bl_description = 'groupに所属するobjectのsceneからのリンクを外す'
    bl_idname = 'gm.unlink_group_objects_to_scene'
    bl_label = 'Unlink Group Objects to Scene'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in context.group.objects:
            if ob.name in context.scene.objects:
                context.scene.objects.unlink(ob)
        return {'FINISHED'}


class GM_OT_call_GM_MT_group_operation(bpy.types.Operator):
    """GM_MT_group_operationを呼ぶ"""
    bl_description = 'GM_MT_group_operationを呼ぶ'
    bl_idname = 'gm.call_gm_mt_group_operation'
    bl_label = 'Call GM_MT_group_operation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        gm = context.scene.group_manager
        gm.active_group = context.group.name
        if context.object:
            gm.active_object = context.object.name
        else:
            gm.active_object = ''
        bpy.ops.wm.call_menu(name='GM_MT_group_operation')
        return {'FINISHED'}


### Menu ######################################################################

class GM_MT_group_operation(bpy.types.Menu):
    bl_label = 'Group Operation'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        gm = context.scene.group_manager
        group = bpy.data.groups[gm.active_group]

        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'  # call invoke
        layout.context_pointer_set('group', group)

        ## Link
        op = layout.operator('gm.link_group_objects_to_scene')
        op = layout.operator('gm.unlink_group_objects_to_scene')
        ## Delete
        op = layout.operator('group.delete', text='Delete Group', icon='X')
        op.group = group.name
        ## Action [Add, Rem, Layer, Move]
        op = layout.operator('group.objects_link', text='Add Selected Objects')
        op.group = group.name
        op = layout.operator('group.objects_unlink',
                             text='Remove Selected Objects')
        op.group = group.name
        op = layout.operator('group.layer', text='Show Object Layers')
        op.group = group.name
        op = layout.operator('group.layer', text='Objects Move to Layer...')
        op.group = group.name
        op.mode = 'move'


class GM_MT_object_operation(bpy.types.Menu):
    bl_label = 'Object Operation'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        gm = context.scene.group_manager
        group = bpy.data.groups[gm.active_group]
        ob = bpy.data.objects[gm.active_object]

        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'  # call invoke
        layout.context_pointer_set('group', group)
        layout.context_pointer_set('object', ob)

        op = layout.operator('wm.exec_string', text='Link Scene',
                             icon='SCENE_DATA')
        l = ['ob = context.object',
             'if ob.name not in context.scene.objects:',
             '  context.scene.objects.link(context.object)']
        op.string = '\n'.join(l)
        op = layout.operator('wm.exec_string', text='Unlink Scene',
                             icon='SCENE_DATA')
        l = ['ob = context.object',
             'if ob.name in context.scene.objects:',
             '  context.scene.objects.unlink(context.object)']
        op.string = '\n'.join(l)

        col = layout.column()
        col.context_pointer_set('object', ob)
        op = col.operator('group.object_unlink', text='Unlink Group',
                          icon='GROUP')
        op.group = group.name

        op = layout.operator('wm.context_set_boolean', text='Select')
        op.data_path = 'object.select'
        op.value = True
        op = layout.operator('wm.context_set_boolean', text='Deselect')
        op.data_path = 'object.select'
        op.value = False

        icon = 'RESTRICT_VIEW_ON' if ob.hide else 'RESTRICT_VIEW_OFF'
        op = layout.operator('wm.context_toggle', text='Toggle Visible',
                             icon=icon)
        op.data_path = 'object.hide'
        icon = 'RESTRICT_SELECT_ON' if ob.hide_select else 'RESTRICT_SELECT_OFF'
        op = layout.operator('wm.context_toggle', text='Toggle Selectable',
                             icon=icon)
        op.data_path = 'object.hide_select'
        icon = 'RESTRICT_RENDER_ON' if ob.hide_render else 'RESTRICT_RENDER_OFF'
        op = layout.operator('wm.context_toggle', text='Toggle Renderable',
                             icon=icon)
        op.data_path = 'object.hide_render'


### Panel #####################################################################
def draw_open_group_options(context, groups, layout):
    flags = set((group.manager.show_options for group in groups))
    if not flags:
        open_flag = 0
    else:
        open_flag = 1 + int(True in flags) - int(False in flags)
    icon = ('RIGHTARROW', 'TRIA_DOWN', 'DOWNARROW_HLT')[open_flag]
    op = layout.operator('wm.exec_string', text='', icon=icon)
    l = ['groups = ' + str([gr.name for gr in groups]),
         'value = ' + ('False' if open_flag == 2 else 'True'),
         'for name in groups:',
         '  group = bpy.data.groups[name]',
         '  group.manager.show_options = value']
    op.string = '\n'.join(l)


def draw_group_options(context, group, layout):
    if not group.manager.show_options:
        return
    scn = context.scene

    box = layout.box()
    split = box.split()

    col = split.column()
    ## Dupli Layers
    col.prop(group, "layers", text="Dupli")
    ## ColorWire
    # row = col.row()
    # row.prop(ggm, 'use_color_wire', text='')
    # row.prop(ggm, 'wire_color', text='')
    # op = col.operator('group.set_wire_color', text='Set Color')
    # op.group = group.name

    col = split.column()
    ## Dupli Offset
    col.prop(group, "dupli_offset", text="")
    ## Set Dupli Offset
    op = col.operator('wm.exec_string', text='From Cursor')
    txt = 'bpy.data.groups["{0}"].dupli_offset = {1}'
    op.string = txt.format(group.name, str(tuple(scn.cursor_location)))


class OBJECT_PT_group_manager(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_label = 'Group Manager'

    def draw(self, context):
        layout = self.layout

        # ob = context.object
        ob = bpy.context.scene.objects.active
        layout.context_pointer_set('object', ob)
        layout.context_pointer_set('active_object', ob)

        groups = get_groups(context, 'active_object')

        ### Top Buttons
        row = layout.row(align=True)
        draw_open_group_options(context, groups, row)
        row.operator("object.group_link", text="Add to Group")
        row.operator("object.group_add", text="", icon='ZOOMIN')

        # XXX, this is bad practice, yes, I wrote it :( - campbell
        value = str(tuple(context.scene.cursor_location))
        for i, group in enumerate(groups):
            ggm = group.manager
            col = layout.column(align=True)

            col.context_pointer_set("group", group)

            row = col.box().row()
            icon = 'DOWNARROW_HLT' if ggm.show_options else 'RIGHTARROW'
            row.prop(ggm, 'show_options', text='', icon=icon)

            row.prop(group, "name", text="")
            row.operator("object.group_remove", text="", icon='X',
                         emboss=False)

            draw_group_options(context, group, col)


TEST_UIList = False

if TEST_UIList:
    class GM_UL_group_objects(bpy.types.UIList):
        def draw_group_objects_restrict(self, context, ob, layout):
            if context.scene.group_manager.show_restrict:
                ## View
                icon = 'RESTRICT_VIEW_ON' if ob.hide else 'RESTRICT_VIEW_OFF'
                op = layout.operator('wm.context_toggle', text='', icon=icon,
                                     emboss=False)
                op.data_path = 'object.hide'
                ## Select
                if ob.hide_select:
                    icon = 'RESTRICT_SELECT_ON'
                else:
                    icon = 'RESTRICT_SELECT_OFF'
                op = layout.operator('wm.context_toggle', text='', icon=icon,
                                     emboss=False)
                op.data_path = 'object.hide_select'
                ## Render
                if ob.hide_render:
                    icon = 'RESTRICT_RENDER_ON'
                else:
                    icon = 'RESTRICT_RENDER_OFF'
                op = layout.operator('wm.context_toggle', text='', icon=icon,
                                     emboss=False)
                op.data_path = 'object.hide_render'

        def draw_item(self, context, layout, data, item, icon, active_data,
                      active_propname):
            group = data
            ob = item
            scn = context.scene

            # row.context_pointer_set('group', group)
            row = layout.row(align=True)
            row.context_pointer_set('object', ob)

            # Menu
            op = row.operator('wm.exec_string', text='', icon='MENU_PANEL')
            l = ['gm = context.scene.group_manager',
                 'gm.active_group = context.group.name',
                 'gm.active_object = context.object.name',
                 'bpy.ops.wm.call_menu(name="GM_MT_object_operation")']
            op.string = '\n'.join(l)

            sub = row.column()  # 非アクティブ表示にするため
            sub.active = ob.name in scn.objects
            if ob.select:
                icon = 'CHECKBOX_HLT'  # 'RADIOBUT_ON'
            else:
                icon = 'CHECKBOX_DEHLT'  # 'RADIOBUT_OFF'
            sub.operator('gm.object_action', text=ob.name, icon=icon)

            sub = row.column()
            sub.context_pointer_set('object', ob)
            op = sub.operator('group.object_unlink', text='', icon='X')
            op.group = group.name

            self.draw_group_objects_restrict(context, ob, row)


class SCENE_PT_group_manager(bpy.types.Panel):
    bl_idname = 'SCENE_PT_group_manager'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_label = 'Group Manager'

    # bl_options = {'DEFAULT_CLOSED'}

    def draw_group_objects_restrict(self, context, ob, layout):
        if context.scene.group_manager.show_restrict:
            ## View
            icon = 'RESTRICT_VIEW_ON' if ob.hide else 'RESTRICT_VIEW_OFF'
            op = layout.operator('wm.context_toggle', text='', icon=icon,
                                 emboss=False)
            op.data_path = 'object.hide'
            ## Select
            if ob.hide_select:
                icon = 'RESTRICT_SELECT_ON'
            else:
                icon = 'RESTRICT_SELECT_OFF'
            op = layout.operator('wm.context_toggle', text='', icon=icon,
                                 emboss=False)
            op.data_path = 'object.hide_select'
            ## Render
            if ob.hide_render:
                icon = 'RESTRICT_RENDER_ON'
            else:
                icon = 'RESTRICT_RENDER_OFF'
            op = layout.operator('wm.context_toggle', text='', icon=icon,
                                 emboss=False)
            op.data_path = 'object.hide_render'

    def draw_group_objects(self, context, group, layout):
        if not group.manager.show_objects:
            return
        scn = context.scene
        gm = scn.group_manager

        if TEST_UIList:
            layout.template_list(
                'GM_UL_group_objects', group.name, group, 'objects', group,
                'active_object_index', rows=1, maxrows=10)
            return

        box = layout.box()
        # col = box.column(align=True)
        split = box.split(0.05)
        split.column()
        col = split.column(align=True)
        for ob in group.objects:
            row = col.row(align=True)
            # row.context_pointer_set('group', group)
            row.context_pointer_set('object', ob)

            # Menu
            op = row.operator('wm.exec_string', text='', icon='MENU_PANEL')
            l = ['gm = context.scene.group_manager',
                 'gm.active_group = context.group.name',
                 'gm.active_object = context.object.name',
                 'bpy.ops.wm.call_menu(name="GM_MT_object_operation")']
            op.string = '\n'.join(l)

            sub = row.column()  # 非アクティブ表示にするため
            sub.active = ob.name in scn.objects
            if ob.select:
                icon = 'CHECKBOX_HLT'  # 'RADIOBUT_ON'
            else:
                icon = 'CHECKBOX_DEHLT'  # 'RADIOBUT_OFF'
            sub.operator('gm.object_action', text=ob.name, icon=icon)

            sub = row.column()
            sub.context_pointer_set('object', ob)
            op = sub.operator('group.object_unlink', text='', icon='X')
            op.group = group.name

            self.draw_group_objects_restrict(context, ob, row)

    def draw_group_actions(self, context, group, layout):
        ## Action [Add, Rem, Layer, Move]
        gm = context.scene.group_manager
        if gm.show_group_ops or group.manager.show_objects:
            row = layout.row(align=True)
            op = row.operator('group.objects_link', text='Add')
            op.group = group.name
            op = row.operator('group.objects_unlink', text='Rem')
            op.group = group.name
            op = row.operator('group.layer', text='Layer')
            op.group = group.name
            op = row.operator('group.layer', text='Move')
            op.group = group.name
            op.mode = 'move'

    def draw_groups_restrict(self, context, group, layout):
        gm = context.scene.group_manager
        if not gm.show_restrict:
            return
        # View
        if {ob.hide for ob in group.objects} == {True}:
            icon = 'RESTRICT_VIEW_ON'
        else:
            icon = 'RESTRICT_VIEW_OFF'
        op = layout.operator('group.objects_restrict', text='', icon=icon)
        op.group = group.name
        op.mode = 'view'
        op.toggle = True
        # Select
        if {ob.hide_select for ob in group.objects} == {True}:
            icon = 'RESTRICT_SELECT_ON'
        else:
            icon = 'RESTRICT_SELECT_OFF'
        op = layout.operator('group.objects_restrict', text='', icon=icon)
        op.group = group.name
        op.mode = 'select'
        op.toggle = True
        # Render
        if {ob.hide_render for ob in group.objects} == {True}:
            icon = 'RESTRICT_RENDER_ON'
        else:
            icon = 'RESTRICT_RENDER_OFF'
        op = layout.operator('group.objects_restrict', text='', icon=icon)
        op.group = group.name
        op.mode = 'render'
        op.toggle = True

    def draw_group(self, context, layout, group):
        scn = context.scene
        gm = scn.group_manager

        ggm = group.manager

        gcol = layout.column(align=True)
        column = gcol.box().column()
        column.context_pointer_set('group', group)
        row = column.row(align=True)

        ## Menu
        op = row.operator('gm.call_gm_mt_group_operation', text='',
                          icon='MENU_PANEL')

        ## Options, Objects, Name
        icon = 'TRIA_DOWN' if ggm.show_options else 'TRIA_RIGHT'
        row.prop(ggm, 'show_options', text='', icon=icon)  # 'GROUP'
        row.prop(ggm, 'show_objects', text='', icon='OBJECT_DATA')
        op = row.operator('gm.group_action', text=group.name)
        ## Restrict
        self.draw_groups_restrict(context, group, row)
        ## Action
        self.draw_group_actions(context, group, column)
        ## Options
        draw_group_options(context, group, gcol)
        ## Objects
        self.draw_group_objects(context, group, gcol)

    def draw_list_type(self, context, layout):
        gm = context.scene.group_manager

        split = layout.row().split(0.25)
        row = split.row(align=True)
        row.prop(context.scene.group_manager, 'show_groups', text='List')

        row = split.row(align=True)
        row.active = gm.show_groups
        if gm.show_groups:
            # 軽量化の為。(SOM等の多量のobjectがある場合、特定の条件下で重くなる)
            groups = get_groups(context, gm.list_type)
        else:
            groups = []

        ## Show Group Ops
        sub = row.column()
        # if gm.show_group_ops:
        #     icon = 'TRIA_DOWN'
        # else:
        #     icon = 'TRIA_RIGHT'
        sub.prop(gm, 'show_group_ops', text='', icon='BUTS')  # 'HAND'

        ## Show Options
        sub = row.column()
        flags = set((group.manager.show_options for group in groups))
        if not flags:
            open_flag = 0
        else:
            open_flag = 1 + int(True in flags) - int(False in flags)
        # icon = 'TRIA_RIGHT' if open_flag == 0 else 'TRIA_DOWN'
        op = sub.operator('wm.exec_string', text='',
                          icon='DOWNARROW_HLT')  # 'GROUP'
        l = ['groups = ' + str([gr.name for gr in groups]),
             'value = ' + ('False' if open_flag == 2 else 'True'),
             'if event.shift: value = False',
             'for name in groups:',
             '  group = bpy.data.groups[name]',
             '  group.manager.show_options = value']
        op.string = '\n'.join(l)

        ## Show Objects
        sub = row.column()
        flags = set((group.manager.show_objects for group in groups))
        if not flags:
            open_flag = 0
        else:
            open_flag = 1 + int(True in flags) - int(False in flags)
        op = sub.operator('wm.exec_string', text='', icon='OBJECT_DATA')
        l = ['groups = ' + str([gr.name for gr in groups]),
             'value = ' + ('False' if open_flag == 2 else 'True'),
             'if event.shift: value = False',
             'for name in groups:',
             '  group = bpy.data.groups[name]',
             '  group.manager.show_objects = value']
        op.string = '\n'.join(l)

        row.prop(context.scene.group_manager, 'list_type', text='')
        row.prop(context.scene.group_manager, 'show_restrict', text='',
                 icon='RESTRICT_RENDER_OFF')
        return groups

    def draw_actob_actions(self, context, layout):
        """ActOb Actions"""
        col = layout.column(align=True)
        # Top
        row = col.row(align=True)
        op = row.operator('group.objects_sync_active', text='Add Act')
        op.mode = 'add'
        op.all = True
        op = row.operator('group.objects_sync_active', text='Rem Act')
        op.mode = 'remove'
        op.all = True
        op = row.operator('group.objects_sync_active', text='Sync Act')
        op.mode = 'sync'
        op.all = True
        # Under
        row = col.row(align=True)
        op = row.operator('group.objects_select', text='Sel Act')
        op.group_filter = 'active_object'
        op.all = True
        op.deselect = False
        op = row.operator('group.objects_select', text='Desel Act')
        op.group_filter = 'active_object'
        op.all = True
        op.deselect = True

    def draw_main_actions(self, context, layout):
        """Main Actions. search popup buttons, new, delete"""
        scn = context.scene
        gm = scn.group_manager
        ob = scn.objects.active

        col = layout.column(align=True)
        # Top
        row = col.row(align=True)
        icon = 'VIEWZOOM'
        row.operator('group.objects_link', text='Add', icon=icon)
        op = row.operator('group.objects_link', text='Assign', icon=icon)
        op.unlink_others = True
        row.operator('group.create', text='', icon='ZOOMIN')
        # Middle
        row = col.row(align=True)
        row.operator('group.objects_unlink', text='Remove', icon=icon)
        row.operator('group.objects_remove', text='Remove All')
        row.operator('group.delete', text='', icon='ZOOMOUT')
        # Under
        row = col.row(align=True)
        op = row.operator('group.objects_select', text='Select', icon=icon)
        op.group_filter = 'all'
        op = row.operator('group.objects_select', text='Deselect', icon=icon)
        op.group_filter = 'all'
        op.deselect = True
        row.prop(gm, 'select_is_visible', text='', icon='RESTRICT_VIEW_OFF')

    def draw(self, context):
        scn = context.scene
        gm = scn.group_manager

        layout = self.layout
        self.draw_main_actions(context, layout)
        self.draw_actob_actions(context, layout)
        groups = self.draw_list_type(context, layout)
        if gm.show_groups:
            for group in groups:
                self.draw_group(context, layout, group)


### Property ##################################################################
class GroupManager(bpy.types.PropertyGroup):
    group = bpy.props.StringProperty(
        name='Group Name',
        description='Updated by invoke_search_popup',
        default='')
    show_groups = bpy.props.BoolProperty(
        name='Draw group list',
        default=True)
    list_type = bpy.props.EnumProperty(
        name='Group list type',
        items=(('all', 'All', ''),
               ('scene', 'Scene', ''),
               ('layer', 'Layer', ''),
               ('visible', 'Visible', ''),
               ('selected', 'Selected', ''),
               ('active_object', 'ActOb', '')),
        default='scene')
    show_restrict = bpy.props.BoolProperty(
        name='Show Restrict',
        default=True)
    show_group_ops = bpy.props.BoolProperty(
        name='Show Group Ops',
        default=True)
    select_is_visible = bpy.props.BoolProperty(
        name='Restrict to visible',
        description='Restrict selection to visible',
        default=False)
    active_group = bpy.props.StringProperty(
        name='Active Group')  # context_pointer_setが使えない場合に
    active_object = bpy.props.StringProperty(
        name='Active Object')  # context_pointer_setが使えない場合に


class GroupManagerProperties(bpy.types.PropertyGroup):
    """each group"""
    use_color_wire = bpy.props.BoolProperty(
        name='use_color_wire',
        default=False)
    wire_color = bpy.props.FloatVectorProperty(
        name='color',
        description='Group wire color',
        default=(0.0, 0.0, 0.0),
        min=0.0,
        max=1.0,
        subtype='COLOR_GAMMA',
        size=3)
    priority = bpy.props.IntProperty(
        name='Priority', default=0,
        min=-100,
        max=100)
    show_options = bpy.props.BoolProperty(
        name='Open Properties',
        default=False)
    show_objects = bpy.props.BoolProperty(
        name='Open Objects List',
        default=False)


# Register
def register():
    addongroup.AddonGroup.register_module(__name__)
    bpy.types.Scene.group_manager = bpy.props.PointerProperty(
        name='Group Manager',
        type=GroupManager)
    bpy.types.Group.manager = bpy.props.PointerProperty(
        name='Group Manager Properties',
        type=GroupManagerProperties)

    if TEST_UIList:
        bpy.types.Group.active_object_index = bpy.props.IntProperty(
            name='Active Object Index')


def unregister():
    addongroup.AddonGroup.unregister_module(__name__)
    if TEST_UIList:
        del bpy.types.Group.active_object_index


if __name__ == '__main__':
    register()
