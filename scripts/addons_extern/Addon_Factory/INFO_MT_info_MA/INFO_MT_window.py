# 情報 > 「ウィンドウ」メニュー

import bpy

################
# パイメニュー #
################



################
# オペレーター #
################

class ToggleJapaneseInterface(bpy.types.Operator):
	bl_idname = "wm.toggle_japanese_interface"
	bl_label = "English UI, Japanese switch"
	bl_description = "Japan language with English interface switch"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		if (not bpy.context.user_preferences.system.use_international_fonts):
			bpy.context.user_preferences.system.use_international_fonts = True
		if (bpy.context.user_preferences.system.language != "ja_JP"):
			bpy.context.user_preferences.system.language = "ja_JP"
		bpy.context.user_preferences.system.use_translate_interface = not bpy.context.user_preferences.system.use_translate_interface
		return {'FINISHED'}


def menu(self, context):

	self.layout.separator()
	self.layout.operator(ToggleJapaneseInterface.bl_idname, icon="FILE_REFRESH")
	self.layout.separator()

