# 3Dビュー > オブジェクトモード > 「選択」メニュー

import bpy, mathutils
import re

################
# オペレーター #
################

class SelectBoundBoxSize(bpy.types.Operator):
	bl_idname = "object.select_bound_box_size"
	bl_label = "Select Object By Size"
	bl_description = "Select Object By Size"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		('LARGE', "Select Large Objects", "", 1),
		('SMALL', "Select Small Objects", "", 2),
		]
	mode = bpy.props.EnumProperty(items=items, name="Selection mode")
	items = [
		('MESH', "Mesh", "", 1),
		('CURVE', "Curve", "", 2),
		('SURFACE', "Surface", "", 3),
		('META', "Meta", "", 4),
		('FONT', "Font", "", 5),
		('ARMATURE', "Armature", "", 6),
		('LATTICE', "Lattice", "", 7),
		('ALL', "all", "", 8),
		]
	select_type = bpy.props.EnumProperty(items=items, name="Select type", default='MESH')
	threshold = bpy.props.FloatProperty(name="Threshold", default=50, min=0, max=100, soft_min=0, soft_max=100, step=100, precision=1, subtype='PERCENTAGE')
	
	def execute(self, context):
		context.scene.update()
		max_volume = -1
		min_volume = 999999999999999
		min_obj = None
		objs = []
		for obj in context.visible_objects:
			if (self.select_type != 'ALL'):
				if (obj.type != self.select_type):
					continue
			bound_box = obj.bound_box[:]
			bound_box0 = mathutils.Vector(bound_box[0][:])
			x = (bound_box0 - mathutils.Vector(bound_box[4][:])).length * obj.scale.x
			y = (bound_box0 - mathutils.Vector(bound_box[3][:])).length * obj.scale.y
			z = (bound_box0 - mathutils.Vector(bound_box[1][:])).length * obj.scale.z
			volume = x + y + z
			objs.append((obj, volume))
			if (max_volume < volume):
				max_volume = volume
			if (volume < min_volume):
				min_volume = volume
				min_obj = obj
		if (self.mode == 'LARGE'):
			threshold_volume = max_volume * (1.0 - (self.threshold * 0.01))
		elif (self.mode == 'SMALL'):
			threshold_volume = max_volume * (self.threshold * 0.01)
		for obj, volume in objs:
			if (self.mode == 'LARGE'):
				if (threshold_volume <= volume):
					obj.select = True
			elif (self.mode == 'SMALL'):
				if (volume <= threshold_volume):
					obj.select = True
		if (min_obj and self.mode == 'SMALL'):
			min_obj.select = True
		return {'FINISHED'}

############################
# オペレーター(関係で選択) #
############################

class SelectGroupedName(bpy.types.Operator):
	bl_idname = "object.select_grouped_name"
	bl_label = "Select Objects Same Name"
	bl_description = "Select Objects with the same name as the Active Object (such as X X.001 X.002)"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		name_base = context.active_object.name
		if (re.search(r'\.\d+$', name_base)):
			name_base = re.search(r'^(.*)\.\d+$', name_base).groups()[0]
		for obj in context.selectable_objects:
			if (re.search('^'+name_base+r'\.\d+$', obj.name) or name_base == obj.name):
				obj.select = True
		return {'FINISHED'}

class SelectGroupedMaterial(bpy.types.Operator):
	bl_idname = "object.select_grouped_material"
	bl_label = "Select Same Material"
	bl_description = "Select Same Material Objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		def GetMaterialList(slots):
			list = []
			for slot in slots:
				if (slot.material):
					list.append(slot.material.name)
			return list
		activeMats = GetMaterialList(context.active_object.material_slots)
		if (0 < len(activeMats)):
			for obj in context.selectable_objects:
				if (activeMats == GetMaterialList(obj.material_slots)):
					obj.select = True
		return {'FINISHED'}

class SelectGroupedModifiers(bpy.types.Operator):
	bl_idname = "object.select_grouped_modifiers"
	bl_label = "Select Same Modifier"
	bl_description = "Select Same Modifier Objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		def GetModifiersString(obj):
			str = ""
			for mod in obj.modifiers:
				str = str + mod.type
			return str
		active_modifiers = GetModifiersString(context.active_object)
		active_type = context.active_object.type
		for obj in context.selectable_objects:
			if (GetModifiersString(obj) == active_modifiers and active_type == obj.type):
				obj.select= True
		return {'FINISHED'}

class SelectGroupedSubsurfLevel(bpy.types.Operator):
	bl_idname = "object.select_grouped_subsurf_level"
	bl_label = "Select Same Subsurf Level"
	bl_description = "Select Same Subsurf Level"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		def GetSubsurfLevel(obj):
			level = 0
			for mod in obj.modifiers:
				if (mod.type == 'SUBSURF'):
					level += mod.levels
			return level
		active_subsurf_level = GetSubsurfLevel(context.active_object)
		active_type = context.active_object.type
		for obj in context.selectable_objects:
			if (GetSubsurfLevel(obj) == active_subsurf_level and active_type == obj.type):
				obj.select= True
		return {'FINISHED'}

class SelectGroupedArmatureTarget(bpy.types.Operator):
	bl_idname = "object.select_grouped_armature_target"
	bl_label = "Select Group Armature Target"
	bl_description = "Select Group Armature Target"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		def GetArmatureTarget(obj):
			target = []
			for mod in obj.modifiers:
				if (mod.type == 'ARMATURE'):
					if (mod.object):
						target.append(mod.object.name)
					else:
						target.append("")
			return set(target)
		active_armature_targets = GetArmatureTarget(context.active_object)
		if (len(active_armature_targets) == 0):
			self.report(type={"ERROR"}, message="There is no armature modifier in the Active Object")
			return {"CANCELLED"}
		active_type = context.active_object.type
		for obj in context.selectable_objects:
			if (len(GetArmatureTarget(obj).intersection(active_armature_targets)) == len(active_armature_targets) and active_type == obj.type):
				obj.select= True
		return {'FINISHED'}

class SelectGroupedSizeThan(bpy.types.Operator):
	bl_idname = "object.select_grouped_size_than"
	bl_label = "Select an object by Size"
	bl_description = "Larger/Smaller"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		('LARGER', "Choose larger ones", "", 1),
		('SMALLER', "Choose smaller ones", "", 2),
		]
	mode = bpy.props.EnumProperty(items=items, name="Mode")
	select_same_size = bpy.props.BoolProperty(name="Select same size", default=True)
	items = [
		('MESH', "Mesh", "", 1),
		('CURVE', "Curve", "", 2),
		('SURFACE', "Surface", "", 3),
		('META', "Meta", "", 4),
		('FONT', "Font", "", 5),
		('ARMATURE', "Armature", "", 6),
		('LATTICE', "Lattice", "", 7),
		('ALL', "All", "", 8),
		('SAME', "Same", "", 9),
		]
	select_type = bpy.props.EnumProperty(items=items, name="Select Type", default='SAME')
	size_multi = bpy.props.FloatProperty(name="Reference size offset", default=1.0, min=0, max=10, soft_min=0, soft_max=10, step=10, precision=3)
	
	def execute(self, context):
		def GetSize(obj):
			bound_box = obj.bound_box[:]
			bound_box0 = mathutils.Vector(bound_box[0][:])
			bound_box0 = mathutils.Vector(bound_box[0][:])
			x = (bound_box0 - mathutils.Vector(bound_box[4][:])).length * obj.scale.x
			y = (bound_box0 - mathutils.Vector(bound_box[3][:])).length * obj.scale.y
			z = (bound_box0 - mathutils.Vector(bound_box[1][:])).length * obj.scale.z
			return x + y + z
		
		active_obj = context.active_object
		if (not active_obj):
			self.report(type={'ERROR'}, message="There is no active object")
			return {'CANCELLED'}
		context.scene.update()
		active_obj_size = GetSize(active_obj) * self.size_multi
		for obj in context.selectable_objects:
			if (self.select_type != 'ALL'):
				if (self.select_type == 'SAME'):
					if (obj.type != active_obj.type):
						continue
				else:
					if (obj.type != self.select_type):
						continue
			size = GetSize(obj)
			if (self.mode == 'LARGER'):
				if (active_obj_size < size):
					obj.select = True
			elif (self.mode == 'SMALLER'):
				if (size < active_obj_size):
					obj.select = True
			if (self.select_same_size):
				if (active_obj_size == size):
					obj.select = True
		return {'FINISHED'}

################
# サブメニュー #
################

class SelectGroupedEX(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_select_object_grouped_ex"
	bl_label = "Select Extended"
	bl_description = "I will select all visible objects that are grouped by property"
	
	def draw(self, context):
		self.layout.operator("object.select_grouped", text="Child recursive").type = 'CHILDREN_RECURSIVE'
		self.layout.operator("object.select_grouped", text="Children").type = 'CHILDREN'
		self.layout.operator("object.select_grouped", text="Parent").type = 'PARENT'
		self.layout.operator("object.select_grouped", text="Siblings").type = 'SIBLINGS'
		self.layout.operator("object.select_grouped", text="Type").type = 'TYPE'
		self.layout.operator("object.select_grouped", text="layerー").type = 'LAYER'
		self.layout.operator("object.select_grouped", text="Group").type = 'GROUP'
		self.layout.operator("object.select_grouped", text="Pass").type = 'PASS'
		self.layout.operator("object.select_grouped", text="Color").type = 'COLOR'
		self.layout.operator("object.select_grouped", text="Properties").type = 'PROPERTIES'
		self.layout.operator("object.select_grouped", text="Keyingset").type = 'KEYINGSET'
		self.layout.operator("object.select_grouped", text="Lamp type").type = 'LAMP_TYPE'
		self.layout.separator()
		self.layout.operator(SelectGroupedSizeThan.bl_idname, text="Larger", icon="PMARKER_ACT").mode = 'LARGER'
		self.layout.operator(SelectGroupedSizeThan.bl_idname, text="Smaller", icon="SPACE2").mode = 'SMALLER'
		self.layout.separator()
		self.layout.operator(SelectGroupedName.bl_idname, text="Object name", icon="OBJECT_DATA")
		self.layout.operator(SelectGroupedMaterial.bl_idname, text="Material", icon="MATERIAL")
		self.layout.operator(SelectGroupedModifiers.bl_idname, text="Modifiers", icon="MODIFIER")
		self.layout.operator(SelectGroupedSubsurfLevel.bl_idname, text="Sub Surf level", icon="MOD_SUBSURF")
		self.layout.operator(SelectGroupedArmatureTarget.bl_idname, text="Same armature deformation", icon="ARMATURE_DATA")


# menu
def menu(self, context):

	self.layout.separator()
	self.layout.operator(SelectBoundBoxSize.bl_idname, text="Select Small Objects", icon="SPACE2").mode = 'SMALL'
	self.layout.operator(SelectBoundBoxSize.bl_idname, text="Select Large Objects", icon="PMARKER_ACT").mode = 'LARGE'
	self.layout.separator()
	self.layout.menu(SelectGroupedEX.bl_idname, icon="ROTATECOLLECTION")

