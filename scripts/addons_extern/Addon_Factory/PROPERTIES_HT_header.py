# プロパティ > ヘッダー

import bpy

################
# オペレーター #
################

class ChangeContextTab(bpy.types.Operator):
	bl_idname = "buttons.change_context_tab"
	bl_label = "Switch to properties tab"
	bl_description = "Turn switch Properties tab"
	bl_options = {'REGISTER'}
	
	is_left = bpy.props.BoolProperty(name="To the left", default=False)
	
	def execute(self, context):
		space_data = None
		for area in context.screen.areas:
			if (area.type == 'PROPERTIES'):
				for space in area.spaces:
					if (space.type == 'PROPERTIES'):
						space_data = space
						break
				else:
					continue
				break
		if (not space_data):
			self.report(type={'ERROR'}, message="Cannot find the properties area")
			return {'CANCELLED'}
		now_tab = space_data.context
		tabs = ['RENDER', 'RENDER_LAYER', 'SCENE', 'WORLD', 'OBJECT', 'CONSTRAINT', 'MODIFIER', 'DATA', 'BONE', 'BONE_CONSTRAINT', 'MATERIAL', 'TEXTURE', 'PARTICLES', 'PHYSICS']
		if (now_tab not in tabs):
			self.report(type={'ERROR'}, message="Is the current tab is unexpected")
			return {'CANCELLED'}
		if (self.is_left):
			tabs.reverse()
		index = tabs.index(now_tab) + 1
		for i in range(len(tabs)):
			try:
				space_data.context = tabs[index]
				break
			except TypeError:
				index += 1
			except IndexError:
				index = 0
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
		row.operator(ChangeContextTab.bl_idname, text="", icon='TRIA_LEFT').is_left = True
		row.operator(ChangeContextTab.bl_idname, text="", icon='TRIA_RIGHT').is_left = False
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
