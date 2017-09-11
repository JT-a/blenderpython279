bl_info = {
    "name": "round_50",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create round_50 primitive.",
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


class round_50(bpy.types.Operator):
    bl_idname = "mesh.round_50"
    bl_label = "round_50"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add round_50 primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="round_50")
        obj = bpy.data.objects.new(name="round_50", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (1.0, 0.25, 0.0), (0.9632923603057861, 0.48176270723342896, 0.0), (0.8567626476287842, 0.6908389329910278, 0.0), (0.6908390522003174, 0.8567626476287842, 0.0), (0.48176267743110657, 0.9632924199104309, 0.0), (0.24999982118606567, 1.0, 0.0)]
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
    self.layout.operator(round_50.bl_idname, text="round_50", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
