"""
*M///////////////////////////////////////////////////////////////////////////////////////
//
//  IMPORTANT: READ BEFORE DOWNLOADING, COPYING, INSTALLING OR USING.
//
//  By downloading, copying, installing or using the software you agree to this license.
//  If you do not agree to this license, do not download, install,
//  copy or use the software.
//
//
//                           License Agreement
//                For Open Source Computer Vision Library
//
// Copyright (C) 2000-2008, Intel Corporation, all rights reserved.
// Copyright (C) 2009, Willow Garage Inc., all rights reserved.
// Third party copyrights are property of their respective owners.
//
// Redistribution and use in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:
//
//   * Redistribution's of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//   * Redistribution's in binary form must reproduce the above copyright notice,
//     this list of conditions and the following disclaimer in the documentation
//     and/or other materials provided with the distribution.
//
//   * The name of the copyright holders may not be used to endorse or promote products
//     derived from this software without specific prior written permission.
//
// This software is provided by the copyright holders and contributors "as is" and
// any express or implied warranties, including, but not limited to, the implied
// warranties of merchantability and fitness for a particular purpose are disclaimed.
// In no event shall the Intel Corporation or contributors be liable for any direct,
// indirect, incidental, special, exemplary, or consequential damages
// (including, but not limited to, procurement of substitute goods or services;
// loss of use, data, or profits; or business interruption) however caused
// and on any theory of liability, whether in contract, strict liability,
// or tort (including negligence or otherwise) arising in any way out of
// the use of this software, even if advised of the possibility of such damage.
//
//M*
"""


import math


def solve_cubic(coeffs, roots):
    """三次方程式の解
    opencv-2.2.0: modules/core/src/mathfuncs.cpp: 2231: cvSolveCubic
    """
    if not (isinstance(coeffs, (list, tuple)) and len(coeffs) >= 3):
        raise TypeError('check coeffs')
    if not (isinstance(roots, list) and len(coeffs) >= 3):
        raise TypeError('check roots')

    n = 0
    a0 = 1
    x0 = x1 = x2 = 0

    if len(coeffs) == 3:
        a1, a2, a3 = coeffs
    elif len(coeffs) >= 4:
        a0, a1, a2, a3, *_ = coeffs

    if a0 == 0:
        if a1 == 0:
            if a2 == 0:
                n = -1 if a3 == 0 else 0
            else:
                # linear equation
                x0 = -a3 / a2
                n = 1
        else:
            # quadratic equation
            d = a2 ** 2 - 4 * a1 * a3
            if d >= 0:
                d = math.sqrt(d)
                q1 = (-a2 + d) * 0.5
                q2 = (a2 + d) * -0.5
                if abs(q1) > abs(q2):
                    x0 = q1 / a1
                    x1 = a3 / q1
                else:
                    x0 = q2 / a1
                    x1 = a3 / q2
                n = 2 if d > 0 else 1
    else:
        a0 = 1 / a0
        a1 *= a0
        a2 *= a0
        a3 *= a0
        Q = (a1 ** 2 - 3 * a2) * (1 / 9)
        R = (2 * a1 ** 3 - 9 * a1 * a2 + 27 * a3) * (1 / 54)
        Qcubed = Q ** 3
        d = Qcubed - R ** 2
        if d >= 0:
            theta = math.acos(R / math.sqrt(Qcubed))
            sqrtQ = math.sqrt(Q)
            t0 = -2 * sqrtQ
            t1 = theta * (1 / 3)
            t2 = a1 * (1 / 3)
            x0 = t0 * math.cos(t1) - t2
            x1 = t0 * math.cos(t1 + (2 * math.pi / 3)) - t2
            x2 = t0 * math.cos(t1 + (4 * math.pi / 3)) - t2
            n = 3
        else:
            d = math.sqrt(-d)
            e = pow(d + abs(R), 1 / 3)
            if R > 0:
                e = -e
            x0 = (e + Q / e) - a1 * (1 / 3)
            n = 1
    roots[0] = x0
    roots[1] = x1
    roots[2] = x2
    return n
