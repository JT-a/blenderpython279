import bpy
from bpy.props import *
print(30*"-")

class Editor():
	
	def __init__(self, editor):
		self._editor = editor
		
	def videos(self, channel = 0):
		return sorted([Clip(v) for v in self._editor.sequences if v.channel == channel or channel == 0], key = lambda v: (v.y, v.x))
	
	@property
	def active(self):
		return self._editor.active_strip

editor = Editor(bpy.context)

class Clip(bpy.types.MovieSequence):
	
	def __init__(self, v):
		self = v
#		self.editor = Editor(editor)
#		self = editor.active_strip
#		print("SELF", self)
#		print(self.frame_start)
		#super(Clip).__init__(self)
		
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
	
	#calculates the gap between clips
	@staticmethod
	def gap(v1, v2):
		videos = [v1, v2]
		if v1.x < v2.x:
			videos.reverse()
		return videos[1].x - (videos[0].x + videos[0].width)
	
	@staticmethod
	def distance(v1, v2):
		if isinstance(v1, int):
			return abs(v2-v1)
		return abs(v1.x - v2.x)
	
	#this function determines if the clip can move horizontally without overlapping with other clips
	#if it overlaps will find the next available room to place the clip
#
#	
#	def move(self, dx, dy):
#		dx = self.calculate_offset(dx)
#		print(dx)
#		self.frame_start += dx 
#		if self.channel + dy >0:
#			self.channel += dy
	
	def __repr__(self):
		return "%s('%s'(%i, %i))" % (self.__class__.__name__, self.name, self.x, self.y)
#c = bpy.context
#editor = c.scene.sequence_editor
#active = Clip(editor.active)

def gap(v1, v2):
	values = [v1, v2]
	if v1[0] > v2[0]:
		values.reverse()
	#print("values", values)
	return values[1][0] - values[0][1]

class CLIP_OT_move(bpy.types.Operator):
	"""Move an object with the mouse, example"""
	bl_idname = "clip.move"
	bl_label = "Clip Move"
#	bl_options = {'REGISTER', 'UNDO'}
	

	orig_frame = IntProperty()
	orig_channel = IntProperty()
	last_frame = IntProperty()
	
	def modal(self, context, event):
		dx, dy = 0, 0
		#editor = context.scene.sequence_editor
	
		#videos = editor.sequences
		
		if event.type in {'RIGHTMOUSE', 'ESC'}:	
			self.strip.frame_start = self.orig_frame			
			self.strip.channel = self.orig_channel
			self.strip.frame_final_duration = self.orig_width
			context.area.header_text_set()
			return {'CANCELLED'}
		elif event.type == "RET":
			context.area.header_text_set()	
			return {'FINISHED'}
		
		inc = 1
		if event.shift:
			inc = 10
		
		if event.value == "PRESS":
			if event.type == "F":
				self.fit = not self.fit
			elif event.type == 'LEFT_ARROW':
				dx = self.strip.calculate_offset(-inc, self.orig_width, self.fit)
			elif event.type == "RIGHT_ARROW":
				#dx = self.strip.calculate_offset(inc, self.orig_width, self.fit)
				dx = 0
				self.fit = True
				#get videos on the right
				intervals = [(v.x, v.width, v.tail) for v in self.editor.videos(self.strip.channel) if v.x > self.strip.x]
				last_pos = (self.strip.x, self.strip.width)
				for v in intervals:
					print(v)							
					
			elif event.type == "UP_ARROW":
				dx, dy = self.diff, 1
			elif event.type == "DOWN_ARROW":
				dx, dy = self.diff, -1
#			
##			#record where the clip should end horizontally
#			self.last_frame = self.strip.frame_start + dx
#			print(dx, dy)
##			#move the clip
#			bpy.ops.transform.seq_slide('INVOKE_DEFAULT', value = (dx, dy))
##			
##			#calculate the difference where it landed.
#			self.diff = self.last_frame - self.strip.x
##			self.total[0] += dx - self.diff
##			self.total[1] += dy

		fit = "ON" if self.fit else "OFF"
		context.area.header_text_set("Offset: (%i, %i) Fit: %s" % (dx, dy, fit))
		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		self.strip = Clip(context.scene.sequence_editor.active_strip)
		self.editor = Editor(context.scene.sequence_editor)
		
		self.orig_frame = self.strip.x
		self.orig_channel = self.strip.channel
		self.orig_width = self.strip.width
		self.fit = False
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}
	
import sys, inspect
classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

def register():
	for name, cls in classes:
		try:
			bpy.utils.register_class(cls)
		except Exception as e:
			print(e)
	
def unregister():
	for name, cls in classes:
		try:
			bpy.utils.unregister_class(cls)
		except Exception as e:
			print(e)

if __name__ == "__main__":
	register()
