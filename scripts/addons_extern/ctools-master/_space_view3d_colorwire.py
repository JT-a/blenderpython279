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
    'name': 'Color Wire',
    'author': 'chromoly',
    'version': (0, 2, 1),
    'blender': (2, 78, 0),
    'location': 'View3D > Shift + Ctrl + D',
    'category': '3D View'}


import bpy

from .utils import addongroup


dtdict = {'BOUNDBOX': 0, 'WIREFRAME': 1, 'SOLID': 2, 'TEXTURED': 3}


class VIEW3D_OT_color_wire_toggle(bpy.types.Operator):
    bl_idname = 'view3d.color_wire_toggle'
    bl_label = 'Toggle Color Wire'
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        v3d = bpy.context.space_data
        dt = v3d.viewport_shade
        if dtdict[dt] <= dtdict['WIREFRAME']:
            v3d.use_color_wire ^= True
        else:
            v3d.use_color_wire_solid ^= True
        return {'FINISHED'}


class VIEW3D_OT_color_wire_copy_color(bpy.types.Operator):
    bl_idname = 'view3d.color_wire_copy_color'
    bl_label = 'Copy Wire Color'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        if not (context.active_object and context.selected_objects):
            return {'FINISHED'}

        usewcol = context.active_object.use_color_wire
        wcol = context.active_object.wire_color
        for ob in context.selected_objects:
            ob.use_color_wire = usewcol
            for i in range(3):
                ob.wire_color[i] = wcol[i]

        return {'FINISHED'}


class VIEW3D_OT_color_wire_select_same_color(bpy.types.Operator):
    bl_idname = 'view3d.color_wire_select_same_color'
    bl_label = 'select by Wire Color'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        if not (context.active_object and context.selected_objects):
            return {'FINISHED'}

        #usewcol = context.active_object.use_color_wire
        wcol = context.active_object.wire_color
        for ob in context.visible_objects:
            if not ob.select:
                for i in range(3):
                    if ob.wire_color[i] != wcol[i]:
                        break
                else:
                    ob.select = True
        return {'FINISHED'}


class VIEW3D_MT_color_wire(bpy.types.Menu):
    #bl_idname = 'view3d.color_wire_menu'
    bl_label = 'Color Wire'

    def draw(self, context):
        v3d = context.space_data
        cwstate = [v3d.use_color_wire, v3d.use_color_wire_solid]
        ls = ['', '']
        ls[0] = 'ON' if cwstate[0] else 'OFF'
        ls[1] = 'ON' if cwstate[1] else 'OFF'
        dt = v3d.viewport_shade
        if dtdict[dt] <= dtdict['WIREFRAME']:
            ls[0] = '[' + ls[0] + ']'
        else:
            ls[1] = '[' + ls[1] + ']'

        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator('view3d.color_wire_toggle',
                        text='Toggle ({0}, {1})'.format(*ls))
        layout.operator('view3d.color_wire_copy_color',
                        text='Copy wire color')
        layout.operator('view3d.color_wire_select_same_color',
                        text='Select same color')


addon_keymaps = []


def register():
    addongroup.AddonGroup.register_module(__name__)
    km = addongroup.AddonGroup.get_keymap('3D View')
    if km:
        kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS',
                                  shift=True, ctrl=True, alt=True)
        kmi.properties.name = 'VIEW3D_MT_color_wire'
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    addongroup.AddonGroup.unregister_module(__name__)


if __name__ == '__main__':
    register()
