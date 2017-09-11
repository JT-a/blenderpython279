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

__author__ = "mkbreuer"
__status__ = "toolplus"
__version__ = "1.0"
__date__ = "2016"

import bpy
from bpy import*
    
class Curve_Wire_All(bpy.types.Operator):
    """Wire on All Objects"""
    bl_idname = "tp_ops.wire_all"
    bl_label = "Wire on All Objects"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        for obj in bpy.data.objects:
            if obj.show_wire:
                obj.show_all_edges = False
                obj.show_wire = False            
            else:
                obj.show_all_edges = True
                obj.show_wire = True
                             
        return {'FINISHED'} 

class Curve_Wire_On(bpy.types.Operator):
    '''Curve Wire on'''
    bl_idname = "tp_ops.wire_on"
    bl_label = "Wire on"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        selection = bpy.context.selected_objects  
         
        if not(selection): 
            for obj in bpy.data.objects:
                obj.show_wire = True
                obj.show_all_edges = True
                
        else:
            for obj in selection:
                obj.show_wire = True
                obj.show_all_edges = True 
        return {'FINISHED'}


class Curve_Wire_Off(bpy.types.Operator):
    '''Curve Wire off'''
    bl_idname = "tp_ops.wire_off"
    bl_label = "Wire off"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        selection = bpy.context.selected_objects  
        
        if not(selection): 
            for obj in bpy.data.objects:
                obj.show_wire = False
                obj.show_all_edges = False
                
        else:
            for obj in selection:
                obj.show_wire = False
                obj.show_all_edges = False   

        return {'FINISHED'}
    
    
    
class OpenCurve(bpy.types.Operator):
    """Open Curve"""
    bl_idname = "curve.open_circle"
    bl_label = "Open Curve"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.cyclic_toggle()     
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


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




class pivotBox(bpy.types.Operator):
   """Set pivot point to Bounding Box"""
   bl_label = "Set pivot point to Bounding Box"
   bl_idname = "view3d.pivot_bounding_box"
   bl_options = {'REGISTER', 'UNDO'}
    
   def execute(self, context):
       bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
       return {"FINISHED"} 

 
class pivotCursor(bpy.types.Operator):
   """Set pivot point to 3D Cursor"""
   bl_label = "Set pivot point to 3D Cursor"
   bl_idname = "view3d.pivot_3d_cursor"
   bl_options = {'REGISTER', 'UNDO'}
    
   def execute(self, context):
       bpy.context.space_data.pivot_point = 'CURSOR'
       return {"FINISHED"} 


class pivotMedian(bpy.types.Operator):
    """Set pivot point to Median Point"""
    bl_label = "Set pivot point to Median Point"
    bl_idname = "view3d.pivot_median"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
        return {"FINISHED"}


class pivotActive(bpy.types.Operator):
   """Set pivot point to Active"""
   bl_label = "Set pivot point to Active"
   bl_idname = "view3d.pivot_active"
   bl_options = {'REGISTER', 'UNDO'}
    
   def execute(self, context):
       bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
       return {"FINISHED"} 


class pivotIndividual(bpy.types.Operator):
    """Set pivot point to Individual"""
    bl_label = "Set pivot point to Individual Point"
    bl_idname = "view3d.pivot_individual"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        return {"FINISHED"}   




def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()




