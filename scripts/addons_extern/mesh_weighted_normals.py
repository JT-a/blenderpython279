bl_info = {
    "name": "Weighted Normals Calculation",
    "description": "Simple operator to calculate weighted normals on the mesh.",
    "author": "Simon Lusenc (50keda)",
    "version": (1, 0),
    "blender": (2, 74, 0),
    "location": "3D View > Quick Search",
    "category": "Object",
    "support": "COMMUNITY"
}

import bpy
import bmesh
import array
from mathutils import Vector


class WeightNormalsCalculator(bpy.types.Operator):
    """Calculate weighted normals for active object."""
    bl_idname = "object.calculate_weighted_normals"
    bl_label = "Weight Normals"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.mode == "OBJECT" and context.object.type == "MESH"

    def execute(self, context):

        mesh = context.object.data

        mesh.use_auto_smooth = True
        bpy.ops.mesh.customdata_custom_splitnormals_clear()

        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()

        nor_weighted = []
        for v in bm.verts:
            max_area = 0
            areas = {}
            for i, f in enumerate(v.link_faces):

                if f.smooth:
                    area = f.calc_area()
                    areas[i] = area

                    if area > max_area:
                        max_area = area

            normal = Vector()
            for i, f in enumerate(v.link_faces):
                if f.smooth:
                    perc = areas[i] / max_area
                    normal += perc * f.normal

            nor_weighted.extend(normal.normalized())

        bm.free()

        nor_list = [(0,)] * len(mesh.loops)
        for poly in mesh.polygons:

            l_s = poly.loop_start
            l_e = poly.loop_start + poly.loop_total - 1

            curr_l = l_s
            prev_l = l_e
            while curr_l <= l_e:

                curr_loop = mesh.loops[curr_l]
                prev_loop = mesh.loops[prev_l]

                # if at least one edge of this corner doesn't use sharp edge
                # apply calculated weighted normal
                if not mesh.edges[curr_loop.edge_index].use_edge_sharp or not mesh.edges[prev_loop.edge_index].use_edge_sharp:

                    curr_n = nor_weighted[curr_loop.vertex_index * 3:curr_loop.vertex_index * 3 + 3]
                    nor_list[curr_l] = curr_n

                else:

                    nor_list[curr_l] = curr_loop.normal

                prev_l = curr_l
                curr_l += 1

        bpy.ops.mesh.customdata_custom_splitnormals_add()
        mesh.normals_split_custom_set(nor_list)
        mesh.free_normals_split()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(WeightNormalsCalculator)


def unregister():
    bpy.utils.unregister_class(WeightNormalsCalculator)


if __name__ == '__main__':
    register()
