# 3Dビュー > アーマチュア編集モード > 「アーマチュア」メニュー

import bpy

##############
# その他関数 #
##############

################
# オペレーター #
################

class DeleteUnmassage(bpy.types.Operator):
	bl_idname = "armature.delete_unmassage"
	bl_label = "Remove the bones with no confirmation"
	bl_description = "Remove the bones with no verification"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.armature.delete()
		return {'FINISHED'}

class Move3DCursor(bpy.types.Operator):
	bl_idname = "armature.move_3d_cursor"
	bl_label = "Bones intact to position the 3D cursor"
	bl_description = "Position of relative born tail (even root), bone, 3 D move cursor position"
	bl_options = {'REGISTER', 'UNDO'}
	
	isTail = bpy.props.BoolProperty(name="Move the tail", default=False)
	
	def execute(self, context):
		for bone in context.selected_bones:
			if (not self.isTail):
				co = bone.tail - bone.head
				bone.head = context.space_data.cursor_location
				bone.tail = context.space_data.cursor_location + co
			else:
				co = bone.head - bone.tail
				bone.head = context.space_data.cursor_location + co
				bone.tail = context.space_data.cursor_location
		return {'FINISHED'}

################
# メニュー追加 #
################

# メニューのオン/オフの判定
def IsMenuEnable(self_id):
	for id in bpy.context.user_preferences.addons["Addon_Factory"].preferences.disabled_menu.split(','):
		if (id == self_id):
			return False
	else:
		return True

# メニューを登録する関数
def menu(self, context):
	if (IsMenuEnable(__name__.split('.')[-1])):
		self.layout.separator()
		self.layout.operator(DeleteUnmassage.bl_idname, icon="PLUGIN")
		self.layout.separator()
		self.layout.operator(Move3DCursor.bl_idname, icon="PLUGIN")
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
