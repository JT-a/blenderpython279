import bpy

bl_info = {
    "name": "Attach bone",
    "author": "SolPie",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "View3D > Specials > Attach bone",
    "description": "attach one bone to another",
    "warning": "",
    "category": "Rigging"}


def attach(context):
    scn = bpy.context.scene
    ops = bpy.ops
    edit_ob = context.active_object
    obs = context.selected_objects
    for obj in obs:
        scn.objects.active = obj
        if obj == edit_ob:
            edit_bone = context.active_bone
        else:
            target_ob = obj
    print(edit_ob, target_ob)
    # print(edit_bone, target_bone)

    def snap_head(select_head=True):
        bpy.ops.object.editmode_toggle()
        scn.objects.active = target_ob
        target_ob.select = True
        edit_ob.select = False
        bpy.ops.object.editmode_toggle()
        target_bone = context.active_bone
        bpy.ops.armature.select_all(action='DESELECT')
        target_bone.select_head = select_head
        target_bone.select_tail = not select_head
        # print(target_bone, target_bone.select, target_bone.select_head, target_bone.select_tail)
        bpy.ops.view3d.snap_cursor_to_selected()
        # snap head to cursor
        bpy.ops.object.editmode_toggle()
        scn.objects.active = edit_ob
        target_ob.select = False
        edit_ob.select = True
        bpy.ops.object.editmode_toggle()
        edit_bone = context.active_bone
        bpy.ops.armature.select_all(action='DESELECT')
        edit_bone.select_head = select_head
        edit_bone.select_tail = not select_head
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        # set roll
        edit_bone.roll = target_bone.roll

        # snap cursor to head
    snap_head(True)
    snap_head(False)


class AttachBone(bpy.types.Operator):
    bl_idname = 'armature.attachbone'
    bl_label = 'attach one bone to another'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'ARMATURE')

    def execute(self, context):
        attach(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AttachBone.bl_idname, text="Attach bone")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_armature_specials.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_armature_specials.remove(menu_func)
