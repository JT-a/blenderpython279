# -*- coding: utf-8 -*-

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
# ***** END GPL LICENCE BLOCK *****

# ------ ------
bl_info = {
    'name': 'extrude_along_path',
    'author': '',
    'version': (0, 2, 6),
    'blender': (2, 6, 5),
    'api': 53207,
    'location': 'View3D > Tool Shelf',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Mesh'}

# ------ ------
import bpy
import bmesh
from mathutils.geometry import intersect_line_plane, intersect_point_line
from bpy.props import BoolProperty, PointerProperty
from math import degrees

# ------ ------


def edit_mode_out():
    bpy.ops.object.mode_set(mode='OBJECT')


def edit_mode_in():
    bpy.ops.object.mode_set(mode='EDIT')


def get_adj_v_(list_):
    tmp = {}
    for i in list_:
        try:
            tmp[i[0]].append(i[1])
        except KeyError:
            tmp[i[0]] = [i[1]]
        try:
            tmp[i[1]].append(i[0])
        except KeyError:
            tmp[i[1]] = [i[0]]
    return tmp


def f_1(frst, list_, last):      # edge chain
    fi = frst
    tmp = [frst]
    while list_ != []:
        for i in list_:
            if i[0] == fi:
                tmp.append(i[1])
                fi = i[1]
                list_.remove(i)
            elif i[1] == fi:
                tmp.append(i[0])
                fi = i[0]
                list_.remove(i)
        if tmp[-1] == last:
            break
    return tmp


def f_2(frst, list_):      # edge loop
    fi = frst
    tmp = [frst]
    while list_ != []:
        for i in list_:
            if i[0] == fi:
                tmp.append(i[1])
                fi = i[1]
                list_.remove(i)
            elif i[1] == fi:
                tmp.append(i[0])
                fi = i[0]
                list_.remove(i)
        if tmp[-1] == frst:
            break
    return tmp


def is_loop_(list_fl):
    return True if len(list_fl) == 0 else False


def e_no_(bme, indx, p, p1):
    tmp1 = (bme.verts[indx].co).copy()
    tmp1[0] += 0.1
    tmp1[1] += 0.1
    tmp1[2] += 0.1
    ip1 = intersect_point_line(tmp1, p, p1)[0]
    return tmp1 - ip1


def get_lc_(bme, list_eks):
    list_ = [set(ek) for ek in list_eks]
    n = len(list_)
    count = 0
    while count < n:
        ek = list_[count]
        for i in range(count + 1, n):
            s = list_[i]
            if s and not ek.isdisjoint(s):
                ek.update(s)
                s.clear()
                break
        else:
            count += 1
    return{i: [ek for ek in list_eks if not s.isdisjoint(ek)] for i, s in enumerate((s for s in list_ if s))}

# ------ ------


def f_(bme, dict_0, list_fl, loop, list_2, list_1):

    n1 = len(list_2)

    list_3 = list_2[:]

    dict_1 = {}
    for k in list_2:
        dict_1[k] = [k]

    n = len(list_1)
    for i in range(n):
        p = (bme.verts[list_1[i]].co).copy()
        p1 = (bme.verts[list_1[(i - 1) % n]].co).copy()
        p2 = (bme.verts[list_1[(i + 1) % n]].co).copy()
        vec1 = p - p1
        vec2 = p - p2
        ang = vec1.angle(vec2, any)

        if round(degrees(ang)) == 180.0 or round(degrees(ang)) == 0.0:
            pp = p - ((e_no_(bme, list_1[i], p, p1)).normalized() * 0.1)
            pn = vec1.normalized()
        else:
            pp = ((p - (vec1.normalized() * 0.1)) + (p - (vec2.normalized() * 0.1))) * 0.5
            pn = ((vec1.cross(vec2)).cross(p - pp)).normalized()

        if loop:      # loop
            if i == 0:
                pass
            else:
                for j in range(n1):
                    v = (bme.verts[list_3[j]].co).copy()
                    bme.verts.new(intersect_line_plane(v, v + (vec1.normalized() * 0.1), pp, pn))
                    bme.verts.index_update()
                    list_3[j] = bme.verts[-1].index
                    dict_1[list_2[j]].append(bme.verts[-1].index)

        else:      # path
            if i == 0:
                pass
            elif i == (n - 1):
                pp_ = p - ((e_no_(bme, list_fl[1] if eap_buf.list_sp[0] == list_fl[0] else list_fl[0], p, p1)).normalized() * 0.1)
                pn_ = vec1.normalized()
                for j in range(n1):
                    v = (bme.verts[list_3[j]].co).copy()
                    bme.verts.new(intersect_line_plane(v, v + (vec1.normalized() * 0.1), pp_, pn_))
                    bme.verts.index_update()
                    dict_1[list_2[j]].append(bme.verts[-1].index)
            else:
                for j in range(n1):
                    v = (bme.verts[list_3[j]].co).copy()
                    bme.verts.new(intersect_line_plane(v, v + (vec1.normalized() * 0.1), pp, pn))
                    bme.verts.index_update()
                    list_3[j] = bme.verts[-1].index
                    dict_1[list_2[j]].append(bme.verts[-1].index)

    # -- -- -- --
    list_4 = [[v.index for v in e.verts] for e in bme.edges if e.select and e.is_valid]
    n2 = len(list_4)

    for t in range(n2):
        for o in range(n if loop else (n - 1)):
            bme.faces.new([bme.verts[dict_1[list_4[t][0]][o]], bme.verts[dict_1[list_4[t][1]][o]], bme.verts[dict_1[list_4[t][1]][(o + 1) % n]], bme.verts[dict_1[list_4[t][0]][(o + 1) % n]]])
            bme.faces.index_update()

# ------ ------


class eap_p_group0(bpy.types.PropertyGroup):
    b = BoolProperty(name='', default=False)

# ------ ------


class eap_buf():
    list_ek = []      # path
    list_sp = []      # start point

# ------ panel 0 ------


class eap_p0(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_label = 'Extrude Along Path'
    bl_context = 'mesh_edit'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.split(0.60, align=True)
        row.label('Start point:')
        row.operator('eap.op1_id', text='Store')
        row1 = box.split(0.60, align=True)
        row1.label('Path:')
        row1.operator('eap.op0_id', text='Store')
        # box.prop(context.scene.eap_custom_props, 'b', text = 'Delete path')
        row2 = layout.split(0.80, align=False)
        row2.operator('eap.op2_id', text='Extrude')
        row2.operator('eap.op3_id', text='?')

# ------ operator 0 ------


class eap_op0(bpy.types.Operator):
    bl_idname = 'eap.op0_id'
    bl_label = '....'
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        edit_mode_out()
        ob_act = context.active_object
        bme = bmesh.new()
        bme.from_mesh(ob_act.data)
        eap_buf.list_ek[:] = []
        for e in bme.edges:
            if e.select and e.is_valid:
                eap_buf.list_ek.append([v.index for v in e.verts])
                e.select_set(0)
        bme.to_mesh(ob_act.data)
        edit_mode_in()
        return {'FINISHED'}

# ------ operator 1 ------


class eap_op1(bpy.types.Operator):
    bl_idname = 'eap.op1_id'
    bl_label = '....'
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        edit_mode_out()
        ob_act = context.active_object
        bme = bmesh.new()
        bme.from_mesh(ob_act.data)
        eap_buf.list_sp[:] = []
        for v in bme.verts:
            if v.select and v.is_valid:
                eap_buf.list_sp.append(v.index)
                v.select_set(0)
        bme.to_mesh(ob_act.data)
        edit_mode_in()
        return {'FINISHED'}

# ------ operator 2 ------


class eap_op2(bpy.types.Operator):
    bl_idname = 'eap.op2_id'
    bl_label = 'Extrude Along Path'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def draw(self, context):
        layout = self.layout

    def execute(self, context):
        b = context.scene.eap_custom_props.b

        edit_mode_out()
        ob_act = context.active_object
        bme = bmesh.new()
        bme.from_mesh(ob_act.data)

        if len(eap_buf.list_sp) != 1:
            self.report({'INFO'}, 'No start point stored in memory unable to continue.')
            edit_mode_in()
            return {'CANCELLED'}
        else:
            if len(eap_buf.list_ek) < 1:
                self.report({'INFO'}, 'No path or loop stored in memory unable to continue.')
                edit_mode_in()
                return {'CANCELLED'}
            else:
                dict_0 = get_lc_(bme, eap_buf.list_ek)
                if len(dict_0) > 1:
                    self.report({'INFO'}, 'More than one edge path or edge loop stored in memory unable to continue.')
                    edit_mode_in()
                    return {'CANCELLED'}
                else:
                    dict_1 = get_adj_v_(eap_buf.list_ek)
                    list_tmp = [i for i in dict_1 if (len(dict_1[i]) > 2)]
                    if len(list_tmp) != 0:
                        self.report({'INFO'}, 'Edge path or edge loop stored in memory is not valid unable to continue.')
                        edit_mode_in()
                        return {'CANCELLED'}
                    else:
                        list_2 = [v.index for v in bme.verts if v.select and v.is_valid]      # <----- list of vertices to be extruded
                        if len(list_2) == 0:
                            self.report({'INFO'}, 'Nothing selected unable to continue.')
                            edit_mode_in()
                            return {'CANCELLED'}
                        else:
                            list_fl = [i for i in dict_1 if (len(dict_1[i]) == 1)]

                            loop = is_loop_(list_fl)
                            # -- -- -- --
                            if loop:
                                list_1 = f_2(eap_buf.list_sp[0], eap_buf.list_ek)
                                del list_1[-1]
                            else:
                                if eap_buf.list_sp[0] not in list_fl:
                                    self.report({'INFO'}, 'Stored start point is not at the begining or the end of the path unable to continue.')
                                    edit_mode_in()
                                    return {'CANCELLED'}
                                elif eap_buf.list_sp[0] in list_fl:
                                    list_1 = f_1(eap_buf.list_sp[0], eap_buf.list_ek, list_fl[1] if eap_buf.list_sp[0] == list_fl[0] else list_fl[0])

                            # -- -- -- --
                            f_(bme, dict_0, list_fl, loop, list_2, list_1)

        # -- -- -- --
        if b == True:
            tmp = [bme.verts.remove(v) for v in [bme.verts[i] for i in list_1]]
            del tmp

        bme.to_mesh(ob_act.data)
        edit_mode_in()
        return {'FINISHED'}

# ------ operator 3 ------


class eap_op3(bpy.types.Operator):
    bl_idname = 'eap.op3_id'
    bl_label = ''
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def draw(self, context):
        layout = self.layout
        layout.label('Help:')

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=400)

# ------ operator 4 ------


class eap_op4(bpy.types.Operator):
    bl_idname = 'eap.op4_id'
    bl_label = ''
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.eap.op3_id('INVOKE_DEFAULT')
        return {'FINISHED'}

# ------ ------
class_list = [eap_p0, eap_op0, eap_op1, eap_op2, eap_op3, eap_op4, eap_p_group0]

# ------ register ------


def register():
    for c in class_list:
        bpy.utils.register_class(c)

    bpy.types.Scene.eap_custom_props = PointerProperty(type=eap_p_group0)

# ------ unregister ------


def unregister():
    for c in class_list:
        bpy.utils.unregister_class(c)

    if 'eap_custom_props' in bpy.context.scene:
        del bpy.context.scene['eap_custom_props']

# ------ ------
if __name__ == "__main__":
    register()
