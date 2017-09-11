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
import re
import math

import bpy
import blf
from bpy import props

from ..utils import addongroup
# from ..utils import vaprops
from ..utils import vawm

# from . import oputils
from . import operators as ops
from .menu_items import draw_separator, draw_property, PieMenu


translate_iface = bpy.app.translations.pgettext_iface


DEFAULT_CORRECTED_RADIUS = False


class FVPColor:
    def __new__(cls, name, default, **kwargs):
        return props.FloatVectorProperty(
            name=name, default=default,
            min=0.0, max=1.0, soft_min=0.0, soft_max=1.0,
            subtype='COLOR_GAMMA', size=4, **kwargs)


class PieMenu_PG_Colors(bpy.types.PropertyGroup):
    use_theme = props.BoolProperty(
        name="Use Theme Color",
        description="if True, read user preference",
        default=False)

    @classmethod
    def _generate_props(cls):
        def gen(attr, klass, name, get_string, **kwargs):
            def get(self):
                if self.use_theme:
                    user_pref = bpy.context.user_preferences
                    theme = user_pref.themes["Default"]
                    ui = theme.user_interface
                    value = eval(get_string, globals(), locals())
                else:
                    value = getattr(self, "prop_" + attr)
                try:
                    ls = list(value)
                    return (ls + [1.0])[:4]
                except:
                    return value

            def set(self, value):
                setattr(self, "prop_" + attr, value)

            setattr(cls, "prop_" + attr, klass(name=name, **kwargs))
            setattr(cls, attr, klass(name=name, set=set, get=get, **kwargs))

        gen("menu_inner", FVPColor, "Menu Inner",
            "ui.wcol_menu_back.inner",
            default=(0.0, 0.0, 0.0, 1.0))
        gen("menu_show_shaded", props.BoolProperty, "Shaded",
            "ui.wcol_menu_back.show_shaded",
            default=False)
        gen("menu_shadetop", props.IntProperty, "Shade Top",
            "ui.wcol_menu_back.shadetop",
            default=30, min=-100, max=100)
        gen("menu_shadedown", props.IntProperty, "Shade Top",
            "ui.wcol_menu_back.shadedown",
            default=-30, min=-100, max=100)
        gen("title_outline", FVPColor, "Title Outline",
            "ui.wcol_menu_back.outline",
            default=(0.0, 0.0, 0.0, 1.0))
        theme = bpy.context.user_preferences.themes["Default"]
        try:
            col = list(theme.view_3d.space.gradients.high_gradient)
        except:
            col = [0.4, 0.4, 0.4]
        gen("title_inner", FVPColor, "Title Inner",
            "ui.wcol_menu_back.inner",
            default=col + [1.0])
        gen("title_inner_sel", FVPColor, "Title Inner Sel",
            "ui.wcol_menu_back.inner_sel",
            default=col + [1.0])
        del theme, col
        gen("title_text", FVPColor, "Title Text",
            "ui.wcol_menu_back.text",
            default=(1.0, 1.0, 1.0, 1.0))
        gen("title_text_sel", FVPColor, "Title Text Sel",
            "ui.wcol_menu_back.text_sel",
            default=(1.0, 1.0, 1.0, 1.0))
        gen("title_show_shaded", props.BoolProperty, "Shaded",
            "ui.wcol_menu_back.show_shaded",
            default=False)
        gen("title_shadetop", props.IntProperty, "Shade Top",
            "ui.wcol_menu_back.shadetop",
            default=30, min=-100, max=100)
        gen("title_shadedown", props.IntProperty, "Shade Down",
            "ui.wcol_menu_back.shadedown",
            default=-30, min=-100, max=100)
        gen("item_outline", FVPColor, "Item Outline",
            "ui.wcol_menu_back.outline",
            default=(0.0, 0.0, 0.0, 1.0))
        gen("item_inner", FVPColor, "Item Inner",
            "ui.wcol_menu_item.inner",
            default=(0.0, 0.0, 0.0, 0.0))
        gen("item_inner_sel", FVPColor, "Item Inner Sel",
            "ui.wcol_menu_item.inner_sel",
            default=(0.9, 0.9, 0.9, 1.0))
        gen("item_text", FVPColor, "Item Text",
            "ui.wcol_menu_item.text",
            default=(1.0, 1.0, 1.0, 1.0))
        gen("item_text_sel", FVPColor, "Item Text Sel",
            "ui.wcol_menu_item.text_sel",
            default=(0.0, 0.0, 0.0, 1.0))
        gen("item_show_shaded", props.BoolProperty, "Shaded",
            "ui.wcol_menu_item.show_shaded",
            default=False)
        gen("item_shadetop", props.IntProperty, "Shade Top",
            "ui.wcol_menu_item.shadetop",
            default=30, min=-100, max=100)
        gen("item_shadedown", props.IntProperty, "Shade Down",
            "ui.wcol_menu_item.shadedown",
            default=-30, min=-100, max=100)
        gen("tooltip_outline", FVPColor, "Tooltip Outline",
            "ui.wcol_tooltip.outline",
            default=(1.0, 1.0, 1.0, 1.0))
        gen("tooltip_inner", FVPColor, "Tooltip Inner",
            "ui.wcol_tooltip.inner",
            default=(0.4, 0.4, 0.4, 1.0))
        gen("tooltip_text", FVPColor, "Tooltip Text",
            "ui.wcol_tooltip.text",
            default=(1.0, 1.0, 1.0, 1.0))
        gen("tooltip_show_shaded", props.BoolProperty, "Shaded",
            "ui.wcol_tooltip.show_shaded",
            default=False)
        gen("tooltip_shadetop", props.IntProperty, "Shade Top",
            "ui.wcol_tooltip.shadetop",
            default=30, min=-100, max=100)
        gen("tooltip_shadedown", props.IntProperty, "Shade Down",
            "ui.wcol_tooltip.shadedown",
            default=-30, min=-100, max=100)
        gen("text", FVPColor, "Text",
            "theme.view_3d.space.text_hi",
            default=(1.0, 1.0, 1.0, 1.0))

    line = FVPColor(
        name="Line",
        default=(1.0, 1.0, 1.0, 1.0))
    separator = FVPColor(
        name="Separator",
        default=(1.0, 1.0, 1.0, 0.5))
    pointer = FVPColor(
        name="Pointer",
        default=(1.0, 1.0, 1.0, 1.0))
    pointer_outline = FVPColor(
        name="Pointer Outline",
        default=(0.0, 0.0, 0.0, 1.0))
    pie_sel = FVPColor(
        name="Pie Sel",
        default=(1.0, 1.0, 1.0, 0.8))
    menu_marker = FVPColor(
        name="Menu Marker",
        default=(1.0, 1.0, 1.0, 1.0))
    menu_marker_outline = FVPColor(
        name="Menu Marker Outline",
        default=(0.0, 0.0, 0.0, 1.0))
    item_highlight = FVPColor(
        name="Item Highlight",
        default=(1.0, 1.0, 1.0, 1.0),
        description="Item outline color",
    )


PieMenu_PG_Colors._generate_props()


def font_id_get(self):
    U = bpy.context.user_preferences
    path = U.system.font_path_ui
    if path:
        i = blf.load(path)
        if i != -1:
            return i
    return 0


def prop_menu_radius_get(self):
    if "menu_radius" in self:
        return self["menu_radius"]
    else:
        wu = vawm.widget_unit()
        space = 2  # draw.ICON_BOX_TEXT_BOX_MARGIN
        if self.draw_type == 'SIMPLE':
            n = 2  # itemは8個を想定。n = len(current_items) / 4
            return wu * (n - 0.5) + space * n
        else:
            # y1 = radius + wu + space
            # y2 = (radius + wu / 2) * math.sin(math.pi / 4) + wu / 2
            # y3 = (radius + wu / 2) * math.sin(math.pi / 4) - wu / 2
            # y4 = wu / 2
            # y1 - y2 = y3 - y4
            r = (-wu - space) / (1 - 2 * math.sin(math.pi / 4)) - wu / 2
            return r


def prop_menu_radius_set(self, value):
    self["menu_radius"] = value


class PieMenuPreferences(addongroup.AddonGroup,
                         bpy.types.PropertyGroup if "." in __name__ else
                         bpy.types.AddonPreferences):
    bl_idname = __package__

    submodules = None

    # menus = []

    font_id = props.IntProperty(
        name="Font ID",
        default=0,
        min=0,
        get=font_id_get)  # 読み込み専用
    font_id_mono = props.IntProperty(
        name="Font ID Mono",
        default=1,
        min=0)  # 読み込み専用
    # 中心からアイコンボックスの境界まで
    if DEFAULT_CORRECTED_RADIUS:
        menu_radius = props.IntProperty(
            name="Menu Radius",
            # default=30,
            min=10,
            get=prop_menu_radius_get,
            set=prop_menu_radius_set,
        )
    else:
        menu_radius = props.IntProperty(
            name="Menu Radius",
            default=0,
            min=10,
        )
    menu_radius_center = props.IntProperty(
        name="Menu Radius Center",
        default=10,
        min=0)
    # submenuに切り替えた際に中心を変えない
    lock_menu_location = props.BoolProperty(
        name="Lock Menu Location",
        default=True)

    # Itemの上下の隙間がこれより狭いならmenu_radiusを広げる
    item_min_space = props.IntProperty(
        name="MenuItem Min Space",
        default=4,
        min=0)

    colors = props.PointerProperty(
        type=PieMenu_PG_Colors)
    """:type: PieMenu_PG_Colors"""

    draw_type = props.EnumProperty(
        name="Draw Type",
        description="Default draw type",
        items=[('SIMPLE', "Simple", ""),
               ('BOX', "Box", ""),
               ('CIRCLE', "Circle", ""),
               ('SIMPLE_BOX', "Simple - Box", ""),
               ('SIMPLE_CIRCLE', "Simple - Circle", "")],
        default='BOX'
    )

    # def reset_menus(self):
    #     self.menus.clear()
    #     pass

    def draw(self, context):
        layout = self.layout
        layout.context_pointer_set("addon_preferences", self)

        draw_install = False
        try:
            import pie_menu
        except:
            draw_install = True
        else:
            try:
                mod = importlib.import_module(
                    ".".join(__name__.split(".")[:-1]))
            except:
                draw_install = True
            else:
                if pie_menu.VERSION != mod.bl_info["version"]:
                    draw_install = True
        if draw_install:
            dst = ops.WM_OT_pie_menu_module_install.install_path()
            row = layout.row()
            row.operator(ops.WM_OT_pie_menu_module_install.bl_idname,
                         text="Install Module")
            row = layout.row()
            row.label("Install Path: " + dst)
            if ops.module_installed:
                row = layout.row()

                row.label("Restart Blender !", icon='ERROR')
            layout.separator()

            super().draw(context)
            return

        colors = self.colors

        column = layout.column()
        sp = column.split()
        col = sp.column()
        col.prop(self, "draw_type")
        draw_property(col, self, "menu_radius", context_attr="addon_preferences", unset=True)
        # col.prop(self, "menu_radius")
        col.prop(self, "menu_radius_center")
        col = sp.column()
        col.prop(self, "lock_menu_location")
        # col.prop(self, "item_min_space")  # わざわざ設定する人もいないだろう
        col.prop(colors, "use_theme", "Use Current Theme")

        split = layout.split()

        column = split.column()
        sub = column.box().column()

        sub.prop(colors, "line")
        sub.prop(colors, "separator")
        sub.prop(colors, "pointer")
        sub.prop(colors, "pointer_outline")
        sub.prop(colors, "pie_sel")
        sub.prop(colors, "item_highlight")

        column = split.column()
        sub = column.box().column()

        sub.active = not colors.use_theme
        sub.label("Menu Back:")
        sub.prop(colors, "menu_inner", text="Inner")
        sub.prop(colors, "menu_show_shaded")
        sub2 = sub.column(align=True)
        sub2.active = colors.menu_show_shaded
        sub2.prop(colors, "menu_shadetop")
        sub2.prop(colors, "menu_shadedown")
        sub.prop(colors, "text")

        column = split.column()
        sub = column.box().column()

        sub.active = not colors.use_theme
        sub.label("Title:")
        sub.prop(colors, "title_outline", text="Outline")
        sub.prop(colors, "title_inner", text="Inner")
        sub.prop(colors, "title_inner_sel", text="Inner Sel")
        sub.prop(colors, "title_text", text="Text")
        sub.prop(colors, "title_text_sel", text="Text Sel")
        sub.prop(colors, "title_show_shaded")
        sub2 = sub.column(align=True)
        sub2.active = colors.title_show_shaded
        sub2.prop(colors, "title_shadetop")
        sub2.prop(colors, "title_shadedown")

        column = split.column()
        sub = column.box().column()

        sub.active = not colors.use_theme
        sub.label("Item:")
        sub.prop(colors, "item_outline", text="Outline")
        sub.prop(colors, "item_inner", text="Inner")
        sub.prop(colors, "item_inner_sel", text="Inner Sel")
        sub.prop(colors, "item_text", text="Text")
        sub.prop(colors, "item_text_sel", text="Text Sel")
        sub.prop(colors, "item_show_shaded")
        sub2 = sub.column(align=True)
        sub2.active = colors.item_show_shaded
        sub2.prop(colors, "item_shadetop")
        sub2.prop(colors, "item_shadedown")

        column = split.column()
        sub = column.box().column()

        sub.active = not colors.use_theme
        sub.label("Tooltip:")
        sub.prop(colors, "tooltip_outline", text="Outline")
        sub.prop(colors, "tooltip_inner", text="Inner")
        sub.prop(colors, "tooltip_text", text="Text")
        sub.prop(colors, "tooltip_show_shaded")
        sub2 = sub.column(align=True)
        sub2.active = colors.tooltip_show_shaded
        sub2.prop(colors, "tooltip_shadetop")
        sub2.prop(colors, "tooltip_shadedown")

        draw_separator(layout)

        super().draw(context)
