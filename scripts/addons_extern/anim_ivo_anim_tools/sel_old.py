import bpy
from bpy.props import *


def deselect_all_posebones():
    ob = bpy.context.active_object
    for n in ob.pose.bones:
        n.bone.select = False


def select_posebone(bone):

    ob = bpy.context.active_object

    if type(bone) == bpy.types.PoseBone:
        bone = bone.bone  # get bone instead of posebone
    elif type(bone) == type(str()):  # string type
        try:
            bone = ob.data.bones[bone]
        except:
            return

    #~ deselect_all_posebones()
    bone.select = True
    ob.data.bones.active = bone


class selection_set_entry(bpy.types.IDPropertyGroup):
    bone_name = StringProperty(name="Name", description="", maxlen=40, default="")


class selection_set(bpy.types.IDPropertyGroup):
    pass

selection_set.name = StringProperty(name="Name", description="", maxlen=40, default="")
#~ selection_set.list = CollectionProperty(type=StringProperty, name="entry", description="")
selection_set.list = CollectionProperty(type=selection_set_entry, name="entries", description="")
#~ selection_set.list = []


class c_selection_sets(bpy.types.IDPropertyGroup):
    pass

c_selection_sets.index = IntProperty(name="Index", description="", default=0, min=-1, max=65535)
c_selection_sets.sets = CollectionProperty(type=selection_set, name="List", description="List of bones for quicker selecting")
c_selection_sets.use_replace = BoolProperty(name="Replace selection", description="", default=True)


bpy.types.Armature.selection_sets = PointerProperty(type=c_selection_sets, name="Selection Sets", description="List of bones for quicker selecting")


class selection_sets_add(bpy.types.Operator):
    '''Add selection set'''
    bl_idname = "armture.selection_sets_add"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ob = context.active_object
        sets = ob.data.selection_sets.sets

        sets.add()
        new_set = sets[len(sets) - 1]
        new_set.name = 'group%d' % len(sets)

        ob.data.selection_sets.index = len(sets) - 1

        return {'FINISHED'}


class selection_sets_remove(bpy.types.Operator):
    '''Remove selection set'''
    bl_idname = "armture.selection_sets_remove"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ob = context.active_object
        index = ob.data.selection_sets.index
        sets = ob.data.selection_sets.sets

        sets.remove(index)

        if index > len(sets) - 1:
            index -= 1

        return {'FINISHED'}


class selection_set_assign(bpy.types.Operator):
    '''Assign bones to active selection set'''
    bl_idname = "armature.selection_set_assign"  # this is important since its how bpy.ops.export.some_data is constructed
    bl_label = "Assign"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ob = context.active_object
        index = ob.data.selection_sets.index
        set = ob.data.selection_sets.sets[index]

        for n in ob.data.bones:
            if n.select:
                set.list.add()
                entry = set.list[len(set.list) - 1]
                entry.bone_name = n.name

        return {'FINISHED'}


class selection_set_remove(bpy.types.Operator):
    '''Remove bones from active selection set'''
    bl_idname = "armature.selection_set_remove"
    bl_label = "Remove"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):

        ob = context.active_object
        index = ob.data.selection_sets.index
        set = ob.data.selection_sets.sets[index]

        for n in ob.data.bones:
            if n.select:

                name = n.name

                remove_list = []
                for i in range(len(set.list)):
                    if set.list[i].bone_name == name:
                        #~ remove_list.append(i)
                        set.list.remove(i)
                        break

                #~ for i in range( len(remove_list) ):
                    #~ set.list.remove(i)

                #~ set.list.add()
                #~ entry = set.list[ len(set.list)-1 ]
                #~ entry.bone_name = n.name

        return {'FINISHED'}


class selection_set_select(bpy.types.Operator):
    '''Select bones from active selection set'''
    bl_idname = "armature.selection_set_select"
    bl_label = "Select"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ob = context.active_object
        index = ob.data.selection_sets.index
        set = ob.data.selection_sets.sets[index]

        if ob.data.selection_sets.use_replace:
            deselect_all_posebones()

        for n in set.list:
            print(n)
            try:
                select_posebone(ob.data.bones[n.bone_name])
            except:
                pass

        return {'FINISHED'}


class deselect_all_bones(bpy.types.Operator):
    '''Deselect all bones'''
    bl_idname = "object.deselect_all_bones"
    bl_label = "Deselect all bones"

    @classmethod
    def poll(cls, context):
        return context.object != None

    def execute(self, context):
        ob = context.active_object

        if ob.type == 'ARMATURE':
            for n in ob.data.bones:
                n.select = False

            ob.data.bones.active = None
            context.scene.frame_current = context.scene.frame_current

        return {'FINISHED'}


#~ class OBJECT_PT_hello(bpy.types.Panel):
    #~ bl_label = "Hello World Panel"
    #~ bl_space_type = "PROPERTIES"
    #~ bl_region_type = "WINDOW"
    #~ bl_context = "object"
#~
class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'


class VIEW3D_PT_tools_ivoanim(View3DPanel, bpy.types.Panel):
    bl_context = "posemode"
    bl_label = "Bone selection sets"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        #~ row = layout.row()
        #~ row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.template_list(obj.data.selection_sets, "sets", obj.data.selection_sets, "index", rows=5)

        col = row.column()
        sub = col.column(align=True)
        sub.operator("armture.selection_sets_add", icon='ZOOMIN', text="")
        sub.operator("armture.selection_sets_remove", icon='ZOOMOUT', text="")

        row = layout.row()
        row.prop(obj.data.selection_sets.sets[obj.data.selection_sets.index], "name")

        row = layout.row()
        #~ col = row.column()

        row.prop(obj.data.selection_sets, "use_replace")
        row.operator('object.deselect_all_bones')

        row = layout.row()
        row.operator('armature.selection_set_assign')
        row.operator('armature.selection_set_remove')

        row = layout.row()
        row.operator('armature.selection_set_select')


def register():
    pass


def unregister():
    pass


if __name__ == "__main__":
    pass
    #~ bpy.ops.object.timeline_jogwheel_modal()
