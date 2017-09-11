import bpy
from bpy.props import *
from mathutils import Vector
from ui_tune_up.utils import dd
dd(30*"-")

#Clip wrapper for easier access to attributes
class Clip(bpy.types.MovieSequence):
	
	def __init__(self, v):
		self = v

	#enable to store additional properties like orig_width 
	def __setattr__(self, attr, value):
		if attr == "x":
			attr = "frame_start"
			value = value - self.frame_offset_start
		elif attr == "tail":
			attr = "frame_start"
			value = value - self.frame_offset_start - self.frame_final_duration
		elif attr == "width":
			attr = "frame_offset_end"
			value = self.frame_offset_end + self.frame_final_duration - value
		bpy.types.MovieSequence.__setattr__(self, attr, value)
		
	@property
	def x(self):
		return self.frame_start + self.frame_offset_start
	
	@property
	def y(self):
		return self.channel
	
	@property
	def width(self):
		return self.frame_final_duration
	
	@property
	def tail(self):
		return self.x + self.width
	
	@property
	def length(self):
		return self.frame_final_duration + self.frame_offset_start + self.frame_offset_end
	
	def __repr__(self):
		return "%s('%s'(%i, %i, %i))" % (self.__class__.__name__, self.name, self.x, self.width, self.tail)
	
	def __str__(self):
		return self.__repr__()

#Editor wrapper
class Editor(bpy.types.SequenceEditor):
	
	def __init__(self, editor):
		self = editor
	
	def videos(self, channel = 0):
		if self.meta_stack:
			videos = self.meta_stack[0].sequences
		else:
			videos = self.sequences
			
		return sorted([Clip(v) for v in videos if v.channel == channel or channel == 0], key = lambda v: (v.y, v.x))
	
	@property
	def active(self):
		if not self.active_strip:
			if len(self.sequences):
				frame = bpy.context.scene.frame_current
				dx = None
				video = None
				for vid in self.sequences:
					v = Clip(vid)
					dist = min(distance(v.x, frame),distance(v.tail, frame))
					if not dx:
						dx = dist
						video = vid
					if dist < dx:
						dx = dist
						video = vid
				self.active_strip = video	
			
		if self.active_strip:
			return Clip(self.active_strip)
	
	#returns a set of all video tips and tails
	@property
	def bounds(self):
		return set([v.x for v in videos] + [v.tail for v in videos])
	
	#returns the videos to active's right or left hand
	def closests(self, right = True):
		active = self.active
		if not active:
			return
		
		if right:
			return [v for v in self.videos(active.y) if v.x > active.x] 
		else:
			vids = [v for v in self.videos(active.y) if v.x < active.x]
			vids.reverse()
			return vids
	@property
	def selected(self):
		return [Clip(v) for v in self.sequences if v.select]
	
#utility functions

def clamp(value, minv, maxv):
	return max(minv, min(value, maxv))

def distance(v1, v2):
	if v1.__class__.__name__ in ["int", "float"]:
		return abs(v2-v1)
	return abs(v1.x - v2.x)

#gap between 2 clips 
#returns start frame and gap's width
def gap(v1, v2):
	videos = [v1, v2]
	if v1.x > v2.x:
		videos.reverse()
	
	return videos[0].tail, videos[1].x - videos[0].tail

#get next available gap, optionally with certain width
def get_gaps(videos, width = 0):
	last = None
	for v in videos:
		if last:
			gs, gw = gap(last, v)
			#discard gaps with no width
			if gw > 0 and gw >= width:
				return gs, gw
		last = v
	
def move(editor, active, dx, dy, fit):
	
	if dx + dy == 0: return
	
	#width differential and direction
	dw = 0
	right = dx > 0
	
	if dy:
		#dx = 0
		dw = active.orig_width - active.width
		videos = []
	else:
		#get videos to the left or right on the same channel
		videos = editor.closests(right)

	if videos:
		closest = videos[0]
		gs, gw = gap(active, closest)
		
		if gw == 0:
			dd("gotta jump", "Fit", fit)

			g = get_gaps(videos, (not fit) * active.width)
			
			if g:
				dd("found gap", g)
				gs, gw = g
				#clamp to the original width

				if not right: gs += gw 
				gw = min(gw, active.orig_width)

			else:
				dd("no gaps, find an edge")
				#furthest edge 
				gs = max([videos[-1].x, videos[-1].tail], key = lambda x: distance(x, active.x))
				gw = active.orig_width
		
			
			dw = gw - active.width
			dx = gs -active.x - (not right) * active.orig_width
			
			dd(5*"%s\t" % ("dx", "owidth", "gs", "gw", "dw"))
			dd(5*"%s\t" % (dx, active.orig_width, gs, gw, dw))  
	
	#return 
	#shrink video
	if dw<0:
		active.frame_offset_end -= dw
	bpy.ops.transform.seq_slide(value = (dx, dy))
	#expand video
	if dw>0:
		active.frame_offset_end -= dw


numbers = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"] + ["NUMPAD_%s" % i for i in range(0, 10)]

class SEQUENCER_OT_move_clip(bpy.types.Operator):
#   """Move an object with the mouse, example"""
	bl_idname = "sequencer.move_clip"
	bl_label = "Move Clip"
	bl_option = {'REGISTER', 'UNDO'}
	
	def modal(self, context, event):
		
		if event.value == "PRESS":
			dx , dy = 0, 0
			#dd(event.type, event.value)
			
			inc = 1 + (event.shift * 9)
				
			if event.type in ["ESC", "RIGHTMOUSE"]:
				#manual undo
				bpy.ops.transform.seq_slide(value = -self.offset)
				self.active.frame_offset_end -= self.active.orig_width -self.active.width
				context.area.header_text_set()
				del self.editor
				del self.active
				dd("oops")
				return {"CANCELLED"}
			
			elif event.type in ["RET", "NUMPAD_ENTER"]:
				dd("done")  
				del self.editor
				del self.active
				context.area.header_text_set()
				return {"FINISHED"}	 
			
			#keyboard inputs
			elif event.type in numbers:
				n = numbers.index(event.type) % 10
				if self.number and self.number!= "-":
					#compensate for the new number
					#this is lazy!, do the maths!
					dx = -int(self.number)
					move(self.editor, self.active, dx, dy, False)
					
				self.number += str(n)
				dx = int(self.number) 
				#dd(self.number)
			elif event.type == "NUMPAD_MINUS":
				
				if self.number and self.number!="-":
					#compensate for the new number
					dx = -int(self.number)
					move(self.editor, self.active, dx, dy, False)
					
					self.number = str(-int(self.number))
					dx = int(self.number)
				else:
					self.number = "-"
				#dd(self.number)
				
			elif event.type == "BACK_SPACE":
				
				if self.number:
					#refactor this pls,... ty
					n = self.number[0:-1]
					dd(self.number, n)
					if not n or n=="-": n = 0
					#dd("compensating", dx)
					dx = -int(self.number)
					move(self.editor, self.active, dx, dy, self.fit)
					
					self.number = str(n)
					dx = int(self.number)
				
						#dx = int(self.number)
					if self.number == "-":
						self.number = ""
					
				dd(self.number)
						
			elif event.type == "F":
				self.fit = not self.fit
					
			if event.type == "RIGHT_ARROW":
				dx, dy = inc, 0
			elif event.type == "LEFT_ARROW":
				dx, dy = -inc, 0
			elif event.type == "UP_ARROW":
				dx, dy = self.diff, 1
			elif event.type == "DOWN_ARROW":
				dx, dy = self.diff, -1
				
			#record the cordinates before moving vertically
			before = self.active.x
			
			move(self.editor, self.active, dx, dy, self.fit)
			
			#look where it landed vertically
			after = self.active.x
				
			self.offset.x = self.active.x - self.start_position[0]
			self.offset.y = self.active.y - self.start_position[1]
			
			if dy == 0:
				self.diff = 0
			else:
				self.diff += before - after
			
		header = "Move Offset: (%i, %i)" % tuple(self.offset)
		header += " (F)it: %s" % ("ON" if self.fit else "OFF",)
		context.area.header_text_set(header)
		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		self.editor = Editor(context.scene.sequence_editor)
		self.active = self.editor.active
		self.active.select_left_handle = False
		self.active.select_right_handle = False
		
		if not self.active:
			del self.editor
			return {'FINISHED'}
		
		self.active.orig_width = self.active.width
		
		self.start_position = self.active.x, self.active.y
		self.offset = Vector([0,0])
		self.diff = 0
		self.fit = False
		self.number = ""
		
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}
	
def navigate(self, context):
	
	direction = self.direction
	
	editor = Editor(context.scene.sequence_editor)
	active = editor.active
	videos = editor.videos()
	#dd(videos)
	if not active: return

	if direction == "LEFT":
		close_left = [v for v in videos if v.x < active.x]

		if close_left:
			return min(close_left, key = lambda v: (distance(v.y, active.y), distance(v, active)))
	
	elif direction == "RIGHT":
		close_right = [v for v in videos if v.x > active.x]
		
		if close_right:
			return min(close_right, key = lambda v: (distance(v.y, active.y), distance(v, active)))

	elif direction == "UP":
		close_up = sorted([v for v in videos if v.y > active.y], key = lambda v: distance(v, active))
		#dd("up", close_up)
		if close_up:
			return min(close_up, key = lambda v: v.y)
	
	elif direction == "DOWN":
		close_down = sorted([v for v in videos if v.y < active.y], key = lambda v: distance(v, active))
		
		if close_down:
			return max(close_down, key = lambda v: v.y)

directions = [
	("UP", "Up", " ", "",  0),
	("DOWN", "Down", " ", "",  1),
	("LEFT", "Left", " ", "", 2),
	("RIGHT", "Right", " ", "",  3)
]   
class SEQUENCER_OT_navigate(bpy.types.Operator):
	"""Sequencer Keyboard Navigation"""
	bl_idname = "sequencer.navigate"
	bl_label = "Sequencer Navigate"

	direction = EnumProperty(items = directions, name = "Direction")
	extend = BoolProperty(default = False, name = "Extend")
	
	@classmethod
	def poll(cls, context):
		return context.area.type == "SEQUENCE_EDITOR" and len(context.scene.sequence_editor.sequences)
	
	def invoke(self, context, event):
		scn = context.scene
		editor = Editor(context.scene.sequence_editor)
		active = editor.active
		active.select_left_handle = False
		active.select_right_handle = False
		#print(event.shift)
			  
		vid = navigate(self, context)
		
		if vid:
			if not self.extend:
				for v in editor.videos():
					v.select = False
		
			vid.select = True
			editor.active_strip = vid

		self.extend = False 
		return {'FINISHED'}

#if select: jump to active clip's tip or tail
#if not, jump  to next tip or tail using tail argument as direction
class SEQUENCER_OT_jump(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "sequencer.jump"
	bl_label = "Goto"
	
	tail = BoolProperty(default = True)
	select = BoolProperty(default = False)
	
#   @classmethod
#   def poll(cls, context):
#	   return True

	def execute(self, context):
		scn = context.scene
		editor = Editor(scn.sequence_editor)
		tail = self.tail
		dd("execute jump", self.select)
		
		if self.select:
			active = editor.active
			if active:
				scn.frame_current = active.x + tail * active.width
		else:
			videos = editor.videos
			current = scn.frame_current

			if tail:
				bounds = [i for i in editor.bounds if i > current]
			else:
				bounds = [i for i in editor.bounds if i < current]
		
			if bounds:
				frame = bounds[tail-1]
				scn.frame_current = frame
				
		return {'FINISHED'}
	
#changes the jump behaviour in the sequence editor
#at the sequence editor uses sequencer.jump
#anywhere else uses screen.frame_jump
class SCREEN_OT_smart_frame_jump(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "screen.smart_frame_jump"
	bl_label = "Jump to Endpoint"
	
	end = BoolProperty(name = "Last Frame", default = False)
	
#   @classmethod
#   def poll(cls, context):
#	   return True
#	   #return context.active_object is not None

	def execute(self, context):
		#dd(context.area.type)
		if context.area.type == "SEQUENCE_EDITOR":
			bpy.ops.sequencer.jump(select = True, tail = self.end)
		else:
			bpy.ops.screen.frame_jump(end = self.end)
		return {'FINISHED'}
	
class CLIP_OT_set_name(bpy.types.Operator):
	"""Sets a clip property"""
	bl_idname = "clip.set_property"
	bl_label = "Set Property"

	value = StringProperty(name = "Name")

	@classmethod
	def poll(cls, context):
		return context.scene.sequence_editor.active_strip is not None
	
	def invoke(self, context, event):
		active = context.scene.sequence_editor.active_strip
		self.value = active.name
		return context.window_manager.invoke_props_dialog(self)
		
	def execute(self, context):
		strip = context.scene.sequence_editor.active_strip
		if self.value and self.value != strip.name:
			strip.name = self.value
		return {'FINISHED'}

#extends sequencer.snap by aligning to a clips tail
class SEQUENCER_OT_smart_snap(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "sequencer.smart_snap"
	bl_label = "Sequencer Snap"
	
	back = BoolProperty(name = "Back", default = False)
	
	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		dd(self.bl_label)
		frame = context.scene.frame_current
		dd(frame, self.back)
		if self.back:
			editor = Editor(context.scene.sequence_editor)
			active = editor.active
			frame -= active.width
		bpy.ops.sequencer.snap(frame = frame)
		return {'FINISHED'}

	
class SEQUENCER_OT_smart_slip(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "sequencer.smart_slip"
	bl_label = "Smart Slip"
	#bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		return context.scene.sequence_editor.active_strip is not None

	def modal(self, context, event):
	
		if event.value == "PRESS":
			if event.type in ["ESC", "RIGHTMOUSE"]:
				self.active.frame_start = self.trim[0]
				self.active.frame_offset_start = self.trim[1]
				self.active.frame_offset_end = self.trim[2]
				context.area.header_text_set()
				dd("oops")
				del self.active 
				del self.editor
				return {'CANCELLED'}
			
			elif event.type in ['RET', "NUMPAD_ENTER"]:
				context.area.header_text_set()
				del self.active 
				del self.editor
				dd("done")
				return {'FINISHED'}
		
			dx = 1 + (event.shift * 9)
			inc = 0
			
			if event.type == "W":
				self.w = not self.w
			
			if self.w:
				dx = self.active.width
				
			if event.type == "LEFT_ARROW":
				start = self.active.frame_offset_start
				if self.active.frame_offset_start < dx:
					inc = -start
				else:
					inc = -dx

			elif event.type == "RIGHT_ARROW":
				end = self.active.frame_offset_end
				if self.active.frame_offset_end < dx:
					inc = end
				else:
					inc = dx
				
			dd(self.active.length, self.active.width, inc)
			if abs(inc) > 0:
				self.active.frame_offset_end -= inc
				self.active.frame_offset_start += inc
				self.active.frame_start -= inc
				
				self.offset += inc
		
		header = "Slip Offset: %i" % self.offset
		header += " Width: %s" % ("ON" if self.w else "OFF",)
		context.area.header_text_set(header)
		return {'RUNNING_MODAL'}
	
	def invoke(self, context, event):
		dd("sliping", event.type)
		self.editor = Editor(context.scene.sequence_editor)
		self.active = self.editor.active
		self.trim = (self.active.frame_start, self.active.frame_offset_start, self.active.frame_offset_end)
		self.offset = 0
		self.w = False
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

#bpy.utils.preview = True
#
#class ANIMATION_smart_preview_range(bpy.types.Operator):
#	"""Toogle on off preview range"""
#	bl_idname = "anim.smart_preview_range"
#	bl_label = "Smart Preview Range"
#	bl_options = {'REGISTER', 'UNDO'}
#	
#	preview = BoolProperty()
#	
##	@classmethod
##	def poll(cls, context):
##		True
##		return context.active_object is not None
#
#	def execute(self, context):
#		
#		if context.area.type == "SEQUENCE_EDITOR":
#			editor = Editor(context.scene.sequence_editor)
#			active = editor.active
#			dd(self.preview)
#			if bpy.utils.preview:
#				bpy.ops.anim.previewrange_set('EXEC_DEFAULT', xmin=active.x, xmax=active.tail, ymin=1, ymax=10)
#			else:
#				bpy.ops.anim.previewrange_clear()
#			
#			bpy.utils.preview = not bpy.utils.preview
#			
#		return {'FINISHED'}

class SEQUENCER_OT_trim(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "sequencer.trim"
	bl_label = "Trim Extends a clip"
	
	trim_out = BoolProperty(name = "Out", default = True)
	reset = BoolProperty(default = False)
	
	@classmethod
	def poll(cls, context):
		return context.scene.sequence_editor.active_strip is not None

	def execute(self, context):
		scn = context.scene
		frame = scn.frame_current
		editor = Editor(scn.sequence_editor)
		active = editor.active
		
		if self.reset:
			if self.trim_out:
				active.frame_offset_end = 0
			else:
				active.frame_offset_start = 0
			return {'FINISHED'}
		
		#refactor this pls, dont be lazy
		median = active.length / 2
		axis = active.x + median
		d = distance(axis, frame)
		offset = int(d - median)
		#print(offset)
		dd("triming", self.trim_out, active.type, hasattr(active, "frame_offset_end"))
		if active.type == "COLOR":
			if not self.trim_out:
				active.frame_start = frame
			
			active.frame_final_duration += offset 
		else:
			if self.trim_out:
				#print("out")
				dout = active.tail - frame
				if offset > 0: dout = -active.frame_offset_end
				active.frame_offset_end += dout
			else:
				#print("in")
				dout = abs(active.x - frame)
				if offset > 0: dout = -active.frame_offset_start
				active.frame_offset_start += dout	
		
		return {'FINISHED'}

def copy_trim(self, context):
	scn = context.scene
	editor = scn.sequence_editor
	active = editor.active_strip
	selected = [v for v in editor.sequences if v.select]
	for v in selected:
		if v != active:
			dd(v.name)
			v.frame_offset_start = active.frame_offset_start
			v.frame_start = active.frame_start
			v.frame_offset_end = active.frame_offset_end 

class SequencerCopyAttributes(bpy.types.Operator):
	"""Copy Attributes"""
	bl_idname = "sequencer.copy_attributes"
	bl_label = "Copy Attributes"

	cmd = StringProperty()

	@classmethod
	def poll(cls, context):
		return context.scene.sequence_editor.active_strip is not None

	def execute(self, context):
		cmd = self.cmd
		scn = context.scene
		editor = scn.sequence_editor
		active = editor.active_strip
		selected = [v for v in editor.sequences if v.select]

		for v in selected:
			if v != active:
				dd(v.name)
				if cmd == "trim":
					v.frame_offset_start = active.frame_offset_start
					v.frame_start = active.frame_start
					v.frame_offset_end = active.frame_offset_end 
				
				elif cmd == "start":
					v.frame_start = active.frame_start
					
		self.cmd = ""
		return {'FINISHED'}

class SEQUENCER_MT_copy_attributes(bpy.types.Menu):
	bl_label = "Copy Attributes"
	bl_idname = "SEQUENCER_MT_copy_attributes"

	def draw(self, context):
		layout = self.layout

		layout.operator(SequencerCopyAttributes.bl_idname, text="Copy Trim").cmd = "trim"
		layout.operator(SequencerCopyAttributes.bl_idname, text="Copy Start").cmd = "start"
		
def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)

def cross(context):
	
	editor = Editor(context.scene.sequence_editor)
	
	selected = editor.selected
	
	if len(selected) == 2:
		v1, v2 = sorted(selected, key = lambda v: v.x)
		if v1.type == v2.type:
			overlap = v1.tail - v2.x
			if overlap>0:
				if v1.type == "SOUND":
					data_path = "volume"
				else:
					data_path = "blend_alpha"

				if data_path == "volume":
					frame = v1.tail - overlap
					setattr(v1, data_path, 1.0)
					v1.keyframe_insert(data_path, -1, frame)
					setattr(v1, data_path, 0.0)
					v1.keyframe_insert(data_path, -1, v1.tail)
					
				setattr(v2, data_path, 0.0)
				v2.keyframe_insert(data_path, -1, v2.x)
				setattr(v2, data_path, 1.0)
				v2.keyframe_insert(data_path, -1, v2.x + overlap)
					
	
if __name__ == "__main__":
	register()
	cross(bpy.context)
	#test stuff here
	
