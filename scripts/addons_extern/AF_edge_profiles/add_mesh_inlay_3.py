bl_info = {
    "name": "Inlay_3",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Inlay_3 primitive.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}


if "bpy" in locals():
    import imp


import bpy
import bmesh
import math
from mathutils import *


class Inlay_3(bpy.types.Operator):
    bl_idname = "mesh.inlay_3"
    bl_label = "Inlay_3"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Inlay_3 primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Inlay_3")
        obj = bpy.data.objects.new(name="Inlay_3", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (-0.11880004405975342, 1.0, 0.0), (-0.0640420913696289, 0.6542719006538391, 0.0), (0.09487175941467285, 0.34238582849502563, 0.0), (0.3423859477043152, 0.09487169981002808, 0.0), (0.6542716026306152, -0.0640420913696289, 0.0), (0.707249104976654, -0.07243290543556213, 0.0), (0.8007224798202515, -0.10118907690048218, 0.0), (0.882461667060852, -0.15488168597221375, 0.0), (0.9459754228591919, -0.22924678027629852, 0.0), (0.9862202405929565, -0.3183790445327759, 0.0), (0.9999998807907104, -0.4152000844478607, 0.0), (0.9999999403953552, -0.7647900581359863, 0.0), (0.988487958908081, -0.8374738693237305, 0.0), (0.9550788402557373, -0.9030429720878601, 0.0), (0.9030429124832153, -0.9550788402557373, 0.0), (0.8374739289283752, -0.988487958908081, 0.0), (0.7647900581359863, -0.9999999403953552, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[1, 0], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [12, 11], [11, 10], [10, 9], [9, 8], [8, 7], [7, 6], [0, 18], [18, 17], [17, 16], [16, 15], [15, 14], [14, 13], [13, 12]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 18, 17, 16, 15, 14, 13, 12)]
        for verts in facelist:
            vlist = []
            for idx in verts:
                vlist.append(bm.verts[idxlist[idx]])
            bm.faces.new(vlist)

        bm.to_mesh(mesh)
        mesh.update()
        bm.free()
        obj.rotation_quaternion = (Matrix.Rotation(math.radians(90), 3, 'X').to_quaternion())

        return {'FINISHED'}


def menu_item(self, context):
    self.layout.operator(Inlay_3.bl_idname, text="Inlay_3", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
