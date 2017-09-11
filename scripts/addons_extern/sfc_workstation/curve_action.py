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
from bpy import*

### switch of spline type ###


class toPoly(bpy.types.Operator):
    """Curve to Poly Spline"""
    bl_idname = "curve.to_poly"
    bl_label = "Curve to Poly Spline"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.spline_type_set(type='POLY')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class toBezier(bpy.types.Operator):
    """Curve to Bezier Spline"""
    bl_idname = "curve.to_bezier"
    bl_label = "Curve to Bezier Spline"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.spline_type_set(type='BEZIER')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class toNurbs(bpy.types.Operator):
    """Curve to Nurbs Spline"""
    bl_idname = "curve.to_nurbs"
    bl_label = "Curve to Nurbs Spline"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.spline_type_set(type='NURBS')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

### switch of handle type ###


class toAutomatic(bpy.types.Operator):
    """Handle to Automatic Rounded Type"""
    bl_idname = "curve.handle_to_automatic"
    bl_label = "Handle to Automatic Rounded Type"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.handle_type_set(type='AUTOMATIC')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class toVector(bpy.types.Operator):
    """Handle to Vector Type"""
    bl_idname = "curve.handle_to_vector"
    bl_label = "Handle to Vector Type"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.handle_type_set(type='VECTOR')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class toAligned(bpy.types.Operator):
    """Handle to Aligned Type"""
    bl_idname = "curve.handle_to_aligned"
    bl_label = "Handle to Aligned Type"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.handle_type_set(type='ALIGNED')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class toFree(bpy.types.Operator):
    """Handle to Free Type"""
    bl_idname = "curve.handle_to_free"
    bl_label = "Handle to Free Type"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.handle_type_set(type='FREE_ALIGN')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

### further operator ###


class SmoothCurve(bpy.types.Operator):
    """Smooth Curve Spline"""
    bl_idname = "curve.smoothspline"
    bl_label = "Smooth Curve Spline"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.smooth()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class CurveDirection(bpy.types.Operator):
    """switch curve direction > only BEZIER"""
    bl_idname = "curve.switch_direction_obm"
    bl_label = "Curve Direction"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.switch_direction()
        bpy.ops.object.editmode_toggle()
        bpy.ops.curvetools2.operatororigintospline0start()
        return {'FINISHED'}


class ConvertBezier(bpy.types.Operator):
    """Convert to Curve with Bezièr Spline Typ"""
    bl_idname = "curve.convert_bezier"
    bl_label = "Convert to Curve with Bezièr Spline Typ"

    def execute(self, context):
        bpy.ops.object.convert(target='CURVE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.spline_type_set(type='BEZIER')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(toPoly)
    bpy.utils.register_class(toBezier)
    bpy.utils.register_class(toNurbs)
    bpy.utils.register_class(toAutomatic)
    bpy.utils.register_class(toVector)
    bpy.utils.register_class(toAligned)
    bpy.utils.register_class(toFree)
    bpy.utils.register_class(SmoothCurve)
    bpy.utils.register_class(CurveDirection)
    bpy.utils.register_class(ConvertBezier)

    # bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_class(toPoly)
    bpy.utils.unregister_class(toBezier)
    bpy.utils.unregister_class(toNurbs)
    bpy.utils.unregister_class(toAutomatic)
    bpy.utils.unregister_class(toVector)
    bpy.utils.unregister_class(toAligned)
    bpy.utils.unregister_class(toFree)
    bpy.utils.unregister_class(SmoothCurve)
    bpy.utils.unregister_class(CurveDirection)
    bpy.utils.unregister_class(ConvertBezier)

    # bpy.utils.unregister_module(__name__)
