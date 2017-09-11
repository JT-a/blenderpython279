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
from bpy.props import IntProperty
from bpy.types import Operator


class timeline_jogwheel_modal(Operator):

    '''Modal jogwheel for the timeline'''

    bl_idname = "scene.timeline_jogwheel_modal"
    bl_label = "Modal timeslider"

    frame = IntProperty()
    first_mouse_x = IntProperty()

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.properties.first_mouse_x - event.mouse_x
            context.scene.frame_current = int(self.properties.frame + delta * -0.1)

        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in ('RIGHTMOUSE', 'ESC'):
            context.scene.frame_current = self.properties.frame
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.scene:
            context.window_manager.modal_handler_add(self)
            self.properties.first_mouse_x = event.mouse_x
            self.properties.frame = context.scene.frame_current
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


classes = (
    timeline_jogwheel_modal,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
