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


import importlib
import os
import shutil
import traceback

import bpy

from ..utils import vaprops
from ..utils.vaprops import idprop_to_py, bl_prop_to_py_prop

from . import custom_icons

menu_buffer = None
item_buffer = None


"""
context addtibutes:
    context.addon_preferences
    context.pie_menu
    context.pie_menu_item
"""


###############################################################################
# Module
###############################################################################
try:
    module_installed
except NameError:
    module_installed = False


class WM_OT_pie_menu_module_install(bpy.types.Operator):
    bl_idname = "wm.pie_menu_module_install"
    bl_label = "Install Module"
    bl_options = {'REGISTER', 'INTERNAL'}

    @staticmethod
    def install_path():
        dir_path = bpy.utils.user_resource('SCRIPTS', "modules", True)
        dst = os.path.join(dir_path, "pie_menu.py")
        return dst

    def error(self):
        err = traceback.format_exc()
        print(err)
        self.report({'ERROR'}, err)
        return {'CANCELLED'}

    def execute(self, context):
        global module_installed
        src = os.path.join(os.path.dirname(__file__), "_pie_menu.py")
        dst = self.install_path()
        mod = importlib.import_module(
            ".".join(__name__.split(".")[:-1]))
        try:
            with open(src, "r", encoding="utf-8") as f:
                text = f.read()
                text = text.replace(
                    "CTOOLS_MODULE_NAME", __name__.split(".")[0])
                text = text.replace(
                    "CURRENT_VERSION", str(mod.bl_info["version"]))
        except:
            return self.error()
        try:
            with open(dst, "w", encoding="utf-8") as f:
                f.write(text)
        except:
            return self.error()
        self.report({'INFO'}, "Restert Blender. (Installed " + dst + ")")
        module_installed = True
        return {'FINISHED'}


###############################################################################
# Menus
###############################################################################
class WM_OT_pie_menu_menus_reset(bpy.types.Operator):
    bl_idname = "wm.pie_menu_menus_reset"
    bl_label = "Reset Menus"
    bl_description = "Reset menus"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        if hasattr(addon_prefs, "reset_menus"):
            try:
                addon_prefs.reset_menus()
            except:
                text = traceback.format_exc()
                print(text)
                self.report({'ERROR'}, text)
        else:
            text = "'{}' object has no attribute 'reset_menus'".format(
                self.__class__.__name__)
            self.report({'WARNING'}, text)
        return {'FINISHED'}


###############################################################################
# Menu
###############################################################################
class WM_OT_pie_menu_menu_add(bpy.types.Operator):
    bl_idname = "wm.pie_menu_menu_add"
    bl_label = "Add Menu"
    bl_description = "Add menu"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        addon_prefs.menus.add()
        return {'FINISHED'}


class WM_OT_pie_menu_menu_remove(bpy.types.Operator):
    bl_idname = "wm.pie_menu_menu_remove"
    bl_label = "Delete Menu"
    bl_description = "Delete menu"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        for i, m in enumerate(addon_prefs.menus):
            if m == menu:
                break
        else:
            i = -1
        if i != -1:
            addon_prefs.menus.remove(i)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class WM_OT_pie_menu_menu_copy(bpy.types.Operator):
    bl_idname = "wm.pie_menu_menu_copy"
    bl_label = "Copy Menu"
    bl_description = "Copy"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        global menu_buffer
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        for i, m in enumerate(addon_prefs.menus):
            if m == menu:
                break
        else:
            i = -1
        if i != -1:
            menu_buffer = idprop_to_py(addon_prefs["menus"][i])
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class WM_OT_pie_menu_menu_paste(bpy.types.Operator):
    bl_idname = "wm.pie_menu_menu_paste"
    bl_label = "Paste Menu"
    bl_description = "Paste"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        for i, m in enumerate(addon_prefs.menus):
            if m == menu:
                break
        else:
            i = -1
        if i != -1 and menu_buffer is not None:
            prop = addon_prefs["menus"][i]
            # clear
            for key in prop.keys():
                if key not in ["show_expanded", "active"]:
                    del prop[key]
            # paste
            buf = menu_buffer.copy()
            for key in ["show_expanded", "active"]:
                if key in buf:
                    del buf[key]
            prop.update(buf)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

class WM_OT_pie_menu_menu_move(bpy.types.Operator):
    bl_idname = "wm.pie_menu_menu_move"
    bl_label = "Move Menu"
    bl_description = "Move menu"
    bl_options = {'REGISTER', 'INTERNAL'}

    direction = bpy.props.IntProperty(
        name="Direction",
    )

    def execute(self, context):
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        for i, m in enumerate(addon_prefs.menus):
            if m == menu:
                break
        else:
            return {'CANCELLED'}

        if self.direction < 0:
            if i > 0:
                addon_prefs.menus.move(i, i - 1)
        elif self.direction > 0:
            if i < len(addon_prefs.menus) - 1:
                addon_prefs.menus.move(i, i + 1)
        return {'FINISHED'}


###############################################################################
# Item
###############################################################################
class WM_OT_pie_menu_item_add(bpy.types.Operator):
    bl_idname = "wm.pie_menu_item_add"
    bl_label = "Add Item"
    bl_description = "Add menu item"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        menu.menu_items.add()
        return {'FINISHED'}


class WM_OT_pie_menu_item_remove(bpy.types.Operator):
    bl_idname = "wm.pie_menu_item_remove"
    bl_label = "Delete Item"
    bl_description = "Delete menu item"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        item = context.pie_menu_item
        for i, itm in enumerate(menu.menu_items):
            if itm == item:
                break
        else:
            i = -1
        if i != -1:
            menu.menu_items.remove(i)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class WM_OT_pie_menu_item_copy(bpy.types.Operator):
    bl_idname = "wm.pie_menu_item_copy"
    bl_label = "Copy Item"
    bl_description = "Copy"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        global item_buffer
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        item = context.pie_menu_item
        prop = None
        for i, itm in enumerate(menu.menu_items):
            if item == itm:
                prop = menu["menu_items"][i]
                break
            elif item == itm.shift:
                prop = menu["menu_items"][i]["shift"]
                break
            elif item == itm.ctrl:
                prop = menu["menu_items"][i]["ctrl"]
                break
        if prop:
            item_buffer = idprop_to_py(prop)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class WM_OT_pie_menu_item_paste(bpy.types.Operator):
    bl_idname = "wm.pie_menu_item_paste"
    bl_label = "Paste Item"
    bl_description = "Paste"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        item = context.pie_menu_item
        prop = None
        for i, itm in enumerate(menu.menu_items):
            if item == itm:
                prop = menu["menu_items"][i]
                break
            elif item == itm.shift:
                prop = menu["menu_items"][i]["shift"]
                break
            elif item == itm.ctrl:
                prop = menu["menu_items"][i]["ctrl"]
                break
        if prop and item_buffer is not None:
            # clear
            for key in prop.keys():
                if key not in ["show_expanded", "active"]:
                    del prop[key]
            # paste
            buf = item_buffer.copy()
            for key in ["show_expanded", "active"]:
                if key in buf:
                    del buf[key]
            for key in ["shift", "ctrl"]:
                if not hasattr(item, key) and key in buf:
                    del buf[key]
            prop.update(buf)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class WM_OT_pie_menu_item_move(bpy.types.Operator):
    bl_idname = "wm.pie_menu_item_move"
    bl_label = "Move Item"
    bl_description = "Move item"
    bl_options = {'REGISTER', 'INTERNAL'}

    direction = bpy.props.IntProperty(
        name="Direction",
    )

    def execute(self, context):
        addon_prefs = context.addon_preferences
        menu = context.pie_menu
        item = context.pie_menu_item

        index = -1
        for i, itm in enumerate(menu.menu_items):
            if itm == item:
                index = i
                break
        if index != -1:
            if self.direction < 0:
                if index > 0:
                    menu.menu_items.move(index, index - 1)
            elif self.direction > 0:
                if index < len(menu.menu_items) - 1:
                    menu.menu_items.move(index, index + 1)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


def prop_item_operator_search_enum_items(self, context):
    items = []
    for mod_name in dir(bpy.ops):
        mod = getattr(bpy.ops, mod_name)
        for func_name in dir(mod):
            if func_name.startswith("_"):
                continue
            name = mod_name + "." + func_name
            items.append((name, name, ""))
    return items


class WM_OT_pie_menu_item_operator_search(bpy.types.Operator):
    bl_idname = "wm.pie_menu_item_operator_search"
    bl_label = "Search Icon"
    bl_description = ""
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_property = "operator"

    operator = bpy.props.EnumProperty(
        items=prop_item_operator_search_enum_items
    )

    def execute(self, context):
        self.__class__.pie_menu_item.operator = self.icon
        return {'FINISHED'}

    def invoke(self, context, event):
        self.__class__.pie_menu_item = context.pie_menu_item
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}


class WM_OT_pie_menu_item_icon_search(bpy.types.Operator):
    bl_idname = "wm.pie_menu_item_icon_search"
    bl_label = "Search Icon"
    bl_description = ""
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_property = "icon"

    icon = vaprops.bl_prop_to_py_prop(
        bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'])
    enum_items = []
    for enum_item in icon[1]["items"]:
        enum_items.append((enum_item[:3] + (enum_item[0], enum_item[4])))
    icon[1]["items"] = enum_items

    def execute(self, context):
        self.__class__.pie_menu_item.icon = self.icon
        return {'FINISHED'}

    def invoke(self, context, event):
        self.__class__.pie_menu_item = context.pie_menu_item
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}


class WM_OT_pie_menu_item_icon_file_search(bpy.types.Operator):
    bl_idname = "wm.pie_menu_item_icon_file_search"
    bl_label = "Search Icon"
    bl_description = ""
    bl_options = {'REGISTER', 'INTERNAL'}

    filepath = bpy.props.StringProperty()
    filename = bpy.props.StringProperty()
    directory = bpy.props.StringProperty()

    """reference:
    editors/space_file/filesel.c: ED_fileselect_set_params
    """
    filter_image = bpy.props.BoolProperty(default=True)
    display_type = bl_prop_to_py_prop(
        bpy.types.FileSelectParams.bl_rna.properties["display_type"])

    def execute(self, context):
        self.__class__.pie_menu_item.icon = self.filepath
        pcol = custom_icons.preview_collections["main"]
        try:
            pcol.load(self.filepath, self.filepath, 'IMAGE')
        except:
            pass
        return {'FINISHED'}

    def invoke(self, context, event):
        self.__class__.pie_menu_item = context.pie_menu_item
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class WM_OT_pie_menu_property_unset(bpy.types.Operator):
    bl_idname = "wm.pie_menu_property_unset"
    bl_label = "Unset Property"
    bl_description = "Clear the property and use default or generated value"
    bl_options = {'REGISTER', 'INTERNAL'}

    data = bpy.props.StringProperty()
    property = bpy.props.StringProperty()

    def execute(self, context):
        obj = eval("context." + self.data)
        if 0:
            # not working at property with get,set function
            if obj.is_property_set(self.property):
                obj.property_unset(self.property)
        else:
            if self.property in obj:
                del obj[self.property]
        return {'FINISHED'}


class WM_OT_pie_menu_text_paste(bpy.types.Operator):
    bl_idname = "wm.pie_menu_text_paste"
    bl_label = "Paste Text"
    bl_description = "Paste multiple lines from clipboard"
    bl_options = {'REGISTER', 'INTERNAL'}

    data_path = bpy.props.StringProperty(
        name="Path",
    )

    def execute(self, context):
        ls = self.data_path.split(".")
        obj = eval("context." + ".".join(ls[:-1]))
        setattr(obj, ls[-1], context.window_manager.clipboard)

        return {'FINISHED'}


classes = [
    WM_OT_pie_menu_module_install,

    WM_OT_pie_menu_menus_reset,

    WM_OT_pie_menu_menu_add,
    WM_OT_pie_menu_menu_remove,
    WM_OT_pie_menu_menu_copy,
    WM_OT_pie_menu_menu_paste,
    WM_OT_pie_menu_menu_move,

    WM_OT_pie_menu_item_add,
    WM_OT_pie_menu_item_remove,
    WM_OT_pie_menu_item_copy,
    WM_OT_pie_menu_item_paste,
    WM_OT_pie_menu_item_move,
    WM_OT_pie_menu_item_operator_search,
    WM_OT_pie_menu_item_icon_search,
    WM_OT_pie_menu_item_icon_file_search,

    WM_OT_pie_menu_property_unset,
    WM_OT_pie_menu_text_paste,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
