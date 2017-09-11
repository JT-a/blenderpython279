# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#
# ***** END GPL LICENCE BLOCK *****


import bpy
import bmesh
import mathutils
import math

# bl_info = {
#    "name": "Faces Along Normals",
#    "description": "Move faces along individual normals.",
#    "author": "Márcio Daniel da Rosa",
#    "version": (1, 1),
#    "blender": (2, 73, 0),
#    "location": "3D View (Edit Mode) > Specials menu (W key) > Move Faces Along Normals",
#    "warning": "",
#    "category": "Mesh"}

# Operator to move the faces. It first calculates a new position for each vertex of the face, for all
# selected faces. So, if a vertex is shared with more than one selected face, it will have more than
# one calculated position. So, the final position is calculated given a list of calculated positions
# for that vertex.


class MoveFacesAlongNormalsOperator(bpy.types.Operator):
    '''Move the faces along individual normal vectors.'''
    bl_idname = "fan.move_faces_along_normals_operator"
    bl_label = "Move Faces Along Normals"
    bl_options = {'REGISTER', 'UNDO'}

    distance = bpy.props.FloatProperty(name="Distance", subtype='DISTANCE', step=1, precision=3)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.object.mode == 'EDIT'

    # Executes the translation for each selected face. If no faces are affected, then translate all faces.
    def execute(self, context):
        if self.distance != 0:
            bm = bmesh.from_edit_mesh(context.object.data)
            some_face_was_affected = self.translate_faces(bm, True)
            if not some_face_was_affected:
                self.translate_faces(bm, False)
            bm.normal_update()
            context.area.tag_redraw()
        return {'FINISHED'}

    # Move the faces. Input: the bmesh and a flag to define if only the selected faces must be translated,
    # or all faces must be translated. Output: True if some face was translated, false if not.
    def translate_faces(self, mesh, selected_faces_only):
        some_face_was_affected = False
        calculated_translations_by_vertex_index = dict()
        for face in mesh.faces:
            if face.select or not selected_faces_only:
                self.calculate_translations_for_face_verts(calculated_translations_by_vertex_index, face)
                some_face_was_affected = True
        self.translate_verts(mesh, calculated_translations_by_vertex_index)
        return some_face_was_affected

    # Calculate the translation for each vertex in the face, along the face normal. Input: the dict where
    # the translation vector will be stored by the vertex index and the face.
    def calculate_translations_for_face_verts(self, results_dict, face):
        for vertex in face.verts:
            translation = mathutils.Vector()
            translation.x = face.normal.x * self.distance
            translation.y = face.normal.y * self.distance
            translation.z = face.normal.z * self.distance
            if vertex.index in results_dict:
                results_dict[vertex.index].append(translation)
            else:
                results_dict[vertex.index] = [translation]

    # Calculates the position for each vertex and updates the coordinates. Input: the bmesh and the dictionary
    # with the calculated translations for the vertices.
    def translate_verts(self, mesh, translations_by_vertex_index):
        mesh.verts.ensure_lookup_table()
        for vertex_index in translations_by_vertex_index.keys():
            vertex = mesh.verts[vertex_index]
            translations = translations_by_vertex_index[vertex_index]
            sum = self.sum_points(translations)
            cathetus = self.distance
            angle = sum.angle(translations[0])
            h = cathetus / math.cos(angle)
            sum.length = abs(h)
            vertex.co += sum

    # input: list of coordinates, output: a coordinate, the sum of the input coordinates
    def sum_points(self, coordinates):
        final_coordinate = mathutils.Vector((0, 0, 0))
        for co in coordinates:
            final_coordinate += co
        return final_coordinate

# Draws the operator in the specials menu


def specials_menu_draw(self, context):
    self.layout.operator("fan.move_faces_along_normals_operator")

# Draws the operator in the faces menu


def faces_menu_draw(self, context):
    self.layout.separator()
    self.layout.operator("fan.move_faces_along_normals_operator")


def register():
    bpy.utils.register_class(MoveFacesAlongNormalsOperator)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(specials_menu_draw)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(faces_menu_draw)


def unregister():
    bpy.utils.unregister_class(MoveFacesAlongNormalsOperator)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(specials_menu_draw)
    bpy.types.VIEW3D_MT_edit_mesh_faces.remove(faces_menu_draw)

if __name__ == "__main__":
    register()
