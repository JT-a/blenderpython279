import bpy
from bpy.props import *
#print(30*"-")

# PANELS 
from ui_tune_up.utils import operator_exists

#enable curve simplify addon
if not operator_exists("graph.simplify"):
	from curve_simplify import GRAPH_OT_simplify

#simplify curves moved to animation editor
class SimplifyCurvesPanel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Simplify Curves"
	bl_idname = "GRAPH_PT_simplify"
	bl_space_type = 'GRAPH_EDITOR'
	bl_region_type = 'UI'
	#bl_context = "object"

	def draw(self, context):
		layout = self.layout

		obj = context.object

		row = layout.row()
		row.operator("graph.simplify")

# HEADERS
def purge(collection):
	removed = 0
	for item in collection:
		if item.users == 0 and item.use_fake_user == False:
			print("%s: %s removed." % (item.__class__.__name__, item.name))
			collection.remove(item)
			removed += 1
	return removed

#FIXED ON 2.76
#draw build proxy at VSE proxy panel
#def draw_proxy(self, context):
#	layout = self.layout

#	row = layout.row()
#	row.operator("sequencer.rebuild_proxy")

#def is_connected(node):
#	for input in node.inputs:
#		if input.links:
#			return True
#	
#	for output in node.outputs:
#		if output.links:
#			return True

#	return False

class PurgeBlendData(bpy.types.Operator):
	"""Purge Blend Data"""
	bl_idname = "wm.purge_data"
	bl_label = "Purge unusued datablocks"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		area = context.area
		# print(area.type)
		
		removed = 0
		if area.type == "VIEW_3D":
			removed = purge(bpy.data.meshes)
			removed += purge(bpy.data.curves)
			removed += purge(bpy.data.materials)
			removed += purge(bpy.data.textures)
			removed += purge(bpy.data.cameras)
			removed += purge(bpy.data.lamps)
			
		elif area.type == "DOPESHEET_EDITOR":
			removed = purge(bpy.data.actions)
		
		elif area.type == "IMAGE_EDITOR":
			removed += purge(bpy.data.images)
			removed += purge(bpy.data.textures)

		elif area.type == "NODE_EDITOR":
			tree = context.space_data.node_tree
			if tree:
				nodes = [node for node in tree.nodes if node.type != "OUTPUT_MATERIAL"]
				for node in nodes:
					if not is_connected(node):
						print("%s: %s removed." % (node.__class__.__name__, node.name))
						tree.nodes.remove(node)
						removed += 1
			
		self.report({'INFO'}, "%s items removed" % removed)				 
		return {'FINISHED'}

def draw_purge_data(self, context):
		layout = self.layout
		if self.bl_space_type == "IMAGE_EDITOR":
			if not context.area.spaces.active.image:
				layout.separator()
			layout.operator("image.make_texture", icon = "TEXTURE", text = "")
		layout.separator()
		layout.operator("wm.purge_data", icon = "GHOST_DISABLED", text = "")
		
class PurgeView3D(bpy.types.Header):
	'''Purge objects, and object data'''
	bl_label = "Purge"
	bl_space_type = "VIEW_3D"

class PurgeDopesheetEditor(bpy.types.Header):
	'''Purge objects, and object data'''
	bl_label = "Purge"
	bl_space_type = "DOPESHEET_EDITOR"

class PurgeImageEditor(bpy.types.Header):
	'''Purge objects, and object data'''
	bl_label = "Purge"
	bl_space_type = "IMAGE_EDITOR"

class PurgeNodeEditor(bpy.types.Header):
	'''Purge objects, and object data'''
	bl_label = "Purge"
	bl_space_type = "NODE_EDITOR"

headers = [PurgeView3D, PurgeImageEditor, PurgeDopesheetEditor, PurgeNodeEditor]
for h in headers:
	h.draw = draw_purge_data

#bpy.types.SpaceTextEditor.last_text = StringProperty(default = "")
#
#class LastText(bpy.types.Header):
#	'''Purge objects, and object data'''
#	bl_label = "Last text"
#	bl_space_type = "TEXT_EDITOR"
#	
#	def __init__(self):
#		print("doit")
#		
#	def draw(self, context):
#		layout = self.layout
#		layout.label("Last: None")
		
		
#bpy.types.SEQUENCER_PT_proxy.append(draw_proxy)
print("ui done.")

def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()