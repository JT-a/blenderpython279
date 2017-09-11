bl_info = {
    "name": "Car",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Car primitive.",
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


class Car(bpy.types.Operator):
    bl_idname = "mesh.car"
    bl_label = "Car"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Car primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Car")
        obj = bpy.data.objects.new(name="Car", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)

        idxlist = []
        vertlist = [(0.318389892578125, 1.0, 0.0), (-1.0, -0.5971899628639221, 0.0), (-1.18287193775177, -0.6410936117172241, 0.0), (-1.3258801698684692, -0.7632342576980591, 0.0), (-1.397850751876831, -0.9369865655899048, 0.0), (-1.3830950260162354, -1.124475121498108, 0.0), (-1.2848296165466309, -1.2848297357559204, 0.0), (-1.124475121498108, -1.3830950260162354, 0.0), (-0.9369868040084839, -1.397850751876831, 0.0), (-0.7632343173027039, -1.3258802890777588, 0.0), (-0.6410936117172241, -1.18287193775177, 0.0), (-0.5971899628639221, -0.9999999403953552, 0.0), (0.5971899628639221, -1.0, 0.0), (0.6410936117172241, -1.18287193775177, 0.0), (0.7632342576980591, -1.3258801698684692, 0.0), (0.9369865655899048, -1.397850751876831, 0.0), (1.124475121498108, -1.3830950260162354, 0.0), (1.2848297357559204, -1.2848296165466309, 0.0), (1.3830950260162354, -1.124475121498108, 0.0), (1.397850751876831, -0.9369866251945496, 0.0), (1.3258802890777588, -0.7632343173027039, 0.0), (1.18287193775177, -0.6410936117172241, 0.0), (0.9999999403953552, -0.5971899628639221, 0.0), (-0.34839022159576416, 1.0, 0.0), (-0.3564126491546631, 0.8980657458305359, 0.0), (-0.38028228282928467, 0.798641562461853, 0.0), (-0.41941142082214355, 0.7041753530502319, 0.0), (-0.47283661365509033, 0.6169934272766113, 0.0), (-0.5392423868179321, 0.5392422676086426, 0.0), (-0.6169934272766113, 0.47283655405044556, 0.0), (-0.7041752338409424, 0.4194115400314331, 0.0), (-0.7986413836479187, 0.38028228282928467, 0.0), (-0.8980656862258911, 0.3564126491546631, 0.0), (-0.9999999403953552, 0.34839022159576416, 0.0), (1.0, 0.05357992649078369, 0.0), (1.187248945236206, 0.13114100694656372, 0.0), (1.2648100852966309, 0.3183899223804474, 0.0), (1.187248945236206, 0.5056389570236206, 0.0), (1.0, 0.5831999778747559, 0.0), (0.812751054763794, 0.5056389570236206, 0.0)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[11, 10], [10, 9], [9, 8], [8, 7], [7, 6], [6, 5], [5, 4], [4, 3], [3, 2], [2, 1], [22, 21], [21, 20], [20, 19], [19, 18], [18, 17], [17, 16], [16, 15], [15, 14], [14, 13], [13, 12], [12, 11], [0, 23], [23, 24], [24, 25], [25, 26], [26, 27], [27, 28], [28, 29], [29, 30], [30, 31], [31, 32], [32, 33], [33, 1], [0, 39], [39, 38], [38, 37], [37, 36], [36, 35], [35, 34], [34, 22]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 0, 39, 38, 37, 36, 35, 34, 22)]
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
    self.layout.operator(Car.bl_idname, text="Car", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
