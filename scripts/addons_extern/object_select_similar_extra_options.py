bl_info = {
    "name": "Select Similar for Bones, more options",
    "description": "The select similar tool for armatures could get more options.",
    "author": "Valera Likhosherstov",
    "version": (1, 0),
    "blender": (2, 73, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
}

import bpy


class BonesExtraSelectSimilar(bpy.types.Operator):
    """Additional options for select_similar operator for Bones"""
    bl_idname = 'armature.select_similar_extra_options'
    bl_label = 'Select Similar Extra Options'
    bl_options = {'REGISTER', 'UNDO'}

    prop_type = bpy.props.StringProperty(name="type",
                                         description="(enum in [‘LENGTH’, ‘DIRECTION’, ‘PREFIX’, ‘SUFFIX’, ‘LAYER’], (optional)) – Type",
                                         default="LENGTH")

    threshold = bpy.props.FloatProperty(name="threshold",
                                        description="(float in [0, 1], (optional)) – Threshold",
                                        default=0.1, min=0.0)

    #  Extra options for search
    search_set = bpy.props.StringProperty(name="search_set",
                                          description="(enum in ['ALL', 'GROUP', 'CHILDREN', 'IMMEDIATE-CHILDREN', 'SIBLINGS']) - Search Set",
                                          default="ALL")

    def deselect_bone(self, bone):
        bone.select = False
        if bone.parent is None:
            bone.select_head = False
        else:
            if not bone.parent.select:
                bone.parent.select_tail = False
        selected_child = False
        for child in bone.children:
            selected_child |= child.select
        bone.select_tail = selected_child

    def filter_selected_as_group(self, active_pose_bone, context):
        for selected_pose_bone in context.selected_pose_bones:
            gr1 = active_pose_bone.bone_group
            gr2 = selected_pose_bone.bone_group
            #  If groups don't exist or are not equal
            if (gr1 is None) or (gr2 is None) or (gr1.name != gr2.name):
                self.deselect_bone(selected_pose_bone.bone)

    def filter_selected_as_children(self, active_bone, context):
        for selected_bone in context.selected_bones:
            if selected_bone not in active_bone.children_recursive:
                self.deselect_bone(selected_bone)

    def filter_selected_as_immediate_children(self, active_bone, context):
        print('Active bone: ' + active_bone.name)
        for selected_bone in context.selected_bones:
            if selected_bone not in active_bone.children:
                self.deselect_bone(selected_bone)

    def filter_selected_as_siblings(self, active_bone, context):
        parent = active_bone.parent
        for selected_bone in context.selected_bones:
            if (parent is None) or (selected_bone not in parent.children):
                self.deselect_bone(selected_bone)

    def execute(self, context):
        if self.search_set == 'GROUP':
            bpy.ops.object.mode_set(mode='POSE')
            active_pose_bone = context.active_pose_bone
            bpy.ops.object.mode_set(mode='EDIT')
            if active_pose_bone is not None:
                bpy.ops.armature.select_similar(type=self.prop_type, threshold=self.threshold)
                bpy.ops.object.mode_set(mode='POSE')
                self.filter_selected_as_group(active_pose_bone, context)
                bpy.ops.object.mode_set(mode='EDIT')
        else:
            active_bone = bpy.context.active_bone
            if active_bone is not None:
                bpy.ops.armature.select_similar(type=self.prop_type, threshold=self.threshold)
                if self.search_set == 'CHILDREN':
                    self.filter_selected_as_children(active_bone, context)
                elif self.search_set == 'IMMEDIATE-CHILDREN':
                    self.filter_selected_as_immediate_children(active_bone, context)
                elif self.search_set == 'SIBLINGS':
                    self.filter_selected_as_siblings(active_bone, context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(BonesExtraSelectSimilar)


def unregister():
    bpy.utils.unregister_class(BonesExtraSelectSimilar)

if __name__ == '__main__':
    register()
