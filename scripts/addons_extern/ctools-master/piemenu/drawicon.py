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


import os
from collections import OrderedDict
import math
import types

import bpy
import bgl
from bpy_extras.image_utils import load_image

from ..utils import vagl

ICON_FILE_NAME = "blender_icons32.png"

icons = OrderedDict()


def make_icon_dict():
    # 一覧はsource/blender/editors/include/UI_icons.h
    bl_rna = bpy.types.UILayout.bl_rna
    items = bl_rna.functions["label"].parameters["icon"].enum_items
    for item in items:
        icons[item.identifier] = item.value


# 96x96
brush_icons = OrderedDict((
    ('BRUSH_ADD', "add.png"),
    ('BRUSH_BLOB', "blob.png"),
    ('BRUSH_BLUR', "blur.png"),
    ('BRUSH_CLAY', "clay.png"),
    ('BRUSH_CLAY_STRIPS', "claystrips.png"),
    ('BRUSH_CLONE', "clone.png"),
    ('BRUSH_CREASE', "crease.png"),
    ('BRUSH_DARKEN', "darken.png"),
    ('BRUSH_FILL', "fill.png"),
    ('BRUSH_FLATTEN', "flatten.png"),
    ('BRUSH_GRAB', "grab.png"),
    ('BRUSH_INFLATE', "inflate.png"),
    ('BRUSH_LAYER', "layer.png"),
    ('BRUSH_LIGHTEN', "lighten.png"),
    ('BRUSH_MASK', "mask.png"),
    ('BRUSH_MIX', "mix.png"),
    ('BRUSH_MULTIPLY', "multiply.png"),
    ('BRUSH_NUDGE', "nudge.png"),
    ('BRUSH_PINCH', "pinch.png"),
    ('BRUSH_SCRAPE', "scrape.png"),
    ('BRUSH_SCULPT_DRAW', "draw.png"),
    ('BRUSH_SMEAR', "smear.png"),
    ('BRUSH_SMOOTH', "smooth.png"),
    ('BRUSH_SNAKE_HOOK', "snake_hook.png"),
    ('BRUSH_SOFTEN', "soften.png"),
    ('BRUSH_SUBTRACT', "subtract.png"),
    ('BRUSH_TEXDRAW', "texdraw.png"),
    ('BRUSH_TEXFILL', "texfill.png"),
    ('BRUSH_TEXMASK', "texmask.png"),
    ('BRUSH_THUMB', "thumb.png"),
    ('BRUSH_ROTATE', "twist.png"),
    ('BRUSH_VERTEXDRAW', "vertexdraw.png"))
)

# 512x512
matcap_icons = \
    OrderedDict(("MATCAP_{:02d}".format(i), "mc{:02d}.jpg".format(i))
                for i in range(1, 25))  # MATCAP_01: mc01.jpg


def vicon_view3d_draw(x, y, w, h, alpha=1.0):
    cx = x + w / 2
    cy = y + h / 2
    d = max(2, h / 3)

    bgl.glColor4f(0.5, 0.5, 0.5, alpha)
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(x, cy - d)
    bgl.glVertex2f(x + w, cy - d)
    bgl.glVertex2f(x, cy + d)
    bgl.glVertex2f(x + w, cy + d)

    bgl.glVertex2f(cx - d, y)
    bgl.glVertex2f(cx - d, y + h)
    bgl.glVertex2f(cx + d, y)
    bgl.glVertex2f(cx + d, y + h)
    bgl.glEnd()

    bgl.glColor4f(0.0, 0.0, 0.0, alpha)
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(x, cy)
    bgl.glVertex2f(x + w, cy)
    bgl.glVertex2f(cx, y)
    bgl.glVertex2f(cx, y + h)
    bgl.glEnd()


def viconutil_draw_tri(pts):
    bgl.glBegin(bgl.GL_TRIANGLES)
    bgl.glVertex2f(*pts[0])
    bgl.glVertex2f(*pts[1])
    bgl.glVertex2f(*pts[2])
    bgl.glEnd()


def viconutil_draw_lineloop(pts):
    bgl.glBegin(bgl.GL_LINE_LOOP)
    for p in pts:
        bgl.glVertex2f(*p)
    bgl.glEnd()


def viconutil_draw_lineloop_smooth(pts):
    linesmooth = vagl.Buffer("bool", 0, bgl.GL_LINE_SMOOTH)
    if not linesmooth:
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
    viconutil_draw_lineloop(pts)
    if not linesmooth:
        bgl.glDisable(bgl.GL_LINE_SMOOTH)


def viconutil_draw_points(pts, point_size):
    bgl.glBegin(bgl.GL_QUADS)
    for p in pts:
        bgl.glVertex2f(p[0] - point_size, p[1] - point_size)
        bgl.glVertex2f(p[0] + point_size, p[1] - point_size)
        bgl.glVertex2f(p[0] + point_size, p[1] + point_size)
        bgl.glVertex2f(p[0] - point_size, p[1] + point_size)
    bgl.glEnd()


def vicon_edit_draw(x, y, w, h, alpha=1.0):
    pts = ((x + 3, y + 3),
           (x + w - 3, y + 3),
           (x + w - 3, y + h - 3),
           (x + 3, y + h - 3))
    bgl.glColor4f(0.0, 0.0, 0.0, alpha)
    viconutil_draw_lineloop(pts)
    bgl.glColor3f(1, 1, 0.0)
    viconutil_draw_points(pts, 1)


def vicon_editmode_dehlt_draw(x, y, w, h, alpha=1.0):
    pts = ((x + w / 2, y + h - 2),
           (x + 3, y + 4),
           (x + w - 3, y + 4))

    bgl.glColor4f(0.0, 0.0, 0.0, 1)
    viconutil_draw_lineloop_smooth(pts)

    bgl.glColor3f(0.9, 0.9, 0.9)
    viconutil_draw_points(pts, 1)


def vicon_editmode_hlt_draw(x, y, w, h, alpha=1.0):
    pts = ((x + w / 2, y + h - 2),
           (x + 3, y + 4),
           (x + w - 3, y + 4))
    bgl.glColor4f(0.5, 0.5, 0.5, alpha)
    viconutil_draw_tri(pts)

    bgl.glColor4f(0.0, 0.0, 0.0, 1)
    viconutil_draw_lineloop_smooth(pts)

    bgl.glColor3f(1, 1, 0.0)
    viconutil_draw_points(pts, 1)


def vicon_disclosure_tri_right_draw(x, y, w, h, alpha=1.0):
    cx = x + w / 2
    cy = y + w / 2
    d = w / 3
    d2 = w / 5

    pts = ((cx - d2, cy + d),
           (cx - d2, cy - d),
           (cx + d2, cy))

    shademodel = vagl.Buffer("int", 0, bgl.GL_SHADE_MODEL)
    bgl.glShadeModel(bgl.GL_SMOOTH)
    bgl.glBegin(bgl.GL_TRIANGLES)
    bgl.glColor4f(0.8, 0.8, 0.8, alpha)
    bgl.glVertex2f(*pts[0])
    bgl.glVertex2f(*pts[1])
    bgl.glColor4f(0.3, 0.3, 0.3, alpha)
    bgl.glVertex2f(*pts[2])
    bgl.glEnd()
    bgl.glShadeModel(shademodel)

    bgl.glColor4f(0.0, 0.0, 0.0, 1)
    viconutil_draw_lineloop_smooth(pts)


def vicon_disclosure_tri_down_draw(x, y, w, h, alpha=1.0):
    cx = x + w / 2
    cy = y + w / 2
    d = w / 3
    d2 = w / 5

    pts = ((cx + d, cy + d2),
           (cx - d, cy + d2),
           (cx, cy - d2))

    shademodel = vagl.Buffer("int", 0, bgl.GL_SHADE_MODEL)
    bgl.glShadeModel(bgl.GL_SMOOTH)
    bgl.glBegin(bgl.GL_TRIANGLES)
    bgl.glColor4f(0.8, 0.8, 0.8, alpha)
    bgl.glVertex2f(*pts[0])
    bgl.glVertex2f(*pts[1])
    bgl.glColor4f(0.3, 0.3, 0.3, alpha)
    bgl.glVertex2f(*pts[2])
    bgl.glEnd()
    bgl.glShadeModel(shademodel)

    bgl.glColor4f(0.0, 0.0, 0.0, 1)
    viconutil_draw_lineloop_smooth(pts)


def vicon_move_up_draw(x, y, w, h, alpha=1.0):
    # d = -2
    d = w / 3 / 2

    linesmooth = vagl.Buffer("bool", 0, bgl.GL_LINE_SMOOTH)
    linewidth = vagl.Buffer("float", 0, bgl.GL_LINE_WIDTH)
    if not linesmooth:
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(1)
    bgl.glColor3f(0.0, 0.0, 0.0)

    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex2f(x + w / 2 - d * 2, y + h / 2 + d)
    bgl.glVertex2f(x + w / 2, y + h / 2 - d + 1)
    bgl.glVertex2f(x + w / 2 + d * 2, y + h / 2 + d)
    bgl.glEnd()

    if not linesmooth:
        bgl.glDisable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(linewidth)


def vicon_move_down_draw(x, y, w, h, alpha=1.0):
    # d = 2
    d = w / 3 / 2

    linesmooth = vagl.Buffer("bool", 0, bgl.GL_LINE_SMOOTH)
    linewidth = vagl.Buffer("float", 0, bgl.GL_LINE_WIDTH)
    if not linesmooth:
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(1)
    bgl.glColor3f(0.0, 0.0, 0.0)

    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex2f(x + w / 2 - d * 2, y + h / 2 + d)
    bgl.glVertex2f(x + w / 2, y + h / 2 - d - 1)
    bgl.glVertex2f(x + w / 2 + d * 2, y + h / 2 + d)
    bgl.glEnd()

    if not linesmooth:
        bgl.glDisable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(linewidth)


def vicon_x_draw(x, y, w, h, alpha=1.0):
    x += 3
    y += 3
    w -= 6
    h -= 6

    linesmooth = vagl.Buffer("bool", 0, bgl.GL_LINE_SMOOTH)
    linewidth = vagl.Buffer("float", 0, bgl.GL_LINE_WIDTH)
    if not linesmooth:
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(2.5)

    bgl.glColor4f(0.0, 0.0, 0.0, alpha)
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(x, y)
    bgl.glVertex2f(x + w, y + h)
    bgl.glVertex2f(x + w, y)
    bgl.glVertex2f(x, y + h)
    bgl.glEnd()

    if not linesmooth:
        bgl.glDisable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(linewidth)


def vicon_small_tri_right_draw(x, y, w, h, alpha=1.0):
    cx = x + w / 2 - 4
    cy = y + w / 2
    d = w / 5
    d2 = w / 7

    pts = ((cx - d2, cy + d),
           (cx - d2, cy - d),
           (cx + d2, cy))

    bgl.glColor4f(0.2, 0.2, 0.2, alpha)

    shademodel = vagl.Buffer("int", 0, bgl.GL_SHADE_MODEL)
    bgl.glShadeModel(bgl.GL_SMOOTH)
    bgl.glBegin(bgl.GL_TRIANGLES)
    bgl.glVertex2f(*pts[0])
    bgl.glVertex2f(*pts[1])
    bgl.glVertex2f(*pts[2])
    bgl.glEnd()
    bgl.glShadeModel(shademodel)


internal_icons = OrderedDict((
    ('VIEW3D_VEC', vicon_view3d_draw),
    ('EDIT_VEC', vicon_edit_draw),
    ('EDITMODE_VEC_DEHLT', vicon_editmode_dehlt_draw),
    ('EDITMODE_VEC_HLT', vicon_editmode_hlt_draw),
    ('DISCLOSURE_TRI_RIGHT_VEC', vicon_disclosure_tri_right_draw),
    ('DISCLOSURE_TRI_DOWN_VEC', vicon_disclosure_tri_down_draw),
    ('MOVE_UP_VEC', vicon_move_up_draw),
    ('MOVE_DOWN_VEC', vicon_move_down_draw),
    ('X_VEC', vicon_x_draw),
    ('SMALL_TRI_RIGHT_VEC', vicon_small_tri_right_draw)
))


icon_buffer = []  # [buffer, img_sx, img_sy]
textures = {}  # {[texture(int), buffer, sx, sy, x, y, w, h] or func, ...}


def get_image_buffer(path):
    img = load_image(path)
    if not img:
        return None
    sx, sy = img.size
    buf = bgl.Buffer(bgl.GL_FLOAT, 4 * sx * sy)
    img.gl_load(filter=bgl.GL_LINEAR, mag=bgl.GL_LINEAR)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, img.bindcode[0])
    bgl.glGetTexImage(bgl.GL_TEXTURE_2D, 0,
                      bgl.GL_RGBA, bgl.GL_FLOAT, buf)
    img.gl_free()
    img.user_clear()
    bpy.data.images.remove(img)
    return buf, sx, sy


def get_texture(name):
    """nameが"icons"なら全体のテクスチャを返す
    :type name: str
    """
    if name in textures:
        return textures[name]

    if name in internal_icons:
        textures[name] = internal_icons[name]
        return textures[name]

    if name == "icons":
        icon_type = "icons"
    elif name in icons and icons[name] < 780:  # 780は"BRUSH_ADD":
        icon_type = "icon"
    elif name in brush_icons:
        icon_type = "brush"
    elif name in matcap_icons:
        icon_type = "matcap"
    elif "." in name:  # 拡張子のドット
        icon_type = "image"
    else:
        return None

    dirname = os.path.dirname(os.path.abspath(__file__))

    if name == "icons":
        filepath = os.path.join(dirname, ICON_FILE_NAME)
        img = load_image(filepath)
        if not img:
            return None
        sx, sy = img.size
        buf = bgl.Buffer(bgl.GL_FLOAT, 4 * sx * sy)
        img.gl_load(filter=bgl.GL_LINEAR, mag=bgl.GL_LINEAR)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, img.bindcode[0])
        bgl.glGetTexImage(bgl.GL_TEXTURE_2D, 0,
                          bgl.GL_RGBA, bgl.GL_FLOAT, buf)
        img.gl_free()
        img.user_clear()
        bpy.data.images.remove(img)
        x = y = 0
        w = sx
        h = sy

    elif icon_type == "icon":
        if "icons" not in textures:
            get_texture("icons")
        tex, buf, sx, sy, _x, _y, _w, _h = textures["icons"]
        row, col = divmod(icons[name], 26)
        x = 10 + (40 + 2) * col
        y = 10 + (40 + 2) * row
        w = h = 32

    elif icon_type in ("brush", "matcap"):
        if icon_type == "brush":
            filepath = os.path.join(dirname, "brushicons", brush_icons[name])
        else:
            filepath = os.path.join(dirname, "matcaps", matcap_icons[name])
        buf, sx, sy = get_image_buffer(filepath)
        if not buf:
            return None
        x = y = 0
        w, h = sx, sy
    else:
        buf, sx, sy = get_image_buffer(name)
        if not buf:
            return None
        x = y = 0
        w, h = sx, sy

    if icon_type == "icon":
        textures[name] = [tex, buf, sx, sy, x, y, w, h]
    else:
        texture = bgl.Buffer(bgl.GL_INT, 1)  # GLuint
        bgl.glGenTextures(1, texture)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture[0])
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER,
                            bgl.GL_LINEAR)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER,
                            bgl.GL_LINEAR)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_S, bgl.GL_CLAMP)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_T, bgl.GL_CLAMP)
        bgl.glTexImage2D(bgl.GL_TEXTURE_2D, 0, bgl.GL_RGBA,
                         sx, sy, 0, bgl.GL_RGBA, bgl.GL_FLOAT, buf)
        textures[name] = [texture[0], buf, sx, sy, x, y, w, h]
    return textures[name]


def draw_fill(color, x, y, size, alpha=1.0, round_radius=0.0, poly_line=None):
    cx = x + size / 2
    cy = y + size / 2

    round_radius = min(size / 2, round_radius)

    gl_blend = bgl.Buffer(bgl.GL_BYTE, 1)
    bgl.glGetIntegerv(bgl.GL_BLEND, gl_blend)
    bgl.glEnable(bgl.GL_BLEND)

    if poly_line is not None:
        coords = [(co[0] - x, co[1] - y) for co in poly_line]
    else:
        r = round_radius
        pi = math.pi
        coords = []  # 0.0 ~ +size の範囲
        # 左下
        coords += vagl.draw_arc_get_vectors(
            r, r, r, pi, pi * 3 / 2, 4)
        # 右下
        coords += vagl.draw_arc_get_vectors(
            x + size - r, r, r, pi * 3 / 2, 0.0, 4)
        # 右上
        coords += vagl.draw_arc_get_vectors(
            x + size - r, y + size - r, r, 0.0, pi / 2, 4)
        # 左上
        coords += vagl.draw_arc_get_vectors(
            r, y + size - r, r, pi / 2, pi, 4)

    if len(color) == 3:
        color = list(color) + [1.0]
    color = vagl.thin_color(color, alpha)
    bgl.glColor4f(*color)

    bgl.glBegin(bgl.GL_POLYGON)
    for co in coords:
        bgl.glVertex2f(co[0] + x, co[1] + y)
    bgl.glEnd()

    if not gl_blend[0]:
        bgl.glDisable(bgl.GL_BLEND)

    return True


def draw(icon, x, y, size, alpha=1.0, round_radius=0.0, rotation=0.0,
         poly_line=None):
    """iconを描画
    :param icon: iconを示す文字列か番号。単色で塗りつぶす場合はRGBAを指定する
    :type icon: str | int | list | tuple
    :param x: 左下座標
    :type x: int
    :param y: 左下座標
    :type y: int
    :type size: int
    :type alpha: int | float
    :param round_radius: 角の丸め半径。size/2で円になる
    :type round_radius: int | float
    :param rotation: 回転させて描画する。回転はアイコンの中心が基準。
        時計回りが正
    :type: rotation: 0.0
    :param poly_line: 描画用のポリゴンの絶対座標。x,yからの相対座標ではない。
        [[x, y], ...]
    :type: list | tuple
    """

    if isinstance(icon, (list, tuple)):
        return draw_fill(icon, x, y, size, alpha, round_radius)

    if isinstance(icon, int):
        for name, value in icons.items():
            if value == icon:
                icon = name
                break
        else:
            return False

    if not icon or icon == 'NONE':
        return False
    else:
        tex_data = get_texture(icon)
    if not tex_data:
        print("icon not found", icon)
        return False

    if isinstance(tex_data, types.FunctionType):  # internal_icons用
        tex_data(x, y, size, size, alpha)
        return True

    texture, buf, sx, sy, xmin, ymin, w, h = tex_data
    round_radius = min(size / 2, round_radius)

    if poly_line is not None:
        coords = [(co[0] - x, co[1] - y) for co in poly_line]
    elif round_radius != 0.0:
        r = round_radius
        pi = math.pi
        a = r
        b = size - r
        coords = []  # 0.0 ~ +size の範囲
        # 左下
        coords += vagl.draw_arc_get_vectors(a, a, r, pi, pi * 3 / 2, 4)
        # 右下
        coords += vagl.draw_arc_get_vectors(b, a, r, pi * 3 / 2, 0.0, 4)
        # 右上
        coords += vagl.draw_arc_get_vectors(b, b, r, 0.0, pi / 2, 4)
        # 左上
        coords += vagl.draw_arc_get_vectors(a, b, r, pi / 2, pi, 4)
    else:
        coords = [[0, 0], [size, 0], [size, size], [0, size]]

    with vagl.GLSettings.push_attrib(bgl.GL_ENABLE_BIT | bgl.GL_TEXTURE_BIT):
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_TEXTURE_2D)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture)

        bgl.glColor4f(1.0, 1.0, 1.0, alpha)

        bgl.glBegin(bgl.GL_POLYGON)
        for co in coords:
            fx = co[0] / size
            fy = co[1] / size
            tx = xmin / sx + max(w, h) / sx * fx
            ty = ymin / sy + max(w, h) / sy * fy
            bgl.glTexCoord2f(tx, ty)
            if rotation != 0.0:
                f = size / 2
                cx = co[0] - f
                cy = co[1] - f
                sin = math.sin(rotation)
                cos = math.cos(rotation)
                co = [cx * cos - cy * sin + f, cx * sin + cy * cos + f]
            bgl.glVertex2f(x + co[0], y + co[1])
        bgl.glEnd()

    return True


make_icon_dict()


###############################################################################
# Register / Unregister
###############################################################################
def register():
    pass


def unregister():
    if textures:
        tex_set = set()
        for tex, buf, sx, sy, _x, _y, _w, _h in textures.values():
            tex_set.add(tex)
        buf = bgl.Buffer(bgl.GL_INT, len(tex_set), list(tex_set))
        bgl.glDeleteTextures(len(buf), buf)
        textures.clear()
