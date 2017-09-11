bl_info = {
    "name": "Inlay_1",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Inlay_1 primitive.",
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


class Inlay_1(bpy.types.Operator):
    bl_idname = "mesh.inlay_1"
    bl_label = "Inlay_1"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Inlay_1 primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Inlay_1")
        obj = bpy.data.objects.new(name="Inlay_1", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (-0.25, 1.0, 0.0), (-0.1888207197189331, 0.6137288808822632, 0.0), (-0.011271238327026367, 0.2652684450149536, 0.0), (0.26526856422424316, -0.011271357536315918, 0.0), (0.6137285232543945, -0.18882060050964355, 0.0), (0.9999998807907104, -0.25, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[0, 1], [2, 1], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 0]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(8, 0, 1, 2, 3, 4, 5, 6, 7)]
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
    self.layout.operator(Inlay_1.bl_idname, text="Inlay_1", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
