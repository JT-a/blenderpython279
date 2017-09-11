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


import enum
import os
import math

import bgl
import blf
from mathutils import Vector

from ..utils import vagl
from ..utils import vawm

from .preferences import PieMenuPreferences
from . import drawicon
from . import oputils

try:
    import pie_menu
except:
    pie_menu = None


# icon_size = ICON_DEFAULT_HEIGHT * (PIXEL_SIZE * dpi / 72.0)
ICON_DEFAULT_HEIGHT = 16

CALC_TEXT_HEIGHT = "W"  # text_height = blf.dimensions(0, CALC_TEXT_HEIGHT)[1]
ICON_BOX_TEXT_BOX_MARGIN = 2
TOOLTIP_MAX_EXECUTE_LINES = 10
GUID_LINE_LENGTH = 10

DISABLE_CROSS_CURSOR = True


class Direction(enum.IntEnum):
    TOP = 0  # UPPER
    # TOP_RIGHT = 1
    RIGHT = 2
    # BOTTOM_RIGHT = 3
    BOTTOM = 4  # LOWER
    # BOTTOM_LEFT = 5
    LEFT = 6
    # TOP_LEFT = 7


class DrawingManager:
    @property
    def prefs(self):
        return PieMenuPreferences.get_instance()

    @property
    def menu(self):
        return self.op.base_menu

    @property
    def icon_box_size(self):
        if self.menu.draw_type == 'SIMPLE':
            return self.widget_unit
        else:
            return self.widget_unit * max(1.0, self.menu.icon_scale)

    def __init__(self, context, op):
        # modal中で変更されるものは入れない
        if not context or not op:
            return
        u = context.user_preferences
        self.op = op

        self.widget_unit = vawm.widget_unit()
        self.dpi = context.user_preferences.system.dpi
        f = u.system.pixel_size * self.dpi / 72
        # フォントの高さ。blf.dimensionsでは一定にならないのでこれを使う
        self.font_height = u.ui_styles[0].widget.points * f
        self.font_height_mono = u.ui_styles[0].widget.points * f
        # # フォント上端（下端）からwidgetまでの距離
        # self.font_space_y = (self.widget_unit - self.font_height) / 2
        # self.font_space_y_mono = (self.widget_unit - self.font_height_mono) / 2

        self.set_font_size(context)

        # グリフ高さの最大値を求める
        id0 = self.prefs.font_id
        id1 = self.prefs.font_id_mono
        blf.enable(id0, blf.WORD_WRAP)
        blf.enable(id1, blf.WORD_WRAP)
        blf.word_wrap(id0, -1)  # \nでのみ改行を行う
        blf.word_wrap(id1, -1)
        _, h1 = blf.dimensions(id0, "0")
        _, h2 = blf.dimensions(id0, "0\n0")
        self.max_glyph_height = (h2 - h1)
        _, h1 = blf.dimensions(id1, "0")
        _, h2 = blf.dimensions(id1, "0\n0")
        self.max_glyph_height_mono = (h2 - h1)
        blf.disable(id0, blf.WORD_WRAP)
        blf.disable(id1, blf.WORD_WRAP)

        # boxの丸め半径
        self.round_radius = self.widget_unit * 0.2
        # 通常アイコンの大きさ。widget_unit * 0.8 でも可
        self.icon_size = ICON_DEFAULT_HEIGHT * f

        # TODO: 暫定的な調整値
        self.ICON_TEXT_MARGIN = self.widget_unit * 0.2

    def update(self, context, op):
        self.__init__(context, op)

    def set_font_size(self, context):
        prefs = self.prefs
        u = context.user_preferences
        size = u.ui_styles[0].widget.points * int(u.system.pixel_size)
        blf.size(prefs.font_id, size, self.dpi)
        blf.size(prefs.font_id_mono, size, self.dpi)

    def rect_update(self, rect, xmin, ymin, xmax, ymax):
        rect[0] = xmin if rect[0] is None else min(rect[0], xmin)
        rect[1] = ymin if rect[1] is None else min(rect[1], ymin)
        rect[2] = xmax if rect[2] is None else max(rect[2], xmax)
        rect[3] = ymax if rect[3] is None else max(rect[3], ymax)

    def round_corner(self, v, position):
        """丸めた座標のリストを返す"""
        def circle_verts_num(r):
            """描画に最適な？円の頂点数を求める"""
            n = 32
            threshold = 2.0  # pixcel
            while True:
                if r * 2 * math.pi / n > threshold:
                    return n
                n -= 4
                if n < 1:
                    return 1

        r = self.round_radius
        num = circle_verts_num(r)
        n = int(num / 4)
        if num <= 4:
            return [v]
        circle = [[v[0] + r * math.cos(a), v[1] + r * math.sin(a)]
                  for a in [math.pi * 2 / num * i for i in range(num)]]
        if position == "top_right":
            verts = [[v[0] - r, v[1] - r] for v in circle[0: n + 1]]
            verts[0][0] = v[0]
            verts[-1][1] = v[1]
        elif position == "top_left":
            verts = [[v[0] + r, v[1] - r] for v in circle[n: n * 2 + 1]]
            verts[0][1] = v[1]
            verts[-1][0] = v[0]
        elif position == "bottom_left":
            verts = [[v[0] + r, v[1] + r] for v in circle[n * 2: n * 3 + 1]]
            verts[0][0] = v[0]
            verts[-1][1] = v[1]
        elif position == "bottom_right":
            verts = [[v[0] - r, v[1] + r]
                     for v in (circle[n * 3:] + [circle[0]])]
            verts[0][1] = v[1]
            verts[-1][0] = v[0]

        return verts

    def gen_text_position(self, string, is_mono=False):
        """描画位置のY座標とboxの幅・高さを返すジェネレータ。
        sendメソッドでは (string, is_mono) か string を渡す。
        一行しかない場合、boxの高さはwidget_unitで固定される。
        Noneを渡すと終了。
        :param string: 改行文字を含む場合は複数行と見做し、
            返り値のY座標は最初の行の位置を表す。
        :type string: str:
        :param is_mono: 固定幅文字を使うなら真。
        :type is_mono: bool
        :return: (描画位置のY座標(boxの上端を基準にして負の方向に進む),
                  boxの幅, boxの高さ)
        :rtype tuple
        """
        y = 0
        width = height = 0

        widget_unit = self.widget_unit

        while True:
            if is_mono:
                font_id = self.prefs.font_id_mono
            else:
                font_id = self.prefs.font_id
            th = blf.dimensions(font_id, CALC_TEXT_HEIGHT)[1]
            if string is not None:
                for line in string.split("\n"):
                    if y == 0:
                        h = widget_unit / 2 + th / 2
                    else:
                        if is_mono:
                            h = self.max_glyph_height_mono
                        else:
                            h = self.max_glyph_height
                    y -= h
                    height += h
                    width = max(width, blf.dimensions(font_id, line)[0])
            h_under = widget_unit / 2 - th / 2
            if y == 0:  # 最初の呼び出しでstringが空文字の場合
                recv = (yield 0, widget_unit, widget_unit)
            else:
                recv = (yield y, width + widget_unit, height + h_under)

            if recv is None:
                string, is_mono = None, False
            elif isinstance(recv, str):
                string, is_mono = recv, False
            else:
                string, is_mono = recv

    def draw_box(self, x, y, w, h,
                 col_back=None, col_inner=None, col_outline=None,
                 back_show_shaded=False, back_shadetop=0, back_shadedown=0,
                 inner_show_shaded=False, inner_shadetop=0, inner_shadedown=0):
        round_radius = self.round_radius

        # アンチエイリアスの効き具合が変わってくるので揃える
        # x = int(x)
        # y = int(y)
        # w = int(w)
        # h = int(h)

        if col_back:
            if back_show_shaded:
                color_top, color_bottom = vagl.shade_color(
                    col_back, back_shadetop, back_shadedown)
                vagl.draw_rounded_box(x, y, w, h, round_radius, True,
                                      color_top, color_bottom)
            else:
                bgl.glColor4f(*col_back)
                vagl.draw_rounded_box(x, y, w, h, round_radius, True)
        if col_inner:
            if inner_show_shaded:
                color_top, color_bottom = vagl.shade_color(
                    col_inner, inner_shadetop, inner_shadedown)
                vagl.draw_rounded_box(x, y, w, h, round_radius, True,
                                      color_top, color_bottom)
            else:
                bgl.glColor4f(*col_inner)
                vagl.draw_rounded_box(x, y, w, h, round_radius, True)
        if col_outline:
            bgl.glColor4f(*col_outline)
            vagl.draw_rounded_box(x, y, w, h, round_radius)

    def draw_text_box(
            self, x, y, text, origin="lower_left",
            col_back=None, col_inner=None, col_outline=None, col_text=None,
            back_show_shaded=False, back_shadetop=0, back_shadedown=0,
            inner_show_shaded=False, inner_shadetop=0, inner_shadedown=0,
            is_mono=False):
        """
        :param origin: x, yの基準がboxのどこにあるか。
                enum in ["upper", "upper_left", "left", "lower_left",
                         "lower", "lower_right", "right", "upper_right"]
        :type text: str
        """
        prefs = self.prefs
        widget_unit = self.widget_unit

        _, w, h = self.gen_text_position(text, is_mono).send(None)
        if "right" in origin:
            x -= w
        elif "left" not in origin:  # ["upper", "lower"]
            x -= w / 2
        if "upper" in origin:
            y -= h
        elif "lower" not in origin:  # ["left", "right"]
            y -= h / 2

        self.draw_box(x, y, w, h, col_back, col_inner, col_outline,
                      back_show_shaded, back_shadetop, back_shadedown,
                      inner_show_shaded, inner_shadetop, inner_shadedown)

        if is_mono:
            font_id = prefs.font_id_mono
        else:
            font_id = prefs.font_id
        lines = text.split("\n")
        if col_text:
            bgl.glColor4f(*col_text)
        g = self.gen_text_position(lines[0], is_mono)
        y2 = None
        for line in lines:
            if y2 is None:
                y2, _, _ = g.send(None)
            else:
                y2, _, _ = g.send(line)
            blf.position(font_id, x + widget_unit / 2, y + h + y2, 0)
            vagl.blf_draw(prefs.font_id, line)

    def draw_icon(self, icon, x, y, size, active, enabled, arrow_rotation,
                  poly_line=None):
        prefs = self.prefs
        colors = prefs.colors

        menu = self.menu
        if menu.draw_type == 'SIMPLE':
            round_radius = 0.0
        elif menu.draw_type == 'BOX':
            round_radius = self.round_radius
        else:
            round_radius = self.widget_unit * menu.icon_scale / 2

        drawn = False
        if icon:
            alpha = 1.0 if enabled else 0.5
            if isinstance(icon, (list, tuple)):
                drawicon.draw_fill(icon, x, y, size, 1.0,
                                   poly_line=poly_line)
                drawn = True
            else:
                drawn = drawicon.draw(icon, x, y, size, alpha,
                                      poly_line=poly_line)

        # アイコンがない場合は矢印を描く
        if not drawn:
            if 0:
                if active and enabled:
                    bgl.glColor4f(*vagl.thin_color(colors.item_text_sel, 0.5))
                else:
                    bgl.glColor4f(*vagl.thin_color(colors.item_text, 0.5))
                bgl.glLineWidth(2.0)
                r = size * 0.3
                vagl.draw_circle(x + size / 2, y + size / 2, r, 32)
                bgl.glLineWidth(1.0)
            alpha = 1.0 if enabled else 0.5
            icon = os.path.join(os.path.dirname(__file__), "arrow.png")
            drawicon.draw(icon, x, y, size, alpha, round_radius,
                          arrow_rotation)

    def calc_item_rect(self, index, label, icon):
        """Itemの描画位置を求める。
        icon_sizeが0以下("connected")の場合はicon_boxとtext_boxは重なる
        :param index: menu.current_items内での位置
        :type index: int | str
        :type label: str
        :type icon: str
        :return: アイコンとテキスト部分のrect
        :rtype: ([float, float, float, float], [float, float, float, float])
        """
        prefs = self.prefs
        wu = self.widget_unit
        menu = self.menu
        """:type: PieMenu"""

        num = len(menu.current_items)
        pie_angle = math.pi * 2 / num
        start_angle = math.pi * 0.5

        if menu.icon_scale > 1.0:
            icon_box_size = wu * menu.icon_scale
        else:
            icon_box_size = wu

        angle = start_angle - pie_angle * index
        if index == 0:
            direction = "top"
        elif index == int(num / 2):
            direction = "bottom"
        elif index < int(num / 2):
            direction = "right"
        else:
            direction = "left"

        tw = blf.dimensions(prefs.font_id, label)[0]

        if menu.draw_type == 'SIMPLE':
            # label + icon: ( 0.4 | WU | 0.1 | text | 0.5 )
            # label:        ( 0.5 | text | 0.5 )
            # icon:         ( 0.4 | WU | 0.4 )
            if label:
                if icon and icon != 'NONE':
                    w = tw + wu * 2
                else:
                    w = tw + wu
            else:
                w = wu * 1.8
            h = wu

            i = index
            if i > int(num / 2):
                i = -i + num
            # y = menu.co[1] + menu.radius_ - (wu + prefs.item_min_space) * i
            y = (menu.co[1] + menu.radius_ -
                 (menu.radius_ * 2 + wu) / (num / 2) * i)

            if direction in {"top", "bottom"}:
                x = menu.co[0] - w / 2
            elif index == int(num / 4):
                x = menu.co[0] + menu.radius_
            elif index == int(num / 4 * 3):
                x = menu.co[0] - menu.radius_ - w
            else:
                y2 = y + wu * 0.5 - menu.co[1]
                x2 = abs(y2 / math.tan(angle))
                if index < int(num / 2):
                    x = menu.co[0] + x2
                else:
                    x = menu.co[0] - x2 - w

            text_box_rect = [x, y, x + w, y + h]
            if icon and icon != 'NONE':
                icon_box_rect = [x + wu * 0.4, y, x + wu * 0.4 + wu, y + h]
            else:
                icon_box_rect = []

        else:
            v = Vector(((menu.radius_ + icon_box_size / 2) * math.cos(angle),
                        (menu.radius_ + icon_box_size / 2) * math.sin(angle)))
            icon_center = menu.co + v

            x = icon_center[0] - icon_box_size / 2
            y = icon_center[1] - icon_box_size / 2
            icon_box_rect = [x, y, x + icon_box_size, y + icon_box_size]

            if label:
                offset = ICON_BOX_TEXT_BOX_MARGIN
                w = tw + wu
                h = wu
                if direction in {"top", "bottom"}:
                    if direction == "top":
                        y = icon_box_rect[3] + offset
                    else:
                        y = icon_box_rect[1] - offset - h
                    x = icon_center[0] - w / 2
                else:
                    if direction == "left":
                        x = icon_box_rect[0] - offset - w
                    else:
                        x = icon_box_rect[2] + offset
                    y = icon_center[1] - h / 2
                text_box_rect = [x, y, x + w, y + h]
            else:
                text_box_rect = []

        return icon_box_rect, text_box_rect

    def draw_active_item_background(self):
        prefs = self.prefs
        colors = prefs.colors
        menu = self.menu
        items = menu.current_items
        widget_unit = self.widget_unit

        if menu.active_index == -1 or not menu.is_valid_click:
            return
        if not items[menu.active_index]:
            return

        r_icon = self.icon_box_size / 2

        i = menu.active_index
        subdiv = 32 if len(items) <= 2 else 16
        if 0:
            angle_start, angle_end = menu.item_boundary_angles[i]
        else:
            pie_angle = math.pi * 2 / len(items)
            angle_start = math.pi * 0.5 - pie_angle * i + pie_angle / 2
            angle_end = angle_start - pie_angle
        angle_subdiv = (angle_start - angle_end) / subdiv
        x, y = menu.co
        bgl.glColor4f(*colors.pie_sel)
        if 0:
            if menu.draw_type == 'SIMPLE':
                if len(menu.menu_items) <= 4:
                    r1 = menu.radius_ - widget_unit * 0.2
                else:
                    # この辺は適当
                    _, rect = self.calc_item_rect(
                        int(len(menu.menu_items) / 4) - 1, "DUMMY", 'NONE')
                    v = Vector((rect[0], rect[1]))
                    r1 = (rect[1] - menu.co[1]) - widget_unit * 0.2
                # r2 = menu.radius_ + r_icon * 2 + widget_unit * 0.2
                r2 = r1 + r_icon * 2 + widget_unit * 0.4
            else:
                r1 = menu.radius_ - widget_unit * 0.2
                r2 = menu.radius_ + r_icon * 2 + widget_unit * 0.2
        else:
            r1 = menu.radius_ - GUID_LINE_LENGTH
            r2 = menu.radius_

        # r1 = prefs.menu_radius_center + widget_unit * 0.5
        # r2 = prefs.menu_radius_center + widget_unit * 0.8
        # bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        bgl.glBegin(bgl.GL_QUAD_STRIP)
        for m in range(subdiv + 1):
            ang = angle_start - angle_subdiv * m
            cosf = math.cos(ang)
            sinf = math.sin(ang)
            bgl.glVertex2f(x + r1 * cosf, y + r1 * sinf)
            bgl.glVertex2f(x + r2 * cosf, y + r2 * sinf)
        bgl.glEnd()

    def draw_guid_lines(self):
        prefs = self.prefs
        colors = prefs.colors
        menu = self.menu
        items = menu.current_items
        icon_box_size = self.icon_box_size
        if 0:
            r1 = (prefs.menu_radius_center +
                  (menu.radius_ - prefs.menu_radius_center) / 2)
            # r1 = menu.radius_
            r2 = menu.radius_ + icon_box_size + 5
        else:
            r1 = menu.radius_ - GUID_LINE_LENGTH
            r2 = menu.radius_
        x, y = menu.co
        col1 = colors.separator
        bgl.glColor4f(*col1)

        if len(items) >= 2:
            if 0:
                for i, item in enumerate(items):
                    if not item:
                        continue
                    ang, _ = menu.item_boundary_angles[i]
                    cosf = math.cos(ang)
                    sinf = math.sin(ang)
                    bgl.glBegin(bgl.GL_LINE_STRIP)
                    bgl.glVertex2f(x + r1 * cosf, y + r1 * sinf)
                    bgl.glVertex2f(x + r2 * cosf, y + r2 * sinf)
                    bgl.glEnd()
            else:
                pie_angle = math.pi * 2 / len(items)
                ang = math.pi * 2 + pie_angle / 2
                for i in range(len(items)):
                    cosf = math.cos(ang)
                    sinf = math.sin(ang)
                    bgl.glBegin(bgl.GL_LINE_STRIP)
                    bgl.glVertex2f(x + r1 * cosf, y + r1 * sinf)
                    bgl.glVertex2f(x + r2 * cosf, y + r2 * sinf)
                    bgl.glEnd()
                    ang -= pie_angle

        # 中心の円
        bgl.glColor4f(*colors.line)
        subdiv = 16 if prefs.menu_radius_center < 20 else 32
        vagl.draw_circle(menu.co[0], menu.co[1], prefs.menu_radius_center,
                         subdiv)

    def draw_titles(self):
        """メニュータイトルと、前、次、親メニューを描画"""
        prefs = self.prefs
        colors = prefs.colors
        widget_unit = self.widget_unit
        menu = self.menu

        _icon_box_rect, text_box_rect = self.calc_item_rect(0, "DUMMY", "")
        w = blf.dimensions(prefs.font_id, menu.label)[0] + widget_unit
        h = widget_unit
        x = menu.co[0] - w / 2
        y = text_box_rect[3] + widget_unit

        col_kwargs = {
            "col_inner": colors.title_inner_sel,
            "col_outline": colors.title_outline,
            "col_text": colors.title_text_sel,
            "inner_show_shaded": colors.title_show_shaded,
            "inner_shadetop": colors.title_shadetop,
            "inner_shadedown": colors.title_shadedown,
        }
        self.draw_text_box(x, y, menu.label, **col_kwargs)
        self.rect_update(menu.rect, x, y, x + w, y + h)

        # # Draw Modifier
        # mod = self.op.last_modifier()
        # for key, p in zip(["shift", "ctrl", "alt", "oskey"],
        #                   [(-1, 1), (-1, -1), (1, 1), (1, -1)]):
        #     attr = key + "_items"
        #     items = getattr(menu, attr)
        #     if not items:
        #         continue
        #     r = widget_unit * 0.2
        #     if p[0] == 1:
        #         cx = x + w + r + 2
        #     else:
        #         cx = x - (r + 2)
        #     if p[1] == 1:
        #         cy = y + h / 2 + r + 1
        #     else:
        #         cy = y + h / 2 - r - 1
        #     bgl.glColor4f(*colors.menu_inner)
        #     vagl.draw_circle(cx, cy, r, 16, True)
        #     if key == mod:
        #         bgl.glColor4f(*colors.item_inner_sel)
        #     else:
        #         bgl.glColor4f(*colors.item_inner)
        #     vagl.draw_circle(cx, cy, r, 16, True)
        #     bgl.glColor4f(*colors.item_outline)
        #     vagl.draw_circle(cx, cy, r, 16, False)
        has_shift = has_ctrl = False
        for item in menu.menu_items:
            if item is not None:
                if item.shift:
                    has_shift = True
                if item.ctrl:
                    has_ctrl = True
        mod = self.op.last_modifier()
        for has_sub_item, key, p in [(has_shift, "shift", (1, 1)),
                                     (has_ctrl, "ctrl", (1, -1))]:
            if not has_sub_item:
                continue
            r = widget_unit * 0.2
            if p[0] == 1:
                cx = x + w + r + 2
            else:
                cx = x - (r + 2)
            if p[1] == 1:
                cy = y + h / 2 + r + 1
            else:
                cy = y + h / 2 - r - 1
            bgl.glColor4f(*colors.menu_inner)
            vagl.draw_circle(cx, cy, r, 16, True)
            if key == mod:
                bgl.glColor4f(*colors.item_inner_sel)
            else:
                bgl.glColor4f(*colors.item_inner)
            vagl.draw_circle(cx, cy, r, 16, True)
            bgl.glColor4f(*colors.item_outline)
            vagl.draw_circle(cx, cy, r, 16, False)

        # others
        col_kw = col_kwargs.copy()
        col_kw["col_inner"] = colors.title_inner
        col_kw["col_text"] = colors.title_text

        # Next
        if menu.next:
            sub_menu = pie_menu.get_menu(menu.next)
            if sub_menu:
                w2 = blf.dimensions(prefs.font_id, sub_menu.label)[0]
                w2 += widget_unit
                x2 = x + w + widget_unit
                self.draw_text_box(x2, y, sub_menu.label, **col_kw)
                self.rect_update(menu.rect, x2, y, x2 + w2, y + widget_unit)

        # Prev
        if menu.prev:
            sub_menu = pie_menu.get_menu(menu.prev)
            if sub_menu:
                w2 = blf.dimensions(prefs.font_id, sub_menu.label)[0]
                w2 += widget_unit
                x2 = x - widget_unit - w2
                self.draw_text_box(x2, y, sub_menu.label, **col_kw)
                self.rect_update(menu.rect, x2, y, x2 + w2, y + widget_unit)

        # History
        if self.op.menu_history:
            y2 = y + h + widget_unit / 2
            for idname, label in self.op.menu_history[::-1]:
                w2 = blf.dimensions(prefs.font_id, label)[0]
                w2 += widget_unit
                x2 = menu.co[0] - w2 / 2
                self.draw_text_box(x2, y2, label, **col_kw)
                self.rect_update(menu.rect, x2, y2, x2 + w2, y2 + widget_unit)
                y2 += widget_unit * 1.5

    # def draw_arrow(self):
    #     """マウスカーソルの方向を指す矢印"""
    #     prefs = self.prefs
    #     menu = self.menu
    #     vec = self.op.mco - menu.co
    #     r_center2 = prefs.menu_radius_center + 2
    #     if vec.length >= prefs.menu_radius_center:
    #         base_w = 16
    #         top_w = 3
    #         handlength = self.widget_unit * 0.6
    #         v = vec.normalized()  # copy
    #         bgl.glColor4f(*prefs.colors.pointer)
    #         vagl.draw_trapezoid(menu.co + v * r_center2,
    #                             v * handlength, base_w, top_w, poly=True)
    #         bgl.glColor4f(*prefs.colors.pointer_outline)
    #         bgl.glLineWidth(2)
    #         vagl.draw_trapezoid(menu.co + v * r_center2,
    #                             v * handlength, base_w, top_w)
    #         bgl.glLineWidth(1)

    def draw_item(self, item, index, active, enabled, highlight):
        prefs = self.prefs
        menu = self.menu
        current_items = menu.current_items

        colors = prefs.colors
        widget_unit = self.widget_unit

        num = len(current_items)
        if index == 0:
            direction = "top"
        elif num % 2 == 0 and index == int(num / 2):
            direction = "bottom"
        elif index < num / 2:
            direction = "right"
        else:
            direction = "left"

        icon_box = item.icon_box_rect
        text_box = item.text_box_rect

        if active:
            col = colors.item_inner_sel
            if not enabled:
                col = vagl.thin_color(col, 0.5)  # TODO: 調整
        else:
            col = colors.item_inner
        if colors.item_show_shaded:
            col_box_top, col_box_bottom = vagl.shade_color(
                col, colors.item_shadetop, colors.item_shadedown)
        else:
            col_box_top = col_box_bottom = col

        if menu.draw_type == 'SIMPLE':
            icon_box_poly_coords = line_coords_icon = []
            icon_size = self.icon_size
        else:
            u1, v1, u2, v2 = icon_box
            if menu.draw_type == 'BOX':
                icon_box_poly_coords = line_coords_icon = (
                    self.round_corner([u1, v1], "bottom_left") +
                    self.round_corner([u2, v1], "bottom_right") +
                    self.round_corner([u2, v2], "top_right") +
                    self.round_corner([u1, v2], "top_left")
                )

                f = self.widget_unit - self.icon_size
                icon_expand = min(max(0.0, menu.icon_expand), 1.0)
                icon_size = self.icon_size + f * icon_expand
            else:
                icon_box_poly_coords = line_coords_icon = []
                subdivide = 32
                radius = (u2 - u1) / 2
                angle = math.pi
                ang = math.pi * 2 / subdivide
                icon_center = (u1 + u2) / 2, (v1 + v2) / 2
                for i in range(subdivide):
                    co = [icon_center[0] + radius * math.cos(angle),
                          icon_center[1] + radius * math.sin(angle)]
                    icon_box_poly_coords.append(co)
                    angle += ang

                icon_expand = min(max(-1.0, menu.icon_expand), 1.0)
                if icon_expand > 0:
                    f = self.widget_unit - self.icon_size
                    icon_size = self.icon_size + f * icon_expand
                else:
                    f = self.icon_size - self.widget_unit * math.sin(math.pi / 4)
                    icon_size = self.icon_size - f * -icon_expand
            icon_size *= menu.icon_scale

        if text_box:
            x1, y1, x2, y2 = text_box
            bottom_left = self.round_corner([x1, y1], "bottom_left")
            bottm_right = self.round_corner([x2, y1], "bottom_right")
            top_right = self.round_corner([x2, y2], "top_right")
            top_left = self.round_corner([x1, y2], "top_left")
            text_box_poly_coords = line_coords = (
                top_left + bottom_left + bottm_right + top_right)
        else:
            text_box_poly_coords = line_coords = []

        if colors.menu_show_shaded:
            _, text_box_rect_top = self.calc_item_rect(0, "DUMMY", "")
            _, text_box_rect_down = self.calc_item_rect(
                int(len(current_items) / 2), "DUMMY", "")
            menu_ymax = text_box_rect_top[3]
            menu_ymin = text_box_rect_down[1]
            col_menu_inner_top, col_menu_inner_bottom = vagl.shade_color(
                colors.menu_inner, colors.menu_shadetop, colors.menu_shadedown)

        def get_menu_inner_color(y):
            y = max(menu_ymin, min(y, menu_ymax))
            f = (y - menu_ymin) / (menu_ymax - menu_ymin)
            return vagl.blend_color(col_menu_inner_top,
                                    col_menu_inner_bottom, f)

        # Draw Back
        # menu back color
        bgl.glColor4f(*colors.menu_inner)
        if colors.menu_inner[3] > 0.0:
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for v in text_box_poly_coords:
                if colors.menu_show_shaded:
                    col = get_menu_inner_color(v[1])
                    bgl.glColor4f(*col)
                bgl.glVertex2f(*v)
            bgl.glEnd()
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for v in icon_box_poly_coords:
                if colors.menu_show_shaded:
                    col = get_menu_inner_color(v[1])
                    bgl.glColor4f(*col)
                bgl.glVertex2f(*v)
            bgl.glEnd()

        # item inner
        bgl.glColor4f(*col_box_top)
        if col_box_top[3] > 0.0 or col_box_bottom[3] > 0.0:
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for v in text_box_poly_coords:
                if colors.item_show_shaded:
                    f = (v[1] - text_box[1]) / widget_unit
                    col = vagl.blend_color(col_box_top, col_box_bottom, f)
                    bgl.glColor4f(*col)
                bgl.glVertex2f(*v)
            bgl.glEnd()
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for v in icon_box_poly_coords:
                if colors.item_show_shaded:
                    f = (v[1] - icon_box[1]) / (icon_box[3] - icon_box[1])
                    col = vagl.blend_color(col_box_top, col_box_bottom, f)
                    bgl.glColor4f(*col)
                bgl.glVertex2f(*v)
            bgl.glEnd()

        # Draw Icon
        if icon_box:
            icon_center = [(icon_box[0] + icon_box[2]) / 2,
                           (icon_box[1] + icon_box[3]) / 2]
            icon_x = icon_center[0] - icon_size / 2
            icon_y = icon_center[1] - icon_size / 2
            rotation = -math.pi * 2 / num * index
            if menu.draw_type == 'SIMPLE':
                poly_line = None
            else:
                poly_line = icon_box_poly_coords
            self.draw_icon(item.icon, icon_x, icon_y, icon_size, active,
                           enabled, rotation, poly_line)

        # Draw Outline
        if highlight:
            bgl.glColor4f(*colors.item_highlight)
            bgl.glLineWidth(2.0)
        else:
            bgl.glColor4f(*colors.item_outline)
        bgl.glBegin(bgl.GL_LINE_LOOP)
        for v in line_coords:
            bgl.glVertex2f(*v)
        bgl.glEnd()
        bgl.glBegin(bgl.GL_LINE_LOOP)
        for v in line_coords_icon:
            bgl.glVertex2f(*v)
        bgl.glEnd()
        bgl.glLineWidth(1.0)

        # Draw Text
        if text_box:
            if not enabled:
                col = vagl.thin_color(colors.item_text, 0.5)
            elif active:
                col = list(colors.item_text_sel)
            else:
                col = list(colors.item_text)
            bgl.glColor4f(*col)
            if menu.draw_type == 'SIMPLE':
                if icon_box:
                    # (0.4 | WU | 0.1 | text | 0.5)
                    x = text_box[0] + widget_unit * 1.5
                else:
                    # ( 0.5 | text | 0.5 )
                    x = text_box[0] + widget_unit * 0.5
            else:
                x = text_box[0] + widget_unit * 0.5

            th = blf.dimensions(prefs.font_id, CALC_TEXT_HEIGHT)[1]
            y = text_box[1] + widget_unit / 2 - th / 2
            blf.position(prefs.font_id, x, y, 0)
            vagl.blf_draw(prefs.font_id, item.label)

        # Menu Marker
        if item.menu:
            b = math.sqrt(2)
            f = b * math.sin(math.pi / 4) / 2
            box = text_box or icon_box
            if direction == "left":
                co = [box[0] + 2, box[1] + 2]
                v = [-f, -f]
            else:
                co = [box[2] - 2, box[1] + 2]
                v = [f, -f]
            if (menu.active_item_index == index and item.enabled and
                    menu.is_valid_click):
                l = 14
            else:
                l = 10
            v = [v[0] * l, v[1] * l]
            bgl.glColor4f(*colors.menu_inner)
            vagl.draw_triangle_relative(co, l * b, v, poly=True)
            bgl.glColor4f(*colors.menu_marker)
            vagl.draw_triangle_relative(co, l * b, v, poly=True)
            bgl.glColor4f(*colors.menu_marker_outline)
            vagl.draw_triangle_relative(co, l * b, v)

        # Shortcut
        ls = ('ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN',
              'EIGHT', 'NINE')
        if item.shortcut in ls:
            shortcut = str(ls.index(item.shortcut))
        else:
            shortcut = item.shortcut
        if shortcut and shortcut != 'NONE':
            if direction == "left":
                tw = blf.dimensions(prefs.font_id, shortcut)[0]
                x = text_box[0] - widget_unit / 2 - tw
            else:
                x = text_box[2] + widget_unit / 2
            y = text_box[1] + widget_unit / 2 - th / 2
            blf.position(prefs.font_id, x, y, 0)
            bgl.glColor4f(*colors.text)
            vagl.blf_draw(prefs.font_id, shortcut)

    def draw_items(self):
        menu = self.menu
        # アクティブな物を最後に描画
        idx_items = list(enumerate(menu.current_items))
        for i, item in idx_items:
            if i == menu.active_index:
                idx_items = idx_items[:i] + idx_items[i + 1:] + [idx_items[i]]
                break

        if menu.highlight == 'NONE':
            highlight_direction = 'NONE'
        elif menu.highlight == 'LAST':
            highlight_direction = menu.get_last_item_direction()
        else:
            highlight_direction = menu.highlight

        for i, item in idx_items:
            if not item:
                continue
            active = i == menu.active_index or i == menu.active_item_index
            if not menu.is_valid_click:
                active = False
            enabled = item.enabled
            highlight = (item.direction == highlight_direction and
                         highlight_direction != 'NONE')
            self.draw_item(item, i, active, enabled, highlight)

    def draw_tooltip(self, context):
        if not self.op.show_tooltip:
            return
        prefs = self.prefs
        colors = prefs.colors
        menu = self.menu
        if menu.active_item_index == -1 or not menu.is_valid_click:
            return
        for i, item in enumerate(menu.current_items):
            if i == menu.active_item_index:
                break
        else:
            return
        rect = item.text_box_rect or item.icon_box_rect

        if item.description:
            g = self.gen_text_position(item.description)
        else:
            g = self.gen_text_position(None)
        _y, w, h = g.send(None)
        execute_string = item.get_execute_string()
        if execute_string:
            ls = execute_string.split("\n")
            if len(ls) > TOOLTIP_MAX_EXECUTE_LINES:
                execute_string = "\n".join(
                    ls[:TOOLTIP_MAX_EXECUTE_LINES] + ["..."])
            execute_string = oputils.format_execute_string(
                execute_string, True)
            exec_lines = execute_string.split("\n")
            execute_string = "\n".join(["Python: " + exec_lines[0]] +
                                       [" " * 8 + s for s in exec_lines[1:]])
            _y, w, h = g.send((execute_string, True))
        else:
            execute_string = ""
        if item.menu:
            menu_string = "Menu: " + item.menu
            _y, w, h = g.send((menu_string, True))
        else:
            menu_string = ""

        g.close()
        minx = (rect[0] + rect[2]) / 2 - w / 2
        miny = rect[1] - self.widget_unit * 0.2 - h
        win = context.window
        if minx + w > win.width:
            minx = win.width - w
        if minx < 0:
            minx = 0
        if miny < 0:
            miny = 0
        if miny + h > win.height:
            miny = win.height - h
        self.draw_box(minx, miny, w, h,
                      col_inner=colors.tooltip_inner,
                      col_outline=colors.tooltip_outline,
                      inner_show_shaded=colors.tooltip_show_shaded,
                      inner_shadetop=colors.tooltip_shadetop,
                      inner_shadedown=colors.tooltip_shadedown)

        g = self.gen_text_position(None)
        g.send(None)
        maxy = miny + h
        if item.description:
            bgl.glColor4f(*colors.tooltip_text)
            for line in item.description.split("\n"):
                ty, w, h = g.send(line)
                blf.position(prefs.font_id,
                             minx + self.widget_unit / 2, maxy + ty, 0)
                blf.draw(prefs.font_id, line)

        if execute_string or menu_string:
            # 青みがかった色にする
            col_exec = list(colors.tooltip_text)
            if col_exec[0] > 0.2 or col_exec[1] > 0.2:
                col_exec[0] = max(0.0, col_exec[0] - 0.2)
                col_exec[1] = max(0.0, col_exec[1] - 0.2)
            else:
                col_exec[2] = min(1.0, col_exec[2] + 0.2)
            bgl.glColor4f(*col_exec)

            lines = [s for s in execute_string.split("\n") if s]
            if menu_string:
                lines.append(menu_string)
            for line in lines:
                ty, w, h = g.send((line, True))
                blf.position(prefs.font_id_mono,
                             minx + self.widget_unit / 2, maxy + ty, 0)
                blf.draw(prefs.font_id_mono, line)
        g.close()

    def draw(self, context):
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glLineWidth(1.0)
        bgl.glShadeModel(bgl.GL_SMOOTH)

        self.set_font_size(context)

        menu = self.menu
        menu.rect = [None] * 4
        for i, item in enumerate(menu.current_items):
            if item:
                item.rect = [None] * 4
                item.icon_box_rect, item.text_box_rect = self.calc_item_rect(
                    i, item.label, item.icon)

        self.draw_active_item_background()
        self.draw_guid_lines()
        self.draw_titles()
        self.draw_items()
        # self.draw_arrow()
        self.draw_tooltip(context)
