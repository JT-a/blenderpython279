bl_info = {
	"name": "vtools Objects Layer Manager",
	"author": "Antonio Mendoza",
	"version": (0, 0, 1),
	"blender": (2, 74, 0),
	"location": "View3D > Properties Panel (N) > Objects Layer Manager",
	"warning": "",
	"description": "simple object layer manager with no count limitations. Only viewport visualization, not related to render process.",
	"category": "Object",
}



import bpy


from bpy.props import (StringProperty,BoolProperty,IntProperty,FloatProperty,FloatVectorProperty,EnumProperty,PointerProperty)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)

# --------- CALLBACKS ------------------#

def callback_changeLayerNameUI(self, value):
	

	for obj in bpy.data.objects:
		if obj.objectLayerManager.name != '' and obj.objectLayerManager.name == self.oldLayerName:
			obj.objectLayerManager.name = self.name
	
	self.oldLayerName = self.name
		   
def callback_setLinkedLayerId(self,value):
	
	for obj in bpy.data.objects:
		if obj.objectLayerManager.name != '' and obj.objectLayerManager.name == self.name:
			obj.objectLayerManager.linkedLayerId= self.linkedLayerId
	
def callback_toogleObjectsVisibility(self,value):
	
 
	layer = self
	
	if layer.visible == False:
		#layer.visible = False
		for obj in bpy.data.objects:
			if obj.objectLayerManager.name == layer.name:
				obj.select = False
				obj.hide = True
	else:
		#layer.visible = True
		for obj in bpy.data.objects:
			if obj.objectLayerManager.name == layer.name:
				obj.select = False
				obj.hide = False
	

def callback_toogleObjectsTemplate(self,value):
	
	layer = self
	
	if layer.template == False:
		for obj in bpy.data.objects:
			if obj.objectLayerManager.name == layer.name:
				obj.select = False
				obj.hide_select = True
	else:
		for obj in bpy.data.objects:
			if obj.objectLayerManager.name == layer.name:
				obj.select = False
				obj.hide_select = False
					
def callback_toogleObjectsRenderable(self,value):
	
	layer = self
	
	if layer.renderable == False:
		for obj in bpy.data.objects:
			if obj.objectLayerManager.name == layer.name:
				obj.select = False
				obj.hide_render = True
	else:
		for obj in bpy.data.objects:
			if obj.objectLayerManager.name == layer.name:
				obj.select = False
				obj.hide_render = False
					

def callback_toogleObjectsSolo(self,value):
	
	
	layer = self
	
	if layer.solo == True:
		for itLayer in bpy.context.scene.objectsLayerManager:
			if itLayer != layer:
				itLayer.visible = False
				itLayer.enabled = False
				
	else:
		for itLayer in bpy.context.scene.objectsLayerManager:	 
			itLayer.visible = True
			itLayer.enabled = True	  
				
	
#--------------------------------------#

#--------- Operators ------------------#

class VTOOLS_OP_addObjectLayer(bpy.types.Operator):
	bl_idname = "vtools.addobjectlayer"
	bl_label = "add new layer"
	bl_description = "add new layer adding selected objects"
	
	def execute(self,context): 
		newLayer = bpy.context.scene.objectsLayerManager.add()
		
		newLayer.name = "layer_" + str(len(bpy.context.scene.objectsLayerManager))
		newLayer.oldLayerName = newLayer.name 
		
		for obj in bpy.context.selected_objects:
			obj.objectLayerManager.name = newLayer.name
			
		return {'FINISHED'}

class VTOOLS_OP_removeObjectLayer(bpy.types.Operator):
	bl_idname = "vtools.removeobjectlayer"
	bl_label = "remove layer"
	bl_description = "remove selected object layer"
	
	def execute(self,context): 
		
		idSelected = bpy.context.scene.objectsLayerManager_ID_index
		
		if idSelected != -1:
			layerName = bpy.context.scene.objectsLayerManager[idSelected].name
			for obj in bpy.data.objects:
				if obj.objectLayerManager.name == layerName:
					obj.objectLayerManager.name = ""
			  
			if idSelected == (len(bpy.context.scene.objectsLayerManager)-1):
				bpy.context.scene.objectsLayerManager_ID_index = bpy.context.scene.objectsLayerManager_ID_index-1
			
			newLayer = bpy.context.scene.objectsLayerManager.remove(idSelected)
		
		return {'FINISHED'}
	

class VTOOLS_OP_addObjectToLayer(bpy.types.Operator):
	bl_idname = "vtools.addobjecttolayer"
	bl_label = "add objects to layer"
	bl_description = "add selected objets into the selected layer"
	
	def execute(self,context): 
		
		idSelected = bpy.context.scene.objectsLayerManager_ID_index
		if idSelected != -1:
			layer = bpy.context.scene.objectsLayerManager[idSelected]
			for obj in bpy.context.selected_objects:
				obj.objectLayerManager.name = layer.name
				obj.hide = not layer.visible
				obj.hide_select = not layer.template
				obj.hide_render = not layer.renderable
				
		  
		return {'FINISHED'}

class VTOOLS_OP_removeObjectFromLayer(bpy.types.Operator):
	bl_idname = "vtools.removeobjectfromlayer"
	bl_label = "remove objects from layer"
	bl_description = "remove every selected objets from the selected layer"
	
	def execute(self,context): 
		
		idSelected = bpy.context.scene.objectsLayerManager_ID_index
		if idSelected != -1:
			layerName = bpy.context.scene.objectsLayerManager[idSelected].name
			for obj in bpy.context.selected_objects:
				if obj.objectLayerManager.name == layerName:
					obj.objectLayerManager.name = ''
		  
		return {'FINISHED'} 

class VTOOLS_OP_selectLayerObjects(bpy.types.Operator):
	bl_idname = "vtools.selectlayerobjects"
	bl_label = "select layer objects"
	bl_description = "select objects linked with this layer"
	
	def execute(self,context): 
		bpy.ops.object.mode_set(mode = 'OBJECT')
		idSelected = bpy.context.scene.objectsLayerManager_ID_index
		if idSelected != -1:
			layerName = bpy.context.scene.objectsLayerManager[idSelected].name
			#bpy.ops.object.select_all(action="DESELECT")
			
			for obj in bpy.data.objects:
				if obj.objectLayerManager.name == layerName:
					obj.select = True
					#bpy.context.scene.objects.active= obj
		  
		return {'FINISHED'}
	  
	  
class VTOOLS_OP_cleanLayers(bpy.types.Operator):
	bl_idname = "vtools.cleanlayers"
	bl_label = "clean layers"
	bl_description = "remove every object from every layer"
	
	def execute(self,context): 
		
		for obj in bpy.data.objects:
			obj.objectLayerManager.name = ""
		  
		return {'FINISHED'}
  

class VTOOLS_OP_moveObjectLayer(bpy.types.Operator):
	
	bl_idname = "vtools.moveobjectlayer"
	bl_label = "move selected layer"
	bl_description = "move selected layer"
	
	direction = IntProperty(default=0)
	
	def execute(self,context): 
		
		idSelected = bpy.context.scene.objectsLayerManager_ID_index
		
		if idSelected != -1:
			numLayers = len(bpy.context.scene.objectsLayerManager)
			layer = bpy.context.scene.objectsLayerManager[idSelected]
			
			
			if numLayers > 1:
				if self.direction == 0:
					if idSelected > 0:
						newId = idSelected - 1
						bpy.context.scene.objectsLayerManager.move(idSelected, newId)
						bpy.context.scene.objectsLayerManager_ID_index = newId
							 
				else:
					if idSelected < (numLayers -1):
						newId = idSelected + 1
						bpy.context.scene.objectsLayerManager.move(idSelected, newId)
						bpy.context.scene.objectsLayerManager_ID_index = newId
		  
		return {'FINISHED'} 
	
class VTOOLS_OP_collectObjectLayers(bpy.types.Operator):
	
	bl_idname = "vtools.colelctobjectlayers"
	bl_label = "collect layers from objects"
	bl_description = "collect layers from objects in scene. ie: when an object is linked or appened"
	
	
	def execute(self,context): 
		
		for obj in bpy.data.objects:
			if obj.objectLayerManager.name != "":
				idLayer = bpy.context.scene.objectsLayerManager.find(obj.objectLayerManager.name)
				if idLayer == -1:
					newLayer = bpy.context.scene.objectsLayerManager.add()
					newLayer.name = obj.objectLayerManager.name
					newLayer.oldLayerName = newLayer.name 
					newLayer.linkedLayerId = obj.objectLayerManager.linkedLayerId
					
		return {'FINISHED'}  
	
#--------------------------------------------------------------#



#----------------VARIABLES ---------------------------------#


class objectlayerManagerProps(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(default="")
	linkedLayerId = bpy.props.IntProperty(default=0, min=0, max = 20)

	
#------------------- UI -----------------------------------#



			
class VTOOLS_UIL_objectsLayerManagerUI(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		drawItem = True
		showVisibleLayers = bpy.context.scene.objectsLayerManager_showVisibleLayers
		if showVisibleLayers:
			if not bpy.context.scene.layers[item.linkedLayerId-1]:
				drawItem = False
		if drawItem:
			row = layout.row(align = True)
			row.enabled = item.enabled
			row.prop(item, "solo", text="",emboss = False, icon='ZOOM_SELECTED')
			row.prop(item, "name", text="", emboss=False, translate=False) 
			if item.visible:
				row.prop(item, "visible", text="",emboss = False, icon='RESTRICT_VIEW_OFF')
			else:
				row.prop(item, "visible", text="",emboss = False, icon='RESTRICT_VIEW_ON')   
			if item.template:
				row.prop(item, "template", text="",emboss = False, icon='RESTRICT_SELECT_OFF')
			else:
				row.prop(item, "template", text="",emboss = False, icon='RESTRICT_SELECT_ON')
			if item.renderable:
				row.prop(item, "renderable", text="",emboss = False, icon='RESTRICT_RENDER_OFF')
			else:
				row.prop(item, "renderable", text="",emboss = False, icon='RESTRICT_RENDER_ON') 
			srow = row.row()
			srow.scale_x =0.25
			srow.prop(item,"linkedLayerId", emboss = False)


	def filter_items(self, context, data, propname):
		# Default return values.
		#flt_neworder = list([0, 1])
		flt_flags = []
		flt_neworder = []   
		layers = getattr(data, propname)
		drawItem = False
		nonVisibleCount = 0
		visibleCount = 0
		layersCount = len(layers.items())
		showVisibleLayers = bpy.context.scene.objectsLayerManager_showVisibleLayers
		
		if showVisibleLayers:
			for layer in layers:
				if not bpy.context.scene.layers[layer.linkedLayerId-1]:
					drawItem = False
					flt_neworder.append(layersCount-1-nonVisibleCount)
					nonVisibleCount += 1

				else:
					drawItem = True
					flt_neworder.append(visibleCount)
					visibleCount +=1		
		
		return flt_flags, flt_neworder
	
class VTOOLS_CC_objectsLayerManager(bpy.types.PropertyGroup):
	   
	name = StringProperty(default="", update=callback_changeLayerNameUI)
	linkedLayerId = IntProperty(name="", default=0, min=0, max = 20, subtype="UNSIGNED", update=callback_setLinkedLayerId)
	layerID = IntProperty()
	oldLayerName = StringProperty()
	visible = BoolProperty(default = True, update=callback_toogleObjectsVisibility)
	template = BoolProperty(default = True, update=callback_toogleObjectsTemplate)
	renderable = BoolProperty(default = True, update=callback_toogleObjectsRenderable)
	enabled = BoolProperty(default = True)
	solo = BoolProperty(default = False, update=callback_toogleObjectsSolo)
	
class VTOOLS_PN_objectsLayerManager(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Layers'
	bl_label = "Objects Layer Manager"
	bl_options = {'DEFAULT_CLOSED'}
	bl_context = 'objectmode'
	def draw(self,context):
		layout = self.layout
		row = layout.row()
		col = row.column()   
		col.template_list('VTOOLS_UIL_objectsLayerManagerUI', "layerID", context.scene, "objectsLayerManager", context.scene, "objectsLayerManager_ID_index", rows=5, type='DEFAULT')	 
		col = row.column(align = True)
		col.operator(VTOOLS_OP_addObjectLayer.bl_idname, icon="ZOOMIN", text="")
		col.operator(VTOOLS_OP_removeObjectLayer.bl_idname, icon="ZOOMOUT", text="")
		col.operator(VTOOLS_OP_collectObjectLayers.bl_idname, icon="RECOVER_LAST", text="")

		showVisibleLayers = bpy.context.scene.objectsLayerManager_showVisibleLayers
		
		if not showVisibleLayers:
		  col.separator()
		  col.operator(VTOOLS_OP_moveObjectLayer.bl_idname, icon="TRIA_UP", text="").direction = 0
		  col.operator(VTOOLS_OP_moveObjectLayer.bl_idname, icon="TRIA_DOWN", text="").direction = 1
		
		row = layout.row(align=True)
		row.prop(context.scene, "objectsLayerManager_showVisibleLayers",text="",toggle=True, icon="LINKED")
		row.operator(VTOOLS_OP_selectLayerObjects.bl_idname, icon="HAND", text="Select", emboss = True)
		row.operator(VTOOLS_OP_addObjectToLayer.bl_idname, icon="ZOOMIN", text="Link")
		row.operator(VTOOLS_OP_removeObjectFromLayer.bl_idname, icon="ZOOMOUT", text="Unlink")
		row.operator(VTOOLS_OP_cleanLayers.bl_idname, icon="X", text="Unlink All")


def register():
	
	bpy.utils.register_module(__name__)   
	bpy.types.Scene.objectsLayerManager = bpy.props.CollectionProperty(type=VTOOLS_CC_objectsLayerManager) 
	bpy.types.Scene.objectsLayerManager_ID_index = bpy.props.IntProperty()
	bpy.types.Object.objectLayerManager = bpy.props.PointerProperty(type=objectlayerManagerProps)
	bpy.types.Scene.objectsLayerManager_showVisibleLayers = bpy.props.BoolProperty(default=False, description="show only objects layers linked to visible layers")
	
def unregister():
	
	bpy.utils.unregister_module(__name__)
	
	del bpy.types.Scene.objectsLayerManager
	del bpy.types.Scene.objectsLayerManager_ID_index 
	del bpy.types.Object.objectLayerManager
	del bpy.types.Scene.objectsLayerManager_showVisibleLayers 

if __name__ == "__main__":
	register()  
			
			
