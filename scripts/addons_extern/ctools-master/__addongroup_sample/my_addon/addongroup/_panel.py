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


import collections.abc
from collections import OrderedDict
import contextlib

import bpy

from ._misc import Registerable

iface = bpy.app.translations.pgettext_iface


class OperatorPanelSettingUnset(Registerable, bpy.types.Operator):
    """特定Panelの一個の項目だけを戻す"""
    bl_idname = "wm.addonprefs_panel_setting_unset"
    bl_label = "Unset Panel Setting"
    bl_description = "Convert panel settings into ID properties " \
                     "(necessary for \"Save User Settings\")"
    bl_options = {'REGISTER', 'INTERNAL'}

    attribute = bpy.props.StringProperty()

    def execute(self, context):
        info_panels = context.info_panels
        panel = context.panel_setting
        info_panels.restore(panel.name, self.attribute)
        context.area.tag_redraw()
        return {'FINISHED'}


class OperatorPanelSettingsRestore(Registerable, bpy.types.Operator):
    """全て初期化"""
    bl_idname = "wm.addonprefs_panel_settings_restore"
    bl_label = "Restore Panel Settings"
    bl_description = "Restore panel settings and clear ID properties"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        info_panels = context.info_panels
        info_panels.restore_all()
        context.area.tag_redraw()
        return {'FINISHED'}


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
    ('scene', ('SCENE', "Scene")),
    ('render', ('RENDER', "Render")),
    ('render_layer', ('RENDER_LAYER', "Render Layers")),
    ('world', ('WORLD', "World")),
    ('object', ('OBJECT', "Object")),
    ('data', ('DATA', "Data")),
    ('material', ('MATERIAL', "Material")),
    ('texture', ('TEXTURE', "Texture")),
    ('particle', ('PARTICLES', "Particles")),
    ('physics', ('PHYSICS', "Physics")),
    ('bone', ('BONE', "Bone")),
    ('modifier', ('MODIFIER', "Modifiers")),
    ('constraint', ('CONSTRAINT', "Constraints")),
    ('bone_constraint', ('BONE_CONSTRAINT', "Bone Constraints")),
])

# Panel.bl_space_typeがVIEW_3Dの場合のPanel.bl_contextと
# Context.modeの対応。値はContext.modeのidentifierとname
bl_context_view3d = OrderedDict([
    ('mesh_edit', ('EDIT_MESH', "Mesh Edit")),  # 0
    ('curve_edit', ('EDIT_CURVE', "Curve Edit")),  # 1
    ('surface_edit', ('EDIT_SURFACE', "Surface Edit")),  # 2
    ('text_edit', ('EDIT_TEXT', "Text Edit")),  # 3
    ('armature_edit', ('EDIT_ARMATURE', "Armature Edit")),  # 4
    ('mball_edit', ('EDIT_METABALL', "Metaball Edit")),  # 5
    ('lattice_edit', ('EDIT_LATTICE', "Lattice Edit")),  # 6
    ('posemode', ('POSE', "Pose")),  # 7
    ('sculpt_mode', ('SCULPT', "Sculpt")),  # 8
    ('weightpaint', ('PAINT_WEIGHT', "Weight Paint")),  # 9
    ('vertexpaint', ('PAINT_VERTEX', "Vertex Paint")),  # 10
    ('imagepaint', ('PAINT_TEXTURE', "Texture Paint")),  # 11
    ('particlemode', ('PARTICLE', "Particle")),  # 12
    ('objectmode', ('OBJECT', "Object")),  # 13
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


def _prop_panel_bl_region_type_items(self, context):
    label = dict([('WINDOW', "Window"),
                  ('HEADER', "Header"),
                  ('CHANNELS', "Channels"),
                  ('TEMPORARY', "Temporary"),
                  ('UI', "UI"),
                  ('TOOLS', "Tools"),
                  ('TOOL_PROPS', "Tool Properties"),
                  ('PREVIEW', "Preview")]
                 )

    items = [(t, label[t], '') for t in area_region_types[self.bl_space_type]]
    _prop_panel_bl_region_type_items.items = items
    return items


def _prop_panel_bl_context_items(self, context):
    if self.bl_space_type == 'PROPERTIES':
        # buttons_main_region_draw()より
        # bl_space_typeが'PROPERTIES'の場合に使う
        items = [(k, k, "") for k in bl_context_properties]
        items = [('empty', "", "")] + items
    else:
        # view3d_tools_region_draw()より
        # これが有効なのはbl_space_typeが'VIEW_3D'でbl_region_typeが
        # 'TOOLS'の場合のみ
        items = [(k, v[1], "") for k, v in bl_context_view3d.items()]
        items = [('empty', "", "")] + items
    _prop_panel_bl_context_items.items = items
    return items


def _set_panel_attributes(panel_class, prop):
    for key in ["bl_label", "bl_category", "bl_space_type", "bl_region_type",
                "bl_context"]:
        value = getattr(prop, key)
        if key == "bl_category":
            if key not in prop and not prop.has_bl_category:
                if hasattr(panel_class, key):
                    delattr(panel_class, key)
                continue
        elif key == "bl_context":
            if key not in prop and not prop.has_bl_context:
                if hasattr(panel_class, key):
                    delattr(panel_class, key)
                continue
        if key == "bl_context" and value == "empty":
            value = ""
        setattr(panel_class, key, value)


def _reregister_panel_classs(prop):
    try:
        panel_class = getattr(bpy.types, prop.name)
        bpy.utils.unregister_class(panel_class)
        _set_panel_attributes(panel_class, prop)
        bpy.utils.register_class(panel_class)
    except Exception:
        import traceback
        traceback.print_exc()


def _prop_panel_get(attr):
    def _get(self):
        if attr in self:
            return self[attr]
        else:
            classes = self.__class__.owner_class._classes_[self["module_name"]]
            for cls in classes:
                if getattr(cls, "bl_idname", cls.__name__) == self.name:
                    break
            default = getattr(AddonPanelSettings, attr)[1].get("default", None)
            if attr in {"bl_label", "bl_category"}:
                return getattr(cls, attr, default)
            else:  # EnumProperty
                items = getattr(AddonPanelSettings, attr)[1]["items"]
                if isinstance(items, collections.abc.Callable):
                    items = items(self, bpy.context)
                    default = 0
                for i, item in enumerate(items):
                    if item[0] == getattr(cls, attr, None):
                        return i
                return default
    return _get


def _prop_panel_set(attr):
    def _set(self, value):
        self[attr] = value
    return _set


def _prop_panel_update(attr):
    def _update(self, context):
        if attr == "bl_space_type":
            self["bl_region_type"] = 0
            self["bl_context"] = 0
        # elif attr == "bl_region_type":
        #     if not self.bl_category:
        #         self["bl_category"] = "Tools"
        if self.reregister:
            _reregister_panel_classs(self)

    return _update


class AddonPanelSettings:
    owner_class = None

    reregister = bpy.props.BoolProperty(
        default=True
    )

    @contextlib.contextmanager
    def disable_reregister(self):
        self.reregister = False
        yield
        self.reregister = True

    module_name = bpy.props.StringProperty()

    bl_idname = bpy.props.StringProperty(
        get=lambda self: self.name)

    prop = bpy.types.Panel.bl_rna.properties["bl_label"]
    bl_label = bpy.props.StringProperty(
        name=prop.name,
        description=prop.description,
        default="",
        get=_prop_panel_get("bl_label"),
        set=_prop_panel_set("bl_label"),
        update=_prop_panel_update("bl_label"),
    )

    # NOTE: bl_categoryとbl_contextは省略可能属性
    prop = bpy.types.Panel.bl_rna.properties["bl_category"]
    bl_category = bpy.props.StringProperty(
        name=prop.name,
        description=prop.description,
        default="",
        get=_prop_panel_get("bl_category"),
        set=_prop_panel_set("bl_category"),
        update=_prop_panel_update("bl_category"),
    )

    """
    NOTE: values of bpy.types.Panel.bl_context

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
    prop = bpy.types.Panel.bl_rna.properties["bl_space_type"]
    bl_space_type = bpy.props.EnumProperty(
        name=prop.name,
        description=prop.description,
        items=(
            # ('EMPTY', "Empty", ""),
            ('VIEW_3D', "3D View", "3D viewport"),
            ('TIMELINE', "Timeline", "Timeline and playback controls"),
            ('GRAPH_EDITOR', "Graph Editor",
             "Edit drivers and keyframe interpolation"),
            ('DOPESHEET_EDITOR', "Dope Sheet",
             "Adjust timing of keyframes"),
            ('NLA_EDITOR', "NLA Editor", "Combine and layer Actions"),
            ('IMAGE_EDITOR', "UV/Image Editor",
             "View and edit images and UV Maps"),
            ('SEQUENCE_EDITOR', "Video Sequence Editor",
             "Video editing tools"),
            ('CLIP_EDITOR', "Movie Clip Editor", "Motion tracking tools"),
            ('TEXT_EDITOR', "Text Editor",
             "Edit scripts and in-file documentation"),
            ('NODE_EDITOR', "Node Editor",
             "Editor for node-based shading and compositing tools"),
            ('LOGIC_EDITOR', "Logic Editor", "Game logic editing"),
            ('PROPERTIES', "Properties",
             "Edit properties of active object and related data-blocks"),
            ('OUTLINER', "Outliner",
             "Overview of scene graph and all available data-blocks"),
            ('USER_PREFERENCES', "User Preferences",
             "Edit persistent configuration settings"),
            ('INFO', "Info",
             "Main menu bar and list of error messages "
             "(drag down to expand and display)"),
            ('FILE_BROWSER', "File Browser", "Browse for files and assets"),
            ('CONSOLE', "Python Console",
             "Interactive programmatic console for advanced editing "
             "and script development"),
        ),
        default='VIEW_3D',
        get=_prop_panel_get("bl_space_type"),
        set=_prop_panel_set("bl_space_type"),
        update=_prop_panel_update("bl_space_type"),
    )
    prop = bpy.types.Panel.bl_rna.properties["bl_region_type"]
    bl_region_type = bpy.props.EnumProperty(
        name=prop.name,
        description=prop.description,
        items=_prop_panel_bl_region_type_items,
        get=_prop_panel_get("bl_region_type"),
        set=_prop_panel_set("bl_region_type"),
        update=_prop_panel_update("bl_region_type"),
    )
    prop = bpy.types.Panel.bl_rna.properties["bl_context"]
    bl_context = bpy.props.EnumProperty(
        name=prop.name,
        description=prop.description,
        items=_prop_panel_bl_context_items,
        get=_prop_panel_get("bl_context"),
        set=_prop_panel_set("bl_context"),
        update=_prop_panel_update("bl_context"),
    )
    del prop

    has_bl_context = bpy.props.BoolProperty()
    has_bl_category = bpy.props.BoolProperty()

    @classmethod
    def new_class(cls, owner_class):
        namespace = {
            "owner_class": owner_class,
        }
        return type("AddonPanelSettings",
                    (cls, bpy.types.PropertyGroup),
                    namespace)


class AddonPanels:
    owner_class = None
    default_settings = None  # CollectionProperty(type=AddonPanelSettings)
    current_settings = None  # CollectionProperty(type=AddonPanelSettings)

    show_panels = bpy.props.BoolProperty(
        name='Show Panels',
    )

    def get_class(self, bl_idname):
        if self.name not in self.owner_class._classes_:
            return None
        for c in self.owner_class._classes_[self.name]:
            if getattr(c, "bl_idname", c.__name__) == bl_idname:
                return c

    def init(self):
        addon_prefs = self.owner_class.get_instance()
        info_panels = addon_prefs.info_panels[self.name]
        info_panels.default_settings.clear()

        if self.name in self.owner_class._classes_:
            panel_classes = [c for c in self.owner_class._classes_[self.name]
                             if issubclass(c, bpy.types.Panel)]
        else:
            panel_classes = []
        for panel_class in panel_classes:
            prop = info_panels.default_settings.add()
            with prop.disable_reregister():
                prop.name = getattr(panel_class, "bl_idname",
                                    panel_class.__name__)
                prop.bl_label = panel_class.bl_label
                prop.module_name = self.name
                if hasattr(panel_class, "bl_category"):
                    prop.bl_category = panel_class.bl_category
                    prop.has_bl_category = True
                # else:
                #     prop.bl_category = ""
                prop.bl_space_type = panel_class.bl_space_type
                prop.bl_region_type = panel_class.bl_region_type
                if hasattr(panel_class, "bl_context"):
                    value = panel_class.bl_context
                    if value == "":
                        value = "empty"
                    prop.bl_context = value
                    prop.has_bl_context = True
                # else:
                #     prop.bl_context = "empty"
            if prop.name not in info_panels.current_settings:
                p = info_panels.current_settings.add()
                p.name = prop.name
                p.module_name = self.name
        i = 0
        for prop in list(info_panels.current_settings):
            if prop.name not in info_panels.default_settings:
                info_panels.current_settings.remove(i)
            else:
                prop.module_name = self.name
                p = info_panels.default_settings[prop.name]
                prop.has_bl_category = p.has_bl_category
                prop.has_bl_context = p.has_bl_context
                i += 1

    def load(self, only_changed=False):
        addon_prefs = self.owner_class.get_instance()
        for prop in addon_prefs.info_panels[self.name].current_settings:
            if only_changed:
                reregister = False
                for attr in ["bl_label", "bl_category", "bl_space_type",
                             "bl_region_type", "bl_context"]:
                    if attr in prop:
                        reregister = True
            else:
                reregister = True
            if reregister:
                _reregister_panel_classs(prop)

    def restore(self, panel_bl_idname, attr):
        """とあるパネルの一属性を初期設定に戻す。UIのXボタンを押した時の動作"""
        addon_prefs = self.owner_class.get_instance()
        info_panels = addon_prefs.info_panels[self.name]
        prop = info_panels.current_settings.get(panel_bl_idname)
        default_prop = info_panels.default_settings.get(panel_bl_idname)
        setattr(prop, attr, getattr(default_prop, attr))
        if attr in prop:  # prop.property_unset(attr) is not working
            del prop[attr]

    def restore_all(self, only_classes=False):
        """初期設定に戻す"""
        addon_prefs = self.owner_class.get_instance()
        info_panels = addon_prefs.info_panels[self.name]

        if only_classes:
            for prop in info_panels.default_settings:
                c = self.get_class(prop.name)
                if c:
                    _set_panel_attributes(c, prop)
            return

        for prop in info_panels.current_settings:
            for attr in ["bl_label", "bl_category", "bl_space_type",
                         "bl_region_type", "bl_context"]:
                if attr in prop:  # prop.property_unset(attr) is not working
                    del prop[attr]
        for prop in info_panels.default_settings:
            _reregister_panel_classs(prop)

    def draw(self, context, layout, box=True):
        if not self.show_panels:
            return

        addon_prefs = self.owner_class.get_instance()
        info_panels = addon_prefs.info_panels[self.name]

        if box:
            column = layout.column().box()
        else:
            column = layout.column()
        column.context_pointer_set("info_panels", info_panels)

        row = column.row()
        split = row.split(0.7)
        split.row()
        row = split.row()
        sp = row.split(align=True)

        sub = sp.row(align=True)
        is_changed = False
        keys = {"bl_label", "bl_category", "bl_space_type", "bl_region_type",
                "bl_context"}
        for prop in self.current_settings:
            if set(prop.keys()) & keys:
                is_changed = True
                break
        sub.enabled = is_changed
        sub.operator(OperatorPanelSettingsRestore.bl_idname, text="Restore")

        for prop in self.current_settings:
            def is_changed(attr):
                default_prop = self.default_settings[prop.name]
                return getattr(prop, attr) != getattr(default_prop, attr)

            prop_box = column.box()
            prop_box.context_pointer_set("panel_setting", prop)

            split = prop_box.split()
            col = split.column()

            row = col.box().row()
            sp = row.split(0.32)
            sub = sp.row()
            sub.label(iface("ID Name") + ":", translate=False)
            sub = sp.row()
            sub.label(prop.name, translate=False)

            row = col.box().row()
            row.prop(prop, "bl_label")
            if is_changed("bl_label"):
                sub = row.row()
                op = sub.operator(OperatorPanelSettingUnset.bl_idname,
                                  text="", icon='X', emboss=False)
                op.attribute = "bl_label"

            row = col.box().row()
            row.prop(prop, "bl_category")
            if is_changed("bl_category"):
                sub = row.row()
                op = sub.operator(OperatorPanelSettingUnset.bl_idname,
                                  text="", icon='X', emboss=False)
                op.attribute = "bl_category"

            col = split.column()

            row = col.box().row()
            row.prop(prop, "bl_space_type")
            if is_changed("bl_space_type"):
                sub = row.row()
                op = sub.operator(OperatorPanelSettingUnset.bl_idname,
                                  text="", icon='X', emboss=False)
                op.attribute = "bl_space_type"

            row = col.box().row()
            row.prop(prop, "bl_region_type")
            if is_changed("bl_region_type"):
                sub = row.row()
                op = sub.operator(OperatorPanelSettingUnset.bl_idname,
                                  text="", icon='X', emboss=False)
                op.attribute = "bl_region_type"

            row = col.box().row()
            row.prop(prop, "bl_context")
            if is_changed("bl_context"):
                sub = row.row()
                op = sub.operator(OperatorPanelSettingUnset.bl_idname,
                                  text="", icon='X', emboss=False)
                op.attribute = "bl_context"

    @classmethod
    def init_collection(cls):
        addon_prefs = cls.owner_class.get_instance()
        info_panels = addon_prefs.info_panels
        if "" not in info_panels:
            item = info_panels.add()
            item.name = ""
        mod_names = [mod.__name__.split(".")[-1]
                     for mod in cls.owner_class._fake_submodules_.values()]
        for mod_name in mod_names:
            if mod_name not in info_panels:
                item = info_panels.add()
                item.name = mod_name
        for item in list(info_panels):
            if item.name != "" and item.name not in mod_names:
                info_panels.remove(info_panels.find(item.name))
        for item in info_panels:
            item.init()
            item.load(only_changed=True)

    @classmethod
    def register(cls):
        classes = [
            OperatorPanelSettingUnset,
            OperatorPanelSettingsRestore,
        ]
        for c in classes:
            c.register_class()

    @classmethod
    def unregister(cls):
        classes = [
            OperatorPanelSettingUnset,
            OperatorPanelSettingsRestore,
        ]
        for c in classes[::-1]:
            c.unregister_class()

    @classmethod
    def new_class(cls, owner_class):
        t = AddonPanelSettings.new_class(owner_class)
        namespace = {
            "owner_class": owner_class,
            "default_settings": bpy.props.CollectionProperty(type=t),
            "current_settings": bpy.props.CollectionProperty(type=t)
        }
        return type("AddonPanels",
                    (cls, bpy.types.PropertyGroup),
                    namespace)
