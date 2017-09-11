import bpy
from . import layer_scene_utils

class LAYERSCENES_MakeActiveButton(bpy.types.Operator):
	bl_idname = "layerscenes_makeactive.button"
	bl_label = "V"
	bl_description = "Make this layer active"
	
	target = bpy.props.StringProperty(default='', name="layer to make active")
	
	def execute(self, context):
		print( "Making scene: %s the currently active layer" %(self.target) )		
		layer_scene_utils.Set_Active_LayerScene( bpy.data.scenes[self.target])
		print( "Active layer is now: %s" %(layer_scene_utils.Get_Active_LayerScene())  )		
		return {'FINISHED'}

""" Draws a single line/layer with every button and schnizz on it"""
class LayerScenesUI_LayerControl:
	def __init__(self , layout, context , scene):
		# Only show actualy designated scene layers
		if( scene.scenelayer_data.is_scenelayer == True):
			children = layer_scene_utils.Get_LayerScene_Children(scene)
			
			# choose correct operator button icon
			button_icon_expand = 'RIGHTARROW'
			if( scene.scenelayer_data.is_optionsexanded == True):
				#layout = layout.box()
				button_icon_expand = 'DOWNARROW_HLT'
			
			row = layout.row(align=True)
			row.alignment = 'EXPAND'	
			
			col = row.column(align=True)
			col.alignment = 'LEFT'
			
			sub_row = col.row()
			# ACTIVE LAYER
			button_icon_active = 'PROP_OFF'
			
			if(scene.scenelayer_data.is_active == True ): 
				button_icon_active = 'PROP_CON'
				
			sub_row.operator("layerscenes_set_active.button", icon = button_icon_active ,emboss = False , text='').target = scene.name
						
			# Expand
			sub_row.operator("layerscenes_toggle_expand.button" , icon=button_icon_expand , text="" , emboss = False).target = scene.name
			
			# open a box in the other colioum
			
				
			col = row.column()
			if( scene.scenelayer_data.is_optionsexanded == True):
				col = col.box()
				
			sub_row = col.row()
			
			# choose correct operator button icon
			button_icon = 'RESTRICT_VIEW_ON'
			
			if( scene.scenelayer_data.visibility == 1 ):
				button_icon = 'RESTRICT_VIEW_OFF'
			if ( scene.scenelayer_data.visibility == 2 ):
				button_icon = 'WORLD_DATA'
			sub_row.operator('layerscenes_toggle_visible.button', icon=button_icon , text='').target = scene.name
			active_layer = layer_scene_utils.Get_Active_LayerScene()
			

			sub_row.prop(scene, 'name', '')
			unsorted_scene = layer_scene_utils.Get_Unsorted_LayerScene()
			
			## All buttons are in different collumns, allowing me to enable and disable them ( like the next button for example )			
			
			# LOCK LAYER
			button_icon_lock = 'UNLOCKED'			
			if( scene.scenelayer_data.is_locked == True):
				button_icon_lock = 'LOCKED'			
			
			sub_row.prop(scene.scenelayer_data, 'is_locked', text='' , icon=button_icon_lock )
						
			delete_allowed = True
			if ( scene == unsorted_scene ):
				delete_allowed = False
			
			
			
			
		# Call normal operators
		# Button: Select this layer
			sub_col = sub_row.column(align=True)
			sub_col.alignment = 'EXPAND'
			sub_col.operator("layerscenes_selectlayerobjects.button", icon = 'RESTRICT_SELECT_OFF', text='').target = scene.name

			# Button: Moves all selected objects to this layer ( 
			sub_col = sub_row.column(align=True)
			sub_col.alignment = 'EXPAND'
			sub_col.operator("layerscenes_add.button" , icon='ZOOMIN' , text='' ).target = scene.name
			
			sub_col = sub_row.column(align=True)
			sub_col.alignment = 'EXPAND'
			sub_col.operator("layerscenes_render_to_file.button", icon='SCENE', text='').target = scene.name
			
			if(scene.scenelayer_data.is_optionsexanded == True): # if not empty
				#box = layout.box()
				row = col.row()
				row.label('Scenelayer ID: ')
				row.prop(scene.scenelayer_data, 'id', '')
				
				# Button: Copy all the objects of this to a new scene
				sub_col = row.column(align=True)
				sub_col.alignment = 'RIGHT'
				sub_col.operator("layerscenes_copylayer.button" , icon='COPY_ID' , text='').target = scene.name
				
				# pops up a confirm delete, NOT allowed on _Unsorted layer
				sub_col = row.column(align=True)
				sub_col.alignment = 'EXPAND'
				sub_col.enabled = delete_allowed
				sub_col.operator("layerscenes_deletelayerconfirm.button" , icon='PANEL_CLOSE', text='').target = scene.name	
				
				row = col.row(align=True)
				row.alignment = 'EXPAND'
				row.prop_search( scene.scenelayer_data, 'parent' , bpy.data , 'scenes')
				for child in children:					
#					LayerScenesUI_LayerControl( layout, context, child)
					LayerScenesUI_LayerControl( col, context, child)
			

class ALTERNATIVES_CreateButton(bpy.types.Operator):
	bl_idname = "layerscenes_create.button"
	bl_label = "New Scene Layer"
	bl_description = "Create a new scene layer"
	bl_icon = 'PANEL_CLOSE'
	
	scenename = bpy.props.StringProperty(default='', name="name of new layer")
	
	def execute(self, context):
		new_layer = None
		if( self.scenename == '' ):
			new_layer = layer_scene_utils.Create_LayerScene( context.scene.new_scenelayer_name )
		else:
			new_layer = layer_scene_utils.Create_LayerScene( self.scenename )
		layers = layer_scene_utils.Get_LayerScenes()
		
		if(len(layers) == 1 ):
			layer_scene_utils.Set_Active_LayerScene( new_layer )
			
		return {'FINISHED'}
		
class ALTERNATIVES_InitButton(bpy.types.Operator):
	bl_idname = "layerscenes_init.button"
	bl_label = "Init!"
	bl_description = "Create a new scene layer"
	bl_icon = 'PANEL_CLOSE'
		
	def execute(self, context):
				# do the adding of the objects to the scene and stuff
		
		# get things to check
		global glob_main_scene_name
		main_scene = layer_scene_utils.Get_Main_Scene()
		unsorted_scene = None
		active_scene = None
		
		# if main scene does not exist
		if( main_scene == None):
			# create new scene
			main_scene = layer_scene_utils.Create_LayerScene('_Viewport')
			main_scene.scenelayer_data.is_scenelayer = False
		
		# check if 'unsorted' layer exists
		
		try:
			unsorted_scene = bpy.data.scenes['_Unsorted']
		except KeyError:
			unsorted_scene = layer_scene_utils.Create_LayerScene('_Unsorted')
			layer_scene_utils.Set_Active_LayerScene(unsorted_scene)
			
		active_scene = layer_scene_utils.Get_Active_LayerScene()
		if( active_scene == None ):
			print("WARNING: Could not find default active scene _Unsorted")
		
		return {'FINISHED'}

	
class ALTERNATIVES_InvokeMenuButton(bpy.types.Operator):
	bl_idname = "layerscenes_deletelayerconfirm.button"
	bl_label = "Delete"
	
	target = bpy.props.StringProperty(default='', name="layer to delete")
	
	def execute(self, context):
		#Reminder to self:
		# Execute is called when the OK button is pressed ( in case of INFO I guess?? )
		# Invoke is called when the operator ( in the UI ) is pressed
		print("ALTERNATIVES_InvokeMenuButton just got executed")
#		message = "delete?" 
#		report_return = self.report({'INFO'}, message)
#		print("report returnvalue: %s" %(report_return))
		# work with message system? http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Interface#A_popup_dialog
		layer_scene_utils.Delete_LayerScene(bpy.data.scenes[self.target])
		return {'FINISHED'}
		
	def invoke(self, context, event):		
		print("ALTERNATIVES_InvokeMenuButton just got invoked")
		#return self.execute(context)
		return context.window_manager.invoke_confirm(self, event)
	
class ALTERNATIVES_DeleteButton(bpy.types.Operator):
	bl_idname = "layerscenes_delete.button"
	bl_label = "Delete Scene Layer"
	bl_description = "Delete this layer"
	bl_icon = 'PANEL_CLOSE'
	
	target = bpy.props.StringProperty(default='', name="layer to delete")
	
	def execute(self, context):
		layer_scene_utils.Delete_LayerScene(bpy.data.scenes[self.target])
		return {'FINISHED'}

class ALTERNATIVES_SetActiveButton(bpy.types.Operator):
	bl_idname = "layerscenes_set_active.button"
	bl_label = "Toggle Active layer"
	bl_description = "Toggles active layer"
	
	target = bpy.props.StringProperty(default='_Unsorted', name='set this layer as the active layer')
		
	def execute(self, context):
		target_layer = bpy.data.scenes[self.target]
		# toggle
		if( target_layer.scenelayer_data.is_active == False ):
			# Make all scenelayers inactive
			scenelayer_list = layer_scene_utils.Get_LayerScenes()
			for scene in scenelayer_list:
				scene.scenelayer_data.is_active = False
			
			# set active layer
			target_layer.scenelayer_data.is_active = True			
		
		# update
		layer_scene_utils.Update_Main_Scene()		
		return {'FINISHED'}

class ALTERNATIVES_RenderToFileButton(bpy.types.Operator):
	bl_idname = "layerscenes_render_to_file.button"
	bl_label = "Render To File"
	bl_description = "Render to file with automatic name."
	
	target = bpy.props.StringProperty(default='_Unsorted', name='Layer name to use.')
		
	def execute(self, context):
		target_layer = bpy.data.scenes[self.target]
		# render
		layer_scene_utils.render_layer_to_file( 'BI' , 'render/' , self.target )
		#layer_scene_utils.render_layer_to_file( 'GLSL' , 'render/' , self.target )
		#layer_scene_utils.Update_Main_Scene()		
		return {'FINISHED'}

		
class ALTERNATIVES_ToggleVisibleButton(bpy.types.Operator):
	bl_idname = "layerscenes_toggle_visible.button"
	bl_label = "Toggle Visibility"
	bl_description = "Toggles visibility"
	
	target = bpy.props.StringProperty(default='_Unsorted', name='Layer to toggle visibility of')
	
	def do_toggle(self, context, altmode = False):
		target_layer = bpy.data.scenes[self.target]
		
		# toggle, system v2
		print("v2: Updating layer visibility")
		
		if( altmode == True ):
			if ( target_layer.scenelayer_data.visibility != 2 ):
				target_layer.scenelayer_data.visibility = 2
			else:
				target_layer.scenelayer_data.visibility = 1
		else:
			# If altmode is OFF, I need to make sure there are no further alt states
			# this means reverting all isolated layers back to one
			layer_scene_utils.set_layer_visibility( 1, filter = 2)
			
			if( target_layer.scenelayer_data.visibility == 0 ):
				target_layer.scenelayer_data.visibility = 1
			else:
				target_layer.scenelayer_data.visibility = 0
		
		
		# update
		layer_scene_utils.Update_Main_Scene()		
		return {'FINISHED'}
		
	def execute(self, context):
		self.do_toggle(context, False)
		return {'FINISHED'}
		
	def invoke(self, context, event):
		print("Toggle visible button got invoked!")
		
		# if shift is pressed on this button, CLEAR ALL ISOLATIONS
		if( event.shift == True):
			layer_scene_utils.set_layer_visibility( 1, filter = 2 )
			layer_scene_utils.Update_Base_Layer()
			return {'FINISHED'}
		# execute with or without ALT	
		return self.do_toggle(context, event.alt)
		return {'PASS_THROUGH'}

class ALTERNATIVES_ToggleExpandButton(bpy.types.Operator):
	bl_idname = "layerscenes_toggle_expand.button"
	bl_label = "Toggle Expand"
	bl_description = "Toggles additional scene info on/off"
	
	target = bpy.props.StringProperty(default='', name='Scene to toggle information on/off')
	
	def execute(self, context):
		
		scene_target = bpy.data.scenes[self.target]
		# toggle
		if( scene_target.scenelayer_data.is_optionsexanded == True ):
			scene_target.scenelayer_data.is_optionsexanded = False
		else:
			scene_target.scenelayer_data.is_optionsexanded =  True
		
		return {'FINISHED'}

class ALTERNATIVES_ToggleLockButton(bpy.types.Operator):
	bl_idname = "layerscenes_toggle_lock.button"
	bl_label = "Toggle Layer Lock"
	bl_description = "Toggles additional scene selection on/off"
	
	target = bpy.props.StringProperty(default='', name='Scene to toggle lock on/off')
	
	shift_method = bpy.props.BoolProperty()
	
	
	def execute(self, context):
		
		scene_target = bpy.data.scenes[self.target]
		# toggle
		if( scene_target.scenelayer_data.is_locked == True ):
			scene_target.scenelayer_data.is_locked = False
		else:
			scene_target.scenelayer_data.is_locked =  True
		
		# lock/ unlock all items in scene
		layer_scene_utils.Set_Scene_Lock( scene_target , scene_target.scenelayer_data.is_locked )
		return {'FINISHED'}
	def invoke(self, context, event):
		print("Invoke")
		if( event.shift == True):
			print("ToggleLock is being pressed using the shift button and the GNAAIVE!")
			self.shift_method = True
			
class ALTERNATIVES_SelectLayerObjectsButton(bpy.types.Operator):
	bl_idname = "layerscenes_selectlayerobjects.button"
	bl_label = "Select layer"
	bl_description = "Select all layer objects in this layer ( Viewport ). ADDS to an existing selection."
	
	target = bpy.props.StringProperty(default='scenelayercopy', name='Scene to select')	
	
	def execute(self, context):
		#create a new layer with a copy of the current layer
		scene_target = bpy.data.scenes[self.target]
		
		# add to selection ( if viewport is viewport )
		layer_scene_utils.add_layer_to_selection( context, scene_target )
		layer_scene_utils.Update_Main_Scene()
		
		return {'FINISHED'}
		
class ALTERNATIVES_CopyLayerButton(bpy.types.Operator):
	bl_idname = "layerscenes_copylayer.button"
	bl_label = "Copy layer"
	bl_description = "Creates a copy of the given sene and all it's objects"
	bl_icon = 'COPY_ID'
	
	target = bpy.props.StringProperty(default='scenelayercopy', name='Scene to copy')
	
	
	def execute(self, context):
		#create a new layer with a copy of the current layer
		
		scene_source = bpy.data.scenes[self.target]
		#scene_target = layer_scene_utils.Create_LayerScene(scene_source.name , True)
		
		# copy all objects from scene1 to scene2
		#layer_scene_utils.Copy_Scene_To_Scene(scene_source, scene_target)
		layer_scene_utils.Duplicate_Scene(scene_source)
		layer_scene_utils.Update_Main_Scene()
		
		# make _viewport active
		main_scene = layer_scene_utils.Get_Main_Scene()		
		bpy.context.screen.scene=bpy.data.scenes[main_scene.name]
		
		return {'FINISHED'}
	
class ALTERNATIVES_AddButton(bpy.types.Operator):
	bl_idname = "layerscenes_add.button"
	bl_label = "Add selected to Scene Layer"
	bl_description = "'Moves' all selected items to this scene layer"
	bl_icon = 'PLAY'
	target = bpy.props.StringProperty(default='', name='target scene')
	
	def execute(self, context):
		scene_target = bpy.data.scenes[self.target]
		scene_source = context.scene 
		objects_selected = context.selected_objects		
		unlink = True
		layer_scene_utils.Add_Objectlist_To_Scene(scene_source, scene_target, objects_selected , unlink)
		# items are now linked to both scenes, unlink from first scene
		
		# make _viewport active
		main_scene = layer_scene_utils.Get_Main_Scene()		
		bpy.context.screen.scene=bpy.data.scenes[main_scene.name]
		
		return {'FINISHED'}

class ALTERNATIVES_UpdateButton(bpy.types.Operator):
	bl_idname = "layerscenes_update.button"
	bl_label = "Update!"
	bl_description = "Adds all selected items to the scene layer"
	
	def execute(self, context):
		layer_scene_utils.Update_Main_Scene()
		main_scene = layer_scene_utils.Get_Main_Scene()
		# make _viewport active
		bpy.context.screen.scene=bpy.data.scenes[main_scene.name]
		
		return {'FINISHED'}

class ALTERNATIVES_DeleteObjectsButton(bpy.types.Operator):
	bl_idname = "layerscenes_deleteobjects.button"
	bl_label = "SUPER Delete!"
	bl_description = "Unlink selected objects from all scenes scenelayers"
	
	def execute(self, context):
		# clear all users of this objects harhar
		selected_objects = bpy.context.selected_objects
		
		for obj in selected_objects:
			scenes = obj.users_scene
			for scene in scenes:
				if( scene.scenelayer_data.is_scenelayer == True ):
					scene.objects.unlink(obj)
		return {'FINISHED'}

class ALTERNATIVES_ConfirmDeleteMenu(bpy.types.Menu):
	bl_idname = "OBJECT_MT_confirmdeletescene_menu"
	bl_label = "Confirm Delete"
	
	bl_name = ''
	target = bpy.props.StringProperty(default='', name="layer to delete")
	
	def draw(self, context):
		layout = self.layout
		layout.label(text="Are you sure?")
		layout.operator("layerscenes_delete.button").target = self.bl_name # pass target scene
		
class ALTERNATIVES_UnlinkObjectButton(bpy.types.Operator):
	bl_idname = "layerscenes_unlinkobject.button"
	bl_label = "Unlink Object"
	bl_icon = 'UNLINKED'
	
	target = bpy.props.StringProperty(default='', name="layer to delete")
	def execute(self, context):
		# unlink selected objects from given scene ( if applicable )
		#obj = context.selected_objects[0]
		scene_target = bpy.data.scenes[self.target]
		selected_objects = context.selected_objects
		
		main_scene = layer_scene_utils.Get_Main_Scene()
		unsorted_scene = layer_scene_utils.Get_Unsorted_LayerScene()
		
		for obj in selected_objects:
			scene_target.objects.unlink(obj)			
		# if unlinking from _Unsoirted and this i s the main scene, unlink it from the main scene as well, to prevent it from getting unsorted again
			if(context.scene == main_scene and unsorted_scene == scene_target):
				main_scene.objects.unlink(obj)
		
		
		
		return {'FINISHED'}
		
			
""" Main User Interface """
class LayerScenesUI(bpy.types.Panel):
	bl_label = "Layer Scene Options:"
	bl_idname = "layersceneui"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"

	def draw(self,context):
		# create defaults if unexisting
		#layer_scene_utils.Update_Base_Layer()
	
		layout = self.layout
		obj = context.object
		scene = context.scene
		layout.label("Layer Scenes:")
		
		row = layout.row(align=True)
		row.alignment = 'EXPAND'
		#row.enabled = False
		# get main scene
		main_scene = layer_scene_utils.Get_Main_Scene()
		if( main_scene != None ):
			prop = row.prop(main_scene, "name" , "Viewport:")
			layout.box()
			row = layout.row()
			if( scene != main_scene ):
				row.label("%s:" %(context.scene.name))
				row.prop(scene.scenelayer_data, 'is_scenelayer' , 'SCENELAYER')
				row = layout.row()
				row.label("%s v2:" %(context.scene.name))
				row.prop(scene.scenelayer_data, 'type','Scene layer type')
			
			row = layout.row( align=True)
			row.alignment = 'EXPAND'
			row.prop(scene, "new_scenelayer_name" , text="")
			
			new_scene_name = 'new layer'			
			if( scene.new_scenelayer_name != ''):
				new_scene_name = scene.new_scenelayer_name
			row.operator("layerscenes_create.button" , "Create Layer").scenename = new_scene_name
				
			# layer list box
			box = layout.box()
			
			for scn in bpy.data.scenes:
				# if scene has a VALID parent, then draw it
				if( layer_scene_utils.Get_LayerScene_Parent( scn ) == None):
					LayerScenesUI_LayerControl( box, context, scn)
			layout.operator('layerscenes_update.button')
			
		else:
			row.operator("layerscenes_init.button")
			#row.operator("layerscenes_create.button").scenename = '_Viewport'
""" Main User Interface for objects """			
class LayerScenesUI(bpy.types.Panel):
	bl_label = "Layer Scene Object Options:"
	bl_idname = "layersceneobjectui"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "object"

	def draw(self,context):
		# create defaults if unexisting
		#layer_scene_utils.Update_Base_Layer()

		main_scene = layer_scene_utils.Get_Main_Scene()
		if( main_scene != None ):
			layout = self.layout
			obj = context.object
			scene = context.scene
			
			main_scene = layer_scene_utils.Get_Main_Scene()
			
			layout.label('Scene is linked to:')
			box = layout.box()
			scene_count = len(obj.users_scene)
			
			#try:
			#	main_scene_index = obj.users_scene.index( main_scene )
			#except KeyError:
			#	scene_count -= 1 # don't count son!
			
			# get all scenes in the selection of objects
			all_user_scenes = []
			for selected_obj in context.selected_objects:
				for scene in selected_obj.users_scene:
					try:
						all_user_scenes.index( scene )
					except ValueError:
						#not exist 
						all_user_scenes.append(scene)
					
						
			#print(all_user_scenes)
			for user_scene in all_user_scenes:
				row = box.row(align=True)
				row.alignment = 'EXPAND'
				
				# the main scene does not count as an actual scene			
				if( main_scene != user_scene):				
					
					# draw logix
					row.label(user_scene.name)
					# unlink layer button only shows when there are no scenes to which this object is linked
					if( scene_count > 1):
						row.operator("layerscenes_unlinkobject.button", icon = 'UNLINKED', text='Unlink').target = user_scene.name
					
print("Imported Layer_scene_ui.py")