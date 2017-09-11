# 3Dビュー > アーマチュア編集モード > 「選択」メニュー

import bpy

################
# オペレーター #
################

class SelectAxisOver(bpy.types.Operator):
	bl_idname = "armature.select_axis_over"
	bl_label = "Select the right half"
	bl_description = "Select the right half of the bone (and other settings too)"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		("0", "The x axis", "", 1),
		("1", "Y軸", "", 2),
		("2", "Z軸", "", 3),
		]
	axis = bpy.props.EnumProperty(items=items, name="Axis")
	items = [
		("-1", "-(Minus)", "", 1),
		("1", "+ (Plus)", "", 2),
		]
	direction = bpy.props.EnumProperty(items=items, name="Direction")
	offset = bpy.props.FloatProperty(name="Offset", default=0, step=10, precision=3)
	threshold = bpy.props.FloatProperty(name="Threshold", default=-0.0001, step=0.01, precision=4)
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode="OBJECT")
		activeObj = context.active_object
		arm = activeObj.data
		direction = int(self.direction)
		offset = self.offset
		threshold = self.threshold
		for bone in arm.bones:
			hLoc = bone.head_local[int(self.axis)]
			tLoc = bone.tail_local[int(self.axis)]
			if (offset * direction <= hLoc * direction + threshold):
				bone.select = True
			if (offset * direction <= tLoc * direction + threshold):
				bone.select = True
		bpy.ops.object.mode_set(mode="EDIT")
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
		self.layout.operator('pose.select_path', icon='PLUGIN')
		self.layout.operator(SelectAxisOver.bl_idname, icon='PLUGIN')
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
