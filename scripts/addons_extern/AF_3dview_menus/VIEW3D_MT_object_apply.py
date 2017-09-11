# 3Dビュー > オブジェクトモード > Ctrl+Aキー

if "bpy" in locals():
    import importlib
    importlib.reload(apply_transform_multiuser)

else:
    from . import apply_transform_multiuser

import bpy

################
# オペレーター #
################

class TransformApplyAll(bpy.types.Operator):
	bl_idname = "object.transform_apply_all"
	bl_label = "Apply position / rotation / scaling"
	bl_description = "I apply the position / rotation / scaling of objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
		return {'FINISHED'}



# menu
def menu(self, context):

	self.layout.separator()
	operator = self.layout.operator(TransformApplyAll.bl_idname, text="Loc/Rot/scale")
	self.layout.separator()
	self.layout.menu("VIEW3D_MT_object_apply_transform_multiuser")
