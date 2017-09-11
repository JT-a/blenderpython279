# 3Dビュー > 「ビュー」メニュー

import bpy, mathutils
import os, csv
import collections

################
# オペレーター #
################

class LocalViewEx(bpy.types.Operator):
	bl_idname = "view3d.local_view_ex"
	bl_label = "Global view / local view (non-zoom)"
	bl_description = "To display only the selected object and place it in the center of the view (it does not zoom)"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		pre_smooth_view = context.user_preferences.view.smooth_view
		context.user_preferences.view.smooth_view = 0
		pre_view_distance = context.region_data.view_distance
		pre_view_location = context.region_data.view_location.copy()
		pre_view_rotation = context.region_data.view_rotation.copy()
		pre_cursor_location = context.space_data.cursor_location.copy()
		bpy.ops.view3d.localview()
		context.space_data.cursor_location = pre_cursor_location
		context.region_data.view_distance = pre_view_distance
		context.region_data.view_location = pre_view_location
		context.region_data.view_rotation = pre_view_rotation
		context.user_preferences.view.smooth_view = pre_smooth_view
		#bpy.ops.view3d.view_selected_ex()
		return {'FINISHED'}

class SaveView(bpy.types.Operator):
	bl_idname = "view3d.save_view"
	bl_label = "Save View"
	bl_description = "Save Current View"
	bl_options = {'REGISTER', 'UNDO'}
	
	index = bpy.props.StringProperty(name="Index", default="Name Me!")
	
	def execute(self, context):
		data = ""
		for line in context.user_preferences.addons["AF_3dview_menus"].preferences.view_savedata.split('|'):
			if (line == ""):
				continue
			try:
				index = line.split(':')[0]
			except ValueError:
				context.user_preferences.addons["AF_3dview_menus"].preferences.view_savedata = ""
				self.report(type={'ERROR'}, message="Does Not Compute")
				return {'CANCELLED'}
			if (str(self.index) == index):
				continue
			data = data + line + '|'
		text = data + str(self.index) + ':'
		co = context.region_data.view_location
		text = text + str(co[0]) + ',' + str(co[1]) + ',' + str(co[2]) + ':'
		ro = context.region_data.view_rotation
		text = text + str(ro[0]) + ',' + str(ro[1]) + ',' + str(ro[2]) + ',' + str(ro[3]) + ':'
		text = text + str(context.region_data.view_distance) + ':'
		text = text + context.region_data.view_perspective
		context.user_preferences.addons["AF_3dview_menus"].preferences.view_savedata = text
		self.report(type={'INFO'}, message="Saved"+str(self.index)+"Current View")
		return {'FINISHED'}
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

class LoadView(bpy.types.Operator):
	bl_idname = "view3d.load_view"
	bl_label = "Load View"
	bl_description = "View(Name"
	bl_options = {'REGISTER', 'UNDO'}
	
	index = bpy.props.StringProperty(name="Index", default="Name Me!")
	
	def execute(self, context):
		for line in context.user_preferences.addons["AF_3dview_menus"].preferences.view_savedata.split('|'):
			if (line == ""):
				continue
			try:
				index, loc, rot, distance, view_perspective = line.split(':')
			except ValueError:
				context.user_preferences.addons["AF_3dview_menus"].preferences.view_savedata = ""
				self.report(type={'ERROR'}, message="You broke it!")
				return {'CANCELLED'}
			if (str(self.index) == index):
				for i, v in enumerate(loc.split(',')):
					context.region_data.view_location[i] = float(v)
				for i, v in enumerate(rot.split(',')):
					context.region_data.view_rotation[i] = float(v)
				context.region_data.view_distance = float(distance)
				context.region_data.view_perspective = view_perspective
				self.report(type={'INFO'}, message="Loaded"+str(self.index)+"Current View")
				break
		else:
			self.report(type={'WARNING'}, message="Rename View"+str(self.index)+"Current View")
		return {'FINISHED'}

class DeleteViewSavedata(bpy.types.Operator):
	bl_idname = "view3d.delete_view_savedata"
	bl_label = "Delete view saved data"
	bl_description = "View Saved Data"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		context.user_preferences.addons["AF_3dview_menus"].preferences.view_savedata = ""
		return {'FINISHED'}

################
# パイメニュー #
################

class PieMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_view_pie"
	bl_label = "Pie menu"
	bl_description = "This is a pie menu of 3D view relationship"
	
	def draw(self, context):
		self.layout.operator(ViewNumpadPieOperator.bl_idname, icon="COLOR")
		self.layout.operator(ViewportShadePieOperator.bl_idname, icon="COLOR")
		self.layout.operator(LayerPieOperator.bl_idname, text="Layer", icon="COLOR")
		self.layout.operator(AreaTypePieOperator.bl_idname, icon="COLOR")

class ViewNumpadPieOperator(bpy.types.Operator):
	bl_idname = "view3d.view_numpad_pie_operator"
	bl_label = "Directions"
	bl_description = "(numeric keypad 1,3,7 Toka)"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=ViewNumpadPie.bl_idname)
		return {'FINISHED'}

class ViewNumpadPie(bpy.types.Menu): #
	bl_idname = "VIEW3D_MT_view_pie_view_numpad"
	bl_label = "Directions"
	bl_description = "(numeric keypad 1,3,7 Toka)"
	
	def draw(self, context):
		self.layout.menu_pie().operator("view3d.viewnumpad", text="Left", icon="TRIA_LEFT").type = "LEFT"
		self.layout.menu_pie().operator("view3d.viewnumpad", text="Right", icon="TRIA_RIGHT").type = "RIGHT"
		self.layout.menu_pie().operator("view3d.viewnumpad", text="Bottom", icon="TRIA_DOWN").type = "BOTTOM"
		self.layout.menu_pie().operator("view3d.viewnumpad", text="Top", icon="TRIA_UP").type = "TOP"
		self.layout.menu_pie().operator("view3d.viewnumpad", text="Back", icon="BBOX").type = "BACK"
		self.layout.menu_pie().operator("view3d.viewnumpad", text="Camera", icon="CAMERA_DATA").type = "CAMERA"
		self.layout.menu_pie().operator("view3d.viewnumpad", text="Front", icon="SOLID").type = "FRONT"
		self.layout.menu_pie().operator("view3d.view_persportho", text="Border move", icon="BORDERMOVE")

class ViewportShadePieOperator(bpy.types.Operator):
	bl_idname = "view3d.viewport_shade_pie_operator"
	bl_label = "Shading switching"
	bl_description = "Shading switching is pie menu"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=ViewportShadePie.bl_idname)
		return {'FINISHED'}

class ViewportShadePie(bpy.types.Menu): #
	bl_idname = "VIEW3D_MT_view_pie_viewport_shade"
	bl_label = "Shading switching"
	bl_description = "Shading switching is pie menu"
	
	def draw(self, context):
		self.layout.menu_pie().operator(SetViewportShade.bl_idname, text="Bound Box", icon="BBOX").mode = "BOUNDBOX"
		self.layout.menu_pie().operator(SetViewportShade.bl_idname, text="Rendered", icon="SMOOTH").mode = "RENDERED"
		self.layout.menu_pie().operator(SetViewportShade.bl_idname, text="Solid", icon="SOLID").mode = "SOLID"
		self.layout.menu_pie().operator(SetViewportShade.bl_idname, text="Textured", icon="POTATO").mode = "TEXTURED"
		self.layout.menu_pie().operator(SetViewportShade.bl_idname, text="Wireframe", icon="WIRE").mode = "WIREFRAME"
		self.layout.menu_pie().operator(SetViewportShade.bl_idname, text="Material", icon="MATERIAL").mode = "MATERIAL"

class SetViewportShade(bpy.types.Operator): #
	bl_idname = "view3d.set_viewport_shade"
	bl_label = "Shading switching"
	bl_description = "I will switch the shading"
	bl_options = {'REGISTER', 'UNDO'}
	
	mode = bpy.props.StringProperty(name="Shading", default="SOLID")
	
	def execute(self, context):
		context.space_data.viewport_shade = self.mode
		return {'FINISHED'}


class LayerPieOperator(bpy.types.Operator):
	bl_idname = "view3d.layer_pie_operator"
	bl_label = "Layer pie menu of"
	bl_description = "This is a pie menu of layer display switching"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=LayerPie.bl_idname)
		return {'FINISHED'}

class LayerPie(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_object_pie_layer"
	bl_label = "Layer pie menu of"
	bl_description = "This is a pie menu of layer display switching"
	
	def draw(self, context):
		box = self.layout.box()
		column = box.column()
		row = column.row()
		row.label(text="Half deselected in the semi-selected + Alt additional selection + Ctrl in Please select the layer to switch (+ Shift)", icon='PLUGIN')
		row = column.row()
		operator = row.operator(LayerPieRun.bl_idname, text="01", icon=self.GetIcon(0))
		operator.nr = 1
		operator = row.operator(LayerPieRun.bl_idname, text="02", icon=self.GetIcon(1))
		operator.nr = 2
		operator = row.operator(LayerPieRun.bl_idname, text="03", icon=self.GetIcon(2))
		operator.nr = 3
		operator = row.operator(LayerPieRun.bl_idname, text="04", icon=self.GetIcon(3))
		operator.nr = 4
		operator = row.operator(LayerPieRun.bl_idname, text="05", icon=self.GetIcon(4))
		operator.nr = 5
		row.separator()
		operator = row.operator(LayerPieRun.bl_idname, text="06", icon=self.GetIcon(5))
		operator.nr = 6
		operator = row.operator(LayerPieRun.bl_idname, text="07", icon=self.GetIcon(6))
		operator.nr = 7
		operator = row.operator(LayerPieRun.bl_idname, text="08", icon=self.GetIcon(7))
		operator.nr = 8
		operator = row.operator(LayerPieRun.bl_idname, text="09", icon=self.GetIcon(8))
		operator.nr = 9
		operator = row.operator(LayerPieRun.bl_idname, text="10", icon=self.GetIcon(9))
		operator.nr = 10
		row = column.row()
		operator = row.operator(LayerPieRun.bl_idname, text="11", icon=self.GetIcon(10))
		operator.nr = 11
		operator = row.operator(LayerPieRun.bl_idname, text="12", icon=self.GetIcon(11))
		operator.nr = 12
		operator = row.operator(LayerPieRun.bl_idname, text="13", icon=self.GetIcon(12))
		operator.nr = 13
		operator = row.operator(LayerPieRun.bl_idname, text="14", icon=self.GetIcon(13))
		operator.nr = 14
		operator = row.operator(LayerPieRun.bl_idname, text="15", icon=self.GetIcon(14))
		operator.nr = 15
		row.separator()
		operator = row.operator(LayerPieRun.bl_idname, text="16", icon=self.GetIcon(15))
		operator.nr = 16
		operator = row.operator(LayerPieRun.bl_idname, text="17", icon=self.GetIcon(16))
		operator.nr = 17
		operator = row.operator(LayerPieRun.bl_idname, text="18", icon=self.GetIcon(17))
		operator.nr = 18
		operator = row.operator(LayerPieRun.bl_idname, text="19", icon=self.GetIcon(18))
		operator.nr = 19
		operator = row.operator(LayerPieRun.bl_idname, text="20", icon=self.GetIcon(19))
		operator.nr = 20
	def GetIcon(self, layer):
		isIn = False
		isHalf = False
		objs = []
		for obj in bpy.data.objects:
			if (obj.layers[layer]):
				isIn = True
				objs.append(obj)
		if (objs):
			for obj in objs:
				if (obj.draw_type != 'WIRE'):
					break
			else:
				isHalf = True
		if (bpy.context.scene.layers[layer]):
			if (isHalf):
				return 'WIRE'
			if (isIn):
				return 'RADIOBUT_ON'
			return 'RADIOBUT_OFF'
		else:
			if (isHalf):
				return 'SOLID'
			if (isIn):
				return 'DOT'
			return 'BLANK1'

class LayerPieRun(bpy.types.Operator): #
	bl_idname = "view3d.layer_pie_run"
	bl_label = "Layer pie menu of"
	bl_description = "You can switch the layer (+ half deselected in the semi-selected + Alt additional selection + Ctrl, Shift)"
	bl_options = {'REGISTER', 'UNDO'}
	
	nr = bpy.props.IntProperty(name="Layer number")
	extend = bpy.props.BoolProperty(name="Select expansion", default=False)
	half = bpy.props.BoolProperty(name="Half-selected", default=False)
	unhalf = bpy.props.BoolProperty(name="Half deselect", default=False)
	
	def execute(self, context):
		nr = self.nr - 1
		if (self.half):
			context.scene.layers[nr] = True
			for obj in context.blend_data.objects:
				if (obj.layers[nr]):
					obj.show_all_edges = True
					obj.draw_type = 'WIRE'
		elif (self.unhalf):
			context.scene.layers[nr] = True
			for obj in context.blend_data.objects:
				if (obj.layers[nr]):
					obj.draw_type = 'TEXTURED'
		elif (self.extend):
			context.scene.layers[nr] = not context.scene.layers[nr]
		else:
			context.scene.layers[nr] = not context.scene.layers[nr]
			for i in range(len(context.scene.layers)):
				if (nr != i):
					context.scene.layers[i] = False
		return {'FINISHED'}
	def invoke(self, context, event):
		if (event.ctrl):
			self.extend = False
			self.half = True
			self.unhalf = False
		elif (event.shift):
			self.extend = True
			self.half = False
			self.unhalf = False
		elif (event.alt):
			self.extend = False
			self.half = False
			self.unhalf = True
		else:
			self.extend = False
			self.half = False
			self.unhalf = False
		return self.execute(context)

################
# サブメニュー #
################

class ShortcutsMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_view_shortcuts"
	bl_label = "Shortcuts"
	bl_description = "This is might be useful function group When you register to shortcut"
	
	def draw(self, context):
		self.layout.operator(LocalViewEx.bl_idname, icon="PLUGIN")
		self.layout.separator()
		self.layout.operator(TogglePanelsA.bl_idname, icon="PLUGIN")
		self.layout.operator(TogglePanelsB.bl_idname, icon="PLUGIN")
		self.layout.operator(TogglePanelsC.bl_idname, icon="PLUGIN")
		self.layout.separator()
		self.layout.operator(ToggleViewportShadeA.bl_idname, icon="PLUGIN")

class ViewSaveAndLoadMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_view_save_and_load"
	bl_label = "View Save & load"
	bl_description = "Save & Load Views"
	
	def draw(self, context):
		self.layout.operator(SaveView.bl_idname, icon="SAVE_AS")
		self.layout.operator(DeleteViewSavedata.bl_idname, icon="COLOR_RED")
		self.layout.separator()
		for line in context.user_preferences.addons["AF_3dview_menus"].preferences.view_savedata.split('|'):
			if (line == ""):
				continue
			try:
				index = line.split(':')[0]
			except ValueError:
				pass
			self.layout.operator(LoadView.bl_idname, text=index+" View", icon="RECOVER_AUTO").index = index

# menu
def menu(self, context):

	self.layout.separator()
	self.layout.prop(context.user_preferences.view, "use_rotate_around_active", icon="PLUGIN")
	self.layout.separator()
	self.layout.operator(LocalViewEx.bl_idname, icon="ZOOM_OUT")

