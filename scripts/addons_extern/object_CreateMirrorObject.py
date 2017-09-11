bl_info = {
    "name": "Create mirror object",
    "category": "Object",
}

import bpy


class CreateMirrorObject(bpy.types.Operator):
    """Create mirror object"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.createmirrorobject"        # unique identifier for buttons and menu items to reference.
    bl_label = "Create mirror object"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.

        # Create base cube
        bpy.ops.mesh.primitive_cube_add()

        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all verts/faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Move over to one side
        bpy.ops.transform.translate(value=(1, 0, 0), constraint_axis=(True, False, False))

        # Deselect all
        bpy.ops.mesh.select_all(action='DESELECT')

        # Get a handle to the object
        obj = bpy.context.active_object

        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Apply mirror modifier
        bpy.ops.object.modifier_add(type='MIRROR')

        # Select face to delete
        obj.data.polygons[0].select = True

        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Delete the middle face
        bpy.ops.mesh.delete(type='FACE')

        # Finally return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}            # this lets blender know the operator finished successfully.


def register():
    bpy.utils.register_class(CreateMirrorObject)


def unregister():
    bpy.utils.unregister_class(CreateMirrorObject)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
