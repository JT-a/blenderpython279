#
# Copyright 2012 Alain PORET
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


bl_info = {
    'name': 'Mesh propeller',
    'author': 'Alain Poret',
    'version': (0, 1),
    "blender": (2, 6, 4),
    "api": 37702,
    'location': 'View3D > Add > Mesh',
    'description': 'Create a boat propeller or a air-screw',
    'warning': '',  # used for warning icon and text in addons panel
    'category': 'Add Mesh'}


import bpy
from bpy.props import FloatVectorProperty, IntProperty,\
    FloatProperty, BoolProperty
#from add_utils import AddObjectHelper, add_object_data
from bpy_extras.object_utils import AddObjectHelper, object_data_add
#from bpy_extras.object_utils import AddObjectHelper
from mathutils import Vector
from math import *


class Heli(object):
    "définition d'une helice"

    def __init__(self, params):

        self.pal = params[0]  # nb_blades     nb de pales
        self.nbr = params[1]  # thi_mesh      finesse maillage
        self.kar = params[2]  # coef_ba       sans dim
        self.kav = params[3]  # coef_bf       sans dim
        self.dev = params[4]  # devers        devers rd/m  0.5
        self.std = params[5]  # step          pas/diam sans dim
        self.gfm = params[6]  # hub_contour   galbe moyeu sans dimension
        self.lar = params[7]  # blade_width   angle d'amplitude de pale degres
        self.inc = params[8]  # incidence     incidence nomimale en degres
        self.dec = params[9]  # angulae_lag   decalage origine angulaire
        self.rat = params[10]  # blade_radius rayon en bout de la pale
        self.dif = params[11]  # cut_rad      r theorique - r reel metres
        self.rap = params[12]  # bl_root_rad  rayon moyeu en pied de pale metre
        self.ral = params[13]  # boring_rad   rayon alesage metres
        self.thi = params[14]  # blade_thick  epaisseur de pale  meters
        self.rac = params[15]  # round_root   rayon du conge de pied de pale
        self.dep = params[16]  # extra_hub    0.05 depassement du moyeu

        self.lar = self.lar * pi / 180  # degres to radians
        self.inc = self.inc * pi / 180  # degres to radians
        self.dec = self.dec * pi / 180  # degres to radians

        self.stp = self.std * (self.rat - self.dif) / pi

        x = 0.0
        rmax = 0.0
        xmax = 0.0
        rgood = 10.0
        dx = 0.2
        while fabs(rmax - rgood) > 1e-10:
            dx = dx * 0.1
            rgood = rmax
            rmax = 0.0
            x = xmax
            while x < self.lar:
                r = ((self.kar * x) / (1.0 + self.kar * x))\
                    * (self.kav * (self.lar - x) /
                       (1.0 + self.kav * (self.lar - x)))
                if r >= rmax:
                    rmax = r
                    xmax = x - dx
                else:
                    break

                x = x + dx

        self.rca = self.rat / rgood


def resoudre(a, b, c):
    delta = b * b - 4.0 * a * c
    if delta < 0:
        return (0, 0.0, 0.0)
    delta = sqrt(delta)
    s1 = (-b - delta) / (a + a)
    s2 = (-b + delta) / (a + a)
    return (2, s1, s2)


def limites(hel, r):
    r = r / hel.rca
    a = r * hel.kar * hel.kav - hel.kar * hel.kav
    b = hel.kar * hel.kav * hel.lar + r * hel.kav -\
        r * hel.kar - r * hel.kav * hel.kar * hel.lar
    c = -r - r * hel.kav * hel.lar
    sols = resoudre(a, b, c)
    return (sols[0], sols[1] - hel.lar * 0.5, sols[2] - hel.lar * 0.5)


def profil(xa):
    return sqrt(xa * (xa - 1) * (xa - 1) * 27.0 / 4.0)


def calvn(pas, alfa, ray, vn):
    vr = Vector((cos(alfa), sin(alfa), 0.0))
    vt = Vector((-ray * sin(alfa), ray * cos(alfa), pas))
    vn = vr.cross(vt)
    vn.normalize()
    return vn


def addpoint(hel, vert_list, na, j, alfa1, alfa2, epe, ray, max, min, i):
    xa = j * 1.0 / na
    xa = xa * xa
    alfa = alfa2 + xa * (alfa1 - alfa2) + ray * hel.dev / hel.rat
    epais = epe * profil(xa)
    vn = Vector()
    vn = calvn(hel.stp, alfa, ray, vn)
    x = ray * cos(alfa) + vn.x * epais
    y = ray * sin(alfa) + vn.y * epais
    z = ray * (alfa - hel.dec) * tan(hel.inc + atan(hel.stp / ray))\
        + vn.z * epais
    vert_list.extend((Vector((x, y, z)),))
    nbpoints = len(vert_list) - 1
    if i == 0:
        if vert_list[nbpoints][2] > max:
            max = vert_list[nbpoints][2]
        if vert_list[nbpoints][2] < min:
            min = vert_list[nbpoints][2]
    return (vert_list, min, max)


def radius(z, centre, rmax, demilong, galbe):
    demilong = demilong * galbe * 0.5
    return rmax * sqrt(1 - (z - centre) * (z - centre) / (demilong * demilong))


def slide_tp(tp, kx, ky):
    return(tp[0] * kx, tp[1] * ky, tp[2])


def turn_tp(tp, si, co):
    x = tp[0]
    y = tp[1]
    z = tp[2]
    return Vector((x * co - y * si, x * si + y * co, z))


def boucle(max, i):
    if i == max:
        return 0
    return i


def makePropeller(params):

    hel = Heli(params)
    na = hel.nbr
    ndt = int(hel.nbr / 5)

    if ndt < 5:
        ndt = 5

    zpmax = -1e40
    zpmin = 1e40

    face_list = []
    vert_list = []

    # maillage d'une pale
    # definition des vertices
    i = 0
    while i <= hel.nbr:

        kr = 1.0 * i / (1.0 * hel.nbr)
        kr = kr * (2 - kr)
        ray = hel.rap + kr * (hel.rat - hel.rap - hel.dif)
        epe = hel.thi * sqrt(1 - pow(ray / hel.rat, 2.0))
        r = limites(hel, ray)
        if r[0] == 2:
            alfa1 = r[1]
            alfa2 = r[2]
            j = na
            while j > 0:
                r = addpoint(hel, vert_list, na, j, alfa1, alfa2,
                             - epe, ray, zpmax, zpmin, i)
                vert_list = r[0]
                zpmin = r[1]
                zpmax = r[2]
                j = j - 1

            j = 0
            while j <= na:
                r = addpoint(hel, vert_list, na, j, alfa1, alfa2,
                             epe, ray, zpmax, zpmin, i)
                vert_list = r[0]
                zpmin = r[1]
                zpmax = r[2]
                j = j + 1

        i = i + 1
    zpmax = (zpmax + hel.rac + hel.dep) * 1.1
    zpmin = (zpmin - hel.rac - hel.dep) * 1.1
    # fin definition des vertices

    # definition des faces
    i = 0
    while i < na:
        j = 0
        while j < hel.nbr:

            p1 = i + (j + 1) * (2 * na + 1)
            p2 = i + 1 + (j + 1) * (2 * na + 1)
            p3 = i + 1 + j * (2 * na + 1)
            p4 = i + j * (2 * na + 1)
            face_list.extend(((p1, p2, p3, p4),))

            j = j + 1
        i = i + 1

    i = na
    while i < 2 * na:
        j = 0
        while j < hel.nbr:

            p1 = i + (j + 1) * (2 * na + 1)
            p2 = i + 1 + (j + 1) * (2 * na + 1)
            p3 = i + 1 + j * (2 * na + 1)
            p4 = i + j * (2 * na + 1)
            face_list.extend(((p1, p2, p3, p4),))

            j = j + 1
        i = i + 1

   # debut ectremite de palle
   # triangle bord attaque
    hnbr = (hel.nbr) * (2 * na + 1)
   # on ajoute les point du bout a la liste des points
    nbext = len(vert_list)
    i = 0
    while i < 2 * na:
        vert_list.extend((vert_list[i + hnbr],))
        i = i + 1

    p1 = na + nbext
    p2 = na - 1 + nbext
    p3 = p2
    p4 = na + 1 + nbext

    face_list.extend(((p1, p2, p3, p4),))

  # triangle  bord de fuite
    p1 = 1 + nbext
    p2 = nbext
    p3 = p2
    p4 = 2 * na - 1 + nbext

    face_list.extend(((p1, p2, p3, p4),))

    i = 1
    while i < na - 1:

        p1 = 2 * na - i + nbext
        p2 = 2 * na - i - 1 + nbext
        p3 = i + 1 + nbext
        p4 = i + nbext

        face_list.extend(((p1, p2, p3, p4),))

        i = i + 1
  # fin extremite de pale
  # findefinition des faces
  # fin maillage d'une pale

  # maillage conge
  # definition vertices

    nbdf = int(na / 5)
    if nbdf < 5:
        nbdf = 5
    orig = len(vert_list)
    zmin = 1e40
    zmax = -1e40
    arot = 0.0

    i = 0
    while i <= 2 * na + nbdf:  # B1

        if i <= 2 * na:
            vtang = vert_list[i] - vert_list[i + 2 * na + 1]

            if i < 2 * na:
                vcote = vert_list[i] - vert_list[i + 1]
            else:
                vcote = vert_list[i - 1] - vert_list[i]
            vcote.normalize()
            vnorm = vcote.cross(vtang)
            vtang.normalize()
            vnorm.normalize()
            if i == 0:
                vnorm0 = vnorm.copy()
            if i == 2 * na:
                vnorm1 = vnorm.copy()
            center = vert_list[i] + vnorm * (-hel.rac)
            bout = vert_list[i]

        else:
            vtang = vnorm1.cross(vnorm0)
            arot = (i - 2 * na) * ((pi - asin(vtang.length)) / (nbdf * 1.0))
            vtang.normalize()
            vnorm = vnorm1 * cos(arot) + vtang.cross(vnorm1) * sin(arot)
            center = bout + vnorm * (-hel.rac)

        j = 0
        while j < ndt:  # B2
            beta = j * (pi / 2) / ndt

            vtem3 = vnorm.copy() * (hel.rac * sin(beta)) + vtang.copy()\
                * hel.rac * cos(beta)

            vert_list.extend(((center + vtem3),))
            nbpoints = len(vert_list) - 1

            if j == 0:
                xx = vert_list[nbpoints][0]
                yy = vert_list[nbpoints][1]
                zz = vert_list[nbpoints][2]
                correction = sqrt(xx * xx + yy * yy)\
                    / radius(zz, 0.5 * (zpmin + zpmax),
                             (hel.rap - hel.rac), zpmin - zpmax, hel.gfm)
                correction = 1 / correction

            k = correction + j * (1 - correction) / (ndt - 1)
            vert_list[nbpoints] = slide_tp(vert_list[nbpoints], k, k)

            if(vert_list[nbpoints][2] < zmin):
                zmin = vert_list[nbpoints][2]
            if(vert_list[nbpoints][2] > zmax):
                zmax = vert_list[nbpoints][2]

            j = j + 1  # B2

        i = i + 1  # B1

  # fin definition vertices
  # definition des faces
    j = 0
    while j < 2 * na:
        p4 = j + 1
        p3 = j
        p2 = orig + j + (ndt - 1) * (j + 1)
        p1 = orig + j + 1 + (ndt - 1) * (j + 2)
        face_list.extend(((p1, p2, p3, p4),))
        j = j + 1

    j = 2 * na
    while j < nbdf + 2 * na:

        p1 = orig + j + (ndt - 1) * (j + 1)
        p2 = 0
        p3 = 0
        p4 = orig + j + 1 + (ndt - 1) * (j + 2)
        face_list.extend(((p1, p2, p3, p4),))
        j = j + 1

    i = 0
    while i < ndt - 1:
        j = 0
        while j < 2 * na + nbdf:

            p1 = orig + i + 1 + (j + 1) * (ndt)
            p2 = orig + i + (j + 1) * (ndt)
            p3 = orig + i + j * (ndt)
            p4 = orig + i + 1 + j * (ndt)

            face_list.extend(((p1, p2, p3, p4),))
            j = j + 1

        i = i + 1

  # fin definition des faces congé
  # fin maillage conge

  # copie des pales
    npnts = len(vert_list)
    ntri = len(face_list)

    pale = 1
    while pale < hel.pal:
        ag = pale * (2 * pi) / (1.0 * hel.pal)
        si = sin(ag)
        co = cos(ag)

        i = 0
        while i < npnts:

            vert_list.extend((turn_tp(vert_list[i], si, co),))
            i = i + 1

        i = 0
        while i < ntri:
            p1 = face_list[i][0] + npnts * pale
            p2 = face_list[i][1] + npnts * pale
            p3 = face_list[i][2] + npnts * pale
            p4 = face_list[i][3] + npnts * pale

            face_list.extend(((p1, p2, p3, p4),))
            i = i + 1

        pale = pale + 1

# fin copie des pales

# moyeu
# vertices moyeu
    zmin = zmin - hel.dep
    zmax = zmax + hel.dep
    nbc = hel.nbr
    nbg = hel.nbr * 2
    npnts = len(vert_list)

    rgex1m = npnts
    i = 0
    while i <= nbc:
        zz = zmin + (zmax - zmin) * i / nbc
        ray = radius(zz, 0.5 * (zpmin + zpmax), (hel.rap - hel.rac),
                     zpmin - zpmax, hel.gfm)

        j = 0
        while j < nbg:
            alfa = j * 2 * pi / nbg
            x = ray * sin(alfa)
            y = ray * cos(alfa)
            z = zz
            vert_list.extend((Vector((x, y, z)),))
            j = j + 1

        i = i + 1
    rgex2m = len(vert_list) - nbg
  # fin vertices moyeu

  # faces moyeu
    i = 0
    while i < nbc:

        j = 0
        while j < nbg:
            p1 = npnts + i * nbg + (boucle(nbg, j))
            p2 = npnts + (i + 1) * nbg + (boucle(nbg, j))
            p3 = npnts + (i + 1) * nbg + (boucle(nbg, j + 1))
            p4 = npnts + i * nbg + (boucle(nbg, j + 1))
            face_list.extend(((p1, p2, p3, p4),))
            j = j + 1

        i = i + 1

  # fin faces moyeu
  # fin moyeu

  # alesage
  # vertex alesage
    ray = hel.ral
    npnts = len(vert_list)
    rgex1a = npnts

    i = 0
    while i <= nbc:
        zz = zmin + (zmax - zmin) * i / nbc

        j = 0
        while j < nbg:
            alfa = j * 2 * pi / nbg
            x = ray * sin(alfa)
            y = ray * cos(alfa)
            z = zz
            vert_list.extend((Vector((x, y, z)),))
            j = j + 1

        i = i + 1

    rgex2a = len(vert_list) - nbg
  # fin vertex alesage

  # faces alesage
    i = 0
    while i < nbc:
        j = 0
        while j < nbg:

            p1 = npnts + i * (nbg) + (boucle(nbg, j + 1))
            p2 = npnts + (i + 1) * (nbg) + (boucle(nbg, j + 1))
            p3 = npnts + (i + 1) * (nbg) + (boucle(nbg, j))
            p4 = npnts + i * (nbg) + (boucle(nbg, j))
            face_list.extend(((p1, p2, p3, p4),))
            j = j + 1

        i = i + 1

  # fin faces alesage

  # fin alesage

  # extremite 1
    rgex1a_r = len(vert_list)
    j = 0
    while j < nbg:
        vert_list.extend((vert_list[rgex1a + j],))
        j = j + 1

    rgex1m_r = len(vert_list)
    j = 0
    while j < nbg:
        vert_list.extend((vert_list[rgex1m + j],))
        j = j + 1

    j = 0
    while j < nbg:

        p1 = rgex1a_r + boucle(nbg, j)
        p2 = rgex1m_r + boucle(nbg, j)
        p3 = rgex1m_r + boucle(nbg, 1 + j)
        p4 = rgex1a_r + boucle(nbg, 1 + j)
        face_list.extend(((p1, p2, p3, p4),))
        j = j + 1

  # fin extremite 1

  # extremite 2
    rgex2a_r = len(vert_list)
    j = 0
    while j < nbg:
        vert_list.extend((vert_list[rgex2a + j],))
        j = j + 1

    rgex2m_r = len(vert_list)
    j = 0
    while j < nbg:
        vert_list.extend((vert_list[rgex2m + j],))
        j = j + 1

    j = 0
    while j < nbg:

        p4 = rgex2a_r + boucle(nbg, j)
        p3 = rgex2m_r + boucle(nbg, j)
        p2 = rgex2m_r + boucle(nbg, 1 + j)
        p1 = rgex2a_r + boucle(nbg, 1 + j)
        face_list.extend(((p1, p2, p3, p4),))
        j = j + 1

  # fin extremite 2
    return vert_list, face_list


def add_propeller_object(self, context):

    params = [self.nb_blades, self.thi_mesh, self.coef_ba, self.coef_bf,
              self.devers, self.step, self.hub_contour, self.blade_width,
              self.incidence, self.angulae_lag, self.blade_radius, self.cut_rad,
              self.bl_root_rad, self.boring_rad, self.blade_thick,
              self.round_root, self.extra_hub]
    verts, faces = makePropeller(params)
    mesh_data = bpy.data.meshes.new(name="Propeller")
    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()
    res = object_data_add(context, mesh_data, operator=self)


class OBJECT_OT_add_propeller(bpy.types.Operator, AddObjectHelper):
    """Add a Mesh Object"""
    bl_idname = "mesh.propeller_add"
    bl_label = "Propeller"
    bl_description = "Create a mesh of boat propeller "
    bl_options = {'REGISTER', 'UNDO'}

    scale = 1.0

    nb_blades = IntProperty(name="Number of blades", default=4,
                            min=1, max=100,
                            description="Number of blades")

    thi_mesh = IntProperty(name="Refinement of the mesh", default=30,
                           min=2, max=200,
                           description="Give greater finer")

    coef_ba = FloatProperty(name="Aspect ratio 1", default=6.0,
                            min=1.0, max=10000.0,
                            description="Aspect ratio")

    coef_bf = FloatProperty(name="Aspect ratio 2", default=200.0,
                            min=1.0, max=10000.0,
                            description="Aspect ratio")

    devers = FloatProperty(name="Devers", default=0.5,
                           min=-10.0, max=10.0,
                           description="Devers of the blade")

    step = FloatProperty(name="Pitch", default=0.3,
                         min=-10.0, max=10.0,
                         description="Propeller pitch")

    hub_contour = FloatProperty(name="Contour", default=1.8,
                                min=1.0, max=1000.0,
                                description="Shapely of hub")

    blade_width = FloatProperty(name="Width", default=90.0,
                                min=1.0, max=1000.0,
                                description="Width of the blade in degrees")

    incidence = FloatProperty(name="Incidence", default=15.0,
                              min=-20.0, max=20.0,
                              description="Angle of incidence in degrees")

    angulae_lag = FloatProperty(name="Lag", default=30.0,
                                min=-1000.0, max=1000.0,
                                description="Lag compensator in degrees")

    blade_radius = FloatProperty(name="Blade radius", default=1.0 * scale,
                                 min=0.0, max=1000.0,
                                 description="Length of a full blade")

    cut_rad = FloatProperty(name="End Cut", default=0.002 * scale,
                            min=0.0, max=1000.0,
                            description="Very small for a full blade")

    bl_root_rad = FloatProperty(name="Hub radius", default=0.3 * scale,
                                min=0.0, max=1000.0,
                                description="Determine the hub radius")

    boring_rad = FloatProperty(name="Boring radius", default=0.17 * scale,
                               min=0.0, max=1000.0,
                               description="Half the diameter of the boring")

    blade_thick = FloatProperty(name="Blade thickness",
                                default=0.05 * scale,
                                min=0.0, max=1000.0,
                                description="Determine the blade thickness")

    round_root = FloatProperty(name="Rounding", default=0.04 * scale,
                               min=0.0, max=1000.0,
                               description="Radius of the rounding of the blade root")

    extra_hub = FloatProperty(name="Overtaking", default=0.05 * scale,
                              min=0.0, max=1000.0,
                              description="Increase the length of the hub")

    def execute(self, context):
        add_propeller_object(self, context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_add_propeller.bl_idname,
                         text="Propeller", icon="PLUGIN")


def register():
    bpy.utils.register_class(OBJECT_OT_add_propeller)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_propeller)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
