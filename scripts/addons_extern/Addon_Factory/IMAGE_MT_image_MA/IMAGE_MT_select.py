# UV/画像エディター > 「選択」メニュー

import bpy
import bmesh

################
# オペレーター #
################

class SelectSeamEdge(bpy.types.Operator):
	bl_idname = "uv.select_seam_edge"
	bl_label = "Select the vertices are isolated"
	bl_description = "Select the vertex are separated by seams"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		activeObj = context.active_object
		me = activeObj.data
		bpy.ops.object.mode_set(mode='OBJECT')
		bm = bmesh.new()
		bm.from_mesh(me)
		uv_lay = bm.loops.layers.uv.active
		use_uv_select_sync = context.scene.tool_settings.use_uv_select_sync
		verts = {}
		for face in bm.faces:
			for loop in face.loops:
				uv = loop[uv_lay].uv
				index = loop.vert.index
				if (str(index) in verts):
					for u in verts[str(index)]:
						if (u == uv[:]):
							break
					else:
						verts[str(index)].append(uv[:])
				else:
					verts[str(index)] = [uv[:]]
		for face in bm.faces:
			for loop in face.loops:
				uv = loop[uv_lay].uv
				vert = loop.vert
				index = vert.index
				if (2 <= len(verts[str(index)])):
					loop[uv_lay].select = True
					if (use_uv_select_sync):
						vert.select = True
		bm.to_mesh(me)
		bm.free()
		bpy.ops.object.mode_set(mode='EDIT')
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
		self.layout.operator(SelectSeamEdge.bl_idname, icon="PLUGIN")
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
