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


import traceback
from collections import OrderedDict

import bpy
import blf

from ..utils import addongroup

from . import oputils


BP = bpy.props.BoolProperty
CP = bpy.props.CollectionProperty
IP = bpy.props.IntProperty
EP = bpy.props.EnumProperty
FP = bpy.props.FloatProperty
FVP = bpy.props.FloatVectorProperty
PP = bpy.props.PointerProperty
SP = bpy.props.StringProperty


def get_prefs():
    return bpy.context.user_preferences.addons[__package__].preferences


def property_from_bpy_struct(prop):
    if prop.type not in ('BOOLEAN', 'ENUM', 'INT', 'FLOAT', 'STRING'):
        return None

    attrs = {'name': prop.name,
             'description': prop.description}

    if prop.type in ('BOOLEAN', 'INT', 'FLOAT') and prop.array_length > 0:
        attrs['default'] = tuple(prop.default_array)
        attrs['size'] = prop.array_length
    else:
        attrs['default'] = prop.default
    if prop.type in ('BOOLEAN', 'INT', 'FLOAT', 'STRING'):
        if prop.subtype == 'LAYER_MEMBER':  # 未対応
            attrs['subtype'] = 'LAYER'
        else:
            attrs['subtype'] = prop.subtype
    if prop.type == 'STRING':
        attrs['maxlen'] = prop.length_max
    if prop.type in ('INT', 'FLOAT'):
        attrs['min'] = prop.hard_min
        attrs['max'] = prop.hard_max
        attrs['soft_min'] = prop.soft_min
        attrs['soft_max'] = prop.soft_max
        attrs['step'] = prop.step
        if prop.type == 'FLOAT':
            attrs['precision'] = prop.precision
            attrs['unit'] = prop.unit
    if prop.type == 'ENUM':
        attrs['items'] = tuple(
            [(p.identifier, p.name, p.description, p.icon, p.value)
             for p in prop.enum_items])

    attrs['options'] = set()
    if prop.is_hidden:
        attrs['options'].add('HIDDEN')
    if prop.is_enum_flag:
        attrs['options'].add('ENUM_FLAG')

    if prop.type == 'BOOLEAN':
        if prop.array_length > 0:
            return bpy.props.BoolVectorProperty(**attrs)
        else:
            return bpy.props.BoolProperty(**attrs)
    elif prop.type == 'ENUM':
        if len(attrs['items']) == 0:
            # get関数があるものと仮定する
            d = {k: attrs[k] for k in ('name', 'description', 'default')}
            d['options'] = attrs['options'] & {'HIDDEN'}
            return bpy.props.StringProperty(**d)
        else:
            return bpy.props.EnumProperty(**attrs)
    elif prop.type == 'FLOAT':
        if prop.array_length > 0:
            return bpy.props.FloatVectorProperty(**attrs)
        else:
            return bpy.props.FloatProperty(**attrs)
    elif prop.type == 'INT':
        if prop.array_length > 0:
            return bpy.props.IntVectorProperty(**attrs)
        else:
            return bpy.props.IntProperty(**attrs)
    elif prop.type == 'STRING':
        return bpy.props.StringProperty(**attrs)


class PieMenuOpArg(bpy.types.PropertyGroup):
    key = SP()  # make_key()の結果を格納

    def make_key(self, string):
        """eg. 'mesh.delete.type' -> 'mesh__DOT__delete__DOT__type'
        """
        return string.replace('.', '__DOT__')

    def draw(self, context, layout):
        """
        :type context: bpy.types.Context
        :type layout: bpy.types.UILayout
        """
        # prop = getattr(self, self.name)
        layout.prop(self, self.name)


def get_operator(name):
    split = name.split('.')
    op = None
    if len(split) == 2:
        m, o = split
        if m in dir(bpy.ops):  # hasattr(bpy.ops, m)は無意味
            mod = getattr(bpy.ops, m)
            if o in dir(mod):  # hasattr(mod, o)は無意味
                op = getattr(mod, o)
    return op


def get_operator_arg_owner(operator_arg):
    """PieMenuOpArgから、それが属するPieMenuMenuとPieMenuItemを取得する"""
    prefs = bpy.context.user_preferences.addons[__package__].preferences
    for menu in prefs.pie_menus:
        for item in menu.menu_items:
            for arg in item.operator_args:
                if arg == operator_arg:
                    return menu, item
            for arg in item.shift.operator_args:
                if arg == operator_arg:
                    return menu, item.shift
            for arg in item.ctrl.operator_args:
                if arg == operator_arg:
                    return menu, item.ctrl
    return None, None


# def operator_arg_update(self):
#     """PieMenuOpArgの属性が更新された際にPieMenuItem.execute_stringを更新する"""
#     menu, item = get_operator_arg_owner(self)
#     if not item:
#         return
#
#     op = get_operator(item.operator)
#     if not op:
#         return
#
#     args = ["'" + item.operator_execution_context + "'"]
#     if item.is_property_set('operator_undo'):
#         args.append(str(item.operator_undo))
#     ls_kwargs = []
#     for arg in self.item.operator_args:
#         n = arg.name.split('__DOT__')[-1]
#         if arg.is_property_set(arg.name):
#             val = getattr(arg, arg.name)
#             if isinstance(val, str):
#                 ls_kwargs.append("{}='{}'".format(n, val))
#             else:
#                 ls_kwargs.append('{}={}'.format(n, val))
#     t = 'bpy.ops.{}({})'.format(op.idname_py(), ', '.join(args + ls_kwargs))
#     item.execute_string = t


def ensure_operator_args(item, clear=False):
    bl_rna = None
    op = get_operator(item.operator)
    if op:
        bl_rna = op.get_rna().bl_rna
    if not bl_rna:
        return

    c_props = [p for p in bl_rna.properties if p.identifier != 'rna_type']
    if clear:
        item.operator_args.clear()
        for i in range(len(c_props)):
            item.operator_args.add()
    else:
        n = len(item.operator_args) - len(c_props)
        if n > 0:
            for i in range(n):
                item.operator_args.remove(len(item.operator_args) - 1)
        elif n < 0:
            for i in range(-n):
                item.operator_args.add()
    for arg, c_prop in zip(item.operator_args, c_props):
        # eg. 'mesh.delete.type' -> 'mesh__DOT__delete__DOT__type'
        arg.name = c_prop.identifier
        arg.key = arg.make_key(item.operator + '.' + arg.name)
        prop = property_from_bpy_struct(c_prop)
        setattr(PieMenuOpArg, arg.key, prop)


def prop_operator_update(self, context):
    ensure_operator_args(self, True)

    # # label, description, poll_stringを上書き
    # op = get_operator(self.operator)
    # if op:
    #     self.label = op.get_rna().bl_rna.name
    #     self.poll_string = 'bpy.ops.{}.poll()'.format(op.idname_py())
    #     self.execute_string = ''


def prop_operator_search_items(self, context):
    if hasattr(prop_operator_search_items, 'items'):
        return prop_operator_search_items.items
    items = []
    for mod in dir(bpy.ops):
        for op in dir(getattr(bpy.ops, mod)):
            name = mod + '.' + op
            items.append((name, name, ''))
    prop_operator_search_items.items = items
    return items


def prop_operator_search_set(self, value):
    items = prop_operator_search_items(self, bpy.context)
    name = items[value][0]
    self.operator = name


class WM_OT_pie_menu_search_operator(bpy.types.Operator):
    """
    Usage:
        op = layout.operator('wm.pie_menu_search_operator',
                             text='', icon='VIEWZOOM')
        WM_OT_pie_menu_search_operator.set_target(op, self)
    """
    bl_idname = 'wm.pie_menu_search_operator'
    bl_label = ''
    bl_description = ''
    bl_options = {'INTERNAL'}
    bl_property = 'operator'

    data = {}

    operator = EP(name='Operator', items=prop_operator_search_items,)
    target = SP()  # value == str(id(item))

    @classmethod
    def set_target(cls, op, obj):
        key = id(obj)
        cls.data[key] = obj
        op.target = str(key)

    def get_target(self):
        return self.data[int(self.target)]

    def execute(self, context):
        prop = self.get_target()
        prop.operator = self.operator
        return {'FINISHED'}

    def invoke(self, context, event):
        if hasattr(prop_operator_search_items, 'items'):
            del prop_operator_search_items.items
        context.window_manager.invoke_search_popup(self)
        return {'INTERFACE'}


class WM_OT_pie_menu_stubs(bpy.types.Operator):
    bl_idname = 'wm.pie_menu_stubs'
    bl_label = 'Execute Function'
    bl_description = ''
    bl_options = {'INTERNAL'}

    function = SP()

    def menu_add(self, context):
        prefs = get_prefs()
        prefs.pie_menus.add()

    def menu_remove(self, context):
        prefs = get_prefs()
        i = list(prefs.pie_menus).index(context.pie_menu)
        prefs.pie_menus.remove(i)

    def item_add(self, context):
        context.pie_menu.menu_items.add()

    def item_remove(self, context):
        i = list(context.pie_menu.menu_items).index(context.pie_item)
        context.pie_menu.menu_items.remove(i)

    def arg_unset(self, context):
        context.pie_arg.property_unset(context.pie_arg.key)

    # @classmethod
    # def menus_unset(cls, context):
    #     prefs = get_prefs()
    #     prefs.property_unset('pie_menus')

    # @classmethod
    # def menus_reset(cls, context):
    #     reset_menus(context)

    def execute(self, context):
        getattr(self, self.function)(context)
        return {'FINISHED'}


def prop_from_text_enum(self, context):
    items = []
    for text in bpy.data.texts:
        items.append((text.name, text.name, ''))
    items = tuple(items)
    prop_from_text_enum.items = items
    return items


class WM_OT_pie_menu_text_from(bpy.types.Operator):
    bl_idname = 'wm.pie_menu_text_from'
    bl_label = 'From Text'
    bl_description = ''
    bl_options = {'INTERNAL'}

    data = {}

    text = EP(name='Text', items=prop_from_text_enum)

    @classmethod
    def set_target(cls, layout, obj, attr):
        cls.data[layout] = (obj, attr)

    def execute(self, context):
        if self.text in bpy.data.texts:
            string = '\n'.join(
                [line.body for line in bpy.data.texts[self.text].lines])
            # setattr(*self.data[context.layout], string)  # 3.5系からの書式
            setattr(*(list(self.data[context.layout]) + [string]))
        return {'FINISHED'}


class WM_OT_pie_menu_text_to(bpy.types.Operator):
    bl_idname = 'wm.pie_menu_text_to'
    bl_label = 'To Text'
    bl_description = 'Overwrite text'
    bl_options = {'INTERNAL'}

    data = {}

    text = EP(name='Text', items=prop_from_text_enum)

    @classmethod
    def set_target(cls, layout, obj, attr):
        cls.data[layout] = (obj, attr)

    def execute(self, context):
        if self.text in bpy.data.texts:
            text = bpy.data.texts[self.text]
            text.clear()
            text.from_string(getattr(*self.data[context.layout]))
        return {'FINISHED'}


class WM_OT_pie_menu_item_auto_complete(bpy.types.Operator):
    bl_idname = 'wm.pie_menu_item_auto_complete'
    bl_label = 'Auto Complete'
    bl_description = ''
    bl_options = {'INTERNAL'}

    def execute(self, context):
        item = context.pie_item
        if item.use_advance:
            op, args_kwargs = oputils.get_operator_arguments(
                item.execute_string)
            if op and args_kwargs:
                args, kwargs = args_kwargs
                item.operator = op.idname_py()
                for arg in item.operator_args:
                    if arg.name in kwargs:
                        try:
                            setattr(arg, arg.key, kwargs[arg.name])
                        except:
                            arg.property_unset(arg.key)
                            traceback.print_exc()
                for value in args:
                    if isinstance(value, str):
                        try:
                            item.operator_execution_context = value
                        except:
                            traceback.print_exc()
                            item.property_unset('operator_execution_context')
                    elif isinstance(value, bool):
                        item.operator_undo = value
        else:
            item.execute_string = item.to_execute_string()
            op = get_operator(item.operator)
        if op:
            bl_rna = op.get_rna().bl_rna
            item.label = bl_rna.name
            item.description = bl_rna.description
            item.poll_string = 'return bpy.ops.{}.poll()'.format(
                op.idname_py())
        return {'FINISHED'}


class PieMenuItem(bpy.types.PropertyGroup):
    label = SP(name='Label')

    # def description_get(self):
    #     if self.use_advance:
    #         if '_description' not in self:
    #             self['_description'] = ''
    #         return self['_description']
    #     else:
    #         op = get_operator(self.operator)
    #         if op:
    #             return op.get_rna().bl_rna.description
    #         else:
    #             return ''
    # def description_set(self, value):
    #     self['_description'] = value
    # description = SP(name='Description', get=description_get,
    #                  set=description_set)
    # del description_get, description_set
    description = SP(name='Description')

    icon = SP(name='Icon')
    # bl_rna = bpy.types.UILayout.bl_rna
    # items = bl_rna.functions['label'].parameters['icon'].enum_items
    # for item in items:
    #     icons[item.identifier] = item.value
    # icon = EP(name='Icon',
    #           items=[(item.identifier, item.name, item.description)
    #                  for item in bpy.types.UILayout.bl_rna.functions['label'].parameters['icon'].enum_items])

    shortcut = EP(
        name='Shortcut',
        items=[(e.identifier, e.name, '') for e in
               bpy.types.Event.bl_rna.properties['type'].enum_items])
    # shortcut = SP(name='Shortcut')
    execute_string = SP(name='Execute String')
    poll_string = SP(name='Poll String')
    menu = SP(name='Menu')
    undo_push = BP(name='Undo Push')

    use_shift = BP(name='Use Shift')
    use_ctrl = BP(name='Use Ctrl')

    # 偽ならoperator, operator_args等を使用
    use_advance = BP(name='Use Advance')

    operator = bpy.props.StringProperty(
        name='Operator',
        update=prop_operator_update)
    operator_args = CP(name='Arguments', type=PieMenuOpArg)
    operator_execution_context = bpy.props.EnumProperty(
        name='Execution Context',
        items=[(s, s, '') for s in
               ['INVOKE_DEFAULT', 'INVOKE_REGION_WIN',
                'INVOKE_REGION_CHANNELS', 'INVOKE_REGION_PREVIEW',
                'INVOKE_AREA', 'INVOKE_SCREEN', 'EXEC_DEFAULT',
                'EXEC_REGION_WIN', 'EXEC_REGION_CHANNELS',
                'EXEC_REGION_PREVIEW', 'EXEC_AREA', 'EXEC_SCREEN']],
        default='INVOKE_DEFAULT'
    )
    operator_undo = bpy.props.BoolProperty(name='Undo', default=False)
    operator_search = bpy.props.EnumProperty(
        name='Operator',
        items=prop_operator_search_items,
        set=prop_operator_search_set,
    )

    show_expanded = BP(name='Show Details')

    def to_execute_string(self):
        op = get_operator(self.operator)
        if not op:
            return ''
        args = ["'" + self.operator_execution_context + "'"]
        if self.is_property_set('operator_undo'):
            args.append(self.operator_undo)
        kwargs = OrderedDict()
        for arg in self.operator_args:
            if arg.is_property_set(arg.key):
                kwargs[arg.name] = getattr(arg, arg.key)
        for k, v in kwargs.items():
            if isinstance(v, str):
                args.append("{}='{}'".format(k, v))
            else:
                try:
                    v = list(v)
                except:
                    pass
                args.append("{}={}".format(k, v))
        return '{}({})'.format(op.idname_py(), ', '.join(args))

    def execute(self, context):
        if self.use_advance:
            if self.execute_string:
                return oputils.execute(self.execute_string,
                                       {'self': self, 'context': context})
            else:
                return None
        else:
            op = get_operator(self.operator)
            args = [self.operator_execution_context]
            if self.is_property_set('operator_undo'):
                args.append(self.operator_undo)
            kwargs = {}
            for arg in self.operator_args:
                if arg.is_property_set(arg.key):
                    kwargs[arg.name] = getattr(arg, arg.key)
            return op(*args, **kwargs)

    def poll(self, context):
        if self.use_advance and self.poll_string:
            return oputils.execute(self.poll_string,
                                   {'self': self, 'context': context})
        else:
            op = oputils.get_operator(self.execute_string)
            if op:
                return op.poll()
            else:
                return True

    def draw(self, context, layout, shift=False, ctrl=False):
        base_column = layout.column()

        column = base_column.box()
        column.context_pointer_set('pie_item', self)

        title_row = column.row()

        split = title_row.split(0.7)
        row = split.row()
        sub = row.row()
        sub.alignment = 'LEFT'
        icon = 'TRIA_DOWN' if self.show_expanded else 'TRIA_RIGHT'
        op = sub.operator('wm.context_toggle', text='', icon=icon,
                          emboss=False)
        op.data_path = 'pie_item.show_expanded'
        if shift:
            sub.label('Shift:')
        elif ctrl:
            sub.label('Ctrl:')

        row.prop(self, 'label')

        row = split.row()
        row.prop(self, 'shortcut', text='', event=True)
        if not shift and not ctrl:
            sub = row.row()
            sub.alignment = 'RIGHT'
            op = sub.operator('wm.pie_menu_stubs', text='', icon='PANEL_CLOSE')
            op.function = 'item_remove'

        if not self.show_expanded:
            return

        row = column.row()
        row.prop(self, 'icon')
        row.prop(self, 'menu')
        row.prop(self, 'use_shift', 'Shift')
        row.prop(self, 'use_ctrl', 'Ctrl')

        row = column.row()
        row.prop(self, 'use_advance', text='Advance')

        box = column.box()
        if self.use_advance:
            col = box.column()
            for attr in ['execute_string', 'poll_string', 'description']:
                row = col.row()
                row.prop(self, attr)

                if attr == 'execute_string':
                    sub = row.row()
                    sub.alignment = 'RIGHT'
                    sub.operator('wm.pie_menu_item_auto_complete', text='',
                                 icon='FILE_REFRESH')

                sub = row.row(align=True)
                sub.alignment = 'RIGHT'
                sub2 = sub.row(align=True)
                sub2.context_pointer_set('layout', sub2)
                sub2.operator_menu_enum(
                    'wm.pie_menu_text_from', 'text', text='',
                    icon='COPYDOWN')
                WM_OT_pie_menu_text_from.set_target(sub2, self, attr)
                sub2 = sub.row(align=True)
                sub2.context_pointer_set('layout', sub2)
                sub2.operator_menu_enum(
                    'wm.pie_menu_text_to', 'text', text='',
                    icon='PASTEDOWN')
                WM_OT_pie_menu_text_to.set_target(sub2, self, attr)
            row = box.row()
            row.prop(self, 'undo_push')
        else:
            row = box.row()
            sub = row.row(align=True)
            sub.prop(self, 'operator')
            op = sub.operator('wm.pie_menu_search_operator',
                              text='', icon='VIEWZOOM')
            WM_OT_pie_menu_search_operator.set_target(op, self)
            sub = row.row()
            sub.prop(self, 'operator_execution_context', text='')
            sub = row.row()
            sub.prop(self, 'operator_undo')
            sub.active = self.is_property_set('operator_undo')

            sub = row.row()
            sub.alignment = 'RIGHT'
            sub.operator('wm.pie_menu_item_auto_complete', text='',
                         icon='FILE_REFRESH')

            if self.operator_args:
                flow = box.column_flow(2)
                for arg in self.operator_args:
                    sub_box = flow.box()
                    row = sub_box.row()
                    sub = row.row()
                    sub.prop(arg, arg.key)
                    if arg.is_property_set(arg.key):
                        sub = row.row()
                        sub.alignment = 'RIGHT'
                        sub.context_pointer_set('pie_arg', arg)
                        op = sub.operator('wm.pie_menu_stubs',
                                          text='', icon='PANEL_CLOSE')
                        op.function = 'arg_unset'
                    else:
                        sub_box.active = False

        if shift or ctrl:
            return

        split = base_column.split(0.05)
        split.column()
        column = split.column()

        if self.use_shift:
            self.shift.draw(context, column, shift=True)
        if self.use_ctrl:
            self.ctrl.draw(context, column, ctrl=True)


PieMenuItem.shift = PP(type=PieMenuItem)
PieMenuItem.ctrl = PP(type=PieMenuItem)


class PieMenuMenu(bpy.types.PropertyGroup):
    idname = SP(name='ID Name', get=lambda self: self.name)
    label = SP(name='Label')
    init_string = SP(name='Init String')
    poll_string = SP(name='Poll String')
    close_string = SP(name='Close String')

    next = SP(name='Next Menu')
    prev = SP(name='Prev Menu')
    center_action = EP(
        name='Center Action',
        items=[('none', 'None', ''),
               ('last', 'Last', ''),
               ('fixed', 'Fixed', '')],
        default='last')
    center_index = IP(name='Center Index', min=0)
    icon_size = IP(name='Icon Size', default=-1, min=-1)
    radius = IP(name='Radius', default=-1)

    menu_items = CP(type=PieMenuItem)

    show_expanded = BP(name='Show Details')
    use_advance = BP(name='Use Advance')

    def draw(self, context, layout):
        column = layout.column(align=True)
        column.context_pointer_set('pie_menu', self)

        if self.show_expanded:
            box = column.box().column()
            title_row = box.row()
        else:
            title_row = column.row()
        row = title_row.row()
        row.alignment = 'LEFT'
        icon = 'TRIA_DOWN' if self.show_expanded else 'TRIA_RIGHT'
        op = row.operator('wm.context_toggle', text='', icon=icon,
                          emboss=False)
        op.data_path = 'pie_menu.show_expanded'

        title_row.prop(self, 'name', text='ID Name')
        title_row.prop(self, 'label', text='Label')

        # 削除
        row = title_row.row()
        row.alignment = 'RIGHT'
        op = row.operator('wm.pie_menu_stubs', text='', icon='PANEL_CLOSE')
        op.function = 'menu_remove'

        if self.show_expanded:
            col = column.box().column()
            # col = box.column()
            row = col.row()
            row.prop(self, 'center_action')
            sub = row.row()
            sub.active = self.center_action == 'fixed'
            sub.prop(self, 'center_index')
            row.prop(self, 'icon_size')
            row.prop(self, 'radius')

            row = col.row()
            row.prop(self, 'use_advance', 'Advance')
            if self.use_advance:
                row = col.row()
                sub = row.row()
                sub.prop(self, 'next')
                sub.prop(self, 'prev')

                for attr, label in [['init_string', 'Init'],
                                    ['poll_string', 'Poll'],
                                    ['close_string', 'Close']]:
                    row = col.row()
                    row.prop(self, attr, text=label)
                    sub = row.row(align=True)
                    sub.alignment = 'RIGHT'
                    sub2 = sub.row(align=True)
                    sub2.context_pointer_set('layout', sub2)
                    sub2.operator_menu_enum(
                        'wm.pie_menu_text_from', 'text', text='',
                        icon='COPYDOWN')
                    WM_OT_pie_menu_text_from.set_target(sub2, self, attr)
                    sub2 = sub.row(align=True)
                    sub2.context_pointer_set('layout', sub2)
                    sub2.operator_menu_enum(
                        'wm.pie_menu_text_to', 'text', text='',
                        icon='PASTEDOWN')
                    WM_OT_pie_menu_text_to.set_target(sub2, self, attr)

            split = col.split(0.05)
            split.column()
            item_col = split.column()
            if self.menu_items:
                for item in self.menu_items:
                    item.draw(context, item_col.column())

            row = item_col.row()
            row.alignment = 'LEFT'
            op = row.operator('wm.pie_menu_stubs', text='Add New',
                              icon='ZOOMIN')
            op.function = 'item_add'



class FVPColor:
    def __new__(cls, name, default, **kwargs):
        return FVP(name=name, default=default,
                   min=0.0, max=1.0, soft_min=0.0, soft_max=1.0,
                   subtype='COLOR_GAMMA', size=4, **kwargs)


class PieMenu_PG_Colors(bpy.types.PropertyGroup):
    use_theme = BP(name='Use Theme Color',
                   description='if True, read user preference',
                   default=False)

    @classmethod
    def _generate_props(cls):
        def gen(attr, klass, name, get_string, **kwargs):
            def get(self):
                if self.use_theme:
                    user_pref = bpy.context.user_preferences
                    theme = user_pref.themes['Default']
                    ui = theme.user_interface
                    value = eval(get_string)
                else:
                    value = getattr(self, 'prop_' + attr)
                try:
                    ls = list(value)
                    return (ls + [1.0])[:4]
                except:
                    return value
            def set(self, value):
                setattr(self, 'prop_' + attr, value)
            setattr(cls, 'prop_' + attr, klass(name=name, **kwargs))
            setattr(cls, attr, klass(name=name, set=set, get=get, **kwargs))

        gen('menu_inner', FVPColor, 'Menu Inner',
            'ui.wcol_menu_back.inner',
            default=(0.0, 0.0, 0.0, 1.0))
        gen('menu_show_shaded', BP, 'Shaded',
            'ui.wcol_menu_back.show_shaded',
            default=False)
        gen('menu_shadetop', IP, 'Shade Top',
            'ui.wcol_menu_back.shadetop',
            default=30, min=-100, max=100)
        gen('menu_shadedown', IP, 'Shade Top',
            'ui.wcol_menu_back.shadedown',
            default=-30, min=-100, max=100)
        gen('title_outline', FVPColor, 'Title Outline',
            'ui.wcol_menu_back.outline',
            default=(0.0, 0.0, 0.0, 1.0))
        theme = bpy.context.user_preferences.themes['Default']
        try:
            col = list(theme.view_3d.space.gradients.high_gradient)
        except:
            col = [0.4, 0.4, 0.4]
        gen('title_inner', FVPColor, 'Title Inner',
            'ui.wcol_menu_back.inner',
            default=col + [1.0])
        gen('title_inner_sel', FVPColor, 'Title Inner Sel',
            'ui.wcol_menu_back.inner_sel',
            default=col + [1.0])
        del theme, col
        gen('title_text', FVPColor, 'Title Text',
            'ui.wcol_menu_back.text',
            default=(1.0, 1.0, 1.0, 1.0))
        gen('title_text_sel', FVPColor, 'Title Text Sel',
            'ui.wcol_menu_back.text_sel',
            default=(1.0, 1.0, 1.0, 1.0))
        gen('title_show_shaded', BP, 'Shaded',
            'ui.wcol_menu_back.show_shaded',
            default=False)
        gen('title_shadetop', IP, 'Shade Top',
            'ui.wcol_menu_back.shadetop',
            default=30, min= -100, max=100)
        gen('title_shadedown', IP, 'Shade Down',
            'ui.wcol_menu_back.shadedown',
            default=-30, min=-100, max=100)
        gen('item_outline', FVPColor, 'Item Outline',
            'ui.wcol_menu_back.outline',
            default=(0.0, 0.0, 0.0, 1.0))
        gen('item_inner', FVPColor, 'Item Inner',
            'ui.wcol_menu_item.inner',
            default=(0.0, 0.0, 0.0, 0.0))
        gen('item_inner_sel', FVPColor, 'Item Inner Sel',
            'ui.wcol_menu_item.inner_sel',
            default=(0.9, 0.9, 0.9, 1.0))
        gen('item_text', FVPColor, 'Item Text',
            'ui.wcol_menu_item.text',
            default=(1.0, 1.0, 1.0, 1.0))
        gen('item_text_sel', FVPColor, 'Item Text Sel',
            'ui.wcol_menu_item.text_sel',
            default=(0.0, 0.0, 0.0, 1.0))
        gen('item_show_shaded', BP, 'Shaded',
            'ui.wcol_menu_item.show_shaded',
            default=False)
        gen('item_shadetop', IP, 'Shade Top',
            'ui.wcol_menu_item.shadetop',
            default=30, min= -100, max=100)
        gen('item_shadedown', IP, 'Shade Down',
            'ui.wcol_menu_item.shadedown',
            default=-30, min=-100, max=100)
        gen('tooltip_outline', FVPColor, 'Tooltip Outline',
            'ui.wcol_tooltip.outline',
            default=(1.0, 1.0, 1.0, 1.0))
        gen('tooltip_inner', FVPColor, 'Tooltip Inner',
            'ui.wcol_tooltip.inner',
            default=(0.4, 0.4, 0.4, 1.0))
        gen('tooltip_text', FVPColor, 'Tooltip Text',
            'ui.wcol_tooltip.text',
            default=(1.0, 1.0, 1.0, 1.0))
        gen('tooltip_show_shaded', BP, 'Shaded',
            'ui.wcol_tooltip.show_shaded',
            default=False)
        gen('tooltip_shadetop', IP, 'Shade Top',
            'ui.wcol_tooltip.shadetop',
            default=30, min=-100, max=100)
        gen('tooltip_shadedown', IP, 'Shade Down',
            'ui.wcol_tooltip.shadedown',
            default=-30, min=-100, max=100)
        gen('text', FVPColor, 'Text',
            'theme.view_3d.space.text_hi',
            default=(1.0, 1.0, 1.0, 1.0))

    line = FVPColor('Line', (1.0, 1.0, 1.0, 1.0))
    separator = FVPColor('Separator', (1.0, 1.0, 1.0, 0.5))
    pointer = FVPColor('Pointer', (1.0, 1.0, 1.0, 1.0))
    pointer_outline = FVPColor('Pointer Outline', (0.0, 0.0, 0.0, 1.0))
    pie_sel = FVPColor('Pie Sel', (1.0, 1.0, 1.0, 0.4))
    menu_marker = FVPColor('Menu Marker', (1.0, 1.0, 1.0, 1.0))
    menu_marker_outline = FVPColor('Menu Marker Outline', (0.0, 0.0, 0.0, 1.0))

PieMenu_PG_Colors._generate_props()


def font_id_get(self):
    U = bpy.context.user_preferences
    path = U.system.font_path_ui
    if path:
        i = blf.load(path)
        if i != -1:
            return i
    return 0


class PieMenuPreferences(addongroup.AddonGroup,
                         bpy.types.PropertyGroup if '.' in __name__ else
                         bpy.types.AddonPreferences):
    bl_idname = __package__

    font_id = IP(name='Font ID', default=0, min=0, get=font_id_get) # 読み込み専用
    font_id_mono = IP(name='Font ID Mono', default=1, min=0)  # 読み込み専用
    # 六時方向からアイテムの描画を始める
    tacho = BP(name="Six O'clock", default=True)
    # 中心からアイコンの円の境界まで
    menu_radius = IP(name='Menu Radius', default=30, min=10)
    menu_radius_center = IP(name='Menu Radius Center', default=10, min=0)
    # submenuに切り替えた際に中心を変えない
    lock_menu_location = BP(name='Lock Menu Location', default=False)

    # Itemの上下の隙間がこれより狭いならmenu_radiusを広げる
    item_min_space = IP(name='MenuItem Min Space', default=4, min=0)
    # ItemのroundedBox描画位置をアイコン方向にずらす (top, bottom)
    item_box_ofsy = IP(name='MenuItem Box Ofsy', default=-3)
    # 上下のItemのアイコンの部分を台形にする
    item_box_trapezoid = IP(name='MenuItem Trapezoid', default=0, min=0)
    tooltip_time = FP(name='Tooltip Time', default=0.4, min=0.0)

    colors = PP(type=PieMenu_PG_Colors)
    """:type: PieMenu_PG_Colors"""

    pie_menus = CP(type=PieMenuMenu)

    def draw(self, context):
        layout = self.layout
        split = layout.split()

        col = split.column()
        col.prop(self, 'tacho')
        col.prop(self, 'menu_radius')
        col.prop(self, 'menu_radius_center')
        col.prop(self, 'lock_menu_location')
        col.prop(self, 'item_min_space')
        col.prop(self, 'item_box_ofsy')
        col.prop(self, 'item_box_trapezoid')
        col.prop(self, 'tooltip_time')

        colors = self.colors

        col = split.column()

        sub = col.box().column()
        sub.prop(colors, 'line')
        sub.prop(colors, 'separator')
        sub.prop(colors, 'pointer')
        sub.prop(colors, 'pointer_outline')
        sub.prop(colors, 'pie_sel')

        col = split.column()

        col.prop(colors, 'use_theme', 'Use Current Theme')

        sub = col.box().column()
        sub.active = not colors.use_theme
        sub.label('Menu Back:')
        sub.prop(colors, 'menu_inner', text='Inner')
        sub.prop(colors, 'menu_show_shaded')
        sub2 = sub.column(align=True)
        sub2.active = colors.menu_show_shaded
        sub2.prop(colors, 'menu_shadetop')
        sub2.prop(colors, 'menu_shadedown')

        sub = col.box().column()
        sub.active = not colors.use_theme
        sub.label('Title:')
        sub.prop(colors, 'title_outline', text='Outline')
        sub.prop(colors, 'title_inner', text='Inner')
        sub.prop(colors, 'title_inner_sel', text='Inner Sel')
        sub.prop(colors, 'title_text', text='Text')
        sub.prop(colors, 'title_text_sel', text='Text Sel')
        sub.prop(colors, 'title_show_shaded')
        sub2 = sub.column(align=True)
        sub2.active = colors.title_show_shaded
        sub2.prop(colors, 'title_shadetop')
        sub2.prop(colors, 'title_shadedown')

        col = split.column()

        sub = col.box().column()
        sub.active = not colors.use_theme
        sub.label('Item:')
        sub.prop(colors, 'item_outline', text='Outline')
        sub.prop(colors, 'item_inner', text='Inner')
        sub.prop(colors, 'item_inner_sel', text='Inner Sel')
        sub.prop(colors, 'item_text', text='Text')
        sub.prop(colors, 'item_text_sel', text='Text Sel')
        sub.prop(colors, 'item_show_shaded')
        sub2 = sub.column(align=True)
        sub2.active = colors.item_show_shaded
        sub2.prop(colors, 'item_shadetop')
        sub2.prop(colors, 'item_shadedown')

        sub = col.box().column()
        sub.active = not colors.use_theme
        sub.label('Tooltip:')
        sub.prop(colors, 'tooltip_outline', text='Outline')
        sub.prop(colors, 'tooltip_inner', text='Inner')
        sub.prop(colors, 'tooltip_text', text='Text')
        sub.prop(colors, 'tooltip_show_shaded')
        sub2 = sub.column(align=True)
        sub2.active = colors.tooltip_show_shaded
        sub2.prop(colors, 'tooltip_shadetop')
        sub2.prop(colors, 'tooltip_shadedown')
        sub.prop(colors, 'text')

        menus_layout = layout.column()
        for menu in self.pie_menus:
            menu.draw(context, menus_layout)

        row = menus_layout.row()
        row.alignment = 'LEFT'
        op = row.operator('wm.pie_menu_stubs', text='Add New',
                          icon='ZOOMIN')
        op.function = 'menu_add'

        super().draw(context)


classes = [
    PieMenuOpArg,
    PieMenuItem,
    PieMenuMenu,

    PieMenu_PG_Colors,
    PieMenuPreferences,

    WM_OT_pie_menu_search_operator,
    WM_OT_pie_menu_stubs,
    WM_OT_pie_menu_text_from,
    WM_OT_pie_menu_text_to,
    WM_OT_pie_menu_item_auto_complete,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

