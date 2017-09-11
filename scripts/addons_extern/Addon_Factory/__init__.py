# Initially this file is loaded when you load the add-on.

import os, csv, codecs

### Addon_Factory Imports ### meta-androcto ###


from .INFO_MT_info_MA import INFO_MT_file_external_data
from .INFO_MT_info_MA import INFO_MT_help
from .INFO_MT_info_MA import INFO_MT_window
from .IMAGE_MT_image_MA import IMAGE_MT_image
from .IMAGE_MT_image_MA import IMAGE_MT_select
from .IMAGE_MT_image_MA import IMAGE_MT_uvs
from .IMAGE_MT_image_MA import IMAGE_MT_view


# Blender Addon Information
bl_info = {
	"name" : "Addon_Factory",
	"author" : "Saidenka, meta-androcto, various",
	"version" : (0, 1, 1),
	"blender" : (2, 7, 5),
	"location" : "Everywhere",
	"description" : "Extended Menu's",
	"warning" : "",
	"wiki_url" : "http://github.com/saidenka/Blender-Scramble-Addon",
	"tracker_url" : "http://github.com/saidenka/Blender-Scramble-Addon/issues",
	"category" : "Addon Factory"
}


if "bpy" in locals():
	import importlib

	importlib.reload(BONE_PT_context_bone)
	importlib.reload(BONE_PT_display)
	importlib.reload(BONE_PT_inverse_kinematics)
	importlib.reload(BONE_PT_transform)
	importlib.reload(DATA_PT_bone_groups)
	importlib.reload(DATA_PT_geometry_curve)
	importlib.reload(DATA_PT_pose_library)
	importlib.reload(DATA_PT_skeleton)
	importlib.reload(DATA_PT_uv_texture)
	importlib.reload(DATA_PT_vertex_colors)
	importlib.reload(DOPESHEET_MT_key)
	importlib.reload(MESH_MT_shape_key_specials)
	importlib.reload(MESH_MT_vertex_group_specials)
	importlib.reload(NODE_MT_node)
	importlib.reload(NODE_MT_view)
	importlib.reload(OBJECT_PT_display)
	importlib.reload(OBJECT_PT_transform)
	importlib.reload(PHYSICS_PT_rigid_body)
	importlib.reload(PROPERTIES_HT_header)
	importlib.reload(RENDER_PT_bake)
	importlib.reload(RENDER_PT_render)
	importlib.reload(SCENE_PT_rigid_body_world)
	importlib.reload(TEXT_MT_text)
	importlib.reload(TEXTURE_MT_specials)
	importlib.reload(TEXTURE_PT_context_texture)
	importlib.reload(TEXTURE_PT_image)
	importlib.reload(TEXTURE_PT_mapping)
	importlib.reload(USERPREF_HT_header)
	importlib.reload(USERPREF_PT_file)
	importlib.reload(VIEW3D_MT_bone_options_toggle)
	importlib.reload(VIEW3D_MT_edit_armature)
	importlib.reload(VIEW3D_MT_paint_weight)
	importlib.reload(VIEW3D_MT_pose_constraints)
	importlib.reload(VIEW3D_MT_pose_showhide)
	importlib.reload(VIEW3D_MT_select_edit_armature)
	importlib.reload(VIEW3D_MT_select_pose)
	importlib.reload(VIEW3D_MT_uv_map)
	importlib.reload(VIEW3D_PT_imapaint_tools_missing)
	importlib.reload(VIEW3D_PT_slots_projectpaint)
	importlib.reload(VIEW3D_PT_tools_imagepaint_external)
	importlib.reload(VIEW3D_PT_transform_orientations)
	importlib.reload(undisplay_commands)
	#importlib.reload(***)

else:
	from . import BONE_PT_context_bone
	from . import BONE_PT_display
	from . import BONE_PT_inverse_kinematics
	from . import BONE_PT_transform
	from . import DATA_PT_bone_groups
	from . import DATA_PT_geometry_curve
	from . import DATA_PT_pose_library
	from . import DATA_PT_skeleton
	from . import DATA_PT_uv_texture
	from . import DATA_PT_vertex_colors
	from . import DOPESHEET_MT_key
	from . import MESH_MT_shape_key_specials
	from . import MESH_MT_vertex_group_specials
	from . import NODE_MT_node
	from . import NODE_MT_view
	from . import OBJECT_PT_display
	from . import OBJECT_PT_transform
	from . import PHYSICS_PT_rigid_body
	from . import PROPERTIES_HT_header
	from . import RENDER_PT_bake
	from . import RENDER_PT_render
	from . import SCENE_PT_rigid_body_world
	from . import TEXT_MT_text
	from . import TEXTURE_MT_specials
	from . import TEXTURE_PT_context_texture
	from . import TEXTURE_PT_image
	from . import TEXTURE_PT_mapping
	from . import USERPREF_HT_header
	from . import USERPREF_PT_file
	from . import VIEW3D_MT_bone_options_toggle
	from . import VIEW3D_MT_edit_armature
	from . import VIEW3D_MT_paint_weight
	from . import VIEW3D_MT_pose_constraints
	from . import VIEW3D_MT_pose_showhide
	from . import VIEW3D_MT_select_edit_armature
	from . import VIEW3D_MT_select_pose
	from . import VIEW3D_MT_uv_map
	from . import VIEW3D_PT_imapaint_tools_missing
	from . import VIEW3D_PT_slots_projectpaint
	from . import VIEW3D_PT_tools_imagepaint_external
	from . import VIEW3D_PT_transform_orientations
	from . import undisplay_commands

import bpy

### Set The International Fonts ### meta-androcto ###
bpy.context.user_preferences.system.use_international_fonts = True
bpy.context.user_preferences.system.language = 'en_US'
bpy.context.user_preferences.system.use_translate_interface = True
bpy.context.user_preferences.system.use_translate_tooltips = True

# Addons Preferences
class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	disabled_menu = bpy.props.StringProperty(name="Disable Menu", default="")
	use_disabled_menu = bpy.props.BoolProperty(name="Toggle Disable Menu", default=False)
	view_savedata = bpy.props.StringProperty(name="View Saved Data", default="")
	key_config_xml_path = bpy.props.StringProperty(name="XML Key Path Config", default="BlenderKeyConfig.xml")

	image_editor_path_1 = bpy.props.StringProperty(name="Path 1 of image-editing software", default="", subtype='FILE_PATH')
	image_editor_path_2 = bpy.props.StringProperty(name="Path 2 of the image-editing software", default="", subtype='FILE_PATH')
	image_editor_path_3 = bpy.props.StringProperty(name="Path 3 image editing software", default="", subtype='FILE_PATH')

	text_editor_path_1 = bpy.props.StringProperty(name="Path 1 text editing software", default="", subtype='FILE_PATH')
	text_editor_path_2 = bpy.props.StringProperty(name="Pass 2 of text editing software", default="", subtype='FILE_PATH')
	text_editor_path_3 = bpy.props.StringProperty(name="Path 3 text editing software", default="", subtype='FILE_PATH')
	
	def draw(self, context):
		layout = self.layout
		layout.label(text="----Addon Factory----")
		layout.label(text="Based on Scramble Addon by Saidenka")
		layout.label(text="Additional menu Items across the ui")

		layout.label(text="Show/hide option for extra ui elements")
		layout.label(text="Toggle Disable menu adds button to ui elements to turn on or off menu's")
		layout.label(text="Options are saveable using Save User Settings")
		layout.prop(self, 'disabled_menu')
		layout.prop(self, 'use_disabled_menu')
		layout.prop(self, 'view_savedata')
		layout.prop(self, 'key_config_xml_path')

		box = layout.box()
		box.label(text="Set Image Editor Paths")	
		box.prop(self, 'image_editor_path_1')
		box.prop(self, 'image_editor_path_2')
		box.prop(self, 'image_editor_path_3')
		box = layout.box()
		box.label(text="Set Text Editor Paths")
		box.prop(self, 'text_editor_path_1')
		box.prop(self, 'text_editor_path_2')
		box.prop(self, 'text_editor_path_3')

# Toggle
class ToggleMenuEnable(bpy.types.Operator):
	bl_idname = "wm.toggle_menu_enable"
	bl_label = "Menu Enable Toggle"
	bl_description = "Scramble on/off"
	bl_options = {'REGISTER', 'UNDO'}
	
	id = bpy.props.StringProperty()
	
	def execute(self, context):
		recovery = ""
		is_on = False
		for id in context.user_preferences.addons["Addon_Factory"].preferences.disabled_menu.split(','):
			if (id == ""):
				continue
			if (id == self.id):
				is_on = True
			else:
				recovery = recovery + id + ","
		if (not is_on):
			recovery = recovery + self.id + ","
		if (recovery != ""):
			if (recovery[-1] == ","):
				recovery = recovery[:-1]
		context.user_preferences.addons["Addon_Factory"].preferences.disabled_menu = recovery
		for area in context.screen.areas:
			area.tag_redraw()
		return {'FINISHED'}

# translation
def GetTranslationDict():
	dict = {}
	path = os.path.join(os.path.dirname(__file__), "TranslationDictionary.csv")
	with codecs.open(path, 'r', 'utf-8') as f:
		reader = csv.reader(f)
		dict['ja_JP'] = {}
		for row in reader:
			for context in bpy.app.translations.contexts:
				dict['ja_JP'][(context, row[1])] = row[0]
		"""
		for lang in bpy.app.translations.locales:
			if (lang == 'ja_JP'):
				continue
			dict[lang] = {}
			for row in reader:
				for context in bpy.app.translations.contexts:
					dict[lang][(context, row[0])] = row[1]
		"""
	return dict

# register
def register():
	bpy.utils.register_module(__name__)
	
	translation_dict = GetTranslationDict()
	bpy.app.translations.register(__name__, translation_dict)

### Addon_Factory Folder Register ### meta-androcto ###

	bpy.types.IMAGE_MT_image.append(IMAGE_MT_image.menu)
	bpy.types.IMAGE_MT_select.append(IMAGE_MT_select.menu)
	bpy.types.IMAGE_MT_view.append(IMAGE_MT_view.menu)
	bpy.types.IMAGE_MT_uvs.append(IMAGE_MT_uvs.menu)
	bpy.types.INFO_MT_file_external_data.append(INFO_MT_file_external_data.menu)
	bpy.types.INFO_MT_help.append(INFO_MT_help.menu)
	bpy.types.INFO_MT_window.append(INFO_MT_window.menu)


### Scramblen Addon Register ### Saidenka ###

	bpy.types.BONE_PT_context_bone.append(BONE_PT_context_bone.menu)
	bpy.types.BONE_PT_display.append(BONE_PT_display.menu)
	bpy.types.BONE_PT_inverse_kinematics.append(BONE_PT_inverse_kinematics.menu)
	bpy.types.BONE_PT_transform.append(BONE_PT_transform.menu)
	bpy.types.DATA_PT_bone_groups.append(DATA_PT_bone_groups.menu)
	bpy.types.DATA_PT_geometry_curve.append(DATA_PT_geometry_curve.menu)
	bpy.types.DATA_PT_pose_library.append(DATA_PT_pose_library.menu)
	bpy.types.DATA_PT_skeleton.append(DATA_PT_skeleton.menu)
	bpy.types.DATA_PT_uv_texture.append(DATA_PT_uv_texture.menu)
	bpy.types.DATA_PT_vertex_colors.append(DATA_PT_vertex_colors.menu)

	bpy.types.DOPESHEET_MT_key.append(DOPESHEET_MT_key.menu)

	bpy.types.MESH_MT_shape_key_specials.append(MESH_MT_shape_key_specials.menu)
	bpy.types.MESH_MT_vertex_group_specials.append(MESH_MT_vertex_group_specials.menu)

	bpy.types.NODE_MT_node.append(NODE_MT_node.menu)
	bpy.types.NODE_MT_view.append(NODE_MT_view.menu)

	bpy.types.VIEW3D_PT_view3d_display.append(OBJECT_PT_display.menu)
	bpy.types.OBJECT_PT_transform.append(OBJECT_PT_transform.menu)

	bpy.types.PHYSICS_PT_rigid_body.append(PHYSICS_PT_rigid_body.menu)

	bpy.types.PROPERTIES_HT_header.append(PROPERTIES_HT_header.menu)

	bpy.types.RENDER_PT_bake.append(RENDER_PT_bake.menu)
	bpy.types.RENDER_PT_render.append(RENDER_PT_render.menu)

	bpy.types.SCENE_PT_rigid_body_world.append(SCENE_PT_rigid_body_world.menu)

	bpy.types.TEXT_MT_text.append(TEXT_MT_text.menu)

	bpy.types.TEXTURE_MT_specials.append(TEXTURE_MT_specials.menu)
	bpy.types.TEXTURE_PT_context_texture.append(TEXTURE_PT_context_texture.menu)
	bpy.types.TEXTURE_PT_image.append(TEXTURE_PT_image.menu)
	bpy.types.TEXTURE_PT_mapping.append(TEXTURE_PT_mapping.menu)

	bpy.types.USERPREF_HT_header.append(USERPREF_HT_header.menu)
	bpy.types.USERPREF_PT_file.append(USERPREF_PT_file.menu)

	bpy.types.VIEW3D_MT_bone_options_toggle.append(VIEW3D_MT_bone_options_toggle.menu)
	bpy.types.VIEW3D_MT_edit_armature.append(VIEW3D_MT_edit_armature.menu)
	bpy.types.VIEW3D_MT_paint_weight.append(VIEW3D_MT_paint_weight.menu)
	bpy.types.VIEW3D_MT_pose_constraints.append(VIEW3D_MT_pose_constraints.menu)
	bpy.types.VIEW3D_MT_pose_showhide.append(VIEW3D_MT_pose_showhide.menu)
	bpy.types.VIEW3D_MT_select_edit_armature.append(VIEW3D_MT_select_edit_armature.menu)
	bpy.types.VIEW3D_MT_select_pose.append(VIEW3D_MT_select_pose.menu)
	bpy.types.VIEW3D_MT_uv_map.append(VIEW3D_MT_uv_map.menu)

	bpy.types.VIEW3D_PT_imapaint_tools_missing.append(VIEW3D_PT_imapaint_tools_missing.menu)
	bpy.types.VIEW3D_PT_slots_projectpaint.append(VIEW3D_PT_slots_projectpaint.menu)
	bpy.types.VIEW3D_PT_tools_imagepaint_external.append(VIEW3D_PT_tools_imagepaint_external.menu)
	bpy.types.VIEW3D_PT_transform_orientations.append(VIEW3D_PT_transform_orientations.menu)

	#bpy.types.***.append(***.menu)

	
# unrigister
def unregister():

	
	bpy.app.translations.unregister(__name__)

### Addon_Factory unregister ### meta-androcto ###

	bpy.types.IMAGE_MT_image.remove(IMAGE_MT_image.menu)
	bpy.types.IMAGE_MT_select.remove(IMAGE_MT_select.menu)
	bpy.types.IMAGE_MT_view.remove(IMAGE_MT_view.menu)
	bpy.types.IMAGE_MT_uvs.remove(IMAGE_MT_uvs.menu)

	bpy.types.INFO_MT_file_external_data.remove(INFO_MT_file_external_data.menu)
	bpy.types.INFO_MT_help.remove(INFO_MT_help.menu)
	bpy.types.INFO_MT_window.remove(INFO_MT_window.menu)

### Scramble Addon unregister ### Saidenka ###	

	bpy.types.BONE_PT_context_bone.remove(BONE_PT_context_bone.menu)
	bpy.types.BONE_PT_display.remove(BONE_PT_display.menu)
	bpy.types.BONE_PT_inverse_kinematics.remove(BONE_PT_inverse_kinematics.menu)
	bpy.types.BONE_PT_transform.remove(BONE_PT_transform.menu)

	bpy.types.DATA_PT_bone_groups.remove(DATA_PT_bone_groups.menu)
	bpy.types.DATA_PT_geometry_curve.remove(DATA_PT_geometry_curve.menu)
	bpy.types.DATA_PT_pose_library.remove(DATA_PT_pose_library.menu)
	bpy.types.DATA_PT_skeleton.remove(DATA_PT_skeleton.menu)
	bpy.types.DATA_PT_uv_texture.remove(DATA_PT_uv_texture.menu)
	bpy.types.DATA_PT_vertex_colors.remove(DATA_PT_vertex_colors.menu)

	bpy.types.DOPESHEET_MT_key.remove(DOPESHEET_MT_key.menu)

	bpy.types.MESH_MT_shape_key_specials.remove(MESH_MT_shape_key_specials.menu)
	bpy.types.MESH_MT_vertex_group_specials.remove(MESH_MT_vertex_group_specials.menu)

	bpy.types.NODE_MT_node.remove(NODE_MT_node.menu)
	bpy.types.NODE_MT_view.remove(NODE_MT_view.menu)

	bpy.types.OBJECT_PT_display.remove(OBJECT_PT_display.menu)
	bpy.types.OBJECT_PT_transform.remove(OBJECT_PT_transform.menu)

	bpy.types.PHYSICS_PT_rigid_body.remove(PHYSICS_PT_rigid_body.menu)

	bpy.types.PROPERTIES_HT_header.remove(PROPERTIES_HT_header.menu)

	bpy.types.RENDER_PT_bake.remove(RENDER_PT_bake.menu)
	bpy.types.RENDER_PT_render.remove(RENDER_PT_render.menu)

	bpy.types.SCENE_PT_rigid_body_world.remove(SCENE_PT_rigid_body_world.menu)

	bpy.types.TEXT_MT_text.remove(TEXT_MT_text.menu)

	bpy.types.TEXTURE_MT_specials.remove(TEXTURE_MT_specials.menu)
	bpy.types.TEXTURE_PT_context_texture.remove(TEXTURE_PT_context_texture.menu)
	bpy.types.TEXTURE_PT_image.remove(TEXTURE_PT_image.menu)
	bpy.types.TEXTURE_PT_mapping.remove(TEXTURE_PT_mapping.menu)

	bpy.types.USERPREF_HT_header.remove(USERPREF_HT_header.menu)
	bpy.types.USERPREF_PT_file.remove(USERPREF_PT_file.menu)

	bpy.types.VIEW3D_MT_bone_options_toggle.remove(VIEW3D_MT_bone_options_toggle.menu)
	bpy.types.VIEW3D_MT_edit_armature.remove(VIEW3D_MT_edit_armature.menu)
	bpy.types.VIEW3D_MT_paint_weight.remove(VIEW3D_MT_paint_weight.menu)
	bpy.types.VIEW3D_MT_pose_constraints.remove(VIEW3D_MT_pose_constraints.menu)
	bpy.types.VIEW3D_MT_pose_showhide.remove(VIEW3D_MT_pose_showhide.menu)
	bpy.types.VIEW3D_MT_select_edit_armature.remove(VIEW3D_MT_select_edit_armature.menu)
	bpy.types.VIEW3D_MT_select_pose.remove(VIEW3D_MT_select_pose.menu)
	bpy.types.VIEW3D_MT_uv_map.remove(VIEW3D_MT_uv_map.menu)

	bpy.types.VIEW3D_PT_imapaint_tools_missing.remove(VIEW3D_PT_imapaint_tools_missing.menu)
	bpy.types.VIEW3D_PT_slots_projectpaint.remove(VIEW3D_PT_slots_projectpaint.menu)
	bpy.types.VIEW3D_PT_tools_imagepaint_external.remove(VIEW3D_PT_tools_imagepaint_external.menu)
	bpy.types.VIEW3D_PT_transform_orientations.remove(VIEW3D_PT_transform_orientations.menu)

	#bpy.types.***.remove(***.menu)


	bpy.utils.unregister_module(__name__)
# メイン関数
if __name__ == "__main__":
	register()
