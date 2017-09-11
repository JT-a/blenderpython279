'''
    Copyright (C) 2011-2012 Brad Corso

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
    to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of
    the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
    OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import bpy
bl_info = {
    "name": "Create Graphene/CNT",
    "author": "Brad Corso, bcorso1@gmail.com",
    "version": (2, 3, 0),
    "blender": (2, 6, 1),
    "api": 41287,
    "location": "View3D > Spacebar Key > Create CNT",
    "description": "Creates Graphene and CNTs of any index (m,n).",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}


def CNT(type=1, res=1, m=10, n=5, bL=1.56, bR=.1, aR=.2):
    import bpy
    from fractions import gcd
    from math import cos, sin, acos, sqrt, copysign, ceil, floor, pi
    from mathutils import Vector, Matrix, Quaternion
    print("Tube: (", m, ",", n, "); Radius: ", bL * sqrt(m * m + n * n + m * n) / (2 * pi))

    cntR = bL * sqrt(m * m + n * n + m * n) / (2 * pi)
    a1 = Vector((bL * sqrt(3) / 2, bL / 2))
    a2 = Vector((bL * sqrt(3) / 2, -bL / 2))
    x = Vector((bL / sqrt(3), 0))

    def Lattice2D(i, j, k):
        return i * a1 + j * a2 + k * x

    o = Lattice2D(0, 0, 0)
    c = Lattice2D(m, n, 0)
    d = gcd(2 * n + m, 2 * m + n)
    t = Lattice2D((2 * n + m) / d, -(2 * m + n) / d, 0)
    print("Unit Length: ", t.magnitude)
    theta = acos(c.normalized()[0] * copysign(1, c[1]))
    u = Matrix(((cos(theta), sin(theta)), (-sin(theta), cos(theta))))

    def Lattice3D(i, j, k):
        r = c.magnitude / (2 * pi)
        p = Lattice2D(i, j, k) * u.transposed()
        return Vector([r * cos(p[0] / r), r * sin(p[0] / r), p[1]])

    imax = 2 * (n + m)
    imin = 0
    jmax = n
    jmin = -(2 * m + n)
    indices = []
    for i in range(imin, imax + 1):
        for j in range(jmin, jmax + 1):
            for k in range(2):
                p = Lattice2D(i, j, k) * u.transposed()
                if p[0] >= 0 - bL / 5 and p[0] <= c.magnitude - bL / 5 and p[1] >= 0 + bL / 10 and p[1] <= t.magnitude + bL / 10:
                    indices.append([i, j, k])
    print("indices: ", len(indices))

    points2D = list(map(lambda x: Lattice2D(x[0], x[1], x[2]) * u.transposed(), indices))
    print("points2D: ", len(points2D))

    bonds2D = []
    for i in range(len(indices)):
        if indices[i][2] == 0:
            p1 = Lattice2D(indices[i][0], indices[i][1], 0) * u.transposed()
            p2 = Lattice2D(indices[i][0], indices[i][1], 1) * u.transposed()
            if p2[0] >= 0 - bL / 5 and p2[0] <= c.magnitude + bL / 5 and p2[1] >= 0 - bL / 10 and p2[1] <= t.magnitude + bL:
                bonds2D.append([p1, p2])
            p2 = Lattice2D(indices[i][0] - 1, indices[i][1], 1) * u.transposed()
            if p2[0] >= 0 - bL / 5 and p2[0] <= c.magnitude + bL / 5 and p2[1] >= 0 - bL / 10 and p2[1] <= t.magnitude + bL:
                bonds2D.append([p1, p2])
            p2 = Lattice2D(indices[i][0], indices[i][1] - 1, 1) * u.transposed()
            if p2[0] >= 0 - bL / 5 and p2[0] <= c.magnitude + bL / 5 and p2[1] >= 0 - bL / 10 and p2[1] <= t.magnitude + bL:
                bonds2D.append([p1, p2])
    print("bonds2D: ", len(bonds2D))

    if type == 0:
        lyrs = [False] * 20
        lyrs[3] = True
        if bpy.data.scenes[0].layers[3] == False:
            bpy.data.scenes[0].layers[3] = True
        bpy.ops.object.select_by_layer(extend=False, layers=4)
        bpy.ops.object.delete()

        if res < 0:
            res = 1

        if bR > 0:
            for i in range(len(bonds2D)):
                temp3D1 = Vector([bonds2D[i][0][0], bonds2D[i][0][1], 0])
                temp3D2 = Vector([bonds2D[i][1][0], bonds2D[i][1][1], 0])
                p = (temp3D1 + temp3D2) * .5
                v = ((temp3D2 - temp3D1).normalized() + Vector((0, 0, 1))) / 2
                qu = Quaternion((v[0], v[1], v[2]), pi)
                eu = qu.to_euler()
                bpy.ops.mesh.primitive_cylinder_add(vertices=res * 4, depth=(temp3D2 - temp3D1).magnitude * 1.05, radius=bR, end_fill_type='NOTHING', location=(p[0], p[1], p[2]), rotation=eu, layers=lyrs)
                if res > 1:
                    bpy.ops.object.shade_smooth()
            print("C bonds rendered")

        if aR > 0:
            for i in range(len(points2D)):
                bpy.ops.mesh.primitive_uv_sphere_add(segments=res * 4, ring_count=res * 2, size=aR, location=(points2D[i][0], points2D[i][1], 0), layers=lyrs)
                if res > 1:
                    bpy.ops.object.shade_smooth()
            print("C atoms rendered")
        bpy.ops.mesh.primitive_uv_sphere_add(size=0, layers=lyrs)

        bpy.ops.object.select_by_layer(extend=False, layers=4)
        bpy.ops.object.join()

        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.active_object.modifiers['Array'].count = 1
        bpy.context.active_object.modifiers['Array'].use_relative_offset = False
        bpy.context.active_object.modifiers['Array'].use_constant_offset = True
        bpy.context.active_object.modifiers['Array'].constant_offset_displace.y = t.magnitude

        # bpy.ops.curve.primitive_bezier_circle_add(rotation=(0, pi/2, 0), layers=lyrs)
        # need to select cnt now.
        # bpy.ops.object.modifier_add(type='CURVE')

    else:
        points3D = list(map(lambda x: Lattice3D(x[0], x[1], x[2]), indices))
        print("points3D: ", len(points3D))

        bonds3D = []
        for i in range(len(indices)):
            if indices[i][2] == 0:
                p13D = Lattice3D(indices[i][0], indices[i][1], 0)
                p23D = Lattice3D(indices[i][0], indices[i][1], 1)
                p2 = Lattice2D(indices[i][0], indices[i][1], 1) * u.transposed()
                if p2[0] >= 0 - bL and p2[0] <= c.magnitude + bL and p2[1] >= 0 - bL and p2[1] <= t.magnitude + bL:
                    bonds3D.append([p13D, p23D])
                p23D = Lattice3D(indices[i][0] - 1, indices[i][1], 1)
                p2 = Lattice2D(indices[i][0] - 1, indices[i][1], 1) * u.transposed()
                if p2[0] >= 0 - bL and p2[0] <= c.magnitude + bL and p2[1] >= 0 - bL and p2[1] <= t.magnitude + bL:
                    bonds3D.append([p13D, p23D])
                p23D = Lattice3D(indices[i][0], indices[i][1] - 1, 1)
                p2 = Lattice2D(indices[i][0], indices[i][1] - 1, 1) * u.transposed()
                if p2[0] >= 0 - bL and p2[0] <= c.magnitude + bL and p2[1] >= 0 - bL and p2[1] <= t.magnitude + bL:
                    bonds3D.append([p13D, p23D])
        print("bonds3D: ", len(bonds3D))

        lyrs = [False] * 20
        lyrs[1] = True
        if bpy.data.scenes[0].layers[1] == False:
            bpy.data.scenes[0].layers[1] = True
        bpy.ops.object.select_by_layer(extend=False, layers=2)
        bpy.ops.object.delete()

        if res < 0:
            res = 1

        if bR > 0:
            for i in range(len(bonds3D)):
                p = (bonds3D[i][0] + bonds3D[i][1]) * .5
                v = ((bonds3D[i][1] - bonds3D[i][0]).normalized() + Vector((0, 0, 1))) / 2
                qu = Quaternion((v[0], v[1], v[2]), pi)
                eu = qu.to_euler()
                bpy.ops.mesh.primitive_cylinder_add(vertices=res * 4, depth=(bonds3D[i][1] - bonds3D[i][0]).magnitude * 1.05, radius=bR, end_fill_type='NOTHING', location=(p[0], p[1], p[2]), rotation=eu, layers=lyrs)
                if res > 1:
                    bpy.ops.object.shade_smooth()
            print("C bonds rendered")
            bpy.ops.mesh.primitive_uv_sphere_add(size=0, layers=lyrs)

            bpy.ops.object.select_by_layer(extend=False, layers=2)
            bpy.ops.object.join()
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].count = 1
            bpy.context.active_object.modifiers['Array'].use_relative_offset = False
            bpy.context.active_object.modifiers['Array'].use_constant_offset = True
            bpy.context.active_object.modifiers['Array'].constant_offset_displace.z = t.magnitude
            bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0))

        lyrs = [False] * 20
        lyrs[2] = True
        if bpy.data.scenes[0].layers[2] == False:
            bpy.data.scenes[0].layers[2] = True
        bpy.ops.object.select_by_layer(extend=False, layers=3)
        bpy.ops.object.delete()

        if aR > 0:
            for i in range(len(points3D)):
                bpy.ops.mesh.primitive_uv_sphere_add(segments=res * 4, ring_count=res * 2, size=aR, location=(points3D[i][0], points3D[i][1], points3D[i][2]), layers=lyrs)
                if res > 1:
                    bpy.ops.object.shade_smooth()
            print("C atoms rendered")
            bpy.ops.mesh.primitive_uv_sphere_add(size=0, layers=lyrs)

            bpy.ops.object.select_by_layer(extend=False, layers=3)
            bpy.ops.object.join()
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].count = 1
            bpy.context.active_object.modifiers['Array'].use_relative_offset = False
            bpy.context.active_object.modifiers['Array'].use_constant_offset = True
            bpy.context.active_object.modifiers['Array'].constant_offset_displace.z = t.magnitude
            bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0))


class CNTDialog(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Create CNT"

    gtype = bpy.props.BoolProperty(name="Type:CNT(1)/Graphene(0):", default=True)
    res = bpy.props.IntProperty(name="Resolution", default=1)
    index_m = bpy.props.IntProperty(name="m", default=5)
    index_n = bpy.props.IntProperty(name="n", default=5)
    bL = bpy.props.FloatProperty(name="C-C Bond Length", default=.312)
    bR = bpy.props.FloatProperty(name="C-C Bond Radius", default=.01)
    aR = bpy.props.FloatProperty(name="C Atom Radius", default=.04)

    def execute(self, context):
        CNT(type=self.gtype, res=self.res, m=self.index_m, n=self.index_n, bL=self.bL, bR=self.bR, aR=self.aR)
        print(self.index_m)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

# registering and menu integration


def register():
    bpy.utils.register_class(CNTDialog)

# unregistering and removing menus


def unregister():
    bpy.utils.unregister_class(CNTDialog)

if __name__ == "__main__":
    register()

# test call
# bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
