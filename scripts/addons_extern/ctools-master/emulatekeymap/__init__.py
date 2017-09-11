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
    'name': 'Emulate Key Map',
    'author': 'chromoly',
    'version': (0, 3, 1),
    'blender': (2, 78, 0),
    'location': 'Screen > Space',
    'description': 'Space + any key, Shift + Space -> any key',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'User Interface',
}

"""
1. Spaceキーと特定キーの組み合わせて別のキーに割り当てられたオペレーターを
   実行する。テンキーレスキーボードを使っている場合等に。
   元々Spaceキーに割り当てられていたメニューは Space + TAB で呼び出せる。
   (初期設定)

2. Shift + Space でキー入力待機モードに入り、入力されたキーに対応する
   オペレーターを実行する。emacsの C-X C-S みたいな機能。
   モードから抜けるには ESC / ctrl + G / shift + Space。
   設定にはテキストファイルを用いる。

listvalidkeysに依存するので単独動作不可。
"""


import importlib
import os
import traceback
import types

import bpy

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(listvalidkeys)
    importlib.reload(st)
except NameError:
    from .. import listvalidkeys
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import structures as st


numpad_preset = {
    'TYPE1': [
        ('NUMPAD_0', 'V'),
        ('NUMPAD_1', 'Z'),
        ('NUMPAD_2', 'X'),
        ('NUMPAD_3', 'C'),
        ('NUMPAD_4', 'A'),
        ('NUMPAD_5', 'S'),
        ('NUMPAD_6', 'D'),
        ('NUMPAD_7', 'Q'),
        ('NUMPAD_8', 'W'),
        ('NUMPAD_9', 'E'),
        ('NUMPAD_PERIOD', 'B'),
        ('NUMPAD_PLUS', 'F'),
        ('NUMPAD_MINUS', 'R'),
        ('NUMPAD_ASTERIX', 'THREE'),
        ('NUMPAD_SLASH', 'TWO'),
        ('NUMPAD_ENTER', 'N '),
        ('SPACE', 'TAB'),
        ('HOME', 'FIVE'),
        ('END', 'T'),

        ('HOLD', 'G'),
    ],

    'TYPE2': [
        ('NUMPAD_0', 'Z'),
        ('NUMPAD_1', 'X'),
        ('NUMPAD_2', 'C'),
        ('NUMPAD_3', 'V'),
        ('NUMPAD_4', 'S'),
        ('NUMPAD_5', 'D'),
        ('NUMPAD_6', 'F'),
        ('NUMPAD_7', 'W'),
        ('NUMPAD_8', 'E'),
        ('NUMPAD_9', 'R'),
        ('NUMPAD_PERIOD', 'A'),
        ('NUMPAD_PLUS', 'G'),
        ('NUMPAD_MINUS', 'T'),
        ('NUMPAD_ASTERIX', 'FOUR'),
        ('NUMPAD_SLASH', 'THREE'),
        ('NUMPAD_ENTER', 'B'),
        ('SPACE', 'TAB'),
        ('HOME', 'ONE'),
        ('END', 'TWO'),

        ('HOLD', 'Q'),
    ],

    'TYPE3': [
        ('NUMPAD_0', 'Z'),
        ('NUMPAD_1', 'A'),
        ('NUMPAD_2', 'S'),
        ('NUMPAD_3', 'D'),
        ('NUMPAD_4', 'Q'),
        ('NUMPAD_5', 'W'),
        ('NUMPAD_6', 'E'),
        ('NUMPAD_7', 'ONE'),
        ('NUMPAD_8', 'TWO'),
        ('NUMPAD_9', 'THREE'),
        ('NUMPAD_PERIOD', 'C'),
        ('NUMPAD_PLUS', 'V'),
        ('NUMPAD_MINUS', 'F'),
        ('NUMPAD_ASTERIX', 'R'),
        ('NUMPAD_SLASH', 'FOUR'),
        ('NUMPAD_ENTER', 'B'),
        ('HOME', 'T'),
        ('END', 'G'),
        ('SPACE', 'TAB'),

        ('HOLD', 'X'),
    ]
}


CONFIG_FILE_NAME = 'special_keymaps.py'


template_docstring = \
"""\"\"\"
keymaps = {keymap: [[key, operator[, argument[, match last]]], ...], ...}

valid modifiers:
    any, shift, ctrl, alt, oskey
valid event types:
    https://www.blender.org/api/blender_python_api_2_78a_release/bpy.types.Event.html#bpy.types.Event.type
exit keys:
    ESC, ctrl + G, ctrl + SPACE, shift + SPACE, any + RIGHTMOUSE
\"\"\"

"""
template_keymaps = \
"""keymaps = {{
    '*': [
        ['ESC', '{idname}', {{}}, True],
        ['ctrl + G', '{idname}', {{}}, True],
        ['any + RIGHTMOUSE', '{idname}', {{}}, True],
    ],

    'Window': [
        ['S', 'wm.search_menu'],
    ],
    'Screen': [
        ['F', 'screen.screen_full_area'],
    ],
    '3D View': [
        ['S', 'wm.call_menu', {{'name': 'VIEW3D_MT_Space_Dynamic_Menu'}}],
    ],
}}
"""


def get_template():
    return template_docstring + template_keymaps.format(
        idname=SCREEN_OT_special_keymap.bl_idname)


###############################################################################
# User Preferences
###############################################################################
CollectionOperator = customproperty.CollectionOperator.derive()


class WM_OT_event_type_search_popup(bpy.types.Operator):
    bl_idname = 'wm.event_type_search_popup'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_property = 'type'

    _prop = bpy.types.KeyMapItem.bl_rna.properties['type']
    _items = [(e.identifier, e.identifier + '    ' + e.name, e.description,
               e.value)
              for e in _prop.enum_items]
    type = bpy.props.EnumProperty(
        items=_items,
        name='Type',
        default='NONE',
    )
    del _prop, _items

    data_path = bpy.props.StringProperty(options={'SKIP_SAVE'})

    def execute(self, context):
        setattr(self.__class__.target, self.__class__.attribute, self.type)
        for area in context.screen.areas:
            area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        # UILayout.context_pointer_set()はinvokeの時は有効でもexecuteの時は
        # 無効になっていたのでその対策
        ls = self.data_path.split('.')
        self.__class__.target = eval('context.' + '.'.join(ls[:-1]))
        self.__class__.attribute = ls[-1]

        context.window_manager.invoke_search_popup(self)
        return {'INTERFACE'}


class EmulationKeyMapItem(bpy.types.PropertyGroup):
    bind_from = bpy.props.StringProperty(
        name='From',
    )
    bind_to = bpy.props.StringProperty(
        name='To',
    )


class EmulateKeyMapsPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    use_emulation_keymap = bpy.props.BoolProperty(
        name='Emulation Keymap',
        default=True
    )
    emulation_keymap = bpy.props.CollectionProperty(
        type=EmulationKeyMapItem)
    emulation_keymap_hold = bpy.props.StringProperty(
        name='Hold',
        description='Hold space key'
    )

    def _numpad_preset_update(self, context):
        prefs = EmulateKeyMapsPreferences.get_instance()
        prefs.emulation_keymap.clear()
        prefs.property_unset('emulation_keymap_hold')
        for bind_to, bind_from in numpad_preset[self.numpad_preset]:
            if bind_to == 'HOLD':
                prefs.emulation_keymap_hold = bind_from
                continue
            item = prefs.emulation_keymap.add()
            item.bind_from = bind_from
            item.bind_to = bind_to

    numpad_preset = bpy.props.EnumProperty(
        name='Numpad Preset',
        items=(('TYPE1', 'Type1', ''),
               ('TYPE2', 'Type2', ''),
               ('TYPE3', 'Type3', '')),
        update=_numpad_preset_update,
    )
    del _numpad_preset_update

    def _special_keymap_modifier_update(self, context):
        replace_keymap_items()

    use_special_keymap = bpy.props.BoolProperty(
        name='Special Keymap',
        update=_special_keymap_modifier_update,
    )

    special_keymap_modifier = bpy.props.EnumProperty(
        items=[('SHIFT', 'Shift + Space', 'Shift + Space'),
               ('CTRL', 'Ctrl + Space', 'Ctrl + Space')],
        default='SHIFT',
        update=_special_keymap_modifier_update,
    )
    del _special_keymap_modifier_update

    def draw(self, context):
        layout = self.layout
        layout.context_pointer_set('addon_prefs', self)

        # Emulation Key Map

        row = layout.row(align=True)
        row.prop(self, 'use_emulation_keymap', text='')
        row.label('Emulation Key Map:')
        box = layout.box()

        column = box.column()
        column.active = self.use_emulation_keymap

        sp = column.split(0.33)
        row = sp.row()
        row.prop(self, 'numpad_preset', text='Preset')
        row = sp.row()
        row = sp.row(align=True)
        # row.alignment = 'RIGHT'
        row.prop(self, 'emulation_keymap_hold', text='Hold')
        op = row.operator(WM_OT_event_type_search_popup.bl_idname, text='',
                          icon='VIEWZOOM')
        op.data_path = 'addon_prefs.emulation_keymap_hold'

        column.separator()

        for i, item in enumerate(self.emulation_keymap):
            row = column.row()
            row.context_pointer_set('prop', item)
            sub = row.row(align=True)
            sub.prop(item, 'bind_from', text='From')
            op = sub.operator(WM_OT_event_type_search_popup.bl_idname, text='',
                              icon='VIEWZOOM')
            op.data_path = 'prop.bind_from'

            sub = row.row(align=True)
            sub.prop(item, 'bind_to', text='To')
            op = sub.operator(WM_OT_event_type_search_popup.bl_idname, text='',
                              icon='VIEWZOOM')
            op.data_path = 'prop.bind_to'

            sub = row.row()
            sub.alignment = 'RIGHT'
            op = sub.operator(CollectionOperator.Remove.bl_idname, text='',
                              icon='X')
            op.data_path = 'addon_prefs.emulation_keymap'
            op.index = i
        row = column.row()
        row.row()
        sub = row.row()
        sub.alignment = 'RIGHT'
        op = sub.operator(CollectionOperator.Add.bl_idname, text='Add',
                          icon='ZOOMIN')
        op.data_path = 'addon_prefs.emulation_keymap'
        op = sub.operator(CollectionOperator.Clear.bl_idname, text='Clear')
        op.data_path = 'addon_prefs.emulation_keymap'

        self.layout.separator()

        # Special Key Maps

        row = layout.row(align=True)
        row.prop(self, 'use_special_keymap', text='')
        row.label('Special Key Map:')
        box = layout.box()

        column = box.column()
        column.active = self.use_special_keymap

        split = column.split(0.5)
        col = split.column()
        row = col.row()
        row.label('Key: ')
        row = col.row()
        row.prop(self, 'special_keymap_modifier', expand=True)
        if self.special_keymap_modifier == 'CTRL':
            if edited_keymap_items:
                column.label('Ctrl + Space -> Shift + Space', icon='ERROR')
            split = column.split(0.02)
            split.column()
            col = split.column()
            for km, kmi in edited_keymap_items:
                text = '* {}: {}'.format(km.name, kmi.name)
                if hasattr(kmi.properties, 'data_path'):
                    text += ": data_path='{}'".format(
                        kmi.properties.data_path)
                elif kmi.idname == 'wm.call_menu':
                    text += ": name='{}'".format(kmi.properties.name)
                col.label(text, translate=False)

            column.separator()

        split = column.split(0.5)
        col = split.column()
        col.label('Config File:')
        file_path = os.path.join(bpy.utils.user_resource('CONFIG'),
                                 CONFIG_FILE_NAME)
        column.label(file_path)
        split = column.split(0.25)
        col = split.column()
        text = 'Edit' if os.path.exists(file_path) else 'New'
        col.operator(SCREEN_OT_edit_keymap.bl_idname, text=text)

        self.layout.separator()

        super().draw(context)


###############################################################################
# Emulate Key Map
###############################################################################
"""
NOTE:
modalkeymapの場合はevent.typeがEVT_MODAL_MAPになる
wm_event_modalkeymap(), wm_event_modalmap_end()参照
event->prevtype = event->type;
event->prevval = event->val;
event->type = EVT_MODAL_MAP;
event->val = kmi->propvalue;
"""


# 未使用
def is_matched_keymap_item(context, event, kmi):
    if not kmi.active:
        return False

    if context.user_preferences.inputs.select_mouse == 'RIGHT':
        action_select = {
            'ACTIONMOUSE': 'LEFTMOUSE',
            'SELECTMOUSE': 'RIGHTMOUSE',
            'EVT_TWEAK_A': 'EVT_TWEAK_L',
            'EVT_TWEAK_S': 'EVT_TWEAK_R',
        }
    else:
        action_select = {
            'ACTIONMOUSE': 'RIGHTMOUSE',
            'SELECTMOUSE': 'LEFTMOUSE',
            'EVT_TWEAK_A': 'EVT_TWEAK_R',
            'EVT_TWEAK_S': 'EVT_TWEAK_L',
        }
    if context.user_preferences.inputs.invert_zoom_wheel:
        zoom_in_out = {
            'WHEELINMOUSE': 'WHEELDOWNMOUSE',
            'WHEELOUTMOUSE': 'WHEELUPMOUSE',
        }
    else:
        zoom_in_out = {
            'WHEELINMOUSE': 'WHEELUPMOUSE',
            'WHEELOUTMOUSE': 'WHEELDOWNMOUSE',
        }

    if kmi.type == event.type:
        match = True
    elif kmi.type in action_select:
        match = action_select[kmi.type] == event.type
    elif kmi.type in zoom_in_out:
        match = zoom_in_out[kmi.type] == event.type
    else:
        match = False

    if not match:
        return False

    if not (kmi.value == event.value or kmi.value == 'ANY'):
        return False

    if kmi.any:
        match = True
    else:
        mods = ['shift', 'ctrl', 'alt', 'oskey']
        match = all([getattr(kmi, m) == getattr(event, m) for m in mods])
    if match and kmi.key_modifier != 'NONE':
        # event.key_modifierに当たるものはpythonAPIでは提供されていない
        ev = st.wmEvent.cast(event)
        value = ev.keymodifier
        prop = bpy.types.KeyMapItem.bl_rna.properties['key_modifier']
        key_modifier = 'NONE'
        for enum_item in prop.enum_items:
            if enum_item.value == value:
                key_modifier = enum_item.identifier
                break
        if kmi.key_modifier != key_modifier:
            match = False

    return match


def find_event_keymap_items(context, event):
    keymap_items = []

    if context.user_preferences.inputs.select_mouse == 'RIGHT':
        action_select = {
            'ACTIONMOUSE': 'LEFTMOUSE',
            'SELECTMOUSE': 'RIGHTMOUSE',
            'EVT_TWEAK_A': 'EVT_TWEAK_L',
            'EVT_TWEAK_S': 'EVT_TWEAK_R',
        }
    else:
        action_select = {
            'ACTIONMOUSE': 'RIGHTMOUSE',
            'SELECTMOUSE': 'LEFTMOUSE',
            'EVT_TWEAK_A': 'EVT_TWEAK_R',
            'EVT_TWEAK_S': 'EVT_TWEAK_L',
        }
    if context.user_preferences.inputs.invert_zoom_wheel:
        zoom_in_out = {
            'WHEELINMOUSE': 'WHEELDOWNMOUSE',
            'WHEELOUTMOUSE': 'WHEELUPMOUSE',
        }
    else:
        zoom_in_out = {
            'WHEELINMOUSE': 'WHEELUPMOUSE',
            'WHEELOUTMOUSE': 'WHEELDOWNMOUSE',
        }

    keymaps = [km for km in listvalidkeys.context_keymaps(context, poll=True)]
    for km in keymaps:
        for kmi in km.keymap_items:
            if not kmi.active:
                continue
            if kmi.idname == SCREEN_OT_emulate_keymap.bl_idname:
                continue

            if kmi.type == event.type:
                match = True
            elif kmi.type in action_select:
                match = action_select[kmi.type] == event.type
            elif kmi.type in zoom_in_out:
                match = zoom_in_out[kmi.type] == event.type
            else:
                match = False
            if match:
                if kmi.value == event.value or kmi.value == 'ANY':
                    if kmi.any:
                        match = True
                    else:
                        mods = ['shift', 'ctrl', 'alt', 'oskey']
                        match = all([getattr(kmi, m) == getattr(event, m)
                                     for m in mods])
                    if kmi.key_modifier != 'NONE':
                        if kmi.key_modifier != event.key_modifier:
                            match = False
                    if match:
                        keymap_items.append(kmi)
    return keymap_items


def get_operator_from_keymap_item(kmi):
    kwargs = {}
    try:
        m, f = kmi.idname.split('.')
        type_name = m.upper() + '_OT_' + f
        if not hasattr(bpy.types, type_name):
            return None, kwargs

        op = getattr(getattr(bpy.ops, m), f)
        for attr in kmi.properties.keys():
            if kmi.properties.is_property_set(attr):
                # NOTE: enumの場合、kmi.properties[attr]とすると
                #       intが返ってくる
                kwargs[attr] = getattr(kmi.properties, attr)
        return op, kwargs
    except:
        traceback.print_exc()
        return None, kwargs


def operator_call(context, event):
    """イベントに一致するオペレーターを実行する。"""
    called = False
    pass_through = False
    running_modal = False
    interface = False

    for kmi in find_event_keymap_items(context, event):
        op, kwargs = get_operator_from_keymap_item(kmi)
        if not op:
            continue

        if op.poll():
            called = True
            try:
                r = op('INVOKE_DEFAULT', **kwargs)
            except:
                traceback.print_exc()
                return called, running_modal, False
            pass_through = 'PASS_THROUGH' in r
            if 'RUNNING_MODAL' in r:
                running_modal = True
            if 'INTERFACE' in r:
                interface = True
            if not pass_through:
                return called, running_modal, pass_through, interface

    return called, running_modal, pass_through, interface


def get_active_area_region(context, event):
    """マウスカーソル位置のAreaとRegionを取得する。
    :type context: bpy.types.Context
    :type event: bpy.types.Event
    :rtype: (bpy.types.Area, bpy.types.Region)
    """
    x, y = event.mouse_x, event.mouse_y
    for area in context.screen.areas:
        if area.x <= x < area.x + area.width:
            if area.y <= y < area.y + area.height:
                for region in area.regions:
                    if region.id == 0:
                        continue
                    if region.x <= x < region.x + region.width:
                        if region.y <= y < region.y + region.height:
                            return area, region
    return None, None


def set_active_area_region(context, area, region):
    """ContextのAreaとRegionを設定する。py_contextを無効化した状態で処理をする。
    返り値は変更前のAreaとRegion。これは bContext.wm.area,
    bContext.wm.region に当たるもの。
    :type context: bpy.types.Context
    :type area: bpy.types.Area
    :type region: bpy.types.Region
    :rtype: (bpy.types.Area, bpy.types.Region)
    """
    py_dict_bak = st.context_py_dict_set(context, None)
    area_bak = context.area  # bContext.wm.area
    region_bak = context.region  # bContext.wm.region

    st.bContext.wm_area_set(area)
    st.bContext.wm_region_set(region, calc_mouse=True)

    st.context_py_dict_set(context, py_dict_bak)
    return area_bak, region_bak


class SCREEN_OT_emulate_keymap(bpy.types.Operator):
    bl_idname = 'screen.emulate_keymap'
    bl_label = 'Emulate Key Map'

    @classmethod
    def poll(self, context):
        prefs = EmulateKeyMapsPreferences.get_instance()
        return context.area and prefs.use_emulation_keymap

    def __init__(self):
        self.event_type = ''
        self.hold = False
        self.terminate = False
        self.header_text = ''

    def modal(self, context, event):
        prefs = EmulateKeyMapsPreferences.get_instance()
        ret = {'RUNNING_MODAL'}

        if self.terminate:
            ret = {'FINISHED'}
        elif event.type == self.event_type and event.value == 'RELEASE':
            if not self.hold:
                ret = {'FINISHED'}
        elif event.type == 'ESC':
            ret = {'FINISHED'}
        # elif event.type == 'RIGHTMOUSE':
        #     ret = {'FINISHED'}
        elif event.type in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'}:
            ret = {'PASS_THROUGH'}

        if (event.type == prefs.emulation_keymap_hold and
                event.value == 'PRESS'):
            self.hold ^= True

        # area, regionと有効なキーマップの更新
        area, region = get_active_area_region(context, event)
        set_active_area_region(context, area, region)

        match = False
        if event.value == 'PRESS':
            for item in prefs.emulation_keymap:
                if item.bind_from == event.type:
                    match = True
                    break

        if match:
            # eventのコピーと値の修正
            event_ = types.SimpleNamespace()
            for attr in dir(event):
                setattr(event_, attr, getattr(event, attr))
            # event.key_modifierに当たるものはpythonAPIでは提供されていない
            ev = st.wmEvent.cast(event)
            value = ev.keymodifier
            prop = bpy.types.KeyMapItem.bl_rna.properties['key_modifier']
            for enum_item in prop.enum_items:
                if enum_item.value == value:
                    event_.key_modifier = enum_item.identifier
                    break
            else:
                event_.key_modifier = 'NONE'
            event_.type = item.bind_to

            called, running_modal, _pass_through, is_interface = \
                operator_call(context, event_)
            if called:
                context.area.tag_redraw()
            if running_modal:
                self.terminate = True
            elif self.hold:
                ret = {'FINISHED'}
            elif is_interface:
                ret = {'FINISHED'}

            self.header_text = '{} -> {}'.format(event.type, event_.type)

        info_area = self.get_info_area(context)
        if info_area:
            if {'FINISHED', 'CANCELLED'} & ret:
                info_area.header_text_set()
                info_area.tag_redraw()
            else:
                self.redraw_info(context)
        return ret

    def get_info_area(self, context):
        for area in context.screen.areas:
            if area.type == 'INFO':
                return area

    def redraw_info(self, context):
        area = self.get_info_area(context)
        if area:
            if self.hold:
                text = 'Emulate Key Map: (Hold)' + self.header_text
            else:
                text = 'Emulate Key Map: ' + self.header_text
            area.header_text_set(text)
            area.tag_redraw()

    def invoke(self, context, event):
        # CONSOLEとTEXT_EDITOR,VIEW_3DのTEXT_EDITモードでは
        # Spaceキーのみでの呼び出しは無視する。
        if event.type == 'SPACE':
            if (not event.shift and not event.ctrl and not event.alt and
                    not event.oskey):
                if (context.area.type in {'CONSOLE', 'TEXT_EDITOR'} or
                        context.area.type == 'VIEW_3D' and
                        context.mode == 'EDIT_TEXT'):
                    return {'CANCELLED', 'PASS_THROUGH'}

        self.event_type = event.type
        context.window_manager.modal_handler_add(self)
        self.redraw_info(context)

        return {'RUNNING_MODAL'}


###############################################################################
# Special Key Map
###############################################################################
class SCREEN_OT_edit_keymap(bpy.types.Operator):
    bl_idname = 'screen.edit_keymap'
    bl_label = 'Edit Key Map'
    bl_description = 'Open config file'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        file_path = os.path.join(bpy.utils.user_resource('CONFIG'),
                                 CONFIG_FILE_NAME)

        for text in bpy.data.texts:
            if text.filepath == file_path:
                break
        else:
            exist = False
            try:
                with open(file_path, 'r', encoding='utf-8'):
                    exist = True
            except:
                pass
            try:
                with open(file_path, 'a', encoding='utf-8') as f:
                    if not exist:
                        f.write(get_template())
            except:
                traceback.print_exc()
                return {'CANCELLED'}
            text = bpy.data.texts.load(file_path)

        self.report({'INFO'}, "See '{}' in the text editor".format(CONFIG_FILE_NAME))

        # write template
        # if not text.as_string().strip():
        #     text.clear()
        #     text.write(get_template())

        return {'FINISHED'}


def event_to_srting(event):
    if isinstance(event, bpy.types.Event):
        event_type = event.type
        mods = event.shift, event.ctrl, event.alt, event.oskey
    else:
        event_type, mods = event

    enum_items = bpy.types.Event.bl_rna.properties['type'].enum_items
    names = {e.identifier: e.name for e in enum_items}

    keys = []
    for name, enable in zip(['Shift', 'Ctrl', 'Alt', 'OSKey'], mods):
        if enable:
            keys.append(name)
    keys.append(names[event_type])
    return ' + '.join(keys)


class SCREEN_OT_special_keymap(bpy.types.Operator):
    bl_idname = 'screen.special_keymap'
    bl_label = 'Special Key Map'
    bl_options = {'REGISTER'}

    operators = {}

    @classmethod
    def poll(self, context):
        prefs = EmulateKeyMapsPreferences.get_instance()
        return prefs.use_special_keymap

    @classmethod
    def kill(cls):
        for op in cls.operators.values():
            op.terminate = True
        cls.operators.clear()

    # @classmethod
    # def register(cls):
    #     pass

    @classmethod
    def unregister(cls):
        cls.operators.clear()

    def __init__(self):
        self.op_key = ('NONE', (False,) * 4)  # 起動時のショートカット
        self.config = None
        self.key_history = []
        self.terminate = False

    def cancel(self, context):
        win_key = bpy.context.window.as_pointer()
        if win_key in self.operators:
            del self.operators[win_key]
        self.redraw_info(context)

    def redraw_info(self, context):
        for area in context.screen.areas:
            if area.type == 'INFO':
                break
        else:
            return

        win_key = context.window.as_pointer()
        if win_key not in SCREEN_OT_special_keymap.operators:
            area.header_text_set()
            area.tag_redraw()
            return

        # enum_items = bpy.types.Event.bl_rna.properties['type'].enum_items
        # event_type_names = {elem.identifier: elem.name for elem in
        #                     enum_items}

        op = SCREEN_OT_special_keymap.operators[win_key]
        text_list = []
        for event_type, modifiers in op.key_history:
            keys = []
            for i, name in enumerate(['shift', 'ctrl', 'alt', 'oskey']):
                if modifiers[i]:
                    keys.append(name)
            # keys.append(event_type_names[event_type])
            keys.append(event_type)
            text_list.append(' + '.join(keys))
        text = ', '.join(text_list)
        area.header_text_set('>>> ' + text)
        area.tag_redraw()

    def format_event(self, event):
        modifiers = [False] * 4
        for i, attr in enumerate(['shift', 'ctrl', 'alt', 'oskey']):
            if getattr(event, attr):
                modifiers[i] = True
        return [event.type, modifiers]

    def modal(self, context, event):
        win_key = bpy.context.window.as_pointer()

        if self.terminate or win_key not in self.operators:
            self.cancel(context)
            return {'FINISHED'}

        if event.type in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'}:
            return {'PASS_THROUGH'}

        if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT', 'LEFT_CTRL',
                          'RIGHT_CTRL', 'LEFT_ALT', 'RIGHT_ALT',
                          'OSKEY'}:
            return {'RUNNING_MODAL'}
        if event.value != 'PRESS':
            return {'RUNNING_MODAL'}

        current_key = self.format_event(event)

        # 起動時と同じキーを押したら終了
        if current_key == self.op_key:
            self.cancel(context)

        if event.type == 'BACK_SPACE' and event.value == 'PRESS':
            self.key_history[-1:] = []
        else:
            self.key_history.append(current_key)

        self.redraw_info(context)

        area, region = get_active_area_region(context, event)
        set_active_area_region(context, area, region)

        def is_matched(history, keys, options):
            import itertools

            if history == keys:
                return True

            only_last = False
            if options and len(options) == 2:
                only_last = options[1]
            if only_last:
                history = history[-1:]

            for hist, op_key in itertools.zip_longest(
                    history, keys, fillvalue=None):
                if hist is None:
                    return False
                elif op_key[0] != hist[0]:
                    return False
                elif op_key[1] is None:  # 'any'
                    continue
                elif op_key[1] != hist[1]:
                    return False
            return True

        items = []
        if '*' in self.config:
            items.extend(self.config['*'])
        for km in listvalidkeys.context_keymaps(context, poll=True):
            if km.name in self.config:
                items.extend(self.config[km.name])

        result = None
        is_running_modal = False
        is_interface = False
        for key, idname, *options in items:
            if not is_matched(self.key_history, key, options):
                continue
            mod, func = idname.split('.')
            op = getattr(getattr(bpy.ops, mod), func)
            if op.poll():
                if options:
                    kwargs = options[0]
                    result = op('INVOKE_DEFAULT', **kwargs)
                else:
                    result = op('INVOKE_DEFAULT')
                is_running_modal = 'RUNNING_MODAL' in result
                is_interface = 'INTERFACE' in result
                if 'PASS_THROUGH' not in result:
                    break

        if is_running_modal:
            # GRAB_CURSORを切らせない為に、呼び出したmodalオペレーターが
            # 終了するまで待つ
            self.terminate = True
            self.cancel(context)
            return {'RUNNING_MODAL'}
        elif result or self.terminate or win_key not in self.operators:
            self.cancel(context)
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def get_config(self):
        file_path = os.path.join(bpy.utils.user_resource('CONFIG'),
                                 CONFIG_FILE_NAME)
        found = True
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except:
            found = False
            # traceback.print_exc()

        config = None
        if found:
            mod = types.ModuleType('tmp')
            error = False
            try:
                exec(text, mod.__dict__)
            except:
                traceback.print_exc()
                error = True
            if not error and 'keymaps' in mod.__dict__:
                if isinstance(mod.keymaps, dict):
                    config = mod.keymaps

        if not config:
            mod = types.ModuleType('tmp')
            text = get_template()
            exec(text, mod.__dict__)
            config = mod.keymaps

        # 書式を揃える
        for name in list(config.keys()):
            config[name] = [list(item) for item in config[name]]
        for items in config.values():
            for item in items:
                keys = item[0]
                key_elems = []
                for s in keys.strip().split(','):
                    ls = [t.strip() for t in s.strip().split('+')]
                    modifiers = [t.lower() for t in ls[:-1]]
                    if 'any' in modifiers:
                        modifiers_ = None
                    else:
                        modifiers_ = [False] * 4
                        for i, m in enumerate(
                                ['shift', 'ctrl', 'alt', 'oskey']):
                            if m in modifiers:
                                modifiers_[i] = True
                    key_elems.append([ls[-1].upper(), modifiers_])
                item[0] = key_elems

        return config

    def invoke(self, context, event):
        prefs = EmulateKeyMapsPreferences.get_instance()
        if prefs.special_keymap_modifier == 'SHIFT':
            if event.ctrl:
                return {'CANCELLED', 'PASS_THROUGH'}
        else:
            if event.shift:
                return {'CANCELLED', 'PASS_THROUGH'}

        if context.area.type in {'CONSOLE', 'TEXT_EDITOR'}:
            op_key = self.format_event(event)
            if op_key == ['SPACE', [False, False, False, False]]:
                return {'CANCELLED', 'PASS_THROUGH'}

        wm = context.window_manager
        win_key = context.window.as_pointer()
        if win_key in self.operators:
            self.cancel(context)
            return {'FINISHED'}
        else:
            self.operators[win_key] = self
            mod = event.shift, event.ctrl, event.alt, event.oskey
            self.op_key = self.format_event(event)
            self.config = self.get_config()
            wm.modal_handler_add(self)
            self.redraw_info(context)
            return {'RUNNING_MODAL'}


disabled_keymap_items = []
edited_keymap_items = []


def replace_keymap_items():
    """special_keymap_modifierが'CTRL'の場合に、衝突する他の
    KeyMapItem(activeとaddon)を変更する。
    shift + space -> disable  (フルスクリーンのショートカットを無効化)
    ctrl + space -> shift + space
    """

    prefs = EmulateKeyMapsPreferences.get_instance()

    restore_replaced_keymap_items()

    if not prefs.use_special_keymap:
        return

    keyconfigs = bpy.context.window_manager.keyconfigs
    for kc in [keyconfigs.active, keyconfigs.addon]:
        if not kc or prefs.special_keymap_modifier == 'SHIFT':
            continue
        for km in kc.keymaps:
            if km.is_modal:
                continue
            for kmi in km.keymap_items:
                if kmi.idname == SCREEN_OT_special_keymap.bl_idname:
                    continue
                if kmi.type == 'SPACE' and kmi.value == 'PRESS':
                    mod = kmi.any, kmi.shift, kmi.ctrl, kmi.alt, kmi.oskey
                    if mod == (False, True, False, False, False):
                        if kmi.active:
                            kmi.active = False
                            disabled_keymap_items.append((km, kmi))
                    elif mod == (False, False, True, False, False):
                        kmi.shift = True
                        kmi.ctrl = False
                        edited_keymap_items.append((km, kmi))


def restore_replaced_keymap_items():
    for km, kmi in disabled_keymap_items:
        kmi.active = True
    disabled_keymap_items.clear()
    for km, kmi in edited_keymap_items:
        kmi.shift = False
        kmi.ctrl = True
    edited_keymap_items.clear()


@bpy.app.handlers.persistent
def scene_update_pre(scene):
    replace_keymap_items()
    bpy.app.handlers.scene_update_pre.remove(scene_update_pre)


###############################################################################
# Register
###############################################################################
classes = [
    CollectionOperator,
    WM_OT_event_type_search_popup,

    EmulationKeyMapItem,
    SCREEN_OT_emulate_keymap,

    SCREEN_OT_special_keymap,
    SCREEN_OT_edit_keymap,

    EmulateKeyMapsPreferences,
]


@EmulateKeyMapsPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    km = EmulateKeyMapsPreferences.get_keymap('Screen Editing')
    if km:
        km.keymap_items.new(SCREEN_OT_special_keymap.bl_idname,
                            'SPACE', 'PRESS', shift=True)
        km.keymap_items.new(SCREEN_OT_special_keymap.bl_idname,
                            'SPACE', 'PRESS', ctrl=True)

        km.keymap_items.new(SCREEN_OT_emulate_keymap.bl_idname,
                            'SPACE', 'PRESS')

    bpy.app.handlers.scene_update_pre.append(scene_update_pre)


@EmulateKeyMapsPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    if scene_update_pre in bpy.app.handlers.scene_update_pre:
        bpy.app.handlers.scene_update_pre.remove(scene_update_pre)

    restore_replaced_keymap_items()


if __name__ == '__main__':
    register()
