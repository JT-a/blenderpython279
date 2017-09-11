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


import bgl

from ..utils import vagl


def gen_screenshot_texture(x, y, w, h):
    """window全体のスクショを撮る
    :rtype: int
    """
    def gen_texture():
        textures = bgl.Buffer(bgl.GL_INT, 1)
        bgl.glGenTextures(1, textures)
        tex = textures[0]
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, tex)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER,
                            bgl.GL_LINEAR)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER,
                            bgl.GL_LINEAR)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)
        return tex

    with vagl.GLSettings.push_attrib():
        bgl.glEnable(bgl.GL_SCISSOR_TEST)
        bgl.glScissor(x, y, w, h)
        tex = gen_texture()
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, tex)
        bgl.glCopyTexImage2D(bgl.GL_TEXTURE_2D, 0, bgl.GL_RGBA, 0, 0, w, h, 0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)
    return tex


def draw_texture(x, y, w, h, texture, mode=None):
    mode_bak = bgl.Buffer(bgl.GL_INT, 1)
    bgl.glGetIntegerv(bgl.GL_DRAW_BUFFER, mode_bak)
    if mode is not None:
        bgl.glDrawBuffer(mode)

    bgl.glEnable(bgl.GL_TEXTURE_2D)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture)

    bgl.glColor4d(1.0, 1.0, 1.0, 1.0)
    bgl.glBegin(bgl.GL_TRIANGLE_FAN)
    bgl.glTexCoord2d(0.0, 0.0)
    bgl.glVertex2i(x, y)
    bgl.glTexCoord2d(1.0, 0.0)
    bgl.glVertex2i(x + w, y)
    bgl.glTexCoord2d(1.0, 1.0)
    bgl.glVertex2i(x + w, y + h)
    bgl.glTexCoord2d(0.0, 1.0)
    bgl.glVertex2i(x, y + h)
    bgl.glEnd()

    bgl.glDisable(bgl.GL_TEXTURE_2D)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)

    if mode is not None:
        bgl.glDrawBuffer(mode_bak[0])


def cross2d(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]
