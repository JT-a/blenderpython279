############################################################################
#
# uv_prj_from_normal.py
#
# Copyright (C) 2014 chaosdesk
#
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
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.#
#
# ##### END GPL LICENSE BLOCK #####
#
############################################################################

bl_info = {
    'name': 'Project From Normal',
    'author': 'chaosdesk',
    'version': (0, 1),
    'blender': (2, 6, 9),
    "location": "View3D > UV Mapping > Project From Normal",
    'description': 'Project from average normal of all Face',
    'warning': '',
    'wiki_url': '',
    'tracker_url': 'http://chaosdesk.blog123.fc2.com/',
    "category": "UV"}


import bpy
import mathutils
from mathutils import Vector, Matrix


MAX_LOCATION = 1


class ProjectFromNormal(object):

    def __init__(self):
        bpy.ops.object.mode_set(mode='OBJECT')

        self.current_obj = bpy.context.selected_objects[0]
        self.mesh = self.current_obj.data
        self.select_poly = []

        # check if more than one face is selected
        self.NoneSelect = True
        for poly in self.mesh.polygons:
            if poly.select == True:
                self.NoneSelect = False
                self.select_poly.append(poly)

        if self.NoneSelect == True:
            return

        if self.mesh.uv_layers.active == None:
            self.mesh.uv_textures.new()

        # translate position that selected polygon's uv
        self.transUvVector()

        bpy.ops.object.mode_set(mode='EDIT')

    def transUvVector(self):
        max_position = 0.
        min_position_x = 0.
        min_position_y = 0.

        # calculate two rotation matrix from normal vector of selected polygons
        vector_nor = self.averageNormal()

        theta_x = self.calcRotAngle('X', vector_nor.x, vector_nor.y, vector_nor.z)
        mat_rotx = Matrix.Rotation(theta_x, 3, 'X')
        vector_nor.rotate(mat_rotx)

        theta_y = self.calcRotAngle('Y', vector_nor.x, vector_nor.y, vector_nor.z)
        mat_roty = Matrix.Rotation(theta_y, 3, 'Y')

        # apply two rotation matrix to vertex
        uv_array = self.mesh.uv_layers.active.data
        for poly in self.select_poly:
            for id in range(poly.loop_start, poly.loop_start + poly.loop_total):
                new_vector = Vector((self.mesh.vertices[self.mesh.loops[id].vertex_index].co[0],
                                     self.mesh.vertices[self.mesh.loops[id].vertex_index].co[1],
                                     self.mesh.vertices[self.mesh.loops[id].vertex_index].co[2]))

                new_vector.rotate(mat_rotx)
                new_vector.rotate(mat_roty)

                uv_array[id].uv = new_vector.to_2d()

                if min_position_x > uv_array[id].uv.x:
                    min_position_x = uv_array[id].uv.x
                if min_position_y > uv_array[id].uv.y:
                    min_position_y = uv_array[id].uv.y

        # recalculate uv position
        for poly in self.select_poly:
            for id in range(poly.loop_start, poly.loop_start + poly.loop_total):
                uv_array[id].uv.x = uv_array[id].uv.x + abs(min_position_x)
                uv_array[id].uv.y = uv_array[id].uv.y + abs(min_position_y)

                if max_position < uv_array[id].uv.x:
                    max_position = uv_array[id].uv.x
                if max_position < uv_array[id].uv.y:
                    max_position = uv_array[id].uv.y

        # scale uv position
        for poly in self.select_poly:
            for id in range(poly.loop_start, poly.loop_start + poly.loop_total):
                uv_array[id].uv.x = uv_array[id].uv.x * MAX_LOCATION / max_position
                uv_array[id].uv.y = uv_array[id].uv.y * MAX_LOCATION / max_position

    def averageNormal(self):
        weight_norx = 0.
        weight_nory = 0.
        weight_norz = 0.
        aver_normal = None

        for poly in self.select_poly:
            weight_norx = weight_norx + (poly.normal.x * poly.area)
            weight_nory = weight_nory + (poly.normal.y * poly.area)
            weight_norz = weight_norz + (poly.normal.z * poly.area)

        aver_normal = Vector((weight_norx, weight_nory, weight_norz))
        aver_normal.normalize()

        return aver_normal

    def calcRotAngle(self, axis, nor_x, nor_y, nor_z):
        theta = 0
        vector_z = Vector((0.0, 0.0, 1.0))
        vector_n = None
        vector_cross = None

        if axis == 'X':
            vector_n = Vector((0.0, nor_y, nor_z))
            theta = vector_z.angle(vector_n, 999)
            vector_cross = vector_n.cross(vector_z)
            if vector_cross.x < 0:
                theta = -(theta)
        elif axis == 'Y':
            vector_n = Vector((nor_x, 0.0, nor_z))
            theta = vector_z.angle(vector_n, 999)
            vector_cross = vector_n.cross(vector_z)
            if vector_cross.y < 0:
                theta = -(theta)
        else:
            pass

        return theta


class NewUvProjectMenu(bpy.types.Operator):
    """Project From Normal"""
    bl_idname = "mesh.uv_project_from_normal_vector"
    bl_label = "Project From Normal Vector"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ProjectFromNormal()
        return {'FINISHED'}


def menu_func(self, context):
    # self.layout.separator()
    self.layout.operator("mesh.uv_project_from_normal_vector",
                         text="Project From Normal",
                         icon='PLUGIN')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)

if __name__ == '__main__':
    register()
