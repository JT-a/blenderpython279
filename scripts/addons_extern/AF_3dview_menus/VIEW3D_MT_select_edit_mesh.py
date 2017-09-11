# 3Dビュー > メッシュ編集モード > 「選択」メニュー

import bpy

################
# オペレーター #
################

class SelectAxisLimit(bpy.types.Operator):
	bl_idname = "mesh.select_axis_limit"
	bl_label = "Select the vertex of X = 0"
	bl_description = "Select the vertex of X = 0"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		("0", "The x axis", "", 1),
		("1", "Y軸", "", 2),
		("2", "Z軸", "", 3),
		]
	axis = bpy.props.EnumProperty(items=items, name="Axis")
	offset = bpy.props.FloatProperty(name="Offset", default=0.0, step=10, precision=3)
	threshold = bpy.props.FloatProperty(name="Threshold", default=0.0000001, min=0.0, soft_min=0.0, step=0.1, precision=10)
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode="OBJECT")
		sel_mode = context.tool_settings.mesh_select_mode[:]
		context.tool_settings.mesh_select_mode = [True, False, False]
		obj = context.active_object
		me = obj.data
		if (obj.type == "MESH"):
			for vert in me.vertices:
				co = [vert.co.x, vert.co.y, vert.co.z][int(self.axis)]
				if (-self.threshold <= co - self.offset <= self.threshold):
					vert.select = True
		bpy.ops.object.mode_set(mode="EDIT")
		context.tool_settings.mesh_select_mode = sel_mode
		return {'FINISHED'}

class SelectAxisOver(bpy.types.Operator):
	bl_idname = "mesh.select_axis_over"
	bl_label = "Select the right half"
	bl_description = "Select the right half of the mesh (other settings too)"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		("0", "The x axis", "", 1),
		("1", "Y軸", "", 2),
		("2", "Z軸", "", 3),
		]
	axis = bpy.props.EnumProperty(items=items, name="Axis")
	items = [
		("-1", "-(Minus)", "", 1),
		("1", "+ (Plus)", "", 2),
		]
	direction = bpy.props.EnumProperty(items=items, name="Direction")
	offset = bpy.props.FloatProperty(name="Offset", default=0, step=10, precision=3)
	threshold = bpy.props.FloatProperty(name="Threshold", default=0.0000001, step=0.1, precision=10)
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode="OBJECT")
		sel_mode = context.tool_settings.mesh_select_mode[:]
		context.tool_settings.mesh_select_mode = [True, False, False]
		obj = context.active_object
		me = obj.data
		if (obj.type == "MESH"):
			for vert in me.vertices:
				co = [vert.co.x, vert.co.y, vert.co.z][int(self.axis)]
				direct = int(self.direction)
				if (self.offset * direct <= co * direct + self.threshold):
					vert.select = True
		bpy.ops.object.mode_set(mode="EDIT")
		context.tool_settings.mesh_select_mode = sel_mode
		return {'FINISHED'}


# menu
def menu(self, context):

	self.layout.separator()
	self.layout.operator(SelectAxisLimit.bl_idname, icon="PLUGIN")
	self.layout.operator(SelectAxisOver.bl_idname, icon="PLUGIN")

