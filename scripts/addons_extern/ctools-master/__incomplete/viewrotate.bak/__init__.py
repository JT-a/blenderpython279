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
    'name': 'View Rotate Plus',
    'author': 'chromoly',
    'version': (0, 1),
    'blender': (2, 77, 0),
    'location': 'View3D',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View',
}


"""

"""


import importlib
import math

import bpy
from mathutils import Quaternion, Vector

try:
    importlib.reload(registerinfo)
    importlib.reload(utils)
except NameError:
    from . import registerinfo
    from . import utils


class ViewRotatePreferences(
        utils.AddonPreferences,
        registerinfo.AddonRegisterInfo,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    release_confirm = bpy.props.BoolProperty(
        name='Release Confirm')

    def draw(self, context):
        layout = self.layout
        split = layout.split()
        column = split.column()
        row = column.row()
        row.prop(self, 'release_confirm')
        column = split.column()
        column = split.column()

        super().draw(context, self.layout)


TRACKBALLSIZE = 1.1
M_SQRT1_2 = 0.70710678118654752440	# 1/sqrt(2)


def angle_wrap_rad(angle):
    def mod_inline(a, b):
        return a - (b * math.floor(a / b))

    return mod_inline(angle + math.pi, math.pi * 2) - math.pi


def calctrackballvec(region, mx, my):
    radius = TRACKBALLSIZE

    x = region.x + (region.width / 2) - mx
    x /= region.width / 4
    y = region.y + (region.height / 2) - my
    y /= region.height / 2

    d = math.sqrt(x ** 2 + y ** 2)
    if d < radius * M_SQRT1_2:
        z = math.sqrt(radius ** 2 - d ** 2)
    else:
        t = radius / M_SQRT1_2
        z = t ** 2 / d

    return Vector([x, y, -z])


def view3d_orbit_calc_center(context):
    return Vector()


class ViewOpsData:
    def __init__(self, context, event):
        U = context.user_preferences
        use_orbit_select = U.view.use_rotate_around_active
        use_orbit_zbuf = U.view.use_mouse_depth_navigate

        rv3d = context.region_dat
        # view_location, view_rotation をpythonで取得・代入する場合、
        # それぞれnegate(),invert()に当たる処理をされている
        self.viewquat = rv3d.view_rotation.inverted()
        self.oldquat = rv3d.view_rotation.inverted()
        self.origx = self.oldx = event.x
        self.origy = self.oldy = event.y

        self.use_dyn_ofs = False

        # (U.uiflag & USER_ORBIT_SELECTION) != 0,
        # (U.uiflag & USER_ZBUF_ORBIT) != 0);
        if use_orbit_select:
            self.use_dyn_ofs = True
            self.dyn_ofs = view3d_orbit_calc_center(context)
            self.dyn_ofs.negate()

        self.trackvec = calctrackballvec(context.region, event.x, event.y)

        self.reverse = 1.0
        if context.region_data.perspective_matrix.col[2][1] < 0.0:
            self.reverse = -1.0


class VIEW3D_OT_rotate_plus(bpy.types.Operator):
    bl_idname = 'view3d.rotate_plus'
    bl_label = 'Rotate View'
    bl_options = {'REGISTER'}

    axis_snap = bpy.props.BoolProperty(
        defalut=False,
        options={'SKIP_SAVE', 'HIDDEN'})

    def __init__(self):
        self.event_type = ''

    @classmethod
    def poll(cls, context):
        area = context.area
        return area and area.type == 'VIEW_3D'

    def modal_keymap_item(self, context, event):
        wm = context.window_manager
        km = wm.keyconfigs.default.keymaps['View3D Rotate Modal'].active()
        for kmi in km.keymap_items:
            if not kmi.active:
                continue
            if kmi.type == event.type and kmi.value == event.value:
                if kmi.any:
                    return kmi
                else:
                    if all([(getattr(kmi, attr) == getattr(event, attr))
                            for attr in ['shift', 'ctrl', 'alt', 'oskey']]):
                        return kmi
        return None

    def viewrotate_apply_dyn_ofs(self, viewquat):
        pass

    def viewrotate_apply_snap(self, vod):
        pass

    def viewrotate_apply(self, context, event):
        # FIXME
        vod = self.vod
        x, y = event.x, event.y
        if context.user_preferences.inputs.view_rotate_method == 'TRACKBALL':
            newvec = calctrackballvec(context.region, event.x, event.y)
            dvec = newvec - vod.trackvec
            angle = (dvec.length / (2.0 * TRACKBALLSIZE)) * math.pi
            angle = angle_wrap_rad(angle)

            axis = vod.trackvec.cross(newvec)
            q1 = Quaternion(axis, angle)
            vod.viewquat = q1 * vod.oldquat

            self.viewrotate_apply_dyn_ofs(vod.viewquat)
        else:
            zvec_global = Vector([0, 0, 1])
            sensitivity = 0.007
            m = vod.viewquat.to_matrix()
            m_inv = m.inverted()

            if (zvec_global - m_inv.col[2]).length > 0.001:
                xaxis = zvec_global.closs(m_inv.col[0])
                if xaxis.dot(m_inv.col[0]) < 0:
                    xaxis.negate()
                fac = zvec_global.angle(m_inv.col[2]) / math.pi
                fac = abs(fac - 0.5) * 2
                fac *= fac
                xaxis = xaxis.lerp(m_inv.col[0], fac)
            else:
                xaxis = m_inv[0].copy()
            quat_local_x = Quaternion(xaxis, sensitivity * - (y - vod.oldy))
            quat_local_x = vod.viewquat * quat_local_x

            def axis_angle_to_quat_single(axis, angle):
                angle_half = angle * 0.5
                angle_cos = math.cos(angle_half)
                angle_sin = math.sin(angle_half)
                axis_index = ['X', 'Y', 'Z'].index(axis)
                q = Quaternion([angle_cos, 0, 0, 0])
                q[axis_index + 1] = angle_sin
                return q
            quat_global_z = axis_angle_to_quat_single(
                'Z', sensitivity * vod.reverse * (x - vod.oldx))
            vod.viewquat = quat_local_x * quat_global_z

            self.viewrotate_apply_dyn_ofs(vod.viewquat)

        vod.viewquat.normalize()
        context.region_data.view_rotation = vod.viewquat.inverted()
        if vod.axis_snap:
            self.viewrotate_apply_snap(vod)

        vod.oldx = x
        vod.oldy = y

        ED_view3d_camera_lock_sync(vod.v3d, context.region_data)

        context.region.tag_redraw()
        pass

    def modal(self, context, event):
        VIEW_PASS = 0
        VIEW_APPLY = 1
        VIEW_CONFIRM = 2
        use_autokey = False
        ret = {'RUNNING_MODAL'}
        event_code = VIEW_PASS

        wm = context.window_manager
        kmi = self.modal_keymap_item(context, event)

        if event.type == 'MOUSEMOVE':
            event_code = VIEW_APPLY

        elif kmi:
            value = kmi.propvalue
            if value == 'CONFIRM':
                event_code = VIEW_CONFIRM
            elif value == 'AXIS_SNAP_ENABLE':
                self.axis_snap = True
                event_code = VIEW_APPLY
            elif value == 'AXIS_SNAP_DISABLE':
                self.axis_snap = False
                event_code = VIEW_APPLY
            elif value == 'SWITCH_TO_ZOOM':
                bpy.ops.view3d.zoom('INVOKE_DEFAULT')
                event_code = VIEW_CONFIRM
            elif value == 'SWITCH_TO_MOVE':
                bpy.ops.view3d.move('INVOKE_DEFAULT')
                event_code = VIEW_CONFIRM

        elif event.type == self.event_type and event.value == 'RELEASE':
            event_code = VIEW_CONFIRM

        if event_code == VIEW_APPLY:
            self.viewrotate_apply(context, event)
            if context.screen.is_animation_playing:
                use_autokey = True
        elif event_code == VIEW_CONFIRM:
            # FIXME: ED_view3d_depth_tag_update
            use_autokey = True
            ret = {'FINISHED'}

        if use_autokey:
            pass

        return ret

    def view3d_ensure_persp(self, view3d, rv3d):

        return True

    def invoke(self, context, event):
        prefs = ViewRotatePreferences.get_instance()

        if self.view3d_ensure_persp(context.space_data, context.region_data):
            context.region.tag_redraw()

        self.event_type = event.type

        self.vod = ViewOpsData(context, event)

        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}


classes = [
    VIEW3D_OT_rotate_plus,
    ViewRotatePreferences,
]


@ViewRotatePreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = ViewRotatePreferences.get_keymap('3D View')
        kmi = km.keymap_items.new('view3d.rotate_plus', 'MIDDLEMOUSE', 'PRESS',
                                  head=True)


@ViewRotatePreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
