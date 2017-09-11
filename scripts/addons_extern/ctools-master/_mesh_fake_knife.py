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
    'name': 'BMesh Fake Knife',
    'author': 'chromoly',
    'version': (0, 1, 1),
    'blender': (2, 78, 0),
    'location': 'View3D',
    'category': 'Mesh'}


import math

import bpy
from mathutils import Vector
import mathutils.geometry as geo
import bgl
import blf
import bmesh

from .utils import addongroup
from .utils import vaview3d as vav
from .utils import vagl as vagl
from .utils import vabmesh as vabm
from .utils import unitsystem


MIN_NUMBER = 1E-8
THRESHOLD = 1E-5  # これより小さい値を同座標とみなす
NONE = "instead_of_None"  # 引数の初期値にNoneが使えない場合に


"""
def mul_persp_np(pmat, arr):
    num = arr.shape[0]
    if pmat.shape[1] == 4 and arr.shape[1] == 3:
        zvalues = np.ones(num).reshape(num, -1)
        arr = np.hstack(arr, zvalues)
    result = arr.dot(pmat.transpose())
    # result.base
    return 
"""


def flatten_matrix(mat):
    # 1dの場合は列優先にする
    m = []
    for col in range(len(mat.col)):
        for row in range(len(mat.row)):
            m.append(mat[row][col])
    return m


def mul_persp(pmat, vec):
    v = pmat * vec.to_4d()
    if v[3] != 0:
        v /= v[3]
    return v.to_3d()


def cross(v1, v2):
    if len(v1) == 2 or len(v2) == 2:
        return v1.x * v2.y - v1.y * v2.x
    else:
        return v1.cross(v2)


class PolyLine:
    """
    ナイフ切断用
    """
    def __init__(self, face, vert, point_coords=None):
        self.face = face  # 処理対象の面
        self.vert = vert  # ここからpointsが伸びる
        
        if point_coords is None:
            self.point_coords = []  # Vector: world co
        else:
            self.point_coords = list(point_coords)  # Vector: world co
        self.point_index = 0
        self.coords = []  # Vector: local co
        self.is_valid = True
        #self.log = []  # tri and loop pair
    
    def clear(self):
        self.point_index = 0
        self.coords[:] = []
        #self.log[:] = []
        
    def copy(self):
        polyline = self.__class__(self.face, self.vert, self.point_coords)
        polyline.point_index = self.point_index
        polyline.coords = [v.copy() for v in self.coords]
        polyline.is_valid = self.is_valid
        #polyline.log = self.log[:]
        return polyline
        

def isect_point_line_v2(v, p1, p2, threshold=THRESHOLD):
    """vがp1-p2線分上に有るか判定。もしそうなら線分上の座標を返す。
    v1とp1(p2)との距離がより小さいならのp1(p2)の座標を返す。
    """
    p1_p2 = p2 - p1
    if p1_p2.length == 0.0:
        if (p1 - v).length < threshold:
            return p1.copy()
        else:
            return None
    dist_hor = p1_p2.dot(v - p1) / p1_p2.length  # hor = horizontal
    dist_ver = cross(p1_p2, v - p1) / p1_p2.length  # ver = vertical
    if abs(dist_ver) < threshold:
        if (p1 - v).length < threshold:
            return p1.copy()
        elif (p2 - v).length < threshold:
            return p2.copy()
        elif 0 <= dist_hor <= p1_p2.length:
            return (v - p1).project(p1_p2) + p1
    return None


def isect_line_line_v2(v1, v2, p1, p2, threshold=THRESHOLD):
    """v1-v2の線分を基準としてp1-p2の線分との交差判定を行う。
    v1-v2かp1-p2の長さが0の場合は交差しないとする。
    thresholdより小さい値を要素が重なっているとみなす。
    交点とv1(v2)との距離がthreshold以下なら、その値はv1(v2)を複製する。
    
    return: 線分同士の交点, 平行な場合のv1-v2とp1の交点, 平行な場合のv1-v2とp2の交点
    """
    v1_v2 = v2 - v1
    p1_p2 = p2 - p1
    
    if (v1_v2).length < threshold or (p1_p2).length < threshold:
        return None, None, None
    
    p1disthor = v1_v2.dot(p1 - v1) / v1_v2.length
    p1distver = cross(v1_v2, p1 - v1) / v1_v2.length
    p2disthor = v1_v2.dot(p2 - v1) / v1_v2.length
    p2distver = cross(v1_v2, p2 - v1) / v1_v2.length
    
    ivec = ivec_p1 = ivec_p2 = None
    
    if abs(p1distver) < threshold and abs(p2distver) < threshold:
        # 線分が重なる
        # p1,p2がedgeの同一線上
        if (v1 - p1).length < threshold:
            ivec_p1 = v1.copy()
        elif (v2 - p1).length < threshold:
            ivec_p1 = v2.copy()
        elif 0 <= p1disthor <= v1_v2.length:
            # p1がv1-v2間 (頂点と重ならない)
            ivec_p1 = v1 + v1_v2.normalized() * p1disthor
        
        if (v1 - p2).length < threshold:
            ivec_p2 = v1.copy()
        elif (v2 - p2).length < threshold:
            ivec_p2 = v2.copy()
        elif 0 <= p2disthor <= v1_v2.length:
            # p2がv1-v2間 (頂点と重ならない)
            ivec_p2 = v1 + v1_v2.normalized() * p2disthor
    
    elif abs(p1distver - p2distver) < threshold:
        # 平行
        pass
    
    elif not (p1distver <= -threshold and p2distver <= -threshold or
            p1distver >= threshold and p2distver >= threshold):
        # p1,p2がv1-v2の片側に存在しない
        d1 = cross(v1_v2, v1 - p1) / v1_v2.length
        d2 = cross(v1_v2, p1_p2) / v1_v2.length
        ivec = p1 + p1_p2 / d2 * d1  # 直線としての交点
        
        vidisthor = v1_v2.dot(ivec - v1) / v1_v2.length
        if vidisthor <= -threshold or vidisthor >= v1_v2.length + threshold:
            # 線分の外
            ivec = None
        elif vidisthor < threshold:
            # v1付近で交差
            ivec = v1.copy()
        elif vidisthor > v1_v2.length - threshold:
            # v2付近で交差
            ivec = v2.copy()

    return ivec, ivec_p1, ivec_p2


def isect_point_tri_persp_to_world(perspective_matrix, point, p1, p2, p3,
                                   clip=True):
    """
    point:      透視投影座標。2d。3dの場合、zは無視される。
    p1, p2, p3: 透視東映座標。3d
    pointから画面に垂直に伸びる直線との交差判定をworld座標で行う。
    返り値はworld座標。
    """
    pmat = perspective_matrix
    pimat = pmat.inverted()
    
    orig = mul_persp(pimat, Vector((point[0], point[1], -1.0)))
    tag = mul_persp(pimat, Vector((point[0], point[1], 0.5)))
    ray = tag - orig
    v1 = mul_persp(pimat, p1)
    v2 = mul_persp(pimat, p2)
    v3 = mul_persp(pimat, p3)
    ivec = geo.intersect_ray_tri(v1, v2, v3, ray, orig, clip)
    return ivec


class Point(bpy.types.PropertyGroup):
    co = bpy.props.FloatVectorProperty(
        name='Coordinate',
        description='World coordinate',
        subtype='XYZ',
        size=3)


class SnapObjects:
    """
    def __init__(self, context):
        self.snap_objects = SnapObjects(context)

    def modal(self, context, event):
        mval = event.mouse_region_x, event.mouse_region_y
        r = self.snap_objects.snap(context, mval, 'VERTEX')
        if r:
            # keys: 'location', 'normal', 'index', 'object'
            ...

        # mesh等が更新されたらキャッシュクリア
        self.snap_objects.update()

    """

    # enum SnapSelect
    SNAP_ALL = 0
    SNAP_NOT_SELECTED = 1
    SNAP_NOT_ACTIVE = 2

    SNAP_MIN_DISTANCE = 30

    SNAP_OBJECT_USE_CACHE = 1 << 0

    # tool_settings.snap_mode
    # SCE_SNAP_MODE_INCREMENT = 0
    SCE_SNAP_MODE_VERTEX = 1
    SCE_SNAP_MODE_EDGE = 2
    SCE_SNAP_MODE_FACE = 3
    # SCE_SNAP_MODE_VOLUME = 4
    # SCE_SNAP_MODE_NODE_X = 5
    # SCE_SNAP_MODE_NODE_Y = 6
    # SCE_SNAP_MODE_NODE_XY = 7
    # SCE_SNAP_MODE_GRID = 8

    BM_ELEM_SELECT = 1 << 0
    BM_ELEM_HIDDEN = 1 << 1

    def __init__(self, context=None):
        self.object_context = None
        if context:
            self.ensure(context)

    def __del__(self):
        self.free()

    def snap_object_context_create_view3d(self, context):
        import bpy
        import ctypes as ct
        cdll = ct.CDLL('')
        func = cdll.ED_transform_snap_object_context_create_view3d
        func.restype = ct.c_void_p

        # area = context.area
        # if not area:
        #     raise ValueError('context.areaがNone')
        # if area.type != 'VIEW_3D':
        #     raise ValueError("context.areaが3DViewではない")

        region = context.region
        if not region:
            raise ValueError('context.regionがNone')
        if region.type != 'WINDOW':
            raise ValueError("context.region.typeが'WINDOW'ではない")
        ar = ct.c_void_p(region.as_pointer())

        view3d = context.space_data
        if not isinstance(view3d, bpy.types.SpaceView3D):
            raise ValueError('context.space_dataがSpaceView3Dではない')
        v3d = ct.c_void_p(view3d.as_pointer())

        bl_main = ct.c_void_p(bpy.data.as_pointer())
        scn = ct.c_void_p(context.scene.as_pointer())
        object_context = func(bl_main, scn, self.SNAP_OBJECT_USE_CACHE, ar, v3d)
        return ct.c_void_p(object_context)

    def ensure(self, context):
        if not self.object_context:
            self.object_context = self.snap_object_context_create_view3d(
                context)

    def update(self, context):
        if self.object_context:
            self.free()
        self.object_context = self.snap_object_context_create_view3d(context)

    def free(self):
        # 開放前にcontext.modeを切り替えてはならない。落ちる。
        import ctypes as ct
        cdll = ct.CDLL('')
        if self.object_context:
            cdll.ED_transform_snap_object_context_destroy(self.object_context)
            self.object_context = None

    def set_editmesh_callbacks(self):
        # ED_transform_snap_object_context_set_editmesh_callbacks(
        #     object_context,
        #        (bool(*)(BMVert *, void *))
        # BM_elem_cb_check_hflag_disabled,
        # bm_edge_is_snap_target,
        # bm_face_is_snap_target,
        # SET_UINT_IN_POINTER((BM_ELEM_SELECT | BM_ELEM_HIDDEN)))

        import ctypes as ct
        cdll = ct.CDLL('')
        func = cdll.ED_transform_snap_object_context_set_editmesh_callbacks
        vfunc = ct.c_void_p(ct.addressof(cdll.BM_elem_cb_check_hflag_disabled))
        # FIXME: efunc,ffuncはstatucで参照出来ない為このコードは動かない
        efunc = ct.c_void_p(ct.addressof(cdll.bm_edge_is_snap_target))
        ffunc = ct.c_void_p(ct.addressof(cdll.bm_face_is_snap_target))

        user_data = ct.c_void_p(self.BM_ELEM_SELECT | self.BM_ELEM_HIDDEN)
        func(self.object_context, vfunc, efunc, ffunc, user_data)

    def create_python_object(self, id_addr, type_name, addr):
        """アドレスからpythonオブジェクトを作成する。
        area = create_python_object(C.screen.as_pointer(), 'Area',
                                    C.area.as_pointer())
        obj = create_python_object(C.active_object.as_pointer(), 'Object',
                                   C.active_object.as_pointer())

        :param id_addr: id_dataのアドレス。自身がIDオブジェクトならそれを指定、
            そうでないなら所属するIDオブジェクトのアドレスを指定する。
            AreaならScreen、ObjectならObjectのアドレスとなる。無い場合はNone。
            正しく指定しないと予期しない動作を起こすので注意。
        :type id_addr: int | None
        :param type_name: 型名。'Area', 'Object' 等。
            SpaceView3D等のSpaceのサブクラスは'Space'でよい。
        :type type_name: str
        :param addr: オブジェクトのアドレス。
        :type addr: int
        :rtype object
        """

        import ctypes as ct

        class _PointerRNA_id(ct.Structure):
            _fields_ = [
                ('data', ct.c_void_p),
            ]

        class PointerRNA(ct.Structure):
            _fields_ = [
                ('id', _PointerRNA_id),
                ('type', ct.c_void_p),  # StructRNA
                ('data', ct.c_void_p),
            ]

        if (not isinstance(id_addr, (int, type(None))) or
                not isinstance(type_name, str) or
                not isinstance(addr, int)):
            raise TypeError('引数の型が間違ってる。(int, str, int)')

        cdll = ct.CDLL('')
        RNA_pointer_create = cdll.RNA_pointer_create
        RNA_pointer_create.restype = None
        pyrna_struct_CreatePyObject = cdll.pyrna_struct_CreatePyObject
        pyrna_struct_CreatePyObject.restype = ct.py_object
        try:
            RNA_type = getattr(cdll, 'RNA_' + type_name)
        except AttributeError:
            raise ValueError("型名が間違ってる。'{}'".format(type_name))

        ptr = PointerRNA()
        RNA_pointer_create(ct.c_void_p(id_addr), RNA_type, ct.c_void_p(addr),
                           ct.byref(ptr))
        return pyrna_struct_CreatePyObject(ct.byref(ptr))

    def snap(self, context, mval, snap_element=None, snap_select='ALL',
             dist_px=SNAP_MIN_DISTANCE):
        import ctypes as ct
        from mathutils import Vector

        cdll = ct.CDLL('')

        if not self.object_context:
            self.ensure(context)

        mval = (ct.c_float * 2)(*mval)
        dist_px = ct.c_float(dist_px)
        r_loc = (ct.c_float * 3)()
        r_no = (ct.c_float * 3)()
        r_index = ct.c_int()
        r_ob = ct.c_void_p()
        actob = context.active_object

        class SnapObjectParams(ct.Structure):
            _fields_ = [
                ('snap_select', ct.c_char),
                ('use_object_edit_cage', ct.c_ubyte),  # unsigned int
            ]

        if snap_select not in {'ALL', 'NOT_SELECTED', 'NOT_ACTIVE'}:
            raise ValueError(
                "snap_select not in {'ALL', 'NOT_SELECTED', 'NOT_ACTIVE'}")
        d = {'ALL': self.SNAP_ALL,
             'NOT_SELECTED': self.SNAP_NOT_SELECTED,
             'SNAP_NOT_ACTIVE': self.SNAP_NOT_ACTIVE
             }
        snap_select = d[snap_select]
        params = SnapObjectParams(snap_select, actob and actob.mode == 'EDIT')

        # self.set_editmesh_callbacks()

        if snap_element:
            snap_mode = snap_element
        else:
            snap_mode = context.tool_settings.snap_element
        if snap_mode not in {'VERTEX', 'EDGE', 'FACE'}:
            if snap_element:
                raise ValueError(
                    "snap_element not in {'VERTEX', 'EDGE', 'FACE'}")
            else:
                return None
        d = {
            # 'INCREMENT': SCE_SNAP_MODE_INCREMENT,
            'VERTEX': self.SCE_SNAP_MODE_VERTEX,
            'EDGE': self.SCE_SNAP_MODE_EDGE,
            'FACE': self.SCE_SNAP_MODE_FACE,
            # 'VOLUME': SCE_SNAP_MODE_VOLUME,
        }
        snap_to = d[snap_mode]

        found = cdll.ED_transform_snap_object_project_view3d_ex(
            self.object_context, snap_to, ct.byref(params), mval,
            ct.byref(dist_px), None, r_loc, r_no, ct.byref(r_index),
            ct.byref(r_ob),
        )

        if found:
            ob = self.create_python_object(r_ob.value, 'Object', r_ob.value)
            return {'location': Vector(r_loc),
                    'normal': Vector(r_no),
                    'index': r_index.value,
                    'object': ob}
        else:
            return None


class MESH_OT_bm_fake_knife(bpy.types.Operator):
    bl_label = 'BMesh Fake Knife'
    bl_idname = 'mesh.bm_fake_knife'
    bl_description = 'Line knife'
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    # dir(points) >> ['__doc__', 'add', 'clear', 'move', 'remove']
    points = bpy.props.CollectionProperty(
        type=Point,
        options={'HIDDEN', 'SKIP_SAVE', 'ANIMATABLE'})
    perspective_matrix = bpy.props.FloatVectorProperty(
        name='Perspective Matrix',
        subtype='MATRIX',
        size=16,
        options={'HIDDEN', 'SKIP_SAVE', 'ANIMATABLE'})
    
    deselect = bpy.props.BoolProperty(
        name='Deselect',
        default=True)
    split_faces = bpy.props.BoolProperty(
        name='Split Faces',
        default=True)
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def draw_callback(self, context):
        if context.region != self.region:
            return
            
        box_size = 10
        circle_size = 12
        
        region = context.region
        rv3d = context.region_data
        
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        blf.position(0, 70, 30, 0)
        blf.draw(0, self.snap_type)
        
        # axis
        if self.axis is not None:
            blf.position(0, 70, 45, 0)
            blf.draw(0, str(math.degrees(self.axis)))
        
        bgl.glEnable(bgl.GL_BLEND)
        
        """# axis
        if self.axis is not None:
            v = vav.project(region, rv3d, self.points[-2])
            bgl.glColor4f(1.0, 1.0, 1.0, 0.5)
            bgl.glBegin(bgl.GL_LINE_STRIP)
            bgl.glVertex2f()
            bgl.glVertex2f()
            bgl.glEnd()
        """
        
        # snap
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        if self.snap_vector:
            v = vav.project(region, rv3d, self.snap_vector)
            if self.snap_grid:
                xmin = v[0] - box_size / 2
                ymin = v[1] - box_size / 2
                w = box_size
                h = box_size
                vagl.draw_box(xmin, ymin, w, h, poly=False)
            else:
                vagl.draw_circle(v[0], v[1], circle_size / 2, 16, poly=False)
        
        """# line
        bgl.glColor4f(1.0, 1.0, 1.0, 0.2)
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for point in self.points[:len(self.points) - 1]:  # [:-1]がバグってる
            bgl.glVertex2f(*vav.project(region, rv3d, point.co).to_2d())
        bgl.glEnd()
        """
        
        # line
        bgl.glColor4f(1.0, 1.0, 1.0, 0.2)
        for polyline in self.polylines:
            bgl.glBegin(bgl.GL_LINE_STRIP)
            for vec in polyline.point_coords:
                bgl.glVertex2f(*vav.project(region, rv3d, vec).to_2d())
            bgl.glEnd()
        
        # point
        x_size2 = 3
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        bgl.glBegin(bgl.GL_LINES)
        for polyline in self.polylines:
            for vec in polyline.point_coords[1:]:
                v = vav.project(region, rv3d, vec)
                bgl.glVertex2f(v[0] - x_size2, v[1] - x_size2)
                bgl.glVertex2f(v[0] + x_size2, v[1] + x_size2)
                bgl.glVertex2f(v[0] - x_size2, v[1] + x_size2)
                bgl.glVertex2f(v[0] + x_size2, v[1] - x_size2)
        bgl.glEnd()
        
        # current line
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for point in self.points[-2:]:
            bgl.glVertex2f(*vav.project(region, rv3d, point.co).to_2d())
        bgl.glEnd()

        # mouse
        cross_size = 10
        cross_ofs = 30
        mco = self.mco
        bgl.glColor4f(1.0, 1.0, 1.0, 0.7)
        bgl.glBegin(bgl.GL_LINES)
        bgl.glVertex2f(mco[0] + cross_ofs, mco[1])  # right
        bgl.glVertex2f(mco[0] + cross_ofs + cross_size, mco[1])
        bgl.glVertex2f(mco[0] - cross_ofs, mco[1])  # left
        bgl.glVertex2f(mco[0] - cross_ofs - cross_size, mco[1])
        bgl.glVertex2f(mco[0], mco[1] + cross_ofs)  # top
        bgl.glVertex2f(mco[0], mco[1] + cross_ofs + cross_size)
        bgl.glVertex2f(mco[0], mco[1] - cross_ofs)  # bottom
        bgl.glVertex2f(mco[0], mco[1] - cross_ofs - cross_size)
        bgl.glEnd()

    def persp_fac_to_world_fac(self, fac, inverted_perspective_matrix, v1, v2):
        """v1,v2はpersp座標"""
        v3 = v1 + (v2 - v1) * fac
        v4 = v3.copy()
        v3[2] = 0.0
        v4[2] = 0.5
        vec1 = mul_persp(inverted_perspective_matrix, v1)
        vec2 = mul_persp(inverted_perspective_matrix, v2)
        vec3 = mul_persp(inverted_perspective_matrix, v3)
        vec4 = mul_persp(inverted_perspective_matrix, v4)
        i1, i2 = geo.intersect_line_line(vec1, vec2, vec3, vec4)
        vec12 = vec2 - vec1
        return vec12.dot(i1 - vec1) / vec12.length ** 2

    def calc_verts_on_line(self, verts, p1, p2, threshold=THRESHOLD):
        # 頂点とp1-p2ラインとの交差判定
        verts_on_line = set()
        for eve in verts:
            v = self.persp_coords[eve].to_2d()
            if isect_point_line_v2(v, p1, p2, threshold):
                verts_on_line.add(eve)
        return verts_on_line

    def point_is_inside_of_tri(self, p, tri, threshold=THRESHOLD,
                               exclude_edges=False):
        """
        pがtriの中に含まれるか調べる。
        p:             2d persp coord
        exclude_edges: triの三辺上に来る場合は偽とする。
        """
        tri_vecs = [self.persp_coords[loop.vert].to_2d() for loop in tri]
        # 三角形の三辺上にくるか調べる
        for i in range(3):
            v1 = tri_vecs[i - 1]
            v2 = tri_vecs[i]
            if isect_point_line_v2(p, v1, v2, threshold):
                if exclude_edges:
                    return False
                else:
                    return True
        return bool(geo.intersect_point_tri_2d(p, *tri_vecs))

    def point_is_inside_of_tris(self, p, tris, threshold=THRESHOLD,
                                exclude_edges=False):
        """
        pがtrisの中に含まれるか調べる。
        p: 2d persp coord
        exclude_edges: trisの外周上に来る場合は偽とする。
        """
        edge_key_tris = tris.vert_pair_dict()
        for tri in tris:
            is_inside = self.point_is_inside_of_tri(p, tri, threshold)
            if is_inside and exclude_edges:
                for i in range(3):
                    eve1 = tri[i - 1].vert
                    eve2 = tri[i].vert
                    #ekey = tris.make_edge_key(eve1, eve2)
                    ekey = tris.hash_sorted((eve1, eve2))
                    if len(edge_key_tris[ekey]) == 1:  # 外周
                        v1 = self.persp_coords[eve1].to_2d()
                        v2 = self.persp_coords[eve2].to_2d()
                        if isect_point_line_v2(p, v1, v2, threshold):
                            is_inside = False
            if is_inside:
                return True
        return False
    
    def search_end_vert(self, context, pmat, polyline):
        # polylineで面を切るvertと、必要ならベクトルを求める

        obmat = context.active_object.matrix_world
        obimat = obmat.inverted()
        
        efa = polyline.face
        face_tris = vabm.LoopTris.from_faces([efa])
        face_tris.correct()
        vert_tris = face_tris.vert_dict()
        
        # 最後のpointが面の外ならこのループ以降判定しない
        p = mul_persp(pmat, polyline.point_coords[-1]).to_2d()
        if not self.point_is_inside_of_tris(p, face_tris):
            polyline.is_valid = False

        p1 = mul_persp(pmat, polyline.point_coords[0]).to_2d()
        p2 = mul_persp(pmat, polyline.point_coords[1]).to_2d()
        verts_on_line = self.calc_verts_on_line(efa.verts, p1, p2)
        
        end_vert = None
        
        for loop1 in efa.loops:
            if loop1.vert == polyline.vert:
                break
        
        for tri in vert_tris[loop1.vert]:
            #print('current tri', [l.vert.index for l in tri])
            polyline.clear()
            tri_loops_on_line = [loop for loop in tri if loop.vert in verts_on_line]
            
            if len(tri_loops_on_line) == 3:
                continue
            
            elif len(tri_loops_on_line) == 2:
                tri_loops_on_line.remove(loop1)
                end_vert = tri_loops_on_line[0].vert
                break
            
            i = tri.index(loop1)
            loop_pairs = [(tri[i - 2], tri[i - 1])]
            cnt = -1
            while True:
                cnt += 1
                if len(loop_pairs) != 1:  # 二巡目以降
                    #print('current tri', [l.vert.index for l in tri])
                    if tri_loops_on_line:
                        end_vert = tri_loops_on_line[0].vert
                        break
                for l2, l3 in loop_pairs:
                    """
                    while 一巡目   while 二巡目以降
                     loop1 |        l2 __|__ l2
                          /|\          \ | /  
                      l2 /___\l3     l3 \ / 
                    """
                    v2 = self.persp_coords[l2.vert].to_2d()
                    v3 = self.persp_coords[l3.vert].to_2d()
                    ivec, ivec_p1, ivec_p2 = isect_line_line_v2(v2, v3, p1, p2)
                    if ivec:
                        for next_tri in vert_tris[l2.vert]:
                            if l3 in next_tri and next_tri != tri:
                                break
                        tri = next_tri
                        t = list(tri)
                        t.remove(l2)
                        if l3 not in t:  # バグ回避
                            break
                        t.remove(l3)  # たまにバグる。何処が原因かさっぱり
                        l0 = t[0]
                        loop_pairs = [(l2, l0), (l3, l0)]
                        tri_loops_on_line = [loop for loop in tri
                                             if loop.vert in verts_on_line]
                        break
                else:
                    # 内側に存在するか
                    inside = self.point_is_inside_of_tri(p2, tri, exclude_edges=True)
                    if inside:  # and len(polyline.point_coords) > 2:
                        # polyline.coordsを求める
                        vec1 = self.persp_coords[tri[0].vert]
                        vec2 = self.persp_coords[tri[1].vert]
                        vec3 = self.persp_coords[tri[2].vert]
                        ivec = isect_point_tri_persp_to_world(pmat, p2,
                                                              vec1, vec2, vec3)
                        if ivec:  # 必ず交差するはずだが……
                            polyline.coords.append(obimat * ivec)
                        
                        polyline.point_index += 1
                        if len(polyline.point_coords) - polyline.point_index < 2:
                            break
                        loop_pairs = [(tri[i], tri[i - 1]) for i in range(3)]
                        i = polyline.point_index
                        p1 = mul_persp(pmat, polyline.point_coords[i]).to_2d()
                        p2 = mul_persp(pmat, polyline.point_coords[i + 1]).to_2d()
                        verts_on_line = self.calc_verts_on_line(efa.verts, p1, p2)
                        tri_loops_on_line = [loop for loop in tri
                                             if loop.vert in verts_on_line]
                    else:
                        break
            if end_vert:
                break
        return end_vert

    def line_cut(self, context, pmat, p1wld:'world co', p2wld:'world co'):
        pimat = pmat.inverted()
        obmat = context.active_object.matrix_world
        
        p1 = mul_persp(pmat, p1wld).to_2d()
        p2 = mul_persp(pmat, p2wld).to_2d()
        p1_p2 = p2 - p1
        if p1_p2.length == 0.0:
            return
        
        # 頂点とラインとの交差判定
        # set of BMVert
        self.verts_on_line = self.calc_verts_on_line(self.bm.verts, p1, p2)

        intersected = []  # edge_splitの引数(edge, facs) # edge.verts[0]基準
        
        # 辺を分割する位置を求める
        for eed in self.bm.edges:
            if not eed.select or eed.hide:
                continue
            mv1, mv2 = eed.verts

            # Get 2D coords of edge's verts
            v1 = self.persp_coords[mv1].to_2d()
            v2 = self.persp_coords[mv2].to_2d()
            
            v1_v2 = v2 - v1
            
            ivec, ivec_p1, ivec_p2 = isect_line_line_v2(v1, v2, p1, p2)
            
            factors = []  # 0 ~ 2
            for v in (ivec, ivec_p1, ivec_p2):
                if v and (v != v1 and v != v2):
                    fac = v1_v2.dot(v - v1) / v1_v2.length ** 2
                    fac_world = self.persp_fac_to_world_fac(
                                         fac, pimat,
                                         self.persp_coords[mv1],
                                         self.persp_coords[mv2])
                    factors.append(fac_world)
            if factors:
                factors.sort()
                intersected.append((eed, factors))

        # 辺を分割
        for eed, factors in intersected:
            eve = eed.verts[0]
            ofs = 0
            vnum = len(self.bm.verts)
            enum = len(self.bm.edges)
            for i, fac in enumerate(factors):
                f = fac - ofs
                eed2, eve = bmesh.utils.edge_split(eed, eve, f)
                eve.index = vnum + i
                eed2.index = enum + i
                eed2.select = eed.select
                ofs += fac
                self.verts_on_line.add(eve)
                self.persp_coords[eve] = mul_persp(pmat, obmat * eve.co)
                self.select_verts.append(eve)
                if eed in self.select_edges:
                    self.select_edges.append(eed2)
        
        # 既存のpolylineへのポイント追加
        for polyline in self.polylines:
            polyline.point_coords.append(p2wld.copy())  # copyしとかないと落ちる
        
        # polylinesへの新規登録
        for efa in self.bm.faces:
            if not efa.select or efa.hide:
                continue
            for eve in self.verts_on_line.intersection(efa.verts):
                # p2が頂点と重なる場合はパス
                if (self.persp_coords[eve].to_2d() - p2).length >= THRESHOLD:
                    polyline = PolyLine(efa, eve, [p1wld.copy(), p2wld.copy()])
                    self.polylines.append(polyline)
        
        polyline_index = 0

        while polyline_index < len(self.polylines):
            polyline = self.polylines[polyline_index]
            if not polyline.is_valid:
                polyline_index += 1
                continue
            
            efa = polyline.face
            face_verts = list(efa.verts)
            
            end_vert = self.search_end_vert(context, pmat, polyline)

            if not end_vert:
                polyline_index += 1
                continue
            start_loop = efa.loops[face_verts.index(polyline.vert)]
            end_loop = efa.loops[face_verts.index(end_vert)]
            
            # 分割
            subdivide = False
            if start_loop != end_loop:  # start_loop == end_loopはどうやっても不可
                if polyline.coords:
                    subdivide = True
                else:
                    if start_loop.link_loop_next != end_loop and \
                       start_loop.link_loop_prev != end_loop:
                        subdivide = True
            if subdivide and self.split_faces:
                vnum = len(self.bm.verts)
                findex = efa.index
                new_face, new_loop = bmesh.utils.face_split(
                    efa, polyline.vert, end_vert,
                    polyline.coords)
                new_face.select = efa.select
                # face_split()でcoordsを指定した場合（空の時は指定しない場合と同じ）、
                # 元のface.is_validはFalseとなり
                # 新規のfaceが2つ追加される。但し、一方のface.indexは元のfaceと同じ、
                # bm.facesでも同位置にある
                # memcpyでも行われたか？

                # インデックスアクセスの前にensure_lookup_table()が必要
                self.bm.faces.ensure_lookup_table()
                old_face = self.bm.faces[findex]
                
                # インデックス
                new_face.index = len(self.bm.faces) - 1
                self.bm.edges.index_update()
                
                # coordsを指定した分割では、bm.vertsの順番がバラバラになる事がある。
                update = False
                for i, eve in enumerate(self.bm.verts[vnum:]):
                    if eve.index == -1:
                        eve.index = vnum + i
                        self.persp_coords[eve] = mul_persp(pmat,
                                                           obmat * eve.co)
                    else:
                        update = True
                if update:
                    for i, eve in enumerate(self.bm.verts):
                        if eve.index == -1:
                            print(i, eve)
                            self.persp_coords[eve] = mul_persp(pmat,
                                                               obmat * eve.co)
                    self.bm.verts.index_update()
                
                # 古い面と新規の二つの面から共通する辺を求めて選択する
                for eed in old_face.edges:
                    if eed in new_face.edges:
                        self.select_edges.append(eed)
                
                # 一度分割したら用済みなので消す
                polyline.is_valid = False
                
                # 他のpolylineのfaceを確認して必要ならPolyLineの追加・無効化
                for pl in self.polylines[:]:
                    if not pl.is_valid or pl.face != efa:
                        continue
                    pl.face = old_face  # pl.face.is_valid == False
                    # new
                    if pl.vert in new_face.verts:
                        new_polyline = pl.copy()
                        new_polyline.face = new_face
                        self.polylines.append(new_polyline)
                    # is_valid = False
                    if pl.vert not in pl.face.verts:
                        pl.is_valid = False
            polyline_index += 1
        
        # remove
        for polyline in self.polylines[:]:
            if not polyline.is_valid:
                self.polylines.remove(polyline)

    def selection_update(self, context):
        #self.bm.select_history.clear()

        if self.deselect:
            for v in self.bm.verts:
                v.select = False
            for e in self.bm.edges:
                e.select = False
            for f in self.bm.faces:
                f.select = False
        
        for v in self.select_verts:
            if v.is_valid:
                v.select = True
                #self.bm.select_history.add(v)
        
        for e in self.select_edges:
            if e.is_valid:
                #self.bm.select_history.add(e)
                e.select = True
                e.verts[0].select = True
                e.verts[1].select = True
        
        if self.bm.select_mode == {'FACE'}:
            for f in self.bm.faces:
                select = True
                for v in f.verts:
                    if not v.select:
                        select = False
                f.select = select
                """if 'EDGE' not in self.bm.select_mode:
                    for e in f.edges:
                        e.select = select
                if 'VERT' not in self.bm.select_mode:
                    for v in f.verts:
                        v.select = select
                """
        
        self.bm.select_flush_mode()
#         self.bm.normal_update()

    def execute(self, context):
        actob = context.active_object
        obmat = actob.matrix_world
        
        context.tool_settings.mesh_select_mode = self.select_mode
        
        if hasattr(self, 'bm_bak'):
            bpy.ops.object.mode_set(mode='OBJECT')
            self.bm_bak.to_mesh(actob.data)
            bpy.ops.object.mode_set(mode='EDIT')
        
        self.init_exec_attrs(context)
        
        pmat_pre = None
        for pmat, point_coords in self.points_executed:
            if pmat != pmat_pre:
                self.persp_coords = {eve: mul_persp(pmat, obmat * eve.co)
                                     for eve in self.bm.verts}
                pmat_pre = pmat
            self.polylines[:] = []
            for i in range(len(point_coords) - 1):
                p1co = point_coords[i]
                p2co = point_coords[i + 1]
                self.line_cut(context, pmat, p1co, p2co)
        
        pmat = self.perspective_matrix
        if pmat != pmat_pre:
            self.persp_coords = {eve: mul_persp(pmat, obmat * eve.co)
                                 for eve in self.bm.verts}
        self.polylines[:] = []
        for i in range(len(self.points) - 1):
            p1co = self.points[i].co
            p2co = self.points[i + 1].co
            self.line_cut(context, pmat, p1co, p2co)
        
        self.selection_update(context)
#         actob.update_tag({'OBJECT', 'DATA'})  # Modifierを更新
        context.area.tag_redraw()
        
        return {'FINISHED'}

    def check_view_lock(self, context):
        self.view_move_zoom_lock = False
        self.view_rotate_lock = False
        for polyline in self.polylines:
            if len(polyline.point_coords) > 1:
                self.view_rotate_lock = True
                if context.region_data.view_perspective != 'ORTHO':
                    self.view_move_zoom_lock = True

    def modal(self, context, event):
        if event.type == 'INBETWEEN_MOUSEMOVE':
            return {'PASS_THROUGH'}

        area = context.area
        region = context.region
        rv3d = context.region_data
        pmat = rv3d.perspective_matrix
        actob = context.active_object
        obmat = actob.matrix_world
        
        if len(self.points) == 0:
            self.points.add()
        
        mco = self.mco = Vector((event.mouse_region_x, event.mouse_region_y))
        
        # マウス座標を3D化。Z値は直前のKnifePointを参照する。
        mco3d = mco.to_3d()
        mco3d[2] = 0.5  # 0以外を指定しておく
        if len(self.points) >= 2:
            v_win = vav.project(region, rv3d, self.points[-2].co)
            mco3d[2] = v_win[2]
        mco_wld = vav.unproject(region, rv3d, mco3d)
        self.points[-1].co[:] = mco_wld

        # perspective座標更新
        if pmat != self.perspective_matrix:
            self.persp_coords = {eve: mul_persp(pmat, obmat * eve.co)
                                 for eve in self.bm.verts}
            self.perspective_matrix = flatten_matrix(pmat)
        
        final_vector = self.points[-1].co.copy()
        if event.ctrl:
            # スナップ
            if event.shift:
                # グリッドにスナップ。
                self.snap_grid = True
                """v3d = context.space_data
                if hasattr(v3d, 'use_local_grid') and v3d.use_local_grid:
                    origin = v3d.local_grid_location
                    quat = v3d.local_grid_rotation
                else:
                    origin = quat = None
                """
                unit_system = unitsystem.UnitSystem(context)
                final_vector = unit_system.snap_local_grid(context, mco_wld,
                                                           event.alt)
                self.snap_vector = final_vector
            else:
                self.snap_grid = False
                result = self.snap_objects.snap(context, mco, self.snap_type)
                if result:
                    if result['object'] == actob and self.snap_type == 'EDGE' \
                       and (event.alt or event.oskey):
                        eed = self.bm.edges[result['index']]
                        vec = obmat * ((eed.verts[0].co + eed.verts[1].co) / 2)
                    else:
                        vec = result['location']
                    final_vector = self.snap_vector = vec
                else:
                    self.snap_vector = None
        else:
            self.snap_vector = None
            
        if self.axis is not None:
            # snap_vecを修正してself.points[-1]を置き換える
            axis_vector = Vector((math.cos(self.axis),
                                  math.sin(self.axis),
                                  0))
            v1 = vav.project(region, rv3d, self.points[-2].co)
            v2 = vav.project(region, rv3d, final_vector)
            v_on_axis = v1 + (v2 - v1).project(axis_vector)
            v_on_axis[2] = v2[2]
            final_vector = vav.unproject(region, rv3d, v_on_axis)

        self.points[-1].co[:] = final_vector[:]
        
        #print(event.type, event.value)

        if event.type in ('LEFT_CTRL', 'LEFT_ALT', 'LEFT_SHIFT',
                          'RIGHT_ALT', 'RIGHT_CTRL', 'RIGHT_SHIFT'):
            context.area.tag_redraw()
        
        elif event.type == 'TAB' and event.value == 'PRESS':
            if self.snap_type == 'VERTEX':
                self.snap_type = 'EDGE'
            else:
                self.snap_type = 'VERTEX'
            context.area.tag_redraw()
        
        elif event.type == 'C' and event.value == 'PRESS':
            if self.axis is not None:
                self.axis = None
            elif len(self.points) >= 2:
                v1 = vav.project(region, rv3d, self.points[-2].co).to_2d()
                v2 = vav.project(region, rv3d, self.points[-1].co).to_2d()
                v = v2 - v1
                if len(v) > 1.0:
                    angle = math.atan2(v[1], v[0])
                    if event.ctrl:
                        self.axis = angle
                    else:
                        pi8 = math.pi / 4
                        for i in range(9):
                            a = -math.pi + pi8 * i
                            if a - pi8 / 2 <= angle < a + pi8 / 2:
                                self.axis = a
                                break
                        if self.axis == -math.pi:
                            self.axis = math.pi
            context.area.tag_redraw()
        
        elif event.type == 'E' and event.value == 'PRESS':
            coords = [p.co.copy() for p in self.points]
            pmat = self.perspective_matrix.copy()
            self.points_executed.append([pmat, coords])
            self.points.clear()
            self.polylines[:] = []
            context.area.tag_redraw()
        
        elif event.type == 'F' and event.value == 'PRESS':
            self.split_faces = not self.split_faces
        
        elif event.type == 'Z' and event.value == 'PRESS':
            if not (event.shift or event.ctrl or event.alt or event.oskey):
                return {'PASS_THROUGH'}
        
        elif event.type == 'D' and event.value == 'PRESS':
            if event.alt and \
               not event.shift and not event.ctrl and not event.oskey:
                return {'PASS_THROUGH'}
        
        elif event.type == 'MOUSEMOVE':
            context.area.tag_redraw()
        
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.axis = None
            if len(self.points) >= 2:
                point1 = self.points[-2]
                point2 = self.points[-1]
                if point1.co == point2.co:
                #if self.mco == self.mco_bak:
                    self.selection_update(context)
                    context.space_data.draw_handler_remove(self._handle,
                                                           'WINDOW')
                    area.header_text_set()
                    context.area.tag_redraw()
                    self.snap_objects.free()
                    return {'FINISHED'}
                else:
                    self.mco_bak = self.mco.copy()
                self.line_cut(context, pmat, point1.co, point2.co)
#                 actob.update_tag({'OBJECT', 'DATA'})  # Modifierを更新
                self.bm.normal_update()
                bmesh.update_edit_mesh(actob.data, True, True)
            point = self.points.add()
            point.co = self.points[-2].co.copy()
            context.area.tag_redraw()
            self.snap_objects.update(context)
            
        elif event.type == 'MIDDLEMOUSE':
            # 視点変更
            self.check_view_lock(context)
            if event.shift and not event.ctrl and not event.alt \
                           and not event.oskey:
                # move
                if not self.view_move_zoom_lock:
                    bpy.ops.view3d.move('INVOKE_DEFAULT')
            elif event.ctrl and not event.shift and not event.alt \
                            and not event.oskey:
                # zoom
                if not self.view_move_zoom_lock:
                    bpy.ops.view3d.zoom('INVOKE_DEFAULT')
            
            elif not event.shift and not event.ctrl and not event.alt \
                 and not event.oskey:
                # rotation
                if not self.view_rotate_lock:
                    bpy.ops.view3d.rotate('INVOKE_DEFAULT')
        
        elif event.type in ('WHEELDOWNMOUSE', 'WHEELUPMOUSE'):
            # 視点変更
            self.check_view_lock(context)
            if event.shift and not event.ctrl and not event.alt \
                           and not event.oskey:
                # move vertical
                if not self.view_move_zoom_lock:
                    if event.type == 'WHEELDOWNMOUSE':
                        pan_type = 'PANDOWN'
                    else:
                        pan_type = 'PANUP'
                    bpy.ops.view3d.view_pan('INVOKE_DEFAULT', type=pan_type)
                    
            elif event.ctrl and not event.shift and not event.alt \
                            and not event.oskey:
                # move horizontal
                if not self.view_move_zoom_lock:
                    if event.type == 'WHEELDOWNMOUSE':
                        pan_type = 'PANLEFT'
                    else:
                        pan_type = 'PANRIGHT'
                    bpy.ops.view3d.view_pan('INVOKE_DEFAULT', type=pan_type)
                    
            elif not event.shift and not event.ctrl and not event.alt \
                 and not event.oskey:
                # zoom
                if not self.view_move_zoom_lock:
                    if event.type == 'WHEELDOWNMOUSE':
                        delta = -1
                    else:
                        delta = 1
                    bpy.ops.view3d.zoom(delta=delta)
        
        elif event.type in ('ENTER', 'RET', 'SPACE'):
            #self.points[-1:] = []  # 未確定のマウス位置のポイントを排除
            #self.execute(context)
            self.selection_update(context)
            context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            area.header_text_set()
            context.area.tag_redraw()
            self.snap_objects.free()
            return {'FINISHED'}
        
        elif event.type in ('RIGHTMOUSE', 'ESC'):
            # 中止
            bpy.ops.object.mode_set(mode='OBJECT')
            self.bm_bak.to_mesh(context.active_object.data)
            self.bm_bak.free()
            bpy.ops.object.mode_set(mode='EDIT')
            context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            area.header_text_set()
            context.area.tag_redraw()
            self.snap_objects.free()
            return {'CANCELLED'}

        texts = ['LMB: define cut lines', 
                 'Return/ Spacebar: confirm',
                 'Esc / RMB: cancel',
                 'E: new cut',
                 'F: split faces ({0})',
                 'Tab: toggle snap type',
                 'Ctrl: snap {1}',
                 'Ctrl + Shift: snap grid',
                 '(Ctrl + (Shift +)) C: angle constraint']
        text = ', '.join(texts)
        bool_str = {True: 'On', False: 'Off'}
        text = text.format(bool_str[self.split_faces], self.snap_type.title())
        area.header_text_set(text)
        
        return {'RUNNING_MODAL'}

    def init_exec_attrs(self, context):
        actob = context.active_object
        obmat = actob.matrix_world
        
        self.bm = bmesh.from_edit_mesh(actob.data)
        self.bm.verts.index_update()
        self.bm.edges.index_update()
        self.bm.faces.index_update()
        
        # キャンセル時の為
        if not hasattr(self, 'bm_bak'):
            self.bm_bak = self.bm.copy()
        
        # [[pmat, coords], ,,,] Eキーでクリアした物をこっちへ移動。
        if not hasattr(self, 'points_executed'):
            self.points_executed = []
        
        if not hasattr(self, 'select_mode'):
            self.select_mode = list(context.tool_settings.mesh_select_mode)
        
        self.polylines = []  # list of Polyline
        self.select_verts = []  # 最後にこの要素だけを選択状態にする
        self.select_edges = []  # 最後にこの要素だけを選択状態にする

    def invoke(self, context, event):

        v3d = context.space_data
        rv3d = context.region_data
        pmat = rv3d.perspective_matrix.copy()
        if len(self.points):
            if self.perspective_matrix.median_scale == 0.0:
                if v3d.type != 'VIEW_3D':
                    txt = 'Need "perspective_matrix" argument if not View3d'
                    self.report({'WARNING'}, txt)
                    return {'CANCELLED'}
                self.perspective_matrix = flatten_matrix(pmat)
            self.execute(context)
            return {'FINISHED'}
        
        if v3d.type != 'VIEW_3D':
            self.report({'WARNING'}, 'Active space must be a View3d')
            return {'CANCELLED'}

        context.window_manager.modal_handler_add(self)
        self._handle = context.space_data.draw_handler_add(self.draw_callback,
                                            (context,), 'WINDOW', 'POST_PIXEL')
        self.region = context.region
        
        self.init_exec_attrs(context)
        
        self.perspective_matrix = flatten_matrix(pmat)
        
        self.mco = Vector((event.mouse_region_x, event.mouse_region_y))
        self.mco_bak = self.mco.copy()
        
        actob = context.active_object
        obmat = actob.matrix_world
        self.persp_coords = {eve: mul_persp(pmat, obmat * eve.co)
                             for eve in self.bm.verts}
        
        self.snap_type = 'VERTEX'  # or 'EDGE'. toggle TAB key
        self.snap_grid = False  # False: vert or edge, True: grid
        self.snap_vector = None  # Vector
        self.axis = None  # float. toggle C key

        self.snap_objects = SnapObjects(context)
        
        # モード決定 (solidなら、ナイフのZ:cut through(OFF)と同様の挙動)
        if v3d.viewport_shade == 'RENDERED':
            self.mode = 'solid'
        elif v3d.viewport_shade in ('BOUNDBOX', 'WIREFRAME') or \
             not v3d.use_occlude_geometry:
            self.mode = 'wire'
        else:
            self.mode = 'solid'
        
        # 視点変更
        self.view_move_zoom_lock = False
        self.view_rotate_lock = False
        
        context.area.tag_redraw()
        
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(MESH_OT_bm_fake_knife.bl_idname, text='BM Fake Knife')


addon_keymaps = []


# Register
def register():
    addongroup.AddonGroup.register_module(__name__)

    bpy.types.VIEW3D_MT_edit_mesh_specials.append(menu_func)

    km = addongroup.AddonGroup.get_keymap('Mesh')
    if km:
        kmi = km.keymap_items.new('mesh.bm_fake_knife', 'K', 'PRESS',
                                  ctrl=True)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('mesh.bm_fake_knife', 'F15', 'PRESS')
        addon_keymaps.append((km, kmi))


def unregister():
    addongroup.AddonGroup.unregister_module(__name__)

    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == '__main__':
    register()
