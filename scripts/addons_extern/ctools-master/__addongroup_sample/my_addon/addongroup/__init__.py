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


"""
Helper module for grouping add-ons
See README.md
"""


from collections import OrderedDict
import importlib
import os
import re
import sys
import traceback

if "bpy" in locals():
    importlib.reload(_misc)
    importlib.reload(_keymap)
    importlib.reload(_class)
    importlib.reload(_panel)
else:
    from . import _misc
    from . import _keymap
    from . import _class
    from . import _panel
from ._keymap import AddonKeyConfig
from ._class import AddonClasses
from ._panel import AddonPanels


import bpy
import addon_utils


__all__ = [
    "AddonInfo",
    "AddonGroup",
    "register_module",
    "unregister_module",
]


"""
NOTE: invalid: get_instance().bl_idname
      ok:      get_instance().__class__.bl_idname
"""


error_message = ""


class WM_OT_nested_addon_enable(_misc.Registerable, bpy.types.Operator):
    # for display error messages with popup
    bl_idname = "wm.nested_addon_enable"
    bl_label = "Enable Add-on"
    bl_description = "Enable an add-on"

    module = bpy.props.StringProperty(
        name="Module",
        description="Module name of the add-on to enable",
    )

    def execute(self, context):
        c = context.addon_preferences.addons.__class__
        c.error = ""
        setattr(context.addon_preferences.addons, "use_" + self.module, True)
        if c.error:
            self.report({'ERROR'}, c.error)
            c.error = ""
            return {'CANCELLED'}
        else:
            return {"FINISHED"}


class WM_OT_nested_addon_disable(_misc.Registerable, bpy.types.Operator):
    # for display error messages with popup
    bl_idname = "wm.nested_addon_disable"
    bl_label = "Disable Add-on"
    bl_description = "Disable an add-on"

    module = bpy.props.StringProperty(
        name="Module",
        description="Module name of the add-on to disable",
    )

    def execute(self, context):
        c = context.addon_preferences.addons.__class__
        c.error = ""
        setattr(context.addon_preferences.addons, "use_" + self.module, False)
        if c.error:
            self.report({'ERROR'}, c.error)
            c.error = ""
            return {'CANCELLED'}
        else:
            return {"FINISHED"}


def fake_module(mod_name, mod_path, speedy=True, force_support=None,
                quiet=True):
    """fake module importing
    source: scripts/modules/addon_utils.py: modules_refresh()
    fix it not to use error_encoding. add "quiet" argument
    """
    if 0:
        global error_encoding

    if bpy.app.debug_python:
        print("fake_module", mod_path, mod_name)
    import ast
    ModuleType = type(ast)
    try:
        file_mod = open(mod_path, "r", encoding='UTF-8')
    except OSError as e:
        print("Error opening file %r: %s" % (mod_path, e))
        return None

    with file_mod:
        if speedy:
            lines = []
            line_iter = iter(file_mod)
            l = ""
            while not l.startswith("bl_info"):
                try:
                    l = line_iter.readline()
                except UnicodeDecodeError as e:
                    if 0:
                        if not error_encoding:
                            error_encoding = True
                            print("Error reading file as UTF-8:", mod_path, e)
                    else:
                        print("Error reading file as UTF-8:", mod_path, e)
                    return None

                if len(l) == 0:
                    break
            while l.rstrip():
                lines.append(l)
                try:
                    l = line_iter.readline()
                except UnicodeDecodeError as e:
                    if 0:
                        if not error_encoding:
                            error_encoding = True
                            print("Error reading file as UTF-8:", mod_path,
                                  e)
                    else:
                        print("Error reading file as UTF-8:", mod_path, e)
                    return None

            data = "".join(lines)

        else:
            data = file_mod.read()
    del file_mod

    try:
        ast_data = ast.parse(data, filename=mod_path)
    except:
        print("Syntax error 'ast.parse' can't read %r" % mod_path)
        import traceback
        traceback.print_exc()
        ast_data = None

    body_info = None

    if ast_data:
        for body in ast_data.body:
            if body.__class__ == ast.Assign:
                if len(body.targets) == 1:
                    if getattr(body.targets[0], "id", "") == "bl_info":
                        body_info = body
                        break

    if body_info:
        try:
            mod = ModuleType(mod_name)
            mod.bl_info = ast.literal_eval(body.value)
            mod.__file__ = mod_path
            mod.__time__ = os.path.getmtime(mod_path)
        except:
            print("AST error parsing bl_info for %s" % mod_name)
            import traceback
            traceback.print_exc()
            raise

        if force_support is not None:
            mod.bl_info["support"] = force_support

        return mod
    else:
        if not quiet:
            print("fake_module: addon missing 'bl_info' "
                  "gives bad performance!: %r" % mod_path)
        return None


class NestedAddons:
    """For dynamically adding attributes

    Dynamically added attributes:
        "prefs_" + module name
        "use_" + module name
        "show_expanded_" + module name
    """

    owner_class = None

    error = ""

    ui_align_box_draw = bpy.props.BoolProperty(
        name="Box Draw",
        description="If applied patch: patch/ui_layout_box.patch",
        default=False)
    ui_use_indent_draw = bpy.props.BoolProperty(
        name="Indent",
        default=True)
    ui_show_private = bpy.props.BoolProperty(
        name="Show Hidden",
        default=False)

    ui_use_addon_filter = bpy.props.BoolProperty(
        name="Filter",
        default=False)

    def _prop_addon_search_get(self):
        return getattr(self, "_ui_addon_search", "")

    def _prop_addon_search_set(self, value):
        setattr(self.__class__, "_ui_addon_search", value)

    def _prop_addon_filter_items(self, context):
        items = [('All', "All", "All Add-ons"),
                 ('Enabled', "Enabled", "All Enabled Add-ons"),
                 ('Disabled', "Disabled", "All Disabled Add-ons"),
                 ]

        items_unique = set()

        for mod_name, fake_mod in self.owner_class._fake_submodules_.items():
            info = addon_utils.module_bl_info(fake_mod)
            if info["category"]:
                items_unique.add(info["category"])

        items.extend([(cat, cat, "") for cat in sorted(items_unique)])
        self.__class__._ui_addon_filter_items = items
        return items

    def _prop_addon_filter_get(self):
        return getattr(self, "_ui_addon_filter", 0)

    def _prop_addon_filter_set(self, value):
        setattr(self.__class__, "_ui_addon_filter", value)

    ui_addon_search = bpy.props.StringProperty(
        name="Search",
        description="Search within the selected filter. "
                    "If startswith \"/\"/, use path search ",
        options={'TEXTEDIT_UPDATE'},
        get=_prop_addon_search_get,
        set=_prop_addon_search_set,
    )
    ui_addon_filter = bpy.props.EnumProperty(
        items=_prop_addon_filter_items,
        name="Category",
        description="Filter add-ons by category",
        get=_prop_addon_filter_get,
        set=_prop_addon_filter_set,
    )

    @classmethod
    def new_class(cls, owner_class):
        return type("NestedAddons",
                    (cls, bpy.types.PropertyGroup),
                    {"owner_class": owner_class})


class _AddonInfo:
    _ADDON_GROUP_ = 1.0

    bl_idname = ""

    submodules = ()
    """str list of sub modules.
    If None is specified, all files and directories included are targeted.

    Sub modules whose heads begin with _ are not displayed in UserPreference
    by default. They are displayed when enable the 'Show Hidden' option.

    :type: list[str]
    """

    # Initialize at register_addon()
    # addons = bpy.props.PointerProperty(
    #     type=NestedAddons.derive())
    addons = None
    """:type: NestedAddons"""

    info_keyconfigs = None
    """:type: list[AddonKeyConfig]"""
    info_classes = None
    """:tyre: list[AddonClasses]"""
    info_panels = None
    """:type: list[AddonPanels]"""

    # Initialize at register()
    _fake_submodules_ = None  # OrderedDict()
    """:type: dict"""
    _classes_ = None
    """Included submodule classes.
    :type: dict[str | list]
    """
    _keymap_items_ = None
    """:type: dict[str|list[(str, int)]]"""

    @classmethod
    def get_instance(cls):
        """return instance
        :rtype: AddonPreferences
        """
        U = bpy.context.user_preferences
        if cls.bl_idname in U.addons:
            return U.addons[cls.bl_idname].preferences
        else:  # wm.read_factory_settings()
            return None

    @classmethod
    def get_keymap(cls, name, keyconfig="addon"):
        """Return result of KeyMaps.new()
        :type name: str
        :param keyconfig: "addon" or "user" or "blender" or
                          "default"(same as "blender")
        :type keyconfig: str
        :rtype: bpy.types.KeyMap
        """
        return AddonKeyConfig.get_keymap(name, keyconfig)

    def _draw_addon_info(self, context, layout, submodule=""):
        column = layout.column()
        column.context_pointer_set("addon_preferences", self)

        info_keyconfig = self.info_keyconfigs[submodule]
        info_classes = self.info_classes[submodule]
        info_panels = self.info_panels[submodule]
        show_keymaps = info_keyconfig.kc_show_keymaps
        show_classes = info_classes.show_classes
        show_panels = info_panels.show_panels

        row = column.row()
        split = row.split()

        # Keyconfig
        sub = split.row()
        icon = 'TRIA_DOWN' if show_keymaps else 'TRIA_RIGHT'
        sub.prop(info_keyconfig, "kc_show_keymaps", text="", icon=icon,
                 emboss=False)
        num = len(info_keyconfig[info_keyconfig.ITEMS])
        text = "{} Key Map Items".format(num)
        sub.label(text)

        # Classes
        sub = split.row()
        icon = 'TRIA_DOWN' if show_classes else 'TRIA_RIGHT'
        sub.prop(info_classes, "show_classes", text="", icon=icon,
                 emboss=False)
        text = "{} Classes".format(len(self._classes_[submodule]))
        sub.label(text)

        # Panels
        sub = split.row()
        icon = 'TRIA_DOWN' if show_panels else 'TRIA_RIGHT'
        sub.prop(info_panels, "show_panels", text="", icon=icon,
                 emboss=False)
        num = len(info_panels.default_settings)
        text = "{} Panels".format(num)
        sub.label(text)

        if show_keymaps or show_classes or show_panels:
            if show_keymaps:
                info_keyconfig.draw(context, column.column())
            if show_classes:
                info_classes.draw(context, column.column())
            if show_panels:
                info_panels.draw(context, column.column())

    @classmethod
    def _verify_info_collections(cls):
        addon_prefs = cls.get_instance()

        keyconfigs = addon_prefs.info_keyconfigs
        if "" not in keyconfigs:
            item = keyconfigs.add()
            item.name = ""
            item.init()

        classes = addon_prefs.info_classes
        if "" not in classes:
            item = classes.add()
            item.name = ""

        panels = addon_prefs.info_panels
        if "" not in panels:
            item = panels.add()
            item.name = ""
            item.init()

    @classmethod
    def _init_dynamic_types(cls):
        """generare and register classes"""

        # set NestedAddons
        t = NestedAddons.new_class(cls)
        bpy.utils.register_class(t)
        cls.addons = bpy.props.PointerProperty(type=t)

        # set AddonKeyConfig
        keyconfig_type = AddonKeyConfig.new_class(cls)
        bpy.utils.register_class(keyconfig_type)
        cls.info_keyconfigs = bpy.props.CollectionProperty(type=keyconfig_type)
        """:type: list[AddonKeyConfig]"""

        # set AddonClasses
        classes_type = AddonClasses.new_class(cls)
        bpy.utils.register_class(classes_type)
        cls.info_classes = bpy.props.CollectionProperty(type=classes_type)
        """:type: list[AddonClasses]"""

        # set AddonPanels
        panels_type = AddonPanels.new_class(cls)
        bpy.utils.register_class(panels_type.default_settings[1]["type"])
        bpy.utils.register_class(panels_type)
        cls.info_panels = bpy.props.CollectionProperty(type=panels_type)
        """:type: list[AddonPanels]"""

    @classmethod
    def _delete_dynamic_types(cls):
        t = cls.addons[1]["type"]
        bpy.utils.unregister_class(t)

        t = cls.info_keyconfigs[1]["type"]
        bpy.utils.unregister_class(t)

        t = cls.info_classes[1]["type"]
        bpy.utils.unregister_class(t)

        t = cls.info_panels[1]["type"]
        bpy.utils.unregister_class(t)
        bpy.utils.unregister_class(t.default_settings[1]["type"])

        cls.addons = None
        cls.info_keyconfigs = None
        cls.info_classes = None
        cls.info_panels = None

    @classmethod
    def _attach_to_preferences(cls, module, classes):
        addon_prefs_type = None
        for c in classes:
            if issubclass(c, bpy.types.AddonPreferences):
                addon_prefs_type = c

        if addon_prefs_type:
            bpy.utils.unregister_class(addon_prefs_type)
            addon_prefs_type.addons = cls.addons
            addon_prefs_type.info_keyconfigs = cls.info_keyconfigs
            addon_prefs_type.info_classes = cls.info_classes
            addon_prefs_type.info_panels = cls.info_panels
            bpy.utils.register_class(addon_prefs_type)

            cls.register()

            addon_prefs_type._classes_ = cls._classes_
            addon_prefs_type._keymap_items_ = cls._keymap_items_
            addon_prefs_type._fake_submodules_ = cls._fake_submodules_
            addon_prefs_type._draw_ex = cls._draw_ex
            addon_prefs_type._draw_addon_info = cls._draw_addon_info

            draw_orig = getattr(addon_prefs_type, "draw", None)
            if draw_orig:
                def draw(self, context):
                    self._draw_orig(context)
                    self._draw_ex(context, draw_bases=False)
            else:
                def draw(self, context):
                    self._draw_ex(context, draw_bases=False)

            addon_prefs_type._draw_orig = draw_orig
            addon_prefs_type.draw = draw
        else:
            bpy.utils.register_class(cls)

        setattr(module, "_ADDON_PREFS_", addon_prefs_type)

    @classmethod
    def _detach_from_preferences(cls, module):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
        if getattr(module, "_ADDON_PREFS_", None):
            prefs = module._ADDON_PREFS_
            if prefs._draw_orig:
                prefs.draw = prefs._draw_orig
            else:
                del prefs.draw
            del prefs.addons
            del prefs.info_keyconfigs
            del prefs.info_classes
            del prefs.info_panels
            del prefs._classes_
            del prefs._keymap_items_
            del prefs._fake_submodules_
            del prefs._draw_ex
            del prefs._draw_addon_info
            delattr(module, "_ADDON_PREFS_")

    @classmethod
    def _get_all_addon_keymap_items(cls):
        kc = bpy.context.window_manager.keyconfigs.addon
        if not kc:
            return []

        items = []
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                items.append((km, kmi))
        return items

    @classmethod
    def register_addon(cls, func, module=None):
        """decorator for addon register function.

        e.g.
        @AddonGroup.register_addon
        def register():
            ...
        """
        import functools

        @functools.wraps(func)
        def register():
            cls._init_dynamic_types()

            # get all registered classes
            prev_classes = set(bpy.utils._bpy_module_classes(
                cls.bl_idname, is_registered=True))

            # get all keymap items
            prev_km_items = [(item[0].name, item[1].id)
                             for item in cls._get_all_addon_keymap_items()]

            # register()
            func()

            # get new classes
            post_classes = set(bpy.utils._bpy_module_classes(
                cls.bl_idname, is_registered=True))
            classes = [c for c in post_classes if c not in prev_classes]
            if module:
                cls._attach_to_preferences(module, classes)
            cls._classes_[""] = classes

            # get new keymap items
            post_km_items = [(item[0].name, item[1].id)
                             for item in cls._get_all_addon_keymap_items()]
            km_items = [item for item in post_km_items
                        if item not in set(prev_km_items)]
            cls._keymap_items_[""] = km_items

            # init CollectionProperty
            cls.info_keyconfigs[1]["type"].init_collection()
            cls.info_classes[1]["type"].init_collection()
            cls.info_panels[1]["type"].init_collection()

        register._register = func
        setattr(register, "_ADDON_GROUP_", None)

        return register

    @classmethod
    def unregister_addon(cls, func, module=None):
        """decorator for addon unregister function.

        e.g.
        @AddonGroup.unregister_addon
        def unregister():
            ...
        """
        import functools

        @functools.wraps(func)
        def unregister():
            addon_prefs = cls.get_instance()

            # restore panels
            for item in addon_prefs.info_panels:
                item.restore_all(only_classes=True)

            # get addon keymap items
            keyconfig_items = []
            for keyconfig in addon_prefs.info_keyconfigs:
                for item in keyconfig[keyconfig.ITEMS]:
                    keyconfig_items.append([item["keymap"], item["id"]])

            # unregister()
            func()

            if module:
                cls._detach_from_preferences(module)

            # remove keymap items that still exist
            for item in keyconfig_items:
                km_name, kmi_id = item
                km = keyconfig.get_keymap(km_name)
                if km:
                    for kmi in km.keymap_items:
                        if kmi.id == kmi_id:
                            keyconfig.remove_item(kmi)

            cls._delete_dynamic_types()

        unregister._unregister = func

        return unregister

    @classmethod
    def wrap_module(cls, module):
        """addon_utils.py用"""
        if not (hasattr(module, "register") and hasattr(module, "unregister")):
            return
        if hasattr(module.register, "_ADDON_GROUP_"):
            return

        new_cls = type(cls.__name__, (cls, bpy.types.AddonPreferences),
                       {"bl_idname": module.__name__})
        module.register = new_cls.register_addon(
            module.register, module=module)
        module.unregister = new_cls.unregister_addon(
            module.unregister, module=module)


class AddonInfo(_AddonInfo):
    def _draw_ex(self, context, draw_bases=True):
        if draw_bases:
            c = super()
            if hasattr(c, "draw"):
                c.draw(context)
        self._draw_addon_info(context, self.layout, submodule="")

    def draw(self, context):
        self._draw_ex(context)

    @classmethod
    def register(cls):
        cls._fake_submodules_ = {}
        cls._classes_ = {}
        cls._keymap_items_ = {}

        cls._verify_info_collections()

        c = super()
        if hasattr(c, "register"):
            c.register()

    @classmethod
    def unregister(cls):
        U = bpy.context.user_preferences
        if cls.bl_idname not in U.addons:  # wm.read_factory_settings()
            return

        cls._classes_.clear()
        cls._keymap_items_.clear()
        cls._fake_submodules_.clear()

        c = super()
        if hasattr(c, "unregister"):
            c.unregister()


class AddonGroup(_AddonInfo):
    """Create a hierarchical add-on.
    """

    # def __getattribute__(self, name):
    #     try:
    #         return super().__getattribute__(name)
    #     except AttributeError:
    #         m = re.match("(use_|show_expanded_|)(.*)", name)
    #         prefix, base = m.groups()
    #         addons = super().__getattribute__("addons")
    #         if base in self._fake_submodules_:
    #             mod = self._fake_submodules_[base]
    #             attr = prefix + self.mod_to_attr(mod)
    #             return getattr(addons, attr)
    #         else:
    #             raise

    # def __setattr__(self, name, value):
    #     def is_bpy_props(val):
    #         """return True if argument:val is in a format such as
    #         (bpy.props.BoolProperty, {name="Name", default="True"})
    #         """
    #         try:
    #             t, kwargs = val
    #             props = [getattr(bpy.props, attr) for attr in dir(bpy.props)]
    #             return t in props and isinstance(kwargs, dict)
    #         except:
    #             return False
    #
    #     prefix, base = re.match("(use_|show_expanded_|)(.*)", name).groups()
    #     addons = self.addons
    #     if base in self._fake_submodules_:
    #         mod = self._fake_submodules_[base]
    #         attr = prefix + self.mod_to_attr(mod)
    #         if is_bpy_props(value):
    #             setattr(addons.__class__, attr, value)
    #         else:
    #             setattr(addons, attr, value)
    #     else:
    #         super().__setattr__(name, value)
    #
    # def __delattr__(self, name):
    #     prefix, base = re.match("(use_|show_expanded_|)(.*)", name).groups()
    #     addons = self.addons
    #     if base in self._fake_submodules_:
    #         mod = self._fake_submodules_[base]
    #         attr = prefix + self.mod_to_attr(mod)
    #         delattr(addons.__class__, attr)
    #     else:
    #         super().__delattr__(name)
    #
    # def __dir__(self):
    #     attrs = list(super().__dir__())
    #     addons = self.addons
    #     for name in self._fake_submodules_:
    #         mod = self._fake_submodules_[name]
    #         attr = self.mod_to_attr(mod)
    #         for pre in ("", "use_", "show_expanded_"):
    #             n = pre + attr
    #             if hasattr(addons, n):
    #                 attrs.append(pre + name)
    #     return attrs

    @classmethod
    def __get_instance(cls, module="", *, root=False, parent=False):
        """return instance or str
        :rtype: AddonPreferences | str
        """
        if root and parent:
            raise ValueError()
        if module and (root or parent):
            raise ValueError()
        if not cls.is_registered:
            raise ValueError("{} is not registered".format(cls))
        U = bpy.context.user_preferences
        attrs = cls.bl_idname.split(".")

        if module:
            m = re.match("(\.*)(.*)", module)
            if m.group(1):
                num = len(m.group(1))
                if num > 1:
                    attrs = attrs[:-(num - 1)]
            attrs.extend(m.group(2).split("."))

        path = "bpy.context.user_preferences.addons['" + attrs[0] + \
               "'].preferences"
        if attrs[0] not in U.addons:  # wm.read_factory_settings()
            return None, path
        addon_prefs = U.addons[attrs[0]].preferences
        if not addon_prefs:
            return None, path
        if root:
            return addon_prefs, path
        for attr in (attrs[1:-1] if parent else attrs[1:]):
            addon_prefs = getattr(addon_prefs.addons, "prefs_" + attr, None)
            path += ".addons.prefs_" + attr
            if not addon_prefs:
                return None, path
        return addon_prefs, path

    @classmethod
    def get_instance(cls, module="", *, root=False, parent=False):
        """return instance
        :rtype: AddonPreferences
        """
        addon_prefs, path = cls.__get_instance(module, root=root, parent=parent)
        return addon_prefs

    @classmethod
    def get_instance_path(cls, module="", *, root=False, parent=False):
        """return instance path
        :rtype: str
        """
        addon_prefs, path = cls.__get_instance(module, root=root, parent=parent)
        return path

    @classmethod
    def __generate_fake_submodules(cls):
        fake_modules = []
        mod = sys.modules[cls.bl_idname]
        if os.path.basename(mod.__file__) != "__init__.py":
            # TODO: zip file
            return OrderedDict()
        addon_dir = os.path.dirname(mod.__file__)
        module_names = bpy.path.module_names(addon_dir)

        def sort_func(item):
            name, path = item
            if cls.submodules is not None:
                if name in cls.submodules:
                    return cls.submodules.index(name)
                else:
                    return len(cls.submodules) + module_names.index(item)
            else:
                return module_names.index(item)

        for mod_name, mod_path in sorted(module_names, key=sort_func):
            # Skip same files and undesignated modules.
            if os.path.realpath(mod_path) == os.path.realpath(__file__):
                continue
            else:
                # check hard link and symbolic link. only unix and windows
                try:
                    if os.path.samefile(mod_path, __file__):
                        continue
                except:
                    pass
            if cls.submodules is not None:
                if mod_name not in cls.submodules:
                    continue

            if cls._fake_submodules_:
                mod = cls._fake_submodules_.get(mod_name)
                if mod:
                    if mod.__time__ != os.path.getmtime(mod_path):
                        print("reloading addon:",
                              mod.__name__,
                              mod.__time__,
                              os.path.getmtime(mod_path),
                              mod_path,
                              )
            mod = fake_module(cls.bl_idname + "." + mod_name, mod_path)
            if mod:
                fake_modules.append(mod)

        fake_modules.sort(
            key=lambda mod: (mod.bl_info.get("category", ""),
                             mod.bl_info["name"]))
        fake_modules = OrderedDict(
            [(mod.__name__[len(cls.bl_idname) + 1:], mod)
             for mod in fake_modules])

        if cls.submodules is not None:
            for name in cls.submodules:
                if name not in fake_modules:
                    print("Submodule not found: {}.{}".format(
                          cls.bl_idname, name))
        return fake_modules

    @classmethod
    def reload_submodules(cls):
        """
        e.g.
        if "bpy" in locals():
            import importlib
            AddonGroup.reload_submodules()
        """
        _fake_submodules_ = cls.__generate_fake_submodules()
        for fake_mod in _fake_submodules_.values():
            try:
                mod_name = fake_mod.__name__
                if mod_name in sys.modules:
                    mod = importlib.import_module(mod_name)
                    # print("Reloading:", mod)
                    importlib.reload(mod)
            except:
                traceback.print_exc()

    @classmethod
    def __init_addons_attributes(cls):
        # Add PointerProperty to parent
        if "." in cls.bl_idname:
            parent_prefs = cls.get_instance(parent=True)
            mod_name = cls.bl_idname.split(".")[-1]
            prop = bpy.props.PointerProperty(type=cls)
            setattr(parent_prefs.addons.__class__, "prefs_" + mod_name, prop)

        addon_prefs = cls.get_instance()

        # Add usd_***, show_expanded_***
        for fake_mod in cls._fake_submodules_.values():
            info = fake_mod.bl_info

            def gen_func(fake_mod):
                def update(self, context):
                    short_name = fake_mod.__name__.split(".")[-1]
                    mod_name = fake_mod.__name__
                    try:
                        mod = importlib.import_module(mod_name)
                    except:
                        traceback.print_exc()
                        cls.__disable_nested_addon(None, short_name, True)
                    else:
                        if getattr(addon_prefs.addons, "use_" + short_name):
                            cls.__enable_nested_addon(mod)
                        else:
                            cls.__disable_nested_addon(mod, short_name, True)
                return update

            update = gen_func(fake_mod)
            prop = bpy.props.BoolProperty(
                name=info["name"],
                description=info.get("description", "").rstrip("."),
                update=update,
            )
            mod_name = fake_mod.__name__.split(".")[-1]
            setattr(addon_prefs.addons.__class__, "use_" + mod_name, prop)

            if 0:
                def gen_func(fake_mod):
                    def fget(self):
                        bl_info = addon_utils.module_bl_info(fake_mod)
                        return int(bl_info["show_expanded"])

                    def fset(self, value):
                        bl_info = addon_utils.module_bl_info(fake_mod)
                        bl_info["show_expanded"] = bool(value)

                    return fget, fset

                fget, fset = gen_func(fake_mod)
                prop = bpy.props.BoolProperty(get=fget, set=fset)
            else:
                prop = bpy.props.BoolProperty()
            setattr(addon_prefs.addons.__class__,
                    "show_expanded_" + mod_name, prop)

    @classmethod
    def __delete_addons_attributes(cls):
        addon_prefs = cls.get_instance()
        parent_addon_prefs = cls.get_instance(parent=True)

        # Delete PointerProperty
        if "." in cls.bl_idname:
            mod_name = cls.bl_idname.split(".")[-1]
            delattr(parent_addon_prefs.addons.__class__, "prefs_" + mod_name)

        # Delete usd_***, show_expanded_***
        dyn_class = addon_prefs.addons.__class__
        for fake_mod in cls._fake_submodules_.values():
            mod_name = fake_mod.__name__.split(".")[-1]
            delattr(dyn_class, "use_" + mod_name)
            delattr(dyn_class, "show_expanded_" + mod_name)

    @classmethod
    def __enable_nested_addon(cls, mod):
        if not hasattr(mod, "__addon_enabled__"):
            mod.__addon_enabled__ = False

        if not mod.__addon_enabled__:
            # get all registered classes
            root_module = cls.bl_idname.split(".")[0]
            prev_classes = set(bpy.utils._bpy_module_classes(
                root_module, is_registered=True))
            mod_name = mod.__name__.split(".")[-1]

            # get all keymap items
            prev_km_items = cls._get_all_addon_keymap_items()

            # register
            try:
                mod.register()
                mod.__addon_enabled__ = True
            except:
                addon_prefs = cls.get_instance()
                c = addon_prefs.addons.__class__
                error = traceback.format_exc()
                print(error)
                if not c.error:
                    c.error = error
                key = "use_" + mod_name
                if key in addon_prefs.addons:
                    del addon_prefs.addons[key]
                cls.__disable_nested_addon(mod, mod_name, False)
                return

            # get new classes
            post_classes = set(bpy.utils._bpy_module_classes(
                root_module, is_registered=True))
            classes = [c for c in post_classes if c not in prev_classes]
            cls._classes_[mod_name] = classes

            # get new keymap items
            post_km_items = cls._get_all_addon_keymap_items()
            km_items = [(item[0].name, item[1].id) for item in post_km_items
                        if item not in set(prev_km_items)]
            cls._keymap_items_[mod_name] = km_items

            cls.__info_register_submodule(mod)

    @classmethod
    def __enable_nested_addons(cls):
        addon_prefs = cls.get_instance()
        for fake_mod in cls._fake_submodules_.values():
            short_name = fake_mod.__name__.split(".")[-1]
            if getattr(addon_prefs.addons, "use_" + short_name):
                mod_name = fake_mod.__name__
                try:
                    mod = importlib.import_module(mod_name)
                except:
                    traceback.print_exc()
                    cls.__disable_nested_addon(None, short_name, False)
                    continue
                cls.__enable_nested_addon(mod)

    @classmethod
    def __disable_nested_addon(cls, mod, mod_name, clear_preferences=False):
        addon_prefs = cls.get_instance()

        if mod and not hasattr(mod, "__addon_enabled__"):
            mod.__addon_enabled__ = False

        # restore panel settings until unregister
        panels = addon_prefs.info_panels
        if mod_name in panels:
            item = panels[mod_name]
            item.restore_all(only_classes=True)

        if mod:
            try:
                if mod.__addon_enabled__:
                    mod.unregister()
            except:
                c = addon_prefs.addons.__class__
                error = traceback.format_exc()
                print(error)
                if not c.error:
                    c.error = error
            mod.__addon_enabled__ = False

        # remove keymap items that still exist
        keyconfigs = addon_prefs.info_keyconfigs
        if mod_name in keyconfigs:
            keyconfig = keyconfigs[mod_name]
            items = _misc.idprop_to_py(keyconfig[keyconfig.ITEMS])
            for item in items:
                km_name = item["keymap"]
                kmi_id = item["id"]
                km = keyconfig.get_keymap(km_name)
                if km:
                    for kmi in km.keymap_items:
                        if kmi.id == kmi_id:
                            keyconfig.remove_item(kmi)
            if clear_preferences:
                keyconfigs.remove(keyconfigs.find(mod_name))

        # remove class item
        classes = addon_prefs.info_classes
        if mod_name in classes:
            if clear_preferences:
                classes.remove(classes.find(mod_name))

        # remove panel item
        panels = addon_prefs.info_panels
        if mod_name in panels:
            if clear_preferences:
                panels.remove(panels.find(mod_name))

        # remove prefs_***, use_***, show_expanded_***
        if clear_preferences:
            for prefix in ("prefs_", "use_", "show_expanded_"):
                if prefix + mod_name in addon_prefs.addons:
                    del addon_prefs.addons[prefix + mod_name]

        # remove module classes and keymap items
        if mod_name in cls._classes_:
            del cls._classes_[mod_name]
        if mod_name in cls._keymap_items_:
            del cls._keymap_items_[mod_name]

    @classmethod
    def __disable_nested_addons(cls, clear_preferences=False):
        addon_prefs = cls.get_instance()
        for fake_mod in cls._fake_submodules_.values():
            short_name = fake_mod.__name__.split(".")[-1]
            if getattr(addon_prefs.addons, "use_" + short_name):
                mod_name = fake_mod.__name__
                try:
                    mod = importlib.import_module(mod_name)
                except:
                    traceback.print_exc()
                    mod = None
                cls.__disable_nested_addon(mod, short_name, clear_preferences)

    @classmethod
    def __info_register_submodule(cls, mod):
        mod_name = mod.__name__.split(".")[-1]
        addon_prefs = cls.get_instance()

        # init info_keyconfigs
        keyconfigs = addon_prefs.info_keyconfigs
        if mod_name in keyconfigs:
            item = keyconfigs[mod_name]
        else:
            item = keyconfigs.add()
            item.name = mod_name
        item.init()
        item.load()

        # init info_classes
        classes = addon_prefs.info_classes
        if mod_name not in classes:
            item = classes.add()
            item.name = mod_name

        # init info_panels
        panels = addon_prefs.info_panels
        if mod_name in panels:
            item = panels[mod_name]
        else:
            item = panels.add()
            item.name = mod_name
        item.init()
        item.load(only_changed=True)

    def _draw_ex(self, context, draw_bases=True):
        """
        :type context: bpy.types.Context
        :type draw_bases: bool
        """
        addons = self.addons
        bl_idname = self.__class__.bl_idname

        if self._fake_submodules_:
            group_layout = self.layout.box()
            """:type: bpy.types.UILayout"""
        else:
            group_layout = self.layout
            """:type: bpy.types.UILayout"""

        if "." not in bl_idname:
            align_box_draw = addons.ui_align_box_draw
            use_indent_draw = addons.ui_use_indent_draw
        else:
            root_prefs = self.get_instance(root=True)
            align_box_draw = root_prefs.addons.ui_align_box_draw
            use_indent_draw = root_prefs.addons.ui_use_indent_draw

        use_filter = addons.ui_use_addon_filter
        if use_filter and self._fake_submodules_:
            split = group_layout.split()
            colsub = split.column()
            sp = colsub.split(0.8)
            row = sp.row()
            row.prop(addons, "ui_addon_search", text="", icon='VIEWZOOM')
            sp.row()
            colsub = split.column()
            sp = colsub.split(0.8)
            row = sp.row()
            row.prop(addons, "ui_addon_filter")
            sp.row()

        filter = addons.ui_addon_filter
        search = addons.ui_addon_search

        for fake_mod in self._fake_submodules_.values():
            mod_name = fake_mod.__name__.split(".")[-1]
            if not addons.ui_show_private and mod_name.startswith("_"):
                continue

            info = addon_utils.module_bl_info(fake_mod)

            is_enabled = getattr(addons, "use_" + mod_name)
            if (not use_filter or (filter == 'All') or
                    (filter == info["category"]) or
                    (filter == 'Enabled' and is_enabled) or
                    (filter == 'Disabled' and not is_enabled)):
                pass
            else:
                continue

            if use_filter and search:
                if search.startswith("//"):
                    if re.search(search.lstrip("//"), fake_mod.__file__):
                        match = True
                    else:
                        match = False
                else:
                    match = True
                    for word in search.split(" "):
                        if not word:
                            continue
                        if word.lower() in info["name"].lower():
                            pass
                        elif (info["author"] and
                              word.lower() in info["author"].lower()):
                            pass
                        else:
                            match = False
                            break
                if not match:
                    continue

            column = group_layout.column(align=align_box_draw)

            # Indent
            if use_indent_draw:
                sp = column.split(0.01)
                sp.column()
                column = sp.column(align=align_box_draw)

            box = column.box()

            # Title
            expand = getattr(addons, "show_expanded_" + mod_name)
            icon = 'TRIA_DOWN' if expand else 'TRIA_RIGHT'
            colsub = box.column()  # boxのままだと行間が広い
            row = colsub.row(align=True)
            row.context_pointer_set("addon_preferences", self)

            op = row.operator("wm.context_toggle", text="", icon=icon,
                              emboss=False)
            op.data_path = "addon_preferences.addons.show_expanded_" + mod_name

            if 0:
                row.prop(addons, "use_" + mod_name, text="")
            else:
                if is_enabled:
                    op_name = "wm.nested_addon_disable"
                    icon = 'CHECKBOX_HLT'
                else:
                    op_name = "wm.nested_addon_enable"
                    icon = 'CHECKBOX_DEHLT'
                op = row.operator(op_name, text="", icon=icon, emboss=False)
                op.module = mod_name

            sub = row.row()
            sub.active = is_enabled
            # sub.alignment = 'RIGHT'
            sub.label("{}: {}".format(info["category"], info["name"]))
            if mod_name.startswith("_"):
                sub.label("", icon='SCRIPTPLUGINS')
            if info.get("warning"):
                sub.label("", icon='ERROR')

            # Info
            if expand:
                # reference: space_userpref.py
                if info["description"]:
                    split = colsub.row().split(percentage=0.15)
                    split.label("Description:")
                    split.label(info["description"])
                if info["location"]:
                    split = colsub.row().split(percentage=0.15)
                    split.label("Location:")
                    split.label(info["location"])
                split = colsub.row().split(percentage=0.15)
                split.label("File:")
                split.label(fake_mod.__file__)
                if info["author"]:
                    mod = sys.modules[bl_idname]
                    base_info = getattr(mod, "bl_info", None)
                    if not isinstance(base_info, dict):
                        base_info = {}
                    if info["author"] != base_info.get("author"):
                        split = colsub.row().split(percentage=0.15)
                        split.label("Author:")
                        split.label(info["author"])
                if info["version"]:
                    split = colsub.row().split(percentage=0.15)
                    split.label("Version:")
                    split.label(".".join(str(x) for x in info["version"]),
                                translate=False)
                if info["warning"]:
                    split = colsub.row().split(percentage=0.15)
                    split.label("Warning:")
                    split.label("  " + info["warning"], icon="ERROR")

                # user_addon = bpy.types.USERPREF_PT_addons.is_user_addon(mod, user_addon_paths)
                # tot_row = bool(info["wiki_url"]) + bool(user_addon)
                tot_row = int(bool(info["wiki_url"]))

                if tot_row:
                    split = colsub.row().split(percentage=0.15)
                    split.label(text="Internet:")
                    if info["wiki_url"]:
                        split.operator("wm.url_open", text="Documentation", icon='HELP').url = info["wiki_url"]
                    split.operator("wm.url_open", text="Report a Bug", icon='URL').url = info.get(
                            "tracker_url",
                            "https://developer.blender.org/maniphest/task/edit/form/2")
                    # if user_addon:
                    #     split.operator("wm.addon_remove", text="Remove", icon='CANCEL').module = mod.__name__

                    for i in range(4 - tot_row):
                        split.separator()

                # Preferences
                if getattr(addons, "use_" + mod_name):
                    try:
                        sub_addon_prefs = getattr(addons, "prefs_" + mod_name,
                                                  None)
                    except:
                        traceback.print_exc()
                        continue

                    if align_box_draw:
                        col = column.box().column()
                    else:
                        col = box.column()

                    col_head = col.column()
                    col_body = col.column()
                    has_error = False
                    if sub_addon_prefs:
                        sub_addon_prefs.layout = col_body
                    if sub_addon_prefs and hasattr(sub_addon_prefs, "draw"):
                        try:
                            sub_addon_prefs.draw(context)
                        except:
                            traceback.print_exc()
                            has_error = True
                    if (not sub_addon_prefs or
                            not hasattr(sub_addon_prefs, "_ADDON_GROUP_")):
                        # TODO: use hasattr or not
                        self._draw_addon_info(context, col_body, mod_name)
                    has_introspect_error = False
                    try:
                        # SyntaxError may occur due to " or "
                        introspect = eval(col_body.introspect())
                    except:
                        # traceback.print_exc()
                        has_introspect_error = True
                    if has_introspect_error or introspect[0] or has_error:
                        if not align_box_draw:
                            sub = col_head.row()
                            # sub.active = False  # To make the color thinner
                            sub.label("…" * 200)
                        col_head.label("Preferences:")
                    if has_error:
                        col_body.label(text="Error (see console)",
                                       icon='ERROR')
                    if sub_addon_prefs:
                        del sub_addon_prefs.layout

        if "." not in bl_idname and self._fake_submodules_:
            row = group_layout.row()
            sub = row.row()
            sub.alignment = 'LEFT'
            sub.prop(addons, "ui_show_private")
            sub.prop(addons, "ui_use_addon_filter")
            sub = row.row()
            sub.alignment = 'RIGHT'
            sub.prop(addons, "ui_align_box_draw")
            sub.prop(addons, "ui_use_indent_draw")

        self._draw_addon_info(context, self.layout, "")

        if not draw_bases:
            return
        c = super()
        if hasattr(c, "draw"):
            c.draw(context)

    def draw(self, context):
        self._draw_ex(context)

    @classmethod
    def register(cls):
        classes = [
            WM_OT_nested_addon_enable,
            WM_OT_nested_addon_disable
        ]
        for c in classes:
            c.register_class()

        cls._fake_submodules_ = cls.__generate_fake_submodules()
        cls._classes_ = {}
        cls._keymap_items_ = {}
        cls.__init_addons_attributes()
        cls.__enable_nested_addons()
        cls._verify_info_collections()

        c = super()
        if hasattr(c, "register"):
            c.register()

    @classmethod
    def unregister(cls):
        U = bpy.context.user_preferences
        attrs = cls.bl_idname.split(".")
        if attrs[0] not in U.addons:  # wm.read_factory_settings()
            return None

        cls.__disable_nested_addons()
        cls._classes_.clear()
        cls._keymap_items_.clear()
        cls.__delete_addons_attributes()
        cls._fake_submodules_.clear()

        classes = [
            WM_OT_nested_addon_enable,
            WM_OT_nested_addon_disable
        ]
        for c in classes:
            c.unregister_class()

        c = super()
        if hasattr(c, "unregister"):
            c.unregister()

    @classmethod
    def register_addon(cls, func, module=None):
        """decorator for addon register function.

        e.g.
        @AddonGroup.register_addon
        def register():
            ...
        """
        import functools

        @functools.wraps(func)
        def register():
            cls._init_dynamic_types()

            # get all registered classes
            root_module = cls.bl_idname.split(".")[0]
            prev_classes = set(bpy.utils._bpy_module_classes(
                root_module, is_registered=True))

            # get all keymap items
            prev_km_items = [(item[0].name, item[1].id)
                             for item in cls._get_all_addon_keymap_items()]

            # register()
            func()

            # get new classes
            post_classes = set(bpy.utils._bpy_module_classes(
                root_module, is_registered=True))
            classes = [c for c in post_classes if c not in prev_classes]
            if module:
                cls._attach_to_preferences(module, classes)
            else:
                for mod_name, mod_classes in cls._classes_.items():
                    if mod_name != "":
                        for c in mod_classes:
                            if c in classes:
                                classes.remove(c)
                                # else:
                                #     raise ValueError()
            cls._classes_[""] = classes

            # get new keymap items
            post_km_items = [(item[0].name, item[1].id)
                             for item in cls._get_all_addon_keymap_items()]
            km_items = [item for item in post_km_items
                        if item not in set(prev_km_items)]
            for mod_name, mod_km_items in cls._keymap_items_.items():
                if mod_name != "":
                    for item in mod_km_items:
                        if item in km_items:
                            km_items.remove(item)
                        # else:
                        #     raise ValueError()
            cls._keymap_items_[""] = km_items

            # init CollectionProperty
            cls.info_keyconfigs[1]["type"].init_collection()
            cls.info_classes[1]["type"].init_collection()
            cls.info_panels[1]["type"].init_collection()

        register._register = func
        setattr(register, "_ADDON_GROUP_", None)

        return register

    @classmethod
    def unregister_addon(cls, func, module=None):
        """decorator for addon unregister function.

        e.g.
        @AddonGroup.unregister_addon
        def unregister():
            ...
        """
        import functools

        @functools.wraps(func)
        def unregister():
            addon_prefs = cls.get_instance()

            # restore panels
            for item in addon_prefs.info_panels:
                item.restore_all(only_classes=True)

            # get addon keymap items
            keyconfig_items = []
            for keyconfig in addon_prefs.info_keyconfigs:
                for item in keyconfig[keyconfig.ITEMS]:
                    keyconfig_items.append([item["keymap"], item["id"]])

            # unregister()
            func()

            if module:
                cls._detach_from_preferences(module)

            # remove keymap items that still exist
            for item in keyconfig_items:
                km_name, kmi_id = item
                km = AddonKeyConfig.get_keymap(km_name)
                if km:
                    for kmi in km.keymap_items:
                        if kmi.id == kmi_id:
                            km.keymap_items.remove(kmi)

            cls._delete_dynamic_types()

        unregister._unregister = func

        return unregister

    @classmethod
    def register_module(cls, module=None, verbose=False):
        """Modified bpy.utils.register_module()
        :type module: str
        :type verbose: bool
        """
        if module:
            if cls.bl_idname and module != cls.bl_idname:
                msg = "Can not specify another module: must {}, got {}"
                msg = msg.format(cls.bl_idname, module)
                raise ValueError(msg)
        else:
            module = cls.bl_idname
        if verbose:
            print("bpy.utils.register_module(%r): ..." % module)
        root_module = module.split(".")[0]
        if cls.bl_idname:
            fake_modules = cls.__generate_fake_submodules()
        else:
            fake_modules = None
        cls_ = None
        for cls_ in bpy.utils._bpy_module_classes(root_module,
                                                  is_registered=False):
            if not cls_.__module__.startswith(module):
                continue
            if fake_modules is not None:
                is_submodule = False
                for m in fake_modules:
                    if cls_.__module__.startswith(module + "." + m):
                        is_submodule = True
                        break
                if is_submodule:
                    continue

            if verbose:
                print("    %r" % cls_)
            try:
                bpy.utils.register_class(cls_)
            except:
                print("bpy.utils.register_module(): "
                      "failed to registering class %r" % cls_)
                import traceback
                traceback.print_exc()
        if verbose:
            print("done.\n")
        if cls_ is None:
            raise Exception("register_module(%r): defines no classes" % module)

    @classmethod
    def unregister_module(cls, module=None, verbose=False):
        """Modified bpy.utils.unregister_module()
        :type module: str
        :type verbose: bool
        """
        if module:
            if cls.bl_idname and module != cls.bl_idname:
                msg = "Can not specify another module: must {}, got {}"
                msg = msg.format(cls.bl_idname, module)
                raise ValueError(msg)
        else:
            module = cls.bl_idname
        if verbose:
            print("bpy.utils.unregister_module(%r): ..." % module)
        root_module = module.split(".")[0]
        if cls.bl_idname:
            fake_modules = cls.__generate_fake_submodules()
        else:
            fake_modules = None
        for cls_ in bpy.utils._bpy_module_classes(root_module,
                                                  is_registered=True):
            if not cls_.__module__.startswith(module):
                continue
            if fake_modules is not None:
                is_submodule = False
                for m in fake_modules:
                    if cls_.__module__.startswith(module + "." + m):
                        is_submodule = True
                        break
                if is_submodule:
                    continue

            if verbose:
                print("    %r" % cls_)
            try:
                bpy.utils.unregister_class(cls_)
            except:
                print("bpy.utils.unregister_module(): "
                      "failed to unregistering class %r" % cls_)
                import traceback
                traceback.print_exc()
        if verbose:
            print("done.\n")


def register_module(module, verbose=False):
    """Modified bpy.utils.register_module()
    :type module: str
    :type verbose: bool
    """
    AddonGroup.register_module(module, verbose)


def unregister_module(module, verbose=False):
    """Modified bpy.utils.unregister_module()
    :type module: str
    :type verbose: bool
    """
    AddonGroup.unregister_module(module, verbose)
