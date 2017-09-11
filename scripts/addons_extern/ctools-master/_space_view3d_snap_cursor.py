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
    'name': 'Snap Cursor',
    'author': 'chromoly',
    'version': (0, 0, 3),
    'blender': (2, 78, 0),
    'location': 'View3D > Mouse > Menu', 
    'description': '',
    'warning': '',
    'category': '3D View'}


from functools import reduce
from itertools import combinations
import math

import bpy
from mathutils import Vector
import mathutils.geometry as geom


from .utils import addongroup
from .utils import vamath as vam

from .localutils.memoize import Memoize


# __addon_enabled__ = False


ANGLE_THRESHOLD = math.radians(0.1)  # radians

memoize = Memoize()


class VIEW3D_OT_snap_cursor(bpy.types.Operator):
    bl_description = ''
    bl_idname = 'view3d.snap_cursor'
    bl_label = 'Snap Cursor'
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls, context):
    #     return context.mode in ('OBJECT', 'EDIT_MESH')
    
    mode = bpy.props.EnumProperty(
        name='Mode',
        items=(('circle', 'Circle', '2D circle from 3 vertices'),
               ('sphere', 'Sphere', '3D sphere from 2 faces'),
               ('median', 'Median Applied Modifiers',
                'Apply modifiers in EDIT_MESH'),
               ('boundbox', 'BoundBox Applied Modifiers',
                'Apply modifiers in EDIT_MESH'),
               # ('selected', 'Selected', 'Default'),
               # ('center', 'Center', 'Default'),
               # ('grid', 'Grid', 'Default'),
               # ('active', 'Active', 'Default')
               ),
        default='circle')

    def get_dm_key(self, context):
        """@memoize用"""
        if context.active_object:
            return context.active_object.name
        else:
            return ''

    @memoize(get_dm_key)
    def get_dm(self, context):
        actob = context.active_object
        if actob:
            return actob.to_mesh(context.scene, True, 'PREVIEW')
        else:
            return None
        
    def execute_builtin(self, context):
        if self.mode == 'selected':
            bpy.ops.view3d.snap_cursor_to_selected()
        elif self.mode == 'center':
            bpy.ops.view3d.snap_cursor_to_center()
        elif self.mode == 'grid':
            bpy.ops.view3d.snap_cursor_to_grid()
        elif self.mode == 'active':
            bpy.ops.view3d.snap_cursor_to_active()
    
    def execute(self, context):
        if self.mode in ('selected', 'center', 'grid', 'active'):
            self.execute_builtin(context)
            return {'FINISHED'}
        
        actob = context.active_object
        mat = actob.matrix_world
        editmode = 'EDIT' in context.mode
        if editmode:
            bpy.ops.object.mode_set(mode='OBJECT')
        
        mesh = None
        if editmode and actob.type == 'MESH':
            mesh = actob.data
        
        loc = None
        if self.mode == 'circle':
            if mesh:
                vecs = (v.co for v in mesh.vertices if v.select and not v.hide)
                vecs = [mat * v for v in vecs]
            else:
                vecs = [Vector(ob.matrix_world.col[3][:3])
                        for ob in context.selected_objects]
            if len(vecs) == 3:
                center = vam.center_of_circumscribed_circle_tri(*vecs)
                if center:
                    loc = center
                    r = (vecs[0] - loc).length
                    self.report({'INFO'}, 'r: {}'.format(r))
            else:
                self.report({'WARNING'}, 'Select 3 vectors')

        elif self.mode == 'sphere':
            if mesh:
                vecs = (v.co for v in mesh.vertices if v.select and not v.hide)
                vecs = [mat * v for v in vecs]
                if len(vecs) < 4:
                    self.report({'WARNING'}, 'Select more than 4 vertices')
                elif len(vecs) > 16:
                    # 計算に時間がかかるのでパス。
                    txt = '{} vertices is selected. Too many'.format(len(vecs))
                    self.report({'WARNING'}, txt)
                else:
                    locations = []
                    normals = []
                    for v1, v2, v3 in combinations(vecs, 3):
                        center = vam.center_of_circumscribed_circle_tri(
                                         v1, v2, v3)
                        if center:
                            locations.append(center)
                            normals.append(geom.normal(v1, v2, v3))
                    inters = []
                    for i, j in combinations(range(len(locations)), 2):
                        cross_length = normals[i].cross(normals[j]).length
                        angle = math.asin(min(cross_length, 1.0))
                        if angle < ANGLE_THRESHOLD:
                            continue
                        v1 = locations[i]
                        v2 = v1 + normals[i]
                        v3 = locations[j]
                        v4 = v3 + normals[j]
                        inter = geom.intersect_line_line(v1, v2, v3, v4)
                        if inter:
                            inters.append((inter[0] + inter[1]) / 2)
                    if inters:
                        loc = (reduce(lambda v1, v2: v1 + v2, inters) /
                               len(inters))
                        r_sum = 0
                        for v in vecs:
                            r_sum += (v - loc).length
                        r = r_sum /len(vecs)
                        self.report({'INFO'}, 'r: {}'.format(r))
                
        elif self.mode == 'median':
            if mesh:
                dm = self.get_dm(context)
                vecs = [v.co for v in dm.vertices if v.select and not v.hide]
                if vecs:
                    vecs = [mat * v for v in vecs]
                    loc = (reduce(lambda v1, v2: v1 + v2, vecs) /
                                       len(vecs))
        
        elif self.mode == 'boundbox':
            if mesh:
                dm = self.get_dm(context)
                vecs = (v.co for v in dm.vertices if v.select and not v.hide)
                vecs = [mat * v for v in vecs]
                if vecs:
                    v = vecs[0]
                    mins = [v[0], v[1], v[2]]
                    maxs = [v[0], v[1], v[2]]
                    for v in vecs:
                        for i in range(3):
                            if v[i] < mins[i]:
                                mins[i] = v[i]
                            if v[i] > maxs[i]:
                                maxs[i] = v[i]
                    loc = Vector([(mins[i] + maxs[i]) / 2 for i in range(3)])
        
        if editmode:
            bpy.ops.object.mode_set(mode='EDIT')

        if loc:
            context.space_data.cursor_location = loc

        return {'FINISHED'}
    
    def invoke(self, context, event):
        memoize.clear()
        self.execute(context)
    
        return {'FINISHED'}


def draw(self, context):
    layout = self.layout.column()
    layout.operator_context = 'INVOKE_DEFAULT'
    layout.separator()

    op = layout.operator('view3d.snap_cursor', text='Cursor to Circle',
                         icon='MESH_CIRCLE')
    op.mode = 'circle'
    op = layout.operator('view3d.snap_cursor', text='Cursor to Sphere',
                         icon='MESH_UVSPHERE')
    op.mode = 'sphere'
    op = layout.operator('view3d.snap_cursor', text='Cursor to Median',
                         icon='ROTATECENTER')
    op.mode = 'median'
    op = layout.operator('view3d.snap_cursor', text='Cursor to BoundBox',
                         icon='ROTATE')
    op.mode = 'boundbox'


def register():
    addongroup.AddonGroup.register_module(__name__)

    bpy.types.VIEW3D_MT_snap.append(draw)


def unregister():
    bpy.types.VIEW3D_MT_snap.remove(draw)

    addongroup.AddonGroup.unregister_module(__name__)


if __name__ == '__main__':
    register()
