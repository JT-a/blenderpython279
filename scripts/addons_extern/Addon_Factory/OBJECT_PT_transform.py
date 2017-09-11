# 「プロパティ」エリア > 「オブジェクト」タブ > 「トランスフォーム」パネル

import bpy

################
# オペレーター #
################

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
		op = row.operator('object.make_link_transform', icon='MAN_TRANS', text="Copy location")
		op.copy_location, op.copy_rotation, op.copy_scale = True, False, False
		op = row.operator('object.make_link_transform', icon='MAN_ROT', text="Rotate copy")
		op.copy_location, op.copy_rotation, op.copy_scale = False, True, False
		op = row.operator('object.make_link_transform', icon='MAN_SCALE', text="Extension of copy")
		op.copy_location, op.copy_rotation, op.copy_scale = False, False, True
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
