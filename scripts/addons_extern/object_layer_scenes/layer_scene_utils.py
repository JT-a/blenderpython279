import bpy

def Get_Main_Scene():
	# get the main scene name
	main_scene_name = bpy.context.scene.scenelayer_data.main_scenelayer
	# try get the main scene
	main_scene = None
	try:
		main_scene = bpy.data.scenes[main_scene_name]
	except KeyError:
		#main_scene = Create_LayerScene(main_scene_name)
		None
		
	return main_scene

	# get all scenelayers
def Get_LayerScenes():
	
	layerscenes_list = []
	for scene in bpy.data.scenes:
		if( scene.scenelayer_data.is_scenelayer == True ):
			layerscenes_list.append( scene )
	
	return layerscenes_list
	

	# get active scenelayer
def Get_Active_LayerScene():
	main_scene = Get_Main_Scene()
	layerscenes_list = Get_LayerScenes()
	
	active_layer = None
	for scene in layerscenes_list:
		if(scene.scenelayer_data.is_active == True):
			active_layer = scene
	
	# DEPRICATED
	#active_layerscene = main_scene.active_scenelayer	
	#return active_layerscene
	
	return active_layer
	
def Get_LayerScene_ID(scene):
	scene_id = 0
	for i in range(0, len(bpy.data.scenes)):
		if( bpy.data.scenes[i] == scene ):
			scene_id = i
	return scene_id
	
def Set_Active_LayerScene(scene):
	main_scene = Get_Main_Scene()
	main_scene.update()
	main_scene.active_scenelayer = scene

def Get_Unsorted_LayerScene():	
	unsorted_layerscene = bpy.data.scenes['_Unsorted']
	return unsorted_layerscene
	
	# returns a list of unsorted objects
def Get_Unsorted_Objects( scene ):
	object_list = [] # empty array
	
	for obj in scene.objects:
		# 1. check if object is part of a scene ( IGNORE ), else add to list
		is_unsorted = True
		
		for userscene in obj.users_scene:
			if( userscene.scenelayer_data.is_scenelayer == True ):
				is_unsorted = False
				
		if(is_unsorted == True):
			object_list.append( obj )
			
	return object_list
	
def Duplicate_Object( scene_target, name, copyobj ):
	ob_new = None
	if(copyobj.type == 'MESH'):
	   # Create new mesh
		mesh = bpy.data.meshes.new(name)	 
		# Create new object associated with the mesh
		ob_new = bpy.data.objects.new(name, mesh)
		ob_new.data = copyobj.data.copy()
		# Copy data block from the old object into the new object
	
		ob_new.scale = copyobj.scale
		ob_new.location = copyobj.location
 
		# Link new object to the given scene and select it
		scene_target.objects.link(ob_new)

	return ob_new
	
def Duplicate_Scene(scene_target):
	override = {'scene':scene_target, # this should not be the source scene
				'blend_data':bpy.context.blend_data,
				'area':bpy.context.area,
				'window':bpy.context.window,
				'region':bpy.context.region,
				'screen':bpy.context.screen}
	bpy.ops.scene.new(override, type='FULL_COPY')
				
				
def Copy_Scene_To_Scene(scene_source, scene_target):
	print('Copying items from %s to %s' %(scene_source.name, scene_target.name))
	current_scene = bpy.context.scene	
	selected_base = []
	
	copies_in_scene_source = []
	
	for obj in scene_source.objects:
		# create copy and append to copies list
		Duplicate_Object(scene_target, obj.name, obj)
	
	
def Add_Objectlist_To_Scene(source_scene,  target_scene , object_list , unlink_source = False ):
	
	#print("Placing objects in scene %s" %( target_scene) )
	#object_list = [bpy.context.scene.objects['Suzanne']]
	current_scene = bpy.context.scene
	main_scene = Get_Main_Scene()
	selected_base = []
	for i in range(0, len(source_scene.object_bases)):
		base = source_scene.object_bases[i]
		baseObject = base.object
		
		for unsortedobject in object_list:
			if( baseObject == unsortedobject):
				selected_base.append(base)
		
	
	override = {'selected_objects':(object_list) , 
				'selected_editable_objects':(object_list) , 
				'selected_bases':selected_base,
				'scene':source_scene, # this should not be the source scene
				'blend_data':bpy.context.blend_data,
				'area':bpy.context.area,
				'window':bpy.context.window,
				'region':bpy.context.region,
				'screen':bpy.context.screen}
	bpy.ops.object.make_links_scene(override, scene=target_scene.name)
	
	unsorted_scene = Get_Unsorted_LayerScene()
	# if unlink is True, then remove all links to other layer scenes
	if (unlink_source == True):
		for obj in object_list:
			# get all linked scenes, get layer scenes from them, and unlink
			obj_scenes = obj.users_scene
			
			for scene in obj_scenes:
				if( scene.scenelayer_data.is_scenelayer == True  or scene == main_scene ):
					
						if( scene != target_scene):
							if( scene == main_scene and  target_scene.scenelayer_data.is_visible == True and ( target_scene.scenelayer_data.visibility == 1 or target_scene.scenelayer_data.visibility == 2) ):
								None
							else:
								scene.objects.unlink(obj)
						
							
					#source_scene.objects.unlink(obj)
					#unsorted_scene.objects.unlink(obj)
			
	
def Update_Main_Scene():
	main_scene = Get_Main_Scene()
	# 1. put all unsorted items in main scene into unsorted
	unsorted_objects = Get_Unsorted_Objects( main_scene )
	print("Found %s unsorted object(s) while updating..." %( len( unsorted_objects)))
		# move objects to active layerscene
		
	target_scene = Get_Active_LayerScene()
	if(target_scene == None):
		print("No active scene found, using _unsorted")
		target_scene = Get_Unsorted_LayerScene()
		
	Add_Objectlist_To_Scene( main_scene ,target_scene, unsorted_objects)
	
	# 2. clear main scene
	
	Clear_Main_Scene()
	# 3. draw main scene
	Draw_Main_Scene()
	
def Clear_Main_Scene():
	main_scene = Get_Main_Scene()
	for obj in main_scene.objects:
		main_scene.objects.unlink(obj)

def Is_Parent_Visible(scene):
	parent = Get_LayerScene_Parent(scene)
	if( parent == None ):
		return True # if there is no parent
	else:
		if parent.scenelayer_data.visibility == 0:
			return False
		if parent.scenelayer_data.is_visible == False:
			return False;
			
		if Get_LayerScene_Parent(parent) != None:
			return Is_Parent_Visible( parent )
		
		# return visibility of parent
		if(parent.scenelayer_data.visibility == 0):
			return False
		else:
			return True
		# depricated
		return parent.scenelayer_data.is_visible

def Set_Scene_Lock(scene_target , lock):
	for obj in scene_target.objects:
		obj.hide_select = lock
		
def Update_SceneLayerData(scene):
	scene.scenelayer_data.name = scene.name
	Set_Scene_Lock( scene , scene.scenelayer_data.is_locked )
	
def Draw_Main_Scene():
	# for each object in EACH layerscene
	main_scene = Get_Main_Scene()
	layerscene_list = Get_LayerScenes()
	
	
	# check for isolations
	layers = [scene for scene in layerscene_list if (scene.scenelayer_data.visibility == 2)]
	
	# draw isolated list if aplicable
	if( len(layers) == 0 ):
		# there are no isolations, normal draw mode activated
		layers = [scene for scene in layerscene_list if ( scene.scenelayer_data.visibility == 1 and Is_Parent_Visible(scene))]
		print("No Isolated layers found, drawing normally: %s Layers" %(len(layers)))
		
		
		
	#for layer in layerscene_list:		
	for layer in layers:
		# update layername in datapool
		Update_SceneLayerData(layer)
		print("Drawing layerscene: %s" %(layer))
		Add_Objectlist_To_Scene(layer, main_scene, layer.objects )
		
		#if( layer.scenelayer_data.is_visible == True and Is_Parent_Visible(layer) ):
			# link all objects to the main scene!
		#	print("Drawing layerscene: %s" %(layer))
		#	Add_Objectlist_To_Scene(layer, main_scene, layer.objects )
		
	
def Delete_LayerScene( scene ):
	print ("deleting layer %s" %(scene.name))
	# don't delete active layer OR unsorted layer
	main_scene = Get_Main_Scene()
	active_scene = Get_Active_LayerScene()
	
	if(	active_scene == scene ):
		print("WARNING: Cannot delete active scene")
	else:
		bpy.data.scenes.remove(scene)

	return {'FINISHED'};

def Get_LayerScenes():
	layers = []	
	for scene in bpy.data.scenes:
		if(scene.scenelayer_data.is_scenelayer == True):
			layers.append( scene )
	return layers

def Update_Base_Layer():
	
	# check existance
	baseLayerName = "unsorted"
	base_layer = None
	try:		
		# check if layer exists
		base_layer = bpy.data.scenes[baseLayerName]
	except KeyError:
		base_layer = Create_LayerScene( baseLayerName )
		
	#base_layer['is_scenelayer'] = True
	
	# check if it's the only layer * make it active_scene_name
	layers = Get_LayerScenes()
	if(len(layers) == 1 ):
		Set_Active_LayerScene( base_layer )
	
	# update active_layer
	#main_scene = Get_Main_Scene()
	#if( main_scene.active_scenelayer == None ):
	#	main_scene.active_scenelayer = bpy.data.scenes['unsorted']
	
	
def Create_LayerScene( layername, createCopy = False ):
	new_scene = None
	
	# if create a copy, just create the new layer and begone with it
	if( createCopy == True ):
		print("Attempting to create new layer %s" %(layername))
		new_scene = bpy.data.scenes.new( layername )
		new_scene.update()
		new_scene.scenelayer_data.is_scenelayer = True		
		new_scene.scenelayer_data.is_visible = True
		new_scene.scenelayer_data.visibility = 1
		print("New layer copy name is %s" %(new_scene.name))
		return new_scene
		
	# if no copy is allowed to be made, do a check to see if the layer already exists
	try:
		bpy.data.scenes[layername]
	except KeyError:
		print("Creating new layer %s" %(layername))
		bpy.data.scenes.new( layername )
		new_scene = bpy.data.scenes[layername]
		new_scene.update()
		#override = {'scene':new_scene}
		#override['is_scenelayer'] = True
		new_scene.scenelayer_data.is_scenelayer = True		
		new_scene.scenelayer_data.is_visible = True
		new_scene.scenelayer_data.visibility = 1

#		new_scene.is_scenelayer = True;	
	return new_scene

	# returns all objects whom's parent is given scene
def Get_LayerScene_Children(source_scene):
	
	scenes_found = []
	
	for scene in bpy.data.scenes:
		if ( scene.scenelayer_data.is_scenelayer == True ):
			if(scene.scenelayer_data.parent == source_scene.name):
				scenes_found.append(scene)
				
	return scenes_found

def HasChildren(source_scene):
	if (Get_LayerScene_Children() != []):
		return True
	return False

def Get_LayerScene_Parent(scene):
	sceneparent_name = scene.scenelayer_data.parent
	parent = None
	try:
		parent = bpy.data.scenes[sceneparent_name]
	except KeyError:
		parent = None
	return parent

def Get_LayerScene_Parent_Root(scene):
	last_parent_found = Get_LayerScene_Parent(scene)
	previous_parent_found = None
	while last_parent_found != None:
		previous_parent_found = last_parent_found
		last_parent_found = Get_LayerScene_Parent(scene)
	
	if( scene == previous_parent_found ):
		return None
	return previous_parent_found
	
def render_layer_to_file(mode = 'GLSL', dir='', sceneName='error'):
	# save render settings
	scene = bpy.context.scene
	rendersettings_orig = (scene.render.resolution_x,scene.render.resolution_y, scene.camera , scene.render.filepath)	
	print ( rendersettings_orig )
	
	operator_context = None
	
	for window in bpy.context.window_manager.windows:
		screen = window.screen
		
		for area in screen.areas:
			if area.type == 'VIEW_3D':
				operator_context = {'window': window, 'screen': screen, 'area': area}
				#bpy.ops.view3d.viewnumpad(operator_context, type='CAMERA')
				scene.update()
	
	filename = '//' + dir + sceneName + ".png"
	scene.render.filepath = filename	
	if ( mode == 'GLSL'):
		bpy.ops.render.opengl( operator_context, write_still=True )
	else: 
		bpy.ops.render.render(write_still=True)
	print("Rendering to %s" %(filename))
	
	#scene = bpy.context.scene
	#rendersettings_orig = (scene.render.resolution_x,scene.render.resolution_y, scene.camera , scene.render.filepath)
	scene.render.resolution_x = rendersettings_orig[0]
	scene.render.resolution_y =  rendersettings_orig[1]
	scene.camera = rendersettings_orig[2]
	scene.render.filepath =  rendersettings_orig[3]
	
	
def add_layer_to_selection(context,  scene_target ):
	# object = bpy.data.objects['OBJECT']
	# object.select = True
	print("adding layer to selection")
	scene_main = Get_Main_Scene()
	if( scene_main.name != scene_target ):
		if( context.scene == scene_main ):
			# if we're in the viewport
			for obj in scene_target.objects:
				obj_main = scene_main.objects[obj.name]
				obj_main.select = True
	
	# 
def scene_layer_locked_update( self, context ):
	print("Lock updated")
	is_locked = self.is_locked
	Update_Main_Scene()

	# make _viewport active
	main_scene = Get_Main_Scene()		
	bpy.context.screen.scene=bpy.data.scenes[main_scene.name]
		
	return None

def set_layer_visibility( target = 1, filter = -1 ):
	layers = Get_LayerScenes()
	
	for layer in layers:
		if( filter != -1 ):
			if( layer.scenelayer_data.visibility == filter ):
				layer.scenelayer_data.visibility = target
		else:
			layer.scenelayer_data.visibility = target
			
print("Imported layer_scene_utils.py")