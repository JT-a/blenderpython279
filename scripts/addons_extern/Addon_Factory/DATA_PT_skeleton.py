# 「プロパティ」エリア > 「アーマチュアデータ」タブ > 「スケルトン」パネル

import bpy

################
# オペレーター #
################

class ShowAllBoneLayers(bpy.types.Operator):
	bl_idname = "pose.show_all_bone_layers"
	bl_label = "View all bone layer"
	bl_description = "All the bone layer and then displays the"
	bl_options = {'REGISTER'}
	
	layers = [False] * 32
	layers[0] = True
	pre_layers = bpy.props.BoolVectorProperty(name="The last layer information", size=32, default=layers[:])
	
	@classmethod
	def poll(cls, context):
		if (context.object):
			if (context.object.type == 'ARMATURE'):
				return True
		return False
	
	def execute(self, context):
		if (all(context.object.data.layers)):
			context.object.data.layers = self.pre_layers[:]
			self.report(type={'INFO'}, message="Unlock all layers display")
		else:
			self.pre_layers = context.object.data.layers[:]
			for i in range(len(context.object.data.layers)):
				context.object.data.layers[i] = True
			self.report(type={'WARNING'}, message="All layers display")
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
		row = self.layout.row(align=True)
		row.operator('pose.toggle_pose_position', icon='POSE_HLT', text="Enables or disables the pause")
		row.operator(ShowAllBoneLayers.bl_idname, icon='RESTRICT_VIEW_OFF', text="All layers display")
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
