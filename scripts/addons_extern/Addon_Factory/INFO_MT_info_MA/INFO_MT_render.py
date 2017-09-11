# 情報 > 「レンダー」メニュー

import bpy
import sys, subprocess

################
# オペレーター #
################

class RenderBackground(bpy.types.Operator):
	bl_idname = "render.render_background"
	bl_label = "Background Render"
	bl_description = "Render From The Commandline"
	bl_options = {'REGISTER'}
	
	is_quit = bpy.props.BoolProperty(name="Quit Blender", default=True)
	items = [
		('IMAGE', "Image", "", 1),
		('ANIME', "Animation", "", 2),
		]
	mode = bpy.props.EnumProperty(items=items, name="Mode", default='IMAGE')
	thread = bpy.props.IntProperty(name="Threads", default=2, min=1, max=16, soft_min=1, soft_max=16)
	
	def execute(self, context):
		blend_path = bpy.data.filepath
		if (not blend_path):
			self.report(type={'ERROR'}, message="blend not saved")
			return {'CANCELLED'}
		if (self.mode == 'IMAGE'):
			subprocess.Popen([sys.argv[0], '-b', blend_path, '-f', str(context.scene.frame_current), '-t', str(self.thread)])
		elif (self.mode == 'ANIME'):
			subprocess.Popen([sys.argv[0], '-b', blend_path, '-a', '-t', str(self.thread)])
		if (self.is_quit):
			bpy.ops.wm.quit_blender()
		return {'FINISHED'}
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

class SetRenderResolutionPercentage(bpy.types.Operator):
	bl_idname = "render.set_render_resolution_percentage"
	bl_label = "Set Resolution"
	bl_description = "Percent of the size of the resolution"
	bl_options = {'REGISTER', 'UNDO'}
	
	size = bpy.props.IntProperty(name="Rendering size (%)", default=100, min=1, max=1000, soft_min=1, soft_max=1000, step=1)
	
	def execute(self, context):
		context.scene.render.resolution_percentage = self.size
		return {'FINISHED'}

class SetRenderSlot(bpy.types.Operator):
	bl_idname = "render.set_render_slot"
	bl_label = "Set render slot"
	bl_description = "I set the slot where you want to save the rendering result"
	bl_options = {'REGISTER', 'UNDO'}
	
	slot = bpy.props.IntProperty(name="Slot", default=1, min=0, max=100, soft_min=0, soft_max=100, step=1)
	
	def execute(self, context):
		bpy.data.images["Render Result"].render_slots.active_index = self.slot
		return {'FINISHED'}

class ToggleThreadsMode(bpy.types.Operator):
	bl_idname = "render.toggle_threads_mode"
	bl_label = "Switch the number of threads"
	bl_description = "I will switch the number of threads in the CPU to be used for rendering"
	bl_options = {'REGISTER', 'UNDO'}

	threads = bpy.props.IntProperty(name="Number of threads", default=1, min=1, max=16, soft_min=1, soft_max=16, step=1)
	
	def execute(self, context):
		if (context.scene.render.threads_mode == 'AUTO'):
			context.scene.render.threads_mode = 'FIXED'
			context.scene.render.threads = self.threads
		else:
			context.scene.render.threads_mode = 'AUTO'
		return {'FINISHED'}
	def invoke(self, context, event):
		if (context.scene.render.threads_mode == 'AUTO'):
			self.threads = context.scene.render.threads
			return context.window_manager.invoke_props_dialog(self)
		else:
			return self.execute(context)

class SetAllSubsurfRenderLevels(bpy.types.Operator):
	bl_idname = "render.set_all_subsurf_render_levels"
	bl_label = "Set All Levels Subsurf"
	bl_description = "Level of Subsurf to apply when rendering"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		('ABSOLUTE', "Absolute value", "", 1),
		('RELATIVE', "Relative value", "", 2),
		]
	mode = bpy.props.EnumProperty(items=items, name="Mode")
	levels = bpy.props.IntProperty(name="Level", default=2, min=-20, max=20, soft_min=-20, soft_max=20, step=1)
	
	def execute(self, context):
		for obj in bpy.data.objects:
			if (obj.type != 'MESH' and obj.type != 'CURVE'):
				continue
			for mod in obj.modifiers:
				if (mod.type == 'SUBSURF'):
					if (self.mode == 'ABSOLUTE'):
						mod.render_levels = self.levels
					elif (self.mode == 'RELATIVE'):
						mod.render_levels += self.levels
					else:
						self.report(type={'ERROR'}, message="Setting value is invalid")
						return {'CANCELLED'}
		for area in context.screen.areas:
			area.tag_redraw()
		return {'FINISHED'}

class SyncAllSubsurfRenderLevels(bpy.types.Operator):
	bl_idname = "render.sync_all_subsurf_render_levels"
	bl_label = "Sync Subsurf Render Levels"
	bl_description = "sync_all_subsurf_render_levels"
	bl_options = {'REGISTER', 'UNDO'}
	
	level_offset = bpy.props.IntProperty(name="Sync Levels", default=0, min=-20, max=20, soft_min=-20, soft_max=20, step=1)
	
	def execute(self, context):
		for obj in bpy.data.objects:
			if (obj.type != 'MESH'):
				continue
			for mod in obj.modifiers:
				if (mod.type == 'SUBSURF'):
					mod.render_levels = mod.levels + self.level_offset
		for area in context.screen.areas:
			area.tag_redraw()
		return {'FINISHED'}
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

################
# サブメニュー #
################

class RenderResolutionPercentageMenu(bpy.types.Menu):
	bl_idname = "INFO_MT_render_resolution_percentage"
	bl_label = "Rendering size (%)"
	bl_description = "Setting is set to either rendered in what percent of the size of the resolution"
	
	def draw(self, context):
		x = bpy.context.scene.render.resolution_x
		y = bpy.context.scene.render.resolution_y
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="10% ("+str(int(x*0.1))+"x"+str(int(y*0.1))+")", icon="PLUGIN").size = 10
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="20% ("+str(int(x*0.2))+"x"+str(int(y*0.2))+")", icon="PLUGIN").size = 20
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="30% ("+str(int(x*0.3))+"x"+str(int(y*0.3))+")", icon="PLUGIN").size = 30
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="40% ("+str(int(x*0.4))+"x"+str(int(y*0.4))+")", icon="PLUGIN").size = 40
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="50% ("+str(int(x*0.5))+"x"+str(int(y*0.5))+")", icon="PLUGIN").size = 50
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="60% ("+str(int(x*0.6))+"x"+str(int(y*0.6))+")", icon="PLUGIN").size = 60
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="70% ("+str(int(x*0.7))+"x"+str(int(y*0.7))+")", icon="PLUGIN").size = 70
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="80% ("+str(int(x*0.8))+"x"+str(int(y*0.8))+")", icon="PLUGIN").size = 80
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="90% ("+str(int(x*0.9))+"x"+str(int(y*0.9))+")", icon="PLUGIN").size = 90
		self.layout.separator()
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="100% ("+str(int(x))+"x"+str(int(y))+")", icon="PLUGIN").size = 100
		self.layout.separator()
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="150% ("+str(int(x*1.5))+"x"+str(int(y*1.5))+")", icon="PLUGIN").size = 150
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="200% ("+str(int(x*2.0))+"x"+str(int(y*2.0))+")", icon="PLUGIN").size = 200
		self.layout.operator(SetRenderResolutionPercentage.bl_idname, text="300% ("+str(int(x*3.0))+"x"+str(int(y*3.0))+")", icon="PLUGIN").size = 300

class SimplifyRenderMenu(bpy.types.Menu):
	bl_idname = "INFO_MT_render_simplify"
	bl_label = "Simplify Render"
	bl_description = "I simplified set of rendering"
	
	def draw(self, context):
		self.layout.prop(context.scene.render, "use_simplify", icon="PLUGIN")
		self.layout.separator()
		self.layout.prop(context.scene.render, "simplify_subdivision", icon="PLUGIN")
		self.layout.prop(context.scene.render, "simplify_shadow_samples", icon="PLUGIN")
		self.layout.prop(context.scene.render, "simplify_child_particles", icon="PLUGIN")
		self.layout.prop(context.scene.render, "simplify_ao_sss", icon="PLUGIN")
		self.layout.prop(context.scene.render, "use_simplify_triangulate", icon="PLUGIN")

class SlotsRenderMenu(bpy.types.Menu):
	bl_idname = "INFO_MT_render_slots"
	bl_label = "Render Slot"
	bl_description = "I will change the slot where you want to save the rendering result"
	
	def draw(self, context):
		for i in range(len(bpy.data.images["Render Result"].render_slots)):
			self.layout.operator(SetRenderSlot.bl_idname, text="スロット"+str(i+1)).slot = i

class ShadeingMenu(bpy.types.Menu):
	bl_idname = "INFO_MT_render_shadeing"
	bl_label = "Use shading"
	bl_description = "I make the shading on / off"
	
	def draw(self, context):
		self.layout.prop(context.scene.render, 'use_textures', icon="PLUGIN")
		self.layout.prop(context.scene.render, 'use_shadows', icon="PLUGIN")
		self.layout.prop(context.scene.render, 'use_sss', icon="PLUGIN")
		self.layout.prop(context.scene.render, 'use_envmaps', icon="PLUGIN")
		self.layout.prop(context.scene.render, 'use_raytrace', icon="PLUGIN")

class SubsurfMenu(bpy.types.Menu):
	bl_idname = "INFO_MT_render_subsurf"
	bl_label = "Subsurf Level All"
	bl_description = "Subsurf subdivision level of all objects"
	
	def draw(self, context):
		operator = self.layout.operator(SetAllSubsurfRenderLevels.bl_idname, text="Subdivision + 1", icon="MOD_SUBSURF")
		operator.mode = 'RELATIVE'
		operator.levels = 1
		operator = self.layout.operator(SetAllSubsurfRenderLevels.bl_idname, text="Subdivision - 1", icon="MOD_SUBSURF")
		operator.mode = 'RELATIVE'
		operator.levels = -1
		self.layout.separator()
		operator = self.layout.operator(SetAllSubsurfRenderLevels.bl_idname, text="Subdivision = 0", icon="MOD_SUBSURF")
		operator.mode = 'ABSOLUTE'
		operator.levels = 0
		operator = self.layout.operator(SetAllSubsurfRenderLevels.bl_idname, text="Subdivision = 1", icon="MOD_SUBSURF")
		operator.mode = 'ABSOLUTE'
		operator.levels = 1
		operator = self.layout.operator(SetAllSubsurfRenderLevels.bl_idname, text="Subdivision = 2", icon="MOD_SUBSURF")
		operator.mode = 'ABSOLUTE'
		operator.levels = 2
		operator = self.layout.operator(SetAllSubsurfRenderLevels.bl_idname, text="Subdivision = 3", icon="MOD_SUBSURF")
		operator.mode = 'ABSOLUTE'
		operator.levels = 3
		self.layout.separator()
		self.layout.operator(SyncAllSubsurfRenderLevels.bl_idname, text="Sync Subsurf Render Levels", icon="MOD_SUBSURF")

class RenderToolsMenu(bpy.types.Operator):
	bl_idname = "render.render_tools"
	bl_label = "Render Menu"
	bl_description = "Pop up Render Settings"
	
	def draw(self, context):
		self.layout.separator()
		self.layout.operator(RenderBackground.bl_idname, icon="COLOR_RED")
		self.layout.separator()
		self.layout.prop(context.scene.render, 'resolution_x', text="Resolution X", icon="CAMERA_DATA")
		self.layout.prop(context.scene.render, 'resolution_y', text="Resolution Y", icon="CAMERA_DATA")
		self.layout.menu(RenderResolutionPercentageMenu.bl_idname, text="Render Resolution (currently:"+str(context.scene.render.resolution_percentage)+"%)", icon="CAMERA_DATA")
		if (bpy.data.images.find("Render Result") != -1):
			self.layout.menu(SlotsRenderMenu.bl_idname, text="Set Render Slot (Currently:"+str(bpy.data.images["Render Result"].render_slots.active_index+1)+")", icon="RENDERLAYERS")
		self.layout.prop_menu_enum(context.scene.render.image_settings, 'file_format', text="File Format", icon="PACKAGE")
		self.layout.separator()
		self.layout.prop(context.scene, 'frame_start', text="Start Frame", icon="COLOR_GREEN")
		self.layout.prop(context.scene, 'frame_end', text="End Frame", icon="COLOR_RED")
		self.layout.prop(context.scene, 'frame_step', text="Frame Step", icon="ALIGN")
		self.layout.prop(context.scene.render, 'fps', text="FPS", icon="AUTO")
		self.layout.separator()
		self.layout.prop(context.scene.render, 'use_antialiasing', text="Anti-aliasing use", icon="PLUGIN")
		self.layout.prop(context.scene.world.light_settings, 'use_ambient_occlusion', text="Use the AO", icon="PLUGIN")
		self.layout.prop(context.scene.render, 'use_freestyle', text="FreeStyle Use", icon="PLUGIN")
		self.layout.menu(ShadeingMenu.bl_idname, icon="TEXTURE_SHADED")
		self.layout.separator()
		text = ToggleThreadsMode.bl_label
		if (context.scene.render.threads_mode == 'AUTO'):
			text = text + " (Current auto-sensing)"
		else:
			text = text + " Current value：" + str(context.scene.render.threads) + ")"
		self.layout.operator(ToggleThreadsMode.bl_idname, text=text, icon="PLUGIN")
		self.layout.menu(SubsurfMenu.bl_idname, icon="MOD_SUBSURF")
		self.layout.prop_menu_enum(context.scene.render, 'antialiasing_samples', text="The number of anti-aliasing sample", icon="ANTIALIASED")
		self.layout.prop(context.scene.world.light_settings, 'samples', text="AO number of samples", icon="WORLD")
		self.layout.separator()
		self.layout.menu(SimplifyRenderMenu.bl_idname, icon="RENDER_RESULT")
	def execute(self, context):
		return {'FINISHED'}
	def invoke(self, context, event):
		return context.window_manager.invoke_popup(self, width = 350)
################
# メニュー追加 #
################

# メニューのオン/オフの判定
def IsMenuEnable(self_id):
	for id in bpy.context.user_preferences.addons["Addon_Factory"].preferences.disabled_menu.split(','):
		if (id == self_id):
			return False
	else:
		return True

# メニューを登録する関数
def menu(self, context):

	self.layout.separator()
	self.layout.operator(RenderToolsMenu.bl_idname, icon="RENDER_RESULT")

