
"""
Find camera parameters to generate a given set of 2D points 
by projection from a corresponding set of 3D points.

The conventional algorithm uses a normalised direct linear transform (DLT)
to obtain an approximate unrestricted fit,
and then a Levenberg-Marquardt nonlinear least-squares method
to obtain the restricted fit from this starting point.

The algorithm here is based instead on a generalised eigenvalue method,
used first for the unrestricted fit (faster and more accurate than the DLT),
and then to make an initial estimate of the restricted solution.
Final refinement is by the Gauss-Newton method (with reweighting).

Version 0.9.8
© M.J.Collett 2011-2014
Physics Department, University of Auckland
"""

import math
import numpy as np
from numpy import linalg as la
from numpy import dot, inner, vstack


def dual(v):
    '''Find anti-symmetric 3x3 matrix dual to 3-vector.'''
    return np.array([[0, v[2], -v[1]], [-v[2], 0, v[0]], [v[1], -v[0], 0]])


def rotation(ntheta):
    '''Find rotation matrix from axis-angle vector.'''
    theta = la.norm(ntheta)
    if theta == 0:
        return np.identity(3)
    Q = dual(ntheta / theta)
    return np.identity(3) - Q * math.sin(theta) + dot(Q, Q) * (1 - math.cos(theta))

######################################################################


def decompose(m):
    '''
    Factor 3x4 camera matrix into 3x3 internal and 3x4 external.

    This is an RQ decomposition,
    enforcing a --+ signature for the internal matrix and 
    positive determinant for the rotation matrix.
    The internal matrix is also normalised.
    NumPy only provides QR, 
    and the index gymnastics required to convert QR to RQ
    make it faster to use a custom routine.
    '''
    r = np.zeros_like(m[:, :-1])
    q = np.empty_like(m)

    r[2, 2] = la.norm(m[2, :-1])
    q[2, :] = m[2, :] / r[2, 2]
    r[1, 2] = inner(m[1, :-1], q[2, :-1])
    w = m[1, :] - r[1, 2] * q[2, :]
    r[1, 1] = -la.norm(w[:-1])
    q[1, :] = w / r[1, 1]
    r[0, 1:] = inner(m[0, :-1], q[1:, :-1])
    w = m[0, :] - dot(r[0, 1:], q[1:, :])
    r[0, 0] = -la.norm(w[:-1])
    q[0, :] = w / r[0, 0]
    q *= np.sign(la.det(q[:, :-1]))
    return r / r[2, 2], q


def extract_scale(P):
    '''
    Estimate scale factors from unconstrained camera matrix.

    Extract a diagonal scale factor so that the remaining matrix
    gives a camera with square pixels after RQ decomposition.
    If L = P[:,:3]*S^(-1) is the descaled 3x3 camera matrix, 
    the rows of L must obey
        |L_3|^2 (L_1 . L_2) = (L_1 . L_3)(L_2 . L_3)
    and
        |L_1 x L_3|^2 = |L_1 x L_2|^2
    Expanding gives linear equations for the (squared) diagonal components of S.
    The solution below uses a magic incantation created by a venerable Sage.
    '''
    Q = P[2, 2] * P[:2, :2] - np.outer(P[:2, 2], P[2, :2])
    h2 = dot(Q[:, 0], Q[:, 1])
    h0 = P[2, 1] * dot(Q[:, 0], Q[:, 0]) - P[2, 0] * h2
    h1 = P[2, 0] * dot(Q[:, 1], Q[:, 1]) - P[2, 1] * h2
    scale = np.array((P[2, 0] * h0, P[2, 1] * h1, P[2, 2]**2 * h2))
    return np.sqrt(np.abs(scale))


def persp_fit(ob4, im2, full=True):
    '''
    Find best-fit unconstrained camera parameters.

    Solved as a generalised eigenvalue problem.
    This is faster than a normalised DLT, and unbiased.
    For reweighting only the location of the principal plane is needed.
    '''
    Ji = la.inv(la.cholesky(dot(ob4.T, ob4)))
    c = inner(ob4, Ji)
    Bx = dot(c.T * im2[:, 0], c)
    By = dot(c.T * im2[:, 1], c)
    Bxx = dot(c.T * im2[:, 0]**2, c)
    Byy = dot(c.T * im2[:, 1]**2, c)
    evals, evects = la.eigh(Bxx - dot(Bx, Bx) + Byy - dot(By, By))
    Q = evects[:, np.argmin(evals)]
    if full:
        return dot(vstack((dot(Bx, Q), dot(By, Q), Q)), Ji)
    else:
        return dot(Q, Ji)


def constrained_fit(ob4, im2, f, ext, centering, u0):
    '''
    Leading-order correction to constrained camera parameters (no scaling).

    A homogeneous linearised calculation,
    solved as a generalised eigenvalue problem.
    For large corrections this is more accurate
    than a standard inhomogeneous linear (Gauss-Newton) approximation,
    but for numerical reasons it has poorer convergence for small corrections.
    '''
    ob4 /= inner(ext[-1, :], ob4)[:, np.newaxis]
    _T = ob4[:, -1]
    _0 = np.zeros_like(_T)
    _X = inner(ext[0, :], ob4)
    _Y = inner(ext[1, :], ob4)
    _Z = np.ones_like(_T)

    # Components are: phi, a1, a2, th3, (u, v).
    D1u = f * vstack((_X, _T, _0, -_Y))
    D1v = f * vstack((_Y, _0, _T, _X))
    if centering >= 0:
        D1u = f * vstack((D1u, -_Z, _0))
        D1v = f * vstack((D1v, _0, -_Z))

    # Components are: k, th1, th2, a3.
    D2u = vstack((_X, _0, _Z, _0, ))
    D2v = vstack((_Y, -_Z, _0, _0, ))
    D2w = vstack((_Z, _Y, -_X, _T, ))
    D2u = (im2[:, 0] - u0[0]) * D2w + f * D2u
    D2v = (im2[:, 1] - u0[1]) * D2w + f * D2v

    S11 = inner(D1u, D1u) + inner(D1v, D1v)
    S12 = inner(D1u, D2u) + inner(D1v, D2v)
    S22 = inner(D2u, D2u) + inner(D2v, D2v)
    if centering > 0:
        S11[-2, -2] += centering
        S11[-1, -1] += centering
        S12[-2:, 0] += centering * u0
        S22[0, 0] += centering * np.sum(u0**2)

    C = inner(D2w, D2w)  # /_T.size
    M = -la.solve(S11, S12)
    S = S22 + dot(S12.T, M)

    Ji = la.inv(la.cholesky(C))
    evals, evects = la.eigh(dot(Ji, inner(S, Ji)))
    h2 = dot(evects[:, np.argmin(evals)], Ji)
    h2 /= h2[0]
    h1 = dot(M, h2)
    h2[3], h1[3] = h1[3], h2[3]
    return h1[0], h1[1:4], h2[1:], h1[-2:]


def constrained_adjust(ob4, im2, f, ext, centering, u0, rescale, scale):
    '''
    Linear correction to constrained camera parameters (with scaling).

    An inhomogeneous linearised calculation (Gauss-Newton method),
    accurate (and rapidly converging) for small corrections.
    Reweighting is required for the true (geometric) error to be minimised.
    '''
    anyscale = rescale.any()
    if anyscale:
        S = np.diag(np.r_[scale, 1])
        P = np.dot(ext, S)
    else:
        P = ext
    ob4 /= inner(P[-1, :], ob4)[:, np.newaxis]
    _T = ob4[:, -1]
    _X = inner(P[0], ob4)
    _Y = inner(P[1], ob4)
    _Z = np.ones_like(_T)
    _0 = np.zeros_like(_T)

    # Components are: phi, a1, a2, a3, th1, th2, th3, (s1, s2), (u, v).
    Du = vstack((_X, _T, _0, _0, _0, _Z, -_Y, ))
    Dv = vstack((_Y, _0, _T, _0, -_Z, _0, _X, ))
    Dw = vstack((_0, _0, _0, _T, _Y, -_X, _0, ))
    if anyscale:
        if rescale.all():
            PX = (P[0] * ob4).T
            PY = (P[1] * ob4).T
            PZ = (P[2] * ob4).T
            Du = vstack((Du, PX[0] - PX[2], PX[1] - PX[2]))
            Dv = vstack((Dv, PY[0] - PY[2], PY[1] - PY[2]))
            Dw = vstack((Dw, PZ[0] - PZ[2], PZ[1] - PZ[2]))
        else:
            Du = vstack((Du, (P[0] * ob4).T[rescale]))
            Dv = vstack((Dv, (P[1] * ob4).T[rescale]))
            Dw = vstack((Dw, (P[2] * ob4).T[rescale]))
    if centering >= 0:
        Du = vstack((Du, -_Z, _0))
        Dv = vstack((Dv, _0, -_Z))
        Dw = vstack((Dw, _0, _0))
    Du -= _X * Dw
    Dv -= _Y * Dw

    A = inner(Du, Du) + inner(Dv, Dv)
    B = inner(Du, im2[:, 0] - u0[0] + f * _X) + inner(Dv, im2[:, 1] - u0[1] + f * _Y)
    if centering > 0:
        A[-2, -2] += centering
        A[-1, -1] += centering
        B[-2:] += centering * u0
    h = -la.solve(A, B) / f

    ds = np.zeros(3)
    if anyscale:
        if rescale.all():
            ds = np.r_[h[7:9], -sum(h[7:9])]
        else:
            ds[rescale] = h[7:7 + np.count_nonzero(rescale)]
    return h[0], h[1:4], h[4:7], h[-2:], ds


def resect_persp(points, offset=0, rescale=(False, False, False), max_evals=8, tol=1e-5):
    ob3 = np.array([v[0] for v in points])
    ob4 = np.column_stack((ob3, np.ones_like(ob3[:, 0])))
    im2 = np.array([v[1] for v in points])
    rescale = np.asarray(rescale)
    scale = np.ones(3)

    # Initial unconstrained fit (2 iterations, with reweighting)
    w = np.inner(persp_fit(ob4, im2, full=False), ob4)
    ob4 /= w[:, np.newaxis]
    P = persp_fit(ob4, im2, full=True)

    # Enforce constraints
    if rescale.any():
        scale1 = extract_scale(P)
        if rescale.all():
            scale1 /= np.mean(scale1)
        else:
            scale1 /= np.mean(scale1[np.logical_not(rescale)])
        np.copyto(scale, scale1, where=rescale)
        P[:, :-1] = np.dot(P[:, :-1], np.diag(1 / scale1))
    cam, ext = decompose(P)
    f = -(cam[0, 0] + cam[1, 1]) / 2
    if offset < 0:
        u0 = np.zeros(2)
    else:
        u0 = cam[:2, 2]

    # Initial correction to constrained fit
    if rescale.any():
        phi, da, theta, du, ds = constrained_adjust(ob4, im2, f, ext, offset, u0, rescale, scale)
        scale *= 1 + ds
    else:
        phi, da, theta, du = constrained_fit(ob4, im2, f, ext, offset, u0)
    ext = dot(rotation(theta), ext)
    ext[:, -1] += da
    if offset >= 0:
        u0 += f * du
    f += f * phi

    # Fine adjustment of constrained fit
    converged = False
    for i in range(max_evals):
        phi, da, theta, du, ds = constrained_adjust(ob4, im2, f, ext, offset, u0, rescale, scale)
        converged = np.max(np.absolute(np.r_[phi, theta, da / f, du, ds])) < tol
        ext = dot(rotation(theta), ext)
        ext[:, -1] += da
        if offset >= 0:
            u0 += f * du
        f += f * phi
        if rescale.any():
            scale *= 1 + ds
        if converged or np.min(scale) < 0:
            break

    return f, u0, ext, scale, converged

######################################################################


def decompose_affine(m):
    '''
    Factor 3x4 affine camera matrix into 3x3 internal, 3x3 rotation and 3x1 location.
    '''
    q = m[:, :-1]
    r = np.zeros_like(q)
    a = m[:, -1]

    r[1, 1] = -la.norm(q[1])
    q[1] /= r[1, 1]
    r[0, 1] = inner(q[0], q[1])
    w = q[0] - r[0, 1] * q[1]
    r[0, 0] = -la.norm(w)
    q[0] = w / r[0, 0]
    q[2] = np.cross(q[0], q[1])
    r[2, 2] = 1

    a[1] /= r[1, 1]
    a[0] -= r[0, 1] * a[1]
    a[0] /= r[0, 0]
    return r, q, a


def affine_scale(P):
    '''
    Estimate scale factors from unconstrained affine camera matrix.
    '''
    h0 = dot(P[:2, 1], P[:2, 2]) * np.cross(P[:2, 1], P[:2, 2])
    h1 = dot(P[:2, 2], P[:2, 0]) * np.cross(P[:2, 2], P[:2, 0])
    h2 = dot(P[:2, 0], P[:2, 1]) * np.cross(P[:2, 0], P[:2, 1])
    return np.sqrt(np.abs(np.array((1 / h0, 1 / h1, 1 / h2))))


def affine_fit(ob4, im2):
    '''
    Find best-fit unconstrained affine camera parameters.
    '''
    B = dot(ob4.T, ob4)
    Bx = dot(im2[:, 0], ob4)
    By = dot(im2[:, 1], ob4)
    return -vstack((la.solve(B, Bx), la.solve(B, By), np.array([0, 0, 0, 1])))


def ortho_adjust(ob3, im2, f, rot, a, rescale, scale):
    '''
    Linear correction to constrained affine camera parameters.
    '''
    anyscale = rescale.any()
    if anyscale:
        S = np.diag(scale)
        R = np.dot(rot, S)
    else:
        R = rot
    _X = inner(R[0], ob3)
    _Y = inner(R[1], ob3)
    _Z = inner(R[2], ob3)
    _T = np.ones_like(ob3[:, 0])
    _0 = np.zeros_like(_T)

    # Components are: phi, a1, a2, th1, th2, th3.
    Du = vstack((_X + a[0], _T, _0, _0, _Z, -_Y, ))
    Dv = vstack((_Y + a[1], _0, _T, -_Z, _0, _X, ))
    if anyscale:
        if rescale.all():
            PX = (R[0] * ob3).T
            PY = (R[1] * ob3).T
            Du = vstack((Du, PX[0] - PX[2], PX[1] - PX[2]))
            Dv = vstack((Dv, PY[0] - PY[2], PY[1] - PY[2]))
        else:
            Du = vstack((Du, (R[0] * ob3).T[rescale]))
            Dv = vstack((Dv, (R[1] * ob3).T[rescale]))
    A = inner(Du, Du) + inner(Dv, Dv)
    B = inner(Du, im2[:, 0] + f * (_X + a[0])) + inner(Dv, im2[:, 1] + f * (_Y + a[1]))

    h = -la.solve(A, B) / f
    ds = np.zeros(3)
    if anyscale:
        if rescale.all():
            ds = np.r_[h[6:8], -sum(h[6:8])]
        else:
            ds[rescale] = h[6:6 + np.count_nonzero(rescale)]
    return h[0], h[1:3], h[3:], ds


def resect_ortho(points, rescale=(False, False, False), max_evals=8, tol=1e-5):
    ob3 = np.array([v[0] for v in points])
    ob4 = np.column_stack((ob3, np.ones_like(ob3[:, 0])))
    im2 = np.array([v[1] for v in points])
    rescale = np.asarray(rescale)
    scale = np.ones(3)

    # Initial unconstrained fit
    P = affine_fit(ob4, im2)

    # Enforce constraints
    if rescale.any():
        scale1 = affine_scale(P)
        if rescale.all():
            scale1 /= np.mean(scale1)
        else:
            scale1 /= np.mean(scale1[np.logical_not(rescale)])
        np.copyto(scale, scale1, where=rescale)
        P[:, :-1] = np.dot(P[:, :-1], np.diag(1 / scale1))
    cam, rot, a = decompose_affine(P)
    f = -(cam[0, 0] + cam[1, 1]) / 2

    # Corrections to constrained fit
    converged = False
    for i in range(max_evals):
        phi, da, theta, ds = ortho_adjust(ob3, im2, -f, rot, a, rescale, scale)
        converged = np.max(np.absolute(np.r_[phi, theta, da / f, ds])) < tol
        rot = dot(rotation(theta), rot)
        a[:2] += da
        f += f * phi
        if rescale.any():
            scale *= 1 + ds
        if converged or np.min(scale) < 0:
            break

    # Strictly, the z-location of an affine camera is at infinity.
    # The following is an arbitrary 'sensible' finite value.
    a[2] = np.min(inner(rot[2], ob3)) - 2 * np.max(inner(rot[2], ob3))

    return f, np.column_stack((rot, a)), scale, converged
