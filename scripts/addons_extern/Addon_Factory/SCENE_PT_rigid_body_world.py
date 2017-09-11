# 「プロパティ」エリア > 「シーン」タブ > 「剛体ワールド」パネル

import bpy

################
# オペレーター #
################

class WorldReset(bpy.types.Operator):
	bl_idname = "rigidbody.world_reset"
	bl_label = "Recreate the rigid world"
	bl_description = "Keep setting, recreate the rigid world"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (not context.scene.rigidbody_world):
			return False
		return context.scene.rigidbody_world.enabled
	def execute(self, context):
		group = context.scene.rigidbody_world.group
		constraints = context.scene.rigidbody_world.constraints
		time_scale = context.scene.rigidbody_world.time_scale
		steps_per_second = context.scene.rigidbody_world.steps_per_second
		use_split_impulse = context.scene.rigidbody_world.use_split_impulse
		solver_iterations = context.scene.rigidbody_world.solver_iterations
		frame_start = context.scene.rigidbody_world.point_cache.frame_start
		frame_end = context.scene.rigidbody_world.point_cache.frame_end
		
		bpy.ops.rigidbody.world_remove()
		bpy.ops.rigidbody.world_add()
		
		context.scene.rigidbody_world.group = group
		context.scene.rigidbody_world.constraints = constraints
		context.scene.rigidbody_world.time_scale = time_scale
		context.scene.rigidbody_world.steps_per_second = steps_per_second
		context.scene.rigidbody_world.use_split_impulse = use_split_impulse
		context.scene.rigidbody_world.solver_iterations = solver_iterations
		context.scene.rigidbody_world.point_cache.frame_start = frame_start
		context.scene.rigidbody_world.point_cache.frame_end = frame_end
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
		self.layout.operator(WorldReset.bl_idname, icon='PLUGIN')
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
