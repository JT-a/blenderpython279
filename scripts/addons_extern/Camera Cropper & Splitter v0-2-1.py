######################################################################################################


############# Add-on description (used by Blender)

bl_info = {
    "name": "Camera cropper & splitter",
    "description": 'Allows to crop the camera view using the render borders or split the frame',
    "author": "Caetano Veyssières",
    "version": (0, 2, 1),
    "blender": (2, 77, 0),
    "location": "Properties > Render > Camera cropper & splitter",
    "warning": "", # used for warning icon and text in addons panel
    "tracker_url": "Not yet",
    "category": "Render"}

##############

import bpy
from bpy.props import *
import math

# ▼ NUMBER OF TILES LIST ▼
tilesNumber = [
	('0', '4', 'Split in 4 tiles'), 
	('1', '16', 'Split in 16 tiles'), 
	('2', '64', 'Split in 64 tiles'),
	('3', '256', 'Split in 256 tiles')]
	
tilingOrder = [
	('0', 'Left to Right', 'Left to Right'), 
	('1', 'Right to left', 'Right to left'), 
	('2', 'Top to Bottom', 'Top to Bottom'),
	('3', 'Bottom to Top', 'Bottom to Top')]

def setTiles():
	bpy.types.Object.my_tiles = EnumProperty(
		items = tilesNumber,
		name = "Number of tiles")
 
setTiles()

def setTilingOrder():
	bpy.types.Object.tiling_order = EnumProperty(
		items = tilingOrder,
		name = "Tiling Order")
 
setTilingOrder()


def findTiles(key):
	for n,tile in enumerate(tilesNumber):
		(key1, name, description) = tile		
		if key == key1:
			return n
	raise NameError("Unrecognized key %s" % key)
	
def findTilingOrder(key):
	for o,order in enumerate(tilingOrder):
		(key1, name, description) = order		
		if key == key1:
			return o
	raise NameError("Unrecognized key %s" % key)
 
# ▼ PANEL LAYOUT ▼
class CropSplitPanel(bpy.types.Panel):
	bl_label = "Camera Crop & Split"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "render"
	
	def draw_header(self, context):
		layout = self.layout
		layout.label(text="", icon="RENDER_REGION")
		
	def draw(self , context):
		layout = self.layout
		row = layout.row()
		split = row.split(percentage=0.5)
		col_left = split.column()
		col_right = split.column(align=True)
		cam = context.scene.camera
		col_left.separator()
		col_left.scale_y = 3
		col_left.operator("cropper.set", text="Crop using borders")
		col_right.label(text="Split Camera over time :")
		col_right.prop_menu_enum(cam, "my_tiles")
		col_right.prop_menu_enum(cam, "tiling_order")
		col_right.operator("splitter.set")
 
# ▼ Split operator ▼
class OBJECT_OT_SplitCamera(bpy.types.Operator):
	bl_idname = "splitter.set"
	bl_label = "Split"
	bl_description = "Splits the camera in tiles over time"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		# ▼ Variables for math formulas ▼
		C = bpy.context
		X = C.scene.render.resolution_x
		Y = C.scene.render.resolution_y
		f = C.scene.camera.data.lens
		
		'''
		▼ Variables to change interpolation mode temporarily (not working yet) ▼
		keyInterp = context.user_preferences.edit.keyframe_new_interpolation_type
		'''
		
		# ▼ Variables for using the selected Number of tiles ▼
		cam = context.scene.camera
		n = findTiles(cam.my_tiles)
		(key, name, description) = tilesNumber[n]
		tiles = float(name)
		
		# ▼ Variables for using the selected Tiling Order ▼
		o = findTilingOrder(cam.tiling_order)
		(key, name, description) = tilingOrder[o]
		order = float(key)
		
		# ▼ Focal length change ▼
		C.scene.camera.data.lens = f * math.sqrt(tiles)
		# ▼ Resolution change ▼ 
		C.scene.render.resolution_x = round(X/math.sqrt(tiles))
		C.scene.render.resolution_y = round(Y/math.sqrt(tiles))
		# ▼ Animated Shift X & Y ▼ 
		context.user_preferences.edit.keyframe_new_interpolation_type ='CONSTANT'
		if (X>Y):
			if (order == 0):
				C.scene.camera.data.shift_x = -(math.sqrt(tiles)/2)+0.5-1
				for _ in range (int(math.sqrt(tiles))):
					C.scene.camera.data.shift_x += 1
					bpy.context.scene.camera.data.keyframe_insert(data_path="shift_x", frame = bpy.context.scene.frame_current)
					C.scene.camera.data.shift_y = ((math.sqrt(tiles)/2)-0.5)*(Y/X)+(Y/X)
					
					for _ in range (int(math.sqrt(tiles))):
						C.scene.camera.data.shift_y -= Y/X
						bpy.context.scene.camera.data.keyframe_insert(data_path="shift_y", frame = bpy.context.scene.frame_current)
						bpy.context.scene.frame_current += 1
			elif (order == 1):
				C.scene.camera.data.shift_x = (math.sqrt(tiles)/2)-0.5+1
				for _ in range (int(math.sqrt(tiles))):
					C.scene.camera.data.shift_x -= 1
					bpy.context.scene.camera.data.keyframe_insert(data_path="shift_x", frame = bpy.context.scene.frame_current)
					C.scene.camera.data.shift_y = ((math.sqrt(tiles)/2)-0.5)*(Y/X)+(Y/X)
					
					for _ in range (int(math.sqrt(tiles))):
						C.scene.camera.data.shift_y -= Y/X
						bpy.context.scene.camera.data.keyframe_insert(data_path="shift_y", frame = bpy.context.scene.frame_current)
						bpy.context.scene.frame_current += 1
			elif (order == 2):
				C.scene.camera.data.shift_y = ((math.sqrt(tiles)/2)-0.5)*(Y/X)+(Y/X)
				for _ in range (int(math.sqrt(tiles))):
					C.scene.camera.data.shift_y -= Y/X
					bpy.context.scene.camera.data.keyframe_insert(data_path="shift_y", frame = bpy.context.scene.frame_current)
					C.scene.camera.data.shift_x = -(math.sqrt(tiles)/2)+0.5-1
									
					for _ in range (int(math.sqrt(tiles))):
						C.scene.camera.data.shift_x += 1
						bpy.context.scene.camera.data.keyframe_insert(data_path="shift_x", frame = bpy.context.scene.frame_current)
						bpy.context.scene.frame_current += 1
			else :
				C.scene.camera.data.shift_y = -((math.sqrt(tiles)/2)-0.5)*(Y/X)-(Y/X)
				for _ in range (int(math.sqrt(tiles))):
					C.scene.camera.data.shift_y += Y/X
					bpy.context.scene.camera.data.keyframe_insert(data_path="shift_y", frame = bpy.context.scene.frame_current)
					C.scene.camera.data.shift_x = -(math.sqrt(tiles)/2)+0.5-1
									
					for _ in range (int(math.sqrt(tiles))):
						C.scene.camera.data.shift_x += 1
						bpy.context.scene.camera.data.keyframe_insert(data_path="shift_x", frame = bpy.context.scene.frame_current)
						bpy.context.scene.frame_current += 1
				
		else :
			if (order == 0):
				C.scene.camera.data.shift_x = -((math.sqrt(tiles)/2)-0.5)*(X/Y)-(X/Y)
				for _ in range (int(math.sqrt(tiles))):
					C.scene.camera.data.shift_x += X/Y
					bpy.context.scene.camera.data.keyframe_insert(data_path="shift_x", frame = bpy.context.scene.frame_current)
					C.scene.camera.data.shift_y = -(math.sqrt(tiles)/2)+0.5-1
									
					for _ in range (int(math.sqrt(tiles))):
						C.scene.camera.data.shift_y += 1
						bpy.context.scene.camera.data.keyframe_insert(data_path="shift_y", frame = bpy.context.scene.frame_current)
						bpy.context.scene.frame_current += 1
			if (order == 1):
				C.scene.camera.data.shift_x = ((math.sqrt(tiles)/2)-0.5)*(X/Y)+(X/Y)
				for _ in range (int(math.sqrt(tiles))):
					C.scene.camera.data.shift_x -= X/Y
					bpy.context.scene.camera.data.keyframe_insert(data_path="shift_x", frame = bpy.context.scene.frame_current)
					C.scene.camera.data.shift_y = -(math.sqrt(tiles)/2)+0.5-1
									
					for _ in range (int(math.sqrt(tiles))):
						C.scene.camera.data.shift_y += 1
						bpy.context.scene.camera.data.keyframe_insert(data_path="shift_y", frame = bpy.context.scene.frame_current)
						bpy.context.scene.frame_current += 1
			if (order == 2):
				C.scene.camera.data.shift_y = (math.sqrt(tiles)/2)-0.5+1
				for _ in range (int(math.sqrt(tiles))):
					C.scene.camera.data.shift_y -= 1
					bpy.context.scene.camera.data.keyframe_insert(data_path="shift_y", frame = bpy.context.scene.frame_current)
					C.scene.camera.data.shift_x = ((math.sqrt(tiles)/2)-0.5)*(X/Y)+(X/Y)
									
					for _ in range (int(math.sqrt(tiles))):
						C.scene.camera.data.shift_x -= X/Y
						bpy.context.scene.camera.data.keyframe_insert(data_path="shift_x", frame = bpy.context.scene.frame_current)
						bpy.context.scene.frame_current += 1
				
			if (order == 3):
				C.scene.camera.data.shift_y = -(math.sqrt(tiles)/2)+0.5-1
				for _ in range (int(math.sqrt(tiles))):
					C.scene.camera.data.shift_y += 1
					bpy.context.scene.camera.data.keyframe_insert(data_path="shift_y", frame = bpy.context.scene.frame_current)
					C.scene.camera.data.shift_x = ((math.sqrt(tiles)/2)-0.5)*(X/Y)+(X/Y)
									
					for _ in range (int(math.sqrt(tiles))):
						C.scene.camera.data.shift_x -= X/Y
						bpy.context.scene.camera.data.keyframe_insert(data_path="shift_x", frame = bpy.context.scene.frame_current)
						bpy.context.scene.frame_current += 1
		'''
		▼ Put interpolation mode back to previous mode (not working yet) ▼
		
		context.user_preferences.edit.keyframe_new_interpolation_type = keyInterp
		'''
		return{'FINISHED'}
		
# ▼ Crop operator ▼
class OBJECT_OT_CropCamera(bpy.types.Operator):
	bl_idname = "cropper.set"
	bl_label = "Crop camera"
	bl_description = "Crops the camera using render borders"
	bl_options = {'REGISTER', 'UNDO'}
 
	def execute(self, context):
		C = bpy.context
		X = C.scene.render.resolution_x
		Y = C.scene.render.resolution_y
		f = C.scene.camera.data.lens
		bXmin = C.scene.render.border_min_x
		bXMAX = C.scene.render.border_max_x
		bYmin = C.scene.render.border_min_y
		bYMAX = C.scene.render.border_max_y
		
		# ▼ Focal length change ▼ 
		if (X>Y):
			if ((X*(bXMAX-bXmin))>((Y*(bYMAX-bYmin)))):
				C.scene.camera.data.lens = f * (1/(bXMAX-bXmin))
			else:
				C.scene.camera.data.lens = f * (X/(Y * (bYMAX - bYmin)))
		else:
			if ((X*(bXMAX-bXmin))>((Y*(bYMAX-bYmin)))):
				C.scene.camera.data.lens = f * (Y/(X * (bXMAX - bXmin)))
			else :
				C.scene.camera.data.lens = f * (1/(bYMAX-bYmin))
		
		# ▼ Resolution change ▼ 
		C.scene.render.resolution_x = round(X * (bXMAX - bXmin))
		C.scene.render.resolution_y = round(Y * (bYMAX - bYmin))
		
		# ▼ Shift X ▼ 
		if ((X * (bXMAX - bXmin))>(Y * (bYMAX - bYmin))):
			C.scene.camera.data.shift_x = (0.5 * (bXMAX + bXmin - 1)) / (bXMAX - bXmin)
		else :
			C.scene.camera.data.shift_x = (0.5 * (X * (bXMAX - bXmin)) * (bXMAX + bXmin - 1))/((Y * (bYMAX - bYmin)) * (bXMAX - bXmin))
		
		# ▼ Shift Y ▼ 
		if ((X * (bXMAX - bXmin))>(Y * (bYMAX - bYmin))):
			C.scene.camera.data.shift_y = (0.5 * (Y * (bYMAX - bYmin)) * (bYMAX + bYmin - 1))/((X * (bXMAX - bXmin)) * (bYMAX - bYmin))
			
		else :
			C.scene.camera.data.shift_y = (0.5 * (bYMAX + bYmin - 1)) / (bYMAX - bYmin)
		
		# ▼ Info report ▼ 
		self.report({'INFO'}, "Converted render borders to camera view")
		return {'FINISHED'}


# ▼ Registration ▼ 

def register():
	bpy.utils.register_module(__name__)
 
def unregister():
	bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
	register()
