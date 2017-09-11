# 「プロパティ」エリア > 「オブジェクト」タブ > 「表示」パネル

import bpy

################
# オペレーター #
################

class CopyDisplaySetting(bpy.types.Operator):
	bl_idname = "object.copy_display_setting"
	bl_label = "Copy the display settings"
	bl_description = "Copy the selected objects of other display settings"
	bl_options = {'REGISTER', 'UNDO'}
	
	copy_show_name = bpy.props.BoolProperty(name="The name", default=True)
	copy_show_axis = bpy.props.BoolProperty(name="Coordinate axes", default=True)
	copy_show_wire = bpy.props.BoolProperty(name="Wire frame", default=True)
	copy_show_all_edges = bpy.props.BoolProperty(name="See all sides", default=True)
	copy_show_bounds = bpy.props.BoolProperty(name="Bound", default=True)
	copy_draw_bounds_type = bpy.props.BoolProperty(name="Type outbound", default=True)
	copy_show_texture_space = bpy.props.BoolProperty(name="Texture space", default=True)
	copy_show_x_ray = bpy.props.BoolProperty(name="X rays", default=True)
	copy_show_transparent = bpy.props.BoolProperty(name="Through", default=True)
	copy_draw_type = bpy.props.BoolProperty(name="Best drawing type", default=True)
	copy_color = bpy.props.BoolProperty(name="Object color", default=True)
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) <= 1):
			return False
		return True
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
	def draw(self, context):
		row = self.layout.row()
		row.prop(self, 'copy_show_name')
		row.prop(self, 'copy_show_bounds')
		row = self.layout.row()
		row.label(text="")
		row.prop(self, 'copy_draw_bounds_type')
		row = self.layout.row()
		row.prop(self, 'copy_show_axis')
		row.prop(self, 'copy_show_texture_space')
		row = self.layout.row()
		row.prop(self, 'copy_show_wire')
		row.prop(self, 'copy_show_x_ray')
		row = self.layout.row()
		row.prop(self, 'copy_show_all_edges')
		row.prop(self, 'copy_show_transparent')
		row = self.layout.row()
		row.prop(self, 'copy_draw_type')
		row.prop(self, 'copy_color')
	
	def execute(self, context):
		active_obj = context.active_object
		for obj in context.selected_objects:
			if (obj.name != active_obj.name):
				if (self.copy_show_name):
					obj.show_name = active_obj.show_name
				if (self.copy_show_axis):
					obj.show_axis = active_obj.show_axis
				if (self.copy_show_wire):
					obj.show_wire = active_obj.show_wire
				if (self.copy_show_all_edges):
					obj.show_all_edges = active_obj.show_all_edges
				if (self.copy_show_bounds):
					obj.show_bounds = active_obj.show_bounds
				if (self.copy_draw_bounds_type):
					obj.draw_bounds_type = active_obj.draw_bounds_type
				if (self.copy_show_texture_space):
					obj.show_texture_space = active_obj.show_texture_space
				if (self.copy_show_x_ray):
					obj.show_x_ray = active_obj.show_x_ray
				if (self.copy_show_transparent):
					obj.show_transparent = active_obj.show_transparent
				if (self.copy_draw_type):
					obj.draw_type = active_obj.draw_type
				if (self.copy_color):
					obj.color = active_obj.color[:]
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
		self.layout.operator(CopyDisplaySetting.bl_idname, icon='MESH_UVSPHERE')
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
