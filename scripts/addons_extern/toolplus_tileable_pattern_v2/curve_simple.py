# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and / or
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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
"""
bl_info = {
    'name': 'Simple Curve',
    'author': 'Spivak Vladimir (http://cwolf3d.korostyshev.net)',
    'version': (1, 5, 2),
    'blender': (2, 6, 9),
    'location': 'View3D > Add > Curve',
    'description': 'Adds Simple Curve',
    'warning': '', # used for warning icon and text in addons panel
    'wiki_url': 'http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Simple_curves',
    'tracker_url': 'https://developer.blender.org/T37664',
    'category': 'Add Curve'}
"""

##------------------------------------------------------------
#### import modules
import bpy
from bpy.props import  *
from mathutils import  *
from math import  *
from bpy_extras.object_utils import *
from random import *


##------------------------------------------------------------
# calculates the matrix for the new object
# depending on user pref
def align_matrix(context, location):
    loc = Matrix.Translation(location)
    obj_align = context.user_preferences.edit.object_align
    if (context.space_data.type == 'VIEW_3D'
        and obj_align == 'VIEW'):
        rot = context.space_data.region_3d.view_matrix.to_3x3().inverted().to_4x4()
    else:
        rot = Matrix()
    align_matrix = loc * rot

    return align_matrix


##------------------------------------------------------------
#### Delete simple curve
def SimpleDelete(name):
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode = 'OBJECT')

    bpy.context.scene.objects.active = bpy.data.objects[name]
    bpy.ops.object.delete()

    return


##------------------------------------------------------------
# Fillet
class BezierPointsFillet(bpy.types.Operator):
    ''''''
    bl_idname = "curve.bezier_points_fillet"
    bl_label = "Bezier points fillet"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "bezier points fillet"

    Fillet_radius = FloatProperty(name = "Radius",
                    default = 0.25,
                    unit = 'LENGTH',
                    description = "radius")

    Types = [('Round', 'Round', 'Round'),
             ('Chamfer', 'Chamfer', 'Chamfer')]
    Fillet_Type = EnumProperty(name = "Type",
                description = "Fillet type",
                items = Types)

    ##### DRAW #####
    def draw(self, context):
        layout = self.layout

        # general options
        col = layout.column()
        col.prop(self, 'Fillet_radius')
        col.prop(self, 'Fillet_Type', expand = True)

        row = layout.row()
        row.operator("help.operator","Help", icon ="INFO")

    ##### POLL #####
    @classmethod
    def poll(cls, context):
        return context.scene != None

    ##### EXECUTE #####
    def execute(self, context):
        #go to object mode
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.mode_set(mode = 'EDIT')

        # turn off undo
        undo = bpy.context.user_preferences.edit.use_global_undo
        bpy.context.user_preferences.edit.use_global_undo = False

        # main function
        spline = bpy.context.object.data.splines.active
        selected = [p for p in spline.bezier_points if p.select_control_point]

        bpy.ops.curve.handle_type_set(type = 'VECTOR')
        n = 0
        ii = []
        for p in spline.bezier_points :
            if p.select_control_point :
                ii.append(n)
                n += 1
            else:
                n += 1

        if n > 2 :

            jn = 0

            for j in ii :

                j += jn

                selected_all = [p for p in spline.bezier_points]

                bpy.ops.curve.select_all(action = 'DESELECT')

                if j != 0 and j != n - 1 :
                    selected_all[j].select_control_point = True
                    selected_all[j + 1].select_control_point = True
                    bpy.ops.curve.subdivide()
                    selected_all = [p for p in spline.bezier_points]
                    selected4 = [selected_all[j - 1], selected_all[j], selected_all[j + 1], selected_all[j + 2]]
                    jn += 1
                    n += 1

                elif j == 0 :
                    selected_all[j].select_control_point = True
                    selected_all[j + 1].select_control_point = True
                    bpy.ops.curve.subdivide()
                    selected_all = [p for p in spline.bezier_points]
                    selected4 = [selected_all[n], selected_all[0], selected_all[1], selected_all[2]]
                    jn += 1
                    n += 1

                elif j == n - 1 :
                    selected_all[j].select_control_point = True
                    selected_all[j - 1].select_control_point = True
                    bpy.ops.curve.subdivide()
                    selected_all = [p for p in spline.bezier_points]
                    selected4 = [selected_all[0], selected_all[n], selected_all[n - 1], selected_all[n - 2]]

                selected4[2].co = selected4[1].co
                s1 = Vector(selected4[0].co)  -  Vector(selected4[1].co)
                s2 = Vector(selected4[3].co)  -  Vector(selected4[2].co)
                s1.normalize()
                s11 = Vector(selected4[1].co) + s1 * self.Fillet_radius
                selected4[1].co = s11
                s2.normalize()
                s22 = Vector(selected4[2].co) + s2 * self.Fillet_radius
                selected4[2].co = s22

                if self.Fillet_Type == 'Round' :
                    if j != n - 1 :
                        selected4[2].handle_right_type = 'VECTOR'
                        selected4[1].handle_left_type = 'VECTOR'
                        selected4[1].handle_right_type = 'ALIGNED'
                        selected4[2].handle_left_type = 'ALIGNED'
                    else:
                        selected4[1].handle_right_type = 'VECTOR'
                        selected4[2].handle_left_type = 'VECTOR'
                        selected4[2].handle_right_type = 'ALIGNED'
                        selected4[1].handle_left_type = 'ALIGNED'
                if self.Fillet_Type == 'Chamfer' :
                        selected4[2].handle_right_type = 'VECTOR'
                        selected4[1].handle_left_type = 'VECTOR'
                        selected4[1].handle_right_type = 'VECTOR'
                        selected4[2].handle_left_type = 'VECTOR'

        bpy.ops.curve.select_all(action = 'SELECT')
        bpy.ops.curve.spline_type_set(type = 'BEZIER')

        # restore pre operator undo state
        bpy.context.user_preferences.edit.use_global_undo = undo

        return {'FINISHED'}

    ##### INVOKE #####
    def invoke(self, context, event):
        self.execute(context)

        return {'FINISHED'}

def subdivide_cubic_bezier(p1, p2, p3, p4, t):
    p12 = (p2-p1)*t + p1
    p23 = (p3-p2)*t + p2
    p34 = (p4-p3)*t + p3
    p123 = (p23-p12)*t + p12
    p234 = (p34-p23)*t + p23
    p1234 = (p234-p123)*t + p123
    return [p12, p123, p1234, p234, p34]

##------------------------------------------------------------
# BezierDivide Operator
class BezierDivide(bpy.types.Operator):
    ''''''
    bl_idname = "curve.bezier_spline_divide"
    bl_label = "Bezier spline divide"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "bezier spline divide"
    
    # align_matrix for the invoke
    align_matrix = Matrix()

    Bezier_t = FloatProperty(name = "t (0% - 100%)",
                    default = 50.0,
                    min = 0.0, soft_min = 0.0,
                    max = 100.0, soft_max = 100.0,
                    description = "t (0% - 100%)")
    
    ##### POLL #####
    @classmethod
    def poll(cls, context):
        return context.scene != None

    ##### EXECUTE #####
    def execute(self, context):
        #go to object mode
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.mode_set(mode = 'EDIT')

        # turn off undo
        undo = bpy.context.user_preferences.edit.use_global_undo
        bpy.context.user_preferences.edit.use_global_undo = False

        # main function
        spline = bpy.context.object.data.splines.active
        vertex = []
        selected_all = [p for p in spline.bezier_points if p.select_control_point]
        h = subdivide_cubic_bezier(selected_all[0].co, selected_all[0].handle_right, selected_all[1].handle_left, selected_all[1].co, self.Bezier_t/100)
        
        selected_all[0].handle_right_type = 'FREE'
        selected_all[0].handle_left_type = 'FREE'
        selected_all[1].handle_right_type = 'FREE'
        selected_all[1].handle_left_type = 'FREE'
        bpy.ops.curve.subdivide(1)
        selected_all = [p for p in spline.bezier_points if p.select_control_point]
        
        selected_all[0].handle_right = h[0]
        selected_all[1].co = h[2]
        selected_all[1].handle_left = h[1]
        selected_all[1].handle_right = h[3]
        selected_all[2].handle_left = h[4]

        # restore pre operator undo state
        bpy.context.user_preferences.edit.use_global_undo = undo

        return {'FINISHED'}

    ##### INVOKE #####
    def invoke(self, context, event):
        self.execute(context)

        return {'FINISHED'}



################################################################################
##### REGISTER #####


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()