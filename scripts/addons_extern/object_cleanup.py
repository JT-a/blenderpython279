bl_info = {
    'name': 'Obj Import files Clean Up',
    'author': 'Ethan Luo, congcong009, (http://www.blenderget.com)',
    'version': (0, 1),
    "blender": (2, 6, 5),
    "api": 52859,
    'location': '',
    'description': 'Convert Tris to Quads faces and Remove Doubles for imported OBJ objects',
    'warning': 'Only working for MESH object',
    'category': 'Mesh'}


import bpy


def tris2Face():

    if bpy.ops.mesh.tris_convert_to_quads.poll():
        bpy.ops.mesh.tris_convert_to_quads()
    print("tris convert done")

    return


def removeDoubleVe():

    if bpy.ops.mesh.remove_doubles.poll():
        bpy.ops.mesh.remove_doubles()
    print("remove done")

    return


def oneButtonCleanUp(object):

    # bpy.ops.object.editmode_toggle()
    if bpy.ops.object.mode_set.poll() == False:
        bpy.ops.object.mode_set.poll = True
        object
        ob.select = True
        ob = bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
    else:
        bpy.ops.object.mode_set(mode='EDIT')

    if bpy.ops.mesh.select_all.poll():
        bpy.ops.mesh.select_all(action='SELECT')

    tris2Face()
    removeDoubleVe()

    bpy.ops.object.mode_set(mode='OBJECT')

    return object


class OneButtonCleanUp(bpy.types.Operator):
    bl_label = "Clean and Tris Convert"
    bl_options = {'REGISTER'}
    bl_idname = "object.onebuttonclean"

    def execute(self, context):

        scn = bpy.context.scene

        for ob in scn.objects:
            if ob.type == 'MESH':
                oneButtonCleanUp(ob)

        return {'FINISHED'}


class ObjectCleanUpPanel(bpy.types.Panel):

    bl_label = "Obj Clean Up Panel"
    bl_region_type = "TOOLS"
    bl_space_type = "VIEW_3D"

    def draw(self, context):
        scn = context.scene
        new_row = self.layout.row

        new_row().operator("object.onebuttonclean")


def register():
    bpy.utils.register_class(OneButtonCleanUp)
    bpy.utils.register_class(ObjectCleanUpPanel)


def unregister():
    bpy.utils.register_class(OneButtonCleanUp)
    bpy.utils.register_class(ObjectCleanUpPanel)


if __name__ == '__main__':
    register()
