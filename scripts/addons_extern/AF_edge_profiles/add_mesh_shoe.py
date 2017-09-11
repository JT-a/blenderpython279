bl_info = {
    "name": "shoe",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create shoe primitive.",
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


class shoe(bpy.types.Operator):
    bl_idname = "mesh.shoe"
    bl_label = "shoe"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add shoe primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="shoe")
        obj = bpy.data.objects.new(name="shoe", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (1.0003929138183594, -0.9976814389228821, 5.032443004893139e-05), (1.0003929138183594, -0.7371903657913208, 5.032443004893139e-05), (0.9147418737411499, -0.30456674098968506, 5.032443004893139e-05), (0.6661726236343384, 0.08570900559425354, 5.032443004893139e-05), (0.2790168523788452, 0.39543354511260986, 5.032443004893139e-05), (-0.20882701873779297, 0.5942887663841248, 5.032443004893139e-05), (-0.5, 0.6628096699714661, 5.032443004893139e-05), (-0.5, 1.0, -1.504686224507168e-07)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[0, 1], [2, 1], [9, 8], [8, 7], [7, 6], [6, 5], [5, 4], [4, 3], [9, 10], [2, 10], [0, 3]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(3, 0, 1, 2, 10, 9, 8, 7, 6, 5, 4)]
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
    self.layout.operator(shoe.bl_idname, text="shoe", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
