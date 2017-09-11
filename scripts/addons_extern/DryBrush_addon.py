bl_info = {
	"name": "Dry Brush",
	"author": "Michael Marlett",
	"version": "1.0",
	"description": "Allows you to use a Dry Brush function for Texture Painting.",
	"category": "Paint",
}

import bpy

"""Class that creates a UI panel and calls the dry Brush Operator"""
class DryBrush_Panel(bpy.types.Panel):
	"""A Custom Panel in the Viewport Toolbar"""
	bl_label = "Dry Brush"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "imagepaint"

	bl_category = "Slots"
	
		
	def draw(self, context):
		bpy.props.img_list = []
		for i in range(len(bpy.data.images)):
			bpy.props.img_list.append((str(i+1),bpy.data.images[i].name,'0'))
		layout = self.layout

		row = layout.row()
		row.label(text="Dry Brush:")
		row = layout.row()
		row.operator("image.adjust_operator", text = "Adjust Dry Brush")
		row = layout.row()
		if bpy.props.selectedImage:
			label = str(bpy.props.selectedImage[1])
		else:
			label = 'Image list'
		row.operator_menu_enum("img_list.menu", 'imgList', text=label)

"""Class that creates the img list property and handles the selection from the list"""	
class Image_list_OT_Menu(bpy.types.Operator):
	bl_idname = "img_list.menu"
	bl_description = "Select the Image to use as a height map"
	bl_label = "Menu"
   
	"""funtion that return the list of current images"""	 
	def get_images(self, context):
		return bpy.props.img_list
	
	imgList = bpy.props.EnumProperty(items = get_images, name = "images", description = "The image list")
	"""gets the user's choice of image"""
	def execute(self,context):
		bpy.props.selectedImage = [n for i, n in enumerate(bpy.props.img_list) \
		if n[0] == self.imgList][0]
		return{"FINISHED"}
	


"""Operator that adjusts the image using compositing nodes"""
class ImageAdjust(bpy.types.Operator):
	"""Adjusts the image to change the depth, falloff, and threshold."""
	bl_idname = "image.adjust_operator"
	bl_label = "Dry Brush Operation"
	bl_options = {'REGISTER', 'UNDO'}
	
	
	depth = bpy.props.IntProperty(name = 'Depth', default = -20, min = -200, max = 0)
	falloff = bpy.props.IntProperty(name = 'Falloff', default = 2, min = 0, max = 100)
	threshold = bpy.props.IntProperty(name = 'Threshold', default = 4)

	
	def execute(self,context):
		"""updates the the img_list"""

		bpy.props.img_list = []
		for i in range(len(bpy.data.images)):
			bpy.props.img_list.append((str(i+1),bpy.data.images[i].name,'0'))

		self.createNodes()
		self.saveImage()
		return {'FINISHED'}

	def createNodes(self):
		bpy.context.scene.use_nodes = True
		tree = bpy.context.scene.node_tree
		"""removes and the default nodes."""
		for n in tree.nodes:
			tree.nodes.remove(n)

		"""Creates image node"""
		image_node = tree.nodes.new(type='CompositorNodeImage')
		image_node.image = bpy.data.images[bpy.props.selectedImage[1]]
		image_node.location = 0,0
		"""Creates Brightness/Contrast Node"""
		bc_node = tree.nodes.new(type='CompositorNodeBrightContrast')
		bc_node.location = 400,0
		bc_node.inputs[1].default_value = self.depth
		bc_node.inputs[2].default_value = self.threshold
		"""Creates Multiply Node"""
		mult_node = tree.nodes.new(type = 'CompositorNodeMath')
		mult_node.location = 800,0
		mult_node.operation = 'MULTIPLY'
		mult_node.inputs[1].default_value = self.falloff
		"""Creates the Composite node"""
		comp_node = tree.nodes.new('CompositorNodeComposite')   
		comp_node.location = 1200,0
		"""Links all the Nodes together"""
		links = tree.links
		link1 = links.new(image_node.outputs[0],bc_node.inputs[0])
		link3 = links.new(bc_node.outputs[0],mult_node.inputs[0])
		link2 = links.new(mult_node.outputs[0],comp_node.inputs[0])

	def saveImage(self):
		"""Saves the current render resolutions"""
		xres = bpy.context.scene.render.resolution_x
		yres = bpy.context.scene.render.resolution_y
		"""resets the render resolution to match image resolution"""
		xres2 = bpy.data.images[bpy.props.selectedImage[1]].size[0]
		yres2 = bpy.data.images[bpy.props.selectedImage[1]].size[1]
		bpy.context.scene.render.resolution_x = xres2
		bpy.context.scene.render.resolution_y = yres2
		"""Saves the image under the name Cache_image.png"""
		bpy.context.scene.render.filepath = '//Cache_image.png'
		bpy.ops.render.render(write_still = True)
		"""Either reloads or opens the image"""
		try:
			bpy.data.images['Cache_image.png'].reload()
		except:
			bpy.ops.image.open(filepath="//Cache_image.png", files=[{"name":"Cache_image.png", "name":"Cache_image.png"}], relative_path=True)
		"""sets the render resolution back to normal"""
		bpy.context.scene.render.resolution_x = xres
		bpy.context.scene.render.resolution_y = yres

"""Puts the ImageAdjust operator in the menu system"""
def menu_func(self,context):
	self.layout.operator(ImageAdjust.bl_idname)
	

	
def register():
	bpy.props.selectedImage = False
	bpy.props.img_list = []
	bpy.utils.register_module(__name__)

	bpy.types.VIEW3D_MT_brush.append(menu_func)
	
	
	
	
def unregister():
	del bpy.props.selectedImage
	del bpy.props.img_list
	bpy.utils.unregister_module(__name__)

	bpy.types.VIEW3D_MT_brush.remove(menu_func)


if __name__ == "__main__":
	register()
