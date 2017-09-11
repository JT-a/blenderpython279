bl_info = {
    "name": "Smooth",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 3),
    "location": "Add > Mesh",
    "description": "Create Smooth primitive.",
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


class Smooth(bpy.types.Operator):
    bl_idname = "mesh.smooth"
    bl_label = "Smooth"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "add Smooth primitive"

    def invoke(self, context, event):

        mesh = bpy.data.meshes.new(name="Smooth")
        obj = bpy.data.objects.new(name="Smooth", object_data=mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        obj.location = scene.cursor_location
        bm = bmesh.new()
        bm.from_mesh(mesh)
        idxlist = []
        vertlist = [(0.9736814498901367, -0.9802608489990234, 0.0), (-1.0263185501098633, -0.9802608489990234, 0.0), (-1.0263185501098633, 1.0197391510009766, 0.0), (-0.010030746459960938, 0.03312969207763672, 1.2079226507921703e-13), (-1.010030746459961, 1.0199980735778809, 1.0658141036401503e-13), (-0.9610872864723206, 0.7241128087043762, 1.0727693961019164e-13), (-0.819047749042511, 0.4453444480895996, 1.0929543945228937e-13), (-0.5978158712387085, 0.2241126298904419, 1.1243933437316347e-13), (-0.3190479278564453, 0.08207321166992188, 1.1640086680989037e-13), (-0.0100308358669281, 0.03312969207763672, 1.2079226507921703e-13), (0.0010576248168945312, 0.022419452667236328, 1.0658141036401503e-13), (0.9740920066833496, -0.9775805473327637, 1.2079226507921703e-13), (0.9521141052246094, -0.6685634851455688, 1.2009673583304042e-13), (0.8100746870040894, -0.38979536294937134, 1.180782359909427e-13), (0.5888428092002869, -0.16856354475021362, 1.14934334293805e-13), (0.31007444858551025, -0.026523947715759277, 1.1097280185707811e-13), (0.0010578334331512451, 0.022419452667236328, 1.0658141036401503e-13)]
        for co in vertlist:
            v = bm.verts.new(co)
            bm.verts.index_update()
            idxlist.append(v.index)
        edgelist = [[0, 1], [2, 1], [2, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 3], [10, 16], [16, 15], [15, 14], [14, 13], [13, 12], [12, 11], [0, 11], [3, 10]]
        for verts in edgelist:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))
        facelist = [(11, 0, 1, 2, 4, 5, 6, 7, 8, 9, 3, 10, 16, 15, 14, 13, 12)]
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
    self.layout.operator(Smooth.bl_idname, text="Smooth", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
