bl_info = {
    "name": "Double",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Double primitive.",
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


class Double(bpy.types.Operator):
    bl_idname = "mesh.double"
    bl_label = "Double"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Double primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Double")
        obj = bpy.data.objects.new(name="Double", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (0.25, 1.0, 0.0), (0.2867075800895691, 0.7682373523712158, 0.0), (0.39323723316192627, 0.5591610670089722, 0.0), (0.5591611862182617, 0.39323723316192627, 0.0), (0.7682371139526367, 0.28670763969421387, 0.0), (0.9999999403953552, 0.25, 0.0), (0.25, -1.0, 0.0), (0.2867075800895691, -0.7682373523712158, 0.0), (0.39323723316192627, -0.5591610670089722, 0.0), (0.5591611862182617, -0.39323723316192627, 0.0), (0.7682371139526367, -0.28670763969421387, 0.0), (0.9999999403953552, -0.25, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[1, 0], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [0, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 7]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(2, 1, 0, 8, 9, 10, 11, 12, 13, 7, 6, 5, 4, 3)]
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
    self.layout.operator(Double.bl_idname, text="Double", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
