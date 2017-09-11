import bpy
from bpy.props import *
from . import layer_scene_utils
# init

global glob_active_sceneLayer
global glob_main_sceneLayer

global glob_CurrentVersion
glob_CurrentVersion = 'v0.505'

glob_active_sceneLayer = None

glob_main_sceneLayer = None

global glob_main_scene_name
glob_main_scene_name = '_Viewport'


	# get set properties of active_sceneLayer
def active_scenelayer_get(self):
	global glob_active_sceneLayer	
	return glob_active_sceneLayer

	
def active_scenelayer_set(self, value):
	print("setting active_scenelayer to %s" %(value))
	global glob_active_sceneLayer
	glob_active_sceneLayer  = value
	
	# get set properties of active_sceneLayer
def main_scenelayer_get(self):
	global glob_main_sceneLayer	
	if( glob_main_sceneLayer == None):
		return '_Viewport'
	return glob_main_sceneLayer

	
def main_scenelayer_set(self, value):
	print("setting glob_main_sceneLayer to %s" %(value))
	global glob_main_sceneLayer
	glob_main_sceneLayer  = value
	
	
def layersceneparent_get(self):
	return self['layersceneparent_val']
	
def layersceneparent_set(self, value):
	print("self/value")
	
	self['layersceneparent_val'] = value
	
def obj_scenelayer_get(self):
	# see if object is in a scenelayer
	scenelayer = None
	found_scenes = self.users_scene
	
	for scn in found_scenes:
		if( scn.scenelayer_data.is_scenelayer == True ):
			scenelayer = scn
	return scenelayer

def obj_scenelayer_set(self, value):
	
	None
	
def obj_scenelayer_get(self):
	
	None

	# passes arguments through to utils
def scenelayer_locked_update(self, context):
	return layer_scene_utils.scene_layer_locked_update( self, context)
	
class SceneLayer_Data(bpy.types.PropertyGroup):

	is_visible = bpy.props.BoolProperty( default= True, name='Show/Hide', update=scenelayer_locked_update )	
	is_scenelayer = bpy.props.BoolProperty( default= False, name='Show/Hide' )
	is_optionsexanded = bpy.props.BoolProperty( default= False, name='Show/Hide' )
	
	is_locked = bpy.props.BoolProperty(default=False , name='Lock/Unlock', update=scenelayer_locked_update)	
	is_active = bpy.props.BoolProperty( default= False, name='Is this the active layer?')	
	
	name = bpy.props.StringProperty(default='defaultlayername', name="Layer name")
	main_scenelayer = property( main_scenelayer_get, main_scenelayer_set)
	parent = bpy.props.StringProperty(default='', name="Parent Layer")
	
	# Upgraded variables
	version = bpy.props.StringProperty(default = glob_CurrentVersion, name = "Version of Scenelayers this layer was created in")
	
	
	id = bpy.props.IntProperty(default = -1 , name="Scene Identifier")	
	"""
	The ID property is checked in the following cases: 
	1. When a scene layer is assigned, a new ID is given to the scenelayer
	2. When a scene layer is coppied from another layer
	3. When the scene is updated ( using the update method )	
	"""
	
	type = bpy.props.IntProperty(default = 0 , name="SceneLayer type 0/1/2 ( none, normal, special,...)")
	"""
	Generally not used yet
	"""
	
	
	visibility = bpy.props.IntProperty(default = 1 ,name="Visibility 0/1/2 ( No, Yes, Isolated)") 
	"""
	Marks if a layer is visible or not
	0 = NOT VISIBLE
	1 = VISIBLE
	2 = overrides visibility, when in layer is isolated, makes this layer visible
	"""
	
	locked = bpy.props.IntProperty(default = 0 ,name="Locked 0/1/2 ( No, Yes, Isolated)") 
	"""
	Marks if a layer is locked or not
	0 = NOT LOCKED
	1 = LOCKED
	2 = overrides lock, 2 means that this layer is editable, and others are not
	"""
	options = bpy.props.IntProperty(default = 0 ,name="Show additional data 0/1/2 ( No, Yes, special/yes)") 
	"""
	Flags for the display of aditional options
	0 = do not show options
	1 = 
	2 = overrides lock, 2 means that this layer is editable, and others are not
	"""
	
# Register important components
def register():
	global glob_main_scene_name
	
	bpy.types.Scene.new_scenelayer_name = bpy.props.StringProperty(default='', name="Layer name")
	
	# dynamic properties
	bpy.types.Scene.active_scenelayer = property( active_scenelayer_get, active_scenelayer_set)
	bpy.types.Object.scenelayer = property(obj_scenelayer_get, obj_scenelayer_set)	
		# scene layer group
	bpy.types.Scene.scenelayer_data = PointerProperty(type=SceneLayer_Data)
   
   
   
if __name__ == "__main__":
	register()

#init_module()

print("Imported Layer_scene_main.py")