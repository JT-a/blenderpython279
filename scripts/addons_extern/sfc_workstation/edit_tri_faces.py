# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Triangle Faces",
    "author": "MKB",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Editmode > Extrude Menu > ALT+E",
    "description": "Triangle Faces into the Extrude Menu",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}


import bpy


class TriangleFaces(bpy.types.Operator):
    """Close selected face with triangle"""
    bl_idname = "mesh.tri_faces"
    bl_label = "Triangle Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.inset(use_boundary=False, thickness=1)
        bpy.ops.mesh.merge(type='CENTER')
        return {'FINISHED'}


def operator_draw(self, context):
    layout = self.layout
    col = layout.column(align=True)
    col.operator("mesh.tri_faces", text="Triangle Faces")


def register():
    bpy.utils.register_class(TriangleFaces)
    bpy.types.VIEW3D_MT_edit_mesh_extrude.append(operator_draw)


def unregister():
    bpy.utils.unregister_class(TriangleFaces)
    bpy.types.VIEW3D_MT_edit_mesh_extrude.remove(operator_draw)


if __name__ == "__main__":
    register()
