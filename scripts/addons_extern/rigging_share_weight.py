import bpy

bl_info = {
    "name": "Share weight",
    "author": "SolPie",
    "version": (1, 2),
    "blender": (2, 69, 0),
    "location": "View3D > Specials > Share weight",
    "description": "Share weight",
    "warning": "",
    "category": "Rigging"}


def auto_weight():
    scn = bpy.context.scene
    ob_edit = bpy.context.active_object
    ob_mesh = None

    # find ob_mesh
    obs = bpy.context.selected_objects
    for ob in obs:
        if ob == ob_edit:
            pass
        else:
            ob_mesh = ob
    ob_mesh.select = False
    # collection select bone name
    bone_sels = []
    for bone in bpy.context.editable_bones:
        bone_sels.append(bone)

    # delete unselected bone
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.duplicate()
    bpy.ops.object.mode_set(mode='EDIT')

    # arm = bpy.data.armatures["Armature"]
    arm = bpy.context.editable_bones[0].id_data
    for bone in arm.edit_bones:
        is_del = True
        for bone_sel in bone_sels:
            if bone_sel.name == bone.name:
                is_del = False
                break
        if is_del:
            # bpy.data.armatures["Armature"].edit_bones.remove()
            arm.edit_bones.remove(bone)

    bpy.ops.object.mode_set(mode='OBJECT')

    tmp_armature = bpy.context.active_object
    print(ob_edit, ob_mesh, tmp_armature)

    # Auto weight
    ob_edit.select = False
    ob_mesh.select = True
    tmp_armature.select = True
    scn.objects.active = tmp_armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    ob_mesh.modifiers[-1].object = bpy.data.objects[ob_edit.name]

    ob_edit.select = True
    ob_mesh.select = True
    tmp_armature.select = False
    scn.objects.active = ob_edit
    bpy.ops.object.parent_set(type='ARMATURE', keep_transform=False)

    # delete tmp armature
    ob_edit.select = False
    ob_mesh.select = False
    tmp_armature.select = True
    scn.objects.active = tmp_armature
    bpy.ops.object.delete(use_global=False)

    # pose mode
    scn.objects.active = ob_edit
    ob_edit.select = True
    bpy.ops.object.posemode_toggle()


class ShareWeight(bpy.types.Operator):
    bl_idname = 'armature.sharewight'
    bl_label = 'share weight from one armature'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'ARMATURE')

    def execute(self, context):
        auto_weight()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ShareWeight.bl_idname, text="Share weight")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_armature_specials.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_armature_specials.remove(menu_func)
