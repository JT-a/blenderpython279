bl_info = {
    "name": "Container",
    "author": "Paweł Łyczkowski",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "View3D",
    "description": "Quickly group objects in a container object",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
}


import bpy
import bpy.ops
import bpy.props


class PlaceInContainer(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "TODO"
    bl_idname = "object.place_in_container"
    bl_label = "Place In Container"
    bl_options = {'REGISTER', 'UNDO'}

    container_name = bpy.props.StringProperty(name="Name", default="Container")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        contents = bpy.context.selected_objects

        # Create a temporary joined object
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False,
                                                           "mode": 'TRANSLATION'},
                                      TRANSFORM_OT_translate={"value": (0, 0, 0), "constraint_axis": (False, False, False),
                                                              "constraint_orientation": 'GLOBAL', "mirror": False,
                                                              "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH',
                                                              "proportional_size": 1, "snap": False,
                                                              "snap_target": 'CLOSEST', "snap_point": (0, 0, 0),
                                                              "snap_align": False, "snap_normal": (0, 0, 0),
                                                              "gpencil_strokes": False, "texture_space": False,
                                                              "remove_on_cancel": False, "release_confirm": False})
        bpy.ops.object.modifier_apply()

        bpy.ops.object.join()
        temp_joined_object = bpy.context.active_object

        # Create a bound box around the temporary joined object
        selected = bpy.context.selected_objects
        for obj in selected:
            # ensure origin is centered on bounding box center
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            # create a cube for the bounding box
            bpy.ops.mesh.primitive_cube_add()
            # our new cube is now the active object, so we can keep track of it in a variable:
            bound_box = bpy.context.active_object

            # copy transforms
            bound_box.dimensions = obj.dimensions
            bound_box.location = obj.location
            bound_box.rotation_euler = obj.rotation_euler
            bound_box.draw_type = 'BOUNDS'
            bound_box.name = self.container_name
            bound_box.hide_render = True

        # Delete the temporary joined object
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = temp_joined_object
        temp_joined_object.select = True
        bpy.ops.object.delete(use_global=False)

        # Parent the contents to the bounding box
        for obj in contents:
            obj.select = True
        bpy.context.scene.objects.active = bound_box
        bound_box.select = True
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

        # Make contents unselectable
        for obj in contents:
            obj.hide_select = True
            obj.select = False

        return {'FINISHED'}


class OpenContainer(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "TODO"
    bl_idname = "object.open_container"
    bl_label = "Open Container"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        container = bpy.context.scene.objects.active

        for obj in bpy.data.objects:
            if obj.parent == container:
                obj.hide_select = False
                obj.select = True

        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        bpy.ops.object.select_all(action='DESELECT')
        container.select = True
        bpy.ops.object.delete(use_global=False)

        return {'FINISHED'}


class ContainerPanel(bpy.types.Panel):
    bl_label = "Container Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        layout.operator('object.place_in_container')
        layout.operator('object.open_container')


def register():
    bpy.utils.register_class(PlaceInContainer)
    bpy.utils.register_class(OpenContainer)
    bpy.utils.register_class(ContainerPanel)


def unregister():
    bpy.utils.unregister_class(OpenContainer)
    bpy.utils.unregister_class(PlaceInContainer)
    bpy.utils.unregister_class(ContainerPanel)


if __name__ == "__main__":
    register()
