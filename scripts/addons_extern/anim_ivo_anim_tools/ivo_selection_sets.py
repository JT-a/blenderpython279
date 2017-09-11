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

#
#  Written by Ivo Grigull
#  http://ivogrigull.com
#  http://character-rigger.com
#

import bpy
from bpy.types import PropertyGroup, Operator, Panel
from bpy.props import (
    BoolProperty, CollectionProperty, IntProperty,
    PointerProperty, StringProperty
)


def deselect_all_posebones_here():
    ob = bpy.context.active_object
    for n in ob.pose.bones:
        n.bone.select = False


def select_posebone_here(bone):

    ob = bpy.context.active_object

    if isinstance(bone, bpy.types.PoseBone):
        bone = bone.bone  # get bone instead of posebone
    elif isinstance(bone, str):  # string type
        try:
            bone = ob.data.bones[bone]
        except:
            return

    bone.select = True
    ob.data.bones.active = bone


class bone_selection_sets_add(Operator):

    '''Add selection set'''

    bl_idname = "object.bone_selection_sets_add"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        sets = ob.bone_selection_sets.sets

        sets.add()
        new_set = sets[len(sets) - 1]
        new_set.name = 'group%d' % len(sets)

        ob.bone_selection_sets.index = len(sets) - 1

        return {'FINISHED'}


class bone_selection_sets_remove(Operator):

    '''Remove selection set'''

    bl_idname = "object.bone_selection_sets_remove"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        index = ob.bone_selection_sets.index
        sets = ob.bone_selection_sets.sets

        sets.remove(index)

        if index > len(sets) - 1:
            index -= 1

        return {'FINISHED'}


class bone_selection_set_assign(Operator):

    '''Assign bones to active selection set'''

    bl_idname = "object.bone_selection_set_assign"
    bl_label = "Assign"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        index = ob.bone_selection_sets.index
        set = ob.bone_selection_sets.sets[index]

        for n in ob.data.bones:
            if n.select:
                set.list.add()
                entry = set.list[len(set.list) - 1]
                entry.bone_name = n.name

        return {'FINISHED'}


class bone_selection_set_remove(Operator):

    '''Remove bones from active selection set'''

    bl_idname = "object.bone_selection_set_remove"
    bl_label = "Remove"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        ob = context.active_object
        index = ob.bone_selection_sets.index
        set = ob.bone_selection_sets.sets[index]

        for n in ob.data.bones:
            if n.select:
                name = n.name

                remove_list = []
                for i in range(len(set.list)):
                    if set.list[i].bone_name == name:
                        # remove_list.append(i)
                        set.list.remove(i)
                        break

        return {'FINISHED'}


class bone_selection_set_select(Operator):

    '''Select bones from active selection set'''

    bl_idname = "object.bone_selection_set_select"
    bl_label = "Select"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        index = ob.bone_selection_sets.index
        set = ob.bone_selection_sets.sets[index]

        if ob.bone_selection_sets.use_replace:
            deselect_all_posebones_here()

        for n in set.list:
            try:
                select_posebone_here(ob.data.bones[n.bone_name])
            except:
                pass

        context.scene.frame_current = context.scene.frame_current

        return {'FINISHED'}


class deselect_all_bones(Operator):

    '''Deselect all bones'''

    bl_idname = "object.deselect_all_bones"
    bl_label = "Deselect all bones"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        ob = context.active_object

        if ob.type == 'ARMATURE':
            for n in ob.data.bones:
                n.select = False

            ob.data.bones.active = None
            context.scene.frame_current = context.scene.frame_current

        return {'FINISHED'}


class VIEW3D_PT_tools_bone_selection_sets(Panel):

    """"""

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Animation'
    bl_context = "posemode"
    bl_label = "Bone selection sets"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        # XXX: Improper data access. See API docs for details on
        # template_list() args.
        row.template_list("Selection Sets", "sets", obj.bone_selection_sets, "index", obj.active_selection_set, rows=5)

        col = row.column()
        sub = col.column(align=True)
        sub.operator("object.bone_selection_sets_add", icon='ZOOMIN', text="")
        sub.operator("object.bone_selection_sets_remove", icon='ZOOMOUT', text="")

        row = layout.row()
        try:
            row.prop(obj.bone_selection_sets.sets[obj.bone_selection_sets.index], "name")
        except:
            pass

        row = layout.row()
        row.prop(obj.bone_selection_sets, "use_replace")
        row.operator('object.deselect_all_bones')

        row = layout.row()
        row.operator('object.bone_selection_set_assign')
        row.operator('object.bone_selection_set_remove')

        row = layout.row()
        row.operator('object.bone_selection_set_select')


class bone_selection_set_entry(PropertyGroup):

    @classmethod
    def register(cls):
        cls.bone_name = StringProperty(name="Name", description="", maxlen=40, default="")

    @classmethod
    def unregister(cls):
        del cls.bone_name


class bone_selection_set(PropertyGroup):

    @classmethod
    def register(cls):
        cls.name = StringProperty(name="Name", description="", maxlen=40, default="")
        cls.list = CollectionProperty(type=cls, name="entries", description="")

    @classmethod
    def unregister(cls):
        del cls.name
        del cls.list


class c_bone_selection_sets(PropertyGroup):

    @classmethod
    def register(cls):
        bpy.types.Object.bone_selection_sets = PointerProperty(
            name="Selection Sets",
            description="List of bones for quicker selecting",
            type=cls
        )
        cls.index = IntProperty(
            name="Index",
            description="",
            default=0,
            min=-1, max=65535
        )
        cls.sets = CollectionProperty(
            type=bone_selection_set,
            name="List",
            description="List of bones for quicker selecting"
        )
        cls.use_replace = BoolProperty(
            name="Replace selection",
            description="",
            default=True
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Object.bone_selection_sets


classes = (
    bone_selection_set_entry,
    bone_selection_set,
    c_bone_selection_sets,
    bone_selection_sets_add,
    bone_selection_sets_remove,
    bone_selection_set_assign,
    bone_selection_set_remove,
    bone_selection_set_select,
    deselect_all_bones,
    VIEW3D_PT_tools_bone_selection_sets
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:

        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
