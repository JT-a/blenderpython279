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


from collections import OrderedDict, defaultdict

import bpy
from mathutils import Vector

from .. import localutils

from . import vaview3d as vav


class Vert():
    def __init__(self, vertex=None):
        if vertex:
            self.index = vertex.index
            self.select = vertex.select
            self.hide = vertex.hide
            self.normal = vertex.normal.copy()
            self.co = vertex.co.copy()
        else:
            self.index = 0
            self.select = False
            self.hide = False
            self.normal = Vector()
            self.co = Vector()
        self.vertices = []
        self.edges = []
        self.faces = []
        self.f1 = 0
        self.f2 = 0
        self.wldco = None  # type:Vector. self.co * ob.matrix_world
        self.winco = None  # type:Vector. world_to_window()
        self.viewco = None  # type:Vector self.wldco * viewmat

    def _get_selected(self):
        return self.select and not self.hide

    def _set_selected(self, val):
        if not self.hide:
            self.select = val

    is_selected = property(_get_selected, _set_selected)

    def copy(self, set_original=False):
        vert = Vert(self)
        if set_original:
            vert.original = self
        return vert

    # def get_edge(self, vert):
    #     key = tuple(sorted((self.index, vert.index)))
    #     return self.pymesh.key_edge.get(key, None)


class Edge():
    def __init__(self, edge=None, vertices=None):
        if edge:
            self.index = edge.index
            self.select = edge.select
            self.hide = edge.hide
            self.is_loose = edge.is_loose
            self.use_edge_sharp = edge.use_edge_sharp
            self.use_seam = edge.use_seam
            self.key = edge.key
            if vertices:
                #self.vertices = [vertices[i] for i in edge.vertices]
                self.vertices = [vertices[edge.vertices[0]],
                                 vertices[edge.vertices[1]]]
        else:
            self.index = 0
            self.select = False
            self.hide = False
            self.is_loose = False
            self.use_edge_sharp = False
            self.use_seam = False
            self.key = ()  # (int, int)
            self.vertices = []
        self.faces = []
        self.f1 = 0
        self.f2 = 0

    def _get_selected(self):
        return self.select and not self.hide

    def _set_selected(self, val):
        if not self.hide:
            self.select = val

    is_selected = property(_get_selected, _set_selected)

    def copy(self, set_original=False):
        edge = Edge(self)
        edge.vertices = list(self.vertices)
        if set_original:
            edge.original = self
        return edge

    def vert_another(self, v):
        if v == self.vertices[0]:
            return self.vertices[1]
        elif v == self.vertices[1]:
            return self.vertices[0]
        else:
            return None


class Face():
    def __init__(self, face=None, vertices=None, key_edge=None):
        if face:
            self.index = face.index
            self.select = face.select
            self.hide = face.hide
            self.material_index = face.material_index
            self.area = face.area
            self.normal = face.normal.copy()
            self.center = face.center.copy()
            self.edge_keys = tuple(face.edge_keys)
            if vertices:
                self.vertices = [vertices[i] for i in face.vertices]
            if key_edge:
                self.edges = [key_edge[key] for key in face.edge_keys]
        else:
            self.index = 0
            self.select = False
            self.hide = False
            self.material_index = 0
            self.area = 0.0
            self.normal = Vector()
            self.center = Vector()
            self.edge_keys = []
            self.vertices = []
            self.edges = []
        self.f1 = 0
        self.f2 = 0

    def _get_selected(self):
        return self.select and not self.hide

    def _set_selected(self, val):
        if not self.hide:
            self.select = val

    is_selected = property(_get_selected, _set_selected)

    def copy(self, set_original=False):
        face = Face(self)
        face.vertices = list(self.vertices)
        face.edges = list(self.edges)
        if set_original:
            face.original = self
        return face

    # def vertices_other(self, vertices, force=False):
    #     ret_vertices = self.vertices[:]
    #     if force:
    #         for v in vertices:
    #             try:
    #                 ret_vertices.remove(v)
    #             except:
    #                 pass
    #     else:
    #         for v in vertices:
    #             try:
    #                 ret_vertices.remove(v)
    #             except:
    #                 return None
    #     return ret_vertices
    #
    # def shared_edges(self, vertices=[], edges=[]):
    #     verts = set()
    #     for edge in edges:
    #         verts.add(edge.vertices[0])
    #         verts.add(edge.vertices[1])
    #     for vert in vertices:
    #         verts.add(vert)
    #     return (e for e in self.edges if e.vertices[0] in verts and \
    #                                      e.vertices[1] in verts and \
    #                                      e not in edges)


class PyMesh():
    def __init__(self, me, select=(None, None, None), hide=(None, None, None)):
        key_edge = key_edge_dict(me, select=None, hide=None)

        def select_hide_check(item, select, hide):
            if (select is None or item.select == select) and \
               (hide is None or item.hide == hide):
                return True
            return False
        vertices = [Vert(v) for v in me.vertices]
        #vertices = [Vert(v) for v in me.vertices if select_hide_check(v)]()
        edges = [Edge(e, vertices) for e in me.edges]
        key_edge = {k: edges[ei] for k, ei in key_edge.items()}
        faces = [Face(f, vertices, key_edge) for f in me.faces]

        for f in faces:
            for v in f.vertices:
                v.faces.append(f)
            for key in f.edge_keys:
                key_edge[key].faces.append(f)
        for e in edges:
            for v in e.vertices:
                v.edges.append(e)
        for v in vertices:
            for e in v.edges:
                v.vertices.append(e.vert_another(v))

        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.key_edge = key_edge

    def calc_world_coordinate(self, matrix_world):
        for vert in self.vertices:
            vert.wldco = matrix_world * vert.co 

    def calc_window_coordinate(self, persmat, sx, sy):
        for vert in self.vertices:
            if vert.wldco:
                vert.winco = vav.world_to_window(vert.wldco,  persmat, sx, sy)

    def calc_view_coordinate(self, view_matrix):
        for vert in self.vertices:
            if vert.wldco:
                vert.viewco = view_matrix * vert.wldco 

    def calc_same_coordinate(self):
        for vert in self.vertices:
            vert.on_vertices = [v for v in vert.vertices if v.co == vert.co]

    def removed_same_coordinate(self, verts):
        d = OrderedDict(zip((tuple(v.co) for v in verts), range(len(verts))))
        return [verts[i] for i in d.values()]

    def find_edge(self, v1, v2):
        return self.key_edge.get(tuple(sorted(v1.index, v2.index)), None)

    # def find_vertices(self, elements, mode='and', remove=True):
    #     faces = [f for f in elements if isinstance(f, Face)]
    #     edges = [e for e in elements if isinstance(e, Edge)]
    #     vertices = [v for v in elements if isinstance(v, Vert)]
    #     l = []
    #     for f in faces:
    #         l.extend(f.vertices)
    #     for e in edges:
    #         l.extend(e.vertices)
    #     l.extend(vertices)
    #     c = Counter(l)
    #     if mode == 'and':
    #         if len(elements) == 1:
    #             ret = list(c.keys())
    #         else:
    #             ret = [k for k, i in c.items() if i > 1]
    #     else:
    #         ret = list(c.keys())
    #     if remove:
    #         for v in vertices:
    #             ret.remove(v)
    #     return ret
    #
    # def find_edges(self, elements, mode='and', remove=True):
    #     faces = [f for f in elements if isinstance(f, Face)]
    #     edges = [e for e in elements if isinstance(e, Edge)]
    #     vertices = [v for v in elements if isinstance(v, Vert)]
    #     l = []
    #     for f in faces:
    #         l.extend(f.edges)
    #     l.extend(edges)
    #     c = Counter(l)
    #     if mode == 'and':
    #         if len(elements) == 1:
    #             ret = list(c.keys())
    #         else:
    #             ret = [k for k, i in c.items() if i > 1]
    #     else:
    #         ret = list(c.keys())
    #     if remove:
    #         for e in edges:
    #             ret.remove(e)
    #     return ret
    #
    # def find_faces(self, elements, mode='and', remove=True):
    #     faces = [f for f in elements if isinstance(f, Face)]
    #     edges = [e for e in elements if isinstance(e, Edge)]
    #     vertices = [v for v in elements if isinstance(v, Vert)]
    #     l = []
    #     l.extend(faces)
    #     c = Counter(l)
    #     if mode == 'and':
    #         if len(elements) == 1:
    #             ret = list(c.keys())
    #         else:
    #             ret = [k for k, i in c.items() if i > 1]
    #     else:
    #         ret = list(c.keys())
    #     if remove:
    #         for e in edges:
    #             ret.remove(e)
    #     return ret


"""
### bpy.typesに追加
class CVert(bpy.types.PropertyGroup):
    index = IntProperty(name='Index', default=0)
    select = BoolProperty(name='Select', default=False)
    hide = BoolProperty(name='Hide', default=False)
    normal = FloatVectorProperty(name='Normal', subtype='XYZ', size=3)
    co = FloatVectorProperty(name='Co', subtype='XYZ', size=3)
    f1 = IntProperty(name='Flag1', default=0)
    f2 = IntProperty(name='Flag2', default=0)
    wldco = FloatVectorProperty(name='WldCo', subtype='XYZ', size=3)
    winco = FloatVectorProperty(name='WinCo', subtype='XYZ', size=3)
    viewco = FloatVectorProperty(name='ViewCo', subtype='XYZ', size=3)
    vec = FloatVectorProperty(name='Vec', description='tmp', subtype='XYZ', size=3)

    def copy_from(self, vert):
        self.index = vert.index
        self.select = vert.select
        self.hide = vert.hide
        self.normal = vert.normal
        self.co = vert.co

    def _get_selected(self):
        return self.select and not self.hide

    def _set_selected(self, val):
        if not self.hide:
            self.select = val

    is_selected = property(_get_selected, _set_selected)


class CEdge(bpy.types.PropertyGroup):
    index = IntProperty(name='Index', default=0)
    select = BoolProperty(name='Select', default=False)
    hide = BoolProperty(name='Hide', default=False)
    normal = FloatVectorProperty(name='Normal', subtype='XYZ', size=3)
    is_loose = BoolProperty(name='Loose', default=False)
    use_edge_sharp = BoolProperty(name='Sharp', default=False)
    use_seam = BoolProperty(name='Seam', default=False)
    key = IntVectorProperty(name='Key', default=(0, 0), size=2)
    f1 = IntProperty(name='Flag1', default=0)
    f2 = IntProperty(name='Flag2', default=0)
    vec = FloatVectorProperty(name='Vec', description='tmp', subtype='XYZ', size=3)

    def copy_from(self, edge):
        self.index = edge.index
        self.select = edge.select
        self.hide = edge.hide
        self.is_loose = edge.is_loose
        self.use_edge_sharp = edge.use_edge_sharp
        self.use_seam = edge.use_seam
        self.key = edge.key

    def _get_selected(self):
        return self.select and not self.hide

    def _set_selected(self, val):
        if not self.hide:
            self.select = val

    is_selected = property(_get_selected, _set_selected)

    def vert_another(self, v):
        if v in self.vertices:
            return self.vertices[self.vertices.index(v) - 1]
        else:
            return None

class CFace(bpy.types.PropertyGroup):
    index = IntProperty(name='Index', default=0)
    select = BoolProperty(name='Select', default=False)
    hide = BoolProperty(name='Hide', default=False)
    material_index = IntProperty(name='Material Index', default=0)
    area = FloatProperty(name='Area', default=0.0)
    normal = FloatVectorProperty(name='Normal', default=(0.0, 0.0, 0.0), subtype='XYZ', size=3)  # DIRECTION, XYZ
    center = FloatVectorProperty(name='Center', default=(0.0, 0.0, 0.0), subtype='XYZ', size=3)  # DIRECTION, XYZ
    #edge_keys =
    f1 = IntProperty(name='Flag1', default=0)
    f2 = IntProperty(name='Flag2', default=0)
    vec = FloatVectorProperty(name='Vec', description='tmp', subtype='XYZ', size=3)
    vertex_indices = IntVectorProperty(name='Vertices', default=(0, 0, 0, 0), size=4)

    def copy_from(self, face):
        self.index = face.index
        self.select = face.select
        self.hide = face.hide
        self.material_index = face.material_index
        self.area = face.area
        self.normal = face.normal
        self.center = face.center

    def _get_selected(self):
        return self.select and not self.hide

    def _set_selected(self, val):
        if not self.hide:
            self.select = val

    is_selected = property(_get_selected, _set_selected)

    def _get_vertices(self):
        return (self.v1, self.v2, self.v3, self.v4)

    def _set_vertices(self, vertices):
        self.v1, self.v2, self.v3, self.v4 = vertices

    vertices = property(_get_selected, _set_selected)


bpy.types.CVert.vertices = CollectionProperty(name='Vertices', type=CVert)
bpy.types.CVert.edges = CollectionProperty(name='Edges', type=CEdge)
bpy.types.CVert.faces = CollectionProperty(name='Faces', type=CFace)
bpy.types.CEdge.vertices = CollectionProperty(name='Vertices', type=CVert)
bpy.types.CEdge.edges = CollectionProperty(name='Edges', type=CEdge)
bpy.types.CEdge.faces = CollectionProperty(name='Faces', type=CFace)
#bpy.types.CFace.vertices = CollectionProperty(name='Vertices', type=CVert)
bpy.types.CFace.edges = CollectionProperty(name='Edges', type=CEdge)
bpy.types.CFace.faces = CollectionProperty(name='Faces', type=CFace)


class CPyMesh(bpy.types.PropertyGroup):
    ### 重過ぎて使い物にならない ###
    '''
    スクリプト中での要素の追加、削除は
    bpy.types.CPyMesh.tmp = CollectionProperty(name='tmp', type=CVert)
    del(bpy.types.CPyMesh.tmp)

    foreach_getの使い方 (op/object.py)
    import array
    arr = array.array('f', [0.0] * 8) * len_faces  # seems to be the fastest way to create an array
    mesh.uv_textures.active.data.foreach_get("uv_raw", arr)
    '''
    vertices = CollectionProperty(name='Vertices', type=CVert)
    edges = CollectionProperty(name='Edges', type=CEdge)
    faces = CollectionProperty(name='Faces', type=CFace)

    def generate(self, me):
        vertices = self.vertices
        edges = self.edges
        faces = self.faces

        # reset
        remove = vertices.remove
        for i in range(len(vertices)):
            remove()
        remove = edges.remove
        for i in range(len(edges)):
            remove()
        remove = faces.remove
        for i in range(len(faces)):
            remove()

        for vert in me.vertices:
            v = vertices.add()
            #v.copy_from(vert)
        for edge in me.edges:
            e = edges.add()
            #e.copy_from(edge)
        for face in me.faces:
            f = faces.add()
            #f.copy_from(face)

#bpy.types.Scene.pymesh = CollectionProperty(name='CPyMesh', type=CPyMesh)
"""

###############################################################################
# Dict
###############################################################################
# def make_checked_dict(items, select=None, hide=None):
#     return {item.index: [] for item in items
#             if (select is None or item.select is select) and
#                (hide is None or item.hide is hide)}


class KeyEdgeDict(dict):
    # def get(self, *key):
    #     if len(key) == 2:  # v1, v2
    #         return super(KeyEdgeDict, self).get(tuple(sorted(key)))
    #     else:
    #         return super(KeyEdgeDict, self).get(key[0])

    def get2(self, v1, v2):
        return self.get(tuple(sorted((v1, v2))))


def key_edge_dict(me, select=None, hide=None):
    check = lambda item: (select is None or item.select == select) and \
                         (hide is None or item.hide == hide)
    # key_edge = {e.key: e.index for e in me.edges if check(e)}
    key_edge = KeyEdgeDict(((e.key, e.index) for e in me.edges if check(e)))
    return key_edge


def vert_verts_dict(me=None, select=None, hide=None, edge_keys=None):
    """
    select: True:選択中, False:非選択, None:全て
    edge_keys: 指定すると、この中の頂点のみを処理した辞書を返す。
    return: type:dict. key:頂点インデックス value:接続する頂点インデックスのリスト。
    """
    check = lambda item: (select is None or item.select == select) and \
                         (hide is None or item.hide == hide)
    if edge_keys is None:
        #vert_verts = {v.index: [] for v in me.vertices if check(v)}
        """
        バグ: エッジ選択モードでエッジを非選択した場合、接続する辺の選択状態に関わらず、
        両端の頂点が非選択になる。
        """
        vert_verts = defaultdict(list)
        vert_verts.update({v.index: [] for v in me.vertices if check(v)})
        for edge in (e for e in me.edges if check(e)):  # edgeで接続判定
            i1, i2 = edge.key
            vert_verts[i1].append(i2)
            vert_verts[i2].append(i1)
    else:
        vert_verts = {}
        for key in edge_keys:
            for i in range(2):
                if key[i] not in vert_verts:
                    vert_verts[key[i]] = [key[i - 1]]
                else:
                    vert_verts[key[i]].append(key[i - 1])
    return vert_verts


def vert_edges_dict(me, select=None, hide=None):
    check = lambda item: (select is None or item.select == select) and \
                         (hide is None or item.hide == hide)
    # vert_edges = {v.index: [] for v in me.vertices if check(v)}
    vert_edges = defaultdict(list)
    vert_edges.update({v.index: [] for v in me.vertices if check(v)})
    for edge in (e for e in me.edges if check(e)):
        for i in edge.key:
            vert_edges[i].append(edge.index)
    return vert_edges


def vert_faces_dict(me, select=None, hide=None):
    check = lambda item: (select is None or item.select == select) and \
                         (hide is None or item.hide == hide)
    # vert_faces = {v.index: [] for v in me.vertices if check(v)}
    vert_faces = defaultdict(list)
    vert_faces.update({v.index: [] for v in me.vertices if check(v)})
    for face in (f for f in me.faces if check(f)):
        for i in face.vertices:
            if isinstance(i, int):
                vert_faces[i].append(face.index)
            else:  # PyMesh
                vert_faces[i.index].append(face.index)
    return vert_faces


def edge_faces_dict(me, select=None, hide=None, key_edge={}):
    check = lambda item: (select is None or item.select == select) and \
                         (hide is None or item.hide == hide)
    # edge_faces = {e.index: [] for e in me.edges if check(e)}
    edge_faces = defaultdict(list)
    edge_faces.update({e.index: [] for e in me.edges if check(e)})
    if isinstance(me, bpy.types.Mesh):
        if not key_edge:
            key_edge = key_edge_dict(me)
        for face in (f for f in me.faces if check(f)):
            for key in face.edge_keys:
                edge_faces[key_edge[key]].append(face.index)
    else:  # PyMesh
        for face in (f for f in me.faces if check(f)):
            for e in face.edges:
                edge_faces[e.index].append(face.index)

    return edge_faces


def face_faces_dict(me, select=None, hide=None, edge_faces={}, key_edge={},
                    vert_faces={}, connect_vert=False):
    """
    connect_vert: Trueなら頂点を共有している面同士は隣接しているとみなす。
                  Falseなら辺を共有している面のみ対象。
    """
    check = lambda item: (select is None or item.select == select) and \
                         (hide is None or item.hide == hide)
    #face_faces = {f.index: [] for f in me.faces if check(f)}
    face_faces = defaultdict(list)
    face_faces.update({f.index: [] for f in me.faces if check(f)})
    if connect_vert:
        if not vert_faces:
            vert_faces = vert_faces_dict(me, select, hide)
        seq = vert_faces.values()
    else:
        if not edge_faces:
            edge_faces = edge_faces_dict(me, select, hide, key_edge)
        seq = edge_faces.values()
    for face_indices in seq:
        for i, face_index in enumerate(face_indices):
            for fi in face_indices[:i] + face_indices[i + 1:]:
                if fi not in face_faces[face_index]:
                    face_faces[face_index].append(fi)
    return face_faces


###############################################################################
# Connect
###############################################################################
def linked_vertices_list(me, select=None, hide=None):
    """辺で繋がった頂点インデックスのリストを返す"""
    vert_verts = vert_verts_dict(me, select=select, hide=hide)
    # return vau.dict_to_linked_items_list(vert_verts)
    def key(v1, v2, data):
        return v1 in data[v2] or v2 in data[v1]
    return localutils.utils.groupwith(vert_verts.keys(), key, vert_verts)


def linked_faces_list(me, select=None, hide=None, connect_vert=False):
    """繋がった面インデックスのリストを返す。"""
    face_faces = face_faces_dict(me, select, hide, connect_vert=connect_vert)
    # return vau.dict_to_linked_items_list(face_faces)
    def key(f1, f2, data):
        return f1 in data[f2] or f2 in data[f1]
    return localutils.utils.groupwith(face_faces.keys(), key, face_faces)


"""
def split_faces_re(me, edkey, efdict, fdict):
    # 旧
    for findex in efdict[edkey]:
        if findex in fdict:
            continue
        fdict[findex] = None
        keys = me.faces[findex].edge_keys
        for key in keys:
            split_faces_re(me, key, efdict, fdict)


def split_faces(me, indexlist=None):
    # 旧
    if indexlist:
        efdict = edge_faces_dict(me, sel=0)
        for key in efdict.keys():
            if len(efdict[key]) == 0:
                del efdict[key]
        indexdict = dict.fromkeys(indexlist)  # for performance
        for f in me.faces:
            if not f.hide and f.index not in indexdict:  # dell
                for key in f.edge_keys:
                    if f.index in efdict[key]:
                        efdict[key].remove[f.index]
    else:
        efdict = edge_faces_dict(me, sel=2)
        for key in efdict.keys():
            if len(efdict[key]) == 0:
                del efdict[key]
        indexdict = dict([[f.index, None] for f in me.faces if \
                          f.select and not f.hide])

    returnlist = []
    while indexdict:
        fdict = {}
        split_faces_re(me, me.faces[list(indexdict.keys())[0]].edge_keys[0], \
                       efdict, fdict)
        returnlist.append(fdict.keys())
        for findex in fdict.keys():
            del indexdict[findex]

    return returnlist
"""


###############################################################################
# Path
###############################################################################
class Path(list):
        def __init__(self, arg=[], cyclic=False):
            super(Path, self).__init__(arg)
            self.cyclic = cyclic
            #self.fill = False  # io_export_svgで使う？


def path_vertices_list(me=None, select=None, hide=None,
                       vert_verts=None, edge_keys=None):
    """pathのリストを返す
    vert_vertsの辞書か、edge_keys(keyのリスト)を指定すると、それのみ処理。
    [i1, i2, i3, i4, i1].cyclic = False  # 四角形、i1に別の辺が接続
    [i1, i2, i3, i4, i1].cyclic = True  # 四角形
    """

    if vert_verts is None:
        if edge_keys is None:
            vert_verts = vert_verts_dict(me, select=select, hide=hide)
        else:
            vert_verts = vert_verts_dict(edge_keys=edge_keys)
    vert_end = {vi: len(vis) != 2 for vi, vis in vert_verts.items()}
    ### vert_vertsから生成
    keys = set()
    for vert, verts in vert_verts.items():
        for v in verts:
            keys.add((min(vert, v), max(vert, v)))
    key_added = {k: False for k in keys}
    #key_edge = key_edge_dict(me, select=select, hide=hide)
    #key_added = {k: False for k in key_edge.keys()}
    paths = []

    # path has end points
    for vibase, vis in vert_verts.items():
        if vert_end[vibase] and len(vis) != 0:  # end point
            for vi in vis:  # 隣接頂点ループ
                if key_added[tuple(sorted((vibase, vi)))]:
                    continue
                path = Path([vibase])
                while True:
                    path.append(vi)
                    if vert_end[vi]:
                        break
                    vi = [i for i in vert_verts[vi] if i != path[-2]][0]
                for i, j in zip(path, path[1:]):
                    key = tuple(sorted((i, j)))
                    key_added[key] = True

                paths.append(path)
        elif len(vis) == 0:
            path = Path([vibase])
            paths.append(path)

    # cyclic path
    for vi in (vi for vi, end in vert_end.items() if end is True):
        del(vert_verts[vi])
    for path in paths:
        for vi in path[1:-1]:
            del(vert_verts[vi])
    while vert_verts:
        for vibase in vert_verts.keys():
            break
        path = Path([vibase], cyclic=True)
        vi = vert_verts[vibase][0]
        del(vert_verts[vibase])
        while vibase != vi:
            path.append(vi)
            vn = [i for i in vert_verts[vi] if i != path[-2]][0]
            del(vert_verts[vi])
            vi = vn
        else:
            path.append(vi)
        paths.append(path)

    return paths


def faces_outline_path(faces:'list of MeshFace', irregular_edges=False):
    """
    linked_faces_listで面を分割した後、この関数を呼び出す。
    faces: 辺を共有する面のリスト。 (ジェネレータでも可)
    irregular_edges: 面を三つ以上持つ辺をoutlineとみなして、pathに含める
    return: 外周の頂点インデックスのリスト(=Path)のリスト。
            通常は[path]を返すが、ループ物や不正な構造な場合(irregular_edges) len(paths) > 1となる
    """
    # 辺が所有する面の数を示す辞書を作成
    key_count = defaultdict(int)
    for face in faces:
        for key in face.edge_keys:
            key_count[key] += 1
    outline_keys = [key for key, count in key_count.items() if \
                    count == 1 or (irregular_edges and count >= 3)]
    paths = path_vertices_list(edge_keys=outline_keys)
    return paths


def face_outline_paths(me, select=None, hide=None, connect_vert=False,
                        irregular_edges=False):
    """
    return: Pathの二次元リスト [[Path, Path], [Path], [Path], ...]
    場合によって、一つの面の塊から複数のPathが生成される。
    """
    paths_list = []
    face_blocks = linked_faces_list(me, select, hide,
                                    connect_vert=connect_vert)
    for face_indices in face_blocks:
        # type: (MeshFace, Face)
        faces = (me.faces[i] for i in face_indices)
        paths = faces_outline_path(faces, irregular_edges)
        paths_list.append(paths)
    return paths_list


###############################################################################
# Convert
###############################################################################
def mesh_convert_to_curve(context, me, mat, threshold):
    """
    meshデータからcurveObjectを生成、sceneにリンクした状態で返す。
    mat: ob.matrix_world
    threshold: smooth angle

    消去したい場合は、context.scene.objects.unlink(newob)
                    bpy.data.objects.remove(newob)
                    bpy.data.curves.remove(curve)
    """

    cu = bpy.data.curves.new(name='CU_mesh_convert_data', type='CURVE')
    newob = bpy.data.objects.new(name='OB_mesh_convert_data',
                                 object_data=cu)
    context.scene.objects.link(newob)
    if me is None:
        #me = ob.data
        me = newob.data  # この修正でいい？

    edge_faces = edge_faces_dict(me)
    edge_keys = [me.edges[i].key for i, faces in edge_faces.items() if \
                 len(faces) == 0 or len(faces) >= 3]
    edge_paths = path_vertices_list(edge_keys=edge_keys)
    outline_blocks = face_outline_paths(me, irregular_edges=False)

    for path_block in outline_blocks + [edge_paths]:
        for path in path_block:
            if not path:
                continue
            vecs = [me.vertices[i].co * mat for i in path]
            # bezier_points生成
            spline = cu.splines.new(type='BEZIER')
            cyclic = spline.use_cyclic_u = path.cyclic
            if cyclic:  # path_vertices_listの仕様を変更した為
                path = path[:-1]
            for i in range(len(vecs) - 1):
                spline.bezier_points.add()
            # 頂点、ハンドル調整
            bezts = spline.bezier_points
            if len(vecs) <= 2:
                for bezt, vec in zip(bezts, vecs):
                    bezt.co = vec
                    bezt.handle_left_type = 'VECTOR'
                    bezt.handle_right_type = 'VECTOR'
            else:
                for i in range(len(vecs)):
                    bezt = bezts[i]
                    bezt.co = vecs[i]
                    if not cyclic and (i == 0 or i == len(vecs) - 1):
                        bezt.handle_left_type = 'VECTOR'
                        bezt.handle_right_type = 'VECTOR'
                        continue
                    else:
                        vec0 = vecs[i - 1]
                        vec1 = vecs[i]
                        if i < len(vecs) - 1:
                            vec2 = vecs[i + 1]
                        else:
                            vec2 = vecs[0]
                    v01 = vec1 - vec0
                    v12 = vec2 - vec1
                    if v01.length and v12.length:
                        angle = v01.angle(v12)
                    else:
                        angle = 0.0
                    if angle <= threshold:
                        bezt.handle_left_type = 'AUTO'
                        bezt.handle_right_type = 'AUTO'
                    else:
                        bezt.handle_left_type = 'VECTOR'
                        bezt.handle_right_type = 'VECTOR'
                # 境界の修正。前と次、若しくは逆のbeztのハンドルがAUTOとVECTORの場合
                for i in range(len(bezts)):
                    bezt = bezts[i]
                    prevbezt = bezts[i - 1]
                    if i < len(bezts) - 1:
                        nextbezt = bezts[i + 1]
                    # left handle
                    if cyclic or (not cyclic and i != 0):
                        if bezt.handle_left_type == 'VECTOR' and \
                           prevbezt.handle_right_type == 'AUTO':
                            bezt.handle_left_type = 'FREE'
                            prev_handle = prevbezt.handle_right - prevbezt.co
                            prev_to_cu = bezt.co - prevbezt.co
                            vec_h = prev_handle.project(prev_to_cu)
                            vec_v = prev_handle - vec_h
                            bezt.handle_left = bezt.co - vec_h + vec_v
                    # right handle
                    if cyclic or (not cyclic and i != len(vecs) - 1):
                        if bezt.handle_right_type == 'VECTOR' and \
                           nextbezt.handle_left_type == 'AUTO':
                            bezt.handle_right_type = 'FREE'
                            next_handle = nextbezt.handle_left - nextbezt.co
                            next_to_cu = bezt.co - nextbezt.co
                            vec_h = next_handle.project(next_to_cu)
                            vec_v = next_handle - vec_h
                            bezt.handle_right = bezt.co - vec_h + vec_v
    return newob


###############################################################################
# Other
###############################################################################
def get_mirrored_mesh(scene, ob):
    # apply MirrorModifier only
    mods = ob.modifiers
    #mods_realtime = [mod.realtime for mod in mods]
    mods_realtime = [mod.show_viewport for mod in mods]
    for mod in mods:
        if mod.type != 'MIRROR':
            #mod.realtime = False
            mod.show_viewport = False

    me = ob.data
    selbuf = [v.select for v in me.vertices]
    for i in range(len(me.vertices)):
        me.vertices[i].select = i % 2
    dm = ob.to_mesh(scene, 1, 'PREVIEW')  # applied modifiers

    me_dm = {}
    finish_firststep = 0
    me_index = 0
    for dm_index in range(len(dm.vertices)):
        if dm.vertices[dm_index].select == me.vertices[me_index].select:
            if finish_firststep == 0:
                me_dm[me_index] = dm_index
                finish_firststep = 1
        else:
            me_index += 1
            me_dm[me_index] = dm_index
            finish_firststep = 1

    dm_me = dict.fromkeys(range(len(dm.vertices)), None)
    for me_index, dm_index in me_dm.items():
        dm_me[dm_index] = me_index

    for i in range(len(me.vertices)):
        me.vertices[i].select = selbuf[i]
    bpy.data.meshes.remove(dm)
    dm = ob.to_mesh(scene, 1, 'PREVIEW')

    for i in range(len(mods)):
        #mods[i].realtime = mods_realtime[i]
        mods[i].show_viewport = mods_realtime[i]

    return dm, me_dm, dm_me


def fill(verts):
    faces = []
    if len(verts) <= 2:
        pass
    elif 3 <= len(verts) <= 4:
        faces.append(verts)
    else:
        i = 0
        j = len(verts) - 1
        end = 0
        while True:
            if j - i == 2:
                # Triangle
                f = verts[i:i + 3]
                end = 1
            elif j - i == 3:
                # Quad
                f = verts[i:i + 4]
                end = 1
            else:
                f = [verts[i], verts[i + 1], verts[j - 1], verts[j]]
            faces.append(f)
            if end:
                break
            i += 1
            j -= 1

    return faces
