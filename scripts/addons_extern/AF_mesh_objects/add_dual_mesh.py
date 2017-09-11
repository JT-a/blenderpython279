# Blender plugin for generating the dual of a mesh
# See README for more information
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Adam Newgas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
'''
bl_info = {
    "name": "Add Dual Mesh",
    "description": "Constructs a mesh replacing vertices with faces and visa versa",
    "author": "Adam Newgas",
    "version": (1, 0, 0),
    "blender": (2, 74, 0),
    "location": "",
    "warning": "",
    "wiki_url": "https://github.com/BorisTheBrave/add_dual_mesh",
    "category": "Add Mesh"}
'''
import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper, object_data_add


def is_boundary(edge):
    return len(edge.link_loops) == 1


def edge_midpoint(edge):
    return (edge.verts[0].co + edge.verts[1].co) / 2


def make_dual_bmesh(bm_orig, preserve_boundary):
    bm = bmesh.new()

    # Create a vertex for every face
    face_to_vert = []
    for face in bm_orig.faces:
        face_to_vert.append(bm.verts.new(face.calc_center_median()))
    # Extra vertex for each non manifold edge
    edge_to_vert = {}
    for edge in bm_orig.edges:
        if is_boundary(edge):
            midpoint = edge_midpoint(edge)
            vert = bm.verts.new(midpoint)
            edge_to_vert[edge.index] = vert
    for vert in bm_orig.verts:
        if not vert.is_manifold:
            continue
        has_boundarys = any(is_boundary(loop.edge) for loop in vert.link_loops)
        if has_boundarys:
            # Copy up this vertex itself into new mesh
            if preserve_boundary:
                vert_vert = bm.verts.new(vert.co)
            for l in vert.link_loops:
                if not is_boundary(l.edge):
                    continue
                new_verts = []
                if preserve_boundary:
                    new_verts.append(vert_vert)
                new_verts.append(edge_to_vert[l.edge.index])
                new_verts.append(face_to_vert[l.face.index])
                while True:
                    l = l.link_loop_prev.link_loop_radial_next
                    if is_boundary(l.edge):
                        new_verts.append(edge_to_vert[l.edge.index])
                        break
                    else:
                        assert l.vert == vert
                        next_face = l.face.index
                        new_verts.append(face_to_vert[next_face])
                bm.faces.new(new_verts)
        else:
            new_verts = []
            l = vert.link_loops[0]
            first_face = l.face.index
            while True:
                l = l.link_loop_prev.link_loop_radial_next
                assert l.vert == vert
                next_face = l.face.index
                new_verts.append(face_to_vert[next_face])
                if next_face == first_face:
                    break
            if len(new_verts) >= 3:
                bm.faces.new(new_verts)
    return bm


def make_dual_bmesh_blend(bm_orig, blend_factor, preserve_boundary, bm, sk):
    loop_to_vert = []
    # Create a vertex for every loop
    for face in bm_orig.faces:
        face_center = face.calc_center_median()
        for loop in face.loops:
            v = face_center * blend_factor + loop.vert.co * (1 - blend_factor)
            vert = bm.verts.new(v)
            if sk:
                vert[sk] = face_center
            loop_to_vert.append(vert)
    # Create two vertices for every boundary
    edge_to_verts = {}
    for edge in bm_orig.edges:
        if not is_boundary(edge):
            continue
        midpoint = edge_midpoint(edge)
        edge_to_verts[edge.index] = [
            bm.verts.new(midpoint * blend_factor + v.co * (1 - blend_factor))
            for v in edge.verts]
        if sk:
            for vert in edge_to_verts[edge.index]:
                vert[sk] = midpoint

    # Connect face verts to loop verts
    for face in bm_orig.faces:
        new_verts = []
        for loop in face.loops:
            new_verts.append(loop_to_vert[loop.index])
        face = bm.faces.new(new_verts)
        face.material_index = 0
    # Connect the 4 loop verts around an edge
    for edge in bm_orig.edges:
        if len(edge.link_loops) == 1:
            loop1 = edge.link_loops[0]
            loop1p = loop1.link_loop_next
            ev1, ev2 = edge_to_verts[edge.index]
            if edge.verts[1] == loop1.vert:
                ev1, ev2 = ev2, ev1
            face = bm.faces.new([loop_to_vert[loop1p.index],
                                 loop_to_vert[loop1.index],
                                 ev1,
                                 ev2])

        elif len(edge.link_loops) == 2:
            loop1, loop2 = edge.link_loops
            loop1p = loop1.link_loop_next
            loop2p = loop2.link_loop_next
            face = bm.faces.new([loop_to_vert[loop.index]
                                 for loop in [loop2p, loop2, loop1p, loop1]])
        face.material_index = 1
    # And a face for each vertex
    for vert in bm_orig.verts:
        if not vert.is_manifold:
            continue
        has_boundarys = any(is_boundary(loop.edge) for loop in vert.link_loops)
        if has_boundarys:
            # Copy up this vertex itself into new mesh
            if preserve_boundary:
                vert_vert = bm.verts.new(vert.co)
            for l in vert.link_loops:
                if not is_boundary(l.edge):
                    continue
                new_verts = []
                if preserve_boundary:
                    new_verts.append(vert_vert)
                ev1, ev2 = edge_to_verts[l.edge.index]
                new_verts.append(ev1 if l.edge.verts[0] == vert else ev2)
                new_verts.append(loop_to_vert[l.index])
                while True:
                    l = l.link_loop_prev.link_loop_radial_next
                    if is_boundary(l.edge):
                        ev1, ev2 = edge_to_verts[l.edge.index]
                        new_verts.append(ev1 if l.edge.verts[0] == vert else ev2)
                        break
                    else:
                        assert l.vert == vert
                        new_verts.append(loop_to_vert[l.index])
                face = bm.faces.new(new_verts)
                face.material_index = 2
        else:
            new_verts = []
            l = vert.link_loops[0]
            first_loop = l
            while True:
                l = l.link_loop_prev.link_loop_radial_next
                assert l.vert == vert
                new_verts.append(loop_to_vert[l.index])
                if l == first_loop:
                    break
            if len(new_verts) >= 3:
                face = bm.faces.new(new_verts)
                face.material_index = 2


class AddDualMeshOperator(bpy.types.Operator, AddObjectHelper):
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "object.dual_mesh_operator"
    bl_label = "Add Dual Mesh"

    preserve_boundary = bpy.props.BoolProperty(
        name="Preserve Boundary",
        description="Keeps boundary edges unchanged")

    use_blending = bpy.props.BoolProperty(
        name="Use Blending",
        description="Generate extra geometry to blend between original and dual mesh")

    blend_factor = bpy.props.FloatProperty(
        name="Blending Factor",
        description="Similarity to dual mesh, from original mesh",
        default=0.5, min=0, max=1)

    use_shape_keys = bpy.props.BoolProperty(
        name="Use Shape Keys",
        description="Perform the blending using Shape Keys")

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ((ob is not None) and
                (ob.mode == "OBJECT") and
                (ob.type == "MESH") and
                (context.mode == "OBJECT"))

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preserve_boundary")
        layout.prop(self, "use_blending")
        col = layout.column()
        col.enabled = self.use_blending
        col.prop(self, "blend_factor")
        col.prop(self, "use_shape_keys")

    def execute(self, context):
        orig_obj = obj = context.active_object
        bm_orig = bmesh.new()
        bm_orig.from_mesh(orig_obj.data)

        mesh = bpy.data.meshes.new(orig_obj.name + ".Dual")
        from bpy_extras import object_utils
        obj = object_utils.object_data_add(context, mesh, operator=None).object

        if not self.use_blending:
            bm = make_dual_bmesh(bm_orig, self.preserve_boundary)
        else:
            mat = bpy.data.materials.new("Faces")
            mat.diffuse_color = (1, 0, 0)
            obj.data.materials.append(mat)
            mat = bpy.data.materials.new("Edges")
            mat.diffuse_color = (0, 1, 0)
            obj.data.materials.append(mat)
            mat = bpy.data.materials.new("Vertices")
            mat.diffuse_color = (0, 0, 1)
            obj.data.materials.append(mat)
            if self.use_shape_keys:
                blend_factor = 0
                obj.shape_key_add("Orig")
                obj.data.shape_keys.use_relative = False
                obj.data.shape_keys.eval_time = self.blend_factor * 10
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                layer = bm.verts.layers.shape.new("Dual")
            else:
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                blend_factor = self.blend_factor
                layer = None
            make_dual_bmesh_blend(bm_orig,
                                  blend_factor,
                                  self.preserve_boundary,
                                  bm,
                                  layer)

        bm.to_mesh(mesh)
        if self.use_blending and self.use_shape_keys:
            obj.data.shape_keys.key_blocks["Orig"].interpolation = "KEY_LINEAR"
            obj.data.shape_keys.key_blocks["Dual"].interpolation = "KEY_LINEAR"

        return {'FINISHED'}
'''
def menu_func(self, context):
    self.layout.operator(AddDualMeshOperator.bl_idname,
                        text="Duel Mesh", icon="PLUGIN")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
	
if __name__ == "__main__":
    register()
'''
