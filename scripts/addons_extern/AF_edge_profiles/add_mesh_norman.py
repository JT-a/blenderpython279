bl_info = {
    "name": "Norman",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Norman primitive.",
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


class Norman(bpy.types.Operator):
    bl_idname = "mesh.norman"
    bl_label = "Norman"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Norman primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Norman")
        obj = bpy.data.objects.new(name="Norman", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(0.4435911178588867, 0.7137556076049805, 0.0), (0.6942288875579834, 0.5462849140167236, 0.0), (0.8616995811462402, 0.29564735293388367, 0.0), (0.9205076694488525, 1.4901161193847656e-08, 0.0), (0.8616998195648193, -0.2956472635269165, 0.0), (0.6942288875579834, -0.5462850332260132, 0.0), (0.4435913562774658, -0.7137556076049805, 0.0), (0.12949275970458984, -0.7725633382797241, 0.0), (0.12949275970458984, 0.7725633382797241, 0.0), (0.12949275970458984, 0.9999998807907104, 0.0), (-0.9205074310302734, 1.0, 0.0), (-0.9205074310302734, -1.0, 0.0), (0.12949275970458984, -1.0, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[9, 8], [0, 8], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [12, 7], [10, 9], [10, 11], [12, 11]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(7, 12, 11, 10, 9, 8, 0, 1, 2, 3, 4, 5, 6)]
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
    self.layout.operator(Norman.bl_idname, text="Norman", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
