# UV/画像エディター > 「ビュー」メニュー

import bpy

################
# オペレーター #
################

class Reset2DCursor(bpy.types.Operator):
	bl_idname = "image.reset_2d_cursor"
	bl_label = "Reset the position of the cursor"
	bl_description = "2D cursor moves in the lower left"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		("C", "Central", "", 1),
		("U", "Shang", "", 2),
		("RU", "On the upper right", "", 3),
		("R", "Right", "", 4),
		("RD", "Lower right", "", 5),
		("D", "Xia", "", 6),
		("LD", "Lower left", "", 7),
		("L", "Left", "", 8),
		("LU", "On the top left", "", 9),
		]
	mode = bpy.props.EnumProperty(items=items, name="Location", default="LD")
	
	def execute(self, context):
		if (bpy.context.edit_image):
			x, y = bpy.context.edit_image.size
		else:
			x = 256
			y = 256
		if (self.mode == "C"):
			bpy.context.space_data.cursor_location = [x/2, y/2]
		elif (self.mode == "U"):
			bpy.context.space_data.cursor_location = [x/2, y]
		elif (self.mode == "RU"):
			bpy.context.space_data.cursor_location = [x, y]
		elif (self.mode == "R"):
			bpy.context.space_data.cursor_location = [x, y/2]
		elif (self.mode == "RD"):
			bpy.context.space_data.cursor_location = [x, 0]
		elif (self.mode == "D"):
			bpy.context.space_data.cursor_location = [x/2, 0]
		elif (self.mode == "LD"):
			bpy.context.space_data.cursor_location = [0, 0]
		elif (self.mode == "L"):
			bpy.context.space_data.cursor_location = [0, y/2]
		elif (self.mode == "LU"):
			bpy.context.space_data.cursor_location = [0, y]
		return {'FINISHED'}

class TogglePanelsA(bpy.types.Operator):
	bl_idname = "image.toggle_panels_a"
	bl_label = "Toggle Panel (mode A)"
	bl_description = "The properties/tool shelf \"both display\" / \"both hide\" toggle"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		toolW = 0
		uiW = 0
		for region in context.area.regions:
			if (region.type == 'TOOLS'):
				toolW = region.width
			if (region.type == 'UI'):
				uiW = region.width
		if (1 < toolW or 1 < uiW):
			if (1 < toolW):
				bpy.ops.image.toolshelf()
			if (1 < uiW):
				bpy.ops.image.properties()
		else:
			bpy.ops.image.toolshelf()
			bpy.ops.image.properties()
		return {'FINISHED'}

class TogglePanelsB(bpy.types.Operator):
	bl_idname = "image.toggle_panels_b"
	bl_label = "Toggle Panel (mode B)"
	bl_description = "\"Panel both hide\" → show only the tool shelf → show only properties → \"Panel both display\" for toggle"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		toolW = 0
		uiW = 0
		for region in context.area.regions:
			if (region.type == 'TOOLS'):
				toolW = region.width
			if (region.type == 'UI'):
				uiW = region.width
		if (toolW <= 1 and uiW <= 1):
			bpy.ops.image.toolshelf()
		elif (toolW <= 1 and 1 < uiW):
			bpy.ops.image.toolshelf()
		else:
			bpy.ops.image.toolshelf()
			bpy.ops.image.properties()
		return {'FINISHED'}

class TogglePanelsC(bpy.types.Operator):
	bl_idname = "image.toggle_panels_c"
	bl_label = "Toggle Panel (mode C)"
	bl_description = "\"Panel both hide\" → \"show only the tool shelf → show only the properties. The toggle"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		toolW = 0
		uiW = 0
		for region in context.area.regions:
			if (region.type == 'TOOLS'):
				toolW = region.width
			if (region.type == 'UI'):
				uiW = region.width
		if (toolW <= 1 and uiW <= 1):
			bpy.ops.image.toolshelf()
		elif (1 < toolW and uiW <= 1):
			bpy.ops.image.toolshelf()
			bpy.ops.image.properties()
		else:
			bpy.ops.image.properties()
		return {'FINISHED'}

################
# サブメニュー #
################

class ShortcutsMenu(bpy.types.Menu):
	bl_idname = "IMAGE_MT_view_shortcuts"
	bl_label = "Shortcut for registration"
	bl_description = "Shortcuts and features that might come in handy"
	
	def draw(self, context):
		self.layout.operator(TogglePanelsA.bl_idname, icon="PLUGIN")
		self.layout.operator(TogglePanelsB.bl_idname, icon="PLUGIN")
		self.layout.operator(TogglePanelsC.bl_idname, icon="PLUGIN")

class Reset2DCursorMenu(bpy.types.Menu):
	bl_idname = "IMAGE_MT_view_reset_2d_cursor"
	bl_label = "Reset the position of the cursor"
	bl_description = "Resets the position of the cursor"
	
	def draw(self, context):
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="Shang").mode = 'U'
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="Right").mode = 'R'
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="Xia").mode = 'D'
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="Left").mode = 'L'
		self.layout.separator()
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="On the upper right").mode = 'RU'
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="Lower right").mode = 'RD'
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="Lower left").mode = 'LD'
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="On the top left").mode = 'LU'
		self.layout.separator()
		self.layout.operator(Reset2DCursor.bl_idname, icon='PLUGIN', text="Central").mode = 'C'

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
		self.layout.menu(Reset2DCursorMenu.bl_idname, icon='PLUGIN')
		self.layout.separator()
		self.layout.menu(ShortcutsMenu.bl_idname, icon="PLUGIN")
	if (context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]
