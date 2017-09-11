# 「プロパティ」エリア > 「ボーン」タブ

import bpy
import re

################
# オペレーター #
################

class CopyBoneName(bpy.types.Operator):
	bl_idname = "object.copy_bone_name"
	bl_label = "Copy to Clipboard bone name"
	bl_description = "To the Clipboard copies the bone name"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (context.active_bone):
			if (context.window_manager.clipboard != context.active_bone.name):
				return True
		if (context.active_pose_bone):
			if (context.window_manager.clipboard != context.active_pose_bone.name):
				return True
		return False
	
	def execute(self, context):
		if (context.active_bone):
			context.window_manager.clipboard = context.active_bone.name
			self.report(type={'INFO'}, message=context.active_bone.name)
		elif (context.active_pose_bone):
			context.window_manager.clipboard = context.active_pose_bone.name
			self.report(type={'INFO'}, message=context.active_pose_bone.name)
		return {'FINISHED'}

class RenameMirrorActiveBone(bpy.types.Operator):
	bl_idname = "pose.rename_mirror_active_bone"
	bl_label = "Flip the bone name"
	bl_description = "The bone name Active Flip"
	bl_options = {'REGISTER', 'UNDO'}
	
	def CheckIsMirror(name):
		if (re.search(r'[\._][lLrR]$', name)):
			return True
		if (re.search(r'[\._][lLrR]\.\d\d\d$', name)):
			return True
		if (re.search(r'[\._]right$', name.lower())):
			return True
		if (re.search(r'[\._]left$', name.lower())):
			return True
		if (re.search(r'[\._]right\.\d\d\d$', name.lower())):
			return True
		if (re.search(r'[\._]left\.\d\d\d$', name.lower())):
			return True
		return False
	
	@classmethod
	def poll(self, context):
		if (context.active_bone):
			return self.CheckIsMirror(context.active_bone.name)
		if (context.active_pose_bone):
			return self.CheckIsMirror(context.active_pose_bone.name)
		return False
	
	def execute(self, context):
		if (context.active_bone):
			bone = context.active_bone
		if (context.active_pose_bone):
			bone = context.active_pose_bone
		pre_name = bone.name
		new_name = pre_name
		for i in range(1):
			if (bone.name[-1] == 'l'):
				new_name = bone.name[:-1] + 'r'
				break
			if (bone.name[-1] == 'L'):
				new_name = bone.name[:-1] + 'R'
				break
			if (bone.name[-1] == 'r'):
				new_name = bone.name[:-1] + 'l'
				break
			if (bone.name[-1] == 'R'):
				new_name = bone.name[:-1] + 'L'
				break
			
			if (re.search(r'[\._][l]\.\d\d\d$', bone.name)):
				new_name = bone.name[:-5] + 'r' + bone.name[-4:]
				break
			if (re.search(r'[\._][L]\.\d\d\d$', bone.name)):
				new_name = bone.name[:-5] + 'R' + bone.name[-4:]
				break
			if (re.search(r'[\._][r]\.\d\d\d$', bone.name)):
				new_name = bone.name[:-5] + 'l' + bone.name[-4:]
				break
			if (re.search(r'[\._][R]\.\d\d\d$', bone.name)):
				new_name = bone.name[:-5] + 'L' + bone.name[-4:]
				break
			
			if (re.search(r'[\._]right$', bone.name.lower())):
				new_name = bone.name[:-5] + 'left'
				break
			if (re.search(r'[\._]left$', bone.name.lower())):
				new_name = bone.name[:-4] + 'right'
				break
			
			if (re.search(r'[\._]right\.\d\d\d$', bone.name.lower())):
				new_name = bone.name[:-9] + 'left' + bone.name[-4:]
				break
			if (re.search(r'[\._]left\.\d\d\d$', bone.name.lower())):
				new_name = bone.name[:-8] + 'right' + bone.name[-4:]
				break
		bone.name = new_name
		if (pre_name != bone.name):
			if (new_name == bone.name):
				self.report(type={'INFO'}, message=pre_name + " => " + bone.name)
			else:
				self.report(type={'WARNING'}, message=pre_name + " => " + bone.name)
		else:
			self.report(type={'ERROR'}, message="No name change failed,")
			return {'CANCELLED'}
		return {'FINISHED'}

class AppendActiveBoneName(bpy.types.Operator):
	bl_idname = "pose.append_active_bone_name"
	bl_label = "Add text to the bone name"
	bl_description = "Adds a string to the active bone name"
	bl_options = {'REGISTER', 'UNDO'}
	
	string = bpy.props.StringProperty(name="Append text")
	
	@classmethod
	def poll(self, context):
		if (context.active_bone):
			return True
		if (context.active_pose_bone):
			return True
		return False
	
	def execute(self, context):
		if (context.active_bone):
			bone = context.active_bone
		if (context.active_pose_bone):
			bone = context.active_pose_bone
		bone.name = bone.name + self.string
		return {'FINISHED'}
################
# サブメニュー #
################

class AppendNameMenu(bpy.types.Menu):
	bl_idname = "BONE_PT_context_bone_append_name"
	bl_label = "A new character,"
	
	def draw(self, context):
		self.layout.operator(AppendActiveBoneName.bl_idname, text=".L").string = '.L'
		self.layout.operator(AppendActiveBoneName.bl_idname, text=".R").string = '.R'
		self.layout.separator()
		self.layout.operator(AppendActiveBoneName.bl_idname, text="_L").string = '_L'
		self.layout.operator(AppendActiveBoneName.bl_idname, text="_R").string = '_R'
		self.layout.separator()
		self.layout.operator(AppendActiveBoneName.bl_idname, text=".left").string = '.left'
		self.layout.operator(AppendActiveBoneName.bl_idname, text=".right").string = '.right'
		self.layout.separator()
		self.layout.operator(AppendActiveBoneName.bl_idname, text="_left").string = '_left'
		self.layout.operator(AppendActiveBoneName.bl_idname, text="_right").string = '_right'

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
		if (context.edit_bone or context.bone):
			row = self.layout.row(align=True)
			row.operator(CopyBoneName.bl_idname, icon='COPYDOWN', text="To the Clipboard")
			row.operator(RenameMirrorActiveBone.bl_idname, icon='MOD_MIRROR', text="Flip Horizontal")
			row.menu(AppendNameMenu.bl_idname, icon='PLUGIN')
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
