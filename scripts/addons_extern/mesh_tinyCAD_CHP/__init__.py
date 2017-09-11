"""
2016 Dealga McArdle | zeffii@hotmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


bl_info = {
    "name": "CHP addon for tinycad",
    "description": "this tinycad add-on performs VTX-V and triggers Fillet in modal mode afterwards",
    "author": "Dealga McArdle",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "category": "Mesh"
}


import math

import bpy
import bmesh
import mathutils

from mathutils import Vector, Matrix
from mathutils.geometry import intersect_line_line as LineIntersect
from mathutils.geometry import intersect_point_line as PtLineIntersect

OWN_PRECISION = 1.0e-5


def point_on_edge(p, edge):
    '''
    # modified from cad_module
    > p:        vector
    > edge:     BMEdge
    < returns:  True / False if a point happens to lie on an edge
    '''
    pt, _percent = PtLineIntersect(p, edge.verts[0].co, edge.verts[1].co)
    on_line = (pt - p).length < OWN_PRECISION
    return on_line and (0.0 <= _percent <= 1.0)


def operate(context, bm, selected):
    edge_1, edge_2 = selected
    edge_1_co_1 = edge_1.verts[0].co
    edge_1_co_2 = edge_1.verts[1].co
    edge_2_co_1 = edge_2.verts[0].co
    edge_2_co_2 = edge_2.verts[1].co
    isect = LineIntersect(edge_1_co_1, edge_1_co_2, edge_2_co_1, edge_2_co_2)

    if (not isect) or ((isect[0] - isect[1]).length >= 1.0e-5):
        print('these edges do not intersect')
        return
    else:
        print('definite intersection found')

    p0 = isect[0]
    p1 = point_on_edge(p0, edge_1)
    p2 = point_on_edge(p0, edge_2)
    if (p1 and p2):
        print('point lies on both edges')
        return
    elif (p1 or p2):
        print('point lies on 1 edge')
        return

    # reaches this point if the intersection doesnt lie on either edge
    def get_vertex(edge):
        IDX_BOOL = bool((edge.verts[0].co - p0).length > (edge.verts[1].co - p0).length)
        return edge.verts[IDX_BOOL]

    bm.select_mode = {'VERT'}
    bm.select_flush_mode()
    v1 = bm.verts.new(p0)
    e1 = bm.edges.new([v1, get_vertex(edge_1)])
    e2 = bm.edges.new([v1, get_vertex(edge_2)])
    edge_1.select = False
    edge_2.select = False
    v1.select = True

    return True


class TCChamferPlus(bpy.types.Operator):
    bl_idname = "tinycad.chamfer_plus"
    bl_label = "CHP | Chamfer Plus"
    bl_description = "Extends towards intersection, then Fillet"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return all([bool(ob), ob.type == 'MESH', ob.mode == 'EDIT'])

    def execute(self, context):
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        selected = [e for e in bm.edges if e.select and (not e.hide)]

        if len(selected) == 2:
            if operate(context, bm, selected):
                bmesh.update_edit_mesh(me, True)

                # bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=True)
                bpy.ops.mesh.bevel('INVOKE_REGION_WIN', vertex_only=True)

                return {"FINISHED"}

        bmesh.update_edit_mesh(me, True)
        return {"CANCELLED"}


def menu_func(self, context):
    operator = self.layout.operator
    operator('tinycad.chamfer_plus', text='CHP | Chamfer+ (VTX-V /w Fillet)')


def register():
    bpy.utils.register_module(__name__)
    try:
        bpy.types.VIEW3D_MT_edit_mesh_tinycad.append(menu_func)
    except:
        print('mesh_tinyCAD menu not found, cannot add')


def unregister():
    bpy.utils.unregister_module(__name__)
    try:
        bpy.types.VIEW3D_MT_edit_mesh_tinycad.remove(menu_func)
    except:
        ...
