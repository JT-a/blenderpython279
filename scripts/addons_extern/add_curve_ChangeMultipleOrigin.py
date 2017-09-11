'''
changeCurveOrigin can relocate origin of curves at max or min of x/y/z vertex of the curve.
Many curves can be applied by multiple selection.

options:
xyz='x'/'y'/'z'. xyz is coodinate to use to compare value. 
maxmin='max'/'min'. maxmin is comaring criteria by max or min.
'''

bl_info = {
    "name": "Change Multiple Curve Origin",
    "author": "Squared Nob",
    "version": (0, 1),
    "blender": (2, 7, 1),
    "location": "",
    "description": "Change multiple curve origins by multiple selection",
    "warning": "",
    "wiki_url": "https://github.com/squarednob/Blender_change_multiple_curve_origin",
    "tracker_url": "https://github.com/squarednob/Blender_change_multiple_curve_origin",
    "category": "Add Curve"}

import bpy


def changeMultipleCurveOrigin(xyz='x', maxmin='max'):

    # Store multiple selected curves.
    selected_curves = bpy.context.selected_objects

    for curve in selected_curves:
        # Deselect all and select one curve.
        bpy.ops.object.select_all(action='DESELECT')
        curve.select = True

        # Return vertex point where max or min value of x/y/x.
        vert_tip_point = getMaxOrMinVertex(curve, xyz, maxmin)

        # Change cursor's location to the tip point.
        bpy.context.scene.cursor_location = vert_tip_point

        # Activate the curve object
        bpy.context.scene.objects.active = curve

        # Set origin at cursor = vertex tip point.
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

# Get curve's vertex point where max/min of x/y/x.


def getMaxOrMinVertex(curve, xyz='x', maxmin='max'):

    # Specify which coordinate will be used to compare.
    coord_index = 0
    if xyz == 'x':
        coord_index = 0
    elif xyz == 'y':
        coord_index = 1
    elif xyz == 'z':
        coord_index = 2
    else:
        coord_index = 0

    # Matrix multiplier for local point to change into global point, due to cursor point using global point.
    curve_matrix_world = curve.matrix_world

    vert_tip_point = (0, 0, 0)
    for i, d in enumerate(curve.data.splines[0].bezier_points):
        # Multply cooridnate by matrix world to make global coordinate. Don't reverse order, it's linear algebla's multipy!
        coord = curve_matrix_world * d.co
        if i == 0:
            vert_tip_point = coord
        else:
            # Switch max or min comperarison
            if maxmin == 'max':
                if vert_tip_point[coord_index] < coord[coord_index]:
                    vert_tip_point = coord
            elif maxmin == 'min':
                if vert_tip_point[coord_index] > coord[coord_index]:
                    vert_tip_point = coord
            else:
                if vert_tip_point[coord_index] < coord[coord_index]:
                    vert_tip_point = coord
    return vert_tip_point

# Main class


class ChangeMultipleCurveOrigin(bpy.types.Operator):
    """Change Multipe Curve Origins"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.change_multiple_curve_origin"        # unique identifier for buttons and menu items to reference.
    bl_label = "Change multiple curve origin"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    # Get user input.
    xyz = bpy.props.StringProperty(name="Choose x/y/z direction",
                                   description="x/y/z direction to compare location of verteces",
                                   default="x")
    maxmin = bpy.props.StringProperty(name="Choose max/min of locations",
                                      description="max/min of locations to pick up a vertex",
                                      default="max")

    def execute(self, context):        # execute() is called by blender when running the operator.
        # Execute main function
        changeMultipleCurveOrigin(xyz=self.xyz, maxmin=self.maxmin)

        return {'FINISHED'}            # this lets blender know the operator finished successfully.


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
