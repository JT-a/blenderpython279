# 「3Dビュー」エリア > プロパティパネル > 「アイテム」パネル
bl_info = {
    "name": "Data Re-Name",
    "author": "saidenka",
    "version": (0, 1),
    "blender": (2, 73),
    "location": "Item Panel",
    "description": "Match Data/Object names",
    "warning": "",
    "wiki_url": "",
    "category": "Item"
}
import bpy
from ..utils import AddonPreferences, SpaceProperty


class DataNameToObjectName(bpy.types.Operator):
    bl_idname = "object.data_name_to_object_name"
    bl_label = "Object names in the data name"
    bl_description = "Set the data name linked to object name"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (not context.object):
            return False
        if (not context.object.data):
            return False
        if (context.object.name == context.object.data.name):
            return False
        return True

    def execute(self, context):
        context.object.name = context.object.data.name
        return {'FINISHED'}


class ObjectNameToDataName(bpy.types.Operator):
    bl_idname = "object.object_name_to_data_name"
    bl_label = "Data name in the object name"
    bl_description = "Sets the data linked to the object name"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (not context.object):
            return False
        if (not context.object.data):
            return False
        if (context.object.name == context.object.data.name):
            return False
        return True

    def execute(self, context):
        context.object.data.name = context.object.name
        return {'FINISHED'}


class CopyObjectName(bpy.types.Operator):
    bl_idname = "object.copy_object_name"
    bl_label = "Copy the object name"
    bl_description = "Copy to the Clipboard object name"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        if (not context.object):
            return False
        if (context.window_manager.clipboard == context.object.name):
            return False
        return True

    def execute(self, context):
        context.window_manager.clipboard = context.object.name
        self.report(type={'INFO'}, message=context.object.name)
        return {'FINISHED'}


class CopyDataName(bpy.types.Operator):
    bl_idname = "object.copy_data_name"
    bl_label = "Copy the data name"
    bl_description = "Copies data to the Clipboard"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        if (not context.object):
            return False
        if (not context.object.data):
            return False
        if (context.window_manager.clipboard == context.object.data.name):
            return False
        return True

    def execute(self, context):
        context.window_manager.clipboard = context.object.data.name
        self.report(type={'INFO'}, message=context.object.data.name)
        return {'FINISHED'}

# メニューを登録する関数


def menu(self, context):

    row = self.layout.row(align=True)
    row.alignment = 'LEFT'
    row.label("Copy Data", icon='COPYDOWN')
    row.operator('object.copy_object_name', icon='OBJECT_DATAMODE', text="")
    if (context.active_bone or context.active_pose_bone):
        row.operator('object.copy_bone_name', icon='BONE_DATA', text="")
    row.operator('object.copy_data_name', icon='EDITMODE_HLT', text="")
    row = self.layout.row(align=True)
    row.alignment = 'LEFT'
    row.label("Name Sync", icon='LINKED')
    row.operator('object.object_name_to_data_name', icon='TRIA_DOWN_BAR', text="")
    row.operator('object.data_name_to_object_name', icon='TRIA_UP_BAR', text="")
#	self.layout.template_ID(context.object, 'data')

classes = [
    DataNameToObjectName,
    ObjectNameToDataName,
    CopyObjectName,
    CopyDataName,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    pass
    bpy.types.VIEW3D_PT_view3d_name.append(menu)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    pass
    bpy.types.VIEW3D_PT_view3d_name.remove(menu)

if __name__ == "__main__":
    register()
