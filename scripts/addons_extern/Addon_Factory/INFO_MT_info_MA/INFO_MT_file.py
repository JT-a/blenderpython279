# 情報 > 「ファイル」メニュー

import bpy
import mathutils
import os.path
import os, sys
import subprocess
import fnmatch

################
# オペレーター #
################

class RestartBlender(bpy.types.Operator):
	bl_idname = "wm.restart_blender"
	bl_label = "Reboot"
	bl_description = "Blender Restart"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		py = os.path.join(os.path.dirname(__file__), "console_toggle.py")
		filepath = bpy.data.filepath
		if (filepath != ""):
			subprocess.Popen([sys.argv[0], filepath, '-P', py])
		else:
			subprocess.Popen([sys.argv[0],'-P', py])
		bpy.ops.wm.quit_blender()
		return {'FINISHED'}

class RecoverLatestAutoSave(bpy.types.Operator):
	bl_idname = "wm.recover_latest_auto_save"
	bl_label = "Load last AutoSave"
	bl_description = "Load last AutoSave"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		tempPath = context.user_preferences.filepaths.temporary_directory
		lastFile = None
		for fileName in fnmatch.filter(os.listdir(tempPath), "*.blend"):
			path = os.path.join(tempPath, fileName)
			if (lastFile):
				mtime = os.stat(path).st_mtime
				if (lastTime < mtime and fileName != "quit.blend"):
					lastFile = path
					lastTime = mtime
			else:
				lastFile = path
				lastTime = os.stat(path).st_mtime
		bpy.ops.wm.recover_auto_save(filepath=lastFile)
		self.report(type={"INFO"}, message="Load last AutoSave file")
		return {'FINISHED'}

class SaveMainfileUnmassage(bpy.types.Operator):
	bl_idname = "wm.save_mainfile_unmassage"
	bl_label = "Save Without Prompt"
	bl_description = "Save the changes without displaying the confirmation message"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		if (bpy.data.filepath != ""):
			bpy.ops.wm.save_mainfile()
			self.report(type={"INFO"}, message=bpy.path.basename(bpy.data.filepath)+" Has been saved")
		else:
			self.report(type={"ERROR"}, message="To save your find")
		return {'FINISHED'}

##############################
# オペレーター(オブジェクト) #
##############################



def menu(self, context):

	self.layout.separator()
	self.layout.operator(RestartBlender.bl_idname, icon="COLOR_GREEN")
	self.layout.operator('wm.save_userpref', icon='SAVE_COPY')
	self.layout.separator()
	self.layout.operator(SaveMainfileUnmassage.bl_idname, icon="FILE_TICK")
	self.layout.operator(RecoverLatestAutoSave.bl_idname, icon="RECOVER_AUTO")


