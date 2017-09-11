# 3Dビュー > メッシュ編集モード > 「メッシュ」メニュー > 「表示/隠す」メニュー

import bpy

################
# オペレーター #
################

class InvertHide(bpy.types.Operator):
	bl_idname = "mesh.invert_hide"
	bl_label = "Show / hide flip"
	bl_description = "Flip display and non-display state"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type == "MESH"):
			bpy.ops.object.mode_set(mode="OBJECT")
			me = obj.data
			for v in me.vertices:
				v.hide = not v.hide
			for e in me.edges:
				for i in e.vertices:
					if (me.vertices[i].hide == True):
						e.hide = True
						break
				else:
					e.hide = False
			for f in me.polygons:
				for i in f.vertices:
					if (me.vertices[i].hide == True):
						f.hide = True
						break
				else:
					f.hide = False
			bpy.ops.object.mode_set(mode="EDIT")
		else:
			self.report(type={"ERROR"}, message="Running on a mesh object is active")
		return {'FINISHED'}

class HideVertexOnly(bpy.types.Operator):
	bl_idname = "mesh.hide_vertex_only"
	bl_label = "Hide only the top"
	bl_description = "To hide the selected vertices, the fixed"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type == "MESH"):
			bpy.ops.object.mode_set(mode="OBJECT")
			me = obj.data
			for vert in me.vertices:
				if (vert.select):
					vert.hide = True
			bpy.ops.object.mode_set(mode="EDIT")
		else:
			self.report(type={"ERROR"}, message="Running on a mesh object is active")
		return {'FINISHED'}

class HideParts(bpy.types.Operator):
	bl_idname = "mesh.hide_parts"
	bl_label = "Hide the selected parts"
	bl_description = "Hides the mesh part more than 1 vertex is selected"
	bl_options = {'REGISTER', 'UNDO'}
	
	unselected = bpy.props.BoolProperty(name="Non-select Division", default=False)
	
	def execute(self, context):
		isSelecteds = []
		for vert in context.active_object.data.vertices:
			isSelecteds.append(vert.select)
		bpy.ops.mesh.select_linked(delimit=set())

		bpy.ops.mesh.hide(unselected=self.unselected)
		bpy.ops.mesh.select_all(action='DESELECT')
		return {'FINISHED'}

def menu(self, context):

	self.layout.separator()
	self.layout.operator(HideParts.bl_idname, icon="PLUGIN", text="Hide the selected parts").unselected = False
	self.layout.operator(HideParts.bl_idname, icon="PLUGIN", text="Hide the unselected parts").unselected = True
	self.layout.separator()
	self.layout.operator(InvertHide.bl_idname, icon="PLUGIN")
	self.layout.separator()
	self.layout.operator(HideVertexOnly.bl_idname, icon="PLUGIN")

