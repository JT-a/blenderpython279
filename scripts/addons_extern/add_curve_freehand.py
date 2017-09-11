# Copyright (c) 2016, DWANGO Co., Ltd.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

bl_info = {
    "name": "Freehand Curve Drawing",
    "author": "ideasman42",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "View3d -> Options -> Curve Options, Shift-LMB to Draw",
    "description": "Edit-mode curve sketching",
    "warning": "",
    "wiki_url": "",
    "category": "Add Curve",
}

# Self contained Python3 module to calculate bezier curves from an array of points.
# This script is in 2 parts, first the module (no Blender deps), then the addon
# (could be split out, keeping a single file for now).

USE_ADDON = True

# ----------------------------------------------------------------------------
# points_to_bezier_3d.py

from collections import namedtuple
import math

# constants
DBL_MAX = 1.79769e+308
DBL_NAN = float("nan")

__all__ = (
    "calc_spline",
)

CornerPoint = namedtuple(
    'CornerPoint',
    ('point',
     'original_index',
     'sharpness',
     'is_corner',
     ))

CornerParams = namedtuple(
    'CornerParams',
    ('sample_num_min',
     'dist_min',
     'dist_max',
     'dist_min_squared',
     'dist_max_squared',
     'angle_max',
     ))

Cubic = namedtuple(
    'Cubic',
    ('p0',
     'p1',
     'p2',
     'p3',
     ))


# Typing:
try:
    import typing
except ImportError:
    typing = None

if typing is not None:
    from typing import (
        List,
        Sequence,
        Tuple,
    )
else:
    # Stub out typing for pypy

    Sequence = {None: None, Cubic: None, int: None, float: None}
    Vector = None
    Vector = Sequence[float]
    List = {None: None, float: None, int: None, Cubic: None}
    Tuple = {None: None, (float, int): None}

Vector = Sequence[float]


# ----------------------------------------------------------------------------
# Mini Math Lib (using tuples)

def len_vnvn(v0, v1):
    return math.sqrt(len_squared_vnvn(v0, v1))


def len_vn(v0):
    return math.sqrt(len_squared_vn(v0))


def len_squared_vnvn(v0, v1):
    d = sub_vnvn(v0, v1)
    return len_squared_vn(d)


def len_squared_vn(v0):
    return dot_vnvn(v0, v0)


def normalized_vn(v0):
    d = len_squared_vn(v0)
    if d != 0:
        d = math.sqrt(d)
        return tuple(a / d for a in v0)
    else:
        return tuple(0.0 for a in v0)


def mul_vn_fl(v0, f):
    return tuple(a * f for a in v0)


def dot_vnvn(v0, v1):
    return sum(a * b for a, b in zip(v0, v1))


def add_vnvn(v0, v1):
    return tuple(a + b for a, b in zip(v0, v1))


def sub_vnvn(v0, v1):
    return tuple(a - b for a, b in zip(v0, v1))


def negated_vn(v0):
    return tuple(-a for a in v0)


def add_vn_index(v0: Vector, i: int, value: float) -> Vector:
    return v0[:i] + ((v0[i] + value),) + v0[i + 1:]

# End math lib
# ----------------------------------------------------------------------------


def cubic_evaluate(cubic: Cubic, t: float) -> Vector:
    s = 1.0 - t

    p01 = add_vnvn(mul_vn_fl(cubic.p0, s), mul_vn_fl(cubic.p1, t))
    p12 = add_vnvn(mul_vn_fl(cubic.p1, s), mul_vn_fl(cubic.p2, t))
    p23 = add_vnvn(mul_vn_fl(cubic.p2, s), mul_vn_fl(cubic.p3, t))

    # now reuse the variables already used

    p01 = add_vnvn(mul_vn_fl(p01, s), mul_vn_fl(p12, t))   # l2
    p23 = add_vnvn(mul_vn_fl(p12, s), mul_vn_fl(p23, t))  # r1

    # l3-r0
    p12 = add_vnvn(mul_vn_fl(p01, s), mul_vn_fl(p23, t))
    return p12


def cubic_calc_point(cubic: Cubic, t: float) -> Vector:
    s = 1.0 - t
    # return cubic.p0 * s * s * s + 3.0 * t * s * (s * cubic.p1 + t * cubic.p2) + t * t * t * cubic.p3
    t3 = t * t * t
    s3 = s * s * s
    return tuple(p0 * s3 + 3.0 * t * s * (s * p1 + t * p2) + t3 * p3
                 for p0, p1, p2, p3 in zip(cubic.p0, cubic.p1, cubic.p2, cubic.p3))


def cubic_calc_speed(cubic: Cubic, t: float) -> Vector:
    s = 1.0 - t
    # return 3.0 * ((cubic.p1 - cubic.p0) * s * s + 2.0 * (cubic.p2 - cubic.p0) * s * t + (cubic.p3 - cubic.p2) * t * t)
    t2 = t * t
    s2 = s * s
    return tuple(3.0 * ((p1 - p0) * s2 + 2.0 * (p2 - p0) * s * t + (p3 - p2) * t2)
                 for p0, p1, p2, p3 in zip(cubic.p0, cubic.p1, cubic.p2, cubic.p3))


def cubic_calc_acceleration(cubic: Cubic, t: float) -> Vector:
    s = 1.0 - t
    # return 6.0 * ((cubic.p2 - 2.0 * cubic.p1 + cubic.p0) * s + (cubic.p3 - 2.0 * cubic.p2 + cubic.p1) * t)
    return tuple(6.0 * ((p2 - 2.0 * p1 + p0) * s + (p3 - 2.0 * p2 + p1) * t)
                 for p0, p1, p2, p3 in zip(cubic.p0, cubic.p1, cubic.p2, cubic.p3))


def cubic_calc_error(
        cubic: Cubic,
        points_offset: Sequence[Vector],
        points_offset_len: int,
        u: float
) -> Tuple[float, int]:
    '''
    Returns a 'measure' of the maximal discrepancy of the points specified
    by points_offset from the corresponding cubic(u[]) points.
    '''

    error_sq_max = 0.0
    error_index = 0

    for i in range(1, points_offset_len - 1):
        pt_eval = cubic_evaluate(cubic, u[i])
        pt_real = points_offset[i]

        err_sq = len_squared_vnvn(pt_real, pt_eval)
        if err_sq >= error_sq_max:
            error_sq_max = err_sq
            error_index = i
    return error_sq_max, error_index


def sq(a):
    return a * a


def B1(u: float) -> float:
    tmp = 1.0 - u
    return 3.0 * u * tmp * tmp


def B2(u: float) -> float:
    return 3.0 * u * u * (1.0 - u)


def B0plusB1(u: float) -> float:
    tmp = 1.0 - u
    return tmp * tmp * (1.0 + 2.0 * u)


def B2plusB3(u: float) -> float:
    return u * u * (3.0 - 2.0 * u)


def is_almost_zero(val, eps=1e-8):
    return -eps < val and val < eps


def points_calc_center_weighted(
        points_offset: Sequence[Vector],
        points_offset_len: int,
) -> Vector:
    """
    Calculate a center that compensates for point spacing.
    """

    w_tot = 0.0
    center = (0.0,) * len(points_offset[0])

    i_prev = points_offset_len - 2
    i_curr = points_offset_len - 1

    w_prev = len_vnvn(points_offset[i_prev], points_offset[i_curr])

    for i_next in range(points_offset_len):
        w_next = len_vnvn(points_offset[i_curr], points_offset[i_next])

        w = w_prev + w_next
        w_tot += w

        center = add_vnvn(center, mul_vn_fl(points_offset[i_curr], w))

        i_prev = i_curr
        i_curr = i_next

        w_prev = w_next

    if w_tot != 0.0:
        center = mul_vn_fl(center, 1.0 / w_tot)

    return center


def cubic_from_points(
        points_offset: Sequence[Vector],
        points_offset_len: int,
        u_prime: Vector,
        tan_l: Vector,
        tan_r: Vector,
) -> Cubic:

    # Point Pairs
    A = [[None, None] for i in range(points_offset_len)]

    p0 = points_offset[0]
    p3 = points_offset[points_offset_len - 1]

    # print(tan_l, tan_r)
    for i in range(points_offset_len):
        A[i][0] = mul_vn_fl(tan_l, B1(u_prime[i]))
        A[i][1] = mul_vn_fl(tan_r, B2(u_prime[i]))
        # print(A[i])

    # double X[2], C[2][2]
    X = [0.0, 0.0]
    C = [[0, 0], [0, 0]]

    for i in range(points_offset_len):
        C[0][0] += dot_vnvn(A[i][0], A[i][0])
        C[0][1] += dot_vnvn(A[i][0], A[i][1])
        C[1][1] += dot_vnvn(A[i][1], A[i][1])

        C[1][0] = C[0][1]

        tmp = sub_vnvn(points_offset[i], mul_vn_fl(p0, B0plusB1(u_prime[i])) + mul_vn_fl(p3, B2plusB3(u_prime[i])))
        X[0] += dot_vnvn(A[i][0], tmp)
        X[1] += dot_vnvn(A[i][1], tmp)

    # double's
    detC0C1 = C[0][0] * C[1][1] - C[0][1] * C[1][0]
    detC0X = X[1] * C[0][0] - X[0] * C[0][1]
    detXC1 = X[0] * C[1][1] - X[1] * C[0][1]

    if is_almost_zero(detC0C1):
        detC0C1 = C[0][0] * C[1][1] * 10e-12
        # print(detC0C1, C[1][1], C[0][0])

    alpha_l = detXC1 / detC0C1
    alpha_r = detC0X / detC0C1

    # The problem that the stupid values for alpha dare not put only when we realize
    # that the sign and wrong, but even if the values are too high.
    # But how do you evaluate it?

    # Meanwhile, we should ensure that 'These values are sometimes so' only problems absurd
    # of approximation and not for bugs in the code.

    if (alpha_l < 0.0 or alpha_r < 0.0):
        alpha_l = alpha_r = len_vnvn(p0, p3) / 3.0

    p1 = sub_vnvn(p0, mul_vn_fl(tan_l, alpha_l))
    p2 = add_vnvn(p3, mul_vn_fl(tan_r, alpha_r))

    # ------------------------------------
    # Clamping (we could make it optional)
    center = points_calc_center_weighted(points_offset, points_offset_len)

    dist_sq_max = 0.0
    for i_curr in range(points_offset_len):
        # dist_sq_max = max(dist_sq_max, len_squared_vnvn(center, points_offset[i_curr]))

        # Use a scaled distance instead
        ofs = sub_vnvn(points_offset[i_curr], center)
        mul_vn_fl(ofs, 3.0)
        dist_sq_max = max(dist_sq_max, len_squared_vn(ofs))
        del ofs
    # print(dist_sq_max, len_squared_vnvn(center, p1), len_squared_vnvn(center, p2))
    p1_dist_sq = len_squared_vnvn(center, p1)
    p2_dist_sq = len_squared_vnvn(center, p2)
    if (p1_dist_sq > dist_sq_max or
            p2_dist_sq > dist_sq_max):

        alpha_l = alpha_r = len_vnvn(p0, p3) / 3.0
        p1 = sub_vnvn(p0, mul_vn_fl(tan_l, alpha_l))
        p2 = add_vnvn(p3, mul_vn_fl(tan_r, alpha_r))

        p1_dist_sq = len_squared_vnvn(center, p1)
        p2_dist_sq = len_squared_vnvn(center, p2)
        # print("Clamp")

    # clamp within the 3x radius
    if p1_dist_sq > dist_sq_max:
        p1 = sub_vnvn(p1, center)
        p1 = mul_vn_fl(p1, math.sqrt(dist_sq_max) / math.sqrt(p1_dist_sq))
        p1 = add_vnvn(p1, center)
    if p2_dist_sq > dist_sq_max:
        p2 = sub_vnvn(p2, center)
        p2 = mul_vn_fl(p2, math.sqrt(dist_sq_max) / math.sqrt(p2_dist_sq))
        p2 = add_vnvn(p2, center)

    del center, dist_sq_max, p1_dist_sq, p2_dist_sq

    # end clamping
    # ------------

    cubic = Cubic(
        # TThickPoint ? - vector is fine too
        tuple(p0),
        tuple(p1),
        tuple(p2),
        tuple(p3),
    )

    del A

    return cubic


def points_calc_coord_length(
        points_offset: Sequence[Vector],
        points_offset_len: int,
) -> List[float]:

    u = [None] * points_offset_len
    u[0] = 0.0
    for i in range(1, points_offset_len):
        u[i] = u[i - 1] + len_vnvn(points_offset[i], points_offset[i - 1])
    # assert(!is_almost_zero(u[points_offset_len - 1]))
    w = u[points_offset_len - 1]
    for i in range(1, points_offset_len):
        u[i] = u[i] / w
    return u


# ----------------------------------------------------------------------------
#
def cubic_find_root(
        cubic: Cubic,
        p: Vector,
        u: float
) -> float:
    """
    Newton-Raphson Method.
    """
    # all vectors
    q0U = cubic_calc_point(cubic, u)
    q1U = cubic_calc_speed(cubic, u)
    q2U = cubic_calc_acceleration(cubic, u)

    # return u - ((q0U - p) * q1U) / (q1U.length_squared() + (q0U - p) * q2U)
    try:
        return u - dot_vnvn(sub_vnvn(q0U, p), q1U) / (len_squared_vn(q1U) + dot_vnvn(sub_vnvn(q0U, p), q2U))
    except ZeroDivisionError:
        return DBL_NAN


def cubic_reparameterize(
        cubic: Cubic,
        points_offset: Sequence[Vector],
        points_offset_len: int,
        u: Vector,
) -> List[float]:
    """
    Recalculate the values of u[] based on the Newton Raphson method
    """

    # double *u_prime = new double[points_offset_len]
    u_prime = [None] * points_offset_len

    for i in range(points_offset_len):
        u_prime[i] = cubic_find_root(cubic, points_offset[i], u[i])
        if not math.isfinite(u_prime[i]):
            del u_prime  # free
            return None

    u_prime.sort()

    if u_prime[0] < 0.0 or u_prime[points_offset_len - 1] > 1.0:
        del u_prime
        return None

    assert(u_prime[0] >= 0.0)
    assert(u_prime[points_offset_len - 1] <= 1.0)

    return u_prime

# ----------------------------------------------------------------------------


def fit_cubic_to_points(
        # Points
        points_offset: Sequence[Vector],
        points_offset_len: int,
        tan_l: Vector,
        tan_r: Vector,
        error_threshold: float,
        # fill in this value
        r_cubic_array: Sequence[Cubic],
):

    iteration_max = 4  # const (make configurable?)
    error_sq = sq(error_threshold)

    if points_offset_len == 2:
        dist = len_vnvn(points_offset[0], points_offset[1]) / 3.0
        r_cubic_array.append(
            Cubic(points_offset[0],
                  sub_vnvn(points_offset[0], (mul_vn_fl(tan_l, dist))),
                  add_vnvn(points_offset[1], (mul_vn_fl(tan_r, dist))),
                  points_offset[1],
                  )
        )
        return

    u = points_calc_coord_length(points_offset, points_offset_len)

    cubic = cubic_from_points(points_offset, points_offset_len, u, tan_l, tan_r)

    error_sq_max, split_index = cubic_calc_error(cubic, points_offset, points_offset_len, u)

    if (error_sq_max < error_sq):
        del u
        r_cubic_array.append(cubic)
        return

    else:
        u_prime = None
        for i in range(iteration_max):
            # delete u_prime
            u_prime = cubic_reparameterize(cubic, points_offset, points_offset_len, u)
            if u_prime is None:
                break

            del cubic
            cubic = cubic_from_points(points_offset, points_offset_len, u_prime, tan_l, tan_r)
            error_sq_max, split_index = cubic_calc_error(cubic, points_offset, points_offset_len, u_prime)
            if error_sq_max < error_sq:
                del u_prime  # free
                del u  # free
                r_cubic_array.append(cubic)
                return

            del u  # free
            u = u_prime

    del u  # free
    del cubic  # free

    # XXX check splinePoint is not an endpoint???
    #
    # This assert happens sometimes... Look into it but disable for now. campbell!
    # assert(split_index > 1)

    assert(split_index < points_offset_len)
    if points_offset[split_index - 1] == points_offset[split_index + 1]:
        tan_center = normalized_vn(sub_vnvn(points_offset[split_index], points_offset[split_index + 1]))
    else:
        tan_center = normalized_vn(sub_vnvn(points_offset[split_index - 1], points_offset[split_index + 1]))

    fit_cubic_to_points(
        points_offset, split_index + 1,
        tan_l, tan_center, error_threshold, r_cubic_array)
    fit_cubic_to_points(
        points_offset[split_index:], points_offset_len - split_index,
        tan_center, tan_r, error_threshold, r_cubic_array)


# ----------------------------------------------------------------------------
# cornerdetector.cpp

def AlgorithmPointI_new(point, original_index):
    return CornerPoint(
        point=tuple((int(a) for a in point)),
        original_index=original_index,
        sharpness=0.0,
        is_corner=False,
    )


def corners_is_corner_ok(
        i_curr: int,
        i_prev: int,
        i_next: int,
        *,
        corner_params: CornerParams,
        corner_points: Vector
) -> bool:
    """
    Check if i_curr and a possible corner and if so prejudice "acuity"
    """

    if (i_curr < 0 or i_curr >= len(corner_points) or
            i_prev < 0 or i_prev >= len(corner_points) or
            i_next < 0 or i_next >= len(corner_points)):

        return False

    a = sub_vnvn(corner_points[i_curr].point, corner_points[i_next].point)
    b = sub_vnvn(corner_points[i_curr].point, corner_points[i_prev].point)
    c = sub_vnvn(corner_points[i_next].point, corner_points[i_prev].point)

    # double
    norm2_a = len_squared_vn(a)
    norm2_b = len_squared_vn(b)

    if ((not (norm2_a <= corner_params.dist_max_squared and norm2_a >= corner_params.dist_min_squared)) or
            (not (norm2_b <= corner_params.dist_max_squared and norm2_b >= corner_params.dist_min_squared))):

        return False

    norm2_c = len_squared_vn(c)
    cosine_of_alpha = (
        (norm2_a + norm2_b - norm2_c) /
        math.sqrt(4.0 * norm2_a * norm2_b))

    if cosine_of_alpha < -1.0:
        cosine_of_alpha = -1.0
    if cosine_of_alpha > 1.0:
        cosine_of_alpha = 1.0

    alpha = math.acos(cosine_of_alpha)

    if alpha <= corner_params.angle_max:
        # corner_points[i_curr].sharpness += math.pi - abs(alpha)
        _ = corner_points[i_curr]
        corner_points[i_curr] = _._replace(sharpness=_.sharpness + math.pi - abs(alpha))
        del _

        return True

    return False


def corners_find_candidates(
        *,
        corner_params: CornerParams,
        corner_points: Sequence[Vector]
) -> None:
    """
    Find the possible angles between points corner_points.
    """

    i_curr = corner_params.dist_max

    while i_curr != len(corner_points) - corner_params.dist_max:
        i_prec = i_curr - 1
        i_next = i_curr + 1
        admissibleCornersCount = 0

        countDown = 5
        while countDown:
            countDown -= 1
            while corners_is_corner_ok(
                    i_curr, i_prec, i_next,
                    corner_params=corner_params,
                    corner_points=corner_points):

                admissibleCornersCount += 1
                countDown = 0
                i_prec -= 1
                i_next += 1

            i_prec -= 1
            i_next += 1

        if admissibleCornersCount:
            # corner_points[i_curr].sharpness /= admissibleCornersCount
            _ = corner_points[i_curr]
            corner_points[i_curr] = _._replace(sharpness=_.sharpness / admissibleCornersCount)
            del _
            if ((corner_points[i_curr].sharpness > (math.pi - corner_params.angle_max)) and
                    (admissibleCornersCount > corner_params.sample_num_min)):

                # corner_points[i_curr].is_corner = True
                corner_points[i_curr] = corner_points[i_curr]._replace(is_corner=True)

        i_curr += 1


def corner_points_calc(
        points: Sequence[Vector],
        *,
        corner_params,
        corner_points
) -> bool:
    '''
    Returns true if and can do the interpolation

    Calculates CornerPoint based on corner_points, checking point by point the step
    between abscissa and ordinate;
    inserts the calculated points in corner_points and based on the amounts being of
    CornerPoint found returns True (and can interpolate) or false (not possible).
    '''

    # for readability only
    IntVector = tuple

    choose_by_distance = False

    i_curr = 0
    i_next = 1

    while i_next <= len(points) - 1:
        if points[i_next] != points[i_curr]:
            corner_points.append(AlgorithmPointI_new(points[i_curr], i_curr))

            guide_line = IntVector((int(a) for a in sub_vnvn(points[i_curr], points[i_next])))

            curr_step = corner_points[-1].point

            while len_squared_vn(tuple(int(a) for a in sub_vnvn(points[i_next], curr_step))) > 1:
                next_point = IntVector((int(a) for a in points[i_next]))

                # TPointI a = next_point - curr_step
                # int i = 0
                steps = [None] * len(curr_step)
                for i in range(len(curr_step)):
                    if curr_step[i] > next_point[i]:
                        steps[i] = add_vn_index(curr_step, i, -1.0)
                    elif curr_step[i] < next_point[i]:
                        steps[i] = add_vn_index(curr_step, i, 1.0)
                    else:
                        steps[i] = curr_step
                        choose_by_distance = True

                if choose_by_distance:
                    choose_by_distance = False
                    len_sq_best = None  # we want smallest
                    for i in range(len(curr_step)):
                        len_sq_test = len_squared_vnvn(steps[i], next_point)
                        if len_sq_best is None or len_sq_test < len_sq_best:
                            len_sq_best = len_sq_test
                            curr_step = steps[i]
                else:
                    # use angle
                    aux = len_squared_vn(guide_line)
                    step_theta_best = None  # we want smallest
                    for i in range(len(curr_step)):
                        try:
                            # TODO, check dot product with normalized vectors instead?
                            step_theta_test = math.acos(
                                dot_vnvn(sub_vnvn(steps[i], next_point), guide_line) /
                                (math.sqrt(len_squared_vnvn(steps[i], next_point) * aux)))
                        except ZeroDivisionError:
                            step_theta_test = DBL_NAN

                        if step_theta_best is None or step_theta_test < step_theta_best:
                            step_theta_best = step_theta_test
                            curr_step = steps[i]

                corner_points.append(AlgorithmPointI_new(curr_step, i_next))

        i_curr += 1
        i_next += 1

    corner_points.append(AlgorithmPointI_new(points[i_curr], i_curr))
    if len(corner_points) < (2 * corner_params.dist_max + 1):
        return False
    return True


# Find the angles between points corner_points
def corners_find(
        neighbor_limit: int,
        corner_indices: List[int],
        *,
        corner_params: CornerParams,
        corner_points: Sequence[Vector]
) -> None:

    assert(isinstance(corner_params.dist_max, int))
    i_curr = corner_params.dist_max

    while i_curr != len(corner_points) - corner_params.dist_max:
        i_perc = i_curr - 1
        i_next = i_curr + 1

        while ((len_squared_vnvn(corner_points[i_curr].point, corner_points[i_perc].point) <= neighbor_limit) and
               (len_squared_vnvn(corner_points[i_curr].point, corner_points[i_next].point) <= neighbor_limit) and

               corner_points[i_curr].is_corner):

            if (corner_points[i_curr].sharpness <= corner_points[i_perc].sharpness or
                    corner_points[i_curr].sharpness <= corner_points[i_next].sharpness):

                # corner_points[i_curr].is_corner = False
                _ = corner_points[i_curr]
                corner_points[i_curr] = _._replace(is_corner=False)
                del _
                break

            i_perc -= 1
            i_next += 1

        if (corner_points[i_curr].is_corner):
            corner_indices.append(corner_points[i_curr].original_index)

        i_curr += 1


def corners_detect(
        input_points: Vector,
        corner_indices: Sequence[int],
        *,
        sample_num_min: int,
        dist_min: float,
        dist_max: float,
        angle_max: float
) -> None:

    corner_params = CornerParams(
        sample_num_min=3,
        dist_min=3,
        dist_max=15,
        dist_min_squared=dist_min ** 2.0,
        dist_max_squared=dist_max ** 2.0,
        angle_max=angle_max,
    )

    corner_points = []

    corner_points_calc(
        input_points,
        corner_params=corner_params,
        corner_points=corner_points,
    )

    if len(corner_points) > 2 * dist_max:
        corners_find_candidates(
            corner_params=corner_params,
            corner_points=corner_points,
        )
        corners_find(
            int(math.sqrt(corner_params.dist_max_squared)) + 10,
            corner_indices,
            corner_params=corner_params,
            corner_points=corner_points,
        )
    del corner_points  # free

    # check for no index equal to an adjacent
    if corner_indices:
        corner_indices_dedupe = []
        corner_indices_dedupe.append(corner_indices[0])
        for i in range(1, len(corner_indices)):
            if corner_indices[i] != corner_indices_dedupe[-1]:
                corner_indices_dedupe.append(corner_indices[i])
        if len(corner_indices_dedupe) != len(corner_indices):
            corner_indices[:] = corner_indices_dedupe
        del corner_indices_dedupe

# end corner detection
# --------------------


def calc_spline(
        points: Sequence[Vector],
        *,
        error: float,
        use_detect_corners: bool=True,
        detect_corners_angle_threshold: float=math.radians(100)
) -> List[Cubic]:
    """
    Main function:

    Take an array of 3d points.
    return the cubic splines
    """

    # points = [tuple(p) for p in points]

    corners = [0]
    if use_detect_corners and len(points) > 2:
        corners_detect(
            points, corners,

            sample_num_min=3,
            dist_min=3,
            dist_max=15,
            angle_max=detect_corners_angle_threshold,
        )
    corners.append(len(points) - 1)

    r_cubic_array = []

    for i in range(1, len(corners)):
        points_offset_len = corners[i] - corners[i - 1] + 1
        first_point = corners[i - 1]

        # print(points_offset_len, first_point)
        assert(points_offset_len >= 1)
        if points_offset_len > 1:
            tan_l = add_vnvn(
                negated_vn(points[first_point + 1]),
                points[first_point])
            tan_r = sub_vnvn(
                points[first_point + points_offset_len - 2],
                points[first_point + points_offset_len - 1])

            tan_l = normalized_vn(tan_l)
            tan_r = normalized_vn(tan_r)

            fit_cubic_to_points(
                points[first_point:], points_offset_len,
                tan_l, tan_r, error, r_cubic_array)

        elif len(points) == 1:
            assert(points_offset_len == 1)
            assert(len(corners) == 2)
            assert(corners[0] == 0)
            assert(corners[1] == 0)
            p = points[0]
            r_cubic_array.append(Cubic(p, p, p, p))

    print(
        "points:", len(r_cubic_array),
        "corners:", len(corners),
        "uuid:", hex(hash(tuple(r_cubic_array)) % 0xFFFFFFFF)[2:].upper(),
    )

    return r_cubic_array


# ----------------------------------------------------------------------------
# Addon

import bpy
import bgl
from bpy.props import (
    BoolProperty,
    FloatProperty,
    PointerProperty,
)


def context_cursor(context):
    scene = context.scene
    space = context.space_data

    cursor = (space if space and space.type == 'VIEW_3D'
              else scene).cursor_location
    return cursor


def points_to_spline(
        spline: bpy.types.Spline,
        spline_data: List[Cubic],
        radius_min: float,
        radius_max: float,
) -> None:

    spline.bezier_points.add(len(spline_data))
    bezier_points = spline.bezier_points

    use_radius = len(spline_data[0][0]) > 3

    if use_radius:
        radius_min = min(radius_min, radius_max)
        radius_max = max(radius_min, radius_max)
        radius_range = radius_max - radius_min

    i = 0
    for i in range(len(bezier_points) - 1):
        cubic = spline_data[i]

        bezt_a = bezier_points[i]
        bezt_b = bezier_points[i + 1]

        bezt_a.co[0:3] = cubic[0][:3]
        bezt_a.handle_right = cubic[1][:3]
        bezt_b.handle_left = cubic[2][:3]
        bezt_b.co[0:3] = cubic[3][:3]

        if use_radius:
            bezt_a.radius = radius_min + (cubic[0][3] * radius_range)

        i += 1

    # cleanup first/last points
    bezt = bezier_points[0]
    bezt.handle_left = bezt.co + (bezt.co - bezt.handle_right)

    bezt = bezier_points[-1]
    bezt.handle_right = bezt.co + (bezt.co - bezt.handle_left)

    if use_radius:
        bezt.radius = radius_min + (spline_data[-1][3][3] * radius_range)


def mouse_path_to_spline(
        context,
        mouse_path: list,
) -> None:

    curve_freehand = context.scene.curve_freehand

    spline_data = calc_spline(
        mouse_path,
        error=curve_freehand.error_threshold,
        use_detect_corners=curve_freehand.use_detect_corners,
        detect_corners_angle_threshold=curve_freehand.detect_corners_angle_threshold,
    )

    obj = context.object
    curve = obj.data
    matrix_inverse = obj.matrix_world.inverted()

    from bpy_extras.view3d_utils import region_2d_to_location_3d
    region = context.region
    rv3d = context.region_data
    depth_pt = context_cursor(context)

    spline_data = [
        Cubic(*[
            (*(matrix_inverse * region_2d_to_location_3d(region, rv3d, pt, depth_pt)), *pt[2:])
            for pt in cubic])
        for cubic in spline_data]

    bpy.ops.curve.select_all(action='DESELECT')

    spline = curve.splines.new(type='BEZIER')
    points_to_spline(
        spline, spline_data,
        curve_freehand.pressure_min,
        curve_freehand.pressure_max,
    )

    for bezt in spline.bezier_points:
        bezt.select_control_point = True
        bezt.select_left_handle = True
        bezt.select_right_handle = True

        # we could get this from the calculation...
        a, b, c = bezt.handle_left, bezt.co, bezt.handle_right
        if (a - b).angle(b - c, -1.0) < 1e-2:
            bezt.handle_left_type = bezt.handle_right_type = 'ALIGNED'


def draw_callback_px(self, context):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    bgl.glLineWidth(2)

    if context.scene.curve_freehand.use_pressure:
        from mathutils import noise
        pt_a = self.mouse_path[0]
        for i in range(1, len(self.mouse_path)):
            # weak but good enough for preview
            pt_b = self.mouse_path[i]
            bgl.glPointSize(1 + (pt_a[2] * 40.0))
            bgl.glBegin(bgl.GL_POINTS)
            bgl.glVertex2i(pt_a[0], pt_a[1])
            bgl.glVertex2i(pt_b[0], pt_b[1])
            bgl.glEnd()
            pt_a = pt_b
    else:
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for pt in self.mouse_path:
            bgl.glVertex2i(pt[0], pt[1])
        bgl.glEnd()

    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class CurveFreehandDraw(bpy.types.Operator):
    """Draw curve splines in edit-mode"""
    bl_idname = "curve.draw"
    bl_label = "Curve Draw Tool"

    bl_options = {'UNDO'}

    def modal(self, context, event):
        context.area.tag_redraw()
        if event.type in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'}:
            mval = (event.mouse_region_x, event.mouse_region_y)

            if context.scene.curve_freehand.use_pressure:
                print(event.pressure)
                mval = mval + (event.pressure,)

            # don't add doubles
            if not self.mouse_path or mval != self.mouse_path[-1]:
                self.mouse_path.append(mval)

        elif event.type == self.init_event_type:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')

            if len(self.mouse_path) > 1:
                mouse_path_to_spline(context, self.mouse_path)
                return {'FINISHED'}
            else:
                return {'CANCELLED'}

        elif event.type == 'ESC':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        self.init_event_type = event.type

        # Check object context
        if context.mode == 'EDIT_CURVE':
            pass
        else:
            self.report({'WARNING'}, "Edit-Curve mode not available")
            return {'CANCELLED'}

        # Check view context
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


class VIEW3D_PT_tools_curveedit_options(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    bl_category = "Options"
    bl_context = "curve_edit"
    bl_label = "Curve Options"

    @classmethod
    def poll(cls, context):
        return context.active_object

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        curve_freehand = scene.curve_freehand

        col = layout.label("Freehand Drawing:")
        col = layout.column()
        col.prop(curve_freehand, "error_threshold")

        col.prop(curve_freehand, "use_detect_corners")
        colsub = col.column()
        colsub.active = curve_freehand.use_detect_corners
        colsub.prop(curve_freehand, "detect_corners_angle_threshold")

        col.prop(curve_freehand, "use_pressure")
        colsub = col.column(align=True)
        colsub.active = curve_freehand.use_pressure
        colsub.prop(curve_freehand, "pressure_min", text="Min")
        colsub.prop(curve_freehand, "pressure_max", text="Max")


class CurveFreehandProps(bpy.types.PropertyGroup):
    use_detect_corners = BoolProperty(
        name="Detect Corners",
        description="Detect sharp corners",
        default=True,
    )

    error_threshold = FloatProperty(
        name="Detail",
        description="Detail threshold (smaller values give more detailed splines)",
        subtype='PIXEL',
        min=0.01, max=1000.0,
        default=10.0,
    )

    detect_corners_angle_threshold = FloatProperty(
        name="Angle Limit",
        description="Detail threshold (smaller values give more detailed splines)",
        subtype='ANGLE',
        min=0.0, max=math.pi,
        default=math.radians(100),
    )

    use_pressure = BoolProperty(
        name="Tablet Pressure",
        description="Map tablet pressure to radius",
        default=False,
    )
    pressure_min = FloatProperty(
        name="Pressure Min",
        min=0.0, max=100.0,
        default=0.0,
    )
    pressure_max = FloatProperty(
        name="Pressure Max",
        min=0.0, max=100.0,
        default=1.0,
    )


classes = (
    CurveFreehandDraw,
    CurveFreehandProps,
    VIEW3D_PT_tools_curveedit_options,
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.curve_freehand = PointerProperty(type=CurveFreehandProps)

    kc = bpy.context.window_manager.keyconfigs.addon

    if kc:  # don't register keymaps from command line
        km = kc.keymaps.new(name="Curve", space_type='EMPTY', region_type='WINDOW')
        kmi = km.keymap_items.new(CurveFreehandDraw.bl_idname, 'ACTIONMOUSE', 'PRESS', shift=True)
        kmi.active = True
        addon_keymaps.append((km, kmi))


def unregister():
    del bpy.types.Scene.curve_freehand

    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
