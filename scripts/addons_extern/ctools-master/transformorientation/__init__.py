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
    'name': 'Transform Orientation Editor',
    'author': 'chromoly',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'location': 'View3D > Properties > Transform Orientations',
    'description': 'Edit transform orientation',
    'wiki_url': '',
    'category': '3D View',
}

"""
作成した Transform Orientation を編集する。
"""


import importlib

import bpy
from mathutils import Vector
import bmesh

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(manipulatormatrix)
    importlib.reload(st)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import manipulatormatrix
    from ..utils import structures as st


PROP_SHOW_ATTR = 'show_transform_orientation_details'
PROP_AXIS_ATTR = 'transform_orientation_matrix'  # + '_x', '_y', '_z'
show_transform_orientation_details = False

AXIS_VALUES_MAX = 10  # 履歴の最大数
copied_axis_values = []  # [(name, Vector), ...]


translation_dict = {
    'ja_JP': {
        ('*', 'String'): '文字列',
    }
}


class TransformOrientationEditorPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        layout.separator()
        super().draw(context)


def get_orientation(context):
    if context.area and context.area.type == 'VIEW_3D':
        return context.space_data.current_orientation
    return None


class OperatorNormalize(bpy.types.Operator):
    bl_idname = 'transfomr.oe_normalize'
    bl_label = 'Normalize Orientation'
    bl_description = 'Normalize orientation'
    bl_options = {'REGISTER', 'INTERNAL'}

    axes = bpy.props.EnumProperty(
        name='Axes',
        items=[('XYZ', 'XYZ', ''),
               ('XZY', 'XZY', ''),
               ('YXZ', 'YXZ', ''),
               ('YZX', 'YZX', ''),
               ('ZXY', 'ZXY', ''),
               ('ZYX', 'ZYX', '')],
        default='XYZ'
    )

    def execute(self, context):
        orientation = get_orientation(context)
        if not orientation:
            return {'CANCELLED'}

        def normalize(vec, index):
            if vec.length == 0.0:
                vec[:] = [0.0] * 3
                vec[index] = 1.0
            else:
                vec.normalize()

        mat = orientation.matrix
        axes = ['XYZ'.index(s) for s in self.axes]
        i, j, k = axes

        vec1 = mat.col[i]
        normalize(vec1, i)

        vec2 = mat.col[j]
        normalize(vec2, j)

        vec3 = mat.col[k]
        normalize(vec3, k)

        if vec1 != vec2:
            if (i + 1) % 3 == j:
                vec3[:] = vec1.cross(vec2).normalized()
                vec2[:] = vec3.cross(vec1).normalized()
            else:
                vec3[:] = vec2.cross(vec1).normalized()
                vec2[:] = vec1.cross(vec3).normalized()
        elif vec1 != vec3:
            if (i + 1) % 3 != k:
                vec2[:] = vec1.cross(vec3).normalized()
                vec3[:] = vec2.cross(vec1).normalized()
            else:
                vec2[:] = vec3.cross(vec1).normalized()
                vec3[:] = vec1.cross(vec2).normalized()
        else:
            v = Vector([0.0] * 3)
            v[i] = 1.0
            q = v.rotation_difference(vec1)
            m = q.to_matrix()
            for c in range(3):
                mat.col[c] = m.col[c]

        return {'FINISHED'}


class OperatorPasteFrom(bpy.types.Operator):
    bl_idname = 'transfomr.oe_paste_from'
    bl_label = 'Paste Orientation'
    bl_description = ''
    bl_options = {'REGISTER', 'INTERNAL'}

    orientation = bpy.props.StringProperty()

    def execute(self, context):
        orientation = get_orientation(context)
        if not orientation:
            return {'CANCELLED'}

        # quadviewの場合は右上のregionを使う
        ctx_bak = st.context_py_dict_get(context)
        ctx = None
        if context.space_data.region_quadviews and ctx_bak is None:
            ctx = context.copy()
            ctx['region'] = context.area.regions[-1]
            st.context_py_dict_set(context, ctx)

        mmat = manipulatormatrix.ManipulatorMatrix(context,
                                                   use_normalized=False)
        if ctx:
            st.context_py_dict_set(context, ctx_bak)

        mmat.orientation = self.orientation
        for i in range(3):
            orientation.matrix.col[i] = mmat.col[i].to_3d()
        return {'FINISHED'}


class OperatorMenu(bpy.types.Operator):
    bl_idname = 'transfomr.oe_menu'
    bl_label = 'Orientation Menu'
    bl_description = ''
    bl_options = {'REGISTER', 'INTERNAL'}

    def invoke(self, context, event):
        bpy.ops.wm.call_menu(name=MenuMain.bl_idname)
        return {'FINISHED'}


class OperatorAxisNormalize(bpy.types.Operator):
    bl_idname = 'transfomr.oe_axis_normalize'
    bl_label = 'Normalize Orientation Axis'
    bl_description = 'Normalize orientation axis'
    bl_options = {'REGISTER', 'INTERNAL'}

    axis = bpy.props.EnumProperty(
        name='Axis',
        items=[('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')],
    )

    def execute(self, context):
        orientation = get_orientation(context)
        if not orientation:
            return {'CANCELLED'}

        i = 'XYZ'.index(self.axis)
        orientation.matrix.col[i].normalize()

        return {'FINISHED'}


class OperatorAxisMove(bpy.types.Operator):
    bl_idname = 'transfomr.oe_axis_move'
    bl_label = 'Move Orientation Axis'
    bl_description = 'Move orientation axis'
    bl_options = {'REGISTER', 'INTERNAL'}

    axes = bpy.props.EnumProperty(
        name='Axes',
        items=[('XY', 'X -> Y', ''),
               ('XZ', 'X -> Z', ''),
               ('YX', 'Y -> X', ''),
               ('YZ', 'Y -> Z', ''),
               ('ZX', 'Z -> X', ''),
               ('ZY', 'Z -> Y', '')],
    )

    def execute(self, context):
        orientation = get_orientation(context)
        if not orientation:
            return {'CANCELLED'}

        move_from = 'XYZ'.index(self.axes[0])
        move_to = 'XYZ'.index(self.axes[1])
        mat = orientation.matrix
        v = mat.col[move_to].copy()
        mat.col[move_to] = mat.col[move_from]
        mat.col[move_from] = v

        return {'FINISHED'}


class OperatorAxisInvert(bpy.types.Operator):
    bl_idname = 'transfomr.oe_axis_invert'
    bl_label = 'Invert Orientation Axis'
    bl_description = 'Invert orientation axis'
    bl_options = {'REGISTER', 'INTERNAL'}

    axis = bpy.props.EnumProperty(
        name='Axis',
        items=[('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')],
    )

    def execute(self, context):
        orientation = get_orientation(context)
        if not orientation:
            return {'CANCELLED'}
        mat = orientation.matrix
        i = 'XYZ'.index(self.axis)
        mat.col[i].negate()
        # -0.0 -> 0.0
        v = mat.col[i]
        for j in range(3):
            if v[j] == -0.0:
                v[j] = 0.0
        return {'FINISHED'}


class OperatorAxisFromNormal(bpy.types.Operator):
    bl_idname = 'transfomr.oe_axis_from_normal'
    bl_label = 'Orientation Axis form Normal-Y'
    bl_description = 'Normal-Y or selected 2 verts'
    bl_options = {'REGISTER', 'INTERNAL'}

    axis = bpy.props.EnumProperty(
        name='Axis',
        items=[('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')],
    )

    def execute(self, context):
        orientation = get_orientation(context)
        if not orientation:
            self.report({'INFO'}, 'Cancelled')
            return {'CANCELLED'}

        mat = orientation.matrix
        i = 'XYZ'.index(self.axis)

        if context.mode == 'EDIT_MESH':
            if context.space_data.pivot_point != 'ACTIVE_ELEMENT':
                me = context.active_object.data
                """:type: bpy.types.Mesh"""
                if me.total_vert_sel == 2:
                    bm = bmesh.from_edit_mesh(me)
                    v1, v2 = [v for v in bm.verts if v.select]
                    nor = (v1.co - v2.co).normalized()
                    if nor.length != 0.0:
                        mat.col[i] = nor
                        self.report({'INFO'}, 'From Selected 2 verts')
                        return {'FINISHED'}

        mmat = manipulatormatrix.ManipulatorMatrix(context)
        if mmat.orientations['NORMAL'] is None:
            self.report({'INFO'}, 'Cancelled')
            return {'CANCELLED'}
        mmat.orientation = 'NORMAL'
        mat.col[i] = mmat.col[1].to_3d()
        self.report({'INFO'}, 'From Normal-Y')
        return {'FINISHED'}


class OperatorAxisCopy(bpy.types.Operator):
    bl_idname = 'transfomr.oe_axis_copy'
    bl_label = 'Copy Orientation Axis'
    bl_description = 'Copy current orientation axis'
    bl_options = {'REGISTER', 'INTERNAL'}

    axis = bpy.props.EnumProperty(
        name='Axis',
        items=[('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')],
    )

    def execute(self, context):
        if not context.area or context.area.type != 'VIEW_3D':
            return {'CANCELLED'}

        mmat = manipulatormatrix.ManipulatorMatrix(context)

        i = 'XYZ'.index(self.axis)
        vec = mmat.col[i].to_3d()
        name = '{}: {} '.format(mmat.orientation, self.axis)
        copied_axis_values.insert(0, (name, vec))
        if len(copied_axis_values) > AXIS_VALUES_MAX:
            copied_axis_values.pop(AXIS_VALUES_MAX)
        return {'FINISHED'}


class OperatorAxisPaste(bpy.types.Operator):
    bl_idname = 'transfomr.oe_axis_paste'
    bl_label = 'Paste Orientation Axis'
    bl_description = 'Paste current orientation axis'
    bl_options = {'REGISTER', 'INTERNAL'}

    axis = bpy.props.EnumProperty(
        name='Axis',
        items=[('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')],
    )
    index = bpy.props.IntProperty()

    def execute(self, context):
        orientation = get_orientation(context)
        if not orientation:
            return {'CANCELLED'}

        if self.index > len(copied_axis_values):
            raise ValueError()

        i = 'XYZ'.index(self.axis)
        orientation.matrix.col[i] = copied_axis_values[self.index][1]
        return {'FINISHED'}


class OperatorAxisPasteFrom(bpy.types.Operator):
    bl_idname = 'transfomr.oe_axis_paste_from'
    bl_label = 'Paste Orientation Axis'
    bl_description = ''
    bl_options = {'REGISTER', 'INTERNAL'}

    orientation = bpy.props.StringProperty()
    axis_from = bpy.props.EnumProperty(
        name='Axis',
        items=[('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')],
    )

    axis_to = bpy.props.EnumProperty(
        name='Axis',
        items=[('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')],
    )

    def execute(self, context):
        orientation = get_orientation(context)
        if not orientation:
            return {'CANCELLED'}

        # quadviewの場合は右上のregionを使う
        ctx_bak = st.context_py_dict_get(context)
        ctx = None
        if context.space_data.region_quadviews and ctx_bak is None:
            ctx = context.copy()
            ctx['region'] = context.area.regions[-1]
            st.context_py_dict_set(context, ctx)

        mmat = manipulatormatrix.ManipulatorMatrix(context,
                                                   use_normalized=False)
        if ctx:
            st.context_py_dict_set(context, ctx_bak)

        mmat.orientation = self.orientation
        i = 'XYZ'.index(self.axis_from)
        j = 'XYZ'.index(self.axis_to)
        orientation.matrix.col[j] = mmat.col[i].to_3d()
        return {'FINISHED'}


class OperatorAxisMenu(bpy.types.Operator):
    bl_idname = 'transfomr.oe_axis_menu'
    bl_label = 'Orientation Axis Menu'
    bl_description = 'Paste from transform orientation axis'
    bl_options = {'REGISTER', 'INTERNAL'}

    axis = bpy.props.EnumProperty(
        name='Axis',
        items=[('X', 'X', ''),
               ('Y', 'Y', ''),
               ('Z', 'Z', '')],
    )

    def invoke(self, context, event):
        gen_paste_from_menus(context)

        menus = [MenuAxisX,
                 MenuAxisY,
                 MenuAxisZ]
        i = 'XYZ'.index(self.axis)
        bpy.ops.wm.call_menu(name=menus[i].bl_idname)
        return {'FINISHED'}


class MenuNormalize(bpy.types.Menu):
    bl_label = 'Normalize'
    bl_idname = 'VIEW3D_MT_toe_normalize'

    def draw(self, context):
        layout = self.layout
        orders = ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX']
        for order in orders:
            op = layout.operator(OperatorNormalize.bl_idname,
                                 text=order)
            op.axes = order


class MenuPasteFrom(bpy.types.Menu):
    bl_label = 'Paste From'
    bl_idname = 'VIEW3D_MT_toe_paste_from'

    def draw(self, context):
        layout = self.layout

        prop = bpy.types.SpaceView3D.bl_rna.properties['transform_orientation']
        for enum_item in prop.enum_items:
            op = layout.operator(OperatorPasteFrom.bl_idname,
                                 text=enum_item.name)
            op.orientation = enum_item.identifier

        layout.separator()

        for transform_orientation in context.scene.orientations:
            name = transform_orientation.name
            op = layout.operator(OperatorPasteFrom.bl_idname, text=name)
            op.orientation = name


class MenuMain(bpy.types.Menu):
    bl_label = 'Orientation Menu'
    bl_idname = 'VIEW3D_MT_toe_main'

    def draw(self, context):
        layout = self.layout
        if 1:
            layout.menu(MenuNormalize.bl_idname)
        elif 2:
            layout.operator_enum(OperatorNormalize.bl_idname, 'axes')
        else:
            orders = ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX']
            for order in orders:
                op = layout.operator(OperatorNormalize.bl_idname,
                                     text='Normalize ' + order)
                op.axes = order
        layout.separator()

        layout.menu(MenuPasteFrom.bl_idname)


class _MenuAxis:
    bl_idname = 'VIEW3D_MT_toe_axis_'
    bl_label = ''
    axis = ''

    def draw(self, context):
        layout = self.layout
        i = 'XYZ'.index(self.axis)

        # Normalize
        op = layout.operator(OperatorAxisNormalize.bl_idname,
                             text='Normalize')
        op.axis = self.axis

        # Up
        col = layout.column()
        op = col.operator(OperatorAxisMove.bl_idname,
                          text='Move Up')
        if i == 0:
            col.enabled = False
        else:
            op.axes = 'XYZ'[i - 1] + 'XYZ'[i]

        # Down
        col = layout.column()
        op = col.operator(OperatorAxisMove.bl_idname,
                          text='Move Down')
        if i == 2:
            col.enabled = False
        else:
            op.axes = 'XYZ'[i] + 'XYZ'[i + 1]

        # Copy
        op = layout.operator(OperatorAxisCopy.bl_idname,
                             text='Copy')
        op.axis = self.axis

        # Paste
        menus = [MenuAxisXPaste,
                 MenuAxisYPaste,
                 MenuAxisZPaste]
        layout.menu(menus[i].bl_idname, text='Paste')

        # Paste from
        menus = [MenuAxisXPasteFrom,
                 MenuAxisYPasteFrom,
                 MenuAxisZPasteFrom]
        layout.menu(menus[i].bl_idname, text='Paste from')


class MenuAxisX(
        _MenuAxis, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_x'
    bl_label = 'X Axis'
    axis = 'X'


class MenuAxisY(
        _MenuAxis, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_y'
    bl_label = 'Y Axis'
    axis = 'Y'


class MenuAxisZ(
        _MenuAxis, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_z'
    bl_label = 'Z Axis'
    axis = 'Z'


class _ManuAxisPaste(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_paste'
    bl_label = 'Paste'
    axis = ''

    def draw(self, context):
        layout = self.layout
        for i, (name, value) in enumerate(copied_axis_values):
            op = layout.operator(OperatorAxisPaste.bl_idname,
                                 text=name)
            op.axis = self.axis
            op.index = i


class MenuAxisXPaste(
        _ManuAxisPaste, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_paste_x'
    axis = 'X'


class MenuAxisYPaste(
        _ManuAxisPaste, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_paste_y'
    axis = 'Y'


class MenuAxisZPaste(
        _ManuAxisPaste, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_paste_z'
    axis = 'Z'


def gen_paste_from_menus(context):
    def gen_menu(identifier, lable, axis):
        class Menu(bpy.types.Menu):
            bl_idname = ('VIEW3D_MT_toe_axis_paste_from_' +
                         identifier + '_' + axis)
            bl_label = lable

            def draw(self, context):
                layout = self.layout
                for ax in 'XYZ':
                    op = layout.operator(OperatorAxisPasteFrom.bl_idname,
                                         text=ax)
                    op.orientation = identifier
                    op.axis_from = ax
                    op.axis_to = axis.upper()

        bpy.utils.register_class(Menu)
        dynamic_menus[(identifier, axis)] = Menu

    dynamic_menus.clear()
    prop = bpy.types.SpaceView3D.bl_rna.properties['transform_orientation']
    for axis in 'XYZ':
        for enum_item in prop.enum_items:
            if (enum_item.identifier, axis) not in dynamic_menus:
                gen_menu(enum_item.identifier, enum_item.name, axis)
        for transform_orientation in context.scene.orientations:
            if (transform_orientation.name, axis) not in dynamic_menus:
                gen_menu(transform_orientation.name,
                         transform_orientation.name, axis)


class _MenuAxisPasteFrom:
    bl_idname = 'VIEW3D_MT_toe_axis_paste_from'
    bl_label = 'Paste From'
    axis = ''

    def draw(self, context):
        layout = self.layout

        prop = bpy.types.SpaceView3D.bl_rna.properties['transform_orientation']
        for enum_item in prop.enum_items:
            menu = dynamic_menus[(enum_item.identifier, self.axis)]
            layout.menu(menu.bl_idname)

        layout.separator()

        for transform_orientation in context.scene.orientations:
            menu = dynamic_menus[(transform_orientation.name, self.axis)]
            layout.menu(menu.bl_idname)


class MenuAxisXPasteFrom(_MenuAxisPasteFrom, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_paste_from_x'
    bl_label = 'Paste From'
    axis = 'X'


class MenuAxisYPasteFrom(_MenuAxisPasteFrom, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_paste_from_y'
    bl_label = 'Paste From'
    axis = 'Y'


class MenuAxisZPasteFrom(_MenuAxisPasteFrom, bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_toe_axis_paste_from_z'
    bl_label = 'Paste From'
    axis = 'Z'


def draw_func(self, context):
    layout = self.layout.column()
    scene = context.scene
    v3d = context.space_data
    orientation = v3d.current_orientation
    if orientation is None:
        return

    row = layout.row()
    row.prop(scene, PROP_SHOW_ATTR, text='Details')

    if not getattr(scene, PROP_SHOW_ATTR):
        return

    row.operator(OperatorMenu.bl_idname, text='', icon='COLLAPSEMENU')

    for i, axis in enumerate('XYZ'):
        column = layout.column()
        row = column.row()
        row.label(axis + ':')
        sub_row = row.row(align=True)

        op = sub_row.operator(OperatorAxisInvert.bl_idname,
                              text='', icon='ZOOMOUT')
        op.axis = axis

        op = sub_row.operator(
            OperatorAxisFromNormal.bl_idname,
            text='', icon='VERTEXSEL')
        op.axis = axis

        op = sub_row.operator(OperatorAxisMenu.bl_idname, text='',
                              icon='COLLAPSEMENU')
        op.axis = axis

        # 数値
        row = column.row()
        col = row.column()
        attr = PROP_AXIS_ATTR + '_' + axis.lower()
        col.prop(scene, attr, text='')


def add_properties():
    for i, axis in enumerate('xyz'):
        def gen(i, axis):
            def fget(self):
                area = bpy.context.area
                if area and area.type == 'VIEW_3D':
                    v3d = area.spaces.active
                    trans_orient = v3d.current_orientation
                    if trans_orient is not None:
                        return trans_orient.matrix.col[i][:3]
                return 0.0, 0.0, 0.0

            def fset(self, value):
                area = bpy.context.area
                if area and area.type == 'VIEW_3D':
                    v3d = area.spaces.active
                    orientation = v3d.current_orientation
                    if orientation is not None:
                        orientation.matrix.col[i][:3] = value

            return fget, fset

        fget, fset = gen(i, axis)
        prop = bpy.props.FloatVectorProperty(
            name=axis,
            size=3,
            subtype='XYZ',
            get=fget,
            set=fset)
        attr = PROP_AXIS_ATTR + '_' + axis
        setattr(bpy.types.Scene, attr, prop)

    # show
    def fget(self):
        return show_transform_orientation_details

    def fset(self, value):
        global show_transform_orientation_details
        show_transform_orientation_details = value

    def update(self, context):
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

    prop = bpy.props.BoolProperty(
        name='Details', description='Show orientation matrix',
        get=fget, set=fset, update=update
    )
    setattr(bpy.types.Scene, PROP_SHOW_ATTR, prop)


def delete_properties():
    for i, axis in enumerate('xyz'):
        attr = PROP_AXIS_ATTR + '_' + axis
        delattr(bpy.types.Scene, attr)
    delattr(bpy.types.Scene, PROP_SHOW_ATTR)


dynamic_menus = {}

classes = [
    TransformOrientationEditorPreferences,

    OperatorNormalize,
    OperatorPasteFrom,
    OperatorMenu,

    OperatorAxisInvert,
    OperatorAxisFromNormal,
    OperatorAxisNormalize,
    OperatorAxisMove,
    OperatorAxisCopy,
    OperatorAxisPaste,
    OperatorAxisPasteFrom,
    OperatorAxisMenu,

    MenuNormalize,
    MenuPasteFrom,
    MenuMain,

    MenuAxisX,
    MenuAxisY,
    MenuAxisZ,
    MenuAxisXPaste,
    MenuAxisYPaste,
    MenuAxisZPaste,
    MenuAxisXPasteFrom,
    MenuAxisYPasteFrom,
    MenuAxisZPasteFrom,
]


@TransformOrientationEditorPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    add_properties()
    bpy.types.VIEW3D_PT_transform_orientations.append(draw_func)

    bpy.app.translations.register(__name__, translation_dict)


@TransformOrientationEditorPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    for cls in dynamic_menus.values():
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_PT_transform_orientations.remove(draw_func)
    delete_properties()

    bpy.app.translations.unregister(__name__)


if __name__ == '__main__':
    register()
