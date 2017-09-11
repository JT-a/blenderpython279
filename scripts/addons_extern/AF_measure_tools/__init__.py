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
# Contributed to by kromar, zmj100, meta-androcto, sambler,
# o #


bl_info = {
    "name": "AF: Measure Tools",
    "author": "Multiple Authors",
    "version": (0, 1),
    "blender": (2, 74, 0),
    "location": "View3D > Properties & Mesh Data",
    "description": "Measure & Display types",
    "warning": "",
    "wiki_url": "",
    "category": "Addon Factory"}

if "bpy" in locals():
    import importlib
    importlib.reload(lint)

else:
    from . import lint


import bpy
import blf
import bgl
import bmesh
from bpy.props import BoolProperty, PointerProperty, FloatProperty, EnumProperty, IntProperty
from bpy_extras.view3d_utils import location_3d_to_region_2d, region_2d_to_location_3d
from mathutils.geometry import intersect_line_plane, area_tri
from mathutils import Vector, Matrix
from math import degrees
from bpy_extras.mesh_utils import ngon_tessellate, edge_face_count
from bgl import glBegin, glPointSize, glColor3f, glVertex3f, glEnd, GL_POINTS

# ------ Mesh Statistics ------
handle = []
do_draw = [False]
com = [(0.0, 0.0, 0.0)]


def arithmeticMean(items):
    """
    Arithmetic mean of the items.
    """
    # sum() doesn't work for lists of Vectors... :-/
    s = items[0].copy()
    for item in items[1:]:
        s += item
    return s / len(items)


def weightedMean(couples):
    """
    Weighted mean of the couples (item, weight).
    """
    # could be made nicer, but this is fast
    items_weighted_sum = couples[0][0] * couples[0][1]
    weights_sum = couples[0][1]
    for item, weight in couples:
        items_weighted_sum += item * weight
        weights_sum += weight

    return items_weighted_sum / weights_sum


def calculateTriangleArea(mesh, vertices, matrix):
    vcs = [matrix * mesh.vertices[i].co for i in vertices]
    return area_tri(*vcs)


def calculateArea(mesh, matrix=None):
    """
    Simply sum up faces areas.
    """
    area = 0.0
    if matrix is None:
        for polygon in mesh.polygons:
            area += polygon.area
    else:
        for polygon in mesh.polygons:
            if len(polygon.vertices) == 3:
                area += calculateTriangleArea(mesh, polygon.vertices, matrix)
            elif len(polygon.vertices) == 4:
                area += calculateTriangleArea(mesh, [polygon.vertices[i] for i in (0, 1, 2)], matrix)
                area += calculateTriangleArea(mesh, [polygon.vertices[i] for i in (0, 2, 3)], matrix)
            else:
                tris = ngon_tessellate(mesh, polygon.vertices)
                for tri in tris:
                    area += calculateTriangleArea(mesh, tri, matrix)

    return area


def calculateTriangleVolume(vertices, reference_point):
    # vertices are already in the right order, thanks to Blender
    vcs = []
    for v in vertices:
        v4 = v.to_4d()
        v4[3] = 1.0
        vcs.append(v4)
    ref4 = reference_point.to_4d()
    ref4[3] = 1.0
    vcs.append(ref4)

    return Matrix(vcs).determinant() / 6.0


def calculateTriangleCOM(vertices, reference_point):
    v = vertices.copy()
    v.append(reference_point)
    return arithmeticMean(v)


def calculatePolygonVolume(mesh, polygon, reference_point):
    if len(polygon.vertices) == 3:
        vcs = [mesh.vertices[polygon.vertices[i]].co for i in (0, 1, 2)]
        return calculateTriangleVolume(vcs, reference_point)

    elif len(polygon.vertices) == 4:
        vcs1 = [mesh.vertices[polygon.vertices[i]].co for i in (0, 1, 2)]
        vcs2 = [mesh.vertices[polygon.vertices[i]].co for i in (0, 2, 3)]
        v1 = calculateTriangleVolume(vcs1, reference_point)
        v2 = calculateTriangleVolume(vcs2, reference_point)
        return v1 + v2

    else:
        volume = 0.0
        tris = ngon_tessellate(mesh, polygon.vertices)
        for tri in tris:
            volume += calculateTriangleVolume(
                [mesh.vertices[i].co for i in tri], reference_point)
        return volume


def calculatePolygonCOM(mesh, polygon, reference_point):
    if len(polygon.vertices) == 3:
        vcs = [mesh.vertices[polygon.vertices[i]].co for i in (0, 1, 2)]
        return calculateTriangleCOM(vcs, reference_point)

    elif len(polygon.vertices) == 4:
        vcs1 = [mesh.vertices[polygon.vertices[i]].co for i in (0, 1, 2)]
        vcs2 = [mesh.vertices[polygon.vertices[i]].co for i in (0, 2, 3)]
        v1 = calculateTriangleVolume(vcs1, reference_point)
        v2 = calculateTriangleVolume(vcs2, reference_point)
        com1 = calculateTriangleCOM(vcs1, reference_point)
        com2 = calculateTriangleCOM(vcs2, reference_point)
        return (com1 * v1 + com2 * v2) / (v1 + v2)

    else:
        couples = []
        tris = ngon_tessellate(mesh, polygon.vertices)
        for tri in tris:
            vs = [mesh.vertices[i].co for i in tri]
            couples.append(
                (calculateTriangleCOM(vs, reference_point),
                 calculateTriangleVolume(vs, reference_point)))
        return weightedMean(couples)


def calculateVolume(mesh, reference_point=Vector((0.0, 0.0, 0.0))):
    """
    Same method as in "Measure Panel" addon.
    See Sheue-ling Lien, James T. Kajiya,
        "A Symbolic Method for Calculating the Integral Properties
         of Arbitrary Nonconvex Polyhedra"
        IEEE October 1984
    """
    volume = 0.0
    for polygon in mesh.polygons:
        volume += calculatePolygonVolume(mesh, polygon, reference_point)

    return volume


def calculateCOM_Volume(mesh, reference_point=Vector((0.0, 0.0, 0.0))):
    couples = []
    for polygon in mesh.polygons:
        v = calculatePolygonVolume(mesh, polygon, reference_point)
        com = calculatePolygonCOM(mesh, polygon, reference_point)
        couples.append((com, v))

    return weightedMean(couples)


def calculateCOM_Faces(mesh):
    couples = []
    for polygon in mesh.polygons:
        couples.append((polygon.center, polygon.area))

    return weightedMean(couples)


def calculateCOM_Edges(mesh):
    couples = []
    for edge in mesh.edges:
        v1, v2 = [mesh.vertices[edge.vertices[i]].co for i in range(2)]
        # not necessary to run arithmeticMean() for 2 vertices...
        couples.append(((v1 + v2) / 2.0, (v2 - v1).length))

    return weightedMean(couples)


def calculateCOM_Vertices(mesh):
    points = [vertex.co for vertex in mesh.vertices]

    return arithmeticMean(points)


def isManifold(mesh, do_check=True):
    if not do_check:
        return True

    """
    edges = {}
    for poly in mesh.polygons:
        for k in poly.edge_keys:
            if k in edges:
                if edges[k] > 1:
                    return False
                edges[k] += 1
            else:
                edges[k] = 1

    s = sorted(edges.values())
    if s[0] != 2 or s[-1] != 2:
        print(2)
        return False
    """

    s = sorted(edge_face_count(mesh))
    if s[0] != 2 or s[-1] != 2:
        return False

    # XXX: check for verts/edges out of faces?
    """
    for edge in mesh.edges:
        if edge not in edges:
            return False
    """

    return True


def isNormalsOrientationClean(mesh, do_check=True):
    if not do_check:
        return True

    for i, p in enumerate(mesh.polygons):
        e = p.edge_keys
        set_e = set(e)
        p_edges = [(p.vertices[i - 1], v) for i, v in enumerate(p.vertices)]
        for q in mesh.polygons[i + 1:]:
            f = q.edge_keys
            q_edges = [(q.vertices[i - 1], v) for i, v in enumerate(q.vertices)]
            inter = set_e.intersection(set(f))
            if len(inter) == 0:
                continue
            vs = inter.pop()
            if (vs in p_edges) == (vs in q_edges):
                return False

    return True


# ------ Mesh Summary ------
from operator import itemgetter


def us(qty):
    """
    Convert qty to truncated string with unit suffixes.
    eg turn 12345678 into 12.3M
    """

    if qty < 1000:
        return str(qty)

    for suf in ['K', 'M', 'G', 'T', 'P', 'E']:
        qty /= 1000
        if qty < 1000:
            return "%3.1f%s" % (qty, suf)


class Properties_meshinfo(bpy.types.Panel):
    bl_label = "Mesh Summary"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        prefs = bpy.context.user_preferences.addons[__name__].preferences
        layout = self.layout

        meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        row = layout.row()
        if len(meshes) == 1:
            row.label(text="1 Mesh object in this scene.", icon='OBJECT_DATA')
        else:
            row.label(text=us(len(meshes)) + " Mesh objects in this scene.", icon='OBJECT_DATA')
            row = layout.row()
            if len(meshes) > prefs.display_limit:
                row.label(text="Top %d mesh objects." % prefs.display_limit)
            else:
                row.label(text="Top %d mesh objects." % len(meshes))

        row = layout.row()
        row.prop(prefs, "calculate_modifier_verts")
        if len(meshes) > 0:
            dataCols = []
            row = layout.row()
            dataCols.append(row.column())  # name
            dataCols.append(row.column())  # verts
            dataCols.append(row.column())  # verts after modifiers
            dataCols.append(row.column())  # edges
            dataCols.append(row.column())  # faces

            topMeshes = [(o, o.name, len(o.data.vertices), len(o.data.edges), len(o.data.polygons)) for o in meshes]
            topMeshes = sorted(topMeshes, key=itemgetter(2), reverse=True)[:prefs.display_limit]

            headRow = dataCols[0].row()
            headRow.label(text="Name")
            headRow = dataCols[1].row()
            headRow.label(text="Verts")
            headRow = dataCols[2].row()
            headRow.label(text="(mod.)")
            headRow = dataCols[3].row()
            headRow.label(text="Edges")
            headRow = dataCols[4].row()
            headRow.label(text="Faces")

            for mo in topMeshes:
                detailRow = dataCols[0].row()
                detailRow.label(text=mo[1])
                detailRow = dataCols[1].row()
                detailRow.label(text=us(mo[2]))
                if prefs.calculate_modifier_verts:
                    detailRow = dataCols[2].row()
                    bm = bmesh.new()
                    bm.from_object(mo[0], context.scene)
                    detailRow.label(text="(" + us(len(bm.verts)) + ")")
                    bm.free()
                detailRow = dataCols[3].row()
                detailRow.label(text=us(mo[3]))
                detailRow = dataCols[4].row()
                detailRow.label(text=us(mo[4]))

            vTotal = sum([len(o.data.vertices) for o in meshes])
            eTotal = sum([len(o.data.edges) for o in meshes])
            fTotal = sum([len(o.data.polygons) for o in meshes])

            totRow = dataCols[0].row()
            totRow.label(text="Scene totals:")
            totRow = dataCols[1].row()
            totRow.label(text=us(vTotal))
            totRow = dataCols[3].row()
            totRow.label(text=us(eTotal))
            totRow = dataCols[4].row()
            totRow.label(text=us(fTotal))

# ------ Index ------


def IM_select(indexList, type):
    # indices = [4608]    #add more indices: [0, 1, 4, 722]
    mesh = bpy.context.active_object.data
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    if type == 'vertex':
        bpy.context.scene.tool_settings.mesh_select_mode = (True, False, False)
        for vert in mesh.vertices:
            # print(vert.index)
            for target in indexList:
                if vert.index == target:
                    vert.select = True
                    print(target, ' vertex selected')

    if type == 'face':
        bpy.context.scene.tool_settings.mesh_select_mode = (False, False, True)
        for face in mesh.polygons:
            # print(face.index)
            for target in indexList:
                if face.index == target:
                    face.select = True
                    print(target, ' face selected')

    if type == 'edge':
        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)
        for edge in mesh.edges:
            # print(edge.index)
            for target in indexList:
                if edge.index == target:
                    edge.select = True
                    print(target, ' edge selected')

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    #bpy.context.scene.tool_settings.mesh_select_mode = (True, True, True)


def IM_show_extra_indices(self, context):
    mesh = bpy.context.active_object.data
    config = bpy.context.scene.CONFIG_IndexMarker
    print("Show indices: ", config.show_extra_indices)

    # enable debug mode, show indices
    # bpy.app.debug  to True while blender is running
    if config.show_extra_indices == True:
        bpy.app.debug = True
        mesh.show_extra_indices = True
    else:
        bpy.app.debug = False
        mesh.show_extra_indices = False

# ------ Ruler ------


def edit_mode_out():
    bpy.ops.object.mode_set(mode='OBJECT')


def edit_mode_in():
    bpy.ops.object.mode_set(mode='EDIT')

# ------ Ruler ------


def draw_callback_px(self, context):

    if context.mode == "EDIT_MESH":
        en0 = context.scene.dt_custom_props.en0

        font_id = 0
        font_size = context.scene.dt_custom_props.fs

        ob_act = context.active_object
        bme = bmesh.from_edit_mesh(ob_act.data)
        mtrx = ob_act.matrix_world

        list_0 = [v.index for v in bme.verts if v.select]
        if len(list_0) != 0:
            p = bme.verts[list_0[0]].co.copy()
            p_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, p)

            q = mtrx * bme.verts[list_0[0]].co.copy()
            q_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, q)

            # -- -- -- -- distance to adjacent vertices
            if context.scene.dt_custom_props.b0 == True:
                list_ = [[v.index for v in e.verts] for e in bme.verts[list_0[0]].link_edges]
                for ek in list_:
                    vi = [i for i in ek if i != list_0[0]][0]
                    p1 = bme.verts[vi].co.copy()
                    loc_0_3d = mtrx * ((p + p1) * 0.5)
                    loc_0_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, loc_0_3d)
                    bgl.glColor4f(1.0, 1.0, 0.0, context.scene.dt_custom_props.a)
                    blf.position(font_id, loc_0_2d[0] + 4, loc_0_2d[1] + 4, 0)
                    blf.size(font_id, font_size, context.user_preferences.system.dpi)
                    blf.draw(font_id, str(round((p - p1).length, 4)))

            bgl.glLineStipple(4, 0xAAAA)
            bgl.glEnable(bgl.GL_LINE_STIPPLE)

            # -- -- -- -- distance to axis local global
            if context.scene.dt_custom_props.b1 == True:

                # -- -- -- -- local
                if en0 == 'opt0':

                    # -- -- -- -- x axis
                    px = mtrx * Vector((0.0, p[1], p[2]))
                    px_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, px)

                    bgl.glEnable(bgl.GL_BLEND)
                    bgl.glColor4f(1.0, 0.0, 0.0, context.scene.dt_custom_props.a)
                    bgl.glBegin(bgl.GL_LINES)
                    bgl.glVertex2f(q_loc_2d[0], q_loc_2d[1])
                    bgl.glVertex2f(px_loc_2d[0], px_loc_2d[1])
                    bgl.glEnd()
                    bgl.glDisable(bgl.GL_BLEND)

                    if context.scene.dt_custom_props.b2 == False:
                        lx = (q_loc_2d + px_loc_2d) * 0.5
                        bgl.glColor4f(1.0, 0.0, 0.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, lx[0] + 4, lx[1] + 4, 0)
                        blf.size(font_id, font_size, context.user_preferences.system.dpi)
                        blf.draw(font_id, str(round(p[0], 4)))

                    # -- -- -- -- y axis
                    py = mtrx * Vector((p[0], 0.0, p[2]))
                    py_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, py)

                    bgl.glEnable(bgl.GL_BLEND)
                    bgl.glColor4f(0.0, 1.0, 0.0, context.scene.dt_custom_props.a)
                    bgl.glBegin(bgl.GL_LINES)
                    bgl.glVertex2f(q_loc_2d[0], q_loc_2d[1])
                    bgl.glVertex2f(py_loc_2d[0], py_loc_2d[1])
                    bgl.glEnd()
                    bgl.glDisable(bgl.GL_BLEND)

                    if context.scene.dt_custom_props.b2 == False:
                        ly = (q_loc_2d + py_loc_2d) * 0.5
                        bgl.glColor4f(0.0, 1.0, 0.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, ly[0] + 4, ly[1] + 4, 0)
                        blf.size(font_id, font_size, context.user_preferences.system.dpi)
                        blf.draw(font_id, str(round(p[1], 4)))

                    # -- -- -- -- z axis
                    pz = mtrx * Vector((p[0], p[1], 0.0))
                    pz_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, pz)

                    bgl.glEnable(bgl.GL_BLEND)
                    bgl.glColor4f(0.0, 0.0, 1.0, context.scene.dt_custom_props.a)
                    bgl.glBegin(bgl.GL_LINES)
                    bgl.glVertex2f(q_loc_2d[0], q_loc_2d[1])
                    bgl.glVertex2f(pz_loc_2d[0], pz_loc_2d[1])
                    bgl.glEnd()
                    bgl.glDisable(bgl.GL_BLEND)

                    if context.scene.dt_custom_props.b2 == False:
                        lz = (q_loc_2d + pz_loc_2d) * 0.5
                        bgl.glColor4f(0.0, 0.0, 1.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, lz[0] + 4, lz[1] + 4, 0)
                        blf.size(font_id, font_size, context.user_preferences.system.dpi)
                        blf.draw(font_id, str(round(p[2], 4)))

                    # -- -- -- --
                    if context.scene.dt_custom_props.b2 == True and context.scene.dt_custom_props.b1 == True:
                        blf.size(font_id, font_size, context.user_preferences.system.dpi)

                        bgl.glColor4f(1.0, 0.0, 0.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, q_loc_2d[0] + 4, q_loc_2d[1] + 4 + font_size + 4 + font_size + 4, 0)
                        blf.draw(font_id, 'x ' + str(round(p[0], 4)))

                        bgl.glColor4f(0.0, 1.0, 0.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, q_loc_2d[0] + 4, q_loc_2d[1] + 4 + font_size + 4, 0)
                        blf.draw(font_id, 'y ' + str(round(p[1], 4)))

                        bgl.glColor4f(0.0, 0.0, 1.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, q_loc_2d[0] + 4, q_loc_2d[1] + 4, 0)
                        blf.draw(font_id, 'z ' + str(round(p[2], 4)))

                # -- -- -- -- global
                elif en0 == 'opt1':

                    # -- -- -- -- x axis
                    ip_x = intersect_line_plane(q, q + (Vector((1.0, 0.0, 0.0)) * 0.1), Vector((0.0, 1.0, 0.0)), Vector((1.0, 0.0, 0.0)))
                    ip_x_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, ip_x)

                    bgl.glEnable(bgl.GL_BLEND)
                    bgl.glColor4f(1.0, 0.0, 0.0, context.scene.dt_custom_props.a)
                    bgl.glBegin(bgl.GL_LINES)
                    bgl.glVertex2f(q_loc_2d[0], q_loc_2d[1])
                    bgl.glVertex2f(ip_x_loc_2d[0], ip_x_loc_2d[1])
                    bgl.glEnd()
                    bgl.glDisable(bgl.GL_BLEND)

                    if context.scene.dt_custom_props.b2 == False:
                        loc_1_2d = (q_loc_2d + ip_x_loc_2d) * 0.5
                        bgl.glColor4f(1.0, 0.0, 0.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, loc_1_2d[0] + 4, loc_1_2d[1] + 4, 0)
                        blf.size(font_id, font_size, context.user_preferences.system.dpi)
                        blf.draw(font_id, str(round((q - ip_x).length, 4)))

                    # -- -- -- -- y axis
                    ip_y = intersect_line_plane(q, q + (Vector((0.0, 1.0, 0.0)) * 0.1), Vector((1.0, 0.0, 0.0)), Vector((0.0, 1.0, 0.0)))
                    ip_y_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, ip_y)

                    bgl.glEnable(bgl.GL_BLEND)
                    bgl.glColor4f(0.0, 1.0, 0.0, context.scene.dt_custom_props.a)
                    bgl.glBegin(bgl.GL_LINES)
                    bgl.glVertex2f(q_loc_2d[0], q_loc_2d[1])
                    bgl.glVertex2f(ip_y_loc_2d[0], ip_y_loc_2d[1])
                    bgl.glEnd()
                    bgl.glDisable(bgl.GL_BLEND)

                    if context.scene.dt_custom_props.b2 == False:
                        loc_2_2d = (q_loc_2d + ip_y_loc_2d) * 0.5
                        bgl.glColor4f(0.0, 1.0, 0.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, loc_2_2d[0] + 4, loc_2_2d[1] + 4, 0)
                        blf.size(font_id, font_size, context.user_preferences.system.dpi)
                        blf.draw(font_id, str(round((q - ip_y).length, 4)))

                    # -- -- -- -- z axis
                    ip_z = intersect_line_plane(q, q + (Vector((0.0, 0.0, 1.0)) * 0.1), Vector((1.0, 0.0, 0.0)), Vector((0.0, 0.0, 1.0)))
                    ip_z_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, ip_z)

                    bgl.glEnable(bgl.GL_BLEND)
                    bgl.glColor4f(0.0, 0.0, 1.0, context.scene.dt_custom_props.a)
                    bgl.glBegin(bgl.GL_LINES)
                    bgl.glVertex2f(q_loc_2d[0], q_loc_2d[1])
                    bgl.glVertex2f(ip_z_loc_2d[0], ip_z_loc_2d[1])
                    bgl.glEnd()
                    bgl.glDisable(bgl.GL_BLEND)

                    if context.scene.dt_custom_props.b2 == False:
                        loc_3_2d = (q_loc_2d + ip_z_loc_2d) * 0.5
                        bgl.glColor4f(0.0, 0.0, 1.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, loc_3_2d[0] + 4, loc_3_2d[1] + 4, 0)
                        blf.size(font_id, font_size, context.user_preferences.system.dpi)
                        blf.draw(font_id, str(round((q - ip_z).length, 4)))

                    # -- -- -- --
                    if context.scene.dt_custom_props.b2 == True and context.scene.dt_custom_props.b1 == True:
                        blf.size(font_id, font_size, context.user_preferences.system.dpi)

                        bgl.glColor4f(1.0, 0.0, 0.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, q_loc_2d[0] + 4, q_loc_2d[1] + 4 + font_size + 4 + font_size + 4, 0)
                        blf.draw(font_id, 'x ' + str(round((q - ip_x).length, 4)))

                        bgl.glColor4f(0.0, 1.0, 0.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, q_loc_2d[0] + 4, q_loc_2d[1] + 4 + font_size + 4, 0)
                        blf.draw(font_id, 'y ' + str(round((q - ip_y).length, 4)))

                        bgl.glColor4f(0.0, 0.0, 1.0, context.scene.dt_custom_props.a)
                        blf.position(font_id, q_loc_2d[0] + 4, q_loc_2d[1] + 4, 0)
                        blf.draw(font_id, 'z ' + str(round((q - ip_z).length, 4)))

            # -- -- -- -- mouse location
            if context.scene.dt_custom_props.b4 == True:

                rgn = context.region      # region
                rgn_3d = context.space_data.region_3d      # region 3d

                bgl.glEnable(bgl.GL_BLEND)
                bgl.glColor4f(1.0, 1.0, 1.0, context.scene.dt_custom_props.a)
                bgl.glBegin(bgl.GL_LINES)
                bgl.glVertex2f(0, dt_buf.y)
                bgl.glVertex2f(dt_buf.x - 15, dt_buf.y)
                bgl.glEnd()
                bgl.glDisable(bgl.GL_BLEND)

                bgl.glEnable(bgl.GL_BLEND)
                bgl.glColor4f(1.0, 1.0, 1.0, context.scene.dt_custom_props.a)
                bgl.glBegin(bgl.GL_LINES)
                bgl.glVertex2f(rgn.width, dt_buf.y)
                bgl.glVertex2f(dt_buf.x + 15, dt_buf.y)
                bgl.glEnd()
                bgl.glDisable(bgl.GL_BLEND)

                bgl.glEnable(bgl.GL_BLEND)
                bgl.glColor4f(1.0, 1.0, 1.0, context.scene.dt_custom_props.a)
                bgl.glBegin(bgl.GL_LINES)
                bgl.glVertex2f(dt_buf.x, 0)
                bgl.glVertex2f(dt_buf.x, dt_buf.y - 15)
                bgl.glEnd()
                bgl.glDisable(bgl.GL_BLEND)

                bgl.glEnable(bgl.GL_BLEND)
                bgl.glColor4f(1.0, 1.0, 1.0, context.scene.dt_custom_props.a)
                bgl.glBegin(bgl.GL_LINES)
                bgl.glVertex2f(dt_buf.x, rgn.height)
                bgl.glVertex2f(dt_buf.x, dt_buf.y + 15)
                bgl.glEnd()
                bgl.glDisable(bgl.GL_BLEND)
                bgl.glDisable(bgl.GL_LINE_STIPPLE)

                t = str(dt_buf.x) + ', ' + str(dt_buf.y)
                lo = region_2d_to_location_3d(context.region, context.space_data.region_3d, Vector((dt_buf.x, dt_buf.y)), Vector((0.0, 0.0, 0.0)))
                t1 = '( ' + str(round(lo[0], 4)) + ', ' + str(round(lo[1], 4)) + ', ' + str(round(lo[2], 4)) + ' )'

                bgl.glColor4f(1.0, 1.0, 1.0, context.scene.dt_custom_props.a)
                blf.position(font_id, dt_buf.x + 15, dt_buf.y + 15, 0)
                blf.size(font_id, 14, context.user_preferences.system.dpi)
                blf.draw(font_id, t1 if context.scene.dt_custom_props.b5 == True else t)

            bgl.glDisable(bgl.GL_LINE_STIPPLE)

            # -- -- -- -- angles
            if context.scene.dt_custom_props.b3 == True:
                list_ek = [[v.index for v in e.verts] for e in bme.verts[list_0[0]].link_edges]
                n1 = len(list_ek)

                for j in range(n1):
                    vec1 = p - bme.verts[[i for i in list_ek[j] if i != list_0[0]][0]].co.copy()
                    vec2 = p - bme.verts[[i for i in list_ek[(j + 1) % n1] if i != list_0[0]][0]].co.copy()
                    ang = vec1.angle(vec2)

                    a_loc_2d = location_3d_to_region_2d(context.region, context.space_data.region_3d, mtrx * (((p - (vec1.normalized() * 0.1)) + (p - (vec2.normalized() * 0.1))) * 0.5))

                    bgl.glColor4f(0.0, 0.757, 1.0, context.scene.dt_custom_props.a)
                    blf.position(font_id, a_loc_2d[0], a_loc_2d[1], 0)
                    blf.size(font_id, font_size, context.user_preferences.system.dpi)
                    blf.draw(font_id, str(round(ang, 4) if context.scene.dt_custom_props.b6 == True else round(degrees(ang), 2)))

            # -- -- -- -- tool on/off
                    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
                    blf.position(font_id, 150, 10, 0)
                    blf.size(font_id, 20, context.user_preferences.system.dpi)
                    blf.draw(font_id, 'Ruler On')

# ------ index ------


class UIElements(bpy.types.PropertyGroup):

    get_indices = bpy.props.StringProperty(name="Index", description="input vertex, face or edge indices here for selection. example: 1,2,3")
    show_extra_indices = bpy.props.BoolProperty(name="Show selected indices", default=False, description="Display the index numbers of selected vertices, edges, and faces. Note: enables debug mode", update=IM_show_extra_indices)

#======================================================================#
#         operators
#======================================================================#


class OBJECT_OP_SelectVertices(bpy.types.Operator):
    bl_idname = "mesh.vertex_select"
    bl_label = "Select vertex"
    bl_description = "select vertices"

    def execute(self, context):
        # get arguments from UIElemtnts
        config = bpy.context.scene.CONFIG_IndexMarker

        # lets convert the values to int and pass the list to the select function
        indexList = []
        detectList = config.get_indices.split(',')
        for i in detectList:
            if i and i.isdigit():
                indexList.append(int(i))
            else:
                print("missing or wrong input")
                break

        # print(indexList)
        type = 'vertex'
        IM_select(indexList, type)
        return {'FINISHED'}


class OBJECT_OP_SelectFaces(bpy.types.Operator):
    bl_idname = "mesh.face_select"
    bl_label = "Select face"
    bl_description = "select faces"

    def execute(self, context):
        # get arguments from UIElemtnts
        config = bpy.context.scene.CONFIG_IndexMarker

        # lets convert the values to int and pass the list to the select function
        indexList = []
        detectList = config.get_indices.split(',')
        for i in detectList:
            if i and i.isdigit():
                indexList.append(int(i))
            else:
                print("missing or wrong input")
                break

        # print(indexList)
        type = 'face'
        IM_select(indexList, type)
        return {'FINISHED'}


class OBJECT_OP_SelectEdges(bpy.types.Operator):
    bl_idname = "mesh.edge_select"
    bl_label = "Select edge"
    bl_description = "select edges"

    def execute(self, context):
        # get arguments from UIElemtnts
        config = bpy.context.scene.CONFIG_IndexMarker

        # lets convert the values to int and pass the list to the select function
        indexList = []
        detectList = config.get_indices.split(',')
        for i in detectList:
            if i and i.isdigit():
                indexList.append(int(i))
            else:
                print("missing or wrong input")
                break

        # print(indexList)
        type = 'edge'
        IM_select(indexList, type)
        return {'FINISHED'}

# ------ ruler ------


class dt_p_group0(bpy.types.PropertyGroup):
    a = FloatProperty(name='', default=1.0, min=0.1, max=1.0, step=10, precision=1)
    fs = IntProperty(name='', default=14, min=12, max=40, step=1)
    b0 = BoolProperty(name='', default=False)
    b1 = BoolProperty(name='', default=True)
    b2 = BoolProperty(name='', default=False)
    b3 = BoolProperty(name='', default=False)
    b4 = BoolProperty(name='', default=False)
    b5 = BoolProperty(name='', default=False)
    b6 = BoolProperty(name='', default=False)
    en0 = EnumProperty(items=(('opt0', 'Local', ''), ('opt1', 'Global', '')), name='', default='opt0')

# ------ ruler------


class dt_buf():
    mha = 0
    text = 'Enable'
    x = 0
    y = 0

# ------ ruler operator 0 ------


class dt_op0(bpy.types.Operator):
    bl_idname = 'dt.op0_id'
    bl_label = 'Display Tool'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def modal(self, context, event):
        context.area.tag_redraw()
        if event.type == 'MOUSEMOVE':
            dt_buf.x = event.mouse_region_x
            dt_buf.y = event.mouse_region_y

        if dt_buf.mha == -1:
            context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            dt_buf.mha = 0
            dt_buf.text = 'Enable'
            return {"CANCELLED"}

        if context.mode != "EDIT_MESH":
            context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            dt_buf.mha = 0
            dt_buf.text = 'Enable'
            return {"CANCELLED"}
        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            if dt_buf.mha < 1:
                dt_buf.mha = 1
                dt_buf.text = 'Disable'
                context.window_manager.modal_handler_add(self)
                self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')
                return {"RUNNING_MODAL"}
            else:
                dt_buf.mha = -1
                if 'dt_custom_props' in bpy.context.scene:
                    del bpy.context.scene['dt_custom_props']
                return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, 'View3D not found, cannot run operator')
            return {'CANCELLED'}

# ------ ------


def menu_(self, context):
    layout = self.layout

    layout.separator()
    col = layout.column()
    col.label(text='Simple Ruler:')

    row = col.split(0.60, align=True)
    row.operator('dt.op0_id', text=dt_buf.text)

    if dt_buf.text == 'Disable':
        col.label('Ruler Font Settings:')
        row_ = col.split(0.50, align=True)
        row_.prop(context.scene.dt_custom_props, 'fs', text='Size', slider=True)
        row_.prop(context.scene.dt_custom_props, 'a', text='Alpha', slider=True)

        col.prop(context.scene.dt_custom_props, 'b0', text='Edge Length')

        row3 = col.row(align=False)
        row3.prop(context.scene.dt_custom_props, 'b3', text='Angle', toggle=False)
        if context.scene.dt_custom_props.b3 == True:
            row3.prop(context.scene.dt_custom_props, 'b6', text='Radians', toggle=False)

        col.prop(context.scene.dt_custom_props, 'b1', text='Distance To Axis', toggle=False)
        if context.scene.dt_custom_props.b1 == True:
            row1 = col.split(0.60, align=True)
            row1.prop(context.scene.dt_custom_props, 'en0', text='')
            row1.prop(context.scene.dt_custom_props, 'b2', text='Mode', toggle=True)

        row2 = col.split(0.80, align=True)
        row2.prop(context.scene.dt_custom_props, 'b4', text='Mouse Location', toggle=False)
        if context.scene.dt_custom_props.b4 == True:
            row2.prop(context.scene.dt_custom_props, 'b5', text='Bu', toggle=True)
    layout.separator()
    col = layout.column()
    col.label(text='Index Marker')
    config = bpy.context.scene.CONFIG_IndexMarker
    layout = self.layout
    ob = context.object
    type = ob.type.capitalize()
    objects = bpy.context.selected_objects
    game = ob.game

    # make sure a object is selected, otherwise hide settings and display warning
    if type == 'Mesh':
        if not objects:
            row = layout.row()
            row.label(text="No Active Object", icon='ERROR')
        else:
            row = layout.column()
            row.prop(config, "show_extra_indices")
            row.prop(config, "get_indices")

            row = layout.row()
            row.operator("mesh.vertex_select", text="vertices")
            row.operator("mesh.face_select", text="faces")
            row.operator("mesh.edge_select", text="edges")

# ------ class list ------

class_list = [
    dt_op0,
    dt_p_group0,
]


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    display_limit = IntProperty(name="Display limit",
                                description="Maximum number of items to list",
                                default=5, min=2, max=20)
    calculate_modifier_verts = BoolProperty(name="Calculate mod. vertices",
                                            description="Calculate vertex count after applying modifiers.",
                                            default=False)

    def draw(self, context):
        layout = self.layout
        layout.label(text="----Measure Tools----")
        layout.label(text="Experimental")
        layout.label(text="Mesh Lint, Measure, Index View & more.")
        layout.label(text="----Mesh Summary----")
        col = layout.column()
        row = col.row()
        row.prop(self, "calculate_modifier_verts")
        row = col.row()
        row.prop(self, "display_limit")
        col = row.column()  # this stops the button stretching

# ------ register ------


def register():
    for c in class_list:
        bpy.utils.register_class(c)
    bpy.types.Scene.dt_custom_props = PointerProperty(type=dt_p_group0)
    bpy.types.VIEW3D_PT_view3d_meshdisplay.append(menu_)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.CONFIG_IndexMarker = bpy.props.PointerProperty(type=UIElements)

# ------ unregister ------


def unregister():
    for c in class_list:
        bpy.utils.unregister_class(c)
    if 'dt_custom_props' in bpy.context.scene:
        del bpy.context.scene['dt_custom_props']
    bpy.types.VIEW3D_PT_view3d_meshdisplay.remove(menu_)

    if bpy.context.scene.get('CONFIG_IndexMarker') != None:
        del bpy.context.scene['CONFIG_IndexMarker']
    bpy.utils.unregister_module(__name__)
# ------ ------
if __name__ == "__main__":
    register()
