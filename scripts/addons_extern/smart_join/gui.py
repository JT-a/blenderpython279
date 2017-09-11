__author__ = 'andrejivanis'
# BEGIN GPL LICENSE BLOCK #####
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
# END GPL LICENSE BLOCK #####

if "bpy" in locals():
    import imp
    imp.reload(core)
    imp.reload(joiner)
else:
    from . import core, joiner

import bpy
from bpy.props import *

class ExpandSjoin(bpy.types.Operator):
    bl_idname = "sjoin.expand"
    bl_label = "Expand Smart Join"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        ao = context.active_object
        if not ao:
            return False
        return core.check_is_sjoin_obj(ao) and not core.check_is_expended(ao)

    def execute(self, context):
        ao = context.active_object
        core.expand_objects(ao, context.scene)

        # somthing changes active object
        ao.select = True
        context.scene.objects.active = ao
        return {'FINISHED'}


def get_first_sjoin_parent(obj):
    robj = obj
    while True:
        if not robj:
            return None
        if core.check_is_expended(robj):
            return robj
        robj = robj.parent


def check_not_expanded_sjoin(context, obj):
    # can be done for multiple meshes with state
    return core.check_is_sjoin_obj(obj)


class CollapseSjoin(bpy.types.Operator):
    bl_idname = "sjoin.collapse"
    bl_label = "Collapse Smart Join"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        ao = context.active_object
        if not ao:
            return False
        return get_first_sjoin_parent(ao)

    def execute(self, context):

        # with expanded collapsed state i can use whole selection as ao
        ao = context.active_object
        scn = context.scene
        obj = get_first_sjoin_parent(ao)

        core.collect_children(obj, scn)
        obj.select = True
        scn.objects.active = obj
        return {'FINISHED'}

class SJoinObjects(bpy.types.Operator):
    bl_idname = "sjoin.join_add"
    bl_label = "Add To Smart Join"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # TODO: if I don't respect len(context.selected_objects) > 1 everything disappears
        return core.check_is_sjoin_obj(context.active_object) and len(context.selected_objects) > 1

    def execute(self, context):
        scn = context.scene
        core.update_lock = True


        active = context.active_object




        # if active is sjoin add others to it
        # TODO: make it work, currently poll is limeted so this isn't called
        if not core.check_is_sjoin_obj(active):
            ac_cop_obj = active.copy()

            for c in active.children:
                if c in context.selected_objects:
                    parent_keep_tr(c, ac_cop_obj, scn)

            ac_cop_mesh = active.data.copy()

            scn.objects.link(ac_cop_obj)
            ac_cop_obj.data = ac_cop_mesh
            ac_cop_obj.select = True

        active.select = False

        selected = context.selected_objects[:]

        '''
        # find what to parent j_object to
        highest = active
        while highest.parent in selected:
            highest = highest.parent


        # create new s_join mesh at the position of active object
        active.data.is_sjoin = True
        active.parent = highest.parent
        '''

        #parerent the selection and merge it
        for o in selected:
            if o.parent not in selected:
                parent_keep_tr(o, active, scn)
                # o.matrix_parent_inverse = j_obj.matrix_world.inverted()

        if not core.check_is_expended(active):
            core.expand_objects(active, context.scene)
            core.collect_children(active, scn)


        core.update_lock = False
        active.select = True

        return {'FINISHED'}


def parent_keep_tr(obj, parent, scn):
    w = obj.matrix_world.copy()
    obj.parent = parent
    scn.update()
    obj.matrix_world = w

class SJoinObjects(bpy.types.Operator):
    bl_idname = "sjoin.join"
    bl_label = "Smart Join"
    bl_options = {'REGISTER', 'UNDO'}


    origin_at_cursor = BoolProperty(default=False, name="Origin At Cursor")

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        core.update_lock = True


        active = context.active_object
        selected = context.selected_objects[:]
        scn = context.scene

        # find what to parent j_object to
        highest = active
        while highest.parent in selected:
            highest = highest.parent

        # create new s_join mesh at the position of active object
        name = active.name + '_sj'
        j_mesh = bpy.data.meshes.new(name = name)
        j_mesh.is_sjoin = True
        j_obj = bpy.data.objects.new(name = name, object_data= j_mesh)
        scn.objects.link(j_obj)
        j_obj.parent = highest.parent
        if self.origin_at_cursor:
            j_obj.location = context.scene.cursor_location
        else:
            j_obj.location = active.matrix_local.to_translation()
        j_obj.layers = active.layers

        j_obj.select = True
        joiner.add_to_loc_view(j_obj, scn)

        scn.objects.active = j_obj
        core.set_object_expended(j_obj)


        #parerent the selection and merge it
        for o in selected:
            if o.parent not in selected:
                parent_keep_tr(o, j_obj, scn)

                # o.matrix_parent_inverse = j_obj.matrix_world.inverted()

        core.collect_children(j_obj, scn)
        core.update_lock = False


        return {'FINISHED'}

class SeparateObjects(bpy.types.Operator):
    bl_idname = "sjoin.separate"
    bl_label = "Separate S.Join"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.ops.sjoin.expand.poll()

    def execute(self, context):
        #TODO this needs to duplicate objects!!!
        active = context.active_object
        data = active.data
        # bpy.ops.sjoin.collapse()
        bpy.ops.sjoin.expand()
        joiner.clear_mesh(data)
        for o in active.children[:]:
            parent_keep_tr(o, active.parent, context.scene)
        active.select = False

        for sc in active.users_scene:
            sc.objects.unlink(active)

        bpy.data.objects.remove(active)
        return {'FINISHED'}

class UpdateRec(bpy.types.Operator):
    bl_idname = "sjoin.update_rec"
    bl_label = "Update S.Join Dependencies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        #TODO this needs to duplicate objects!!!
        for o in context.selected_objects:
            if o.data:
                core.update_data_rec(o.data)
        return {'FINISHED'}


class ApplySJ(bpy.types.Operator):
    bl_idname = "sjoin.apply"
    bl_label = "Apply Smart Join"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and core.check_is_sjoin_obj(context.active_object) and not core.check_is_expended(context.active_object)

    def execute(self, context):
        context.active_object.data.is_sjoin = False
        return {'FINISHED'}

class SJ_BasePanel(bpy.types.Panel):
    bl_label = "Smart Join"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Tools'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator('sjoin.join')
        row.operator('sjoin.separate')
#        layout.operator('sjoin.join_add')
        layout.separator()
        row = layout.row(align=True)
        row.operator('sjoin.expand')
        row.operator('sjoin.collapse')
        layout.operator('sjoin.update_rec')
        layout.operator('sjoin.apply')