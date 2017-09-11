bl_info = {
    "name": "Quad",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Quad primitive.",
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


class Quad(bpy.types.Operator):
    bl_idname = "mesh.quad"
    bl_label = "Quad"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Quad primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Quad")
        obj = bpy.data.objects.new(name="Quad", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(1.0, 0.5, 0.0), (1.0, -0.5, 0.0), (-1.0, -0.5, 0.0), (-0.5, 1.0, 0.0), (-0.5244717597961426, 0.8454915285110474, 0.0), (-0.5954915285110474, 0.7061073780059814, 0.0), (-0.7061074376106262, 0.5954914689064026, 0.0), (-0.8454914093017578, 0.5244717597961426, 0.0), (-0.9999999403953552, 0.5, 0.0), (-0.8454915285110474, -0.5244717597961426, 0.0), (-0.7061073780059814, -0.5954915285110474, 0.0), (-0.5954914689064026, -0.7061074376106262, 0.0), (-0.5244717597961426, -0.8454914093017578, 0.0), (-0.5, -0.9999999403953552, 0.0), (0.8454915285110474, -0.5244717597961426, 0.0), (0.7061073780059814, -0.5954915285110474, 0.0), (0.5954914689064026, -0.7061074376106262, 0.0), (0.5244717597961426, -0.8454914093017578, 0.0), (0.5, -0.9999999403953552, 0.0), (0.8454915285110474, 0.5244717597961426, 0.0), (0.7061073780059814, 0.5954915285110474, 0.0), (0.5954914689064026, 0.7061074376106262, 0.0), (0.5244717597961426, 0.8454914093017578, 0.0), (0.5, 0.9999999403953552, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[16, 17], [11, 12], [21, 22], [10, 11], [3, 4], [14, 15], [4, 5], [9, 10], [5, 6], [19, 20], [6, 7], [2, 9], [7, 8], [15, 16], [8, 2], [1, 14], [12, 13], [20, 21], [0, 19], [17, 18], [18, 13], [1, 0], [22, 23], [23, 3]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(4, 5, 6, 7, 8, 2, 9, 10, 11, 12, 13, 18, 17, 16, 15, 14, 1, 0, 19, 20, 21, 22, 23, 3)]
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
    self.layout.operator(Quad.bl_idname, text="Quad", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
