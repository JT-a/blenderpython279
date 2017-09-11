#NEW MENUS! 
#for easy to access common functionality

import bpy, bgl
from bpy.props import *


def unlock_objects(scn):
	#look for visible objects
	active_layers = [i for i, l in enumerate(scn.layers) if l]
	for obj in scn.objects:
		for i in active_layers:
			if obj.layers[i] and not obj.hide and obj.hide_select:
				#unlock them
				obj.hide_select = False

#UNLOCKS ALL VISIBLE OBJECTS
class OBJECT_OT_hide_select_clear(bpy.types.Operator):
	"""Unlocks all visible objects"""
	bl_idname = "object.hide_select_clear"
	bl_label = "Clear All Restrict Select"

	def execute(self, context):
		scn = context.scene

		unlock_objects(scn) 

		return {'FINISHED'}

bpy.utils.register_class(OBJECT_OT_hide_select_clear)

#added to object specials 
class ObjectDisplayMenu(bpy.types.Menu):
	bl_label = "Display Menu"
	bl_idname = "OBJECT_MT_display_menu"

	def draw(self, context):
		layout = self.layout
		obj = context.object
		
		if obj:
			layout.prop(obj, "show_name")
			layout.prop(obj, "show_axis")
			layout.prop(obj, "show_wire")
			layout.prop(obj, "show_x_ray")

bpy.utils.register_class(ObjectDisplayMenu)

def object_specials(self, context):
	layout = self.layout
	obj = context.object


	layout.operator("object.hide_select_clear")
	layout.operator_context = 'INVOKE_DEFAULT'
	layout.operator("view3d.ruler")

	if obj.type in  ["MESH", "CURVE"]:
		layout.operator("object.shade_smooth")
		layout.operator("object.shade_flat")
	layout.separator()
	layout.prop_menu_enum(obj, "draw_type", text = "Draw Type")
	layout.menu(ObjectDisplayMenu.bl_idname)
	layout.separator()
	#row.label(text="", icon='RESTRICT_VIEW_OFF')
	layout.prop(obj, "hide", icon="RESTRICT_VIEW_OFF")
	layout.prop(obj, "hide_select", icon = "RESTRICT_SELECT_OFF")
	layout.prop(obj, "hide_render", icon = "RESTRICT_RENDER_OFF")

def curve_specials(self, context):
	layout = self.layout
	curve = context.object.data
	layout.prop(curve, "show_handles")
	layout.prop(curve, "show_normal_face")

screen_icons = {
	"3D View Full": "GROUP",
	"Animation": "IPO",
	"Compositing": "NODETREE",
	"Default": "OBJECT_DATA",
	"Game Logic": "LOGIC",
	"Motion Tracking": "RENDER_ANIMATION",
	"Scripting": "TEXT",
	"UV Editing": "IMAGE_COL",
	"Video Editing": "SEQUENCE",
}


def change_screen(self, context):

	if self.active_screen in [scr.name for scr in bpy.data.screens] and self.active_screen != context.window.screen.name:
		context.window.screen = bpy.data.screens[self.active_screen]

items = []  

def get_screens(self, context):
	global items
	if len(items)!= len(bpy.data.screens):
		items = []
		for i, scr in enumerate(bpy.data.screens):
			if scr.name != "temp":
				if scr.name in screen_icons:
					icon = screen_icons[scr.name]
				else:
					icon = "SPLITSCREEN"
				items.append((scr.name, scr.name, "", icon, i))
	
	return items

#identifier, label, description,  icon,  enum 
bpy.types.Scene.active_screen = EnumProperty(items = get_screens, update = change_screen)


class WM_OT_change_screen(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "wm.change_screen"
	bl_label = "Selects screen"
	
	screen = StringProperty(default = "")
	
	@classmethod
	def poll(cls, context):
		return len(bpy.data.screens)

	def execute(self, context):
		#check current scene
		current_scn = context.scene
		for screen in bpy.data.screens:
			if screen.scene != current_scn:
				screen.scene = current_scn
		context.window.screen = bpy.data.screens[self.screen]
		
		return {'FINISHED'}

class WINDOW_MT_screen_types(bpy.types.Menu):
	bl_label = "Screens"
	bl_idname = "WINDOW_MT_screen_types"

	def draw(self, context):
		layout = self.layout
		
		for src in bpy.data.screens:
			if src.name != "temp":
				try:
					icon = screen_icons[src.name]
				except:
					icon = "SPLITSCREEN"
				layout.operator("wm.change_screen", icon = icon, text = src.name).screen = src.name

def draw_callback_px(self, context):
	#print("mouse points", len(self.mouse_path))

	font_id = 0  # XXX, need to find out how best to get this.
	w = self.aw
	h = self.ah
	mx = self.mx
	my = self.my
			
	# draw some text
#   blf.position(font_id, 15, 30, 0)
#   blf.size(font_id, 20, 72)
	#blf.draw(font_id, "Hello Word " + str(len(self.mouse_path)))

	# 50% alpha, 2 pixel width line
	bgl.glEnable(bgl.GL_BLEND)
	bgl.glLineWidth(1)

	if self.direction == "VERTICAL":
		
		bgl.glColor4f(1.0, 1.0, 1.0, 0.5)
		bgl.glBegin(bgl.GL_LINE_STRIP)
		bgl.glVertex2i(mx, 0)
		bgl.glVertex2i(mx, h)
		bgl.glEnd()
		
		bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
		bgl.glBegin(bgl.GL_LINE_STRIP)
		bgl.glVertex2i(mx+1, 0)
		bgl.glVertex2i(mx+1, h)	 
		bgl.glEnd()
		
	elif self.direction == "HORIZONTAL":
		bgl.glColor4f(1.0, 1.0, 1.0, 0.5)
		bgl.glBegin(bgl.GL_LINE_STRIP)
		bgl.glVertex2i(0, my)
		bgl.glVertex2i(w, my)
		bgl.glEnd()
		
		bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
		bgl.glBegin(bgl.GL_LINE_STRIP)
		bgl.glVertex2i(0, my+1)
		bgl.glVertex2i(w, my+1)
		bgl.glEnd()
	

	# restore opengl defaults
	bgl.glLineWidth(1)
	bgl.glDisable(bgl.GL_BLEND)
	bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class GestureSplitOperator(bpy.types.Operator):
	'''Split the screen area with the move of mouse/tablet pen'''
	bl_idname = "screen.split_gesture"
	bl_label = "Split Screen Area"
	#bl_options = {"REGISTER"}
	
	mouse_x = IntProperty()
	mouse_y = IntProperty()
	limit = IntProperty(default = 30)
	direction = StringProperty()
	flip_key = "F5"
		
	def modal(self, context, event):
		context.area.tag_redraw()

		if self.direction:
			context.area.header_text_set(self.flip_key + ": Change Axis. ESC: Cancel")
		else:
			context.area.header_text_set("Move the mouse vertically or horizontally.")
			
		if event.type == 'MOUSEMOVE':
			#self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))
			self.mx = event.mouse_region_x
			self.my = event.mouse_region_y
			
			#print(self.mx, self.my, context.area.width, self.direction)			
			if abs(self.mx - self.mouse_x) > self.limit and self.direction == "":
				self.direction = "HORIZONTAL"
			elif abs(self.my - self.mouse_y) > self.limit and self.direction == "":
				self.direction = "VERTICAL"
			
			
		elif event.type == self.flip_key and event.value == "PRESS":
			if self.direction == "HORIZONTAL":
				self.direction = "VERTICAL"
			else:
				self.direction = "HORIZONTAL"
			
		elif event.type == 'LEFTMOUSE' and self.direction:
			print(self.mx, self.my)
			self.space_type.draw_handler_remove(self._handle, 'WINDOW')
			if self.direction == "HORIZONTAL":
				factor = (event.mouse_y - self.ay) / self.ah
			else:
				factor = self.mx / self.aw
			context.area.header_text_set()
			bpy.ops.screen.area_split(direction = self.direction, factor = factor)
			return {'FINISHED'}

		elif event.type in {'RIGHTMOUSE', 'ESC'}:
			self.space_type.draw_handler_remove(self._handle, 'WINDOW')
			context.area.header_text_set()
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		print(event.type)
		# the arguments we pass the the callback
		args = (self, context)
		self.mouse_x = event.mouse_region_x
		self.mouse_y = event.mouse_region_y
		self.mx = event.mouse_region_x
		self.my = event.mouse_region_y
		self.aw = context.area.width
		self.ah = context.area.height
		self.ax = context.area.x
		self.ay = context.area.y
		self.space_type = type(context.space_data)
		# Add the region OpenGL drawing callback
		# draw in view space with 'POST_VIEW' and 'PRE_VIEW'
		self._handle = self.space_type.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

		#self.mouse_path = []

		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

#icons = ["VIEW3D", "TIME", "IPO", "ACTION"]	
#items = [("ITEM%i" % i, "Item %i" % i, "", icon, i) for i, icon in enumerate(icons)]
#bpy.types.Scene.test = EnumProperty(items = items)

class LayoutMenu(bpy.types.Menu):
	bl_label = "Layout"
	bl_idname = "WINDOW_MT_layout_menu"

	def draw(self, context):
		layout = self.layout
		area = context.area
		
		row = layout.menu_pie()
		#screen types
		row.menu("WINDOW_MT_screen_types")
		#row.props_enum(context.scene, "active_screen")

		#properties context
		pareas = [parea for parea in context.screen.areas if parea.type == "PROPERTIES"]
		if pareas:
			parea = pareas[0]
			spc = parea.spaces.active
			row.props_enum(spc , "context")

		#area types
		row.props_enum(area, "type")
		row = row.column(align=True)
		#row.operator_context = "EXEC_DEFAULT"
		#row.operator("screen.split", text="Split Horizontal")
		#row.operator("screen.area_join")
		row.operator("screen.split_gesture", text="Split Screen")
	
		#op2 = row.operator("screen.area_split", text="Split Vertical")
		#op2.direction = "VERTICAL"
		
		
#bpy.utils.register_class(LayoutMenu)

#VIEW3D TOOLS
bpy.types.VIEW3D_MT_object_specials.append(object_specials)
bpy.types.VIEW3D_MT_edit_curve_specials.append(curve_specials)
print("Menus done.")

		
def register():
	bpy.utils.register_module(__name__)
			
def unregister():
	bpy.utils.unregister_module(__name__)
			
if __name__ == "__main__":
	register()
