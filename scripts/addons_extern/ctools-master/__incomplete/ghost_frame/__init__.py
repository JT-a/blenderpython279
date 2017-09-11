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
    'name': 'Ghost Frame',
    'author': 'chromoly',
    'version': (0, 1),
    'blender': (2, 77, 0),
    'location': 'View3D',
    'description': '',
    'warning': '',
    'wiki_url': 'https://github.com/chromoly/ghost_frame',
    'tracker_url': '',
    'category': '3D View'}


import os
import math

import bpy

from .utils import AddonPreferences, SpaceProperty


class GhostFramePreferences(
        AddonPreferences,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout


class VIEW3D_PG_GhostFrameAspect(bpy.types.PropertyGroup):
    enable = bpy.props.BoolProperty()
    ghost_type = bpy.props.EnumProperty(
        items=(('A', '', ''),
               ('B', '', ''),
               ('C', '', '')),
        default='A')
    # Around Frame
    ghost_step = bpy.props.FloatProperty()
    ghost_size = bpy.props.FloatProperty()
    # In Range
    ghost_frame_start = bpy.props.FloatProperty()
    ghost_frame_end = bpy.props.FloatProperty()
    ghost_frame_step = bpy.props.FloatProperty()

    # 共通
    show_only_ghost_selected = bpy.props.BoolProperty()


space_prop = SpaceProperty(
    [bpy.types.SpaceView3D, 'ghost_frame', VIEW3D_PG_GhostFrameAspect])


textures = {}


"""
"""

def gen_texture(context, scene, area, region, frame):
    render = scene.render
    """:type: bpy.types.RenderSettings"""

    view3d = area.spaces.active
    if view3d.region_quadviews:
        for r, rv3d in zip([r for r in area.regions if r.type == 'WINDOW'],
                           view3d.region_quadviews):
            if r == region:
                break
    else:
        rv3d = view3d.region_3d
    modelview_mat = tuple([tuple(r) for r in rv3d.view_matrix])
    projection_mat = tuple([tuple(r) for r in rv3d.window_matrix])

    # key = (area.as_pointer, frame, region.width, region.height, modelview_mat,
    #        projection_mat)
    # if key in textures:
    #     return textures[key]

    w = render.resolution_x
    h = render.resolution_y
    scale = render.resolution_percentage
    format = render.image_settings.file_format
    color_mode = render.image_settings.color_mode
    compression = render.image_settings.compression
    filepath = render.filepath
    frame_current = scene.frame_current

    render.resolution_x = region.width
    render.resolution_y = region.height
    render.resolution_percentage = 100
    render.image_settings.file_format = 'PNG'
    render.image_settings.color_mode = 'RGBA'
    render.image_settings.compression = 15

    context_dict = context.copy()
    context_dict['scene'] = scene
    context_dict['area'] = area
    context_dict['region'] = region

    for frame in range(100):
        path = os.path.join(bpy.app.tempdir,
                            '{}_{}.png'.format(area.as_pointer(), frame))
        scene.frame_set(frame)
        render.filepath = path
        print(path)
        bpy.ops.render.opengl(context_dict, write_still=True)

    # restore
    render.resolution_x = w
    render.resolution_y = h
    render.resolution_percentage = scale
    render.image_settings.file_format = format
    render.image_settings.color_mode = color_mode
    render.image_settings.compression = compression
    render.filepath = filepath
    scene.frame_set(frame_current)


class VIEW3D_OT_ghost(bpy.types.Operator):
    bl_idname = 'view3d.ghost'
    bl_label = 'Ghost'
    def execute(self, context):
        import time
        t = time.time()
        gen_texture(context, context.scene, context.area, context.region, 0)
        print(time.time() - t)
        return {'FINISHED'}


def draw_callback_pre():
    context = bpy.context

    # 生成されたテクスチャをフレーム順に重ねて描画していく


def validate_texture_cache(context, view3d):
    # キャッシュを取得
    pass


def frame_change_post(dummy):
    context = bpy.context

    validate_texture_cache(context, None)



classes = [
    GhostFramePreferences,
    VIEW3D_PG_GhostFrameAspect,
    VIEW3D_OT_ghost,
]

addon_keymaps = []


handle = None


def register():
    global handle

    for cls in classes:
        bpy.utils.register_class(cls)

    space_prop.register()

    bpy.app.handlers.frame_change_post.append(frame_change_post)
    handle = bpy.types.SpaceView3D.draw_handler_add(
        draw_callback_pre, (), 'WINDOW', 'PRE_VIEW')

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    # if kc:
    #     km = kc.keymaps.new('Screen Editing', space_type='EMPTY')
    #     kmi = km.keymap_items.new('view3d.quadview_move', 'LEFTMOUSE', 'PRESS',
    #                               head=True)
    #     addon_keymaps.append((km, kmi))


def unregister():
    global handle

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
    handle = None
    bpy.app.handlers.frame_change_post.remove(frame_change_post)

    space_prop.unregister()

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
