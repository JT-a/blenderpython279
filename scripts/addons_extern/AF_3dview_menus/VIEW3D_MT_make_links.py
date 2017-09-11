# 3Dビュー > オブジェクトモード > 「Ctrl+L」キー

import bpy, bmesh

################
# オペレーター #
################

class MakeLinkObjectName(bpy.types.Operator):
	bl_idname = "object.make_link_object_name"
	bl_label = "Link Object Names"
	bl_description = "Rename 001 002 from selected object name"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		return True
	def execute(self, context):
		name = context.active_object.name
		for obj in context.selected_objects:
			if (obj.name != name):
				obj.name = "temp"
				obj.name = name
		bpy.context.active_object.name = name
		return {'FINISHED'}

class MakeLinkLayer(bpy.types.Operator):
	bl_idname = "object.make_link_layer"
	bl_label = "Move Layer"
	bl_description = "Move Objects to the last selected object's layer"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		return True
	def execute(self, context):
		for obj in context.selected_objects:
			if (obj.name != context.active_object.name):
				obj.layers = context.active_object.layers
		return {'FINISHED'}

class MakeLinkDisplaySetting(bpy.types.Operator):
	bl_idname = "object.make_link_display_setting"
	bl_label = "Visibility of objects to the same"
	bl_description = "Copy the settings of the display panel of the active object to other selected objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	isSameType = bpy.props.BoolProperty(name="Only objects of the same type", default=True)
	show_name = bpy.props.BoolProperty(name="The name", default=True)
	show_axis = bpy.props.BoolProperty(name="Coordinate axes", default=True)
	show_wire = bpy.props.BoolProperty(name="Wire frame", default=True)
	show_all_edges = bpy.props.BoolProperty(name="See all sides", default=True)
	show_bounds = bpy.props.BoolProperty(name="Bound", default=True)
	show_texture_space = bpy.props.BoolProperty(name="Texture space", default=True)
	show_x_ray = bpy.props.BoolProperty(name="X rays", default=True)
	show_transparent = bpy.props.BoolProperty(name="Through", default=True)
	draw_bounds_type = bpy.props.BoolProperty(name="Types of bounces", default=True)
	draw_type = bpy.props.BoolProperty(name="Best drawing type", default=True)
	color = bpy.props.BoolProperty(name="Object color", default=True)
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		return True
	def execute(self, context):
		activeObj = context.active_object
		for obj in context.selected_objects:
			if (not self.isSameType or activeObj.type == obj.type):
				if (obj.name != activeObj.name):
					if (self.show_name):
						obj.show_name = activeObj.show_name
					if (self.show_axis):
						obj.show_axis = activeObj.show_axis
					if (self.show_wire):
						obj.show_wire = activeObj.show_wire
					if (self.show_all_edges):
						obj.show_all_edges = activeObj.show_all_edges
					if (self.show_bounds):
						obj.show_bounds = activeObj.show_bounds
					if (self.show_texture_space):
						obj.show_texture_space = activeObj.show_texture_space
					if (self.show_x_ray):
						obj.show_x_ray = activeObj.show_x_ray
					if (self.show_transparent):
						obj.show_transparent = activeObj.show_transparent
					if (self.draw_bounds_type):
						obj.draw_bounds_type = activeObj.draw_bounds_type
					if (self.draw_type):
						obj.draw_type = activeObj.draw_type
					if (self.color):
						obj.color = activeObj.color
		return {'FINISHED'}

class MakeLinkUVNames(bpy.types.Operator):
	bl_idname = "object.make_link_uv_names"
	bl_label = "Link to UV map of the sky"
	bl_description = "Empties the Add UV active objects to other objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		if (context.object.type != 'MESH'):
			return False
		if (len(context.object.data.uv_layers) <= 0):
			return False
		for obj in context.selected_objects:
			if (obj.name != context.object.name):
				if (obj.type == 'MESH'):
					return True
		return False
	def execute(self, context):
		active_obj = context.active_object
		target_objs = []
		for obj in context.selected_objects:
			if (obj.type == 'MESH' and active_obj.name != obj.name):
				target_objs.append(obj)
		for obj in target_objs:
			for uv in active_obj.data.uv_layers:
				obj.data.uv_textures.new(uv.name)
		return {'FINISHED'}

class MakeLinkArmaturePose(bpy.types.Operator):
	bl_idname = "object.make_link_armature_pose"
	bl_label = "Link motion of the armature"
	bl_description = "By constraints on other selected armature mimic active armature movement"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		if (context.object.type != 'ARMATURE'):
			return False
		for obj in context.selected_objects:
			if (obj.name != context.object.name):
				if (obj.type == 'ARMATURE'):
					return True
		return False
	def execute(self, context):
		active_obj = context.active_object
		target_objs = []
		for obj in context.selected_objects:
			if (obj.type == 'ARMATURE' and active_obj.name != obj.name):
				target_objs.append(obj)
		for obj in target_objs:
			for bone in active_obj.pose.bones:
				try:
					target_bone = obj.pose.bones[bone.name]
				except KeyError:
					continue
				consts = target_bone.constraints
				for const in consts[:]:
					consts.remove(const)
				const = consts.new('COPY_TRANSFORMS')
				const.target = active_obj
				const.subtarget = bone.name
		return {'FINISHED'}

class MakeLinkSoftbodySettings(bpy.types.Operator):
	bl_idname = "object.make_link_softbody_settings"
	bl_label = "Links for soft body"
	bl_description = "Sets the active object soft copies to other selected objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		for mod in context.object.modifiers:
			if (mod.type == 'SOFT_BODY'):
				break
		else:
			return False
		return True
	def execute(self, context):
		active_obj = context.active_object
		active_softbody = None
		for mod in active_obj.modifiers:
			if (mod.type == 'SOFT_BODY'):
				active_softbody = mod
				break
		target_objs = []
		for obj in context.selected_objects:
			if (active_obj.name != obj.name):
				target_objs.append(obj)
		for obj in target_objs:
			target_softbody = None
			for mod in obj.modifiers:
				if (mod.type == 'SOFT_BODY'):
					target_softbody = mod
					break
			else:
				target_softbody = obj.modifiers.new("Softbody", 'SOFT_BODY')
			for name in dir(active_softbody.settings):
				if (name[0] != '_'):
					try:
						value = active_softbody.settings.__getattribute__(name)
						target_softbody.settings.__setattr__(name, value)
					except AttributeError:
						pass
			for name in dir(active_softbody.point_cache):
				if (name[0] != '_'):
					try:
						value = active_softbody.point_cache.__getattribute__(name)
						target_softbody.point_cache.__setattr__(name, value)
					except AttributeError:
						pass
		return {'FINISHED'}

class MakeLinkClothSettings(bpy.types.Operator):
	bl_idname = "object.make_link_cloth_settings"
	bl_label = "Links for cross-"
	bl_description = "Cloth simulation for the active object copies to other selected objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		for mod in context.object.modifiers:
			if (mod.type == 'CLOTH'):
				break
		else:
			return False
		return True
	def execute(self, context):
		active_obj = context.active_object
		active_cloth = None
		for mod in active_obj.modifiers:
			if (mod.type == 'CLOTH'):
				active_cloth = mod
				break
		target_objs = []
		for obj in context.selected_objects:
			if (active_obj.name != obj.name):
				target_objs.append(obj)
		for obj in target_objs:
			target_cloth = None
			for mod in obj.modifiers:
				if (mod.type == 'CLOTH'):
					target_cloth = mod
					break
			else:
				target_cloth = obj.modifiers.new("Cloth", 'CLOTH')
			for name in dir(active_cloth.settings):
				if (name[0] != '_'):
					try:
						value = active_cloth.settings.__getattribute__(name)
						target_cloth.settings.__setattr__(name, value)
					except AttributeError:
						pass
			for name in dir(active_cloth.point_cache):
				if (name[0] != '_'):
					try:
						value = active_cloth.point_cache.__getattribute__(name)
						target_cloth.point_cache.__setattr__(name, value)
					except AttributeError:
						pass
		return {'FINISHED'}

######################
# オペレーター(変形) #
######################

class MakeLinkTransform(bpy.types.Operator):
	bl_idname = "object.make_link_transform"
	bl_label = "Link to deformation"
	bl_description = "Information of the active object copies to other selected objects"
	bl_options = {'REGISTER', 'UNDO'}
	
	copy_location = bpy.props.BoolProperty(name="Location", default=True)
	copy_rotation = bpy.props.BoolProperty(name="Rotation", default=True)
	copy_scale = bpy.props.BoolProperty(name="Zoom in / out", default=True)
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		return True
	def execute(self, context):
		active_obj = context.active_object
		for obj in context.selected_objects:
			if (obj.name != active_obj.name):
				if (self.copy_location):
					obj.location = active_obj.location[:]
				if (self.copy_rotation):
					obj.rotation_mode = active_obj.rotation_mode
					if (obj.rotation_mode == 'QUATERNION'):
						obj.rotation_quaternion = active_obj.rotation_quaternion[:]
					elif (obj.rotation_mode == 'AXIS_ANGLE'):
						obj.rotation_axis_angle = active_obj.rotation_axis_angle[:]
					else:
						obj.rotation_euler = active_obj.rotation_euler[:]
				if (self.copy_scale):
					obj.scale = active_obj.scale[:]
		return {'FINISHED'}

################
# サブメニュー #
################

class TransformMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_make_links_transform"
	bl_label = "Deformation"
	bl_description = "Links to information about transform objects"
	
	def draw(self, context):
		op = self.layout.operator(MakeLinkTransform.bl_idname, text="Transform")
		op.copy_location, op.copy_rotation, op.copy_scale = True, True, True
		self.layout.separator()
		op = self.layout.operator(MakeLinkTransform.bl_idname, text="Location")
		op.copy_location, op.copy_rotation, op.copy_scale = True, False, False
		op = self.layout.operator(MakeLinkTransform.bl_idname, text="Rotation")
		op.copy_location, op.copy_rotation, op.copy_scale = False, True, False
		op = self.layout.operator(MakeLinkTransform.bl_idname, text="Zoom in / out")
		op.copy_location, op.copy_rotation, op.copy_scale = False, False, True

# menu
def menu(self, context):

	self.layout.separator()
	self.layout.label(text= "Experimental")
	self.layout.menu(TransformMenu.bl_idname)
	self.layout.operator(MakeLinkObjectName.bl_idname, text="Object name")
	self.layout.operator(MakeLinkLayer.bl_idname, text="Move Layer")
	self.layout.operator(MakeLinkDisplaySetting.bl_idname, text="Display settings")
	self.layout.separator()
	self.layout.operator(MakeLinkSoftbodySettings.bl_idname, text="Soft Body")
	self.layout.operator(MakeLinkClothSettings.bl_idname, text="CLoth")
	self.layout.separator()
	self.layout.operator(MakeLinkUVNames.bl_idname, text="UV")
	self.layout.operator(MakeLinkArmaturePose.bl_idname, text="Pose")

