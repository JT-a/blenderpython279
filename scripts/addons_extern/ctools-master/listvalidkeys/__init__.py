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
    'name': 'List Valid Keys',
    'author': 'chromoly',
    'version': (0, 1, 3),
    'blender': (2, 78, 0),
    'location': 'Screen -> Shift + Ctrl + Alt + \\',
    'description': 'Print valid shortcut',
    'warning': '',
    'wiki_url': '',
    'category': 'User Interface'
}


from collections import OrderedDict
import ctypes as ct
import importlib

import bpy

try:
    importlib.reload(addongroup)
    importlib.reload(structures)
except NameError:
    from ..utils import addongroup
    from ..utils import structures


TEXT_NAME = 'valid_shortcuts.txt'


class ListValidKeysPreferences(
    addongroup.AddonGroup,
    bpy.types.PropertyGroup if '.' in __name__ else
    bpy.types.AddonPreferences):
    bl_idname = __name__

    output = bpy.props.EnumProperty(
        name='Output',
        items=[('STDOUT', 'StdOut', ''),
               ('TEXT', 'Text',
                "See '{}' in the text editor".format(TEXT_NAME))],
        default='STDOUT',
    )

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        split = column.split()
        col = split.column()
        col.prop(self, 'output')
        split.column()
        split.column()

        self.layout.separator()
        super().draw(context)


class wmKeyMap(ct.Structure):
    _fields_ = [
        ('next', ct.c_void_p),
        ('prev', ct.c_void_p),
        ('items', structures.ListBase),
        ('diff_items', structures.ListBase),
        ('idname', ct.c_char * 64),
        ('spaceid', ct.c_short),
        ('regienid', ct.c_short),
        ('flag', ct.c_short),
        ('kmi_id', ct.c_short),
        ('poll', ct.CFUNCTYPE(ct.c_int, ct.c_void_p)),  # arg = bContext
        ('modal_items', ct.c_void_p),
    ]


def _handler_keymaps(kc, handlers):
    if not handlers.first:
        return []

    keymaps = []
    handler_ptr = structures.wmEventHandler.cast(handlers.first,
                                                 contents=False)
    while handler_ptr:
        handler = handler_ptr.contents
        if ord(handler.flag) & structures.WM_HANDLER_DO_FREE:
            pass
        else:
            if handler.keymap:
                if handler.keymap:
                    km = ct.cast(ct.c_void_p(handler.keymap),
                                 ct.POINTER(wmKeyMap)).contents
                    name = km.idname.decode()
                    keymap = kc.keymaps.get(name)
                    if keymap:
                        keymaps.append(keymap.active())
                    else:
                        # ミス
                        raise ValueError()
        handler_ptr = handler.next
    return keymaps


def _window_modal_keymaps(kc, window):
    if not window:
        return []
    win = structures.wmWindow.cast(window)
    return _handler_keymaps(kc, win.modalhandlers)


def _region_keymaps(kc, region):
    if not region:
        return []
    ar = structures.ARegion.cast(region)
    return _handler_keymaps(kc, ar.handlers)


def _area_keymaps(kc, area):
    if not area:
        return []
    sa = structures.ScrArea.cast(area)
    return _handler_keymaps(kc, sa.handlers)


def _window_keymaps(kc, window):
    if not window:
        return []
    win = structures.wmWindow.cast(window)
    return _handler_keymaps(kc, win.handlers)


def keymap_poll(context, keymap):
    C = ct.c_void_p(context.as_pointer())
    km_ptr = ct.cast(ct.c_void_p(keymap.as_pointer()), ct.POINTER(wmKeyMap))
    km = km_ptr.contents
    return not km.poll or km.poll(C)


def context_keymaps(context, keymap_type='USER', regions=None, poll=False):
    wm = context.window_manager
    kc = getattr(wm.keyconfigs, keymap_type.lower())

    keymap_list = []
    # 'Screen Editing'
    keymap_list.extend(_window_modal_keymaps(kc, context.window))
    # region
    if regions is None:
        regions = [context.region]
    for region in regions:
        keymap_list.extend(_region_keymaps(kc, region))
    # area (大抵は空)
    keymap_list.extend(_area_keymaps(kc, context.area))
    # 'Window', 'Screen'
    keymap_list.extend(_window_keymaps(kc, context.window))

    keymap_list = sorted(set(keymap_list), key=keymap_list.index)

    if poll:
        keymap_list = [km for km in keymap_list if keymap_poll(context, km)]

    return keymap_list


class WM_OT_list_valid_keys(bpy.types.Operator):
    bl_idname = 'wm.list_valid_keys'
    bl_label = 'List Valid Keys'
    bl_description = 'See Console(Command prompt)'

    keymap_type = bpy.props.EnumProperty(
        name='KeyMap Type',
        items=(('DEFAULT', 'Default', ''),
               ('ADDON', 'Addon', ''),
               # ('USER_MOD', 'User Modified', ''),
               ('USER', 'User', 'Final keymaps')),
        default='USER',
        options={'SKIP_SAVE'}
    )
    use_all = bpy.props.BoolProperty(
        name='All',
        description='Ignore priority. Not include modal keymaps',
        options={'SKIP_SAVE'}
    )

    use_window = bpy.props.BoolProperty(
        name='Window', options={'SKIP_SAVE'})
    use_header = bpy.props.BoolProperty(
        name='Header', options={'SKIP_SAVE'})
    use_channels = bpy.props.BoolProperty(
        name='Channels', options={'SKIP_SAVE'})
    use_temporary = bpy.props.BoolProperty(
        name='Temporary', options={'SKIP_SAVE'})
    use_ui = bpy.props.BoolProperty(
        name='UI', options={'SKIP_SAVE'})
    use_tools = bpy.props.BoolProperty(
        name='Tools', options={'SKIP_SAVE'})
    use_tool_props = bpy.props.BoolProperty(
        name='Tool Properties', options={'SKIP_SAVE'})
    use_preview = bpy.props.BoolProperty(
        name='Preview', options={'SKIP_SAVE'})
    # keymap_poll()の結果が偽の物も含める
    include_invalid_keymaps = bpy.props.BoolProperty(
        name='Include Invalid Key Maps',
        options={'SKIP_SAVE'}
    )

    def __init__(self):
        context = bpy.context
        self.area = context.area
        self.region = context.region

    def check(self, context):
        return True

    @staticmethod
    def sorted_region_types(region_types):
        prop = bpy.types.Region.bl_rna.properties['type']
        identifiers = [e.identifier for e in prop.enum_items]
        return sorted(region_types, key=identifiers.index)

    @staticmethod
    def enum_item_identifer_to_name(type, prop, identifier):
        prop = type.bl_rna.properties[prop]
        for e in prop.enum_items:
            if e.identifier == identifier:
                return e.name
        raise ValueError()

    def draw(self, context):
        area = self.area
        region = self.region

        layout = self.layout

        layout.prop(self, 'keymap_type', text='KeyMap')
        layout.prop(self, 'use_all')

        column = layout.column()
        if self.use_all:
            column.active = False
            column.label('')
        else:
            area_name = self.enum_item_identifer_to_name(
                bpy.types.Area, 'type', area.type)
            region_name = self.enum_item_identifer_to_name(
                bpy.types.Region, 'type', region.type)
            column.label('{} - {}'.format(area_name, region_name))
        area_region_types = set(r.type for r in area.regions)
        area_region_types = self.sorted_region_types(area_region_types)
        visible_region_types = set(r.type for r in area.regions
                           if r.id != 0)
        flow = column.column_flow(2)
        for region_type in area_region_types:
            col = flow.column()
            col.active = region_type in visible_region_types
            col.prop(self, 'use_' + region_type.lower(), toggle=True)
        column.prop(self, 'include_invalid_keymaps')

    def execute(self, context):
        output = []

        wm = context.window_manager
        kc = getattr(wm.keyconfigs, self.keymap_type.lower())

        if self.use_all:
            output.append('Key Maps')
            keymap_list = []
            for km in kc.keymaps:
                if not km.is_modal:
                    keymap_list.append(km)
        else:
            area_region_types = set(r.type for r in context.area.regions)
            region_types = []
            for attr in dir(self):
                if attr.startswith('use_'):
                    region_type = attr.replace('use_', '').upper()
                    if region_type in area_region_types:
                        if getattr(self, attr):
                            region_types.append(region_type)
            region_types = self.sorted_region_types(region_types)
            region_types_name = [
                self.enum_item_identifer_to_name(bpy.types.Region, 'type', rt)
                for rt in region_types]

            area = context.area
            # region = context.region
            if len(region_types) == 1:
                rt = region_types_name[0]
            elif len(region_types_name) > 1:
                rt = '[{}]'.format(', '.join(region_types_name))
            else:
                rt = 'NONE'
            area_name = self.enum_item_identifer_to_name(
                bpy.types.Area, 'type', area.type)
            output.append('<{} - {}> Key Maps'.format(area_name, rt))

            regions = [r for r in area.regions if r.type in region_types]
            keymap_list = context_keymaps(context, self.keymap_type, regions)

        keymap_list_valid = []
        keymap_items = []
        kmi_km = {}
        km_name_max = kmi_name_max = 0
        for km in keymap_list:
            if not self.use_all and not self.include_invalid_keymaps:
                if not keymap_poll(context, km):
                    output.append('    {}  ...fail'.format(km.name))
                    continue
            keymap_list_valid.append(km)
            output.append('    {}'.format(km.name))
            km_name_max = max(km_name_max, len(km.name))
            for kmi in km.keymap_items:
                if kmi.active:
                    kmi_name_max = max(kmi_name_max, len(kmi.name))
                    keymap_items.append(kmi)
                    kmi_km[kmi] = km
        output.append('')

        type_prop = bpy.types.Event.bl_rna.properties['type']
        type_items = OrderedDict(
            [(e.identifier, e.name)
             for e in type_prop.enum_items])
        type_keys = list(type_items.keys())

        value_prop = bpy.types.Event.bl_rna.properties['value']
        value_items = OrderedDict(
            [(e.identifier, e.name)
             for e in value_prop.enum_items])
        value_max = 0
        for kmi in keymap_items:
            value_max = max(len(value_items[kmi.value]), value_max)

        select_mouse = context.user_preferences.inputs.select_mouse
        if select_mouse == 'RIGHT':
            d = {'ACTIONMOUSE': 'LEFTMOUSE',
                 'SELECTMOUSE': 'RIGHTMOUSE',
                 'EVT_TWEAK_A': 'EVT_TWEAK_L',
                 'EVT_TWEAK_S': 'EVT_TWEAK_R',
                 }
        else:
            d = {'ACTIONMOUSE': 'RIGHTMOUSE',
                 'SELECTMOUSE': 'LEFTMOUSE',
                 'EVT_TWEAK_A': 'EVT_TWEAK_R',
                 'EVT_TWEAK_S': 'EVT_TWEAK_L',
                 }
        if context.user_preferences.inputs.invert_zoom_wheel:
            d['WHEELINMOUSE'] = 'WHEELDOWNMOUSE'
            d['WHEELOUTMOUSE'] = 'WHEELUPMOUSE'
        else:
            d['WHEELINMOUSE'] = 'WHEELUPMOUSE'
            d['WHEELOUTMOUSE'] = 'WHEELDOWNMOUSE'

        d_reversed = {v: k for k, v in d.items()}

        keymap_items_grouped = {}
        for kmi in keymap_items:
            kmi_type = d.get(kmi.type, kmi.type)
            keymap_items_grouped.setdefault(kmi_type, []).append(kmi)
        keymap_items_grouped = OrderedDict(
            [(kmi_type, keymap_items_grouped[kmi_type])
             for kmi_type in sorted(keymap_items_grouped, key=type_keys.index)]
        )

        for kmi_type, items in keymap_items_grouped.items():
            if kmi_type == 'NONE' or kmi_type.startswith('TIMER'):
                continue

            t = type_items[kmi_type]
            if kmi_type in d_reversed:
                t += ' ({})'.format(type_items[d_reversed[kmi_type]])
            output.append('{}'.format(t))

            for kmi in items:
                mod = '*' if kmi.any else ' '
                mod += 'S' if kmi.shift else '-'
                mod += 'C' if kmi.ctrl else '-'
                mod += 'A' if kmi.alt else '-'
                mod += 'O' if kmi.oskey else '-'
                if kmi.key_modifier != 'NONE':
                    mod += '[{}]'.format(type_items[kmi.key_modifier])
                else:
                    mod += '   '
                # TODO: key_modifierが一文字でないとインデントが崩れる
                txt = '    {} {:{}}  {:{}}  {:{}}  {}'.format(
                    mod,
                    value_items[kmi.value],
                    value_max,
                    "'" + kmi.name + "'",
                    kmi_name_max + 2,
                    '(' + kmi_km[kmi].name + ')',
                    kmi_name_max + 2,
                    'U' if kmi.is_user_defined or kmi.is_user_modified else ''
                )
                output.append(txt.rstrip())
        output.append('')

        output.append('Unused:')
        for kmi_type in type_keys:
            kmi_type = d.get(kmi_type, kmi_type)
            if kmi_type == 'NONE' or kmi_type.startswith('TIMER'):
                continue
            if kmi_type in {'MOUSEMOVE',
                            'INBETWEEN_MOUSEMOVE',
                            # 'PEN',
                            # 'ERASER',
                            'LEFT_CTRL',
                            'RIGHT_CTRL',
                            'LEFT_SHIFT',
                            'RIGHT_SHIFT',
                            'LEFT_ALT',
                            'RIGHT_ALT',
                            'OSKEY',
                            'GRLESS',
                            'LINE_FEED',
                            'TEXTINPUT',
                            'WINDOW_DEACTIVATE',
                            }:
                continue
            # if kmi_type.startswith('NDOF'):
            #     continue
            if kmi_type not in keymap_items_grouped:
                output.append('    {}'.format(type_items[kmi_type]))

        output.append('')

        addon_prefs = ListValidKeysPreferences.get_instance()
        if addon_prefs.output == 'STDOUT':
            print('\n'.join(output))
        else:
            text = bpy.data.texts.get(TEXT_NAME)
            if not text:
                text = bpy.data.texts.new(TEXT_NAME)
            text.clear()
            text.write('\n'.join(output))
            self.report({'INFO'},
                        "See '{}' in the text editor".format(TEXT_NAME))
        return {'FINISHED'}

    def invoke(self, context, event):
        prop = bpy.types.Region.bl_rna.properties['type']
        is_property_set = False
        for e in prop.enum_items:
            attr = 'use_' + e.identifier.lower()
            if self.properties.is_property_set(attr):
                is_property_set = True
                break
        if not is_property_set:
            setattr(self, 'use_' + context.region.type.lower(), True)

        return context.window_manager.invoke_props_dialog(self)


classes = [
    ListValidKeysPreferences,
    WM_OT_list_valid_keys,
]


@ListValidKeysPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = ListValidKeysPreferences.get_keymap('Screen Editing')
        kmi = km.keymap_items.new(
            WM_OT_list_valid_keys.bl_idname,
            'BACK_SLASH', 'PRESS', shift=True, ctrl=True, alt=True)


@ListValidKeysPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


# 途中で出たゴミ ------------------------------------------------
# # structure.pyを使うほどではないのでコピペ
# class ListBase(ct.Structure):
#     _fields_ = [
#         ('first', ct.c_void_p),
#         ('last', ct.c_void_p),
#     ]

# def _region_keyamps(area, region):
#     if not area or not region:
#         return []
#
#     at = area.type
#     rt = region.type
#     if at == 'CONSOLE':
#         if rt == 'WINDOW':
#             return ('View2D',
#                     'Console')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Header')
#     elif at == 'FILE_BROWSER':
#         if rt == 'WINDOW':
#             return ('View2D',
#                     'File Browser',
#                     'File Browser Main')
#         elif rt == 'TOOLS':
#             return ('View2D Buttons List',
#                     'File Browser')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Header',
#                     'File Browser')
#     elif at == 'INFO':
#         if rt == 'WINDOW':
#             return ('View2D',
#                     'Frames',
#                     'Info')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'USER_PREFERENCES':
#         if rt == 'WINDOW':
#             return 'View2D Buttons List'
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Header')
#     elif at == 'OUTLINER':
#         if rt == 'WINDOW':
#             return ('View2D',
#                     'Frames',
#                     'Outliner')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'PROPERTIES':
#         if rt == 'WINDOW':
#             return ('Frames',
#                     'View2D Buttons List',
#                     'Property Editor')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'LOGIC_EDITOR':
#         if rt == 'WINDOW':
#             return ('View2DFrames',
#                     'Logic Editor')
#         elif rt == 'UI':
#             return ('Frames',
#                     'View2D Buttons List',
#                     'Logic Editor')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'NODE_EDITOR':
#         if rt == 'WINDOW':
#             return ('View2D',
#                     'Frames',
#                     'Grease Pencil',
#                     'Grease Pencil Stroke Edit Mode',
#                     'Node Generic',
#                     'Node Editor')
#         elif rt == 'UI':
#             return ('Frames',
#                     'View2D Buttons List',
#                     'Node Generic')
#         elif rt == 'TOOLS':
#             return ('Frames',
#                     'View2D Buttons List',
#                     'Node Generic')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'TEXT_EDITOR':
#         if rt == 'WINDOW':
#             return ('Text Generic',
#                     'Text')
#         elif rt == 'UI':
#             return ('View2D Buttons List',
#                     'Text Generic')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Header')
#     elif at == 'CLIP_EDITOR':
#         if rt == 'WINDOW':
#             return ('Frames',
#                     'Grease Pencil',
#                     'Grease Pencil Stroke Edit Mode',
#                     'Mask Editing',
#                     'Clip',
#                     'Clip Editor')
#         elif rt == 'PREVIEW':  # graph,dopeの右側
#             return ('View2D',
#                     'Frames',
#                     'Clip',
#                     'Clip Graph Editor',
#                     'Clip Dopesheet Editor')
#         elif rt == 'CHANNELS':  # graph,dopeの左側
#             return ('Frames',
#                     'Clip Dopesheet Editor')
#         elif rt == 'UI':
#             return ('Frames',
#                     'View2D Buttons List',
#                     'Clip')
#         elif rt == 'TOOLS':
#             return ('Frames',
#                     'View2D Buttons List',
#                     'Clip')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'SEQUENCE_EDITOR':
#         if rt == 'WINDOW':
#             return ('View2D',
#                     'Animation',
#                     'Frames',
#                     'SequencerCommon',
#                     'Sequencer')
#         elif rt == 'PREVIEW':
#             return ('View2D',
#                     'Frames',
#                     'Grease Pencil',
#                     'Grease Pencil Stroke Edit Mode',
#                     'SequencerCommon',
#                     'SequencerPreview')
#         elif rt == 'UI':
#             return ('Frames',
#                     'SequencerCommon',
#                     'View2D Buttons List')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'IMAGE_EDITOR':
#         if rt == 'WINDOW':
#             return ('Frames',
#                     'Grease Pencil',
#                     'Grease Pencil Stroke Edit Mode',
#                     'Mask Editing',
#                     'Curve',
#                     'Paint Curve',
#                     'Image Paint',
#                     'UV Editor',
#                     'UV Sculpt',
#                     'Image Generic',
#                     'Image')
#         elif rt == 'UI':
#             return ('Frames',
#                     'View2D Buttons List',
#                     'Image Generic')
#         elif rt == 'TOOLS':
#             return ('Frames',
#                     'View2D Buttons List',
#                     'Image Generic')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'NLA_EDITOR':
#         if rt == 'WINDOW':
#             return ('View2D',
#                     'Animation',
#                     'Frames',
#                     'NLA Editor',
#                     'NLA Generic')
#         elif rt == 'CHANNELS':
#             return ('View2D',
#                     'Frames',
#                     'NLA Channels',
#                     'Animation Channels',
#                     'NLA Generic')
#         elif rt == 'UI':
#             return ('View2D Buttons List',
#                     'NLA Generic')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header')
#     elif at == 'VIEW_3D':
#         if rt == 'WINDOW':
#             return ('Grease Pencil',
#                     'Grease Pencil Stroke Edit Mode',
#                     'Face Mask',
#                     'Weight Paint Vertex Selection',
#                     'Pose',
#                     'Object Mode',
#                     'Paint Curve',
#                     'Curve',
#                     'Image Paint',
#                     'Vertex Paint',
#                     'Weight Paint',
#                     'Sculpt',
#                     'Mesh',
#                     'Armature',
#                     'Metaball',
#                     'Lattice',
#                     'Particle',
#                     'Font',
#                     'Object Non-modal',
#                     'Frames',
#                     '3D View Generic',
#                     '3D View')
#         elif rt == 'UI':
#             return ('Frames',
#                     'View2D Buttons List',
#                     '3D View Generic')
#         elif rt == 'TOOLS':
#             return ('Frames',
#                     'View2D Buttons List',
#                     '3D View Generic')
#         elif rt == 'TOOL_PROPS':
#             return ('Frames',
#                     'View2D Buttons List',
#                     '3D View Generic')
#         elif rt == 'HEADER':
#             return ('View2D',
#                     'Frames',
#                     'Header',
#                     '3D View Generic')
#
#     # ミス
#     raise ValueError('{}: {}'.format(at, rt))

# space_flags = {
#     'VIEW_3D':
#         {'WINDOW':
#              [{'ED_KEYMAP_GPENCIL'},
#               ['Face Mask',
#                'Weight Paint Vertex Selection',
#                'Pose',
#                'Object Mode',
#                'Paint Curve',
#                'Curve',
#                'Image Paint',
#                'Vertex Paint',
#                'Weight Paint',
#                'Sculpt',
#                'Mesh',
#                'Curve',
#                'Armature',
#                'Pose',
#                'Metaball',
#                'Lattice',
#                'Particle',
#                'Font',
#                'Object Non-modal',
#                'Frames',
#                '3D View Generic',
#                '3D View',
#                ]],  # view3d_main_region_init
#          'UI':
#              [{'ED_KEYMAP_UI', 'ED_KEYMAP_FRAMES'},
#               ['3D View Generic']],
#          'TOOLS':
#              [{'ED_KEYMAP_UI', 'ED_KEYMAP_FRAMES'},
#               ['3D View Generic']]
#          },
#     'GRAPH_EDITOR': {},
#     'DOPESHEET_EDITOR': {},
#     'NLA_EDITOR': {},
#     'TIMELINE': {},
#     'IMAGE_EDITOR': {},
#     'OUTLINER': {},
#     'NODE_EDITOR': {},
#     'SEQUENCE_EDITOR': {},
#     'LOGIC_EDITOR': {},
#     'FILE_BROWSER': {},
#     'INFO': {},
#     'PROPERTIES': {},
#     'CONSOLE': {},
#     'CLIP_EDITOR': {},
# }