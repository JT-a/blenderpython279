# 「3Dビュー」エリア > テクスチャペイント > ツールシェルフ > 「データなし」パネル

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
		if (context.object):
			if (context.object.active_material):
				if (context.object.active_material.use_nodes):
					self.layout.prop(context.object.active_material, 'use_nodes', icon='PLUGIN', text="Because the nodes used in non-")
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
