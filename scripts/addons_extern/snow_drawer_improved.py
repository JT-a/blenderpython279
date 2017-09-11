bl_info = {
"name": "Snow Drawer", 
"version": (1, 0, 0),
"blender": (2, 78, 0),
"location": "Tool Shelf > Snow Drawer > Snow Drawer" ,
"description": "Draw snow on objects using weight paint and convert to mesh.",
"category": "Object"} 
  
   
import bpy
from bpy.props import BoolProperty, EnumProperty
from bpy.types import Panel



######################################################################################
#Draw Snow Panel  
class DrawSnowPanel(bpy.types.Panel):
	"""Creates a Panel in the Logic Editor properties window""" 
	bl_label = "Snow Drawer" 
	bl_idname = "OBJECT_draw_snow_panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Create"
	

	def draw(self, context):
		layout = self.layout
		
		act_obj = bpy.context.active_object
		scene = bpy.context.scene
   
		col = layout.column(align = True)

		snow_settings = context.scene.snow_settings
	
		if snow_settings == False:  
			col.operator("object.draw_snow", text="Create Snow", icon='FREEZE')

		if 'SnowDrawer_SnowBall' in bpy.data.objects:
			snow_particle = bpy.data.objects['SnowDrawer_SnowBall']
   
				   
			if scene.active_layer and not act_obj or not act_obj:   
				col.label(text="Snow object not on this layer!", icon='ERROR')


			if scene.active_layer and act_obj or act_obj:   							
				if snow_particle.mode != 'EDIT' and act_obj.mode == 'EDIT' and 'SnowDrawer_SnowParticles' in act_obj.particle_systems:

					col.operator("object.snow_weight", text="Re-Calculate Weights", icon='WPAINT_HLT')
					snow_edit = context.scene.snow_edit 	
					if snow_edit == True:
						edit = col.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT')
						edit.mode= 'EDIT' 

			
				if snow_particle.mode != 'EDIT' and act_obj.mode == 'OBJECT'  and 'SnowDrawer_SnowParticles' in act_obj.particle_systems or act_obj.mode == 'WEIGHT_PAINT' and 'SnowDrawer_SnowParticles' in act_obj.particle_systems:    
							
					col.operator("object.snow_to_mesh", text="Snow to Mesh", icon='MESH_ICOSPHERE')
					col.operator("object.snow_weight", text="Re-Calculate Weights", icon='WPAINT_HLT')
					if snow_particle.mode != 'EDIT' and act_obj.mode == 'OBJECT':
					   col.operator("object.snow_delete", text="Delete Snow", icon='CANCEL')
					snow_edit = context.scene.snow_edit 	
					if snow_edit == True:
						edit = col.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT')
						edit.mode= 'EDIT'
			  
					col.prop(act_obj, "snow_bool", text="Use Snow Modifier")

				snow_bool = context.object.snow_bool
				if snow_bool == True and act_obj.mode == 'OBJECT'  and 'SnowDrawer_SnowParticles' in act_obj.particle_systems or snow_bool == True and act_obj.mode == 'WEIGHT_PAINT' and 'SnowDrawer_SnowParticles' in act_obj.particle_systems:
					col.label(text="Modifier tends to fail on thin snow!", icon='ERROR')



				if snow_particle.mode != 'EDIT' and act_obj.mode != 'OBJECT' and act_obj.mode != 'EDIT' and act_obj.mode != 'WEIGHT_PAINT' and 'SnowDrawer_SnowParticles' in act_obj.particle_systems:  
							
					col.label(text="Must be in Object, Edit, or Weight Paint mode!", icon='ERROR')




				if snow_particle.mode != 'EDIT' and act_obj.mode == 'OBJECT' and 'SnowDrawer_SnowParticles' not in act_obj.particle_systems:	
							
					col.label(text="Object doesn't have a 'SnowDrawer_SnowParticles' particle system!", icon='ERROR')
					col.label(text="Must be the wrong object selected!")
					for scn_objs in scene.objects:
						if 'SnowDrawer_SnowParticles' in scn_objs.particle_systems:
							col.label(text="Object with snow is:   " + scn_objs.name)

#If 'SnowDrawer_SnowBall' is selected to change origin point
				if snow_settings == True:
					snow_particle = bpy.data.objects['SnowDrawer_SnowBall']
					if snow_particle.mode == 'EDIT':	
						snow_object = bpy.context.selected_objects[0]   		
						col = layout.column(align = True)    
						col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0], "co", text="Particle Origin")
						col.operator("object.snow_origin", text="Particle Origin", icon='LAYER_ACTIVE')
						col.label("Emit From:")
						col = layout.column(align = True)
						col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "emit_from", expand=True)
						col = layout.column(align = True) 
						col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "count", text="Snow Density")
						col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "draw_percentage", text="Random Shape")
						col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "size_random", text="Random Size")
						col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "particle_size", text="Snow Depth")
						col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "drag_factor", text="Snow Melting")
						col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'], "resolution", text="Snow Resolution")
						col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'], "threshold", text="Snow Threshold")
						col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0], "stiffness", text="Snow Stiffness")
						col.prop(snow_object.particle_systems['SnowDrawer_SnowParticles'], "seed", text="Seed") 		
						col.prop(bpy.data.objects["SnowDrawer_SnowBall"], "scale", text="Snow Particle Scaling")				
						box = layout.box()
						box.prop(act_obj, "snow_presets")
						row = layout.row() 
						box.operator("object.snow_presets", text="Apply Preset", icon='FILE_TICK')


#If object that snow is applied to is selected and not in weight paint mode
					if act_obj.mode == 'OBJECT' or 'WEIGHT_PAINT':  			
						if act_obj.mode == 'OBJECT' and 'SnowDrawer_SnowParticles' in act_obj.particle_systems:
							col = layout.column(align = True)
							col.label("Particle Origin:")
							col.operator("object.snow_origin", text="Particle Origin", icon='LAYER_ACTIVE') 	   
							col.label("Snow Brush:")	
							weight = col.operator("object.mode_set", text="Draw Snow", icon='VPAINT_HLT')
							weight.mode= 'WEIGHT_PAINT'
							col.label("Emit From:")
							col = layout.column(align = True)
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "emit_from", expand=True)
							col = layout.column(align = True)
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "count", text="Snow Density")
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "draw_percentage", text="Random Shape")
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "size_random", text="Random Size")
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "particle_size", text="Snow Depth")
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "drag_factor", text="Snow Melting")
							col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'], "resolution", text="Snow Resolution")
							col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'], "threshold", text="Snow Threshold")
							col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0], "stiffness", text="Snow Stiffness")
							if 'SnowDrawer_SnowParticles' in act_obj.particle_systems: 
								col.prop(act_obj.particle_systems['SnowDrawer_SnowParticles'], "seed", text="Seed") 			
							col.prop(bpy.data.objects["SnowDrawer_SnowBall"], "scale", text="Snow Particle Scaling")				
							box = layout.box()
							box.prop(act_obj, "snow_presets")
							row = layout.row() 
							box.operator("object.snow_presets", text="Apply Preset", icon='FILE_TICK')
			
#If object that snow is applied to is selected and is in weight paint mode  				
						if act_obj.mode == 'WEIGHT_PAINT' and 'SnowDrawer_SnowParticles' in act_obj.particle_systems:
							col = layout.column(align = True)
							col.label("Particle Origin:")
							col.operator("object.snow_origin", text="Particle Origin", icon='LAYER_ACTIVE') 	   
							col.label("Snow Brush:")	
							object = col.operator("object.mode_set", text="Object Mode", icon='OBJECT_DATAMODE')
							object.mode= 'OBJECT'
							for scn in bpy.data.scenes:
								scn_name = scn.name 
							col.prop(bpy.data.scenes[scn_name].tool_settings.unified_paint_settings, "weight", slider= True) 
							col.prop(bpy.data.scenes[scn_name].tool_settings.unified_paint_settings, "size", slider= True)  	
							col.prop(bpy.data.brushes["Snow Drawer"], "strength")
							col.prop(bpy.data.brushes["Snow Drawer"], "vertex_tool", text="")
							col.prop(act_obj, "snow_hide", icon='RESTRICT_VIEW_OFF', toggle= True)  		   
							col.label("Emit From:")
							col = layout.column(align = True)
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "emit_from", expand=True)
							col = layout.column(align = True) 
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "count", text="Snow Density")
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "draw_percentage", text="Random Shape")
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "size_random", text="Random Size")
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "particle_size", text="Snow Depth")
							col.prop(bpy.data.particles["SnowDrawer_SnowParticles"], "drag_factor", text="Snow Melting")
							col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'], "resolution", text="Snow Resolution")
							col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'], "threshold", text="Snow Threshold")
							col.prop(bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0], "stiffness", text="Snow Stiffness")
							if 'SnowDrawer_SnowParticles' in act_obj.particle_systems: 
								col.prop(act_obj.particle_systems['SnowDrawer_SnowParticles'], "seed", text="Seed") 			
							col.prop(bpy.data.objects["SnowDrawer_SnowBall"], "scale", text="Snow Particle Scaling")				
							box = layout.box()
							box.prop(act_obj, "snow_presets")
							row = layout.row() 
							box.operator("object.snow_presets", text="Apply Preset", icon='FILE_TICK')     
######################################################################################  		 



######################################################################################
#Start draw snow operator
class DrawSnow(bpy.types.Operator):
	"""Create snow on the active object"""  
	bl_idname = "object.draw_snow"
	bl_label = "Draw Snow"

	
	def execute(self, context):
	
		act_obj = bpy.context.active_object
		snow_object = bpy.context.active_object
		scene = bpy.context.scene



		if snow_object.mode != 'EDIT':
			bpy.ops.snowedit.errormessage('INVOKE_DEFAULT')
			return {'CANCELLED'}



		if snow_object.mode == 'EDIT':
	
			bpy.data.brushes.new(name ='Snow Drawer', mode='WEIGHT_PAINT')
			bpy.context.tool_settings.weight_paint.brush = bpy.data.brushes['Snow Drawer']
							
			act_obj.show_name = True
	
			bpy.ops.view3d.snap_cursor_to_selected()			
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
			bpy.ops.object.metaball_add(type ='BALL')

			act_obj = bpy.context.active_object

			act_obj.name = 'SnowDrawer_SnowBall'
			act_obj.data.name = 'SnowDrawer_SnowBall'
			act_obj.scale[0] = .074
			act_obj.scale[1] = .074
			act_obj.scale[2] = .074
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .2
			bpy.data.objects['SnowDrawer_SnowBall'].parent = snow_object
			bpy.ops.view3d.snap_selected_to_cursor(use_offset= False)
			act_obj.select = False
			snow_object.select = True
			scene.objects.active = snow_object
			######################################################################################



			######################################################################################
			#Add Vertex Group to the object to apply snow to
			act_obj = bpy.context.active_object

			snow_vertex = act_obj.vertex_groups.new()
			snow_vertex.name = "Snow_Vertex"
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)
			bpy.ops.mesh.select_similar(type='NORMAL', threshold=0.33)
			bpy.context.scene.tool_settings.vertex_group_weight = 1.0
			bpy.ops.object.vertex_group_assign()
			######################################################################################



			######################################################################################
			#Add Snow Particle System
			act_obj = bpy.context.active_object

			bpy.ops.object.particle_system_add()

			final_size = act_obj.data

			particle_number = len(final_size.vertices)


			#Settings
			act_obj.particle_systems[0].name = 'SnowDrawer_SnowParticles'
			act_obj.particle_systems.active_index = 0
			act_obj.particle_systems['SnowDrawer_SnowParticles'].seed = 10


			if 'SnowDrawer_SnowParticles' not in bpy.data.particles:				
				bpy.data.particles[0].name = 'SnowDrawer_SnowParticles'
				bpy.data.particles['SnowDrawer_SnowParticles'].type = 'HAIR'
				bpy.data.particles['SnowDrawer_SnowParticles'].hair_step = 3
				bpy.data.particles['SnowDrawer_SnowParticles'].use_advanced_hair = True
				#Emission
				bpy.data.particles['SnowDrawer_SnowParticles'].count = particle_number
				bpy.data.particles['SnowDrawer_SnowParticles'].hair_length = 0.0
				bpy.data.particles['SnowDrawer_SnowParticles'].userjit = 10
				bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'FACE'
				bpy.data.particles['SnowDrawer_SnowParticles'].use_emit_random = False
				bpy.data.particles['SnowDrawer_SnowParticles'].use_even_distribution = True
				#Velocity
				bpy.data.particles['SnowDrawer_SnowParticles'].normal_factor = 0.0
				bpy.data.particles['SnowDrawer_SnowParticles'].tangent_factor = .25
				bpy.data.particles['SnowDrawer_SnowParticles'].tangent_phase = .05
				bpy.data.particles['SnowDrawer_SnowParticles'].factor_random = .15
				bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[0] = .1
				bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[1] = 0.0
				bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[2] = .05    
				#Physics
				bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
				bpy.data.particles['SnowDrawer_SnowParticles'].physics_type = 'NEWTON'
				bpy.data.particles['SnowDrawer_SnowParticles'].particle_size =  .9
				bpy.data.particles['SnowDrawer_SnowParticles'].brownian_factor = .31
				bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
				bpy.data.particles['SnowDrawer_SnowParticles'].integrator = 'VERLET'
				#Render
				bpy.data.particles['SnowDrawer_SnowParticles'].render_type = 'OBJECT'
				bpy.data.particles['SnowDrawer_SnowParticles'].dupli_object = bpy.data.objects['SnowDrawer_SnowBall']
				bpy.data.particles['SnowDrawer_SnowParticles'].use_scale_dupli = True
				bpy.data.particles['SnowDrawer_SnowParticles'].use_rotation_dupli = True
				#Vertex Groups
				act_obj.particle_systems['SnowDrawer_SnowParticles'].vertex_group_density = 'Snow_Vertex'
				act_obj.particle_systems['SnowDrawer_SnowParticles'].vertex_group_length = 'Snow_Vertex'
				bpy.data.brushes["Snow Drawer"].vertex_tool = 'ADD'
				bpy.data.brushes["Snow Drawer"].strength = 1.0
				bpy.ops.object.mode_set(mode='OBJECT', toggle=False)				
				context.scene.snow_settings = True


			if 'SnowDrawer_SnowParticles' in bpy.data.particles:				
				par_set = bpy.data.particles['SnowDrawer_SnowParticles']
				act_obj.particle_systems['SnowDrawer_SnowParticles'].settings = par_set
				bpy.data.particles['SnowDrawer_SnowParticles'].type = 'HAIR'
				bpy.data.particles['SnowDrawer_SnowParticles'].hair_step = 3
				bpy.data.particles['SnowDrawer_SnowParticles'].use_advanced_hair = True
				#Emission
				bpy.data.particles['SnowDrawer_SnowParticles'].count = particle_number
				bpy.data.particles['SnowDrawer_SnowParticles'].hair_length = 0.0
				bpy.data.particles['SnowDrawer_SnowParticles'].userjit = 10
				bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'FACE'
				bpy.data.particles['SnowDrawer_SnowParticles'].use_emit_random = False
				bpy.data.particles['SnowDrawer_SnowParticles'].use_even_distribution = True
				#Velocity
				bpy.data.particles['SnowDrawer_SnowParticles'].normal_factor = 0.0
				bpy.data.particles['SnowDrawer_SnowParticles'].tangent_factor = .25
				bpy.data.particles['SnowDrawer_SnowParticles'].tangent_phase = .05
				bpy.data.particles['SnowDrawer_SnowParticles'].factor_random = .15
				bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[0] = .1
				bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[1] = 0.0
				bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[2] = .05    
				#Physics
				bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
				bpy.data.particles['SnowDrawer_SnowParticles'].physics_type = 'NEWTON'
				bpy.data.particles['SnowDrawer_SnowParticles'].particle_size =  .9
				bpy.data.particles['SnowDrawer_SnowParticles'].brownian_factor = .31
				bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
				bpy.data.particles['SnowDrawer_SnowParticles'].integrator = 'VERLET'
				#Render
				bpy.data.particles['SnowDrawer_SnowParticles'].render_type = 'OBJECT'
				bpy.data.particles['SnowDrawer_SnowParticles'].dupli_object = bpy.data.objects['SnowDrawer_SnowBall']
				bpy.data.particles['SnowDrawer_SnowParticles'].use_scale_dupli = True
				bpy.data.particles['SnowDrawer_SnowParticles'].use_rotation_dupli = True
				#Vertex Groups
				act_obj.particle_systems['SnowDrawer_SnowParticles'].vertex_group_density = 'Snow_Vertex'
				act_obj.particle_systems['SnowDrawer_SnowParticles'].vertex_group_length = 'Snow_Vertex'
				bpy.data.brushes["Snow Drawer"].vertex_tool = 'ADD'
				bpy.data.brushes["Snow Drawer"].strength = 1.0
				bpy.ops.object.mode_set(mode='OBJECT', toggle=False)				
				context.scene.snow_settings = True


		return {'FINISHED'}
######################################################################################



######################################################################################
#Snow to mesh operator
class SnowMesh(bpy.types.Operator):
	"""Make snow into mesh object"""  
	bl_idname = "object.snow_to_mesh"
	bl_label = "Make Snow"

	
	def execute(self, context):

		snow_object = bpy.context.selected_objects[0]
		act_obj = bpy.context.active_object
		scene = bpy.context.scene
		snow_bool = context.object.snow_bool


		if snow_bool == True:   
			act_obj.show_name = False     
			context.scene.snow_settings = False 	   
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
			snow_convert = bpy.data.objects['SnowDrawer_SnowBall']
			snow_convert.select = True
			scene.objects.active = snow_convert
			snow_object.select = False
			scene.objects.active = snow_convert
			bpy.ops.object.convert(target= 'MESH')
			bpy.ops.object.transform_apply(location= False, rotation= False, scale= True)
			snow_object.select = True
			bpy.ops.object.modifier_add(type= 'BOOLEAN')
			bpy.context.object.modifiers[0].name = "SnowDrawer_SnowBool"
			bpy.context.object.modifiers["SnowDrawer_SnowBool"].object = act_obj
			bpy.context.object.modifiers["SnowDrawer_SnowBool"].operation = 'DIFFERENCE'
			bpy.context.object.modifiers["SnowDrawer_SnowBool"].solver = 'CARVE'
			bpy.ops.object.modifier_apply(apply_as= 'DATA', modifier= "SnowDrawer_SnowBool")
			#Smooth vertices
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)
			bpy.ops.mesh.select_all(action= 'SELECT')
			bpy.ops.mesh.vertices_smooth(factor= 0.5, repeat= 2)
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
			#############################################################
			snow_converted = bpy.data.objects['SnowDrawer_SnowBall.001']
			snow_converted.name = act_obj.name + "_" + "Snow"
			snow_mesh_converted = bpy.data.meshes['Mesh']
			snow_mesh_converted.name = snow_converted.name
			bpy.context.space_data.viewport_shade = 'SOLID'
			bpy.ops.view3d.snap_cursor_to_center()
			bpy.ops.object.origin_set(type= 'ORIGIN_GEOMETRY')
			bpy.data.objects[act_obj.name + "_" + "Snow"].parent = None
			snow_object.select = True
			scene.objects.active = snow_object
			bpy.ops.object.particle_system_remove()

			for meta in bpy.data.metaballs:
				meta_name = meta.name     
				if meta_name.startswith("SnowDrawer_SnowBall"):
					meta = bpy.data.metaballs[meta_name]
					bpy.data.metaballs.remove(meta)

			for snow in bpy.data.particles:
				snow_name = snow.name     
				if snow_name.startswith("SnowDrawer_SnowParticles"):
					particles = bpy.data.particles[snow_name]
					bpy.data.particles.remove(particles)		

			for snow_brush in bpy.data.brushes:
				snow_brush = snow_brush.name	 
				if snow_brush.startswith("Snow Drawer"):
					snow_brush_delete = bpy.data.brushes[snow_brush]
					bpy.data.brushes.remove(snow_brush_delete, do_unlink = True)

			obj = bpy.context.object
			   
			if 'Snow_Vertex' in obj.vertex_groups:
				bpy.ops.object.vertex_group_remove(all=False)
			

		if snow_bool == False:
			act_obj.show_name = False     
			context.scene.snow_settings = False 	   
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
			snow_convert = bpy.data.objects['SnowDrawer_SnowBall']
			snow_convert.select = True
			scene.objects.active = snow_convert
			snow_object.select = False
			scene.objects.active = snow_convert
			bpy.ops.object.convert(target= 'MESH')
			bpy.ops.object.transform_apply(location= False, rotation= False, scale= True)
			snow_object.select = True
			#Smooth vertices
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)
			bpy.ops.mesh.select_all(action= 'SELECT')
			bpy.ops.mesh.vertices_smooth(factor= 0.5, repeat= 2)
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
			#############################################################
			snow_converted = bpy.data.objects['SnowDrawer_SnowBall.001']
			snow_converted.name = act_obj.name + "_" + "Snow"
			snow_mesh_converted = bpy.data.meshes['Mesh']
			snow_mesh_converted.name = snow_converted.name
			bpy.context.space_data.viewport_shade = 'SOLID'
			bpy.ops.view3d.snap_cursor_to_center()
			bpy.ops.object.origin_set(type= 'ORIGIN_GEOMETRY')
			bpy.data.objects[act_obj.name + "_" + "Snow"].parent = None
			snow_object.select = True
			scene.objects.active = snow_object
			bpy.ops.object.particle_system_remove()

			for meta in bpy.data.metaballs:
				meta_name = meta.name     
				if meta_name.startswith("SnowDrawer_SnowBall"):
					meta = bpy.data.metaballs[meta_name]
					bpy.data.metaballs.remove(meta)

			for snow in bpy.data.particles:
				snow_name = snow.name     
				if snow_name.startswith("SnowDrawer_SnowParticles"):
					particles = bpy.data.particles[snow_name]
					bpy.data.particles.remove(particles)		

			for snow_brush in bpy.data.brushes:
				snow_brush = snow_brush.name	 
				if snow_brush.startswith("Snow Drawer"):
					snow_brush_delete = bpy.data.brushes[snow_brush]
					bpy.data.brushes.remove(snow_brush_delete, do_unlink = True)

			obj = bpy.context.object
			   
			if 'Snow_Vertex' in obj.vertex_groups:
				bpy.ops.object.vertex_group_remove(all=False)

								
		return {'FINISHED'}
######################################################################################



######################################################################################
class SnowWeightOperator(bpy.types.Operator):
	"""Re-calculate weights"""  
	bl_idname = "object.snow_weight"
	bl_label = "Snow Weight"


	def execute(self, context):
	

		snow_object = bpy.context.active_object


		if snow_object.mode != 'EDIT':
			context.scene.snow_edit = True    
			bpy.ops.snowedit.errormessage('INVOKE_DEFAULT')
			return {'CANCELLED'}


		if snow_object.mode == 'EDIT' and 'Snow_Vertex' in snow_object.vertex_groups:   	
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)	
			scene = bpy.context.scene
			snow_object_layer = scene.active_layer  	   
			snow_particle = bpy.data.objects["SnowDrawer_SnowBall"]
			snow_particle.select = True
			snow_particle.layers[19] = True
			snow_particle.layers[snow_object_layer] = False
			snow_particle.select = False	 
			############################################################################################################3   		
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)    
			############################################################################################################3   	  
			context.scene.snow_edit = False    
			bpy.ops.object.vertex_group_remove(all=False)   		 
			snow_vertex = snow_object.vertex_groups.new()
			snow_vertex.name = "Snow_Vertex"
			bpy.ops.mesh.select_similar(type='NORMAL', threshold=0.33)
			bpy.context.scene.tool_settings.vertex_group_weight = 1.0
			bpy.ops.object.vertex_group_assign()
			bpy.data.particles['SnowDrawer_SnowParticles'].dupli_object = bpy.data.objects['SnowDrawer_SnowBall']   
			#Vertex Groups
			snow_object.particle_systems['SnowDrawer_SnowParticles'].vertex_group_density = 'Snow_Vertex'
			snow_object.particle_systems['SnowDrawer_SnowParticles'].vertex_group_length = 'Snow_Vertex'
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'FACE'
			############################################################################################################3 
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False) 
			scene = bpy.context.scene
			snow_object_layer = scene.active_layer  		  
			snow_particle = bpy.data.objects["SnowDrawer_SnowBall"]
			snow_particle.select = True 	   
			snow_particle.layers[snow_object_layer] = True
			snow_particle.layers[19] = False
			snow_particle.select = False	 
			bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)

		else:
			bpy.ops.snowvertexgroup.errormessage('INVOKE_DEFAULT')
			return {'CANCELLED'}

	
		return {'FINISHED'}
######################################################################################



######################################################################################
class SnowEditErrorOperator(bpy.types.Operator):
	bl_idname = "snowedit.errormessage"
	bl_label = "Snow Edit Error"


	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_popup(self, width=400, height=50)
		return {'FINISHED'}

	def draw(self, context):
		layout = self.layout
		layout.label(text = "Must be in edit mode and select a face or vertice for the direction of snow", icon = "ERROR")
######################################################################################



######################################################################################
class SnowVertexErrorOperator(bpy.types.Operator):
	bl_idname = "snowvertexgroup.errormessage"
	bl_label = "Snow Vertex Error"


	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_popup(self, width=150, height=50)
		return {'FINISHED'}

	def draw(self, context):
		layout = self.layout
		layout.label(text = "No vertex group!", icon = "ERROR")
######################################################################################



######################################################################################

class SnowPresets(bpy.types.Operator):
	"""Apply selected preset to the snow"""  
	bl_idname = "object.snow_presets"
	bl_label = "Snow Presets"


	def execute(self, context):

		
		snow_preset = context.object.snow_presets
					
		#Snow Preset 1
		if snow_preset == "PRESET1":
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'VERT'
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 3000
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = 1.05
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .2
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .04
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .05
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .03

		#Snow Preset 2
		if snow_preset == "PRESET2":
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'FACE'
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 1525
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .3
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = .95
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .3
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .08
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .07
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .04

		#Snow Preset 3
		if snow_preset == "PRESET3":
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'VOLUME'
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 5000
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .3
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = .6
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .8
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .6
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .08
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .140
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .06

		#Snow Preset 4
		if snow_preset == "PRESET4":
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'VERT'
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 3000
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = 1.05
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .2
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .07
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .08
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .06

		#Snow Default
		if snow_preset == "DEFAULT":	
			act_obj = bpy.context.active_object

			final_size = act_obj.data

			particle_number = len(final_size.vertices)
	
			act_obj.particle_systems['SnowDrawer_SnowParticles'].seed = 10     
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'FACE'
			bpy.data.particles['SnowDrawer_SnowParticles'].draw_percentage = 100
			bpy.data.particles['SnowDrawer_SnowParticles'].count = particle_number
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = .9
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .2
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .074
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .074
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .074

		#Snow Preset 5
		if snow_preset == "PRESET5":
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'VERT'
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 1100
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = .9
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .2
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .08
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .120
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .09

		#Snow Preset 6
		if snow_preset == "PRESET6":
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'VERT'
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 1100
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = .95
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = 0.0
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .675
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = 1.0
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .2
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .1
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .07
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .07

		#Snow Preset 7
		if snow_preset == "PRESET7":
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'FACE'
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 5000
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .3
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = .6
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .8
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .6
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .08
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .140
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .06

		#Snow Preset 8
		if snow_preset == "PRESET8":
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'FACE'
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 3000
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = 1.05
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .1
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .2
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .04
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .05
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .03

		#Snow Preset 9
		if snow_preset == "PRESET9":
			bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[0] = .1
			bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[1] = 0.0
			bpy.data.particles['SnowDrawer_SnowParticles'].object_align_factor[2] = .05    
			bpy.data.particles['SnowDrawer_SnowParticles'].emit_from = 'FACE'
			bpy.data.particles['SnowDrawer_SnowParticles'].use_even_distribution = True
			bpy.data.particles['SnowDrawer_SnowParticles'].count = 6000
			bpy.data.particles['SnowDrawer_SnowParticles'].size_random = .1
			bpy.data.particles['SnowDrawer_SnowParticles'].particle_size = 1.00
			bpy.data.particles['SnowDrawer_SnowParticles'].drag_factor = .2
			bpy.data.metaballs['SnowDrawer_SnowBall'].resolution = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].threshold = .7
			bpy.data.metaballs['SnowDrawer_SnowBall'].elements[0].stiffness = .2
			bpy.data.objects['SnowDrawer_SnowBall'].scale[0] = .05
			bpy.data.objects['SnowDrawer_SnowBall'].scale[1] = .05
			bpy.data.objects['SnowDrawer_SnowBall'].scale[2] = .02



		return {'FINISHED'}
######################################################################################



######################################################################################
class SnowDeleteOperator(bpy.types.Operator):
	"""Remove snow particle system."""  
	bl_idname = "object.snow_delete"
	bl_label = "Snow Delete"


	def execute(self, context):
	

		snow_object = bpy.context.active_object
		snow_particle = bpy.data.objects['SnowDrawer_SnowBall']

		bpy.data.objects['SnowDrawer_SnowBall'].parent = None
		
		bpy.ops.object.vertex_group_remove(all=False)
		snow_object.select = False     
		snow_particle.select = True
		bpy.ops.object.delete(use_global= False)

		snow_object.select = True
		for meta in bpy.data.metaballs:
			meta_name = meta.name     
			if meta_name.startswith("SnowDrawer_SnowBall"):
				meta = bpy.data.metaballs[meta_name]
				bpy.data.metaballs.remove(meta)  

		#for snow in bpy.data.particles:
			#snow_name = snow.name     
			#if snow_name.startswith("SnowDrawer_SnowParticles_Remove"):
				#particles = bpy.data.particles[snow_name]
				#bpy.data.particles.remove(particles, do_unlink= True)


		#bpy.data.particles["SnowDrawer_SnowParticles"].name = "SnowDrawer_SnowParticles_Remove"
		snow_object.show_name = False 
		bpy.ops.object.particle_system_remove()
		context.scene.snow_settings = False
		
		for snow_brush in bpy.data.brushes:
			snow_brush = snow_brush.name	 
			if snow_brush.startswith("Snow Drawer"):
				snow_brush_delete = bpy.data.brushes[snow_brush]
				bpy.data.brushes.remove(snow_brush_delete, do_unlink = True)

			
		return {'FINISHED'}
######################################################################################



######################################################################################
class SnowOriginOperator(bpy.types.Operator):
	"""Click to change the particle's origin, click again to set the origin."""  
	bl_idname = "object.snow_origin"
	bl_label = "Snow Origin"


	def execute(self, context):
	

		snow_object = bpy.context.selected_objects[0]
		scene = bpy.context.scene
		snow_particle = bpy.data.objects['SnowDrawer_SnowBall']
		snow_origin_bool = context.object.snow_origin_bool


		if snow_origin_bool == True:		
			snow_particle.select = False
			snow_object.draw_type = 'SOLID'
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
			scene.objects.active = snow_object
			bpy.context.space_data.show_manipulator = True
			context.object.snow_origin_bool = False    


		if snow_origin_bool == False:
			snow_particle.select = True
			snow_object.draw_type = 'WIRE'
			scene.objects.active = snow_particle
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)
			bpy.context.space_data.show_manipulator = False  
			context.object.snow_origin_bool = True 

	
		return {'FINISHED'}
######################################################################################



######################################################################################
def snow_hide(self, context):

	snow_hide = context.object.snow_hide

	if snow_hide == False:
		scene = bpy.context.scene
		snow_object_layer = scene.active_layer  		  
		snow_particle = bpy.data.objects["SnowDrawer_SnowBall"]
		snow_particle.select = True 	   
		snow_particle.layers[snow_object_layer] = True
		snow_particle.layers[19] = False
		snow_particle.select = False
		
	if snow_hide == True:
		scene = bpy.context.scene
		snow_object_layer = scene.active_layer  	   
		snow_particle = bpy.data.objects["SnowDrawer_SnowBall"]
		snow_particle.select = True
		snow_particle.layers[19] = True
		snow_particle.layers[snow_object_layer] = False
		snow_particle.select = False
######################################################################################


def register():
	bpy.utils.register_class(DrawSnowPanel)
	bpy.utils.register_class(DrawSnow)
	bpy.utils.register_class(SnowMesh)
	bpy.utils.register_class(SnowEditErrorOperator)
	bpy.utils.register_class(SnowPresets)
	bpy.utils.register_class(SnowWeightOperator)
	bpy.utils.register_class(SnowVertexErrorOperator)
	bpy.utils.register_class(SnowOriginOperator)
	bpy.utils.register_class(SnowDeleteOperator)

	bpy.types.Scene.snow_settings = bpy.props.BoolProperty(
		name = "",
		description = "",
		default = False
	  )
	bpy.types.Scene.snow_edit = bpy.props.BoolProperty(
		name = "",
		description = "",
		default = False
	  )
	bpy.types.Object.snow_origin_bool = bpy.props.BoolProperty(
		name = "",
		description = "Double click to change / set the particles origin.",
		default = False,
	  )
	bpy.types.Object.snow_bool = bpy.props.BoolProperty(
		name = "",
		description = "Use a difference boolean modifier when making snow into mesh.",
		default = True
	  )
	bpy.types.Object.snow_hide = bpy.props.BoolProperty(
		name = "",
		description = "If weight painting with snow is slow, toggle to hide / reveal snow.",
		default = False,
		update = snow_hide
	  )
	bpy.types.Object.snow_presets = bpy.props.EnumProperty(
			name = "Snow Presets",
			description = "Apply this preset to the snow",
			items = [
				("DEFAULT", "Default", "", 1),
				("PRESET1", "Snow 1", "", 2),
				("PRESET3", "Snow 2", "", 4),
				("PRESET4", "Snow 3", "", 5),
				("PRESET5", "Snow 4", "", 6),
				("PRESET6", "Snow 5", "", 7),
				("PRESET7", "Snow 6", "", 8),
				("PRESET2", "Melted Snow 3", "", 3),
				("PRESET8", "Melted Snow 2", "", 9),
				("PRESET9", "Melted Snow 1", "", 10),   		 
			]
		)
######################################################################################

	
def unregister():
	bpy.utils.unregister_class(DrawSnowPanel)
	bpy.utils.unregister_class(DrawSnow)
	bpy.utils.unregister_class(SnowMesh)
	bpy.utils.unregister_class(SnowEditErrorOperator)
	bpy.utils.unregister_class(SnowPresets)
	bpy.utils.unregister_class(SnowWeightOperator)
	bpy.utils.unregister_class(SnowVertexErrorOperator)
	bpy.utils.unregister_class(SnowOriginOperator)
	bpy.utils.unregister_class(SnowDeleteOperator)

	del bpy.types.Scene.snow_settings
	del bpy.types.Object.snow_presets
	del bpy.types.Object.snow_bool
	del bpy.types.Object.snow_edit
	del bpy.types.Object.snow_origin_bool
	del bpy.types.Object.snow_hide

	
if __name__ == "__main__":
	register()

