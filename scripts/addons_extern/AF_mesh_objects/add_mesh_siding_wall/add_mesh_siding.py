bl_info = {
    "name": "Architecture: Siding",
    "description": "Generates 11 Different Types Of Siding",
    "author": "Jacob Morris",
    "blender": (2, 72, 0),
    "location": "View3D > Add > Mesh",
    "version": (0, 5),
    "category": "Add Mesh"
}
import bpy
from bpy.props import *
from random import uniform as r_float
from math import sqrt as sqrt
import mathutils
from math import radians


def bool(corner_data):
    verts = []
    faces = []  # Verts and Faces
    for ob in corner_data:
        p = len(verts)
        verts.append((ob[0], 0.5, ob[1]))
        verts.append((ob[0], -0.5, ob[1]))  # Bottom > Left
        verts.append((ob[2], -0.5, ob[1]))
        verts.append((ob[2], 0.5, ob[1]))  # Bottom > Right
        verts.append((ob[0], 0.5, ob[3]))
        verts.append((ob[0], -0.5, ob[3]))  # Top > Left
        verts.append((ob[2], -0.5, ob[3]))
        verts.append((ob[2], 0.5, ob[3]))  # Top > Right
        faces.append((p, p + 3, p + 2, p + 1))
        faces.append((p + 4, p + 5, p + 6, p + 7))  # Top & Bottom
        faces.append((p, p + 1, p + 5, p + 4))
        faces.append((p + 2, p + 3, p + 7, p + 6))  # Left & Right
        faces.append((p, p + 4, p + 7, p + 3))
        faces.append((p + 1, p + 2, p + 6, p + 5))  # Back & Front
    return (verts, faces)


def wood_vertical(oh, ow, is_slope, slope, is_width_vary, width_vary, bw, verts, faces, bs, is_length_vary, length_vary, max_boards):
    cur_x = 0.0
    batten_pos = []
    m_b_n = False
    m_b = None  # middle board location
    last_z = oh - ((slope * (ow / 2)) / 12)  # height - what that slope and width would give for height
    if last_z <= 0:  # check is it is a negative number
        slope = ((24 * oh) / ow) - 0.01
        last_z = oh - ((slope * (ow / 2)) / 12)  # if it is change to slope that fits
    if is_slope == False:  # if flat
        last_z = oh
    while cur_x < ow:  # while x position is less than overall width
        if is_length_vary == True:  # if varied length
            v = oh * (length_vary * 0.45)
            bl = r_float((oh / 2) - v, (oh / 2) + v)
        else:
            bl = oh
            max_boards = 1
        if is_width_vary == True:  # if varied width
            v = bw * (width_vary * 0.75)
            bw2 = r_float(bw - v, bw + v)
        else:
            bw2 = bw
        if is_slope == True:  # if slope calculate edge height difference for that width
            z_dif = (slope * bw2) / 12
        bz = 0.0
        counter = 1
        faces_normal = False
        while bz < last_z:
            if cur_x + bw2 > ow:  # finish with correct width board
                bw2 = ow - cur_x
            p = len(verts)  # get index for adding faces at end
            if is_slope == True:
                if cur_x + bw2 < ow / 2:  # slope up
                    verts.append((cur_x, 0.0, bz))
                    verts.append((cur_x, -0.02539, bz))
                    cur_x += bw2  # Bottom > Left
                    verts.append((cur_x, -0.02539, bz))
                    verts.append((cur_x, 0.0, bz))
                    cur_x -= bw2
                    bz += bl  # Bottom > Right
                    if bz < last_z - 0.25 and counter != max_boards:
                        verts.append((cur_x, 0.0, bz))
                        verts.append((cur_x, -0.02539, bz))
                        cur_x += bw2  # Top > Left
                        verts.append((cur_x, -0.02539, bz))
                        verts.append((cur_x, 0.0, bz))
                        cur_x -= bw2
                        bz += 0.003175  # Top > Right
                    else:
                        bz = last_z
                        verts.append((cur_x, 0.0, bz))
                        verts.append((cur_x, -0.02539, bz))
                        cur_x += bw2
                        bz += z_dif  # Top > Left
                        batten_pos.append([cur_x, bz])
                        verts.append((cur_x, -0.02539, bz))
                        verts.append((cur_x, 0.0, bz))
                        cur_x -= bw2  # Top > Right
                        bz += (slope * bs) / 12  # height gained over gap
                        if bz > oh:
                            bz = oh - ((slope * ((cur_x + bw2 + bs) - (ow / 2))) / 12)
                        last_z = bz
                    face_normal = True
                elif cur_x >= ow / 2:  # slope down
                    verts.append((cur_x, 0.0, bz))
                    verts.append((cur_x, -0.02539, bz))
                    cur_x += bw2  # Bottom > Left
                    verts.append((cur_x, -0.02539, bz))
                    verts.append((cur_x, 0.0, bz))
                    cur_x -= bw2
                    bz += bl  # Bottom > Right
                    if bz < last_z - z_dif and counter != max_boards:
                        verts.append((cur_x, 0.0, bz))
                        verts.append((cur_x, -0.02539, bz))
                        cur_x += bw2  # Top > Left
                        verts.append((cur_x, -0.02539, bz))
                        verts.append((cur_x, 0.0, bz))
                        cur_x -= bw2
                        bz += 0.003175  # Top > Right
                    else:
                        bz = last_z
                        verts.append((cur_x, 0.0, bz))
                        verts.append((cur_x, -0.02539, bz))
                        cur_x += bw2  # Top > Left
                        z_dif = (slope * bw2) / 12
                        bz -= z_dif
                        batten_pos.append([cur_x, bz])
                        verts.append((cur_x, -0.02539, bz))
                        verts.append((cur_x, 0.0, bz))
                        cur_x -= bw2  # Top > Right
                        bz -= (slope * bs) / 12  # height lost over gap
                        last_z = bz
                    face_normal = True
                elif cur_x < ow / 2 and cur_x + bw2 > ow / 2:  # middle board
                    verts.append((cur_x, 0.0, bz))
                    verts.append((cur_x, -0.02539, bz))
                    cur_x += bw2  # Bottom > Left
                    verts.append((cur_x, -0.02539, bz))
                    verts.append((cur_x, 0.0, bz))
                    cur_x -= bw2
                    bz += bl  # Bottom > Right
                    if bz < last_z - 0.25 and counter != max_boards:
                        verts.append((cur_x, 0.0, bz))
                        verts.append((cur_x, -0.02539, bz))
                        cur_x += bw2  # Top > Left
                        verts.append((cur_x, -0.02539, bz))
                        verts.append((cur_x, 0.0, bz))
                        cur_x -= bw2
                        bz += 0.003175  # Top > Right
                        face_normal = True
                    else:
                        face_normal = False
                        bz -= bl
                        # insert verts before last set
                        verts.insert(len(verts) - 2, (ow / 2, -0.02539, bz))
                        verts.insert(len(verts) - 2, (ow / 2, 0.0, bz))  # Bottom > Middle
                        # top verts
                        verts.append((cur_x, 0.0, last_z))
                        verts.append((cur_x, -0.02539, last_z))
                        cur_x += bw2  # Top > Left
                        verts.append((ow / 2, -0.02539, oh))
                        verts.append((ow / 2, 0.0, oh))  # Top > Middle
                        bz = oh - (slope * (cur_x - (ow / 2)) / 12)
                        batten_pos.append([cur_x, bz])
                        verts.append((cur_x, -0.02539, bz))
                        verts.append((cur_x, 0.0, bz))
                        cur_x -= bw2  # Top > Right
                        m_b_n = len(verts)
                        bz -= (slope * bs) / 12  # height lost over gap
                        last_z = bz
            # flat
            elif is_slope == False:
                verts.append((cur_x, 0.0, bz))
                verts.append((cur_x, -0.02539, bz))
                cur_x += bw2  # Bottom > Left
                verts.append((cur_x, -0.02539, bz))
                verts.append((cur_x, 0.0, bz))
                cur_x -= bw2
                bz += bl  # Bottom > Right
                if bz > oh:
                    bz = oh
                elif bz < oh and counter == max_boards:
                    bz = oh
                verts.append((cur_x, 0.0, bz))
                verts.append((cur_x, -0.02539, bz))
                cur_x += bw2  # Top > Left
                if bz == oh:  # record data for battens
                    batten_pos.append([cur_x, oh])
                verts.append((cur_x, -0.02539, bz))
                verts.append((cur_x, 0.0, bz))
                bz += 0.003175
                cur_x -= bw2  # Top > Right
            counter += 1
            # faces
            if is_slope == False or face_normal == True:
                faces.append((p, p + 3, p + 2, p + 1))
                faces.append((p + 4, p + 5, p + 6, p + 7))  # Bottom & Top
                faces.append((p, p + 1, p + 5, p + 4))
                faces.append((p + 1, p + 2, p + 6, p + 5))  # Left & Front
                faces.append((p + 2, p + 3, p + 7, p + 6))
                faces.append((p, p + 4, p + 7, p + 3))  # Right
            else:
                faces.append((p, p + 3, p + 2, p + 1))
                faces.append((p + 2, p + 3, p + 5, p + 4))  # Bottom
                faces.append((p + 6, p + 7, p + 8, p + 9))
                faces.append((p + 8, p + 10, p + 11, p + 9))  # Top
                faces.append((p, p + 1, p + 7, p + 6))
                faces.append((p + 1, p + 2, p + 8, p + 7))  # Left & Front Left
                faces.append((p + 2, p + 4, p + 10, p + 8))
                faces.append((p + 4, p + 5, p + 11, p + 10))  # Front Right & Right
                faces.append((p, p + 6, p + 9, p + 3))
                faces.append((p + 3, p + 9, p + 11, p + 5))  # Back
        cur_x += bw2 + bs
    out_data = [m_b_n, batten_pos]
    return (verts, faces, out_data)


def wood_ton_gro(oh, ow, is_slope, slope, bw, verts, faces, is_length_vary, length_vary, max_boards):
    cur_x = 0.0
    hi = 0.01270  # half inch
    fei = 0.015875  # five/eights inch
    oi = 0.02540  # inch
    # get variables ready
    if is_slope == True:
        last_z = oh - ((slope * (ow / 2)) / 12)
        if last_z <= 0:
            slope = ((24 * oh) / ow) - 0.01
            last_z = oh - ((slope * (ow / 2)) / 12)
        z_dif = (slope * bw) / 12
        h_dif = (slope * 0.01270) / 12
    else:
        last_z = oh
        z_dif = 0.0
    while cur_x < ow:
        cur_z = 0.0
        if is_length_vary == True:
            v = oh * (length_vary * 0.45)
            bl = r_float((oh / 2) - v, (oh / 2) + v)
        else:
            bl = oh
        counter = 1
        while cur_z < last_z:
            p = len(verts)
            face_normal = False
            do_slope = False
            # flat
            if is_slope == False:
                # bottom
                if cur_x + bw > ow:
                    bw = ow - cur_x
                verts.append((cur_x + hi, -fei, cur_z))
                verts.append((cur_x, -fei, cur_z))  # Left > Back
                verts.append((cur_x, -oi, cur_z))
                verts.append((cur_x + hi, -oi, cur_z))
                cur_x += bw  # Left > Front
                verts.append((cur_x, -oi, cur_z))
                verts.append((cur_x, -hi, cur_z))
                verts.append((cur_x + hi, -hi, cur_z))
                cur_x -= bw
                # top
                cur_z += bl
                if cur_z > last_z - 0.25 or counter == max_boards:
                    cur_z = last_z
                verts.append((cur_x + hi, -fei, cur_z))
                verts.append((cur_x, -fei, cur_z))  # Left > Back
                verts.append((cur_x, -oi, cur_z))
                verts.append((cur_x + hi, -oi, cur_z))
                cur_x += bw  # Let > Front
                verts.append((cur_x, -oi, cur_z))
                verts.append((cur_x, -hi, cur_z))
                verts.append((cur_x + hi, -hi, cur_z))
                cur_x -= bw
                cur_z += 0.003175
                face_normal = True
            else:
                # slope up
                if cur_x + bw < ow / 2:
                    verts.append((cur_x + hi, -fei, cur_z))
                    verts.append((cur_x, -fei, cur_z))  # Left > Back
                    verts.append((cur_x, -oi, cur_z))
                    verts.append((cur_x + hi, -oi, cur_z))
                    cur_x += bw  # Left > Front
                    verts.append((cur_x, -oi, cur_z))
                    verts.append((cur_x, -hi, cur_z))
                    verts.append((cur_x + hi, -hi, cur_z))
                    cur_x -= bw
                    # top
                    cur_z += bl
                    if cur_z > last_z - 0.25 or counter == max_boards:
                        cur_z = last_z
                        verts.append((cur_x + hi, -fei, cur_z + h_dif))
                        verts.append((cur_x, -fei, cur_z))  # Left > Back
                        verts.append((cur_x, -oi, cur_z))
                        verts.append((cur_x + hi, -oi, cur_z + h_dif))
                        cur_x += bw  # Left > Front
                        verts.append((cur_x, -oi, cur_z + z_dif))
                        verts.append((cur_x, -hi, cur_z + z_dif))
                        verts.append((cur_x + hi, -hi, cur_z + z_dif + h_dif))
                        cur_x -= bw
                        cur_z += z_dif + ((slope * 0.006350) / 12)
                        last_z = cur_z
                    else:
                        verts.append((cur_x + hi, -fei, cur_z))
                        verts.append((cur_x, -fei, cur_z))  # Left > Back
                        verts.append((cur_x, -oi, cur_z))
                        verts.append((cur_x + hi, -oi, cur_z))
                        cur_x += bw
                        verts.append((cur_x, -oi, cur_z))
                        verts.append((cur_x, -hi, cur_z))
                        verts.append((cur_x + hi, -hi, cur_z))
                        cur_x -= bw
                        cur_z += 0.003175
                    face_normal = True
                # slope down
                elif cur_x > ow / 2:
                    if cur_x + bw > ow:
                        bw = ow - cur_x
                        z_dif = (slope * bw) / 12
                    verts.append((cur_x + hi, -fei, cur_z))
                    verts.append((cur_x, -fei, cur_z))
                    verts.append((cur_x, -oi, cur_z))
                    verts.append((cur_x + hi, -oi, cur_z))
                    cur_x += bw
                    verts.append((cur_x, -oi, cur_z))
                    verts.append((cur_x, -hi, cur_z))
                    verts.append((cur_x + hi, -hi, cur_z))
                    cur_x -= bw
                    cur_z += bl
                    if cur_z > last_z - z_dif - 0.1 or counter == max_boards:  # do top
                        cur_z = last_z
                        verts.append((cur_x + hi, -fei, cur_z - h_dif))
                        verts.append((cur_x, -fei, cur_z))
                        verts.append((cur_x, -oi, cur_z))
                        verts.append((cur_x + hi, -oi, cur_z - h_dif))
                        cur_x += bw
                        cur_z -= z_dif
                        verts.append((cur_x, -oi, cur_z))
                        verts.append((cur_x, -hi, cur_z))
                        verts.append((cur_x + hi, -hi, cur_z - h_dif))
                        cur_x -= bw
                        cur_z -= (slope * 0.006350) / 12
                        last_z = cur_z
                        face_normal = True
                    else:
                        verts.append((cur_x + hi, -fei, cur_z))
                        verts.append((cur_x, -fei, cur_z))
                        verts.append((cur_x, -oi, cur_z))
                        verts.append((cur_x + hi, -oi, cur_z))
                        cur_x += bw
                        verts.append((cur_x, -oi, cur_z))
                        verts.append((cur_x, -hi, cur_z))
                        verts.append((cur_x + hi, -hi, cur_z))
                        cur_x -= bw
                        cur_z += 0.003175
                        face_normal = True
                # middle board
                elif cur_x < ow / 2 and cur_x + bw > ow / 2:
                    c = ow / 2  # center
                    if cur_x + hi < c:  # center is not in first half inch
                        verts.append((cur_x + hi, -fei, cur_z))
                        verts.append((cur_x, -fei, cur_z))  # Left > Back
                        verts.append((cur_x, -oi, cur_z))
                        verts.append((cur_x + hi, -oi, cur_z))  # Left > Front
                        if cur_z + bl > last_z - 0.25 or counter == max_boards:  # put middle set in
                            cur_x += bw
                            verts.append((c, -oi, cur_z))
                            verts.append((c, -hi, cur_z))  # Middle
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x, -hi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z))  # Right
                            cur_x -= bw
                            verts.append((cur_x + hi, -fei, last_z + h_dif))
                            verts.append((cur_x, -fei, last_z))  # Left > Back
                            verts.append((cur_x, -oi, last_z))
                            verts.append((cur_x + hi, -oi, last_z + h_dif))
                            cur_x += bw  # Left > Front
                            verts.append((c, -oi, oh))
                            verts.append((c, -hi, oh))
                            b_l = cur_x - c  # Center
                            cur_z = oh - ((slope * b_l) / 12)
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x, -hi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z - h_dif))
                            cur_x -= bw
                            cur_z -= (slope * 0.006350) / 12
                            last_z = cur_z
                            face_normal = "middle"
                        else:  # normal board
                            cur_x += bw
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x, -hi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z))
                            cur_x -= bw
                            cur_z += bl
                            verts.append((cur_x + hi, -fei, cur_z))
                            verts.append((cur_x, -fei, cur_z))
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x + hi, -oi, cur_z))
                            cur_x += bw
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x, -hi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z))
                            cur_z += 0.003175
                            face_normal = True
                            cur_x -= bw
                    elif cur_x + hi > c:  # center is in first half inch
                        if cur_z < last_z - 0.25 and is_length_vary == True and counter != max_boards:
                            verts.append((cur_x + hi, -fei, cur_z))
                            verts.append((cur_x, -fei, cur_z))
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x + hi, -oi, cur_z))
                            cur_x += bw
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x, -hi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z))
                            cur_x -= bw
                            cur_z += 0.003175
                            face_normal = True
                        else:
                            c = ow / 2
                            verts.append((c, -fei, cur_z))
                            verts.append((cur_x, -fei, cur_z))
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((c, -oi, cur_z))  # Left Side and Left Middle
                            verts.append((cur_x + hi, -oi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z))
                            cur_x += bw  # Left Left
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x, -hi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z))
                            cur_x -= bw
                            cur_z = last_z
                            verts.append((c, -fei, oh))
                            verts.append((cur_x, -fei, cur_z))
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((c, -oi, oh))
                            b_l = (cur_x + hi) - c
                            cur_z = oh - ((slope * b_l) / 12)
                            verts.append((cur_x + hi, -oi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z))
                            # figure right edge top height
                            cur_z = oh - ((slope * (bw - hi)) / 12)
                            cur_x += bw
                            verts.append((cur_x, -oi, cur_z))
                            verts.append((cur_x, -hi, cur_z))
                            verts.append((cur_x + hi, -hi, cur_z - h_dif))
                            cur_z -= (slope * 0.006350) / 12
                            cur_x -= bw
                            last_z = cur_z
                            face_normal = "not_middle"
            counter += 1
            # faces
            if is_slope == False or face_normal == True:
                a = ((p, p + 1, p + 8, p + 7), (p + 1, p + 2, p + 9, p + 8), (p + 2, p + 3, p + 10, p + 9), (p + 3, p + 4, p + 11, p + 10),
                     (p + 4, p + 5, p + 12, p + 11), (p + 2, p + 3, p + 10, p + 9), (p, p + 3, p + 2, p + 1), (p, p + 5, p + 4, p + 3),
                     (p + 7, p + 8, p + 9, p + 10), (p + 7, p + 10, p + 11, p + 12), (p, p + 7, p + 12, p + 5), (p + 5, p + 6, p + 13, p + 12))
                for i in a:
                    faces.append(i)
            elif is_slope == True and face_normal in ("not_middle", "middle"):
                a = ((p, p + 1, p + 2, p + 3), (p, p + 3, p + 4, p + 5), (p + 4, p + 6, p + 7, p + 5), (p + 9, p + 10, p + 11, p + 12),
                     (p + 9, p + 12, p + 13, p + 14), (p + 13, p + 15, p + 16, p + 14), (p + 1, p + 2, p + 11, p + 10),
                     (p + 2, p + 3, p + 12, p + 11), (p + 3, p + 4, p + 13, p + 12), (p + 4, p + 6, p + 15, p + 13), (p + 7, p + 8, p + 17, p + 16),
                     (p + 6, p + 7, p + 16, p + 15), (p + 7, p + 8, p + 17, p + 16), (p, p + 9, p + 14, p + 5), (p + 5, p + 14, p + 16, p + 7))
                for i in a:
                    faces.append(i)
                if face_normal == "middle":
                    faces.append((p, p + 1, p + 10, p + 9))
                elif face_normal == "not_middle":
                    faces.append((p, p + 1, p + 10, p + 9))

        cur_x += bw + 0.006350
    return (verts, faces)


def wood_lap(oh, ow, is_slope, slope, bw, verts, faces, is_length_vary, length_vary, max_boards, thickness):
    cur_z = 0.0  # current z
    oi = 0.02540  # inch
    th = thickness  # thickness
    y_dif = (th / (bw - th)) * bw  # how far out the bottom of the board is on y
    if is_slope == True:
        square = oh - ((slope * (ow / 2)) / 12)  # z height where slope starts
        if square <= 0:  # recalculate slope if it would put the edges below zero
            slope = ((24 * oh) / ow) - 0.01
            square = oh - ((slope * (ow / 2)) / 12)
        x_dif = (12 * bw) / slope  # distance to loose on each side if sloped
        last_x = ow  # what the last x value was
    else:
        square = oh
        last_x = ow
    start_x = 0.0  # used to jumpstart cur_x if sloped
    step = ((oi * 39.3701) / ((bw * 39.3701) - (oi * 39.3701))) ** 2  # y gain per inch down
    while cur_z < oh:
        fb = True  # for conditional on left side split board
        cur_x = 0.0  # current x in this row
        counter = 1  # counts boards
        while cur_x < last_x:
            face_normal = False
            p = len(verts)
            if is_length_vary == True:
                v = ow * (length_vary * 0.49)
                bl = r_float((ow / 2) - v, (ow / 2) + v)
            else:
                bl = last_x
            b_z = sqrt(((bw * 39.3701) ** 2) - 1)
            b_z = b_z / 39.3701
            if is_slope == False or cur_z + b_z < square:  # flat
                verts.append((cur_x, -y_dif, cur_z))
                verts.append((cur_x, -y_dif - th, cur_z))  # Bottom > Left
                if cur_x + bl > ow or counter == max_boards:
                    bl = ow - cur_x
                if cur_z + b_z > oh and square == oh:
                    b_z = oh - cur_z
                cur_x += bl
                verts.append((cur_x, -y_dif - th, cur_z))
                verts.append((cur_x, -y_dif, cur_z))
                cur_x -= bl  # Bottom > Right
                cur_z += b_z
                verts.append((cur_x, 0.0, cur_z))
                verts.append((cur_x, -th, cur_z))
                cur_x += bl  # Top > Left
                verts.append((cur_x, -th, cur_z))
                verts.append((cur_x, 0.0, cur_z))
                cur_x += 0.003175
                if cur_x < ow:
                    cur_z -= b_z
                else:
                    if cur_z < oh:
                        cur_z -= (sqrt(1 - step)) / 39.3701
                face_normal = True
            elif cur_z > square:  # slope the ends
                if cur_z + b_z < oh:  # do normal sloped boards
                    if cur_x == 0.0:
                        cur_x = start_x
                    if cur_x + bl <= cur_x + x_dif or cur_x + bl >= last_x - x_dif:  # recalculate bl
                        l = (last_x - x_dif) - (cur_x + x_dif)
                        v = l * (length_vary * 0.49)
                        bl = r_float((l / 2) - v, (l / 2) + v)
                        bl += x_dif
                    if is_length_vary == True:
                        if cur_x == start_x:  # left side board
                            verts.append((cur_x, -y_dif, cur_z))
                            verts.append((cur_x, -y_dif - th, cur_z))  # Bottom > Left
                            verts.append((cur_x + bl, -y_dif - th, cur_z))
                            verts.append((cur_x + bl, -y_dif, cur_z))  # Bottom > Right
                            cur_z += b_z
                            cur_x += x_dif
                            bl -= x_dif
                            start_x = cur_x
                            verts.append((cur_x, 0.0, cur_z))
                            verts.append((cur_x, -th, cur_z))  # Top > Left
                            verts.append((cur_x + bl, -th, cur_z))
                            verts.append((cur_x + bl, 0.0, cur_z))
                            cur_x += bl  # Top > Right
                            cur_z -= b_z
                            cur_x += 0.003175
                            start_x -= ((12 * sqrt(1 - step)) / slope) / 39.3701
                        elif cur_x > start_x and cur_x + bl < last_x - x_dif and max_boards > 2:  # middle board
                            verts.append((cur_x, -y_dif, cur_z))
                            verts.append((cur_x, -y_dif - th, cur_z))  # Bottom > Left
                            verts.append((cur_x + bl, -y_dif - th, cur_z))
                            verts.append((cur_x + bl, -y_dif, cur_z))
                            cur_z += b_z  # Bottom > Right
                            verts.append((cur_x, 0.0, cur_z))
                            verts.append((cur_x, -th, cur_z))  # Top > Left
                            verts.append((cur_x + bl, -th, cur_z))
                            verts.append((cur_x + bl, 0.0, cur_z))
                            cur_x += bl  # Top > Right
                            cur_x += 0.003175
                            cur_z -= b_z
                        elif cur_x + bl > last_x - x_dif or counter == max_boards or max_boards == 2:  # right side board
                            verts.append((cur_x, -y_dif, cur_z))
                            verts.append((cur_x, -y_dif - th, cur_z))  # Bottom > Left
                            verts.append((last_x, -y_dif - th, cur_z))
                            verts.append((last_x, -y_dif, cur_z))  # Bottom > Right
                            cur_z += b_z
                            last_x -= x_dif
                            verts.append((cur_x, 0.0, cur_z))
                            verts.append((cur_x, -th, cur_z))  # Top > Left
                            verts.append((last_x, -th, cur_z))
                            verts.append((last_x, 0.0, cur_z))  # Top > Right
                            c = ((12 * sqrt(1 - step)) / slope) / 39.3701
                            last_x += c
                            cur_x = last_x
                            cur_z -= (sqrt(1 - step)) / 39.3701
                        face_normal = True
                    else:  # one board
                        verts.append((cur_x, -y_dif, cur_z))
                        verts.append((cur_x, -y_dif - th, cur_z))  # Bottom > Left
                        verts.append((last_x, -y_dif - th, cur_z))
                        verts.append((last_x, -y_dif, cur_z))  # Bottom > Right
                        cur_z += b_z
                        cur_x += x_dif
                        verts.append((cur_x, 0.0, cur_z))
                        verts.append((cur_x, -th, cur_z))
                        last_x -= x_dif  # Top > Left
                        verts.append((last_x, -th, cur_z))
                        verts.append((last_x, 0.0, cur_z))  # Top > Right
                        face_normal = True
                        cur_z -= (sqrt(1 - step)) / 39.3701
                        c = (12 * ((sqrt(1 - step)) / 39.3701)) / slope
                        cur_x -= c
                        start_x = cur_x
                        last_x += c
                        cur_x = last_x
                        face_normal = True  # update variables
                else:  # top board
                    cur_x = start_x
                    verts.append((cur_x, -y_dif, cur_z))
                    verts.append((cur_x, -y_dif - th, cur_z))  # Bottom > Left
                    verts.append((last_x, -y_dif - th, cur_z))
                    verts.append((last_x, -y_dif, cur_z))  # Bottom > Right
                    cur_z += (((ow / 2) - cur_x) * slope) / 12
                    verts.append((ow / 2, 0.0, cur_z))
                    verts.append((ow / 2, -th, cur_z))  # Top
                    face_normal = "triangle"
                    cur_x = ow
                    cur_z = oh  # finish loop
            elif cur_z < square and cur_z + b_z > square:  # split board
                if is_length_vary == False:  # one board
                    verts.append((cur_x, -y_dif, cur_z))
                    verts.append((cur_x, -y_dif - th, cur_z))  # Bottom > Left
                    verts.append((ow, -y_dif - th, cur_z))
                    verts.append((ow, -y_dif, cur_z))  # Bottom > Right
                    y = ((cur_z + b_z) - square) * (y_dif / bw)  # calculate y distance at square
                    verts.append((cur_x, -y, square))
                    verts.append((cur_x, -y - th, square))  # Middle > Left
                    verts.append((ow, -y - th, square))
                    verts.append((ow, -y, square))
                    cur_z += b_z  # Middle > Right
                    s = (x_dif / bw) * (cur_z - square)
                    cur_x += s
                    last_x -= s  # figure out distance to slope back
                    verts.append((cur_x, 0.0, cur_z))
                    verts.append((cur_x, -th, cur_z))  # Top > Left
                    verts.append((last_x, -th, cur_z))
                    verts.append((last_x, 0.0, cur_z))  # Top > Right
                    if (cur_z - square) * 39.3701 < 1:
                        start_x = 0.0
                        last_x = ow
                        cur_x = last_x
                    else:
                        c = ((12 * sqrt(1 - step)) / slope) / 39.3701
                        start_x = cur_x - c
                        last_x += c
                        cur_x = last_x
                    cur_z -= (sqrt(1 - step)) / 39.3701
                    face_normal = "split board"
                elif fb == True:  # if multiple boards: this is left side split one
                    if bl < cur_x + x_dif:  # makes sure board is not to long
                        bl = cur_x + x_dif + 0.1
                    verts.append((0.0, -y_dif, cur_z))
                    verts.append((0.0, -y_dif - th, cur_z))
                    cur_x += bl  # Bottom > Left
                    verts.append((cur_x, -y_dif - th, cur_z))
                    verts.append((cur_x, -y_dif, cur_z))
                    cur_x -= bl  # Bottom > Right
                    y = ((cur_z + b_z) - square) * (y_dif / bw)  # figures out y distance at square based on board width
                    verts.append((0.0, -y, square))
                    verts.append((0.0, -y - th, square))
                    cur_x += bl  # Middle > Left
                    verts.append((cur_x, -y - th, square))
                    verts.append((cur_x, -y, square))
                    cur_x -= bl  # Middle > Right
                    cur_z += b_z
                    s = (12 * (cur_z - square)) / slope
                    cur_x += s
                    start_x = cur_x  # add board z height, figure out slope distance based on width left, add it
                    verts.append((cur_x, 0.0, cur_z))
                    verts.append((cur_x, -th, cur_z))
                    cur_x -= s
                    cur_x += bl  # Top > Left
                    verts.append((cur_x, -th, cur_z))
                    verts.append((cur_x, 0.0, cur_z))
                    cur_z -= b_z
                    last_x -= s
                    cur_x += 0.003175
                    start_x -= ((12 * sqrt(1 - step)) / slope) / 39.3701  # update variables
                    face_normal = "split board"
                    fb = False
                elif cur_x + bl < ow - x_dif and max_boards != 2:  # middle board
                    if counter != max_boards:
                        verts.append((cur_x, -y_dif, cur_z))
                        verts.append((cur_x, -y_dif - th, cur_z))
                        cur_x += bl  # Bottom > Left
                        verts.append((cur_x, - y_dif - th, cur_z))
                        verts.append((cur_x, -y_dif, cur_z))
                        cur_x -= bl  # Bottom > Right
                        cur_z += b_z
                        verts.append((cur_x, 0.0, cur_z))
                        verts.append((cur_x, -th, cur_z))
                        cur_x += bl  # Top > Left
                        verts.append((cur_x, -th, cur_z))
                        verts.append((cur_x, 0.0, cur_z))
                        cur_x += 0.003175  # Top > Right
                        cur_z -= b_z
                        face_normal = True
                elif cur_x + bl >= ow - x_dif or counter == max_boards or max_boards == 2:  # right side board
                    verts.append((cur_x, -y_dif, cur_z))
                    verts.append((cur_x, -y_dif - th, cur_z))  # Bottom > Left
                    verts.append((ow, -y_dif - th, cur_z))
                    verts.append((ow, -y_dif, cur_z))  # Bottom > Right
                    y = ((cur_z + b_z) - square) * (y_dif / bw)  # figures out y distance at square based on board width
                    verts.append((cur_x, -y, square))
                    verts.append((cur_x, -y - th, square))  # Middle > Left
                    verts.append((ow, -y - th, square))
                    verts.append((ow, -y, square))
                    cur_z += b_z  # Middle > Right
                    verts.append((cur_x, 0.0, cur_z))
                    verts.append((cur_x, -th, cur_z))  # Top > Left
                    s = (12 * (cur_z - square)) / slope
                    x2 = ow - s
                    last_x = x2
                    verts.append((x2, -th, cur_z))
                    verts.append((x2, 0.0, cur_z))  # Top > Right
                    face_normal = "split board"
                    cur_z -= (sqrt(1 - step)) / 39.3701
                    c = (12 * ((sqrt(1 - step)) / 39.3701)) / slope  # subtract distance gained during lap
                    last_x += c
                    fb = True
                    cur_x = last_x
            counter += 1
            if is_slope == False or face_normal == True:
                a = ((p, p + 1, p + 5, p + 4), (p + 1, p + 2, p + 6, p + 5), (p + 2, p + 3, p + 7, p + 6),
                     (p, p + 3, p + 2, p + 1), (p + 4, p + 5, p + 6, p + 7), (p, p + 4, p + 7, p + 3))
                for i in a:
                    faces.append(i)
            elif face_normal == "split board":
                a = ((p, p + 1, p + 5, p + 4), (p + 4, p + 5, p + 9, p + 8), (p + 9, p + 10, p + 11, p + 8),
                     (p + 6, p + 7, p + 11, p + 10), (p + 2, p + 3, p + 7, p + 6), (p, p + 3, p + 2, p + 1),
                     (p + 1, p + 2, p + 6, p + 5), (p + 5, p + 6, p + 10, p + 9), (p, p + 4, p + 7, p + 3), (p + 4, p + 8, p + 11, p + 7))
                for i in a:
                    faces.append(i)
            elif face_normal == "triangle":
                a = ((p, p + 3, p + 2, p + 1), (p, p + 1, p + 5, p + 4), (p + 1, p + 2, p + 5), (p + 2, p + 3, p + 4, p + 5), (p, p + 4, p + 3))
                for i in a:
                    faces.append(i)
    return (verts, faces)


def wood_lap_bevel(oh, ow, is_slope, slope, bw, is_length_vary, length_vary, faces, verts, max_boards):  # beveled lapped siding
    cur_z = 0.0
    last_x = ow
    start_x = 0.0
    oi = 0.02540  # inch
    tb = bw / 2.5  # thrid of board width
    tb2 = (bw * 39.3701) / 2.5
    ohi = (tb2 * 0.5) / (tb2 - 0.5)
    ohi /= 39.3701  # bottom y
    hi = oi - ohi  # top y
    y_step = ohi / tb  # per unit down this is how far you go on y
    if is_slope == True:
        square = oh - ((slope * (ow / 2)) / 12)  # z height where slope starts
        if square <= 0:  # recalculate slope if it would put the edges below zero
            slope = ((24 * oh) / ow) - 0.01
            square = oh - ((slope * (ow / 2)) / 12)
        x_dif = (12 * bw) / slope  # distance to per whole board
        tb_dif = (12 * tb) / slope  # x difference for tb height
        m_dif = (12 * (bw - (2 * tb))) / slope  # x difference for middle of board height
    else:
        square = oh
    while cur_z < oh:
        temp_x = 0.0
        cur_x = 0.0
        face_normal = False
        counter = 1
        if start_x != 0.0:
            cur_x = start_x
        if cur_x >= last_x:
            cur_z = oh
        while cur_x < last_x:
            s_d = False
            enter = False  # square done
            if is_length_vary == True:
                v = ow * (length_vary * 0.45)
                bl = r_float((ow / 2) - v, (ow / 2) + v)
                if cur_x + bl > ow or counter == max_boards:
                    bl = ow - cur_x
            else:
                bl = ow
            p = len(verts)  # position for vert indexs
            # verts
            if is_slope == False or cur_z + bw <= square:  # flat or below square
                if cur_z == oh:
                    cur_z -= oi
                v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, -ohi, cur_z))
                cur_z += tb  # Bottom Row
                if cur_z > oh:
                    cur_z = oh
                    face_normal = "eight"  # eight vertices
                v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))  # Second Row
                if cur_z < oh:
                    cur_z += bw - (2 * tb)
                    if cur_z > oh:
                        cur_z = oh
                        face_normal = "twelve"  # twelve vertices
                    v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))  # Third Row
                if cur_z < oh:
                    cur_z += tb
                    if cur_z > oh:
                        cur_z = oh
                    v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z))
                    face_normal = True  # Top Row
                cur_x += bl
                if is_length_vary == False:
                    cur_x = last_x
                    if cur_z < oh:
                        cur_z -= oi
                else:
                    if cur_x < ow:
                        cur_z -= bw
                        cur_x += 0.003175
                    elif cur_x >= ow and cur_z < oh:
                        cur_z -= oi
                for i in v:
                    verts.append(i)
            elif cur_z < square and cur_z + bw > square:  # middle board
                if is_length_vary == False:  # single board
                    v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, -ohi, cur_z))  # Bottom Row
                    cur_z += tb
                    if cur_z > square:
                        y = (cur_z - square) * y_step
                        v += ((cur_x, -y, square), (cur_x, -oi, square), (last_x, -oi, square), (last_x, -y, square))  # At Square
                        s = (12 * (cur_z - square)) / slope
                        cur_x += s
                        last_x -= s
                        s_d = True
                    v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))
                    cur_z += bw - (2 * tb)  # Second Row
                    if s_d == True:
                        s = (12 * (bw - (2 * tb))) / slope
                        cur_x += s
                        last_x -= s
                    if s_d != True and cur_z > square:  # Now do square row
                        v += ((cur_x, 0.0, square), (cur_x, -oi, square), (last_x, -oi, square), (last_x, 0.0, square))
                        s = (12 * (cur_z - square)) / slope
                        cur_x += s
                        last_x -= s
                        s_d = True
                    v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))
                    cur_z += tb  # Third Row
                    if s_d == True:
                        s = (12 * tb) / slope
                        cur_x += s
                        last_x -= s
                    if s_d != True and cur_z > square:  # Now do square row
                        y = hi + ((ohi / tb) * (cur_z - square))
                        v += ((cur_x, 0.0, square), (cur_x, -y, square), (last_x, -y, square), (last_x, 0.0, square))  # At Square
                        s = (12 * (cur_z - square)) / slope
                        cur_x += s
                        last_x -= s
                        s_d = True
                    v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (last_x, -hi, cur_z), (last_x, 0.0, cur_z))  # Third Row
                    cur_z -= oi
                    face_normal = "square"
                    if cur_z > square:
                        s = (12 * oi) / slope
                        start_x = cur_x - s
                        last_x += s
                        cur_x = last_x
                    else:
                        last_x += s
                        cur_x = last_x
                    for i in v:
                        verts.append(i)
                else:
                    if cur_x == 0.0:  # left board
                        v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, -ohi, cur_z))  # Bottom Row
                        cur_z += tb
                        if cur_z > square:
                            y = (cur_z - square) * y_step
                            v += ((cur_x, -y, square), (cur_x, -oi, square), (cur_x + bl, -oi, square), (cur_x + bl, -y, square))  # At Square
                            s = (12 * (cur_z - square)) / slope
                            cur_x += s
                            bl -= s
                            s_d = True
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))
                        cur_z += bw - (2 * tb)  # Second Row
                        if s_d == True:
                            s = (12 * (bw - (2 * tb))) / slope
                            cur_x += s
                            bl -= s
                        if cur_z > square and s_d != True:
                            v += ((cur_x, 0.0, square), (cur_x, -oi, square), (cur_x + bl, -oi, square), (cur_x + bl, 0.0, square))  # At Square
                            s = (12 * (cur_z - square)) / slope
                            cur_x += s
                            bl -= s
                            s_d = True
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))
                        cur_z += tb  # Third Row
                        if s_d == True:
                            s = (12 * tb) / slope
                            cur_x += s
                            bl -= s
                        if cur_z > square and s_d != True:
                            y = hi + ((ohi / tb) * (cur_z - square))
                            v += ((cur_x, 0.0, square), (cur_x, -y, square), (cur_x + bl, -y, square), (cur_x + bl, 0.0, square))  # At Square
                            s = (12 * (cur_z - square)) / slope
                            cur_x += s
                            bl -= s
                            s_d = True
                        v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z))
                        temp_x = cur_x  # Top Row
                        if s_d == False:
                            face_normal = True
                        else:
                            face_normal = "square"
                        cur_z -= bw
                        cur_x += 0.003175
                        cur_x += bl
                        for i in v:
                            verts.append(i)
                    elif cur_x + bl < last_x - x_dif and max_boards > 2 and counter != max_boards:  # middle board
                        v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, -ohi, cur_z))  # Bottom Row
                        cur_z += tb
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))  # Second Row
                        cur_z += bw - (2 * tb)
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))  # Third Row
                        cur_z += tb
                        v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z))  # Top Row
                        face_normal = True
                        cur_z -= bw
                        cur_x += 0.003175
                        cur_x += bl
                        for i in v:
                            verts.append(i)
                    elif cur_x + bl >= last_x - x_dif or counter == max_boards:  # right board
                        v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, -ohi, cur_z))  # Bottom Row
                        cur_z += tb
                        if cur_z > square:
                            y = (cur_z - square) * y_step
                            v += ((cur_x, -y, square), (cur_x, -oi, square), (last_x, -oi, square), (last_x, -y, square))  # At Square
                            s = (12 * (cur_z - square)) / slope
                            last_x -= s
                            s_d = True
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))
                        cur_z += bw - (2 * tb)  # Second Row
                        if s_d == True:
                            s = (12 * (bw - (2 * tb))) / slope
                            last_x -= s
                        if cur_z > square and s_d != True:
                            v += ((cur_x, 0.0, square), (cur_x, -oi, square), (last_x, -oi, square), (last_x, 0.0, square))  # At Square
                            s = (12 * (cur_z - square)) / slope
                            last_x -= s
                            s_d = True
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))
                        cur_z += tb  # Third Row
                        if s_d == True:
                            s = (12 * tb) / slope
                            last_x -= s
                        if cur_z > square and s_d != True:
                            y = hi + ((ohi / tb) * (cur_z - square))
                            v += ((cur_x, 0.0, square), (cur_x, -y, square), (last_x, -y, square), (last_x, 0.0, square))  # At Square
                            s = (12 * (cur_z - square)) / slope
                            last_x -= s
                            s_d = True
                        v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (last_x, -hi, cur_z), (last_x, 0.0, cur_z))  # Top Row
                        if s_d == False:
                            face_normal = True
                        else:
                            face_normal = "square"
                        cur_z -= oi
                        start_x = temp_x
                        if cur_z <= square:
                            start_x = 0.0
                            last_x = ow
                            cur_x = last_x
                        else:
                            s = (12 * oi) / slope
                            start_x -= s
                            last_x += s
                            cur_x = last_x
                        for i in v:
                            verts.append(i)
            elif cur_z >= square and cur_z + bw <= oh:  # regular sloping boards
                if is_length_vary == False:  # single sloping board
                    v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, -ohi, cur_z))  # Bottom Row
                    cur_z += tb
                    cur_x += tb_dif
                    last_x -= tb_dif
                    v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))  # Second Row
                    cur_z += bw - (2 * tb)
                    cur_x += m_dif
                    last_x -= m_dif
                    v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))  # Third Row
                    cur_z += tb
                    cur_x += tb_dif
                    last_x -= tb_dif
                    v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (last_x, -hi, cur_z), (last_x, 0.0, cur_z))  # Top Row
                    cur_z -= oi
                    s = (12 * oi) / slope
                    cur_x -= s
                    last_x += s
                    start_x = cur_x
                    face_normal = True
                    cur_x = last_x
                    for i in v:
                        verts.append(i)
                elif is_length_vary == True:
                    if face_normal == False:  # figure out if single board
                        if last_x - start_x < 1.25:
                            enter = True
                        elif (last_x - x_dif) - (cur_x + x_dif) < 1:
                            enter = True
                    if enter == True:  # single board
                        v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, -ohi, cur_z))  # Bottom Row
                        cur_z += tb
                        cur_x += tb_dif
                        last_x -= tb_dif
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))  # Second Row
                        cur_z += bw - (2 * tb)
                        cur_x += m_dif
                        last_x -= m_dif
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))  # Third Row
                        cur_z += tb
                        cur_x += tb_dif
                        last_x -= tb_dif
                        v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (last_x, -hi, cur_z), (last_x, 0.0, cur_z))  # Top Row
                        cur_z -= oi
                        s = (12 * oi) / slope
                        cur_x -= s
                        last_x += s
                        start_x = cur_x
                        face_normal = True
                        cur_x = last_x
                        if cur_z + oi >= oh:
                            cur_z = oh
                        for i in v:
                            verts.append(i)
                    else:
                        if cur_x == start_x:  # left board
                            if cur_x + bl > last_x - x_dif or x_dif > bl:
                                l = (last_x - x_dif) - (cur_x + x_dif)
                                v = l * (length_vary * 0.45)
                                bl = r_float(l - v, x_dif + v)
                            v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, -ohi, cur_z))  # Bottom Row
                            cur_z += tb
                            cur_x += tb_dif
                            bl -= tb_dif
                            v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))  # Second Row
                            cur_z += bw - (2 * tb)
                            cur_x += m_dif
                            bl -= m_dif
                            v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))  # Third Row
                            cur_z += tb
                            cur_x += tb_dif
                            bl -= tb_dif
                            v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z))  # Top Row
                            cur_z -= bw
                            start_x = cur_x
                            cur_x += bl + 0.003175
                            face_normal = True
                            for i in v:
                                verts.append(i)
                        elif cur_x + bl < last_x - x_dif and counter != max_boards and max_boards > 2:  # middle board
                            v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, -ohi, cur_z))  # Bottom Row
                            cur_z += tb
                            v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))  # Second Row
                            cur_z += bw - (2 * tb)
                            v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (cur_x + bl, -oi, cur_z), (cur_x + bl, 0.0, cur_z))  # Third Row
                            cur_z += tb
                            v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z))  # Top Row
                            cur_z -= bw
                            cur_x += bl + 0.003175
                            face_normal = True
                            for i in v:
                                verts.append(i)
                        elif cur_x + bl > last_x - x_dif or counter == max_boards or max_boards == 2:  # right board
                            v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, -ohi, cur_z))  # Bottom Row
                            cur_z += tb
                            last_x -= tb_dif
                            v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))  # Second Row
                            cur_z += bw - (2 * tb)
                            last_x -= m_dif
                            v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))  # Third Row
                            cur_z += tb
                            last_x -= tb_dif
                            v += ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (last_x, -hi, cur_z), (last_x, 0.0, cur_z))  # Top Row
                            cur_z -= oi
                            s = (12 * oi) / slope
                            start_x -= s
                            last_x += s
                            cur_x = last_x
                            face_normal = True
                            for i in v:
                                verts.append(i)
            elif cur_z + bw > oh:  # top triangle board
                v = ((cur_x, -ohi, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, -ohi, cur_z))  # Bottom Row
                cur_z += tb
                if cur_z > oh:  # If currently higher than overall height make triangle
                    cur_z -= tb
                    s = (12 * (oh - cur_z)) / slope
                    cur_z = oh
                    cur_x += s
                    last_x -= s
                    v += ((ow / 2, 0.0, cur_z), (ow / 2, -oi, cur_z))
                    cur_x = last_x
                    face_normal = "tri_lev_one"  # Top Row
                else:  # not yet
                    cur_x += tb_dif
                    last_x -= tb_dif
                    v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))  # Second Row
                    cur_z += bw - (2 * tb)
                    if cur_z > oh:  # if now
                        cur_z -= tb
                        s = (12 * (oh - cur_z)) / slope
                        cur_z = oh
                        cur_x += s
                        last_x -= s
                        v += ((ow / 2, 0.0, cur_z), (ow / 2, -oi, cur_z))
                        cur_x = last_x
                        face_normal = "tri_lev_two"  # Top Row
                    else:  # not yet
                        cur_x += m_dif
                        last_x -= m_dif
                        v += ((cur_x, 0.0, cur_z), (cur_x, -oi, cur_z), (last_x, -oi, cur_z), (last_x, 0.0, cur_z))  # Third Row
                        cur_z = oh
                        v += ((ow / 2, 0.0, cur_z), (ow / 2, -hi, cur_z))
                        face_normal = "tri_lev_three"
                        cur_x = ow  # Top Row
                cur_x = last_x
                cur_z = oh
                for i in v:
                    verts.append(i)
            counter += 1
            # faces
            if face_normal == True or face_normal == "square":
                f = [(p, p + 3, p + 2, p + 1), (p, p + 1, p + 5, p + 4), (p + 4, p + 5, p + 9, p + 8), (p + 8, p + 9, p + 13, p + 12),
                     (p + 1, p + 2, p + 6, p + 5), (p + 5, p + 6, p + 10, p + 9), (p + 9, p + 10, p + 14, p + 13), (p, p + 4, p + 7, p + 3),
                     (p + 2, p + 3, p + 7, p + 6), (p + 6, p + 7, p + 11, p + 10), (p + 10, p + 11, p + 15, p + 14), (p + 12, p + 13, p + 14, p + 15),
                     (p + 4, p + 8, p + 11, p + 7), (p + 8, p + 12, p + 15, p + 11)]
                if face_normal == "square":
                    del f[11]
                    f += ((p + 8, p + 12, p + 15, p + 11), (p + 12, p + 13, p + 17, p + 16), (p + 13, p + 14, p + 18, p + 17), (p + 14, p + 15, p + 19, p + 18),
                          (p + 12, p + 16, p + 19, p + 15), (p + 16, p + 17, p + 18, p + 19))
                for i in f:
                    faces.append(i)
            elif face_normal == "eight":
                f = ((p, p + 3, p + 2, p + 1), (p + 1, p + 2, p + 6, p + 5), (p, p + 1, p + 5, p + 4), (p + 2, p + 3, p + 7, p + 6), (p + 4, p + 5, p + 6, p + 7), (p, p + 4, p + 7, p + 3))
                for i in f:
                    faces.append(i)
            elif face_normal == "twelve":
                f = ((p, p + 3, p + 2, p + 1), (p + 1, p + 2, p + 6, p + 5), (p, p + 1, p + 5, p + 4), (p + 2, p + 3, p + 7, p + 6), (p, p + 4, p + 7, p + 3),
                     (p + 4, p + 5, p + 9, p + 8), (p + 5, p + 6, p + 10, p + 9), (p + 6, p + 7, p + 11, p + 10), (p + 4, p + 8, p + 11, p + 7), (p + 8, p + 9, p + 10, p + 11))
                for i in f:
                    faces.append(i)
            elif face_normal in ("tri_lev_one", "tri_lev_two", "tri_lev_three"):
                f = []
                if face_normal == "tri_lev_one":  # level on
                    f.append((p, p + 3, p + 2, p + 1))
                elif face_normal == "tri_lev_two":  # level two
                    f += ((p, p + 3, p + 2, p + 1), (p, p + 1, p + 5, p + 4), (p + 1, p + 2, p + 6, p + 5), (p + 2, p + 3, p + 7, p + 6), (p, p + 4, p + 7, p + 3))
                    p += 4
                elif face_normal == "tri_lev_three":  # level three
                    f += ((p, p + 3, p + 2, p + 1), (p, p + 1, p + 5, p + 4), (p + 1, p + 2, p + 6, p + 5), (p + 2, p + 3, p + 7, p + 6), (p, p + 4, p + 7, p + 3),
                          (p + 4, p + 5, p + 9, p + 8), (p + 5, p + 6, p + 10, p + 9), (p + 6, p + 7, p + 11, p + 10), (p + 4, p + 8, p + 11, p + 7))
                    p += 8
                f += ((p, p + 1, p + 5, p + 4), (p + 1, p + 2, p + 5), (p + 2, p + 3, p + 4, p + 5), (p, p + 4, p + 3))
                for i in f:
                    faces.append(i)
    return (verts, faces)


def vinyl_vertical(oh, ow, is_slope, slope, is_length_vary, length_vary, bw, baw, faces, verts, max_boards):
    cur_x = 0.0
    if (bw / 2) - 0.003175 <= baw:  # batten to wide
        baw = (bw / 2) - 0.003175
    hi = 0.01270
    ei = 0.003175
    tei = 0.009525  # convenience variables; half inch, left side distance to batten, 1/8 inch, 3/8 inch
    space = (bw - (2 * baw)) / 2
    rsx = space + baw
    lsx = bw - baw
    if is_slope == True:
        square = oh - ((slope * (ow / 2)) / 12)
        last_z = square
        z_dif = (slope * bw) / 12  # z height where slope starts
        if square <= 0:  # recalculate slope if it would put the edges below zero
            slope = ((24 * oh) / ow) - 0.01
            square = oh - ((slope * (ow / 2)) / 12)
            last_z = square
            z_dif = (slope * bw) / 12
    else:
        last_z = oh
    c_d = False
    while cur_x < ow:  # main loop for width
        counter = 1
        cur_z = 0.0
        while cur_z < last_z:  # while height it not enough
            face_normal = False
            p = len(verts)
            if is_length_vary == True and counter != max_boards:  # calculate board length
                v = oh * (length_vary * 0.45)
                bl = r_float((oh / 2) - v, (oh / 2) + v)
            else:
                bl = oh
            if cur_z + bl > oh:
                bl = oh - cur_z
            # verts
            if is_slope == False:  # normal boards
                v = []
                for i in range(2):
                    v += ((cur_x, -tei, cur_z), (cur_x, 0.0, cur_z), (cur_x + space + ei, 0.0, cur_z), (cur_x + space, -hi, cur_z))  # Left Side First Batten
                    v += ((cur_x + rsx, -hi, cur_z), (cur_x + rsx - ei, 0.0, cur_z), (cur_x + lsx + ei, 0.0, cur_z), (cur_x + lsx, -hi, cur_z))  # Left Side Second Batten
                    v += ((cur_x + bw, -hi, cur_z), (cur_x + bw, -ei, cur_z))
                    cur_z += bl
                cur_z -= bl
                if cur_x + bw <= ow:
                    cur_z += ei
                    face_normal = True
                else:
                    if cur_x + space >= ow:  # cut back to beginning and then place last set of verts
                        del v[2:10]
                        del v[4: len(v)]
                        v.insert(2, (ow, 0.0, cur_z - bl))
                        v.insert(len(v), (ow, 0.0, cur_z))
                        face_normal = "lev_one"
                    elif cur_x + rsx >= ow:
                        del v[4:10]
                        del v[8: len(v)]
                        v.insert(4, (ow, -hi, cur_z - bl))
                        v.insert(len(v), (ow, -hi, cur_z))
                        face_normal = "lev_two"
                    elif cur_x + lsx >= ow:
                        del v[6:10]
                        del v[12: len(v)]
                        v.insert(6, (ow, 0.0, cur_z - bl))
                        v.insert(len(v), (ow, 0.0, cur_z))
                        face_normal = "lev_three"
                    elif cur_x + bw > ow:
                        del v[8:10]
                        del v[16: len(v)]
                        v.insert(8, (ow, -hi, cur_z - bl))
                        v.insert(len(v), (ow, -hi, cur_z))
                        face_normal = "lev_four"
                if cur_z >= oh:
                    cur_x += bw - ei
                for i in v:
                    verts.append(i)
            elif is_slope == True:
                if cur_x + bw <= ow / 2:  # Sloping up
                    v = ((cur_x, -tei, cur_z), (cur_x, 0.0, cur_z), (cur_x + space + ei, 0.0, cur_z), (cur_x + space, -hi, cur_z))  # Left Side First Batten
                    v += ((cur_x + rsx, -hi, cur_z), (cur_x + rsx - ei, 0.0, cur_z), (cur_x + lsx + ei, 0.0, cur_z), (cur_x + lsx, -hi, cur_z))  # Left Side Second Batten
                    v += ((cur_x + bw, -hi, cur_z), (cur_x + bw, -ei, cur_z))
                    cur_z += bl
                    if cur_z >= last_z - 0.004:  # slope top
                        z1 = last_z
                        z2 = last_z + ((slope * (space + ei)) / 12)
                        z3 = last_z + ((slope * space) / 12)
                        z4 = last_z + ((slope * rsx) / 12)
                        z5 = last_z + ((slope * (rsx - ei)) / 12)
                        z6 = last_z + ((slope * (lsx + ei)) / 12)
                        z7 = last_z + ((slope * lsx) / 12)
                        z8 = last_z + ((slope * bw) / 12)
                    else:
                        z1 = cur_z
                        z2 = cur_z
                        z3 = cur_z
                        z4 = cur_z
                        z5 = cur_z
                        z6 = cur_z
                        z7 = cur_z
                        z8 = cur_z
                    v += ((cur_x, -tei, z1), (cur_x, 0.0, z1), (cur_x + space + ei, 0.0, z2), (cur_x + space, -hi, z3))  # Left Side First Batten
                    v += ((cur_x + rsx, -hi, z4), (cur_x + rsx - ei, 0.0, z5), (cur_x + lsx + ei, 0.0, z6), (cur_x + lsx, -hi, z7))  # Left Side Second Batten
                    v += ((cur_x + bw, -hi, z8), (cur_x + bw, -ei, z8))
                    face_normal = True
                    if is_length_vary == False or z1 == last_z:
                        cur_x += bw - ei
                        last_z = z8 - ((slope * ei) / 12)
                        cur_z = last_z
                    elif is_length_vary == True and z1 == cur_z:
                        cur_z += 0.003175
                    for i in v:
                        verts.append(i)
                elif cur_x < ow / 2 and cur_x + bw > ow / 2:  # Middle board
                    if is_length_vary == True and cur_z + bl < last_z - z_dif:  # bottom board
                        v = []
                        for i in range(2):
                            v += ((cur_x, -tei, cur_z), (cur_x, 0.0, cur_z), (cur_x + space + ei, 0.0, cur_z), (cur_x + space, -hi, cur_z))  # Left Side First Batten
                            v += ((cur_x + rsx, -hi, cur_z), (cur_x + rsx - ei, 0.0, cur_z), (cur_x + lsx + ei, 0.0, cur_z), (cur_x + lsx, -hi, cur_z))  # Left Side Second Batten
                            v += ((cur_x + bw, -hi, cur_z), (cur_x + bw, -ei, cur_z))
                            cur_z += bl
                        cur_z -= bl
                        cur_z += ei
                        face_normal = True
                        for i in v:
                            verts.append(i)
                    else:  # top split board
                        v = ((cur_x, -tei, cur_z), (cur_x, 0.0, cur_z), (cur_x, 0.0, last_z), (cur_x, -tei, last_z))
                        cur_x += space  # Left
                        if cur_x > ow / 2:  # if past peak
                            v += ((ow / 2, 0.0, cur_z), (ow / 2, 0.0, oh))
                            last_z = oh - ((slope * (cur_x - (ow / 2))) / 12)
                            c_d = True
                            face_normal = "s_1"
                            slope_ei = -((slope * ei) / 12)  # place peak and slope other side down
                        else:
                            last_z += (slope * space) / 12
                            slope_ei = ((slope * ei) / 12)  # if not peak keep slopping up
                        v += ((cur_x + ei, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x, -hi, last_z), (cur_x + ei, 0.0, last_z + slope_ei))
                        cur_x += baw  # place next row
                        if cur_x > ow / 2 and c_d == False:  # if past peak and peak not done yet
                            v += ((ow / 2, -hi, cur_z), (ow / 2, -hi, oh))
                            last_z = oh - ((slope * (cur_x - (ow / 2))) / 12)
                            c_d = True
                            face_normal = "s_2"
                            slope_ei = -((slope * ei) / 12)  # place peak and slope down other side
                        elif c_d == True:
                            last_z -= (slope * baw) / 12  # if already slopped countinue down
                        else:
                            last_z += (slope * baw) / 12
                            slope_ei = ((slope * ei) / 12)  # otherwise keep slopping up
                        v += ((cur_x, -hi, cur_z), (cur_x - ei, 0.0, cur_z), (cur_x - ei, 0.0, last_z - slope_ei), (cur_x, -hi, last_z))
                        cur_x += space  # Third Set
                        if cur_x > ow / 2 and c_d == False:  # if past peak and peak not done yet
                            v += ((ow / 2, 0.0, cur_z), (ow / 2, 0.0, oh))
                            last_z = oh - ((slope * (cur_x - (ow / 2))) / 12)
                            c_d = True
                            face_normal = "s_3"
                            slope_ei = -((slope * ei) / 12)  # place peak and slope down on other side
                        elif c_d == True:
                            last_z -= (slope * space) / 12  # slope down
                        else:
                            last_z += (slope * space) / 12
                            slope_ei = ((slope * ei) / 12)  # slope up
                        v += ((cur_x + ei, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x, -hi, last_z), (cur_x + ei, 0.0, last_z + slope_ei))
                        cur_x += baw  # Fourth Set
                        if cur_x > ow / 2 and c_d == False:  # peak
                            v += ((ow / 2, -hi, cur_z), (ow / 2, -hi, oh))
                            last_z = oh - ((slope * (cur_x - (ow / 2))) / 12)
                            face_normal = "s_4"  # place peak and slope down on other side
                        elif c_d == True:
                            last_z -= (slope * baw) / 12
                        v += ((cur_x, -hi, cur_z), (cur_x, -ei, cur_z), (cur_x, -ei, last_z), (cur_x, -hi, last_z))
                        cur_x -= ei
                        if cur_x < ow / 2:
                            last_z = oh - ((slope * ((ow / 2) - cur_x)) / 12)
                            cur_z = last_z
                        else:
                            last_z += (slope * ei) / 12
                            cur_z = last_z
                        for i in v:
                            verts.append(i)
                elif cur_x >= ow / 2:  # Sloping down
                    spacez = (slope * space) / 12
                    rsz = (slope * rsx) / 12
                    lsz = (slope * lsx) / 12
                    eiz = (slope * ei) / 12
                    l_b = False
                    v = [(cur_x, -tei, cur_z), (cur_x, 0.0, cur_z), (cur_x + space + ei, 0.0, cur_z), (cur_x + space, -hi, cur_z), (cur_x + rsx, -hi, cur_z)]
                    v += ((cur_x + rsx - ei, 0.0, cur_z), (cur_x + lsx + ei, 0.0, cur_z), (cur_x + lsx, -hi, cur_z), (cur_x + bw, -hi, cur_z), (cur_x + bw, -ei, cur_z))
                    if cur_z + bl > last_z - z_dif - 0.05 or is_length_vary == False:  # slope top
                        v += ((cur_x, -tei, last_z), (cur_x, 0.0, last_z), (cur_x + space + ei, 0.0, last_z - spacez - eiz), (cur_x + space, -hi, last_z - spacez), (cur_x + rsx, -hi, last_z - rsz))
                        v += ((cur_x + rsx - ei, 0.0, last_z - rsz + eiz), (cur_x + lsx + ei, 0.0, last_z - lsz - eiz), (cur_x + lsx, -hi, last_z - lsz), (cur_x + bw, -hi, last_z - z_dif), (cur_x + bw, -ei, last_z - z_dif))
                        l_b = "slope"
                    elif is_length_vary == True and cur_z + bl <= last_z - z_dif - 0.05:  # flat top
                        cur_z += bl
                        v += ((cur_x, -tei, cur_z), (cur_x, 0.0, cur_z), (cur_x + space + ei, 0.0, cur_z), (cur_x + space, -hi, cur_z), (cur_x + rsx, -hi, cur_z))
                        v += ((cur_x + rsx - ei, 0.0, cur_z), (cur_x + lsx + ei, 0.0, cur_z), (cur_x + lsx, -hi, cur_z), (cur_x + bw, -hi, cur_z), (cur_x + bw, -ei, cur_z))
                        l_b = "flat"
                    if cur_x + bw > ow:  # cut boards back
                        if l_b == "slope":
                            bottom = cur_z
                            top = last_z - (slope * (ow - cur_x)) / 12
                        elif l_b == "flat":
                            bottom = cur_z - bl
                            top = cur_z
                        if cur_x + space >= ow:  # cut back to beginning and then place last set of verts
                            del v[2:10]
                            del v[4: len(v)]
                            v.insert(2, (ow, 0.0, bottom))
                            v.insert(len(v), (ow, 0.0, top))
                            face_normal = "lev_one"
                        elif cur_x + rsx >= ow:
                            del v[4:10]
                            del v[8: len(v)]
                            v.insert(4, (ow, -hi, bottom))
                            v.insert(len(v), (ow, -hi, top))
                            face_normal = "lev_two"
                        elif cur_x + lsx >= ow:
                            del v[6:10]
                            del v[12: len(v)]
                            v.insert(6, (ow, 0.0, bottom))
                            v.insert(len(v), (ow, 0.0, top))
                            face_normal = "lev_three"
                        elif cur_x + bw > ow:
                            del v[8:10]
                            del v[16: len(v)]
                            v.insert(8, (ow, -hi, bottom))
                            v.insert(len(v), (ow, -hi, top))
                            face_normal = "lev_four"
                    else:
                        face_normal = True
                    if l_b == "slope":
                        cur_x += bw - ei
                        last_z -= z_dif - eiz
                        cur_z = last_z
                    elif l_b == "flat":
                        cur_z += ei
                    for i in v:
                        verts.append(i)
            counter += 1
            # faces
            if face_normal == True:
                f = ((p, p + 1, p + 11, p + 10), (p + 1, p + 2, p + 12, p + 11), (p + 2, p + 3, p + 13, p + 12), (p + 3, p + 4, p + 14, p + 13), (p + 4, p + 5, p + 15, p + 14),
                     (p + 5, p + 6, p + 16, p + 15), (p + 6, p + 7, p + 17, p + 16), (p + 7, p + 8, p + 18, p + 17), (p + 8, p + 9, p + 19, p + 18))
            elif face_normal == "lev_one":
                f = ((p, p + 1, p + 4, p + 3), (p + 1, p + 2, p + 5, p + 4))
            elif face_normal == "lev_two":
                f = ((p, p + 1, p + 6, p + 5), (p + 1, p + 2, p + 7, p + 6), (p + 2, p + 3, p + 8, p + 7), (p + 3, p + 4, p + 9, p + 8))
            elif face_normal == "lev_three":
                f = ((p, p + 1, p + 8, p + 7), (p + 1, p + 2, p + 9, p + 8), (p + 2, p + 3, p + 10, p + 9), (p + 3, p + 4, p + 11, p + 10), (p + 4, p + 5, p + 12, p + 11), (p + 5, p + 6, p + 13, p + 12))
            elif face_normal == "lev_four":
                f = ((p, p + 1, p + 10, p + 9), (p + 1, p + 2, p + 11, p + 10), (p + 2, p + 3, p + 12, p + 11), (p + 3, p + 4, p + 13, p + 12), (p + 4, p + 5, p + 14, p + 13),
                     (p + 5, p + 6, p + 15, p + 14), (p + 6, p + 7, p + 16, p + 15), (p + 7, p + 8, p + 17, p + 16))
            elif face_normal == "s_1":
                f = ((p, p + 1, p + 2, p + 3), (p + 1, p + 4, p + 5, p + 2), (p + 4, p + 6, p + 9, p + 5), (p + 6, p + 7, p + 8, p + 9), (p + 7, p + 10, p + 13, p + 8), (p + 10, p + 11, p + 12, p + 13),
                     (p + 11, p + 14, p + 17, p + 12), (p + 14, p + 15, p + 16, p + 17), (p + 15, p + 18, p + 21, p + 16), (p + 18, p + 19, p + 20, p + 21))
            elif face_normal == "s_2":
                f = ((p, p + 1, p + 2, p + 3), (p + 1, p + 4, p + 7, p + 2), (p + 4, p + 5, p + 6, p + 7), (p + 5, p + 8, p + 9, p + 6), (p + 8, p + 10, p + 13, p + 9), (p + 10, p + 11, p + 12, p + 13),
                     (p + 11, p + 14, p + 17, p + 12), (p + 14, p + 15, p + 16, p + 17), (p + 15, p + 18, p + 21, p + 16), (p + 18, p + 19, p + 20, p + 21))
            elif face_normal == "s_3":
                f = ((p, p + 1, p + 2, p + 3), (p + 1, p + 4, p + 7, p + 2), (p + 4, p + 5, p + 6, p + 7), (p + 5, p + 8, p + 11, p + 6), (p + 8, p + 9, p + 10, p + 11), (p + 9, p + 12, p + 13, p + 10),
                     (p + 12, p + 14, p + 17, p + 13), (p + 14, p + 15, p + 16, p + 17), (p + 15, p + 18, p + 21, p + 16), (p + 18, p + 19, p + 20, p + 21))
            elif face_normal == "s_4":
                f = ((p, p + 1, p + 2, p + 3), (p + 1, p + 4, p + 7, p + 2), (p + 4, p + 5, p + 6, p + 7), (p + 5, p + 8, p + 11, p + 6), (p + 8, p + 9, p + 10, p + 11), (p + 9, p + 12, p + 15, p + 10),
                     (p + 12, p + 13, p + 14, p + 15), (p + 13, p + 16, p + 17, p + 14), (p + 16, p + 18, p + 21, p + 17), (p + 18, p + 19, p + 20, p + 21))
            if face_normal != False:
                for i in f:
                    faces.append(i)
    return (verts, faces)


def vinyl_lap(oh, ow, is_slope, slope, is_length_vary, length_vary, bw, faces, verts, max_boards):  # vinyl horizontal lapped siding
    cur_z = 0.0
    start_x = 0.0
    tqi = 0.01905
    if is_slope == True:
        square = oh - ((slope * (ow / 2)) / 12)
        if square <= 0:  # recalculate slope if it would put the edges below zero
            slope = ((24 * oh) / ow) - 0.01
            square = oh - ((slope * (ow / 2)) / 12)
    else:
        square = oh
    last_x = ow
    y_step = tqi / bw
    x_dif = (bw * 12) / slope
    while cur_z < oh:
        cur_x = start_x
        counter = 1
        sd = False
        while cur_x < last_x:
            p = len(verts)
            face_normal = False
            if is_length_vary == True:
                l = (last_x - x_dif) - (start_x + x_dif)
                v = l * length_vary * 0.49
                bl = r_float((l / 2) - v, (l / 2) + v)
                bl += x_dif
            elif is_length_vary == False:
                bl = ow
            if cur_x + bl > ow or counter == max_boards:
                bl = ow - cur_x
            # verts
            if is_slope == False or cur_z + bw <= square:  # flat or below square
                if cur_z + bw > oh:
                    bw = oh - cur_z
                v = ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (cur_x, 0.0, cur_z + bw), (cur_x + bl, 0.0, cur_z), (cur_x + bl, -tqi, cur_z), (cur_x + bl, 0.0, cur_z + bw))
                for i in v:
                    verts.append(i)
                cur_x += bl + 0.003175
                face_normal = True
                if cur_x >= ow:
                    cur_z += bw
            elif cur_z < square and cur_z + bw > square:
                if is_length_vary == False:
                    y = tqi - ((square - cur_z) * y_step)
                    face_normal = "split"
                    s = ((cur_z + bw - square) * 12) / slope
                    v = ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (cur_x, -y, square), (cur_x + s, 0.0, cur_z + bw))
                    v += ((ow, 0.0, cur_z), (ow, -tqi, cur_z), (ow, -y, square), (ow - s, 0.0, cur_z + bw))
                    for i in v:
                        verts.append(i)
                    start_x = cur_x + s
                    last_x = ow - s
                    cur_z += bw
                    cur_x = last_x
                else:
                    if cur_x == 0.0:  # right side
                        y = tqi - ((square - cur_z) * y_step)
                        face_normal = "split"
                        s = ((cur_z + bw - square) * 12) / slope
                        v = ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (cur_x, -y, square), (cur_x + s, 0.0, cur_z + bw))
                        start_x = cur_x + s
                        cur_x += bl - s
                        v += ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (cur_x, -y, square), (cur_x, 0.0, cur_z + bw))
                        cur_x += 0.003175
                        for i in v:
                            verts.append(i)
                    elif cur_x + bl < last_x - x_dif and max_boards != 2:  # middle
                        v = ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z)(cur_x, 0.0, cur_z + bw))
                        cur_x += bl - 0.003175
                        v += ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (cur_x, 0.0, cur_z + bw))
                        cur_x += 0.003175
                        face_normal = True
                        for i in v:
                            verts.append(i)
                    else:  # right side
                        y = tqi - ((square - cur_z) * y_step)
                        face_normal = "split"
                        s = ((cur_z + bw - square) * 12) / slope
                        v = ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (cur_x, -y, square), (cur_x, 0.0, cur_z + bw))
                        v += ((ow, 0.0, cur_z), (ow, -tqi, cur_z), (ow, -y, square), (ow - s, 0.0, cur_z + bw))
                        last_x = ow - s
                        cur_x = last_x
                        cur_z += bw
                        for i in v:
                            verts.append(i)
            elif cur_z >= square and cur_z + bw < oh and is_slope == True:  # sloping
                if last_x - cur_x < 1 and sd == False and cur_x == start_x:
                    sd = True
                if is_length_vary == True and sd == False:
                    if cur_x == start_x:  # left
                        x1 = cur_x + x_dif
                        x2 = cur_x + bl
                        x3 = x2
                        start_x = x1
                        nx = cur_x + bl + 0.003175
                    elif cur_x + bl < last_x - x_dif:  # middle
                        x1 = cur_x
                        x2 = cur_x + bl
                        x3 = x2
                        nx = cur_x + bl + 0.003175
                    else:  # right
                        x1 = cur_x
                        x2 = last_x
                        x3 = last_x - x_dif
                        last_x -= x_dif
                        nx = last_x
                    v = ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (x1, 0.0, cur_z + bw), (x2, 0.0, cur_z), (x2, -tqi, cur_z), (x3, 0.0, cur_z + bw))
                    cur_x = nx
                    face_normal = True
                    for i in v:
                        verts.append(i)
                    if cur_x >= last_x:
                        cur_z += bw
                else:
                    v = ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (cur_x + x_dif, 0.0, cur_z + bw), (last_x, 0.0, cur_z), (last_x, -tqi, cur_z), (last_x - x_dif, 0.0, cur_z + bw))
                    for i in v:
                        verts.append(i)
                    start_x = cur_x + x_dif
                    last_x -= x_dif
                    cur_x = last_x
                    face_normal = True
                    cur_z += bw
            elif cur_z + bw >= oh and is_slope == True:  # triangle
                v = ((cur_x, 0.0, cur_z), (cur_x, -tqi, cur_z), (last_x, 0.0, cur_z), (last_x, -tqi, cur_z), (ow / 2, 0.0, oh))
                for i in v:
                    verts.append(i)
                cur_x = ow
                cur_z = oh
                face_normal = "triangle"
            counter += 1
            # faces
            if face_normal == True:
                faces.append((p, p + 3, p + 4, p + 1))
                faces.append((p + 1, p + 4, p + 5, p + 2))
            elif face_normal == "split":
                faces.append((p, p + 4, p + 5, p + 1))
                faces.append((p + 1, p + 5, p + 6, p + 2))
                faces.append((p + 2, p + 6, p + 7, p + 3))
            elif face_normal == "triangle":
                faces.append((p, p + 2, p + 3, p + 1))
                faces.append((p + 1, p + 3, p + 4))
    return (verts, faces)


def vinyl_dutch_lap(oh, ow, is_slope, slope, is_length_vary, length_vary, bw, faces, verts, max_boards):
    cur_z = 0.0
    last_x = ow
    start_x = 0.0
    if is_slope == True:
        square = oh - ((slope * (ow / 2)) / 12)  # z height where slope starts
        if square <= 0:  # recalculate slope if it would put the edges below zero
            slope = ((24 * oh) / ow) - 0.01
            square = oh - ((slope * (ow / 2)) / 12)
    else:
        square = oh
    bw = bw / 2
    bb = bw * (2 / 3)
    bt = bw * (1 / 3)
    hi = 0.01270
    y_step = hi / bt  # board width, board bottom width, board top width, half inch
    x_dif = (12 * bw) / slope
    bb_dif = (12 * bb) / slope
    bt_dif = (12 * bt) / slope  # x diff for board, x dif for board bottom, x dif for board top
    while cur_z < oh:
        cur_x = start_x
        counter = 1
        while cur_x < last_x:
            face_normal = False
            p = len(verts)
            sd = False
            if is_length_vary == True and counter != max_boards:  # figure board length
                l = (last_x - x_dif) - (start_x + x_dif)
                v = l * length_vary * 0.49
                bl = r_float((l / 2) - v, (l / 2) + v)
                bl += x_dif
            else:
                bl = ow
            if cur_x + bl > ow:
                bl = ow - cur_x
            # verts
            if is_slope == False or cur_z + bw <= square:  # flat or below square
                v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z))
                cur_z += bb
                if cur_z > oh:
                    cur_z = oh
                    v += ((cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z))
                    face_normal = "two"
                else:
                    v += ((cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z))
                    cur_z += bt
                    if cur_z > oh:
                        y = (cur_z - oh) * y_step
                        cur_z = oh
                        v += ((cur_x, -y, cur_z), (cur_x + bl, -y, cur_z))
                    else:
                        v += ((cur_x, 0.0, cur_z), (cur_x + bl, 0.0, cur_z))
                    face_normal = True
                for i in v:
                    verts.append(i)
                cur_x += bl + 0.003175
                if cur_x < ow:
                    cur_z -= bw
            elif is_slope == True and cur_z < square and cur_z + bw > square:  # middle board
                if is_length_vary == False:  # single board
                    v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (ow, -hi, cur_z), (ow, 0.0, cur_z))
                    cur_z += bb
                    if cur_z > square:
                        v += ((cur_x, -hi, square), (ow, -hi, square))
                        s = (12 * (cur_z - square)) / slope
                        cur_x += s
                        last_x -= s
                        sd = True
                    v += ((cur_x, -hi, cur_z), (last_x, -hi, cur_z))
                    cur_z += bt
                    if cur_z > square and sd == False:
                        y = (cur_z - square) * y_step
                        v += ((cur_x, -y, square), (ow, -y, square))
                        s = (12 * (cur_z - square)) / slope
                        cur_x += s
                        last_x -= s
                        sd = True
                    else:
                        cur_x += bt_dif
                        last_x -= bt_dif
                    v += ((cur_x, 0.0, cur_z), (last_x, 0.0, cur_z))
                    start_x = cur_x
                    cur_x = last_x
                    if sd == False:
                        face_normal = True
                    elif sd == True:
                        face_normal = "split"
                    for i in v:
                        verts.append(i)
                elif cur_x == start_x:  # left single
                    v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z))
                    cur_z += bb
                    if cur_z > square:
                        v += ((cur_x, -hi, square), (cur_x + bl, -hi, square))
                        s = (12 * (cur_z - square)) / slope
                        cur_x += s
                        bl -= s
                        sd = True
                    v += ((cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z))
                    cur_z += bt
                    if cur_z > square and sd == False:
                        y = (cur_z - square) * y_step
                        v += ((cur_x, -y, square), (cur_x + bl, -y, square))
                        s = (12 * (cur_z - square)) / slope
                        cur_x += s
                        bl -= s
                        sd = True
                    else:
                        cur_x += bt_dif
                        bl -= bt_dif
                    v += ((cur_x, 0.0, cur_z), (cur_x + bl, 0.0, cur_z))
                    start_x = cur_x
                    cur_x += bl + 0.003175
                    cur_z -= bw
                    if sd == False:
                        face_normal = True
                    elif sd == True:
                        face_normal = "split"
                    for i in v:
                        verts.append(i)
                elif cur_x + bl < last_x - x_dif - 0.1:  # middle single
                    v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z), (cur_x, -hi, cur_z + bb), (cur_x + bl, -hi, cur_z + bb))
                    v += ((cur_x, 0.0, cur_z + bw), (cur_x + bl, 0.0, cur_z + bw))
                    face_normal = True
                    cur_x += bl + 0.003175
                    for i in v:
                        verts.append(i)
                else:  # right single
                    v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (ow, -hi, cur_z), (ow, 0.0, cur_z))
                    cur_z += bb
                    if cur_z > square:
                        v += ((cur_x, -hi, square), (ow, -hi, square))
                        s = (12 * (cur_z - square)) / slope
                        last_x -= s
                        sd = True
                    v += ((cur_x, -hi, cur_z), (last_x, -hi, cur_z))
                    cur_z += bt
                    if cur_z > square and sd == False:
                        y = (cur_z - square) * y_step
                        v += ((cur_x, -y, square), (ow, -y, square))
                        s = (12 * (cur_z - square)) / slope
                        last_x -= s
                        sd = True
                    else:
                        last_x -= bt_dif
                    v += ((cur_x, 0.0, cur_z), (last_x, 0.0, cur_z))
                    cur_x = last_x
                    if sd == False:
                        face_normal = True
                    elif sd == True:
                        face_normal = "split"
                    for i in v:
                        verts.append(i)
            elif cur_z >= square and cur_z + bw < oh - 0.01:  # sloping
                if is_length_vary == False or last_x - start_x <= 1 and cur_x == start_x:  # single board
                    v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (last_x, -hi, cur_z), (last_x, 0.0, cur_z), (cur_x + bb_dif, -hi, cur_z + bb), (last_x - bb_dif, -hi, cur_z + bb))
                    v += ((cur_x + x_dif, 0.0, cur_z + bw), (last_x - x_dif, 0.0, cur_z + bw))
                    start_x = cur_x + x_dif
                    last_x -= x_dif
                    face_normal = True
                    cur_x = last_x
                    cur_z += bw
                    for i in v:
                        verts.append(i)
                elif cur_x == start_x:  # left single
                    v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z), (cur_x + bb_dif, -hi, cur_z + bb), (cur_x + bl, -hi, cur_z + bb))
                    v += ((cur_x + x_dif, 0.0, cur_z + bw), (cur_x + bl, 0.0, cur_z + bw))
                    start_x = cur_x + x_dif
                    cur_x += bl + 0.003175
                    face_normal = True
                    for i in v:
                        verts.append(i)
                elif cur_x + bl < last_x - x_dif:  # middle single
                    v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (cur_x + bl, -hi, cur_z), (cur_x + bl, 0.0, cur_z), (cur_x, -hi, cur_z + bb), (cur_x + bl, -hi, cur_z + bb))
                    v += ((cur_x, 0.0, cur_z + bw), (cur_x + bl, 0.0, cur_z + bw))
                    face_normal = True
                    cur_x += bl + 0.003175
                    for i in v:
                        verts.append(i)
                else:  # right single
                    v = ((cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (last_x, -hi, cur_z), (last_x, 0.0, cur_z), (cur_x, -hi, cur_z + bb), (last_x - bb_dif, -hi, cur_z + bb))
                    v += ((cur_x, 0.0, cur_z + bw), (last_x - x_dif, 0.0, cur_z + bw))
                    last_x -= x_dif
                    cur_z += bw
                    face_normal = True
                    cur_x = last_x
                    for i in v:
                        verts.append(i)
            else:  # triangle
                v = [(cur_x, 0.0, cur_z), (cur_x, -hi, cur_z), (last_x, -hi, cur_z), (last_x, 0.0, cur_z)]
                cur_z += bb
                if cur_z >= oh:
                    v.append((ow / 2, -hi, oh))
                    face_normal = "tri_lev_one"
                else:
                    v += ((cur_x + bb_dif, -hi, cur_z), (last_x - bb_dif, -hi, cur_z))
                    cur_z += bt
                    y = (cur_z - oh) * y_step
                    v.append((ow / 2, -y, oh))
                    face_normal = "tri_lev_two"
                cur_x = last_x
                cur_z = oh
                for i in v:
                    verts.append(i)
            counter += 1
            # faces
            if face_normal == True:
                faces.append((p, p + 3, p + 2, p + 1))
                faces.append((p + 1, p + 2, p + 5, p + 4))
                faces.append((p + 4, p + 5, p + 7, p + 6))
            elif face_normal == "two":
                faces.append((p, p + 3, p + 2, p + 1))
                faces.append((p + 1, p + 2, p + 5, p + 4))
            elif face_normal == "split":
                faces.append((p, p + 3, p + 2, p + 1))
                faces.append((p + 1, p + 2, p + 5, p + 4))
                faces.append((p + 4, p + 5, p + 7, p + 6))
                faces.append((p + 6, p + 7, p + 9, p + 8))
            elif face_normal == "tri_lev_one":
                faces.append((p, p + 3, p + 2, p + 1))
                faces.append((p + 1, p + 2, p + 4))
            elif face_normal == "tri_lev_two":
                faces.append((p, p + 3, p + 2, p + 1))
                faces.append((p + 1, p + 2, p + 5, p + 4))
                faces.append((p + 4, p + 5, p + 6))
    return (verts, faces)


def tin_normal(oh, ow, is_slope, slope, faces, verts):
    cur_x = 0.0
    cur_z = 0.0
    con = 39.3701
    osi = (1 / 16) / con
    hi = 0.5 / con
    eti = 0.8 / con
    nti = 0.9 / con
    fei = (5 / 8) / con
    tei = (3 / 8) / con
    nfei = 0.6875 / con
    oi = 1 / con
    otqi = 1.75 / con
    # one sixtenth in,        half in,     eight tenths inch, nine tenths,     five eigths,        three eights inch,    not five eights, one inch,    one &  three quarter inch
    ofei = oi + fei
    ohi = oi + hi
    qi = hi / 2
    ei = (1 / 8) / con
    tqi = otqi - oi
    if is_slope == True:
        square = oh - ((slope * (ow / 2)) / 12)  # z height where slope starts
        if square <= 0:  # recalculate slope if it would put the edges below zero
            slope = ((24 * oh) / ow) - 0.01
            square = oh - ((slope * (ow / 2)) / 12)
        hid = (hi * slope) / 12
        feid = (fei * slope) / 12
        nfeid = (nfei * slope) / 12
        cur_z = square
    while cur_x < ow:
        p = len(verts)
        face_normal = False
        # verts
        if is_slope == False:  # flat
            v2 = []
            a_e = False  # verts holder 2, at_edge for putting in last set of verts
            for i in range(4):
                if i == 0:
                    y = -osi
                else:
                    y = 0.0
                v = ((cur_x, y, cur_z), (cur_x, y, oh), (cur_x + hi, -eti + y, cur_z), (cur_x + hi, -eti + y, oh), (cur_x + fei, -nti + y, cur_z), (cur_x + fei, -nti + y, oh))  # Left Top Of Rib
                v += ((cur_x + nfei, -oi + y, cur_z), (cur_x + nfei, -oi + y, oh))
                cur_x += otqi
                v += ((cur_x - nfei, -oi + y, cur_z), (cur_x - nfei, -oi + y, oh), (cur_x - fei, -nti + y, cur_z), (cur_x - fei, -nti + y, oh))  # Right Mid Rib
                v += ((cur_x - hi, -eti + y, cur_z), (cur_x - hi, -eti + y, oh), (cur_x, 0.0 + y, cur_z), (cur_x, 0.0 + y, oh))
                cur_x += ofei
                for i in range(2):
                    v += ((cur_x, 0.0, cur_z), (cur_x, 0.0, oh), (cur_x + qi, -ei, cur_z), (cur_x + qi, -ei, oh))
                    cur_x += oi
                    v += ((cur_x, -ei, cur_z), (cur_x, -ei, oh), (cur_x + qi, 0.0, cur_z), (cur_x + qi, 0.0, oh))
                    cur_x += ohi + qi
                cur_x += ei
                for i in v:
                    v2.append(i)
            v2 += ((cur_x, 0.0, cur_z), (cur_x, 0.0, oh), (cur_x + hi, -eti, cur_z), (cur_x + hi, -eti, oh), (cur_x + fei, -nti, cur_z), (cur_x + fei, -nti, oh))  # Left Top Of Rib
            v2 += ((cur_x + nfei, -oi, cur_z), (cur_x + nfei, -oi, oh))
            cur_x += otqi
            v2 += ((cur_x - nfei, -oi, cur_z), (cur_x - nfei, -oi, oh), (cur_x - fei, -nti, cur_z), (cur_x - fei, -nti, oh))  # Right Mid Rib
            v2 += ((cur_x - hi, -eti, cur_z), (cur_x - hi, -eti, oh), (cur_x, 0.0, cur_z), (cur_x, 0.0, oh))
            cur_x -= otqi
            face_normal = True
            vts = []
            if cur_x + otqi > ow:  # chop off extra
                counter = 0
                for i in v2:
                    if i[0] <= ow:
                        vts.append(i)
                    elif i[0] > ow and a_e == False:
                        a_e = True
                        b_o = v2[counter - 1]
                        f_o = i
                        dif_x = f_o[0] - b_o[0]
                        dif_y = f_o[1] - b_o[1]
                        r_r = dif_y / dif_x
                        b = b_o[1] - (r_r * b_o[0])
                        y2 = (ow * r_r) + b
                        vts.append((ow, y2, cur_z))
                        vts.append((ow, y2, oh))
                    counter += 1
                f_t = int((len(vts) / 2) - 1)
            else:
                vts = v2
                f_t = 71
            for i in vts:
                verts.append(i)
        elif is_slope == True:  # slopped
            v2 = []
            a_e = False
            for i in range(4):
                # calculate z's coming up for rib
                x_list = [cur_x, cur_x + hi, cur_x + fei, cur_x + nfei, cur_x + otqi - nfei, cur_x + otqi - fei, cur_x + otqi - hi, cur_x + otqi, cur_x + otqi + ofei]
                z = []
                for x in x_list:
                    if x <= ow / 2:
                        cz = oh - ((((ow / 2) - x) * slope) / 12)
                    else:
                        cz = oh - (((x - (ow / 2)) * slope) / 12)
                    z.append(cz)
                if i == 0:
                    y = -osi
                else:
                    y = 0.0
                v = ((cur_x, y, 0.0), (cur_x, y, z[0]), (cur_x + hi, -eti + y, 0.0), (cur_x + hi, -eti + y, z[1]))
                v += ((cur_x + fei, -nti + y, 0.0), (cur_x + fei, -nti + y, z[2]), (cur_x + nfei, -oi + y, 0.0), (cur_x + nfei, -oi + y, z[3]))
                cur_x += otqi
                v += ((cur_x - nfei, -oi + y, 0.0), (cur_x - nfei, -oi + y, z[4]), (cur_x - fei, -nti + y, 0.0), (cur_x - fei, -nti + y, z[5]))
                v += ((cur_x - hi, -eti + y, 0.0), (cur_x - hi, -eti + y, z[6]), (cur_x, 0.0 + y, 0.0), (cur_x, 0.0 + y, z[7]))
                cur_x += ofei
                cur_z = z[8]
                for i in range(2):
                    x_list = [cur_x, cur_x + qi, cur_x + oi, cur_x + oi + qi, cur_x + ohi + oi + qi]
                    z = []
                    for x in x_list:
                        if x <= ow / 2:
                            cz = oh - ((((ow / 2) - x) * slope) / 12)
                        else:
                            cz = oh - (((x - (ow / 2)) * slope) / 12)
                        z.append(cz)
                    v += ((cur_x, 0.0, 0.0), (cur_x, 0.0, z[0]), (cur_x + qi, -ei, 0.0), (cur_x + qi, -ei, z[1]))
                    cur_x += oi
                    v += ((cur_x, -ei, 0.0), (cur_x, -ei, z[2]), (cur_x + qi, 0.0, 0.0), (cur_x + qi, 0.0, z[3]))
                    cur_x += ohi + qi
                    cur_z = z[4]
                cur_x += ei
                if cur_x <= ow / 2:
                    cur_z = oh - ((((ow / 2) - cur_x) * slope) / 12)
                else:
                    cur_z = oh - (((cur_x - (ow / 2)) * slope) / 12)
                for i in v:
                    v2.append(i)
            x_list = [cur_x, cur_x + hi, cur_x + fei, cur_x + nfei, cur_x + otqi - nfei, cur_x + otqi - fei, cur_x + otqi - hi, cur_x + otqi, cur_x - otqi]
            z = []
            for x in x_list:
                if x <= ow / 2:
                    cz = oh - ((((ow / 2) - x) * slope) / 12)
                else:
                    cz = oh - (((x - (ow / 2)) * slope) / 12)
                z.append(cz)
            v2 += ((cur_x, 0.0, 0.0), (cur_x, 0.0, z[0]), (cur_x + hi, -eti, 0.0), (cur_x + hi, -eti, z[1]))
            v2 += ((cur_x + fei, -nti, 0.0), (cur_x + fei, -nti, z[2]), (cur_x + nfei, -oi, 0.0), (cur_x + nfei, -oi, z[3]))
            cur_x += otqi
            v2 += ((cur_x - nfei, -oi, 0.0), (cur_x - nfei, -oi, z[4]), (cur_x - fei, -nti, 0.0), (cur_x - fei, -nti, z[5]))
            v2 += ((cur_x - hi, -eti, 0.0), (cur_x - hi, -eti, z[6]), (cur_x, 0.0, 0.0), (cur_x, 0.0, z[7]))
            cur_x -= otqi
            face_normal = True
            vts = []
            cur_z = z[8]
            # finalize verts
            if cur_x + otqi > ow:  # chop off extra
                counter = 0
                for i in v2:
                    if i[0] <= ow:
                        vts.append(i)
                    elif i[0] > ow and a_e == False:
                        a_e = True
                        b_o = v2[counter - 1]
                        f_o = i
                        dif_x = f_o[0] - b_o[0]
                        dif_y = f_o[1] - b_o[1]
                        r_r = dif_y / dif_x
                        b = b_o[1] - (r_r * b_o[0])
                        y2 = (ow * r_r) + b
                        vts.append((ow, y2, 0.0))
                        vts.append((ow, y2, square))
                    counter += 1
                f_t = int((len(vts) / 2) - 1)
            elif cur_x - 0.9144 < ow / 2 and cur_x > ow / 2:  # middle sheet
                counter = 0
                for i in v2:
                    vts.append(i)
                    if i[0] < ow / 2 and (v2[counter + 1])[0] > ow / 2:  # place middle set
                        b_o = i
                        f_o = v2[counter + 1]
                        dif_x = f_o[0] - b_o[0]
                        dif_y = f_o[1] - b_o[1]
                        r_r = dif_y / dif_x
                        b = b_o[1] - (r_r * b_o[0])
                        y2 = ((ow / 2) * r_r) + b
                        vts.append((ow / 2, y2, 0.0))
                        vts.append((ow / 2, y2, oh))
                    counter += 1
                f_t = int((len(vts) / 2) - 1)
            else:
                vts = v2
                f_t = 71
            for set in vts:
                verts.append(set)
        # faces
        if face_normal == True:
            for i in range(f_t):
                faces.append((p, p + 2, p + 3, p + 1))
                p += 2
    return (verts, faces)


def tin_angular(oh, ow, is_slope, slope, faces, verts):
    cur_x = 0.0
    cur_z = 0.0
    con = 39.3701
    # variables
    osi = (1 / 16) / con
    hi = (1 / 2) / con
    oqi = (5 / 4) / con
    ohi = (3 / 2) / con
    ti = ohi + hi
    qi = (1 / 4) / con
    ei = (1 / 8) / con
    if is_slope == True:
        square = oh - ((slope * (ow / 2)) / 12)  # z height where slope starts
        if square <= 0:  # recalculate slope if it would put the edges below zero
            slope = ((24 * oh) / ow) - 0.01
            square = oh - ((slope * (ow / 2)) / 12)
        cur_z = square
    while cur_x < ow:
        p = len(verts)
        face_normal = False
        # verts
        if is_slope == False:  # flat
            v2 = []
            a_e = False
            for i in range(3):
                if i == 0:
                    y = -osi
                else:
                    y = 0.0
                v = ((cur_x, y, 0.0), (cur_x, y, oh), (cur_x + hi, -oqi + y, 0.0), (cur_x + hi, -oqi + y, oh), (cur_x + ohi, -oqi + y, 0.0), (cur_x + ohi, -oqi + y, oh))
                v += ((cur_x + ti, 0.0 + y, 0.0), (cur_x + ti, 0.0 + y, oh))
                cur_x += 2 * ti
                for i in range(2):
                    v += ((cur_x, 0.0, 0.0), (cur_x, 0.0, oh), (cur_x + qi, -ei, 0.0), (cur_x + qi, -ei, oh), (cur_x + ohi, -ei, 0.0), (cur_x + ohi, -ei, oh))
                    cur_x += ohi
                    v += ((cur_x + qi, 0.0, 0.0), (cur_x + qi, 0.0, oh))
                    cur_x += qi + ti + hi
                cur_x -= hi
                for i in v:
                    v2.append(i)
            v2 += ((cur_x, 0.0, 0.0), (cur_x, 0.0, oh), (cur_x + hi, -oqi, 0.0), (cur_x + hi, -oqi, oh), (cur_x + ohi, -oqi, 0.0), (cur_x + ohi, -oqi, oh))
            v2 += ((cur_x + ti, 0.0, 0.0), (cur_x + ti, 0.0, oh))
            vts = []
            face_normal = True
            if cur_x + ti > ow:  # cut off extra
                counter = 0
                for i in v2:
                    if i[0] <= ow:
                        vts.append(i)
                    elif i[0] > ow and a_e == False:
                        a_e = True
                        b_o = v2[counter - 1]
                        f_o = i
                        dif_x = f_o[0] - b_o[0]
                        dif_y = f_o[1] - b_o[1]
                        r_r = dif_y / dif_x
                        b = b_o[1] - (r_r * b_o[0])
                        y2 = (ow * r_r) + b
                        vts.append((ow, y2, cur_z))
                        vts.append((ow, y2, oh))
                    counter += 1
                f_t = int((len(vts) / 2) - 1)
            else:
                vts = v2
                f_t = 38
            for i in vts:
                verts.append(i)
        elif is_slope == True:  # slope
            v2 = []
            a_e = False
            for i in range(3):
                if i == 0:
                    y = -osi
                else:
                    y = 0.0
                x_list = [cur_x, cur_x + hi, cur_x + ohi, cur_x + ti, cur_x + ti + ti]
                z = []
                for x in x_list:
                    if x <= ow / 2:
                        cz = oh - ((((ow / 2) - x) * slope) / 12)
                    else:
                        cz = oh - (((x - (ow / 2)) * slope) / 12)
                    z.append(cz)
                v = ((cur_x, y, 0.0), (cur_x, y, z[0]), (cur_x + hi, -oqi + y, 0.0), (cur_x + hi, -oqi + y, z[1]), (cur_x + ohi, -oqi + y, 0.0), (cur_x + ohi, -oqi + y, z[2]))
                v += ((cur_x + ti, 0.0 + y, 0.0), (cur_x + ti, 0.0 + y, z[3]))
                cur_x += 2 * ti
                cur_z = z[4]
                for i in range(2):
                    x_list = [cur_x, cur_x + qi, cur_x + ohi, cur_x + ohi + qi, cur_x + ohi + qi + ti + hi]
                    z = []
                    for x in x_list:
                        if x <= ow / 2:
                            cz = oh - ((((ow / 2) - x) * slope) / 12)
                        else:
                            cz = oh - (((x - (ow / 2)) * slope) / 12)
                        z.append(cz)
                    v += ((cur_x, 0.0, 0.0), (cur_x, 0.0, z[0]), (cur_x + qi, -ei, 0.0), (cur_x + qi, -ei, z[1]), (cur_x + ohi, -ei, 0.0), (cur_x + ohi, -ei, z[2]))
                    cur_x += ohi
                    v += ((cur_x + qi, 0.0, 0.0), (cur_x + qi, 0.0, z[3]))
                    cur_x += qi + ti + hi
                    cur_z = z[4]
                cur_x -= hi
                if cur_x <= ow / 2:
                    cur_z = oh - ((((ow / 2) - cur_x) * slope) / 12)
                else:
                    cur_z = oh - (((cur_x - (ow / 2)) * slope) / 12)
                for set in v:
                    v2.append(set)
            x_list = [cur_x, cur_x + hi, cur_x + ohi, cur_x + ti]
            z = []
            for x in x_list:
                if x <= ow / 2:
                    cz = oh - ((((ow / 2) - x) * slope) / 12)
                else:
                    cz = oh - (((x - (ow / 2)) * slope) / 12)
                z.append(cz)
            v2 += ((cur_x, 0.0, 0.0), (cur_x, 0.0, z[0]), (cur_x + hi, -oqi, 0.0), (cur_x + hi, -oqi, z[1]), (cur_x + ohi, -oqi, 0.0), (cur_x + ohi, -oqi, z[2]))
            v2 += ((cur_x + ti, 0.0, 0.0), (cur_x + ti, 0.0, z[3]))
            vts = []
            face_normal = True
            cur_z = z[0]
            if cur_x + ti > ow:  # cut off extra
                counter = 0
                for i in v2:
                    if i[0] <= ow:
                        vts.append(i)
                    elif i[0] > ow and a_e == False:
                        a_e = True
                        b_o = v2[counter - 1]
                        f_o = i
                        dif_x = f_o[0] - b_o[0]
                        dif_y = f_o[1] - b_o[1]
                        r_r = dif_y / dif_x
                        b = b_o[1] - (r_r * b_o[0])
                        y2 = (ow * r_r) + b
                        vts.append((ow, y2, 0.0))
                        vts.append((ow, y2, square))
                    counter += 1
                f_t = int((len(vts) / 2) - 1)
            elif cur_x - 0.9144 < ow / 2 and cur_x > ow / 2:  # middle sheet
                counter = 0
                for i in v2:
                    vts.append(i)
                    if i[0] < ow / 2 and (v2[counter + 1])[0] > ow / 2:  # place middle set
                        b_o = i
                        f_o = v2[counter + 1]
                        dif_x = f_o[0] - b_o[0]
                        dif_y = f_o[1] - b_o[1]
                        r_r = dif_y / dif_x
                        b = b_o[1] - (r_r * b_o[0])
                        y2 = ((ow / 2) * r_r) + b
                        vts.append((ow / 2, y2, 0.0))
                        vts.append((ow / 2, y2, oh))
                    counter += 1
                f_t = int((len(vts) / 2) - 1)
            else:
                vts = v2
                f_t = 38
            for i in vts:
                verts.append(i)
        # faces
        if face_normal == True:
            for i in range(f_t):
                faces.append((p, p + 2, p + 3, p + 1))
                p += 2
    return (verts, faces)


def bricks(oh, ow, is_slope, slope, b_w, b_h, b_offset, gap, ran_offset, b_vary, faces, verts):  # bricks
    cur_z = 0.0
    off = 1 / (100 / b_offset)
    last_x = ow
    depth = 3.5 / 39.3701
    offset = False
    while cur_z < oh:
        cur_x = 0.0
        if ran_offset == True:
            off = r_float(0.1 * b_vary, 1 * b_vary)
        while cur_x < last_x:
            # verts
            face_normal = False
            p = len(verts)
            b_w2 = b_w
            if cur_x == 0.0 and offset == True:
                b_w2 = b_w * off
            elif cur_x + b_w2 > last_x:
                b_w2 = last_x - cur_x
            if cur_z + b_h > oh:
                b_h = oh - cur_z
            v = ((cur_x, 0.0, cur_z), (cur_x, -depth, cur_z), (cur_x + b_w2, -depth, cur_z), (cur_x + b_w2, 0.0, cur_z))
            cur_z += b_h
            v += ((cur_x, 0.0, cur_z), (cur_x, -depth, cur_z), (cur_x + b_w2, -depth, cur_z), (cur_x + b_w2, 0.0, cur_z))
            cur_z -= b_h
            cur_x += b_w2 + gap
            face_normal = True
            for i in v:
                verts.append(i)
            # faces
            if face_normal == True:
                f = ((p, p + 3, p + 2, p + 1), (p, p + 1, p + 5, p + 4), (p + 1, p + 2, p + 6, p + 5), (p + 2, p + 3, p + 7, p + 6),
                     (p + 4, p + 5, p + 6, p + 7), (p, p + 4, p + 7, p + 3))
                for i in f:
                    faces.append(i)
        cur_z += gap + b_h
        if offset == False:
            offset = True
        elif offset == True:
            offset = False
    return (verts, faces)


def bricks_cut(oh, ow, slope):  # creates object to cut slope
    verts = []
    faces = []
    square = oh - ((slope * (ow / 2)) / 12)  # z height where slope starts
    if square <= 0:  # recalculate slope if it would put the edges below zero
        slope = ((24 * oh) / ow) - 0.01
        square = oh - ((slope * (ow / 2)) / 12)
    v = ((0.0, 0.5, square), (0.0, -0.5, square), (ow / 2, 0.5, oh), (ow / 2, -0.5, oh), (ow, 0.5, square), (ow, -0.5, square))
    v += ((0.0, 0.5, oh + 0.5), (0.0, -0.5, oh + 0.5), (ow / 2, 0.5, oh + 0.5), (ow / 2, -0.5, oh + 0.5), (ow, 0.5, oh + 0.5), (ow, -0.5, oh + 0.5))
    for i in v:
        verts.append(i)
    f = ((0, 2, 3, 1), (2, 4, 5, 3), (0, 1, 7, 6), (1, 3, 9, 7), (3, 5, 11, 9), (5, 4, 10, 11), (4, 2, 8, 10), (2, 0, 6, 8), (6, 7, 9, 8), (8, 9, 11, 10))
    for i in f:
        faces.append(i)
    return (verts, faces)


def bricks_mortar(oh, ow, m_d):  # creates mortar object
    verts = []
    faces = []
    depth = 3.5 / 39.3701
    y = depth - m_d
    v = ((0.0, 0.0, 0.0), (0.0, -y, 0.0), (ow, -y, 0.0), (ow, 0.0, 0.0), (0.0, 0.0, oh), (0.0, -y, oh), (ow, -y, oh), (ow, 0.0, oh))
    for i in v:
        verts.append(i)
    f = ((0, 3, 2, 1), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (0, 4, 7, 3), (4, 5, 6, 7))
    for i in f:
        faces.append(i)
    return (verts, faces)

# add object


def addSiding(context, mat, if_tin, if_wood, if_vinyl, is_slope, over_width, over_height, board_width,
              slope, is_width_vary, width_vary, is_cutout, num_cutouts, nc1, nc2, nc3, nc4, nc5, batten_width,
              board_space, is_length_vary, length_vary, max_boards, b_width, b_height, b_offset, b_gap, m_depth, b_ran_offset, b_vary):

    # convert measurements to imperial and round
    ow = round(over_width / 3.28084, 5)
    oh = round(over_height / 3.28084, 5)
    bw = round(board_width / 39.3701, 5)
    baw = round(batten_width / 39.3701, 5)
    bs = round(board_space / 39.3701, 5)
    b_w = round(b_width / 39.3701, 5)
    b_h = round(b_height / 39.3701, 5)
    b_gap = round(b_gap / 39.3701, 5)
    m_d = round(m_depth / 39.3701, 5)

    # evaluate cutouts
    cutouts = []
    if is_cutout == True:
        if nc1 != "" and num_cutouts >= 1:
            add = nc1.split(",")
            cutouts.append(add)
        if nc2 != "" and num_cutouts >= 2:
            add = nc2.split(",")
            cutouts.append(add)
        if nc3 != "" and num_cutouts >= 3:
            add = nc3.split(",")
            cutouts.append(add)
        if nc4 != "" and num_cutouts >= 4:
            add = nc4.split(",")
            cutouts.append(add)
        if nc5 != "" and num_cutouts >= 5:
            add = nc5.split(",")
            cutouts.append(add)
    cuts = []
    for i in cutouts:
        pre = []
        skip = False
        if len(i) == 4:
            for i2 in i:
                try:
                    i2 = round(float(i2) / 3.28084, 5)
                    pre.append(i2)
                except:
                    skip = True
        if skip == False and pre != []:
            cuts.append(pre)
    # determine corner points
    corner_data = []
    for i in cuts:
        cut = []
        cut.append(i[0])
        cut.append(i[1])  # Start X & Z
        cut.append(i[0] + i[3])
        cut.append(i[1] + i[2])  # Bottom > Right & Top > Left
        corner_data.append(cut)
    #verts and faces
    verts = []
    faces = []

    # Wood
    if mat == "1" and if_wood == "1":  # Wood > Vertical
        data_back = wood_vertical(oh, ow, is_slope, slope, is_width_vary, width_vary, bw, verts, faces, bs, is_length_vary, length_vary, max_boards)
        verts = data_back[0]
        faces = data_back[1]
    elif mat == "1" and if_wood == "2":  # Wood > Vertical: Tongue & Groove
        data_back = wood_ton_gro(oh, ow, is_slope, slope, bw, verts, faces, is_length_vary, length_vary, max_boards)
        verts = data_back[0]
        faces = data_back[1]
    elif mat == "1" and if_wood == "3":  # Wood > Vertical: Board & Batten
        data_back = wood_vertical(oh, ow, is_slope, slope, False, width_vary, bw, verts, faces, 0.00635, is_length_vary, length_vary, max_boards)
        verts = data_back[0]
        faces = data_back[1]
        batten_pos = data_back[2]
        # add battens
        if is_slope == True:
            z_dif = round(((slope * batten_width) / 12) / 39.3701, 5)
        else:
            z_dif = 0.0
        p = len(verts)
        c = 0.00635 / 2
        for i in batten_pos[1]:
            is_center = False
            cur_x = (i[0] + c) - (baw / 2)
            s_dif = (slope * (i[0] - cur_x)) / 12
            cur_z = i[1]
            if is_slope == True:
                if cur_x < ow / 2:
                    cur_z -= s_dif
                else:
                    cur_z += s_dif
            if cur_x + baw < ow:
                p = len(verts)
                verts.append((cur_x, -0.02539, 0.0))
                verts.append((cur_x, -0.04444, 0.0))  # Bottom > Left
                verts.append((cur_x + baw, -0.04444, 0.0))
                verts.append((cur_x + baw, -0.02539, 0.0))  # Bottom > Right
                verts.append((cur_x, -0.02539, cur_z))
                verts.append((cur_x, -0.04444, cur_z))  # Top > Left
                if is_slope == False:  # flat
                    verts.append((cur_x + baw, -0.04444, oh))
                    verts.append((cur_x + baw, -0.02539, oh))  # Top > Right
                elif is_slope == True:
                    if cur_x < ow / 2 and cur_x + baw < ow / 2:  # slope up
                        verts.append((cur_x + baw, -0.04444, cur_z + z_dif))
                        verts.append((cur_x + baw, -0.02539, cur_z + z_dif))  # Top > Right
                    elif cur_x < ow / 2 and cur_x + baw > ow / 2:  # middle board
                        del verts[len(verts) - 1]
                        del verts[len(verts) - 1]  # remove top > right set
                        verts.insert(len(verts) - 2, (ow / 2, -0.04444, 0.0))
                        verts.insert(len(verts) - 2, (ow / 2, -0.02539, 0.0))  # insert bottom middle set
                        z_pos = oh - ((slope * ((ow / 2) - cur_x)) / 12)  # figure out whats on left and calculate height
                        verts.append((cur_x, -0.02539, z_pos))
                        verts.append((cur_x, -0.04444, z_pos))  # Top > Left
                        verts.append((ow / 2, -0.04444, oh))
                        verts.append((ow / 2, -0.02539, oh))  # Top > Middle
                        z_pos = oh - ((slope * ((cur_x + baw) - (ow / 2))) / 12)  # figure out what on right and calculate height
                        verts.append((cur_x + baw, -0.04444, z_pos))
                        verts.append((cur_x + baw, -0.02539, z_pos))
                        is_center = True  # Top > Right
                    elif cur_x > ow / 2:  # slope down
                        verts.append((cur_x + baw, -0.04444, cur_z - z_dif))
                        verts.append((cur_x + baw, -0.02539, cur_z - z_dif))  # Top > Right
                if is_center == False:
                    a = ((p, p + 3, p + 2, p + 1), (p + 4, p + 5, p + 6, p + 7), (p, p + 1, p + 5, p + 4), (p + 1, p + 2, p + 6, p + 5),
                         (p + 2, p + 3, p + 7, p + 6), (p, p + 4, p + 7, p + 3))
                    for i in a:
                        faces.append(i)
                else:
                    a = ((p, p + 4, p + 7, p + 3), (p + 2, p + 3, p + 5, p + 4), (p + 6, p + 7, p + 8, p + 9), (p + 8, p + 10, p + 11, p + 9),
                         (p, p + 1, p + 7, p + 6), (p + 1, p + 2, p + 8, p + 7), (p + 2, p + 4, p + 10, p + 8), (p + 4, p + 5, p + 11, p + 10),
                         (p, p + 6, p + 9, p + 3), (p + 3, p + 9, p + 11, p + 5))
                    for i in a:
                        faces.append(i)
    elif mat == "1" and if_wood == "4":  # Wood > Horizontal: Lap
        data_back = wood_lap(oh, ow, is_slope, slope, bw, verts, faces, is_length_vary, length_vary, max_boards, 0.02540)
        verts = data_back[0]
        faces = data_back[1]
    elif mat == "1" and if_wood == "5":  # Wood > Horizontal: Lap Bevel
        data_back = wood_lap_bevel(oh, ow, is_slope, slope, bw, is_length_vary, length_vary, faces, verts, max_boards)
        verts = data_back[0]
        faces = data_back[1]
    # Vinyl
    elif mat == "2" and if_vinyl == "1":  # Vinyl > Vertical
        data_back = vinyl_vertical(oh, ow, is_slope, slope, is_length_vary, length_vary, bw, baw, faces, verts, max_boards)
        verts = data_back[0]
        faces = data_back[1]
    elif mat == "2" and if_vinyl == "2":  # Vinyl > Horizontal: Lap
        data_back = vinyl_lap(oh, ow, is_slope, slope, is_length_vary, length_vary, bw, faces, verts, max_boards)
        verts = data_back[0]
        faces = data_back[1]
    elif mat == "2" and if_vinyl == "3":  # EVinyl > Horizontal: Dutch Lap
        data_back = vinyl_dutch_lap(oh, ow, is_slope, slope, is_length_vary, length_vary, bw, faces, verts, max_boards)
        verts = data_back[0]
        faces = data_back[1]
    # Tin
    elif mat == "3" and if_tin == "1":  # Tin > Normal
        data_back = tin_normal(oh, ow, is_slope, slope, faces, verts)
        verts = data_back[0]
        faces = data_back[1]
    elif mat == "3" and if_tin == "2":  # Tin > Angular
        data_back = tin_angular(oh, ow, is_slope, slope, faces, verts)
        verts = data_back[0]
        faces = data_back[1]
    # Fiber Cement
    elif mat == "4":  # Fiber Cement > Horizontal: Half-Lap
        data_back = wood_lap(oh, ow, is_slope, slope, bw, verts, faces, is_length_vary, length_vary, max_boards, 0.009525)
        verts = data_back[0]
        faces = data_back[1]
    # Bricks
    elif mat == "5":  # Bricks
        data_back = bricks(oh, ow, is_slope, slope, b_w, b_h, b_offset, b_gap, b_ran_offset, b_vary, faces, verts)
        verts = data_back[0]
        faces = data_back[1]

    # create object
    me = bpy.data.meshes.new("siding")
    me.from_pydata(verts, [], faces)
    ob = bpy.data.objects.new("siding", me)
    context.scene.objects.link(ob)
    return (ob, corner_data)

# UI


class MEST_OT_primitive_add_siding(bpy.types.Operator):
    """Add Siding"""
    bl_idname = "mesh.primitive_add_siding"
    bl_label = "Add Siding"
    bl_description = "Siding Generator"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # get objects in scene
    mat = EnumProperty(items=(("1", "Wood", ""), ("2", "Vinyl", ""), ("3", "Tin", ""), ("4", "Fiber Cement", ""), ("5", "Bricks", "")),
                       default="1", name="")
    if_tin = EnumProperty(items=(("1", "Normal", ""), ("2", "Angular", "")), default="1",
                          name="")
    if_wood = EnumProperty(items=(("1", "Vertical", ""), ("2", "Vertical: Tongue & Groove", ""),
                                  ("3", "Vertical: Board & Batten", ""), ("4", "Horizontal: Lap", ""),
                                  ("5", "Horizontal: Lap Bevel", "")), default="1", name="")
    if_vinyl = EnumProperty(items=(("1", "Vertical", ""), ("2", "Horizontal: Lap", ""),
                                   ("3", "Horizontal: Dutch Lap", "")), default="1", name="")

    # measurements
    object_cut = BoolProperty(name="From Object?", default=False)
    is_slope = BoolProperty(name="Slope Top?", default=False)
    over_width = FloatProperty(name="Overall Width (ft)", min=1.0, max=100.0, default=20.0, description="Width From Left To Right In Feet")
    over_height = FloatProperty(name="Overall Height (ft)", min=2.0, max=50.0, default=8.0, description="Height in Feet")
    board_width = FloatProperty(name="Board Width (in)", min=4.0, max=12.0, default=6.0, description="Board Width (Or Average If Width Varience Is Checked) In Inches")
    batten_width = FloatProperty(name="Batten Width (in)", min=0.5, max=4.0, default=2.0, description="Width Of Batten In Inches")
    board_space = FloatProperty(name="Board Gap (in)", min=0.05, max=2.0, default=0.25, description="Gap Between Boards In Inches")
    slope = FloatProperty(name="Slope (X/12)", min=1.0, max=12.0, default=4.0, description="Slope In RISE/RUN Format In Inches")
    is_width_vary = BoolProperty(name="Vary Width?", default=False)
    width_vary = FloatProperty(name="Width Varience", min=0.1, max=1.0, default=0.25)
    is_cutout = BoolProperty(name="Cutouts?", default=False, description="Cutout Rectangles?")
    num_cutouts = IntProperty(name="# Cutouts", min=1, max=5, default=1)
    is_length_vary = BoolProperty(name="Vary Length?", default=False)
    length_vary = FloatProperty(name="Length Varience", min=0.1, max=1.0, default=0.25)
    max_boards = IntProperty(name="Max # Of Boards", min=2, max=6, default=2, description="Max Number Of Boards Possible To Be Placed")
    res = IntProperty(name="Bevel Resolution", min=1, max=6, default=1, description="Bevel Modifier  # Of Segments")
    rotation = FloatVectorProperty(name="", description="Rotate Siding", unit="ROTATION")
    x_off = FloatProperty(name="X-Offset", min=-100.0, max=100.0, default=0.0, description="Offset Side To Side")
    location = FloatVectorProperty(name="", description="Move Siding", subtype="TRANSLATION")
    # brick specific
    b_width = FloatProperty(name="Brick Width (in)", min=4.000, max=10.000, default=7.625, description="Brick Width")
    b_height = FloatProperty(name="Brick Height (in)", min=2.000, max=5.000, default=2.375, description="Brick Height")
    b_ran_offset = BoolProperty(name="Random Offset?", default=False, description="Random Offset Between Rows")
    b_offset = FloatProperty(name="Brick Offset", subtype="PERCENTAGE", min=0.01, max=100.0, default=50.0, description="Brick Offset Between Rows")
    b_gap = FloatProperty(name="Gap (in)", min=0.1, max=1, default=0.5, description="Gap Between Bricks")
    m_depth = FloatProperty(name="Mortar Depth (in)", min=0.1, max=1.0, default=0.25, description="Mortar Depth")
    b_vary = FloatProperty(name="Offset Varience", min=0.1, max=1.0, default=0.5, description="Offset Varience")
    is_bevel = BoolProperty(name="Bevel?", default=False, description="Bevel Brick *Vertices Add Up Quickly*")
    ####materials####
    is_material = BoolProperty(name="Cycles Materials?", default=False, description="Adds Cycles Materials")
    mat_color = FloatVectorProperty(name="Color", subtype="COLOR", default=(1.0, 1.0, 1.0), min=0.0, max=1.0, description="Color For Siding")
    is_preview = BoolProperty(name="Preview Material?", default=False, description="Preview Material On Object")
    im_scale = FloatProperty(name="Image Scale", max=10.0, min=0.1, default=1.0, description="Change Image Scaling")
    col_image = StringProperty(name="Color Image", subtype="FILE_PATH", description="File Path For Color Image")
    is_bump = BoolProperty(name="Normal Map?", default=False, description="Add Normal To Material?")
    norm_image = StringProperty(name="Normal Map Image", subtype="FILE_PATH", description="File Path For Normal Map Image")
    bump_amo = FloatProperty(name="Normal Stength", min=0.001, max=2.000, default=0.250, description="Normal Map Strength")
    # brick specific
    bump_type = EnumProperty(items=(("1", "Dimpled", ""), ("2", "Ridges", ""), ("3", "Flaky", ""), ("4", "Smooth", "")), name="Bump Type")
    color_style = EnumProperty(items=(("constant", "Constant", "Single Color"), ("speckled", "Speckled", "Speckled Pattern"), ("multiple", "Multiple", "Two Mixed Colors"), ("extreme", "Extreme", "Three Mixed Colors")), name="Color Style")
    mat_color2 = FloatVectorProperty(name="Color 2", subtype="COLOR", default=(1.0, 1.0, 1.0), min=0.0, max=1.0, description="Color 2 For Siding")
    mat_color3 = FloatVectorProperty(name="Color 3", subtype="COLOR", default=(1.0, 1.0, 1.0), min=0.0, max=1.0, description="Color 3 For Siding")
    color_sharp = FloatProperty(name="Color Sharpness", min=0.0, max=10.0, default=1.0, description="Sharpness Of Color Edges")
    mortar_color = FloatVectorProperty(name="Mortar Color", subtype="COLOR", default=(1.0, 1.0, 1.0), min=0.0, max=1.0, description="Color For Mortar")
    mortar_bump = FloatProperty(name="Mortar Bump", min=0.0, max=1.0, default=0.25, description="Mortar Bump Amount")
    brick_bump = FloatProperty(name="Brick Bump", min=0.0, max=1.0, default=0.25, description="Brick Bump Amount")
    color_scale = FloatProperty(name="Color Scale", min=0.01, max=20.0, default=1.0, description="Color Scale")
    bump_scale = FloatProperty(name="Bump Scale", min=0.01, max=20.0, default=1.0, description="Bump Scale")
    #Cutout Variables################################################################
    nc1 = StringProperty(name="", default="", description="X, Y, Height, Width In (ft)")
    nc2 = StringProperty(name="", default="", description="X, Y, Height, Width In (ft)")
    nc3 = StringProperty(name="", default="", description="X, Y, Height, Width In (ft)")
    nc4 = StringProperty(name="", default="", description="X, Y, Height, Width In (ft)")
    nc5 = StringProperty(name="", default="", description="X, Y, Height, Width In (ft)")

    @classmethod
    def poll(self, context):
        return context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        layout.label("Material:")
        layout.prop(self, "mat", icon="MATERIAL")

        # types
        layout.label("Type(s):")
        if self.mat == "1":
            layout.prop(self, "if_wood", icon="OBJECT_DATA")
            type = "wood"
        elif self.mat == "2":
            layout.prop(self, "if_vinyl", icon="OBJECT_DATA")
            type = "vinyl"
        elif self.mat == "3":
            layout.prop(self, "if_tin", icon="OBJECT_DATA")
            type = "tin"
        elif self.mat == "4":
            layout.label("Horizontal: Lap", icon="OBJECT_DATA")
            type = ""
        elif self.mat == "5":
            layout.label("Bricks", icon="OBJECT_DATA")

        # measurements
        layout.prop(self, "object_cut", icon="FACESEL")
        if self.object_cut == False:
            layout.prop(self, "over_width")
            layout.prop(self, "over_height")
            layout.separator()
        elif self.object_cut == True:
            layout.label("Using Active Object", icon="FACESEL")
            layout.prop(self, "x_off")
            layout.separator()
        if self.mat not in ("3", "5"):
            layout.prop(self, "board_width")
        elif self.mat == "3":
            layout.label("Sheet Lays: 36 (in)", icon="ARROW_LEFTRIGHT")
        if self.mat != "5":
            if type == "wood" and self.if_wood == "1":
                layout.prop(self, "board_space")
            if type == "vinyl" or type == "wood":
                if self.if_vinyl == "1" and type == "vinyl":
                    layout.prop(self, "batten_width")
                    if self.batten_width > (self.board_width / 2) - 0.125:
                        layout.label("Max Width: " + str(round((self.board_width / 2) - 0.125, 3)) + " in", icon="ERROR")
                elif self.if_wood == "3" and type == "wood":
                    layout.prop(self, "batten_width")
        elif self.mat == "5":
            layout.prop(self, "b_width")
            layout.prop(self, "b_height")
            layout.prop(self, "b_ran_offset", icon="NLA")
            if self.b_ran_offset == False:
                layout.prop(self, "b_offset")
            else:
                layout.prop(self, "b_vary")
            layout.separator()
            layout.prop(self, "b_gap")
            layout.prop(self, "m_depth")
            layout.prop(self, "is_bevel", icon="MOD_BEVEL")
            if self.is_bevel == True:
                layout.prop(self, "res", icon="OUTLINER_DATA_CURVE")
        layout.separator()
        if self.object_cut == False:
            layout.prop(self, "is_slope", icon="TRIA_UP")
            if self.is_slope == True:
                layout.label("Pitch x/12:", icon="LINCURVE")
                layout.prop(self, "slope")
                ht = round(self.over_height - ((self.slope * (self.over_width / 2)) / 12), 2)
                if ht <= 0:
                    slope = round(((24 * self.over_height) / self.over_width) - 0.01, 2)
                    ht = round(self.over_height - ((slope * (self.over_width / 2)) / 12), 2)
                    layout.label("Max Slope: " + str(slope), icon="ERROR")
                layout.label("Height At Edges: " + str(ht) + " ft", icon="TEXT")
        if self.mat != "5":
            if type == "wood":
                if self.if_wood == "1":
                    layout.prop(self, "is_width_vary", icon="UV_ISLANDSEL")
                    if self.is_width_vary == True:
                        layout.prop(self, "width_vary")
            if self.mat != "3":
                layout.prop(self, "is_length_vary", icon="NLA")
            if self.is_length_vary == True:
                layout.prop(self, "length_vary")
                layout.prop(self, "max_boards")
            if self.mat == "2":
                layout.prop(self, "res", icon="OUTLINER_DATA_CURVE")
        if self.object_cut == False:
            layout.prop(self, "is_cutout", icon="MOD_BOOLEAN")
            if self.is_cutout == True:
                layout.prop(self, "num_cutouts")
                layout.label("X, Z, Height, Width In (ft)")
                for i in range(1, self.num_cutouts + 1):
                    layout.label("Cutout " + str(i) + ":", icon="MOD_BOOLEAN")
                    layout.prop(self, "nc" + str(i))
        layout.separator()
        layout.prop(self, "is_material", icon="MATERIAL")
        layout.separator()
        if self.is_material == True:
            if self.mat in ("2", "3"):  # tin and vinyl
                layout.prop(self, "mat_color", icon="COLOR")
            elif self.mat in ("1", "4"):  # wood and fiber cement
                layout.prop(self, "col_image", icon="COLOR")
                print(self.col_image)
                layout.prop(self, "is_bump", icon="SMOOTHCURVE")
                if self.is_bump == True:  # add normal map
                    layout.prop(self, "norm_image", icon="TEXTURE")
                    layout.prop(self, "bump_amo")
                layout.prop(self, "im_scale", icon="MAN_SCALE")
            elif self.mat == "5":  # bricks
                layout.prop(self, "color_style", icon="COLOR")
                layout.prop(self, "mat_color", icon="COLOR")
                if self.color_style != "constant":
                    layout.prop(self, "mat_color2", icon="COLOR")
                if self.color_style == "extreme":
                    layout.prop(self, "mat_color3", icon="COLOR")
                layout.prop(self, "color_sharp")
                layout.prop(self, "color_scale")
                layout.separator()
                layout.prop(self, "mortar_color", icon="COLOR")
                layout.prop(self, "mortar_bump")
                layout.prop(self, "bump_type", icon="SMOOTHCURVE")
                if self.bump_type != "4":
                    layout.prop(self, "brick_bump")
                    layout.prop(self, "bump_scale")
            layout.separator()
            layout.prop(self, "is_preview", icon="SCENE")
        layout.label("Rotation (XYZ):", icon="MAN_ROT")
        layout.prop(self, "rotation")
        layout.label("Location:", icon="MAN_TRANS")
        layout.prop(self, "location")

    def execute(self, context):
        if bpy.context.scene.render.engine != "CYCLES":  # make cycles
            bpy.context.scene.render.engine == "CYCLES"
        ob = bpy.context.scene.objects.active
        enter = False
        if ob != None:
            if ob.type == "MESH":
                if ob.name.startswith("siding"):
                    pass
                else:
                    enter = True
        if self.object_cut == True and enter == False:
            self.report({"ERROR"}, "Object Not Valid")
        if self.object_cut == True and enter == True:
            pattern = bpy.context.scene.objects.active
            pattern_dim = tuple(pattern.dimensions)
            dims = []
            dims2 = []
            for i in pattern_dim:
                i += 0.1
                i *= 3.28084
                dims.append(i)
            for i in pattern_dim:
                i += 0.1
                dims2.append(i)
            db = addSiding(context, self.mat, self.if_tin, self.if_wood, self.if_vinyl, self.is_slope,
                           dims[0], dims[1], self.board_width, self.slope, self.is_width_vary, self.width_vary,
                           self.is_cutout, self.num_cutouts, self.nc1, self.nc2, self.nc3, self.nc4, self.nc5, self.batten_width,
                           self.board_space, self.is_length_vary, self.length_vary, self.max_boards, self.b_width, self.b_height,
                           self.b_offset, self.b_gap, self.m_depth, self.b_ran_offset, self.b_vary)
        else:
            db = addSiding(context, self.mat, self.if_tin, self.if_wood, self.if_vinyl, self.is_slope,
                           self.over_width, self.over_height, self.board_width, self.slope, self.is_width_vary, self.width_vary,
                           self.is_cutout, self.num_cutouts, self.nc1, self.nc2, self.nc3, self.nc4, self.nc5, self.batten_width,
                           self.board_space, self.is_length_vary, self.length_vary, self.max_boards, self.b_width, self.b_height,
                           self.b_offset, self.b_gap, self.m_depth, self.b_ran_offset, self.b_vary)
        ob = db[0]
        corner_data = db[1]
        #rotation and location
        if self.object_cut == False or enter == False:
            ob.location = bpy.context.scene.cursor_location
            ob.rotation_euler = self.rotation
        elif self.object_cut == True and enter == True:
            verts = [vert.co for vert in pattern.data.vertices]  # get vertex data
            tup_verts = [vert.to_tuple() for vert in verts]  # convert to tuples
            x = None
            z = None
            y = None
            for i in tup_verts:  # find smallest x and z values
                if x == None:
                    x = i[0]
                elif i[0] < x:
                    x = i[0]
                if z == None:
                    z = i[2]
                elif i[2] < z:
                    z = i[2]
                if y == None:
                    y = i[1]
                elif i[1] < y:
                    y = i[1]
            position = pattern.matrix_world * mathutils.Vector((x + self.x_off, y, z))  # get world space
            ob.location = tuple(position)
            eur = (pattern.rotation_euler).copy()
            eur.rotate_axis("X", radians(-90.0))  # subtract rotation from object to make up for rotating up
            ob.rotation_euler = eur
        # add mortar if bricks and materials
        if self.mat == "5":
            try:
                data_back = bricks_mortar(dims2[1], dims2[0], round(self.m_depth / 39.3701, 5))
            except:
                data_back = bricks_mortar(round(self.over_height / 3.28084, 5), round(self.over_width / 3.28084, 5), round(self.m_depth / 39.3701, 5))
            m_verts = data_back[0]
            m_faces = data_back[1]  # create mortar object
            me2 = bpy.data.meshes.new("mortar")
            me2.from_pydata(m_verts, [], m_faces)
            mortar = bpy.data.objects.new("mortar", me2)
            context.scene.objects.link(mortar)
            mortar.location = ob.location
            mortar.rotation_euler = ob.rotation_euler  # set position and rotation
            if self.is_material == True:
                try:
                    m_mat = bpy.data.materials.get("mortar")
                    m_mat.use_nodes = True  # add materials
                except:
                    m_mat = bpy.data.materials.new("mortar")
                    m_mat.use_nodes = True
                # figure brick name
                b_name = "brick_" + str(self.color_style) + "_" + str(self.bump_type)
                try:
                    b_mat = bpy.data.materials.get(b_name)
                    b_mat.use_nodes = True
                except:
                    b_mat = bpy.data.materials.new(b_name)
                    b_mat.use_nodes = True
                ob.data.materials.append(b_mat)
                mortar.data.materials.append(m_mat)
            if self.is_slope == False and (self.object_cut == False or enter == False) and self.is_cutout == False:
                already_selected = []
                scene = context.scene  # join mortar and bricks object
                for obs in scene.objects:
                    if obs.select == True:
                        already_selected.append(obs.name)
                    obs.select = False
                mortar.select = True
                ob.select = True
                bpy.context.scene.objects.active = ob
                name = ob.name
                bpy.ops.object.join()
                ob = bpy.data.objects[name]
                for i in already_selected:
                    (bpy.data.objects[i]).select = True
        # cut slope for bricks
        if self.mat == "5" and self.is_slope == True:
            data_back = bricks_cut(round(self.over_height / 3.28084, 5), round(self.over_width / 3.28084, 5), self.slope)
            s_verts = data_back[0]
            s_faces = data_back[1]
            me3 = bpy.data.meshes.new("slope_cut")
            me3.from_pydata(s_verts, [], s_faces)
            cut = bpy.data.objects.new("slope_cut", me3)
            context.scene.objects.link(cut)
            cut.location = ob.location
            cut.rotation_euler = ob.rotation_euler
            bpy.context.scene.objects.active = ob
            bpy.ops.object.modifier_add(type="BOOLEAN")
            bpy.context.object.modifiers["Boolean"].object = cut
            bpy.context.object.modifiers["Boolean"].operation = "DIFFERENCE"
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
            bpy.context.scene.objects.active = mortar
            bpy.ops.object.modifier_add(type="BOOLEAN")
            bpy.context.object.modifiers["Boolean"].object = cut
            bpy.context.object.modifiers["Boolean"].operation = "DIFFERENCE"
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
            already_selected = []
            scene = context.scene
            for obs in scene.objects:
                if obs.type == "MESH" and obs.name.startswith("slope_cut"):
                    obs.select = True
                else:
                    if obs.select == True:
                        already_selected.append(obs.name)
                    obs.select = False
            bpy.ops.object.delete()
            if (self.object_cut == False or enter == False) and self.is_cutout == False:
                mortar.select = True
                ob.select = True
                bpy.context.scene.objects.active = ob
                bpy.ops.object.join()
            for i in already_selected:
                (bpy.data.objects[i]).select = True
        elif self.mat == "2":  # vinyl: solidify and bevel
            bpy.context.scene.objects.active = ob
            bpy.ops.object.modifier_add(type="BEVEL")
            bpy.context.object.modifiers["Bevel"].width = 0.003048
            if self.if_vinyl == "3":
                bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
            bpy.context.object.modifiers["Bevel"].segments = self.res
            bpy.context.object.modifiers["Bevel"].limit_method = "ANGLE"
            bpy.context.object.modifiers["Bevel"].angle_limit = 1.4
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Bevel")
            bpy.ops.object.modifier_add(type="SOLIDIFY")
            bpy.context.object.modifiers["Solidify"].thickness = 0.002
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Solidify")
        elif self.mat == "3":  # tin solidify
            bpy.context.scene.objects.active = ob
            bpy.ops.object.modifier_add(type="SOLIDIFY")
            bpy.context.object.modifiers["Solidify"].thickness = 0.0003429
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Solidify")
        # bool objects
        if self.is_cutout == True:
            bool_stuff = bool(corner_data)
            if bool_stuff[0] != []:
                verts2 = bool_stuff[0]
                faces2 = bool_stuff[1]
                bool_me = bpy.data.meshes.new("bool")
                bool_me.from_pydata(verts2, [], faces2)
                bool_ob = bpy.data.objects.new("bool", bool_me)
                bpy.context.scene.objects.link(bool_ob)
                bool_ob.location = bpy.context.scene.cursor_location
                bool_ob.rotation_euler = self.rotation
                bpy.context.scene.objects.active = ob
                bpy.ops.object.modifier_add(type="BOOLEAN")
                bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[bool_ob.name]
                bpy.context.object.modifiers["Boolean"].operation = "DIFFERENCE"
                bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
                if self.mat == "5":  # bricks
                    bpy.context.scene.objects.active = mortar
                    bpy.ops.object.modifier_add(type="BOOLEAN")
                    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[bool_ob.name]
                    bpy.context.object.modifiers["Boolean"].operation = "DIFFERENCE"
                    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
                scene = context.scene
                for obs in scene.objects:
                    if obs.type == "MESH" and obs.name.startswith("bool"):
                        obs.select = True
                    else:
                        obs.select = False
                bpy.ops.object.delete()
                if self.mat == "5":
                    mortar.select = True
                    ob.select = True
                    bpy.context.scene.objects.active = ob
                    bpy.ops.object.join()
        elif self.object_cut == True and enter == True:
            bpy.context.scene.objects.active = pattern
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].thickness = 1
            bpy.context.object.modifiers["Solidify"].offset = 0
            bpy.context.scene.objects.active = ob
            bpy.ops.object.modifier_add(type="BOOLEAN")
            bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[pattern.name]
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
            if self.mat == "5":
                bpy.context.scene.objects.active = mortar
                bpy.ops.object.modifier_add(type="BOOLEAN")
                bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[pattern.name]
                bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
                already_selected = []
                scene = context.scene  # join mortar and bricks object
                for obs in scene.objects:
                    if obs.select == True:
                        already_selected.append(obs.name)
                    obs.select = False
                mortar.select = True
                ob.select = True
                bpy.context.scene.objects.active = ob
                name = ob.name
                bpy.ops.object.join()
                ob = bpy.data.objects[name]
                for i in already_selected:
                    (bpy.data.objects[i]).select = True
            bpy.context.scene.objects.active = pattern
            bpy.ops.object.modifier_remove(modifier="Solidify")
        # bevel bricks
        if self.is_bevel == True and self.mat == "5":
            bpy.context.scene.objects.active = ob
            bpy.ops.object.modifier_add(type="BEVEL")
            bpy.context.object.modifiers["Bevel"].width = 0.0024384
            bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
            bpy.context.object.modifiers["Bevel"].segments = self.res
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Bevel")
        # materials
        bpy.context.scene.objects.active = ob
        rgba = list(self.mat_color)
        rgba.append(1.0)
        if self.is_material == True and self.mat not in ("1", "5"):  # tin or vinyl or fibercement
            if self.mat == "2":
                mat_name = "vinyl_siding"
                rough = 0.3
            elif self.mat == "3":
                mat_name = "tin_siding"
                rough = 0.18
            elif self.mat == "4":
                mat_name = "fibercement_siding"
                rough = 0.35
            try:
                mat = bpy.data.materials.get(mat_name)
                mat.use_nodes = True
                mat.diffuse_color = (rgba[0], rgba[1], rgba[2])
                nodes = mat.node_tree.nodes
                node = nodes["Diffuse BSDF"]
                node.color = rgba
                ob.data.materials.append(mat)
            except:
                mat = bpy.data.materials.new(mat_name)
                mat.use_nodes = True
                nodes = mat.node_tree.nodes
                node = nodes["Diffuse BSDF"]
                mat.node_tree.nodes.remove(node)
                node = nodes.new("ShaderNodeBsdfDiffuse")
                node.inputs[0].default_value = rgba
                node.location = -100, 400
                mat.diffuse_color = (rgba[0], rgba[1], rgba[2])
                node = nodes.new("ShaderNodeBsdfGlossy")
                node.name = "Glossy"
                node.inputs[1].default_value = rough
                node.location = -100, 200
                node = nodes.new("ShaderNodeMixShader")
                node.name = "Mix"
                node.location = 100, 300
                node.inputs[0].default_value = 0.05
                outN = nodes["Diffuse BSDF"].outputs[0]
                inN = nodes["Mix"].inputs[1]
                mat.node_tree.links.new(outN, inN)
                outN = nodes["Glossy"].outputs[0]
                inN = nodes["Mix"].inputs[2]
                mat.node_tree.links.new(outN, inN)
                outN = nodes["Mix"].outputs[0]
                inN = nodes["Material Output"].inputs[0]
                mat.node_tree.links.new(outN, inN)
                ob.data.materials.append(mat)
        elif self.is_material == True and self.mat == "1":  # wood
            ob.select = True
            mat_name = "wood_siding"
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            override = bpy.context.copy()
                            override["area"] = area
                            override["region"] = region
                            override["active_object"] = (bpy.context.selected_objects)[0]
                            bpy.ops.uv.smart_project(override)
            mat_enter = False
            mat_enter2 = False
            for im in bpy.data.images:  # check for images
                if im.filepath == self.col_image and mat_enter == False:
                    col_im = im
                    enter = True
                if im.filepath == self.norm_image and mat_enter2 == False and self.is_bump == True:
                    norm_im = im
                    mat_enter2 = True
            if mat_enter == False and self.col_image != "":
                col_im = bpy.data.images.load(self.col_image)
            if self.is_bump == True and mat_enter2 == False and self.norm_image != "":
                norm_im = bpy.data.images.load(self.norm_image)
            try:  # update current material
                mat = bpy.data.materials.get(mat_name)
                mat.use_nodes = True
                nodes = mat.node_tree.nodes
                node = nodes["scale"]
                node.scale = (self.im_scale, self.im_scale, self.im_scale)
                node = nodes["color_image"]
                node.image = col_im
                node = nodes["normal_image"]
                if self.is_bump == True:
                    node.image = norm_im
                node = nodes["normal_map"]
                node.inputs[0].default_value = self.bump_amo
                node = nodes["math"]
                if self.is_bump == True:
                    node.inputs[1].default_value = 1.0
                else:
                    node.inputs[1].default_value = 0.0
                ob.data.materials.append(mat)
            except:
                mat = bpy.data.materials.new(mat_name)
                mat.use_nodes = True
                nodes = mat.node_tree.nodes
                node = nodes.new("ShaderNodeTexCoord")
                node.location = -700, 0
                node.name = "uv_coords"
                node = nodes.new("ShaderNodeMapping")
                node.location = -500, 0
                node.name = "scale"
                node.scale = (self.im_scale, self.im_scale, self.im_scale)
                node = nodes.new("ShaderNodeTexImage")
                node.location = -100, 150
                node.name = "color_image"
                node.image = col_im
                node = nodes.new("ShaderNodeTexImage")
                node.location = -100, -150
                node.name = "normal_image"
                if self.is_bump == True:
                    node.image = norm_im
                node = nodes["Diffuse BSDF"]
                node.location = 100, 100
                node.name = "diffuse"
                node = nodes.new("ShaderNodeNormalMap")
                node.location = 100, -100
                node.name = "normal_map"
                node.inputs[0].default_value = self.bump_amo
                node = nodes.new("ShaderNodeMath")
                node.location = 300, -100
                node.name = "math"
                node.operation = "MULTIPLY"
                if self.is_bump == True:
                    node.inputs[1].default_value = 1.0
                else:
                    node.inputs[1].default_value = 0.0
                node = nodes["Material Output"]
                node.location = 500, 0
                o = nodes["uv_coords"].outputs[2]
                i = nodes["scale"].inputs[0]
                mat.node_tree.links.new(o, i)
                o = nodes["scale"].outputs[0]
                i = nodes["color_image"].inputs[0]
                mat.node_tree.links.new(o, i)
                o = nodes["scale"].outputs[0]
                i = nodes["normal_image"].inputs[0]
                mat.node_tree.links.new(o, i)
                o = nodes["color_image"].outputs[0]
                i = nodes["diffuse"].inputs[0]
                mat.node_tree.links.new(o, i)
                o = nodes["normal_image"].outputs[0]
                i = nodes["normal_map"].inputs[1]
                mat.node_tree.links.new(o, i)
                o = nodes["normal_map"].outputs[0]
                i = nodes["math"].inputs[0]
                mat.node_tree.links.new(o, i)
                o = nodes["math"].outputs[0]
                i = nodes["Material Output"].inputs[2]
                mat.node_tree.links.new(o, i)
                ob.data.materials.append(mat)
        elif self.is_material == True and self.mat == "5":  # brick
            ob.select = True  # uv unwrap
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            bpy.ops.object.editmode_toggle()
                            override = bpy.context.copy()
                            override["area"] = area
                            override["region"] = region
                            override["active_object"] = (bpy.context.selected_objects)[0]
                            bpy.ops.mesh.select_all()
                            bpy.ops.uv.cube_project(override)
                            bpy.ops.object.editmode_toggle()
            # mortar
            mat = bpy.data.materials.get("mortar")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            mat.diffuse_color = self.mortar_color
            if len(nodes) > 2:  # update
                node = nodes["Diffuse BSDF"]
                node.inputs[0].default_value = (self.mortar_color[0], self.mortar_color[1], self.mortar_color[2], 1.0)
                node = nodes["b_amount"]
                node.inputs[1].default_value = self.mortar_bump
            else:  # create
                node = nodes["Diffuse BSDF"]
                node.inputs[0].default_value = (self.mortar_color[0], self.mortar_color[1], self.mortar_color[2], 1.0)
                node = nodes.new("ShaderNodeTexCoord")
                node.name = "uv_coords"
                node.location = -700, 200
                node = nodes.new("ShaderNodeMapping")
                node.name = "scale"
                node.location = -500, 200
                node.scale = (15.0, 15.0, 15.0)
                node = nodes.new("ShaderNodeTexNoise")
                node.name = "b_noise"
                node.location = -150, 200
                node.inputs[1].default_value = 100.0
                node = nodes.new("ShaderNodeMath")
                node.name = "b_amount"
                node.location = 50, 100
                node.operation = "MULTIPLY"
                node.inputs[1].default_value = self.mortar_bump
                # connections
                o = nodes["uv_coords"].outputs[2]
                i = nodes["scale"].inputs[0]
                mat.node_tree.links.new(o, i)
                o = nodes["scale"].outputs[0]
                i = nodes["b_noise"].inputs[0]
                mat.node_tree.links.new(o, i)
                o = nodes["b_noise"].outputs[1]
                i = nodes["b_amount"].inputs[0]
                mat.node_tree.links.new(o, i)
                o = nodes["b_amount"].outputs[0]
                i = nodes["Material Output"].inputs[2]
                mat.node_tree.links.new(o, i)
            # brick
            b_name = "brick_" + str(self.color_style) + "_" + str(self.bump_type)
            mat = bpy.data.materials.get(b_name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            mat.diffuse_color = self.mat_color
            if self.color_style == "constant":  # single color
                node = nodes["Diffuse BSDF"]
                node.inputs[0].default_value = (self.mat_color[0], self.mat_color[1], self.mat_color[2], 1.0)
            elif self.color_style == "speckled":  # speckled
                if len(nodes) > 2:  # update
                    node = nodes["scale"]
                    node.scale = (self.color_scale * 2.0, self.color_scale * 2.0, self.color_scale * 2.0)
                    node = nodes["color_vary"]
                    node.inputs[2].default_value = self.color_sharp * 2
                    nodes["color1"].outputs[0].default_value = (self.mat_color[0], self.mat_color[1], self.mat_color[2], 1.0)
                    nodes["color2"].outputs[0].default_value = (self.mat_color2[0], self.mat_color2[1], self.mat_color2[2], 1.0)
                else:  # create
                    node = nodes.new("ShaderNodeTexCoord")
                    node.name = "uv_coords"
                    node.location = -1500, 200
                    node = nodes.new("ShaderNodeMapping")
                    node.name = "scale"
                    node.location = -1300, 200
                    node.scale = (self.color_scale * 2.0, self.color_scale * 2.0, self.color_scale * 2.0)
                    node.label = "Color Scale"
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "c_noise1"
                    node.location = -1200, 400
                    node.inputs[1].default_value = 2.0
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "c_noise2"
                    node.location = -1200, 600
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "cn1|cn2"
                    node.location = -1000, 475
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "color_vary"
                    node.location = -850, 400
                    node.inputs[2].default_value = self.color_sharp * 2.0
                    node.label = "Color Sharpness"
                    node = nodes.new("ShaderNodeRGB")
                    node.name = "color1"
                    node.location = -900, 50
                    node.outputs[0].default_value = (self.mat_color[0], self.mat_color[1], self.mat_color[2], 1.0)
                    node.label = "Color 1"
                    node = nodes.new("ShaderNodeRGB")
                    node.name = "color2"
                    node.location = -900, 250
                    node.outputs[0].default_value = (self.mat_color2[0], self.mat_color2[1], self.mat_color2[2], 1.0)
                    node.label = "Color 2"
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "c1|c2"
                    node.location = -700, 300
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "c1Xc2"
                    node.location = -700, 100
                    node.blend_type = "MULTIPLY"
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "c_noise3"
                    node.location = -1000, 700
                    node.inputs[1].default_value = 600.0
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "contrast"
                    node.location = -800, 700
                    node.inputs[2].default_value = 6.0
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "c_noise4"
                    node.location = -800, 575
                    node.inputs[1].default_value = 1000.0
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "con|cn4"
                    node.location = -600, 600
                    node.inputs[1].default_value = (0.0, 0.0, 0.0, 1.0)
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "contrast2"
                    node.location = -400, 400
                    node.inputs[2].default_value = 4.0
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "final|"
                    node.location = -200, 300
                    links = [["uv_coords", 2, "scale", 0], ["uv_coords", 2, "c_noise3", 0], ["uv_coords", 2, "c_noise4", 0], ["scale", 0, "c_noise1", 0], ["scale", 0, "c_noise2", 0],
                             ["c_noise1", 1, "cn1|cn2", 2], ["c_noise2", 1, "cn1|cn2", 1], ["cn1|cn2", 0, "color_vary", 0], ["color_vary", 0, "c1|c2", 0], ["color1", 0, "c1|c2", 1],
                             ["color2", 0, "c1|c2", 2], ["color1", 0, "c1Xc2", 1], ["color2", 0, "c1Xc2", 2], ["c1|c2", 0, "final|", 1], ["c1Xc2", 0, "final|", 2],
                             ["c_noise3", 1, "contrast", 0], ["contrast", 0, "con|cn4", 0], ["c_noise4", 1, "con|cn4", 2], ["con|cn4", 0, "contrast2", 0], ["contrast2", 0, "final|", 0], ["final|", 0, "Diffuse BSDF", 0]]
                    for i in links:
                        o = nodes[i[0]].outputs[i[1]]
                        i = nodes[i[2]].inputs[i[3]]
                        mat.node_tree.links.new(o, i)
            elif self.color_style == "multiple":  # multiple mixed
                if len(nodes) > 2:  # update
                    nodes["scale"].scale = (self.color_scale, self.color_scale, self.color_scale)
                    nodes["color_vary"].inputs[2].default_value = self.color_sharp
                    nodes["color1"].outputs[0].default_value = (self.mat_color[0], self.mat_color[1], self.mat_color[2], 1.0)
                    nodes["color2"].outputs[0].default_value = (self.mat_color2[0], self.mat_color2[1], self.mat_color2[2], 1.0)
                else:  # create
                    node = nodes.new("ShaderNodeTexCoord")
                    node.name = "uv_coords"
                    node.location = -1100, 300
                    node = nodes.new("ShaderNodeMapping")
                    node.name = "scale"
                    node.location = -925, 350
                    node.scale = (self.color_scale, self.color_scale, self.color_scale)
                    node.label = "Color Scale"
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "c_noise"
                    node.location = -600, 600
                    node.inputs[1].default_value = 4.0
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "color_vary"
                    node.location = -400, 500
                    node.inputs[2].default_value = self.color_sharp
                    node.label = "Color Sharpness"
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "c1|c2"
                    node.location = -200, 450
                    node = nodes.new("ShaderNodeRGB")
                    node.name = "color1"
                    node.location = -500, 175
                    node.outputs[0].default_value = (self.mat_color[0], self.mat_color[1], self.mat_color[2], 1.0)
                    node.label = "Color 1"
                    node = nodes.new("ShaderNodeRGB")
                    node.name = "color2"
                    node.location = -500, 375
                    node.outputs[0].default_value = (self.mat_color2[0], self.mat_color2[1], self.mat_color2[2], 1.0)
                    node.label = "Color 2"
                    links = [["uv_coords", 2, "scale", 0], ["scale", 0, "c_noise", 0], ["c_noise", 1, "color_vary", 0], ["color_vary", 0, "c1|c2", 0], ["color1", 0, "c1|c2", 2], ["color2", 0, "c1|c2", 1], ["c1|c2", 0, "Diffuse BSDF", 0]]
                    for i in links:
                        o = nodes[i[0]].outputs[i[1]]
                        i = nodes[i[2]].inputs[i[3]]
                        mat.node_tree.links.new(o, i)
            elif self.color_style == "extreme":  # three colors
                if len(nodes) > 2:  # update
                    nodes["scale"].scale = (self.color_scale, self.color_scale, self.color_scale)
                    nodes["c_v1"].inputs[2].default_value = self.color_sharp
                    nodes["color1"].outputs[0].default_value = (self.mat_color[0], self.mat_color[1], self.mat_color[2], 1.0)
                    nodes["color2"].outputs[0].default_value = (self.mat_color2[0], self.mat_color2[1], self.mat_color2[2], 1.0)
                    nodes["color3"].outputs[0].default_value = (self.mat_color3[0], self.mat_color3[1], self.mat_color3[2], 1.0)
                    nodes["c_v2"].inputs[2].default_value = self.color_sharp * 1.25
                    nodes["c_v3"].inputs[2].default_value = self.color_sharp * 1.25
                else:  # create
                    node = nodes.new("ShaderNodeTexCoord")
                    node.name = "uv_coords"
                    node.location = -1700, 400
                    node = nodes.new("ShaderNodeMapping")
                    node.name = "scale"
                    node.location = -1500, 400
                    node.scale = (self.color_scale, self.color_scale, self.color_scale)
                    node.label = "Color Scale"
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "c_noise"
                    node.location = -1100, 600
                    node.inputs[1].default_value = 10.0
                    node = nodes.new("ShaderNodeRGB")
                    node.name = "color3"
                    node.location = -1150, 800
                    node.outputs[0].default_value = (self.mat_color3[0], self.mat_color3[1], self.mat_color3[2], 1.0)
                    node.label = "Color 3"
                    node = nodes.new("ShaderNodeRGB")
                    node.name = "color2"
                    node.location = -1050, 400
                    node.outputs[0].default_value = (self.mat_color2[0], self.mat_color2[1], self.mat_color2[2], 1.0)
                    node.label = "Color 2"
                    node = nodes.new("ShaderNodeRGB")
                    node.name = "color1"
                    node.location = -1050, 200
                    node.outputs[0].default_value = (self.mat_color[0], self.mat_color[1], self.mat_color[2], 1.0)
                    node.label = "Color 1"
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "c_v1"
                    node.location = -900, 525
                    node.inputs[2].default_value = self.color_sharp
                    node.label = "Color Sharpness 1"
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "c1|c2"
                    node.location = -700, 400
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "c_noise2"
                    node.location = -900, 800
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "c_v2"
                    node.location = -700, 700
                    node.inputs[2].default_value = self.color_sharp * 1.25
                    node.label = "Color Sharpness 2"
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "c3|c2c1"
                    node.location = -500, 600
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "c_noise3"
                    node.location = -600, 900
                    node.inputs[1].default_value = 50.0
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "c_v3"
                    node.location = -400, 800
                    node.inputs[2].default_value = self.color_sharp * 1.25
                    node.label = "Color Sharpness 3"
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "c1|c2.2"
                    node.location = -400, 400
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "final|"
                    node.location = -250, 600
                    links = [["uv_coords", 2, "scale", 0], ["scale", 0, "c_noise", 0], ["scale", 0, "c_noise2", 0], ["scale", 0, "c_noise3", 0], ["c_noise", 1, "c_v1", 0], ["c_v1", 0, "c1|c2", 0],
                             ["color1", 0, "c1|c2", 2], ["color2", 0, "c1|c2", 1], ["color1", 0, "c1|c2.2", 2], ["color2", 0, "c1|c2.2", 1], ["color3", 0, "c3|c2c1", 1], ["c_noise2", 1, "c_v2", 0],
                             ["c_v2", 0, "c3|c2c1", 0], ["c1|c2", 0, "c3|c2c1", 2], ["c_noise3", 1, "c_v3", 0], ["c_v3", 0, "final|", 0], ["c3|c2c1", 0, "final|", 2], ["c1|c2.2", 0, "final|", 1], ["final|", 0, "Diffuse BSDF", 0]]
                    for i in links:
                        o = nodes[i[0]].outputs[i[1]]
                        i = nodes[i[2]].inputs[i[3]]
                        mat.node_tree.links.new(o, i)
            # bump
            if self.color_style == "constant":  # get uv_coords if constant because that material doesn't have one yet
                node = nodes.new("ShaderNodeTexCoord")
                node.name = "uv_coords"
                node.location = -1700, 400
            if self.bump_type == "1":  # dimpled
                try:  # update
                    nodes["b_scale"].scale = (self.bump_scale, self.bump_scale, self.bump_scale)
                    nodes["b_amount"].inputs[1].default_vale = self.brick_bump
                except:  # create
                    node = nodes.new("ShaderNodeMapping")
                    node.name = "b_scale"
                    node.location = -700, -100
                    node.scale = (self.bump_scale, self.bump_scale, self.bump_scale)
                    node.label = "Scale Amount"
                    node.label = "Bump Scale"
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "b_noise"
                    node.location = -300, 0
                    node.inputs[1].default_value = 400.0
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "b_noise2"
                    node.location = -300, -200
                    node.inputs[1].default_value = 200.0
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "bn|bn2"
                    node.location = -100, -100
                    node = nodes.new("ShaderNodeMath")
                    node.name = "b_amount"
                    node.location = 100, 0
                    node.operation = "MULTIPLY"
                    node.inputs[1].default_value = self.brick_bump
                    node.label = "Bump Amount"
                    node.label = "Bump Amount"
                    links = [["uv_coords", 3, "b_scale", 0], ["b_scale", 0, "b_noise", 0], ["b_scale", 0, "b_noise2", 0], ["b_noise", 1, "bn|bn2", 1], ["b_noise2", 1, "bn|bn2", 2], ["bn|bn2", 0, "b_amount", 0], ["b_amount", 0, "Material Output", 2]]
                    for i in links:
                        o = nodes[i[0]].outputs[i[1]]
                        i = nodes[i[2]].inputs[i[3]]
                        mat.node_tree.links.new(o, i)
            elif self.bump_type == "2":  # ridges
                try:  # update
                    nodes["b_scale"].scale = (self.bump_scale, self.bump_scale, self.bump_scale)
                    nodes["b_amount"].inputs[1].default_value = self.brick_bump
                except:  # create
                    nodes = mat.node_tree.nodes
                    node = nodes.new("ShaderNodeMapping")
                    node.name = "b_scale"
                    node.location = -800, -100
                    node.rotation = (radians(-45.0), 0.0, 0.0)
                    node.scale = (self.bump_scale, self.bump_scale, self.bump_scale)
                    node.label = "Bump Scale"
                    node = nodes.new("ShaderNodeTexWave")
                    node.name = "b_wave"
                    node.location = -400, 0
                    node.inputs[1].default_value = 100.0
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "b_noise"
                    node.location = -400, -200
                    node.inputs[1].default_value = 400.0
                    node.inputs[3].default_value = 1.0
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "bw|bn"
                    node.location = -200, -100
                    node.blend_type = "ADD"
                    node.inputs[0].default_value = 1.0
                    node = nodes.new("ShaderNodeMath")
                    node.name = "b_amount"
                    node.location = 100, 0
                    node.operation = "MULTIPLY"
                    node.inputs[1].default_value = self.brick_bump
                    node.label = "Bump Amount"
                    links = [["uv_coords", 2, "b_scale", 0], ["b_scale", 0, "b_noise", 0], ["b_scale", 0, "b_wave", 0], ["b_noise", 1, "bw|bn", 2], ["b_wave", 1, "bw|bn", 1], ["bw|bn", 0, "b_amount", 0], ["b_amount", 0, "Material Output", 2]]
                    for i in links:
                        o = nodes[i[0]].outputs[i[1]]
                        i = nodes[i[2]].inputs[i[3]]
                        mat.node_tree.links.new(o, i)
            elif self.bump_type == "3":  # flaky
                try:  # update
                    nodes["b_scale"].scale = (self.bump_scale, self.bump_scale, self.bump_scale)
                    nodes["b_scale2"].scale = (self.bump_scale, self.bump_scale, self.bump_scale)
                    nodes["b_amount"].inputs[1].default_value = self.brick_bump
                except:
                    node = nodes.new("ShaderNodeMapping")
                    node.name = "b_scale"
                    node.location = -1500, -700
                    node.scale = (self.bump_scale, self.bump_scale, self.bump_scale)
                    node.label = "Bump Scale"
                    node = nodes.new("ShaderNodeMapping")
                    node.name = "b_scale2"
                    node.location = -1500, -400
                    node.rotation = (radians(-45.0), 0.0, 0.0)
                    node.scale = (self.bump_scale, self.bump_scale, self.bump_scale)
                    node.label = "Bump Scale 2"
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "b_noise"
                    node.location = -1400, -200
                    node.inputs[1].default_value = 40.0
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "bc"
                    node.location = -1200, -250
                    node.inputs[2].default_value = 15.0
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "b_noise2"
                    node.location = -1200, -50
                    node.inputs[1].default_value = 12.0
                    node.inputs[3].default_value = 1.0
                    node = nodes.new("ShaderNodeTexWave")
                    node.name = "wave"
                    node.location = -1150, -500
                    node.inputs[1].default_value = 30.0
                    node.inputs[2].default_value = 4.0
                    node = nodes.new("ShaderNodeBrightContrast")
                    node.name = "bc2"
                    node.location = -1000, -200
                    node.inputs[2].default_value = 15.0
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "w|bc"
                    node.location = -950, -425
                    node.inputs[1].default_value = (0.2, 0.2, 0.2, 1.0)
                    node = nodes.new("ShaderNodeTexMusgrave")
                    node.name = "musgrave"
                    node.location = -900, -600
                    node.inputs[1].default_value = 300.0
                    node = nodes.new("ShaderNodeTexNoise")
                    node.name = "b_noise3"
                    node.location = -800, -900
                    node.inputs[1].default_value = 1500.0
                    node.inputs[3].default_value = 0.25
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "bc2|m1"
                    node.location = -750, -300
                    node.inputs[1].default_value = (0.2, 0.2, 0.2, 1.0)
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "m2|mus"
                    node.location = -700, -500
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "m2|m3"
                    node.location = -500, -400
                    node.inputs[1].default_value = (0.2, 0.2, 0.2, 1.0)
                    node = nodes.new("ShaderNodeMath")
                    node.name = "math"
                    node.location = -500, -800
                    node.operation = "MULTIPLY"
                    node.inputs[1].default_value = 0.1
                    node = nodes.new("ShaderNodeInvert")
                    node.name = "invert"
                    node.location = -350, -600
                    node = nodes.new("ShaderNodeMixRGB")
                    node.name = "m3|math"
                    node.location = -150, -550
                    node = nodes.new("ShaderNodeMath")
                    node.name = "b_amount"
                    node.location = 100, -200
                    node.operation = "MULTIPLY"
                    node.inputs[1].default_value = self.brick_bump
                    node.label = "Bump Amount"
                    links = [["uv_coords", 2, "b_scale", 0], ["uv_coords", 2, "b_scale2", 0], ["b_scale", 0, "b_noise", 0], ["b_scale", 0, "b_noise2", 0], ["b_scale", 0, "musgrave", 0], ["b_scale2", 0, "wave", 0], ["b_noise", 1, "bc", 0],
                             ["b_noise2", 1, "bc2", 0], ["bc", 0, "w|bc", 0], ["wave", 1, "w|bc", 2], ["bc2", 0, "bc2|m1", 0], ["w|bc", 0, "bc2|m1", 2], ["musgrave", 1, "m2|mus", 2], ["b_noise3", 1, "math", 1], ["bc2|m1", 0, "m2|mus", 0],
                             ["m2|mus", 0, "m2|m3", 2], ["bc2|m1", 0, "m2|m3", 0], ["m2|m3", 0, "invert", 1], ["m2|m3", 0, "m3|math", 1], ["invert", 0, "m3|math", 0], ["math", 0, "m3|math", 2], ["m3|math", 0, "b_amount", 0], ["b_amount", 0, "Material Output", 2]]
                    for i in links:
                        o = nodes[i[0]].outputs[i[1]]
                        i = nodes[i[2]].inputs[i[3]]
                        mat.node_tree.links.new(o, i)
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if self.is_preview == True:
                            space.viewport_shade = 'RENDERED'
                        else:
                            space.viewport_shade = "SOLID"
        # update rotation and location
        ob.location = ob.location + self.location
        eur = (ob.rotation_euler).copy()
        tup = tuple(self.rotation)
        eur.rotate_axis("X", tup[0])
        eur.rotate_axis("Y", tup[1])
        eur.rotate_axis("Z", tup[2])
        ob.rotation_euler = eur
        return {"FINISHED"}


def panel_func(self, context):
    self.layout.operator("mesh.primitive_add_siding", text="Siding", icon="UV_ISLANDSEL")

# Register


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(panel_func)
    try:
        bpy.types.MESH_PT_addons.append(panel_func)
    except:
        pass


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(panel_func)
    try:
        bpy.types.MESH_PT_addons.remove(panel_func)
    except:
        pass
if __name__ == "__main__":
    register()
