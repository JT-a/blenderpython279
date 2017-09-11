bl_info = {
    "name": "F Toggle mesh selectability",
    "category": "Object",
}
import bpy

class ObjSelectability(bpy.types.Operator):
    """Toggle mesh selectability"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.toggleselectability"        # unique identifier for buttons and menu items to reference.
    bl_label = "FTMS Toggle Mesh Selectability"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.
        do_i_hide_select = not bpy.context.active_object.hide_select
        if bpy.context.selected_objects == []:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    ob.hide_select = True
            else:
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        ob.hide_select = do_i_hide_select
        else:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        do_i_hide_select2 = not ob.hide_select
                        for ob in bpy.context.scene.objects:
                            ob.hide_select = do_i_hide_select2                    
                        break                
                bpy.context.object.hide_select = False
            else:
                for ob in bpy.context.selected_objects:
                    ob.hide_select = not ob.hide_select
        return {'FINISHED'}      # this lets blender know the operator finished successfully.

def register():
    bpy.utils.register_class(ObjSelectability)


def unregister():
    bpy.utils.unregister_class(ObjSelectability)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()