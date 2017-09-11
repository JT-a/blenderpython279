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
    'name': 'Custom Keymap',
    'author': 'chromoly',
    'version': (0, 1, 1),
    'blender': (2, 78, 0),
    'location': '',
    'description': 'Add keymap items',
    'warning': '',
    'category': 'User Interface'}


import functools
import traceback

import bpy

from .utils import addongroup


class CustomKeyMapPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__


class VIEW3D_OT_view_selected_no_zoom(bpy.types.Operator):
    bl_label = 'View Selected no zoom'
    bl_idname = 'view3d.view_selected_no_zoom'
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        v3d = context.space_data
        cursor_bak = v3d.cursor_location[:]
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.view3d.view_center_cursor()
        v3d.cursor_location = cursor_bak
        return {'FINISHED'}


class TRANSFORM_OT_select_translate(bpy.types.Operator):
    bl_label = 'Activate/Select/Translate'
    bl_idname = 'transform.select_translate'
    bl_options = {'REGISTER'}

    select = bpy.props.BoolProperty(
        name='Select',
        default=True,
        options={'SKIP_SAVE'}
    )
    toggle = bpy.props.BoolProperty(
        name='Toggle Selection',
        default=False,
        options={'SKIP_SAVE'}
    )

    @classmethod
    def poll(cls, context):
        return bpy.ops.view3d.select.poll()

    def invoke(self, context, event):
        if self.select:
            bpy.ops.view3d.select(context.copy(), 'INVOKE_DEFAULT',
                                  toggle=self.toggle)

        kwargs = {'release_confirm': True}
        wm = context.window_manager
        constraint_axis = [False, False, False]
        if hasattr(wm, 'view3d_transform_constraint'):
            if context.area.type == 'VIEW_3D':
                for ax in wm.view3d_transform_constraint:
                    constraint_axis[['X', 'Y', 'Z'].index(ax)] = True
        if not all(constraint_axis) and any(constraint_axis):
            kwargs['constraint_axis'] = constraint_axis
        ret = bpy.ops.transform.translate(
            context.copy(), 'INVOKE_DEFAULT', **kwargs)

        context.area.tag_redraw()
        return ret


class TRANSFORM_OT_translate_mod(bpy.types.Operator):
    bl_label = 'Translate Mod'
    bl_idname = 'transform.translate_mod'
    bl_options = {'REGISTER'}

    @classmethod
    def header_draw(cls, self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.window_manager, 'view3d_transform_constraint',
                 text='')

    @classmethod
    def register(cls):
        bpy.types.WindowManager.view3d_transform_constraint = \
            bpy.props.EnumProperty(
                name='Transform Constraint',
                items=(('X', 'X', ''),
                       ('Y', 'Y', ''),
                       ('Z', 'Z', ''),
                       ('XY', 'XY', ''),
                       ('XZ', 'XZ', ''),
                       ('YZ', 'YZ', ''),
                       ('XYZ', 'XYZ', '')),
                default='XYZ',
                options={'SKIP_SAVE'}
            )

        bpy.types.VIEW3D_HT_header.append(cls.header_draw)

    @classmethod
    def unregister(cls):
        bpy.types.VIEW3D_HT_header.remove(cls.header_draw)
        del bpy.types.WindowManager.view3d_transform_constraint

    @classmethod
    def poll(cls, context):
        return bpy.ops.transform.translate.poll()

    def invoke(self, context, event):
        wm = context.window_manager
        constraint_axis = [False, False, False]
        if context.area.type == 'VIEW_3D':
            for ax in wm.view3d_transform_constraint:
                constraint_axis[['X', 'Y', 'Z'].index(ax)] = True
        kwargs = {}
        if not all(constraint_axis) and any(constraint_axis):
            kwargs['constraint_axis'] = constraint_axis
        return bpy.ops.transform.translate(context.copy(), 'INVOKE_DEFAULT',
                                           **kwargs)


class WM_OT_context_set_enum_redraw(bpy.types.Operator):
    bl_label = 'Context Set Enum'
    bl_idname = 'wm.context_set_enum_redraw'
    bl_options = {'REGISTER', 'INTERNAL'}

    data_path = bpy.props.StringProperty(options={'SKIP_SAVE'})
    value = bpy.props.StringProperty(options={'SKIP_SAVE'})

    def invoke(self, context, event):
        import traceback
        try:
            ls = self.data_path.split('.')
            obj = eval('context.' + '.'.join(ls[:-1]))
            attr = ls[-1]
            setattr(obj, attr, self.value)
        except:
            traceback.print_exc()
        for area in context.screen.areas:
            area.tag_redraw()
        return {'FINISHED'}


class ToggleTranslateINterface(bpy.types.Operator):
    bl_label = 'Toggle Translate Interface'
    bl_idname = 'wm.toggle_translate_interface'

    def invoke(self, context, event):
        U = context.user_preferences
        if U.system.use_translate_interface and \
                U.system.use_translate_tooltips:
            U.system.use_translate_interface = False
            U.system.use_translate_tooltips = False
        else:
            U.system.use_translate_interface = True
            U.system.use_translate_tooltips = True
        return {'FINISHED'}


classes = [
    CustomKeyMapPreferences,
    VIEW3D_OT_view_selected_no_zoom,
    TRANSFORM_OT_select_translate,
    TRANSFORM_OT_translate_mod,
    WM_OT_context_set_enum_redraw,
    ToggleTranslateINterface
]


def new_keymap_item(kmname, *args, **kwargs):
    km = CustomKeyMapPreferences.get_keymap(kmname)
    return km.keymap_items.new(*args, **kwargs)


@CustomKeyMapPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    kc = bpy.context.window_manager.keyconfigs.addon
    if not kc:
        return

    ## Screen
    add = functools.partial(new_keymap_item, 'Screen')
    # add('screen.redo_last', 'F6', 'PRESS')  # 何故か消えてたので
    add('screen.redo_last', 'F19', 'PRESS')
    add('screen.redo_last', 'F18', 'PRESS')
    # add('screen.redo_last', 'BUTTON5MOUSE', 'PRESS')

    add('screen.screen_full_area', 'F', 'PRESS', oskey=True)

    add(ToggleTranslateINterface.bl_idname, 'F6', 'PRESS', ctrl=True)
    
    ## View3D
    add = functools.partial(new_keymap_item, '3D View')

    kmi = add(TRANSFORM_OT_select_translate.bl_idname, 'SELECTMOUSE', 'PRESS',
              oskey=True)
    kmi = add(TRANSFORM_OT_select_translate.bl_idname, 'SELECTMOUSE', 'PRESS',
              shift=True, oskey=True)
    kmi.properties.toggle = True
    kmi = add(TRANSFORM_OT_select_translate.bl_idname, 'ACTIONMOUSE', 'PRESS',
              oskey=True)
    kmi.properties.select = False

    # Constraint Axis
    kmi = add(WM_OT_context_set_enum_redraw.bl_idname,
              'ONE', 'PRESS', oskey=True)
    kmi.properties.data_path = 'window_manager.view3d_transform_constraint'
    kmi.properties.value = 'X'
    kmi = add(WM_OT_context_set_enum_redraw.bl_idname,
              'ONE', 'PRESS', shift=True, oskey=True)
    kmi.properties.data_path = 'window_manager.view3d_transform_constraint'
    kmi.properties.value = 'YZ'

    kmi = add(WM_OT_context_set_enum_redraw.bl_idname,
              'TWO', 'PRESS', oskey=True)
    kmi.properties.data_path = 'window_manager.view3d_transform_constraint'
    kmi.properties.value = 'Y'
    kmi = add(WM_OT_context_set_enum_redraw.bl_idname,
              'TWO', 'PRESS', shift=True, oskey=True)
    kmi.properties.data_path = 'window_manager.view3d_transform_constraint'
    kmi.properties.value = 'XZ'

    kmi = add(WM_OT_context_set_enum_redraw.bl_idname,
              'THREE', 'PRESS', oskey=True)
    kmi.properties.data_path = 'window_manager.view3d_transform_constraint'
    kmi.properties.value = 'Z'
    kmi = add(WM_OT_context_set_enum_redraw.bl_idname,
              'THREE', 'PRESS', shift=True, oskey=True)
    kmi.properties.data_path = 'window_manager.view3d_transform_constraint'
    kmi.properties.value = 'XY'

    kmi = add(WM_OT_context_set_enum_redraw.bl_idname,
              'FOUR', 'PRESS', oskey=True)
    kmi.properties.data_path = 'window_manager.view3d_transform_constraint'
    kmi.properties.value = 'XYZ'

    kmi = add('transform.translate_mod', 'G', 'PRESS')
    kmi = add('transform.translate_mod', 'EVT_TWEAK_S', 'ANY', any=True)


    # kmi = add('view3d.viewnumpad', 'A', 'PRESS', oskey=True)
    # kmi.properties.type = 'FRONT'
    # kmi = add('view3d.viewnumpad', 'S', 'PRESS', oskey=True)
    # kmi.properties.type = 'RIGHT'
    # kmi = add('view3d.viewnumpad', 'Q', 'PRESS', oskey=True)
    # kmi.properties.type = 'TOP'
    # kmi = add('view3d.viewnumpad', 'A', 'PRESS', ctrl=True, oskey=True)
    # kmi.properties.type = 'BACK'
    # kmi = add('view3d.viewnumpad', 'S', 'PRESS', ctrl=True, oskey=True)
    # kmi.properties.type = 'LEFT'
    # kmi = add('view3d.viewnumpad', 'Q', 'PRESS', ctrl=True, oskey=True)
    # kmi.properties.type = 'BOTTOM'
    # kmi = add('view3d.viewnumpad', 'F', 'PRESS', oskey=True)
    # kmi.properties.type = 'CAMERA'
    # kmi = add('view3d.object_as_camera', 'F', 'PRESS', ctrl=True, oskey=True)
    # kmi = add('view3d.view_persportho', 'D', 'PRESS', oskey=True)
    # kmi = add('view3d.localview', 'W', 'PRESS', oskey=True)
    #
    # kmi = add('view3d.viewnumpad', 'A', 'PRESS', shift=True, oskey=True)
    # kmi.properties.align_active = True
    # kmi.properties.type = 'FRONT'
    # kmi = add('view3d.viewnumpad', 'S', 'PRESS', shift=True, oskey=True)
    # kmi.properties.align_active = True
    # kmi.properties.type = 'RIGHT'
    # kmi = add('view3d.viewnumpad', 'Q', 'PRESS', shift=True, oskey=True)
    # kmi.properties.align_active = True
    # kmi.properties.type = 'TOP'
    # kmi = add('view3d.viewnumpad', 'A', 'PRESS', shift=True, ctrl=True,
    #           oskey=True)
    # kmi.properties.align_active = True
    # kmi.properties.type = 'BACK'
    # kmi = add('view3d.viewnumpad', 'S', 'PRESS', shift=True, ctrl=True,
    #           oskey=True)
    # kmi.properties.align_active = True
    # kmi.properties.type = 'LEFT'
    # kmi = add('view3d.viewnumpad', 'Q', 'PRESS', shift=True, ctrl=True,
    #           oskey=True)
    # kmi.properties.align_active = True
    # kmi.properties.type = 'BOTTOM'
    
    kmi = add('wm.context_toggle_enum', 'Q', 'PRESS')
    kmi.properties.data_path = 'space_data.pivot_point'
    kmi.properties.value_1 = 'CURSOR'
    kmi.properties.value_2 = 'BOUNDING_BOX_CENTER'
    kmi = add('wm.context_toggle_enum', 'Q', 'PRESS', shift=True)
    kmi.properties.data_path = 'space_data.pivot_point'
    kmi.properties.value_1 = 'MEDIAN_POINT'
    kmi.properties.value_2 = 'ACTIVE_ELEMENT'

    try:
        kmi = add('view3d.view_orbit', 'NUMPAD_6', 'PRESS', shift=True,
                  ctrl=True)
        kmi.properties.type = 'ORBITCCW'
        kmi = add('view3d.view_orbit', 'NUMPAD_4', 'PRESS', shift=True,
                  ctrl=True)
        kmi.properties.type = 'ORBITCW'
    except:
        traceback.print_exc()

    ## Mesh
    add = functools.partial(new_keymap_item, 'Mesh')

    # kmi = add('wm.context_toggle', 'D', 'PRESS', alt=True)
    # kmi.properties.data_path = 'space_data.use_occlude_geometry'

    # kmi = add('mesh.select_linked', 'BUTTON16MOUSE', 'PRESS', ctrl=True)
    # kmi = add('mesh.select_linked_pick', 'BUTTON16MOUSE', 'PRESS')
    # kmi.properties.deselect = False
    # kmi = add('mesh.select_linked_pick', 'BUTTON16MOUSE', 'PRESS', shift=True)
    # kmi.properties.deselect = True

    kmi = add('mesh.select_more', 'WHEELUPMOUSE', 'PRESS', ctrl=True, oskey=True)
    kmi = add('mesh.select_less', 'WHEELDOWNMOUSE', 'PRESS', ctrl=True,
              oskey=True)

    ## Layer
    try:
        add = functools.partial(new_keymap_item, '3D View')
        kmi = add('view3d.layers', 'ATKEY', 'PRESS')
        kmi.properties.nr = 0
        add = functools.partial(new_keymap_item, 'Armature')
        kmi = add('armature.layers_show_all', 'ATKEY', 'PRESS', ctrl=True)
        add = functools.partial(new_keymap_item, 'Pose')
        kmi = add('armature.layers_show_all', 'ATKEY', 'PRESS', ctrl=True)
    except:
        pass

    bl_rna = bpy.types.Event.bl_rna

    # if 'BUTTON5MOUSE' in bl_rna.properties['type'].enum_items:
    add = functools.partial(new_keymap_item, 'Outliner')
    kmi = add('outliner.show_active', 'BUTTON5MOUSE', 'PRESS')

    # if 'F13' not in bl_rna.properties['type'].enum_items:
    #     return

    # Lキーに該当するもの
    add = functools.partial(new_keymap_item, 'Grease Pencil Stroke Edit Mode')
    kmi = add('gpencil.select_linked', 'F13', 'PRESS')
    kmi = add('gpencil.select_linked', 'F13', 'PRESS', ctrl=True)

    add = functools.partial(new_keymap_item, 'Face Mask')
    kmi = add('paint.face_select_linked', 'F13', 'PRESS', ctrl=True)
    kmi = add('paint.face_select_linked_pick', 'F13', 'PRESS')
    kmi.properties.deselect = False
    kmi = add('paint.face_select_linked_pick', 'F13', 'PRESS',
              shift=True)
    kmi.properties.deselect = True

    add = functools.partial(new_keymap_item, 'Pose')
    kmi = add('pose.select_linked', 'F13', 'PRESS')
    kmi = add('poselib.browse_interactive', 'F13', 'PRESS',
              ctrl=True)
    kmi = add('poselib.pose_add', 'F13', 'PRESS', shift=True)
    kmi = add('poselib.pose_remove', 'F13', 'PRESS', alt=True)
    kmi = add('poselib.pose_rename', 'F13', 'PRESS',
              shift=True, ctrl=True)

    add = functools.partial(new_keymap_item, 'Object Mode')
    kmi = add('object.select_linked', 'F13', 'PRESS', shift=True)
    kmi = add('wm.call_menu', 'F13', 'PRESS', ctrl=True)
    kmi.properties.name = 'VIEW3D_MT_make_links'
    kmi = add('object.make_local', 'F13', 'PRESS')

    add = functools.partial(new_keymap_item, 'Curve')
    kmi = add('curve.select_linked', 'F13', 'PRESS', ctrl=True)
    kmi = add('curve.select_linked_pick', 'F13', 'PRESS')
    kmi.properties.deselect = False
    kmi = add('curve.select_linked_pick', 'F13', 'PRESS', shift=True)
    kmi.properties.deselect = True

    add = functools.partial(new_keymap_item, 'Sculpt')
    kmi = add('paint.brush_select', 'F13', 'PRESS')

    add = functools.partial(new_keymap_item, 'Mesh')
    kmi = add('mesh.select_linked', 'F13', 'PRESS', ctrl=True)
    kmi = add('mesh.select_linked_pick', 'F13', 'PRESS')
    kmi.properties.deselect = False
    kmi = add('mesh.select_linked_pick', 'F13', 'PRESS', shift=True)
    kmi.properties.deselect = True

    add = functools.partial(new_keymap_item, 'Armature')
    kmi = add('armature.select_linked', 'F13', 'PRESS')

    add = functools.partial(new_keymap_item, 'Particle')
    kmi = add('particle.select_linked', 'F13', 'PRESS')
    kmi.properties.deselect = False
    kmi = add('particle.select_linked', 'F13', 'PRESS', shift=True)
    kmi.properties.deselect = True

    add = functools.partial(new_keymap_item, 'UV Editor')
    kmi = add('uv.select_linked', 'F13', 'PRESS', ctrl=True)
    kmi = add('uv.select_linked_pick', 'F13', 'PRESS')
    kmi = add('uv.select_linked', 'F13', 'PRESS', shift=True,
              ctrl=True)
    kmi.properties.extend = True
    kmi = add('uv.select_linked_pick', 'F13', 'PRESS', shift=True)
    kmi.properties.extend = True

    add = functools.partial(new_keymap_item, 'Mask Editing')
    kmi = add('mask.select_linked', 'F13', 'PRESS', ctrl=True)
    kmi = add('mask.select_linked_pick', 'F13', 'PRESS')
    kmi.properties.deselect = False
    kmi = add('mask.select_linked_pick', 'F13', 'PRESS', shift=True)
    kmi.properties.deselect = True

    add = functools.partial(new_keymap_item, 'Graph Editor')
    kmi = add('graph.select_linked', 'F13', 'PRESS')

    add = functools.partial(new_keymap_item, 'Node Editor')
    # kmi = add('node.nw_modify_labels', 'F13', 'PRESS', shift=True,
    #           alt=True)
    # kmi = add('node.nw_clear_label', 'F13', 'PRESS', alt=True)
    kmi = add('node.select_linked_to', 'F13', 'PRESS', shift=True)
    kmi = add('node.select_linked_from', 'F13', 'PRESS')

    add = functools.partial(new_keymap_item, 'Dopesheet')
    kmi = add('action.select_linked', 'F13', 'PRESS')

    add = functools.partial(new_keymap_item, 'Sequencer')
    kmi = add('sequencer.lock', 'F13', 'PRESS', shift=True)
    kmi = add('sequencer.unlock', 'F13', 'PRESS', shift=True,
              alt=True)
    kmi = add('sequencer.select_linked_pick', 'F13', 'PRESS')
    kmi = add('sequencer.select_linked_pick', 'F13', 'PRESS',
              shift=True)
    kmi.properties.extend = True
    kmi = add('sequencer.select_linked', 'F13', 'PRESS',
              ctrl=True)

    add = functools.partial(new_keymap_item, 'Clip Editor')
    kmi = add('clip.lock_tracks', 'F13', 'PRESS', ctrl=True)
    kmi.properties.action = 'LOCK'
    kmi = add('clip.lock_tracks', 'F13', 'PRESS', alt=True)
    kmi.properties.action = 'UNLOCK'
    kmi = add('wm.context_toggle', 'F13', 'PRESS')
    kmi.properties.data_path = 'space_data.lock_selection'

    add = functools.partial(new_keymap_item, 'Clip Graph Editor')
    kmi = add('wm.context_toggle', 'F13', 'PRESS')
    kmi.properties.data_path = 'space_data.lock_time_cursor'


@CustomKeyMapPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
