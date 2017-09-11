# UV/画像エディター > 「画像」メニュー

import bpy
import os

################
# オペレーター #
################

class ProjectEditEX(bpy.types.Operator):
	bl_idname = "image.project_edit_ex"
	bl_label = "Quick Edit (extend)"
	bl_description = "Do the quick editing in an external editor of the additional files page of the custom"
	bl_options = {'REGISTER'}
	
	index = bpy.props.IntProperty(name="Number to use", default=1, min=1, max=3, soft_min=1, soft_max=3)
	
	def execute(self, context):
		pre_path = context.user_preferences.filepaths.image_editor
		if (self.index == 1):
			context.user_preferences.filepaths.image_editor = context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_1
		elif (self.index == 2):
			context.user_preferences.filepaths.image_editor = context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_2
		elif (self.index == 3):
			context.user_preferences.filepaths.image_editor = context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_3
		bpy.ops.image.project_edit()
		context.user_preferences.filepaths.image_editor = pre_path
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
		col = self.layout.column(align=True)
		col.label(text="Add Quick Edit", icon='PLUGIN')
		if (context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_1):
			path = os.path.basename(context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_1)
			name, ext = os.path.splitext(path)
			col.operator(ProjectEditEX.bl_idname, icon="PLUGIN", text=name).index = 1
		if (context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_2):
			path = os.path.basename(context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_2)
			name, ext = os.path.splitext(path)
			col.operator(ProjectEditEX.bl_idname, icon="PLUGIN", text=name).index = 2
		if (context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_3):
			path = os.path.basename(context.user_preferences.addons["Addon_Factory"].preferences.image_editor_path_3)
			name, ext = os.path.splitext(path)
			col.operator(ProjectEditEX.bl_idname, icon="PLUGIN", text=name).index = 3
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
