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
    "name": "Sculpt Stroke On Grease Pencil",
    "author": "Joel Daniels",
    "version": (1, 0),
    "blender": (2, 6, 9),
    "location": "Properties Panel (Sculpt Mode)",
    "description": "Sculpt strokes can be made along grease pencil strokes or along a selected curve snapped to the exterior of the sculpt mesh",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sculpting"}

import bpy

def curve_enumerator(self, context):
    curves = []
    for ob in context.scene.objects:
        if ob.type == 'CURVE':
            curves.append((ob.name, ob.name, ""))
    return curves

class SCULPT_OT_(bpy.types.Operator):
    bl_idname = "sculpt.grease_pencil_stroke"
    bl_label = "Stroke On Grease Pencil"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        ob = context.object
        spacing = ob.gp_stroke_samples
        brush_stroke = bpy.ops.sculpt.brush_stroke
        if not ob.gp_stroke_use_curve:
            if ob.grease_pencil is None:
                self.report({'INFO'}, "Please create a grease pencil stroke.")
                return {'FINISHED'}
            layers = ob.grease_pencil.layers
            for layer in layers:
                for strokes in layer.active_frame.strokes:
                    for i in range(0, len(strokes.points), spacing):
                        p = strokes.points[i]
                        x, y, z = p.co[0], p.co[1], p.co[2]
                        stroke = [{ "name": "defaultStroke",
                        "mouse" : (0.0, 0.0),
                        "pen_flip" : False,
                        "is_start": True,
                        "location": (x, y, z),
                        "pressure": 1.0,
                        "size": 1.0,                        
                        "time": 1.0},
                        
                       {"name" : "defaultStroke2",
                       "mouse" : (0.0, 0.0),
                       "pen_flip" : False,
                       "is_start" : False,
                       "location":(x, y, z),
                       "mouse": (0.0, 0.0),
                        "pressure":1.0,
                        "size": 1.0,                        
                        "time":1.0
                        }
                        ]
                        
                        brush_stroke(stroke=stroke)
            
        else:
            curve = ob.gp_stroke_curve_ob
            if curve == "":
                self.report({"INFO"}, "You need to select a curve!")
                return {'FINISHED'} 
            curve = context.scene.objects[curve]
            mesh = curve.to_mesh(context.scene, True, 'RENDER')
            mat = curve.matrix_world
            loc_obj_space = [v.co for v in mesh.vertices]
            loc_world_space=list(map(lambda x: mat*x, loc_obj_space))
            for i in range(0, len(loc_world_space), spacing):
                        p = loc_world_space[i]
                        x, y, z = p[0], p[1], p[2]
                        stroke = [{ "name": "defaultStroke",
                        "mouse" : (0.0, 0.0),
                        "pen_flip" : False,
                        "is_start": True,
                        "location": (x, y, z),
                        "pressure": 1.0,
                        "size": 1.0,                        
                        "time": 1.0},
                        
                       {"name" : "defaultStroke2",
                       "mouse" : (0.0, 0.0),
                       "pen_flip" : False,
                       "is_start" : False,
                       "location":(x, y, z),
                       "mouse": (0.0, 0.0),
                        "pressure":1.0,
                        "size": 1.0,                        
                        "time":1.0
                        }
                        ]
                        
                        brush_stroke(stroke=stroke)
            bpy.data.meshes.remove(mesh)
            
        return {'FINISHED'}

class SCULPT_PT_myStrokePanel(bpy.types.Panel):
    bl_label = "Stroke On Grease Pencil"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "GP"
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.mode == 'SCULPT'
       
    def draw(self, context):
        layout = self.layout
        object = context.object
        scene = context.scene
        layout.prop(object, "gp_stroke_use_curve")
        if object.gp_stroke_use_curve:
            curve_list = curve_enumerator(self, context)
            if len(curve_list) > 0: 
                #Don't display anything but text if no curves are available
                layout.prop(object, "gp_stroke_curve_ob", text = "Curve")
                if object.gp_stroke_curve_ob != "":
                    curve = scene.objects[object.gp_stroke_curve_ob].data
                    layout.prop(curve, "resolution_u", text = "Curve Resolution")
            else:
                layout.label("There are no curves in the scene!")
             
        layout.prop(object, "gp_stroke_samples")
        layout.operator("sculpt.grease_pencil_stroke")
        
        
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Object.gp_stroke_use_curve = bpy.props.BoolProperty(
                                    name = "Sculpt stroke along curve",
                                    description = "Sculpt stroke along a curve object",
                                    default = False)
                                  
    bpy.types.Object.gp_stroke_curve_ob = bpy.props.EnumProperty(items =
                                    curve_enumerator,
                                    name = "",
                                    description = "Curve to use as guide for sculpt stroke")
                                    
    bpy.types.Object.gp_stroke_samples = bpy.props.IntProperty(name = "Spacing", description = "Spacing of samples taken from grease pencil stroke", default = 2, min = 1, max = 10)                   
    
def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()