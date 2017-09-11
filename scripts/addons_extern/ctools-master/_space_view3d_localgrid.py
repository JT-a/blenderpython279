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
    'name': 'Local Grid',
    'author': 'chromoly',
    'version': (1, 1, 2),
    'blender': (2, 78, 0),
    'location': 'View3D',
    'category': '3D View'}


from collections import OrderedDict
import re

import bpy
from mathutils import Euler, Vector, Quaternion
import bmesh

from .utils import addongroup
from .utils import vaobject as vaob
from .utils import vaview3d as vav
from .utils import vaoperator as vaop
from .utils import vaarmature as vaarm


USE_OBB = True
USE_MANIPULATOR = True


if USE_MANIPULATOR:
    from .utils import manipulatormatrix
if USE_OBB:
    from .utils import convexhull


###############################################################################
# Property
###############################################################################
class LocalGridPreset(bpy.types.PropertyGroup):
    """メニューアイテムとして使用"""
    location = bpy.props.FloatVectorProperty(
        name='Location',
        default=(0, 0, 0),
        step=1,
        precision=3,
        subtype='XYZ',
        size=3)
    rotation = bpy.props.FloatVectorProperty(
        name='Rotation',
        default=(1, 0, 0, 0),
        step=1,
        precision=3,
        subtype='QUATERNION',
        size=4)
    delta_rotation_euler = bpy.props.FloatVectorProperty(
        name='Delta Rotation',
        default=(0, 0, 0),
        step=1,
        precision=3,
        subtype='EULER',
        size=3)

    class LocalGridPresetTemp:
        def __init__(self):
            self.name = ''
            self.location = Vector((0, 0, 0))
            self.rotation = Quaternion((1, 0, 0, 0))
            self.delta_rotation_euler = Euler((0, 0, 0))

    def copy(self):
        """仮のクラスを返す"""
        inst = LocalGridPreset.LocalGridPresetTemp()
        if self:
            inst.name = self.name
            inst.location = self.location.copy()
            inst.rotation = self.rotation.copy()
            inst.delta_rotation_euler = self.delta_rotation_euler.copy()
        return inst


class LocalGridData(bpy.types.PropertyGroup):
    """Scene.local_gridにメニューアイテムを確保"""
    presets = bpy.props.CollectionProperty(
        name='Presets',
        type=LocalGridPreset)


###############################################################################
# Main Operator
###############################################################################
def mat4_to_loc_quat(mat):
    loc = mat.to_translation()
    # @ math_matrix.c: mat4_to_loc_quat()
    # so scale doesn't interfere with rotation [#24291]
    # note: this is a workaround for negative matrix not working for
    # rotation conversion, FIXME
    if mat.is_negative:
        mat = mat.to_3x3()
        for i in range(3):
            for j in range(3):
                mat[i][j] *= -1
    quat = mat.to_quaternion()
    return loc, quat


def loc_quat_from_obb(context):
    if context.mode == 'OBJECT':
        obs = context.selected_objects
        coords = [ob.matrix_world.to_translation() for ob in obs]
    elif context.mode == 'EDIT_MESH':
        ob = context.active_object
        obmat = ob.matrix_world
        bm = bmesh.from_edit_mesh(ob.data)
        coords = [obmat * v.co for v in bm.verts if v.select]
    else:
        coords = []
    if not coords:
        return None, None
    elif len(coords) == 1:
        return coords[0], Quaternion((1, 0, 0, 0))
    else:
        mat, _scale = convexhull.OBB(coords)
        return mat4_to_loc_quat(mat)


def loc_quat_from_cursor_selection(context):
    """locationに3DCursor, rotationに二つの選択要素を用いる。
    rotationは選択要素がX軸になるように現在の視点をZ軸で回転する。
    """

    actob = context.active_object
    if actob:
        mat = actob.matrix_world
    else:
        mat = None

    coords = None
    if context.mode == 'OBJECT':
        if 1 <= len(context.selected_objects) <= 2:
            coords = [ob.matrix_world.to_translation()
                      for ob in context.selected_objects]
    elif context.mode == 'EDIT_MESH':
        bm = bmesh.from_edit_mesh(actob.data)
        verts = [v for v in bm.verts if v.select]
        if 1 <= len(verts) <= 2:
            coords = [mat * v.co for v in verts]
    elif context.mode in ('EDIT_ARMATURE', 'POSE'):
        bone_coords = []
        if context.mode == 'EDIT_ARMATURE':
            bones = actob.data.edit_bones
        else:
            bones = actob.pose.bones
        with vaarm.CustomProperty():
            for bone in bones:
                if bone.is_visible:
                    if bone.select_head:
                        parent = bone.parent
                        if not (parent and parent.is_visible and
                                parent.select_tail and bone.use_connect):
                            bone_coords.append(mat * bone.head)
                    if bone.select_tail:
                        bone_coords.append(mat * bone.tail)
            if 1 <= len(bone_coords) <= 2:
                coords = bone_coords

    loc = context.space_data.cursor_location.copy()
    rv3d = context.region_data
    if coords and len(coords) == 2:
        quat = rv3d.view_rotation.normalized()
        vmat = rv3d.view_matrix
        v1 = vmat * coords[0]
        v2 = vmat * coords[1]
        v = v2 - v1
        v[2] = 0.0
        if v.length > 0.0:
            v.normalize()
            q = v.rotation_difference(Vector((1, 0, 0)))
            quat.invert()
            quat = q * quat
            quat.invert()
    else:
        quat = None

    return loc, quat


class data:
    presets = []  # undoで戻されるので……
    preset_added = False
    preset_removed = False

    @classmethod
    def presets_init(cls, context):
        cls.presets.clear()
        for preset in context.scene.local_grid.presets:
            cls.presets.append(preset.copy())
        cls.preset_added = False
        cls.preset_removed = False

    @classmethod
    def presets_apply(cls, context):
        # TODO: 名称の重複解消
        presets = context.scene.local_grid.presets
        presets.clear()
        for temp_preset in cls.presets:
            preset = presets.add()
            for attr in dir(temp_preset):
                if not attr.startswith('_'):
                    setattr(preset, attr, getattr(temp_preset, attr))


def collection_property_unique_name(collection_property):
    """CollectionPropertyのname属性を重複しないように変更する"""
    for prop in collection_property:
        if not prop.name:
            prop.name = 'Preset'
    names = [prop.name for prop in collection_property]
    for i, prop in enumerate(collection_property):
        if names.index(prop.name) == i:
            continue

        name = prop.name
        m = re.match('(.*?)\.(\d+)', name)
        if m:
            base_name = m.group(1)
            count = int(m.group(2))
        else:
            base_name = name
            count = 0
        while name in names:
            count += 1
            name = '{}.{:03}'.format(base_name, count)
        prop.name = names[i] = name


class VIEW3D_OT_localgrid_preset_add(bpy.types.Operator):
    bl_label = 'Add Local Grid Preset'
    bl_description = 'Add local grid preset'
    bl_idname = 'view3d.localgrid_preset_add'
    bl_options = {'REGISTER'}

    name = bpy.props.StringProperty(
        name='Name',
        options={'SKIP_SAVE'})
    location = bpy.props.FloatVectorProperty(
        name='Location',
        step=1,
        precision=3,
        subtype='XYZ',
        size=3,
        options={'SKIP_SAVE'})
    rotation = bpy.props.FloatVectorProperty(
        name='Rotation',
        default=(1, 0, 0, 0),
        step=1,
        precision=3,
        subtype='QUATERNION',
        size=4,
        options={'SKIP_SAVE'})
    delta_rotation_euler = bpy.props.FloatVectorProperty(
        name='Delta Rotation',
        default=(0, 0, 0),
        step=1,
        precision=3,
        subtype='EULER',
        size=3,
        options={'SKIP_SAVE'})
    use_cache = bpy.props.BoolProperty(
        name='Use Cache',
        default=False,
        options={'SKIP_SAVE', 'HIDDEN'})

    def execute(self, context):
        presets = context.scene.local_grid.presets
        preset = presets.add()
        for attr in ['name', 'location', 'rotation', 'delta_rotation_euler']:
            setattr(preset, attr, getattr(self, attr))
        if self.use_cache:
            data.presets.append(preset.copy())
            data.preset_added = True
            collection_property_unique_name(data.presets)
        else:
            collection_property_unique_name(presets)
        self.name = presets[-1].name
        return {'FINISHED'}


class VIEW3D_OT_localgrid_preset_edit(bpy.types.Operator):
    bl_label = 'Edit Local Grid Preset'
    bl_description = 'Apply preset changes'
    bl_idname = 'view3d.localgrid_preset_edit'
    bl_options = {'REGISTER'}

    index = bpy.props.IntProperty(
        name='Index',
        min=0,
        options={'SKIP_SAVE'})
    name = bpy.props.StringProperty(
        name='Name',
        options={'SKIP_SAVE'})
    location = bpy.props.FloatVectorProperty(
        name='Location',
        step=1,
        precision=3,
        subtype='XYZ',
        size=3,
        options={'SKIP_SAVE'})
    rotation = bpy.props.FloatVectorProperty(
        name='Rotation',
        default=(1, 0, 0, 0),
        step=1,
        precision=3,
        subtype='QUATERNION',
        size=4,
        options={'SKIP_SAVE'})
    delta_rotation_euler = bpy.props.FloatVectorProperty(
        name='Delta Rotation',
        default=(0, 0, 0),
        step=1,
        precision=3,
        subtype='EULER',
        size=3,
        options={'SKIP_SAVE'})
    use_cache = bpy.props.BoolProperty(
        name='Use Cache',
        default=False,
        options={'SKIP_SAVE', 'HIDDEN'})

    def execute(self, context):
        if self.use_cache:
            presets = data.presets
        else:
            presets = context.scene.local_grid.presets
        if not (0 <= self.index < len(presets)):
            return {'CANCELLED'}
        preset = presets[self.index]
        for attr in ['name', 'location', 'rotation', 'delta_rotation_euler']:
            if self.properties.is_property_set(attr):
                setattr(preset, attr, getattr(self, attr))
        collection_property_unique_name(presets)
        self.name = presets[-1].name
        return {'FINISHED'}


class VIEW3D_OT_localgrid_preset_remove(bpy.types.Operator):
    bl_label = 'Remove Local Grid Preset'
    bl_description = 'Remove local grid preset'
    bl_idname = 'view3d.localgrid_preset_remove'
    bl_options = {'REGISTER'}

    index = bpy.props.IntProperty(
        name='Index',
        min=0,
        options={'SKIP_SAVE'})
    use_cache = bpy.props.BoolProperty(
        name='Use Cache',
        default=False,
        options={'SKIP_SAVE', 'HIDDEN'})

    def execute(self, context):
        if self.use_cache:
            presets = data.presets
        else:
            presets = context.scene.local_grid.presets
        if not (0 <= self.index < len(presets)):
            return {'CANCELLED'}
        if self.use_cache:
            presets[self.index: self.index + 1] = []
            data.preset_removed = True
        else:
            presets.remove(self.index)
        return {'FINISHED'}


class VIEW3D_OT_localgrid_ex(vaop.OperatorTemplate, bpy.types.Operator):
    bl_label = 'Toggle Local Grid'
    bl_idname = 'view3d.localgrid_ex'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'type'

    mode = bpy.props.EnumProperty(
        name='Mode',
        items=(('TOGGLE', 'Toggle', ''),
               ('ENABLE', 'Enable', ''),
               ('DISABLE', 'Disable', ''),
               ('NONE', 'None', 'Not change')),
        default='TOGGLE',
        options={'SKIP_SAVE'})

    def _type_items(self, context):
        items = [
            ('NONE', 'None', 'Edit current location and rotation', 'GRID', 0),
            ('OBJECT', 'Object', 'Object matrix', 'OBJECT_DATA', 1),
            ('VIEW', 'View', 'View matrix', 'RESTRICT_VIEW_OFF', 3),
            ('CURSOR_SELECTION', 'Cursor Selection',
             'location: 3D cursor, rotation: selected elements',
             'VERTEXSEL', 4),
        ]
        if USE_MANIPULATOR:
            items.append(
                ('MANIPULATOR', 'Manipulator', 'Transform manipulator matrix',
                 'MANIPUL', 2))
        if USE_OBB:
            items.append(('OBB', 'OBB', 'Calc convexhull and OBB',
                          'VERTEXSEL', 5))
        # プリセット要素を追加。identifierはpresetsでのインデックス
        if hasattr(context, 'scene') and context.scene:
            for i, preset in enumerate(data.presets):
                items.append((str(i), preset.name, '', 'NONE', len(items)))
        VIEW3D_OT_localgrid_ex._type_items_cache = items
        return items

    def _type_update(self, context):
        """属性値の初期化"""
        for prop_name in ['preset_name', 'location', 'rotation',
                          'delta_rotation_euler']:
            self.property_unset(prop_name)
        self.type_updated = True

    type = bpy.props.EnumProperty(
        name='Type',
        items=_type_items,
        update=_type_update,
        options={'SKIP_SAVE'},
    )
    type_updated = bpy.props.BoolProperty(
        name='',
        description='typeが更新されたら真になる',
        options={'SKIP_SAVE', 'HIDDEN'})

    preset_name = bpy.props.StringProperty(
        name='Preset Name',
        options={'SKIP_SAVE'})

    set_location = bpy.props.BoolProperty(
        name='Set Location',
        default=True,
        options={'SKIP_SAVE'})
    set_rotation = bpy.props.BoolProperty(
        name='Set Rotation',
        default=True,
        options={'SKIP_SAVE'})
    location = bpy.props.FloatVectorProperty(
        name='Location',
        step=1,
        precision=3,
        subtype='XYZ',
        size=3,
        options={'SKIP_SAVE'})
    rotation = bpy.props.FloatVectorProperty(
        name='Rotation',
        default=(1, 0, 0, 0),
        step=1,
        precision=3,
        subtype='QUATERNION',
        size=4,
        options={'SKIP_SAVE'})
    delta_rotation_euler = bpy.props.FloatVectorProperty(
        name='Delta Rotation',
        default=(0, 0, 0),
        step=1,
        precision=3,
        subtype='EULER',
        size=3,
        options={'SKIP_SAVE'})

    preset_add = bpy.props.BoolProperty(
        name='Added Preset Item',
        options={'SKIP_SAVE', 'HIDDEN'})
    not_draw_props = bpy.props.BoolProperty(
        name='',
        options={'SKIP_SAVE', 'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.area and context.area.type == 'VIEW_3D'

    def __init__(self):
        context = bpy.context
        v3d = context.space_data
        rv3d = context.region_data

        # keep v3d attrs
        self._use_local_grid = v3d.use_local_grid
        self._local_grid_location = v3d.local_grid_location.copy()
        self._local_grid_rotation = v3d.local_grid_rotation.copy()
        if self._local_grid_rotation.magnitude == 0.0:
            # [0, 0, 0, 0] -> [1, 0, 0, 0]
            self._local_grid_rotation.identity()
        # keep rv3d attrs
        self._view_location = rv3d.view_location.copy()
        self._view_rotation = rv3d.view_rotation.copy()
        self._view = vav.quat_to_axis_view(
            rv3d.view_rotation.inverted(), v3d.local_grid_rotation)

        # cache
        if USE_MANIPULATOR:
            self.mmat = manipulatormatrix.ManipulatorMatrix(context)
        if USE_OBB:
            self.obb_loc_quat = None

        data.presets_init(context)

    def get_region_view(self, context):
        """各Region毎の現在の視点を求める
        :rtype: OrderedDict
        """
        area = context.area
        v3d = context.space_data
        regions = OrderedDict()  # {region: [rv3d, view], ...}
        win_regions = [ar for ar in area.regions if ar.type == 'WINDOW']
        if v3d.region_quadviews:
            rv3ds = v3d.region_quadviews
        else:
            rv3ds = [v3d.region_3d]
        if v3d.use_local_grid:
            lg_rot = v3d.local_grid_rotation
        else:
            lg_rot = None
        for region, rv3d in zip(win_regions, rv3ds):
            view = vav.quat_to_axis_view(rv3d.view_rotation.inverted(), lg_rot)
            regions[region] = [rv3d, view]
        return regions

    def is_set_enable(self):
        if self.mode == 'TOGGLE':
            value = not self._use_local_grid
        elif self.mode == 'ENABLE':
            value = True
        elif self.mode == 'DISABLE':
            value = False
        else:  # 'NONE'
            value = self._use_local_grid
        return value

    def cancel(self, context):
        v3d = context.space_data
        v3d.use_local_grid = self._use_local_grid
        v3d.local_grid_location = self._local_grid_location
        v3d.local_grid_rotation = self._local_grid_rotation
        collection_property_unique_name(data.presets)
        data.presets_apply(context)

    def execute(self, context):
        # NUMPADで視点変更する事も考慮して視点をその都度計算する
        region_views = self.get_region_view(context)

        v3d = context.space_data

        presets = data.presets
        if data.preset_added:
            self.type = str(len(presets) - 1)
            data.preset_added = False
        if data.preset_removed:
            self.properties.property_unset('preset_name')
            data.preset_removed = False
        if self.type.isnumeric():
            preset = presets[int(self.type)]
        else:
            preset = None

        # location, rotation, delta_rotation_eulerの更新
        if preset:
            loc = preset.location
            quat = preset.rotation
            drot = preset.delta_rotation_euler
            name = presets[int(self.type)].name
        else:
            loc = quat = None
            name = ''
            if self.type == 'OBJECT':
                ob = context.active_object
                if ob and (ob.mode != 'OBJECT' or ob.select):
                    loc, quat = mat4_to_loc_quat(ob.matrix_world)
                    name = ob.name
                else:
                    if self.is_set_enable():
                        self.report({'WARNING'}, 'No active object')
                        self.cancel(context)
                        return {'CANCELLED'}
            elif self.type == 'VIEW':
                rv3d, view = region_views[context.region]
                loc, quat = rv3d.view_location, rv3d.view_rotation
                name = 'View'
            elif self.type == 'CURSOR_SELECTION':
                loc, quat = loc_quat_from_cursor_selection(context)
                name = 'Selection'
            elif self.type == 'MANIPULATOR':
                v3d = context.space_data
                mmat = self.mmat
                mmat.update(context, view_only=True, cursor_only=True)
                loc, quat = mat4_to_loc_quat(mmat)
                name = 'Manipulator'
            elif self.type == 'OBB':
                if not self.obb_loc_quat:
                    self.obb_loc_quat = loc_quat_from_obb(context)
                loc, quat = self.obb_loc_quat
                name = 'OBB'
            else:  # 'NONE'
                loc, quat = self._local_grid_location, self._local_grid_rotation
            drot = Euler((0, 0, 0))

        if not self.properties.is_property_set('location') and loc:
            self.location = loc
        if not self.properties.is_property_set('rotation') and quat:
            self.rotation = quat
        if not self.properties.is_property_set('delta_rotation_euler'):
            self.delta_rotation_euler = drot
        if not self.properties.is_property_set('preset_name'):
            self.preset_name = name

        # update v3d.use_local_grid
        v3d.use_local_grid = self.is_set_enable()
        # update v3d.local_grid_location
        if self.set_location:
            loc = self.location
        else:
            loc = self._local_grid_location
        v3d.local_grid_location = loc
        # update v3d.local_grid_rotation
        if self.set_rotation:
            quat = self.rotation
        else:
            quat = self._local_grid_rotation
        drot = self.delta_rotation_euler.to_quaternion()
        v3d.local_grid_rotation = (quat * drot).normalized()

        # 視点変更。typeが更新された際のみsmooth_viewを有効にする
        if not self.type_updated:
            smooth_view = context.user_preferences.view.smooth_view
            context.user_preferences.view.smooth_view = 0
        for region, (rv3d, view) in region_views.items():
            if view not in ('user', None) and not rv3d.lock_rotation:
                override = context.copy()
                override['region'] = region
                bpy.ops.view3d.viewnumpad(override, type=view.upper())
        if not self.type_updated:
            context.user_preferences.view.smooth_view = smooth_view
        self.type_updated = False

        # Undoで戻されるlocal_grid.presetsに変更を適用する
        collection_property_unique_name(data.presets)
        data.presets_apply(context)

        return {'FINISHED'}

    def invoke(self, context, event):
        if event.shift or event.ctrl:
            if self.type.isnumeric():
                bpy.ops.view3d.localgrid_preset_remove(index=int(self.type))
                self.not_draw_props = True
                return {'FINISHED'}
        return self.execute(context)

    def draw(self, context):
        if self.not_draw_props:
            return

        layout = self.layout

        preset = None
        if self.type.isnumeric():
            i = int(self.type)
            if 0 <= i < len(data.presets):
                preset = data.presets[i]

        for attr in self.as_keywords():
            if attr == 'preset_name':
                # if not preset:
                continue
            col = self.draw_property(attr, layout)
            if attr == 'location':
                col.active = self.set_location
            elif attr in ('rotation', 'delta_rotation_euler'):
                col.active = self.set_rotation

        # Preset
        self.draw_property('preset_name', layout, text='Preset')
        # Preset Add
        row = layout.row(align=True)
        sub = row.row()
        op = sub.operator('view3d.localgrid_preset_add', text='',
                          icon='ZOOMIN')
        op.name = self.preset_name
        op.location = self.location
        op.rotation = self.rotation
        op.delta_rotation_euler = self.delta_rotation_euler
        op.use_cache = True
        # Preset Remove
        sub = row.row()
        sub.enabled = preset is not None
        op = sub.operator('view3d.localgrid_preset_remove', text='',
                          icon='ZOOMOUT')
        if preset:
            op.index = i
            op.use_cache = True
        # Preset Edit
        sub = row.row()
        sub.enabled = preset is not None
        op = sub.operator('view3d.localgrid_preset_edit', text='Apply')
        if preset:
            op.index = i
            op.name = self.preset_name
            op.location = self.location
            op.rotation = self.rotation
            op.delta_rotation_euler = self.delta_rotation_euler
            op.use_cache = True


###############################################################################
# Utils
###############################################################################
# 3D Cursor -------------------------------------------------------------------
class VIEW3D_OT_localgrid_cursor_clear(bpy.types.Operator):
    bl_label = 'Reset 3D Cursor Location'
    bl_idname = 'view3d.localgrid_cursor_location_clear'
    # bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        v3d = context.space_data
        scn = context.scene
        if v3d.use_local_grid:
            v3d.cursor_location = v3d.local_grid_location
        else:
            v3d.cursor_location = [0.0, 0.0, 0.0]
        return {'FINISHED'}


# Object Location -------------------------------------------------------------
class OBJECT_OT_custom_location_set(vaop.OperatorTemplate, bpy.types.Operator):
    bl_label = 'Set Location'
    bl_description = 'Move object to'
    bl_idname = 'object.custom_location_set'
    bl_options = {'REGISTER', 'UNDO'}

    type = bpy.props.EnumProperty(
        name='Type',
        items=(('ACTIVE', 'Active Object', ''),
               ('ORIGIN', 'Scene Origin', 'Scene origin or local grid origin'),
               ('CUSTOM', 'Custom', '')),
        default='ACTIVE',
        options={'SKIP_SAVE'})
    location = bpy.props.FloatVectorProperty(
        name='Location',
        step=1,
        precision=3,
        subtype='XYZ',
        size=3,
        options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        v3d = context.space_data
        scene = context.scene
        cursor_bak = v3d.cursor_location.copy()
        # カーソルを移動
        if self.type == 'ACTIVE':
            actob = context.active_object
            if actob:
                location = actob.matrix_world.to_translation()
            else:
                return {'FINISHED'}
        elif self.type == 'ORIGIN':
            if v3d.use_local_grid:
                location = v3d.local_grid_location
            else:
                location = Vector()
        else:
            location = self.location
        v3d.cursor_location = location

        # view3d.snap_selected_to_cursor()でオブジェクトを移動
        override = context.copy()
        for ob in vaob.sorted_objects(context.selected_objects):
            if self.type == 'ACTIVE' and ob == context.active_object:
                continue

            # ソースを見ないと判らないってのはどうなのよ
            override['selected_objects'] = [ob]
            override['selected_editable_objects'] = [ob]

            bpy.ops.view3d.snap_selected_to_cursor(override)

        v3d.cursor_location = cursor_bak
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        for attr in self.properties.bl_rna.properties.keys():
            col = self.draw_property(attr, layout)
            if attr == 'location' and self.type != 'CUSTOM':
                col.active = False


class OBJECT_OT_custom_location_apply(vaop.OperatorTemplate, bpy.types.Operator):
    bl_label = 'Apply Location'
    bl_idname = 'object.custom_location_apply'
    bl_options = {'REGISTER', 'UNDO'}

    type = bpy.props.EnumProperty(
        name='Type',
        items=(('ACTIVE', 'Active Object', ''),
               ('GRID', 'Grid', ''),
               ('CUSTOM', 'Custom', '')),
        default='ACTIVE',
        options={'SKIP_SAVE'})
    location = bpy.props.FloatVectorProperty(
        name='Location',
        step=1,
        precision=3,
        subtype='XYZ',
        size=3,
        options={'SKIP_SAVE'})
    use_delta = bpy.props.BoolProperty(
        name='Use delta',
        description='Include Object.delta_location',
        default=False,
        options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        if self.type == 'ACTIVE':
            actob = context.active_object
            if actob:
                location = actob.matrix_world.to_translation()
            else:
                return {'FINISHED'}
        elif self.type == 'GRID':
            v3d = context.space_data
            if v3d.use_local_grid:
                location = v3d.local_grid_location
            else:
                location = Vector()
        else:
            location = self.location

        override = context.copy()
        for ob in vaob.sorted_objects(context.selected_objects):
            if self.type == 'ACTIVE' and ob == context.active_object:
                continue

            # オペレータのソースを見ないと判らないってのはどうなのよ
            override['selected_objects'] = [ob]
            override['selected_editable_objects'] = [ob]

            delta = ob.delta_location.copy()
            if ob.parent:
                mat = ob.parent.matrix_world * ob.matrix_parent_inverse
                target_loc = mat.inverted() * location
            else:
                target_loc = location

            ob.location -= target_loc
            if self.use_delta:
                ob.location += delta
            context.scene.update()

            bpy.ops.object.transform_apply(override, location=True)

            ob.location += target_loc
            context.scene.update()

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        for attr in self.properties.bl_rna.properties.keys():
            col = self.draw_property(attr, layout)
            if attr == 'location' and self.type != 'CUSTOM':
                col.active = False


# Object Rotation -------------------------------------------------------------
class OBJECT_OT_custom_rotation_set(vaop.OperatorTemplate, bpy.types.Operator):
    bl_label = 'Set Rotation'
    bl_idname = 'object.custom_rotation_set'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    type = bpy.props.EnumProperty(
        name='Type',
        items=(('ACTIVE', 'Active Object', ''),
               ('GRID', 'Grid', ''),
               ('CUSTOM', 'Custom', '')),
        default='ACTIVE',
        options={'SKIP_SAVE'})
    rotation = bpy.props.FloatVectorProperty(
        name='Rotation',
        description='World coordinates',
        default=(1, 0, 0, 0),
        step=1,
        precision=3,
        subtype='QUATERNION',
        size=4,
        options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        # Note: world_rot = parent_mat * parent_inv * delta_rot * rot

        if self.type == 'ACTIVE':
            actob = context.active_object
            if actob:
                rotation = actob.matrix_world.to_quaternion()
            else:
                return {'FINISHED'}
        elif self.type == 'GRID':
            v3d = context.space_data
            if v3d.use_local_grid:
                rotation = v3d.local_grid_rotation
            else:
                rotation = Quaternion((1, 0, 0, 0))
        else:
            rotation = self.rotation

        for ob in vaob.sorted_objects(context.selected_objects):
            if self.type == 'ACTIVE' and ob == context.active_object:
                continue

            if ob.parent:
                parent_mat = ob.parent.matrix_world.to_3x3()
                parent_inv = ob.matrix_parent_inverse.to_3x3()
                mat = parent_mat * parent_inv
                quat = mat.inverted().to_quaternion() * rotation
            else:
                quat = rotation
            if ob.rotation_mode == 'AXIS_ANGLE':
                axis, angle = quat.to_axis_angle()
                ob.rotation_axis_angle = [angle] + list(axis)
            elif ob.rotation_mode == 'QUATERNION':
                delta = ob.delta_rotation_quaternion
                q = delta.inverted() * quat
                ob.rotation_quaternion = q
            else:
                delta = ob.delta_rotation_euler.to_quaternion()
                q = delta.inverted() * quat
                ob.rotation_euler = q.to_euler(ob.rotation_mode)

            # Object.matrix_worldを更新する為、Scene.update()を実行する
            # ob.update_tag({'OBJECT', 'DATA'})
            context.scene.update()

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        for attr in self.properties.bl_rna.properties.keys():
            col = self.draw_property(attr, layout)
            if attr == 'rotation' and self.type != 'CUSTOM':
                col.active = False


class OBJECT_OT_custom_rotation_apply(vaop.OperatorTemplate,
                                      bpy.types.Operator):
    bl_label = 'Appli Rotation'
    bl_idname = 'object.custom_rotation_apply'
    bl_options = {'REGISTER', 'UNDO'}

    type = bpy.props.EnumProperty(
        name='Type',
        items=(('ACTIVE', 'Active Object', ''),
               ('GRID', 'Grid', ''),
               ('CUSTOM', 'Custom', '')),
        default='ACTIVE',
        options={'SKIP_SAVE'})
    rotation = bpy.props.FloatVectorProperty(
        name='Rotation',
        description='Use active object\'s matrix_world if not set',
        default=(1, 0, 0, 0),
        step=1,
        precision=3,
        subtype='QUATERNION',
        size=4,
        options={'SKIP_SAVE'})
    use_delta = bpy.props.BoolProperty(
        name='Use delta',
        description='Include Object.delta_rotation_quaternion '
                    '(or delta_rotation_euler)',
        default=True,
        options={'SKIP_SAVE'})  # locationの場合とは違いTrueなのはblenderの仕様

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        if self.type == 'ACTIVE':
            actob = context.active_object
            if actob:
                rotation = actob.matrix_world.to_quaternion()
            else:
                return {'FINISHED'}
        elif self.type == 'GRID':
            v3d = context.space_data
            if v3d.use_local_grid:
                rotation = v3d.local_grid_rotation
            else:
                rotation = Quaternion((1, 0, 0, 0))
        else:
            rotation = self.rotation

        # world_rot = parent_mat * parent_inv * delta_rot * rot
        override = context.copy()
        for ob in vaob.sorted_objects(context.selected_objects):
            if self.type == 'ACTIVE' and ob == context.active_object:
                continue

            # オペレータのソース部分を見ないと判らないってのはどうなのよ
            override['selected_objects'] = [ob]
            override['selected_editable_objects'] = [ob]

            if ob.parent:
                parent_mat = ob.parent.matrix_world.to_3x3()
                parent_inv = ob.matrix_parent_inverse.to_3x3()
                mat = parent_mat * parent_inv
                target_quat = mat.inverted().to_quaternion() * rotation
            else:
                target_quat = rotation

            if ob.rotation_mode == 'AXIS_ANGLE':
                def rotate(quat):
                    angle, *axis = ob.rotation_axis_angle
                    local_quat = Quaternion(axis, angle)
                    q = quat * local_quat
                    axis, angle = q.to_axis_angle()
                    ob.rotation_axis_angle = [angle] + list(axis)
                rotate(target_quat.inverted())
                context.scene.update()

                bpy.ops.object.transform_apply(override, rotation=True)

                rotate(target_quat)

            elif ob.rotation_mode == 'QUATERNION':
                # transform_apply()は
                # delta_rotation_quaternion * rotation_quaternion の回転状態で
                # 計算される。その後rotation_quaternionはクリアされるが
                # delta_rotation_quaternionの数値はそのまま残る
                if self.use_delta:
                    delta = ob.delta_rotation_quaternion
                    # normalize()必要？
                else:
                    delta = Quaternion([1, 0, 0, 0])
                rot = ob.rotation_quaternion

                # target_quatの逆回転を行いtransform_apply()、
                # そしてtarget_quat分回転する
                # target.inverted() * delta * rot = delta * quat
                # quat = delta.inverted() * target.inverted() * delta * rot

                quat = delta.inverted() * target_quat.inverted() * delta * rot
                ob.rotation_quaternion = quat

                # ob.update_tag({'OBJECT', 'DATA'})
                context.scene.update()

                bpy.ops.object.transform_apply(override, rotation=True)

                ob.rotation_quaternion = target_quat * ob.rotation_quaternion
                # ob.update_tag({'OBJECT', 'DATA'})

            else:
                if self.use_delta:
                    delta = ob.delta_rotation_euler.to_quaternion()
                else:
                     delta = Quaternion([1, 0, 0, 0])
                rot = ob.rotation_euler.to_quaternion()

                quat = delta.inverted() * target_quat.inverted() * delta * rot
                ob.rotation_euler = quat.to_euler(ob.rotation_mode)
                context.scene.update()

                bpy.ops.object.transform_apply(override, rotation=True)

                ob.rotation_euler = target_quat.to_euler(ob.rotation_mode)

            context.scene.update()

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        for attr in self.properties.bl_rna.properties.keys():
            col = self.draw_property(attr, layout)
            if attr == 'rotation' and self.type != 'CUSTOM':
                col.active = False


###############################################################################
# Menu
###############################################################################
class VIEW3D_MT_localgrid_utils(bpy.types.Menu):
    bl_label = 'Local Grid Utils'
    bl_description = ''
    bl_options = {'REGISTER'}

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        op = layout.operator(
            'view3d.localgrid_cursor_location_clear',
            text='Reset 3D Cursor', icon='CURSOR')
        op = layout.operator(
            'object.custom_location_set',
            text='Clear Object Location', icon='MAN_TRANS')
        op.type = 'ORIGIN'
        op = layout.operator(
            'object.custom_rotation_set',
            text='Clear Object Rotation', icon='MAN_ROT')
        op.type = 'GRID'

        layout.separator()
        op = layout.operator(
            'object.custom_location_apply',
            text='Apply Object Location', icon='MANIPUL')
        op.type = 'GRID'
        op = layout.operator(
            'object.custom_rotation_apply',
            text='Apply Object Rotation', icon='MANIPUL')
        op.type = 'GRID'


class VIEW3D_MT_localgrid(bpy.types.Menu):
    bl_label = 'Local Grid Menu'
    bl_description = 'Local Grid menu'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT' # call invoke

        # Sub Menu
        layout.menu('VIEW3D_MT_localgrid_utils', text='Utils', icon='CURSOR')
        layout.separator()

        # Toggle
        op = layout.operator('view3d.localgrid_ex',
                             text='Toggle', icon='ARROW_LEFTRIGHT')
        op.mode = 'TOGGLE'
        op.type = 'NONE'

        # Set Object
        op = layout.operator('view3d.localgrid_ex',
                             text='Object', icon='OBJECT_DATA')
        op.mode = 'ENABLE'
        op.type = 'OBJECT'

        # Set View
        op = layout.operator('view3d.localgrid_ex',
                             text='View', icon='RESTRICT_VIEW_OFF')
        op.mode = 'ENABLE'
        op.type = 'VIEW'

        # Set View Selection
        op = layout.operator('view3d.localgrid_ex',
                             text='Cursor Selection', icon='CURSOR')
        op.mode = 'ENABLE'
        op.type = 'CURSOR_SELECTION'

        # Set Manipulator
        if USE_MANIPULATOR:
            op = layout.operator('view3d.localgrid_ex',
                                 text='Manipulator', icon='MANIPUL')
            op.mode = 'ENABLE'
            op.type = 'MANIPULATOR'

        # Set OBB
        if USE_OBB:
            op = layout.operator('view3d.localgrid_ex',
                                 text='OBB', icon='VERTEXSEL')
            op.mode = 'ENABLE'
            op.type = 'OBB'

        if context.scene.local_grid.presets:
            layout.separator()
            for i, preset in enumerate(context.scene.local_grid.presets):
                op = layout.operator('view3d.localgrid_ex', text=preset.name)
                op.mode = 'ENABLE'
                op.type = str(i)


###############################################################################
# Register
###############################################################################
addon_keymaps = []


def register():
    addongroup.AddonGroup.register_module(__name__)

    bpy.types.Scene.local_grid = bpy.props.PointerProperty(
        name='Local Grid',
        type=LocalGridData)

    km = addongroup.AddonGroup.get_keymap('3D View')
    if km:
        kmi = km.keymap_items.new(
            'wm.call_menu', 'NUMPAD_SLASH', 'PRESS', ctrl=True)
        kmi.properties.name = 'VIEW3D_MT_localgrid'
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            'view3d.localgrid_ex', 'NUMPAD_SLASH', 'PRESS', shift=True,
            ctrl=True)
        kmi.properties.mode = 'TOGGLE'
        kmi.properties.type = 'NONE'
        addon_keymaps.append((km, kmi))

        # kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS', ctrl=True,
        #                           oskey=True)
        # kmi.properties.name = 'VIEW3D_MT_localgrid'
        # addon_keymaps.append((km, kmi))
        #
        # kmi = km.keymap_items.new('view3d.localgrid_ex', 'E', 'PRESS',
        #                           oskey=True)
        # kmi.properties.mode = 'TOGGLE'
        # # # TODO: itemsが関数のEPに代入すると落ちるバグ
        # # kmi.properties.type_ = 'OBJECT'
        # kmi.properties.type = 'OBJECT'
        # addon_keymaps.append((km, kmi))

        # kmi = km.keymap_items.new('view3d.localgrid_ex', 'E', 'PRESS',
        #                           ctrl=True, oskey=True)
        # kmi.properties.mode = 'ENABLE'
        # addon_keymaps.append((km, kmi))
        #
        # kmi = km.keymap_items.new('view3d.localgrid_ex', 'E', 'PRESS',
        #                           shift=True, oskey=True)
        # kmi.properties.mode = 'TOGGLE'
        # kmi.properties.set_location = False
        # kmi.properties.set_rotation = False
        # addon_keymaps.append((km, kmi))


def unregister():
    addongroup.AddonGroup.unregister_module(__name__)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    if bpy.context.scene.get('local_grid') != None:
        del bpy.context.scene['local_grid']
    try:
        del bpy.types.Scene.local_grid
    except:
        pass


if __name__ == '__main__':
    register()
