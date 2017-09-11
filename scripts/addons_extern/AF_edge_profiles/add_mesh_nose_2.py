bl_info = {
    "name": "nose_2",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create nose_2 primitive.",
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


class nose_2(bpy.types.Operator):
    bl_idname = "mesh.nose_2"
    bl_label = "nose_2"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add nose_2 primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="nose_2")
        obj = bpy.data.objects.new(name="nose_2", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(-1.0, -1.0, 0.0), (1.0, 0.010400176048278809, 0.0), (-1.0, 1.0, 0.0), (1.0, -0.010400176048278809, 0.0), (0.9505475163459778, 0.301830530166626, 0.0), (0.8070307374000549, 0.5834981203079224, 0.0), (0.5834980010986328, 0.8070307970046997, 0.0), (0.30183082818984985, 0.950547456741333, 0.0), (-0.01040009967982769, 1.0, 0.0), (0.9505475163459778, -0.301830530166626, 0.0), (0.8070307374000549, -0.5834981203079224, 0.0), (0.5834980010986328, -0.8070307970046997, 0.0), (0.30183082818984985, -0.950547456741333, 0.0), (-0.01040009967982769, -1.0, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[10, 9], [2, 0], [2, 8], [11, 10], [8, 7], [7, 6], [12, 11], [6, 5], [5, 4], [13, 12], [4, 3], [0, 13], [9, 1], [1, 3]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(4, 5, 6, 7, 8, 2, 0, 13, 12, 11, 10, 9, 1, 3)]
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
    self.layout.operator(nose_2.bl_idname, text="nose_2", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
