# wahooney_action_enable_export.py Copyright (C) 2009-2010, Keith "Wahooney" Boshoff
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Unity Export Tools",
    "author": "Keith (Wahooney) Boshoff",
    "version": (0, 9, 10),
    "blender": (2, 7, 6),
    "description": "A collection of tools for exporting meshes and animations to Unity3D",
    "url": "",
    "category": "Tools"}

"""

Version History:

0.7: Use blender's standard fbx exporter

0.8: Improve blend shape exporter (each mesh gets exported to it's own file and contains all of it's flex shapes)

0.9: Added prop_searches to Animation Group and Collapse Head

0.9.5: Integrated action exporter into group exporter

0.9.7: Added texture exporter

0.9.8: Added custom FBX export option

0.9.9: Technical debt
    * Improved guess buttons (auto-icon)
    * Reorganized options into more logical groupings
    * Fixed Export Textures not exporting images that haven't been loaded yet.
    * Fixed Export Layers not updating the scene (breaks exporting shadow rigs)

0.9.10:
    * Made Sub Path optional

0.9.11:
    * Export textures only exports selected groups' textures

TODO: Add filtering out of external groups, add more built-in lists
    http://www.blender.org/api/blender_python_api_2_73_8/bpy.types.UIList.html#advanced-uilist-example-filtering-and-reordering

"""

import bpy, os
import bgl
import blf
import re
from bpy.props import *
from mathutils import Vector, Matrix

#unity_global_scale = 10

#
#
# General functions
#
#

def fix_path(path):
    return os.path.normpath(bpy.path.abspath(path))

def enable_action_export(context):
    action = context.active_object.animation_data.action

    if (action):
        action['export'] = True;

def rename (replaceText, withText, target):
    return re.sub (replaceText, withText, target)

#~ class EnableActionExport(bpy.types.Operator):
    #~ ''''''
    #~ bl_idname = "actions.enable_export"
    #~ bl_label = "Enable Action Export"

    #~ @classmethod
    #~ def poll(cls, context):
        #~ return context.active_object != None

    #~ def execute(self, context):
        #~ enable_action_export(context)
        #~ return {'FINISHED'}

#
#
# GUESS EXPORT OPERATOR
#
#

def replace (string, what_string, with_string):
    if (len (what_string) != len (with_string)):
        return string

    result = string

    for i, r in enumerate (what_string):
        result = result.replace (r, with_string[i])

    return result

def guess_export_path(context):
    filepath = context.blend_data.filepath

    if not filepath:
        return

    filepath = os.path.dirname(filepath)

    filepath = replace (filepath,
        ["Author", "author"],
        ["Assets", "assets"])

    if context.user_preferences.filepaths.use_relative_paths:
        context.scene.unity_export_path = bpy.path.relpath (filepath)
    else:
        context.scene.unity_export_path = bpy.path.abspath (filepath)

class GuessExportPath (bpy.types.Operator):
    ''''''
    bl_idname = "scene.unity_export_guess_path"
    bl_label = "Guess Unity Export Path"
    bl_description = "Guess the export path from the current .blend file path\nRespects User Preferences > Relative Paths"

    def execute(self, context):
        guess_export_path(context)
        return {'FINISHED'}

def get_export_path (context, sub_path=""):

    scene = context.scene

    export_path = "";

    if scene.unity_export_path == "":
        filepath = context.blend_data.filepath
        filename = filepath[filepath.rfind(os.path.sep)+1:filepath.rfind(".blend")]
    else:
        export_path = scene.unity_export_path

    if not export_path.endswith (os.path.sep):
        export_path += os.path.sep

    if export_path != "":
        export_path = export_path[:export_path.rfind(os.path.sep)]
        export_path = fix_path(export_path)

    export_path += os.path.sep + sub_path

    if not os.path.exists(export_path):
        if context.scene.unity_make_path:
            os.makedirs(export_path)
        else:
            self.report({'WARNING'}, "Path '%s' doesn't exist" % export_path)

    return export_path

#
#
# GUESS TEXTURE EXPORT
#
#
def guess_texture_export_path(context):
    filepath = context.blend_data.filepath

    filepath = os.path.dirname(filepath)

    filepath = replace (filepath,
        ["Author", "author", "models", "Models", "meshes", "Meshes"],
        ["assets", "assets", "textures", "Textures", "textures", "Textures"])

    if context.user_preferences.filepaths.use_relative_paths:
        context.scene.unity_texture_export_path = bpy.path.relpath (filepath)
    else:
        context.scene.unity_texture_export_path = bpy.path.abspath (filepath)

class GuessTextureExportPath (bpy.types.Operator):
    ''''''
    bl_idname = "scene.unity_texture_export_guess_path"
    bl_label = "Guess Unity Texture Export Path"
    bl_description = "Guess the export path from the current .blend file path\nRespects User Preferences > Relative Paths"

    def execute(self, context):
        guess_texture_export_path(context)
        return {'FINISHED'}

def get_texture_export_path (context, sub_path=""):

    scene = context.scene

    texture_export_path = ""

    if scene.unity_texture_export_path == "":
        filepath = context.blend_data.filepath
        filename = filepath[filepath.rfind(os.path.sep)+1:filepath.rfind(".blend")]
    else:
        texture_export_path = scene.unity_texture_export_path

    if not texture_export_path.endswith (os.path.sep):
        texture_export_path += os.path.sep

    if texture_export_path != "":
        texture_export_path = texture_export_path[:texture_export_path.rfind(os.path.sep)]
        texture_export_path = fix_path(texture_export_path)

    texture_export_path += os.path.sep + sub_path

    if not os.path.exists(texture_export_path):
        if context.scene.unity_make_path:
            os.makedirs(texture_export_path)
        else:
            self.report({'WARNING'}, "Path '%s' doesn't exist, try using 'Create missing folders on export'" % texture_export_path)

    return texture_export_path


def export_groups_textures(context, operator):

    images = []

    scene = context.scene

    use_lib = scene.unity_use_libraries

    # cycle through groups
    for group in bpy.data.groups:

        if not group.unity_export or (not use_lib and group.library != None):
            continue

        print(group.name)

        if not len(group.objects):
            print(group.name, " has no objects")
            continue

        export_objects = []

        obj = None

        # select objects for export and offset by group dupli offset
        for obj in group.objects:
            if obj.unity_export:

                export_objects.append(obj)

        for obj in export_objects:

            if obj == None:
                continue

            for mat in obj.material_slots:

                if mat == None or mat.material == None:
                    continue

                for tex in mat.material.texture_slots:

                    if tex == None or tex.texture == None:
                        continue

                    if tex.texture.type == 'IMAGE' and tex.texture.image != None and images.count (tex.texture.image) < 1:
                        # Update texture if it has no data, it may not have loaded yet
                        if not tex.texture.image.has_data:
                            tex.texture.image.update ()

                        if tex.texture.image.has_data:
                            images.append (tex.texture.image)

        if len(images) == 0:
            print("No textures to export")
            continue

        scene.objects.active = export_objects[0]
        scene.update()

        for image in images:

            if image.name.lower ().endswith ("." + image.file_format.lower ()):
                filename = image.name
            else:
                filename = image.name + "." + image.file_format.lower ()

            export_path = get_texture_export_path (context, group.unity_subpath if group.unity_use_subpath else "")

            orig_filepath_raw = image.filepath_raw

            image.filepath_raw = os.path.join (export_path, filename)
            image.update ()

            image.save ()

            #print (image.name)
            print ("Saved to: %s" % image.filepath_raw)

            image.filepath_raw = orig_filepath_raw
            image.update()


class ExportGroupsTextures(bpy.types.Operator):
    ''''''
    bl_idname = "export.unity_groups_textures"
    bl_label = "Export Groups Textures"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        export_groups_textures(context, self)
        return {'FINISHED'}

#
#
# EXPORT GROUP ACTIONS OPERATOR
#
#
def export_actions_to_unity(self, context):
    active = context.active_object
    scene = context.scene
    selection = context.selected_objects

    for group in bpy.data.groups:
        if group.unity_animation:
            export_group_actions(self, context, scene, group)

    for ob in scene.objects:
        ob.select = False

    for sel in selection:
        sel.select = True

    scene.objects.active = active

def export_group_actions(self, context, scene, group):

    active = scene.objects.active
    forward = scene.unity_forward_axis

    if not scene.unity_use_libraries and group.library != None:
        return

    # find exportable actions
    actions = [act for act in group.unity_actions if act.export and act.action_name in bpy.data.actions]
    selection = context.selected_objects

    # store original actions for all objects
    animation_objects = [group.objects[obj.object_name] for obj in group.unity_action_objects if obj.object_name in group.objects]

    if len(animation_objects) == 0:
        self.report({'WARNING'}, "There are no actions to export in %s" % group.name)
        return

    store_actions = {}

    for obj in animation_objects:
        if obj.animation_data == None:
            continue

        store_actions[obj] = obj.animation_data.action

    range_store = [scene.frame_start, scene.frame_end]

    export_path = get_export_path (context, sub_path=group.unity_subpath if group.unity_use_subpath else "")

    if (export_path == ""):
        return

    # store layers
    store_layers = []

    for i in scene.layers:
        store_layers.append(i)

    for action in actions:

        act = bpy.data.actions[action.action_name]

        for f in act.fcurves:
            f.is_valid = True

        for sel in context.selected_objects:
            sel.select = False

        for obj in animation_objects:
            if obj.animation_data == None:
                obj.animation_data_create()

            obj.animation_data.action = act

            print (act.name)

        namestore = {}

        # set export layers
        if group.unity_use_export_layers:
            for i, state in enumerate(group.unity_export_layers):
                scene.layers[i] = state
        else:
            for i, state in enumerate(store_layers):
                scene.layers[i] = state

        scene.update ()

        for obj in group.objects:

            for act_obj in group.unity_action_objects:
                if obj.name == act_obj.object_name or not scene.unity_only_export_action_objects:
                    obj.select = obj.unity_export

                    # rename object
                    if obj.unity_use_rename:

                        namestore[obj] = obj.name
                        obj.name = rename (scene.unity_export_name_find, scene.unity_export_name_replace, obj.name)

                        #rename data
                        if obj.data is not None:

                            namestore[obj.data] = obj.data.name
                            obj.data.name = rename (scene.unity_export_name_find, scene.unity_export_name_replace, obj.data.name)

        fr = act.frame_range

        scene.frame_start = action.start_frame;
        scene.frame_end = action.end_frame;

        export_path = get_export_path (context, sub_path=group.unity_subpath if group.unity_use_subpath else "")

        fbx = group.name + "@" + act.name.strip() + ".fbx"

        if scene.use_custom_exporter:
            bpy.ops.export_scene.fbx_yup(filepath=export_path + fbx
                , use_selection=True
                # scene
                , axis_forward='Z'
                , axis_up='Y'
                , global_scale=scene.unity_global_scale*100
                # animation
                , use_anim_optimize=action.optimize
                , use_anim_action_all=False)
        else:
            bpy.ops.export_scene.fbx(filepath=export_path + fbx
              , use_selection=True
              , batch_mode='OFF'
              # scene
              , global_scale=scene.unity_global_scale
              , axis_forward='-Z'
              , axis_up='Y'
              , bake_space_transform=True
              # objects
              , use_custom_props=True
              # animation
              , bake_anim=True
              , bake_anim_use_all_actions=False
              , bake_anim_use_nla_strips=False
              , bake_anim_simplify_factor=0.0 if action.optimize else 1.0
              # rig
              , add_leaf_bones=False
              , use_armature_deform_only=True
            )

        for o in namestore:
            o.name = namestore[o];

    scene.frame_start = range_store[0]
    scene.frame_end = range_store[1]

    # Restore original actions
    for obj, act in store_actions.items():
        obj.animation_data.action = act

    # Restore original layers
    for i, l in enumerate(store_layers):
        scene.layers[i] = l

class ExportActionsForUnity(bpy.types.Operator):
    ''''''
    bl_idname = "export.actions_for_unity"
    bl_label = "Export Actions for Unity"

    def execute(self, context):
        export_actions_to_unity(self, context)
        return {'FINISHED'}

#
#
#   EXPORT GROUPS TO FBX OPERATOR
#
#
def pure_curve(obj):
    return obj.type == 'CURVE' and obj.data.bevel_depth == 0 and obj.data.extrude == 0 and obj.data.bevel_object == None

def collapse_group(argGroup):
    group = bpy.data.groups[argGroup]
    objects = bpy.data.objects
    scene = bpy.context.scene

    for obj in objects:
        obj.select = False

    meshes = []
    collapse_objects = []

    head_object = None

    for obj in group.objects:
        if obj.name == group.unity_head and pure_curve (obj):
            return None

    for obj in group.objects:

        # deselect everything
        for o in objects:
            o.select = False

        ob = None

        if obj.type in ['CURVE']:
            #convert curves (and other convertable objects) to meshes

            # this is a pure_curve, skip it
            if pure_curve (obj):
                continue

            scene.objects.active = obj
            obj.select = True

            bpy.ops.object.convert(target='MESH', keep_original=True)
            ob = scene.objects.active
            scene.objects.active = None

        elif obj.type == 'MESH':

            ob = obj.copy()
            scene.objects.link(ob)

        else:

            continue

        if (ob.data.users != 1):
            ob.data = ob.data.copy()

        if obj.name == group.unity_head:
            head_object = ob
        else:
            meshes.append(ob.data)

        collapse_objects.append(ob)

    for obj in collapse_objects:
        obj.select = True

    scene.objects.active = head_object
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.join()

    for mesh in meshes:
        bpy.data.meshes.remove(mesh)

    return head_object

def export_groups_to_fbx(context, operator):
    select = []
    active = context.active_object
    scene = context.scene
    use_lib = scene.unity_use_libraries
    use_dupli = scene.unity_use_duplis

    forward = scene.unity_forward_axis

    # clear object selection, store current object selection
    for obj in bpy.data.objects:
        if obj.select:
            select.append(obj)

        obj.select = False

    # store layers
    store_layers = []

    for i in scene.layers:
        store_layers.append(i)

    # cycle through groups
    for group in bpy.data.groups:

        if not group.unity_export or (not use_lib and group.library != None):
            continue

        if group.unity_collapse and group.unity_head in group.objects and pure_curve (group.objects[group.unity_head]):
            continue

        print(group.name)

        if not len(group.objects):
            print(group.name, " has no objects")
            continue

        # set export layers
        if group.unity_use_export_layers:
            for i, l in enumerate(group.unity_export_layers):
                scene.layers[i] = l
        else:
            for i, l in enumerate(store_layers):
                scene.layers[i] = l

        # store animation objects
        animation_objects = [group.objects[obj.name] for obj in group.unity_action_objects if obj.name in group.objects]

        store_actions = {}

        for obj in animation_objects:
            if obj.animation_data == None:
                continue

            store_actions[obj] = obj.animation_data.action

        # set static pose
        if group.unity_static_action in bpy.data.actions:
            for obj in animation_objects:
                obj.animation_data.action = bpy.data.actions[group.unity_static_action]

        cleanup_objects = []

        export_objects = []

        obj = None

        if group.unity_collapse:

            obj = collapse_group(group.name)

            if not obj:
                continue

            cleanup_objects.append(obj)
            export_objects.append(obj)

        else:
            # select objects for export and offset by group dupli offset
            for obj in group.objects:
                if obj.unity_export:

                    # convert non-mesh -> mesh (curve)
                    if obj.type == 'CURVE':
                        scene.objects.active = obj
                        bpy.ops.object.convert(target='MESH', keep_original=True)
                        obj = scene.objects.active
                        cleanup_objects.append(obj)

                    export_objects.append(obj)

        namestore = {}

        for obj in export_objects:

            if obj == None:
                continue

            obj.select = obj.unity_export

            if obj.unity_use_rename:

                namestore[obj] = obj.name
                obj.name = rename (scene.unity_export_name_find, scene.unity_export_name_replace, obj.name)

                if obj.data is not None:

                    namestore[obj.data] = obj.data.name
                    obj.data.name = rename (scene.unity_export_name_find, scene.unity_export_name_replace, obj.data.name)


            if group.unity_disable_blend_shapes and obj.type == 'MESH':
                mesh = obj.data

                shape_keys = mesh.shape_keys

                if shape_keys != None:
                    for key in shape_keys.key_blocks:
                        key.value = 0.0

            if obj.parent == None:
                obj.location -= group.dupli_offset

            if use_dupli:
                obj['dupli'] = obj.dupli_type
                obj.dupli_type = 'NONE'

        if len(export_objects) == 0:
            print("No objects to export")
            continue

        scene.objects.active = export_objects[0]
        scene.update()

        export_path = get_export_path (context, group.unity_subpath if group.unity_use_subpath else "")

        fbx = group.name + ".fbx"

        print (export_path)

        if scene.use_custom_exporter:
            bpy.ops.export_scene.fbx_yup(filepath=export_path + fbx
                , use_selection=True
                # scene
                , axis_forward='Z'
                , axis_up='Y'
                , global_scale=scene.unity_global_scale*100
                # animation
                , use_anim=group.unity_animation
                , use_anim_optimize=group.unity_optimize
                , use_anim_action_all=False)
        else:
            bpy.ops.export_scene.fbx(filepath=export_path + fbx
                , use_selection=True
                , batch_mode='OFF'
                # scene
                , global_scale=scene.unity_global_scale
                , axis_forward='-Z'
                , axis_up='Y'
                , bake_space_transform=True
                # objects
                , use_custom_props=True
                # animation
                , bake_anim=True
                , bake_anim_use_all_actions=False
                , bake_anim_use_nla_strips=False
                , bake_anim_simplify_factor=0.0 if group.unity_optimize else 1.0
                # rig
                , add_leaf_bones=False
                , use_armature_deform_only=True
            )
        print("'%s' exported." % group.name)

        # return objects to previous positions
        if len(cleanup_objects):
            for o in cleanup_objects:
                if (o == None):
                    continue

                context.scene.objects.unlink(o)
                data = o.data
                bpy.data.objects.remove(o)
                bpy.data.meshes.remove(data)

        else:
            for obj in group.objects:
                obj.select = False

                if obj.parent == None:
                    obj.location += group.dupli_offset

                    if use_dupli:
                        obj.dupli_type = obj['dupli']

        for obj, act in store_actions.items():
            obj.animation_data.action = act

        for o in namestore:
            o.name = namestore[o];

    # restore object selection
    for obj in select:
        obj.select = True

    scene.objects.active = active

    for i, l in enumerate(store_layers):
        scene.layers[i] = l

class ExportGroupsToFBX(bpy.types.Operator):
    ''''''
    bl_idname = "export.groups_to_fbx"
    bl_label = "Export Groups to FBX"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        export_groups_to_fbx(context, self)
        return {'FINISHED'}

def group_assign_z_up(context):
    active = context.active_object

    for group in bpy.data.groups:
        for obj in group.objects:
            if obj.select:
                group['z-up'] = 1

class GroupAssignZUp(bpy.types.Operator):
    ''''''
    bl_idname = "group.assign_zup"
    bl_label = "Assign Z-Up to Group"

    @classmethod
    def poll(cls, context):
        return context.active_object != None or len(context.selected_objects)

    def execute(self, context):
        group_assign_z_up(context)
        return {'FINISHED'}

def dupli_offset_to_selected(context):
    active = context.active_object

    for group in bpy.data.groups:
        for obj in group.objects:
            if obj.select:
                group.dupli_offset = obj.location

class DupliOffsetToSelected(bpy.types.Operator):
    ''''''
    bl_idname = "group.dupli_offset_to_selected"
    bl_label = "Move Dupli-Offset to Selected"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        dupli_offset_to_selected(context)
        return {'FINISHED'}

def group_name_from_selected(context):
    active = context.active_object

    for group in bpy.data.groups:
        for obj in group.objects:
            if obj.select:
                group.name = obj.name

class GroupNameFromSelected(bpy.types.Operator):
    ''''''
    bl_idname = "group.group_name_from_selected"
    bl_label = "Rename Group from Selected"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        group_name_from_selected(context)
        return {'FINISHED'}

def get_export_actions(context):
    scene = context.scene
    active = context.active_object

    # convert old method
    for act in bpy.data.actions:
        if 'export' in act:
            act.unity_export = act['export']
            del act['export']

    actions = bpy.data.actions

    filepath = context.blend_data.filepath
    filename = filepath[filepath.rfind(os.path.sep)+1:filepath.rfind(".blend")]

    for group in bpy.data.groups:
        for ob in group.objects:
            if ob == active:
                filename = group.name
                break

    return {'actions': actions, 'filename': filename}

def get_export_groups():

    groups = bpy.data.groups

    return groups

class UnityActionAdd(bpy.types.Operator):
    '''Add an action to the current group'''
    bl_idname = "group.unity_action_add"
    bl_label = "Add Unity Action to Group"

    @classmethod
    def poll(cls, context):
        return context.group != None;

    def execute(self, context):
        context.group.unity_actions.add();
        return {'FINISHED'}

class UnityActionRemove(bpy.types.Operator):
    '''Remove current action from the current group'''
    bl_idname = "group.unity_action_remove"
    bl_label = "Remove Unity Action from Group"

    @classmethod
    def poll(cls, context):
        return hasattr (context, "group") and context.group != None and hasattr(context, "unity_group_action") and context.unity_group_action != None

    def execute(self, context):

        index = -1

        for i, a in enumerate(context.group.unity_actions):
            if a == context.unity_group_action:
                index = i

        if index >= 0:
            context.group.unity_actions.remove(index)

        return {'FINISHED'}

class UnityActionObjectAdd(bpy.types.Operator):
    '''Add an action object to the current group action'''
    bl_idname = "group.unity_action_object_add"
    bl_label = "Add Group Object to Unity Actions"

    @classmethod
    def poll(cls, context):
        return context.group != None;

    def execute(self, context):
        context.group.unity_action_objects.add();
        return {'FINISHED'}

class UnityActionObjectRemove(bpy.types.Operator):
    '''Remove group object from current action'''
    bl_idname = "group.unity_action_object_remove"
    bl_label = "Remove Group Object from Unity Actions"

    @classmethod
    def poll(cls, context):
        return hasattr (context, "group") and context.group != None and hasattr(context, "unity_group_action_object") and context.unity_group_action_object != None

    def execute(self, context):

        index = -1

        for i, a in enumerate(context.group.unity_action_objects):
            if a == context.unity_group_action_object:
                index = i
        print(index)
        if index >= 0:
            context.group.unity_action_objects.remove(index)

        return {'FINISHED'}

class UnityActionRangeGuess(bpy.types.Operator):
    '''Guess the frame range of the current action exporter'''
    bl_idname = "group.unity_action_guess_frame_range"
    bl_label = "Guess frame range, cased on first and last frames"
    bl_description = "Guess the animation range of the current action"

    @classmethod
    def poll(cls, context):
        return context.group != None and context.unity_group_action != None

    def execute(self, context):

        if context.unity_group_action.action_name in bpy.data.actions:
            act = bpy.data.actions[context.unity_group_action.action_name]
            fr = act.frame_range
            context.unity_group_action.start_frame = int(fr[0])
            context.unity_group_action.end_frame = int(fr[1])
        else:
            if context.unity_group_action.action_name == '' or context.unity_group_action.action_name is None:
                self.report ({'ERROR_INVALID_INPUT'}, "Action group name is empty")
            else:
                self.report ({'ERROR_INVALID_INPUT'}, "Action %s does not exist" % context.unity_group_action.action_name)

        return {'FINISHED'}

class UnityActionRangeShow(bpy.types.Operator):
    '''Set the current animation range to the action range'''
    bl_idname = "group.unity_action_show_frame_range"
    bl_label = "Show the current action frame range"

    @classmethod
    def poll(cls, context):
        return context.group != None and context.unity_group_action != None

    def execute(self, context):

        act = bpy.data.actions[context.unity_group_action.action_name]

        context.scene.frame_start = context.unity_group_action.start_frame
        context.scene.frame_end = context.unity_group_action.end_frame

        return {'FINISHED'}

class UNITY_UL_export_groups(bpy.types.UIList):

    GROUP_EXTERNAL = 1 << 0

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        ob = data
        group = item

        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            row = layout.row (align=True)
            row.prop(group, 'unity_export', icon='EXPORT', text='')
            row.prop(group, 'unity_use_subpath', icon='DISCLOSURE_TRI_DOWN' if group.unity_use_subpath else 'DISCLOSURE_TRI_RIGHT', text='')

            if group.unity_use_subpath:
                row.prop(group, 'unity_subpath', emboss=False, icon='FILE_FOLDER', text='')

            row.prop(group, 'name', emboss=False, icon_value=icon, text='')
            row.prop(group, 'unity_disable_blend_shapes', icon='SHAPEKEY_DATA', text='')
            row.prop(group, 'unity_animation', icon='ACTION', text='')
            row.prop(group, 'unity_optimize', icon='MOD_DECIM', text='')

        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon_value=icon)

        # TODO start here

    def draw_filter(self, context, layout):
        # Nothing much to say here, it's usual UI code...
        row = layout.row(align=True)
        scene = context.scene

        #row = row.row(align=True)
        row.prop(self, "filter_name", text="")
        icon = 'ZOOM_OUT' if self.use_filter_invert else 'ZOOM_IN'
        row.prop(self, "use_filter_invert", text="", icon=icon)

        #row = layout.row(align=True)
        row.separator()
        row.prop(self, "use_filter_sort_alpha", text='', toggle=True)
        icon = 'TRIA_UP' if self.use_filter_sort_reverse else 'TRIA_DOWN'
        row.prop(self, "use_filter_sort_reverse", text="", icon=icon)

        row.separator()
        row.prop(scene, 'unity_hide_external_groups', text='', toggle=True, icon='EXTERNAL_DATA')

    def filter_items(self, context, data, propname):
        # This function gets the collection property (as the usual tuple (data, propname)), and must return two lists:
        # * The first one is for filtering, it must contain 32bit integers were self.bitflag_filter_item marks the
        #   matching item as filtered (i.e. to be shown), and 31 other bits are free for custom needs. Here we use the
        #   first one to mark VGROUP_EMPTY.
        # * The second one is for reordering, it must return a list containing the new indices of the items (which
        #   gives us a mapping org_idx -> new_idx).
        # Please note that the default UI_UL_list defines helper functions for common tasks (see its doc for more info).
        # If you do not make filtering and/or ordering, return empty list(s) (this will be more efficient than
        # returning full lists doing nothing!).
        groups = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, groups, "name", reverse=self.use_filter_sort_reverse)

        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(groups)

        scene = context.scene
        if scene.unity_hide_external_groups:
            for i, g in enumerate(groups):
                if g.library == None:
                    flt_flags[i] |= self.GROUP_EXTERNAL
                else:
                    flt_flags[i] &= ~self.bitflag_filter_item


        # Reorder by name or average weight.
        if self.use_filter_sort_alpha:
            flt_neworder = helper_funcs.sort_items_by_name(groups, "name")

        return flt_flags, flt_neworder

from bpy.types import Menu, Panel, Operator
from bl_operators.presets import AddPresetBase

class UNITY_RENAME_MT_presets(Menu):
    bl_label = "Rename Presets"
    preset_subdir = "unity_export_rename"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset

class AddPresetUnityRename(AddPresetBase, Operator):
    """Add a Unity Rename Preset"""
    bl_idname = "scene.unity_preset_add"
    bl_label = "Add Renaming Preset"
    preset_menu = "UNITY_RENAME_MT_presets"

    # IMPORTANT: you need to specify below, what will be serialized to a preset file

    preset_defines = [
        "scene = bpy.context.scene"
    ]

    preset_values = [
        "scene.unity_export_name_find",
        "scene.unity_export_name_replace",
    ]

    preset_subdir = "unity_export_rename" # make sure it's the same as in your menu class


class UNITY_PT_Scene(bpy.types.Panel):
    bl_label = 'Unity Export Tools'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_default_closed = False

    def draw (self, context):

        layout = self.layout
        scene = context.scene
        use_lib = scene.unity_use_libraries

        # tools

        layout.label(text='Tools', icon='MODIFIER')

        col = layout.column(align=True)

        if GroupNameFromSelected:
            col.operator(GroupNameFromSelected.bl_idname, text='Rename Groups From Selected')

        if bpy.ops.object.rename_from_data:
            col.operator("object.rename_from_data", text='Rename Objects From Data')

        col.operator(DupliOffsetToSelected.bl_idname, text='Dupli-Offset to Object')

        col = layout.column(align=True)

        # Export Groups List

        col.label("Export Groups", icon='GROUP')
        #col.prop (scene, "show_all_scenes")

        col.template_list('UNITY_UL_export_groups', '', bpy.data, 'groups', scene, 'unity_active_export_group_index', rows=3)

        groups = get_export_groups()

        # Group Settings

        if (scene.unity_active_export_group_index < len(groups)):

            group = groups[scene.unity_active_export_group_index]

            if group is not None:

                layout.separator ()
                box2 = layout.box()

                box2.label (group.unity_subpath + group.name, icon='GROUP')

                row = box2.row(align=True)

                row.prop(group, 'unity_use_subpath', text='', icon='DISCLOSURE_TRI_DOWN' if group.unity_use_subpath else 'DISCLOSURE_TRI_RIGHT')

                if group.unity_use_subpath:
                    row.prop(group, 'unity_subpath', text='', icon='FILE_FOLDER')

                row.prop (group, "name", icon='GROUP', text='')

                #layers
                col_export_layers = box2.column()
                col_export_layers.prop(group, 'unity_use_export_layers', text="Export Layers", toggle=True, icon='RENDERLAYERS')
                if group.unity_use_export_layers:
                    col_export_layers.prop(group, 'unity_export_layers', text="")

                # animation
                row = box2.row(align=True)
                row.prop(group, 'unity_animation', toggle=True)
                row.prop(group, 'unity_optimize', toggle=True)

                box2.prop_search(group, "unity_static_action", bpy.data, "actions", text='Static Action', icon='ARMATURE_DATA')

                # group actions
                column_action = box2.column(align=True);
                column_action.context_pointer_set("group", group)

                if len (group.unity_actions) > 0:
                    column_action.operator("group.unity_action_add")

                for i, act in enumerate(group.unity_actions):

                    adv_icon = "TRIA_RIGHT"

                    if act.expanded:
                        adv_icon = "TRIA_DOWN";

                    row_action = column_action.row(align=True);

                    row_action.prop(act, 'expanded', icon=adv_icon, text='', emboss=False)

                    row_action.context_pointer_set("unity_group_action", act)
                    row_action.context_pointer_set("group", group)

                    row_action.prop(act, "export", icon='ACTION', text='')
                    row_action.prop_search(act, "action_name", bpy.data, "actions", text='', icon='NONE')
                    row_action.prop(act, "optimize", icon='MOD_DECIM', text='')
                    row_action.operator("group.unity_action_remove", text="", icon="X")

                    if act.expanded:
                        row_action = column_action.row (align=True);
                        row_action.context_pointer_set("unity_group_action", act)
                        row_action.prop (act, "start_frame");
                        row_action.prop (act, "end_frame");
                        row_action.operator ("group.unity_action_guess_frame_range", text="", icon='AUTO')

                        icon = 'VISIBLE_IPO_OFF'

                        if act.show_frame_range: icon= 'VISIBLE_IPO_ON'

                        row_action.prop (act, "show_frame_range", text="", icon=icon)

                column_action.operator("group.unity_action_add")

                # group action objects
                column_action = box2.column(align=True);
                column_action.context_pointer_set("group", group)

                for i, obj in enumerate(group.unity_action_objects):
                    row_action = column_action.row (align=True);

                    if obj.object_name in bpy.data.objects:
                        ob = bpy.data.objects[obj.object_name]
                        row_action.prop (ob, "unity_use_actions", text='', icon='ACTION_TWEAK')

                    row_action.context_pointer_set("unity_group_action_object", obj)
                    row_action.context_pointer_set("group", group)

                    row_action.prop_search(obj, "object_name", group, "objects", icon='OBJECT_DATA', text='')
                    row_action.operator("group.unity_action_object_remove", text="", icon="ZOOMOUT")

                column_action.operator("group.unity_action_object_add")
                column_action.prop (scene, 'unity_only_export_action_objects', text='Only export action objects', emboss=True, toggle=True);


                # show objects
                col = box2.column (align=True)
                col.prop(group, 'unity_show_objects', icon="TRIA_DOWN" if group.unity_show_objects else "TRIA_RIGHT", emboss=True)

                if group.unity_show_objects:

                    for o in group.objects:
                        row = col.row (align=True)

                        obj_icon = "OBJECT_DATA"

                        for a_obj in group.unity_action_objects:
                            if o.name == a_obj.object_name:
                                obj_icon = "SEQUENCE"
                                break

                        data_icon = "MESH_DATA"

                        row.prop (o, "unity_export", emboss=True, text='', icon='EXPORT')
                        row.prop (o, "name", text='', icon=obj_icon)

                        if o.data != None:
                            row.prop (o.data, "name", text='', icon=data_icon)

                        row.prop (o, "unity_use_rename", text='', icon='FILE_TEXT')

                    col.prop(group, 'unity_show_objects', icon='TRIA_UP', emboss=True)


                # collapse
                row = box2.row(align=True)
                row.prop(group, 'unity_collapse', toggle=True, text="Collapse")

                if group.unity_collapse:
                    icon = 'QUESTION'
                    if group.unity_head == "":
                        pass
                    elif group.unity_head in group.objects:
                        icon = 'FILE_TICK'
                    else:
                        icon = 'ERROR'

                    row.prop_search(group, 'unity_head', group, "objects", text="", icon="OBJECT_DATA")

                    if group.unity_head in group.objects and pure_curve (group.objects[group.unity_head]):
                        box2.label ("%s is not a valid collapse head" % group.unity_head, icon='ERROR')
                    #row.prop(group, 'unity_head', text="", icon=icon)

        # Renaming
        layout.separator ()
        box = layout.box ()

        col2 = box.column (align=True)
        col2.label ("Renaming", icon='SHORTDISPLAY')
        col2.prop(scene, 'unity_export_name_find', text='', icon='FILTER')
        col2.prop(scene, 'unity_export_name_replace', text='', icon='PASTEDOWN')

        row = col2.row(align=True)
        row.menu("UNITY_RENAME_MT_presets", text=bpy.types.UNITY_RENAME_MT_presets.bl_label)
        row.operator("scene.unity_preset_add", text="", icon='ZOOMIN')
        row.operator("scene.unity_preset_add", text="", icon='ZOOMOUT').remove_active = True

        col2.prop(scene, 'unity_preview_renaming', toggle=True)

        if (scene.unity_preview_renaming and scene.unity_active_export_group_index < len(groups)):

            group = groups[scene.unity_active_export_group_index]

            for o in group.objects:
                row = col2.row (align=True)
                row.active=o.unity_use_rename

                row.prop (o, "name", text='')
                row.label (rename (scene.unity_export_name_find, scene.unity_export_name_replace, o.name))
                row.prop (o, "unity_use_rename", icon='FILE_TEXT', text='')



        # Export

        # get export counts
        num = 0
        num_actions = 0

        for group in groups:

            if group is not None:

                if group.unity_export:
                    num += 1

                if group.unity_animation:
                    for act in group.unity_actions:
                        if act.export:
                            num_actions += 1

        plural = "Group"

        if num != 1:
            plural = "Groups"

        plural_actions = "Action"

        if num_actions != 1:
            plural_actions = "Actions"

        # layout

        layout.separator ()
        box = layout.box()
        #box.label(text='Export')

        row = box.row ()

        row.label("Export path")
        row.prop(scene, 'unity_global_scale', text='Scale')

        row = box.row (align=True)

        row.operator(GuessExportPath.bl_idname, text=(''), icon='AUTO')
        row.prop(scene, 'unity_export_path', text="")
        row.prop(scene, 'unity_make_path', text='', icon='NEWFOLDER')
        # for blender standard - col.prop(scene, 'unity_forward_axis')

        column = box.column()
        column.enabled = len(groups) > 0

        col = box.column (align=True)
        col.prop(scene, "use_custom_exporter", toggle=True)

        row = col.row (align=True)
        row.prop(scene, "unity_use_duplis", toggle=True)
        row.prop(scene, "unity_use_libraries", toggle=True)

        col = box.column ()

        col.operator(ExportGroupsToFBX.bl_idname, text='Export %d %s to FBX (Y-Up)' % (num, plural), icon='GROUP')

        col.operator(ExportActionsForUnity.bl_idname, text='Export %d %s to FBX (Y-Up)' % (num_actions, plural_actions), icon='ACTION')



        # Export referenced textures

        layout.separator ()
        box = layout.box()

        box.label(text='Export Texture Path')
        row = box.row (align=True)
        row.operator(GuessTextureExportPath.bl_idname, text=(''), icon='AUTO')
        row.prop(scene, 'unity_texture_export_path', text="")
        row.prop(scene, 'unity_make_path', text='', icon='NEWFOLDER')

        col = box.column()
        col.enabled = len(groups) > 0

        plural = "Group's" if num == 1 else "Groups'"

        col.operator(ExportGroupsTextures.bl_idname, text='Export %d %s Textures' % (num, plural), icon='TEXTURE')

class UNITY_PT_Object(bpy.types.Panel):
    bl_label = 'Unity Export Properties'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_default_closed = False

    def draw (self, context):

        layout = self.layout
        scene = context.scene
        obj = context.active_object

        layout.prop(obj, 'unity_export')
        layout.prop(obj, 'unity_use_actions')

type = bpy.types

def update_frame_range (self, context):

    if self.show_frame_range:
        context.scene.frame_start = self.start_frame
        context.scene.frame_end = self.end_frame

class UnityExportAction(bpy.types.PropertyGroup):
    expanded = bpy.props.BoolProperty(name="Expanded", default=False, options={'SKIP_SAVE'})

    action_name = bpy.props.StringProperty(name="Action Name", default="")

    optimize = bpy.props.BoolProperty(name="Optimize Action", default=True)
    export = bpy.props.BoolProperty(name="Export Action", default=True)

    start_frame = bpy.props.IntProperty(name="Start Frame", default=0, update=update_frame_range)
    end_frame = bpy.props.IntProperty(name="End Frame", default=0, update=update_frame_range)
    show_frame_range = bpy.props.BoolProperty(name="Show range", default=False, update=update_frame_range)

class UnityExportActionObject(bpy.types.PropertyGroup):
    object_name = bpy.props.StringProperty(name="Object Name", default="")

def register():

    bpy.utils.register_module(__name__)

    # scene

    type.Scene.show_all_scenes = BoolProperty(name='All Scenes', description='Show groups/objects in all scenes', default=True)
    type.Scene.unity_export_path = StringProperty(name='Export Path', description='Location to export files to', subtype='DIR_PATH')
    type.Scene.unity_make_path = BoolProperty(name='Make Paths', description='Creates missing folders defined by export path and subpaths', default=True)
    type.Scene.unity_use_libraries = BoolProperty(name='Export Libraries', description='Export externally linked groups', default=False)
    type.Scene.unity_use_duplis = BoolProperty(name='Export Duplis', description='Export Dupli-Types as meshes, disables all Dupli-Types when off', default=False)
    type.Scene.unity_hide_external_groups = BoolProperty(name='Hide External Groups', description='Hide groups that are linked to external files', default=True)
    type.Scene.unity_only_export_action_objects = BoolProperty(name='Only include action objects', description='Only exports objects defined in the action objects list', default=True)
    type.Scene.unity_forward_axis = EnumProperty(name='Direction', items=(('Z', "Forward", ""),('-Z', "-Forward", "")), default='Z')
    type.Scene.unity_global_scale = FloatProperty(name='Global Scale', default=1, min=0)
    type.Scene.unity_active_export_group_index = IntProperty(name='Active Export Group Index', default=0, min=0)

    type.Scene.unity_export_name_find = StringProperty(name='Export Find', description='Regular expression pattern to rename all objects on export', default="")
    type.Scene.unity_export_name_replace = StringProperty(name='Export Replace', description='Replace regex string with this', default="")
    type.Scene.unity_preview_renaming = BoolProperty(name='Preview Renaming', description='Preview renaming on current group', default=False, options={'SKIP_SAVE'})

    type.Scene.use_custom_exporter = BoolProperty(name='Use Custom Exporter', description='Use the old Unity Exporter with better y-up exporter', default=False)

    # texture export

    type.Scene.unity_texture_export_path = StringProperty(name='Export Path', description='Location to export files to', subtype='DIR_PATH')
    type.Scene.unity_texture_guess_path_relative = BoolProperty(name='Relative Path', description='Guess path as relative', default=True)

    # shape keys

    type.Key.unity_export = BoolProperty(name='Export ShapeKey', description='ShapeKey is to be exported', default=False)
    type.Key.unity_prefix = StringProperty(name='Prefix', description='')

    # actions

    type.Action.unity_export = BoolProperty(name='Export Action', description='Action is to be exported', default=False)
    type.Action.unity_optimize = BoolProperty(name='Optimize Action', description='Action is to be optimized', default=True)
    type.Action.unity_group = StringProperty(name='Action Group', description='Group action will be exported with', default="")

    # objects

    type.Object.unity_export = BoolProperty(name='Export Object', description='Include Object in Unity Export', default=True)
    type.Object.unity_use_actions = BoolProperty(name='Apply Actions on Export', description='Include actions on the object', default=True)
    type.Object.unity_use_rename = BoolProperty(name='Rename on Export', description='Rename this object and data on export', default=True)

    # groups

    type.Group.unity_export = BoolProperty(name='Export Group', description='Group is to be exported', default=True)
    type.Group.unity_show_advanced = BoolProperty(name='Show Advanced Options', description='Show Advanced options in UI', default=False, options={'SKIP_SAVE'})
    type.Group.unity_static_action = StringProperty(name='Static Action', description='Static (Rest Pose) action for object export', default="")

    type.Group.unity_use_export_layers = BoolProperty(name='Use Export Layers', description='Use scene layer mask', default=True)
    type.Group.unity_export_layers = BoolVectorProperty(name='Export Layers', description='List of scene layers to include in this group', size=20, default=(True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True), subtype='LAYER')

    type.Group.unity_use_subpath = BoolProperty(name='Use Export Subpath', description='Use the subpath on this group', default=False)
    type.Group.unity_subpath = StringProperty(name='Export Subpath', description='Location prefix to file name')

    type.Group.unity_head = StringProperty(name='Group Head', description='Main object in the group')
    type.Group.unity_collapse = BoolProperty(name='Collapse', description='Collapse group before export (needs group head)', default=False)

    type.Group.unity_show_objects = BoolProperty(name='Show Export Objects', description='Shows Objects in this Group to be Exported', default=False, options={'SKIP_SAVE'})

    type.Group.unity_animation = BoolProperty(name='Export Animation', description='Export Animation in this group', default=True)
    type.Group.unity_actions = CollectionProperty(name='Export Actions', type=UnityExportAction, description='Actions to export with this group')
    type.Group.unity_action_objects = CollectionProperty(name='Export Action Objects', type=UnityExportActionObject, description='Objects in this group to apply animations to')

    type.Group.unity_optimize = BoolProperty(name='Optimize Animation', description='Optimize Animation in this group', default=True)
    type.Group.unity_disable_blend_shapes = BoolProperty(name='Disable Blend Shapes', description='Zero all blend shapes in this group', default=True)

def unregister():
    #del type.Scene.unity_export_path
    #del type.Action.unity_export
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
