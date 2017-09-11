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
    'name': "rInstances",
    'author': "PLyczkowski",
    'version': (1, 0, 0),
    'blender': (2, 7, 6),
    'api': 41270,
    'location': "View3D > Toolbar > Relations",
    'warning': "Addon creates a new scene called rInstance Storage. Please don't touch it!",
    'description': "Convert objects to group instances instantly.",
    'wiki_url': "",
    'tracker_url': "",
    'category': 'Object'}

import bpy
import bmesh
from bpy.props import EnumProperty

RSCENE = "rInstance Storage"
RGROUP = "rGroup"


class TurnToRInstance(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "TODO"
    bl_idname = "object.turn_to_rinstance"
    bl_label = "Selection to Instance"
    bl_options = {'REGISTER', 'UNDO'}

    container_name = bpy.props.StringProperty(name="Name", default="Instance")
    use_rotation_from_active = bpy.props.BoolProperty(name="Rotation from Active", default=True)

    pivot_placement = EnumProperty(
        name="Pivot Placement",
        items=(('MEDIAN', 'Median', ''),
               ('ACTIVE', 'Active', ''),
               ('CURSOR', 'Cursor', '')
               ),
        default='MEDIAN'
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        contents = bpy.context.selected_objects
        active = bpy.context.scene.objects.active

        storeCursorX = context.space_data.cursor_location.x
        storeCursorY = context.space_data.cursor_location.y
        storeCursorZ = context.space_data.cursor_location.z

        if self.pivot_placement == "MEDIAN":
            bpy.ops.view3d.snap_cursor_to_selected()
        elif self.pivot_placement == "ACTIVE":
            bpy.ops.view3d.snap_cursor_to_active()

        # store rotation
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        empty_rotation_saver = bpy.context.active_object
        empty_rotation_saver.rotation_euler = active.rotation_euler

        # add empty
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        empty_obj = bpy.context.active_object

        # copy rotation from active
        if self.use_rotation_from_active:
            bpy.ops.object.select_all(action='DESELECT')
            empty_obj.select = True
            empty_obj.rotation_euler = empty_rotation_saver.rotation_euler

        # Parent the contents to empty
        for obj in contents:
            obj.select = True
            obj.parent = empty_obj
        bpy.context.scene.objects.active = empty_obj
        empty_obj.select = True
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

        # move to center
        bpy.ops.object.select_all(action='DESELECT')
        empty_obj.select = True
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()

        # unparent
        bpy.ops.object.select_all(action='DESELECT')
        for obj in contents:
            obj.select = True
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        # delete empty
        bpy.ops.object.select_all(action='DESELECT')
        empty_obj.select = True
        bpy.ops.object.delete(use_global=False)

        # add group
        bpy.ops.object.select_all(action='DESELECT')
        for obj in contents:
            obj.select = True
        bpy.ops.group.create(name=RGROUP)

        # get newest rgroup
        group = bpy.context.selected_objects[0].users_group[0]

        # Try to get or create new rscene
        rscene = get_or_create_rscene(context)

        # move to an rscene
        bpy.ops.object.select_all(action='DESELECT')
        for obj in contents:
            obj.select = True
            bpy.ops.object.make_links_scene(scene=RSCENE)
            bpy.ops.object.delete(use_global=False)

        # add instace
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        instance_empty = bpy.context.scene.objects.active
        bpy.context.object.name = self.container_name
        bpy.context.object.empty_draw_size = 0.01
        bpy.context.object.dupli_type = 'GROUP'
        bpy.context.object.dupli_group = bpy.data.groups[group.name]
        instance_empty["is_rcontainer"] = True

        # restore rotation
        if self.use_rotation_from_active:
            bpy.context.object.rotation_euler = empty_rotation_saver.rotation_euler

        # clean up
        bpy.ops.object.select_all(action='DESELECT')
        empty_rotation_saver.select = True
        bpy.ops.object.delete(use_global=False)
        bpy.ops.object.clean_up_rinstances()

        # restore cursor
        context.space_data.cursor_location.x = storeCursorX
        context.space_data.cursor_location.y = storeCursorY
        context.space_data.cursor_location.z = storeCursorZ

        # select instance
        instance_empty.select = True

        return {'FINISHED'}


class ReleaseRInstance(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "TODO"
    bl_idname = "object.release_rinstance"
    bl_label = "Release Selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        selected = bpy.context.selected_objects
        rscene = get_rscene(context)
        current_scene = bpy.context.window.screen.scene

        bpy.ops.object.select_all(action='DESELECT')

        for obj in selected:

            # make sure it's an rinstance
            if obj.get('is_rcontainer') is not None and obj.type == "EMPTY" and obj.dupli_type == 'GROUP':

                # get rinstance
                target_rinstance = obj

                # get target rgroup
                target_rgroup = obj.dupli_group

                bpy.ops.object.empty_add(type='PLAIN_AXES')
                instance_replacement_empty = bpy.context.scene.objects.active
                instance_replacement_empty.rotation_euler = target_rinstance.rotation_euler
                instance_replacement_empty.location = target_rinstance.location
                bpy.ops.object.select_all(action='DESELECT')

                # switch to rscene
                bpy.context.window.screen.scene = rscene

                # deselect all
                bpy.ops.object.select_all(action='DESELECT')

                # select if in rgroup
                for obj in rscene.objects:

                    for group in obj.users_group:  # All groups on object

                        if group == target_rgroup:

                            obj.select = True

                bpy.ops.object.make_links_scene(scene=current_scene.name)

                # switch back to current scene
                bpy.context.window.screen.scene = current_scene

                # currently selected - linked from rscene
                bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=False, material=False, texture=False, animation=False)
                rgroup_contents = bpy.context.selected_objects

                # # make single user which also removes from rgroup
                # bpy.ops.object.select_all(action='DESELECT')
                # for obj in rgroup_contents:
                # 	obj.select=True
                # 	bpy.context.scene.objects.active = obj

                # parent to empty
                bpy.ops.object.select_all(action='DESELECT')
                bpy.ops.object.empty_add(type='PLAIN_AXES')
                relocation_empty = bpy.context.scene.objects.active

                # parent rgroup contents to relocation empty
                for obj in rgroup_contents:
                    obj.parent = relocation_empty

                # relocate to instance replacement empty
                relocation_empty.location = instance_replacement_empty.location
                relocation_empty.rotation_euler = instance_replacement_empty.rotation_euler

                # unparent rgroup contents
                bpy.ops.object.select_all(action='DESELECT')
                for obj in rgroup_contents:
                    obj.select = True
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

                # clean up
                bpy.ops.object.select_all(action='DESELECT')
                instance_replacement_empty.select = True
                relocation_empty.select = True
                target_rinstance.select = True
                bpy.ops.object.delete(use_global=False)

        # TODO reselect the rinstances contents here

        bpy.ops.object.clean_up_rinstances()

        return {'FINISHED'}

# TODO

# class OpenRInstance(bpy.types.Operator):
# 	'''Tooltip'''
# 	bl_description = "TODO"
# 	bl_idname = "object.release_rinstance"
# 	bl_label = "Release Selected"
# 	bl_options = {'REGISTER', 'UNDO'}

# 	@classmethod
# 	def poll(cls, context):
# 		return True

# 	def execute(self, context):

# 		selected = bpy.context.selected_objects
# 		rscene = get_rscene(context)
# 		current_scene = bpy.context.window.screen.scene

# 		bpy.ops.object.select_all(action='DESELECT')

# 		for obj in selected:

# 			# make sure it's an rinstance
# 			if obj.get('is_rcontainer') is not None and obj.type == "EMPTY" and obj.dupli_type == 'GROUP':

# 				# get rinstance
# 				target_rinstance = obj

# 				# get target rgroup
# 				target_rgroup = obj.dupli_group

# 		bpy.ops.object.clean_up_rinstances()

# 		return {'FINISHED'}


class RInstancesToObjects(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "TODO"
    bl_idname = "object.rinstances_to_objects"
    bl_label = "Instances to Objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        # replace make_real with manual duplicate objects from group and place over instances

        # make duplicates real
        for obj in bpy.context.selected_objects:

            if obj.get('is_rcontainer') is not None:

                bpy.ops.object.duplicates_make_real()

        selected = bpy.context.selected_objects

        # remove empties
        for obj in selected:

            if obj.get('is_rcontainer') is not None:

                bpy.ops.object.select_all(action='DESELECT')
                obj.select = True
                bpy.ops.object.delete(use_global=False)

        # reselect rest
        for obj in selected:
            obj.select = True

        bpy.ops.object.clean_up_rinstances()

        return {'FINISHED'}


class CleanUpRInstances(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Deletes all objects in the storage that do not have an instance."
    bl_idname = "object.clean_up_rinstances"
    bl_label = "Clean Up Instances"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        rscene = get_rscene(context)
        current_scene = bpy.context.window.screen.scene

        selected = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')

        bpy.context.window.screen.scene = rscene

        bpy.ops.object.select_all(action='DESELECT')

        if rscene is not None:

            for obj in rscene.objects:  # All objects in rscene

                got_instance = False

                for group in obj.users_group:  # All groups on object

                    # if RGROUP in group.name:

                    for obj2 in bpy.data.objects:

                        if obj2.type == "EMPTY" and obj2.dupli_type == 'GROUP' and obj2.dupli_group == group:

                            got_instance = True

                if got_instance == False:

                    print("RContainer object " + obj.name + " is orphaned, deleting.")
                    obj.select = True
                    bpy.ops.object.delete()

        bpy.context.window.screen.scene = current_scene

        # reselect what was selected
        for obj in selected:
            obj.select = True

        return {'FINISHED'}


def get_rscene(context):
    rscene_name = RSCENE

    if rscene_name in bpy.data.scenes:
        return bpy.data.scenes[rscene_name]
    else:
        return None


def get_or_create_rscene(context):
    rscene_name = RSCENE

    if rscene_name in bpy.data.scenes:
        return bpy.data.scenes[rscene_name]
    else:
        return bpy.data.scenes.new(rscene_name)
    return None


class addButtonsInObjectMode(bpy.types.Panel):
    bl_idname = "rInstances"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Relations"

    bl_label = "rInstances"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)

        col.operator("object.turn_to_rinstance")
        col.operator("object.release_rinstance")
        col = layout.column(align=True)
        col.operator("object.rinstances_to_objects")


def register():

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
