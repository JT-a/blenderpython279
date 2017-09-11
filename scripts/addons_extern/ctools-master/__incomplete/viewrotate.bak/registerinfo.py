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


from collections import OrderedDict
import contextlib
import traceback

import bpy


# try:
#     from .customproperty import CustomProperty
# except:
#     from _addon_customproperty import CustomProperty

__all__ = [
    'AddonRegisterInfo',
    'area_region_types',
    'bl_context_properties',
    'bl_context_view3d',
    'space_type_class_name',
]


def name_mangling(class_name, attr):
    if not attr.startswith('__') or attr.endswith('__'):
        return attr
    if not isinstance(class_name, str):  # クラスオブジェクトを想定
        class_name = class_name.__name__
    return '_' + class_name.lstrip('_') + attr


def idprop_to_py(prop):
    if isinstance(prop, list):
        return [idprop_to_py(p) for p in prop]
    elif hasattr(prop, 'to_dict'):
        return prop.to_dict()
    elif hasattr(prop, 'to_list'):
        return prop.to_list()
    else:
        return prop


def _get_addon_property_group(bl_idname):
    """
    :rtype: _AddonPropertyGroup
    """
    wm = bpy.context.window_manager
    # NOTE: self.bl_idname は '\x06' となっている
    return wm.addon_property_groups.get(bl_idname)


#####################################################################
# operator
#####################################################################
class _Helper:
    def get_register_addon_info(self, context):
        """
        :rtype: AddonRegisterInfo
        """
        addon_prefs = context.addon_preferences
        for attr in dir(addon_prefs.__class__):  # クラスにしか属性が無い
            obj = getattr(addon_prefs, attr)
            if hasattr(obj, 'register_addon_INFO'):
                return obj
        raise ValueError()


class _Registerable(_Helper):
    _users = 0

    @classmethod
    def register_class(cls, rename=False):
        import re
        if issubclass(cls, bpy.types.Operator):
            mod, func = cls.bl_idname.split('.')
            class_name = mod.upper() + '_OT_' + func
        elif issubclass(cls, bpy.types.Menu):
            class_name = cls.bl_idname
        else:
            class_name = cls.__name__
        if rename:
            if cls._users == 0 or not hasattr(bpy.types, class_name):
                while hasattr(bpy.types, class_name):
                    base, num = re.match('([a-zA-Z_]+)(\d*)$',
                                         func).groups()
                    if num == '':
                        func = base + '0'
                    else:
                        func = base + str(int(num) + 1)
                    class_name = mod.upper() + '_OT_' + func
                cls.bl_idname = mod + '.' + func
                bpy.utils.register_class(cls)
                cls._users = 1
            else:
                print('{} already registered'.format(cls))
        else:
            if hasattr(bpy.types, class_name):
                getattr(bpy.types, class_name)._users += 1
            else:
                bpy.utils.register_class(cls)
                cls._users = 1

    @classmethod
    def unregister_class(cls, force=False):
        if issubclass(cls, bpy.types.Operator):
            mod, func = cls.bl_idname.split('.')
            class_name = mod.upper() + '_OT_' + func
        elif issubclass(cls, bpy.types.Menu):
            class_name = cls.bl_idname
        else:
            class_name = cls.__name__
        if hasattr(bpy.types, class_name):
            other_cls = getattr(bpy.types, class_name)
            if other_cls._users > 0:
                other_cls._users -= 1
            if force:
                other_cls._users = 0
            if other_cls._users == 0:
                if other_cls.is_registered:
                    bpy.utils.unregister_class(other_cls)
        # else:
        #     bpy.utils.unregister_class(cls)  # 例外を出させるため


class _OperatorKeymapItemAdd(_Registerable, bpy.types.Operator):
    bl_idname = 'wm.ari_keymap_item_add'
    bl_label = 'Add Key Map Item'
    bl_description = 'Add key map item'
    bl_options = {'REGISTER', 'INTERNAL'}

    def _get_entries():
        import bpy_extras.keyconfig_utils

        modal_keymaps = {'View3D Gesture Circle', 'Gesture Border',
                         'Gesture Zoom Border', 'Gesture Straight Line',
                         'Standard Modal Map', 'Knife Tool Modal Map',
                         'Transform Modal Map', 'Paint Stroke Modal',
                         'View3D Fly Modal', 'View3D Walk Modal',
                         'View3D Rotate Modal', 'View3D Move Modal',
                         'View3D Zoom Modal', 'View3D Dolly Modal', }

        def get():
            def _get(entry):
                idname, spaceid, regionid, children = entry
                if not ('INVALID_MODAL_KEYMAP' and
                                idname in modal_keymaps):
                    yield entry
                    for e in children:
                        yield from _get(e)

            for entry in bpy_extras.keyconfig_utils.KM_HIERARCHY:
                yield from _get(entry)

        return list(get())

    keymap = bpy.props.EnumProperty(
        name='KeyMap',
        items=[(entry[0], entry[0], '') for entry in _get_entries()])
    del _get_entries

    def execute(self, context):
        ari = self.get_register_addon_info(context)
        km = ari.get_keymap(self.keymap)
        if km.is_modal:
            kmi = km.keymap_items.new_modal(
                propvalue='', type='A', value='PRESS')
            print("WARNING: '{}' is modal keymap. "
                  "Cannot remove keymap item "
                  "when unregister".format(self.keymap))
        else:
            kmi = km.keymap_items.new(
                idname='none', type='A', value='PRESS')
            ari.keymap_item_add(kmi)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if self.properties.is_property_set('keymap'):
            return self.execute(context)
        else:
            return bpy.ops.wm.call_menu(name=_MenuKeymapItemAdd.bl_idname)


class _OperatorKeymapItemRemove(_Registerable, bpy.types.Operator):
    bl_idname = 'wm.ari_keymap_item_remove'
    bl_label = 'Remove Key Map Item'
    bl_description = 'Remove key map item'
    bl_options = {'REGISTER', 'INTERNAL'}

    item_id = bpy.props.IntProperty()

    def execute(self, context):
        ari = self.get_register_addon_info(context)
        for kmi in context.keymap.keymap_items:
            if kmi.id == self.item_id:
                ari.keymap_item_remove(kmi)
                return {'FINISHED'}
        context.area.tag_redraw()
        return {'CANCELLED'}


class _OperatorKeymapsWrite(_Registerable, bpy.types.Operator):
    bl_idname = 'wm.ari_keymaps_write'
    bl_label = 'Write KeyMaps'
    bl_description = 'Convert key map items into ID properties ' \
                     '(necessary for \'Save User Settings\')'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        ari = self.get_register_addon_info(context)
        value = ari.keymap_items_get_attributes()
        addon_prefs[ari.KM_IDPROP_NAME] = value
        return {'FINISHED'}


class _OperatorKeymapsRestore(_Registerable, bpy.types.Operator):
    bl_idname = 'wm.ari_keymaps_restore'
    bl_label = 'Restore KeyMaps'
    bl_description = 'Restore key map items and clear ID properties'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        ari = self.get_register_addon_info(context)
        ari.keymap_items_restore()
        if ari.KM_IDPROP_NAME in addon_prefs:
            del addon_prefs[ari.KM_IDPROP_NAME]
        context.area.tag_redraw()
        return {'FINISHED'}


class _OperatorPanelSettingWrite(_Registerable, bpy.types.Operator):
    bl_idname = 'wm.ari_panel_settings_write'
    bl_label = 'Write Panel Settings'
    bl_description = ''
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        addon_prop = _get_addon_property_group(addon_prefs.__class__.bl_idname)
        if addon_prop:
            panel_settings = addon_prop.get('panel_settings')
            if panel_settings:
                ari = self.get_register_addon_info(context)
                addon_prefs[ari.PANEL_IDPROP_NAME] = panel_settings
        return {'FINISHED'}


class _OperatorPanelSettingUnset(_Registerable, bpy.types.Operator):
    """特定Panelの一個の項目だけを戻す"""
    bl_idname = 'wm.ari_panel_setting_unset'
    bl_label = 'Unset Panel Setting'
    bl_description = 'Convert panel settings into ID properties ' \
                     '(necessary for \'Save User Settings\')'
    bl_options = {'REGISTER', 'INTERNAL'}

    attribute = bpy.props.StringProperty()

    def execute(self, context):
        prop = context.panel_setting
        ari = self.get_register_addon_info(context)
        ari.panel_setting_restore(prop.name, self.attribute)
        context.area.tag_redraw()
        return {'FINISHED'}


class _OperatorPanelSettingsRestore(_Registerable, bpy.types.Operator):
    """全て初期化"""
    bl_idname = 'wm.ari_panel_settings_restore'
    bl_label = 'Restore Panel Settings'
    bl_description = 'Restore panel settings and clear ID properties'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        ari = self.get_register_addon_info(context)
        ari.panel_settings_restore()
        if ari.PANEL_IDPROP_NAME in addon_prefs:
            del addon_prefs[ari.PANEL_IDPROP_NAME]
        context.area.tag_redraw()
        return {'FINISHED'}


#####################################################################
# menu
#####################################################################
class _MenuKeymapItemAdd(_Registerable, bpy.types.Menu):
    bl_idname = 'WM_MT_ari_keymap_item_add'
    bl_label = 'Add New'

    def draw(self, context):
        import bpy_extras.keyconfig_utils

        addon_prefs = context.addon_preferences
        ari = self.get_register_addon_info(context)

        layout = self.layout
        column = layout.column()
        column.context_pointer_set('addon_preferences', addon_prefs)

        def get_non_modal_km_hierarchy():
            if not 'INVALID_MODAL_KEYMAP':
                return bpy_extras.keyconfig_utils.KM_HIERARCHY

            modal_keymaps = {'View3D Gesture Circle', 'Gesture Border',
                             'Gesture Zoom Border',
                             'Gesture Straight Line', 'Standard Modal Map',
                             'Knife Tool Modal Map', 'Transform Modal Map',
                             'Paint Stroke Modal', 'View3D Fly Modal',
                             'View3D Walk Modal', 'View3D Rotate Modal',
                             'View3D Move Modal', 'View3D Zoom Modal',
                             'View3D Dolly Modal'}

            def get_entry(entry):
                idname, spaceid, regionid, children = entry
                if idname not in modal_keymaps:
                    children_non_modal = []
                    for child in children:
                        e = get_entry(child)
                        if e:
                            children_non_modal.append(e)
                    return [idname, spaceid, regionid, children_non_modal]

            km_hierarchy = [e for e in
                            [get_entry(e) for e in
                             bpy_extras.keyconfig_utils.KM_HIERARCHY]
                            if e]
            return km_hierarchy

        km_hierarchy = get_non_modal_km_hierarchy()

        def max_depth(entry, depth):
            idname, spaceid, regionid, children = entry
            if children:
                d = max([max_depth(e, depth + 1) for e in children])
                return max(depth, d)
            else:
                return depth

        depth = 1
        for entry in bpy_extras.keyconfig_utils.KM_HIERARCHY:
            depth = max(depth, max_depth(entry, 1))

        used_keymap_names = {kmname for kmname, kmiid in ari.keymap_items}

        # 左の列を全部描画してから右の列にいかないとおかしな事になる

        table = []

        def gen_table(entry, row_index, col_index):
            idname, spaceid, regionid, children = entry
            if row_index > len(table) - 1:
                table.append([None for i in range(depth)])
            table[row_index][col_index] = idname
            if children:
                col_index += 1
                for e in children:
                    row_index = gen_table(e, row_index, col_index)
            else:
                row_index += 1
            return row_index

        row_index = 0
        col_index = 0
        for entry in km_hierarchy:
            row_index = gen_table(entry, row_index, col_index)

        split_list = []
        for i, row in enumerate(table):
            if row[0] and i > 0:
                split_list.append((column.split(), False))
            split_list.append((column.split(), True))
        for i in range(depth):
            j = 0
            for split, not_separator in split_list:
                row = split.row()
                if not_separator:
                    name = table[j][i]
                    if name:
                        if name in used_keymap_names:
                            icon = 'FILE_TICK'
                        else:
                            icon = 'NONE'
                        op = row.operator(_OperatorKeymapItemAdd.bl_idname,
                                          text=name, icon=icon)
                        op.keymap = name
                    j += 1
                else:
                    row.separator()


#####################################################################
# panel
#####################################################################
area_region_types = OrderedDict([
    # # EMPTY: 0
    # ('EMPTY', []),
    # VIEW_3D: 1
    ('VIEW_3D', ['WINDOW', 'UI', 'TOOLS', 'TOOL_PROPS', 'HEADER']),
    # TIMELINE: 15
    ('TIMELINE', ['WINDOW', 'HEADER']),
    # GRAPH_EDITOR: 2
    ('GRAPH_EDITOR', ['WINDOW', 'CHANNELS', 'UI', 'HEADER']),
    # DOPESHEET_EDITOR: 12
    ('DOPESHEET_EDITOR', ['WINDOW', 'CHANNELS', 'UI', 'HEADER']),
    # NLA_EDITOR: 13
    ('NLA_EDITOR', ['WINDOW', 'CHANNELS', 'UI', 'HEADER']),
    # IMAGE_EDITOR: 6
    ('IMAGE_EDITOR', ['WINDOW', 'UI', 'TOOLS', 'HEADER']),
    # SEQUENCE_EDITOR: 8
    ('SEQUENCE_EDITOR', ['WINDOW', 'PREVIEW', 'UI', 'HEADER']),
    # CLIP_EDITOR: 20
    ('CLIP_EDITOR', ['WINDOW', 'PREVIEW', 'CHANNELS', 'UI', 'TOOLS',
                     'TOOL_PROPS', 'HEADER']),
    # TEXT_EDITOR: 9
    ('TEXT_EDITOR', ['WINDOW', 'UI', 'HEADER']),
    # NODE_EDITOR: 16
    ('NODE_EDITOR', ['WINDOW', 'UI', 'TOOLS', 'HEADER']),
    # LOGIC_EDITOR: 17
    ('LOGIC_EDITOR', ['WINDOW', 'UI', 'HEADER']),
    # PROPERTIES: 4
    ('PROPERTIES', ['WINDOW', 'HEADER']),
    # OUTLINER: 3
    ('OUTLINER', ['WINDOW', 'HEADER']),
    # USER_PREFERENCES: 19
    ('USER_PREFERENCES', ['WINDOW', 'HEADER']),
    # INFO: 7
    ('INFO', ['WINDOW', 'HEADER']),
    # FILE_BROWSER: 5
    ('FILE_BROWSER', ['WINDOW', 'UI', 'TOOLS', 'TOOL_PROPS', 'HEADER']),
    # CONSOLE: 18
    ('CONSOLE', ['WINDOW', 'HEADER']),
])

# Panel.bL_space_typeがPROPERTIESの場合のPanel.bl_contextと
# SpaceProperties.contextの対応。値はSpaceProperties.contextのidentifierとname
bl_context_properties = OrderedDict([
    ('scene', ('SCENE', 'Scene')),
    ('render', ('RENDER', 'Render')),
    ('render_layer', ('RENDER_LAYER', 'Render Layers')),
    ('world', ('WORLD', 'World')),
    ('object', ('OBJECT', 'Object')),
    ('data', ('DATA', 'Data')),
    ('material', ('MATERIAL', 'Material')),
    ('texture', ('TEXTURE', 'Texture')),
    ('particle', ('PARTICLES', 'Particles')),
    ('physics', ('PHYSICS', 'Physics')),
    ('bone', ('BONE', 'Bone')),
    ('modifier', ('MODIFIER', 'Modifiers')),
    ('constraint', ('CONSTRAINT', 'Constraints')),
    ('bone_constraint', ('BONE_CONSTRAINT', 'Bone Constraints')),
])

# Panel.bl_space_typeがVIEW_3Dの場合のPanel.bl_contextと
# Context.modeの対応。値はContext.modeのidentifierとname
bl_context_view3d = OrderedDict([
    ('mesh_edit', ('EDIT_MESH', 'Mesh Edit')),  # 0
    ('curve_edit', ('EDIT_CURVE', 'Curve Edit')),  # 1
    ('surface_edit', ('EDIT_SURFACE', 'Surface Edit')),  # 2
    ('text_edit', ('EDIT_TEXT', 'Text Edit')),  # 3
    ('armature_edit', ('EDIT_ARMATURE', 'Armature Edit')),  # 4
    ('mball_edit', ('EDIT_METABALL', 'Metaball Edit')),  # 5
    ('lattice_edit', ('EDIT_LATTICE', 'Lattice Edit')),  # 6
    ('posemode', ('POSE', 'Pose')),  # 7
    ('sculpt_mode', ('SCULPT', 'Sculpt')),  # 8
    ('weightpaint', ('PAINT_WEIGHT', 'Weight Paint')),  # 9
    ('vertexpaint', ('PAINT_VERTEX', 'Vertex Paint')),  # 10
    ('imagepaint', ('PAINT_TEXTURE', 'Texture Paint')),  # 11
    ('particlemode', ('PARTICLE', 'Particle')),  # 12
    ('objectmode', ('OBJECT', 'Object')),  # 13
])


# Space.typeとクラス名の先頭の文字列との対応。例: bpy.types.USERPREF_HT_header
space_type_class_name = OrderedDict([
    ('VIEW_3D', 'VIEW3D'),
    ('TIMELINE', 'TIME'),
    ('GRAPH_EDITOR', 'GRAPH'),
    ('DOPESHEET_EDITOR', 'DOPESHEET'),
    ('NLA_EDITOR', 'NLA'),
    ('IMAGE_EDITOR', 'IMAGE'),
    ('SEQUENCE_EDITOR', 'SEQUENCER'),
    ('CLIP_EDITOR', 'CLIP'),
    ('TEXT_EDITOR', 'TEXT'),
    ('NODE_EDITOR', 'NODE'),
    ('LOGIC_EDITOR', 'LOGIC'),
    ('PROPERTIES', 'PROPERTIES'),
    ('OUTLINER', 'OUTLINER'),
    ('USER_PREFERENCES', 'USERPREF'),
    ('INFO', 'INFO'),
    ('FILE_BROWSER', 'FILEBROWSER'),
    ('CONSOLE', 'CONSOLE'),
])


def _panel_prop_bl_region_type_items(self, context):
    label = dict([('WINDOW', 'Window'),
                  ('HEADER', 'Header'),
                  ('CHANNELS', 'Channels'),
                  ('TEMPORARY', 'Temporary'),
                  ('UI', 'UI'),
                  ('TOOLS', 'Tools'),
                  ('TOOL_PROPS', 'Tool Properties'),
                  ('PREVIEW', 'Preview')]
                 )

    items = [(t, label[t], '') for t in area_region_types[self.bl_space_type]]
    _panel_prop_bl_region_type_items.items = items
    return items


def _panel_prop_bl_context_items(self, context):
    if self.bl_space_type == 'PROPERTIES':
        # buttons_main_region_draw()より
        # bl_space_typeが'PROPERTIES'の場合に使う
        items = [(k, k, '') for k in bl_context_properties]
        items = [('empty', '', '')] + items
    else:
        # view3d_tools_region_draw()より
        # これが有効なのはbl_space_typeが'VIEW_3D'でbl_region_typeが
        # 'TOOLS'の場合のみ
        items = [(k, v[1], '') for k, v in bl_context_view3d.items()]
        items = [('empty', '', '')] + items
    _panel_prop_bl_context_items.items = items
    return items


def _reregister_panel_classs(panel_bl_idname, prop):
    panel_class = getattr(bpy.types, panel_bl_idname)
    bpy.utils.unregister_class(panel_class)
    for key in ['bl_label', 'bl_category', 'bl_space_type', 'bl_region_type',
                'bl_context']:
        value = getattr(prop, key)
        if key == 'bl_context' and value == 'empty':
            value = ''
        setattr(panel_class, key, value)
    bpy.utils.register_class(panel_class)


def _panel_prop_update_func(attr):
    def _update(self, context):
        if attr == 'bl_space_type':
            self['bl_region_type'] = 0
            self['bl_context'] = 0
        if self.reregister:
            _reregister_panel_classs(self.name, self)

    return _update


class _AddonPanelSetting(_Registerable, bpy.types.PropertyGroup):
    reregister = bpy.props.BoolProperty(
        default=True)

    @contextlib.contextmanager
    def disable_reregister(self):
        self.reregister = False
        yield
        self.reregister = True

    bl_idname = bpy.props.StringProperty(
        get=lambda self: self.name)

    prop = bpy.types.Panel.bl_rna.properties['bl_label']
    bl_label = bpy.props.StringProperty(
        name=prop.name,
        description=prop.description,
        update=_panel_prop_update_func('bl_label'),
    )

    # NOTE: bl_categoryとbl_contextは省略可能属性
    prop = bpy.types.Panel.bl_rna.properties['bl_category']
    bl_category = bpy.props.StringProperty(
        name=prop.name,
        description=prop.description,
        update=_panel_prop_update_func('bl_category'),
    )

    """
    NOTE: bpy.types.Panel.bl_contextで有効な値

    BKE_context.h:
    enum {
        CTX_MODE_EDIT_MESH = 0,
        CTX_MODE_EDIT_CURVE,
        CTX_MODE_EDIT_SURFACE,
        CTX_MODE_EDIT_TEXT,
        CTX_MODE_EDIT_ARMATURE,
        CTX_MODE_EDIT_METABALL,
        CTX_MODE_EDIT_LATTICE,
        CTX_MODE_POSE,
        CTX_MODE_SCULPT,
        CTX_MODE_PAINT_WEIGHT,
        CTX_MODE_PAINT_VERTEX,
        CTX_MODE_PAINT_TEXTURE,
        CTX_MODE_PARTICLE,
        CTX_MODE_OBJECT
    };

    context.c:
    static const char *data_mode_strings[] = {
        "mesh_edit",
        "curve_edit",
        "surface_edit",
        "text_edit",
        "armature_edit",
        "mball_edit",
        "lattice_edit",
        "posemode",
        "sculpt_mode",
        "weightpaint",
        "vertexpaint",
        "imagepaint",
        "particlemode",
        "objectmode",
        NULL
    };
    """
    prop = bpy.types.Panel.bl_rna.properties['bl_space_type']
    bl_space_type = bpy.props.EnumProperty(
        name=prop.name,
        description=prop.description,
        items=(
            # ('EMPTY', 'Empty', ''),
            ('VIEW_3D', '3D View', '3D viewport'),
            ('TIMELINE', 'Timeline', 'Timeline and playback controls'),
            ('GRAPH_EDITOR', 'Graph Editor',
             'Edit drivers and keyframe interpolation'),
            ('DOPESHEET_EDITOR', 'Dope Sheet',
             'Adjust timing of keyframes'),
            ('NLA_EDITOR', 'NLA Editor', 'Combine and layer Actions'),
            ('IMAGE_EDITOR', 'UV/Image Editor',
             'View and edit images and UV Maps'),
            ('SEQUENCE_EDITOR', 'Video Sequence Editor',
             'Video editing tools'),
            ('CLIP_EDITOR', 'Movie Clip Editor', 'Motion tracking tools'),
            ('TEXT_EDITOR', 'Text Editor',
             'Edit scripts and in-file documentation'),
            ('NODE_EDITOR', 'Node Editor',
             'Editor for node-based shading and compositing tools'),
            ('LOGIC_EDITOR', 'Logic Editor', 'Game logic editing'),
            ('PROPERTIES', 'Properties',
             'Edit properties of active object and related data-blocks'),
            ('OUTLINER', 'Outliner',
             'Overview of scene graph and all available data-blocks'),
            ('USER_PREFERENCES', 'User Preferences',
             'Edit persistent configuration settings'),
            ('INFO', 'Info',
             'Main menu bar and list of error messages '
             '(drag down to expand and display)'),
            (
                'FILE_BROWSER', 'File Browser', 'Browse for files and assets'),
            ('CONSOLE', 'Python Console',
             'Interactive programmatic console for advanced editing '
             'and script development'),
        ),
        default='VIEW_3D',
        update=_panel_prop_update_func('bl_space_type'),
    )
    prop = bpy.types.Panel.bl_rna.properties['bl_region_type']
    bl_region_type = bpy.props.EnumProperty(
        name=prop.name,
        description=prop.description,
        items=_panel_prop_bl_region_type_items,
        update=_panel_prop_update_func('bl_region_type'),
    )
    prop = bpy.types.Panel.bl_rna.properties['bl_context']
    bl_context = bpy.props.EnumProperty(
        name=prop.name,
        description=prop.description,
        items=_panel_prop_bl_context_items,
        update=_panel_prop_update_func('bl_context'),
    )
    del prop


_AddonPanelSetting.__name__ = 'AddonPanelSetting'


# property ------------------------------------------------------
class _AddonPropertyGroup(_Registerable, bpy.types.PropertyGroup):
    """
    context.window_manager.addon_property_groups = \
        bpy.props.CollectionProperty(type=bpy.types.AddonPropertyGroup)
    """
    show_keymaps = bpy.props.BoolProperty(
        name='Show KeyMaps',
    )
    filter_type = bpy.props.EnumProperty(
        name='Filter Type',
        description='Filter method',
        items=[('NAME', 'Name',
                'Filter based on the operator name'),
               ('KEY', 'Key-Binding',
                'Filter based on key bindings')],
        default='NAME',
    )
    filter_text = bpy.props.StringProperty(
        name='Filter',
        description='Search term for filtering in the UI',
    )
    show_classes = bpy.props.BoolProperty(
        name='Show Classes',
    )
    show_attributes = bpy.props.BoolProperty(
        name='Show Attributes',
    )
    show_panels = bpy.props.BoolProperty(
        name='Show Panels',
    )

    default_panel_settings = bpy.props.CollectionProperty(
        type=_AddonPanelSetting)
    panel_settings = bpy.props.CollectionProperty(
        type=_AddonPanelSetting)


_AddonPropertyGroup.__name__ = 'AddonPropertyGroup'


#####################################################################
# Load Handler
#####################################################################
# ロードするとWindowManagerの属性が初期化されるのでそれを防ぐ
_wm_addon_property_groups_bak = None


@bpy.app.handlers.persistent
def _wm_addon_property_groups_load_pre(scene):
    global _wm_addon_property_groups_bak
    wm = bpy.context.window_manager
    value = wm.get('addon_property_groups')
    if value is not None:
        value = idprop_to_py(value)
    _wm_addon_property_groups_bak = value


@bpy.app.handlers.persistent
def _wm_addon_property_groups_load_post(scene):
    wm = bpy.context.window_manager
    if _wm_addon_property_groups_bak is not None:
        wm['addon_property_groups'] = _wm_addon_property_groups_bak


#####################################################################
# AddonRegisterInfo
#####################################################################
class _AddonRegisterInfo:
    """共通な属性"""
    bl_idname = ''

    @classmethod
    def _get_addon_property_group(cls):
        """
        :rtype: _AddonPropertyGroup
        """
        return _get_addon_property_group(cls.bl_idname)

    @classmethod
    def get_instance(cls):
        """AddonPreferencesのインスタンスを返す。
        :rtype: AddonPreferences
        """
        U = bpy.context.user_preferences
        attrs = cls.bl_idname.split('.')
        prefs = U.addons[attrs[0]].preferences
        for attr in attrs[1:]:
            prefs = getattr(prefs, attr)
        return prefs


class _AddonRegisterInfoKeyMap(_AddonRegisterInfo):
    KM_IDPROP_NAME = 'AddonKeyMapUtility_keymap_items'

    __lock_default_keymap_items = False

    # [(km.name, kmi.id), ...]
    keymap_items = ()
    """:type: list[(str, int)]"""

    # keymaps_set_default()の際に_keymap_itemsを複製
    # [(km.name, kmi.id), ...]s
    __default_keymap_items = ()
    """:type: list[(str, int)]"""

    # keymap_items_get_attributes()の返り値。
    __default_keymap_item_values = ()

    @staticmethod
    def get_keymap(name, keyconfig='addon'):
        """KeyMaps.new()の結果を返す。name以外の引数は勝手に補間してくれる。
        :type name: str
        :param keyconfig: 'addon' or 'user' or 'blender' or 'default'
        :type keyconfig: str
        :rtype: bpy.types.KeyMap
        """
        import bpy_extras.keyconfig_utils

        # Documentは無いのでblenderを起動してis_modalを確認するしか方法が無い
        modal_keymaps = {
            'View3D Gesture Circle', 'Gesture Border',
            'Gesture Zoom Border', 'Gesture Straight Line',
            'Standard Modal Map', 'Knife Tool Modal Map',
            'Transform Modal Map', 'Paint Stroke Modal', 'View3D Fly Modal',
            'View3D Walk Modal', 'View3D Rotate Modal', 'View3D Move Modal',
            'View3D Zoom Modal', 'View3D Dolly Modal', }

        keyconfigs = bpy.context.window_manager.keyconfigs
        if keyconfig == 'addon':  # 'Blender Addon'
            kc = keyconfigs.addon
        elif keyconfig == 'user':  # 'Blender User'
            kc = keyconfigs.user
        elif keyconfig in {'default', 'blender'}:  # 'Blender'
            kc = keyconfigs.default
        else:
            raise ValueError()
        if not kc:
            return None

        # if 'INVALID_MODAL_KEYMAP' and name in modal_keymaps:
        #     msg = "not support modal keymap: '{}'".format(name)
        #     raise ValueError(msg)

        def get(ls, name):
            for keymap_name, space_type, region_type, children in ls:
                if keymap_name == name:
                    is_modal = keymap_name in modal_keymaps
                    return kc.keymaps.new(keymap_name, space_type=space_type,
                                          region_type=region_type,
                                          modal=is_modal)
                elif children:
                    km = get(children, name)
                    if km:
                        return km

        km = get(bpy_extras.keyconfig_utils.KM_HIERARCHY, name)
        if not km:
            msg = "Keymap '{}' not in builtins".format(name)
            raise ValueError(msg)
        return km

    @staticmethod
    def __verify_keyconfigs():
        return bpy.context.window_manager.keyconfigs.addon is not None

    @classmethod
    def __reversed_keymap_table(cls):
        """KeyMapItemがキー、KeyMapが値の辞書を返す"""
        if not cls.__verify_keyconfigs():
            return
        kc = bpy.context.window_manager.keyconfigs.addon
        km_table = {}
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                km_table[kmi] = km
        return km_table

    @classmethod
    def keymap_items_get_attributes(cls):
        """
        :return: [[keymap_name, attrs, props], ...]
            第一要素はkeymap名。
            第二要素はKeymapItemの属性名(activeやshift等)とその値の辞書。
            第三要素はそのキーマップに割り当てられたオペレータのプロパティーの
            辞書。is_property_set()で判定して、未変更ならその値は辞書に含めない
        :rtype: list
        """
        import itertools
        import mathutils

        if not cls.__verify_keyconfigs():
            return

        values = []
        km_table = cls.__reversed_keymap_table()

        keympap_items = []
        for item in list(cls.keymap_items):
            km_name, kmi_id = item
            km = cls.get_keymap(km_name)
            for kmi in km.keymap_items:
                if kmi.id == kmi_id:
                    keympap_items.append(kmi)
                    break

        for kmi in keympap_items:
            km = km_table[kmi]
            # KeyMapItemの属性
            attrs = {}
            for attr in ('active', 'map_type', 'type', 'value', 'propvalue',
                         'idname', 'any', 'shift', 'ctrl', 'alt', 'oskey',
                         'key_modifier'):
                value = getattr(kmi, attr)
                if isinstance(value, bool):
                    value = int(value)
                attrs[attr] = value
            # オペレータのプロパティ
            op_props = {}
            if not km.is_modal:
                for attr in kmi.properties.bl_rna.properties.keys():
                    if attr == 'rna_type':
                        continue
                    if kmi.properties.is_property_set(attr):
                        value = getattr(kmi.properties, attr)
                        if isinstance(value, bool):
                            value = int(value)
                        elif isinstance(value, (
                                mathutils.Color, mathutils.Euler,
                                mathutils.Vector, mathutils.Quaternion)):
                            value = list(value)
                        elif isinstance(value, mathutils.Matrix):
                            value = list(
                                itertools.chain.from_iterable(value.col))
                        op_props[attr] = value

            values.append([km.name, attrs, op_props])

        return values

    @classmethod
    def keymap_items_set_attributes(cls, values):
        """一旦全部のKeyMapItemを削除してからvaluesに従って追加する。
        keymap_items_get_attributes()と対になっている。
        :param values: keymap_items_get_attributes()の返り値
        :type values: list | tuple
        """
        import traceback
        if not cls.__verify_keyconfigs():
            return
        cls.keymap_items_remove()
        keymap_items = []
        for km_name, attrs, op_props in values:
            km = cls.get_keymap(km_name)
            if 'INVALID_MODAL_KEYMAP' and km.is_modal:
                raise ValueError(
                    "not support modal keymap: '{}'".format(km.name))
            if km.is_modal:
                args = {name: attrs[name] for name in (
                    'type', 'value', 'propvalue', 'any', 'shift', 'ctrl',
                    'alt', 'oskey', 'key_modifier')}
                kmi = km.keymap_items.new_modal(**args)
                # kmi.propvalue = attrs['propvalue']  # 適用できていないから
                # TODO: ModalKeyMap使用不可。
                #       val: enum "TRANSLATE" not found in ('NONE')
            else:
                args = {name: attrs[name] for name in (
                    'idname', 'type', 'value', 'any', 'shift', 'ctrl', 'alt',
                    'oskey', 'key_modifier')}
                kmi = km.keymap_items.new(**args)
            kmi.active = attrs['active']
            for name, value in op_props.items():
                try:
                    setattr(kmi.properties, name, value)
                except:
                    traceback.print_exc()
            keymap_items.append(kmi)
        cls.keymap_items_add(keymap_items)

    @classmethod
    def keymap_item_add(cls, kmi):
        """KeyMapItemを登録する
        :param kmi: KeyMapItem 若しくは (KeyMap名, KeyMapItemのid)
        :type kmi: bpy.types.KeyMapItem | (str, int)
        """
        if not cls.__verify_keyconfigs():
            return
        if isinstance(kmi, bpy.types.KeyMapItem):
            km_tabel = cls.__reversed_keymap_table()
            km = km_tabel[kmi]
        else:
            km, kmi = kmi
        if 'INVALID_MODAL_KEYMAP' and km.is_modal:
            raise ValueError("not support modal keymap: '{}'".format(km.name))
        cls.keymap_items.append((km.name, kmi.id))

    @classmethod
    def keymap_items_add(cls, addon_keymaps):
        """KeyMapItemを登録する。
        :param addon_keymaps: KeyMapItem 若しくは (KeyMap名, KeyMapItemのid) の
            リスト
        :type addon_keymaps: list[bpy.types.KeyMapItem] | list[(str, int)]
        """
        if not cls.__verify_keyconfigs():
            return
        km_tabel = cls.__reversed_keymap_table()
        items = []
        for kmi in addon_keymaps:
            if isinstance(kmi, bpy.types.KeyMapItem):
                km = km_tabel[kmi]
            else:
                km, kmi = kmi
            if km.is_modal:  # 現在modalは不可
                raise ValueError(
                    "not support modal keymap: '{}'".format(km.name))
            items.append((km.name, kmi.id))
        cls.keymap_items.extend(items)

    @classmethod
    def keymap_item_remove(cls, kmi, remove=True):
        """KeyMapItemの登録を解除する
        :param kmi: KeyMapItem 若しくは (KeyMap名, KeyMapItemのid)
        :type kmi: bpy.types.KeyMapItem | (str, int)
        :param remove: KeyMapItemをKeyMapItemsから削除する
        :type remove: bool
        """
        if not cls.__verify_keyconfigs():
            return
        km_table = cls.__reversed_keymap_table()
        if isinstance(kmi, bpy.types.KeyMapItem):
            km = km_table[kmi]
            item = (km.name, kmi.id)
        else:
            item = kmi
            km_name, kmi_id = item
            km = cls.get_keymap(km_name)
            for kmi in km.keymap_items:
                if kmi.id == kmi_id:
                    break
            else:
                raise ValueError('KeyMapItem not fond')
        if 'INVALID_MODAL_KEYMAP' and km.is_modal:
            raise ValueError("not support modal keymap: '{}'".format(km.name))
        cls.keymap_items.remove(item)
        if remove:
            km.keymap_items.remove(kmi)
            # 強制的に更新
            bpy.context.window_manager.keyconfigs.active = \
                bpy.context.window_manager.keyconfigs.active

    @classmethod
    def keymap_items_remove(cls, remove=True,
                            remove_only_added=False):
        """全てのKeyMapItemの登録を解除する。
        :param remove: KeyMapItemをKeyMap.keymap_itemsから削除する
        :type remove: bool
        :param remove_only_added:
            self._default_keymap_itemsに含まれないもののみ消す
        :type remove_only_added: bool
        """
        if not cls.__verify_keyconfigs():
            return
        if remove:
            for km_name, kmi_id in cls.keymap_items:
                if remove_only_added:
                    if (km_name, kmi_id) in cls.__default_keymap_items:
                        continue
                km = cls.get_keymap(km_name)
                for kmi in km.keymap_items:
                    if kmi.id == kmi_id:
                        break
                else:
                    # raise ValueError('KeyMapItem not fond')
                    print('KeyMapItem not fond. KeyMap: {}, ID: {}'.format(
                          km_name, kmi_id))
                if 'INVALID_MODAL_KEYMAP' and km.is_modal:
                    raise ValueError(
                        "not support modal keymap: '{}'".format(km.name))
                km.keymap_items.remove(kmi)
        cls.keymap_items.clear()

        # commit 103fbb3afc076383b94910e535374c5db398d06c
        #     Fix memory leak caused by unknown opeartor of keymap item
        #
        # addonのKeyMapからKeyMapItemを消してもuserのKeyMapには
        # まだ残ったままで、これの更新はメインループで行われる。
        # この更新前にKeyMapItemに割り当てられたオペレーターをunregister
        # してしまっているとKeyMapItem開放時にSegmentation faultで落ちる。
        bpy.context.window_manager.keyconfigs.active = \
            bpy.context.window_manager.keyconfigs.active

    @classmethod
    def keymap_items_set_default(cls):
        """現在登録しているKeyMapItemを初期値(restore時の値)とする"""
        cls.__default_keymap_item_values.clear()
        values = cls.keymap_items_get_attributes()
        if values:
            cls.__default_keymap_item_values[:] = values
        cls.__default_keymap_items = cls.keymap_items[:]

    @classmethod
    def keymap_items_init(cls, addon_keymaps):
        cls.keymap_items.clear()
        cls.keymap_items_add(addon_keymaps)
        cls.keymap_items_set_default()

    @classmethod
    def keymap_items_load(cls):
        """保存されたキーマップを読んで現在のキーマップを置き換える"""
        addon_prefs = cls.get_instance()
        if cls.KM_IDPROP_NAME not in addon_prefs:
            return False
        cls.keymap_items_set_attributes(addon_prefs[cls.KM_IDPROP_NAME])
        return True

    @classmethod
    def keymap_items_restore(cls):
        """キーマップを初期値に戻す"""
        cls.keymap_items_set_attributes(cls.__default_keymap_item_values)
        cls.keymap_items_set_default()

    # draw ----------------------------------------------------------
    __EVENT_TYPES = set()
    __EVENT_TYPE_MAP = {}
    __EVENT_TYPE_MAP_EXTRA = {}

    __INDENTPX = 16

    def __indented_layout(self, layout, level):
        if level == 0:
            # Tweak so that a percentage of 0 won't split by half
            level = 0.0001
        indent = level * self.__INDENTPX / bpy.context.region.width

        split = layout.split(percentage=indent)
        col = split.column()
        col = split.column()
        return col

    def __draw_entry(self, display_keymaps, entry, col, level=0):
        idname, spaceid, regionid, children = entry

        for km, km_items in display_keymaps:
            if (km.name == idname and km.space_type == spaceid and
                        km.region_type == regionid):
                self.__draw_km(display_keymaps, km, km_items, children, col,
                               level)

    def __draw_km(self, display_keymaps, km, km_items, children, layout,
                  level):
        from bpy.app.translations import pgettext_iface as iface_
        from bpy.app.translations import contexts as i18n_contexts

        # km = km.active()  # keyconfigs.userのkeymapが返ってくる

        layout.context_pointer_set("keymap", km)

        col = self.__indented_layout(layout, level)

        row = col.row(align=True)
        row.prop(km, "show_expanded_children", text="", emboss=False)
        row.label(text=km.name, text_ctxt=i18n_contexts.id_windowmanager)

        # if km.is_user_modified or km.is_modal:
        if km.is_modal:
            subrow = row.row()
            subrow.alignment = 'RIGHT'

            # if km.is_user_modified:
            #     subrow.operator("wm.keymap_restore", text="Restore")
            if km.is_modal:
                subrow.label(text="", icon='LINKED')
            del subrow

        if km.show_expanded_children:
            if children:
                # Put the Parent key map's entries in a 'global' sub-category
                # equal in hierarchy to the other children categories
                subcol = self.__indented_layout(col, level + 1)
                subrow = subcol.row(align=True)
                subrow.prop(km, "show_expanded_items", text="", emboss=False)
                subrow.label(text=iface_("%s (Global)") % km.name,
                             translate=False)
            else:
                km.show_expanded_items = True

            # Key Map items
            if km.show_expanded_items:
                kmi_level = level + 3 if children else level + 1
                # for kmi in km.keymap_items:
                for kmi in km_items:
                    self.__draw_kmi(km, kmi, col, kmi_level)

            # Child key maps
            if children:
                for entry in children:
                    self.__draw_entry(display_keymaps, entry, col,
                                      level + 1)

            col.separator()

    def __draw_kmi(self, km, kmi, layout, level):
        map_type = kmi.map_type

        col = self.__indented_layout(layout, level)

        if kmi.show_expanded:
            col = col.column(align=True)
            box = col.box()
        else:
            box = col.column()

        split = box.split(percentage=0.01)

        # header bar
        row = split.row()
        row.prop(kmi, "show_expanded", text="", emboss=False)

        row = split.row()
        row.prop(kmi, "active", text="", emboss=False)

        if km.is_modal:
            row.prop(kmi, "propvalue", text="")
        else:
            row.label(text=kmi.name)

        row = split.row()
        row.prop(kmi, "map_type", text="")
        if map_type == 'KEYBOARD':
            row.prop(kmi, "type", text="", full_event=True)
        elif map_type == 'MOUSE':
            row.prop(kmi, "type", text="", full_event=True)
        elif map_type == 'NDOF':
            row.prop(kmi, "type", text="", full_event=True)
        elif map_type == 'TWEAK':
            subrow = row.row()
            subrow.prop(kmi, "type", text="")
            subrow.prop(kmi, "value", text="")
        elif map_type == 'TIMER':
            row.prop(kmi, "type", text="")
        else:
            row.label()

        sub = row.row()
        op = sub.operator(_OperatorKeymapItemRemove.bl_idname, text="",
                          icon='X')
        op.item_id = kmi.id
        if self.__lock_default_keymap_items:
            if (km.name, kmi.id) in self.__default_keymap_items:
                sub.enabled = False

        # Expanded, additional event settings
        if kmi.show_expanded:
            box = col.box()

            split = box.split(percentage=0.4)
            sub = split.row()

            if km.is_modal:
                sub.prop(kmi, "propvalue", text="")
            else:
                # One day...
                # ~ sub.prop_search(kmi, "idname", bpy.context.window_manager,
                #  "operators_all", text="")
                sub.prop(kmi, "idname", text="")

            if map_type not in {'TEXTINPUT', 'TIMER'}:
                sub = split.column()
                subrow = sub.row(align=True)

                if map_type == 'KEYBOARD':
                    subrow.prop(kmi, "type", text="", event=True)
                    subrow.prop(kmi, "value", text="")
                elif map_type in {'MOUSE', 'NDOF'}:
                    subrow.prop(kmi, "type", text="")
                    subrow.prop(kmi, "value", text="")

                subrow = sub.row()
                subrow.scale_x = 0.75
                subrow.prop(kmi, "any")
                subrow.prop(kmi, "shift")
                subrow.prop(kmi, "ctrl")
                subrow.prop(kmi, "alt")
                subrow.prop(kmi, "oskey", text="Cmd")
                subrow.prop(kmi, "key_modifier", text="", event=True)

            # Operator properties
            box.template_keymap_item_properties(kmi)

    def __draw_filtered(self, display_keymaps, filter_type, filter_text,
                        layout):
        _EVENT_TYPES = self.__EVENT_TYPES
        _EVENT_TYPE_MAP = self.__EVENT_TYPE_MAP
        _EVENT_TYPE_MAP_EXTRA = self.__EVENT_TYPE_MAP_EXTRA

        if filter_type == 'NAME':
            def filter_func(kmi):
                return (filter_text in kmi.idname.lower() or
                        filter_text in kmi.name.lower())
        else:
            if not _EVENT_TYPES:
                enum = bpy.types.Event.bl_rna.properties["type"].enum_items
                _EVENT_TYPES.update(enum.keys())
                _EVENT_TYPE_MAP.update(
                    {item.name.replace(" ", "_").upper(): key for key, item in
                     enum.items()})

                del enum
                _EVENT_TYPE_MAP_EXTRA.update(
                    {"`": 'ACCENT_GRAVE',
                     "*": 'NUMPAD_ASTERIX',
                     "/": 'NUMPAD_SLASH',
                     "RMB": 'RIGHTMOUSE',
                     "LMB": 'LEFTMOUSE',
                     "MMB": 'MIDDLEMOUSE',
                     })
                _EVENT_TYPE_MAP_EXTRA.update(
                    {"%d" % i: "NUMPAD_%d" % i for i in range(10)})
            # done with once off init

            filter_text_split = filter_text.strip()
            filter_text_split = filter_text.split()

            # Modifier {kmi.attribute: name} mapping
            key_mod = {"ctrl": "ctrl", "alt": "alt", "shift": "shift",
                       "cmd": "oskey", "oskey": "oskey", "any": "any",}
            # KeyMapItem like dict, use for comparing against
            # attr: {states, ...}
            kmi_test_dict = {}
            # Special handling of 'type' using a list if sets,
            # keymap items must match against all.
            kmi_test_type = []

            # initialize? - so if a if a kmi has a MOD assigned it wont show up.
            # ~ for kv in key_mod.values():
            # ~    kmi_test_dict[kv] = {False}

            # altname: attr
            for kk, kv in key_mod.items():
                if kk in filter_text_split:
                    filter_text_split.remove(kk)
                    kmi_test_dict[kv] = {True}

            # whats left should be the event type
            def kmi_type_set_from_string(kmi_type):
                kmi_type = kmi_type.upper()
                kmi_type_set = set()

                if kmi_type in _EVENT_TYPES:
                    kmi_type_set.add(kmi_type)

                if not kmi_type_set or len(kmi_type) > 1:
                    # replacement table
                    for event_type_map in (_EVENT_TYPE_MAP,
                                           _EVENT_TYPE_MAP_EXTRA):
                        kmi_type_test = event_type_map.get(kmi_type)
                        if kmi_type_test is not None:
                            kmi_type_set.add(kmi_type_test)
                        else:
                            # print("Unknown Type:", kmi_type)

                            # Partial match
                            for k, v in event_type_map.items():
                                if (kmi_type in k) or (kmi_type in v):
                                    kmi_type_set.add(v)
                return kmi_type_set

            for i, kmi_type in enumerate(filter_text_split):
                kmi_type_set = kmi_type_set_from_string(kmi_type)

                if not kmi_type_set:
                    return False

                kmi_test_type.append(kmi_type_set)
            # tiny optimization, sort sets so the smallest is first
            # improve chances of failing early
            kmi_test_type.sort(key=lambda kmi_type_set: len(kmi_type_set))

            # main filter func, runs many times
            def filter_func(kmi):
                for kk, ki in kmi_test_dict.items():
                    val = getattr(kmi, kk)
                    if val not in ki:
                        return False

                # special handling of 'type'
                for ki in kmi_test_type:
                    val = kmi.type
                    if val == 'NONE' or val not in ki:
                        # exception for 'type'
                        # also inspect 'key_modifier' as a fallback
                        val = kmi.key_modifier
                        if not (val == 'NONE' or val not in ki):
                            continue
                        return False

                return True

        for km, km_items in display_keymaps:
            # km = km.active()  # keyconfigs.userのkeymapが返ってくる
            layout.context_pointer_set("keymap", km)

            if filter_text:
                filtered_items = [kmi for kmi in km_items if filter_func(kmi)]
            else:
                filtered_items = km_items

            if filtered_items:
                col = layout.column()

                row = col.row()
                row.label(text=km.name, icon='DOT')

                for kmi in filtered_items:
                    self.__draw_kmi(km, kmi, col, 1)

        return True

    def __draw_hierarchy(self, display_keymaps, layout):
        from bpy_extras import keyconfig_utils
        for entry in keyconfig_utils.KM_HIERARCHY:
            self.__draw_entry(display_keymaps, entry, layout)

    def _draw_addon_keymaps(self, context, layout, hierarchy=False, box=True):
        addon_prop = self._get_addon_property_group()
        addon_prefs = self.get_instance()
        space_pref = context.space_data

        if box:
            col = layout.column().box()
        else:
            col = layout.column()

        sub = col.column()

        subsplit = sub.split()
        subcol = subsplit.column()

        subcolsplit = subcol.split(percentage=0.7)  # 右側にwrite,restore

        display_keymaps = {}
        for item in list(self.keymap_items):
            km_name, kmi_id = item
            km = self.get_keymap(km_name)
            for kmi in km.keymap_items:
                if kmi.id == kmi_id:
                    break
            else:
                self.keymap_items.remove(item)
                continue
            items = display_keymaps.setdefault(km, [])
            items.append(kmi)
        for km, items in display_keymaps.items():
            ls = list(km.keymap_items)
            items.sort(key=ls.index)
        display_keymaps = list(display_keymaps.items())

        row = subcolsplit.row()
        rowsub = row.split(align=True, percentage=0.33)
        # postpone drawing into rowsub, so we can set alert!

        # col.separator()

        if 0:
            filter_type = space_pref.filter_type
            filter_text = space_pref.filter_text.strip()
        else:
            filter_type = addon_prop.filter_type
            filter_text = addon_prop.filter_text

        if filter_text or not hierarchy:
            filter_text = filter_text.lower()
            ok = self.__draw_filtered(display_keymaps, filter_type,
                                      filter_text, col)
        else:
            self.__draw_hierarchy(display_keymaps, col)
            ok = True

        colsub = col.split(percentage=0.2).column()
        colsub.operator(_OperatorKeymapItemAdd.bl_idname, text="Add New",
                        icon='ZOOMIN')

        # go back and fill in rowsub
        if 0:
            rowsub.prop(space_pref, "filter_type", text="")
        else:
            rowsub.prop(addon_prop, 'filter_type', text="")
        rowsubsub = rowsub.row(align=True)
        if not ok:
            rowsubsub.alert = True
        if 0:
            rowsubsub.prop(space_pref, "filter_text", text="", icon='VIEWZOOM')
        else:
            rowsubsub.prop(addon_prop, 'filter_text', text="", icon='VIEWZOOM')

        # Write / Restore
        default_km = self.__default_keymap_item_values
        current_km = self.keymap_items_get_attributes()
        if self.KM_IDPROP_NAME in addon_prefs:
            prop = addon_prefs[self.KM_IDPROP_NAME]
            idp_km = idprop_to_py(prop)
        else:
            idp_km = None
        subcolsplitrow = subcolsplit.row().split(align=True)
        # Write
        subcolsplitrow_sub = subcolsplitrow.row(align=True)
        if current_km == default_km and self.KM_IDPROP_NAME not in addon_prefs:
            subcolsplitrow_sub.enabled = False
        else:
            subcolsplitrow_sub.enabled = current_km != idp_km
        subcolsplitrow_sub.operator(_OperatorKeymapsWrite.bl_idname,
                                    text='Write')
        # Restore
        subcolsplitrow_sub = subcolsplitrow.row(align=True)
        if current_km == default_km and self.KM_IDPROP_NAME not in addon_prefs:
            subcolsplitrow_sub.enabled = False
        subcolsplitrow_sub.operator(_OperatorKeymapsRestore.bl_idname,
                                    text='Restore')


class _AddonRegisterInfoPanel(_AddonRegisterInfo):
    PANEL_IDPROP_NAME = 'PANEL_SETTINGS'

    @classmethod
    def panel_settings_init(cls, panel_classes):
        addon_prop = cls._get_addon_property_group()
        addon_prop.default_panel_settings.clear()
        addon_prop.panel_settings.clear()

        for panel_class in panel_classes:
            prop = addon_prop.default_panel_settings.add()
            with prop.disable_reregister():
                prop.name = getattr(panel_class, 'bl_idname',
                                    panel_class.__name__)
                prop.bl_label = panel_class.bl_label
                if hasattr(panel_class, 'bl_category'):
                    prop.bl_category = panel_class.bl_category
                else:
                    prop.bl_category = ''
                prop.bl_space_type = panel_class.bl_space_type
                prop.bl_region_type = panel_class.bl_region_type
                if hasattr(panel_class, 'bl_context'):
                    value = panel_class.bl_context
                    if value == '':
                        value = 'empty'
                    prop.bl_context = value
                else:
                    prop.bl_context = 'empty'
        if addon_prop.default_panel_settings:
            addon_prop['panel_settings'] = addon_prop['default_panel_settings']

        cls.panel_settings_load()

    @classmethod
    def __panel_setting_reregister(cls, panel_bl_idname):
        addon_prop = cls._get_addon_property_group()
        prop = addon_prop.panel_settings[panel_bl_idname]
        _reregister_panel_classs(panel_bl_idname, prop)

    @classmethod
    def panel_settings_load(cls):
        """ユーザー設定を適用する"""
        addon_prop = cls._get_addon_property_group()
        addon_prefs = cls.get_instance()
        if cls.PANEL_IDPROP_NAME in addon_prefs:
            settings = idprop_to_py(addon_prop.get('panel_settings', []))
            saved_settings = idprop_to_py(addon_prefs[cls.PANEL_IDPROP_NAME])
            for saved_setting in saved_settings:
                for setting in settings:
                    if setting['name'] == saved_setting['name']:
                        setting.update(saved_setting)
                        break
            addon_prop['panel_settings'] = settings

        for prop in addon_prop.panel_settings:
            cls.__panel_setting_reregister(prop.name)

    @classmethod
    def panel_setting_restore(cls, panel_bl_idname, attr):
        """とあるパネルの一属性を初期設定に戻す。UIのXボタンを押した時の動作"""
        addon_prop = cls._get_addon_property_group()
        prop = addon_prop.panel_settings.get(panel_bl_idname)
        default_prop = addon_prop.default_panel_settings.get(panel_bl_idname)
        try:
            setattr(prop, attr, getattr(default_prop, attr))
        except:
            # bl_space_typeを変更していた場合にbl_region_typeを
            # 戻そうとして失敗するとか
            traceback.print_exc()

    @classmethod
    def panel_settings_restore(cls):
        """初期設定に戻す"""
        addon_prop = cls._get_addon_property_group()
        if not addon_prop:
            return
        if addon_prop.default_panel_settings:
            addon_prop['panel_settings'] = addon_prop['default_panel_settings']
        else:
            addon_prop.panel_settings.clear()

        # 適用
        for prop in addon_prop.panel_settings:
            cls.__panel_setting_reregister(prop.name)

    def _draw_addon_panels(self, context, layout, box=True):
        addon_prefs = self.get_instance()
        addon_prop = self._get_addon_property_group()

        if box:
            column = layout.column().box()
        else:
            column = layout.column()
        column.context_pointer_set('addon_preferences', addon_prefs)

        row = column.row()
        split = row.split(0.7)
        _ = split.row()
        row = split.row()
        sp = row.split(align=True)
        sub = sp.row(align=True)

        current_settings = idprop_to_py(addon_prop.get('panel_settings', []))
        default_settings = idprop_to_py(
            addon_prop.get('default_panel_settings', []))
        if self.PANEL_IDPROP_NAME in addon_prefs:
            saved_settings = idprop_to_py(addon_prefs[self.PANEL_IDPROP_NAME])
        else:
            saved_settings = None

        if saved_settings is None:
            sub.enabled = current_settings != default_settings
        else:
            sub.enabled = current_settings != saved_settings
        sub.operator(_OperatorPanelSettingWrite.bl_idname, text='Write')
        sub = sp.row(align=True)
        if saved_settings is None:
            sub.enabled = current_settings != default_settings
        else:
            sub.enabled = True
        sub.operator(_OperatorPanelSettingsRestore.bl_idname, text='Restore')

        for prop in addon_prop.panel_settings:
            def is_changed(attr):
                default_prop = addon_prop.default_panel_settings[prop.name]
                return getattr(prop, attr) != getattr(default_prop, attr)

            prop_box = column.box()
            prop_box.context_pointer_set('panel_setting', prop)

            split = prop_box.split()
            col = split.column()

            row = col.box().row()
            row.label('bpy.types.{}'.format(prop.name))

            row = col.box().row()
            row.prop(prop, 'bl_label')
            if is_changed('bl_label'):
                sub = row.row()
                op = sub.operator(_OperatorPanelSettingUnset.bl_idname,
                                  text='', icon='X', emboss=False)
                op.attribute = 'bl_label'

            row = col.box().row()
            row.prop(prop, 'bl_category')
            if is_changed('bl_category'):
                sub = row.row()
                op = sub.operator(_OperatorPanelSettingUnset.bl_idname,
                                  text='', icon='X', emboss=False)
                op.attribute = 'bl_category'

            col = split.column()

            row = col.box().row()
            row.prop(prop, 'bl_space_type')
            if is_changed('bl_space_type'):
                sub = row.row()
                op = sub.operator(_OperatorPanelSettingUnset.bl_idname,
                                  text='', icon='X', emboss=False)
                op.attribute = 'bl_space_type'

            row = col.box().row()
            row.prop(prop, 'bl_region_type')
            if is_changed('bl_region_type'):
                sub = row.row()
                op = sub.operator(_OperatorPanelSettingUnset.bl_idname,
                                  text='', icon='X', emboss=False)
                op.attribute = 'bl_region_type'

            row = col.box().row()
            row.prop(prop, 'bl_context')
            if is_changed('bl_context'):
                sub = row.row()
                op = sub.operator(_OperatorPanelSettingUnset.bl_idname,
                                  text='', icon='X', emboss=False)
                op.attribute = 'bl_context'


class _AddonRegisterInfoClass(_AddonRegisterInfo):
    addon_classes = ()
    """:type: list[T]"""

    @classmethod
    def addon_classes_add(cls, types):
        cls.addon_classes.extend(types)

    @classmethod
    def addon_classes_remove(cls):
        for t in cls.addon_classes:
            if t.is_registered:
                bpy.utils.unregister_class(t)
        cls.addon_classes.clear()

    def _draw_addon_classes(self, context, layout, box=True):
        if box:
            col = layout.column().box()
        else:
            col = layout.column()

        row = col.row()

        # NOTE: register可能なクラスはRNA_def_struct_register_funcs()で
        #       regメンバに代入しているもの
        # registerable_classes = [
        #     bpy.types.AddonPreferences,
        #     bpy.types.Panel,
        #     bpy.types.UIList,
        #     bpy.types.Menu,
        #     bpy.types.Header,
        #     bpy.types.Operator,
        #     bpy.types.Macro,
        #     bpy.types.KeyingSetInfo,
        #     bpy.types.RenderEngine,
        #     bpy.types.PropertyGroup,
        #     bpy.types.Node,
        #     bpy.types.NodeCustomGroup,
        #     bpy.types.ShaderNode,
        #     bpy.types.CompositorNode,
        #     bpy.types.TextureNode,
        #     bpy.types.NodeSocket,
        #     bpy.types.NodeSocketInterface,
        #     bpy.types.NodeTree,
        # ]
        classes = []
        for c in self.addon_classes:
            if not c.is_registered:
                continue
            name = c.bl_rna.name
            for base in c.__bases__:
                if issubclass(base, bpy.types.bpy_struct):
                    classes.append((c, name, base))
                    break
            else:
                classes.append((c, name, None))
        classes.sort(key=lambda x: (getattr(x[2], '__name__', ''), x[1]))

        split = row.split(0.2)
        col1 = split.column()
        col_ = split.split(0.5)
        col2 = col_.column()
        col3 = col_.column()
        for class_type, class_name, base_class in classes:
            col1.label(base_class.__name__)
            col2.label(class_name)
            print(class_type, getattr(class_type, 'bl_label', ''))
            col3.label(getattr(class_type, 'bl_label', ''))


class _AddonRegisterInfoAttribute(_AddonRegisterInfo):
    addon_attributes = ()
    """:type: list[(str, str)]"""

    @classmethod
    def addon_attributes_add(cls, attributes):
        cls.addon_attributes.extend(attributes)

    @classmethod
    def addon_attributes_remove(cls):
        for class_name, attr in cls.addon_attributes:
            cls_ = getattr(bpy.types, class_name, None)
            if cls_:
                if hasattr(cls_, attr):
                    delattr(cls_, attr)
        cls.addon_attributes.clear()

    def _draw_addon_attributes(self, context, layout, box=True):
        if box:
            col = layout.column().box()
        else:
            col = layout.column()

        attributes = self.addon_attributes[:]
        attributes.sort(key=lambda x: (x[0], x[1]))

        for class_name, attr in attributes:
            col.label(class_name + '.' + attr)


class AddonRegisterInfo(  # _AddonRegisterInfo,
                        _AddonRegisterInfoKeyMap,
                        _AddonRegisterInfoPanel,
                        _AddonRegisterInfoClass,
                        _AddonRegisterInfoAttribute):

    IGRORE_ADDONS = ['CTools']  # bl_info['name']
    register_addon_INFO = True  # この属性の有無でインスタンスを判別する

    @classmethod
    def derive(cls, bl_idname=None, lock_default_keymap_items=None):
        """クラス属性を初期化した新しいクラスを生成して返す。__new__や__init__が
        使えないので苦肉の策
        直接継承せずにこれで生成したクラスを使う
        :rtype: AddonRegisterInfo
        """
        attrs = {
            'keymap_items': [],
            name_mangling(_AddonRegisterInfoKeyMap.__name__, '__default_keymap_items'): [],
            name_mangling(_AddonRegisterInfoKeyMap.__name__, '__default_keymap_item_values'): [],
            'addon_classes': [],
            'addon_attributes': [],
        }
        if bl_idname is not None:
            attrs['bl_idname'] = bl_idname
        if lock_default_keymap_items is not None:
            key = name_mangling(cls.__name__,
                                '__lock_default_keymap_items')
            attrs[key] = lock_default_keymap_items
        t = type(cls.__name__, (cls,), attrs)
        return t

    # draw ----------------------------------------------------------
    def draw(self, context, hierarchy=False, box=True, **kwargs):
        """キーマップアイテムの一覧を描画。
        :param context: bpy.types.Context
        :param layout: bpy.types.UILayout
        :param hierarchy: 階層表示にする
        :type hierarchy: bool
        :param box: 展開時にBoxで囲む
        :type box: bool
        """

        layout = self.layout
        addon_prefs = self.get_instance()

        column = layout.column()
        column.context_pointer_set('addon_preferences', addon_prefs)

        addon_prop = self._get_addon_property_group()
        show_keymaps = addon_prop.show_keymaps
        show_classes = addon_prop.show_classes
        show_attributes = addon_prop.show_attributes
        show_panels = addon_prop.show_panels

        row = column.row()
        split = row.split()

        sub = split.row()
        icon = 'TRIA_DOWN' if show_keymaps else 'TRIA_RIGHT'
        sub.prop(addon_prop, 'show_keymaps', text='', icon=icon, emboss=False)

        text = '{} Key Map Items'.format(len(self.keymap_items))
        sub.label(text)

        sub = split.row()
        icon = 'TRIA_DOWN' if show_classes else 'TRIA_RIGHT'
        sub.prop(addon_prop, 'show_classes', text='', icon=icon, emboss=False)
        text = '{} Classes'.format(len(self.addon_classes))
        sub.label(text)

        if self.addon_attributes:
            sub = split.row()
            icon = 'TRIA_DOWN' if show_attributes else 'TRIA_RIGHT'
            sub.prop(addon_prop, 'show_attributes', text='', icon=icon,
                     emboss=False)
            text = '{} Attributes'.format(len(self.addon_attributes))
            sub.label(text)

        if addon_prop.default_panel_settings:
            sub = split.row()
            icon = 'TRIA_DOWN' if show_panels else 'TRIA_RIGHT'
            sub.prop(addon_prop, 'show_panels', text='', icon=icon,
                     emboss=False)
            text = '{} Panels'.format(len(addon_prop.panel_settings))
            sub.label(text)

        # メソッドが上書きされてるかもしれないのでクラスから直接実行する
        if show_keymaps:
            self._draw_addon_keymaps(context, column, hierarchy, box)
        if show_classes and self.addon_classes:
            self._draw_addon_classes(context, layout, box)
        if show_attributes and self.addon_attributes:
            self._draw_addon_attributes(context, layout, box)
        if show_panels and addon_prop.default_panel_settings:
            self._draw_addon_panels(context, layout, box)

        c = super()
        if hasattr(c, 'draw'):
            c.draw(context, **kwargs)

    # register / unregister -----------------------------------------
    @classmethod
    def register(cls):
        """継承したクラスでもregisterを定義するなら、super関数を使って
        このメソッドを呼ぶ。
        super().register()
        """
        # 属性初期化
        cls.keymap_items = []
        setattr(cls, name_mangling(_AddonRegisterInfoKeyMap.__name__,
                                   '__default_keymap_items'), [])
        setattr(cls, name_mangling(_AddonRegisterInfoKeyMap.__name__,
                                   '__default_keymap_item_values'), [])
        # cls.__default_keymap_items = []
        # cls.__default_keymap_item_values = []
        cls.addon_classes = []
        cls.addon_attributes = []

        classes = [_OperatorKeymapItemAdd,
                   _OperatorKeymapItemRemove,
                   _OperatorKeymapsWrite,
                   _OperatorKeymapsRestore,
                   _OperatorPanelSettingWrite,
                   _OperatorPanelSettingUnset,
                   _OperatorPanelSettingsRestore,
                   _MenuKeymapItemAdd,
                   _AddonPanelSetting,
                   _AddonPropertyGroup,
                   ]
        for c in classes:
            c.register_class()

        c = getattr(bpy.types, _AddonPropertyGroup.__name__)
        bpy.types.WindowManager.addon_property_groups = \
            bpy.props.CollectionProperty(type=c)

        for func in bpy.app.handlers.load_pre:
            if func.__name__ == _wm_addon_property_groups_load_pre.__name__:
                break
        else:
            bpy.app.handlers.load_pre.append(
                _wm_addon_property_groups_load_pre)
        for func in bpy.app.handlers.load_post:
            if func.__name__ == _wm_addon_property_groups_load_post.__name__:
                break
        else:
            bpy.app.handlers.load_post.append(
                _wm_addon_property_groups_load_post)

        c = super()
        if hasattr(c, 'register'):
            c.register()

    @classmethod
    def unregister(cls):
        """注意事項はregisterと同じ"""

        classes = [_OperatorKeymapItemAdd,
                   _OperatorKeymapItemRemove,
                   _OperatorKeymapsWrite,
                   _OperatorKeymapsRestore,
                   _OperatorPanelSettingWrite,
                   _OperatorPanelSettingUnset,
                   _OperatorPanelSettingsRestore,
                   _MenuKeymapItemAdd,
                   _AddonPanelSetting,
                   _AddonPropertyGroup,
                   ]
        for c in classes[::-1]:
            c.unregister_class()

        if not hasattr(bpy.types, _AddonPropertyGroup.__name__):
            del bpy.types.WindowManager.addon_property_groups
            bpy.app.handlers.load_pre.remove(
                _wm_addon_property_groups_load_pre)
            bpy.app.handlers.load_post.remove(
                _wm_addon_property_groups_load_post)

        c = super()
        if hasattr(c, 'unregister'):
            c.unregister()

    # wrap ----------------------------------------------------------
    @classmethod
    def register_addon(cls, func, module=None, instance=None, **kwargs):
        import functools

        if not module:
            module = func.__module__

        def get_km_items():
            kc = bpy.context.window_manager.keyconfigs.addon
            if not kc:
                return None

            items = []
            for km in kc.keymaps:
                for kmi in km.keymap_items:
                    items.append((km, kmi))
            return items

        @functools.wraps(func)
        def _register():
            items_pre = get_km_items()
            bpy_types_pre = set(dir(bpy.types))

            func()

            items_post = get_km_items()
            bpy_types_post = set(dir(bpy.types))

            if items_pre is not None and items_post is not None:
                keymap_items = [item for item in items_post
                                if item not in items_pre]
            else:
                keymap_items = []

            new_types = []
            new_panel_classes = []
            addon_prefs_class = None
            root_module = module.split('.')[0]
            for c in bpy.utils._bpy_module_classes(
                    root_module, is_registered=True):
                if not c.__module__.startswith(module):
                    continue
                new_types.append(c)
                if issubclass(c, bpy.types.AddonPreferences):
                    addon_prefs_class = c
                if issubclass(c, bpy.types.Panel):
                    new_panel_classes.append(c)

            new_types_set = set(new_types)
            for attr in bpy_types_post:
                if attr in bpy_types_pre:
                    continue
                c = getattr(bpy.types, attr)
                if c in new_types_set:
                    continue
                new_types.append(c)
                if issubclass(c, bpy.types.AddonPreferences):
                    addon_prefs_class = c
                if issubclass(c, bpy.types.Panel):
                    new_panel_classes.append(c)

            if instance:  # addon_utils.py用
                instance.register()

                draw_orig = None
                if addon_prefs_class:
                    if hasattr(addon_prefs_class, 'draw'):
                        def draw(self, context):
                            draw._draw(self, context)
                            instance.layout = self.layout
                            instance.draw(context)
                            del instance.layout

                        draw_orig = addon_prefs_class.draw
                    else:
                        def draw(self, context):
                            instance.layout = self.layout
                            instance.draw(context)
                            del instance.layout
                    addon_prefs_class.draw = draw
                    # TODO: 属性名で衝突の可能性
                    addon_prefs_class.register_info = instance

                else:
                    def draw(self, context):
                        instance.layout = self.layout
                        instance.draw(context)
                        del instance.layout

                    cls_ = instance.__class__
                    name = cls_.bl_idname.replace('.', '_').upper()
                    addon_prefs_class = type(
                        'AddonPreferences' + name,
                        (bpy.types.AddonPreferences,),
                        {'bl_idname': cls_.bl_idname,
                         'register_info': instance,
                         'draw': draw,
                         'is_temporary_class': True}
                    )
                    bpy.utils.register_class(addon_prefs_class)
                draw._draw = draw_orig

                instance.__class__.addon_preferences_class = \
                    addon_prefs_class

            wm = bpy.context.window_manager
            prop = wm.addon_property_groups.add()
            prop.name = cls.bl_idname

            if instance:
                instance.keymap_items_init(keymap_items)
                instance.keymap_items_load()
                instance.addon_classes_add(new_types)
                instance.panel_settings_init(new_panel_classes)
            else:
                cls.keymap_items_init(keymap_items)
                cls.keymap_items_load()
                cls.addon_classes_add(new_types)
                cls.panel_settings_init(new_panel_classes)

        _register._register = func

        cls_ = super()
        if hasattr(cls_, 'register_addon'):
            _register = cls_.register_addon(_register, **kwargs)

        return _register

    @classmethod
    def register_addon_ex(cls, module=None, instance=None):
        import functools
        return functools.partial(cls.register_addon, module=module,
                                 instance=instance)

    @classmethod
    def unregister_addon(cls, func, unregister_classes=False,
                         instance=None, **kwargs):
        import functools

        @functools.wraps(func)
        def _unregister():
            if instance:
                prefs_class = instance.__class__.addon_preferences_class
            else:
                prefs_class = cls

            if instance:
                instance.keymap_items_remove(remove_only_added=True)
                if unregister_classes:
                    instance.addon_classes_remove()
                else:
                    instance.addon_classes.clear()
                instance.panel_settings_restore()
            else:
                prefs_class.keymap_items_remove()
                if unregister_classes:
                    prefs_class.addon_classes_remove()
                else:
                    prefs_class.addon_classes.clear()
                cls.panel_settings_restore()

            wm = bpy.context.window_manager
            i = wm.addon_property_groups.find(cls.bl_idname)
            wm.addon_property_groups.remove(i)

            if instance:
                if getattr(prefs_class, 'is_temporary_class', None) is True:
                    bpy.utils.unregister_class(prefs_class)
                else:
                    if prefs_class.draw._draw:
                        prefs_class.draw = prefs_class.draw._draw
                    else:
                        delattr(prefs_class, 'draw')
                    delattr(prefs_class, 'register_info')

                instance.unregister()

            # TODO: funcを最初に呼んで、キーマップの削除を後回しにする
            func()

        _unregister._unregister = func

        c = super()
        if hasattr(c, 'unregister_addon'):
            _unregister = c.unregister_addon(_unregister, **kwargs)

        return _unregister

    @classmethod
    def unregister_addon_ex(cls, unregister_classes=False, instance=None):
        import functools
        return functools.partial(cls.unregister_addon,
                                 unregister_classes=unregister_classes,
                                 instance=instance)

    @classmethod
    def wrap_module(cls, module):
        """addon_utils.py用"""
        if getattr(module, 'bl_info', {}).get('name') in cls.IGRORE_ADDONS:
            return
        if not (hasattr(module, 'register') and hasattr(module, 'unregister')):
            return
        if hasattr(module.register, '_register'):
            return

        new_cls = cls.derive(module.__name__, lock_default_keymap_items=True)
        instance = new_cls()
        module.register = new_cls.register_addon(
            module.register, module.__name__, instance=instance)
        module.unregister = new_cls.unregister_addon(
            module.unregister, instance=instance)
