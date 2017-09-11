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
from bpy.types import Operator, Menu


def main(context):
    data = context.active_object.data
    for n in data.vertices:
        n.co.x += 0.1


class move_op(Operator):

    ''''''

    bl_idname = "object.move_op"
    bl_label = "Ivo move"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return ('FINISHED')


class ivo_subdiv(Operator):

    ''''''

    bl_idname = "object.ivo_subdiv"
    bl_label = "Subdivide"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.modifier_add(type='SUBSURF')
        return ('FINISHED')


class wiretoggle(Operator):

    ''''''

    bl_idname = "object.wiretoggle"
    bl_label = "Ivo wiretoggle"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        ob.show_wire = not ob.show_wire
        return ('FINISHED')


class xraytoggle(Operator):

    ''''''

    bl_idname = "object.xraytoggle"
    bl_label = "Ivo X-Ray toggle"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        ob.show_x_ray = not ob.show_x_ray
        return ('FINISHED')


class ivo_shade_smooth(Operator):

    ''''''

    bl_idname = "object.ivo_shade_smooth"
    bl_label = "Shade smooth"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.shade_smooth()
        return ('FINISHED')


class ivo_reset_transforms(Operator):

    '''Reset current pose bone'''

    bl_idname = "object.ivo_reset_transforms"
    bl_label = "Reset transforms"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        try:
            bpy.ops.pose.rot_clear()
            bpy.ops.pose.loc_clear()
            bpy.ops.pose.scale_clear()
        except:
            bpy.ops.object.rotation_clear()
            bpy.ops.object.scale_clear()
            bpy.ops.object.location_clear()

        return ('FINISHED',)


class ivo_reset_all_transforms(Operator):

    '''Reset all pose bones'''

    bl_idname = "object.ivo_reset_all_transforms"
    bl_label = "Reset all transforms"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = bpy.context.active_object

        for n in ob.pose.bones:
            n.matrix_basis.identity()

        bpy.context.scene.frame_current = bpy.context.scene.frame_current
        return ('FINISHED')


class ivo_armature_show_all_layers(Operator):

    ''''''

    bl_idname = "object.ivo_armature_show_all_layers"
    bl_label = "Show all am Layers"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        for n in range(len(ob.data.layers)):
            ob.data.layers[n] = True

        return ('FINISHED')


class ivo_armature_show_first_layer(Operator):

    ''''''

    bl_idname = "object.ivo_armature_show_first_layer"
    bl_label = "Show first armature layer"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        for n in range(len(ob.data.layers)):
            ob.data.layers[n] = False
        ob.data.layers[0] = True

        return ('FINISHED')


class draw_axis_toggle(Operator):

    ''''''

    bl_idname = "armature.draw_axis_toggle"
    bl_label = "Show axes"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        ob.data.show_axes = not ob.data.show_axes
        return ('FINISHED')


class VIEW3D_MT_ivo(Menu):

    """"""

    bl_label = "Ivo Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        # layout.operator("object.moveOp", text="Move")
        layout.operator("object.wiretoggle", text="Wireframe on shaded")
        layout.operator("object.xraytoggle", text="X-Ray")
        layout.operator("object.ivo_subdiv", text="Subdivide")
        layout.operator("object.ivo_shade_smooth", text="Shade smooth")
        layout.operator("object.ivo_reset_transforms")
        layout.operator("object.ivo_reset_all_transforms")
        layout.operator("object.ivo_armature_show_all_layers")
        layout.operator("armature.draw_axis_toggle")
        layout.operator("object.ivo_armature_show_first_layer")

# the menu can then be called anywhere with:
# layout.menu(VIEW3D_MT_template)

# or you can bind it to a key by giving the operator "wm.call_menu"
# the parameter "VIEW3D_MT_template" or whaterver you call your menu :)

classes = (
    move_op,
    ivo_subdiv,
    wiretoggle,
    xraytoggle,
    ivo_shade_smooth,
    ivo_reset_transforms,
    ivo_reset_all_transforms,
    ivo_armature_show_all_layers,
    ivo_armature_show_first_layer,
    draw_axis_toggle,
    VIEW3D_MT_ivo
)

def register():
    for cls in classes:
        bpy.types.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.types.unregister_class(cls)

if __name__ == "__main__":
    register()
