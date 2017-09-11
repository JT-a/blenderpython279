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
    'name': 'Boolean Utils',
    'author': 'chromoly',
    'version': (0, 0, 2),
    'blender': (2, 78, 0),
    'location': 'View3D',
    'description': '',
    'wiki_url': '',
    'category': '3D View',
}


import math

import bpy
import bmesh
from mathutils import Matrix

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(vaoperator)
    importlib.reload(vaprops)
    importlib.reload(wrapoperator)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import vaoperator
    from ..utils import vamath as vam
    from ..utils import vaprops
    from ..utils import vaview3d as vav
    from ..utils import wrapoperator


translation_dict = {
    'ja_JP': {
        ('*', 'String'): '文字列',
    }
}


class Preferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__


class OperatorKnifeProjectPlus(vaoperator.OperatorTemplate,
                               bpy.types.Operator):
    bl_idname = 'mesh.knife_project_plus'
    bl_label = 'Knife Project Plus'
    bl_options = {'REGISTER', 'UNDO'}

    mode = bpy.props.EnumProperty(
        name='Mode',
        items=(('OBJECTS', 'Objects', 'Selected Objects'),
               ('SELECTED', 'Selected', 'Selected Elements')),
        default='OBJECTS',
    )
    cut_through = bpy.props.BoolProperty(
        name='Cut through',
        description='Cut through all faces, not just visible ones'
    )
    elements = bpy.props.EnumProperty(
        name='Elements',
        items=(('BOUNDARY', 'Boundary', ''),
               ('EDGE', 'Edge', '')),
        default='BOUNDARY'
    )
    use_add_elements = bpy.props.BoolProperty(
        name='Add elements',
        description='Instead of subdivision'
    )
    keep_selection = bpy.props.BoolProperty(
        name='Keep Selection',
    )

    @classmethod
    def poll(self, context):
        return context.area.type == 'VIEW_3D'

    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        props = self.as_keywords()
        for attr, value in props.items():
            col = layout.column()
            if self.mode == 'OBJECTS':
                if attr in ('elements', 'use_add_elements', 'use_add_elements',
                            'keep_selection'):
                    col.active = False
            if attr in ('mode', 'elements'):
                self.draw_property(attr, col, row=True, expand=True)
            else:
                self.draw_property(attr, col)

    def execute(self, context):
        if self.mode == 'OBJECTS':
            try:
                bpy.ops.mesh.knife_project(self.cut_through)
            except RuntimeError as err:
                self.report({'ERROR'}, err.args[0])
            return {'FINISHED'}

        v3d = context.space_data
        scene = context.scene
        actob = context.active_object
        me = actob.data
        selected_objects = [ob for ob in context.selected_objects
                            if ob != actob]

        if me.total_edge_sel + me.total_face_sel == 0:
            return {'FINISHED'}

        bm = bmesh.from_edit_mesh(me)

        if self.elements == 'BOUNDARY':
            for e in bm.edges:
                if e.select and (e.is_boundary or e.is_wire):
                    break
            else:
                return {'FINISHED'}

        actob_select = actob.select
        actob.select = True
        for ob in selected_objects:
            ob.select = False

        def disable_modifiers(ob):
            for src, dst in zip(actob.modifiers, ob.modifiers):
                if src.show_viewport:
                    if not (src.show_in_editmode and src.show_on_cage):
                        dst.show_viewport = False

        me = actob.data
        bm = bmesh.from_edit_mesh(me)
        vert_layer = bm.verts.layers.int.new('tmp_flag')
        edge_layer = bm.edges.layers.int.new('tmp_flag')
        face_layer = bm.faces.layers.int.new('tmp_flag')

        # set layer flag
        for v in bm.verts:
            v[vert_layer] = int(v.select)
        # edge_verts = {}
        for e in bm.edges:
            e[edge_layer] = int(e.select)
        #     edge_verts[e] = tuple(e.verts)
        for f in bm.faces:
            f[face_layer] = int(f.select)

        bmesh.update_edit_mesh(me)

        if self.use_add_elements:
            bpy.ops.object.mode_set(toggle=True)
            bpy.ops.object.duplicate()
            actob_bak = [ob for ob in context.selected_objects
                         if ob != actob][0]
            actob_bak.select = False
            scene.objects.active = actob
            actob.select = True
            bpy.ops.object.mode_set(toggle=True)

            bm = bmesh.from_edit_mesh(me)
            vert_layer = bm.verts.layers.int.new('tmp_flag')
            edge_layer = bm.edges.layers.int.new('tmp_flag')
            face_layer = bm.faces.layers.int.new('tmp_flag')

        verts = [v for v in bm.verts if v.select]
        edges = [e for e in bm.edges if e.select]
        faces = [f for f in bm.faces if f.select]
        if self.elements == 'BOUNDARY':
            elems = verts + edges + faces
        else:
            elems = verts + edges
        ret = bmesh.ops.duplicate(bm, geom=elems)
        bpy.ops.mesh.select_all(action='DESELECT')
        for elem in ret['geom']:
            elem.select = True
        # bmesh.update_edit_mesh(me)
        bpy.ops.mesh.separate(type='SELECTED')
        for elem in elems:
            elem.select = True
        knife_object = [ob for ob in context.selected_objects
                        if ob != actob][0]
        knife_object.select = False
        disable_modifiers(knife_object)

        for ob in selected_objects:
            ob.select = False
        knife_object.select = True
        bpy.ops.mesh.hide(unselected=False)
        # scene.tool_settings.mesh_select_mode[1] = True
        bpy.ops.mesh.knife_project(cut_through=self.cut_through)
        knife_object.select = False

        # unhide
        for v in bm.verts:
            if v[vert_layer]:
                v.hide = False
        for e in bm.edges:
            if e[edge_layer]:
                e.hide = False
        for f in bm.faces:
            if f[face_layer]:
                f.hide = False

        if self.elements == 'EDGE':
            # mode = scene.tool_settings.mesh_select_mode
            # bpy.ops.mesh.select_all(action='DESELECT')
            for e in bm.edges:
                # bpy.ops.mesh.knife_project()では結果がedgeとfaceのtagに
                # 代入される
                if not e.tag:
                    e.select = True
            bm.select_flush(True)
            if not scene.tool_settings.mesh_select_mode[1]:
                for e in bm.edges:
                    if e.select:
                        for f in e.link_faces:
                            if f.select:
                                break
                        else:
                            e.select = False
                # 非選択になってしまった頂点を戻す
                for e in bm.edges:
                    if e.select:
                        e.select = True
            # bm.select_flush_mode()

        if self.use_add_elements:
            sel_num = me.total_vert_sel + me.total_edge_sel + me.total_face_sel
            if sel_num:
                # 現在の座標で新規頂点に shape key に適用させる。
                # やらないと [0.0, 0.0, 0.0] になる
                bpy.ops.object.mode_set(toggle=True)
                bpy.ops.object.mode_set(toggle=True)

                # vertex parent がある場合、頂点を消して親となる頂点インデックス
                # が不正な値の状態で処理を続けると、(editmodeを抜ける段階で？)
                # その頂点インデックスが変更されてしまうので注意

                bm = bmesh.from_edit_mesh(me)
                vnum_all = len(bm.verts)
                enum_all = len(bm.edges)
                fnum_all = len(bm.faces)
                verts = [v for v in bm.verts if v.select]
                edges = [e for e in bm.edges if e.select]
                faces = [f for f in bm.faces if f.select]
                elems = verts + edges + faces
                ret = bmesh.ops.duplicate(bm, geom=elems)
                bmesh.update_edit_mesh(me)

                bpy.ops.mesh.reveal()
                bpy.ops.mesh.select_all(action='SELECT')

                bpy.ops.object.mode_set(toggle=True)
                for v in actob_bak.data.vertices:
                    v.select = False
                for e in actob_bak.data.edges:
                    e.select = False
                for f in actob_bak.data.polygons:
                    f.select = False
                vnum_bak = len(actob_bak.data.vertices)
                enum_bak = len(actob_bak.data.edges)
                fnum_bak = len(actob_bak.data.polygons)
                actob_bak.select = True
                bpy.ops.object.join()
                bpy.ops.object.mode_set(toggle=True)

                bm = bmesh.from_edit_mesh(me)
                verts = bm.verts[vnum_bak: vnum_bak + vnum_all]
                edges = bm.edges[enum_bak: enum_bak + enum_all]
                faces = bm.faces[fnum_bak: fnum_bak + fnum_all]
                elems = verts + edges + faces
                bmesh.ops.delete(bm, geom=elems, context=1)

                bmesh.update_edit_mesh(me)

            elif self.use_add_elements:
                bpy.data.meshes.remove(actob_bak.data, True)

        bm = bmesh.from_edit_mesh(me)
        vert_layer = bm.verts.layers.int.get('tmp_flag')
        edge_layer = bm.edges.layers.int.get('tmp_flag')
        face_layer = bm.faces.layers.int.get('tmp_flag')

        if self.keep_selection:
            bpy.ops.mesh.select_all(action='DESELECT')
            for v in bm.verts:
                if v[vert_layer]:
                    v.select = True
            for e in bm.edges:
                if e[edge_layer]:
                    e.select = True
            for f in bm.faces:
                if f[face_layer]:
                    f.select = True

        if vert_layer:
            bm.verts.layers.int.remove(vert_layer)
        if edge_layer:
            bm.edges.layers.int.remove(edge_layer)
        if face_layer:
            bm.faces.layers.int.remove(face_layer)

        bpy.data.meshes.remove(knife_object.data, True)

        actob.select = actob_select
        for ob in selected_objects:
            ob.select = True

        return {'FINISHED'}


class OperatorMeshIntersectPlus(vaoperator.OperatorTemplate,
                                bpy.types.Operator):
    bl_idname = 'mesh.intersect_plus'
    bl_label = 'Intersect (Knife) Plus'
    bl_options = {'REGISTER', 'UNDO'}

    mode = vaprops.bl_prop_to_py_prop(
        bpy.types.MESH_OT_intersect.bl_rna.properties['mode'])
    # separate_modeはuse_add_elementsが有効な時は無意味になる
    separate_mode = vaprops.bl_prop_to_py_prop(
        bpy.types.MESH_OT_intersect.bl_rna.properties['separate_mode'])
    use_add_elements = bpy.props.BoolProperty(
        name='Add elements',
        description='Instead of subdivision'
    )
    threshold = vaprops.bl_prop_to_py_prop(
        bpy.types.MESH_OT_intersect.bl_rna.properties['threshold'])

    @classmethod
    def poll(self, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        # self.test(context)
        # return {'FINISHED'}

        if not self.use_add_elements:
            bpy.ops.mesh.intersect(
                mode=self.mode, separate_mode=self.separate_mode,
                threshold=self.threshold)
            return {'FINISHED'}

        obj = context.active_object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        vert_layer = bm.verts.layers.int.new('tmp_flag')
        edge_layer = bm.edges.layers.int.new('tmp_flag')
        face_layer = bm.faces.layers.int.new('tmp_flag')
        face_index_layer = bm.faces.layers.int.new('tmp_index')

        # flag -> select: 1, hide: 1 <<1, original: 1 << 2
        for elems, layer in zip([bm.verts, bm.edges, bm.faces],
                                [vert_layer, edge_layer, face_layer]):
            for elem in elems:
                elem[layer] = elem.select | (elem.hide << 1)

        orig_verts = list(bm.verts)
        orig_edges = list(bm.edges)
        orig_faces = list(bm.faces)
        orig_elems = orig_verts + orig_edges + orig_faces
        ret = bmesh.ops.duplicate(bm, geom=orig_elems)
        for elems, layer in zip([orig_verts, orig_edges, orig_faces],
                                [vert_layer, edge_layer, face_layer]):
            for elem in elems:
                elem[layer] |= 1 << 2

        for i, f in enumerate(bm.faces):
            f[face_index_layer] = i

        # hideはコピーするがselectはコピーしないクソ仕様
        for elem in orig_faces:
            elem_ = ret['face_map'][elem]
            elem_.select = elem.select
            elem_.hide = elem.hide
        for elem in orig_edges:
            elem_ = ret['edge_map'][elem]
            elem_.select = elem.select
            elem_.hide = elem.hide
        for elem in orig_verts:
            elem_ = ret['vert_map'][elem]
            elem_.select = elem.select
            elem_.hide = elem.hide

        # オリジナルを全部隠す
        for elem in orig_elems:
            elem.select = False
            elem.hide = True

        # context.scene.tool_settings.mesh_select_mode = [False, True, False]
        select_mode = bm.select_mode
        bm.select_mode = {'EDGE'}
        bmesh.update_edit_mesh(mesh)

        verts = list(bm.verts)
        edges = list(bm.edges)
        faces = list(bm.faces)
        if self.mode == 'SELECT_UNSELECT':
            bpy.ops.mesh.intersect_boolean(
                operation='INTERSECT', use_swap=False,
                threshold=self.threshold)
        else:
            bpy.ops.mesh.intersect(
                mode='SELECT', separate_mode='CUT', threshold=self.threshold)
        if (list(bm.verts) == verts and list(bm.edges) == edges and
                list(bm.faces) == faces):
            non_delete_elems = set(orig_elems)
            delete_verts = []
            for v in bm.verts:
                if v not in non_delete_elems:
                    delete_verts.append(v)
            bmesh.ops.delete(bm, geom=delete_verts, context=1)
            restore_select = True
        else:
            # self.mode が 'SELECT' の場合はソースに修正を加えていないと駄目
            isect_edges = [e for e in bm.edges if e.select]
            ret = bmesh.ops.duplicate(bm, geom=isect_edges)
            isect_duplicated = ret['geom']
            for elem in isect_duplicated:
                elem.select = True

            non_delete_elems = set(orig_elems + isect_duplicated)
            delete_verts = []
            for v in bm.verts:
                if v not in non_delete_elems:
                    delete_verts.append(v)
            bmesh.ops.delete(bm, geom=delete_verts, context=1)
            restore_select = False

        bm.select_mode = select_mode

        # オリジナルを元に戻す
        for elems, layer in zip([orig_verts, orig_edges, orig_faces],
                                [vert_layer, edge_layer, face_layer]):
            for elem in elems:
                flag = elem[layer]
                if not (flag & 2):
                    elem.hide = False
                if restore_select:
                    if flag & 1:
                        elem.select = True

        bm.verts.layers.int.remove(vert_layer)
        bm.edges.layers.int.remove(edge_layer)
        bm.faces.layers.int.remove(face_layer)

        bmesh.update_edit_mesh(mesh)

        return {'FINISHED'}


class Menu(bpy.types.Menu):
    bl_idname = 'MESH_MT_intersect_boolean'
    bl_label = 'Knife & Boolean'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('mesh.knife_tool')
        # layout.operator('mesh.knife_project')
        layout.operator(OperatorKnifeProjectPlus.bl_idname,
                        text='Knife Project')
        layout.separator()

        # layout.operator('mesh.intersect')
        layout.operator(OperatorMeshIntersectPlus.bl_idname,
                        text='Intersect (Knife)')
        layout.separator()

        op = layout.operator('mesh.intersect_boolean', text='Intersect')
        op.operation = 'INTERSECT'
        op = layout.operator('mesh.intersect_boolean', text='Union')
        op.operation = 'UNION'
        op = layout.operator('mesh.intersect_boolean', text='Difference')
        op.operation = 'DIFFERENCE'


class PasteObject(bpy.types.Operator):
    """
    invokeでactiveobjectを複製
    modal中でスナップ、クリックで位置確定、その後、回転とスケール、クリックで確定。
    継続するならアクティブオブジェクトをまた複製
    キャンセルで複製したオブジェクトを削除。


    """
    bl_idname = 'object.paste'
    bl_label = 'Paste Object'
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR', 'BLOCKING'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def view_axis(self, context, mco):
        """手前から奥に向かうベクトル"""
        region = context.region
        rv3d = context.region_data

        near = vav.unproject(region, rv3d, (*mco, 0.01))
        far = vav.unproject(region, rv3d, (*mco, 1.0))
        return (far - near).normalized()

    def ray_cast(self, context, event):
        """
        :type context: bpy.types.Context
        :type event: bpy.types.Event
        """
        mco = event.mouse_region_x, event.mouse_region_y
        region = context.region
        rv3d = context.region_data

        origin = vav.unproject(region, rv3d, (*mco, 0.01))
        direction = self.view_axis(context, mco)

        self.actob.hide = True
        self.dupliob.hide = True
        # (result, location, normal, index, object, matrix)
        result = context.scene.ray_cast(origin, direction)
        self.actob.hide = False
        self.dupliob.hide = False
        return result

    def pixel_size(self, context):
        """1 pixel 分の blender unit を返す"""
        # unitsystem.pyより
        rv3d = context.region_data
        if rv3d is None:
            return None
        region = context.region
        sx, sy = region.width, region.height
        view_location = rv3d.view_location
        persmat = rv3d.perspective_matrix

        v1 = persmat[0].to_3d()
        v2 = persmat[1].to_3d()
        len_px = 2.0 / min(v1.length, v2.length)
        len_sc = max(sx, sy)
        pixsize = len_px / len_sc

        def mul_project_m4_v3_zfac(mat, co):
            return ((mat.col[0][3] * co[0]) + (mat.col[1][3] * co[1]) + (
                mat.col[2][3] * co[2]) + mat.col[3][3])

        def ED_view3d_pixel_size(mat, co):
            return mul_project_m4_v3_zfac(mat, co) * pixsize * 1.0

        pixel_size = ED_view3d_pixel_size(persmat, view_location)

        return pixel_size

    def modal(self, context, event):
        """
        :type context: bpy.types.Context
        :type event: bpy.types.Event
        """
        pixel_size = self.pixel_size(context)

        mco = event.mouse_region_x, event.mouse_region_y

        def calc_mat(mco):
            _, location, normal, index, obj, matrix = self.result

            mat = Matrix.Identity(3)
            mat.col[2] = normal
            mvec_near = vav.unproject(context.region, context.region_data,
                                 (*mco, 0.01))
            direction = self.view_axis(context, mco)
            mvec_far = mvec_near + direction
            plane = vam.PlaneVector(location, normal)
            isect = plane.intersect(mvec_near, mvec_far)
            mat.col[0] = (isect - location).normalized()
            mat.col[1] = (mat.col[2].cross(mat.col[0])).normalized()
            mat = mat.to_4x4()
            mat.col[3][:3] = location
            return mat

        if not self.mco:
            # result, location, normal, index, obj, matrix
            result = self.ray_cast(context, event)
            if result[0]:
                self.result = result
                mat = calc_mat((mco[0] + 10, mco[1]))
                self.dupliob.matrix_world = mat

        if event.type in {'MOUSEMOVE'}:
            if self.mco:
                # 回転、拡大縮小。右方向が回転の初期値
                x = mco[0] - self.mco[0]
                y = mco[1] - self.mco[1]
                # angle = math.atan2(y, x)

                mat = calc_mat(mco)
                px_scale = math.sqrt(x ** 2 + y ** 2)
                dim = self.actob.dimensions[0]
                scale = px_scale * pixel_size / dim * 2
                m = Matrix.Scale(scale, 4)
                self.dupliob.matrix_world = mat * m

        if event.type in {'LEFTMOUSE'}:
            if event.value == 'PRESS':
                self.dupliob.draw_type = 'TEXTURED'
                self.mco = mco
            elif event.value == 'RELEASE':
                self.dupliob.select = False
                self.duplicate_object(context)
                self.mco = None

        elif event.type in {'SPACE', 'RET', 'PADENTER'}:
            if event.value == 'PRESS':
                if not self.mco:
                    self.cancel(context)
                return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            if event.value == 'PRESS':
                self.cancel(context)
                return {'CANCELLED'}

        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def cancel(self, context):  # これ明示的に呼び出さないと駄目だっけ？
        # dupliobを消す
        objects = [ob for ob in context.selected_objects
                   if ob != self.dupliob]
        for ob in objects:
            ob.select = False
        self.dupliob.select = True
        bpy.ops.object.delete()
        for ob in objects:
            ob.select = True
        self.actob.select = True
        context.scene.objects.active = self.actob

    def duplicate_object(self, context):
        objects = context.selected_objects
        for ob in objects:
            ob.select = False
        self.actob.select = True
        bpy.ops.object.duplicate()
        self.dupliob = context.selected_objects[0]
        context.scene.objects.active = self.dupliob
        for ob in objects:
            ob.select = True
        self.actob.select = False

        self.dupliob.draw_type = 'WIRE'

    def invoke(self, context, event):
        self.mco = None
        self.actob = self.dupliob = None
        self.result = None

        self.actob = context.active_object
        self.duplicate_object(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


classes = [
    Preferences,
    OperatorKnifeProjectPlus,
    OperatorMeshIntersectPlus,
    Menu,
    # PasteObject,
]


@Preferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.translations.register(__name__, translation_dict)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = Preferences.get_keymap('Mesh')
        kmi = km.keymap_items.new('wm.call_menu', 'B', 'PRESS',
                                  shift=True, ctrl=True, alt=True)
        kmi.properties.name = Menu.bl_idname


@Preferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)


if __name__ == '__main__':
    register()
