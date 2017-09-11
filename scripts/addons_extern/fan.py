import bpy
import bmesh
import mathutils
import math

bl_info = {
    "name": "Move Along Normals",
    "description": "Move vertices, edges or faces along individual normals.",
    "author": "Márcio Daniel da Rosa",
    "version": (1, 4),
    "blender": (2, 73, 0),
    "location": "3D View (Edit Mode) > Specials menu (W key) > Move Along Normals",
    "warning": "",
    "category": "Mesh"}

# Operator to move the vertices, edges or normals. It first calculates a new position for each selected
# vertex. If a vertex is shared with more than one selected face or edge, it will have more than
# one calculated position. Then, the final position is calculated given a list of calculated positions
# for that vertex.
class MoveFacesAlongNormalsOperator(bpy.types.Operator):
    '''Move the vertices, edges or faces along individual normal vectors.'''
    bl_idname = "fan.move_faces_along_normals_operator"
    bl_label = "Move Along Normals"
    bl_options = {'REGISTER', 'UNDO'}
    
    distance = bpy.props.FloatProperty(name="Distance", subtype='DISTANCE', step=1, precision=3)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.object.mode == 'EDIT'

    def execute(self, context):
        if self.distance != 0:
            mesh = bmesh.from_edit_mesh(context.object.data)
            self.translate_verts(mesh)
            mesh.normal_update()
            context.area.tag_redraw()
        return {'FINISHED'}

    def is_vertex_connected_to_a_selected_edge(self, vertex):
        for edge in vertex.link_edges:
            if edge.select:
                return True
        return False

    def is_edge_connected_to_a_selected_face(self, edge):
        for face in edge.link_faces:
            if face.select:
                return True
        return False

    def calculate_edge_normal(self, edge):
        result = mathutils.Vector((0, 0, 0))
        for face in edge.link_faces:
            result += face.normal
        return result.normalized()

    def add_normal_to_direction(self, normal, direction):
        direction += normal * self.distance
        angle = direction.angle(normal)
        cathetus = self.distance
        hypotenuse = cathetus / math.cos(angle)
        return direction.normalized() * hypotenuse

    # Updates the positions of the selected vertices. Input: the bmesh.
    def translate_verts(self, mesh):
        mesh.verts.ensure_lookup_table()
        for vertex in mesh.verts:
            if vertex.select:
                direction = mathutils.Vector((0, 0, 0))
                if self.is_vertex_connected_to_a_selected_edge(vertex):
                    for face in vertex.link_faces:
                        if face.select:
                            direction = self.add_normal_to_direction(face.normal, direction)
                    for edge in vertex.link_edges:
                        if edge.select and not self.is_edge_connected_to_a_selected_face(edge):
                            edge_normal = self.calculate_edge_normal(edge)
                            if edge_normal.length > 0:
                                direction = self.add_normal_to_direction(edge_normal, direction)
                else:
                    direction = vertex.normal * self.distance
                vertex.co += direction
    
# Draws the operator in the specials menu
def specials_menu_draw(self, context):
    self.layout.operator("fan.move_faces_along_normals_operator")

def register():
    bpy.utils.register_class(MoveFacesAlongNormalsOperator)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(specials_menu_draw)

def unregister():
    bpy.utils.unregister_class(MoveFacesAlongNormalsOperator)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(specials_menu_draw)
    
if __name__ == "__main__":
    register()