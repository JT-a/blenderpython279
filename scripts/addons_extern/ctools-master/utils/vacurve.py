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


import math
import re

import bpy
import mathutils
from mathutils import Matrix, Vector, geometry
from mathutils.geometry import interpolate_bezier

from . import vamath as vam
from . import vaview3d as vav
from . import vautils as vau
from .vamath import MIN_NUMBER
from .vacv import solve_cubic


# Simpson
def composite_simpson(func, a, b, subdivide):
    """積分。
    n は [a, b] を均等に偶数個に分割した際の部分区間の個数 (= subdivide)
    h は各部分区間の長さ
    """
    n = int(math.ceil(subdivide / 2) * 2)  # 偶数である事を保証
    h = (b - a) / n
    val = 0
    for i in range(n + 1):
        x = a + h * i
        if i == 0 or i == n:  # 先頭、終端
            val += func(x)
        elif i % 2:  # 奇数
            val += 4 * func(x)
        else:  # 偶数
            val += 2 * func(x)
    return h / 3 * val


#####################################################################
# BezierCurve
#####################################################################
class BezierCurve(list):
    """二次元ベクトルの場合、三次元ベクトルに拡張する。"""

    def __init__(self, v1, v2, v3, v4, radiuses=None, weights=None):
        size_list = [len(v1), len(v2), len(v3), len(v4)]
        if set(size_list) not in [{2}, {3}]:
            raise ValueError('2次元か3次元のVectorで統一せよ')

        self[:] = [v1.to_3d(), v2.to_3d(), v3.to_3d(), v4.to_3d()]
        self.size = set(size_list).pop()
        self.radiuses = list(radiuses) if radiuses else [1.0, 1.0]
        self.weights = list(weights) if weights else [0.0, 0.0]

        # coefficients: [[xa, xb, xc, xd], [ya, yb, yc, yd], [za, zb, zc, zd]]
        self.coefficients = [[0.0] * 4 for i in range(3)]
        self.update_coefficients()

    def __call__(self, t, size=3):
        size = min((self.size, size))
        vec = Vector([0.0 for i in range(size)])
        for i in range(size):
            vec[i] = self.coefficients[i][0] * t ** 3 + \
                     self.coefficients[i][1] * t ** 2 + \
                     self.coefficients[i][2] * t + \
                     self.coefficients[i][3]
        return vec

        # NOTE: ベクトルから求める場合。
        # def f(t, i):
        #     val = (1 - t) ** 3 * self[0][i] + \
        #           3 * (1 - t) ** 2 * t * self[1][i] + \
        #           3 * (1 - t) * t ** 2 * self[2][i] + \
        #           t ** 3 * self[3][i]
        #     return val
        # if size == 3:
        #     vec = Vector((f(t, 0), f(t, 1), f(t, 2)))
        #     return vec
        # else:
        #     vec = Vector((f(t, 0), f(t, 1)))
        #     return vec

    def update_coefficients(self):
        v1, v2, v3, v4 = self
        for i in range(self.size):
            self.coefficients[i][0] = -v1[i] + 3 * v2[i] - 3 * v3[i] + v4[i]
            self.coefficients[i][1] = 3 * (v1[i] - 2 * v2[i] + v3[i])
            self.coefficients[i][2] = 3 * (-v1[i] + v2[i])
            self.coefficients[i][3] = v1[i]
        if self.size == 2:
            self.coefficients[2][:] = [0.0, 0.0, 0.0, 0.0]

    def copy(self):
        return BezierCurve(self[0], self[1], self[2], self[3],
                           self.radiuses, self.weights)

    def copy_from(self, other):
        for i in range(4):
            self[i][:] = other[i]
        for attr in dir(other):
            try:
                setattr(self, attr, getattr(other, attr))
            except:
                pass

    def transform(self, mat):
        for i in range(4):
            self[i] = mat * self[i]
        self.update_coefficients()

    def transformed(self, mat):
        bez = self.copy()
        bez.transform(mat)
        return bez

    def transform_to_region_coords(self, sx, sy, persmat):
        """world -> region 変換を行う。"""
        for i in range(4):
            self[i] = vav.project_v3(sx, sy, persmat, self[i])
        self.update_coefficients()

    def transform_to_world(self, sx, sy, persmat):
        """region -> world 変換を行う。"""
        for i in range(4):
            self[i] = vav.unproject_v3(sx, sy, persmat, self[i])
        self.update_coefficients()

    def to_2d(self):
        bez = self.copy()
        for i in range(4):
            bez[i] = bez[i].to_2d()
        bez.update_coefficients()
        return bez

    def to_3d(self):
        bez = self.copy()
        for i in range(4):
            bez[i] = bez[i].to_3d()
        bez.update_coefficients()
        return bez

    def length(self, subdivide=100):
        """長さを求める
        :param subdivide: 分割数。大きいほど制度が上がる。
        :type subdivide: int
        :rtype: float
        """

        def dt(t, i):
            """bezierCurveの座標を求める式 x = f(t)を微分
            i: (0, 1, 2) == (x, y, z)
            """
            a = -self[0][i] + 3 * self[1][i] - 3 * self[2][i] + self[3][i]
            b = 3 * (self[0][i] - 2 * self[1][i] + self[2][i])
            c = 3 * (-self[0][i] + self[1][i])
            return 3 * a * t ** 2 + 2 * b * t + c

        def dt_length_3d(t):
            return math.sqrt(dt(t, 0) ** 2 + dt(t, 1) ** 2 + dt(t, 2) ** 2)

        def dt_length_2d(t):
            return math.sqrt(dt(t, 0) ** 2 + dt(t, 1) ** 2)

        if self.size == 3:
            return composite_simpson(dt_length_3d, 0, 1.0, subdivide)
        else:
            return composite_simpson(dt_length_2d, 0, 1.0, subdivide)

    def length_factor(self, target, factor, subdivide=100):
        """target側からfactor位置までの長さ。
        :param target: 0で先頭、1で末尾。
        :type target: int
        :param factor: 0.0 - 1.0 以外の範囲も可
        :type factor: float
        :type subdivide: int
        """
        bez = self.copy()
        if target == 0:
            bez.slide(1, factor)
        else:
            bez.slide(0, factor)
        return bez.length(subdivide)

    def reverse(self):
        super(BezierCurve, self).reverse()
        self.update_coefficients()

    def reversed(self):
        bez = self.copy()
        bez.reverse()
        return bez

    def slide(self, target, factor):
        """カーブに沿って片側を内側に移動する。weight, radiusも変更する。
        :param target: 0ならv1、1ならv4を移動。
        :type target: int
        :param factor: factorの位置に頂点を移動する。0.0 - 1.0 以外の範囲も可
        :type factor: float
        """
        t = factor
        v1, v2, v3, v4 = self[:]

        p = v2 + (v3 - v2) * t
        v2_new = v1 + (v2 - v1) * t
        v3_new = v4 + (v3 - v4) * (1 - t)
        v_left = v2_new + (p - v2_new) * t
        v_right = v3_new + (p - v3_new) * (1 - t)
        v_co = v_left + (v_right - v_left) * t

        r1, r2 = self.radiuses
        r = r1 + (r2 - r1) * t
        w1, w2 = self.weights
        w = w1 + (w2 - w1) * t

        if target == 0:
            self[0] = v_co
            self[1] = v_right
            self[2] = v3_new
            self[3] = v4
            self.radiuses[0] = r
            self.weights[0] = w
        else:
            self[0] = v1
            self[1] = v2_new
            self[2] = v_left
            self[3] = v_co
            self.radiuses[1] = r
            self.weights[1] = w

        self.update_coefficients()

    # subdivide -----------------------------------------------------
    def subdivide(self, factor):
        """分割したBezierCurveを返す
        :param factor: 分割位置
        :rtype: tuple[BezierCurve]
        """
        if isinstance(factor, (int, float)):
            return self.subdivide_sngle(factor)
        else:
            return self.subdivide_multi(factor)

    def subdivide_sngle(self, factor):
        """分割したbezierを2つ返す。
        :param factor: 分割位置。
            factor<0ならv1方向に、factor>1ならv4方向に伸ばしたbezierを作る。
            この場合、v1v2v3v4には変更を加えない。
        :type factor: float
        :rtype: [BezierCurve, BezierCurve]
        """

        t = factor
        v1, v2, v3, v4 = self[:]
        p = v2 + (v3 - v2) * t
        v2_new = v1 + (v2 - v1) * t
        v3_new = v4 + (v3 - v4) * (1 - t)
        v_left = v2_new + (p - v2_new) * t
        v_right = v3_new + (p - v3_new) * (1 - t)
        v_co = v_left + (v_right - v_left) * t
        radius = sum(self.radiuses) / 2
        weight = sum(self.weights) / 2
        if 0.0 <= t <= 1.0:
            b1 = BezierCurve(v1, v2_new, v_left, v_co,
                             radiuses=[self.radiuses[0], radius],
                             weights=[self.weights[0], weight])
            b2 = BezierCurve(v_co, v_right, v3_new, v4,
                             radiuses=[radius, self.radiuses[1]],
                             weights=[weight, self.weights[1]])
        elif t < 0.0:
            b1 = BezierCurve(v_co, v_left, v2_new, v1,
                             radiuses=[radius, self.radiuses[0]],
                             weights=[weight, self.weights[0]])
            b2 = self.copy()
        else:
            b1 = self.copy()
            b2 = BezierCurve(v4, v3_new, v_right, v_co,
                             radiuses=[self.radiuses[1], radius],
                             weights=[self.weights[1], weight])
        return [b1, b2]

    def subdivide_multi_exec(self, v1, v2, v3, v4, factors: '0.0<=t<=1.0',
                             radiuses=(1.0, 1.0), weights=(0.0, 0.0)):
        """self.subdivide_multiから呼び出し"""
        num = len(factors)

        bezier_points = []
        for i in range(2 + num):
            bezier_points.append([Vector(), Vector(), Vector(), 0.0, 0.0])
        bezier_points[0][1] = v1
        bezier_points[0][2] = v2
        bezier_points[0][3] = radiuses[0]
        bezier_points[0][4] = weights[0]
        bezier_points[-1][0] = v3
        bezier_points[-1][1] = v4
        bezier_points[-1][3] = radiuses[1]
        bezier_points[-1][4] = weights[1]

        # factorsを分割に使用する値に修正
        # [1/4, 2/4, 3/4] -> [1/4, 1/3, 1/2]
        subdivide_factors = []
        prevfac = 0.0
        for i in range(num):
            if prevfac == 1.0:
                fac = 0.0
            else:
                fac = (factors[i] - prevfac) / (1.0 - prevfac)
            subdivide_factors.append(fac)
            prevfac = factors[i]

        bezt = bezier_points[-1]
        prevbezt = bezier_points[0]

        pvecs = [prevbezt[0], prevbezt[1], prevbezt[2]]

        for i in range(num):
            factor = subdivide_factors[i]

            beztnew = bezier_points[1 + i]
            prevbeztnew = bezier_points[i]

            v1 = pvecs[1].lerp(pvecs[2], factor)
            v2 = pvecs[2].lerp(bezt[0], factor)
            v3 = bezt[0].lerp(bezt[1], factor)

            v4 = v1.lerp(v2, factor)
            v5 = v2.lerp(v3, factor)

            # change handle of prev beztnew
            prevbeztnew[2] = v1
            # new point
            beztnew[0] = v4
            beztnew[1] = v4.lerp(v5, factor)
            beztnew[2] = v5
            # handle of next bezt
            bezt[0] = v3

            beztnew[3] = (prevbezt[3] + bezt[3]) / 2  # radius
            beztnew[4] = (prevbezt[4] + bezt[4]) / 2  # weight

            pvecs = [beztnew[0], beztnew[1], beztnew[2]]

        return bezier_points

    def subdivide_multi(self, factors):
        """分割した複数のbezierを返す。
        :param factors: 分割位置。
            factor<0ならv1方向に、factor>1ならv4方向に伸ばしたbezierを作る。
            この場合、v1v2v3v4には変更を加えない。
        :type factors: list[float] | tuple[float]
        :rtype: list[BezierCurve]
        """
        if not factors:
            raise ValueError('factorsが空')

        factors = list(factors)

        facmin = min(factors)
        facmax = max(factors)
        if facmin < 0.0 or facmax > 1.0:
            bez_bak = self.copy()
            if facmin < 0.0:
                self.slide(0, facmin)
                factors.append(0.0)
            if facmax > 1.0:
                self.slide(1, facmax)
                factors.append(1.0)
            factors = [facmin + (facmax - facmin) * t for t in factors]
            if 0.0 in factors:
                factors.remove(0.0)
            if 1.0 in factors:
                factors.remove(1.0)
        factors.sort()

        func = self.subdivide_multi_exec
        bezier_points = func(self[0], self[1], self[2], self[3], factors,
                             self.radiuses, self.weights)

        if facmin < 0.0 or facmax > 1.0:
            # self.slideで変更した物を戻す。
            self.copy_from(bez_bak)
            self.update_coefficients()

        bezier_curves = []
        for i in range(len(factors) + 1):
            p1 = bezier_points[i]
            p2 = bezier_points[i + 1]
            bez = BezierCurve(p1[1], p1[2], p2[0], p2[1],
                              [p1[3], p2[3]], [p1[4], p2[4]])
            bezier_curves.append(bez)

        return bezier_curves

    # intersect -----------------------------------------------------
    def intersect_line(self, p1, p2,
                       limit_line=True, limit_bezier=True):
        """XY座標のみ使い、bezierCurveと線分の交点を求め、tを返す。
        :param p1: 線分の片側。
        :type p1: Vector
        :param p2: 線分の片側。
        :type p2: Vector
        :param limit_line: 真ならp1-p2を線分、偽なら直線とみなす。
        :type limit_line: bool
        :param limit_bezier: 真なら交差範囲を 0.0 <= t <= 1.0 に制限する。
        :type limit_bezier: bool
        :rtype: float
        """

        v1, v2, v3, v4 = self[:]
        # 二次元に統一
        v1 = v1.to_2d()
        v2 = v2.to_2d()
        v3 = v3.to_2d()
        v4 = v4.to_2d()
        p1 = p1.to_2d()
        p2 = p2.to_2d()

        p12 = p2 - p1
        if p12.length < MIN_NUMBER:
            raise ValueError('Line is zero length')

        # translation. p1 -> origin, p12 -> X-Axis
        # p12をX軸、p1が原点になるように変換して、y=0となる場所を求める。
        theta = math.atan2(p12[1], p12[0])
        mat = Matrix.Rotation(-theta, 2)
        orig = mat * p1
        vec1 = mat * v1 - orig
        vec2 = mat * v2 - orig
        vec3 = mat * v3 - orig
        vec4 = mat * v4 - orig

        # get t value if y == 0. グラフでyが0となる時のtを求める。
        # coeffs = make_bezier_func_coefficients(vec1, vec2, vec3, vec4, 1)
        bez = BezierCurve(vec1, vec2, vec3, vec4)
        coeffs = bez.coefficients[1]
        roots = [0.0, 0.0, 0.0]
        num = solve_cubic(coeffs, roots)  # 三次方程式を解いてrootsに格納

        # bezier_func = make_bezier_func_2d(v1, v2, v3, v4)

        result = [t for t in roots[:num] if 0 <= t <= 1 or not limit_bezier]
        result.sort()
        if limit_line:
            result_tmp = []
            for t in result:
                # v = bezier_func(t) - p1
                v = self(t, size=2) - p1
                if p12.dot(v) >= 0.0:
                    proj = v.project(p12)
                    if proj.length <= p12.length:
                        result_tmp.append(t)
            result = result_tmp
        return result

    def intersect_bezier(self, other, min_length=1E-5):
        """XY座標のみ使い、bezierCurve同士の交点を求め、tを返す。
        必ず0<=t<=1となる。
        :type other: BezierCurve
        :param min_length: 閾値
        :type min_length: float
        :rtype: list[float]
        """

        def re_func(intersect_facs, bez1, bez2, t1, t2, t3, t4, min_length):
            """
            分割後の頂点で再帰をした場合、float型の所為で計算誤差が酷い。
            """
            bez1s = bez1.subdivide_multi((t1, t2))
            b1 = bez1s[1]
            bez2s = bez2.subdivide_multi((t3, t4))
            b2 = bez2s[1]

            # q1の凸形状を求める。
            b1_convex_indices = vam.convex_vecs_2d(b1)
            b1_convex = [b1[i] for i in b1_convex_indices]
            b1_num = len(b1_convex)

            # q2の凸形状を求める。
            b2_convex_indices = vam.convex_vecs_2d(b2)
            b2_convex = [b2[i] for i in b2_convex_indices]
            b2_num = len(b2_convex)

            if b1_num == b2_num == 4:
                collision = vam.collision_quad_quat_2d(*(b1 + b2))
            elif b1_num == 3 and b2_num == 4:
                collision = vam.collision_tri_quat_2d(*(b1_convex + b2_convex))
            elif b1_num == 4 and b2_num == 3:
                collision = vam.collision_tri_quat_2d(*(b2_convex + b1_convex))
            else:
                isect = vam.intersect_tri_tri_2d(*(b1_convex + b2_convex))
                if isect:
                    collision = True
                else:
                    inside = vam.inside_tri_tri_2d  # -1,0,1
                    collision = True if inside != 0 else False

            if collision:
                # 長さで終了判定
                # b1_length = bezier_length_2d(v1, v2, v3, v4, 10)  # 2D,10分割
                # b2_length = bezier_length_2d(v5, v6, v7, v8, 10)
                b1_length = b1.length(subdivide=10, size=2)  # 2D
                b2_length = b2.length(subdivide=10, size=2)
                # print(t1, t2, t3, t4)

                if b1_length < min_length or b2_length < min_length:
                    intersect_facs.append((t1, t2, t3, t4))
                    return

                # 分割
                if b1_length >= b2_length:
                    t5 = (t1 + t2) / 2
                    re_func(intersect_facs, bez1, bez2, t1, t5, t3, t4,
                            min_length)
                    re_func(intersect_facs, bez1, bez2, t5, t2, t3, t4,
                            min_length)
                else:
                    t5 = (t3 + t4) / 2
                    re_func(intersect_facs, bez1, bez2, t1, t2, t3, t5,
                            min_length)
                    re_func(intersect_facs, bez1, bez2, t1, t2, t5, t4,
                            min_length)

        intersect_facs = []
        t1 = 0.0  # b1
        t2 = 1.0  # b1
        t3 = 0.0  # b2
        t4 = 1.0  # b2

        re_func(intersect_facs, self, other, t1, t2, t3, t4, min_length)

        return intersect_facs


#####################################################################
# Generate BezierCurve from bpy.types.Spline
#####################################################################
def make_bezier_curve(spline, index):
    """
    indexとindex+1の位置のポイントで作成。
    """
    point_num = len(spline.bezier_points)
    bp1 = spline.bezier_points[index]
    bp2 = spline.bezier_points[index + 1 if index < point_num - 1 else 0]
    v1 = bp1.co
    v2 = bp1.handle_right
    v3 = bp2.handle_left
    v4 = bp2.co
    r1 = bp1.radius
    r2 = bp2.radius
    w1 = bp1.weight
    w2 = bp2.weight

    bez = BezierCurve(v1, v2, v3, v4, (r1, r2), (w1, w2))
    return bez


def make_bezier_curves(spline):
    bezier_curves = []

    point_num = len(spline.bezier_points)
    if spline.use_cyclic_u:
        seg_num = point_num
    else:
        seg_num = point_num - 1

    for i in range(seg_num):
        bez = make_bezier_curve(spline, i)
        bezier_curves.append(bez)

    return bezier_curves


#####################################################################
# Update bpy.types.BezierSplinePoint.

# Insert BezierCurves to bpy.types.Spline(bpy.types.BezierSplinePoint)
#####################################################################

def insert_bezier_curves(spline: 'Spline',
                         index: 'insert position same as list',
                         new_curves: 'list of BezierCurve'):
    """
    e.g. point0と1の間に追加したい場合は、indexに1を指定。
    基本的にbezier_curvesの先頭、後尾の値で既存のbezier_pointsの値を書き換える。
    if index in (0, len(bezier_points)):
        if spline.use_cyclic_u == True:
            len(new_curves)-1個追加。
            bezier_curvesの先端か終端の値でbezier_pointsの[-1]か[0]の値を変更する。
        else:
            len(new_curves)個追加。
    else:
        len(new_curves)-1個追加。
    """
    bezier_points = spline.bezier_points

    if index == 0 or index == len(bezier_points):
        if spline.use_cyclic_u:
            new_num = len(new_curves) - 1
        else:
            new_num = len(new_curves)
    else:
        new_num = len(new_curves) - 1

    if new_num == 0:
        return 0

    bezier_points.add(new_num)

    # データを新規分に複写。
    tgt_index = len(bezier_points) - 1
    src_index = tgt_index - new_num
    while tgt_index >= index + new_num:
        # tgtにsrcのデータを複写する
        tgt = bezier_points[tgt_index]
        src = bezier_points[src_index]
        for attr in dir(src):
            try:
                setattr(tgt, attr, getattr(src, attr))
            except:
                pass
        tgt_index -= 1
        src_index -= 1

    # indexの一個前のデータを全新規分に複写
    if index == 0:
        src = bezier_points[new_num]
    else:
        src = bezier_points[index - 1]
    for i in range(index, index + new_num):
        tgt = bezier_points[i]
        for attr in dir(src):
            try:
                setattr(tgt, attr, getattr(src, attr))
            except:
                pass

    # BezierCurveの値を適用。
    if index == 0 and not spline.use_cyclic_u:
        bp1_index = 0
    else:
        bp1_index = index - 1

    for i in range(len(new_curves)):
        p1 = bezier_points[bp1_index + i]
        if bp1_index + i + 1 == len(bezier_points):  # インデックス外
            # cyclicな箇所の最後
            p2 = bezier_points[0]
        else:
            p2 = bezier_points[bp1_index + i + 1]
        bez = new_curves[i]
        p1.co = bez[0]
        p1.handle_right = bez[1]
        p2.co = bez[3]
        p2.handle_left = bez[2]
        p1.radius, p2.radius = bez.radiuses
        p1.weight, p2.weight = bez.weights

    return new_num


#####################################################################
# Old Funcs
#####################################################################
# def insert_bezier_points(spline, index, num=1):
#     """
#     indexの位置にデフォルト値のbezierポイントをnum個追加。
#     例: 1と2の間に追加したい場合は、indexに2を指定。
#     """
#     bezier_points = spline.bezier_points
#     bezier_points.add(num)
#     # 初期値を確保
#     default_values = {}
#     for attr in dir(bezier_points[-1]):
#         val = getattr(bezier_points[-1], attr)
#         default_values[attr] = val
#     # データを複写。
#     """for i in range(len(bezier_points) - 1, index, -1):
#         # tgtにsrcのデータを複写する
#         src = bezier_points[i - num]
#         tgt = bezier_points[i]
#         for attr in dir(src):
#             val = getattr(src, attr)
#             try:
#                 setattr(tgt, attr, val)
#             except:
#                 pass
#     """
#     tgt_index = len(bezier_points) - 1
#     src_index = tgt_index - num
#     while tgt_index >= index + num:
#         # tgtにsrcのデータを複写する
#         tgt = bezier_points[tgt_index]
#         src = bezier_points[src_index]
#         for attr in dir(src):
#             try:
#                 setattr(tgt, attr, getattr(src, attr))
#             except:
#                 pass
#         tgt_index -= 1
#         src_index -= 1
#
#     # 初期値を反映。
#     for i in range(num):
#         for key, value in default_values.items():
#             try:
#                 setattr(bezier_points[index + i], key, value)
#             except:
#                 pass
#
#
# def subdivide_bezier_points(spline, index, factors):
#     """
#     indexの位置のsegmentを分割する。
#     index: 0 <= index <= (len(bezier_points) -1 if cyclic else len(bezier_points) - 2)
#     factors: list of t. e.g.[0.2, 0.7, 0,9] ソート済みである亊
#     cyclicな部分を分割する場合、index = len(bezier_points)
#     """
#     bezier_points = spline.bezier_points
#     if index == len(bezier_points) - 1:
#         # cyclicな箇所を分割する場合。
#         add_cyclic_segment = True
#     else:
#         add_cyclic_segment = False
#
#     num = len(factors)
#     insert_bezier_points(spline, index + 1, num)
#
#     # factorsを分割に使用する値に修正
#     # [1/4, 2/4, 3/4] -> [1/4, 1/3, 1/2]
#     subdivide_factors = []
#     prevfac = 0.0
#     for i in range(num):
#         if prevfac == 1.0:
#             fac = 0.0
#         else:
#             fac = (factors[i] - prevfac) / (1.0 - prevfac)
#         subdivide_factors.append(fac)
#         prevfac = factors[i]
#
#     if add_cyclic_segment:
#         bezt = bezier_points[0]
#         prevbezt = bezier_points[-1 - (num)]
#     else:
#         bezt = bezier_points[index + 1 + num]
#         prevbezt = bezier_points[index]
#
#     pvecs = [prevbezt.handle_left, prevbezt.co, prevbezt.handle_right]
#
#     for i in range(num):
#         factor = subdivide_factors[i]
#
#         beztnew = bezier_points[index + 1 + i]
#         prevbeztnew = bezier_points[index + i]
#
#         for attr in dir(bezt):
#             try:
#                 val = getattr(bezt, attr)
#                 setattr(beztnew, attr, val)
#             except:
#                 pass
#
#         v1 = pvecs[1].lerp(pvecs[2], factor)
#         v2 = pvecs[2].lerp(bezt.handle_left, factor)
#         v3 = bezt.handle_left.lerp(bezt.co, factor)
#
#         v4 = v1.lerp(v2, factor)
#         v5 = v2.lerp(v3, factor)
#
#         # change handle of prev beztnew
#         prevbeztnew.handle_right = v1
#         # new point
#         beztnew.handle_left = v4
#         beztnew.co = v4.lerp(v5, factor)
#         beztnew.handle_right = v5
#         # handle of next bezt
#         # この分岐は無くても問題なかった。
#         """if add_cyclic_segment and i == num - 1:
#             bezier_points[0].handle_left = v3
#         else:
#             bezt.handle_left = v3
#         """
#         bezt.handle_left = v3
#
#         beztnew.radius = (prevbezt.radius + bezt.radius) / 2
#         beztnew.weight = (prevbezt.weight + bezt.weight) / 2
#
#         pvecs = [beztnew.handle_left, beztnew.co, beztnew.handle_right]


# class BezTriple:
#     def __init__(self, bezt):
#         # 'FREE_ALIGN','AUTOMATIC','VECTOR','ALIGNED'
#         d = {'co': Vector(),
#              'handle_left': Vector(),
#              'handle_left_type': 'FREE_ALIGN',
#              'handle_right': Vector(),
#              'handle_right_type': Vector(),
#              'hide': False,
#              'select_control_point': False,
#              'select_left_handle': False,
#              'select_right_handle': False,
#              'weight': 0.0,
#              'radius': 0.0,
#              'tilt': 0.0}
#         if bezt:
#             for key in d.keys():
#                 val = getattr(bezt, key)
#                 if isinstance(val, Vector):
#                     val = val.copy()
#                 d[key] = val
#         for key, value in d.items():
#             setattr(self, key, value)
#         self.bezt = bezt
#
#     # 別名 hl, hr, hltype, hrtype
#     def _get_handle_left(self):
#         return self.handle_left
#     def _set_handle_left(self, val):
#         self.handle_left = val
#     hl = property(_get_handle_left, _set_handle_left)
#     def _get_handle_left_type(self):
#         return self.handle_left_type
#     def _set_handle_left_type(self, val):
#         self.handle_left_type = val
#     hltype = property(_get_handle_left_type, _set_handle_left_type)
#     def _get_handle_right(self):
#         return self.handle_right
#     def _set_handle_right(self, val):
#         self.handle_right = val
#     hr = property(_get_handle_right, _set_handle_right)
#     def _get_handle_right_type(self):
#         return self.handle_right_type
#     def _set_handle_right_type(self, val):
#         self.handle_right_type = val
#     hrtype = property(_get_handle_right_type, _set_handle_right_type)
#
#     # selectc, selectl, selectr
#     def _get_select_control_point(self):
#         return self.select_control_point
#     def _set_select_control_point(self, val):
#         self.select_control_point = val
#     selectc = property(_get_select_control_point, _set_select_control_point)
#     def _get_select_left_handle(self):
#         return self.select_left_handle
#     def _set_select_left_handle(self, val):
#         self.select_left_handle = val
#     selectl = property(_get_select_left_handle, _set_select_left_handle)
#     def _get_select_right_handle(self):
#         return self.select_right_handle
#     def _set_select_right_handle(self, val):
#         self.select_right_handle = val
#     selectr = property(_get_select_right_handle, _set_select_right_handle)
#
#
# class Spline(list):
#     def __init__(self, spline=None):
#         #super(Spline, self).__init__(l)
#         d = {'hide': False,
#              'type': 'POLY', # POLY,BEZIER,BSPLINE,CARDINAL,NURBS
#              'use_cyclic_u': False}
#         if spline:
#             for key in d.keys():
#                 d[key] = getattr(spline, key)
#         for key, value in d.items():
#             setattr(self, key, value)
#         if spline:
#             if self.type == 'BEZIER':
#                 for bezier_point in spline.bezier_points:
#                     bezt = BezTriple(bezier_point)
#                     self.append(bezt)
#             else:
#                 pass
#     # 別名 cyclic
#     def _get_cyclic(self):
#         return self.use_cyclic_u
#     def _set_cyclic(self, val):
#         self.use_cyclic_u = val
#     cyclic = property(_get_cyclic, _set_cyclic)
#
#
# class Splines(list):
#     def __init__(self, splines=None):
#         if splines:
#             for spline in splines:
#                 self.append(Spline(spline))
#
#
# def bezt_is_selected(curve, bezt):
#     if bezt.hide:
#         return False
#     if curve.show_handles:
#         if bezt.select_control_point or \
#            bezt.select_left_handle or bezt.select_right_handle:
#             return True
#     else:
#         if bezt.select_control_point:
#             return True
#     return False
#
#
# def make_bezier_func_3d(v1, v2, v3, v4, i=None):
#     """
#     v1: bezt1.co
#     v2: bezt1.handle_right
#     v3: bezt2.handle_left
#     v4: bezt2.co
#     i: index [0, 1, 2] (== x, y, z)
#     """
#     # tを渡してベクトルを返す関数を生成する。
#     def func(t):
#         def f(t, i):
#             val = (1 - t) ** 3 * v1[i] + \
#                   3 * (1 - t) ** 2 * t * v2[i] + \
#                   3 * (1 - t) * t ** 2 * v3[i] + \
#                   t ** 3 * v4[i]
#             return val
#         vec = Vector((f(t, 0), f(t, 1), f(t, 2)))
#         return vec
#     return func
#
#
# def make_bezier_func_2d(v1, v2, v3, v4):
#     """
#     v1: bezt1.co
#     v2: bezt1.handle_right
#     v3: bezt2.handle_left
#     v4: bezt2.co
#     """
#     # tを渡してベクトルを返す関数を生成する。
#     def func(t):
#         def f(t, i):
#             val = (1 - t) ** 3 * v1[i] + \
#                   3 * (1 - t) ** 2 * t * v2[i] + \
#                   3 * (1 - t) * t ** 2 * v3[i] + \
#                   t ** 3 * v4[i]
#             return val
#         vec = Vector((f(t, 0), f(t, 1)))
#         return vec
#     return func
#
#
# def make_bezier_func_1d(f1, f2, f3, f4):
#     def func(t):
#         val = (1 - t) ** 3 * f1 + \
#               3 * (1 - t) ** 2 * t * f2 + \
#               3 * (1 - t) * t ** 2 * f3 + \
#               t ** 3 * f4
#         return val
#     return func
#
#
# def make_bezier_func_coefficients(v1, v2, v3, v4, i):
#     """
#     v1: bezt1.co
#     v2: bezt1.handle_right
#     v3: bezt2.handle_left
#     v4: bezt2.co
#     i: index [0, 1, 2] (== x, y, z)
#     f(t) = a*t**3 + b*t**2 + c*t + d
#     """
#     a = 3 * v2[i] + v4[i] - 3 * v3[i] - v1[i]
#     b = 3 * (v1[i] - 2 * v2[i] + v3[i])
#     c = 3 * (v2[i] - v1[i])
#     d = v1[i]
#     return a, b, c, d
#
#
# def intersect_bezier_line(v1, v2, v3, v4, p1, p2,
#                           limit_line=True, limit_bezier=True):
#     """
#     XY座標でbezierCurveと線分の交点を求め、tを返す。 （二次元）
#     limit_line: True=p1-lv2を線分とみなす。 False=直線とみなす。
#     limit_bezier: True 0<=t<=1に制限する。
#     """
#
#     # 二次元に統一
#     v1 = v1.to_2d()
#     v2 = v2.to_2d()
#     v3 = v3.to_2d()
#     v4 = v4.to_2d()
#     p1 = p1.to_2d()
#     p2 = p2.to_2d()
#
#     p12 = p2 - p1
#     if p12.length < MIN_NUMBER:
#         raise ValueError('Line is zero length')
#
#     # translation. p1 -> origin, p12 -> X-Axis
#     # p12をX軸、p1が原点になるように変換して、y=0となる場所を求める。
#     theta = math.atan2(p12[1], p12[0])
#     mat = Matrix.Rotation(-theta, 2)
#     orig = mat * p1
#     vec1 = mat * v1 - orig
#     vec2 = mat * v2 - orig
#     vec3 = mat * v3 - orig
#     vec4 = mat * v4 - orig
#
#     # get t value if y == 0. グラフでyが0となる時のtを求める。
#     coeffs = make_bezier_func_coefficients(vec1, vec2, vec3, vec4, 1)
#     roots = [0.0, 0.0, 0.0]
#     num = solve_cubic(coeffs, roots)  # 三次方程式を解いてrootsに格納
#
#     bezier_func = make_bezier_func_2d(v1, v2, v3, v4)
#
#     result = [t for t in roots[:num] if 0 <= t <= 1 or not limit_bezier]
#     result.sort()
#     if limit_line:
#         result_tmp = []
#         for t in result:
#             v = bezier_func(t) - p1
#             if p12.dot(v) >= 0.0:
#                 proj = v.project(p12)
#                 if proj.length <= p12.length:
#                     result_tmp.append(t)
#         result = result_tmp
#     return result
#
#
# def intersect_bezier_bezier(v1, v2, v3, v4, v5, v6, v7, v8,
#                                min_length=1E-5):
#     """
#     XY座標でbezierCurve同士の交点を求め、tを返す。 （二次元）
#     """
#     def re_func(intersect_facs, bez1, bez2, t1, t2, t3, t4, min_length):
#         """
#         分割後の頂点で再帰をした場合、float型の所為で計算誤差が酷い。
#         何故2.5系に移るときにdouble型にしなかったのかと小一時間ry
#         """
#
#         # 再帰関数
#         #v1, v2, v3, v4 = bez1
#         #v5, v6, v7, v8 = bez2
#
#         subdiv_points1 = subdivide_bezier_multi(bez1[0], bez1[1], bez1[2], bez1[3],
#                                                 (t1, t2))
#         subdiv_points2 = subdivide_bezier_multi(bez2[0], bez2[1], bez2[2], bez2[3],
#                                                 (t3, t4))
#         v1 = subdiv_points1[1][1]
#         v2 = subdiv_points1[1][2]
#         v3 = subdiv_points1[2][0]
#         v4 = subdiv_points1[2][1]
#
#         v5 = subdiv_points2[1][1]
#         v6 = subdiv_points2[1][2]
#         v7 = subdiv_points2[2][0]
#         v8 = subdiv_points2[2][1]
#
#         b1 = (v1, v2, v3, v4)
#         b2 = (v5, v6, v7, v8)
#
#         # q1の凸形状を求める。
#         b1_convex_indices = vam.convex_vecs_2d(b1)
#         b1_convex = [b1[i] for i in b1_convex_indices]
#         b1_num = len(b1_convex)
#
#         # q2の凸形状を求める。
#         b2_convex_indices = vam.convex_vecs_2d(b2)
#         b2_convex = [b2[i] for i in b2_convex_indices]
#         b2_num = len(b2_convex)
#
#         if b1_num == b2_num == 4:
#             collision = vam.collision_quad_quat_2d(*(b1 + b2))
#         elif b1_num == 3 and b2_num == 4:
#             collision = vam.collision_tri_quat_2d(*(b1_convex + b2_convex))
#         elif b1_num == 4 and b2_num == 3:
#             collision = vam.collision_tri_quat_2d(*(b2_convex + b1_convex))
#         else:
#             isect = vam.intersect_tri_tri_2d(*(b1_convex + b2_convex))
#             if isect:
#                 collision = True
#             else:
#                 inside = vam.inside_tri_tri_2d  # -1,0,1
#                 collision = True if inside != 0 else False
#
#         if collision:
#             # 長さで終了判定
#             b1_length = bezier_length_2d(v1, v2, v3, v4, 10)  # 2D,10分割
#             b2_length = bezier_length_2d(v5, v6, v7, v8, 10)
#             #print(t1, t2, t3, t4)
#
#             if b1_length < min_length or b2_length < min_length:
#                 intersect_facs.append((t1, t2, t3, t4))
#                 return
#
#             # 分割
#             if b1_length >= b2_length:
#                 # q1を分割
#                 #b1a, b1b = subdivide_bezier(v1, v2, v3, v4, 0.5)
#                 t5 = (t1 + t2) / 2
#                 #re_func(intersect_facs, b1a, b2, t1, t5, t3, t4, min_length)
#                 #re_func(intersect_facs, b1b, b2, t5, t2, t3, t4, min_length)
#                 re_func(intersect_facs, bez1, bez2, t1, t5, t3, t4, min_length)
#                 re_func(intersect_facs, bez1, bez2, t5, t2, t3, t4, min_length)
#             else:
#                 # q2を分割
#                 #b2a, b2b = subdivide_bezier(v5, v6, v7, v8, 0.5)
#                 t5 = (t3 + t4) / 2
#                 #re_func(intersect_facs, b1, b2a, t1, t2, t3, t5, min_length)
#                 #re_func(intersect_facs, b1, b2b, t1, t2, t5, t4, min_length)
#                 re_func(intersect_facs, bez1, bez2, t1, t2, t3, t5, min_length)
#                 re_func(intersect_facs, bez1, bez2, t1, t2, t5, t4, min_length)
#
#     # 二次元に統一
#     v1 = v1.to_2d()
#     v2 = v2.to_2d()
#     v3 = v3.to_2d()
#     v4 = v4.to_2d()
#     v5 = v5.to_2d()
#     v6 = v6.to_2d()
#     v7 = v7.to_2d()
#     v8 = v8.to_2d()
#
#     b1 = (v1, v2, v3, v4)
#     b2 = (v5, v6, v7, v8)
#
#     intersect_facs = []
#     t1 = 0.0  # b1
#     t2 = 1.0  # b1
#     t3 = 0.0  # b2
#     t4 = 1.0  # b2
#
#     re_func(intersect_facs, b1, b2, t1, t2, t3, t4, min_length)
#
#     return intersect_facs
#
#
# def extend_bezier(v1, v2, v3, v4, factor):
#     """
#     factor: 0未満ならv1方向に伸ばす。0以上ならv4方向に伸ばす。
#     """
#     if factor >= 0.0:
#         t = 1.0 + factor
#     else:
#         t = factor
#     p = v2 + (v3 - v2) * t
#     v2_new = v1 + (v2 - v1) * t
#     v3_new = v4 + (v3 - v4) * (1 - t)
#     v_left = v2_new + (p - v2_new) * t
#     v_right = v3_new + (p - v3_new) * (1 - t)
#     v_co = v_left + (v_right - v_left) * t
#     if factor < 0.0:
#         return (v_co, v_right, v3_new, v4.copy())
#     else:
#         return (v1.copy(), v2_new, v_left, v_co)
#
#
# def subdivide_bezier(v1, v2, v3, v4, t:'0.0<=t<=1.0'):
#     """
#     tで分割したbezierを2つ返す。
#     t<0ならv1方向に、t>1ならv4方向に伸ばしたbezierを作る。この場合、v1v2v3v4には変更を加えない。
#     v1: bezt1.co
#     v2: bezt1.handle_right
#     v3: bezt2.handle_left
#     v4: bezt2.co
#     return: ((co, handle_right, handle_left, co), (co, handle_right,...))
#     """
#     p = v2 + (v3 - v2) * t
#     v2_new = v1 + (v2 - v1) * t
#     v3_new = v4 + (v3 - v4) * (1 - t)
#     v_left = v2_new + (p - v2_new) * t
#     v_right = v3_new + (p - v3_new) * (1 - t)
#     v_co = v_left + (v_right - v_left) * t
#     if 0.0 <= t <= 1.0:
#         return ((v1.copy(), v2_new, v_left, v_co),
#                 (v_co.copy(), v_right, v3_new, v4.copy()))
#     elif t < 0.0:
#         return ((v_co, v_left, v2_new, v1.copy()),
#                 (v1.copy(), v2.copy(), v3.copy(), v4.copy()))
#     else:
#         return ((v1.copy(), v2.copy(), v3.copy(), v4.copy()),
#                 (v4.copy(), v3_new, v_right, v_co))
#
# def subdivide_bezier_multi(v1, v2, v3, v4, factors:'0.0<=t<=1.0',
#                               radiuses=(1.0, 1.0), weights=(0.0, 0.0)):
#     """
#     返り値の仕様に留意。
#     factorの位置でbezierを分割したものを返す。len(factors)+2長の頂点を表すリスト。
#     [(handle_left, co, handle_right, radius, weight), ...]
#     """
#     num = len(factors)
#
#     bezier_points = []
#     for i in range(2 + num):
#         bezier_points.append([Vector(), Vector(), Vector(), 0.0, 0.0])
#     bezier_points[0][1] = v1
#     bezier_points[0][2] = v2
#     bezier_points[0][3] = radiuses[0]
#     bezier_points[0][4] = weights[0]
#     bezier_points[-1][0] = v3
#     bezier_points[-1][1] = v4
#     bezier_points[-1][3] = radiuses[1]
#     bezier_points[-1][4] = weights[1]
#
#     # factorsを分割に使用する値に修正
#     # [1/4, 2/4, 3/4] -> [1/4, 1/3, 1/2]
#     subdivide_factors = []
#     prevfac = 0.0
#     for i in range(num):
#         if prevfac == 1.0:
#             fac = 0.0
#         else:
#             fac = (factors[i] - prevfac) / (1.0 - prevfac)
#         subdivide_factors.append(fac)
#         prevfac = factors[i]
#
#     bezt = bezier_points[-1]
#     prevbezt = bezier_points[0]
#
#     pvecs = [prevbezt[0], prevbezt[1], prevbezt[2]]
#
#     for i in range(num):
#         factor = subdivide_factors[i]
#
#         beztnew = bezier_points[1 + i]
#         prevbeztnew = bezier_points[i]
#
#         """for attr in dir(bezt):
#             try:
#                 val = getattr(bezt, attr)
#                 setattr(beztnew, attr, val)
#             except:
#                 pass
#         """
#
#         v1 = pvecs[1].lerp(pvecs[2], factor)
#         v2 = pvecs[2].lerp(bezt[0], factor)
#         v3 = bezt[0].lerp(bezt[1], factor)
#
#         v4 = v1.lerp(v2, factor)
#         v5 = v2.lerp(v3, factor)
#
#         # change handle of prev beztnew
#         prevbeztnew[2] = v1
#         # new point
#         beztnew[0] = v4
#         beztnew[1] = v4.lerp(v5, factor)
#         beztnew[2] = v5
#         # handle of next bezt
#         # この分岐は無くても問題なかった。
#         """if add_cyclic_segment and i == num - 1:
#             bezier_points[0].handle_left = v3
#         else:
#             bezt.handle_left = v3
#         """
#         bezt[0] = v3
#
#
#         beztnew[3] = (prevbezt[3] + bezt[3]) / 2  # radius
#         beztnew[4] = (prevbezt[4] + bezt[4]) / 2  # weight
#
#         pvecs = [beztnew[0], beztnew[1], beztnew[2]]
#
#     return bezier_points
#
#
# def bezier_length_2d(v1, v2, v3, v4, subdivide=100):
#     def dt(t, i):
#         """bezierCurveの座標を求める式 x = f(t)を微分
#         i: (0, 1, 2) == (x, y, z)
#         """
#         a = -v1[i] + 3 * v2[i] - 3 * v3[i] + v4[i]
#         b = 3 * (v1[i] - 2 * v2[i] + v3[i])
#         c = 3 * (-v1[i] + v2[i])
#         return 3 * a * t ** 2 + 2 * b * t + c
#
#     def dt_length_2D(t):
#         return math.sqrt(dt(t, 0) ** 2 + dt(t, 1) ** 2)
#
#     return composite_simpson(dt_length_2D, 0, 1.0, subdivide)
#
#
# def bezier_length_3d(v1, v2, v3, v4, subdivide=100):
#     """
#     f(t) = a*t**3 + b*t**2 + c*t + d
#     """
#     """
#     a = 3 * v2[i] + v4[i] - 3 * v3[i] - v1[i]
#     b = 3 * (v1[i] - 2 * v2[i] + v3[i])
#     c = 3 * (v2[i] - v1[i])
#     d = v1[i]
#     """
#     def dt(t, i):
#         """bezierCurveの座標を求める式 x = f(t)を微分
#         i: (0, 1, 2) == (x, y, z)
#         """
#         a = -v1[i] + 3 * v2[i] - 3 * v3[i] + v4[i]
#         b = 3 * (v1[i] - 2 * v2[i] + v3[i])
#         c = 3 * (-v1[i] + v2[i])
#         return 3 * a * t ** 2 + 2 * b * t + c
#
#     def dt_length_3D(t):
#         return math.sqrt(dt(t, 0) ** 2 + dt(t, 1) ** 2 + dt(t, 2) ** 2)
#
#     return composite_simpson(dt_length_3D, 0, 1.0, subdivide)
#
#
# def bezier_length(v1, v2, v3, v4, subdivide=100, size=3):
#     """汎用。"""
#     if size == 3:
#         length = bezier_length_3d(v1, v2, v3, v4, subdivide)
#     else:
#         length = bezier_length_2d(v1, v2, v3, v4, subdivide)
#     return length
#
#
# def bezier_spline_length(curve, spline, subdivide=100, size=3, mat=None):
#     """
#     spline(bezier type)の長さを求める
#     """
#     if mat is None:
#         mat = Matrix.Scale(1.0, 4)
#     bezts = spline.bezier_points
#     length = 0.0
#     for i in range(-1 if spline.use_cyclic_u else 0, len(bezts) - 1):
#         prevbezt = bezts[i]
#         bezt = bezts[i + 1]
#         if bezt_is_selected(curve, prevbezt) and bezt_is_selected(curve, bezt):
#             v1 = prevbezt.co * mat
#             v2 = prevbezt.handle_right * mat
#             v3 = bezt.handle_left * mat
#             v4 = bezt.co * mat
#             if size == 3:
#                 length += bezier_length_3d(v1, v2, v3, v4, subdivide)
#             else:
#                 length += bezier_length_2d(v1, v2, v3, v4, subdivide)
#     return length


#####################################################################
# Bezier Surface (未完成)
#####################################################################

class CoonsPatch:
    def __init__(self, p0, p1, q0, q1):
        # (U,V)
        #   (0,1)      (1,1)
        #        __q1__
        #    p0 |      | p1
        #       |__q0__|
        #   (0,0)      (1,0)
        self.p0 = p0
        self.p1 = p1
        self.q0 = q0
        self.q1 = q1

    def __call__(self, u, v):
        p0 = self.p0
        p1 = self.p1
        q0 = self.q0
        q1 = self.q1

        vec = (1 - u) * p0(v) + u * p1(v) + (1 - v) * q0(u) + v * q1(u) \
              - (1 - u) * (1 - v) * p0(0) - u * (1 - v) * p1(0) - (
                                                                  1 - u) * v * p0(
            1) - u * v * p1(1)
        return vec


def bernstein(n, i, t):
    x = math.factorial(n) / (math.factorial(n - i) * math.factorial(i))
    return x * t ** i * (1 - t) ** (n - i)


class GregoryPatch:
    # [i j k]
    # 030    130    230    330
    #        120    220
    # 020  121        221  320
    #
    # 010  111        211  310
    #        110    210
    # 000    100    200    300

    def __init__(self, *args, **kw):
        # *args: BezierSplinePoint * 4 or Vector * 12 or Vector * 20
        # **kw: correct = True or False
        correct = kw.get('correct', True)
        if len(args) in (4, 12):
            if len(args) == 4:
                b1, b2, b3, b4 = args
                p010, p000, p100 = b1.handle_left, b1.co, b1.handle_right
                p200, p300, p310 = b2.handle_left, b2.co, b2.handle_right
                p320, p330, p230 = b3.handle_left, b3.co, b3.handle_right
                p130, p030, p020 = b4.handle_left, b4.co, b4.handle_right
            else:
                (p000, p100, p200, p300, p310, p320, p330, p230, p130, p030,
                 p020, p010) = args
            p110, p210 = self.calc_inside(p000, p100, p200, p300, p310, p330,
                                          p230, p130, p030, p010, correct)
            p211, p221 = self.calc_inside(p300, p310, p320, p330, p230, p030,
                                          p020, p010, p000, p200, correct)
            p220, p120 = self.calc_inside(p330, p230, p130, p030, p020, p000,
                                          p100, p200, p300, p320, correct)
            p121, p111 = self.calc_inside(p030, p020, p010, p000, p100, p300,
                                          p310, p320, p330, p130, correct)

        for key, value in locals().items():
            if re.match('p\d\d\d', key):
                setattr(self, key, value)
        """self.p000 = p000
        self.p100 = p100
        self.p200 = p200
        self.p300 = p300
        self.p010 = p010
        self.p110 = p110
        self.p210 = p210
        self.p310 = p310
        self.p020 = p020
        self.p120 = p120
        self.p220 = p220
        self.p320 = p320
        self.p030 = p030
        self.p130 = p130
        self.p230 = p230
        self.p330 = p330
        self.p111 = p111
        self.p211 = p211
        self.p121 = p121
        self.p221 = p221
        """

    def calc_inside(self, p00, p10, p20, p30,
                    p31, p33, p23, p13, p03, p01, correct):
        # 内部制御点の計算
        a1 = p01 - p00
        a2 = p31 - p30
        c1 = p10 - p00
        c2 = p20 - p10
        c3 = p30 - p20
        length = c1.length + c2.length + c3.length

        v1 = a1.lerp(a2, c1.length / length)
        if correct:
            v1 *= (p13 - p10).length / (p03 - p00).length
        p11 = v1 + p10

        v2 = a1.lerp(a2, (c1.length + c2.length) / length)
        if correct:
            v2 *= (p23 - p20).length / (p33 - p30).length
        p21 = v2 + p20

        return p11, p21

    def __call__(self, u, v):
        def q(self, i, j, u, v):
            if i not in (1, 2) or j not in (1, 2):
                return getattr(self, 'p{0}{1}0'.format(i, j))
            elif u == 0.0 or u == 1.0 or v == 0.0 or v == 1.0:
                return Vector()
            elif i == 1 and j == 1:
                f = u * self.p110 + v * self.p111
                return f / (u + v)
            elif i == 1 and j == 2:
                f = u * self.p120 + (1 - v) * self.p121
                return f / (u + (1 - v))
            elif i == 2 and j == 1:
                f = (1 - u) * self.p210 + v * self.p211
                return f / ((1 - u) + v)
            elif i == 2 and j == 2:
                f = (1 - u) * self.p220 + (1 - v) * self.p221
                return f / ((1 - u) + (1 - v))

        vec = Vector()
        for i in range(4):
            for j in range(4):
                f = bernstein(3, i, u) * bernstein(3, j, v)
                vec += f * q(self, i, j, u, v)
        return vec

    def convert_mesh(self, subdiv):
        vecs = []
        faces = []
        # vecs
        for i in range(subdiv + 1):
            for j in range(subdiv + 1):
                u = 1.0 / subdiv * i
                v = 1.0 / subdiv * j
                vec = self(u, v)
                vecs.append(vec)
        # faces
        for i in range(subdiv):
            for j in range(subdiv):
                f1 = i * (subdiv + 1) + j
                f2 = f1 + 1
                f3 = (i + 1) * (subdiv + 1) + j + 1
                f4 = f3 - 1
                face = [f1, f2, f3, f4]
                faces.append(face)
        return vecs, faces


class GregoryPatchTri:
    #             p2
    #        /          \
    #      e2p f2p   f2m e2m
    #    e0m f0m       f1p e1p
    #   /     f0p    f1m      \
    # p0 ---- e0p -- e1m ----- p1

    def __init__(self, *args):
        # *args: BezierSplinePoint * 3 or Vector * 9 or Vector * 15
        # p0から反時計回り、fは最後
        if len(args) in (3, 9):
            if len(args) == 3:
                b1, b2, b3 = args
                e0m, p0, e0p = b1.handle_left, b1.co, b1.handle_right
                e1m, p1, e1p = b2.handle_left, b2.co, b2.handle_right
                e2m, p2, e2p = b3.handle_left, b3.co, b3.handle_right
            else:
                p0, e0p, e1m, p1, e1p, e2m, p2, e2p, e0m = args
            f0p, f1m = self.calc_inside(p0, e0p, e1m, p1, e1p, p2, e0m)
            f1p, f2m = self.calc_inside(p1, e1p, e2m, p2, e2p, p0, e1m)
            f2p, f0m = self.calc_inside(p2, e2p, e0m, p0, e0p, p1, e2m)
        else:
            (p0, e0p, e1m, p1, e1p, e2m, p2, e2p, e0m,
             f0p, f1m, f1p, f2m, f2p, f0m) = args
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.e0m = e0m
        self.e1m = e1m
        self.e2m = e2m
        self.e0p = e0p
        self.e1p = e1p
        self.e2p = e2p
        self.f0m = f0m
        self.f1m = f1m
        self.f2m = f2m
        self.f0p = f0p
        self.f1p = f1p
        self.f2p = f2p

    def calc_inside(self, p0, e0p, e1m, p1, e1p, p2, e0m):
        # 問題あり。まともな内部制御点が生成されない。
        a1 = e0m - p0
        a2 = e1p - p1
        c1 = e0p - p0
        c2 = e1m - e0p
        c3 = p1 - e1m
        length = c1.length + c2.length + c3.length

        v1 = a1.lerp(a2, c1.length / length)
        f0p = v1 + e0p
        # correctは今の所無し

        v2 = a1.lerp(a2, c1.length / length)
        f1m = v2 + e1m

        return f0p, f1m

    def __call__(self, u, v, w):
        # u + v + w == 1.0
        f0 = (w * self.f0m + v * self.f0p) / (v + w)
        f1 = (u * self.f1m + w * self.f1p) / (w + u)
        f2 = (v * self.f2m + u * self.f2p) / (u + v)
        vec = u ** 3 * self.p0 + v ** 3 * self.p1 + w ** 3 * self.p2 \
              + 3 * u * v * (u + v) * (u * self.e0p + v * self.e1m) \
              + 3 * v * w * (v + w) * (v * self.e1p + w * self.e2m) \
              + 3 * w * u * (w + u) * (w * self.e2p + u * self.e0m) \
              + 12 * u * v * w * (u * f0 + v * f1 + w * f2)
        return vec


# Bezier Triple
def bernstein_tri(n, i, j, k, u, v):
    f = math.factorial(i) * math.factorial(j) * math.factorial(k)
    return math.factorial(n) / f * u ** i * v ** j * (1 - u - v) ** k


class BezierSurfaceTri:
    def __init__(self, p300, p201, p210, p102, p111, p120,
                 p003, p012, p021, p030):
        self.points = {}
        self.points[(3, 0, 0)] = p300
        self.points[(2, 0, 1)] = p201
        self.points[(2, 1, 0)] = p210
        self.points[(1, 0, 2)] = p102
        self.points[(1, 1, 1)] = p111
        self.points[(1, 2, 0)] = p120
        self.points[(0, 0, 3)] = p003
        self.points[(0, 1, 2)] = p012
        self.points[(0, 2, 1)] = p021
        self.points[(0, 3, 0)] = p030

    def __call__(self, u, v):
        #          p300
        #       p201  p210
        #    p102  p111  p120
        # p003  p012  p021  p030
        #
        vec = Vector()
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    if i + j + k != 3:
                        continue
                    f = bernstein_tri(3, i, j, k, u, v)
                    vec += f * self.points[(i, j, k)]

### テスト的な物 終了###
