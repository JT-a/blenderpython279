#BLENDER OPERATORS
import bpy, bmesh
from bpy.props import *
from ui_tune_up.utils import dd
from ui_tune_up.select_paired_rings import MESH_OT_select_pair_rings
dd(30*"-")

	
### 3D VIEW

#overrides default add bdezier curve
class CURVE_OT_primitive_bezier_curve_add(bpy.types.Operator):
	"""Adds a bezier curve"""
	bl_idname = "curve.primitive_bezier_curve_add"
	bl_label = "Construct a Bezier Curve"

	@classmethod
	def poll(cls, context):
		return context.area.type == "VIEW_3D" and context.mode == "OBJECT"

	def execute(self, context):
		scn = context.scene
		name = "BezierCurve"
		curve = bpy.data.curves.new(name, "CURVE")
		curve.dimensions = "3D"
		curve.fill_mode = "FULL"
		spline = curve.splines.new("BEZIER")
		points = spline.bezier_points
		points[0].handle_left_type = "AUTO"
		points[0].handle_right_type = "AUTO"
		points.add()
		points[1].handle_left_type = "AUTO"
		points[1].handle_right_type = "AUTO"
		points[1].co = [2,0,0]
		obj = bpy.data.objects.new(name, curve)
		obj.location = scn.cursor_location
		bpy.ops.object.select_all(action = "DESELECT")
		scn.objects.link(obj)
		obj.select = True
		scn.objects.active = obj
		return {'FINISHED'}
	
#selects all curve points between 2 points
class CURVE_OT_select_path(bpy.types.Operator):
	"""Select curve path"""
	bl_idname = "curve.select_path"
	bl_label = "Curve Select Path"

	@classmethod
	def poll(cls, context):
		return context.mode == "EDIT_CURVE"
	
	def invoke(self, context, event):
		bpy.ops.view3d.select(toggle=True, location = (event.mouse_region_x, event.mouse_region_y))
		obj = context.object
		spline = obj.data.splines.active
		if spline:
			if spline.type == "BEZIER":
				points = spline.bezier_points
				selection = [i for i, p in enumerate(points) if p.select_control_point == True]
				if len(selection)>1:
					for i in range(min(selection), max(selection)):
						points[i].select_control_point = True
						points[i].select_left_handle = True
						points[i].select_right_handle = True

			else:
				points = spline.points
				selection = [i for i, p in enumerate(points) if p.select == True]
				if len(selection)>1:
					for i in range(min(selection), max(selection)):
						points[i].select = True
		return {'FINISHED'}

	
bpy.utils.last_matrix = None

#toogle quad views and sets lock_rotation to False if necessary
#this is useful to change views without the numpad
#because the perspective view isnt respected when it toggles, it turns into an orthographic view, 
#disable lock rotation helps to counter that behaviour
class SCREEN_OT_toggle_quadviews(bpy.types.Operator):
	"""Toggle quad views and sets RegionView3D.lock_rotation to False"""
	bl_idname = "screen.toggle_quadviews"
	bl_label = "Toogle Unlocked Quadviews"

	@classmethod
	def poll(cls, context):
		return context.area.type == "VIEW_3D"
	
	def execute(self, context):
		
		dd(30*"-")
		quads = len(context.space_data.region_quadviews) > 0
		if quads:
			persp = context.space_data.region_quadviews[-1]
			bpy.utils.last_matrix = persp.view_matrix.copy()
		else:
			persp = context.space_data.region_3d
			if persp.view_perspective == "PERSP":
				bpy.utils.last_matrix = persp.view_matrix.copy()
			
#		if context.space_data.region_quadviews:
#			persp = context.space_data.region_quadviews[-1]
			
		bpy.ops.screen.region_quadview()
		
		#print(bpy.utils.last_matrix)
		#context.space_data.region_3d.lock_rotation = True
		if context.space_data.region_quadviews:
			for q in context.space_data.region_quadviews:
				if q.lock_rotation:
					q.lock_rotation = False
					
		if context.space_data.region_quadviews:
			persp = context.space_data.region_quadviews[-1]
			if bpy.utils.last_matrix:
				persp.view_perspective = "PERSP"
				persp.view_matrix = bpy.utils.last_matrix

				
		return {'FINISHED'}
	
#sets origin to selected on edit mesh
class MESH_OT_origin_set(bpy.types.Operator):
	"""Sets objects origin on edit mesh"""
	bl_idname = "mesh.origin_set"
	bl_label = "Sets objects origin on edit mesh"

	@classmethod
	def poll(cls, context):
		return context.mode == "EDIT_MESH"

	def execute(self, context):
		obj = context.object
		editmode = context.mode == "EDIT_MESH"
		
		bpy.ops.view3d.snap_cursor_to_selected()
		
		if editmode:
			bpy.ops.object.editmode_toggle()

		bpy.ops.object.origin_set(type = "ORIGIN_CURSOR")

		if editmode:
			bpy.ops.object.editmode_toggle()
		
		return {'FINISHED'}

##on edit mode, pressing M key will toggle mark seams over selection
class MESH_OT_smart_mark_seam(bpy.types.Operator):
	"""Toggle Mark Seam on selected edges"""
	bl_idname = "mesh.smart_mark_seam"
	bl_label = "Smart Mark Seam"

	@classmethod
	def poll(cls, context):
		return context.mode == "EDIT_MESH"

	def execute(self, context):
		spc = context.space_data
		sync = context.tool_settings.use_uv_select_sync
		#print("marking seam", spc.type)
		obj = context.object
		me = bmesh.from_edit_mesh(obj.data)
			
		#if not uvsync, get selected edges from the uv editor
		if spc.type == "IMAGE_EDITOR" and not sync:

			uvlayer = me.loops.layers.uv.active
			
			selected_uvs = set()
			posible_edges = set()
			
			#look for selected uvs and related edges
			for e in me.edges:
				for l in e.link_loops:
					uv = l[uvlayer]
					vert = l.vert
					if uv.select:
						selected_uvs.add(vert.index)
						posible_edges.add(e)
			
			#select edges if uvs/vertex are selected
			selected_edges = []
			mark = True
			for e in posible_edges:
				if e.verts[0].index in selected_uvs and e.verts[1].index in selected_uvs:
					selected_edges.append(e)
					if e.select and e.seam:
						mark = False
					
			for e in selected_edges:
				e.seam = mark
				
			bmesh.update_edit_mesh(obj.data)
		else:
			clear = False
			for e in me.edges:
				if e.select and e.seam:
					clear = True
					break
					
			bpy.ops.mesh.mark_seam(clear = clear)
		
		return {'FINISHED'}
	
#applies to graph and sequence editor
class SCREEN_OT_smart_view_selected(bpy.types.Operator):
	"""Performs View All or View selected wheter something is selected or not"""
	bl_idname = "screen.smart_view_selected"
	bl_label = "Smart View Selected"

#	@classmethod
#	def poll(cls, context):
#		return context.active_object is not None

	def execute(self, context):
	
		selected = False
						
		if context.area.type == "GRAPH_EDITOR":	
			for a in bpy.data.actions:
				for c in a.fcurves:
					if c.select:
						for k in c.keyframe_points:
							if k.select_control_point or k.select_right_handle or k.select_left_handle:
								dd(a.name)
								selected = True
								break
			if selected:
				bpy.ops.graph.view_selected(include_handles=True)
			else:
				bpy.ops.graph.view_all()
		elif context.area.type == "SEQUENCE_EDITOR":
			for c in context.scene.sequence_editor.sequences:
				if c.select:
					selected = True
					break
			dd(context.area.type, selected)
			if selected:
				bpy.ops.sequencer.view_selected()
			else:
				bpy.ops.sequencer.select_all(action='TOGGLE')
				bpy.ops.sequencer.view_selected()
				bpy.ops.sequencer.select_all(action='TOGGLE')
			
		return {'FINISHED'}

# FIXED ON BLENDER 2.73
### GRAPH EDITOR
#class GRAPH_OT_show_toggle(bpy.types.Operator):
#	"""Show/Hide selected animation curves"""
#	bl_idname = "graph.show_toggle"
#	bl_label = "Toggle Animation Curves"
#		
#	cmd = EnumProperty(items = [
#		("HIDE", "Hide", "", "", 0),
#		("UNHIDE", "Unhide", "", "", 1),
#		("SOLO", "Solo", "", "", 2)], name="Command")
#	
#	@classmethod
#	def poll(cls, context):
#		return context.space_data.type == "GRAPH_EDITOR"
#
#	def execute(self, context):
#		cmd = self.cmd
#		dd(cmd)
#		for a in bpy.data.actions:
#			for c in a.fcurves:
#				if cmd == "hide":
#					if c.select:
#						c.hide = True
#				elif cmd == "solo":
#					if c.select:
#						c.hide = False
#					else:
#						c.hide = True
#				elif cmd == "unhide":
#					c.hide = False			
#		
#		return {'FINISHED'}
	
#Syncs datablocks names with filenames
#just fix this, is wrong, is renaming datablocks that are ok
def sync_filenames(data):
	i=0
	for f in data:
		if bpy.types.BlendDataTextures in data.mro():
			tex = f
			name = tex.type.capitalize()

			if tex.type == "IMAGE":
				f = tex.image
				if f and f.filepath:
					name = bpy.path.basename(f.filepath)
				else:
					continue

			if tex.name != name:
					print("Renamed:", tex.name, name)
					tex.name = name
					i+=1			

		else:
			if f and f.filepath:
				filename = bpy.path.basename(f.filepath)
				if f.name != filename:
					print("Renamed:", f.name, filename)
					f.name = filename
					i+=1
	return i
				
class SyncFilenames(bpy.types.Operator):
	"""Renames datablocks with the filename or texture type"""
	bl_idname = "wm.sync_filenames"
	bl_label = "Sync Filenames"
	
	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		area = context.area.type
		res = 0
		if area == "TEXT_EDITOR":
			res = sync_filenames(bpy.data.texts)
		elif area == "IMAGE_EDITOR":
			res= sync_filenames(bpy.data.images)
			res += sync_filenames(bpy.data.textures)
			
		plural = "file" if res == 1 else "files"
		
		self.report({'INFO'}, "%s %s renamed." % (res, plural))
		
		return {'FINISHED'}

def draw_sync_filenames(self, context):
	layout = self.layout

	if isinstance(self, bpy.types.Header):
		layout.operator(SyncFilenames.bl_idname, text="", icon = "SHORTDISPLAY")
	else:
		layout.operator(SyncFilenames.bl_idname)

### UV EDITOR

#toggle pin uv
class UV_OT_smart_pin(bpy.types.Operator):
	"""Toggle pin uv"""
	bl_idname = "uv.smart_pin"
	bl_label = "Smart UV Pin"

	@classmethod
	def poll(cls, context):
		return context.space_data.type == "IMAGE_EDITOR" and context.mode == "EDIT_MESH"

	def execute(self, context):
		### REFACTOR THIS!
		print(30*"-")
		obj = context.object
		me = bmesh.from_edit_mesh(obj.data)
		uvlayer = me.loops.layers.uv.verify()
		
		if context.tool_settings.use_uv_select_sync:
			clear = False
				
			for v in me.verts:
				for l in v.link_loops:
					uv = l[uvlayer]
					if v.select and uv.pin_uv:
						clear = True
						break
				if clear: break
			
			bpy.ops.uv.pin(clear = clear)
		else:
			#this works on unsync mode
			pin = True
			for v in me.verts:
				for l in v.link_loops:
					uv = l[uvlayer]
					if uv.pin_uv:
						pin = False
						break
				if not pin: break
			
			for v in me.verts:
				for l in v.link_loops:
					uv = l[uvlayer]
					if uv.select:
						uv.pin_uv = pin
			
			bmesh.update_edit_mesh(obj.data)

		return {'FINISHED'}
			
class UV_OT_smart_select(bpy.types.Operator):
	"""Syncs mesh selection modes to the UV Editor"""
	bl_idname = "uv.smart_select"
	bl_label = "Smart UV Select"

	value = StringProperty()
	
	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		ts = context.tool_settings
		sync = ts.use_uv_select_sync
		mode = self.value
		
		if not sync:
			ts.uv_select_mode = mode
			#print("selecting all")
			#bpy.ops.mesh.select_all()
		else:
			if mode != "ISLAND":
				ts.mesh_select_mode = [mode == "VERTEX", mode == "EDGE", mode == "FACE"]
			
		return {'FINISHED'}
	
### IMAGE EDITOR

#gets the image from image editor
def get_image(context):
	for area in context.screen.areas:
		if area.type == "IMAGE_EDITOR" and area.spaces.active.image:
			return area.spaces.active.image

#gets a texture that has the editor's image
def get_texture(context):

	img = get_image(context)
	
	if img:
		tex = None
		for t in bpy.data.textures:
			if t.type == "IMAGE" and t.image == img:
				tex = t
				break
		
		if not tex:
			#create texture if necessary
			tex = bpy.data.textures.new(name = img.name, type = "IMAGE")
			tex.image = img
			
		return tex
	
#checks whether the active material has the image editor's texture
def has_texture(context):
	obj = context.object
	if not obj: return False
	
	mat = obj.active_material
	if not mat: return False
	
	engine = context.scene.render.engine
	
	if engine == "BLENDER_RENDER":
		texture = get_texture(context)
		for slot in mat.texture_slots:
			if slot:
				tex = slot.texture
				if tex == texture:
					return True

	elif engine == "CYCLES":
		img = get_image(context)
		if mat.node_tree and img:
			for node in mat.node_tree.nodes:
				if node.type == "TEX_IMAGE" and node.image == img:
					return True
	return False

def apply_texture(context):
	#we have checked that the object hasnt the texture
	#the texture exists
	obj = context.object
	mat = obj.active_material
	created = False
	
	if not mat:
		mat = bpy.data.materials.new(obj.name)
		#if created we can wire the texture to the default diffuse shader
		created = True
		
		if len(obj.material_slots):
			#we are on an empty slot cos active_material is None
			obj.material_slots[obj.active_material_index].material = mat 
		else:
			obj.data.materials.append(mat)
					
	engine = context.scene.render.engine
	
	if engine == "BLENDER_RENDER":
		tex = get_texture(context)
		for i, tex_slot in enumerate(mat.texture_slots):
			if not tex_slot:
				new_slot = mat.texture_slots.add()
				new_slot.texture = tex
				break
	
	#on cycles just add an image to the material 
	#and connect it if the material is created	  
	elif engine == "CYCLES":
		mat.use_nodes = True
		img = get_image(context)
		tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
		tex.image = img

		if created:
			#wire the texture with the diffuse shader
			#look for the diffuse node
			for node in mat.node_tree.nodes:
				if node.type == "BSDF_DIFFUSE":
					tex.location = (node.location.x - 300, node.location.y)
					input = node.inputs['Color']
					output = tex.outputs['Color']
					mat.node_tree.links.new(input, output)
			
class IMAGE_OT_make_texture(bpy.types.Operator):
	"""Creates a texture out of an image"""
	bl_idname = "image.make_texture"
	bl_label = "Make texture out of an image"
	#bl_options = {"REGISTER", "UNDO"}
	
	apply = BoolProperty(name = "Apply to selected", default = False)
	
	@classmethod
	def poll(cls, context):
		return context.area.type == "IMAGE_EDITOR" and context.area.spaces.active.image is not None
	
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "apply")

	def invoke(self, context, event):		
		if has_texture(context):
			self.report({'INFO'}, "Material already has the texture.")				
		else:
			return context.window_manager.invoke_props_dialog(self)
		return {'FINISHED'}
	
	def execute(self, context):
		dd("execute")
		if self.apply:  
			apply_texture(context)		
		return {'FINISHED'}
	
#fixes external image edit
def external_edit(self, context):
	
	from os.path import exists
	image = context.space_data.image
	path = bpy.path.abspath(image.filepath)
	
	if path and exists(path):
		prefs = context.user_preferences
		editor = prefs.filepaths.image_editor
		if editor:
			if exists(editor):
				import subprocess
				cmd = [editor, path]
				subprocess.Popen(cmd)		   
				return {'FINISHED'}
			else:
				self.report({'ERROR'}, '"%s" doesnt exists. Opening with default app.' % editor)			
		
		from ui_tune_up.preferences import op
		op(path)
	return {'FINISHED'}

bpy.types.IMAGE_OT_external_edit.execute = external_edit
bpy.types.IMAGE_MT_image.append(draw_sync_filenames)
bpy.types.TEXT_MT_text.append(draw_sync_filenames)	
dd("operators loaded")
	
def register():
	bpy.utils.register_module(__name__)

			
def unregister():
	bpy.utils.unregister_module(__name__)
			
if __name__ == "__main__":
	register()
