# <pep8 compliant>
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Khalibloo Panel",
    "version": (1, 0),
    "author": "Khalifa Lame",
    "blender": (2, 78, 0),
    "description": "A huge collection of tools for batch operations and handling of repetitive tasks. Also includes tools for setting up DAZ Genesis and Genesis 2 characters and clothes.",
    "location": "3D Viewport > Properties(N) Panel > Khalibloo",
    "category": "Tools"}

import bpy
from . import utils
from . import custom_ops
from . import genesis_tools

#============================================================================
# DRAW PANEL
#============================================================================

class KhaliblooPanel(bpy.types.Panel):
    """Creates a Panel in the properties context of the 3D viewport"""
    bl_label = "Khalibloo"
    bl_idname = "khalibloo_panel_3d"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        platform = bpy.context.scene.khalibloo_platform
        genesis_subclass = bpy.context.scene.khalibloo_genesis_platform_subclass
        genesis2_subclass = bpy.context.scene.khalibloo_genesis2_platform_subclass
        genesis3_subclass = bpy.context.scene.khalibloo_genesis3_platform_subclass
        general_subclass = bpy.context.scene.khalibloo_general_platform_subclass
        mod_filter_mode = bpy.context.scene.khalibloo_modifier_filter_mode


        #Platforn type
        layout.prop(scene, "khalibloo_platform", text="", expand=False)

#---------------------------------------------------------------------------------
        #GENERAL TOOLS
        if (platform == 'GENERAL'):
            #Category type
            layout.prop(scene, "khalibloo_general_platform_subclass", expand=True)
            layout.separator()


            #OBJECT DATA TAB
            if (general_subclass == 'OBJECT DATA'):
                #layout.separator()
                #layout.label(text="Apply: ")
                #row = layout.row(align=True)
                #row.operator("object.khalibloo_apply_location", text="Location")
                #row.operator("object.khalibloo_apply_rotation", text="Rotation")
                #row.operator("object.khalibloo_apply_scale", text="Scale")
                #layout.operator("object.khalibloo_apply_visual_transform", text="Visual Transform")

                layout.separator()
                layout.operator("object.khalibloo_assign_obj_indices", text="Assign Pass Indices")

                layout.separator()
                row = layout.row(align=True)
                row.operator("object.khalibloo_unhide_select", text="", icon='RESTRICT_SELECT_OFF')
                row.operator("object.khalibloo_hide_select", text="", icon='RESTRICT_SELECT_ON')
                row.operator("object.khalibloo_unhide_render", text="", icon='RESTRICT_RENDER_OFF')
                row.operator("object.khalibloo_hide_render", text="", icon='RESTRICT_RENDER_ON')

                layout.separator()
                layout.label(text="Multi Edit: ")
                row = layout.row(align=True)
                row.operator("object.khalibloo_multiedit_start", text="Start")
                row.operator("object.khalibloo_multiedit_end", text="End")


            #MESH DATA TAB
            if (general_subclass == 'MESH DATA'):
                layout.separator()
                layout.operator("object.khalibloo_name_object_data")
                layout.operator("object.khalibloo_copy_all_shape_keys")
                layout.operator("object.khalibloo_shrinkwrap_update")
                layout.separator()
                layout.label(text="Morph data:")
                layout.operator("object.khalibloo_bind_mesh")
                layout.operator("object.khalibloo_update_bound_mesh")
                #layout.prop(scene, "khalibloo_spread_harden_vgroups")
                #layout.operator("object.khalibloo_harden_weights")

            #MATERIALS TAB
            elif (general_subclass == 'MATERIALS'):
                layout.separator()
                layout.operator("object.khalibloo_setup_imported_materials")
                layout.operator("object.khalibloo_toonify")
                layout.operator("object.khalibloo_receive_transparent_shadows")
                layout.operator("object.khalibloo_materials_remove", text='Remove Materials', icon='X')
                layout.operator("object.khalibloo_assign_mat_indices", text="Assign Pass Indices")

                layout.separator()
                row = layout.row(align=True)
                row.label(text="Textures:", icon='TEXTURE')
                row.operator("object.khalibloo_textures_on", text='', icon='RESTRICT_VIEW_OFF')
                row.operator("object.khalibloo_textures_off", text='', icon='RESTRICT_VIEW_ON')

            #MODIFIERS TAB
            elif (general_subclass == 'MODIFIERS'):
                layout.separator()
                layout.prop(scene, "khalibloo_modifier_type", expand=False)
                layout.operator("object.khalibloo_add_modifier", text='Add Modifier', icon='ZOOMIN')

                layout.separator()
                layout.prop(scene, "khalibloo_modifier_filter_mode", expand=True)

                row = layout.row(align=True)
                row.operator("object.khalibloo_modifiers_realtime_on", text='', icon='RESTRICT_VIEW_OFF')
                row.operator("object.khalibloo_modifiers_realtime_off", text='', icon='RESTRICT_VIEW_ON')
                row.operator("object.khalibloo_modifiers_render_on", text='', icon='RESTRICT_RENDER_OFF')
                row.operator("object.khalibloo_modifiers_render_off", text='', icon='RESTRICT_RENDER_ON')
                #row.operator("object.khalibloo_modifiers_editmode_on", text='', icon='EDITMODE_HLT')
                #row.operator("object.khalibloo_modifiers_editmode_off", text='', icon='VIEW3D')
                row.operator("object.khalibloo_modifiers_apply", text='Apply')
                row.operator("object.khalibloo_modifiers_remove", text='', icon='X')

            #ARMATURES TAB
            elif (general_subclass == 'ARMATURES'):
                layout.separator()
                layout.operator("object.khalibloo_metarig_gamerig_hookup")
                layout.operator("object.khalibloo_rigify_neck_fix")

            #CONSTRAINTS TAB
            elif (general_subclass == 'CONSTRAINTS'):
                layout.separator()
                row = layout.row(align=True)
                row.operator("object.khalibloo_constraints_unmute", text='', icon='RESTRICT_VIEW_OFF')
                row.operator("object.khalibloo_constraints_mute", text='', icon='RESTRICT_VIEW_ON')
                row.operator("object.khalibloo_constraints_remove", text='', icon='X')

                layout.separator()

                row = layout.row(align=True)
                row.label(text="Bone Constraints:", icon='CONSTRAINT_BONE')
                row = layout.row(align=True)
                row.operator("object.khalibloo_bone_constraints_unmute", text='', icon='RESTRICT_VIEW_OFF')
                row.operator("object.khalibloo_bone_constraints_mute", text='', icon='RESTRICT_VIEW_ON')
                row.operator("object.khalibloo_bone_constraints_remove", text='', icon='X')

            #CUSTOM_OPS
            elif (general_subclass == 'CUSTOM_OPS'):
                datatype = scene.khalibloo_ops_datatype
                obj_subtype = scene.khalibloo_ops_obj_subtype
                use_obj_type_filters = scene.khalibloo_ops_use_obj_type_filters
                mat_subtype_01 = scene.khalibloo_ops_mat_subtype_01
                mat_subtype_02 = scene.khalibloo_ops_mat_subtype_02
                scene_subtype = scene.khalibloo_ops_scene_subtype
                mod_scope = scene.khalibloo_ops_mod_scope
                const_scope = scene.khalibloo_ops_const_scope

                col = layout.column(align=True)
                box = col.box()
                box.label(text="Operate on:")
                box = col.box()
                row = box.row(align=True)
                if (datatype == 'OBJECTS'):
                    row.prop(scene, "khalibloo_ops_scope03", text="")
                elif (datatype in ['SCENES', 'WORLDS']):
                    row.prop(scene, "khalibloo_ops_scope05", text="")
                row.prop(scene, "khalibloo_ops_datatype", text="")
                if (datatype == 'OBJECTS'):
                    if (obj_subtype == 'MATERIALS'):
                        row = box.row(align=True)
                        row.prop(scene, "khalibloo_ops_scope01", text="")
                        row.prop(scene, "khalibloo_ops_obj_subtype", text="")
                        if (mat_subtype_01 != 'NONE'):
                            row = box.row(align=True)
                            row.prop(scene, "khalibloo_ops_scope04_01", text="")
                            row.prop(scene, "khalibloo_ops_mat_subtype_01", text="")
                        else:
                            row = box.row()
                            row.prop(scene, "khalibloo_ops_mat_subtype_01", text="")
                    elif (obj_subtype == 'MODIFIERS'):
                        row = box.row(align=True)
                        row.prop(scene, "khalibloo_ops_mod_scope", text="")
                        row.prop(scene, "khalibloo_ops_obj_subtype", text="")
                        if (mod_scope == 'SPECIFIC'):
                            box.prop(scene, "khalibloo_ops_mod_subtype", text="")
                    elif (obj_subtype == 'CONSTRAINTS'):
                        row = box.row(align=True)
                        row.prop(scene, "khalibloo_ops_const_scope", text="")
                        row.prop(scene, "khalibloo_ops_obj_subtype", text="")
                        if (const_scope == 'SPECIFIC'):
                            box.prop(scene, "khalibloo_ops_const_subtype", text="")
                    elif (obj_subtype in ['VERTEX_GROUPS', 'SHAPE_KEYS']):
                        row = box.row(align=True)
                        row.prop(scene, "khalibloo_ops_scope01", text="")
                        row.prop(scene, "khalibloo_ops_obj_subtype", text="")
                    elif (obj_subtype in ['UV_MAPS', 'VERTEX_COLORS']):
                        row = box.row(align=True)
                        row.prop(scene, "khalibloo_ops_scope01", text="")
                        row.prop(scene, "khalibloo_ops_obj_subtype", text="")
                    else:
                        row = box.row()
                        row.prop(scene, "khalibloo_ops_obj_subtype", text="")
                elif (datatype == 'MATERIALS'):
                    if (mat_subtype_02 != 'NONE'):
                        row = box.row(align=True)
                        row.prop(scene, "khalibloo_ops_scope04_02", text="")
                        row.prop(scene, "khalibloo_ops_mat_subtype_02", text="")
                    else:
                        row = box.row()
                        row.prop(scene, "khalibloo_ops_mat_subtype_02", text="")
                elif (datatype == 'SCENES'):
                    row = box.row()
                    row.prop(scene, "khalibloo_ops_scene_subtype", text="")

                if (datatype == 'OBJECTS'):
                    col = layout.column(align=True)
                    box = col.box()
                    split = box.split(percentage=0.2)
                    col1 = split.column()
                    #row = col.row()
                    col1.alignment = 'LEFT'
                    col1.prop(scene, "khalibloo_ops_use_obj_type_filters", text="")
                    col1 = split.column()
                    col1.alignment = 'LEFT'
                    col1.label(text="Object type filters:") # TODO: add an "ALL" toggle to filters
                    if(use_obj_type_filters):
                        box = col.box()
                        split = box.split()
                        col = split.column()
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Meshes", toggle=True, index=0)
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Curves", toggle=True, index=1)
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Armatures", toggle=True, index=2)
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Nurbs", toggle=True, index=3)
                        col = split.column()
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Metaballs", toggle=True, index=4)
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Cameras", toggle=True, index=5)
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Lamps", toggle=True, index=6)
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Speakers", toggle=True, index=7)
                        col = split.column()
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Texts", toggle=True, index=8)
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Lattices", toggle=True, index=9)
                        col.prop(scene, "khalibloo_ops_obj_type_filters", text="Empties", toggle=True, index=10)

                layout.separator()
                layout.operator("object.khalibloo_opblock_add", icon='ZOOMIN')
                for block in scene.khalibloo_opblocks:
                    if (block != None):
                        layout.separator()
                        box = layout.box()
                        split = box.split(percentage=0.6)
                        col = split.column()
                        row = col.row(align=True)
                        row.alignment = 'LEFT'
                        row.label(block.name)
                        col = split.column()
                        split = col.split(percentage=0.7)
                        col = split.column()
                        row = col.row(align=True)
                        row.alignment = 'RIGHT'
                        #row.operator("object.khalibloo_opblock" + block.strIndex + "_move_up", text="", icon='TRIA_UP')
                        #row.operator("object.khalibloo_opblock" + block.strIndex + "_move_down", text="", icon='TRIA_DOWN')
                        col = split.column()
                        row = col.row()
                        row.alignment = 'RIGHT'
                        row.operator("object.khalibloo_opblock" + block.strIndex + "_remove", text="", icon='X')
                        box.separator()

                        box.prop(scene, block.prefix+"action_mode")
                        box.prop(scene, block.prefix+"action")

                layout.separator()
                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_opblocks_execute", text="Execute")


#-----------------------------------------------------------------------------------
        #GENESIS TOOLS
        elif (platform == 'DAZ GENESIS'):

            #Genesis Object type
            layout.prop(scene, "khalibloo_genesis_platform_subclass", expand=True)
            layout.separator()

            #if it's a Genesis figure
            if (genesis_subclass == 'FIGURE'):

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_setup")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_vgroups")

                layout.operator("object.khalibloo_genesis_unrigify_vgroups")

                # Morphs
                layout.separator()
                layout.prop(scene, "khalibloo_genesis_morph_dir")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_import_genesis_morphs")

                # Check boxes
                layout.separator()
                layout.prop(scene, "khalibloo_affect_textures")
                layout.prop(scene, "khalibloo_merge_mats")

                #row = layout.row()
                layout.operator("object.khalibloo_genesis_material_setup")

            #If it's a Genesis item
            elif (genesis_subclass == 'ITEM'):

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_vgroups")

                layout.operator("object.khalibloo_genesis_unrigify_vgroups")

#-----------------------------------------------------------------------------------
        #GENESIS 2 TOOLS
        elif (platform == 'DAZ GENESIS 2'):

            #Genesis Object type
            layout.prop(scene, "khalibloo_genesis2_platform_subclass", expand=True)
            layout.separator()

            #if it's a Genesis 2 Male
            if (genesis2_subclass == 'MALE'):

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis2male_rigify_setup")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_vgroups")

                layout.operator("object.khalibloo_genesis_unrigify_vgroups")

                # Morphs
                layout.separator()
                layout.prop(scene, "khalibloo_genesis_morph_dir")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_import_genesis_morphs")

                # Check boxes
                layout.separator()
                layout.prop(scene, "khalibloo_affect_textures")
                layout.prop(scene, "khalibloo_merge_mats")

                layout.operator("object.khalibloo_genesis_material_setup")


            #if it's a Genesis 2 Female
            if (genesis2_subclass == 'FEMALE'):

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis2female_rigify_setup")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_vgroups")

                layout.operator("object.khalibloo_genesis_unrigify_vgroups")



                # Morphs
                layout.separator()
                layout.prop(scene, "khalibloo_genesis_morph_dir")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_import_genesis_morphs")

                # Check boxes
                layout.separator()
                layout.prop(scene, "khalibloo_affect_textures")
                layout.prop(scene, "khalibloo_merge_mats")

                # Materials
                layout.operator("object.khalibloo_genesis_material_setup")

            #If it's a Genesis Item
            elif (genesis2_subclass == 'ITEM'):
                # Big button
                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_vgroups")

                layout.operator("object.khalibloo_genesis_unrigify_vgroups")

#-----------------------------------------------------------------------------------
        #GENESIS 3 TOOLS
        elif (platform == 'DAZ GENESIS 3'):

            #Genesis Object type
            layout.prop(scene, "khalibloo_genesis3_platform_subclass", expand=True)
            layout.separator()

            #if it's a Genesis 3 Male
            if (genesis3_subclass == 'MALE'):
                #layout.label("Genesis 3 Male unavailable")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis3male_rigify_setup")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_vgroups")

                layout.operator("object.khalibloo_genesis_unrigify_vgroups")

                # Morphs
                layout.separator()
                layout.prop(scene, "khalibloo_genesis_morph_dir")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_import_genesis_morphs")

                # Check boxes
                layout.separator()
                layout.prop(scene, "khalibloo_affect_textures")
                layout.prop(scene, "khalibloo_merge_mats")

                layout.operator("object.khalibloo_genesis_material_setup")


            #if it's a Genesis 3 Female
            if (genesis3_subclass == 'FEMALE'):

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis3female_rigify_setup")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_vgroups")

                layout.operator("object.khalibloo_genesis_unrigify_vgroups")



                # Morphs
                layout.separator()
                layout.prop(scene, "khalibloo_genesis_morph_dir")

                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_import_genesis_morphs")

                # Check boxes
                layout.separator()
                layout.prop(scene, "khalibloo_affect_textures")
                layout.prop(scene, "khalibloo_merge_mats")

                # Materials
                layout.operator("object.khalibloo_genesis_material_setup")

            #If it's a Genesis Item
            elif (genesis3_subclass == 'ITEM'):
                # Big button
                row = layout.row()
                row.scale_y = 2.0
                row.operator("object.khalibloo_genesis_rigify_vgroups")

                layout.operator("object.khalibloo_genesis_unrigify_vgroups")


class KhaliblooPanelUV(bpy.types.Panel):
    """Creates a Panel in the tool shelf of the UV/Image editor"""
    bl_label = "Khalibloo Panel"
    bl_idname = "khalibloo_panel_uv"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align = True)
        row.operator("uv.khalibloo_uv_flatten_x", text="Flatten X")
        row.operator("uv.khalibloo_uv_flatten_y", text="Flatten Y")

        #layout.prop(scene, "khalibloo_image")
        #layout.template_ID(bpy.context.space_data, "image", new="image.new")

        #row = layout.row(align = True)
        #row.prop(scene, "khalibloo_batchbake_startframe")
        #row.prop(scene, "khalibloo_batchbake_endframe")

def register():
    utils.initialize()
    custom_ops.initialize()
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
