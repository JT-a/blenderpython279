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
    'name': 'Utility Menu',
    'author': 'chromoly',
    'version': (0, 0, 4),
    'blender': (2, 78, 0),
    'location': 'View3D > Mouse > Menu',
    'description': '',
    'warning': '',
    'category': '3D View'}


import bpy

from .utils import addongroup
from .utils.vaarmature import get_visible_bones, get_selected_bones


class CONSTRAINT_OT_childof_set_inverse(bpy.types.Operator):
    bl_idname = 'constraint.childof_set_inverse_selected'
    bl_label = 'Set Inverse'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode in ('OBJECT', 'POSE')
    
    def execute(self, context=None):
        if context.mode == 'OBJECT':
            for base in context.selected_bases:
                ob = base.object
                for con in ob.constraints:
                    if con.type == 'CHILD_OF':
                        c = context.copy()
                        c['active_object'] = c['object'] = ob
                        c['active_base'] = base
                        c['constraint'] = con
                        bpy.ops.constraint.childof_set_inverse(c,
                                        constraint=con.name, owner='OBJECT')
                        ob.update_tag({'OBJECT', 'DATA'})
        elif context.mode == 'POSE':
            base = context.active_base
            ob = base.object
            arm = ob.data
            bone = arm.bones.active
            for pbone in context.selected_pose_bones:
                for con in pbone.constraints:
                    if con.type == 'CHILD_OF':
                        arm.bones.active = pbone.bone
                        c = context.copy()
                        c['constraint'] = con
                        bpy.ops.constraint.childof_set_inverse(c,
                                        constraint=con.name, owner='BONE')
            arm.bones.active = bone
            ob.update_tag({'OBJECT', 'DATA'})

        return {'FINISHED'}
    

class OBJECT_OT_apply_modifiers(bpy.types.Operator):
    ''' Apply selected object modifiers '''
    bl_description = 'Apply selected object modifiers'
    bl_idname = 'object.apply_modifiers'
    bl_label = 'Apply Modifiers'
    bl_options = {'REGISTER', 'UNDO'}

    apply_armature = bpy.props.BoolProperty(
        name='Apply Armature Modifiers',
        default=False)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects

    def execute(self, context=None):
        scn = context.scene
        actob = scn.objects.active
        for ob in context.selected_objects:
            scn.objects.active = ob
            modifier_names = [mod.name for mod in ob.modifiers]
            for name in modifier_names:
                if ob.modifiers[name].type == 'ARMATURE':
                    if self.apply_armature:
                        bpy.ops.object.modifier_apply(modifier=name)
                else:
                    bpy.ops.object.modifier_apply(modifier=name)
        scn.objects.active = actob
        return {'FINISHED'}

    '''def invoke(self, context=None, event=None):
        # Invoke the operator.
        # Return type: enum in [‘RUNNING_MODAL’, ‘CANCELLED’, ‘FINISHED’, ‘PASS_THROUGH’]
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}
    '''


class ARMATURE_OT_set_armature_properties(bpy.types.Operator):
    '''Set Armature options'''
    bl_label = 'Set Armature Options'
    bl_idname = 'armature.set_armature_properties'
    bl_options = {'REGISTER', 'UNDO'}

    mode = bpy.props.EnumProperty(
        items=(('no', '--', ''),
               ('OBJECT', 'Object Mode', ''),
               ('POSE', 'Pose Mode', '')),
        name='Mode',
        description='',
        default='no')
    pose_position = bpy.props.EnumProperty(
        items=(('no', '--', ''),
               ('POSE', 'Pose Position', ''),
               ('REST', 'Rest Position', '')),
        name='Pose Position',
        description='',
        default='no')
    draw_type = bpy.props.EnumProperty(
        items=(('no', '--', ''),
               ('OCTAHEDRAL', 'Octahedral', ''),
               ('STICK', 'Stick', ''),
               ('BBONE', 'B-Bone', ''),
               ('ENVELOPE', 'Envelope', '')),
        name='Display Type',
        description='',
        default='no')
    show_names = bpy.props.EnumProperty(
        items=(('no', '--', ''),
               ('draw', 'Draw Name', ''),
               ('hide', 'Hide Name', '')),
        name='Display Name',
        description='',
        default='no')
    show_axes = bpy.props.EnumProperty(
        items=(('no', '--', ''),
               ('draw', 'Draw Axes', ''),
               ('hide', 'Hide Axes', '')),
        name='Display Axes',
        description='',
        default='no')

    @classmethod
    def poll(cls, context):
        armobs = [ob for ob in context.selected_objects if \
                  ob.type == 'ARMATURE']
        return len(armobs) >= 1

    def execute(self, context):
        selobs = [ob for ob in context.selected_objects if \
                                                         ob.type == 'ARMATURE']
        if not selobs:
            return {'FINISHED'}
        actob = context.active_object
        for ob in selobs:
            arm = ob.data
            if self.mode != 'no':
                if context.active_object.mode != 'EDIT':
                    context.scene.objects.active = ob
                    bpy.ops.object.mode_set(mode=self.mode)
            if self.pose_position != 'no':
                arm.pose_position = self.pose_position
            if self.draw_type != 'no':
                arm.draw_type = self.draw_type
            if self.show_names != 'no':
                arm.show_names = True if self.show_names == 'draw' else False
            if self.show_axes != 'no':
                arm.show_axes = True if self.show_axes == 'draw' else False
        if self.mode != 'no' and actob:
            context.scene.objects.active = actob
        return {'FINISHED'}

    def draw(self, context=None):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        col = layout.column()
        col.label('Mode:')
        sub = col.row()
        sub.prop(self, 'mode', text='Mode', expand=True)
        col.label('Pose State:')
        sub = col.row()
        sub.prop(self, 'pose_position', text='Pose State', expand=True)
        col.label('Draw Type:')
        sub = col.row()
        sub.prop(self, 'draw_type', text='Draw Type', expand=True)
        col.label('Draw Names:')
        sub = col.row()
        sub.prop(self, 'show_names', text='Draw Names', expand=True)
        col.label('Draw Axes:')
        sub = col.row()
        sub.prop(self, 'show_axes', text='Draw Axes', expand=True)
        col = layout.column()

    def invoke(self, context=None, event=None):
        wm = context.window_manager
        wm.invoke_props_dialog(self)
        return {'RUNNING_MODAL'}


class OBJECT_OT_copy_pose_constraints(bpy.types.Operator):
    ''' copy pose bone's constraints from linked active object '''
    # ObjectModeとPoseModeで動作
    bl_description = ''
    bl_idname = 'object.copy_pose_constraints'
    bl_label = 'Copy pose bone constraints'
    bl_options = {'REGISTER', 'UNDO'}

    all_linked = bpy.props.BoolProperty(
        name='All linked armatures',
        description='All Linked Armatures instead selected',
        default=False)

    @classmethod
    def poll(cls, context):
        actob = context.active_object
        return actob and actob.type == 'ARMATURE' and \
                                               actob.mode in ('OBJECT', 'POSE')

    def execute(self, context=None):
        actob = context.active_object
        if not actob or actob.type != 'ARMATURE':
            return {'FINISHED'}

        if self.all_linked:
            obs = [ob for ob in bpy.data.objects if ob.data == actob.data]
        else:
            obs = [ob for ob in context.selected_objects \
                   if ob.data == actob.data]
        if actob in obs:
            obs.remove(actob)

        actpose = actob.pose
        actposebonenames = [bone.name for bone in actpose.bones]
        for ob in obs:
            pose = ob.pose
            for bone in pose.bones:
                for con in [con for con in bone.constraints]:
                    bone.constraints.remove(con)
                constraints = actpose.bones[bone.name].constraints
                for con in constraints:
                    newcon = bone.constraints.new(con.type)
                    for item in dir(con):
                        try:
                            setattr(newcon, item, getattr(con, item))
                        except:
                            pass
        return {'FINISHED'}

    '''
    def invoke(self, context=None, event=None):
        return {'FINISHED'}
    '''


def get_armature_objects(context):
    obs = [ob for ob in context.selected_objects if ob.type == 'ARMATURE']
    actob = context.active_object
    if actob and actob not in obs:
        obs.append(actob)
    return obs


class POSE_OT_reset_transform(bpy.types.Operator):
    ''' reset Loction, Rotation, Scale '''
    bl_description = 'Reset loction, rotation, scale. ' + \
                     '(when PoseMode, only selected)'
    bl_idname = 'pose.reset_transform'
    bl_label = 'Reset Transform'
    bl_options = {'REGISTER', 'UNDO'}

    allbones = bpy.props.BoolProperty(
        name='Also Hidden and not Selected', default=False)
    loc = bpy.props.BoolProperty(name='Location', default=False)
    rot = bpy.props.BoolProperty(name='Rotation', default=False)
    scale = bpy.props.BoolProperty(name='Scale', default=False)

    @classmethod
    def poll(cls, context):
        obs = get_armature_objects(context)
        return obs and context.mode in ('OBJECT', 'POSE')

    def execute(self, context=None):
        obs = get_armature_objects(context)
        for ob in obs:
            arm = ob.data
            #for bone in [b for b in ob.pose.bones if bone_is_visible(arm, b)]:
            if self.allbones:
                bones = ob.pose.bones
            else:
                if context.mode == 'OBJECT':
                    bones = get_visible_bones(ob, mode='POSE')
                else:
                    bones = get_selected_bones(ob, mode='POSE')
            for bone in bones:
                if self.loc:
                    for i in range(3):
                        if not bone.lock_location[i]:
                            bone.location[i] = 0
                if self.rot:
                    for i in range(3):
                        if not bone.lock_rotation[i]:
                            bone.rotation_quaternion[i + 1] = 0
                    if bone.rotation_mode in ('QUATERNION', 'AXIS_ANGLE'):
                        if bone.lock_rotations_4d and not bone.lock_rotation_w:
                            bone.rotation_quaternion[0] = 1
                if self.scale:
                    for i in range(3):
                        if not bone.lock_scale[i]:
                            bone.scale[i] = 1

        return {'FINISHED'}

    '''
    def invoke(self, context=None, event=None):
        return {'FINISHED'}
    '''


class POSE_OT_set_driver_target_as_self(bpy.types.Operator):
    ''' '''
    bl_description = ''
    bl_idname = 'pose.set_driver_target_as_self'
    bl_label = 'Set driver target as self'
    bl_options = {'REGISTER', 'UNDO'}

    fc_select = bpy.props.BoolProperty(
        name='Selected FCurve only', default=False)

    @classmethod
    def poll(cls, context):
        obs = get_armature_objects(context)
        return obs and context.mode in ('OBJECT', 'POSE')

    def execute(self, context=None):
        obs = get_armature_objects(context)
        for ob in obs:
            for fcurve in ob.animation_data.drivers:
                # fcurve.data_path == 'pose.bones["Bone.002"].constraints["IK"].influence'
                if not self.fc_select or self.fc_select and fcurve.select:
                    for variable in fcurve.driver.variables:
                        for target in variable.targets:
                            if target.id_type == 'OBJECT':
                                target.id = ob
        return {'FINISHED'}

    '''
    def invoke(self, context=None, event=None):
        return {'FINISHED'}
    '''


class VIEW3D_MT_utilities_object(bpy.types.Menu):
    bl_label = 'Object'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN' # call invoke

        #actob = context.active_object
        #selobs = context.selected_objects
        '''op = layout.operator('view3d.rename_objects',
                             text='Rename Objects', icon='OBJECT_DATA')
        op.mode = context.mode
        '''
#         layout.menu('OBJECT_MT_align_to_active_object', icon='MANIPUL')
        op = layout.operator('object.apply_modifiers', icon='MODIFIER')


class VIEW3D_MT_utilities_armature(bpy.types.Menu):
    bl_label = "Armature"
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN' # call invoke

        #actob = context.active_object
        #selobs = context.selected_objects
        '''op = layout.operator('view3d.rename_objects', text='Rename Bones',
                             icon='BONE_DATA')
        op.mode = context.mode
        '''
        op = layout.operator('armature.set_armature_properties',
                             text='Set Options', icon='POSE_HLT')
        op = layout.operator('object.copy_pose_constraints',
                             text='Sync linked armature constraints',
                             icon='CONSTRAINT')
        op = layout.operator('pose.reset_transform',
                             text='Reset Bones Transform',
                             icon='MANIPUL')
        op.loc = op.rot = op.scale = True
        op = layout.operator('pose.set_driver_target_as_self',
                             text='Set driver target as self',
                             icon='OBJECT_DATA')


class VIEW3D_MT_utilities(bpy.types.Menu):
    '''Custom Menu'''
    bl_label = 'Utilities'
    #bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        retval = False
        actob = context.active_object
        if actob:
            if actob.mode == 'EDIT':
                retval = True
        if context.mode in ('OBJECT', 'POSE'):
            retval = True
        return retval

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN' # call invoke

        '''
        actob = context.active_object
        selobs = context.selected_objects
        if context.mode in ('POSE', 'EDIT_ARMATURE'):
            op = layout.operator('view3d.rename_objects',
                                 text='Rename Bones')
            op.mode = context.mode
        else:
            op = layout.operator('view3d.rename_objects',
                                 text='Rename Objects')
            op.mode = context.mode
        #op = layout.operator('view3d.rename_bones',
        #                     text='Raname Bones')
        op = layout.operator('view3d.set_armature_properties',
                             text='Set Armature Options')
        '''
        if context.mode in ('POSE', 'EDIT_ARMATURE'):
            label = 'Rename Bones'
            mode = context.mode
        else:
            label = 'Rename Objects'
            mode = 'OBJECT'
        op = layout.operator('object.rename_objects', text=label,
                             icon='BONE_DATA')
        op.mode = mode
        
        layout.operator('constraint.childof_set_inverse_selected',
                        text='ChildOf Set Inverse',
                        icon='CONSTRAINT')
        
        layout.menu('VIEW3D_MT_utilities_object', icon='OBJECT_DATA')
        layout.menu('VIEW3D_MT_utilities_armature',
                    icon='OUTLINER_OB_ARMATURE')


addon_keymaps = []


def register():
    addongroup.AddonGroup.register_module(__name__)

    km = addongroup.AddonGroup.get_keymap('3D View')
    if km:
        kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS', shift=True,
                                  ctrl=True)
        kmi.properties.name = 'VIEW3D_MT_utilities'
        addon_keymaps.append((km, kmi))


def unregister():
    addongroup.AddonGroup.unregister_module(__name__)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == '__main__':
    register()
