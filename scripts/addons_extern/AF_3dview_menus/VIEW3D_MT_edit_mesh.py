# 3Dビュー > メッシュ編集モード > 「メッシュ」メニュー

import bpy

################
# オペレーター #
################

class ToggleMeshSelectMode(bpy.types.Operator):
	bl_idname = "mesh.toggle_mesh_select_mode"
	bl_label = "Mesh selection mode"
	bl_description = "Mesh selection mode → top → side surface. Switch and"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		mode = context.tool_settings.mesh_select_mode
		if (mode[2]):
			context.tool_settings.mesh_select_mode = (True, False, False)
			self.report(type={"INFO"}, message="Vertex select mode")
		elif (mode[1]):
			context.tool_settings.mesh_select_mode = (False, False, True)
			self.report(type={"INFO"}, message="Face selection mode")
		else:
			context.tool_settings.mesh_select_mode = (False, True, False)
			self.report(type={"INFO"}, message="\"Edge\" mode")
		return {'FINISHED'}

################
# パイメニュー #
################

class SelectModePieOperator(bpy.types.Operator):
	bl_idname = "mesh.select_mode_pie_operator"
	bl_label = "Mesh selection mode"
	bl_description = "Is a pie menu selection of mesh"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=SelectModePie.bl_idname)
		return {'FINISHED'}

class SelectModePie(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_edit_mesh_pie_select_mode"
	bl_label = "Mesh selection mode"
	bl_description = "Is a pie menu selection of mesh"
	
	def draw(self, context):
		self.layout.menu_pie().operator("mesh.select_mode", text="Vertex", icon='VERTEXSEL').type = 'VERT'
		self.layout.menu_pie().operator("mesh.select_mode", text="Noodles", icon='FACESEL').type = 'FACE'
		self.layout.menu_pie().operator("mesh.select_mode", text="Edge", icon='EDGESEL').type = 'EDGE'

class ProportionalPieOperator(bpy.types.Operator):
	bl_idname = "mesh.proportional_pie_operator"
	bl_label = "Proportional edit"
	bl_description = "Is a pie menu proportional edit"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		if (context.scene.tool_settings.proportional_edit == "DISABLED"):
			bpy.ops.wm.call_menu_pie(name=ProportionalPie.bl_idname)
		else:
			context.scene.tool_settings.proportional_edit = "DISABLED"
		return {'FINISHED'}

class ProportionalPie(bpy.types.Menu): #
	bl_idname = "VIEW3D_MT_edit_mesh_pie_proportional"
	bl_label = "Proportional edit"
	bl_description = "Is a pie menu proportional edit"
	
	def draw(self, context):
		self.layout.menu_pie().operator(SetProportionalEdit.bl_idname, text="Enabling", icon="PROP_ON").mode = "ENABLED"
		self.layout.menu_pie().operator(SetProportionalEdit.bl_idname, text="Projection (2D)", icon="PROP_ON").mode = "PROJECTED"
		self.layout.menu_pie().operator(SetProportionalEdit.bl_idname, text="Connection", icon="PROP_CON").mode = "CONNECTED"

class SetProportionalEdit(bpy.types.Operator): #
	bl_idname = "mesh.set_proportional_edit"
	bl_label = "Set the proportional editing modes"
	bl_description = "Set the proportional editing modes"
	bl_options = {'REGISTER'}
	
	mode = bpy.props.StringProperty(name="Mode", default="DISABLED")
	
	def execute(self, context):
		context.scene.tool_settings.proportional_edit = self.mode
		return {'FINISHED'}

################
# サブメニュー #
################

class PieMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_edit_mesh_pie_menu"
	bl_label = "Pie menu"
	bl_description = "Is a pie on the mesh editing"
	
	def draw(self, context):
		self.layout.operator(SelectModePieOperator.bl_idname, icon="COLOR")
		self.layout.operator(ProportionalPieOperator.bl_idname, icon="COLOR")

class ShortcutMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_edit_mesh_shortcut"
	bl_label = "Shortcuts"
	bl_description = "Experimental Shortcuts menu"
	
	def draw(self, context):
		self.layout.operator(ToggleMeshSelectMode.bl_idname, icon="EDITMODE_HLT")

# menu
def menu(self, context):

	self.layout.separator()
	self.layout.menu(ShortcutMenu.bl_idname, icon="LINE_DATA")

