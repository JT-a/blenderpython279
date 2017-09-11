bl_info = {
    "name": "round_up",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create round_up primitive.",
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


class round_up(bpy.types.Operator):
    bl_idname = "mesh.round_up"
    bl_label = "round_up"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add round_up primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="round_up")
        obj = bpy.data.objects.new(name="round_up", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(0.5483438968658447, -1.0005161762237549, -1.8124410416930914e-08), (-0.9516561031341553, -1.0005161762237549, -1.8124410416930914e-08), (-0.9516561031341553, 0.9994838237762451, -1.8124410416930914e-08), (0.5483438968658447, -0.5005161762237549, -1.8124410416930914e-08), (0.07300214469432831, 0.9994838237762451, -1.8124410416930914e-08), (0.07013797014951706, 1.0005161762237549, 1.8124410416930914e-08), (0.7626547813415527, -0.2912794351577759, 1.4395173053571853e-08), (0.9097340106964111, -0.014108240604400635, 1.8124410416930914e-08), (0.9516561031341553, 0.26670801639556885, 1.8124410416930914e-08), (0.8862746953964233, 0.5475244522094727, 1.8124410416930914e-08), (0.7000843286514282, 0.7855889797210693, 1.8124410416930914e-08), (0.4214304983615875, 0.9446582794189453, 1.8124410416930914e-08)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[0, 1], [2, 1], [2, 4], [3, 0], [6, 3], [4, 5], [7, 6], [8, 7], [9, 8], [10, 9], [11, 10], [11, 5]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(3, 0, 1, 2, 4, 5, 11, 10, 9, 8, 7, 6)]
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
    self.layout.operator(round_up.bl_idname, text="round_up", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
