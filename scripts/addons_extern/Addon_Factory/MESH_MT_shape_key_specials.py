# プロパティ > 「オブジェクトデータ」タブ > シェイプキー一覧右の▼

import bpy

################
# オペレーター #
################

class CopyShape(bpy.types.Operator):
	bl_idname = "mesh.copy_shape"
	bl_label = "Duplicate a shape key"
	bl_description = "Duplicate the active shape key"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		ob = context.active_object
		if (ob):
			if (ob.type == 'MESH'):
				if (ob.active_shape_key):
					return True
		return False
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type == "MESH"):
			me = obj.data
			keys = {}
			for key in me.shape_keys.key_blocks:
				keys[key.name] = key.value
				key.value = 0
			obj.active_shape_key.value = 1
			relativeKey = obj.active_shape_key.relative_key
			while relativeKey != relativeKey.relative_key:
				relativeKey.value = 1
				relativeKey = relativeKey.relative_key
			obj.shape_key_add(name=obj.active_shape_key.name, from_mix=True)
			obj.active_shape_key_index = len(me.shape_keys.key_blocks) - 1
			for k, v in keys.items():
				me.shape_keys.key_blocks[k].value = v
		return {'FINISHED'}

class ShowShapeBlockName(bpy.types.Operator):
	bl_idname = "mesh.show_shape_block_name"
	bl_label = "Examine the shape name"
	bl_description = "Copy to the Clipboard, and then displays the name of the shape blocks"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		ob = context.active_object
		if (ob):
			if (ob.type == 'MESH'):
				if (ob.data.shape_keys):
					return True
		return False
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type == "MESH"):
			shape_keys = obj.data.shape_keys
			if (shape_keys != None):
				self.report(type={"INFO"}, message=shape_keys.name)
				context.window_manager.clipboard = shape_keys.name
			else:
				self.report(type={"ERROR"}, message="Shape key does not exist")
		else:
			self.report(type={"ERROR"}, message="Mesh objects are not")
		return {'FINISHED'}

class RenameShapeBlockName(bpy.types.Operator):
	bl_idname = "mesh.rename_shape_block_name"
	bl_label = "Block shape name in the object name"
	bl_description = "Same as object name the name of the shape blocks"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		ob = context.active_object
		if (ob):
			if (ob.type == 'MESH'):
				if (ob.data.shape_keys):
					return True
		return False
	
	def execute(self, context):
		obj = context.active_object
		me = obj.data
		me.shape_keys.name = obj.name
		return {'FINISHED'}

class InsertKeyframeAllShapes(bpy.types.Operator):
	bl_idname = "mesh.insert_keyframe_all_shapes"
	bl_label = "Hit the keyframes of all shapes"
	bl_description = "Inserts a keyframe for all shapes on the current frame"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		ob = context.active_object
		if (ob):
			if (ob.type == 'MESH'):
				if (ob.active_shape_key):
					return True
		return False
	
	def execute(self, context):
		for shape in context.active_object.data.shape_keys.key_blocks:
			shape.keyframe_insert(data_path="value")
		for area in context.screen.areas:
			area.tag_redraw()
		return {'FINISHED'}

class SelectShapeTop(bpy.types.Operator):
	bl_idname = "object.select_shape_top"
	bl_label = "Select the top"
	bl_description = "Select the top shape key"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		ob = context.active_object
		if (ob):
			if (ob.type == 'MESH'):
				if (ob.data.shape_keys):
					if (2 <= len(ob.data.shape_keys.key_blocks)):
						return True
		return False
	
	def execute(self, context):
		context.active_object.active_shape_key_index = 0
		return {'FINISHED'}

class SelectShapeBottom(bpy.types.Operator):
	bl_idname = "object.select_shape_bottom"
	bl_label = "Select the bottom row"
	bl_description = "Select the bottom shape key"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		ob = context.active_object
		if (ob):
			if (ob.type == 'MESH'):
				if (ob.data.shape_keys):
					if (2 <= len(ob.data.shape_keys.key_blocks)):
						return True
		return False
	
	def execute(self, context):
		context.active_object.active_shape_key_index = len(context.active_object.data.shape_keys.key_blocks) - 1
		return {'FINISHED'}

class ShapeKeyApplyRemoveAll(bpy.types.Operator):
	bl_idname = "object.shape_key_apply_remove_all"
	bl_label = "Remove all shape and holds the shape of the current"
	bl_description = "Remove all shape key while maintaining the shape of the mesh current"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		ob = context.active_object
		if (ob):
			if (ob.type == 'MESH'):
				if (ob.data.shape_keys):
					if (2 <= len(ob.data.shape_keys.key_blocks)):
						return True
		return False
	
	def execute(self, context):
		bpy.ops.object.shape_key_add(from_mix=True)
		bpy.ops.object.shape_key_move(type='DOWN')
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		bpy.ops.object.shape_key_remove(all=True)
		return {'FINISHED'}

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
		self.layout.operator(SelectShapeTop.bl_idname, icon='PLUGIN')
		self.layout.operator(SelectShapeBottom.bl_idname, icon='PLUGIN')
		self.layout.separator()
		self.layout.operator(CopyShape.bl_idname, icon='PLUGIN')
		self.layout.operator(ShapeKeyApplyRemoveAll.bl_idname, icon='PLUGIN')
		self.layout.separator()
		self.layout.operator(InsertKeyframeAllShapes.bl_idname, icon='PLUGIN')
		self.layout.separator()
		self.layout.operator(ShowShapeBlockName.bl_idname, icon='PLUGIN')
		self.layout.operator(RenameShapeBlockName.bl_idname, icon='PLUGIN')
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
