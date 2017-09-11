bl_info = {
    "name": "Round_100",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Round_100 primitive.",
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


class Round_100(bpy.types.Operator):
    bl_idname = "mesh.round_100"
    bl_label = "Round_100"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Round_100 primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Round_100")
        obj = bpy.data.objects.new(name="Round_100", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (0.9021129608154297, -0.3819658160209656, 0.0), (0.6180341243743896, 0.17557036876678467, 0.0), (0.17557036876678467, 0.6180340051651001, 0.0), (-0.38196635246276855, 0.9021131992340088, 0.0), (-0.9999995827674866, 1.0, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[0, 1], [2, 1], [2, 8], [8, 7], [7, 6], [6, 5], [5, 4], [4, 3], [3, 0]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(3, 0, 1, 2, 8, 7, 6, 5, 4)]
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
    self.layout.operator(Round_100.bl_idname, text="Round_100", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
