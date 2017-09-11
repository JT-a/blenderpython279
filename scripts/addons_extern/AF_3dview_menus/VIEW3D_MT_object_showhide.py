# 3Dビュー > オブジェクトモード > 「オブジェクト」メニュー > 「表示/隠す」メニュー

import bpy

################
# オペレーター #
################

class InvertHide(bpy.types.Operator):
	bl_idname = "object.invert_hide"
	bl_label = "Show / Hide Flip"
	bl_description = "Flips the object\'s view state and non-State"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		objs = []
		for obj in bpy.data.objects:
			for i in range(len(bpy.context.scene.layers)):
				if (bpy.context.scene.layers[i] and obj.layers[i]):
					for obj2 in objs:
						if (obj.name == obj2.name):
							break
					else:
						objs.append(obj)
		for obj in objs:
			obj.hide = not obj.hide
		return {'FINISHED'}

class HideOnlyType(bpy.types.Operator):
	bl_idname = "object.hide_only_mesh"
	bl_label = "Hide Object By Type"
	bl_description = "Hides the object of a specific type are displayed"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		("MESH", "Mesh", "", 1),
		("CURVE", "Curve", "", 2),
		("SURFACE", "Surface", "", 3),
		("META", "Metaballs", "", 4),
		("FONT", "Text", "", 5),
		("ARMATURE", "Armature", "", 6),
		("LATTICE", "Lattice", "", 7),
		("EMPTY", "Empty", "", 8),
		("CAMERA", "Camera", "", 9),
		("LAMP", "Lamp", "", 10),
		("SPEAKER", "Speakers", "", 11),
		]
	type = bpy.props.EnumProperty(items=items, name="Hide object type")
	
	def execute(self, context):
		for obj in context.selectable_objects:
			if (obj.type == self.type):
				obj.hide = True
		return {'FINISHED'}

class HideExceptType(bpy.types.Operator):
	bl_idname = "object.hide_except_mesh"
	bl_label = "Show Object by Type"
	bl_description = "Hides the object non-specific type that is displayed"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		("MESH", "Mesh", "", 1),
		("CURVE", "Curve", "", 2),
		("SURFACE", "Surface", "", 3),
		("META", "Metaballs", "", 4),
		("FONT", "Text", "", 5),
		("ARMATURE", "Armature", "", 6),
		("LATTICE", "Lattice", "", 7),
		("EMPTY", "Empty", "", 8),
		("CAMERA", "Camera", "", 9),
		("LAMP", "Lamp", "", 10),
		("SPEAKER", "Speakers", "", 11),
		]
	type = bpy.props.EnumProperty(items=items, name="Leave the object type")
	
	def execute(self, context):
		for obj in context.selectable_objects:
			if (obj.type != self.type):
				obj.hide = True
		return {'FINISHED'}


# menu
def menu(self, context):

	self.layout.separator()
	self.layout.operator(InvertHide.bl_idname)
	self.layout.separator()
	self.layout.operator(HideOnlyType.bl_idname)
	self.layout.operator(HideExceptType.bl_idname)

