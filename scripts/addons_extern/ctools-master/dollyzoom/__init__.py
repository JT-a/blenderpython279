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
    'name': 'Dolly Zoom',
    'author': 'chromoly',
    'version': (0, 1, 2),
    'blender': (2, 78, 0),
    'location': '3DView > UI > Dolly Zoom, 3DView > Ctrl + Shift + F',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View',
}


import ctypes as ct
import importlib
import math

import bpy
from mathutils import Matrix, Vector

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(st)
    importlib.reload(vaprops)
    importlib.reload(wrapoperator)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import structures as st
    from ..utils import vaprops
    from ..utils import wrapoperator


PROP_MODE_ATTR = 'ct_dz_mode'
PROP_LENS_ATTR = 'ct_dz_camera_lens'
PROP_ANGLE_ATTR = 'ct_dz_camera_angle'
PROP_ADJUST_ATTR = 'ct_dz_dof_adjust'
PROP_V3D_LENS_ATTR = 'ct_dz_v3d_lens'
PROP_USE_VIEW_LOCATION = 'ct_dz_use_view_location'


###############################################################################
# Addon Preferences
###############################################################################
class WM_OT_event_type_search_popup2(bpy.types.Operator):
    # emulatekeymapのと名前が被るのを避ける
    bl_idname = 'wm.event_type_search_popup2'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_property = 'type'

    _prop = bpy.types.KeyMapItem.bl_rna.properties['type']
    _items = [(e.identifier, e.identifier + '    ' + e.name, e.description,
               e.value)
              for e in _prop.enum_items]
    type = bpy.props.EnumProperty(
        items=_items,
        name='Type',
        default='NONE',
    )
    del _prop, _items

    data_path = bpy.props.StringProperty(options={'SKIP_SAVE'})

    def execute(self, context):
        setattr(self.__class__.target, self.__class__.attribute, self.type)
        for area in context.screen.areas:
            area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        # UILayout.context_pointer_set()はinvokeの時は有効でもexecuteの時は
        # 無効になっていたのでその対策
        ls = self.data_path.split('.')
        self.__class__.target = eval('context.' + '.'.join(ls[:-1]))
        self.__class__.attribute = ls[-1]

        context.window_manager.invoke_search_popup(self)
        return {'INTERFACE'}


class AddonDollyZoomPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    walk_key = bpy.props.StringProperty(
        name='Walk Navigation Key',
        default='T'
    )
    fly_key = bpy.props.StringProperty(
        name='Fly Navigation Key',
        default='T',
    )

    def draw(self, context):
        layout = self.layout
        layout.context_pointer_set('addon_prefs', self)

        sp = layout.split()
        column = sp.column()

        row = column.row(align=True)
        row.prop(self, 'walk_key', text='Walk Key')
        op = row.operator(WM_OT_event_type_search_popup2.bl_idname, text='',
                          icon='VIEWZOOM')
        op.data_path = 'addon_prefs.walk_key'

        row = column.row(align=True)
        row.prop(self, 'fly_key', text='Fly Key')
        op = row.operator(WM_OT_event_type_search_popup2.bl_idname, text='',
                          icon='VIEWZOOM')
        op.data_path = 'addon_prefs.fly_key'

        column = sp.column()

        layout.separator()

        super().draw(context)


###############################################################################
# Operator
###############################################################################

def BKE_camera_sensor_size(camera):
    if camera.sensor_fit == 'VERTICAL':
        return camera.sensor_height
    return camera.sensor_width


def focallength_to_fov(focal_length, sensor):
    """lens > angle"""
    return 2.0 * math.atan((sensor / 2.0) / focal_length)


def fov_to_focallength(hfov, sensor):
    """angle > lens"""
    return (sensor / 2.0) / math.tan(hfov * 0.5)


# BKE_camera_view_frame_ex()

# DNA_camera_types.h
CAMERA_SENSOR_FIT_AUTO = 0
DEFAULT_SENSOR_WIDTH = 32.0
DEFAULT_SENSOR_HEIGHT = 18.0


class CameraParams:
    def __init__(self, ob=None):
        """BKE_camera_params_init()参照"""
        # lens
        self.is_ortho = False
        self.lens = 0.0
        self.ortho_scale = 0.0

        self.shiftx = self.shifty = self.offsetx = self.offsety = 0.0

        # sensor
        self.sensor_x = 0.0
        self.sensor_y = 0.0
        self.sensor_fit = 0

        # clipping
        self.clipsta = 0.0
        self.clipend = 0.0

        # fields
        self.use_fields = 0
        self.field_second = 0
        self.field_odd = 0

        # computed viewplane
        self.ycor = 0.0
        self.viewdx = 0.0
        self.viewdy = 0.0
        self.viewplane = [0.0] * 4

        # computed matrix
        self.winmat = Matrix.Identity(4)

        self.params_init()

        # CAMERA用
        self.YF_dofdist = 0.0  # dof_distance
        self.dof_ob = None  # dof_object

        if ob:
            self.from_object(ob)

    def params_init(self):
        self.sensor_x = DEFAULT_SENSOR_WIDTH
        self.sensor_y = DEFAULT_SENSOR_HEIGHT
        self.sensor_fit = CAMERA_SENSOR_FIT_AUTO
        self.zoom = 1.0
        self.clipsta = 0.1
        self.clipend = 100.0

    def from_object(self, ob):
        """BKE_camera_params_from_object()参照"""
        if not ob:
            return

        if ob.type == 'CAMERA':
            camera = ob.data
            """:type: bpy.types.Camera"""

            if camera.type == 'ORTHO':
                self.is_ortho = True
            self.lens = camera.lens
            self.ortho_scale = camera.ortho_scale

            self.shiftx = camera.shift_x
            self.shifty = camera.shift_y

            self.sensor_x = camera.sensor_width
            self.sensor_y = camera.sensor_height
            self.sensor_fit = camera.sensor_fit
            self.clipsta = camera.clip_start
            self.clipend = camera.clip_end

            self.YF_dofdist = camera.dof_distance
            self.dof_ob = camera.dof_object

        elif ob.type == 'LAMP':
            lamp = ob.data
            """:type: bpy.types.Lamp"""
            if lamp.type == 'SPOT':
                fac = math.cos(lamp.spot_size * 0.5)
                phi = math.acos(fac)
                self.lens = 16.0 * fac / math.sin(phi)
            else:
                self.lens = 0.0
            if self.lens == 0.0:
                self.lens = 35.0

            if lamp.type != 'HEMI':
                self.clipsta = lamp.shadow_buffer_clip_start
                self.clipend = lamp.shadow_buffer_clip_end

        else:
            self.lens = 35.0

        # ED_view3d_viewplane_get
            # BKE_camera_params_from_view3d
            # BKE_camera_params_compute_viewplane


###############################################################################
# Walk Navigation EX
###############################################################################
class WalkInfo(st.Cast, ct.Structure):
    """view3d_walk.c"""
    _fields_ = st.fields(
        ct.c_void_p, 'rv3d',
        ct.c_void_p, 'v3d',
        ct.c_void_p, 'ar',
        ct.c_void_p, 'scene',
        ct.c_void_p, 'timer',
    )

try:
    _ = walk_ot_attrs
except NameError:
    walk_ot_attrs = wrapoperator.convert_operator_attributes('view3d.walk')
_VIEW3D_OT_walk_ex = type('_VIEW3D_OT_walk_ex', (), walk_ot_attrs)


def distance_from_camera(camera_obj, loc):
    mat = camera_obj.matrix_world
    ray = -mat.col[2].to_3d().normalized()
    v = (loc - mat.to_translation()).project(ray)
    dist = v.length
    if ray.dot(v) < 0.0:
        dist *= -1
    return dist


def distance_from_view(rv3d, loc):
    mat = rv3d.view_matrix.inverted()
    ray = -mat.col[2].to_3d().normalized()
    v = (loc - mat.to_translation()).project(ray)
    dist = v.length
    if ray.dot(v) < 0.0:
        dist *= -1
    return dist


def camera_dof_distance(camera_obj):
    if not camera_obj or camera_obj.type != 'CAMERA':
        raise ValueError()

    camera = camera_obj.data
    if camera.dof_object:
        tar_loc = camera.dof_object.matrix_world.to_translation()
        return distance_from_camera(camera_obj, tar_loc)
    else:
        return camera.dof_distance


def camera_cursor_distance(scene, area, camera_obj):
    if area and area.type == 'VIEW_3D':
        cursor = area.spaces.active.cursor_location
    else:
        cursor = scene.cursor_location
    return distance_from_camera(camera_obj, cursor)


def camera_screen_size(scene, area, camera_obj, use_dof=False):
    if not camera_obj or use_dof and camera_obj.type != 'CAMERA':
        raise ValueError()

    camera = camera_obj.data
    if use_dof:
        dist = camera_dof_distance(camera_obj)
    else:
        dist = camera_cursor_distance(scene, area, camera_obj)
    if dist > 0.0:
        return dist * math.tan(camera.angle / 2) * 2
    else:
        return 0.0


def rv3d_screen_size(v3d, rv3d):
    dist = distance_from_view(rv3d, v3d.cursor_location)
    if dist > 0.0:
        # sensorはDEFAULT_SENSOR_WIDTHで合ってるのか？
        angle = focallength_to_fov(v3d.lens, DEFAULT_SENSOR_WIDTH)
        return dist * math.tan(angle / 2) * 2
    else:
        return 0.0


class _Navigate:
    bl_idname = ''
    bl_label = ''

    def __init__(self):
        self.dolly_zoom = False
        self.camera_lens_bak = 35.0
        self.screen_size = 0.0  # dolly_zoom有効時に計算
        self.rv3d_view_distance_bak = self.rv3d_view_distance = 0.0
        self.v3d_lens_bak = self.v3d_lens = 35.0  # degrees
        self.rv3d_view_location = Vector()
        # self.projected_view_location = Vector([0.0, 0.0, 0.0, 1.0])

    def cancel(self, context):
        super().cancel(context)

    def header_text_set(self, context):
        addon_prefs = AddonDollyZoomPreferences.get_instance()
        if self.__class__.bl_idname == 'view3d.walk_ex':
            event_type = addon_prefs.walk_key
        else:
            event_type = addon_prefs.fly_key

        for region in context.area.regions:
            if region.type == 'HEADER':
                break
        else:
            return
        ar = st.ARegion.cast(region)
        if ar.headerstr:
            try:
                s = ar.headerstr.decode('utf-8')
            except:
                return
            if not s.endswith('decrease speed'):
                s = ','.join(s.split(',')[:-1])
            value = 'ON' if self.dolly_zoom else 'OFF'
            s += ', {}:lens ({})'.format(event_type, value)
            context.area.header_text_set(s)

    def calc_screen_size(self, context):
        self.screen_size = 0.0
        rv3d = context.region_data
        if rv3d.view_perspective == 'CAMERA':
            camera_obj = context.scene.camera
            if camera_obj and camera_obj.type == 'CAMERA':
                self.screen_size = camera_screen_size(
                    context.scene, context.area, camera_obj)
        else:
            self.screen_size = rv3d_screen_size(context.space_data, rv3d)

    def modal(self, context, event):
        addon_prefs = AddonDollyZoomPreferences.get_instance()
        v3d = context.space_data
        rv3d = context.region_data

        if self.__class__.bl_idname == 'view3d.walk_ex':
            event_type = addon_prefs.walk_key
        else:
            event_type = addon_prefs.fly_key

        if event.type == event_type and event.value == 'PRESS':
            self.dolly_zoom ^= True
            if self.dolly_zoom:
                self.rv3d_view_location = rv3d.view_location.copy()
                self.v3d_lens = v3d.lens
                self.calc_screen_size(context)

        r = super().modal(context, event)

        ev = st.wmEvent.cast(event)
        op = st.wmOperator.cast(self.as_pointer())
        if self.__class__.bl_idname == 'view3d.walk_ex':
            walk_fly = WalkInfo.cast(op.customdata)
        else:
            walk_fly = FlyInfo.cast(op.customdata)

        camera_obj = camera = None
        if rv3d.view_perspective == 'CAMERA':
            camera_obj = context.scene.camera
            if camera_obj and camera_obj.type == 'CAMERA':
                camera = camera_obj.data

        if (event.type == 'TIMER' and ev.customdata == walk_fly.timer and
                self.dolly_zoom):
            cursor = context.space_data.cursor_location
            if rv3d.view_perspective == 'CAMERA':
                if camera:
                    mat = camera_obj.matrix_world
                    ray = -mat.col[2].to_3d().normalized()
                    loc = mat.col[3].to_3d()
                    v = cursor - loc
                    dist = v.project(ray).length
                    if v.dot(ray) < 0:
                        dist *= -1

                    if self.screen_size > 0.0 and dist > 0.0:
                        f = math.atan(self.screen_size / 2 / dist)
                        angle = f * 2
                        size = BKE_camera_sensor_size(camera)
                        lens = fov_to_focallength(angle, size)
                        camera.lens = max(1.0, lens)
                    else:
                        camera.lens = self.camera_lens_bak
                    # TODO: dof_distanceの扱い
            else:
                mat = rv3d.view_matrix.inverted()
                ray = -mat.col[2].to_3d().normalized()
                loc = mat.to_translation()
                v = cursor - loc
                dist = v.project(ray).length
                if v.dot(ray) < 0:
                    dist *= -1

                if self.screen_size > 0.0 and dist > 0.0:
                    f = math.atan(self.screen_size / 2 / dist)
                    angle = f * 2
                    lens = fov_to_focallength(angle, DEFAULT_SENSOR_WIDTH)
                    v3d.lens = min(max(1.0, lens), 250.0)
                else:
                    v3d.lens = self.v3d_lens_bak
                rv3d.update()  # recalc matrices

        if 'CANCELLED' in r:
            if camera:
                camera.lens = self.camera_lens_bak
            v3d.lens = self.v3d_lens_bak
            rv3d.view_distance = self.rv3d_view_distance_bak

        self.header_text_set(context)
        return r

    def invoke(self, context, event):
        # registerの時にはまだmodalkeymapが設定されていない
        # このオペレーターの場合、設定しないとキー入力とヘッダの描画に
        # 問題が起こる
        if self.__class__.bl_idname == 'view3d.walk_ex':
            ot = wrapoperator.get_operator_type('view3d.walk')
        else:
            ot = wrapoperator.get_operator_type('view3d.fly')
        ex_ot = wrapoperator.get_operator_type(self.__class__.bl_idname)
        ex_ot.modalkeymap = ot.modalkeymap

        v3d = context.space_data
        rv3d = context.region_data
        self.rv3d_view_distance_bak = rv3d.view_distance
        self.v3d_lens_bak = v3d.lens
        self.rv3d_view_location = rv3d.view_location.copy()
        self.rv3d_view_distance = rv3d.view_distance  # modal中では0.0になる
        self.v3d_lens = v3d.lens
        if rv3d.view_perspective == 'CAMERA':
            camera_obj = context.scene.camera
            if camera_obj and camera_obj.type == 'CAMERA':
                camera = camera_obj.data
                self.camera_lens_bak = camera.lens
        if self.dolly_zoom:
            self.calc_screen_size(context)

        return super().invoke(context, event)


class VIEW3D_OT_walk_ex(_Navigate, _VIEW3D_OT_walk_ex, bpy.types.Operator):
    bl_idname = 'view3d.walk_ex'
    bl_label = 'Walk Navigation EX'


###############################################################################
# Fly Navigation EX
###############################################################################
class FlyInfo(st.Cast, ct.Structure):
    """view3d_fly.c"""
    _fields_ = st.fields(
        ct.c_void_p, 'rv3d',
        ct.c_void_p, 'v3d',
        ct.c_void_p, 'ar',
        ct.c_void_p, 'scene',
        ct.c_void_p, 'timer',
    )

try:
    _ = fly_ot_attrs
except NameError:
    fly_ot_attrs = wrapoperator.convert_operator_attributes('view3d.fly')
_VIEW3D_OT_fly_ex = type('_VIEW3D_OT_fly_ex', (), fly_ot_attrs)


class VIEW3D_OT_fly_ex(_Navigate, _VIEW3D_OT_fly_ex, bpy.types.Operator):
    bl_idname = 'view3d.fly_ex'
    bl_label = 'Fly Navigation EX'


###############################################################################
# View Navigation EX
###############################################################################
try:
    _ = navigate_ot_attrs
except NameError:
    navigate_ot_attrs = wrapoperator.convert_operator_attributes(
        'view3d.navigate')
_VIEW3D_OT_navigate_ex = type('_VIEW3D_OT_navigate_ex', (),
                              navigate_ot_attrs)


class VIEW3D_OT_navigate_ex(_VIEW3D_OT_navigate_ex, bpy.types.Operator):
    bl_idname = 'view3d.navigate_ex'
    bl_label = 'View Navigation EX'

    def invoke(self, context, event):
        U = context.user_preferences
        if U.inputs.navigation_mode == 'FLY':
            bpy.ops.view3d.fly_ex('INVOKE_DEFAULT')
        else:
            bpy.ops.view3d.walk_ex('INVOKE_DEFAULT')
        return {'FINISHED'}


###############################################################################
# Camera Focus from 3D Cursor
###############################################################################
class CAMERA_OT_focus_from_cursor(bpy.types.Operator):
    bl_idname = 'camera.focus_from_cursor'
    bl_label = 'Camera Focus from 3D Cursor'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        ob = context.scene.camera
        return ob and ob.type == 'CAMERA'

    def execute(self, context):
        scene = context.scene
        area = context.area
        ob = scene.camera
        if ob and ob.type == 'CAMERA':
            if area and area.type == 'VIEW_3D':
                cursor = area.spaces.active.cursor_location
            else:
                cursor = scene.cursor_location
            ob.data.dof_distance = max(0.0, distance_from_camera(ob, cursor))
            return {'FINISHED'}
        return {'CANCELLED'}


###############################################################################
# Panel
###############################################################################
class VIEW3D_PT_dolly_zoom(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_dolly_zoom'
    bl_label = 'Dolly Zoom'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        """:type: bpy.types.UILayout"""
        scene = context.scene

        v3d = context.space_data
        if v3d.region_quadviews:
            rv3d = v3d.region_quadviews[-1]
        else:
            rv3d = v3d.region_3d

        is_camera = rv3d.view_perspective == 'CAMERA'

        row = layout.row()
        row.prop(scene, PROP_MODE_ATTR, expand=True)
        row.active = not is_camera

        column = layout.column()
        if getattr(scene, PROP_MODE_ATTR) == 'CAMERA' or is_camera:
            col = column.column()
            is_camera = scene.camera and scene.camera.type == 'CAMERA'
            col.enabled = is_camera
            if (scene.camera and scene.camera.type == 'CAMERA' and
                    scene.camera.data.lens_unit == 'FOV'):
                col.prop(scene, PROP_ANGLE_ATTR)
            else:
                col.prop(scene, PROP_LENS_ATTR)
            col = column.column()
            col.active = is_camera
            col.prop(scene, PROP_ADJUST_ATTR)
            col.operator(CAMERA_OT_focus_from_cursor.bl_idname,
                         text='Set Focus from 3D Cursor')
        else:
            col = column.column()
            # col.active = rv3d.view_perspective == 'PERSP'
            col.prop(scene, PROP_V3D_LENS_ATTR)
            col.prop(scene, PROP_USE_VIEW_LOCATION)

    @classmethod
    def world_to_basis(cls, obj, loc):
        if obj.parent:
            v = obj.parent.matrix_world.inverted() * loc
            obj.location = obj.matrix_basis * obj.matrix_local.inverted() * v
        else:
            obj.location = loc

    @classmethod
    def set_params_v3d(cls, context, lens):
        v3d = context.area.spaces.active

        if v3d.region_quadviews:
            rv3ds = v3d.region_quadviews
        else:
            rv3ds = [v3d.region_3d]
        for rv3d in rv3ds:
            if (rv3d.view_perspective == 'ORTHO' or
                    getattr(context.scene, PROP_USE_VIEW_LOCATION)):
                rv3d.view_distance *= lens / v3d.lens
            else:
                dist = distance_from_view(rv3d, v3d.cursor_location)
                if rv3d.view_distance != 0.0 and dist > 0.0:
                    rv3d.view_distance += dist * lens / v3d.lens - dist
        v3d.lens = lens
        for rv3d in rv3ds:
            rv3d.update()  # recalc matrices

    @classmethod
    def set_params(cls, context, lens=None, angle=None, use_dof=False):
        scene = context.scene
        camera_obj = scene.camera
        if not camera_obj or camera_obj.type != 'CAMERA':
            return

        camera = scene.camera.data
        sensor = BKE_camera_sensor_size(camera)

        if lens is not None:
            lens = max(1.0, lens)
            angle = focallength_to_fov(lens, sensor)
        elif angle is not None:
            angle = min(max(0.0, angle), math.pi)
            lens = fov_to_focallength(angle, sensor)
            lens = max(1.0, lens)
            angle = focallength_to_fov(lens, sensor)

        prev_angle = camera.angle
        camera.lens = lens

        if use_dof:
            distance = camera_dof_distance(camera_obj)
        else:
            distance = camera_cursor_distance(scene, context.area, camera_obj)

        if distance <= 0.0:
            return

        screen_size = distance * math.tan(prev_angle / 2) * 2
        dist = screen_size / (math.tan(angle / 2) * 2)
        mat = camera_obj.matrix_world
        ray = -mat.col[2].to_3d().normalized()
        loc_world = mat.to_translation() + ray * (distance - dist)

        if camera_obj.parent:
            v = camera_obj.parent.matrix_world.inverted() * loc_world
            camera_obj.location = (camera_obj.matrix_basis *
                                   camera_obj.matrix_local.inverted() * v)
        else:
            camera_obj.location = loc_world

        if getattr(scene, PROP_ADJUST_ATTR):
            d = camera.dof_distance + dist - distance
            camera.dof_distance = max(0.0, d)

    @classmethod
    def register(cls):
        def redraw_v3d_ui(self, context):
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'UI':
                            region.tag_redraw()

        def redraw_v3d(self, context):
            context.area.tag_redraw()

        # camera lens -----------------------------------------------
        prop = vaprops.bl_prop_to_py_prop(
            bpy.types.Camera.bl_rna.properties['lens'])

        def fget(self):
            scene = self
            if scene.camera and scene.camera.type == 'CAMERA':
                camera = scene.camera.data
                return camera.lens
            else:
                return 35.0

        def fset(self, value):
            scene = self
            if scene.camera and scene.camera.type == 'CAMERA':
                VIEW3D_PT_dolly_zoom.set_params(bpy.context, lens=value)

        prop[1]['get'] = fget
        prop[1]['set'] = fset
        prop[1]['update'] = redraw_v3d
        setattr(bpy.types.Scene, PROP_LENS_ATTR, prop)

        # camera angle ----------------------------------------------
        prop = vaprops.bl_prop_to_py_prop(
            bpy.types.Camera.bl_rna.properties['angle'])

        def fget(self):
            scene = self
            if scene.camera and scene.camera.type == 'CAMERA':
                camera = scene.camera.data
                return camera.angle
            else:
                return focallength_to_fov(35.0, DEFAULT_SENSOR_WIDTH)

        def fset(self, value):
            scene = self
            if scene.camera and scene.camera.type == 'CAMERA':
                VIEW3D_PT_dolly_zoom.set_params(bpy.context, angle=value)

        prop[1]['get'] = fget
        prop[1]['set'] = fset
        prop[1]['update'] = redraw_v3d
        setattr(bpy.types.Scene, PROP_ANGLE_ATTR, prop)

        # adjust dof distance ---------------------------------------
        def fget(self):
            return getattr(VIEW3D_PT_dolly_zoom, PROP_ADJUST_ATTR, False)

        def fset(self, value):
            return setattr(VIEW3D_PT_dolly_zoom, PROP_ADJUST_ATTR, value)

        prop = bpy.props.BoolProperty(
            name='Adjust DOF Distance',
            get=fget,  # Sceneにゴミを追加しないようにget,set関数を設定する
            set=fset,
            update=redraw_v3d_ui,
        )
        setattr(bpy.types.Scene, PROP_ADJUST_ATTR, prop)

        # v3d lens --------------------------------------------------
        prop = vaprops.bl_prop_to_py_prop(
            bpy.types.SpaceView3D.bl_rna.properties['lens'])

        def fget(self):
            area = bpy.context.area
            if area and area.type == 'VIEW_3D':
                return area.spaces.active.lens
            else:
                return 35.0

        def fset(self, value):
            area = bpy.context.area
            if area and area.type == 'VIEW_3D':
                VIEW3D_PT_dolly_zoom.set_params_v3d(bpy.context, value)

        prop[1]['get'] = fget
        prop[1]['set'] = fset
        prop[1]['update'] = redraw_v3d
        setattr(bpy.types.Scene, PROP_V3D_LENS_ATTR, prop)

        # use view_location -----------------------------------------
        def fget(self):
            return getattr(VIEW3D_PT_dolly_zoom, PROP_USE_VIEW_LOCATION, False)

        def fset(self, value):
            return setattr(VIEW3D_PT_dolly_zoom, PROP_USE_VIEW_LOCATION, value)

        prop = bpy.props.BoolProperty(
            name='View Location',
            description='Use view location instead of 3D cursor',
            get=fget,
            set=fset,
            update=redraw_v3d_ui,
        )
        setattr(bpy.types.Scene, PROP_USE_VIEW_LOCATION, prop)

        # mode ------------------------------------------------------
        def fget(self):
            return getattr(VIEW3D_PT_dolly_zoom, PROP_MODE_ATTR, 0)

        def fset(self, value):
            return setattr(VIEW3D_PT_dolly_zoom, PROP_MODE_ATTR, value)

        prop = bpy.props.EnumProperty(
            name='Mode',
            items=[('VIEW_3D', '3D View', 'Depth: 3D cursor / view location'),
                   ('CAMERA', 'Camera', 'Depth: 3D cursor')
                   ],
            default='VIEW_3D',
            get=fget,
            set=fset,
            update=redraw_v3d_ui,
        )
        setattr(bpy.types.Scene, PROP_MODE_ATTR, prop)

    @classmethod
    def unregister(cls):
        delattr(bpy.types.Scene, PROP_LENS_ATTR)
        delattr(bpy.types.Scene, PROP_ANGLE_ATTR)
        delattr(bpy.types.Scene, PROP_ADJUST_ATTR)


###############################################################################
# Register
###############################################################################
classes = [
    AddonDollyZoomPreferences,
    WM_OT_event_type_search_popup2,
    VIEW3D_OT_walk_ex,
    VIEW3D_OT_fly_ex,
    VIEW3D_OT_navigate_ex,
    CAMERA_OT_focus_from_cursor,
    VIEW3D_PT_dolly_zoom,
]


@AddonDollyZoomPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    km = AddonDollyZoomPreferences.get_keymap('3D View')
    if km:
        km.keymap_items.new(VIEW3D_OT_navigate_ex.bl_idname,
                            'F', 'PRESS', shift=True, ctrl=True)


@AddonDollyZoomPreferences.unregister_addon
def unregister():
    walk_ex_ot = wrapoperator.get_operator_type('view3d.walk_ex')
    walk_ex_ot.modalkeymap = None
    fly_ex_ot = wrapoperator.get_operator_type('view3d.fly_ex')
    fly_ex_ot.modalkeymap = None

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
