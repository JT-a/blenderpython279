# 3Dビュー > メッシュ編集モード > 「W」キー

import bpy

################
# オペレーター #
################

class PaintSelectedVertexColor(bpy.types.Operator):
	bl_idname = "mesh.paint_selected_vertex_color"
	bl_label = "Fill the selected vertex vertex color"
	bl_description = "Active vertex colors for the selected vertices with specified color fills"
	bl_options = {'REGISTER', 'UNDO'}
	
	color = bpy.props.FloatVectorProperty(name="Color", default=(1, 1, 1), step=1, precision=3, subtype='COLOR_GAMMA', min=0, max=1, soft_min=0, soft_max=1)
	
	def execute(self, context):
		activeObj = context.active_object
		me = activeObj.data
		bpy.ops.object.mode_set(mode='OBJECT')
		i = 0
		for poly in me.polygons:
			for vert in poly.vertices:
				if (me.vertices[vert].select):
					me.vertex_colors.active.data[i].color = self.color
				i += 1
		bpy.ops.object.mode_set(mode='EDIT')
		return {'FINISHED'}

class SelectTopShape(bpy.types.Operator):
	bl_idname = "mesh.select_top_shape"
	bl_label = "Select the shape on the top of"
	bl_description = "Schipke is at the top of the list, select"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		context.active_object.active_shape_key_index = 0
		return {'FINISHED'}

class ToggleShowCage(bpy.types.Operator):
	bl_idname = "mesh.toggle_show_cage"
	bl_label = "Transition modifiers apply to the editing cage"
	bl_description = "Toggles whether to apply modifiers to total en bloc spondylectomy in the editing"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		activeObj = context.active_object
		nowMode = 0
		for modi in activeObj.modifiers:
			if (modi.show_in_editmode and nowMode <= 0):
				nowMode = 1
			if (modi.show_on_cage and nowMode <= 1):
				nowMode = 2
		newMode = nowMode + 1
		if (newMode >= 3):
			newMode = 0
		for modi in activeObj.modifiers:
			if (newMode == 0):
				modi.show_in_editmode = False
				modi.show_on_cage = False
			if (newMode == 1):
				modi.show_in_editmode = True
				modi.show_on_cage = False
			if (newMode == 2):
				modi.show_in_editmode = True
				modi.show_on_cage = True
		if (newMode == 0):
			self.report(type={'INFO'}, message="Display / adaptation of cage both have been cleared")
		if (newMode == 1):
			self.report(type={'INFO'}, message="Only cage you\'ve turned")
		if (newMode == 2):
			self.report(type={'INFO'}, message="Show cage / adaptation, both turned")
		return {'FINISHED'}

class ToggleMirrorModifier(bpy.types.Operator):
	bl_idname = "mesh.toggle_mirror_modifier"
	bl_label = "Toggle Miller modifier"
	bl_description = "Delete if not Miller modifier added, Yes"
	bl_options = {'REGISTER', 'UNDO'}
	
	use_x = bpy.props.BoolProperty(name="The x axis", default=True)
	use_y = bpy.props.BoolProperty(name="Y軸", default=False)
	use_z = bpy.props.BoolProperty(name="Z軸", default=False)
	use_mirror_merge = bpy.props.BoolProperty(name="Combination", default=True)
	use_clip = bpy.props.BoolProperty(name="Clipping", default=False)
	use_mirror_vertex_groups = bpy.props.BoolProperty(name="Vertex group mirror", default=False)
	use_mirror_u = bpy.props.BoolProperty(name="Texture U mirror", default=False)
	use_mirror_v = bpy.props.BoolProperty(name="Texture V Miller", default=False)
	merge_threshold = bpy.props.FloatProperty(name="Combined distance", default=0.001, min=0, max=1, soft_min=0, soft_max=1, step=0.01, precision=6)
	is_top = bpy.props.BoolProperty(name="Add at the top", default=True)
	
	def execute(self, context):
		activeObj = context.active_object
		is_mirrored = False
		for mod in activeObj.modifiers:
			if (mod.type == 'MIRROR'):
				is_mirrored = True
				break
		if (is_mirrored):
			for mod in activeObj.modifiers:
				if (mod.type == 'MIRROR'):
					activeObj.modifiers.remove(mod)
		else:
			new_mod = activeObj.modifiers.new("Mirror", 'MIRROR')
			new_mod.use_x = self.use_x
			new_mod.use_y = self.use_y
			new_mod.use_z = self.use_z
			new_mod.use_mirror_merge = self.use_mirror_merge
			new_mod.use_clip = self.use_clip
			new_mod.use_mirror_vertex_groups = self.use_mirror_vertex_groups
			new_mod.use_mirror_u = self.use_mirror_u
			new_mod.use_mirror_v = self.use_mirror_v
			new_mod.merge_threshold = self.merge_threshold
			if (self.is_top):
				for i in range(len(activeObj.modifiers)):
					bpy.ops.object.modifier_move_up(modifier=new_mod.name)
		return {'FINISHED'}
	def invoke(self, context, event):
		activeObj = context.active_object
		for mod in activeObj.modifiers:
			if (mod.type == 'MIRROR'):
				self.execute(context)
				return {'RUNNING_MODAL'}
		return context.window_manager.invoke_props_dialog(self)

class SelectedVertexGroupAverage(bpy.types.Operator):
	bl_idname = "mesh.selected_vertex_group_average"
	bl_label = "Fill the selected vertex in average weighted"
	bl_description = "Fills the selected vertex, vertices weighted average"
	bl_options = {'REGISTER', 'UNDO'}
	
	strength = bpy.props.FloatProperty(name="Mix strength", default=1, min=0, max=1, soft_min=0, soft_max=1, step=10, precision=3)
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	def execute(self, context):
		obj = context.active_object
		if (obj.type == "MESH"):
			pre_mode = obj.mode
			bpy.ops.object.mode_set(mode='OBJECT')
			vert_groups = []
			for vg in obj.vertex_groups:
				vert_groups.append([])
			selected_verts = []
			for vert in obj.data.vertices:
				if (vert.select):
					selected_verts.append(vert)
					for i in range(len(vert_groups)):
						for vge in vert.groups:
							if (i == vge.group):
								vert_groups[vge.group].append(vge.weight)
								break
						else:
							vert_groups[i].append(0)
			vert_groups_average = []
			for weights in vert_groups:
				vert_groups_average.append(0)
				for weight in weights:
					vert_groups_average[-1] += weight
				vert_groups_average[-1] /= len(weights)
			i = 0
			for vg in obj.vertex_groups:
				for vert in selected_verts:
					pre_weight = 0
					for vge in vert.groups:
						if (obj.vertex_groups[vge.group].name == vg.name):
							pre_weight = vge.weight
							break
					weight = (vert_groups_average[i] * self.strength) + (pre_weight * (1 - self.strength))
					vg.add([vert.index], weight, "REPLACE")
				i += 1
			bpy.ops.object.mode_set(mode=pre_mode)
		else:
			self.report(type={"ERROR"}, message="Mesh objects are not")
			return {'CANCELLED'}
		return {'FINISHED'}


# Menu
def menu(self, context):

	self.layout.separator()
	self.layout.prop(context.object.data, "use_mirror_x", icon="PLUGIN", text="X axis mirror edit")


