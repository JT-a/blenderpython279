bl_info = {
    "name": "Inlay_2",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Inlay_2 primitive.",
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


class Inlay_2(bpy.types.Operator):
    bl_idname = "mesh.inlay_2"
    bl_label = "Inlay_2"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Inlay_2 primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Inlay_2")
        obj = bpy.data.objects.new(name="Inlay_2", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.04894345998764038, 0.6909831166267395, 0.0), (0.19098299741744995, 0.4122147560119629, 0.0), (0.41221487522125244, 0.19098293781280518, 0.0), (0.6909828186035156, 0.048943519592285156, 0.0), (0.9999999403953552, 0.0, 0.0), (1.0, -0.5999999642372131, 0.0), (0.5999999046325684, -1.0, 3.552713678800501e-15)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[1, 0], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [0, 9], [9, 8], [8, 7]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(2, 1, 0, 9, 8, 7, 6, 5, 4, 3)]
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
    self.layout.operator(Inlay_2.bl_idname, text="Inlay_2", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
