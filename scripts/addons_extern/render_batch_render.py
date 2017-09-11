bl_info = {
	"name": "Batch Render",
	"author": "Hubert (szczuro) Niecko",
	"version": (0, 1, 1),
	"blender": (2, 65, 0),
	"location": "Render settings > Batch Render",
	"description": "Render chosen frames",
	"warning": "This is early dev stage of script",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Render"}

import bpy

"""
	TODO 
	  Store and restore filepath and current frame
	  Assign output panel props
"""		
### methods ###########################################
def removeWhiteSpaces(inputString):
	""" remove white spaces """
	return "".join(inputString.split())
	
def checkString(inputString):
	"""check if string is parsable, return true or string with error"""
	for i in inputString:
		if "1234567890, ".find(i) == -1: 
			return "Error: only digits, space or ',' are allowed"
	return True
  
def parseFrameList(inputString):
	""" parse string to list of frames"""
	inputString = removeWhiteSpaces(inputString)
	frList = []
	for i in inputString.split(","):
		if i != "":
			frList.append(int(i))
	return frList

def update_props(self, context):
	""" frames String prop on update """
#	debug("update start")
	br = context.window_manager.batch_render
	check = checkString(br.frame_string)
	if check == True:
		frameList = parseFrameList(br.frame_string)
		print(frameList)
		if br.sort_list==True: #sort list
			print ("sorting frames")
			frameList.sort()
		br.frame_list =	str(frameList)[1:-1].replace(" ","")
	else:
		br.frame_list = check

### class ########################################################
class BatchRender(bpy.types.Operator):
	""" Render list of images to '//render/file#####.*'  """
	bl_idname = "render.batch"
	bl_label = "Batch Render"
	bl_options = {'REGISTER'}

	def execute (self,context):
		br = context.window_manager.batch_render
		check = checkString(br.frame_string)
		if check != True:
			return {'CANCELLED'}
		frameList = parseFrameList(br.frame_list)
		print ("Rendering frames:"+str(frameList))

		for i in frameList:
			print ("Render frame: "+str(i))
			bpy.context.scene.frame_current = i
			bpy.context.scene.render.filepath = "//render/file%.5i" % i
			bpy.ops.render.render(write_still = True)
		return {'FINISHED'}

class BatchRenderPanel (bpy.types.Panel):
	bl_label = "Batch Render"
	bl_idname = ".RENDER_PT_batch_render"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"
	
	def draw (self, context):
		br = context.window_manager.batch_render
		layout = self.layout
		col = layout.column(align=True)
		
		col.prop(br,"frame_string")
		col.prop(br,"sort_list")
		col.label(br.frame_list)
		col.operator("render.batch")
		
class BatchRenderProps(bpy.types.PropertyGroup):
	"""
	Fake module like class
	bpy.context.scene.render.batch
	"""
	frame_string = bpy.props.StringProperty(name = "Frames",
		default = "1",
		update = update_props,
		description = "List of frames to render divided by comas. White spaces will be removed.")
	frame_list = bpy.props.StringProperty(name = "Frames List",
		default = "1",
		description = "list of frames to render")
	sort_list = bpy.props.BoolProperty(name = "Sort list",
		default = True,
		update = update_props,
		description = "Enables sorting of frame list")

### registering ########################################################
classes = [BatchRenderProps,BatchRenderPanel,BatchRender]

def register():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.WindowManager.batch_render =\
		bpy.props.PointerProperty(type = BatchRenderProps)

def unregister():
	for c in classes:
		bpy.utils.unregister_class(c)
	try:
		del bpy.types.WindowManager.batch_render
	except:
		pass

### testing purpose #########################################################
if __name__ == "__main__":
	register()
