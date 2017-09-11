bl_info = {
    "name": "Cornice",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Cornice primitive.",
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


class Cornice(bpy.types.Operator):
    bl_idname = "mesh.cornice"
    bl_label = "Cornice"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Cornice primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Cornice")
        obj = bpy.data.objects.new(name="Cornice", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(-1.0, 1.0, 0.0), (1.0, 0.5895997285842896, 0.0), (0.979913592338562, 0.7164203524589539, 0.0), (0.9216204881668091, 0.8308269381523132, 0.0), (0.8308268785476685, 0.9216205477714539, 0.0), (0.7164204716682434, 0.979913592338562, 0.0), (0.5895997881889343, 1.0, 0.0), (-1.0, -0.5895997285842896, 0.0), (-0.979913592338562, -0.7164203524589539, 0.0), (-0.9216204881668091, -0.8308269381523132, 0.0), (-0.8308268785476685, -0.9216205477714539, 0.0), (-0.7164204716682434, -0.979913592338562, 0.0), (-0.5895997881889343, -1.0, 0.0), (1.0, 0.4883997440338135, 0.0), (0.5400593280792236, 0.4155522584915161, 0.0), (0.12514060735702515, 0.20414066314697266, 0.0), (-0.2041407823562622, -0.12514078617095947, 0.0), (-0.4155522584915161, -0.5400589108467102, 0.0), (-0.4883997440338135, -0.9999998807907104, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[0, 6], [6, 5], [5, 4], [4, 3], [3, 2], [2, 1], [12, 11], [11, 10], [10, 9], [9, 8], [8, 7], [7, 0], [1, 13], [13, 14], [14, 15], [15, 16], [16, 17], [17, 18], [18, 12]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(11, 10, 9, 8, 7, 0, 6, 5, 4, 3, 2, 1, 13, 14, 15, 16, 17, 18, 12)]
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
    self.layout.operator(Cornice.bl_idname, text="Cornice", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
