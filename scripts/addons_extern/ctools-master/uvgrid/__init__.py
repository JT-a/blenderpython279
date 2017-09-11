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
    'name': 'Make UV Grid',
    'author': 'chromoly',
    'version': (0, 1, 2),
    'blender': (2, 78, 0),
    'location': 'Image Editor > Header > Image > Make UV Grid',
    'description': 'Make UV grid image',
    'warning': "need 'Pillow' python module",
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Image',
}


import importlib
import math
import numpy as np
from PIL import Image, ImageDraw

import bpy

try:
    importlib.reload(addongroup)
except NameError:
    from ..utils import addongroup


DEFAULT_PATTERN = 'CHECKER'  # 'CHECKER', 'CHECKER_CIRCLE', 'FULL'


def draw_grid(image, color, origin, offset, line_width, color_image=None,
              mask_image=None):
    color = tuple(color)
    if len(color) == 3:
        color += (255,)
    if color[3] == 0:
        return image

    if offset[0] == 0 or offset[1] == 0:
        raise ValueError()

    image_draw = ImageDraw.Draw(image, 'RGBA')
    use_mask = color[3] < 255
    if use_mask:
        color_image.paste(color[:3], [0, 0, *image.size])
        mask_image.paste(0, [0, 0, *image.size])
        mask_draw = ImageDraw.Draw(mask_image)
    width, height = image.size

    origin = [origin[0], height - 1 - origin[0]]
    while origin[0] + math.ceil(line_width / 2) > 0:
        origin[0] -= offset[0]
    while origin[1] + math.ceil(line_width / 2) < height:
        origin[1] += offset[1]

    i = 0
    while True:
        x = origin[0] + i * offset[0]
        if x - math.ceil(line_width / 2) > width:
            break
        if use_mask:
            mask_draw.line([(x, 0), (x, height)], fill=color[3],
                           width=line_width)
        else:
            image_draw.line([(x, 0), (x, height)], fill=color[:3],
                            width=line_width)
        i += 1
    i = 0
    while True:
        y = origin[1] - i * offset[1]
        if y + math.ceil(line_width / 2) < 0:
            break
        if use_mask:
            mask_draw.line([(0, y), (width, y)], fill=color[3],
                           width=line_width)
        else:
            image_draw.line([(0, y), (width, y)], fill=color[:3],
                            width=line_width)
        i += 1

    if use_mask:
        image = Image.composite(color_image, image, mask_image)

    return image


def draw_position(size, origin, offset, ext=0):
    """origin, offsetはblender(左下が原点)の座標系で、
    返り値はPILでの座標系(左上が原点)
    """
    width, height = size
    x = origin[0]
    y = height - 1 - origin[1]
    while y < height + ext:
        y += offset[1]
        x -= offset[2]
    while x < 0:
        x += offset[0]
    while x > -ext:
        x -= offset[0]
    while True:
        if x > width + ext:
            y -= offset[1]
            if y < -ext:
                break
            x += offset[2]
            while x > -ext:
                x -= offset[0]
            continue
        yield (x, y)
        x += offset[0]


def draw_checker(image, color, origin, offset, checker_size, color_image=None,
                 mask_image=None):
    color = tuple(color)
    if len(color) == 3:
        color += (255,)
    if color[3] == 0:
        return image

    if offset[0] == 0 or offset[1] == 0:
        raise ValueError()

    image_draw = ImageDraw.Draw(image, 'RGBA')
    use_mask = color[3] < 255
    if use_mask:
        color_image.paste(color[:3], [0, 0, *image.size])
        mask_image.paste(0, [0, 0, *image.size])
        mask_draw = ImageDraw.Draw(mask_image)

    for x, y in draw_position(image.size, origin, offset):
        if use_mask:
            mask_draw.rectangle(
                [x, y - checker_size[1] + 1, x + checker_size[0] - 1, y],
                fill=color[3])
        else:
            image_draw.rectangle(
                [x, y - checker_size[1] + 1, x + checker_size[0] - 1, y],
                fill=color[:3])

    if use_mask:
        image = Image.composite(color_image, image, mask_image)

    return image


def draw_circle(image, color, origin, offset, diameter, color_image=None,
                mask_image=None):
    # NOTE: 円を描く時にfillのalpha値が1より小さい時にアウトラインが濃いまま
    #       という問題が発生するので、Image.composite()を使用する事。

    color = tuple(color)
    if len(color) == 3:
        color += (255,)
    if color[3] == 0:
        return image

    image_draw = ImageDraw.Draw(image, 'RGBA')
    use_mask = color[3] < 255
    if mask_image:
        mask_scale = round(mask_image.width / image.width)
        mask_scale_y = round(mask_image.height / image.height)
        if mask_scale != mask_scale_y:
            raise ValueError()
        if mask_scale != 1.0:
            use_mask = True
    if use_mask:
        color_image.paste(color[:3], [0, 0, *image.size])
        mask_image.paste(0, [0, 0, *image.size])
        mask_draw = ImageDraw.Draw(mask_image)
        diameter *= mask_scale

    r, m = divmod(diameter - 1, 2)

    for x, y in draw_position(image.size, origin, offset, r):
        if use_mask:
            x *= mask_scale
            y *= mask_scale

        if use_mask:
            mask_draw.ellipse(
                [(x - r, y - r), (x + r + m, y + r + m)],
                fill=color[3])
        else:
            image_draw.ellipse(
                [(x - r, y - r), (x + r + m, y + r + m)],
                fill=color[:3])

    if use_mask:
        mask_image = mask_image.resize(image.size, Image.BICUBIC)
        image = Image.composite(color_image, image, mask_image)

    return image


class UVGridPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__


def make_uv_grid(
        width, height,
        grid_size, line_width, circle_diameter,
        col_base, col_checker, col_circle,
        col_grid, col_grid_sub,
        col_checker_shade=0.0, col_grid_shade=0.0,
        ssaa=2):
    col_base = tuple(col_base)
    if col_grid is not None:
        col_grid = tuple(col_grid)
    if col_grid_sub is not None:
        col_grid_sub = tuple(col_grid_sub)
    if col_checker is not None:
        col_checker = tuple(col_checker)
    if col_circle is not None:
        col_circle = tuple(col_circle)

    size = (width, height)
    size_ssaa = (width * ssaa, height * ssaa)

    image = Image.new('RGB', size, col_base[:3] + (255,))
    color_image = Image.new('RGB', size)
    mask_image = Image.new('L', size, 0)
    mask_image_ssaa = Image.new('L', size_ssaa, 0)

    # Draw Checker
    if col_checker:
        image = draw_checker(
            image, col_checker, [0, 0],
            [grid_size * 2, grid_size, grid_size],
            [grid_size, grid_size], color_image, mask_image)

    # Draw Sub Grid
    if col_grid_sub:
        image = draw_grid(
            image, col_grid_sub, [int(grid_size / 2), int(grid_size / 2)],
            [grid_size, grid_size], 1, color_image, mask_image)

    # Draw Shaded Checker
    if col_checker_shade != 0.0:
        if col_checker_shade > 0.0:
            col = (255, 255, 255, int(255 * col_checker_shade))
        else:
            col = (0, 0, 0, int(255 * -col_checker_shade))
        gs16 = grid_size * 16
        image = draw_checker(
            image, col, [gs16, 0],
            [gs16 * 2, gs16, gs16],
            [gs16, gs16], color_image, mask_image)

    # Draw Main Grid
    if col_grid:
        image = draw_grid(
            image, col_grid, [0, 0], [grid_size, grid_size], line_width,
            color_image, mask_image)

        # Draw Shaded Main Grid
        if col_grid_shade != 0.0:
            f = col_grid_shade
            if col_grid_shade > 0:
                col = [int(i * (1.0 - f) + 255 * f) for i in col_grid]
            else:
                col = [int(i * (1.0 + f)) for i in col_grid]
            col = tuple(col[:3] + [col_grid[3]])
            image = draw_grid(
                image, col, [0, 0], [grid_size * 8, grid_size * 8],
                line_width, color_image, mask_image)

    # Draw Circle
    if col_circle:
        origin = [round(grid_size / 2), grid_size + round(grid_size / 2)]
        offset = [grid_size * 4, grid_size * 2, grid_size * 2]
        image = draw_circle(
            image, col_circle, origin, offset,
            circle_diameter, color_image, mask_image_ssaa
        )

    # Convert to numpy array
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image = image.convert('RGBA')
    arr = np.asarray(image, dtype=np.float)
    arr.shape = -1
    arr /= 255

    return arr


# # numpy test
# """
# i = Image.open('lena.jpg')
# a = numpy.asarray(i) # a is readonly
# i = Image.fromarray(a)
#
# """
# def blend_array(front, back):
#     mixed = (front + back) / 2
#     alpha_front = front[:, :, 3]
#     alpha_back = back[:, :, 3]
#     a1 = alpha_front * alpha_back
#     a2 = alpha_front * (1 - alpha_back)
#     a3 = alpha_back * (1 - alpha_front)
#     a = a1 + a2 + a3
#     non_zero = a != 0.0
#     arr = (a1[:, :, np.newaxis] * mixed + a2[:, :, np.newaxis] * front +
#            a3[:, :,np.newaxis] * back)
#     arr[non_zero] /= a[non_zero]
#     arr[non_zero != True] = 0.0
#     arr[:, :, 3] = a[:, 0]
#     return arr


class OperatorUVGrid(bpy.types.Operator):
    bl_idname = 'image.make_uv_grid'
    bl_label = 'UV Grid'
    bl_options = {'REGISTER', 'UNDO'}

    image_size = bpy.props.IntVectorProperty(
        name='Image Size',
        default=(512, 512),
        min=1,
        max=65536,
        subtype='XYZ',
        size=2,
    )
    grid_size = bpy.props.IntProperty(
        name='Grid Size',
        default=32,
        min=1,
        max=65536,
    )
    line_width = bpy.props.IntProperty(
        name='Line Width',
        default=1,
        min=1,
        max=20,
    )
    circle_diameter = bpy.props.IntProperty(
        name= 'Circle Diameter',
        default=71,
        min=1,
        max=65536,
    )

    col_base = bpy.props.FloatVectorProperty(
        name='Base',
        default=(0.8, 0.8, 0.8),
        subtype='COLOR_GAMMA',
        size=3,
        min=0.0,
        max=1.0
    )
    col_checker = bpy.props.FloatVectorProperty(
        name='Checker',
        default=(0.9, 0.9, 0.9, 1.0),
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0,
        max=1.0
    )
    col_grid = bpy.props.FloatVectorProperty(
        name='Grid',
        default=(0.1, 0.1, 0.1, 1.0),
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0,
        max=1.0
    )
    col_grid_sub = bpy.props.FloatVectorProperty(
        name='Sub Grid',
        default=(0.6, 0.6, 0.6, 1.0),
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0,
        max=1.0
    )
    col_circle = bpy.props.FloatVectorProperty(
        name='Circle',
        default=((0.0, 0.0, 0.0, 0.0) if DEFAULT_PATTERN == 'CHECKER' else
                 (0.0, 0.0, 0.0, 0.24)),
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0,
        max=1.0
    )

    col_grid_shade = bpy.props.FloatProperty(
        name='Grid Shade',
        default=0.0 if DEFAULT_PATTERN != 'FULL' else 1.0,
        min=-1.0,
        max=1.0
    )
    col_checker_shade = bpy.props.FloatProperty(
        name='Checker Shade',
        default=0.0 if DEFAULT_PATTERN != 'FULL' else -0.15,
        min=-1.0,
        max=1.0
    )

    ssaa = bpy.props.IntProperty(
        name='SSAA',
        default=2,
        min=1,
        max=8,
    )

    @classmethod
    def poll(cls, context):
        return context.area and context.area.type == 'IMAGE_EDITOR'

    @classmethod
    def test_generate(cls, context):
        space_image = context.space_data
        """:type: bpy.types.SpaceImageEditor"""
        image = space_image.image
        if image:
            if image.source == 'GENERATED':
                generate = False
            elif image.source == 'FILE':
                if 0:
                    if not image.has_data:
                        image.source = 'GENERATED'
                        space_image.image = image  # 画面を更新する為
                    generate = False
                generate= not image.has_data
            else:
                generate = True
        else:
            generate = True
        return generate

    def verify_image(self, context):
        if context.area.type != 'IMAGE_EDITOR':
            return bpy.data.images.new('UV Grid', 512, 512, True)

        space_image = context.space_data
        """:type: bpy.types.SpaceImageEditor"""
        image = space_image.image
        if self.test_generate(context):
            image = bpy.data.images.new('UV Grid', 512, 512, True)
            """:type: bpy.types.Image"""
            space_image.image = image
        return image

    def draw(self, context):
        layout = self.layout

        if context.area.type != 'IMAGE_EDITOR':
            layout.label('Not Image Editor', icon='ERROR')
            return

        space_image = context.space_data
        """:type: bpy.types.SpaceImageEditor"""
        image = space_image.image

        for p in self.rna_type.properties:
            if p.identifier == 'rna_type':
                continue
            row = layout.row()
            if p.identifier == 'image_size':
                # GENERATED又は新規作成以外は無効化
                if image:
                    if image.source in {'SEQUENCE', 'MOVIE', 'VIEWER'}:
                        row.enabled = False
                    elif image.source == 'FILE':
                        if image.has_data:
                            row.enabled = False
            split = row.split()
            col = split.column()
            col.label(p.name)
            col = split.column()
            col.prop(self, p.identifier, text='')

        layout.separator()

        col = layout.column()
        if OperatorUVGrid.test_generate(context):
            text = 'New image'
        else:
            text = 'Update image'
        col.label(text, icon='INFO')

    def execute(self, context):
        if context.area.type != 'IMAGE_EDITOR':
            return {'CANCELLED'}

        win = context.window
        win.cursor_modal_set('WAIT')

        image = self.verify_image(context)
        if image.source == 'GENERATED':
            image.generated_width = self.image_size[0]
            image.generated_height = self.image_size[1]

        def conv(value):
            return tuple([round(f * 255) for f in value])

        arr = make_uv_grid(
            image.size[0], image.size[1],
            grid_size=self.grid_size, line_width=self.line_width,
            circle_diameter=self.circle_diameter,
            col_base=conv(self.col_base), col_checker=conv(self.col_checker),
            col_circle=conv(self.col_circle), col_grid=conv(self.col_grid),
            col_grid_sub=conv(self.col_grid_sub),
            col_checker_shade=self.col_checker_shade,
            col_grid_shade=self.col_grid_shade,
            ssaa=self.ssaa,
        )

        arr.shape = -1
        image.pixels = tuple(arr)  # listかtupleに変換してからのほうが若干速くなる

        win.cursor_modal_restore()

        context.area.tag_redraw()

        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.properties.is_property_set('image_size'):
            space_image = context.space_data
            """:type: bpy.types.SpaceImageEditor"""
            image = space_image.image
            if image and image.has_data:
                self.image_size = image.size

        return context.window_manager.invoke_props_dialog(self)


def menu_item(self, context):
    layout = self.layout
    col = layout.column()
    col.separator()
    col.operator(OperatorUVGrid.bl_idname, text='Make UV Grid')

classes = [
    UVGridPreferences,
    OperatorUVGrid,
]


@UVGridPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.IMAGE_MT_image.append(menu_item)


@UVGridPreferences.unregister_addon
def unregister():
    bpy.types.IMAGE_MT_image.remove(menu_item)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
