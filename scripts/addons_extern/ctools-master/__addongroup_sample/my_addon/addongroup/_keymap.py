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


import bpy

from ._misc import idprop_to_py, Registerable


# NOTE: <ID property arrays> allowed: [{}, ""], error: [{}, 1] [1, ""]


###############################################################################
# Operator, Menu
###############################################################################
class OperatorKeymapItemAdd(Registerable, bpy.types.Operator):
    bl_idname = "wm.addonprefs_keymap_item_add"
    bl_label = "Add Key Map Item"
    bl_description = "Add key map item"
    bl_options = {'REGISTER', 'INTERNAL'}

    def _get_entries():
        import bpy_extras.keyconfig_utils

        modal_keymaps = {"View3D Gesture Circle", "Gesture Border",
                         "Gesture Zoom Border", "Gesture Straight Line",
                         "Standard Modal Map", "Knife Tool Modal Map",
                         "Transform Modal Map", "Paint Stroke Modal",
                         "View3D Fly Modal", "View3D Walk Modal",
                         "View3D Rotate Modal", "View3D Move Modal",
                         "View3D Zoom Modal", "View3D Dolly Modal", }

        def get():
            def _get(entry):
                idname, spaceid, regionid, children = entry
                if not ("INVALID_MODAL_KEYMAP" and idname in modal_keymaps):
                    yield entry
                    for e in children:
                        yield from _get(e)

            for entry in bpy_extras.keyconfig_utils.KM_HIERARCHY:
                yield from _get(entry)

        return list(get())

    keymap = bpy.props.EnumProperty(
        name="KeyMap",
        items=[(entry[0], entry[0], "") for entry in _get_entries()])
    del _get_entries

    def execute(self, context):
        keyconfig = context.keyconfig
        """:type: AddonKeyConfig"""
        km = keyconfig.get_keymap(self.keymap)
        if km.is_modal:
            kmi = km.keymap_items.new_modal(
                propvalue="", type='A', value='PRESS')
            print("WARNING: '{}' is modal keymap. "
                  "Cannot remove keymap item "
                  "when unregister".format(self.keymap))
        else:
            kmi = km.keymap_items.new(
                idname="none", type='A', value='PRESS')
            keyconfig.add_item(kmi)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if self.properties.is_property_set("keymap"):
            return self.execute(context)
        else:
            return bpy.ops.wm.call_menu(name=MenuKeymapItemAdd.bl_idname)


class OperatorKeymapItemRemove(Registerable, bpy.types.Operator):
    bl_idname = "wm.addonprefs_keymap_item_remove"
    bl_label = "Remove Key Map Item"
    bl_description = "Remove key map item"
    bl_options = {'REGISTER', 'INTERNAL'}

    item_id = bpy.props.IntProperty()

    def execute(self, context):
        keyconfig = context.keyconfig
        """:type: AddonKeyConfig"""
        for kmi in context.keymap.keymap_items:
            if kmi.id == self.item_id:
                keyconfig.remove_item(kmi)
                return {'FINISHED'}
        context.area.tag_redraw()
        return {'CANCELLED'}


class OperatorKeymapsWrite(Registerable, bpy.types.Operator):
    bl_idname = "wm.addonprefs_keymaps_write"
    bl_label = "Write KeyMaps"
    bl_description = "Convert addon key map items to ID properties. " \
                     "This needs to be done before 'Save User Settings'"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        keyconfig = context.keyconfig
        """:type: AddonKeyConfig"""
        value = keyconfig.get_current_values()
        keyconfig[keyconfig.SAVED_VALUES] = value
        return {'FINISHED'}


class OperatorKeymapsRestore(Registerable, bpy.types.Operator):
    bl_idname = "wm.addonprefs_keymaps_restore"
    bl_label = "Restore KeyMaps"
    bl_description = "Restore key map items and clear ID properties"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        keyconfig = context.keyconfig
        """:type: AddonKeyConfig"""
        keyconfig.restore()
        if keyconfig.SAVED_VALUES in keyconfig:
            del keyconfig[keyconfig.SAVED_VALUES]
        context.area.tag_redraw()
        return {'FINISHED'}


class MenuKeymapItemAdd(Registerable, bpy.types.Menu):
    bl_idname = "WM_MT_addonprefs_keymap_item_add"
    bl_label = "Add New"

    module_name = bpy.props.StringProperty()

    def draw(self, context):
        import bpy_extras.keyconfig_utils

        # addon_prefs = context.addon_preferences
        keyconfig = context.keyconfig
        """:type: AddonKeyConfig"""

        layout = self.layout
        column = layout.column()
        # column.context_pointer_set("addon_preferences", addon_prefs)
        column.context_pointer_set("keyconfig", keyconfig)

        def get_non_modal_km_hierarchy():
            if not "INVALID_MODAL_KEYMAP":
                return bpy_extras.keyconfig_utils.KM_HIERARCHY

            modal_keymaps = {"View3D Gesture Circle", "Gesture Border",
                             "Gesture Zoom Border",
                             "Gesture Straight Line", "Standard Modal Map",
                             "Knife Tool Modal Map", "Transform Modal Map",
                             "Paint Stroke Modal", "View3D Fly Modal",
                             "View3D Walk Modal", "View3D Rotate Modal",
                             "View3D Move Modal", "View3D Zoom Modal",
                             "View3D Dolly Modal"}

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

        used_keymap_names = {item["keymap"] for item in
                             keyconfig[keyconfig.ITEMS]}

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
                        op = row.operator(OperatorKeymapItemAdd.bl_idname,
                                          text=name, icon=icon)
                        op.keymap = name
                    j += 1
                else:
                    row.separator()


###############################################################################
# Property Group
###############################################################################
class AddonKeyConfig:
    ITEMS = "current_items"
    DEFAULT_ITEMS = "default_items"
    DEFAULT_VALUES = "default_values"
    SAVED_VALUES = "saved_values"

    owner_class = None

    lock_default_keymap_items = False

    kc_show_keymaps = bpy.props.BoolProperty(
        name="Show KeyMaps",
        default=False,
    )
    kc_filter_type = bpy.props.EnumProperty(
        name="Filter Type",
        description="Filter method",
        items=[('NAME', "Name",
                "Filter based on the operator name"),
               ('KEY', "Key-Binding",
                "Filter based on key bindings")],
        default='NAME',
    )
    kc_filter_text = bpy.props.StringProperty(
        name="Filter",
        description="Search term for filtering in the UI",
        default="",
    )

    unsaved_props = [
        "kc_show_keymaps",
        "kc_filter_type",
        "kc_filter_text",
    ]

    def gen(attr, default):
        def fget(self):
            return getattr(self.__class__, "_" + attr, default)

        def fset(self, value):
            setattr(self.__class__, "_" + attr, value)
        return fget, fset

    for attr, prop in dict(locals()).items():
        if attr in unsaved_props:
            kwargs = prop[1]
            default = kwargs["default"]
            if prop[0] == bpy.props.EnumProperty:
                for i, p in enumerate(kwargs["items"]):
                    if p[0] == default:
                        default = i
                        break
            kwargs["get"], kwargs["set"] = gen(attr, default)
    del unsaved_props, gen, attr, prop, kwargs

    @classmethod
    def new_class(cls, owner_class, lock_default_keymap_items=False):
        namespace = {
            "owner_class": owner_class,
            "lock_default_keymap_items": lock_default_keymap_items
        }
        return type("AddonKeyConfig",
                    (cls, bpy.types.PropertyGroup),
                    namespace)

    @staticmethod
    def get_keymap(name, keyconfig="addon"):
        """Return result of KeyMaps.new()
        :type name: str
        :param keyconfig: "addon" or "user" or "blender" or
                          "default"(same as "blender")
        :type keyconfig: str
        :rtype: bpy.types.KeyMap
        """
        import bpy_extras.keyconfig_utils

        # ref: KeyMap.is_modal
        modal_keymaps = {
            "View3D Gesture Circle", "Gesture Border",
            "Gesture Zoom Border", "Gesture Straight Line",
            "Standard Modal Map", "Knife Tool Modal Map",
            "Transform Modal Map", "Paint Stroke Modal", "View3D Fly Modal",
            "View3D Walk Modal", "View3D Rotate Modal", "View3D Move Modal",
            "View3D Zoom Modal", "View3D Dolly Modal", "Eyedropper Modal Map"}

        keyconfigs = bpy.context.window_manager.keyconfigs
        if keyconfig == "addon":  # "Blender Addon"
            kc = keyconfigs.addon
        elif keyconfig == "user":  # "Blender User"
            kc = keyconfigs.user
        elif keyconfig in {"default", "blender"}:  # "Blender"
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
            def get_names(ls):
                for keymap_name, space_type, region_type, children in ls:
                    yield keymap_name
                    yield from get_names(children)

            all_names = list(get_names(
                bpy_extras.keyconfig_utils.KM_HIERARCHY))
            for name in modal_keymaps:
                all_names.remove(name)
            msg = "Keymap '{}' not in builtins\n".format(name)
            msg += "[\n"
            msg += "\n".join(["    '" + name + "'" for name in all_names])
            msg += "\n]\n"
            raise ValueError(msg)
        return km

    @staticmethod
    def verify_keyconfigs():
        return bpy.context.window_manager.keyconfigs.addon is not None

    def reversed_keymap_table(self):
        """:return: {KeyMapItem: KeyMap, ...}"""
        if not self.verify_keyconfigs():
            return
        kc = bpy.context.window_manager.keyconfigs.addon
        km_table = {kmi: km for km in kc.keymaps for kmi in km.keymap_items}
        return km_table

    def add_item(self, keymap_item):
        """Register key map item.
        Object references are invalid because rebuild properties.
        :param keymap_item: KeyMapItem
        :type keymap_item: bpy.types.KeyMapItem
        """
        if not self.verify_keyconfigs():
            return
        km_tabel = self.reversed_keymap_table()
        km = km_tabel[keymap_item]
        if 'INVALID_MODAL_KEYMAP' and km.is_modal:
            raise ValueError("not support modal keymap: '{}'".format(km.name))
        items = idprop_to_py(self[self.ITEMS])
        items.append({"keymap": km.name, "id": keymap_item.id})
        self[self.ITEMS] = items

    def add_items(self, keymap_items):
        """Register key map items.
        Object references are invalid because rebuild properties.
        :param keymap_items: list of KeyMapItem
        :type keymap_items: list[bpy.types.KeyMapItem]
        """
        if not self.verify_keyconfigs():
            return
        km_tabel = self.reversed_keymap_table()
        new_items = []
        for keymap_item in keymap_items:
            km = km_tabel[keymap_item]
            if 'INVALID_MODAL_KEYMAP' and km.is_modal:
                raise ValueError(
                    "not support modal keymap: '{}'".format(km.name))
            new_items.append({"keymap": km.name, "id": keymap_item.id})
        items = idprop_to_py(self[self.ITEMS])
        items.extend(new_items)
        self[self.ITEMS] = items

    def remove_item(self, keymap_item, wm=True):
        """Unregister key map item.
        Object references are invalid because rebuild properties.
        :param keymap_item: KeyMapItem
        :type keymap_item: bpy.types.KeyMapItem
        :param wm: Remove from KeyMap.keymap_items
        :type wm: bool
        """
        if not self.verify_keyconfigs():
            return
        km_table = self.reversed_keymap_table()
        km = km_table[keymap_item]
        item = {"keymap": km.name, "id": keymap_item.id}
        if 'INVALID_MODAL_KEYMAP' and km.is_modal:
            raise ValueError("not support modal keymap: '{}'".format(km.name))
        items = idprop_to_py(self[self.ITEMS])
        items.remove(item)
        self[self.ITEMS] = items
        if wm:
            km.keymap_items.remove(keymap_item)
            # Force Update
            bpy.context.window_manager.keyconfigs.active = \
                bpy.context.window_manager.keyconfigs.active

    def remove_items(self, wm=True, only_changed=False):
        """Unregister key map items.
        Object references are invalid because rebuild properties.
        :param wm: Remove from KeyMap.keymap_items
        :type wm: bool
        :param only_changed: ignore included in self.default_keymap_items
        :type only_changed: bool
        """
        if not self.verify_keyconfigs():
            return
        if wm:
            default_items = idprop_to_py(self[self.DEFAULT_ITEMS])
            for item in idprop_to_py(self[self.ITEMS]):
                km_name = item["keymap"]
                kmi_id = item["id"]
                if only_changed:
                    if item in default_items:
                        continue
                km = self.get_keymap(km_name)
                for kmi in km.keymap_items:
                    if kmi.id == kmi_id:
                        break
                else:
                    # raise ValueError('KeyMapItem not fond')
                    print("KeyMapItem not fond. KeyMap: {}, ID: {}".format(
                        km_name, kmi_id))
                    continue
                if "INVALID_MODAL_KEYMAP" and km.is_modal:
                    raise ValueError(
                        "not support modal keymap: '{}'".format(km.name))
                km.keymap_items.remove(kmi)
        self[self.ITEMS] = []

        # commit 103fbb3afc076383b94910e535374c5db398d06c
        #     Fix memory leak caused by unknown opeartor of keymap item
        #
        # addonのKeyMapからKeyMapItemを消してもuserのKeyMapには
        # まだ残ったままで、これの更新はメインループで行われる。
        # この更新前にKeyMapItemに割り当てられたオペレーターをunregister
        # してしまっているとKeyMapItem開放時にSegmentation faultで落ちる。
        bpy.context.window_manager.keyconfigs.active = \
            bpy.context.window_manager.keyconfigs.active

    def get_current_values(self):
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

        if not self.verify_keyconfigs():
            return

        values = []
        km_table = self.reversed_keymap_table()

        keympap_items = []
        for item in self[self.ITEMS]:
            km_name = item["keymap"]
            kmi_id = item["id"]
            km = self.get_keymap(km_name)
            for kmi in km.keymap_items:
                if kmi.id == kmi_id:
                    keympap_items.append(kmi)
                    break

        for kmi in keympap_items:
            km = km_table[kmi]

            info = {"keymap": km.name}

            # KeyMapItem properties
            attrs = {}
            for attr in ("active", "map_type", "type", "value", "propvalue",
                         "idname", "any", "shift", "ctrl", "alt", "oskey",
                         "key_modifier"):
                value = getattr(kmi, attr)
                if isinstance(value, bool):
                    value = int(value)
                attrs[attr] = value

            # operator properties
            op_props = {}
            if not km.is_modal:
                if kmi.properties is None:
                    # TODO: Investigation of occurrence condition
                    continue
                for attr in kmi.properties.bl_rna.properties.keys():
                    if attr == "rna_type":
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

            values.append([info, attrs, op_props])

        return values

    def set_current_values(self, values):
        """一旦全部のKeyMapItemを削除してからvaluesに従って追加する。
        get_current_values()と対になっている。
        :param values: get_current_values()の返り値
        :type values: list | tuple
        """
        import traceback
        if not self.verify_keyconfigs():
            return
        self.remove_items()
        keymap_items = []
        for info, attrs, op_props in values:
            km = self.get_keymap(info["keymap"])
            if "INVALID_MODAL_KEYMAP" and km.is_modal:
                raise ValueError(
                    "not support modal keymap: '{}'".format(km.name))
            if km.is_modal:
                args = {name: attrs[name] for name in (
                    "type", "value", "propvalue", "any", "shift", "ctrl",
                    "alt", "oskey", "key_modifier")}
                kmi = km.keymap_items.new_modal(**args)
                # kmi.propvalue = attrs["propvalue"]  # 適用できていないから
                # TODO: Can't use ModalKeyMap
                #       val: enum "TRANSLATE" not found in ('NONE')
            else:
                args = {name: attrs[name] for name in (
                    "idname", "type", "value", "any", "shift", "ctrl", "alt",
                    "oskey", "key_modifier")}
                kmi = km.keymap_items.new(**args)
            kmi.active = attrs["active"]
            for name, value in op_props.items():
                try:
                    setattr(kmi.properties, name, value)
                except:
                    traceback.print_exc()
            keymap_items.append(kmi)
        self.add_items(keymap_items)

    def set_default(self):
        """現在登録しているKeyMapItemを初期値(restore時の値)とする"""
        self[self.DEFAULT_VALUES] = []
        values = self.get_current_values()
        if values:
            self[self.DEFAULT_VALUES] = values
        self[self.DEFAULT_ITEMS] = self[self.ITEMS]

    def init(self):
        keymap_items = self.owner_class._keymap_items_
        if self.name in keymap_items:
            self[self.ITEMS] = [{"keymap": km, "id": id_} for km, id_ in
                                keymap_items[self.name]]
        else:
            self[self.ITEMS] = []
        self[self.DEFAULT_ITEMS] = []
        self[self.DEFAULT_VALUES] = []
        self.set_default()

    def load(self):
        """Replace keymap items with saved"""
        if self.SAVED_VALUES in self:
            self.set_current_values(idprop_to_py(self[self.SAVED_VALUES]))
            return True
        else:
            return False

    def restore(self):
        """Restore keymap items"""
        self.set_current_values(idprop_to_py(self[self.DEFAULT_VALUES]))
        self.set_default()

    # draw ----------------------------------------------------------
    _EVENT_TYPES = set()
    _EVENT_TYPE_MAP = {}
    _EVENT_TYPE_MAP_EXTRA = {}

    _INDENTPX = 16

    def _indented_layout(self, layout, level):
        if level == 0:
            # Tweak so that a percentage of 0 won't split by half
            level = 0.0001
        indent = level * self._INDENTPX / bpy.context.region.width

        split = layout.split(percentage=indent)
        col = split.column()
        col = split.column()
        return col

    def _draw_entry(self, display_keymaps, entry, col, level=0):
        idname, spaceid, regionid, children = entry

        for km, km_items in display_keymaps:
            if (km.name == idname and km.space_type == spaceid and
                    km.region_type == regionid):
                self._draw_km(display_keymaps, km, km_items, children, col,
                              level)

    def _draw_km(self, display_keymaps, km, km_items, children, layout,
                 level):
        from bpy.app.translations import pgettext_iface as iface_
        from bpy.app.translations import contexts as i18n_contexts

        # km = km.active()  # keyconfigs.userのkeymapが返ってくる

        layout.context_pointer_set("keymap", km)

        col = self._indented_layout(layout, level)

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
                subcol = self._indented_layout(col, level + 1)
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
                    self._draw_kmi(km, kmi, col, kmi_level)

            # Child key maps
            if children:
                for entry in children:
                    self._draw_entry(display_keymaps, entry, col,
                                     level + 1)

            col.separator()

    def _draw_kmi(self, km, kmi, layout, level):
        map_type = kmi.map_type

        col = self._indented_layout(layout, level)

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
        op = sub.operator(OperatorKeymapItemRemove.bl_idname, text="",
                          icon='X')
        op.item_id = kmi.id
        if self.lock_default_keymap_items:
            default_items = idprop_to_py(self[self.DEFAULT_ITEMS])
            if {"keymap": km.name, "id": kmi.id} in default_items:
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

    def _draw_filtered(self, display_keymaps, filter_type, filter_text,
                       layout):
        _EVENT_TYPES = self._EVENT_TYPES
        _EVENT_TYPE_MAP = self._EVENT_TYPE_MAP
        _EVENT_TYPE_MAP_EXTRA = self._EVENT_TYPE_MAP_EXTRA

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
                       "cmd": "oskey", "oskey": "oskey", "any": "any"}
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
                    self._draw_kmi(km, kmi, col, 1)

        return True

    def _draw_hierarchy(self, display_keymaps, layout):
        from bpy_extras import keyconfig_utils
        for entry in keyconfig_utils.KM_HIERARCHY:
            self._draw_entry(display_keymaps, entry, layout)

    def _draw_addon_keymaps(self, context, layout, hierarchy=False, box=True):
        if box:
            col = layout.column().box()
        else:
            col = layout.column()

        sub = col.column()

        subsplit = sub.split()
        subcol = subsplit.column()

        subcolsplit = subcol.split(percentage=0.7)  # 右側にwrite,restore

        display_keymaps = {}
        for item in idprop_to_py(self[self.ITEMS]):
            km_name = item["keymap"]
            kmi_id = item["id"]
            km = self.get_keymap(km_name)
            for kmi in km.keymap_items:
                if kmi.id == kmi_id:
                    break
            else:
                # TODO: idpropの書き換えはエラーとなるか？？
                items = idprop_to_py(self[self.ITEMS])
                items.remove(item)
                self[self.ITEMS] = items
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

        filter_type = self.kc_filter_type
        filter_text = self.kc_filter_text

        if filter_text or not hierarchy:
            filter_text = filter_text.lower()
            ok = self._draw_filtered(display_keymaps, filter_type,
                                     filter_text, col)
        else:
            self._draw_hierarchy(display_keymaps, col)
            ok = True

        colsub = col.split(percentage=0.2).column()
        colsub.operator(OperatorKeymapItemAdd.bl_idname, text="Add New",
                        icon='ZOOMIN')

        # go back and fill in rowsub
        rowsub.prop(self, "kc_filter_type", text="")
        rowsubsub = rowsub.row(align=True)
        if not ok:
            rowsubsub.alert = True
        rowsubsub.prop(self, "kc_filter_text", text="", icon='VIEWZOOM')

        # Write / Restore
        default_values = idprop_to_py(self[self.DEFAULT_VALUES])
        current_values = self.get_current_values()
        if self.SAVED_VALUES in self:
            saved_values = idprop_to_py(self[self.SAVED_VALUES])
        else:
            saved_values = None
        subcolsplitrow = subcolsplit.row().split(align=True)
        # Write
        subcolsplitrow_sub = subcolsplitrow.row(align=True)
        if current_values == default_values and self.SAVED_VALUES not in self:
            subcolsplitrow_sub.enabled = False
        else:
            subcolsplitrow_sub.enabled = current_values != saved_values
        icon = 'INFO' if subcolsplitrow_sub.enabled else 'NONE'
        subcolsplitrow_sub.operator(OperatorKeymapsWrite.bl_idname,
                                    text="Save", icon=icon)
        # Restore
        subcolsplitrow_sub = subcolsplitrow.row(align=True)
        if current_values == default_values and self.SAVED_VALUES not in self:
            subcolsplitrow_sub.enabled = False
        subcolsplitrow_sub.operator(OperatorKeymapsRestore.bl_idname,
                                    text="Restore")

    def draw(self, context, layout, hierarchy=False, box=True, **kwargs):
        """キーマップアイテムの一覧を描画。
        :param context: bpy.types.Context
        :param layout: bpy.types.UILayout
        :param hierarchy: 階層表示にする
        :type hierarchy: bool
        :param box: 展開時にBoxで囲む
        :type box: bool
        """
        if not self.kc_show_keymaps:
            return

        addon_prefs = self.owner_class.get_instance()
        column = layout.column()
        column.context_pointer_set("addon_preferences", addon_prefs)
        column.context_pointer_set("keyconfig", self)
        self._draw_addon_keymaps(context, column, hierarchy, box)

    @classmethod
    def init_collection(cls):
        addon_prefs = cls.owner_class.get_instance()
        info_keyconfigs = addon_prefs.info_keyconfigs
        if "" not in info_keyconfigs:
            item = info_keyconfigs.add()
            item.name = ""
            item.init()
        mod_names = [mod.__name__.split(".")[-1]
                     for mod in cls.owner_class._fake_submodules_.values()]
        for mod_name in mod_names:
            if mod_name not in info_keyconfigs:
                item = info_keyconfigs.add()
                item.name = mod_name
        for item in list(info_keyconfigs):
            if item.name != "" and item.name not in mod_names:
                info_keyconfigs.remove(info_keyconfigs.find(item.name))
        for item in info_keyconfigs:
            item.init()
            item.load()

    @classmethod
    def register(cls):
        classes = [
            OperatorKeymapItemAdd,
            OperatorKeymapItemRemove,
            OperatorKeymapsWrite,
            OperatorKeymapsRestore,
            MenuKeymapItemAdd,
        ]
        for c in classes:
            c.register_class()

    @classmethod
    def unregister(cls):
        classes = [
            OperatorKeymapItemAdd,
            OperatorKeymapItemRemove,
            OperatorKeymapsWrite,
            OperatorKeymapsRestore,
            MenuKeymapItemAdd,
        ]
        for c in classes[::-1]:
            c.unregister_class()
