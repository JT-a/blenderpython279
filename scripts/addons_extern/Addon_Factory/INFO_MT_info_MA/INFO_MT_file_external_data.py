# 情報 > 「ファイル」メニュー > 「外部データ」メニュー

import bpy
import os, shutil

################
# オペレーター #
################

class ResaveAllImage(bpy.types.Operator):
	bl_idname = "image.resave_all_image"
	bl_label = "Resave textures folder, all images"
	bl_description = "All external files referenced by image data to resave the textures folder"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(cls, context):
		if (context.blend_data.filepath == ""):
			return False
		for img in bpy.data.images:
			if (img.filepath != ""):
				return True
		return False
	def execute(self, context):
		for img in context.blend_data.images:
			if (img.filepath != ""):
				try:
					img.pack()
					img.unpack()
				except RuntimeError:
					pass
		self.report(type={"INFO"}, message="repaired and stored in the textures folder")
		return {'FINISHED'}

class IsolationTexturesUnusedFiles(bpy.types.Operator):
	bl_idname = "image.isolation_textures_unused_files"
	bl_label = "isolate unused files in the textures folder"
	bl_description = "Files in a textures folder with the Blend files, do not use isolates them in a backup folder"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(cls, context):
		path = context.blend_data.filepath
		if (context.blend_data.filepath == ""):
			return False
		dir = os.path.dirname(path)
		if (not os.path.isdir( os.path.join(dir, "textures") )):
			return False
		for img in bpy.data.images:
			if (img.filepath != ""):
				return True
		return False
	def execute(self, context):
		names = []
		for img in context.blend_data.images:
			if (img.filepath != ""):
				names.append(bpy.path.basename(img.filepath))
		tex_dir = os.path.join( os.path.dirname(context.blend_data.filepath), "textures")
		backup_dir = os.path.join(tex_dir, "backup")
		if (not os.path.isdir(backup_dir)):
			os.mkdir(backup_dir)
		for name in os.listdir(tex_dir):
			path = os.path.join(tex_dir, name)
			if (not os.path.isdir(path)):
				if (name not in names):
					src = path
					dst = os.path.join(path, backup_dir, name)
					shutil.move(src, dst)
					self.report(type={'INFO'}, message=name+"Isolation")
		return {'FINISHED'}

class OpenRecentFiles(bpy.types.Operator):
	bl_idname = "wm.open_recent_files"
	bl_label = "Open text in \"recent files\""
	bl_description = "Open the \"recent files\" in Blender text editor"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		path = os.path.join(bpy.utils.user_resource('CONFIG'), "recent-files.txt")
		pre_texts = context.blend_data.texts[:]
		bpy.ops.text.open(filepath=path)
		for text in context.blend_data.texts[:]:
			for pre in pre_texts:
				if (text.name == pre.name):
					break
			else:
				new_text = text
				break
		max_area = 0
		target_area = None
		for area in context.screen.areas:
			if (area.type == 'TEXT_EDITOR'):
				target_area = area
				break
			if (max_area < area.height * area.width):
				max_area = area.height * area.width
				target_area = area
		target_area.type = 'TEXT_EDITOR'
		for space in target_area.spaces:
			if (space.type == 'TEXT_EDITOR'):
				space.text = new_text
		return {'FINISHED'}

class OpenBookmarkText(bpy.types.Operator):
	bl_idname = "wm.open_bookmark_text"
	bl_label = "Open text in \"bookmarks\""
	bl_description = "Blender text editor open the file browser bookmarks"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		path = os.path.join(bpy.utils.user_resource('CONFIG'), "bookmarks.txt")
		pre_texts = context.blend_data.texts[:]
		bpy.ops.text.open(filepath=path)
		for text in context.blend_data.texts[:]:
			for pre in pre_texts:
				if (text.name == pre.name):
					break
			else:
				new_text = text
				break
		max_area = 0
		target_area = None
		for area in context.screen.areas:
			if (area.type == 'TEXT_EDITOR'):
				target_area = area
				break
			if (max_area < area.height * area.width):
				max_area = area.height * area.width
				target_area = area
		target_area.type = 'TEXT_EDITOR'
		for space in target_area.spaces:
			if (space.type == 'TEXT_EDITOR'):
				space.text = new_text
		return {'FINISHED'}


def menu(self, context):

	self.layout.separator()
	self.layout.operator('image.reload_all_image')
	self.layout.separator()
	self.layout.operator(ResaveAllImage.bl_idname)
	self.layout.operator(IsolationTexturesUnusedFiles.bl_idname)
	self.layout.separator()
	self.layout.operator(OpenRecentFiles.bl_idname)
	self.layout.operator(OpenBookmarkText.bl_idname)

