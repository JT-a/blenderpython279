bl_info = {
    "name": "nose_1",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create nose_1 primitive.",
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


class nose_1(bpy.types.Operator):
    bl_idname = "mesh.nose_1"
    bl_label = "nose_1"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add nose_1 primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="nose_1")
        obj = bpy.data.objects.new(name="nose_1", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (1.0, 0.6000000238418579, 0.0), (0.9804226160049438, 0.7236067652702332, 0.0), (0.923606812953949, 0.8351141214370728, 0.0), (0.835114061832428, 0.9236068725585938, 0.0), (0.7236068844795227, 0.9804226160049438, 0.0), (0.6000000834465027, 1.0, 0.0), (1.0, -0.6000000238418579, 0.0), (0.9804226160049438, -0.7236067652702332, 0.0), (0.923606812953949, -0.8351141214370728, 0.0), (0.835114061832428, -0.9236068725585938, 0.0), (0.7236068844795227, -0.9804226160049438, 0.0), (0.6000000834465027, -1.0, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[1, 0], [1, 7], [7, 6], [6, 5], [5, 4], [4, 3], [3, 2], [0, 13], [13, 12], [12, 11], [11, 10], [10, 9], [9, 8], [8, 2]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(7, 1, 0, 13, 12, 11, 10, 9, 8, 2, 3, 4, 5, 6)]
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
    self.layout.operator(nose_1.bl_idname, text="nose_1", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
