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
    'name': 'Lock 3D Cursor',
    'author': 'chromoly',
    'version': (0, 4, 2),
    'blender': (2, 78, 0),
    'location': '3D View -> Action Mouse / Alt + Action Mouse',
    'description': 'commit a791153: 3D Cursor: Add option to lock it in place '
                   'to prevent accidental modification',
    'warning': '',
    'wiki_url': 'https://github.com/chromoly/lock_cursor3d',
    'tracker_url': '',
    'category': '3D View'
}


import ctypes as ct
import importlib
import math

import bpy
import bgl
import blf
import bmesh
import mathutils
from mathutils import Vector
from mathutils import geometry as geom


try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(structures)
    importlib.reload(vagl)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import structures
    from ..utils import vagl


class LockCursorPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__


PROJECT_MIN_NUMBER = 1E-5


def project(region, rv3d, vec):
    """World Coords (3D) -> Window Coords (3D).
    Window座標は左手系で、Zのクリッピング範囲は0~1。
    """
    v = rv3d.perspective_matrix * vec.to_4d()
    if abs(v[3]) > PROJECT_MIN_NUMBER:
        v /= v[3]
    x = (1 + v[0]) * region.width * 0.5
    y = (1 + v[1]) * region.height * 0.5
    z = (1 + v[2]) * 0.5
    return Vector((x, y, z))


def unproject(region, rv3d, vec, depth_location:"world coords"=None):
    """Window Coords (2D / 3D) -> World Coords (3D).
    Window座標は左手系で、Zのクリッピング範囲は0~1。
    """
    x = vec[0] * 2.0 / region.width - 1.0
    y = vec[1] * 2.0 / region.height - 1.0
    if depth_location:
        z = (project(region, rv3d, depth_location)[2] - 0.5) * 2
    else:
        z = 0.0 if len(vec) == 2 else (vec[2] - 0.5) * 2
    v = rv3d.perspective_matrix.inverted() * Vector((x, y, z, 1.0))
    if abs(v[3]) > PROJECT_MIN_NUMBER:
        v /= v[3]
    return v.to_3d()


def center_of_circumscribed_circle_tri(v1, v2, v3):
    """三角形の外接円の中心点を求める"""
    if v1 != v2 and v2 != v3 and v3 != v1:
        # 垂直二等分線の交差点を求める
        v12 = v2 - v1
        v13 = v3 - v1
        med12 = (v1 + v2) / 2
        med13 = (v1 + v3) / 2
        per12 = v13 - v13.project(v12)
        per13 = v12 - v12.project(v13)
        inter = geom.intersect_line_line(med12, med12 + per12,
                                        med13, med13 + per13)
        if inter:
            return (inter[0] + inter[1]) / 2
    return None


class VIEW3D_OT_cursor3d(bpy.types.Operator):
    """組み込みのVIEW3D_OT_cursor3dを上書きする"""
    bl_idname = 'view3d.cursor3d'
    bl_label = 'Set 3D Cursor'
    bl_options = {'REGISTER'}

    operator_type = None

    use_modal = bpy.props.BoolProperty(
        name='Modal',
        default=False,
        options={'SKIP_SAVE'}
    )
    use_depth = bpy.props.BoolProperty(
        name='Depth',
        default=False,
        options={'SKIP_SAVE'}
    )
    use_snap = bpy.props.BoolProperty(
        name='Snap',
        default=False,
        options={'SKIP_SAVE'}
    )
    use_precision = bpy.props.BoolProperty(
        name='Precision',
        default=False,
        options={'SKIP_SAVE'}
    )

    @classmethod
    def poll(cls, context):
        if cls.operator_type is None:
            return False
        r = cls.operator_type.poll(context.as_pointer())
        return r and not context.space_data.lock_cursor_location

    def call_builtin_cursor3d(self, context, event):
        self.__class__.operator_type.invoke(
            context.as_pointer(), self.as_pointer(), event.as_pointer())

    def snap_to_circle(self, context):
        if context.mode == 'EDIT_MESH':
            ob = context.active_object
            mat = ob.matrix_world
            bm = bmesh.from_edit_mesh(ob.data)
            verts = [v for v in bm.verts if v.select]
            if len(verts) != 3:
                self.report({'WARNING'}, 'Select 3 vertices')
                return
            vecs = [mat * v.co for v in verts]
        elif context.mode == 'OBJECT':
            vecs = [ob.matrix_world.to_translation()
                    for ob in context.selected_objects]
            if len(vecs) != 3:
                self.report({'WARNING'}, 'Select 3 objects')
                return
        else:
            return

        center = center_of_circumscribed_circle_tri(*vecs)
        if center is not None:
            context.space_data.cursor_location = center

    def view_axis(self, context):
        """画面のZ軸の方を向いている軸を返す。
        :type context: bpy.types.Context
        :return: 返り値は次の何れか。 'x', 'y', 'z', '-x', '-y', '-z', ''
        :rtype: str
        """
        threshold = 1e-5

        if context.area.type != 'VIEW_3D':
            return None

        v3d = context.space_data
        rv3d = context.region_data
        if not rv3d:
            return None

        zvec = rv3d.view_matrix.inverted().col[2].to_3d()
        if hasattr(v3d, 'use_local_grid') and v3d.use_local_grid:
            zvec = v3d.local_grid_rotation.inverted() * zvec

        for i, axis in enumerate('xyz'):
            v = Vector([0.0, 0.0, 0.0])
            v[i] = 1.0
            f = zvec.dot(v)
            if f > 1.0 - threshold:
                return axis
            elif f < -1.0 + threshold:
                return '-' + axis
        return ''

    def snap_grid(self, context, vec, precision=False):
        """
        :type context: bpy.types.Context
        :type vec: mathutils.Vector
        :type precision: bool
        :rtype: mathutils.Vector
        """
        v3d = context.space_data
        """:type: bpy.types.SpaceView3D"""
        rv3d = context.region_data
        """:type: bpy.types.RegionView3D"""

        c_rv3d = structures.RegionView3D.cast(rv3d)
        bupg = c_rv3d.gridview
        if precision:
            if context.scene.unit_settings.system == 'NONE':
                bupg /= v3d.grid_subdivisions
            else:
                bupg /= 10

        localgrid = hasattr(v3d, 'use_local_grid') and v3d.use_local_grid

        if localgrid:
            origin = v3d.local_grid_location
            quat = v3d.local_grid_rotation
            mat = quat.to_matrix().to_4x4()
            mat.translation = origin
            imat = mat.inverted()
            v = imat * vec
        else:
            v = vec.copy()

        view = self.view_axis(context)
        if view in {'x', '-x'}:
            axes = [1, 2]
        elif view in {'y', '-y'}:
            axes = [0, 2]
        elif view in {'z', '-z'}:
            axes = [0, 1]
        else:
            axes = [0, 1, 2]
        for i in axes:
            v[i] = bupg * math.floor(0.5 + v[i] / bupg)

        if localgrid:
            v = mat * v

        return v

    def cursor3d(self, context, event):
        U = context.user_preferences
        use_depth = U.view.use_mouse_depth_cursor
        scene = context.scene
        v3d = context.space_data
        region = context.region
        rv3d = context.region_data

        if self.use_snap and self.use_depth:
            # snap
            U.view.use_mouse_depth_cursor = False
            self.call_builtin_cursor3d(context, event)
            U.view.use_mouse_depth_cursor = use_depth

            cur = v3d.cursor_location
            cur = self.snap_grid(context, cur, self.use_precision)
            v3d.cursor_location = cur

            # depth
            cur_2d_near = project(region, rv3d, cur)
            cur_2d_near[2] = 0.001
            cur_2d_far = cur_2d_near.copy()
            cur_2d_far[2] = 1.0
            v1 = unproject(region, rv3d, cur_2d_near)
            v2 = unproject(region, rv3d, cur_2d_far)
            ray = v2 - v1

            result, location, normal, index, obj, matrix = scene.ray_cast(
                v1, ray)
            if result:
                location = (location - cur).project(ray) + cur
                v3d.cursor_location = location

        else:
            U.view.use_mouse_depth_cursor = self.use_depth
            self.call_builtin_cursor3d(context, event)
            U.view.use_mouse_depth_cursor = use_depth

            if self.use_snap:
                cur = v3d.cursor_location
                cur = self.snap_grid(context, cur, self.use_precision)
                v3d.cursor_location = cur

        self.cursor_location = v3d.cursor_location

    def action_select_mouse(self, context):
        U = context.user_preferences
        if U.inputs.select_mouse == 'RIGHT':
            return 'LEFTMOUSE', 'RIGHTMOUSE'
        else:
            return 'RIGHTMOUSE', 'LEFTMOUSE'

    def event_status_update(self, event):
        if not hasattr(self, 'event_status'):
            self.event_status = set()
        if event.value == 'PRESS':
            self.event_status.add(event.type)
        elif event.value == 'RELEASE':
            self.event_status.discard(event.type)

    def exit(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(
            self.handler, 'WINDOW')
        context.area.header_text_set()
        context.area.tag_redraw()

    def header_text(self, context, event):
        snap = 'ON' if self.use_snap else 'OFF'
        precision = 'ON' if self.use_precision else 'OFF'
        depth = 'ON' if self.use_depth else 'OFF'
        text = 'Snap: {}(Ctrl), Precision: {}(Shift), Depth: {}(Alt)'
        text += ', Snap Selected: (S), Snap Active: (A)'
        if context.mode in {'OBJECT', 'EDIT_MESH'}:
            text += ', Snap Circle: (C)'
        text = text.format(snap, precision, depth)
        return text

    def modal(self, context, event):
        """
        :type context: bpy.types.Context
        :type event: bpy.types.Event
        :rtype: set
        """
        self.event_status_update(event)
        action_mouse, select_mouse = self.action_select_mouse(context)
        self.mco = event.mouse_region_x, event.mouse_region_y

        if event.type == 'INBETWEEN_MOUSEMOVE':
            return {'RUNNING_MODAL'}

        if event.type == self.event_type and event.value == 'RELEASE':
            if self.mco != self.mco_prev:
                context.space_data.cursor_location = self.cursor_location_bak
                self.cursor3d(context, event)
            self.exit(context)
            return {'FINISHED'}

        if event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'SPACE', 'RET',
                          'NUMPAD_ENTER', 'ESC'}:
            if event.value == 'PRESS':
                self.exit(context)
                return {'FINISHED'}

        if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT'}:
            if event.value == 'PRESS':
                self.shift = True
            elif event.value == 'RELEASE':
                self.shift = False
        if event.type in {'LEFT_CTRL', 'RIGHT_CTRL'}:
            if event.value == 'PRESS':
                self.ctrl = True
            elif event.value == 'RELEASE':
                self.ctrl = False
        if event.type in {'LEFT_ALT', 'RIGHT_ALT'}:
            if event.value == 'PRESS':
                self.alt = True
            elif event.value == 'RELEASE':
                self.alt = False

        # if event.type == 'D' and event.value == 'PRESS':
        #     self.use_depth ^= True

        self.use_depth = self.alt ^ self._use_depth
        self.use_snap = self.ctrl ^ self._use_snap
        self.use_precision = self.shift ^ self._use_precision

        update_cursor = False
        if (event.type == 'MOUSEMOVE' and
                (action_mouse in self.event_status or
                 self.event_type in self.event_status)):
            update_cursor = True
        elif (event.type == action_mouse and event.value == 'PRESS' or
              event.type == self.event_type and event.value == 'PRESS'):
            update_cursor = True
        elif event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT',
                            'LEFT_CTRL', 'RIGHT_CTRL',
                            'LEFT_ALT', 'RIGHT_ALT'}:
            update_cursor = True
        if update_cursor:
            context.space_data.cursor_location = self.cursor_location_bak
            self.cursor3d(context, event)
        elif event.value == 'PRESS':
            if event.type == 'A':
                bpy.ops.view3d.snap_cursor_to_active()
                self.exit(context)
                return {'FINISHED'}
            elif event.type == 'S':
                bpy.ops.view3d.snap_cursor_to_selected()
                self.exit(context)
                return {'FINISHED'}
            elif event.type == 'C':
                if context.mode in {'OBJECT', 'EDIT_MESH'}:
                    self.snap_to_circle(context)
                    self.exit(context)
                    return {'FINISHED'}

        self.mco_prev = self.mco

        context.area.header_text_set(self.header_text(context, event))

        context.area.tag_redraw()  # self.cursor3d()の呼び出しがあるから不要か？

        return {'RUNNING_MODAL'}

    def draw_callback(self, context):

        if context.region.as_pointer() != self.region:
            return
        glsettings = vagl.GLSettings(context)

        glsettings.push()

        cursor_2d = project(context.region, context.region_data,
                            context.space_data.cursor_location)

        unit_settings = context.scene.unit_settings
        text_lines = []
        for i in range(3):
            if unit_settings.system == 'NONE':
                text = '{:.5f}'.format(self.cursor_location[i])
            else:
                text = bpy.utils.units.to_string(
                    unit_settings.system,
                    'LENGTH',
                    self.cursor_location[i],
                    5,
                    split_unit=unit_settings.use_separate
                )
            text_lines.append(text)

        col = context.user_preferences.themes['Default'].view_3d.space.text_hi
        bgl.glColor3f(*col)
        blf.size(0, 12, context.user_preferences.system.dpi)
        tw_max = max(blf.dimensions(0, t)[0] for t in text_lines)
        if 0:
            p = [cursor_2d[0] - tw_max - 5, cursor_2d[1] - 40, 0]
        else:
            p = [self.mco[0] - tw_max - 5, self.mco[1] - 40, 0]
        th = blf.dimensions(0, '-.0123456789')[1]
        lf = th * 1.2
        for i, text in enumerate(text_lines):
            tw, _ = blf.dimensions(0, text)
            blf.position(0, p[0] + tw_max - tw, p[1], p[2])
            vagl.blf_draw(0, text)
            p[1] -= lf

        if 0:
            p = [cursor_2d[0] + 5, cursor_2d[1] - 40, 0]
        else:
            p = [self.mco[0] + 5, self.mco[1] - 40, 0]
        if self.use_snap:
            blf.position(0, *p)
            vagl.blf_draw(0, 'Snap')
        p[1] -= lf
        if self.use_precision:
            blf.position(0, *p)
            vagl.blf_draw(0, 'Precision')
        p[1] -= lf
        if self.use_depth:
            blf.position(0, *p)
            vagl.blf_draw(0, 'Depth')
        p[1] -= lf

        glsettings.pop()

    def invoke(self, context, event):
        """
        :type context: bpy.types.Context
        :type event: bpy.types.Event
        :rtype: set
        """
        U = context.user_preferences
        v3d = context.space_data

        self.mco = event.mouse_region_x, event.mouse_region_y
        self.mco_prev = self.mco
        self.cursor_location = context.space_data.cursor_location.copy()
        self.cursor_location_bak = self.cursor_location.copy()

        if not self.properties.is_property_set('use_depth'):
            self.use_depth = U.view.use_mouse_depth_cursor
        if not self.properties.is_property_set('use_snap'):
            self.use_snap = v3d.snap_cursor_to_grid
        self._use_depth = self.use_depth
        self._use_snap = self.use_snap
        self._use_precision = self.use_precision
        self.shift = False
        self.ctrl = False
        self.alt = False
        self.event_type = event.type
        self.event_status_update(event)

        self.cursor3d(context, event)

        if self.use_modal or event.alt:
            context.window_manager.modal_handler_add(self)
            context.area.header_text_set(self.header_text(context, event))
            self.handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
            self.region = context.region.as_pointer()
            return {'RUNNING_MODAL'}
        else:
            return {'FINISHED'}


CustomProperty = customproperty.CustomProperty.derive()


draw_func_bak = None


def panel_draw_set():
    global draw_func_bak

    def draw(self, context):
        layout = self.layout
        view = context.space_data

        custom_prop = CustomProperty.active()
        attrs = custom_prop.ensure(view, 'lock_cursor_location',
                                   'snap_cursor_to_grid')
        row = layout.row()
        sp = row.split()
        attr = attrs['lock_cursor_location']
        sub = sp.row()
        sub.prop(custom_prop, attr, text='Lock')
        sub = sp.row()
        sub.active = not view.lock_cursor_location
        attr = attrs['snap_cursor_to_grid']
        sub.prop(custom_prop, attr, text='Snap')

        col = layout.column()
        col.active = not view.lock_cursor_location
        col.prop(view, 'cursor_location', text='Location')

    draw_func_bak = None

    cls = bpy.types.VIEW3D_PT_view3d_cursor
    if hasattr(cls.draw, '_draw_funcs'):
        # bpy_types.py: _GenericUI._dyn_ui_initialize
        for i, func in enumerate(cls.draw._draw_funcs):
            if func.__module__ == cls.__module__:
                cls.draw._draw_funcs[i] = draw
                draw_func_bak = func
                break
    else:
        draw_func_bak = cls.draw
        cls.draw = draw


def panel_draw_restore():
    cls = bpy.types.VIEW3D_PT_view3d_cursor
    if hasattr(cls.draw, '_draw_funcs'):
        if draw_func_bak:
            for i, func in enumerate(cls.draw._draw_funcs):
                if func.__module__ == __name__:
                    cls.draw._draw_funcs[i] = draw_func_bak
    else:
        cls.draw = draw_func_bak


classes = [
    LockCursorPreferences,
    VIEW3D_OT_cursor3d,
    CustomProperty,
]


@LockCursorPreferences.register_addon
def register():
    # オリジナルのwmOperatorTypeを確保しておく
    pyop = bpy.ops.view3d.cursor3d
    opinst = pyop.get_instance()
    pyrna = structures.BPy_StructRNA.cast(id(opinst))
    op = structures.wmOperator.cast(pyrna.ptr.data)
    VIEW3D_OT_cursor3d.operator_type = op.type.contents

    for cls in classes:
        bpy.utils.register_class(cls)

    CustomProperty.utils.register_space_property(
        bpy.types.SpaceView3D, 'lock_cursor_location',
        bpy.props.BoolProperty(
            name='Lock Cursor Location',
            description='3D Cursor location is locked to prevent it from '
                        'being accidentally moved')
    )
    CustomProperty.utils.register_space_property(
        bpy.types.SpaceView3D, 'snap_cursor_to_grid',
        bpy.props.BoolProperty(
            name='Cursor to Grid',
            description='Snap cursor to nearest grid division')
    )

    panel_draw_set()

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = LockCursorPreferences.get_keymap('3D View')
        kmi = km.keymap_items.new('view3d.cursor3d', 'ACTIONMOUSE', 'PRESS',
                                  alt=True)
        kmi.properties.use_modal = True


@LockCursorPreferences.unregister_addon
def unregister():
    panel_draw_restore()

    CustomProperty.utils.unregister_space_property(
        bpy.types.SpaceView3D, 'lock_cursor_location',
    )
    CustomProperty.utils.unregister_space_property(
        bpy.types.SpaceView3D, 'snap_cursor_to_grid',
    )

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
