# 「プロパティ」エリア > 「アーマチュアデータ」タブ > 「ボーングループ」パネル

import bpy

################
# オペレーター #
################

class BoneGroupOnlyShow(bpy.types.Operator):
	bl_idname = "pose.bone_group_only_show"
	bl_label = "Show only bone bones group"
	bl_description = "Group active on bones and the bones of other hide"
	bl_options = {'REGISTER', 'UNDO'}
	
	reverse = bpy.props.BoolProperty(name="Flip", default=False)
	
	@classmethod
	def poll(cls, context):
		if (context.active_object):
			if (context.active_object.type == 'ARMATURE'):
				if (len(context.active_object.pose.bone_groups)):
					return True
		return False
	
	def execute(self, context):
		obj = context.active_object
		arm = obj.data
		for pbone in obj.pose.bones:
			bone = arm.bones[pbone.name]
			for i in range(len(arm.layers)):
				if (arm.layers[i] and bone.layers[i]):
					if (not pbone.bone_group):
						if (not self.reverse):
							bone.hide = True
						else:
							bone.hide = False
						break
					if (obj.pose.bone_groups.active.name == pbone.bone_group.name):
						if (not self.reverse):
							bone.hide = False
						else:
							bone.hide = True
					else:
						if (not self.reverse):
							bone.hide = True
						else:
							bone.hide = False
					break
		return {'FINISHED'}

class BoneGroupShow(bpy.types.Operator):
	bl_idname = "pose.bone_group_show"
	bl_label = "Bones bones group show"
	bl_description = "Active bone group show or hide"
	bl_options = {'REGISTER', 'UNDO'}
	
	reverse = bpy.props.BoolProperty(name="Flip", default=False)
	
	@classmethod
	def poll(cls, context):
		if (context.active_object):
			if (context.active_object.type == 'ARMATURE'):
				if (len(context.active_object.pose.bone_groups)):
					return True
		return False
	
	def execute(self, context):
		obj = context.active_object
		arm = obj.data
		for pbone in obj.pose.bones:
			bone = arm.bones[pbone.name]
			for i in range(len(arm.layers)):
				if (arm.layers[i] and bone.layers[i]):
					if (pbone.bone_group):
						if (obj.pose.bone_groups.active.name == pbone.bone_group.name):
							if (not self.reverse):
								bone.hide = False
							else:
								bone.hide = True
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
		row = self.layout.row()
		sub = row.row(align=True)
		sub.operator(BoneGroupShow.bl_idname, icon='RESTRICT_VIEW_OFF', text="Says").reverse = False
		sub.operator(BoneGroupShow.bl_idname, icon='RESTRICT_VIEW_ON', text="Hide").reverse = True
		sub = row.row(align=True)
		sub.operator(BoneGroupOnlyShow.bl_idname, icon='RESTRICT_VIEW_OFF', text="Only display").reverse = False
		sub.operator(BoneGroupOnlyShow.bl_idname, icon='RESTRICT_VIEW_ON', text="Only hide").reverse = True
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
