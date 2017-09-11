#########################################
# resamples baked f-curves to a new     #
# action + f-curve or a 3d bezier curve #
#########################################

bl_info = {
    "name": "unbake f-curve",
    "author": "liero",
    "version": (0, 5),
    "blender": (2, 7, 3),
    "location": "View3D > Animation tab > Properties Panel",
    "description": "Resample baked f-curve to a new Action / f-curve",
    "category": "Animation"}

import bpy
from bpy.props import BoolProperty, FloatProperty


class Boton(bpy.types.Panel):
    bl_label = 'unBake selected fcurves'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Animate"

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        box = layout.box()
        box.operator('curve.unbake_action')
        box.operator('curve.unbake_bezier')


class UnBakeA(bpy.types.Operator):
    bl_idname = 'curve.unbake_action'
    bl_label = 'unBake to Action'
    bl_description = 'Resample baked f-curve to a new Action / f-curve'
    bl_options = {'REGISTER', 'UNDO'}

    RGB = BoolProperty(name='Use RGB colors', default=True, description='Use RGB colors for f-curves')

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.animation_data)

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        column.label(text='Unbake Action:')
        column.prop(self, 'RGB')

    def execute(self, context):
        obj = context.object
        pts = [(c.sampled_points, c.data_path, c.array_index) for c in obj.animation_data.action.fcurves if c.sampled_points and c.select]
        if pts:
            keys = bpy.data.actions.new(name='KEYS')
            for sam, dat, ind in pts:
                fcu = keys.fcurves.new(data_path=dat, index=ind)
                if self.RGB:
                    fcu.color_mode = 'AUTO_RGB'
                fcu.keyframe_points.add(len(sam))
                for i in range(len(sam)):
                    w = fcu.keyframe_points[i]
                    w.co = w.handle_left = w.handle_right = sam[i].co
            obj.animation_data.action = keys
        return{'FINISHED'}


class UnBakeB(bpy.types.Operator):
    bl_idname = 'curve.unbake_bezier'
    bl_label = 'unBake to 3D'
    bl_description = 'Resample baked f-curve to a 3d Bezier curve'
    bl_options = {'REGISTER', 'UNDO'}

    scaleX = FloatProperty(name='X scale', min=.01, max=5, default=.1, description='X scale for 3d curve')
    scaleY = FloatProperty(name='Y scale', min=.001, max=5, default=1, description='Z scale for 3d curve')
    use_radius = BoolProperty(name='Use Radius', default=True, description='Use Radius and Beveling or just Draw the Profile')

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.animation_data)

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        column.label(text='Unbake Bezier:')
        column.prop(self, 'scaleX')
        column.prop(self, 'scaleY')
        column.prop(self, 'use_radius')

    def execute(self, context):
        obj = context.object
        for c in obj.animation_data.action.fcurves:
            if c.sampled_points and c.select:
                sam = c.sampled_points
                cu = bpy.data.curves.new('path', 'CURVE')
                cu.dimensions = '3D'
                if self.use_radius:
                    cu.fill_mode = 'FULL'
                    cu.bevel_resolution = 6
                    cu.resolution_u = 1
                    cu.bevel_depth = 1
                spline = cu.splines.new('BEZIER')
                spline.bezier_points.add(len(sam) - 1)
                curva = bpy.data.objects.new('curve', cu)
                curva.name = c.data_path + ' ' + str(c.array_index)
                context.scene.objects.link(curva)
                for i in range(len(sam)):
                    w = spline.bezier_points[i]
                    y = self.scaleY * sam[i].co[1]
                    if self.use_radius:
                        w.radius = y
                        y = 0
                    coords = (self.scaleX * sam[i].co[0], y, 0)
                    w.co = w.handle_left = w.handle_right = coords

        return{'FINISHED'}


def register():
    bpy.utils.register_class(Boton)
    bpy.utils.register_class(UnBakeA)
    bpy.utils.register_class(UnBakeB)


def unregister():
    bpy.utils.unregister_class(Boton)
    bpy.utils.unregister_class(UnBakeA)
    bpy.utils.unregister_class(UnBakeB)

if __name__ == '__main__':
    register()
