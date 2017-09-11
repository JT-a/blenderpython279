# メニューに表示されないコマンド

import bpy

################
# オペレーター #
################

class ScrollEnd(bpy.types.Operator):
	bl_idname = "view2d.scroll_end"
	bl_label = "Scroll to end"
	bl_description = "Scroll to the bottom of the screen"
	bl_options = {'UNDO'}
	
	def execute(self, context):
		for i in range(20):
			bpy.ops.view2d.scroll_down(page=True)
		bpy.ops.view2d.scroll_down(page=False)
		return {'FINISHED'}
