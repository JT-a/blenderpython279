# 3Dビュー > オブジェクトモード > 「オブジェクト」メニュー

import bpy, bmesh

################
# パイメニュー #
################

class CopyPieOperator(bpy.types.Operator):
	bl_idname = "object.copy_pie_operator"
	bl_label = "Copy Pie"
	bl_description = "Copy pie menu of is about the object"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=CopyPie.bl_idname)
		return {'FINISHED'}

class CopyPie(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_object_pie_copy"
	bl_label = "Copy Pie"
	bl_description = "Copy pie menu (test)"
	
	def draw(self, context):
		self.layout.menu_pie().operator("view3d.copybuffer", icon="COPY_ID")
		self.layout.menu_pie().operator(CopyObjectName.bl_idname, icon="MONKEY")

class ObjectModePieOperator(bpy.types.Operator):
	bl_idname = "object.object_mode_pie_operator"
	bl_label = "Object interactive mode"
	bl_description = "This is a pie menu of objects interactive mode"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=ObjectModePie.bl_idname)
		return {'FINISHED'}

class ObjectModePie(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_object_pie_object_mode"
	bl_label = "Object interactive mode"
	bl_description = "This is a pie menu of objects interactive mode"
	
	def draw(self, context):
		self.layout.menu_pie().operator(SetObjectMode.bl_idname, text="Pose", icon="POSE_HLT").mode = "POSE"
		self.layout.menu_pie().operator(SetObjectMode.bl_idname, text="Sculpt", icon="SCULPTMODE_HLT").mode = "SCULPT"
		self.layout.menu_pie().operator(SetObjectMode.bl_idname, text="Weight Paint", icon="WPAINT_HLT").mode = "WEIGHT_PAINT"
		self.layout.menu_pie().operator(SetObjectMode.bl_idname, text="Object", icon="OBJECT_DATAMODE").mode = "OBJECT"
		self.layout.menu_pie().operator(SetObjectMode.bl_idname, text="", icon="PARTICLEMODE").mode = "PARTICLE_EDIT"
		self.layout.menu_pie().operator(SetObjectMode.bl_idname, text="Edit", icon="EDITMODE_HLT").mode = "EDIT"
		self.layout.menu_pie().operator(SetObjectMode.bl_idname, text="Texture Paint", icon="TPAINT_HLT").mode = "TEXTURE_PAINT"
		self.layout.menu_pie().operator(SetObjectMode.bl_idname, text="Vertex Paint", icon="VPAINT_HLT").mode = "VERTEX_PAINT"


class SetObjectMode(bpy.types.Operator): #
	bl_idname = "object.set_object_mode"
	bl_label = "Set the object interactive mode"
	bl_description = "I set the interactive mode of object"
	bl_options = {'REGISTER'}
	
	mode = bpy.props.StringProperty(name="Interactive mode", default="OBJECT")
	
	def execute(self, context):
		if (context.active_object):
			try:
				bpy.ops.object.mode_set(mode=self.mode)
			except TypeError:
				self.report(type={"WARNING"}, message=context.active_object.name+" It is not possible to enter into the interactive mode")
		else:
			self.report(type={"WARNING"}, message="There is no active object")
		return {'FINISHED'}

class SubdivisionSetPieOperator(bpy.types.Operator):
	bl_idname = "object.subdivision_set_pie_operator"
	bl_label = "Subsurface Pie"
	bl_description = "This is a pie menu to set the level of Subsurface modifier"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=SubdivisionSetPie.bl_idname)
		return {'FINISHED'}

class SubdivisionSetPie(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_object_pie_subdivision_set"
	bl_label = "Sabusafu Pie"
	bl_description = "This is a pie menu to set the level of Sabusafu"
	
	def draw(self, context):
		self.layout.menu_pie().operator("object.subdivision_set", text="Level:2", icon="MOD_SUBSURF").level = 2
		self.layout.menu_pie().operator("object.subdivision_set", text="Level:6", icon="MOD_SUBSURF").level = 6
		self.layout.menu_pie().operator("object.subdivision_set", text="Level:0", icon="MOD_SUBSURF").level = 0
		self.layout.menu_pie().operator("object.subdivision_set", text="Level:4", icon="MOD_SUBSURF").level = 4
		self.layout.menu_pie().operator("object.subdivision_set", text="Level:3", icon="MOD_SUBSURF").level = 3
		self.layout.menu_pie().operator("object.subdivision_set", text="Level:5", icon="MOD_SUBSURF").level = 5
		self.layout.menu_pie().operator("object.subdivision_set", text="Level:1", icon="MOD_SUBSURF").level = 1

class DrawTypePieOperator(bpy.types.Operator):
	bl_idname = "object.draw_type_pie_operator"
	bl_label = "Best drawing type Pie"
	bl_description = "This is a pie menu to set the highest drawing type"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=DrawTypePie.bl_idname)
		return {'FINISHED'}

class DrawTypePie(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_object_pie_draw_type"
	bl_label = "Best Draw Type"
	bl_description = "Best draw Type"
	
	def draw(self, context):
		self.layout.menu_pie().operator(SetDrawType.bl_idname, text="Bounds", icon="BBOX").type = "BOUNDS"
		self.layout.menu_pie().operator(SetDrawType.bl_idname, text="Wire", icon="WIRE").type = "WIRE"
		self.layout.menu_pie().operator(SetDrawType.bl_idname, text="Solid", icon="SOLID").type = "SOLID"
		self.layout.menu_pie().operator(SetDrawType.bl_idname, text="Textured", icon="POTATO").type = "TEXTURED"


class SetDrawType(bpy.types.Operator): #
	bl_idname = "object.set_draw_type"
	bl_label = "Set Draw Type"
	bl_description = "Set Draw Type"
	bl_options = {'REGISTER'}
	
	type = bpy.props.StringProperty(name="Drawing type", default="OBJECT")
	
	def execute(self, context):
		for obj in context.selected_objects:
			obj.draw_type = self.type
		return {'FINISHED'}

################
# オペレーター #
################

class DeleteUnmassage(bpy.types.Operator):
	bl_idname = "object.delete_unmassage"
	bl_label = "Delete Without Confirm"
	bl_description = "Delete Without Confirm"
	bl_options = {'REGISTER', 'UNDO'}
	
	use_global = bpy.props.BoolProperty(name="Overall Delete", default=False)
	
	def execute(self, context):
		if (context.active_object):
			self.report(type={"INFO"}, message=context.active_object.name+"I have been deleted, goodbye.")
		bpy.ops.object.delete(use_global=self.use_global)
		return {'FINISHED'}

################
# サブメニュー #
################

class PieMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_object_pie_menu"
	bl_label = "Pie menu"
	bl_description = "This is a pie menu for the object manipulation"
	
	def draw(self, context):
		self.layout.operator(CopyPieOperator.bl_idname, icon="COLOR")
		self.layout.operator(ObjectModePieOperator.bl_idname, icon="COLOR")
		self.layout.operator(SubdivisionSetPieOperator.bl_idname, icon="COLOR")
		self.layout.operator(DrawTypePieOperator.bl_idname, icon="COLOR")

class ShortcutMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_object_shortcut"
	bl_label = "Shortcuts"
	bl_description = "Quick Shortcuts"
	
	def draw(self, context):
		self.layout.operator(DeleteUnmassage.bl_idname, icon="COLOR_RED")
#		self.layout.operator(ApplyModifiersAndJoin.bl_idname, icon="PLUGIN")


# Menu
def menu(self, context):
	self.layout.separator()
	self.layout.menu(ShortcutMenu.bl_idname, icon="LINE_DATA")
	self.layout.menu(PieMenu.bl_idname, icon="COLOR")

