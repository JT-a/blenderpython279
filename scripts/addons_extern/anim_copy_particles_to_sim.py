bl_info = {
    "name": "Copy Particles to Rigid Bodies",
    "version": (0, 0, 8),
    "blender": (2, 6, 8),
    "location": "View3D > Tool Shelf",
    "description": "Transfers dupliobjects from a PS to a Rigid Bodies simulation",
    "author": "Liero (on blenderartist), Eli Spizzichino",
    "category": "Animation",
}

import bpy
import random
from mathutils import *
from math import *


def generic_copy(source, target, skip_props=("bl_rna", "name", "rna_type", "type")):
    """ copy attributes from source to target """
    for attr in dir(source):
        if attr.startswith("_") or attr in skip_props:
            continue
        setattr(target, attr, getattr(source, attr))
    return

# code modified from modifierTools tears of steel


def copy_animation(source, target, offset=0):
    if source.animation_data and source.animation_data.action:
        action = source.animation_data.action
        for fcu in action.fcurves:
            # create new animation data if needed
            if not target.animation_data:
                target.animation_data_create()

            # if there's no action assigned to selected object
            # create new one
            if not target.animation_data.action:
                action_name = target.name + "Action"
                bpy.data.actions.new(name=action_name)
                action2 = bpy.data.actions[action_name]
                target.animation_data.action = action2
            else:
                action2 = target.animation_data.action

            # delete existing curve if present
            for fcu2 in action2.fcurves:
                if fcu2.data_path == fcu.data_path:
                    action2.fcurves.remove(fcu2)
                    break

            # create new fcurve
            fcu2 = action2.fcurves.new(data_path=fcu.data_path,
                                       index=fcu.array_index)
            fcu2.color = fcu.color

            # create keyframes
            fcu2.keyframe_points.add(len(fcu.keyframe_points))

            # copy keyframe settings
            for x in range(len(fcu.keyframe_points)):
                point = fcu.keyframe_points[x]
                point2 = fcu2.keyframe_points[x]

                point2.co = point.co + Vector([offset, 0])
                point2.handle_left = point.handle_left + Vector([offset, 0])
                point2.handle_left_type = point.handle_left_type
                point2.handle_right = point.handle_right + Vector([offset, 0])
                point2.handle_right_type = point.handle_right_type

    return {'FINISHED'}


class Particles_to_Sim(bpy.types.Operator):
    bl_idname = 'object.particles_to_simulation'
    bl_label = 'Copy Particles'
    bl_description = 'Transfers dupliobjects from a PS to a Rigid Bodies simulation'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = bpy.context.object
        return(obj and obj.particle_systems)

    def execute(self, context):
        wm = bpy.context.window_manager
        scn = bpy.context.scene
        fps = scn.render.fps
        obj = bpy.context.object
        set = obj.particle_systems[0].settings
        par = obj.particle_systems[0].particles
        txt = 'Set Particle System dupliobject to a Rigid Body object / group'

        # disable simulation
        scn.rigidbody_world.enabled = False

        # to avoid PS cache troubles
        obj.particle_systems[0].seed += 1

        # get dupliobject from particles system
        if set.render_type == 'OBJECT':
            duplist = [set.dupli_object]
        elif set.render_type == 'GROUP':
            duplist = set.dupli_group.objects[:]
        else:
            self.report({'ERROR'}, txt)
            return{'FINISHED'}

        # check if dupliobjects are valid
        for d in duplist:
            if not d.rigid_body:
                self.report({'ERROR'}, txt)
                return{'FINISHED'}

        # an Empty as parent allows to move / rotate later
        bpy.ops.object.add(type='EMPTY')
        bpy.context.object.name = 'Bullet Particles'
        bpy.ops.object.select_all(action='DESELECT')
        root = scn.objects.active
        delta = obj.location * wm.use_loc
        root.location = delta
        for i, p in enumerate(par):
            print("%i off %i particles" % (i, len(par)))
            dup = random.choice(duplist)
            born_time = round(p.birth_time, 2)
            die_time = round(p.die_time, 2)

            scn.frame_set(born_time)
            phy = bpy.data.objects.new('particle.000', dup.data)
            scn.objects.link(phy)
            scn.objects.active = phy  # ..?
            phy.select = True
            phy.rotation_euler = p.rotation.to_euler()
            bpy.ops.rigidbody.objects_add(type='ACTIVE')
            scn.frame_set(scn.frame_current)  # ..?
            phy.parent = root

            # copy sub particle system
            dup.select = True
            scn.objects.active = dup
            fake_context = bpy.context.copy()
            fake_context["object"] = phy
            bpy.ops.object.particle_system_add(fake_context)
            psys = phy.particle_systems[-1]
            psys.settings = dup.particle_systems[-1].settings.copy()

            # bpy.ops.object.make_links_data(type='MODIFIERS')
            # bpy.ops.object.copy_obj_mod()
            phy.select = False

            # copy rigid body settings
            generic_copy(dup.rigid_body, phy.rigid_body)

            # keyframe unborn particle
            phy.scale = [p.size] * 3
            phy.location = p.location - delta
            phy.rigid_body.kinematic = True
            phy.keyframe_insert('location', frame=born_time)
            phy.rigid_body.keyframe_insert('kinematic', frame=born_time)

            # keyframe particle pop up
            if not set.show_unborn:
                phy.scale = [0] * 3
                phy.keyframe_insert('scale', frame=born_time - wm.pre_frames)
                phy.scale = [p.size] * 3
                phy.keyframe_insert('scale', frame=born_time)

            # keyframe alive particle
            phy.location += p.velocity / fps * wm.vel_mult
            phy.keyframe_insert('location', frame=born_time + 1)
            phy.rigid_body.kinematic = False
            phy.rigid_body.keyframe_insert('kinematic', frame=born_time + 2)

            if wm.use_field:
                # offset subparticle start, end and emitter visibility
                psys_set = psys.settings
                random_offset = random.randrange(0, 100) * wm.field_offset_rand
                field_offset = wm.field_offset + random_offset
                if wm.field_offset_born:
                    field_offset += born_time - 1
                elif wm.field_offset_die:
                    field_offset += born_time + die_time - 2
                psys_set.frame_end += field_offset
                psys_set.frame_start += field_offset

                # subparticle emitter visibility
                psys_set.use_render_emitter = True
                psys_set.keyframe_insert('use_render_emitter', frame=field_offset - wm.pre_frames)
                psys_set.use_render_emitter = False
                psys_set.keyframe_insert('use_render_emitter', frame=field_offset)

                # create field copy
                if not wm.field_obj:
                    continue
                field_obj = bpy.data.objects[wm.field_obj]

                if field_obj.field.type is not 'NONE':
                    origin = Vector([0] * 3)
                    bpy.ops.object.select_all(action='DESELECT')
                    field_obj.select = True
                    # bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False})
                    bpy.ops.object.effector_add(type=field_obj.field.type, location=origin, rotation=phy.rotation_euler)
                    new_field = bpy.context.active_object  # scn.objects.active
                    generic_copy(field_obj.field, new_field.field)
                    copy_animation(field_obj, new_field, field_offset)
                    if wm.field_follows:
                        new_field.parent = phy
                        new_field.location += Vector([random.choice([random.random(), - random.random()])] * 3) * wm.field_rand_loc
                    else:
                        new_field.parent = root
                        new_field.location += phy.location

                else:
                    self.report({'ERROR'}, "selected object is not a field type")

            bpy.ops.object.select_all(action='DESELECT')
        # hide emmitter
        obj.hide = obj.hide_render = True
        scn.frame_set(scn.frame_start)
        bpy.ops.object.select_all(action='DESELECT')
        scn.objects.active = root
        root.select = True

        # enable simulation
        scn.rigidbody_world.enabled = True

        return{'FINISHED'}


class PanelP2RB(bpy.types.Panel):
    bl_label = '...Particles to Simulation'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    @classmethod
    def poll(cls, context):
        obj = bpy.context.object
        return(obj and obj.particle_systems)

    def draw(self, context):
        wm = bpy.context.window_manager
        scn = bpy.context.scene
        obj = bpy.context.object
        set = obj.particle_systems[0].settings
        layout = self.layout
        layout.operator('object.particles_to_simulation')
        layout.prop(wm, 'use_loc')
        column = layout.column(align=True)
        column.prop(wm, 'vel_mult')
        if not set.show_unborn:
            column.prop(wm, 'pre_frames')
        column.separator()
        column.prop(scn.rigidbody_world, "use_split_impulse")
        column.separator()
        box = layout.box()
        box.prop(wm, 'use_field', text="Use force field")
        subbox = box.box()
        subbox.enabled = wm.use_field
        column = subbox.column(align=True)
        column.label("Force field to duplicate")
        column.prop_search(wm, "field_obj", scn, "objects", text='', icon='FORCE_FORCE')
        row = subbox.row()
        column.label(text="Random position the force field")
        column.prop(wm, 'field_rand_loc')

        subbox = layout.box()
        column = subbox.column()
        column.label(text="Offset all the animation")
        col_b = subbox.column()
        col_b.prop(wm, 'field_offset_born')
        col_b.enabled = not wm.field_offset_die
        col_d = subbox.column()
        col_d.prop(wm, 'field_offset_die')
        col_d.enabled = not wm.field_offset_born
        col_offset = subbox.column()
        col_offset.prop(wm, 'field_offset')
        col_offset.prop(wm, 'field_offset_rand')


bpy.types.WindowManager.vel_mult = bpy.props.FloatProperty(name='Speed',
                                                           min=0.01, max=50, default=1, description='Particle speed multiplier')
bpy.types.WindowManager.use_loc = bpy.props.BoolProperty(name='Origin at emiter',
                                                         default=True, description='Place simulation root object at emiter start position '
                                                         ', maybe disable for animated emitters')
bpy.types.WindowManager.pre_frames = bpy.props.IntProperty(name='Grow time',
                                                           min=1, max=50, default=1, description='Frames to scale particles before simulating')


# row.prop(part, "factor_random")
bpy.types.WindowManager.use_field = bpy.props.BoolProperty(name='Use Force',
                                                           default=True, description='Add a force field to each copy of the particle')
bpy.types.WindowManager.field_obj = bpy.props.StringProperty()
# bpy.types.WindowManager.field_obj=bpy.props.FloatProperty(name='Random',
#        min=0, max=1, default=0, description='Particle speed multiplier')
bpy.types.WindowManager.field_follows = bpy.props.BoolProperty(name='Field follow particle',
                                                               default=False, description='Parent the new force field to the new created particle')
bpy.types.WindowManager.field_rand_loc = bpy.props.FloatProperty(name='Random Loc',
                                                                 min=0, max=100, default=0, description='Random location multiplier for the field')
bpy.types.WindowManager.field_offset = bpy.props.FloatProperty(name="Offset",
                                                               description="Offset of the animations in frames", default=10.0, soft_max=100.0, soft_min=-100.0, step=100)
bpy.types.WindowManager.field_offset_born = bpy.props.BoolProperty(name='On born offset',
                                                                   default=False, description='Offset the animation when particle Born for sub partcles and fields')
bpy.types.WindowManager.field_offset_die = bpy.props.BoolProperty(name='On die offset',
                                                                  default=True, description='Offset the animation when particle Die for sub partcles and fields')

bpy.types.WindowManager.field_offset_rand = bpy.props.FloatProperty(name='Random',
                                                                    soft_min=-10, soft_max=10, default=0, step=1, description='Random offset of the animation')


def register():
    bpy.utils.register_class(Particles_to_Sim)
    bpy.utils.register_class(PanelP2RB)


def unregister():
    bpy.utils.unregister_class(Particles_to_Sim)
    bpy.utils.unregister_class(PanelP2RB)

if __name__ == '__main__':
    register()
