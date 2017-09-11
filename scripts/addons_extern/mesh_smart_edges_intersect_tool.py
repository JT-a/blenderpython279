bl_info = {
    'name': "Smart two edges intersect tool (cad VTX)",
    'author': "luxuy blendercn",
    'version': (1, 0, 0),
    'blender': (2, 70, 0),
    'location': 'View3D > EditMode > (w) Specials',
    'warning': "",
    'category': 'Mesh'}

import bpy
import bmesh
from math import *
from mathutils import Matrix, Vector
from bpy.props import FloatProperty, IntProperty, BoolProperty, EnumProperty, StringProperty
from mathutils.geometry import *


def pt_in_line(pt, line):
    vec1 = pt - line[0]
    vec2 = pt - line[1]

    k = vec1.cross(vec2)
    print("---------", k.length)
    if k.length < 10e-4:
        # 共线
        m = vec1.dot(vec2)
        if m == 0:
            return 1

        if m > 0:
            return "out"
        else:
            return "in"
    else:
        return None


class CurToIntersect(bpy.types.Operator):
    bl_idname = "bpt.smart_vtx"
    bl_label = "Smart 2 edges intersect(auto vtx)"

    bl_options = {'REGISTER', 'UNDO'}
    flag = BoolProperty(name="Force to co planar", default=True)

    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'EDIT_MESH':
            return True
        return False

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')

        context.tool_settings.mesh_select_mode = (False, True, True)

        ob = context.object
        me = ob.data

        bm = bmesh.new()

        bm.from_mesh(ob.data)
        # bmesh.from_edit_mesh(me)
        mw = ob.matrix_world
        bpy.ops.object.mode_set(mode='OBJECT')

        sel_edges = []
        for e in ob.data.edges:
            if e.select:
                sel_edges.append(e)
        if len(sel_edges) != 2:
            msg = "Must select only 2 edges !"
            self.report({"INFO"}, msg)
            bpy.ops.object.mode_set(mode='EDIT')
            return {"FINISHED"}
        bm.edges.ensure_lookup_table()
        e1 = bm.edges[sel_edges[0].index]
        e2 = bm.edges[sel_edges[1].index]

        pts = intersect_line_line(e1.verts[0].co, e1.verts[1].co, e2.verts[0].co, e2.verts[1].co)

        if (pts[0] - pts[1]).length > 10e-4:
            bpy.ops.object.editmode_toggle()

            if self.flag:
                msg = "No coplanar, but changed to co-planar now!"

                save = context.space_data.transform_orientation, context.space_data.pivot_point
                context.space_data.transform_orientation = 'VIEW'
                context.space_data.pivot_point = 'ACTIVE_ELEMENT'
                bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='VIEW')

                context.space_data.transform_orientation, context.space_data.pivot_point = save
                self.execute(context)
            else:
                msg = "No coplanar!"

            self.report({"INFO"}, msg)

        else:
            self.execute(context)

        return {"FINISHED"}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        ob = context.object
        me = ob.data

        bm = bmesh.new()

        bm.from_mesh(ob.data)
        # bmesh.from_edit_mesh(me)
        mw = ob.matrix_world
        bpy.ops.object.mode_set(mode='OBJECT')

        sel_edges = []
        for e in ob.data.edges:
            if e.select:
                sel_edges.append(e)
        bm.edges.ensure_lookup_table()
        e1 = bm.edges[sel_edges[0].index]
        e2 = bm.edges[sel_edges[1].index]

        pts = intersect_line_line(e1.verts[0].co, e1.verts[1].co, e2.verts[0].co, e2.verts[1].co)

        if (pts[0] - pts[1]).length > 10e-4:
            bpy.ops.object.editmode_toggle()
            return {'FINISHED'}

        # context.scene.cursor_location=mw*pts[0]
        line1 = [v.co for v in e1.verts]
        line2 = [v.co for v in e2.verts]
        s1 = pt_in_line(pts[0], line1)
        s2 = pt_in_line(pts[1], line2)
        print(s1, s2)
        edges = []
        if s1 == 'in':
            edges.append(e1)
        if s2 == 'in':
            edges.append(e2)
        print(edges)

        bm.verts.index_update()
        bm.edges.index_update()
        bmesh.ops.subdivide_edges(bm, edges=edges, cuts=1)

        if len(edges) == 1:
            bm.verts.ensure_lookup_table()
            bm.verts[-1].co = pts[0]
            if s1 == 'in':
                print("---")

                if (e2.verts[0].co - pts[0]).length > (e2.verts[1].co - pts[0]).length:
                    # v4.co=pts[0]
                    if len(e2.verts[1].link_edges) == 1:  # 自由端
                        print("free")
                        e2.verts[1].co = pts[0]
                        if len(set(e1.link_faces) & set(e2.verts[0].link_faces)) > 0:
                            print("ok")
                            v = e2.verts[0]
                            bmesh.ops.delete(bm, geom=[e2.verts[1]], context=1)

                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1], v])
                    else:
                        if len(set(e1.link_faces) & set(e2.verts[1].link_faces)) > 0:

                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1], e2.verts[1]])
                        else:
                            bm.edges.new([bm.verts[-1], e2.verts[1]])
                else:
                    if len(e2.verts[0].link_edges) == 1:  # 自由端
                        print("free")
                        e2.verts[0].co = pts[0]
                        if len(set(e1.link_faces) & set(e2.verts[1].link_faces)) > 0:
                            print("ok")
                            v = e2.verts[1]
                            bmesh.ops.delete(bm, geom=[e2.verts[0]], context=1)

                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1], v])
                    else:
                        if len(set(e1.link_faces) & set(e2.verts[0].link_faces)) > 0:

                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1], e2.verts[0]])
                        else:
                            bm.edges.new([bm.verts[-1], e2.verts[0]])
            else:
                if (e1.verts[0].co - pts[0]).length > (e1.verts[1].co - pts[0]).length:
                    # v4.co=pts[0]
                    if len(e1.verts[1].link_edges) == 1:  # 自由端
                        print("free")
                        e1.verts[1].co = pts[0]
                        if len(set(e2.link_faces) & set(e1.verts[0].link_faces)) > 0:
                            print("ok")
                            v = e1.verts[0]
                            bmesh.ops.delete(bm, geom=[e1.verts[1]], context=1)

                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1], v])
                    else:
                        if len(set(e2.link_faces) & set(e1.verts[1].link_faces)) > 0:

                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1], e1.verts[1]])
                        else:
                            bm.edges.new([bm.verts[-1], e1.verts[1]])
                else:
                    # v3.co=pts[0]
                    if len(e1.verts[0].link_edges) == 1:  # 自由端
                        print("free")
                        e1.verts[0].co = pts[0]
                        if len(set(e2.link_faces) & set(e1.verts[1].link_faces)) > 0:
                            print("ok")
                            v = e1.verts[1]
                            bmesh.ops.delete(bm, geom=[e1.verts[0]], context=1)

                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1], v])
                    else:

                        if len(set(e2.link_faces) & set(e1.verts[0].link_faces)) > 0:

                            bmesh.ops.connect_verts(bm, verts=[bm.verts[-1], e1.verts[0]])
                        else:
                            bm.edges.new([bm.verts[-1], e1.verts[0]])

        if len(edges) == 2:
            bm.verts.ensure_lookup_table()
            bm.verts[-1].co = pts[0]
            bm.verts[-2].co = pts[0]
        if len(edges) == 0:
            print("\n" * 10)
            bm.verts.new(pts[0])
            if (e1.verts[0].co - pts[0]).length > (e1.verts[1].co - pts[0]).length:
                # v4.co=pts[0]
                if len(e1.verts[1].link_edges) == 1:  # 自由端

                    e1.verts[1].co = pts[0]
                else:

                    bm.edges.new([bm.verts[-1], e1.verts[1]])
            else:
                if len(e1.verts[0].link_edges) == 1:  # 自由端
                    e1.verts[0].co = pts[0]
                else:
                    bm.edges.new([bm.verts[-1], e1.verts[0]])

            if (e2.verts[0].co - pts[0]).length > (e2.verts[1].co - pts[0]).length:
                    # v4.co=pts[0]
                if len(e2.verts[1].link_edges) == 1:  # 自由端

                    e2.verts[1].co = pts[0]
                else:

                    bm.edges.new([bm.verts[-1], e2.verts[1]])
            else:
                if len(e2.verts[0].link_edges) == 1:  # 自由端
                    e2.verts[0].co = pts[0]
                else:
                    bm.edges.new([bm.verts[-1], e2.verts[0]])

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
        bm.to_mesh(ob.data)
        bpy.ops.object.editmode_toggle()
        # bmesh.update_edit_mesh(me, tessface=True, destructive=True)
        bm.free()

        # bpy.ops.mesh.remove_doubles()

        return {'FINISHED'}
#---------------------------------------------


def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator('bpt.smart_vtx')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)

if __name__ == "__main__":
    register()
