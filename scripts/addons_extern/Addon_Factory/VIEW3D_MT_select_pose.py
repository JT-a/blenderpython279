# 3Dビュー > ポーズモード > 「選択」メニュー

import bpy
import re

################
# オペレーター #
################

class SelectSerialNumberNameBone(bpy.types.Operator):
	bl_idname = "pose.select_serial_number_name_bone"
	bl_label = "Select a numbered bone."
	bl_description = "Select the name with a number X.001 in bone"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type != 'ARMATURE'):
			self.report(type={"ERROR"}, message="Run with an armature object")
			return {"CANCELLED"}
		arm = obj.data
		for bone in context.visible_pose_bones[:]:
			if (re.search(r'\.\d+$', bone.name)):
				arm.bones[bone.name].select = True
		return {'FINISHED'}

class SelectMoveSymmetryNameBones(bpy.types.Operator):
	bl_idname = "pose.select_move_symmetry_name_bones"
	bl_label = "Symmetrical bones move selection"
	bl_description = "If you choose X.R change selection to X.L, if X.L to X.R"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		def GetMirrorBoneName(name):
			new_name = re.sub(r'([\._])L$', r"\1R", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])l$', r"\1r", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])R$', r"\1L", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])r$', r"\1l", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])L([\._]\d+)$', r"\1R\2", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])l([\._]\d+)$', r"\1r\2", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])R([\._]\d+)$', r"\1L\2", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])r([\._]\d+)$', r"\1l\2", name)
			if (new_name != name): return new_name
			return name
		obj = context.active_object
		if (obj.type != 'ARMATURE'):
			self.report(type={"ERROR"}, message="Run with an armature object")
			return {"CANCELLED"}
		arm = obj.data
		pre_selected_pose_bones = context.selected_pose_bones[:]
		for bone in pre_selected_pose_bones[:]:
			mirror_name = GetMirrorBoneName(bone.name)
			if (mirror_name == bone.name):
				self.report(type={"WARNING"}, message=bone.name+"The name that corresponds to the mirror, ignore")
				continue
			try:
				arm.bones[mirror_name]
			except KeyError:
				self.report(type={"WARNING"}, message=bone.name+"The ignores because bone-to-be does not exist")
				continue
			arm.bones[mirror_name].select = True
		for bone in pre_selected_pose_bones[:]:
			arm.bones[bone.name].select = False
		try:
			arm.bones.active = arm.bones[GetMirrorBoneName(arm.bones.active.name)]
		except KeyError:
			arm.bones.active = arm.bones[context.selected_pose_bones[0].name]
		return {'FINISHED'}

class SelectSameConstraintBone(bpy.types.Operator):
	bl_idname = "pose.select_same_constraint_bone"
	bl_label = "Select the bone of the same constraints"
	bl_description = "Select additional bone with active bone and same kind of constraint."
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		active = context.active_pose_bone
		activeConstraints = []
		for const in active.constraints:
			activeConstraints.append(const.type)
		for bone in context.visible_pose_bones:
			constraints = []
			for const in bone.constraints:
				constraints.append(const.type)
			if (len(activeConstraints) == len(constraints)):
				for i in range(len(constraints)):
					if (activeConstraints[i] != constraints[i]):
						break
				else:
					context.active_object.data.bones[bone.name].select = True
		return {'FINISHED'}

class SelectSameNameBones(bpy.types.Operator):
	bl_idname = "pose.select_same_name_bones"
	bl_label = "Select the bone of the same name."
	bl_description = "Regarding the bone names, such as X-X.001 X.002 with the same name, select"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type != 'ARMATURE'):
			self.report(type={"ERROR"}, message="Run with an armature object")
			return {"CANCELLED"}
		arm = obj.data
		name_base = context.active_pose_bone.name
		if (re.search(r'\.\d+$', name_base)):
			name_base = re.search(r'^(.*)\.\d+$', name_base).groups()[0]
		for bone in context.visible_pose_bones[:]:
			if (re.search('^'+name_base+r'\.\d+$', bone.name) or name_base == bone.name):
				arm.bones[bone.name].select = True
		return {'FINISHED'}

class SelectSymmetryNameBones(bpy.types.Operator):
	bl_idname = "pose.select_symmetry_name_bones"
	bl_label = "Select Add name of symmetrical bone"
	bl_description = "If you select X.R X.L also selected X.R X.L if additional selection"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		def GetMirrorBoneName(name):
			new_name = re.sub(r'([\._])L$', r"\1R", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])l$', r"\1r", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])R$', r"\1L", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])r$', r"\1l", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])L([\._]\d+)$', r"\1R\2", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])l([\._]\d+)$', r"\1r\2", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])R([\._]\d+)$', r"\1L\2", name)
			if (new_name != name): return new_name
			new_name = re.sub(r'([\._])r([\._]\d+)$', r"\1l\2", name)
			if (new_name != name): return new_name
			return name
		obj = context.active_object
		if (obj.type != 'ARMATURE'):
			self.report(type={"ERROR"}, message="Run with an armature object")
			return {"CANCELLED"}
		arm = obj.data
		for bone in context.selected_pose_bones[:]:
			mirror_name = GetMirrorBoneName(bone.name)
			if (mirror_name == bone.name):
				self.report(type={"WARNING"}, message=bone.name+"The name that corresponds to the mirror, ignore")
				continue
			try:
				arm.bones[mirror_name]
			except KeyError:
				self.report(type={"WARNING"}, message=bone.name+"The ignores because bone-to-be does not exist")
				continue
			arm.bones[mirror_name].select = True
		return {'FINISHED'}

class SelectChildrenEnd(bpy.types.Operator):
	bl_idname = "pose.select_children_end"
	bl_label = "Until the end of the bone"
	bl_description = "Select bones child-child child\'s bones. And we will select to the end"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if (not obj):
			self.report(type={'ERROR'}, message="There is no active object")
			return {'CANCELLED'}
		if (obj.type != 'ARMATURE'):
			self.report(type={'ERROR'}, message="Run with an armature object")
			return {'CANCELLED'}
		arm = obj.data
		selected_bones = context.selected_pose_bones[:]
		for bone in selected_bones:
			bone_children = []
			for b in arm.bones[bone.name].children[:]:
				bone_children.append(b)
			bone_queue = bone_children[:]
			while (0 < len(bone_queue)):
				removed_bone = bone_queue.pop(0)
				for b in removed_bone.children[:]:
					bone_queue.append(b)
					bone_children.append(b)
			for b in bone_children:
				b.select = True
		return {'FINISHED'}

class SelectParentEnd(bpy.types.Operator):
	bl_idname = "pose.select_parent_end"
	bl_label = "Select the bone"
	bl_description = "Choice bones parent → parent of parent bone. And we will select to the end"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if (not obj):
			self.report(type={'ERROR'}, message="There is no active object")
			return {'CANCELLED'}
		if (obj.type != 'ARMATURE'):
			self.report(type={'ERROR'}, message="Run with an armature object")
			return {'CANCELLED'}
		arm = obj.data
		selected_bones = context.selected_pose_bones[:]
		for bone in selected_bones:
			target_bone = arm.bones[bone.name]
			while target_bone.parent:
				target_bone = target_bone.parent
				target_bone.select = True
		return {'FINISHED'}

class SelectPath(bpy.types.Operator):
	bl_idname = "pose.select_path"
	bl_label = "Select the route of bones"
	bl_description = "Select the select bones of two paths"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		bones = []
		if (context.selected_bones):
			if (2 == len(context.selected_bones)):
				bones = context.selected_bones
		if (context.selected_pose_bones):
			if (2 == len(context.selected_pose_bones)):
				bones = context.selected_pose_bones
		if (2 == len(bones)):
			parents = []
			for bone in bones:
				parents.append(bone)
				while (parents[-1].parent):
					parents[-1] = parents[-1].parent
			if (parents[0].name == parents[1].name):
				return True
		return False
	
	def execute(self, context):
		obj = context.active_object
		pose = obj.pose
		arm = obj.data
		parents = []
		pre_mode = obj.mode
		if (obj.mode == 'EDIT'):
			bones = context.selected_bones
		else:
			bones = context.selected_pose_bones
		for bone in bones:
			parents.append([bone.name])
			while (pose.bones[parents[-1][-1]].parent):
				parents[-1].append(pose.bones[parents[-1][-1]].parent.name)
		bpy.ops.object.mode_set(mode='OBJECT')
		for bone_name in set(parents[0]) ^ set(parents[1]):
			arm.bones[bone_name].select = True
		bpy.ops.object.mode_set(mode=pre_mode)
		return {'FINISHED'}

################
# サブメニュー #
################

class SelectGroupedMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_select_pose_grouped"
	bl_label = "Selected relationship (extended)"
	bl_description = "Ability to select all visible bones together with the same properties menu."
	
	def draw(self, context):
		self.layout.operator('pose.select_grouped', text="Layer", icon='PLUGIN').type = 'LAYER'
		self.layout.operator('pose.select_grouped', text="Group", icon='PLUGIN').type = 'GROUP'
		self.layout.operator('pose.select_grouped', text="Keying set", icon='PLUGIN').type = 'KEYINGSET'
		self.layout.separator()
		self.layout.operator(SelectSameNameBones.bl_idname, text="Bone name", icon='PLUGIN')
		self.layout.operator(SelectSymmetryNameBones.bl_idname, text="Mirror name", icon='PLUGIN')
		self.layout.operator(SelectSameConstraintBone.bl_idname, text="Constraint", icon='PLUGIN')

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
		self.layout.separator()
		self.layout.operator(SelectPath.bl_idname, icon='PLUGIN')
		self.layout.separator()
		self.layout.operator(SelectParentEnd.bl_idname, icon='PLUGIN')
		self.layout.operator(SelectChildrenEnd.bl_idname, icon='PLUGIN')
		self.layout.separator()
		self.layout.operator(SelectSerialNumberNameBone.bl_idname, icon='PLUGIN')
		self.layout.operator(SelectMoveSymmetryNameBones.bl_idname, icon='PLUGIN')
		self.layout.separator()
		self.layout.menu(SelectGroupedMenu.bl_idname, icon='PLUGIN')
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
